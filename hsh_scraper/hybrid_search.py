"""
Hybrid-Suche — Semantische und schlüsselwortbasierte Suche in der Wissensdatenbank.

Kurzbeschreibung
----------------
Durchsucht die Qdrant-Collection 'hsh_knowledge' mit einer kombinierten
Hybrid-Suche: Dense Vektorsuche (Jina) und BM25 Sparse Vektorsuche werden
per Qdrant-nativer Prefetch+RRF-Fusion zusammengeführt. Kann als
eigenständige CLI oder als importiertes Modul vom Chatbot verwendet werden.

Ausführliche Beschreibung
--------------------------
Eine einfache Vektorsuche findet semantisch ähnliche Texte, übersieht aber
exakte Schlüsselwörter (z.B. Modulnummern, Namen). Eine reine Keyword-Suche
findet exakte Begriffe, versteht aber keine Bedeutungen. Die Hybrid-Suche
kombiniert beide Verfahren und erreicht so höhere Treffergenauigkeit.

Sucharchitektur:

1. Semantische Suche (Dense Search, Arm 1)
   Die Nutzeranfrage wird mit jinaai/jina-embeddings-v3 vektorisiert
   (task="retrieval.query"). Qdrant vergleicht den Vektor gegen den
   benannten Vektor "dense" und liefert die CANDIDATE_LIMIT ähnlichsten Treffer.

2. BM25 Sparse Search (Arm 2)
   Die Anfrage wird mit SparseTextEmbedding("Qdrant/bm25") in einen
   Sparse-Vektor umgewandelt. Qdrant vergleicht diesen gegen den
   benannten Vektor "sparse" — echte Relevanz-Scores, nicht Storage-Reihenfolge.

3. Qdrant-native RRF-Fusion (Prefetch + FusionQuery)
   Beide Arme laufen als Prefetch in einem einzigen query_points()-Aufruf.
   Qdrant führt die Reciprocal Rank Fusion intern durch — kein Python-RRF-Code.
   FusionQuery(RRF) belohnt Treffer, die in beiden Armen gut ranken.

4. Deduplizierung nach Quell-URL (max_per_url=2)
   Nach der Fusion: maximal MAX_PER_URL Chunks pro source_url werden behalten.
   Dies verhindert, dass viele Chunks desselben Dokuments alle Top-Plätze
   belegen, erlaubt aber einen zweiten relevanten Absatz pro Quelle.

5. Semantisches Reranking (Cross-Encoder)
   Nach URL-Dedup werden die Treffer mit jinaai/jina-reranker-v2-base-multilingual
   nach echter semantischer Relevanz neu bewertet und sortiert. Der Cross-Encoder
   bewertet (Query, Passage)-Paare — deutlich präziser als reine Vektornähe.
   Aktivierbar via USE_RERANKER, deaktivierbar falls Modell nicht verfügbar.

6. Context Augmentation (Nachbar-Chunks, Top-N)
   Für die AUGMENT_TOP_N am höchsten gerankten Treffer werden die unmittelbar
   benachbarten Chunks (chunk_index - 1 und chunk_index + 1) derselben source_url
   nachgeladen. Dies verhindert, dass Informationen an Chunk-Grenzen zerrissen werden.
   Nachbar-Chunks werden dem Kontext vorangestellt/angehängt, aber nicht
   als eigenständige Top-Treffer gezählt.

Konfiguration:
   TOP_K           — Anzahl der finalen Ergebnisse (Standard: 8)
   CANDIDATE_LIMIT — Kandidaten pro Sucharm (Standard: 100)
   DEDUP_BUFFER    — Faktor für Überabtastung vor URL-Dedup (Standard: 4)
   MAX_PER_URL     — Max. Chunks pro source_url nach Dedup (Standard: 2)
   USE_RERANKER    — Semantisches Reranking aktivieren (Standard: True)
   AUGMENT_TOP_N   — Für wie viele Top-Treffer Nachbar-Chunks geladen werden (Standard: 3)

Voraussetzungen:
   - Qdrant läuft lokal, Collection 'hsh_knowledge' befüllt mit Dense+Sparse
     (Ausgabe von hpc_vectorizer.py + local_importer.py)

Abhängigkeiten: qdrant-client, fastembed
"""

import sys

from fastembed import SparseTextEmbedding, TextEmbedding
from qdrant_client import QdrantClient, models

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

QDRANT_URL      = "http://localhost:6333"
COLLECTION_NAME = "hsh_knowledge"
DENSE_MODEL     = "jinaai/jina-embeddings-v3"
SPARSE_MODEL    = "Qdrant/bm25"
RERANKER_MODEL  = "jinaai/jina-reranker-v2-base-multilingual"

# URLs die in Suchergebnissen nicht angezeigt werden sollen
BLOCKED_URL_PREFIXES = (
    "https://serwiss.bib.",
    "http://serwiss.bib.",
)

TOP_K           = 8    # finale Ergebnisse nach URL-Dedup
CANDIDATE_LIMIT = 100  # Kandidaten pro Sucharm (Prefetch limit)
DEDUP_BUFFER    = 4    # TOP_K * DEDUP_BUFFER = Ergebnisse von Qdrant vor Dedup
MAX_PER_URL     = 2    # max. Chunks pro source_url nach Dedup
USE_RERANKER    = True # Cross-Encoder Reranking nach URL-Dedup
AUGMENT_TOP_N   = 3    # Nachbar-Chunks nur für die Top-N Treffer laden

# ---------------------------------------------------------------------------
# Embedding-Hilfsfunktionen
# ---------------------------------------------------------------------------


def embed_query_dense(embedder: TextEmbedding, query: str) -> list[float]:
    """Dense-Embedding für eine Suchanfrage (task=retrieval.query)."""
    return list(embedder.embed([query], task="retrieval.query"))[0].tolist()


def embed_query_sparse(embedder: SparseTextEmbedding, query: str) -> models.SparseVector:
    """BM25-Sparse-Embedding für eine Suchanfrage."""
    result = list(embedder.embed([query]))[0]
    return models.SparseVector(
        indices=result.indices.tolist(),
        values=result.values.tolist(),
    )


# ---------------------------------------------------------------------------
# Core search
# ---------------------------------------------------------------------------


def _fetch_neighbor_chunk(
    client: QdrantClient,
    source_url: str,
    chunk_index: int,
) -> dict | None:
    """Lädt einen einzelnen Nachbar-Chunk (chunk_index) einer source_url aus Qdrant.

    Gibt das Payload-Dict zurück oder None wenn kein Treffer.
    """
    hits, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="source_url",
                    match=models.MatchValue(value=source_url),
                ),
                models.FieldCondition(
                    key="chunk_index",
                    match=models.MatchValue(value=chunk_index),
                ),
            ]
        ),
        limit=1,
        with_payload=True,
        with_vectors=False,
    )
    return hits[0].payload if hits else None


def create_reranker():
    """Erzeugt den Cross-Encoder-Reranker mit Import-Fallback."""
    if not USE_RERANKER:
        return None
    try:
        try:
            from fastembed import TextCrossEncoder
        except ImportError:
            from fastembed.rerank.cross_encoder import TextCrossEncoder
        return TextCrossEncoder(model_name=RERANKER_MODEL)
    except Exception:
        raise


def perform_hybrid_search(
    client: QdrantClient,
    dense_embedder: TextEmbedding,
    sparse_embedder: SparseTextEmbedding,
    query: str,
    top_k: int = TOP_K,
    query_filter: models.Filter | None = None,
    reranker=None,
) -> list[dict]:
    """Hybrid-Suche via Qdrant-nativem Prefetch + RRF-Fusion.

    Beide Sucharme (Dense + Sparse) laufen in einem einzigen Qdrant-Aufruf.
    Die RRF-Fusion erfolgt serverseitig — kein Python-RRF-Code nötig.
    Nach der Fusion:
      1. URL-Dedup: max. MAX_PER_URL Chunks pro source_url.
      2. Semantisches Reranking via Cross-Encoder (wenn reranker übergeben).
      3. Context Augmentation: für die AUGMENT_TOP_N besten Treffer werden
         Nachbar-Chunks (chunk_index ± 1) nachgeladen und dem Payload angehängt.
    """
    dense_vec  = embed_query_dense(dense_embedder, query)
    sparse_vec = embed_query_sparse(sparse_embedder, query)

    # ── Qdrant-native Prefetch + RRF ──────────────────────────────────────
    raw_results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[
            models.Prefetch(
                query=dense_vec,
                using="dense",
                limit=CANDIDATE_LIMIT,
                filter=query_filter,
            ),
            models.Prefetch(
                query=sparse_vec,
                using="sparse",
                limit=CANDIDATE_LIMIT,
                filter=query_filter,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=top_k * DEDUP_BUFFER,
        with_payload=True,
    ).points

    # ── Geblockte URLs herausfiltern ───────────────────────────────────────
    raw_results = [
        h for h in raw_results
        if not (h.payload or {}).get("source_url", "").startswith(BLOCKED_URL_PREFIXES)
    ]

    # ── URL-Dedup: max. MAX_PER_URL Chunks pro source_url ─────────────────
    url_counts: dict[str, int] = {}
    results: list[dict] = []

    for hit in raw_results:
        source_url = (hit.payload or {}).get("source_url", str(hit.id))
        count = url_counts.get(source_url, 0)
        if count < MAX_PER_URL:
            url_counts[source_url] = count + 1
            results.append({
                "id":      hit.id,
                "score":   hit.score,
                "payload": hit.payload,
            })
        if len(results) == top_k:
            break

    # ── Semantisches Reranking via Cross-Encoder ───────────────────────────
    if reranker is not None and results:
        passages = [r["payload"].get("text", "") for r in results]
        scores = list(reranker.rerank(query, passages))
        results = [r for _, r in sorted(zip(scores, results), key=lambda x: x[0], reverse=True)]

    # ── Context Augmentation: Nachbar-Chunks für Top-N nachladen ──────────
    for i, result in enumerate(results):
        if i >= AUGMENT_TOP_N:
            break

        payload     = result["payload"] or {}
        source_url  = payload.get("source_url", "")
        chunk_index = payload.get("chunk_index")
        total       = payload.get("total_chunks", 0)

        if source_url and chunk_index is not None:
            prev_text = ""
            next_text = ""

            if chunk_index > 0:
                prev = _fetch_neighbor_chunk(client, source_url, chunk_index - 1)
                if prev:
                    prev_text = prev.get("text", "")

            if chunk_index < total - 1:
                nxt = _fetch_neighbor_chunk(client, source_url, chunk_index + 1)
                if nxt:
                    next_text = nxt.get("text", "")

            # Erweiterten Text im Payload hinterlegen
            core_text = payload.get("text", "")
            parts = []
            if prev_text:
                parts.append(prev_text)
            parts.append(core_text)
            if next_text:
                parts.append(next_text)
            result["payload"] = {**payload, "text": "\n\n".join(parts)}

    return results


# ---------------------------------------------------------------------------
# RAG context builder
# ---------------------------------------------------------------------------


def build_rag_context(results: list[dict]) -> str:
    """Wandelt Suchergebnisse in einen formatierten Kontext-String für das LLM um."""
    blocks = []
    for i, r in enumerate(results, 1):
        p = r["payload"]
        lines = [
            f"[Quelle {i}] {p.get('title', '(kein Titel)')}",
            f"URL: {p.get('source_url', '—')}",
            f"Stand: {p.get('crawl_date', 'unbekannt')}",
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
        p       = r["payload"]
        score   = r["score"]
        url     = p.get("source_url", "—")
        faculty = p.get("faculty", "")
        heading = p.get("section_heading", "")
        date    = p.get("crawl_date", "")
        preview = p.get("text", "")[:200].replace("\n", " ")

        print(f"\n  ┌─ Treffer {i}  (RRF-Score: {score:.5f})")
        print(f"  │  URL      : {url}")
        if faculty:
            print(f"  │  Fakultät : {faculty}")
        if heading:
            print(f"  │  Abschnitt: {heading}")
        if date:
            print(f"  │  Stand    : {date}")
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

    # ── Embedding-Modelle laden ───────────────────────────────────────────
    print(f"\nLade Dense-Modell '{DENSE_MODEL}'…")
    dense_embedder = TextEmbedding(model_name=DENSE_MODEL)

    print(f"Lade Sparse-Modell '{SPARSE_MODEL}'…")
    sparse_embedder = SparseTextEmbedding(model_name=SPARSE_MODEL)

    reranker = None
    if USE_RERANKER:
        try:
            print(f"Lade Reranker '{RERANKER_MODEL}'…")
            reranker = create_reranker()
        except Exception as exc:
            print(f"Reranker nicht verfügbar — weiter ohne Reranking: {exc}")

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

        results = perform_hybrid_search(
            client, dense_embedder, sparse_embedder, query, reranker=reranker
        )
        print_results(results)


if __name__ == "__main__":
    main()
