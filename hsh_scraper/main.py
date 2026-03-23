"""
HsH Web-Spider — Automatischer Crawler für die Website der Hochschule Hannover.

Kurzbeschreibung
----------------
Crawlt die gesamte Website der Hochschule Hannover (hs-hannover.de) und speichert
jede Seite als strukturierte Markdown-Datei mit YAML-Metadaten-Header. Bildet die
erste Stufe der RAG-Pipeline (Retrieval-Augmented Generation).

Ausführliche Beschreibung
--------------------------
Das Programm arbeitet als Breadth-First-Spider: Ausgehend von einer oder mehreren
Startseiten (SEED_URLS) werden alle internen Links entdeckt, in eine Warteschlange
eingereiht und nacheinander abgearbeitet.

Wesentliche Funktionen:

1. BFS-Crawling (Breadth-First Search)
   Die Hauptschleife in main() verwaltet eine deque als Warteschlange und ein
   visited-Set zur Duplikaterkennung. Gefundene interne Links werden normalisiert
   (Fragment und Query-Parameter entfernt, Slash-Normalisierung) und nur dann
   eingereiht, wenn sie zur erlaubten Domain (ALLOWED_DOMAIN) gehören.

2. Cache-Prüfung (is_fresh)
   Vor jedem Crawl prüft is_fresh(), ob bereits eine aktuell genug gecachte
   Markdown-Datei für diese URL existiert. Ist die Datei jünger als MAX_AGE_DAYS,
   wird die Seite trotzdem heruntergeladen (für Link-Extraktion), aber nicht neu
   gespeichert. PDFs werden bei frischem Cache vollständig übersprungen.

3. HTML-Verarbeitung (process_html)
   Nutzt die Bibliothek Crawl4AI mit einem AsyncWebCrawler. Eine CrawlerRunConfig
   mit CSS-Selektoren und Ausschluss-Regeln filtert Boilerplate (Navigation, Footer,
   Cookie-Banner, Sidebars) heraus und extrahiert nur den Hauptinhalt. Das Ergebnis
   wird als Markdown gespeichert. Über result.links werden neue URLs entdeckt.

4. PDF-Verarbeitung (process_pdf)
   PDF-Dateien werden per httpx heruntergeladen und mit pymupdf4llm in Markdown
   konvertiert. Die Erkennung erfolgt über Dateiendung oder Content-Type-Header.

5. Ausgabeformat
   Jede gespeicherte Datei beginnt mit einem YAML-Frontmatter-Block:
     ---
     source_url: "https://..."
     title: "Seitentitel"
     crawl_date: "2026-03-08"
     content_type: "html"
     ---
   Dateinamen folgen dem Schema: YYYY-MM-DD_url-pfad-slug.md

6. Fehlerprotokoll (write_error_report)
   Alle fehlgeschlagenen URLs werden mit Fehlermeldung und Referrer (die Seite,
   auf der der Link gefunden wurde) in einer Excel-Datei (YYYY-MM-DD_fehler.xlsx)
   im Ausgabeverzeichnis gespeichert.

Konfiguration (Konstanten am Anfang der Datei):
   SEED_URLS        — Startseiten des Crawls
   MAX_PAGES        — Maximale Anzahl zu crawlender Seiten
   ALLOWED_DOMAIN   — Nur Links innerhalb dieser Domain werden verfolgt
   MAX_AGE_DAYS     — Wie alt eine gecachte Datei sein darf, bevor neu gecrawlt wird
   OUTPUT_DIR       — Zielverzeichnis für Markdown-Dateien
   RATE_LIMIT_SECONDS — Pause zwischen zwei Requests (Server schonen)

Abhängigkeiten: crawl4ai, httpx, pymupdf4llm, python-slugify, openpyxl
"""

import asyncio
import logging
import os
import tempfile
from collections import deque
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

import httpx
import openpyxl
import pymupdf4llm
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from slugify import slugify
from url_filter import (
    ALLOWED_DOMAIN,
    BLOCKED_DOMAINS,
    DecisionStats,
    UrlDecisionStore,
    evaluate_rag_url,
    format_decision_summary,
    normalize_url,
)

# ---------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------h------

SEED_URLS = ["https://www.hs-hannover.de/"]
MAX_PAGES = 10000
MAX_AGE_DAYS = 7  # Re-crawl pages older than this many days

OUTPUT_DIR = Path(__file__).parent / "data" / "ingested"
RATE_LIMIT_SECONDS = 2

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


def make_filename(url: str, today: str) -> str:
    """Create a filename like ``2026-02-26_studium-studienangebot.md``."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    slug = slugify(path) if path else "index"
    return f"{today}_{slug}.md"


def build_yaml_header(
    source_url: str,
    title: str,
    crawl_date: str,
    content_type: str = "html",
) -> str:
    """Return a YAML front-matter block."""
    return (
        "---\n"
        f'source_url: "{source_url}"\n'
        f'title: "{title}"\n'
        f'crawl_date: "{crawl_date}"\n'
        f'content_type: "{content_type}"\n'
        "---\n"
    )


def save_markdown(filepath: Path, header: str, body: str) -> None:
    """Write the YAML header + Markdown body to *filepath*."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(header + "\n" + body, encoding="utf-8")
    logger.info("Saved %s", filepath)


def is_fresh(url: str) -> bool:
    """Return True if a recent enough cached file exists for *url*.

    Searches OUTPUT_DIR for files matching ``*_<slug>.md`` and checks whether
    the date prefix in the filename is within MAX_AGE_DAYS of today.
    """
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    slug = slugify(path) if path else "index"
    cutoff = date.today() - timedelta(days=MAX_AGE_DAYS)
    for filepath in OUTPUT_DIR.glob(f"*_{slug}.md"):
        stem = filepath.stem          # e.g. "2026-02-26_studium-studienangebot"
        date_part = stem.split("_")[0]
        try:
            file_date = date.fromisoformat(date_part)
        except ValueError:
            continue
        if file_date >= cutoff:
            logger.info("Skipping (fresh cache from %s): %s", file_date, url)
            return True
    return False


# ---------------------------------------------------------------------------
# PDF handling
# ---------------------------------------------------------------------------


async def process_pdf(url: str, today: str) -> None:
    """Download a PDF and convert it to Markdown via pymupdf4llm."""
    logger.info("Downloading PDF: %s", url)
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name

    try:
        md_text = pymupdf4llm.to_markdown(tmp_path)
    finally:
        os.unlink(tmp_path)

    title = Path(urlparse(url).path).stem or "PDF Document"
    header = build_yaml_header(url, title, today, content_type="pdf")
    filename = make_filename(url, today)
    save_markdown(OUTPUT_DIR / filename, header, md_text)


# ---------------------------------------------------------------------------
# HTML handling
# ---------------------------------------------------------------------------


async def process_html(
    crawler: AsyncWebCrawler,
    url: str,
    today: str,
    config: CrawlerRunConfig,
    *,
    save: bool = True,
) -> None:
    """Crawl an HTML page and save its Markdown representation."""
    logger.info("Crawling: %s", url)
    result = await crawler.arun(url=url, config=config)

    if not result.success:
        raise RuntimeError(result.error_message or "Crawl failed (unknown reason)")

    # Prefer markdown_v2.raw_markdown if available, fall back to .markdown
    md_content = ""
    if hasattr(result, "markdown_v2") and result.markdown_v2:
        md_content = getattr(result.markdown_v2, "raw_markdown", "") or ""
    if not md_content:
        md_content = result.markdown or ""

    title = ""
    if hasattr(result, "metadata") and result.metadata:
        title = result.metadata.get("title", "") or ""
    if not title:
        # Fallback: first Markdown heading
        for line in md_content.splitlines():
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break
    if not title:
        title = url

    if save:
        header = build_yaml_header(url, title, today, content_type="html")
        filename = make_filename(url, today)
        save_markdown(OUTPUT_DIR / filename, header, md_content)
    return result


# ---------------------------------------------------------------------------
# Error report
# ---------------------------------------------------------------------------


def write_error_report(errors: list[dict], today: str) -> None:
    """Write a list of crawl errors to an Excel file in OUTPUT_DIR."""
    if not errors:
        logger.info("No errors — skipping error report.")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fehler"

    headers = ["URL", "Gefunden auf (Referrer)", "Fehlermeldung"]
    ws.append(headers)

    # Bold header row
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)

    for entry in errors:
        ws.append([entry["url"], entry["referrer"], entry["error"]])

    # Auto-fit column widths (heuristic)
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 80)

    filepath = OUTPUT_DIR / f"{today}_fehler.xlsx"
    wb.save(filepath)
    logger.info("Error report saved: %s (%d entries)", filepath, len(errors))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def is_pdf_url(url: str) -> bool:
    """Check if *url* points to a PDF — by extension or Content-Type header."""
    if url.lower().endswith(".pdf"):
        return True
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.head(url, timeout=10)
            content_type = resp.headers.get("content-type", "")
            return "application/pdf" in content_type.lower()
    except httpx.HTTPError:
        return False


async def main() -> None:
    today = date.today().isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    success_count = 0
    fail_count = 0
    skip_count = 0
    errors: list[dict] = []
    referrers: dict[str, str] = {}

    config = CrawlerRunConfig(
        # ── Content targeting (HsH TYPO3 structure) ───────────────
        css_selector="main, .content-main, #content, .frame-default",

        # ── Exclude boilerplate elements ──────────────────────────
        excluded_tags=[
            "nav", "header", "footer", "aside", "form",
            "iframe", "script", "style", "noscript",
        ],
        excluded_selector=(
            # Navigation
            "nav.main-menu, .main-menu, .main-menu__mainmenu, "
            "ul#tabmenu1, ul[role='menubar'], "
            # Header & Quicklinks
            "header, .quicklinks, "
            # Breadcrumb
            ".breadcrumb, .breadcrumbs, [aria-label='breadcrumb'], "
            # Footer
            "footer, .footer, .site-footer, "
            # Cookiebot cookie-consent banner
            "#CybotCookiebotDialog, #CybotCookiebotDialogBody, "
            "[id*='Cookiebot'], [class*='cookiebot'], "
            # Sidebar & misc
            "aside, .sidebar, .widget, "
            ".search-form, form[role='search'], "
            ".social-media, .share-buttons"
        ),

        # ── Wait for main content to render ───────────────────────
        # wait_for="css:main" entfernt: Seiten ohne <main>-Element
        # (z.B. karriere.hs-hannover.de) liefen sonst in einen 60s-Timeout.
        # Das Content-Targeting übernimmt css_selector zuverlässig allein.
    )

    # BFS state
    visited: set[str] = set()
    queue: deque[str] = deque()
    filter_stats = DecisionStats()

    with UrlDecisionStore() as decision_store:
        for seed in SEED_URLS:
            decision = evaluate_rag_url(seed)
            filter_stats.add(decision)
            decision_store.record(decision, source="main")
            if not decision.is_allowed:
                logger.warning(
                    "Seed-URL durch den RAG-Filter blockiert (%s): %s",
                    decision.reason,
                    decision.normalized_url,
                )
                continue
            if decision.normalized_url not in visited:
                visited.add(decision.normalized_url)
                queue.append(decision.normalized_url)
                referrers[decision.normalized_url] = "(seed)"

        pages_processed = 0

        async with AsyncWebCrawler() as crawler:
            while queue and pages_processed < MAX_PAGES:
                url = queue.popleft()
                pages_processed += 1

                try:
                    fresh = is_fresh(url)
                    if fresh:
                        skip_count += 1
                    if await is_pdf_url(url):
                        if not fresh:
                            await process_pdf(url, today)
                            success_count += 1
                    else:
                        result = await process_html(crawler, url, today, config, save=not fresh)
                        if not fresh:
                            success_count += 1
                        # Neue Links werden vor dem Einreihen zentral bewertet.
                        links_data = getattr(result, "links", {}) or {}
                        for link_dict in links_data.get("internal", []):
                            href = link_dict.get("href", "")
                            if not href or not href.startswith("http"):
                                continue
                            decision = evaluate_rag_url(href)
                            filter_stats.add(decision)
                            decision_store.record(decision, source="main")
                            if not decision.is_allowed:
                                continue
                            if decision.normalized_url not in visited:
                                visited.add(decision.normalized_url)
                                queue.append(decision.normalized_url)
                                referrers[decision.normalized_url] = url
                except Exception as exc:
                    logger.error("Error processing %s: %s", url, exc)
                    fail_count += 1
                    errors.append({
                        "url": url,
                        "referrer": referrers.get(url, "(unknown)"),
                        "error": str(exc),
                    })

                # Rate-limit between requests (skip after the last one)
                if queue and pages_processed < MAX_PAGES:
                    await asyncio.sleep(RATE_LIMIT_SECONDS)

    write_error_report(errors, today)

    for line in format_decision_summary(filter_stats):
        logger.info(line)

    logger.info(
        "Done. %d succeeded, %d failed, %d skipped (fresh cache) out of %d URLs visited.",
        success_count,
        fail_count,
        skip_count,
        pages_processed,
    )


if __name__ == "__main__":
    asyncio.run(main())
