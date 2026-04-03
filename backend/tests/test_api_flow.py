import json

from fastapi.testclient import TestClient

from app.api.routes import documents as document_routes
from app.api.routes import query as query_routes
from app.main import app


client = TestClient(app)


def _configure_temp_storage(tmp_path) -> None:
    upload_dir = tmp_path / "uploads"
    vector_dir = tmp_path / "vector_store"
    upload_dir.mkdir(parents=True, exist_ok=True)
    vector_dir.mkdir(parents=True, exist_ok=True)

    document_routes.document_service.upload_dir = upload_dir
    document_routes.document_service.metadata_file = upload_dir / "documents.json"
    document_routes.document_service.metadata_file.write_text("[]", encoding="utf-8")
    document_routes.document_service.max_upload_bytes = 10 * 1024 * 1024

    index_file = vector_dir / "index.json"
    index_file.write_text("[]", encoding="utf-8")

    document_routes.ingestion_service.vector_store.store_path = vector_dir
    document_routes.ingestion_service.vector_store.index_file = index_file

    query_routes.query_service.vector_store.store_path = vector_dir
    query_routes.query_service.vector_store.index_file = index_file


def test_upload_and_query_flow(tmp_path) -> None:
    _configure_temp_storage(tmp_path)

    upload_response = client.post(
        "/api/documents/upload",
        files={
            "file": (
                "policy.txt",
                b"All employees must use MFA. Passwords rotate every 90 days.",
                "text/plain",
            )
        },
    )
    assert upload_response.status_code == 200
    payload = upload_response.json()
    assert payload["filename"] == "policy.txt"
    assert payload["chunks_indexed"] > 0

    query_response = client.post(
        "/api/query",
        json={"question": "What is the MFA policy?", "top_k": 3},
    )
    assert query_response.status_code == 200
    answer = query_response.json()

    assert isinstance(answer["answer"], str)
    assert answer["retrieved_chunks"] >= 1
    assert len(answer["citations"]) >= 1
    assert {"source", "chunk_id", "snippet", "score"}.issubset(answer["citations"][0].keys())


def test_upload_rejects_unsupported_content_type(tmp_path) -> None:
    _configure_temp_storage(tmp_path)

    response = client.post(
        "/api/documents/upload",
        files={"file": ("malware.exe", b"fake-binary", "application/octet-stream")},
    )
    assert response.status_code == 400
    payload = response.json()
    assert payload["code"] == "unsupported_file_type"


def test_query_without_documents_returns_404(tmp_path) -> None:
    _configure_temp_storage(tmp_path)

    response = client.post(
        "/api/query",
        json={"question": "Any docs?", "top_k": 2},
    )
    assert response.status_code == 404
    payload = response.json()
    assert payload["code"] == "no_documents_indexed"

    index_file = query_routes.query_service.vector_store.index_file
    assert json.loads(index_file.read_text(encoding="utf-8")) == []
