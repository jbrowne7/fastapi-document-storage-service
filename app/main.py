from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as documents_router
from app.services.storage import ensure_bucket
from app.core.config import settings


def create_app() -> FastAPI:

    app = FastAPI(title="rag-fastapi")

    # Routers
    app.include_router(auth_router)
    app.include_router(documents_router)
    
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/")
    def root():
        return {"message": "rag-fastapi is running"}

    return app

import os, sys
print("ECS ENVIRONMENT VARIABLES:")
for key in ["DATABASE_USER", "DATABASE_PASSWORD", "DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME"]:
    print(f"{key}: {os.getenv(key)}")
sys.exit(0)
ensure_bucket(settings.S3_BUCKET)
app = create_app()