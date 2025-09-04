from __future__ import annotations

from typing import cast
import io
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient

import app.api.deps as deps_mod
import app.api.routes.documents as docs_mod


class _User:
    def __init__(self, id_: str = "user-123"):
        self.id = id_


def _auth_override():
    return _User()


def _set_auth_override(client: TestClient):
    app = cast(FastAPI, client.app)
    app.dependency_overrides[deps_mod.get_current_user] = _auth_override


def _clear_auth_override(client: TestClient):
    app = cast(FastAPI, client.app)
    app.dependency_overrides.pop(deps_mod.get_current_user, None)


"""
For this test suite, we mock out the actual S3 upload to avoid external dependencies, we do
this using monkeypatching to replace the upload_fileobj function with a fake one.
"""
def test_upload_success(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    _set_auth_override(client)

    def fake_upload_fileobj(user_id: str, doc_id: str, filename: str, fileobj):
        assert user_id == "user-123"
        assert filename == "hello.txt"
        return {
            "bucket": "rag-documents",
            "key": f"users/{user_id}/docs/{doc_id}/{filename}",
            "doc_id": doc_id,
        }

    monkeypatch.setattr(docs_mod, "upload_fileobj", fake_upload_fileobj, raising=True)

    files = {"file": ("hello.txt", io.BytesIO(b"hello world"), "text/plain")}
    resp = client.post("/documents/upload", files=files)

    _clear_auth_override(client)

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["bucket"] == "rag-documents"
    assert data["key"].endswith("/hello.txt")
    assert "doc_id" in data and isinstance(data["doc_id"], str)

def test_upload_duplicate_filename(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    _set_auth_override(client)

    def fake_upload_fileobj(user_id: str, doc_id: str, filename: str, fileobj):
        raise docs_mod.DuplicateFilenameError(filename)

    monkeypatch.setattr(docs_mod, "upload_fileobj", fake_upload_fileobj, raising=True)

    files = {"file": ("dup.txt", io.BytesIO(b"bytes"), "text/plain")}
    response = client.post("/documents/upload", files=files)

    _clear_auth_override(client)

    assert response.status_code in (400, 409)
    body = response.json()
    assert "detail" in body and isinstance(body["detail"], dict)
    detail = body["detail"]
    assert detail.get("code") == "file already exists"
    assert detail.get("filename") == "dup.txt"
