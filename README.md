# rag-fastapi
Python FastAPI service that ingests documents and answers questions with cited responses using retrieval‑augmented generation (RAG).

## Stack
- Python
- FastAPI
- PostgreSQL
- LLM (Haven't decided which one yet)

## API endpoints (MVP)
- Auth
	- POST /auth/register — create user
	- POST /auth/login — get JWT access (and optional refresh)
	- POST /auth/refresh — refresh access token (if used)
	- GET  /me — current user (requires Bearer token)
- Documents
	- POST /documents/upload — upload file (or presigned flow later)
	- GET  /documents — list user documents
	- DELETE /documents/{id} — delete document
- QA
	- POST /qa/query — ask question
- Health
	- GET /healthz — liveness check

## Development plan:
- Setup repo, envs, project structure, etc
- Implement basic API auth endpoints
- Implement document upload
- Ingestion pipeline: extract text, chunk, embed, and index in a vector store
- RAG query endpoint: retrieve top-k (per user), generate answer with citations
- Observability: structured logs, metrics, tracing
- Security: per-user filtering, size/type limits
- Tests & CI: unit/integration/E2E + GitHub Actions, pre-commit hooks
- Deploy: Docker Compose for dev; cloud Postgres + object storage + vector DB

## Run locally
1. Create a virtual env and install dependencies
   
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -U pip
	pip install -r requirements.txt
	```

2. Start the API

	```bash
	uvicorn app.main:app --reload --port 8000
	```

3. Open http://127.0.0.1:8000 and check `/healthz` or the docs at `/docs`.