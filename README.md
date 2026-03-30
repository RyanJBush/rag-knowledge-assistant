# RAG Knowledge Assistant

Production-oriented, portfolio-ready RAG (Retrieval-Augmented Generation) knowledge assistant.

## Current Status
- ✅ Phase 1: Planning
- ✅ Phase 2: Architecture
- ✅ Phase 3: Setup
- ✅ Phase 4: Backend MVP (ingestion + retrieval + citations)
- ✅ Phase 5: Frontend dashboard + chat UI
- ✅ Phase 6: Testing baseline
- ✅ Phase 7: Deployment guidance + portfolio packaging

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open:
- Frontend: http://localhost:5173
- Backend docs: http://localhost:8000/docs

## API Examples

### Health
```bash
curl http://localhost:8000/api/health
```

### Upload a document
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./sample.txt;type=text/plain"
```

### List documents
```bash
curl http://localhost:8000/api/documents
```

### Query documents
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the document say?","top_k":4}'
```

### Frontend env
Set `VITE_API_BASE_URL` (optional) to point to your backend API base. Default is `http://localhost:8000/api`.

## Testing

### Backend
```bash
cd backend
source .venv/bin/activate
pytest
ruff check .
ruff format --check .
```

### Frontend
```bash
cd frontend
npm run lint
```

## Deployment
- Detailed deployment steps: `docs/DEPLOYMENT.md`
- Portfolio talking points and resume bullets: `docs/PORTFOLIO.md`

### Recommended hosting split
- **Backend:** Render or Railway
- **Frontend:** Vercel or Netlify

## Demo Checklist
- Upload at least one TXT/PDF document.
- Ask a question grounded in uploaded content.
- Verify returned citations include source + chunk id + snippet.
- Show error-handling states (e.g., query before upload).
