# RAGHSH — RAG-System für die Hochschule Hannover

**RAGHSH** ist ein vollständiges **Retrieval-Augmented Generation (RAG)**-System, das Fragen zur Hochschule Hannover ausschließlich auf Basis offizieller Dokumente beantwortet. Es kombiniert einen automatischen Web-Spider mit einer Vektor-Datenbank, einem semantischen Reranker und einem großen Sprachmodell (LLM) der GWDG ChatAI API.

---

## Inhaltsverzeichnis

1. [Konzept: Was ist RAG und warum?](#konzept-was-ist-rag-und-warum)
2. [Systemübersicht](#systemübersicht)
3. [Verzeichnisstruktur](#verzeichnisstruktur)
4. [Abhängigkeiten und Bibliotheken](#abhängigkeiten-und-bibliotheken)
5. [Einrichtung](#einrichtung)
6. [Nutzung — Schritt für Schritt](#nutzung--schritt-für-schritt)
7. [Programmübersicht](#programmübersicht)
8. [Technische Architektur](#technische-architektur)
9. [Konfigurationsparameter](#konfigurationsparameter)
10. [Ideen zur Weiterentwicklung](#ideen-zur-weiterentwicklung)

---

## Konzept: Was ist RAG und warum?

### Das Problem mit reinen LLMs

Große Sprachmodelle wie GPT-4 oder Llama sind auf riesigen Textmengen trainiert und können fließend antworten — aber sie haben fundamentale Schwächen für institutionelle Wissenssysteme:

- **Halluzinierung**: LLMs erfinden plausibel klingende, aber falsche Fakten
- **Wissensstichtag**: Das Trainingskorpus endet zu einem bestimmten Datum; aktuelle Änderungen (Prüfungsordnungen, Fristen, Ansprechpartner) sind unbekannt
- **Fehlende Spezifität**: Allgemeine Informationen zur Hochschule Hannover sind im Training kaum vorhanden
- **Keine Quellenangaben**: Woher kommt die Information? Lässt sich die Aussage nachvollziehen?

### Die RAG-Lösung

**Retrieval-Augmented Generation** löst diese Probleme durch eine zweistufige Architektur:

```
Nutzerfrage
    │
    ▼
[Stufe 1: Retrieval]
Suche in der Vektordatenbank nach den
relevantesten Textstellen aus offiziellen
HsH-Dokumenten (Hybrid-Suche: Dense + BM25)
    │
    ▼
[Stufe 2: Generation]
LLM erhält Frage + Kontext und darf
NUR auf Basis dieser Textstellen antworten
    │
    ▼
Faktentreue Antwort mit Quellenangaben
```

Das LLM fungiert dabei als **intelligenter Leser und Formulierer**, nicht als Wissensquelle. Die Wissensbasis bleibt jederzeit aktualisierbar und nachvollziehbar.

### Hybrid-Suche: Dense + Sparse Vectors

Dieses System verwendet zwei komplementäre Suchmethoden, die per **Reciprocal Rank Fusion (RRF)** kombiniert werden:

| Methode | Stärke | Schwäche |
|---------|--------|----------|
| **Dense Search** (Jina Embeddings) | Semantisches Verstehen, Synonyme, Paraphrasen | Exakte Bezeichnungen können verloren gehen |
| **BM25 Sparse Search** | Exakte Schlüsselwörter, Modulnummern, Namen | Kein semantisches Verständnis |

**Beispiel:** Die Frage „Wie unterbreche ich mein Studium?" findet über Dense Search semantisch verwandte Texte über „Beurlaubung", die das Wort „Unterbrechung" nicht enthalten. Über BM25 findet die Suche Texte mit dem exakten Begriff „Beurlaubungsantrag".

### Reranking: die dritte Qualitätsstufe

Nach der RRF-Fusion werden die Ergebnisse einem **Cross-Encoder-Reranker** übergeben (`jinaai/jina-reranker-v2-base-multilingual`). Anders als Embedding-Modelle, die Dokument und Anfrage separat kodieren, bewertet ein Cross-Encoder jedes (Frage, Passage)-Paar gemeinsam — diese direkte Interaktion ermöglicht präzisere Relevanzurteile auf Kosten von mehr Rechenzeit.

### Context Augmentation

Texte werden in Chunks aufgeteilt, die an Grenzen „abgeschnitten" werden können. RAGHSH lädt für die Top-3-Treffer automatisch die benachbarten Chunks (vorheriger und nachfolgender) nach und hängt sie an den Kerntext an — damit gehen keine Informationen an Chunk-Grenzen verloren.

Zusätzlich gibt es eine **begrenzte zweite Retrieval-Runde**, wenn der erste Kontext erkennbar unvollständig ist. Dann fordert der Chatbot gezielt mehr Kontext an, z.B. Nachbar-Chunks, einen ganzen Abschnitt oder eine zweite Suche für eine fehlende Vergleichsseite. So bleibt der Standard-Kontext klein, ohne bei Regelwerken, Abkürzungen oder Vergleichsfragen vorschnell zu halluzinieren.

---

## Systemübersicht

```
Phase 1: Datensammlung
  main.py / resume_crawler.py  →  data/ingested/*.md
  (Web-Spider: HTML + PDF → Markdown mit YAML-Header)

Phase 1b: Qualitätsprüfung
  check_quality.py  →  Audit des Rohkorpus
  (bewertet Dateien, zeigt Sprache, Score und Problemgruende)

Phase 1c: Kuratierung und Organisation
  clean_corpus.py  →  data/curated/*.md + data/curated_report.json
  (entfernt schlechte Links/Boilerplate, markiert Sprache, Gruppen, Topics)

Phase 2a: Vektorisierung auf dem HPC-Cluster  [empfohlen für große Datenmengen]
  hpc_vectorizer.py  →  hsh_vectors.parquet
  (Dense + BM25 Sparse Vectors; bevorzugt data/curated, faellt sonst auf data/ingested zurueck)

Phase 2b: Sparse-Anreicherung lokal  [Fallback für ältere Parquet-Dateien]
  enrich_sparse.py  →  hsh_vectors_enriched.parquet

Phase 3: Datenbank befüllen
  local_importer.py  →  Qdrant-Collection 'hsh_knowledge'
  (erkennt automatisch: enriched > plain Parquet)

Phase 4: Suche testen (optional, CLI)
  hybrid_search.py  →  Interaktive Hybrid-Suche ohne LLM

Phase 5a: Web-App
  hsh_web_app.py (Streamlit)  →  Chatbot mit Rollen- und Fakultätsfilter

Phase 5b: CLI-Chatbot
  hsh_chatbot.py  →  Interaktiver Terminal-Chatbot

Hilfsprogramme:
  corpus_quality.py  →  gemeinsame Bewertungs-/Kuratierungslogik
  check_quality.py   →  read-only Qualitätsprüfung der Markdown-Dateien
  delete_qdrant.py   →  Collection zurücksetzen (nach Schema-Änderungen)
```

---

## Verzeichnisstruktur

```
RAGHSH/
├── docker-compose.yml               # Qdrant-Vektordatenbank als Docker-Container
├── qdrant_data/                     # Persistenter Speicher für Qdrant (Docker Volume)
└── hsh_scraper/
    ├── main.py                      # Phase 1: Web-Spider (BFS-Crawler)
    ├── resume_crawler.py            # Phase 1b: Spider fortsetzen / Lücken schließen
    ├── url_filter.py                # Gemeinsame RAG-URL-Filterung + SQLite-Ablage
    ├── crawl_helpers.py             # Gemeinsame Crawl-Utilities (Sitemaps, Quality Gates, Reporting)
    ├── corpus_quality.py            # Geteilte Quality-/Cleaning-Logik für Roh- und Kurationskorpus
    ├── clean_corpus.py              # Phase 1c: Rohkorpus bereinigen und organisieren
    ├── hpc_vectorizer.py            # Phase 2a: HPC-Vektorisierung (Dense + BM25 → Parquet)
    ├── enrich_sparse.py             # Phase 2b: BM25-Spalten lokal hinzufügen (Fallback)
    ├── local_importer.py            # Phase 3: Parquet → Qdrant
    ├── hybrid_search.py             # Phase 4: Hybrid-Suche (Dense + BM25 + Reranker)
    ├── rag_followup.py              # Bedarfsorientierte zweite Retrieval-Runde
    ├── hsh_web_app.py               # Phase 5a: Streamlit Web-App
    ├── hsh_chatbot.py               # Phase 5b: CLI-Chatbot
    ├── delete_qdrant.py             # Hilfsprogramm: Collection löschen und neu anlegen
    ├── check_quality.py             # Hilfsprogramm: Read-only Qualitätsprüfung der MD-Dateien
    ├── ingest_to_qdrant.py          # Ältere All-in-One Vektorisierung (superseded)
    ├── requirements.txt             # Python-Abhängigkeiten
    ├── .env                         # API-Schlüssel (nicht im Git!)
    ├── .env.example                 # Vorlage für .env
    ├── hsh_vectors.parquet          # HPC-Ausgabe (Dense + Sparse Vektoren)
    ├── hsh_vectors_enriched.parquet # Optional: lokal angereicherte Parquet-Datei
    └── data/
        ├── url_decisions.db         # SQLite-Historie der URL-Entscheidungen
        ├── curated/                 # Bereinigtes Korpus für die Vektorisierung
        │   └── YYYY-MM-DD_slug.md
        ├── curated_report.json      # Report der Kuratierungsentscheidung pro Datei
        └── ingested/                # Rohkorpus aus dem Crawl
            └── YYYY-MM-DD_slug.md
```

---

## Abhängigkeiten und Bibliotheken

### Infrastruktur

| Komponente | Beschreibung |
|---|---|
| **Docker** | Laufzeitumgebung für Qdrant |
| **Qdrant** (`qdrant/qdrant`) | Vektordatenbank, Port 6333 (HTTP/REST) und 6334 (gRPC) |
| **Python 3.12** | Laufzeitumgebung für alle Skripte |
| **GWDG ChatAI API** | OpenAI-kompatibler LLM-Dienst für Hochschulen |

### Python-Bibliotheken

| Bibliothek | Verwendung |
|---|---|
| **crawl4ai** | Asynchroner Web-Crawler mit JavaScript-Unterstützung (Playwright-Backend) |
| **pymupdf4llm** | PDF → LLM-optimiertes Markdown |
| **python-slugify** | URL-sichere Dateinamen aus URL-Pfaden |
| **openpyxl** | Excel-Fehlerbericht nach dem Crawl |
| **qdrant-client** | Python-Client für Qdrant (Upsert, Hybrid-Suche, Payload-Indizes) |
| **fastembed** | Lokale Embedding-Modelle ohne externe API — Dense (`jinaai/jina-embeddings-v3`), Sparse (`Qdrant/bm25`), Reranker (`jinaai/jina-reranker-v2-base-multilingual`) |
| **pyarrow** | Parquet-Lesen/-Schreiben mit Row-Group-Streaming |
| **langchain-text-splitters** | Zweistufiges Chunking: `MarkdownHeaderTextSplitter` + `RecursiveCharacterTextSplitter` |
| **streamlit** | Web-App-Framework für `hsh_web_app.py` |
| **openai** | OpenAI-kompatibler HTTP-Client für GWDG ChatAI |
| **python-dotenv** | Lädt den API-Schlüssel aus `.env` |
| **httpx** | Async-HTTP-Client für PDF-Downloads |

---

## Einrichtung

### 1. Voraussetzungen

- Docker und Docker Compose installiert
- Python 3.12 installiert
- GWDG ChatAI API-Schlüssel

### 2. Qdrant-Datenbank starten

```bash
cd RAGHSH
docker compose up -d
```

Prüfen ob Qdrant läuft:
```bash
curl http://localhost:6333/healthz
# {"title":"qdrant - vector search engine","version":"..."}
```

### 3. Python-Umgebung einrichten

```bash
cd hsh_scraper
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt

# Playwright-Browser für crawl4ai herunterladen:
playwright install chromium
```

### 4. API-Schlüssel konfigurieren

```bash
cp .env.example .env
# .env öffnen und GWDG_API_KEY eintragen
```

Inhalt der `.env`:
```ini
GWDG_API_KEY=dein-schluessel-hier
GWDG_API_BASE=https://chat-ai.academiccloud.de/v1
```

---

## Nutzung — Schritt für Schritt

### Phase 1: Website crawlen

```bash
python main.py
```

Crawlt `www.hs-hannover.de` per Breadth-First-Search (BFS). Jede Seite wird als Markdown-Datei mit YAML-Header gespeichert. Bereits frisch gecachte Seiten (< `MAX_AGE_DAYS` Tage) werden übersprungen.

Zusätzlich bewertet ein gemeinsamer RAG-Filter jede neu entdeckte URL, bevor sie in die Queue gelangt. Geblockt werden aktuell u.a.:

- der englische Bereich unter `/en` auf allen HsH-Subdomains
- Medien-Dateien wie Bilder, Audio und Video
- technische Assets wie CSS/JS/Archive
- nicht-oeffentliche App-/Login-Bereiche wie `moodle.hs-hannover.de` und `intranet.hs-hannover.de` sowie Auth-Pfade (`/login`, `/logout`, `/shibboleth`, `/saml`, `/oauth`)
- `fileadmin/_processed_`-Assets
- Office-Dokumente ohne Ingest-Support (`.docx`, `.pptx`, `.xlsx`, ...)
- offensichtlich kaputte URLs mit rohen Markdown-/Junk-Zeichen wie `*` oder `|`
- bekannte Backend-/Interndomains wie `serwiss.bib.hs-hannover.de` und `typo3backend-live.hs-hannover.de`

Jede Entscheidung wird in `data/url_decisions.db` gespeichert.

```
2026-03-14 [INFO] Crawling: https://www.hs-hannover.de/
2026-03-14 [INFO] Saved data/ingested/2026-03-14_index.md
...
2026-03-14 [INFO] Done. 847 succeeded, 3 failed, 0 skipped out of 850 URLs visited.
```

### Phase 1b: Crawler fortsetzen

```bash
python resume_crawler.py          # Analysiert und crawlt fehlende/veraltete URLs
python resume_crawler.py --dry-run  # nur Analyse, kein Crawlen
```

`resume_crawler.py` liest alle vorhandenen Markdown-Dateien, extrahiert darin enthaltene Links und crawlt nur Seiten, die fehlen oder veraltet sind. Ideal für inkrementelle Aktualisierungen.

Der gleiche RAG-Filter wird auch im Resume-Pfad verwendet. `--dry-run` zeigt dadurch nicht nur die Crawl-Kategorien (frisch / veraltet / fehlend), sondern auch eine Zusammenfassung der Filterentscheidungen inklusive Gruenden und Beispiel-URLs.

Die SQLite-Datei `data/url_decisions.db` wird bei Bedarf automatisch angelegt und fortlaufend aktualisiert.

### (Optional) Qualität prüfen

```bash
python check_quality.py
```

Gibt eine Tabelle aller Roh-Markdown-Dateien aus und nutzt dieselben Regeln wie die spätere Kuratierung:

```
Filename                          Words  Type    Lang   Score  Quality
───────────────────────────────────────────────────────────────────────
2026-03-14_index.md               1.234  html    de        96  OK
2026-03-14_preview-page.md           52  html    mixed     58  PRUEFEN
2026-03-14_exchange-info.md         410  html    en        25  PRUEFEN
```

Es werden u.a. bewertet:

- Mindesttextmenge für HTML/PDF
- Fehlerseitenmuster
- sprachlich gemischte oder englische Seiten
- Preview-/Backend-Links im Body
- ältere Duplikate desselben URL-Slugs

### Phase 1c: Korpus bereinigen und organisieren

```bash
python clean_corpus.py
```

`clean_corpus.py` liest `data/ingested/`, schreibt ein bereinigtes Korpus nach `data/curated/` und erzeugt einen JSON-Report in `data/curated_report.json`.

Bereinigungen und Anreicherungen:

- entfernt geblockte Preview-/Backend-Links direkt aus dem Markdown-Body
- normalisiert relative Links zu offiziellen absoluten URLs
- entfernt typische Boilerplate-Zeilen wie Teilen-/Scroll-Hinweise
- verwirft englische Seiten standardmäßig
- ergänzt Metadaten wie `language`, `quality_score`, `document_kind`, `source_family`, `document_group`, `topic_tags`

Optional mit eigenen Pfaden:

```bash
python clean_corpus.py \
  --input-dir data/ingested \
  --output-dir data/curated \
  --report-file data/curated_report.json
```

### Phase 2a: Vektorisierung auf dem HPC-Cluster (empfohlen)

```bash
# Auf dem HPC-Cluster (z.B. GWDG/KISSKI mit NVIDIA H100):
python hpc_vectorizer.py   →  hsh_vectors.parquet

# Datei auf lokalen Rechner übertragen:
scp hsh_vectors.parquet user@localhost:~/RAGHSH/hsh_scraper/
```

`hpc_vectorizer.py` erzeugt **beide** Vektortypen in einem Durchlauf und verwendet automatisch `data/curated/`, wenn dort bereits bereinigte Markdown-Dateien vorliegen. Falls nicht, fällt das Skript auf `data/ingested/` zurück.

Es erzeugt:
- Dense Embeddings (GPU-beschleunigt, Batch-Größe 64)
- BM25 Sparse Embeddings (CPU-only, Batch-Größe 256)
- Chunk-Metadaten für spätere Filterung und Gruppierung im Retrieval

Output: `hsh_vectors.parquet` (komprimiert mit ZSTD, enthält Dense-, Sparse- und Qualitätsmetadaten)

### Phase 2b: Sparse-Anreicherung lokal (Fallback)

```bash
python enrich_sparse.py   →  hsh_vectors_enriched.parquet
```

Wenn eine ältere `hsh_vectors.parquet` ohne Sparse-Spalten vorliegt (z.B. vom alten `ingest_to_qdrant.py`), berechnet dieses Skript die BM25-Vektoren lokal und schreibt eine neue Datei.

> **Hinweis:** `local_importer.py` erkennt automatisch, welche Datei vorliegt — `hsh_vectors_enriched.parquet` hat Vorrang vor `hsh_vectors.parquet`.

### Phase 3: Datenbank befüllen

```bash
python delete_qdrant.py   # Alte Collection löschen + neu mit Indizes anlegen
python local_importer.py  # Parquet-Datei in Qdrant hochladen
```

`delete_qdrant.py` ist nötig nach:
- Schema-Änderungen (z.B. neue Vektortypen)
- Komplettem Neucrawl
- Fehlerhafte Daten in der Datenbank

`local_importer.py` lädt die Daten in Batches von 256 Punkten hoch. Bei Unterbrechung kann `RESUME_FROM_ROW` gesetzt werden, um den Import fortzusetzen.

```
2026-03-14 [INFO] Parquet-Datei: hsh_vectors.parquet (245.3 MB, 28.451 Zeilen)
2026-03-14 [INFO] Collection 'hsh_knowledge' angelegt (dense=1024dim, sparse=BM25)
2026-03-14 [INFO]   Row-Group 1/847  [  0.1%]  256 Punkte hochgeladen (gesamt)
...
2026-03-14 [INFO] Fertig. 28.451 Punkte hochgeladen.
```

### Phase 4: Suche testen (optional)

```bash
python hybrid_search.py
```

Interaktive Hybrid-Suche ohne LLM. Nützlich zur Diagnose der Trefferqualität:

```
Frage> Bewerbungsfristen Bachelor Informatik

  ┌─ Treffer 1  (RRF-Score: 0.03226)
  │  URL      : https://www.hs-hannover.de/studium/bewerbung/...
  │  Fakultät : Fakultät IV
  │  Abschnitt: Bewerbung > Fristen
  │  Stand    : 2026-03-10
  │  Vorschau : Die Bewerbungsfrist für den Bachelorstudiengang...
  └──────────────────────────────────────────────────────────────
```

### Phase 5a: Web-App starten

```bash
streamlit run hsh_web_app.py
# → http://localhost:8501
```

Die Web-App bietet:
- **Rollenauswahl**: Studierender / Mitarbeitender / Lehrender / Besucher (passt den Ton des LLM an)
- **Fakultätsfilter**: Ergebnisse werden auf die gewählte Fakultät + fakultätsübergreifende Seiten (ohne Fakultätszuordnung) eingeschränkt
- **Streaming-Antworten** mit Quellenangaben und optionalem Denkprozess-Expander
- **Veralterungswarnung**: Falls eine Quelle älter als 6 Monate ist, empfiehlt das System Nachprüfung
- **Follow-up Retrieval**: bei unvollständigem Erstkontext kann gezielt weiterer Kontext nachgeladen werden

### Phase 5b: CLI-Chatbot

```bash
python hsh_chatbot.py
```

Startet eine interaktive Terminal-Session mit dynamischer Modellauswahl:

```
Modell wählen:
  [1] meta-llama-3.1-70b-instruct
  [2] deepseek-r1
  [3] gpt-4o
  ...
Auswahl (Enter = 1): 2

HsH-Chatbot bereit.  Strg+C oder 'exit' zum Beenden.

Frage> Wie beantrage ich eine Beurlaubung?
```

---

## Programmübersicht

### `main.py` — Web-Spider

Crawlt die gesamte HsH-Website per **Breadth-First-Search (BFS)**.

| Parameter | Standard | Beschreibung |
|---|---|---|
| `SEED_URLS` | `["https://www.hs-hannover.de/"]` | Startseiten |
| `MAX_PAGES` | `10.000` | Maximale Seitenanzahl |
| `ALLOWED_DOMAIN` | `hs-hannover.de` | Nur diese Domain und ihre Subdomains |
| `BLOCKED_DOMAINS` | `{"serwiss.bib.hs-hannover.de", "typo3backend-live.hs-hannover.de"}` | Geblockte Subdomains |
| `MAX_AGE_DAYS` | `7` | Cache-Alter in Tagen |
| `RATE_LIMIT_SECONDS` | `0.5` | Pause zwischen Requests |

- **HTML**: Crawl4AI (Playwright) mit CSS-Selektor `main, .content-main, #content, .frame-default`; boilerplate (Navigation, Header, Footer, Cookie-Banner) wird ausgeblendet
- **PDF**: httpx-Download + pymupdf4llm-Konvertierung
- **Dateiformat**: `YYYY-MM-DD_url-slug.md` mit YAML-Frontmatter (`source_url`, `title`, `crawl_date`, `content_type`)
- **RAG-Filter**: Neue Links werden vor dem Queueing durch `url_filter.py` bewertet und in `data/url_decisions.db` protokolliert
- **Sitemap-Seeding**: erkannte `sitemap.xml`-Dateien werden zusätzlich als Seed-Quelle genutzt
- **Soft-Priorisierung**: URLs werden als `allow_high_value`, `allow_low_value` oder `block` klassifiziert; High-Value-Links werden bevorzugt gecrawlt
- **Post-Crawl-Quality-Gate**: sehr kurze, nav-lastige oder offensichtliche Junk-Seiten werden nach der Extraktion noch verworfen

---

### `resume_crawler.py` — Crawler fortsetzen

Analysiert den Bestand der Markdown-Dateien und crawlt ergänzend:

| Parameter | Standard | Beschreibung |
|---|---|---|
| `MAX_PAGES` | `40.000` | Erhöhtes Limit für Resume |
| `BLOCKED_DOMAINS` | identisch mit `main.py` | Geblockte Subdomains |

Kategorisiert URLs in: frisch gecacht / veraltet / nur als Link bekannt, nicht gecrawlt.

Zusätzlich:

- bewertet `resume_crawler.py` alle gespeicherten `source_url`-Einträge und alle im Markdown gefundenen Links mit demselben RAG-Filter
- speichert die Entscheidungen in `data/url_decisions.db`
- zeigt bei `--dry-run` eine Filter-Zusammenfassung nach Gruenden

---

### `url_filter.py` — Gemeinsame URL-Policy

Zentrale Bewertungslogik fuer `main.py` und `resume_crawler.py`.

- normalisiert URLs strenger und entfernt Tracking-/Print-/Fragment-Varianten
- blockiert klar unnuetze RAG-Ziele wie Preview-/Backend-/Dev-Hosts, `/en`-Bereiche, Moodle-/Intranet-/Auth-Pfade, Medien-Dateien, technische Assets, `_processed_`-Dateien und bekannte Backend-Domains
- blockiert Low-Value-Pfade wie News-Archive, Galerie-/Tag-/Promo-Seiten deutlich aggressiver
- bewertet erlaubte Ziele als `allow_high_value` oder `allow_low_value`, damit Studium-/Bewerbungs-/Pruefungsseiten frueher gecrawlt werden
- verwendet zusaetzliche PDF-Heuristiken, um z.B. Ordnungen/Formulare/Faqs zu bevorzugen
- speichert jede Entscheidung in einer kleinen SQLite-Datenbank (`data/url_decisions.db`) inklusive Grund

---

### `hpc_vectorizer.py` — HPC-Vektorisierung

Erzeugt Dense + BM25 Sparse Vectors aus Markdown-Dateien und speichert sie als Parquet. Wenn `data/curated/` vorhanden und nicht leer ist, wird dieses bereinigte Korpus bevorzugt verarbeitet; andernfalls dient `data/ingested/` als Fallback. Alternativ kann per `RAG_SOURCE_DIR=/pfad/...` ein eigenes Quellverzeichnis gesetzt werden.

| Parameter | Standard | Beschreibung |
|---|---|---|
| `DENSE_MODEL` | `jinaai/jina-embeddings-v3` | 1024-dim multilinguales Embedding-Modell |
| `SPARSE_MODEL` | `Qdrant/bm25` | Statistisches BM25-Modell (CPU-only) |
| `CHUNK_SIZE` | `1.000` | Max. Zeichen pro Chunk |
| `CHUNK_OVERLAP` | `200` | Überlappung zwischen Chunks (20%) |
| `DENSE_BATCH_SIZE` | `64` | Chunks pro GPU-Embedding-Aufruf |
| `SPARSE_BATCH_SIZE` | `256` | Chunks pro BM25-Aufruf |
| `RESUME_FROM_FILE` | `1` | Dateinummer für Neustart nach Abbruch |

**Zweistufige Chunking-Strategie:**
1. `MarkdownHeaderTextSplitter` — teilt an `#`, `##`, `###`; Überschriften-Hierarchie wird als `section_heading`-Metadatum (`H1 > H2 > H3`) bewahrt
2. `RecursiveCharacterTextSplitter` — teilt zu große Abschnitte weiter

**Parquet-Schema (19 Spalten):**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `id` | string | UUID5 aus `source_url + chunk_index` (deterministisch) |
| `vector` | list\<float32\> | 1024-dim Dense-Einbettungsvektor |
| `source_url` | string | Ursprungs-URL |
| `title` | string | Seitentitel |
| `crawl_date` | string | ISO-8601-Datum |
| `content_type` | string | `html` oder `pdf` |
| `faculty` | string | Aus URL extrahiert: `/f1/`–`/f5/`, Subdomains |
| `language` | string | Sprachklassifikation aus der Kuratierung (`de`, `en`, `mixed`, `unknown`) |
| `quality_score` | string | Qualitätswert aus `clean_corpus.py` |
| `document_kind` | string | Z.B. `regulation`, `module_handbook`, `contact_service` |
| `source_family` | string | Grobe Zugehörigkeit, z.B. `faculty_4`, `internationales` |
| `document_group` | string | Feiner Gruppenschlüssel für zusammengehörige Dokumente |
| `topic_tags` | string | Mit `|` getrennte Themen-Tags, z.B. `bewerbung|rueckmeldung` |
| `section_heading` | string | Überschriften-Breadcrumb |
| `text` | string | Volltext des Chunks |
| `chunk_index` | int32 | Position im Dokument |
| `total_chunks` | int32 | Gesamtanzahl Chunks des Dokuments |
| `sparse_indices` | list\<int32\> | BM25 Token-IDs |
| `sparse_values` | list\<float32\> | BM25 Gewichte |

**Fakultätserkennung** aus der URL:
- Pfadbasiert: `/f1/` → `Fakultät I`, ..., `/f5/` → `Fakultät V`
- Subdomain-basiert: `karriere.*` → `Karriere`, `bibliothek.*` → `Bibliothek`, `international.*` → `International`

---

### `enrich_sparse.py` — Sparse-Anreicherung (Fallback)

Liest eine Dense-only-Parquet-Datei und berechnet BM25-Vektoren lokal.

| Parameter | Standard | Beschreibung |
|---|---|---|
| `INPUT_FILE` | `hsh_vectors.parquet` | Eingabe (Dense-only) |
| `OUTPUT_FILE` | `hsh_vectors_enriched.parquet` | Ausgabe (Dense + Sparse) |
| `SPARSE_BATCH_SIZE` | `256` | Chunks pro BM25-Aufruf |

---

### `local_importer.py` — Qdrant-Import

Lädt die Parquet-Datei in Qdrant. Erkennt automatisch:
1. `hsh_vectors_enriched.parquet` (bevorzugt)
2. `hsh_vectors.parquet` (Fallback)

| Parameter | Standard | Beschreibung |
|---|---|---|
| `UPLOAD_BATCH` | `256` | Punkte pro Upsert-Aufruf |
| `RESUME_FROM_ROW` | `0` | Neustart-Zeilenindex bei Abbruch |

**Collection-Schema:**
- Benannte Dense-Vektoren: `"dense"` (1024-dim, Cosine)
- Sparse-Vektoren: `"sparse"` (BM25)

**Payload-Indizes** (für effiziente Suche und Augmentation):
- `text` — Volltext-Index (MULTILINGUAL-Tokenizer: deutsches Stemming, Kompositaaufspaltung)
- `faculty` — Keyword-Index (Fakultätsfilter)
- `chunk_index` — Integer-Index (Context Augmentation)
- `source_url` — Keyword-Index (Context Augmentation + Dedup)
- `document_kind` — Keyword-Index (Regelwerk/Formular/FAQ gezielt filterbar)
- `document_group` — Keyword-Index (verwandte Dokumente gruppiert nutzbar)
- `language` — Keyword-Index (deutsch/englisch trennbar)

---

### `hybrid_search.py` — Hybrid-Suchpipeline

Hybrid-Suchpipeline mit Qdrant-nativer Fusion, Reranking und Nachbar-Augmentation.

| Parameter | Standard | Beschreibung |
|---|---|---|
| `CANDIDATE_LIMIT` | `100` | Kandidaten pro Sucharm (Dense + Sparse je 100) |
| `TOP_K` | `8` | Finale Ergebnisse nach URL-Dedup |
| `DEDUP_BUFFER` | `4` | Faktor vor URL-Dedup: 8 × 4 = 32 Rohergebnisse |
| `MAX_PER_URL` | `2` | Max. Chunks pro `source_url` nach Dedup |
| `USE_RERANKER` | `True` | Cross-Encoder-Reranking aktivieren |
| `AUGMENT_TOP_N` | `3` | Nachbar-Chunks für die Top-N Treffer laden |
| `BLOCKED_URL_PREFIXES` | `("https://serwiss.bib.", ...)` | Gefilterte URL-Präfixe |

**Pipeline-Schritte:**

```
1. Dense-Embedding der Anfrage  (task=retrieval.query)
2. Sparse-Embedding der Anfrage (BM25)
3. Qdrant-Prefetch + RRF-Fusion (ein Datenbankaufruf)
   ├── Dense-Arm: 100 Kandidaten
   └── Sparse-Arm: 100 Kandidaten
      → Qdrant-native RRF: score = Σ 1/(k + Rang)
4. Geblockte URLs herausfiltern
5. URL-Dedup: max. 2 Chunks pro source_url → 8 Treffer
6. Cross-Encoder-Reranking: jede (Frage, Passage) neu bewerten
7. Context Augmentation: für Top-3 Nachbar-Chunks nachladen
```

**`build_rag_context()`** formatiert die Ergebnisse für das LLM:
```
[Quelle 1] Titel
URL: https://...
Stand: 2026-03-14
Fakultät: Fakultät IV
Abschnitt: Prüfungen > Prüfungsformen

<Chunk-Text ggf. mit Nachbar-Chunks>
```

---

### `hsh_web_app.py` — Streamlit Web-App

| Parameter | Standard | Beschreibung |
|---|---|---|
| `RAG_TOP_K` | `6` | Kontext-Chunks pro Anfrage |
| `TEMPERATURE` | `0.0` | Deterministisch, keine Kreativitäts-Halluzinierung |

**Rollenanpassung:** Das LLM ändert seinen Sprachstil je nach Nutzerrolle (Studierender, Mitarbeitender, Lehrender, Besucher).

**Fakultätsfilter (OR-Logik):**
```
faculty == gewählte Fakultät  ODER  faculty == ""
```
Zentrale Einrichtungen (ohne Fakultätszuordnung) erscheinen immer — unabhängig vom Filter.

**Veralterungswarnung:** Wenn die älteste gefundene Quelle > 180 Tage alt ist, enthält der System-Prompt automatisch eine Empfehlung zur Nachprüfung.

**System-Prompt-Regeln:**
1. Antworten ausschließlich auf Basis des Kontexts
2. Keine Spekulation oder Erfindung
3. Bei fehlendem Kontext: definierte Standardantwort
4. Widersprüche zwischen Quellen explizit benennen
5. Alte Quellen (erkennbar am `Stand:`-Feld) kenntlich machen
6. Quellenangabe am Ende jeder Antwort (Titel, URL, Abschnitt, Datum)

---

### `hsh_chatbot.py` — CLI-Chatbot

| Parameter | Standard | Beschreibung |
|---|---|---|
| `EMBED_MODEL` | `jinaai/jina-embeddings-v3` | Dense-Embedding |
| `SPARSE_MODEL` | `Qdrant/bm25` | Sparse-Embedding |
| `RAG_TOP_K` | `4` | Kontext-Chunks pro Anfrage |
| `DEBUG_PROMPT` | `True` | Vollständigen LLM-Prompt ausgeben |

Dynamische Modellauswahl: Beim Start werden alle verfügbaren Modelle von der GWDG-API abgefragt. Reasoning-Modelle (DeepSeek R1 o.ä.) zeigen ihren Denkprozess in einem separaten `[Thinking]`-Block.

Zusätzlich nutzt der Chatbot eine **begrenzte Follow-up-Retrieval-Runde**: Wenn der erste Kontext für eine Definition, einen Vergleich oder einen Regelwerksausschnitt unvollständig ist, kann `rag_followup.py` gezielt mehr Nachbar-Chunks, einen Abschnitt oder eine zweite Suche anfordern. Für aktuelle Fragen wie „heute" wird dagegen bewusst nicht endlos nachgeladen.

---

### `delete_qdrant.py` — Collection zurücksetzen

Löscht die bestehende Collection vollständig und legt sie mit allen Payload-Indizes neu an. **Muss vor `local_importer.py` ausgeführt werden**, wenn sich das Schema geändert hat oder ein Neuimport gewünscht ist.

> ⚠️ Unwiderruflich — alle Vektoren und Metadaten gehen verloren.

---

### `check_quality.py` — Qualitätsprüfung

Analysiert alle Markdown-Dateien auf Qualitätsprobleme:

| Kriterium | Schwellwert |
|---|---|
| Mindestwörter (HTML) | 30 |
| Mindestwörter (PDF) | 50 |
| Erkannte Fehlermuster | „404", „Seite nicht gefunden", „Zugriff verweigert", … |
| Duplikate | Ältere Version desselben URL-Slugs |
| Sprachheuristik | `de`, `en`, `mixed`, `unknown` |
| Preview-/Backend-Links im Body | werden als Qualitätsproblem markiert |

### `clean_corpus.py` — Kuratierung des Rohkorpus

Transformiert `data/ingested/` in ein bereinigtes `data/curated/`.

- entfernt geblockte Links und offensichtliche Boilerplate
- ergänzt Qualitäts- und Gruppen-Metadaten
- verwirft problematische Dateien vor der Vektorisierung
- schreibt mit `data/curated_report.json` einen maschinenlesbaren Prüfbericht pro Datei

---

## Technische Architektur

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Nutzerfrage                                   │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│  hybrid_search.py — Hybrid-Suche + Reranking                         │
│                                                                      │
│  Anfrage → Dense-Embedding (Jina v3, 1024-dim)                       │
│  Anfrage → BM25-Sparse-Embedding (Qdrant/bm25)                       │
│                                                                      │
│  ┌──────────────────────────┐  ┌───────────────────────────────┐     │
│  │  Dense Prefetch          │  │  Sparse Prefetch (BM25)       │     │
│  │  using="dense", limit=100│  │  using="sparse", limit=100    │     │
│  └────────────┬─────────────┘  └──────────────┬────────────────┘     │
│               └────────────────┬──────────────┘                      │
│                                ▼                                     │
│              Qdrant-native RRF-Fusion (ein Roundtrip)                │
│                                │                                     │
│                                ▼                                     │
│              URL-/Host-Filter und Low-Value-Filter                   │
│                                │                                     │
│                                ▼                                     │
│              URL-Deduplizierung (max. 2 Chunks/URL)                  │
│                                │                                     │
│                                ▼                                     │
│              Cross-Encoder-Reranking (jina-reranker-v2)              │
│                                │                                     │
│                                ▼                                     │
│              Context Augmentation (Nachbar-Chunks Top-3)             │
│                                │                                     │
│              Top-8 Chunks mit erweitertem Kontext                   │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  hsh_web_app.py / hsh_chatbot.py — Prompt-Aufbau                     │
│                                                                      │
│  [System]  Rolle + Fakultätskontext + Regelwerk                      │
│            + ggf. Veralterungswarnung (>180 Tage)                    │
│                                                                      │
│  [User]    Kontext aus offiziellen HsH-Dokumenten:                   │
│            [Quelle 1] Titel | URL | Stand | Abschnitt | Text         │
│            ---                                                       │
│            [Quelle 2] ...                                            │
│            ---                                                       │
│            Frage: {nutzerfrage}                                      │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  │  optional bei unvollstaendigem Kontext
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  rag_followup.py — gezielte zweite Retrieval-Runde                  │
│  • neighbour_chunks / full_section / same_group_documents / new_search│
│  • maximal eine zusaetzliche Runde                                   │
│  • keine Endlosschleifen fuer aktuelle „heute"-Fragen                │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  GWDG ChatAI API (OpenAI-kompatibel)                                 │
│  Modelle: GPT-4o, Llama 3.3 70B, DeepSeek R1, …                     │
│  Temperature: 0.0 (deterministisch)                                  │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  Ausgabe                                                             │
│  • [Denkprozess] (nur Reasoning-Modelle, in Expander)               │
│  • Antworttext                                                       │
│  • Quellenangaben: Titel — URL — Abschnitt (Stand: Datum)           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Konfigurationsparameter

### Schnellreferenz: alle konfigurierbaren Werte

| Skript | Parameter | Standard | Bedeutung |
|--------|-----------|----------|-----------|
| `main.py` | `MAX_PAGES` | 10.000 | Max. gecrawlte Seiten |
| `main.py` | `MAX_AGE_DAYS` | 7 | Cache-TTL in Tagen |
| `main.py` | `RATE_LIMIT_SECONDS` | 0.5 | Pause zwischen Requests |
| `main.py` | `BLOCKED_DOMAINS` | `{serwiss.bib..., typo3backend-live...}` | Geblockte Subdomains |
| `resume_crawler.py` | `MAX_PAGES` | 40.000 | Erhöhtes Limit |
| `url_filter.py` | `BLOCKED_DOMAINS` | `{serwiss.bib..., typo3backend-live...}` | Geblockte/technische Subdomains |
| `url_filter.py` | `BLOCKED_APP_HOSTS` | `{moodle.hs-hannover.de, intranet.hs-hannover.de}` | Nicht-oeffentliche App-Hosts |
| `url_filter.py` | `BLOCKED_AUTH_PATH_MARKERS` | `("/login", "/logout", ...)` | Auth-/Login-Pfade |
| `url_filter.py` | `BROKEN_URL_MARKERS` | `("*", "|", ...)` | Kaputte/artefaktbehaftete URLs blockieren |
| `url_filter.py` | `DECISION_DB_PATH` | `data/url_decisions.db` | SQLite-Datei fuer URL-Entscheidungen |
| `clean_corpus.py` | `--keep-english` | `False` | Englischsprachige Dateien standardmaessig verwerfen |
| `hpc_vectorizer.py` | `CHUNK_SIZE` | 1.000 | Max. Chunk-Zeichen |
| `hpc_vectorizer.py` | `CHUNK_OVERLAP` | 200 | Überlappung |
| `hpc_vectorizer.py` | `DENSE_BATCH_SIZE` | 64 | GPU-Batch |
| `hpc_vectorizer.py` | `SPARSE_BATCH_SIZE` | 256 | CPU-Batch |
| `hpc_vectorizer.py` | `RESUME_FROM_FILE` | 1 | Neustart-Dateinummer |
| `hpc_vectorizer.py` | `RAG_SOURCE_DIR` | automatisch | Bevorzugt `data/curated/`, sonst `data/ingested/` |
| `local_importer.py` | `UPLOAD_BATCH` | 256 | Punkte pro Upsert |
| `local_importer.py` | `RESUME_FROM_ROW` | 0 | Neustart-Zeilenindex |
| `hybrid_search.py` | `CANDIDATE_LIMIT` | 100 | Kandidaten pro Arm |
| `hybrid_search.py` | `TOP_K` | 8 | Finale Ergebnisse |
| `hybrid_search.py` | `MAX_PER_URL` | 2 | Max. Chunks/URL |
| `hybrid_search.py` | `USE_RERANKER` | `True` | Reranking an/aus |
| `hybrid_search.py` | `AUGMENT_TOP_N` | 3 | Nachbar-Augmentation |
| `hsh_web_app.py` | `RAG_TOP_K` | 6 | Kontext-Chunks |
| `hsh_chatbot.py` | `RAG_TOP_K` | 4 | Kontext-Chunks (CLI) |
| `hsh_chatbot.py` | `DEBUG_PROMPT` | `True` | Prompt ausgeben |

---

## Ideen zur Weiterentwicklung

### 1. Automatisierte Qualitätssicherung und Tests

**Evaluations-Framework (RAG-Evals):**
Eine strukturierte Testbibliothek mit Frage-Antwort-Paaren erlaubt automatisierte Messungen der Antwortqualität. Werkzeuge wie [RAGAS](https://docs.ragas.io) messen:
- **Faithfulness**: Wird die Antwort ausschließlich durch den Kontext gestützt?
- **Answer Relevancy**: Beantwortet die Antwort die gestellte Frage?
- **Context Precision/Recall**: Finden die richtigen Chunks die richtigen Antworten?

Ein einfacher Goldstandard-Datensatz (50–100 kuratierte Fragen mit Erwartungsantworten und relevanten Quell-URLs) könnte als `pytest`-Test in die CI-Pipeline einfließen und bei jedem Deployment automatisch prüfen, ob Verbesserungen (neue Modelle, neue Chunk-Größen) die Qualität tatsächlich steigern oder verschlechtern.

**Retrieval-Monitoring:**
Logging der RRF-Scores und Reranker-Scores in eine Zeitreihe (z.B. SQLite oder Prometheus) ermöglicht es, Trendbrüche zu erkennen — etwa wenn ein Neucrawl schlechte Daten einspielt oder ein Modell-Update das Retrieval verändert.

---

### 2. Datenqualität durch LLMs verbessern

**LLM-gestützte Chunk-Bereinigung:**
Statt reine Zeichenzahl-Heuristiken für die Qualitätsprüfung zu verwenden, kann ein schnelles Sprachmodell (z.B. `Llama-3.1-8B`) jede Markdown-Datei bewerten:
- Enthält diese Seite tatsächlich informative Inhalte?
- Ist der Text kohärent oder besteht er aus Navigationselementen?
- Ist die Seite auf Deutsch verfasst?

Prompt-Vorlage:
```
Bewerte diesen Text auf einer Skala von 1 (wertlos) bis 5 (sehr informativ).
Antworte nur mit der Zahl und einer einzeiligen Begründung.

Text: {chunk_text[:500]}
```

Seiten unter einem Schwellwert (z.B. < 3) werden vor der Vektorisierung gefiltert.

**Automatische Metadaten-Extraktion:**
Ein LLM kann aus dem Volltext zusätzliche strukturierte Metadaten ableiten:
- Studiengang-Tags (`bachelor`, `master`, `weiterbildung`)
- Themen-Tags (`prüfungen`, `bewerbung`, `stundenplan`, `finanzen`)
- Zielgruppen-Tags

Diese Tags erweitern die Payload und ermöglichen präzisere Filter in der Suche.

**Volltext-Normalisierung:**
Deutsche Komposita werden von Suchmaschinen oft nicht aufgespalten. Ein LLM kann Komposita in Chunks vorverarbeiten: `„Modulhandbuchseite"` → `„Modulhandbuch Seite"`, was BM25-Treffer verbessert.

---

### 3. Zweistufige API-Zugriffe: das LLM wählt selbst

**Konzept: Agentenbasierte Retrieval-Planung**

Das aktuelle System verwendet eine feste Suchstrategie: Eine Anfrage → eine Suchanfrage → Kontext → Antwort. Bei komplexen, mehrteiligen Fragen (z.B. „Welche Prüfungsformen gibt es in Fakultät III im Masterstudium, und wie unterscheiden sich diese von Fakultät IV?") ist diese Strategie unzureichend.

**Stufe 1 — Planungsphase (LLM entscheidet, was es suchen möchte):**

Das LLM erhält die Nutzerfrage und ein Tool-Schema:

```python
tools = [
    {
        "name": "suche_wissensdatenbank",
        "description": "Sucht in der Wissensdatenbank der HsH nach relevanten Dokumenten.",
        "parameters": {
            "query": "Suchanfrage (natürlichsprachlich)",
            "faculty": "Optional: Fakultät I–V oder leer für alle",
            "max_results": "Anzahl der Ergebnisse (1–10)"
        }
    }
]
```

Das LLM kann mehrere Suchanfragen formulieren:
```json
[
  {"query": "Prüfungsformen Masterstudium Fakultät III", "faculty": "Fakultät III"},
  {"query": "Prüfungsformen Masterstudium Fakultät IV", "faculty": "Fakultät IV"},
  {"query": "Unterschiede Prüfungsordnung Master Fakultäten"}
]
```

**Stufe 2 — Antwortphase:**
Alle Suchergebnisse werden zusammengestellt und das LLM formuliert eine fundierte, vergleichende Antwort.

Dieser Ansatz entspricht dem **ReAct-Muster** (Reason + Act) und kann mit dem OpenAI Function-Calling-API oder dem Anthropic Tool Use umgesetzt werden.

**Selektives Nachladen per `chunk_index`:**
Eine Erweiterung ermöglicht es dem LLM, nach der ersten Antwort gezielt weitere Chunks anzufordern:
- „Ich brauche die vollständige Prüfungsordnung dieser Seite, bitte lade alle Chunks von `source_url=...`"
- Das System lädt daraufhin alle Chunks mit dieser `source_url` nach

Dies reduziert die durchschnittliche Kontextmenge (günstiger) und erhöht die bei Bedarf abrufbare Informationstiefe.

---

### 4. Weitere Verbesserungsideen

**Query-Expansion:**
Automatische Erweiterung der Suchanfrage um Synonyme und verwandte Begriffe vor der Vektorisierung. Beispiel: `„Urlaubssemester"` → `„Beurlaubung Exmatrikulation Studienunterbrechung"`. Dies erhöht den Recall besonders für BM25.

**Chunk-Größenoptimierung:**
Aktuell: 1.000 Zeichen mit 200 Zeichen Überlappung. Experimentell wären 1.500 Zeichen (weniger Grenzschnitte) oder adaptive Chunk-Größen basierend auf dem Dokumenttyp (PDFs oft länger zusammenhängend als HTML-Snippets).

**Semantisches Chunking:**
Statt fester Zeichengrenzen könnten Chunks an semantischen Grenzen (Themenwechsel) geteilt werden, z.B. mit einem Sentence-Transformer, der Ähnlichkeiten aufeinanderfolgender Sätze misst.

**Frischegewichtung:**
`crawl_date` als Ranking-Signal nutzen: neuere Seiten erhalten einen leichten Relevanzbonus. Wichtig für Seiten mit häufig aktualisierten Inhalten (Fristen, Ansprechpartner).

**Feedback-Loop:**
Nutzer können Antworten mit 👍/👎 bewerten. Negativ bewertete Anfragen werden in den Goldstandard-Datensatz aufgenommen und helfen, Schwächen systematisch zu identifizieren.

**Prüfen welche Domains sich aus der Suche noch ausschließen lassen.**
Entsprechende Liste hinterlegen. Z.B. Alle Seite in dem INhalte von Papern stehen. Es ist vielleicht interessant welche Person an welchem Paper geschrieben hat, aber Inhalte sind nicht so relevant.

**Englischsprachige Webseiten der Hochschule von der Suche ausschließen lassen.** 
Deutsche INhalte sind aktueller und für die Suche relevanter.

**Nicht nur Chunks übergeben sondern komplette Datei**
Hintergrund: Manche Dinge sind nicht zu verstehen ohne die Legende zu kennen. Wie z.B. was bedeutet [K90]? Alternativ: Solche INformationen extrahieren und stets mit übergeben. 
