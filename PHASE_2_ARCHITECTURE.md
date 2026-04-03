# Phase 2 — Architecture: RAG-Based AI Knowledge Assistant

## 1) Architecture Summary
The system uses a **clean, modular full-stack architecture**:
- **Frontend (React + TypeScript + Tailwind)** handles document upload, document library browsing, and chat-style querying.
- **Backend (FastAPI)** exposes API endpoints for health, ingestion, document listing, and query.
- **RAG pipeline** parses files, chunks text, creates embeddings, stores vectors, retrieves top-k relevant chunks, and generates grounded answers with citations.
- **Local-first persistence** stores files and vectors on disk to keep setup simple and portfolio-friendly.

Design goal: look production-oriented without overengineering for a 3–7 day build.

## 2) Backend Module Responsibilities
### `app/api/routes/`
- `health.py`: liveness/ready checks.
- `documents.py`: upload and list endpoints.
- `query.py`: question-answer endpoint returning structured answer + citations.

### `app/core/`
- `config.py`: settings from environment variables via Pydantic settings.
- `logging.py`: centralized logging format + log level setup.

### `app/schemas/`
- Request/response DTOs for upload, document metadata, query request, query response, citation model, and API errors.

### `app/services/`
- `document_service.py`: file storage + document metadata operations.
- `ingestion_service.py`: orchestrates parse → chunk → embed → index.
- `query_service.py`: orchestrates retrieve → generate → format citations.

### `app/rag/`
- `parser.py`: extract text from PDF/TXT.
- `chunker.py`: fixed-size + overlap chunking with metadata.
- `embedder.py`: embedding model adapter.
- `vector_store.py`: vector upsert/search abstraction.
- `generator.py`: answer generation abstraction (local fallback + optional API).

### `app/db/` (lightweight optional)
- SQLite tables for document metadata and ingestion timestamps.
- Useful recruiter signal with minimal complexity.

## 3) Frontend Page/Component Responsibilities
### Pages
- `DashboardPage`: composed enterprise layout (left: upload/library, right: chat/results).

### Components
- `UploadPanel`: file picker + upload status.
- `DocumentLibrary`: list of ingested docs with metadata.
- `ChatPanel`: question input + answer stream area.
- `AnswerCard`: final response rendering.
- `CitationList`: source document, chunk id, snippet/page reference.
- `RetrievalDebugPanel` (optional): top-k retrieved chunks for transparency.

### Frontend Library Layer
- `lib/api.ts`: typed API client.
- `types/api.ts`: shared request/response interfaces.
- `hooks/*`: data hooks for upload/documents/query state and loading/error handling.

## 4) Ingestion Flow (Upload → Extract → Chunk → Embed → Index)
1. User uploads PDF/TXT to `/api/documents/upload`.
2. Backend validates extension/size and saves file to `data/uploads/`.
3. Parser extracts normalized text and page metadata (when available).
4. Chunker splits text into fixed-size chunks with overlap (simple + explainable).
5. Embedder computes vector for each chunk.
6. Vector store writes vectors + metadata (doc id, chunk id, source filename, snippet/page).
7. Backend returns ingestion summary (document id, chunks indexed, status).

## 5) Query Flow (Question → Retrieve → Generate → Cite)
1. User sends question to `/api/query`.
2. Query is embedded with same embedding model.
3. Vector store performs top-k similarity search.
4. Query service builds grounded context from retrieved chunks.
5. Generator produces answer using retrieved context only (plus fallback mode if no external API key).
6. Response includes:
   - `answer`
   - `citations[]` (source, chunk id, snippet/page, relevance score)
   - optional `debug.retrieved_chunks` for transparency.

## 6) Vector Store Choice + Justification
**Choice: Chroma (local persistent mode)** for MVP.

Why:
- simple local persistence out of the box
- easy developer experience and retrieval API
- works well for student/local demos without infra overhead
- fast enough for portfolio-scale corpora

Alternative (FAISS) can be introduced later for speed tuning; Chroma is better for quick, clean delivery.

## 7) Configuration Strategy
Use environment-driven config via `pydantic-settings`:
- app env: `APP_ENV`, `LOG_LEVEL`, `API_PREFIX`
- file handling: `MAX_UPLOAD_MB`, `UPLOAD_DIR`
- chunking: `CHUNK_SIZE`, `CHUNK_OVERLAP`
- retrieval: `TOP_K`
- embeddings: `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL`
- generation: `LLM_PROVIDER`, `LLM_MODEL`, `OPENAI_API_KEY` (optional)
- vector db: `VECTOR_STORE_DIR`, `COLLECTION_NAME`

Include `.env.example` with sane local defaults and fallback-friendly behavior.

## 8) Error Handling Strategy
- Centralized exception handlers for validation and domain errors.
- Consistent error response schema:
  - `code`
  - `message`
  - `details` (optional)
- Defensive checks:
  - unsupported file type
  - empty extracted text
  - oversized uploads
  - no indexed docs found
  - retrieval returns no relevant chunks
- User-safe messaging on frontend + developer-useful logs on backend.

## 9) Why This Architecture Is Scalable + Recruiter-Friendly
- Clear separation of concerns (API vs services vs RAG internals).
- Pluggable embeddings/generation providers through adapters and config.
- Predictable schemas and typed frontend integration.
- Local-first MVP that can evolve to cloud storage/vector DB later.
- Demonstrates production thinking (config, error contracts, modularity) while staying buildable in under a week.
