"""
HsH-Chatbot — KI-gestützter Auskunfts-Assistent der Hochschule Hannover.

Kurzbeschreibung
----------------
Interaktiver Chatbot, der Fragen zur Hochschule Hannover ausschließlich auf
Basis offizieller Dokumente beantwortet. Kombiniert die lokale Hybrid-Suche
(hybrid_search.py) mit einem großen Sprachmodell der GWDG ChatAI API zu einer
vollständigen RAG-Pipeline (Retrieval-Augmented Generation).

Ausführliche Beschreibung
--------------------------
Herkömmliche Chatbots halluzinieren — sie erfinden Antworten, die plausibel
klingen, aber falsch sind. Das ist bei offiziellen Informationen (Prüfungs-
ordnungen, Bewerbungsfristen, Modulhandbücher) inakzeptabel. Dieser Chatbot
löst das Problem durch die RAG-Architektur: Das LLM erhält nicht nur die Frage,
sondern auch relevante Textstellen aus den offiziellen Dokumenten als Kontext.

Verarbeitungsablauf pro Nutzeranfrage:

  Nutzerfrage
      │
      ▼
  1. Hybrid-Suche in Qdrant
     perform_hybrid_search() aus hybrid_search.py sucht die 4 relevantesten
     Textabschnitte (RAG_TOP_K=4) aus der Wissensdatenbank. Die Suche kombiniert
     semantische Vektorsuche mit Volltextsuche (RRF-Fusion, URL-Deduplizierung).
      │
      ▼
  2. Kontext aufbauen
     build_rag_context() formatiert die Treffer als lesbaren Text mit Quellenangaben
     (Titel, URL, Abschnittsüberschrift, Fakultät).
      │
      ▼
  3. Prompt zusammenstellen
     build_rag_messages() erstellt die Messages-Liste für die Chat-API:
     - system: Persona und strikte Regeln (nur aus Kontext antworten, Quellen nennen)
     - user: Kontext-Block + eigentliche Frage
      │
      ▼
  4. LLM-Anfrage an GWDG ChatAI
     ask_llm() sendet den Prompt an das gewählte Modell (OpenAI-kompatibler Client,
     Base-URL: https://chat-ai.academiccloud.de/v1). Temperature=0.0 eliminiert
     kreative Freiheiten für maximale Faktenreue.
      │
      ▼
  5. Ausgabe
     - [Thinking]-Block (nur bei Reasoning-Modellen wie DeepSeek R1)
     - Antworttext des Modells
     - Liste der verwendeten Quellen mit RRF-Score

Besonderheiten:

  Debug-Modus (DEBUG_PROMPT = True):
    Zeigt den vollständigen an das LLM gesendeten Prompt vor jeder Antwort an.
    Unentbehrlich beim Testen und Optimieren des System-Prompts. Mit
    DEBUG_PROMPT = False deaktivieren für den Produktionsbetrieb.

  Dynamische Modellauswahl:
    Beim Start werden alle verfügbaren Modelle von der GWDG-API abgefragt und
    nummeriert angezeigt. Der Nutzer wählt per Eingabe das gewünschte Modell.
    So können verschiedene Modelle (GPT-4, Llama, DeepSeek R1 etc.) ohne
    Code-Änderung getestet werden.

  Reasoning-Unterstützung:
    Manche Modelle (z.B. DeepSeek R1) liefern neben der Antwort auch einen
    internen Denkprozess (reasoning_content). Dieser wird separat in einem
    [Thinking]-Block ausgegeben.

Konfiguration:
   GWDG_API_KEY    — API-Schlüssel (aus .env-Datei, nicht im Code!)
   GWDG_API_BASE   — Basis-URL der GWDG ChatAI API
   RAG_TOP_K       — Anzahl der Kontext-Dokumente pro Anfrage (Standard: 4)
   TEMPERATURE     — Kreativität des LLM (0.0 = deterministisch/faktengetreu)
   DEBUG_PROMPT    — Vollständigen Prompt ausgeben (True/False)

Einrichtung:
   cp .env.example .env
   # GWDG_API_KEY in .env eintragen
   python hsh_chatbot.py

Abhängigkeiten: openai, python-dotenv, fastembed, qdrant-client
   sowie hybrid_search.py (lokales Modul)
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastembed import SparseTextEmbedding, TextEmbedding
from openai import OpenAI, APIConnectionError, AuthenticationError
from qdrant_client import QdrantClient

# Eigene Module
from hybrid_search import build_rag_context, create_reranker, perform_hybrid_search

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

# .env aus dem Skript-Verzeichnis laden (überschreibt keine gesetzten Env-Vars)
load_dotenv(Path(__file__).parent / ".env")

GWDG_API_KEY  = os.getenv("GWDG_API_KEY", "")
GWDG_API_BASE = os.getenv("GWDG_API_BASE", "https://chat-ai.academiccloud.de/v1")

QDRANT_URL      = "http://localhost:6333"
EMBED_MODEL     = "jinaai/jina-embeddings-v3"
SPARSE_MODEL    = "Qdrant/bm25"
RAG_TOP_K       = 4      # Treffer für den Kontext
TEMPERATURE     = 0.0    # Maximale Faktenreue
DEBUG_PROMPT    = True   # Zeigt den vollständigen LLM-Prompt vor jeder Anfrage

SYSTEM_PROMPT = """\
Du bist der offizielle Assistent der Hochschule Hannover (HsH).

Regeln:
- Antworte AUSSCHLIESSLICH auf Basis des bereitgestellten Kontextes.
- Erfinde keine Informationen und spekuliere nicht.
- Falls die Antwort im Kontext nicht enthalten ist, antworte wörtlich:
  "Dazu liegen mir keine Informationen aus den offiziellen Dokumenten der HsH vor."
- Schreibe klar, präzise und auf Deutsch. Die verschiedenen Fakultäten der 
Hochschule Hannover haben unterschiedliche Regelungen, daher ist es wichtig, 
die Antwort so spezifisch wie möglich zu formulieren. Wenn die Fakultät nicht eindeutig 
aus dem Kontext hervorgeht und dies wichtig wäre, gib dies in der Antwort an.

- Nenne am Ende jeder Antwort die verwendeten Quellen im Format:
    Quellen:
    - <Titel> | <URL> | <Abschnitt>
"""

# ---------------------------------------------------------------------------
# GWDG / OpenAI API
# ---------------------------------------------------------------------------


def build_client() -> OpenAI:
    """Erstellt und validiert den OpenAI-kompatiblen GWDG-Client."""
    if not GWDG_API_KEY:
        print("Fehler: GWDG_API_KEY fehlt.")
        print("  → Kopiere .env.example nach .env und trage deinen Key ein.")
        sys.exit(1)
    return OpenAI(api_key=GWDG_API_KEY, base_url=GWDG_API_BASE)


def get_available_models(client: OpenAI) -> list[str]:
    """Fragt die Modellliste vom GWDG-Server ab."""
    try:
        return [m.id for m in client.models.list().data]
    except AuthenticationError:
        print("Fehler: API-Key ungültig oder abgelaufen.")
        sys.exit(1)
    except APIConnectionError as exc:
        print(f"Fehler: GWDG-API nicht erreichbar — {exc}")
        sys.exit(1)


def select_model(client: OpenAI) -> str:
    """Zeigt verfügbare Modelle und lässt den Nutzer auswählen."""
    print("Rufe Modellliste von der GWDG-API ab…\n")
    models = get_available_models(client)

    if not models:
        print("Keine Modelle gefunden.")
        sys.exit(1)

    for i, model_id in enumerate(models, 1):
        print(f"  [{i:2}] {model_id}")

    print()
    try:
        choice = int(input(f"Modell wählen (1–{len(models)}): "))
        selected = models[choice - 1]
    except (ValueError, IndexError):
        print("Ungültige Eingabe — erstes Modell wird verwendet.")
        selected = models[0]

    print(f"\n  → Aktiv: {selected}\n")
    return selected


def ask_llm(
    client: OpenAI,
    model: str,
    messages: list[dict],
) -> tuple[str, str]:
    """Sendet eine Anfrage an das GWDG-Modell.

    Gibt (antwort, denkprozess) zurück.
    Bei Modellen ohne reasoning_content ist denkprozess ein leerer String.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=TEMPERATURE,
    )
    msg = response.choices[0].message
    reasoning = getattr(msg, "reasoning_content", "") or ""
    answer    = msg.content or ""
    return answer, reasoning


# ---------------------------------------------------------------------------
# RAG-Pipeline
# ---------------------------------------------------------------------------


def build_rag_messages(question: str, context: str) -> list[dict]:
    """Erstellt die Messages-Liste für die Chat-Completion-API."""
    user_content = (
        f"Kontext aus den offiziellen HsH-Dokumenten:\n\n"
        f"{context}\n\n"
        f"---\n\n"
        f"Frage: {question}"
    )
    return [
        {"role": "system",  "content": SYSTEM_PROMPT},
        {"role": "user",    "content": user_content},
    ]


def format_sources(results: list[dict]) -> str:
    """Kompakte Quellenzeilen aus den Qdrant-Treffern."""
    lines = []
    for r in results:
        p       = r["payload"]
        url     = p.get("source_url", "—")
        title   = p.get("title", "—")
        heading = p.get("section_heading", "")
        line    = f"  • {title} | {url}"
        if heading:
            line += f" | {heading}"
        lines.append(line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Ausgabe-Helfer
# ---------------------------------------------------------------------------

SEP = "─" * 70


def print_thinking(reasoning: str) -> None:
    if not reasoning:
        return
    print(f"\n[Thinking]\n{SEP}")
    print(reasoning.strip())
    print(SEP)


def print_answer(answer: str, model: str) -> None:
    print(f"\n[{model}]\n{SEP}")
    print(answer.strip())
    print(SEP)


def print_llm_input(messages: list[dict]) -> None:
    """Gibt den vollständigen Prompt übersichtlich auf der Konsole aus."""
    if not DEBUG_PROMPT:
        return
    DBG = "░" * 70
    print(f"\n{DBG}")
    print("  DEBUG — An das LLM gesendete Messages")
    print(DBG)
    for msg in messages:
        role    = msg["role"].upper()
        content = msg["content"]
        print(f"\n  ┌─ [{role}]")
        for line in content.splitlines():
            print(f"  │  {line}")
        print(f"  └{'─' * 68}")
    print(f"{DBG}\n")


def print_retrieved_sources(results: list[dict]) -> None:
    print(f"\n[Verwendete Quellen  (RRF-Score)]")
    for r in results:
        p    = r["payload"]
        url  = p.get("source_url", "—")
        head = p.get("section_heading", "")
        print(f"  {r['score']:.5f}  {url}" + (f"  [{head}]" if head else ""))


# ---------------------------------------------------------------------------
# Chat-Schleife
# ---------------------------------------------------------------------------


def chat_loop(
    gwdg_client: OpenAI,
    model: str,
    qdrant_client: QdrantClient,
    embedder: TextEmbedding,
    sparse_embedder: SparseTextEmbedding,
    reranker=None,
) -> None:
    """Interaktive RAG-Chat-Schleife."""
    print(f"HsH-Chatbot bereit.  Strg+C oder 'exit' zum Beenden.\n")

    while True:
        # ── Eingabe ───────────────────────────────────────────────────────
        try:
            question = input("Frage> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAuf Wiedersehen.")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit", "q"}:
            print("Auf Wiedersehen.")
            break

        # ── RAG: Suche + Kontext ──────────────────────────────────────────
        results = perform_hybrid_search(
            qdrant_client, embedder, sparse_embedder, question, top_k=RAG_TOP_K, reranker=reranker
        )

        if not results:
            print("\nKeine passenden Dokumente in der Wissensdatenbank gefunden.\n")
            continue

        context  = build_rag_context(results)
        messages = build_rag_messages(question, context)

        # ── Debug-Ausgabe des Prompts ─────────────────────────────────────
        print_llm_input(messages)

        # ── LLM-Anfrage ───────────────────────────────────────────────────
        try:
            answer, reasoning = ask_llm(gwdg_client, model, messages)
        except Exception as exc:
            print(f"\nFehler bei der API-Anfrage: {exc}\n")
            continue

        # ── Ausgabe ───────────────────────────────────────────────────────
        print_thinking(reasoning)
        print_answer(answer, model)
        print_retrieved_sources(results)
        print()


# ---------------------------------------------------------------------------
# Einstiegspunkt
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("  HsH-Chatbot  —  RAG + GWDG ChatAI")
    print("=" * 70 + "\n")

    # ── GWDG-Client + Modellauswahl ───────────────────────────────────────
    gwdg_client = build_client()
    model       = select_model(gwdg_client)

    # ── Qdrant verbinden ──────────────────────────────────────────────────
    try:
        qdrant_client = QdrantClient(url=QDRANT_URL, timeout=10)
        qdrant_client.get_collections()
    except Exception as exc:
        print(f"Fehler: Qdrant nicht erreichbar — {exc}")
        print("  → docker compose up -d")
        sys.exit(1)

    # ── Embedding-Modell laden ────────────────────────────────────────────
    print(f"Lade Embedding-Modell '{EMBED_MODEL}'…")
    embedder = TextEmbedding(model_name=EMBED_MODEL)

    print(f"Lade Sparse-Modell '{SPARSE_MODEL}'…")
    sparse_embedder = SparseTextEmbedding(model_name=SPARSE_MODEL)

    reranker = None
    try:
        print("Lade Reranker…")
        reranker = create_reranker()
    except Exception as exc:
        print(f"Reranker nicht verfügbar — weiter ohne Reranking: {exc}")

    print("Modelle geladen.\n")

    # ── Chat starten ──────────────────────────────────────────────────────
    chat_loop(gwdg_client, model, qdrant_client, embedder, sparse_embedder, reranker=reranker)


if __name__ == "__main__":
    main()
