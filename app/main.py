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

print("DATABASE_PASSWORD:", settings.DATABASE_PASSWORD)
ensure_bucket(settings.S3_BUCKET)
app = create_app()