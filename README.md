# RAGHSH — RAG-System für die Hochschule Hannover

**RAGHSH** ist ein vollständiges **Retrieval-Augmented Generation (RAG)**-System, das Fragen zur Hochschule Hannover ausschließlich auf Basis offizieller Dokumente beantwortet. Es kombiniert einen automatischen Web-Spider mit einer Vektor-Datenbank und einem großen Sprachmodell (LLM) der GWDG ChatAI API.

---

## Inhaltsverzeichnis

1. [Systemübersicht](#systemübersicht)
2. [Verzeichnisstruktur](#verzeichnisstruktur)
3. [Abhängigkeiten und Bibliotheken](#abhängigkeiten-und-bibliotheken)
4. [Einrichtung](#einrichtung)
5. [Nutzung — Schritt für Schritt](#nutzung--schritt-für-schritt)
6. [Programmübersicht](#programmübersicht)
7. [Konfigurationsparameter](#konfigurationsparameter)
8. [Technische Architektur](#technische-architektur)

---

## Systemübersicht

```
Phase 1: Daten sammeln
  main.py  →  data/ingested/*.md  (Web-Spider, HTML + PDF → Markdown)

Phase 2: Daten vektorisieren
  ingest_to_qdrant.py  →  Qdrant-Collection 'hsh_knowledge'

Phase 3: Suchen (optional als CLI)
  hybrid_search.py  →  Hybrid-Suche (Dense + FTS + RRF)

Phase 4: Chatbot
  hsh_chatbot.py  →  RAG-Pipeline + GWDG LLM → Antwort

Hilfsprogramm:
  check_quality.py  →  Qualitätsprüfung + Löschvorschläge
```

Das System löst das **Halluzinationsproblem** herkömmlicher Chatbots: Das LLM erhält nicht nur die Nutzerfrage, sondern auch die relevanten Textstellen aus offiziellen HsH-Dokumenten als Kontext — und darf nur auf dieser Basis antworten.

---

## Verzeichnisstruktur

```
RAGHSH/
├── docker-compose.yml          # Qdrant-Vektordatenbank als Docker-Container
├── qdrant_data/                # Persistenter Speicher für Qdrant (Docker Volume)
├── screenshots/
│   └── dom_check.png           # Screenshot für Entwicklungszwecke
└── hsh_scraper/
    ├── main.py                 # Phase 1: Web-Spider (BFS-Crawler)
    ├── ingest_to_qdrant.py     # Phase 2: Vektorisierung und Datenbankbefüllung
    ├── hybrid_search.py        # Phase 3: Hybrid-Suche (Dense + FTS + RRF)
    ├── hsh_chatbot.py          # Phase 4: Interaktiver RAG-Chatbot
    ├── check_quality.py        # Hilfsprogramm: Qualitätsprüfung der MD-Dateien
    ├── requirements.txt        # Python-Abhängigkeiten
    ├── .env                    # API-Schlüssel (nicht im Git!)
    ├── .env.example            # Vorlage für .env
    └── data/
        └── ingested/           # Gescrapte Seiten als Markdown-Dateien
            ├── .gitkeep
            ├── YYYY-MM-DD_slug.md   # HTML-Seiten (Namensschema)
            └── YYYY-MM-DD_slug.md   # PDF-Dokumente
```

> **Hinweis:** Das Verzeichnis `.venv/` (Python-Virtualenv) liegt ebenfalls in `hsh_scraper/` und ist nicht im Git eingecheckt.

---

## Abhängigkeiten und Bibliotheken

### Infrastruktur

| Komponente | Beschreibung |
|---|---|
| **Docker** | Laufzeitumgebung für Qdrant |
| **Qdrant** (Docker Image `qdrant/qdrant`) | Vektordatenbank, Port 6333 (HTTP) und 6334 (gRPC) |
| **Python 3.12** | Laufzeitumgebung für alle Skripte |

### Python-Bibliotheken (`requirements.txt`)

| Bibliothek | Verwendung |
|---|---|
| **crawl4ai[all]** | Asynchroner Web-Crawler mit JavaScript-Unterstützung (Playwright-Backend). Extrahiert strukturierten Markdown-Text aus HTML-Seiten. |
| **pymupdf4llm** | Konvertiert PDF-Dateien in LLM-optimiertes Markdown (via PyMuPDF). |
| **python-slugify** | Erzeugt URL-sichere Dateinamen aus URL-Pfaden (z.B. `/studium/bachelor/` → `studium-bachelor`). |
| **openpyxl** | Erstellt den Excel-Fehlerbericht nach dem Crawl-Durchlauf. |
| **qdrant-client** | Python-Client für die Qdrant-Vektordatenbank (Upsert, Vektorsuche, Volltextsuche, Payload-Index). |
| **fastembed** | Lokales Embedding-Modell (`jinaai/jina-embeddings-v3`, 1024 Dimensionen, multilingual). Erzeugt Vektoren ohne externe API. |
| **langchain-text-splitters** | Zweistufiges Chunking: `MarkdownHeaderTextSplitter` (strukturell) + `RecursiveCharacterTextSplitter` (größenbasiert). |
| **openai** | OpenAI-kompatibler HTTP-Client für die GWDG ChatAI API (kein OpenAI-Konto erforderlich). |
| **python-dotenv** | Lädt den API-Schlüssel aus der `.env`-Datei. |

### Standardbibliotheken (keine Installation nötig)

`asyncio`, `collections.deque`, `gc`, `logging`, `pathlib`, `re`, `sys`, `tempfile`, `uuid`

---

## Einrichtung

### 1. Voraussetzungen

- Docker und Docker Compose installiert
- Python 3.12 installiert
- GWDG ChatAI API-Schlüssel (https://chat-ai.academiccloud.de)

### 2. Repository klonen / Verzeichnis anlegen

```bash
cd RAGHSH
```

### 3. Qdrant-Datenbank starten

```bash
docker compose up -d
```

Prüfen ob Qdrant läuft:
```bash
curl http://localhost:6333/healthz
# Antwort: {"title":"qdrant - vector search engine","version":"..."}
```

### 4. Python-Umgebung einrichten

```bash
cd hsh_scraper
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt

# Playwright-Browser für crawl4ai herunterladen
playwright install chromium
```

### 5. API-Schlüssel konfigurieren

```bash
cp .env.example .env
# .env öffnen und GWDG_API_KEY eintragen
```

Inhalt der `.env`:
```
GWDG_API_KEY=dein-schluessel-hier
GWDG_API_BASE=https://chat-ai.academiccloud.de/v1
```

---

## Nutzung — Schritt für Schritt

### Phase 1: Website crawlen

```bash
cd hsh_scraper
python main.py
```

Das Programm crawlt `www.hs-hannover.de` per Breadth-First-Search (BFS) und speichert jede Seite als Markdown-Datei in `data/ingested/`. Bereits gecrawlte Seiten werden nicht erneut gespeichert (Cache, konfigurierbar über `MAX_AGE_DAYS`).

**Fortschrittsausgabe:**
```
2026-03-08 10:00:01 [INFO] Crawling: https://www.hs-hannover.de/
2026-03-08 10:00:03 [INFO] Saved data/ingested/2026-03-08_index.md
...
2026-03-08 12:00:00 [INFO] Done. 847 succeeded, 3 failed, 0 skipped out of 850 URLs visited.
```

Ein Excel-Fehlerbericht (`YYYY-MM-DD_fehler.xlsx`) wird automatisch in `data/ingested/` erstellt.

### (Optional) Qualität prüfen

```bash
python check_quality.py
```

Gibt eine Tabelle aller Markdown-Dateien aus und listet Löschvorschläge für minderwertige Dateien:

```
Filename                          Words  Tables  Type    Quality
-------------------------------------------------------------
2026-03-08_index.md               1 234       3  html    OK
2026-03-08_fehler-seite.md            8       0  html    LÖSCHEN
...

LÖSCHVORSCHLÄGE (2 von 850 Dateien)
  2026-03-08_fehler-seite.md
    • Zu wenig Text: 8 Wörter (Minimum für HTML: 30)
```

### Phase 2: Daten in Qdrant laden

```bash
python ingest_to_qdrant.py
```

Liest alle Markdown-Dateien, zerlegt sie in Chunks, erzeugt Vektoren mit dem lokalen Embedding-Modell (`jinaai/jina-embeddings-v3`) und lädt sie in Qdrant. Ein erneuter Lauf aktualisiert vorhandene Einträge (Upsert, keine Duplikate).

> **Hinweis:** Beim ersten Aufruf wird das Embedding-Modell (~1 GB) heruntergeladen.

**Fortschrittsausgabe:**
```
2026-03-08 [INFO]   [  1/847   0.1%]  2026-03-08_index.md             →  12 chunk(s)  (total:    12)
2026-03-08 [INFO]   [  2/847   0.2%]  2026-03-08_studium.md           →   8 chunk(s)  (total:    20)
...
2026-03-08 [INFO] Total chunks : 9 341
2026-03-08 [INFO] Avg chunks/file : 11.0
2026-03-08 [INFO] Avg chunk length: 687 chars
```

### Phase 3: Suche testen (optional)

```bash
python hybrid_search.py
```

Startet eine interaktive Suche direkt in der Datenbank, ohne LLM. Nützlich zum Debuggen der Trefferqualität:

```
Frage> Bewerbungsfristen Bachelor Informatik

  ┌─ Treffer 1  (RRF-Score: 0.03226)
  │  URL      : https://www.hs-hannover.de/studium/bewerbung/...
  │  Fakultät : Fakultät IV
  │  Abschnitt: Bewerbung > Fristen
  │  Vorschau : Die Bewerbungsfrist für den Bachelorstudiengang...
  └──────────────────────────────────────────────────────────────
```

### Phase 4: Chatbot starten

```bash
python hsh_chatbot.py
```

Beim Start werden alle verfügbaren LLM-Modelle von der GWDG-API abgefragt:

```
Rufe Modellliste von der GWDG-API ab…

  [ 1] gpt-4o
  [ 2] gpt-4o-mini
  [ 3] llama-3.3-70b-instruct
  [ 4] deepseek-r1
  ...

Modell wählen (1–12): 3

  → Aktiv: llama-3.3-70b-instruct

HsH-Chatbot bereit.  Strg+C oder 'exit' zum Beenden.

Frage> Wie bewerbe ich mich für den Bachelor Informatik?
```

Die Antwort enthält den Quellnachweis aus den offiziellen Dokumenten:

```
[llama-3.3-70b-instruct]
──────────────────────────────────────────────────────────────────────
Für den Bachelorstudiengang Informatik (Fakultät IV) bewerben Sie sich
über das Online-Portal der HsH. Die Bewerbungsfrist für das Wintersemester
endet am 15. Juli...

Quellen:
- Bewerbung & Zulassung | https://www.hs-hannover.de/studium/... | Fristen
──────────────────────────────────────────────────────────────────────
```

---

## Programmübersicht

### `main.py` — Web-Spider

Crawlt die gesamte HsH-Website per **Breadth-First-Search (BFS)**.

| Parameter | Standard | Beschreibung |
|---|---|---|
| `SEED_URLS` | `["https://www.hs-hannover.de/"]` | Startseiten |
| `MAX_PAGES` | `10 000` | Maximale Seitenanzahl |
| `ALLOWED_DOMAIN` | `hs-hannover.de` | Nur diese Domain wird gecrawlt |
| `MAX_AGE_DAYS` | `7` | Seiten jünger als N Tage werden nicht neu gespeichert |
| `RATE_LIMIT_SECONDS` | `2` | Pause zwischen Requests |

- HTML-Seiten werden mit **Crawl4AI** (Playwright-Backend) gecrawlt, JavaScript-gerenderte Inhalte werden korrekt verarbeitet
- PDFs werden mit **httpx** heruntergeladen und mit **pymupdf4llm** in Markdown konvertiert
- Frisch gecachte Seiten werden trotzdem gecrawlt (für Link-Extraktion), aber nicht neu gespeichert
- Alle fehlgeschlagenen URLs werden in einer Excel-Datei protokolliert

---

### `ingest_to_qdrant.py` — Vektorisierung

Liest Markdown-Dateien und befüllt die Qdrant-Datenbank.

| Parameter | Standard | Beschreibung |
|---|---|---|
| `CHUNK_SIZE` | `1 000` | Maximale Chunk-Größe in Zeichen |
| `CHUNK_OVERLAP` | `200` | Überlappung zwischen Chunks |
| `EMBED_BATCH_SIZE` | `16` | Chunks pro Embedding-Aufruf (RAM-Steuerung) |
| `EMBED_MODEL` | `jinaai/jina-embeddings-v3` | Lokales Embedding-Modell |
| `COLLECTION_NAME` | `hsh_knowledge` | Name der Qdrant-Collection |

**Chunking-Strategie (zweistufig):**
1. `MarkdownHeaderTextSplitter` — teilt an Überschriften (#, ##, ###), bewahrt Überschriften-Hierarchie als Metadaten
2. `RecursiveCharacterTextSplitter` — zerteilt zu große Abschnitte weiter

**RAM-Management:** Streaming-Pipeline, nie mehr als ein Mini-Batch im Speicher. Nach jedem Batch: explizites `del` + `gc.collect()`.

---

### `hybrid_search.py` — Hybridsuche

Kombiniert zwei Suchmethoden via **Reciprocal Rank Fusion (RRF)**:

| Arm | Methode | Stärke |
|---|---|---|
| Dense Search | Vektorähnlichkeit (Cosine) | Semantisches Verstehen |
| Full-Text Search | MatchText auf `text`-Feld | Exakte Schlüsselwörter, Abkürzungen |

**RRF-Score:** `Σ 1 / (60 + Rang)` — Treffer in beiden Armen werden bevorzugt.

**Deduplizierung:** Nach der Fusion wird pro `source_url` nur der beste Chunk behalten, damit `TOP_K` Ergebnisse tatsächlich K verschiedene Quellen repräsentieren.

---

### `hsh_chatbot.py` — RAG-Chatbot

| Parameter | Standard | Beschreibung |
|---|---|---|
| `RAG_TOP_K` | `4` | Anzahl Kontext-Dokumente pro Anfrage |
| `TEMPERATURE` | `0.0` | Kreativität des LLM (0 = deterministisch) |
| `DEBUG_PROMPT` | `True` | Vollständigen LLM-Prompt ausgeben |
| `GWDG_API_BASE` | `https://chat-ai.academiccloud.de/v1` | API-Endpunkt |

**RAG-Pipeline pro Anfrage:**
1. Hybrid-Suche → 4 relevante Chunks
2. Kontext-String aufbauen (Titel, URL, Abschnitt, Text)
3. System-Prompt + Kontext + Frage → GWDG LLM
4. Antwort + Quellenangaben ausgeben

**Reasoning-Modelle:** DeepSeek R1 und ähnliche Modelle liefern einen internen Denkprozess (`reasoning_content`), der in einem `[Thinking]`-Block separat ausgegeben wird.

---

### `check_quality.py` — Qualitätsprüfung

Analysiert alle Markdown-Dateien und schlägt minderwertige Dateien zum Löschen vor.

**Löschkriterien:**

| Kriterium | Schwellwert | Erklärung |
|---|---|---|
| Kein YAML-Header | — | Datei korrupt oder leer |
| Zu wenig Text (HTML) | < 30 Wörter | Fehlerseite, leere Weiterleitung |
| Zu wenig Text (PDF) | < 50 Wörter | Deckblatt, leeres Formular |
| Fehlerseitenmuster | — | „404", „Seite nicht gefunden" u.a. |
| Duplikat | — | Ältere Version desselben URL-Slugs |

---

## Konfigurationsparameter

### `.env` — Geheime Zugangsdaten

```ini
GWDG_API_KEY=<dein-api-schluessel>
GWDG_API_BASE=https://chat-ai.academiccloud.de/v1
```

### `docker-compose.yml` — Qdrant-Container

```yaml
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - ./qdrant_data:/qdrant/storage   # Persistenter Speicher
```

---

## Technische Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                      Nutzerfrage                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  hybrid_search.py                                           │
│                                                             │
│  ┌──────────────────┐    ┌─────────────────────────────┐   │
│  │  Dense Search    │    │  Full-Text Search           │   │
│  │  (Vektoren,      │    │  (MatchText auf             │   │
│  │   Cosine-Sim)    │    │   Payload-Feld 'text')      │   │
│  └────────┬─────────┘    └──────────────┬──────────────┘   │
│           │                             │                   │
│           └──────────┬──────────────────┘                   │
│                      ▼                                      │
│              RRF-Fusion + URL-Deduplizierung                │
│                      │                                      │
│                      ▼                                      │
│            Top-K Chunks (Standard: 4)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  hsh_chatbot.py — Prompt-Aufbau                             │
│                                                             │
│  [System]  Persona + Regeln (nur aus Kontext antworten)    │
│  [User]    Kontext-Blöcke + Nutzerfrage                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  GWDG ChatAI API                                            │
│  (OpenAI-kompatibel, https://chat-ai.academiccloud.de/v1)  │
│  Modelle: GPT-4o, Llama 3, DeepSeek R1, …                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Ausgabe                                                    │
│  • [Thinking]-Block (nur Reasoning-Modelle)                │
│  • Antworttext                                              │
│  • Quellenangaben mit RRF-Score                            │
└─────────────────────────────────────────────────────────────┘
```

### Datenbankschema (Qdrant Payload pro Chunk)

| Feld | Typ | Beschreibung |
|---|---|---|
| `source_url` | string | Ursprungs-URL der Seite |
| `title` | string | Seitentitel |
| `crawl_date` | string | Datum des Crawls (ISO 8601) |
| `content_type` | string | `html` oder `pdf` |
| `faculty` | string | Fakultätsbezeichnung (aus URL extrahiert) |
| `section_heading` | string | Überschriften-Breadcrumb (z.B. `Studium > Bachelor > Bewerbung`) |
| `text` | string | Volltext des Chunks (für FTS indiziert) |
| `chunk_index` | int | Position innerhalb des Quelldokuments |
| `total_chunks` | int | Gesamtanzahl Chunks des Quelldokuments |

Punkt-IDs sind deterministische **UUID5** aus `source_url + chunk_index` — ein erneuter Lauf von `ingest_to_qdrant.py` aktualisiert vorhandene Einträge (Upsert) ohne Duplikate zu erzeugen.
