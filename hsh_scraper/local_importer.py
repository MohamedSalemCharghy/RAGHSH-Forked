"""
Lokaler Qdrant-Importer — Parquet-Datei in Qdrant-Datenbank laden.

Kurzbeschreibung
----------------
Liest die von hpc_vectorizer.py erzeugte Parquet-Datei und lädt die Vektoren
samt Metadaten per Upsert in die lokale Qdrant-Instanz.

Workflow:
    1. HPC:   python hpc_vectorizer.py   →  hsh_vectors.parquet
    2. Transfer: scp user@hpc:~/hsh_vectors.parquet ./
    3. Lokal: python local_importer.py

Verhalten bei erneutem Aufruf:
    Punkt-IDs sind deterministisch (UUID5 aus source_url + chunk_index).
    Ein erneuter Lauf überschreibt vorhandene Einträge (Upsert), erzeugt
    keine Duplikate.

Konfiguration:
    PARQUET_FILE    — Pfad zur Eingabedatei
    QDRANT_URL      — Adresse der lokalen Qdrant-Instanz
    COLLECTION_NAME — Name der Collection
    UPLOAD_BATCH    — Punkte pro upsert-Aufruf
    RESUME_FROM_ROW — Neustart ab Zeile N (0 = von Anfang an)

Abhängigkeiten (lokales VirtualEnv):
    pip install qdrant-client pyarrow
"""

import logging
import sys
from pathlib import Path

import pyarrow.parquet as pq
from qdrant_client import QdrantClient, models

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

PARQUET_FILE    = Path(__file__).parent / "hsh_vectors.parquet"
QDRANT_URL      = "http://localhost:6333"
COLLECTION_NAME = "hsh_knowledge"
VECTOR_SIZE     = 1024

UPLOAD_BATCH    = 100  # Punkte pro upsert-Aufruf

# Neustart nach Unterbrechung: 0-basierter Zeilenindex.
# 0 = von Anfang an. Bei Abbruch bei Batch N: RESUME_FROM_ROW = N * UPLOAD_BATCH
RESUME_FROM_ROW = 0

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


def ensure_collection(client: QdrantClient) -> None:
    """Erstellt die Collection falls sie noch nicht existiert."""
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )
        # Volltext-Index auf dem 'text'-Feld für Hybrid-Suche
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="text",
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=15,
                lowercase=True,
            ),
        )
        logger.info("Collection '%s' angelegt (dim=%d, cosine)", COLLECTION_NAME, VECTOR_SIZE)
    else:
        logger.info("Collection '%s' existiert bereits — Upsert-Modus", COLLECTION_NAME)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    # ── 1. Parquet-Datei prüfen ───────────────────────────────────────────
    if not PARQUET_FILE.exists():
        logger.error("Datei nicht gefunden: %s", PARQUET_FILE)
        logger.error("Bitte zuerst hpc_vectorizer.py auf dem HPC ausführen")
        sys.exit(1)

    # Parquet-Metadaten lesen ohne den gesamten Inhalt in den RAM zu laden
    pf = pq.ParquetFile(PARQUET_FILE)
    total_rows = pf.metadata.num_rows
    size_mb    = PARQUET_FILE.stat().st_size / 1_048_576
    logger.info("Parquet-Datei: %s  (%.1f MB, %d Zeilen)", PARQUET_FILE, size_mb, total_rows)

    # ── 2. Qdrant verbinden ───────────────────────────────────────────────
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=30)
        client.get_collections()
        logger.info("Verbunden mit Qdrant: %s", QDRANT_URL)
    except Exception as exc:
        logger.error("Verbindung zu Qdrant fehlgeschlagen: %s — %s", QDRANT_URL, exc)
        logger.error("Docker-Container starten:  docker compose up -d")
        sys.exit(1)

    ensure_collection(client)

    # ── 3. Zeilenweise in Batches einlesen und hochladen ─────────────────
    if RESUME_FROM_ROW > 0:
        logger.info("Überspringe die ersten %d Zeilen (RESUME_FROM_ROW=%d)",
                    RESUME_FROM_ROW, RESUME_FROM_ROW)

    uploaded   = 0
    row_cursor = 0

    # iter_batches liest Row-Group-weise — passt sich automatisch an die
    # in hpc_vectorizer.py geschriebene Row-Group-Größe an.
    for batch in pf.iter_batches(batch_size=UPLOAD_BATCH):
        batch_start = row_cursor
        batch_end   = row_cursor + len(batch)
        row_cursor  = batch_end

        # Überspringe Zeilen vor RESUME_FROM_ROW
        if batch_end <= RESUME_FROM_ROW:
            continue
        if batch_start < RESUME_FROM_ROW:
            # Teilweise überspringen: nur den Rest des Batches verwenden
            offset = RESUME_FROM_ROW - batch_start
            batch  = batch.slice(offset)

        # PyArrow-Batch → PointStruct-Liste
        ids             = batch.column("id").to_pylist()
        vectors         = batch.column("vector").to_pylist()
        source_urls     = batch.column("source_url").to_pylist()
        titles          = batch.column("title").to_pylist()
        crawl_dates     = batch.column("crawl_date").to_pylist()
        content_types   = batch.column("content_type").to_pylist()
        faculties       = batch.column("faculty").to_pylist()
        section_headings = batch.column("section_heading").to_pylist()
        texts           = batch.column("text").to_pylist()
        chunk_indices   = batch.column("chunk_index").to_pylist()
        total_chunks    = batch.column("total_chunks").to_pylist()

        points = [
            models.PointStruct(
                id=ids[i],
                vector=vectors[i],
                payload={
                    "source_url":      source_urls[i],
                    "title":           titles[i],
                    "crawl_date":      crawl_dates[i],
                    "content_type":    content_types[i],
                    "faculty":         faculties[i],
                    "section_heading": section_headings[i],
                    "text":            texts[i],
                    "chunk_index":     chunk_indices[i],
                    "total_chunks":    total_chunks[i],
                },
            )
            for i in range(len(ids))
        ]

        try:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
        except Exception as exc:
            logger.error("Upsert fehlgeschlagen bei Zeile %d: %s", batch_start, exc)
            logger.error("Zum Fortsetzen: RESUME_FROM_ROW = %d", batch_start)
            sys.exit(1)

        uploaded += len(points)
        pct = 100.0 * uploaded / max(total_rows - RESUME_FROM_ROW, 1)
        logger.info("  [%6d/%6d  %5.1f%%]  %d Punkte hochgeladen",
                    uploaded, total_rows - RESUME_FROM_ROW, pct, len(points))

        del points, vectors

    logger.info("─" * 60)
    logger.info("Fertig. %d Punkte in Collection '%s' eingefügt/aktualisiert.",
                uploaded, COLLECTION_NAME)
    logger.info("─" * 60)


if __name__ == "__main__":
    main()
