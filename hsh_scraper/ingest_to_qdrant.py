"""
Vektorisierung — Markdown-Dateien in die Qdrant-Vektordatenbank einlesen.

Kurzbeschreibung
----------------
Liest alle Markdown-Dateien aus data/ingested/, zerlegt sie in inhaltliche
Textabschnitte (Chunks), wandelt diese in Vektoren um und lädt sie in die
Qdrant-Collection 'hsh_knowledge'. Bildet die zweite Stufe der RAG-Pipeline.

Ausführliche Beschreibung
--------------------------
Dieses Skript verbindet den Web-Spider (main.py) mit der Suchinfrastruktur.
Es verarbeitet die vom Spider erzeugten Markdown-Dateien und macht deren Inhalt
semantisch durchsuchbar. Die Verarbeitung erfolgt dateiweise als Stream, um den
Hauptspeicherverbrauch konstant zu halten.

Verarbeitungsablauf pro Datei:

1. Parsing (parse_markdown_file)
   Der YAML-Frontmatter-Header wird vom Textinhalt getrennt. Aus dem Header
   werden Metadaten (URL, Titel, Crawl-Datum, Content-Typ) extrahiert.

2. Zweistufiges Chunking (chunk_document)
   Stufe 1 — Strukturelles Chunking mit MarkdownHeaderTextSplitter:
     Das Dokument wird an Überschriften (#, ##, ###) aufgetrennt. Jeder
     entstandene Abschnitt erhält die Überschriften-Hierarchie als Metadaten
     (z.B. "Studium > Bachelor > Bewerbung"). So bleibt der thematische Kontext
     auch nach dem Aufteilen erhalten.
   Stufe 2 — Größenbegrenzung mit RecursiveCharacterTextSplitter:
     Abschnitte, die größer als CHUNK_SIZE (1000 Zeichen) sind, werden weiter
     unterteilt, mit einer Überlappung von CHUNK_OVERLAP (200 Zeichen), damit
     kein inhaltlicher Zusammenhang verloren geht.

3. Metadaten-Anreicherung
   Jeder Chunk erhält folgende Felder im Qdrant-Payload:
     - source_url, title, crawl_date, content_type  (aus dem YAML-Header)
     - section_heading   (Überschriften-Breadcrumb aus Stufe 1)
     - faculty           (aus der URL extrahiert, z.B. '/f4/' → 'Fakultät IV')
     - chunk_index, total_chunks  (Position innerhalb des Dokuments)

4. Vektorisierung (Embedding)
   Jeder Chunk-Text wird mit dem Modell jinaai/jina-embeddings-v3 (1024
   Dimensionen, multilingual) in einen Vektor umgewandelt. Der Parameter
   task="retrieval.passage" optimiert das Modell für die Indexierungsaufgabe.
   Die Einbettung erfolgt in Mini-Batches (EMBED_BATCH_SIZE=16), um den
   Speicherbedarf konstant zu halten. Nach jedem Batch werden die numpy-Arrays
   explizit gelöscht und der Garbage Collector aufgerufen.

5. Upload nach Qdrant (upsert)
   Die fertigen Punkte (Vektor + Payload) werden in die Collection
   'hsh_knowledge' hochgeladen. Die Punkt-IDs sind deterministische UUIDs
   (UUID5 aus URL + Chunk-Index), so dass ein erneuter Lauf des Skripts die
   vorhandenen Einträge aktualisiert (Upsert) statt Duplikate zu erzeugen.

Speicherverwaltung:
   Der gesamte Prozess ist als Streaming-Pipeline aufgebaut: Es werden nie alle
   Chunks aller Dateien gleichzeitig im RAM gehalten. Peak-Verbrauch ≈
   Embedding-Modell (~500 MB) + EMBED_BATCH_SIZE Vektoren (< 1 MB).

Konfiguration (Konstanten am Anfang der Datei):
   QDRANT_URL        — Adresse der Qdrant-Instanz (Standard: localhost:6333)
   COLLECTION_NAME   — Name der Qdrant-Collection
   EMBED_MODEL       — Name des Embedding-Modells (FastEmbed)
   CHUNK_SIZE        — Maximale Chunk-Größe in Zeichen
   CHUNK_OVERLAP     — Überlappung zwischen aufeinanderfolgenden Chunks
   EMBED_BATCH_SIZE  — Anzahl Chunks pro Embedding-Aufruf (RAM-Steuerung)

Voraussetzungen:
   - Qdrant läuft lokal:  docker compose up -d
   - Markdown-Dateien in data/ingested/ vorhanden (Ausgabe von main.py)

Abhängigkeiten: qdrant-client, fastembed, langchain-text-splitters
"""

import gc
import logging
import os
import sys
import uuid
from pathlib import Path

from fastembed import TextEmbedding
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_INGESTED_DIR = Path(__file__).parent / "data" / "ingested"
CURATED_DIR = Path(__file__).parent / "data" / "curated"
INGESTED_DIR = Path(
    os.getenv(
        "RAG_SOURCE_DIR",
        CURATED_DIR if CURATED_DIR.exists() and any(CURATED_DIR.glob("*.md")) else RAW_INGESTED_DIR,
    )
)
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "hsh_knowledge"

EMBED_MODEL = "jinaai/jina-embeddings-v3"
VECTOR_SIZE = 1024          # output dimension of jina-embeddings-v3

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBED_BATCH_SIZE  = 16    # chunks per embedding call — limits peak RAM
UPLOAD_BATCH_SIZE = 16    # must equal EMBED_BATCH_SIZE so vectors are freed immediately

# Abbruch/Neustart: auf 1 setzen um von Anfang an zu verarbeiten.
# Bei Unterbrechung diese Zahl auf die zuletzt angezeigte Dateinummer setzen,
# um den Prozess ab dieser Stelle fortzusetzen (1-basierter Index).
RESUME_FROM_FILE = 1

# Markdown heading levels used for structural pre-splitting
HEADERS_TO_SPLIT = [("#", "h1"), ("##", "h2"), ("###", "h3")]

# URL path segments → faculty label
FACULTY_MAP = {
    "f1": "Fakultät I",
    "f2": "Fakultät II",
    "f3": "Fakultät III",
    "f4": "Fakultät IV",
    "f5": "Fakultät V",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_markdown_file(path: Path) -> tuple[dict, str] | None:
    """Return (metadata_dict, body_text) parsed from a YAML-front-matter .md file.

    Returns None if the file has no front matter or an empty body.
    """
    text = path.read_text(encoding="utf-8")

    parts = text.split("---", 2)
    if len(parts) < 3:
        logger.warning("No YAML front matter in %s — skipping", path.name)
        return None

    yaml_block = parts[1]
    body = parts[2].strip()

    if not body:
        logger.warning("Empty body in %s — skipping", path.name)
        return None

    meta: dict[str, str] = {}
    for line in yaml_block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')

    return meta, body


def sort_markdown_files(md_files: list[Path]) -> list[Path]:
    """Sort curated files by semantic grouping before ingest."""
    sortable: list[tuple[tuple[str, str, str, str], Path]] = []
    for path in md_files:
        result = parse_markdown_file(path)
        if result is None:
            key = ("zz_unknown", "zz_unknown", "", path.name)
        else:
            meta, _ = result
            key = (
                meta.get("source_family", "zz_unknown"),
                meta.get("document_group", "zz_unknown"),
                meta.get("source_url", ""),
                path.name,
            )
        sortable.append((key, path))
    return [path for _, path in sorted(sortable, key=lambda item: item[0])]


def extract_faculty(url: str) -> str:
    """Extract faculty label from URL path, e.g. '/f4/' → 'Fakultät IV'."""
    lower = url.lower()
    for code, name in FACULTY_MAP.items():
        if f"/{code}/" in lower:
            return name
    return ""


def chunk_document(
    meta: dict,
    body: str,
    rec_splitter: RecursiveCharacterTextSplitter,
) -> list[dict]:
    """Two-stage structural chunking.

    Stage 1 — MarkdownHeaderTextSplitter:
        Splits the document at heading boundaries (#, ##, ###) and stores
        the heading hierarchy as metadata on each section.

    Stage 2 — RecursiveCharacterTextSplitter:
        Any section that still exceeds CHUNK_SIZE is further subdivided,
        preserving the heading context.
    """
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT,
        strip_headers=False,   # keep heading text inside the chunk
    )
    header_sections = header_splitter.split_text(body)

    base_payload = {
        "source_url":   meta.get("source_url", ""),
        "title":        meta.get("title", ""),
        "crawl_date":   meta.get("crawl_date", ""),
        "content_type": meta.get("content_type", "html"),
        "faculty":      extract_faculty(meta.get("source_url", "")),
        "language":     meta.get("language", ""),
        "quality_score": meta.get("quality_score", ""),
        "document_kind": meta.get("document_kind", ""),
        "source_family": meta.get("source_family", ""),
        "document_group": meta.get("document_group", ""),
        "topic_tags":    meta.get("topic_tags", ""),
    }

    final_chunks: list[dict] = []
    chunk_idx = 0

    for section in header_sections:
        # Build a breadcrumb string from the heading hierarchy metadata
        heading_parts = [
            section.metadata[k]
            for k in ("h1", "h2", "h3")
            if section.metadata.get(k)
        ]
        section_heading = " > ".join(heading_parts)

        text = section.page_content.strip()
        if not text:
            continue

        # Further split oversized sections
        sub_texts = rec_splitter.split_text(text) if len(text) > CHUNK_SIZE else [text]

        for sub in sub_texts:
            final_chunks.append({
                **base_payload,
                "text":            sub,
                "section_heading": section_heading,
                "chunk_index":     chunk_idx,
            })
            chunk_idx += 1

    # Back-fill total_chunks now that the final count is known
    total = len(final_chunks)
    for c in final_chunks:
        c["total_chunks"] = total

    return final_chunks


def make_point_id(source_url: str, chunk_index: int) -> str:
    """Deterministic UUID so re-running the script upserts rather than duplicates."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_url}#{chunk_index}"))


def ensure_collection(client: QdrantClient) -> None:
    """Create the Qdrant collection if it does not already exist."""
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )
        logger.info("Created collection '%s' (dim=%d, cosine)", COLLECTION_NAME, VECTOR_SIZE)
    else:
        logger.info("Collection '%s' already exists — upserting new/updated points", COLLECTION_NAME)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:

    # ── 1. Connect to Qdrant ──────────────────────────────────────────────
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=10)
        client.get_collections()
        logger.info("Connected to Qdrant at %s", QDRANT_URL)
    except Exception as exc:
        logger.error(
            "Cannot connect to Qdrant at %s — %s\n"
            "  Start the container with:  docker compose up -d",
            QDRANT_URL,
            exc,
        )
        sys.exit(1)

    # ── 2. Scan ingested directory ────────────────────────────────────────
    md_files = sort_markdown_files(list(INGESTED_DIR.glob("*.md")))
    if not md_files:
        logger.error("No .md files found in %s", INGESTED_DIR)
        sys.exit(1)
    logger.info("Found %d .md file(s) in %s", len(md_files), INGESTED_DIR)

    if RESUME_FROM_FILE > 1:
        skip = RESUME_FROM_FILE - 1
        logger.info("Skipping first %d file(s) (RESUME_FROM_FILE=%d)", skip, RESUME_FROM_FILE)
        md_files = md_files[skip:]

    # ── 3. Prepare splitters ──────────────────────────────────────────────
    rec_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # ── 4. Load embedding model once ──────────────────────────────────────
    logger.info(
        "Loading embedding model '%s' (first run downloads the model ~1 GB)…",
        EMBED_MODEL,
    )
    embedder = TextEmbedding(model_name=EMBED_MODEL)
    logger.info("Model loaded.")

    # ── 5. Ensure collection ──────────────────────────────────────────────
    ensure_collection(client)

    # ── 6. Stream: parse → chunk → embed → upload, one mini-batch at a time ─
    # Peak RAM ≈ model  +  EMBED_BATCH_SIZE vectors  (constant, never grows)
    # After each mini-batch: vectors and PointStructs are deleted immediately.
    # gc.collect() after each file forces numpy to release pages back to the OS.
    total_points  = 0
    skipped       = 0
    chunk_counts: list[int] = []
    char_len_sum  = 0     # running sum instead of storing all lengths
    char_len_count = 0

    for path in md_files:
        result = parse_markdown_file(path)
        if result is None:
            skipped += 1
            continue

        meta, body = result
        chunks = chunk_document(meta, body, rec_splitter)
        if not chunks:
            skipped += 1
            continue

        file_points = 0

        # ── Mini-batch loop: EMBED_BATCH_SIZE chunks at a time ────────────
        for sub_start in range(0, len(chunks), EMBED_BATCH_SIZE):
            sub_chunks  = chunks[sub_start : sub_start + EMBED_BATCH_SIZE]
            sub_texts   = [c["text"] for c in sub_chunks]

            # Embed this mini-batch; generator consumed immediately
            sub_vectors = list(embedder.embed(sub_texts, task="retrieval.passage"))

            points = [
                models.PointStruct(
                    id=make_point_id(c["source_url"], c["chunk_index"]),
                    vector=sub_vectors[i].tolist(),
                    payload=c,
                )
                for i, c in enumerate(sub_chunks)
            ]

            try:
                client.upsert(collection_name=COLLECTION_NAME, points=points)
            except Exception as exc:
                logger.error("Upload failed for %s (offset %d): %s",
                             path.name, sub_start, exc)
                sys.exit(1)

            file_points += len(points)

            # ── Explicit release of numpy arrays & PointStructs ───────────
            del sub_vectors, points

        total_points   += file_points
        char_len_sum   += sum(len(c["text"]) for c in chunks)
        char_len_count += file_points
        chunk_counts.append(file_points)

        files_done = md_files.index(path) + 1
        abs_done = files_done + (RESUME_FROM_FILE - 1)
        total_all = len(md_files) + (RESUME_FROM_FILE - 1)
        pct = 100.0 * abs_done / total_all
        logger.info(
            "  [%d/%d  %5.1f%%]  %-55s → %3d chunk(s)  (total: %d)",
            abs_done, total_all, pct, path.name, file_points, total_points,
        )

        # ── Release chunk list; nudge Python to return pages to the OS ────
        del chunks
        gc.collect()

    if total_points == 0:
        logger.error("No usable content found — aborting.")
        sys.exit(1)

    # ── 7. Final statistics ───────────────────────────────────────────────
    avg_chunk_len = char_len_sum / char_len_count if char_len_count else 0
    avg_chunks_per_file = sum(chunk_counts) / len(chunk_counts) if chunk_counts else 0

    logger.info("─" * 60)
    logger.info("Collection   : %s", COLLECTION_NAME)
    logger.info("Files parsed : %d  (skipped: %d)", len(md_files) - skipped, skipped)
    logger.info("Total chunks : %d", total_points)
    logger.info("Avg chunks/file : %.1f", avg_chunks_per_file)
    logger.info("Avg chunk length: %.0f chars", avg_chunk_len)
    logger.info("─" * 60)


if __name__ == "__main__":
    main()
