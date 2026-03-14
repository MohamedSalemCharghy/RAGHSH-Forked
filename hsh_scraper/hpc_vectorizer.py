"""
HPC-Vektorisierung — Markdown-Dateien vektorisieren und als Parquet exportieren.

Kurzbeschreibung
----------------
Dieses Skript ist für den Einsatz auf einem HPC-Cluster (z.B. GWDG/KISSKI mit
NVIDIA H100) vorgesehen. Es hat keine Qdrant-Abhängigkeit. Stattdessen werden
alle erzeugten Vektoren und Metadaten in eine komprimierte Parquet-Datei
geschrieben, die anschließend auf den lokalen Rechner übertragen und dort mit
local_importer.py in Qdrant geladen werden kann.

Workflow:
    1. HPC: python hpc_vectorizer.py   →  hsh_vectors.parquet
    2. Transfer: scp hsh_vectors.parquet user@localhost:~/RAGHSH/hsh_scraper/
    3. Lokal:  python local_importer.py

Speicherverwaltung:
    Die PyArrow-ParquetWriter-API wird genutzt, um dateiweise Row-Groups zu
    schreiben. Es wird nie mehr als eine Datei (ihre Chunks + Vektoren) gleichzeitig
    im RAM gehalten. Peak-Verbrauch ≈ Dense-Modell (~500 MB) + Sparse-Modell (~50 MB)
    + EMBED_BATCH_SIZE × VECTOR_SIZE × 4 Byte pro Dense-Mini-Batch.

Parquet-Schema:
    id              string          — deterministischer UUID5 (source_url + chunk_index)
    vector          list<float32>   — 1024-dimensionaler Dense-Einbettungsvektor (Jina)
    source_url      string
    title           string
    crawl_date      string
    content_type    string          — 'html' oder 'pdf'
    faculty         string
    section_heading string
    text            string          — Volltext des Chunks
    chunk_index     int32
    total_chunks    int32
    sparse_indices  list<int32>     — Token-IDs der BM25-Terme
    sparse_values   list<float32>   — BM25-Gewichte der Terme

Konfiguration:
    RESUME_FROM_FILE   — Neustart ab Dateinummer (1 = von Anfang an)
    DENSE_BATCH_SIZE   — Chunks pro Dense-Embedding-Aufruf (H100: 64 empfohlen)
    SPARSE_BATCH_SIZE  — Chunks pro BM25-Aufruf (CPU-only, größere Batches OK)
    OUTPUT_FILE        — Ausgabedatei (Parquet)

Abhängigkeiten (HPC-VirtualEnv):
    pip install fastembed langchain-text-splitters pyarrow
"""

import gc
import logging
import sys
import uuid
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from fastembed import SparseTextEmbedding, TextEmbedding
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

INGESTED_DIR    = Path(__file__).parent / "data" / "ingested"
OUTPUT_FILE     = Path(__file__).parent / "hsh_vectors.parquet"

DENSE_MODEL      = "jinaai/jina-embeddings-v3"
SPARSE_MODEL     = "Qdrant/bm25"
VECTOR_SIZE      = 1024          # Ausgabedimension von jina-embeddings-v3

CHUNK_SIZE       = 1000
CHUNK_OVERLAP    = 200
DENSE_BATCH_SIZE  = 64           # H100 verarbeitet größere Batches effizient
SPARSE_BATCH_SIZE = 256          # BM25 ist CPU-only, größere Batches sind kein Problem

RESUME_FROM_FILE = 1             # 1 = von Anfang an; N = ab Datei N weitermachen

HEADERS_TO_SPLIT = [("#", "h1"), ("##", "h2"), ("###", "h3")]

FACULTY_MAP = {
    "f1": "Fakultät I",
    "f2": "Fakultät II",
    "f3": "Fakultät III",
    "f4": "Fakultät IV",
    "f5": "Fakultät V",
}

# ---------------------------------------------------------------------------
# Parquet-Schema
# ---------------------------------------------------------------------------

PARQUET_SCHEMA = pa.schema([
    pa.field("id",              pa.string()),
    pa.field("vector",          pa.list_(pa.float32())),
    pa.field("source_url",      pa.string()),
    pa.field("title",           pa.string()),
    pa.field("crawl_date",      pa.string()),
    pa.field("content_type",    pa.string()),
    pa.field("faculty",         pa.string()),
    pa.field("section_heading", pa.string()),
    pa.field("text",            pa.string()),
    pa.field("chunk_index",     pa.int32()),
    pa.field("total_chunks",    pa.int32()),
    pa.field("sparse_indices",  pa.list_(pa.int32())),
    pa.field("sparse_values",   pa.list_(pa.float32())),
])

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Hilfsfunktionen (identisch mit ingest_to_qdrant.py)
# ---------------------------------------------------------------------------


def parse_markdown_file(path: Path) -> tuple[dict, str] | None:
    """Liest YAML-Frontmatter und Body aus einer Markdown-Datei."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        logger.warning("Kein YAML-Header in %s — übersprungen", path.name)
        return None
    yaml_block = parts[1]
    body = parts[2].strip()
    if not body:
        logger.warning("Leerer Body in %s — übersprungen", path.name)
        return None
    meta: dict[str, str] = {}
    for line in yaml_block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')
    return meta, body


def extract_faculty(url: str) -> str:
    """Ermittelt die Fakultätszugehörigkeit aus der URL.

    Prüft zuerst URL-Pfad-Segmente (/f1/ bis /f5/), dann Subdomains.
    Gibt "" zurück für zentrale Einrichtungen ohne Fakultätszugehörigkeit.
    """
    lower = url.lower()

    # Pfad-basierte Erkennung: /f1/ bis /f5/
    for code, name in FACULTY_MAP.items():
        if f"/{code}/" in lower:
            return name

    # Subdomain-basierte Erkennung
    from urllib.parse import urlparse
    netloc = urlparse(lower).netloc
    if netloc.startswith("karriere."):
        return "Karriere"
    if netloc.startswith("bibliothek."):
        return "Bibliothek"
    if netloc.startswith("international."):
        return "International"

    return ""


def chunk_document(meta: dict, body: str,
                   rec_splitter: RecursiveCharacterTextSplitter) -> list[dict]:
    """Zweistufiges strukturelles Chunking (Überschriften + Größenbegrenzung)."""
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT,
        strip_headers=False,
    )
    header_sections = header_splitter.split_text(body)

    base_payload = {
        "source_url":   meta.get("source_url", ""),
        "title":        meta.get("title", ""),
        "crawl_date":   meta.get("crawl_date", ""),
        "content_type": meta.get("content_type", "html"),
        "faculty":      extract_faculty(meta.get("source_url", "")),
    }

    final_chunks: list[dict] = []
    chunk_idx = 0

    for section in header_sections:
        heading_parts = [
            section.metadata[k]
            for k in ("h1", "h2", "h3")
            if section.metadata.get(k)
        ]
        section_heading = " > ".join(heading_parts)
        text = section.page_content.strip()
        if not text:
            continue
        sub_texts = rec_splitter.split_text(text) if len(text) > CHUNK_SIZE else [text]
        for sub in sub_texts:
            final_chunks.append({
                **base_payload,
                "text":            sub,
                "section_heading": section_heading,
                "chunk_index":     chunk_idx,
            })
            chunk_idx += 1

    total = len(final_chunks)
    for c in final_chunks:
        c["total_chunks"] = total
    return final_chunks


def make_point_id(source_url: str, chunk_index: int) -> str:
    """Deterministischer UUID5 — identisch mit ingest_to_qdrant.py."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_url}#{chunk_index}"))


def chunks_to_record_batch(chunks: list[dict],
                           dense_vectors: list,
                           sparse_indices: list[list[int]],
                           sparse_values: list[list[float]]) -> pa.RecordBatch:
    """Erstellt einen PyArrow-RecordBatch aus Chunks, Dense- und Sparse-Vektoren."""
    return pa.record_batch(
        {
            "id":              [make_point_id(c["source_url"], c["chunk_index"]) for c in chunks],
            "vector":          [v.tolist() for v in dense_vectors],
            "source_url":      [c["source_url"]      for c in chunks],
            "title":           [c["title"]           for c in chunks],
            "crawl_date":      [c["crawl_date"]      for c in chunks],
            "content_type":    [c["content_type"]    for c in chunks],
            "faculty":         [c["faculty"]         for c in chunks],
            "section_heading": [c["section_heading"] for c in chunks],
            "text":            [c["text"]            for c in chunks],
            "chunk_index":     [c["chunk_index"]     for c in chunks],
            "total_chunks":    [c["total_chunks"]    for c in chunks],
            "sparse_indices":  sparse_indices,
            "sparse_values":   sparse_values,
        },
        schema=PARQUET_SCHEMA,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    # ── 1. Dateien einlesen ───────────────────────────────────────────────
    md_files = sorted(INGESTED_DIR.glob("*.md"))
    if not md_files:
        logger.error("Keine .md-Dateien gefunden in %s", INGESTED_DIR)
        sys.exit(1)
    logger.info("Gefunden: %d .md-Datei(en) in %s", len(md_files), INGESTED_DIR)

    if RESUME_FROM_FILE > 1:
        skip = RESUME_FROM_FILE - 1
        logger.info("Überspringe die ersten %d Datei(en) (RESUME_FROM_FILE=%d)",
                    skip, RESUME_FROM_FILE)
        md_files = md_files[skip:]

    # ── 2. Splitter vorbereiten ───────────────────────────────────────────
    rec_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # ── 3. Embedding-Modelle laden ────────────────────────────────────────
    logger.info("Lade Dense-Modell '%s' …", DENSE_MODEL)
    dense_embedder = TextEmbedding(model_name=DENSE_MODEL)

    logger.info("Lade Sparse-Modell '%s' (BM25, CPU-only) …", SPARSE_MODEL)
    sparse_embedder = SparseTextEmbedding(model_name=SPARSE_MODEL)
    logger.info("Beide Modelle bereit.")

    # ── 4. Parquet-Writer öffnen ──────────────────────────────────────────
    # Schreibt dateiweise Row-Groups → konstanter RAM-Bedarf
    writer = pq.ParquetWriter(
        OUTPUT_FILE,
        schema=PARQUET_SCHEMA,
        compression="zstd",
        compression_level=3,
    )
    logger.info("Schreibe nach: %s", OUTPUT_FILE)

    total_points = 0
    skipped      = 0
    total_all    = len(md_files) + (RESUME_FROM_FILE - 1)

    try:
        for files_done, path in enumerate(md_files, start=1):
            result = parse_markdown_file(path)
            if result is None:
                skipped += 1
                continue

            meta, body = result
            chunks = chunk_document(meta, body, rec_splitter)
            if not chunks:
                skipped += 1
                continue

            file_batches: list[pa.RecordBatch] = []
            texts = [c["text"] for c in chunks]

            # ── Dense-Batches (GPU) ───────────────────────────────────────
            dense_vecs_all: list = []
            for d_start in range(0, len(texts), DENSE_BATCH_SIZE):
                batch_texts = texts[d_start : d_start + DENSE_BATCH_SIZE]
                dense_vecs_all.extend(
                    list(dense_embedder.embed(batch_texts, task="retrieval.passage"))
                )

            # ── Sparse-Batches (CPU/BM25) ─────────────────────────────────
            sparse_indices_all: list[list[int]]   = []
            sparse_values_all:  list[list[float]] = []
            for s_start in range(0, len(texts), SPARSE_BATCH_SIZE):
                batch_texts = texts[s_start : s_start + SPARSE_BATCH_SIZE]
                for emb in sparse_embedder.embed(batch_texts):
                    sparse_indices_all.append(emb.indices.tolist())
                    sparse_values_all.append(emb.values.tolist())

            # ── RecordBatches zusammenstellen ─────────────────────────────
            for sub_start in range(0, len(chunks), DENSE_BATCH_SIZE):
                sub_end    = sub_start + DENSE_BATCH_SIZE
                sub_chunks = chunks[sub_start:sub_end]
                batch = chunks_to_record_batch(
                    sub_chunks,
                    dense_vecs_all[sub_start:sub_end],
                    sparse_indices_all[sub_start:sub_end],
                    sparse_values_all[sub_start:sub_end],
                )
                file_batches.append(batch)

            # Alle Batches dieser Datei als eine Row-Group schreiben
            if file_batches:
                table = pa.Table.from_batches(file_batches, schema=PARQUET_SCHEMA)
                writer.write_table(table)
                file_points   = len(table)
                total_points += file_points

                abs_done = files_done + (RESUME_FROM_FILE - 1)
                pct      = 100.0 * abs_done / total_all
                logger.info(
                    "  [%d/%d  %5.1f%%]  %-55s → %3d Chunk(s)  (gesamt: %d)",
                    abs_done, total_all, pct, path.name, file_points, total_points,
                )
                del table, file_batches

            del chunks, texts, dense_vecs_all, sparse_indices_all, sparse_values_all
            gc.collect()

    finally:
        writer.close()

    if total_points == 0:
        logger.error("Kein verwendbarer Inhalt — abgebrochen.")
        sys.exit(1)

    size_mb = OUTPUT_FILE.stat().st_size / 1_048_576
    logger.info("─" * 60)
    logger.info("Ausgabe      : %s  (%.1f MB)", OUTPUT_FILE, size_mb)
    logger.info("Dateien      : %d  (übersprungen: %d)",
                len(md_files) - skipped, skipped)
    logger.info("Chunks gesamt: %d  (Dense + Sparse)", total_points)
    logger.info("─" * 60)
    logger.info("Nächster Schritt: Datei auf lokalen Rechner übertragen")
    logger.info("  scp %s user@localhost:~/RAGHSH/hsh_scraper/", OUTPUT_FILE)
    logger.info("Dann direkt: python local_importer.py  (enrich_sparse.py nicht nötig)")


if __name__ == "__main__":
    main()
