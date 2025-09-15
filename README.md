# rag-fastapi
A Python FastAPI service for secure per-user document upload, listing, and deletion, with S3-compatible storage and JWT authentication.

## Contents
- [Stack](#stack)
- [API endpoints](#api-endpoints)
- [Features](#features)
- [Development plan](#development-plan)
- [Run locally](#run-locally)

## Stack
- Python
- FastAPI
- PostgreSQL
- S3-compatible storage (AWS S3 or LocalStack)

## API endpoints (MVP)
- Auth
	- POST /auth/register — create user
	- POST /auth/login — get JWT access (and optional refresh)
	- GET  /me — current user (requires Bearer token)
- Documents
	- POST /documents/upload — upload file (or presigned flow later)
	- GET  /documents — list user documents
	- DELETE /documents/{id} — delete document
- Health
	- GET /healthz — liveness check

## Features
- Per-user secure document storage and access control
- Unique filenames enforced per user to prevent duplicates
- JWT-based authentication for all endpoints
- Presigned S3 URLs for secure file downloads
- CI with LocalStack S3 and Postgres for reliable testing

## Development plan:
- Setup repo, envs, project structure, etc
- Implement basic API auth endpoints
- Implement document upload
- Observability: structured logs, metrics, tracing
- Tests & CI: unit/integration/E2E + GitHub Actions, pre-commit hooks
- Deploy: Docker Compose for dev; cloud Postgres + object storage

## Run locally
1. **Start dependencies with Docker Compose**

    ```bash
    docker compose up -d
    ```

    This will start both Postgres and LocalStack S3 locally.

2. **Run database migrations**:

    ```bash
    alembic upgrade head
    ```

3. **Create a virtual env and install dependencies**
   
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    ```

4. **Start the API**

	```bash
	uvicorn app.main:app --port 8000
	```

5. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and check `/healthz` or the docs at `/docs`.