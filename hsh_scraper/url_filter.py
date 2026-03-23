"""
Gemeinsame URL-Filterung und kleine SQLite-Ablage fuer den HsH-Crawler.

Das Ziel ist nicht, moeglichst viele Links zu crawlen, sondern moeglichst
nuetzliche Quellen fuer das RAG-System zu behalten. Deshalb bewertet dieses
Modul jede URL nach ihrem voraussichtlichen Wissenswert fuer das Korpus.
"""

from __future__ import annotations

import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_DOMAIN = "hs-hannover.de"
BLOCKED_DOMAINS = {
    "serwiss.bib.hs-hannover.de",
    "typo3backend-live.hs-hannover.de",
}

DECISION_DB_PATH = Path(__file__).parent / "data" / "url_decisions.db"

ENGLISH_SECTION_HOST = "www.hs-hannover.de"
ENGLISH_SECTION_PREFIX = "/en"
PROCESSED_ASSET_MARKER = "/fileadmin/_processed_/"

MEDIA_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".bmp",
    ".tiff",
    ".ico",
    ".mp3",
    ".wav",
    ".ogg",
    ".m4a",
    ".aac",
    ".flac",
    ".mp4",
    ".webm",
    ".mov",
    ".avi",
    ".mkv",
    ".wmv",
}

TECHNICAL_EXTENSIONS = {
    ".css",
    ".js",
    ".json",
    ".xml",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".xz",
}

OFFICE_EXTENSIONS = {
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".odt",
    ".ods",
    ".odp",
}

HTML_LIKE_EXTENSIONS = {
    "",
    ".html",
    ".htm",
    ".php",
    ".asp",
    ".aspx",
    ".jsp",
    ".jspx",
}


@dataclass(frozen=True)
class UrlDecision:
    url: str
    normalized_url: str
    decision: str
    reason: str

    @property
    def is_allowed(self) -> bool:
        return self.decision == "allow"


@dataclass
class DecisionStats:
    decision_counts: Counter[str] = field(default_factory=Counter)
    reason_counts: Counter[str] = field(default_factory=Counter)
    blocked_samples: dict[str, list[str]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def add(self, decision: UrlDecision, *, sample_limit: int = 5) -> None:
        self.decision_counts[decision.decision] += 1
        self.reason_counts[decision.reason] += 1
        if decision.decision == "block":
            samples = self.blocked_samples[decision.reason]
            if decision.normalized_url not in samples and len(samples) < sample_limit:
                samples.append(decision.normalized_url)


def normalize_url(url: str) -> str:
    """Normalisiert Host/Pfad und entfernt Query/Fragment-Rauschen."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return url

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return parsed._replace(
        scheme=scheme,
        netloc=netloc,
        path=path,
        query="",
        fragment="",
        params="",
    ).geturl()


def is_same_domain(url: str) -> bool:
    """True nur fuer oeffentliche HsH-URLs ausserhalb geblockter Subdomains."""
    netloc = urlparse(normalize_url(url)).netloc.lower()
    if not netloc or netloc in BLOCKED_DOMAINS:
        return False
    return netloc == ALLOWED_DOMAIN or netloc.endswith("." + ALLOWED_DOMAIN)


def evaluate_rag_url(url: str) -> UrlDecision:
    """Bewertet, ob eine URL wahrscheinlich nuetzlich fuer das RAG-Korpus ist."""
    normalized = normalize_url(url)

    try:
        parsed = urlparse(normalized)
    except ValueError:
        return UrlDecision(url, normalized, "block", "blockiert_ungueltige_url")

    if parsed.scheme not in {"http", "https"}:
        return UrlDecision(url, normalized, "block", "blockiert_nicht_http")

    host = parsed.netloc.lower()
    path = parsed.path or "/"
    path_lower = path.lower()

    if host in BLOCKED_DOMAINS:
        return UrlDecision(url, normalized, "block", "blockiert_backend_domain")

    if not is_same_domain(normalized):
        return UrlDecision(url, normalized, "block", "blockiert_externe_domain")

    if host == ENGLISH_SECTION_HOST and (
        path_lower == ENGLISH_SECTION_PREFIX
        or path_lower.startswith(ENGLISH_SECTION_PREFIX + "/")
    ):
        return UrlDecision(
            url,
            normalized,
            "block",
            "blockiert_englischen_en_bereich",
        )

    if PROCESSED_ASSET_MARKER in path_lower:
        return UrlDecision(url, normalized, "block", "blockiert_processed_asset")

    suffix = Path(path_lower).suffix

    if suffix in MEDIA_EXTENSIONS:
        return UrlDecision(url, normalized, "block", "blockiert_medien_datei")

    if suffix in TECHNICAL_EXTENSIONS:
        return UrlDecision(url, normalized, "block", "blockiert_technisches_asset")

    if suffix == ".pdf":
        return UrlDecision(url, normalized, "allow", "erlaubt_oeffentliches_pdf")

    if suffix in OFFICE_EXTENSIONS:
        return UrlDecision(url, normalized, "allow", "erlaubt_office_dokument")

    if suffix in HTML_LIKE_EXTENSIONS:
        return UrlDecision(url, normalized, "allow", "erlaubt_oeffentliche_html_seite")

    return UrlDecision(url, normalized, "allow", "erlaubt_oeffentliche_datei")


def format_decision_summary(
    stats: DecisionStats,
    *,
    max_reasons: int = 10,
    max_samples: int = 3,
) -> list[str]:
    """Erzeugt kurze Zusammenfassungszeilen fuer Logs oder Reports."""
    total = sum(stats.decision_counts.values())
    if total == 0:
        return []

    lines = [
        (
            "RAG-Filter: "
            f"{total} Entscheidungen "
            f"(erlaubt={stats.decision_counts.get('allow', 0)}, "
            f"blockiert={stats.decision_counts.get('block', 0)})"
        )
    ]

    for reason, count in stats.reason_counts.most_common(max_reasons):
        lines.append(f"  {reason}: {count}")

    sample_reasons = sorted(
        stats.blocked_samples,
        key=lambda reason: (-stats.reason_counts[reason], reason),
    )[:max_samples]
    for reason in sample_reasons:
        lines.append(f"  Beispiel {reason}: {stats.blocked_samples[reason][0]}")

    return lines


class UrlDecisionStore:
    """Kleine SQLite-Ablage fuer URL-Entscheidungen."""

    def __init__(
        self,
        db_path: Path = DECISION_DB_PATH,
        *,
        commit_interval: int = 100,
    ) -> None:
        self.db_path = Path(db_path)
        self.commit_interval = max(1, commit_interval)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._ensure_schema()
        self._pending_writes = 0

    def _ensure_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS url_decisions (
                normalized_url TEXT PRIMARY KEY,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                first_source TEXT NOT NULL,
                last_source TEXT NOT NULL,
                seen_count INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        self._conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_url_decisions_reason
            ON url_decisions(reason)
            """
        )
        self._conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_url_decisions_last_seen
            ON url_decisions(last_seen)
            """
        )
        self._conn.commit()

    def record(self, decision: UrlDecision, *, source: str) -> None:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._conn.execute(
            """
            INSERT INTO url_decisions (
                normalized_url,
                decision,
                reason,
                first_seen,
                last_seen,
                first_source,
                last_source,
                seen_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(normalized_url) DO UPDATE SET
                decision = excluded.decision,
                reason = excluded.reason,
                last_seen = excluded.last_seen,
                last_source = excluded.last_source,
                seen_count = url_decisions.seen_count + 1
            """,
            (
                decision.normalized_url,
                decision.decision,
                decision.reason,
                now,
                now,
                source,
                source,
            ),
        )
        self._pending_writes += 1
        if self._pending_writes >= self.commit_interval:
            self.commit()

    def lookup(self, url: str) -> dict[str, str | int] | None:
        normalized = normalize_url(url)
        row = self._conn.execute(
            """
            SELECT normalized_url, decision, reason, first_seen, last_seen,
                   first_source, last_source, seen_count
            FROM url_decisions
            WHERE normalized_url = ?
            """,
            (normalized,),
        ).fetchone()
        if row is None:
            return None
        return {
            "normalized_url": row[0],
            "decision": row[1],
            "reason": row[2],
            "first_seen": row[3],
            "last_seen": row[4],
            "first_source": row[5],
            "last_source": row[6],
            "seen_count": row[7],
        }

    def commit(self) -> None:
        self._conn.commit()
        self._pending_writes = 0

    def close(self) -> None:
        if self._conn is not None:
            if self._pending_writes:
                self.commit()
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "UrlDecisionStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
