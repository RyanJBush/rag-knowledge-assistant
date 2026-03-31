# RAG Knowledge Assistant

> A production-oriented, full-stack AI knowledge assistant that answers questions grounded in your own documents — with citations.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)
![Tailwind](https://img.shields.io/badge/Tailwind-4.x-38BDF8)

---

## What It Does

1. **Upload** PDF or plain-text documents via the browser
2. Documents are **parsed → chunked → embedded** and indexed in a local FAISS vector store
3. Ask any **natural-language question** — the system retrieves the most relevant chunks and returns a grounded answer with **source citations**

---

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design.

```
Browser (React/Vite)
    │
    │  REST API
    ▼
FastAPI Backend
    ├── Ingestion: File → Parse → Chunk → Embed → FAISS
    └── Query:    Question → Embed → FAISS Search → LLM → Answer + Citations
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, Pydantic v2 |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector store | FAISS (`IndexFlatL2`) |
| Metadata | SQLite (stdlib `sqlite3`) |
| PDF parsing | PyPDF2 |
| Frontend | React 19, Vite, TypeScript, Tailwind CSS v4 |
| Linting | ruff (Python), ESLint + Prettier (JS/TS) |
| Testing | pytest, pytest-asyncio, httpx |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Clone & configure

```bash
git clone https://github.com/RyanJBush/rag-knowledge-assistant.git
cd rag-knowledge-assistant
cp .env.example .env   # edit if needed
```

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

---

## Demo Flow

1. Open http://localhost:5173
2. Drag & drop a `.pdf` or `.txt` file into the **Upload** panel
3. Wait for "✓ Uploaded successfully"
4. Type a question in the **Chat** box
5. Read the answer + view source citations below

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/documents/upload` | Upload a document |
| GET | `/api/v1/documents` | List uploaded documents |
| POST | `/api/v1/query` | Ask a question |

### Query request/response

```json
// POST /api/v1/query
{ "question": "What is RAG?", "top_k": 5 }

// Response
{
  "answer": "Based on the retrieved documents: ...",
  "query": "What is RAG?",
  "citations": [
    {
      "document_id": "uuid",
      "source_filename": "my_doc.pdf",
      "chunk_index": 3,
      "snippet": "RAG stands for Retrieval-Augmented Generation...",
      "score": 0.142
    }
  ]
}
```

---

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

## Linting

```bash
# Python
cd backend && python -m ruff check app/ tests/

# TypeScript
cd frontend && npm run lint
```

---

## Configuration

Copy `.env.example` to `.env`. Key variables:

| Variable | Default | Description |
|---|---|---|
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace model name |
| `CHUNK_SIZE` | `500` | Words per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `5` | Chunks retrieved per query |
| `LLM_PROVIDER` | `extractive` | `extractive` / `openai` / `anthropic` |
| `OPENAI_API_KEY` | — | Required if `LLM_PROVIDER=openai` |

---

## Project Structure

```
rag-knowledge-assistant/
├── .env.example
├── docs/
│   └── ARCHITECTURE.md
├── backend/
│   ├── app/
│   │   ├── api/routes/        # health, documents, query
│   │   ├── core/              # config, logging
│   │   ├── db/                # SQLite metadata
│   │   ├── rag/               # parser, chunker, embedder, retriever, generator
│   │   ├── schemas/           # Pydantic models
│   │   ├── services/          # document_service orchestration
│   │   └── main.py
│   ├── data/
│   │   ├── uploads/
│   │   └── vector_store/
│   ├── tests/
│   ├── pyproject.toml
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/        # UploadPanel, DocumentLibrary, ChatInterface, CitationPanel
    │   ├── hooks/             # useDocuments, useChat
    │   ├── lib/               # api.ts
    │   ├── pages/             # Dashboard
    │   └── types/             # TypeScript interfaces
    ├── vite.config.ts
    └── package.json
```

---

## Resume Highlights

- Built an **end-to-end RAG pipeline** (parse → chunk → embed → index → retrieve → generate) from scratch without heavy frameworks
- Designed a **pluggable LLM provider abstraction** (`BaseLLMProvider`) enabling zero-code-change swap between extractive, OpenAI, and Anthropic backends
- Implemented **FAISS vector search** with persistent index and chunk-level citation tracking
- Delivered a **polished React/TypeScript/Tailwind** chat UI with document library, drag-and-drop upload, and source citation display
- Achieved **100% test pass rate** with pytest, mocked embeddings for CI-safe integration tests
