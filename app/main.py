from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as documents_router

import os
import uvicorn


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

app = create_app()