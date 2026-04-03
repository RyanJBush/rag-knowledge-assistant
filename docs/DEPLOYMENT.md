# Deployment Guide (Phase 7)

## Recommended Hosting Split
- **Backend (FastAPI):** Render Web Service (free/student-friendly) or Railway.
- **Frontend (Vite React static):** Vercel or Netlify.
- **Why this split:** simplest DX, quick setup, and easy public demo URL sharing.

## 1) Backend Deployment (Render)

### A. Create service
1. Push repo to GitHub.
2. In Render, create a new **Web Service** from the repo.
3. Set root directory to `backend`.

### B. Build / Start commands
- Build command:
  ```bash
  pip install -e .[dev]
  ```
- Start command:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### C. Environment variables
Configure at least:
- `APP_ENV=production`
- `API_PREFIX=/api`
- `LOG_LEVEL=INFO`
- `CORS_ALLOWED_ORIGINS=https://<your-frontend-domain>` (comma-separate multiple origins, include localhost for local dev as needed)
- `UPLOAD_DIR=backend/data/uploads`
- `VECTOR_STORE_DIR=backend/data/vector_store`
- `MAX_UPLOAD_MB=10`
- `CHUNK_SIZE=800`
- `CHUNK_OVERLAP=120`
- `TOP_K=4`
- `EMBEDDING_PROVIDER=sentence-transformers`
- `EMBEDDING_MODEL=all-MiniLM-L6-v2`
- `LLM_PROVIDER=mock` (or `openai` if configured)
- `LLM_MODEL=local`
- `OPENAI_API_KEY` (optional)

### D. Verify backend deployment
- Open `${BACKEND_URL}/docs`.
- Verify `${BACKEND_URL}/api/health` returns `status: ok`.
- Upload a TXT file and run `/api/query` from docs UI.

## 2) Frontend Deployment (Vercel)

### A. Create project
1. Import GitHub repo in Vercel.
2. Set root directory to `frontend`.

### B. Build settings
- Install command: `npm install`
- Build command: `npm run build`
- Output directory: `dist`

### C. Environment variable
- `VITE_API_BASE_URL=<your_backend_url>/api`

### D. Verify frontend deployment
- Open deployed frontend URL.
- Upload sample document.
- Ask a question and verify citations are visible.

## 3) One-Command Local Demo Script (Optional)

```bash
# Terminal 1
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev
```

## 4) Practical Free/Student-Friendly Options
- Backend: Render, Railway, Fly.io.
- Frontend: Vercel, Netlify, Cloudflare Pages.
- Single-host fallback: Dockerize backend + frontend and deploy together on Railway/Fly.io.

## 5) Demo Checklist
- [ ] Backend health endpoint works in production.
- [ ] Upload TXT/PDF works.
- [ ] Query returns grounded answer.
- [ ] Citations include source + chunk id + snippet.
- [ ] Frontend handles loading/error states.
- [ ] README has setup + deployment + demo flow.

## 6) Production Notes
- Current storage is local filesystem (good for MVP demos).
- For persistent production use, move uploads + index to durable storage (S3 + managed DB/vector DB).
- Add auth/rate limiting before exposing publicly in multi-user mode.
