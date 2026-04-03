# Phase 1 — Planning: RAG-Based AI Knowledge Assistant

## 1) Concise Project Overview
Build a production-oriented, local-first internal knowledge assistant that ingests PDF/TXT files, indexes chunked text embeddings in a vector store, and answers user questions with grounded citations through a FastAPI + React dashboard.

This MVP is intentionally scoped for a **3–7 day build** while still demonstrating strong engineering fundamentals:
- modular backend service architecture
- explainable RAG with source citations
- full-stack integration
- deployment-ready project hygiene

## 2) Target User / Use Case
### Primary User Persona
**Operations analyst / team member** at a small company who needs fast answers from internal docs (SOPs, onboarding docs, policies, meeting notes) without manually searching files.

### Business Use Case
“I upload internal documents once, then ask questions and get concise answers with citation snippets so I can trust and verify responses.”

## 3) Core Features (MVP In Scope)
1. **Document upload** (PDF + TXT for MVP).
2. **Text extraction + chunking** (fixed-size chunks with overlap).
3. **Embeddings + vector indexing** (local persistent vector store).
4. **Grounded question answering** endpoint.
5. **Structured citations** in every answer:
   - source document name
   - chunk id
   - snippet (and page number when available)
6. **Document library listing** endpoint.
7. **Frontend dashboard** with:
   - upload panel
   - document list
   - chat-style query UI
   - citation display
8. **Basic quality/tooling**:
   - pytest, ruff, eslint, prettier
   - env-based config
   - clear README + scripts

## 4) Non-Goals (Out of Scope for MVP)
- Multi-user auth and RBAC.
- Real-time collaborative chat.
- Advanced eval pipelines / tracing stacks.
- OCR-heavy scans and complex document layouts.
- Hybrid retrieval tuning, rerankers, and agentic workflows.
- Production-grade observability stack (keep lightweight logs only).

## 5) MVP Success Criteria
Project is successful when all are true:
1. User can upload at least one PDF/TXT and see it listed.
2. Query returns an answer grounded in retrieved chunks.
3. Response always includes top-k citations in structured JSON.
4. Frontend clearly displays answer + linked source context.
5. App runs locally with straightforward setup in README.
6. Basic tests/linting pass in CI-like local workflow.
7. Demo can be shown end-to-end in under 5 minutes.

## 6) Proposed Final Folder Structure
```text
rag-knowledge-assistant/
  README.md
  .gitignore
  .editorconfig
  .env.example
  Makefile
  backend/
    pyproject.toml
    app/
      api/
        routes/
          health.py
          documents.py
          query.py
      core/
        config.py
        logging.py
      schemas/
        common.py
        document.py
        query.py
      services/
        document_service.py
        ingestion_service.py
        query_service.py
      rag/
        parser.py
        chunker.py
        embedder.py
        vector_store.py
        generator.py
      db/
        models.py
        session.py
      main.py
    tests/
      test_health.py
      test_upload.py
      test_query.py
    data/
      uploads/
      vector_store/
  frontend/
    package.json
    tsconfig.json
    vite.config.ts
    src/
      App.tsx
      main.tsx
      components/
        layout/
        upload/
        documents/
        chat/
        citations/
      pages/
        DashboardPage.tsx
      lib/
        api.ts
      hooks/
        useUpload.ts
        useQuery.ts
        useDocuments.ts
      types/
        api.ts
```

## 7) Implementation Plan for Later Phases
### Phase 2 — Architecture
- Finalize module boundaries and request/response contracts.
- Define ingestion/query sequence diagrams.
- Choose vector store and generation fallback strategy.

### Phase 3 — Setup
- Scaffold backend + frontend structure.
- Configure linting, formatting, tests, env, and scripts.
- Add starter health endpoint + basic UI shell.

### Phase 4 — Backend
- Implement upload, parsing, chunking, embedding/indexing pipeline.
- Implement query endpoint with retrieval and structured citations.
- Add robust validation and predictable error responses.

### Phase 5 — Frontend
- Build dashboard with upload + library + chat + citations.
- Integrate API client and loading/error states.
- Add simple but polished enterprise-style UI.

### Phase 6 — Testing
- Add backend endpoint and pipeline structure tests.
- Add lint/format checks and optional frontend smoke test.
- Document covered/not-covered areas.

### Phase 7 — Deployment
- Add deployment instructions (backend + frontend split).
- Improve README with demo steps and env setup.
- Provide portfolio talking points + resume bullets.

## 8) Why This Project Is High-Signal for Recruiters
This project demonstrates practical, interview-friendly skills across:
- **AI Engineering**: end-to-end RAG with grounded citation outputs.
- **Backend Engineering**: modular FastAPI services and clear API contracts.
- **Frontend Product Thinking**: clean UX for upload, query, and transparency.
- **Production Mindset**: env config, lint/test tooling, deployment readiness.

It’s realistic enough to finish quickly, while still looking like a professional internal AI tool rather than a toy chatbot.
