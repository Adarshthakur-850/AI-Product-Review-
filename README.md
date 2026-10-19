# ProductGuard AI

**A multilingual product-conversation auditing and coaching platform**

ProductGuard AI helps evaluate sales and customer-service conversations against an approved product catalog. It analyzes provider statements for factual claims, product relevance, unanswered questions, repetition, and overly long responses, then produces a transparent quality score and coaching suggestions.

It is designed for conversations in **English**, **Hindi (Devanagari)**, and **Hinglish** (Romanized Hindi and code-switched language).

[Repository](https://github.com/Adarshthakur-850/AI-Product-Review-) · [FastAPI docs](http://localhost:8000/docs) · [Streamlit dashboard](http://localhost:8501)

## Contents

- [What it does](#what-it-does)
- [How it works](#how-it-works)
- [Technology stack](#technology-stack)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Run with Docker](#run-with-docker)
- [REST API](#rest-api)
- [Product catalog and sample data](#product-catalog-and-sample-data)
- [Tests](#tests)
- [Important implementation notes](#important-implementation-notes)
- [Privacy and safe use](#privacy-and-safe-use)
- [Roadmap](#roadmap)

## What it does

- **Multilingual language detection:** identifies English, Devanagari Hindi, and Romanized/code-switched Hinglish using a script- and marker-based detector.
- **Transcript ingestion:** accepts raw, speaker-labelled text or structured transcript segments for conversation audits.
- **Product-grounded claim checks:** compares detected claims with specifications and commercial terms in JSON product catalogs. Claims can be marked verified, contradicted, unsupported, or ambiguous, depending on the check.
- **Relevance analysis:** flags provider statements that are off-topic, repetitive, unsupported, or contradictory.
- **Transparent quality scoring:** scores conversations out of 100 across five configured dimensions.
- **Coaching suggestions:** generates improvement feedback and candidate replacement responses using product catalog information and the selected report language.
- **Interactive dashboard:** presents a Streamlit interface for reviewing sample data, auditing conversations, inspecting catalog information, and viewing provider analytics.
- **REST API:** exposes endpoints for transcript auditing, product catalog management, provider metrics, and health checks.
- **Guide generation:** generates Markdown and Word (.docx) service-provider talk-track/testing guides for catalog products.

## How it works

1. A user selects an approved product and supplies a transcript or structured turns.
2. The system labels each turn with a detected language and assigns speaker roles.
3. Provider statements are analyzed for claims and checked against catalog facts.
4. The relevance classifier and quality scorer evaluate the conversation.
5. The coaching component assembles findings, score deductions, and suggested replacements.
6. Results are presented through the dashboard or API.

### Quality score

The default scoring rubric totals 100 points:

| Dimension | Maximum |
|---|---:|
| Factual accuracy | 30 |
| Product relevance | 25 |
| Answer quality | 20 |
| Conciseness | 15 |
| Communication clarity | 10 |
| **Total** | **100** |

The score is a rule-based product-compliance and communication indicator, not a guarantee of legal compliance or a substitute for human review.

## Technology stack

- **Language:** Python
- **API:** FastAPI, Uvicorn, Pydantic
- **Dashboard:** Streamlit
- **Data and analysis:** pandas, NumPy, scikit-learn
- **Persistence:** SQLAlchemy with SQLite by default
- **Audio utilities:** SpeechRecognition, SoundFile, optional pyttsx3 text-to-speech
- **Visualization:** Plotly
- **Testing:** pytest, HTTPX
- **Deployment:** Docker and Docker Compose

## Project structure

```text
AI-Product-Review-/
├── api/
│   ├── main.py                 # FastAPI app and router registration
│   ├── routes/
│   │   ├── calls.py             # Conversation audit routes
│   │   ├── products.py          # Product catalog routes
│   │   └── providers.py         # Provider metrics routes
│   └── schemas/                 # Request/response schemas
├── core/
│   ├── config.py                # Application settings and scoring weights
│   ├── exceptions.py
│   └── security.py              # Transcript PII redaction helpers
├── dashboard/
│   └── app.py                   # Streamlit UI
├── data/
│   ├── catalog/                 # Approved product JSON catalogs
│   └── sample_conversations/    # English, Hindi, Hinglish examples
├── db/
│   ├── models.py
│   └── session.py               # SQLAlchemy engine and DB initialization
├── services/
│   ├── auditor_pipeline.py
│   ├── audio_service.py
│   ├── claim_verifier.py
│   ├── coach_generator.py
│   ├── knowledge_base.py
│   ├── language_detector.py
│   ├── quality_scorer.py
│   ├── relevance_classifier.py
│   ├── script_doc_generator.py
│   └── stt_service.py
├── tests/
├── generated_docs/              # Generated guides and examples
├── generate_provider_script.py
├── requirements.txt
├── run.py
├── Dockerfile
└── docker-compose.yml
```

## Requirements

- Python **3.12** recommended (the Docker image uses Python 3.12)
- pip
- Git (to clone the repository)
- Docker Desktop and Docker Compose (optional, for containerized setup)

Audio features may require additional system audio libraries or microphone permissions, depending on the operating system.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Adarshthakur-850/AI-Product-Review-.git
cd AI-Product-Review-
```

### 2. Create and activate a virtual environment

**Windows PowerShell**
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
python run.py dashboard
``

Open [http://localhost:8501](http://localhost:8501).

### 5. Start the API

In a separate terminal, activate the same virtual environment and run:

```bash
python run.py api
``

- API base URL: [http://localhost:8000](http://localhost:8000)
- Interactive API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

### Run both services

The dashboard and API are separate processes in local development. Keep both terminals running if you use dashboard features that depend on the API.

## Run with Docker

From the repository root:

```bash
docker compose up --build
```

The Compose file starts separate API and dashboard containers:

- Dashboard: [http://localhost:8501](http://localhost:8501)
- API: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Stop the containers with:

```bash
docker compose down
```

The default Compose configuration mounts the project directory into both containers and configures SQLite for the API service.

## REST API

The API uses the `/api/v1` prefix for application routes.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Service name, version, status, supported languages |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/calls` | Audit a raw or structured conversation transcript |
| `POST` | `/api/v1/calls/{call_id}/audio` | Accept an audio upload request |
| `GET` | `/api/v1/calls/{call_id}/status` | Get a call's current cached status |
| `GET` | `/api/v1/calls/{call_id}/transcript` | Retrieve transcript segments |
| `GET` | `/api/v1/calls/{call_id}/report` | Retrieve the generated coaching report |
| `POST` | `/api/v1/calls/realtime-turn` | Audit a single conversational turn |
| `GET` | `/api/v1/products` | List catalog products |
| `GET` | `/api/v1/products/{product_id}` | Retrieve a product record |
| `POST` | `/api/v1/products` | Add a product to the catalog |
| `POST` | `/api/v1/products/{product_id}/documents` | Append catalog information to a product record |
| `GET` | `/api/v1/providers` | List provider analytics records |
| `GET` | `/api/v1/providers/{provider_id}/performance` | Retrieve a provider's metrics |

Use the interactive Swagger UI at `/docs` to inspect request schemas and try the endpoints.

### Example: audit a transcript

The call endpoint requires disclosure confirmation when the application setting `REQUIRE_RECORDING_DISCLOSURE` is enabled.

```bash
curl -X POST "http://localhost:8000/api/v1/calls" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "quantum-sound-pro",
    "provider_name": "Demo Provider",
    "disclosure_confirmed": true,
    "target_report_language": "Hinglish",
    "raw_transcript": "Customer: Is headphone ki battery kitni der chalti hai?\nProvider: Sir, iska battery backup around 30 hours hai."
  }'
```

Request field requirements may be inspected in the OpenAPI schema at `/docs`.

## Product catalog and sample data

The repository includes JSON catalog examples under `data/catalog/` and sample conversations under `data/sample_conversations/`. These are demonstration data; replace them with product information that has been reviewed and approved by your organization before using the application for real customer interactions.

Catalog records can contain:

- Product specifications
- Commercial terms and pricing
- Policies and warranty details
- Frequently asked questions and approved answers

The knowledge-base service loads catalog JSON files and uses lexical keyword overlap and attribute matching to retrieve relevant facts. Despite the RAG-style design, the current retrieval implementation is a lightweight local catalog search rather than a vector database pipeline.

## Tests

Run the available automated tests from the repository root:

```bash
python run.py test
```

Or run pytest directly:

```bash
python -m pytest tests/ -v
```

The tests cover language detection, claim verification, quality scoring, API endpoints, end-to-end sample audits, and document generation.

A test badge should only be treated as current when the suite has been run against the latest commit. This README does not assert that tests passed in the current environment.

## Generate provider guides

Generate Markdown and Word guide files for every product in the catalog:

```bash
python generate_provider_script.py --all
```

For one product:

```bash
python generate_provider_script.py quantum-sound-pro
```

Generated documents are written to `generated_docs/`.

## Important implementation notes

This repository contains a working prototype with a mix of implemented services and demonstration components. Keep these distinctions in mind:

- **Audio upload route:** the API upload endpoint currently validates the filename extension and acknowledges receipt; it does not itself run the full transcription-and-audit pipeline. The dashboard microphone workflow calls the audio utility separately.
- **Speech recognition:** the audio utility uses the SpeechRecognition package with Google's online recognition service and a fallback language. It needs network access and should not be assumed to work offline.
- **Provider analytics:** provider names, call counts, scores, and trends returned by the provider routes are currently representative hard-coded sample records, not analytics calculated from a production call database.
- **Call storage:** processed call objects are held in an in-memory cache in the API route, so call status/transcript/report lookup does not persist across server restarts.
- **Scoring and claim extraction:** the rules are heuristic and should be validated against your product catalog and real, reviewed examples before operational use.
- **Database:** SQLAlchemy models and SQLite initialization are present, but the call audit route currently returns data from the in-memory cache rather than using a full persistent call-record workflow.
- **Privacy and permissions:** PII-redaction helpers exist for common email, telephone and payment-card patterns. Review the data flow, logging, access controls, retention, consent handling and applicable laws before processing real recordings or personal information.
- **CORS and authentication:** the current API configuration allows all CORS origins and does not implement a production authentication/authorization layer. Tighten this before exposing the service publicly.

## Privacy and safe use

- Obtain any legally required consent before recording, uploading, or analyzing calls.
- Do not commit customer recordings, real transcripts, API keys, passwords, access tokens, or production customer data to Git.
- Use synthetic or anonymized examples for development and tests.
- Configure authentication, access control, encryption, retention/deletion, logging, and restricted CORS origins before deployment.
- Treat automated findings as decision support; have a qualified person review consequential coaching or compliance decisions.

## Roadmap

- [ ] Persist audited call records and reports with a complete database workflow.
- [ ] Connect the audio-upload API to a real transcription-and-audit pipeline with size limits and robust error handling.
- [ ] Replace representative provider metrics with database-backed aggregate analytics.
- [ ] Add authentication, role-based access control, and restrictive CORS settings.
- [ ] Add CI that runs the test suite for every pull request and update status badges from real workflow results.
- [ ] Strengthen multilingual evaluation with reviewed test sets and measurable precision/recall.
- [ ] Add structured configuration and observability for local and container deployments.

## Contributing

1. Fork the repository and create a focused feature branch.
2. Make a change and add or update tests.
3. Run `python run.py test`.
4. Open a pull request describing the change and validation results.

## License

No license file was visible in the repository when this README was prepared. Add a `LICENSE` file before granting others explicit permission to reuse or distribute the project.

---

Built as a multilingual AI-assisted quality and product-claim auditing project.
