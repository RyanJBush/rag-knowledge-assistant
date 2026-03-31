# Architecture — RAG Knowledge Assistant

## Overview

This system is a **Retrieval-Augmented Generation (RAG)** pipeline that lets users upload documents and ask natural-language questions grounded in their content.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser (React)                         │
│   ┌────────────┐  ┌────────────────┐  ┌─────────────────────┐  │
│   │  Upload    │  │  Document      │  │  Chat + Citations   │  │
│   │  Panel     │  │  Library       │  │  Panel              │  │
│   └─────┬──────┘  └───────┬────────┘  └──────────┬──────────┘  │
└─────────┼─────────────────┼────────────────────── ┼────────────┘
          │ POST /upload     │ GET /documents         │ POST /query
          ▼                  ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Ingestion Pipeline                    │  │
│  │  File → Parser → Chunker → Embedder → FAISS Index        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Query Pipeline                       │  │
│  │  Query → Embedder → FAISS Search → LLM Provider → Answer │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────────────┐  │
│  │  FAISS Index │  │  SQLite DB    │  │  Uploaded Files    │  │
│  │  + metadata  │  │  (doc meta)   │  │  (data/uploads/)   │  │
│  └──────────────┘  └───────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ingestion Pipeline

```
POST /api/v1/documents/upload
         │
         ▼
    parser.py
  extract raw text
  (PDF → PyPDF2, TXT → decode)
         │
         ▼
    chunker.py
  sliding-window word chunks
  (default: 500 words, 50-word overlap)
         │
         ▼
    embedder.py
  sentence-transformers: all-MiniLM-L6-v2
  → dense float32 vectors (384 dims)
         │
         ▼
    retriever.py
  FAISS IndexFlatL2: add vectors
  pickle metadata (doc_id, chunk_index, text, filename)
         │
         ▼
    db/metadata.py
  SQLite: record document metadata
```

---

## Query Pipeline

```
POST /api/v1/query  {"question": "...", "top_k": 5}
         │
         ▼
    embedder.py
  encode question → query vector
         │
         ▼
    retriever.py
  FAISS nearest-neighbour search
  → top-k (doc_id, chunk_text, score)
         │
         ▼
    generator.py
  LLM provider (abstracted)
  default: ExtractiveLLMProvider
  (concatenates retrieved chunks into answer)
         │
         ▼
    QueryResponse
  { answer, citations[], query }
```

---

## Component Responsibilities

| Component | Responsibility |
|---|---|
| `app/api/routes/` | HTTP interface, request validation, error handling |
| `app/services/document_service.py` | Orchestrates the ingestion pipeline |
| `app/rag/parser.py` | Text extraction from supported file formats |
| `app/rag/chunker.py` | Sliding-window word chunking with overlap |
| `app/rag/embedder.py` | Singleton sentence-transformer wrapper |
| `app/rag/retriever.py` | FAISS index build/search/persist |
| `app/rag/generator.py` | Abstract LLM provider; pluggable for OpenAI etc. |
| `app/db/metadata.py` | SQLite document metadata CRUD |
| `app/core/config.py` | Centralised pydantic-settings config |

---

## Vector Store Choice: FAISS (IndexFlatL2)

**Why FAISS?**
- Runs fully **in-process** — no external service needed
- `IndexFlatL2` is exact nearest-neighbour (no approximation errors)
- Trivially persisted with `faiss.write_index` + `pickle` for metadata
- Easily swappable for `IndexIVFFlat` or Chroma when scale demands it

**Trade-off:** The full index is loaded into memory on each query. For production at scale, a dedicated vector DB (Chroma, Qdrant, Weaviate) would be preferable.

---

## LLM Provider Abstraction

`generator.py` defines `BaseLLMProvider` with a single `generate(query, chunks) → str` method. The factory `get_llm_provider()` returns the configured implementation:

| Provider | Key required | Behaviour |
|---|---|---|
| `extractive` (default) | None | Concatenates top-k chunks |
| `openai` | `OPENAI_API_KEY` | GPT chat completion |
| `anthropic` | `ANTHROPIC_API_KEY` | Claude messages API |

Adding a new provider requires only implementing `BaseLLMProvider` — no other code changes.

---

## Error Handling Strategy

- FastAPI HTTP exceptions with structured `{"detail": "..."}` bodies
- Unsupported file types → 400
- Index not found or empty → graceful empty citation list
- Config validation at startup via pydantic-settings

---

## Configuration

All runtime config is driven by environment variables (see `.env.example`). Pydantic-settings validates types at startup — no silent misconfiguration.
