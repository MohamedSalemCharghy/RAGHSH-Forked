"""
HsH-Web-App — Streamlit-Oberfläche für den RAG-Chatbot der Hochschule Hannover.

Aufruf:
    streamlit run hsh_web_app.py

Abhängigkeiten:
    pip install streamlit openai python-dotenv fastembed qdrant-client
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from fastembed import SparseTextEmbedding, TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client import models as qmodels

from hybrid_search import (
    CANDIDATE_LIMIT,
    DENSE_MODEL,
    SPARSE_MODEL,
    build_rag_context,
    embed_query_dense,
    embed_query_sparse,
    perform_hybrid_search,
)

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

load_dotenv(Path(__file__).parent / ".env")

GWDG_API_KEY  = os.getenv("GWDG_API_KEY", "")
GWDG_API_BASE = os.getenv("GWDG_API_BASE", "https://chat-ai.academiccloud.de/v1")
QDRANT_URL    = "http://localhost:6333"
COLLECTION    = "hsh_knowledge"
RAG_TOP_K     = 6
TEMPERATURE   = 0.0

ROLLEN = ["Studierender", "Mitarbeitender", "Lehrender", "Besucher"]

FAKULTAETEN = [
    "Alle Fakultäten",
    "Fakultät I",
    "Fakultät II",
    "Fakultät III",
    "Fakultät IV",
    "Fakultät V",
]

ROLLEN_HINWEIS = {
    "Studierender":   "Du sprichst mit einem Studierenden. Verwende klare, zugängliche Sprache und erkläre Fachbegriffe.",
    "Mitarbeitender": "Du sprichst mit einem Mitarbeitenden. Antworte fachlich präzise.",
    "Lehrender":      "Du sprichst mit einer lehrenden Person. Antworte auf akademischem Niveau.",
    "Besucher":       "Du sprichst mit einer interessierten Person. Erkläre allgemeinverständlich.",
}

# ---------------------------------------------------------------------------
# Seitenconfig — muss vor allen anderen st.*-Aufrufen stehen
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="HsH-Assistent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Gecachte Ressourcen — analog zu hsh_chatbot.py, nur einmal geladen
# ---------------------------------------------------------------------------


@st.cache_resource(show_spinner="Verbinde mit Qdrant …")
def get_qdrant_client() -> QdrantClient:
    client = QdrantClient(url=QDRANT_URL, timeout=10)
    client.get_collections()
    return client


@st.cache_resource(show_spinner="Lade Dense-Embedding-Modell …")
def get_dense_embedder() -> TextEmbedding:
    return TextEmbedding(model_name=DENSE_MODEL)


@st.cache_resource(show_spinner="Lade Sparse-Embedding-Modell (BM25) …")
def get_sparse_embedder() -> SparseTextEmbedding:
    return SparseTextEmbedding(model_name=SPARSE_MODEL)


@st.cache_resource(show_spinner="Lade Reranker-Modell …")
def get_reranker():
    from hybrid_search import RERANKER_MODEL, USE_RERANKER
    if not USE_RERANKER:
        return None
    try:
        from fastembed import TextCrossEncoder
        return TextCrossEncoder(model_name=RERANKER_MODEL)
    except Exception:
        return None


@st.cache_resource(show_spinner="Verbinde mit GWDG-API …")
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=GWDG_API_KEY, base_url=GWDG_API_BASE, timeout=30)


@st.cache_resource(show_spinner="Lade Modellliste …")
def get_model_list() -> list[str]:
    """Ruft die Modellliste ab — identisch mit hsh_chatbot.get_available_models()."""
    client = get_openai_client()
    try:
        return sorted(m.id for m in client.models.list().data)
    except Exception:
        return ["meta-llama-3.1-8b-instruct", "gpt-4o-mini", "gpt-4o"]


# ---------------------------------------------------------------------------
# System-Prompt (rollenadaptiv) — analog zu SYSTEM_PROMPT in hsh_chatbot.py
# ---------------------------------------------------------------------------


def build_system_prompt(rolle: str, fakultaet: str) -> str:
    rollen_hinweis = ROLLEN_HINWEIS.get(rolle, "")
    if fakultaet != "Alle Fakultäten":
        fak_hinweis = (f"Der Nutzer gehört der {fakultaet} an. "
                       "Nimm ausschließlich Informationen dieser Fakultät und sortiere alles andere aus. Nenne immer den Kontext der Information.")
    else:
        fak_hinweis = ("Der Nutzer hat keine Fakultät gewählt. "
                       "Weise immer auf unterschiedliche Regelungen je Fakultät hin, wenn relevant.")
    return f"""\
Du bist der offizielle Assistent der Hochschule Hannover (HsH).

Nutzer-Profil:
- Rolle: {rolle} — {rollen_hinweis}
- {fak_hinweis}

Regeln:
1. Antworte AUSSCHLIESSLICH auf Basis des bereitgestellten Kontextes.
2. Erfinde keine Informationen und spekuliere nicht.
3. Falls die Antwort im Kontext nicht enthalten ist, antworte wörtlich:
   "Dazu liegen mir keine Informationen aus den offiziellen Dokumenten der HsH vor."
4. Wenn sich Quellenangaben widersprechen, weise explizit darauf hin.
5. Wenn eine Quelle ein älteres Datum trägt (erkennbar am "Stand:"-Feld im Kontext),
   empfehle dem Nutzer, die Angabe direkt auf der offiziellen Website zu verifizieren.
6. Schreibe klar, präzise und auf Deutsch.
7. Nenne am Ende jeder Antwort die verwendeten Quellen im Format:
   **Quellen:**
   - <Titel> — <URL> — Abschnitt: <Abschnitt> (Stand: <Datum>)
"""


# ---------------------------------------------------------------------------
# Suche mit optionalem Fakultätsfilter
# ---------------------------------------------------------------------------


def search(
    qdrant: QdrantClient,
    dense_embedder: TextEmbedding,
    sparse_embedder: SparseTextEmbedding,
    query: str,
    fakultaet: str,
    reranker=None,
) -> list[dict]:
    """Hybrid-Suche (Prefetch+RRF) mit optionalem Fakultätsfilter.

    Filterlogik bei gewählter Fakultät:
      faculty == gewählte_Fakultät  OR  faculty == ""
    Dokumente ohne Fakultätszugehörigkeit (zentrale Einrichtungen, Bibliothek
    etc.) werden immer einbezogen und nicht herausgefiltert.
    """

    faculty_filter = None
    if fakultaet != "Alle Fakultäten":
        # ODER-Verknüpfung: gewählte Fakultät ODER keine Fakultät (zentral)
        faculty_filter = qmodels.Filter(
            should=[
                qmodels.FieldCondition(
                    key="faculty",
                    match=qmodels.MatchValue(value=fakultaet),
                ),
                qmodels.FieldCondition(
                    key="faculty",
                    match=qmodels.MatchValue(value=""),
                ),
            ],
        )

    return perform_hybrid_search(
        qdrant,
        dense_embedder,
        sparse_embedder,
        query,
        top_k=RAG_TOP_K,
        query_filter=faculty_filter,
        reranker=reranker,
    )


# ---------------------------------------------------------------------------
# Streaming — analog zu ask_llm() in hsh_chatbot.py, aber mit write_stream
# ---------------------------------------------------------------------------


def stream_response(openai_client: OpenAI, model: str, messages: list[dict]) -> str:
    """Streamt Denkprozess und Antwort in einem einzigen API-Aufruf.

    Unterstützt zwei Varianten der Reasoning-Ausgabe:
      1. Separates Feld  delta.reasoning_content  (ältere DeepSeek-API)
      2. Inline-Tags     <think>…</think>          in delta.content
         (neuere Modelle, z.B. DeepSeek R1 via GWDG)

    Layout:
      ▶ 💭 Denkprozess   ← st.expander, zugeklappt bis Nutzer klickt
      ──────────────────
        Antworttext      ← live Token für Token
    """
    thinking_expander    = st.expander("💭 Denkprozess", expanded=False)
    thinking_placeholder = thinking_expander.empty()
    answer_placeholder   = st.empty()

    reasoning_parts: list[str] = []
    answer_parts:    list[str] = []

    # Zustandsautomat für <think>-Tag-Parsing
    in_think = False   # befinden wir uns gerade innerhalb von <think>…</think>?
    buffer   = ""      # sammelt angebrochene Tag-Grenzen über Chunk-Grenzen

    stream = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=TEMPERATURE,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta if chunk.choices else None
        if not delta:
            continue

        # ── Variante 1: separates reasoning_content-Feld ─────────────────
        r = getattr(delta, "reasoning_content", None)
        if r:
            reasoning_parts.append(r)
            thinking_placeholder.markdown("".join(reasoning_parts))
            continue

        # ── Variante 2: <think>…</think> inline im content ────────────────
        token = delta.content or ""
        if not token:
            continue

        buffer += token

        # Verarbeite den Buffer zeichenweise soweit möglich
        while buffer:
            if in_think:
                end = buffer.find("</think>")
                if end == -1:
                    # Kompletter Rest ist noch Reasoning; letzten 8 Zeichen puffern
                    # (könnten Anfang von </think> sein)
                    safe = max(0, len(buffer) - 8)
                    reasoning_parts.append(buffer[:safe])
                    buffer = buffer[safe:]
                    break
                else:
                    reasoning_parts.append(buffer[:end])
                    buffer  = buffer[end + len("</think>"):]
                    in_think = False
            else:
                start = buffer.find("<think>")
                if start == -1:
                    # Kein Tag im Buffer — alles ist Antworttext; letzten 7 Zeichen puffern
                    safe = max(0, len(buffer) - 7)
                    answer_parts.append(buffer[:safe])
                    buffer = buffer[safe:]
                    break
                else:
                    # Text vor dem Tag
                    if start > 0:
                        answer_parts.append(buffer[:start])
                    buffer  = buffer[start + len("<think>"):]
                    in_think = True

        # UI aktualisieren
        if reasoning_parts:
            thinking_placeholder.markdown("".join(reasoning_parts))
        if answer_parts:
            answer_placeholder.markdown("".join(answer_parts))

    # Restlichen Buffer leeren
    if buffer:
        if in_think:
            reasoning_parts.append(buffer)
        else:
            answer_parts.append(buffer)

    # Letztes UI-Update
    if reasoning_parts:
        thinking_placeholder.markdown("".join(reasoning_parts))
    if answer_parts:
        answer_placeholder.markdown("".join(answer_parts))

    # Expander ausblenden wenn kein Reasoning vorhanden
    if not reasoning_parts:
        thinking_expander.empty()

    return "".join(answer_parts)


# ---------------------------------------------------------------------------
# Quellen-Anzeige
# ---------------------------------------------------------------------------


def render_sources(results: list[dict]) -> None:
    if not results:
        return
    with st.expander("Verwendete Quellen", expanded=True):
        for i, r in enumerate(results, 1):
            p = r["payload"]
            title   = p.get("title", "(kein Titel)")
            url     = p.get("source_url", "")
            heading = p.get("section_heading", "")
            faculty = p.get("faculty", "")

            st.markdown(f"**{i}. {title}**")
            if url:
                st.markdown(f"[{url}]({url})")
            meta_parts = []
            if heading:
                meta_parts.append(f"Abschnitt: {heading}")
            if faculty:
                meta_parts.append(f"Fakultät: {faculty}")
            meta_parts.append(f"RRF-Score: {r['score']:.4f}")
            st.caption("  ·  ".join(meta_parts))

            if i < len(results):
                st.divider()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar(modelle: list[str]) -> tuple[str, str, str]:
    with st.sidebar:
        st.markdown("## ⚙️ Einstellungen")

        st.markdown("### Mein Profil")
        rolle = st.radio("Ich bin …", ROLLEN, index=0)
        fakultaet = st.selectbox("Fakultät", FAKULTAETEN, index=0)

        st.markdown("### Modell")
        modell = st.selectbox("GWDG-Modell", modelle, index=0)

        st.divider()
        st.info(
            "**HsH-KI-Assistent**\n\n"
            "Beantwortet Fragen ausschließlich auf Basis offizieller "
            "HsH-Dokumente. Keine Terminvereinbarung, keine Formulare.\n\n"
            "Betrieben mit GWDG ChatAI & lokalem Qdrant-Index."
        )

        if st.button("Chat zurücksetzen", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    return rolle, fakultaet, modell


# ---------------------------------------------------------------------------
# Haupt-App
# ---------------------------------------------------------------------------


def main() -> None:
    # ── Pflichtprüfungen ──────────────────────────────────────────────────
    if not GWDG_API_KEY:
        st.error("GWDG_API_KEY fehlt. Bitte `.env`-Datei prüfen.")
        st.stop()

    try:
        qdrant = get_qdrant_client()
    except Exception as exc:
        st.error(f"Qdrant nicht erreichbar: {exc}\n\n`docker compose up -d` ausführen.")
        st.stop()

    dense_embedder  = get_dense_embedder()
    sparse_embedder = get_sparse_embedder()
    reranker        = get_reranker()
    openai_client   = get_openai_client()
    modelle         = get_model_list()

    # ── Sidebar ───────────────────────────────────────────────────────────
    rolle, fakultaet, modell = render_sidebar(modelle)

    # ── Titel ─────────────────────────────────────────────────────────────
    st.title("🎓 HsH-Assistent")
    st.caption(f"Modell: **{modell}** · Rolle: **{rolle}** · Fakultät: **{fakultaet}**")

    # ── Chat-Verlauf ──────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                render_sources(msg["sources"])

    # ── Nutzereingabe ─────────────────────────────────────────────────────
    question = st.chat_input("Stellen Sie Ihre Frage zur Hochschule Hannover …")
    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # ── RAG: Suche + Kontext ──────────────────────────────────────────────
    with st.spinner("Suche in der Wissensdatenbank …"):
        results = search(qdrant, dense_embedder, sparse_embedder, question, fakultaet, reranker)

    if not results:
        with st.chat_message("assistant"):
            st.warning("Keine passenden Dokumente in der Wissensdatenbank gefunden.")
        return

    context = build_rag_context(results)

    # Veralterungswarnung: älteste Quelle älter als 180 Tage?
    from datetime import date, timedelta
    system_prompt = build_system_prompt(rolle, fakultaet)
    dates = [r["payload"].get("crawl_date", "") for r in results if r.get("payload")]
    valid_dates = [d for d in dates if d]
    if valid_dates:
        oldest = min(valid_dates)
        try:
            if (date.today() - date.fromisoformat(oldest)) > timedelta(days=180):
                system_prompt += (
                    "\nHinweis: Mindestens eine der verwendeten Quellen ist älter als 6 Monate. "
                    "Weise den Nutzer darauf hin, zeitkritische Informationen direkt auf "
                    "der offiziellen HsH-Website zu verifizieren."
                )
        except ValueError:
            pass

    llm_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": (
            f"Kontext aus den offiziellen HsH-Dokumenten:\n\n"
            f"{context}\n\n---\n\nFrage: {question}"
        )},
    ]

    # ── Streaming-Antwort ─────────────────────────────────────────────────
    with st.chat_message("assistant"):
        try:
            answer = stream_response(openai_client, modell, llm_messages)
        except Exception as exc:
            st.error(f"Fehler bei der API-Anfrage: {exc}")
            return
        render_sources(results)

    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": results,
    })


if __name__ == "__main__":
    main()
