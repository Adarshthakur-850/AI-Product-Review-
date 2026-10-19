# ProductGuard AI — Multilingual Product Conversation Auditor

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Tests-21%20Passed-brightgreen.svg)](tests/)

**ProductGuard AI** is a production-quality compliance and communication intelligence platform for sales and customer-service conversations. It audits calls in **English**, **Hindi (Devanagari)**, and **Hinglish (Romanized / Code-Switched)** to ensure service providers explain only verified product information, avoid off-topic discussions, accurately resolve customer questions, and continuously improve their communication skills.

---

## 🌟 Key Capabilities

1. **Multilingual Utterance Recognition**:
   - Sentence-level detection of **English (`en`)**, **Devanagari Hindi (`hi`)**, and **Romanized Hinglish (`hi-Latn`)**.
   - Handles natural code-switching (e.g., *"Sir, iska battery backup around 30 hours hai with fast charging."*) while preserving technical terminology and numerical specifications.
   - Raw transcripts are never overwritten or force-translated.
2. **Product Knowledge Base (RAG)**:
   - Grounded verification against approved product catalog specifications, prices, warranties, and return policies.
   - Strictly handles uncataloged queries as *"Unverified — insufficient product information"* rather than inventing specifications.
3. **10-Class Relevance & Topic Classification**:
   - Classifies every provider turn into categories such as Direct Answer, Relevant Feature, Price/Availability, Polite Greeting, Necessary Clarification, Repetition, Off-Topic Personal Discussion, Unsupported Claim, or Contradictory Statement.
4. **Factual Claim Verification**:
   - Categorizes extracted claims into `VERIFIED` ✅, `CONTRADICTED` ❌, `UNSUPPORTED` ⚠️, and `AMBIGUOUS`.
5. **100-Point Evaluation Framework**:
   - **Factual Accuracy**: 30 points
   - **Product Relevance**: 25 points
   - **Answer Quality**: 20 points
   - **Conciseness**: 15 points
   - **Communication Clarity**: 10 points
   - Transparent deduction audit trail explaining the exact reason for every point deducted.
6. **Private Coaching Report & Grounded Replacement Responses**:
   - Generates actionable, non-punitive coaching reports for service providers.
   - Synthesizes short, verified replacement responses in the provider's requested language (**English**, **Hindi**, or **Hinglish**).

---

## 🏛️ System Architecture

```
                    ┌─────────────────────────┐
                    │ Authorized Audio / Text │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────▼───────────────┐
                 │ Multilingual Language Detector│
                 │   (English, Hindi, Hinglish)  │
                 └───────────────┬───────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │                           │                           │
┌────▼────────────────┐ ┌────────▼──────────────┐ ┌──────────▼──────────────┐
│ Relevance & Topic   │ │ Factual Claim         │ │ Product Knowledge Base  │
│ Classifier (10 Cat) │ │ Extractor & Verifier  │ │ (Approved Catalog RAG)  │
└────┬────────────────┘ └────────┬──────────────┘ └──────────┬──────────────┘
     │                           │                           │
     └───────────────────────────┼───────────────────────────┘
                                 │
                 ┌───────────────▼───────────────┐
                 │ 100-Point Quality Evaluator   │
                 └───────────────┬───────────────┘
                                 │
                 ┌───────────────▼───────────────┐
                 │ Private Coaching Report &     │
                 │ Grounded Response Generator   │
                 └───────────────┬───────────────┘
                                 │
          ┌──────────────────────┴──────────────────────┐
          │                                             │
┌─────────▼────────┐                         ┌──────────▼────────┐
│ FastAPI REST API │                         │ Streamlit Auditor │
│ (Port 8000)      │                         │ Dashboard (8501)  │
└──────────────────┘                         └───────────────────┘
```

---

## 🚀 Quickstart & Execution

### 1. Run Automated Test Suite
Verify that all 15 unit and integration tests pass:
```powershell
python run.py test
```

### 2. Launch the Streamlit Auditor Dashboard
Launch the interactive web dashboard:
```powershell
python run.py dashboard
```
Open your browser to: **`http://localhost:8501`**

Inside the dashboard:
- Navigate to **"🎙️ Audit a Conversation"**
- Select from the preloaded benchmark cases (e.g. *Case 1: Hinglish — Quantum Sound Pro*)
- Click **"🚀 Run Complete Conversation Audit"** to view real-time score gauges, claim verification matrices, and grounded response rewrites!

### 3. Launch the FastAPI REST Server
Start the production REST API:
```powershell
python run.py api
```
- API Base: **`http://localhost:8000`**
- Interactive Swagger Documentation: **`http://localhost:8000/docs`**

### 4. Generate Service Provider Talk-Track & Model Testing Script (.docx)
Generate standard Word (.docx) and Markdown (.md) talk-track guides containing approved dialogues, forbidden claims, and benchmark testing prompts:
```powershell
python generate_provider_script.py --all
```
Generated documents are saved in the `generated_docs/` folder and can also be downloaded directly from the dashboard under the **📦 Approved Product Catalog** tab.

---

## 📋 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | System status and supported language metadata |
| `GET` | `/health` | Application health check |
| `POST` | `/api/v1/calls` | Submit conversation transcript for full compliance audit |
| `POST` | `/api/v1/calls/{id}/audio` | Upload authorized call recording (`.wav`, `.mp3`, `.m4a`) |
| `GET` | `/api/v1/calls/{id}/transcript`| Retrieve timestamped, speaker-labeled transcript segments |
| `GET` | `/api/v1/calls/{id}/report` | Retrieve completed private coaching report |
| `GET` | `/api/v1/products` | List all approved products in the knowledge base |
| `GET` | `/api/v1/products/{id}` | Retrieve verified product specs, pricing, and policies |
| `POST` | `/api/v1/products` | Register a new product into the catalog |
| `GET` | `/api/v1/providers` | List service providers and multi-call compliance summaries |

---

## 🐳 Docker Deployment

Run both the API and Streamlit dashboard using Docker Compose:
```bash
docker-compose up --build
```
- API will be accessible on port `8000`
- Dashboard will be accessible on port `8501`
