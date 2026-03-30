.PHONY: backend-install backend-run backend-test backend-lint frontend-install frontend-run frontend-lint

backend-install:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -e .[dev]

backend-run:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000

backend-test:
	cd backend && . .venv/bin/activate && pytest

backend-lint:
	cd backend && . .venv/bin/activate && ruff check . && ruff format --check .

frontend-install:
	cd frontend && npm install

frontend-run:
	cd frontend && npm run dev

frontend-lint:
	cd frontend && npm run lint
