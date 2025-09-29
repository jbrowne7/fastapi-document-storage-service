from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as documents_router
from app.services.storage import ensure_bucket
from app.core.config import settings
import sys, os


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

print(f"settings.database_host: {settings.DATABASE_HOST}")
print("Done")
sys.exit(0)
# print(f"os database host: {os.getenv("DATABASE_HOST")}")

ensure_bucket(settings.S3_BUCKET)
app = create_app()