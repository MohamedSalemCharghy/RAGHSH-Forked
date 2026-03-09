"""
Hybrid-Suche — Semantische und schlüsselwortbasierte Suche in der Wissensdatenbank.

Kurzbeschreibung
----------------
Durchsucht die Qdrant-Collection 'hsh_knowledge' mit einer kombinierten
Hybrid-Suche: semantische Vektorsuche und Volltextsuche werden mit dem
Reciprocal Rank Fusion (RRF)-Verfahren zusammengeführt. Kann als
eigenständige CLI oder als importiertes Modul vom Chatbot verwendet werden.

Ausführliche Beschreibung
--------------------------
Eine einfache Vektorsuche findet semantisch ähnliche Texte, übersieht aber
exakte Schlüsselwörter (z.B. Modulnummern, Namen). Eine reine Volltextsuche
findet exakte Begriffe, versteht aber keine Bedeutungen. Die Hybrid-Suche
kombiniert beide Verfahren und erreicht so höhere Treffergenauigkeit.

Sucharchitektur:

1. Semantische Suche (Dense Search, Arm 1)
   Die Nutzeranfrage wird mit jinaai/jina-embeddings-v3 vektorisiert
   (task="retrieval.query" — optimiert für Suchanfragen). Der resultierende
   Vektor wird gegen alle gespeicherten Chunk-Vektoren per Cosine-Ähnlichkeit
   verglichen. Qdrant liefert die ähnlichsten CANDIDATE_LIMIT (50) Treffer.

2. Volltextsuche (Full-Text Search, Arm 2)
   Ein Payload-Index auf dem Feld 'text' (Wort-Tokenisierung, ensure_fulltext_index)
   erlaubt eine klassische Stichwortsuche mit MatchText. Qdrant liefert alle
   Dokumente, die das Suchwort enthalten, in der Reihenfolge der internen
   Datenbankreihenfolge.

3. Reciprocal Rank Fusion (RRF)
   Beide Trefferlisten werden mit RRF zusammengeführt. Jedes Ergebnis erhält
   den Score: Σ 1 / (RRF_K + Rang). RRF_K = 60 ist ein bewährter Standardwert.
   Ergebnisse, die in beiden Armen auftauchen, erhalten höhere Scores und
   steigen in der Rangliste auf.

4. Deduplizierung nach Quell-URL
   Da ein langes Dokument (z.B. ein 200-seitiges PDF) in viele Chunks aufgeteilt
   wird, können mehrere Chunks derselben Quelle in den Top-Ergebnissen landen.
   Nach der RRF-Fusion wird daher nur der beste Chunk pro source_url behalten.
   Dies stellt sicher, dass die Top-K Ergebnisse tatsächlich K verschiedene
   Quellen repräsentieren.

Funktionen für den Chatbot-Import:
   perform_hybrid_search(client, embedder, query, top_k)
     → Führt die vollständige Hybrid-Suche durch und gibt eine Liste von
       Ergebnis-Dicts zurück (id, score, payload).

   build_rag_context(results)
     → Wandelt die Suchergebnisse in einen formatierten Kontext-String um,
       der direkt als Eingabe für ein Large Language Model geeignet ist.

Interaktive CLI:
   Wird das Skript direkt ausgeführt, startet eine Eingabeschleife im Terminal.
   Zu jeder Frage werden die Top-3 Treffer mit Score, URL, Abschnittsüberschrift
   und einem 200-Zeichen-Vorschautext ausgegeben.

Konfiguration:
   TOP_K           — Anzahl der angezeigten Ergebnisse (Standard: 3)
   CANDIDATE_LIMIT — Kandidaten pro Sucharm vor der Fusion (Standard: 50)
   RRF_K           — RRF-Konstante (Standard: 60)

Voraussetzungen:
   - Qdrant läuft lokal und die Collection 'hsh_knowledge' ist befüllt
     (Ausgabe von ingest_to_qdrant.py)

Abhängigkeiten: qdrant-client, fastembed
"""

import sys

from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

QDRANT_URL      = "http://localhost:6333"
COLLECTION_NAME = "hsh_knowledge"
EMBED_MODEL     = "jinaai/jina-embeddings-v3"

TOP_K           = 3    # results shown to the user
CANDIDATE_LIMIT = 50   # candidates per arm — needs headroom for deduplication by URL
RRF_K           = 60   # RRF constant (industry default)

# ---------------------------------------------------------------------------
# Index setup
# ---------------------------------------------------------------------------


def ensure_fulltext_index(client: QdrantClient) -> None:
    """Create a word-tokenised full-text index on the 'text' payload field.

    Idempotent — silently ignored if the index already exists.
    """
    try:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="text",
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=50,
                lowercase=True,
            ),
        )
        print("Full-text index on 'text' ensured.")
    except Exception:
        pass   # already exists


# ---------------------------------------------------------------------------
# Core search
# ---------------------------------------------------------------------------


def embed_query(embedder: TextEmbedding, query: str) -> list[float]:
    """Embed a user query using the retrieval.query task for jina-embeddings-v3."""
    return list(embedder.embed([query], task="retrieval.query"))[0].tolist()


def perform_hybrid_search(
    client: QdrantClient,
    embedder: TextEmbedding,
    query: str,
    top_k: int = TOP_K,
) -> list[dict]:
    """Hybrid search via manual Reciprocal Rank Fusion (RRF).

    Two independent search arms:
      1. Dense vector search  — semantic similarity
      2. Full-text search     — exact / partial keyword match

    RRF score = Σ  1 / (RRF_K + rank_i)   for each arm the result appears in.
    This rewards results that rank well in *both* arms.
    """

    # ── Arm 1: Dense search ───────────────────────────────────────────────
    query_vector = embed_query(embedder, query)
    dense_hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=CANDIDATE_LIMIT,
        with_payload=True,
    ).points

    # ── Arm 2: Full-text search ───────────────────────────────────────────
    fts_hits, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="text",
                    match=models.MatchText(text=query),
                )
            ]
        ),
        limit=CANDIDATE_LIMIT,
        with_payload=True,
        with_vectors=False,
    )

    # ── Collect payloads ──────────────────────────────────────────────────
    payloads: dict = {}
    for hit in dense_hits:
        payloads[hit.id] = hit.payload
    for hit in fts_hits:
        payloads[hit.id] = hit.payload

    # ── RRF fusion ────────────────────────────────────────────────────────
    rrf_scores: dict[str, float] = {}
    for rank, hit in enumerate(dense_hits):
        rrf_scores[hit.id] = rrf_scores.get(hit.id, 0.0) + 1.0 / (RRF_K + rank + 1)
    for rank, hit in enumerate(fts_hits):
        rrf_scores[hit.id] = rrf_scores.get(hit.id, 0.0) + 1.0 / (RRF_K + rank + 1)

    # ── Deduplicate: keep only the best-scoring chunk per source URL ──────
    # Multiple chunks from the same document can all rank highly (same PDF
    # split into 50 chunks → top-3 could be chunk #4, #5, #6 of the same file).
    # We scan all candidates in score order and keep the first hit per URL.
    all_sorted = sorted(rrf_scores, key=rrf_scores.__getitem__, reverse=True)

    seen_urls: set[str] = set()
    top_ids: list = []
    for pid in all_sorted:
        source_url = (payloads.get(pid) or {}).get("source_url", str(pid))
        if source_url not in seen_urls:
            seen_urls.add(source_url)
            top_ids.append(pid)
        if len(top_ids) == top_k:
            break

    return [
        {"id": pid, "score": rrf_scores[pid], "payload": payloads[pid]}
        for pid in top_ids
        if pid in payloads
    ]


# ---------------------------------------------------------------------------
# RAG context builder
# ---------------------------------------------------------------------------


def build_rag_context(results: list[dict]) -> str:
    """Assemble top search results into a single context string for LLM input.

    Each block contains URL, optional section heading, and full chunk text,
    separated by a visible delimiter for easy parsing by the LLM.
    """
    blocks = []
    for i, r in enumerate(results, 1):
        p = r["payload"]
        lines = [
            f"[Quelle {i}] {p.get('title', '(kein Titel)')}",
            f"URL: {p.get('source_url', '—')}",
        ]
        if p.get("faculty"):
            lines.append(f"Fakultät: {p['faculty']}")
        if p.get("section_heading"):
            lines.append(f"Abschnitt: {p['section_heading']}")
        lines.append("")
        lines.append(p.get("text", ""))
        blocks.append("\n".join(lines))

    return "\n\n---\n\n".join(blocks)


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------


def print_results(results: list[dict]) -> None:
    """Pretty-print ranked results to the terminal."""
    if not results:
        print("  Keine Treffer gefunden.")
        return

    for i, r in enumerate(results, 1):
        p     = r["payload"]
        score = r["score"]
        url     = p.get("source_url", "—")
        faculty = p.get("faculty", "")
        heading = p.get("section_heading", "")
        preview = p.get("text", "")[:200].replace("\n", " ")

        print(f"\n  ┌─ Treffer {i}  (RRF-Score: {score:.5f})")
        print(f"  │  URL      : {url}")
        if faculty:
            print(f"  │  Fakultät : {faculty}")
        if heading:
            print(f"  │  Abschnitt: {heading}")
        print(f"  │  Vorschau : {preview}…")
        print(f"  └{'─' * 62}")


# ---------------------------------------------------------------------------
# Main / interactive CLI
# ---------------------------------------------------------------------------


def main() -> None:

    # ── Connect ───────────────────────────────────────────────────────────
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=10)
        client.get_collections()
    except Exception as exc:
        print(f"Fehler: Qdrant nicht erreichbar — {exc}")
        print("  → docker compose up -d")
        sys.exit(1)

    # ── Ensure full-text index ────────────────────────────────────────────
    ensure_fulltext_index(client)

    # ── Load embedding model ──────────────────────────────────────────────
    print(f"\nLade Embedding-Modell '{EMBED_MODEL}'…")
    embedder = TextEmbedding(model_name=EMBED_MODEL)
    print("Bereit.  Tippe eine Frage, Enter zum Suchen, Strg+C zum Beenden.\n")

    # ── Interactive loop ──────────────────────────────────────────────────
    while True:
        try:
            query = input("Frage> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAuf Wiedersehen.")
            break

        if not query:
            continue

        results = perform_hybrid_search(client, embedder, query)
        print_results(results)

        # RAG-Kontext bereits verfügbar für den nächsten Schritt (GWDG-API)
        _context = build_rag_context(results)
        # print("\n── RAG-Kontext ──\n", _context)  # zum Debuggen einkommentieren


if __name__ == "__main__":
    main()
