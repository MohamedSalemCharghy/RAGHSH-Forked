"""
RAG-Evaluation fuer den HsH-Chatbot.

Kurzueberblick
--------------
Dieses Skript bewertet die bestehende RAG-Pipeline des Repositories end-to-end.
Es nutzt dieselben Kernbausteine wie der eigentliche Chatbot:

1. dieselbe Qdrant-basierte Hybrid-Suche aus `hybrid_search.py`
2. dieselbe GWDG/OpenAI-kompatible LLM-Anbindung aus `hsh_chatbot.py`
3. denselben Prompt-Aufbau fuer die Antwortgenerierung

Damit misst die Evaluation nicht irgendeine vereinfachte Testlogik, sondern
moeglichst genau das Verhalten, das spaeter auch im produktiven Chatbot
verwendet wird.


Was das Skript konkret macht
----------------------------
Fuer jede Zeile im JSONL-Datensatz wird folgender Ablauf ausgefuehrt:

1. Die Frage wird aus dem Datensatz gelesen.
2. Die bestehende Hybrid-Suche holt die Top-K-Kontext-Chunks aus Qdrant.
3. Die Treffer werden mit `build_rag_context()` zu einem LLM-Kontext formatiert.
4. Das LLM erzeugt auf Basis desselben Repo-Prompts eine Antwort.
5. Danach werden mehrere Kennzahlen berechnet, zum Beispiel:
   - ob erwartete URLs in den Treffern vorkamen
   - wie hoch der URL-Recall war
   - wie stark der Retrieval-Kontext die geforderten Fakten abdeckt
   - wie stark die Antwort mit einer Referenzantwort ueberlappt
   - wie viele geforderte Fakten in der Antwort auftauchen
6. Optional kann ein LLM-as-a-Judge-Lauf eingeschaltet werden.
7. Am Ende werden eine Konsolen-Zusammenfassung und eine JSON-Ergebnisdatei
   unter `hsh_scraper/evals/results/` gespeichert.


Wichtig zur Modellwahl
----------------------
Dieses Skript verwendet absichtlich dieselbe LLM-Anbindung wie der Rest des
Repos: den GWDG-ChatAI-Dienst ueber den OpenAI-kompatiblen Client aus
`hsh_chatbot.py`.

Das konkrete Eval-Modell wird zentral ganz oben in diesem Skript aufgeloest:

- zuerst per CLI mit `--model`
- sonst per Umgebungsvariable `RAG_EVAL_MODEL`
- sonst automatisch aus einer Liste von im Repo bereits verwendeten bzw.
  dokumentierten Modellen

Dadurch startest du mit demselben LLM-Setup wie im Projekt, kannst aber spaeter
sehr leicht auf ein anderes Modell wechseln, ohne die Evaluationslogik
anzupassen.

Beispiele:

    python hsh_scraper/evals/evaluate_rag.py
    python hsh_scraper/evals/evaluate_rag.py --model gpt-4o
    RAG_EVAL_MODEL=deepseek-r1 python hsh_scraper/evals/evaluate_rag.py

Falls du auch das Judge-Modell separat steuern willst:

    python hsh_scraper/evals/evaluate_rag.py --judge --judge-model gpt-4o
    RAG_JUDGE_MODEL=gpt-4o python hsh_scraper/evals/evaluate_rag.py --judge


Datensatzformat
---------------
Die Datei `datasets/eval_dataset.jsonl` ist bewusst flexibel gehalten, damit du
spaeter weitere Beispiele leicht ergaenzen kannst. Pro Zeile wird genau ein
JSON-Objekt erwartet.

Minimalbeispiel:

    {"question": "Wie beantrage ich eine Beurlaubung?"}

Primaeres Schema fuer deinen Datensatz:

    {
      "id": "q001",
      "category": "bewerbung",
      "question": "Wie beantrage ich eine Beurlaubung?",
      "reference_answer": "Expected answer here.",
      "required_facts": [
        "fact 1",
        "fact 2"
      ]
    }

Optional zusaetzlich moeglich:

    {
      "id": "q002",
      "category": "studium",
      "question": "Wo finde ich Informationen zu Bewerbungsfristen?",
      "reference_answer": "Expected answer here.",
      "required_facts": [
        "fact 1"
      ],
      "expected_urls": [
        "https://www.hs-hannover.de/studium/..."
      ],
      "faculty": "Fakultät IV"
    }

Unterstuetzte Feldnamen:

- `question`, alternativ `query` oder `prompt`
- `category`
- `ground_truth`, alternativ `expected_answer` oder `reference_answer`
- `expected_urls`, alternativ `gold_urls` oder `relevant_urls`
- `required_facts`, alternativ `expected_phrases`, `keywords` oder `must_include`
- `faculty` oder `fakultaet`
- `should_answer` fuer spaetere Negativ-/No-Answer-Faelle

Das Skript versucht absichtlich mehrere Alias-Namen zu akzeptieren, damit du
deinen Datensatz im Laufe der Zeit erweitern kannst, ohne bei jeder kleinen
Schema-Aenderung sofort Code anpassen zu muessen.


Was die Kennzahlen bedeuten
---------------------------
1. `retrieval_hit`
   Mindestens eine erwartete URL wurde in den Top-K-Treffern gefunden.

2. `retrieval_url_recall`
   Anteil der erwarteten URLs, die in den Treffern enthalten waren.

3. `context_fact_hit_ratio`
   Anteil der `required_facts`, die bereits im Retrieval-Kontext vorkommen.
   Das ist besonders nuetzlich fuer dein aktuelles JSONL-Schema, weil man damit
   auch ohne Gold-URLs sehen kann, ob das Retrieval die richtigen Informationen
   geholt hat.

4. `answer_token_f1`
   Ein einfacher lexikalischer Vergleich zwischen Modellantwort und
   Referenzantwort. Das ist kein perfektes semantisches Mass, aber ein sehr
   nuetzlicher, schneller Basisindikator.

5. `answer_fact_hit_ratio`
   Anteil der `required_facts`, die in der Modellantwort auftauchen.

6. `judge_*`
   Nur wenn `--judge` aktiviert ist: zusaetzliche qualitative Bewertung durch
   ein LLM, das Korrektheit, Erdung im Kontext und Vollstaendigkeit einschaetzt.


Bewusste Designentscheidungen
-----------------------------
- Keine Zusatzabhaengigkeiten wie RAGAS:
  Das Repo hat derzeit keine Evaluationsbibliothek dafuer eingetragen. Dieses
  Skript bleibt deshalb bei Standardbibliothek plus den bereits vorhandenen
  Repo-Abhaengigkeiten.

- Gleicher Prompt wie im Chatbot:
  Die Antwortgenerierung nutzt `build_rag_messages()` aus `hsh_chatbot.py`.
  So misst du tatsaechlich das bestehende Verhalten und nicht einen abweichenden
  Eval-Sonderprompt.

- Gleiche Suchpipeline wie im Produktivsystem:
  Retrieval laeuft ueber `perform_hybrid_search()` und damit ueber dense search,
  sparse search, RRF-Fusion, URL-Dedup, optionales Reranking und Nachbar-Chunk-
  Augmentation.

- Leerer Datensatz wird freundlich behandelt:
  Wenn `eval_dataset.jsonl` noch leer ist, bricht das Skript nicht mit einer
  kryptischen Fehlermeldung ab, sondern zeigt ein Beispiel-Schema an. Das passt
  zu deinem Hinweis, dass du spaeter mehr Daten eintragen wirst.


Grenzen der Evaluation
----------------------
- Lexikalische Metriken koennen gute Paraphrasen zu streng bestrafen.
- Ein LLM-as-a-Judge ist hilfreich, aber nicht unfehlbar.
- Ohne `ground_truth`, `required_facts` oder `expected_urls` kann das Skript
  zwar Antworten generieren, aber nur eingeschraenkt automatisch bewerten.

Trotzdem ist dieses Skript ein sehr guter pragmatischer Startpunkt, um Retrieval
und Antwortqualitaet systematisch messbar zu machen und spaeter mit groesseren
Datensaetzen auszubauen.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from fastembed import SparseTextEmbedding, TextEmbedding
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client import models as qmodels

# Damit das Skript auch von `hsh_scraper/evals/` aus direkt gestartet werden kann,
# wird das uebergeordnete `hsh_scraper/`-Verzeichnis explizit in den Importpfad gelegt.
SCRAPER_DIR = Path(__file__).resolve().parents[1]
if str(SCRAPER_DIR) not in sys.path:
    sys.path.insert(0, str(SCRAPER_DIR))

from hsh_chatbot import (  # noqa: E402
    EMBED_MODEL,
    QDRANT_URL,
    RAG_TOP_K,
    SPARSE_MODEL,
    ask_llm,
    build_client,
    build_rag_messages,
    get_available_models,
)
from hybrid_search import (  # noqa: E402
    RERANKER_MODEL,
    USE_RERANKER,
    build_rag_context,
    perform_hybrid_search,
)

# ---------------------------------------------------------------------------
# Zentrale Konfiguration
# ---------------------------------------------------------------------------

EVALS_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET_PATH = EVALS_DIR / "datasets" / "eval_dataset.jsonl"
RESULTS_DIR = EVALS_DIR / "results"

# Dieses Skript startet standardmaessig mit Modellen, die im Repo bereits
# verwendet oder dokumentiert sind. Wechseln kannst du spaeter bequem per
# `--model`, `--judge-model`, `RAG_EVAL_MODEL` oder `RAG_JUDGE_MODEL`.
REPO_MODEL_PREFERENCES = (
    "gpt-4o-mini",
    "gpt-4o",
    "meta-llama-3.1-8b-instruct",
    "meta-llama-3.1-70b-instruct",
    "deepseek-r1",
)
MODEL_OVERRIDE_ENV = "RAG_EVAL_MODEL"
JUDGE_MODEL_ENV = "RAG_JUDGE_MODEL"

NO_INFO_ANSWER = (
    "Dazu liegen mir keine Informationen aus den offiziellen Dokumenten der HsH vor."
)

JUDGE_SYSTEM_PROMPT = """\
Du bist ein strenger Evaluator fuer ein Retrieval-Augmented-Generation-System.
Bewerte die gegebene Modellantwort nur anhand der bereitgestellten Frage,
des Referenzmaterials und des RAG-Kontexts.

Antworte ausschliesslich mit einem JSON-Objekt in diesem Format:
{
  "correctness": 0.0,
  "groundedness": 0.0,
  "completeness": 0.0,
  "verdict": "pass|partial|fail",
  "reason": "kurze Begruendung"
}

Bewertungshinweise:
- correctness: Ist die Antwort inhaltlich richtig?
- groundedness: Ist die Antwort durch den Kontext gedeckt?
- completeness: Beantwortet die Antwort die Frage ausreichend?
- Nutze nur Werte zwischen 0.0 und 1.0.
- Wenn Informationen fehlen, bewerte konservativ.
"""

WORD_RE = re.compile(r"\w+", re.UNICODE)


def parse_args() -> argparse.Namespace:
    """Liest alle CLI-Parameter ein.

    Das Skript ist so aufgebaut, dass es sofort ohne Parameter lauffaehig ist.
    Gleichzeitig kann die Evaluation ueber Optionen wie Datensatzpfad, Modell,
    Judge-Modell oder Top-K flexibel angepasst werden, ohne dass der Code
    veraendert werden muss.
    """
    parser = argparse.ArgumentParser(
        description="Bewertet die bestehende HsH-RAG-Pipeline gegen einen JSONL-Datensatz.",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET_PATH,
        help="Pfad zur JSONL-Datei mit den Eval-Beispielen.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=RAG_TOP_K,
        help="Wie viele Retrieval-Treffer fuer jede Frage verwendet werden sollen.",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Explizites LLM fuer die Antwortgenerierung. Ueberschreibt RAG_EVAL_MODEL.",
    )
    parser.add_argument(
        "--judge",
        action="store_true",
        help="Optional ein LLM als Judge fuer qualitative Zusatzscores verwenden.",
    )
    parser.add_argument(
        "--judge-model",
        default="",
        help="Explizites Judge-Modell. Ueberschreibt RAG_JUDGE_MODEL.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optionaler expliziter Pfad fuer die JSON-Ergebnisdatei.",
    )
    return parser.parse_args()


def first_non_empty(*values: Any) -> str:
    """Gibt den ersten sinnvollen String aus einer Kandidatenliste zurueck.

    Diese kleine Hilfsfunktion macht das Datensatzschema absichtlich tolerant:
    mehrere Alias-Feldnamen koennen auf dieselbe interne Struktur abgebildet
    werden.
    """
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def to_string_list(value: Any) -> list[str]:
    """Normalisiert Feldwerte zu einer String-Liste.

    Akzeptiert:
    - `None`
    - einzelne Strings
    - Listen/Tuples/Sets mit gemischten Werten

    Dadurch kann der Datensatz spaeter ohne grossen Umbau wachsen.
    """
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, (list, tuple, set)):
        result = []
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
        return result
    text = str(value).strip()
    return [text] if text else []


def normalize_example(raw: dict[str, Any], line_number: int) -> dict[str, Any]:
    """Ueberfuehrt ein rohes JSON-Objekt in ein stabiles internes Eval-Schema.

    Pflicht ist nur eine Frage. Alles andere ist optional und wird nur dann
    fuer Kennzahlen herangezogen, wenn es im Datensatz wirklich vorhanden ist.
    """
    question = first_non_empty(
        raw.get("question"),
        raw.get("query"),
        raw.get("prompt"),
    )
    if not question:
        raise ValueError(
            f"Zeile {line_number}: Es wurde keine Frage gefunden "
            f"(erwartet z.B. `question`, `query` oder `prompt`)."
        )

    should_answer = raw.get("should_answer")
    if isinstance(should_answer, str):
        should_answer = should_answer.strip().lower() in {"1", "true", "ja", "yes"}

    return {
        "id": first_non_empty(raw.get("id")) or f"row-{line_number}",
        "category": first_non_empty(raw.get("category")),
        "question": question,
        "ground_truth": first_non_empty(
            raw.get("ground_truth"),
            raw.get("expected_answer"),
            raw.get("reference_answer"),
        ),
        "expected_urls": to_string_list(
            raw.get("expected_urls") or raw.get("gold_urls") or raw.get("relevant_urls")
        ),
        "required_facts": to_string_list(
            raw.get("required_facts")
            or raw.get("expected_phrases")
            or raw.get("keywords")
            or raw.get("must_include")
        ),
        "faculty": first_non_empty(raw.get("faculty"), raw.get("fakultaet")),
        "should_answer": should_answer,
        "meta": raw,
    }


def load_dataset(dataset_path: Path) -> list[dict[str, Any]]:
    """Laedt den JSONL-Datensatz und validiert jede Zeile einzeln.

    Leere Zeilen werden ignoriert. Fehlerhafte Zeilen fuehren bewusst zu einer
    klaren Exception mit Zeilennummer, damit Datensatzprobleme frueh sichtbar
    werden.
    """
    if not dataset_path.exists():
        raise FileNotFoundError(f"Datensatz nicht gefunden: {dataset_path}")

    examples: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(dataset_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Zeile {line_number}: Ungueltiges JSON ({exc})") from exc
        if not isinstance(raw, dict):
            raise ValueError(f"Zeile {line_number}: Jede JSONL-Zeile muss ein Objekt sein.")
        examples.append(normalize_example(raw, line_number))
    return examples


def print_empty_dataset_hint(dataset_path: Path) -> None:
    """Gibt eine freundliche Anleitung aus, wenn der Datensatz noch leer ist."""
    print(f"Der Datensatz ist noch leer: {dataset_path}")
    print()
    print("Beispiel fuer eine gueltige JSONL-Zeile:")
    print(
        '{"id":"q001","category":"bewerbung","question":"Wie beantrage ich eine Beurlaubung?",'
        '"reference_answer":"Expected answer here.",'
        '"required_facts":["fact 1","fact 2"]}'
    )
    print()
    print("Du kannst spaeter einfach weitere Zeilen anhaengen. Der Code muss dafuer nicht angepasst werden.")


def normalize_url(url: str) -> str:
    """Normalisiert URLs fuer robuste Vergleiche zwischen Golddaten und Treffern.

    Entfernt Query-Parameter, Fragmente und ueberfluessige Trailing-Slashes, damit
    geringfuegige Formatunterschiede nicht zu falschen Fehlbewertungen fuehren.
    """
    text = url.strip()
    if not text:
        return ""
    parts = urlsplit(text)
    cleaned_path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), cleaned_path, "", ""))


def normalize_text(text: str) -> str:
    """Normalisiert Text fuer einfache string- und tokenbasierte Metriken."""
    tokens = WORD_RE.findall(text.casefold())
    return " ".join(tokens)


def token_f1(prediction: str, reference: str) -> float | None:
    """Berechnet ein einfaches tokenbasiertes F1-Mass.

    Dieses Mass ist bewusst simpel gehalten: Es ist schnell, transparent und
    benoetigt keine Zusatzbibliotheken. Wenn keine Referenzantwort vorhanden ist,
    wird `None` zurueckgegeben.
    """
    pred_norm = normalize_text(prediction)
    ref_norm = normalize_text(reference)
    if not ref_norm:
        return None
    if not pred_norm:
        return 0.0

    pred_counter = Counter(pred_norm.split())
    ref_counter = Counter(ref_norm.split())
    overlap = sum((pred_counter & ref_counter).values())
    if overlap == 0:
        return 0.0

    precision = overlap / sum(pred_counter.values())
    recall = overlap / sum(ref_counter.values())
    return 2 * precision * recall / (precision + recall)


def fact_hit_details(text: str, required_facts: list[str]) -> dict[str, Any]:
    """Prueft, welche geforderten Fakten in einem Text explizit auftauchen.

    Die gleiche Logik wird sowohl auf den Retrieval-Kontext als auch auf die
    Modellantwort angewendet. So lassen sich Retrieval-Abdeckung und
    Antwortqualitaet mit demselben Datensatzschema messen.
    """
    if not required_facts:
        return {
            "matched_required_facts": [],
            "missing_required_facts": [],
            "required_fact_hit_ratio": None,
        }

    answer_norm = normalize_text(text)
    if not answer_norm:
        return {
            "matched_required_facts": [],
            "missing_required_facts": required_facts,
            "required_fact_hit_ratio": 0.0,
        }

    matched = []
    missing = []
    for fact in required_facts:
        if normalize_text(fact) in answer_norm:
            matched.append(fact)
        else:
            missing.append(fact)

    return {
        "matched_required_facts": matched,
        "missing_required_facts": missing,
        "required_fact_hit_ratio": len(matched) / len(required_facts),
    }


def safe_mean(values: list[float | None]) -> float | None:
    """Bildet den Mittelwert ueber alle vorhandenen Werte und ignoriert `None`."""
    usable = [value for value in values if value is not None]
    if not usable:
        return None
    return sum(usable) / len(usable)


def build_faculty_filter(faculty: str) -> qmodels.Filter | None:
    """Erzeugt denselben Fakultaeitsfilter wie die Web-App.

    Wenn eine Fakultät vorgegeben ist, werden sowohl Treffer dieser Fakultät als
    auch fakultätsuebergreifende Dokumente ohne Zuordnung (`faculty == ""`)
    zugelassen.
    """
    if not faculty:
        return None

    return qmodels.Filter(
        should=[
            qmodels.FieldCondition(
                key="faculty",
                match=qmodels.MatchValue(value=faculty),
            ),
            qmodels.FieldCondition(
                key="faculty",
                match=qmodels.MatchValue(value=""),
            ),
        ],
    )


def load_qdrant_client() -> QdrantClient:
    """Stellt die Verbindung zu Qdrant her und prueft sie sofort."""
    client = QdrantClient(url=QDRANT_URL, timeout=10)
    client.get_collections()
    return client


def load_dense_embedder() -> TextEmbedding:
    """Laedt das Dense-Embedding-Modell der bestehenden RAG-Pipeline."""
    return TextEmbedding(model_name=EMBED_MODEL)


def load_sparse_embedder() -> SparseTextEmbedding:
    """Laedt das BM25-Sparse-Modell der bestehenden RAG-Pipeline."""
    return SparseTextEmbedding(model_name=SPARSE_MODEL)


def load_reranker():
    """Laedt optional denselben Reranker wie `hybrid_search.py`.

    Wenn das Reranker-Modell lokal nicht verfuegbar ist, faellt die Evaluation
    automatisch auf die Basis-Retrieval-Pipeline ohne Reranking zurueck.
    """
    if not USE_RERANKER:
        return None
    try:
        from fastembed import TextCrossEncoder

        return TextCrossEncoder(model_name=RERANKER_MODEL)
    except Exception as exc:
        print(f"Reranker nicht verfuegbar, Evaluation laeuft ohne Reranking weiter: {exc}")
        return None


def resolve_model_name(
    client: OpenAI,
    cli_value: str,
    env_var: str,
    available_models: list[str] | None = None,
) -> tuple[str, str]:
    """Waehlt das Modell fuer die Evaluation nachvollziehbar und transparent aus.

    Prioritaet:
    1. expliziter CLI-Wert
    2. Umgebungsvariable
    3. erstes verfuegbares Modell aus `REPO_MODEL_PREFERENCES`
    4. sonst erstes Modell aus der Serverliste
    """
    requested = cli_value.strip() or os.getenv(env_var, "").strip()
    if available_models is None:
        available_models = get_available_models(client)

    if requested:
        if requested in available_models:
            return requested, f"explizit gesetzt ({env_var} oder CLI)"
        return requested, (
            f"explizit gesetzt, aber nicht in der aktuellen Modellliste gefunden; "
            f"es wird trotzdem versucht"
        )

    for candidate in REPO_MODEL_PREFERENCES:
        if candidate in available_models:
            return candidate, "automatisch aus den im Repo hinterlegten Modell-Praeferenzen gewaehlt"

    if not available_models:
        raise RuntimeError("Die Modellliste der GWDG-API ist leer.")

    return available_models[0], "erstes verfuegbares Modell der GWDG-API"


def extract_source_urls(results: list[dict[str, Any]]) -> list[str]:
    """Extrahiert die Quell-URLs aus den Retrieval-Treffern."""
    urls = []
    for result in results:
        payload = result.get("payload") or {}
        url = str(payload.get("source_url", "")).strip()
        if url:
            urls.append(url)
    return urls


def evaluate_retrieval(
    results: list[dict[str, Any]],
    expected_urls: list[str],
) -> dict[str, Any]:
    """Berechnet URL-basierte Retrieval-Kennzahlen fuer ein Beispiel."""
    retrieved_urls = extract_source_urls(results)
    normalized_retrieved = {normalize_url(url) for url in retrieved_urls if url}
    normalized_expected = [normalize_url(url) for url in expected_urls if normalize_url(url)]

    url_hits = [
        expected_url
        for expected_url in normalized_expected
        if expected_url in normalized_retrieved
    ]

    if normalized_expected:
        retrieval_hit = bool(url_hits)
        retrieval_url_recall = len(url_hits) / len(normalized_expected)
    else:
        retrieval_hit = None
        retrieval_url_recall = None

    return {
        "retrieved_urls": retrieved_urls,
        "retrieval_hit": retrieval_hit,
        "retrieval_url_recall": retrieval_url_recall,
        "matched_expected_urls": url_hits,
    }


def build_judge_messages(
    example: dict[str, Any],
    context: str,
    answer: str,
    retrieval_metrics: dict[str, Any],
) -> list[dict[str, str]]:
    """Erstellt den Prompt fuer die optionale LLM-as-a-Judge-Bewertung."""
    expected_urls = example["expected_urls"] or []
    required_facts = example["required_facts"] or []
    ground_truth = example["ground_truth"] or ""

    user_content = (
        f"Kategorie:\n{example['category'] or '(keine Kategorie angegeben)'}\n\n"
        f"Frage:\n{example['question']}\n\n"
        f"Referenzantwort:\n{ground_truth or '(keine Referenzantwort vorhanden)'}\n\n"
        f"Geforderte Fakten:\n{json.dumps(required_facts, ensure_ascii=False)}\n\n"
        f"Erwartete URLs:\n{json.dumps(expected_urls, ensure_ascii=False)}\n\n"
        f"Retrieval-Kennzahlen:\n{json.dumps(retrieval_metrics, ensure_ascii=False, indent=2)}\n\n"
        f"RAG-Kontext:\n{context or '(kein Kontext gefunden)'}\n\n"
        f"Modellantwort:\n{answer or '(keine Antwort erzeugt)'}"
    )
    return [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


def parse_judge_response(text: str) -> dict[str, Any]:
    """Extrahiert das JSON-Objekt aus der Judge-Antwort."""
    raw = text.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError(f"Judge-Antwort ist kein JSON: {raw}")
        parsed = json.loads(match.group(0))

    if not isinstance(parsed, dict):
        raise ValueError("Judge-Antwort ist kein JSON-Objekt.")

    return {
        "correctness": float(parsed.get("correctness", 0.0)),
        "groundedness": float(parsed.get("groundedness", 0.0)),
        "completeness": float(parsed.get("completeness", 0.0)),
        "verdict": str(parsed.get("verdict", "")).strip(),
        "reason": str(parsed.get("reason", "")).strip(),
    }


def maybe_judge_answer(
    client: OpenAI,
    judge_model: str,
    example: dict[str, Any],
    context: str,
    answer: str,
    retrieval_metrics: dict[str, Any],
) -> dict[str, Any] | None:
    """Fuehrt optional eine qualitative Zusatzbewertung mit einem Judge-LLM aus."""
    if not answer:
        return None

    messages = build_judge_messages(example, context, answer, retrieval_metrics)
    judge_answer, judge_reasoning = ask_llm(client, judge_model, messages)
    parsed = parse_judge_response(judge_answer)
    parsed["raw_answer"] = judge_answer
    if judge_reasoning:
        parsed["reasoning"] = judge_reasoning
    return parsed


def evaluate_example(
    example: dict[str, Any],
    rag_client: OpenAI,
    rag_model: str,
    qdrant_client: QdrantClient,
    dense_embedder: TextEmbedding,
    sparse_embedder: SparseTextEmbedding,
    reranker,
    top_k: int,
    judge_client: OpenAI | None = None,
    judge_model: str | None = None,
) -> dict[str, Any]:
    """Bewertet ein einzelnes Datensatz-Beispiel komplett end-to-end.

    Die Funktion fuehrt Retrieval, Kontextaufbau, Antwortgenerierung und
    Kennzahlenberechnung in genau der Reihenfolge aus, in der auch das
    eigentliche RAG-System arbeitet.
    """
    faculty_filter = build_faculty_filter(example["faculty"])
    results = perform_hybrid_search(
        qdrant_client,
        dense_embedder,
        sparse_embedder,
        example["question"],
        top_k=top_k,
        query_filter=faculty_filter,
        reranker=reranker,
    )
    context = build_rag_context(results) if results else ""
    retrieval_metrics = evaluate_retrieval(results, example["expected_urls"])
    context_fact_metrics = fact_hit_details(context, example["required_facts"])

    answer = ""
    reasoning = ""
    messages: list[dict[str, str]] = []

    # Der eigentliche CLI-Chatbot springt bei komplett leerem Retrieval aus der
    # Schleife heraus. Hier wird dieses Verhalten bewusst beibehalten.
    if results:
        messages = build_rag_messages(example["question"], context)
        answer, reasoning = ask_llm(rag_client, rag_model, messages)

    lexical_f1 = token_f1(answer, example["ground_truth"])
    answer_fact_metrics = fact_hit_details(answer, example["required_facts"])
    no_info_expected = example["should_answer"] is False
    returned_no_info = normalize_text(answer) == normalize_text(NO_INFO_ANSWER)

    judge_metrics = None
    if judge_client is not None and judge_model:
        judge_metrics = maybe_judge_answer(
            judge_client,
            judge_model,
            example,
            context,
            answer,
            retrieval_metrics,
        )

    return {
        "id": example["id"],
        "category": example["category"],
        "question": example["question"],
        "faculty": example["faculty"],
        "ground_truth": example["ground_truth"],
        "expected_urls": example["expected_urls"],
        "required_facts": example["required_facts"],
        "should_answer": example["should_answer"],
        "retrieval": {
            **retrieval_metrics,
            **context_fact_metrics,
            "top_k": top_k,
            "result_count": len(results),
        },
        "answer": {
            "text": answer,
            "reasoning": reasoning,
            "generated": bool(answer),
            "returned_no_info_answer": returned_no_info,
            "no_info_expected": no_info_expected,
            "token_f1": lexical_f1,
            **answer_fact_metrics,
        },
        "messages": messages,
        "context": context,
        "judge": judge_metrics,
    }


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Verdichtet alle Einzelresultate zu einem kompakten Gesamtbericht."""
    retrieval_hits = [item["retrieval"]["retrieval_hit"] for item in results]
    retrieval_recalls = [item["retrieval"]["retrieval_url_recall"] for item in results]
    context_fact_scores = [item["retrieval"]["required_fact_hit_ratio"] for item in results]
    token_f1_scores = [item["answer"]["token_f1"] for item in results]
    answer_fact_scores = [item["answer"]["required_fact_hit_ratio"] for item in results]
    judge_correctness = [
        item["judge"]["correctness"] if item.get("judge") else None
        for item in results
    ]
    judge_groundedness = [
        item["judge"]["groundedness"] if item.get("judge") else None
        for item in results
    ]
    judge_completeness = [
        item["judge"]["completeness"] if item.get("judge") else None
        for item in results
    ]

    hit_values = [1.0 for value in retrieval_hits if value is True]
    miss_values = [0.0 for value in retrieval_hits if value is False]

    return {
        "examples": len(results),
        "generated_answers": sum(1 for item in results if item["answer"]["generated"]),
        "retrieval_hit_rate": safe_mean(hit_values + miss_values),
        "avg_retrieval_url_recall": safe_mean(retrieval_recalls),
        "avg_context_fact_hit_ratio": safe_mean(context_fact_scores),
        "avg_answer_token_f1": safe_mean(token_f1_scores),
        "avg_answer_fact_hit_ratio": safe_mean(answer_fact_scores),
        "avg_judge_correctness": safe_mean(judge_correctness),
        "avg_judge_groundedness": safe_mean(judge_groundedness),
        "avg_judge_completeness": safe_mean(judge_completeness),
    }


def format_metric(value: float | None) -> str:
    """Formatiert Kennzahlen fuer die Konsole."""
    if value is None:
        return "n/a"
    return f"{value:.3f}"


def build_output_path(cli_output: Path | None) -> Path:
    """Erzeugt einen sinnvollen Dateinamen fuer die JSON-Ausgabe."""
    if cli_output is not None:
        return cli_output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return RESULTS_DIR / f"rag_eval_{timestamp}.json"


def save_results(
    output_path: Path,
    summary: dict[str, Any],
    metadata: dict[str, Any],
    results: list[dict[str, Any]],
) -> None:
    """Speichert die komplette Evaluation als JSON-Datei."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": metadata,
        "summary": summary,
        "results": results,
    }
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_summary(summary: dict[str, Any], results: list[dict[str, Any]], output_path: Path) -> None:
    """Gibt einen kompakten, gut lesbaren Konsolenbericht aus."""
    print()
    print("=" * 72)
    print("RAG-Evaluation abgeschlossen")
    print("=" * 72)
    print(f"Beispiele                 : {summary['examples']}")
    print(f"Antworten generiert       : {summary['generated_answers']}")
    print(f"Retrieval-Hit-Rate        : {format_metric(summary['retrieval_hit_rate'])}")
    print(f"Ø URL-Recall              : {format_metric(summary['avg_retrieval_url_recall'])}")
    print(f"Ø Kontext-Fact-Hit-Ratio  : {format_metric(summary['avg_context_fact_hit_ratio'])}")
    print(f"Ø Answer Token-F1         : {format_metric(summary['avg_answer_token_f1'])}")
    print(f"Ø Answer-Fact-Hit-Ratio   : {format_metric(summary['avg_answer_fact_hit_ratio'])}")
    if summary["avg_judge_correctness"] is not None:
        print(f"Ø Judge Correctness       : {format_metric(summary['avg_judge_correctness'])}")
        print(f"Ø Judge Groundedness      : {format_metric(summary['avg_judge_groundedness'])}")
        print(f"Ø Judge Completeness      : {format_metric(summary['avg_judge_completeness'])}")
    print(f"JSON-Ergebnisdatei        : {output_path}")
    print()

    for item in results:
        retrieval_hit = item["retrieval"]["retrieval_hit"]
        hit_label = "n/a" if retrieval_hit is None else ("hit" if retrieval_hit else "miss")
        print(
            f"[{item['id']}] {hit_label} | "
            f"token_f1={format_metric(item['answer']['token_f1'])} | "
            f"context_facts={format_metric(item['retrieval']['required_fact_hit_ratio'])} | "
            f"answer_facts={format_metric(item['answer']['required_fact_hit_ratio'])} | "
            f"frage={item['question']}"
        )


def main() -> None:
    """Startet die komplette Evaluation von Datensatz bis Ergebnisdatei."""
    args = parse_args()

    examples = load_dataset(args.dataset)
    if not examples:
        print_empty_dataset_hint(args.dataset)
        return

    print(f"Datensatz geladen: {args.dataset}")
    print(f"Anzahl Beispiele: {len(examples)}")
    print()
    print("Dieses Skript nutzt dieselbe GWDG/OpenAI-kompatible LLM-Anbindung wie das Repo.")
    print(f"Modellwechsel: --model <name> oder {MODEL_OVERRIDE_ENV}=<name>")
    if args.judge:
        print(f"Judge-Modell wechseln: --judge-model <name> oder {JUDGE_MODEL_ENV}=<name>")
    print()

    rag_client = build_client()
    available_models = get_available_models(rag_client)
    rag_model, rag_reason = resolve_model_name(
        rag_client,
        args.model,
        MODEL_OVERRIDE_ENV,
        available_models=available_models,
    )
    print(f"Eval-Modell: {rag_model} ({rag_reason})")

    judge_client = None
    judge_model = None
    if args.judge:
        judge_client = rag_client
        judge_model, judge_reason = resolve_model_name(
            judge_client,
            args.judge_model,
            JUDGE_MODEL_ENV,
            available_models=available_models,
        )
        print(f"Judge-Modell: {judge_model} ({judge_reason})")
    print()

    print(f"Lade Embedding-Modell '{EMBED_MODEL}' …")
    dense_embedder = load_dense_embedder()
    print(f"Lade Sparse-Modell '{SPARSE_MODEL}' …")
    sparse_embedder = load_sparse_embedder()
    print("Verbinde mit Qdrant …")
    qdrant_client = load_qdrant_client()
    reranker = load_reranker()
    print()

    results = []
    for index, example in enumerate(examples, 1):
        print(f"[{index}/{len(examples)}] Evaluiere: {example['id']} — {example['question']}")
        result = evaluate_example(
            example=example,
            rag_client=rag_client,
            rag_model=rag_model,
            qdrant_client=qdrant_client,
            dense_embedder=dense_embedder,
            sparse_embedder=sparse_embedder,
            reranker=reranker,
            top_k=args.top_k,
            judge_client=judge_client,
            judge_model=judge_model,
        )
        results.append(result)

    summary = summarize_results(results)
    output_path = build_output_path(args.output)
    metadata = {
        "dataset": str(args.dataset),
        "top_k": args.top_k,
        "eval_model": rag_model,
        "judge_enabled": args.judge,
        "judge_model": judge_model,
        "embed_model": EMBED_MODEL,
        "sparse_model": SPARSE_MODEL,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    save_results(output_path, summary, metadata, results)
    print_summary(summary, results, output_path)


if __name__ == "__main__":
    main()
