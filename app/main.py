from fastapi import FastAPI

import os
import uvicorn


def create_app() -> FastAPI:
    app = FastAPI(title="rag-fastapi")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/")
    def root():
        return {"message": "rag-fastapi is running"}

    return app

app = create_app()