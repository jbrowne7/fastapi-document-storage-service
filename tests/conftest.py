import time
from fastapi import FastAPI
import pytest
import os, sys
from fastapi.testclient import TestClient
from sqlalchemy import text


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.main import app
from app.db.base import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # wait for DB
    for _ in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except Exception:
            time.sleep(1)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)