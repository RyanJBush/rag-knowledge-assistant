from app.core.config import get_settings
from app.rag.vector_store import LocalVectorStore
from app.services.query_service import QueryService


def test_query_service_returns_citations(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("VECTOR_STORE_DIR", str(tmp_path / "vector_store"))
    get_settings.cache_clear()

    store = LocalVectorStore()
    store.upsert(
        [
            {
                "id": "doc-1::chunk-0",
                "embedding": [0.1] * 384,
                "metadata": {
                    "document_id": "doc-1",
                    "source": "sample.txt",
                    "chunk_id": "chunk-0",
                    "snippet": "Sample snippet",
                    "page": None,
                },
                "text": "Sample chunk text",
            }
        ]
    )

    service = QueryService()
    result = service.ask("What is in the sample?", top_k=1)

    assert "answer" in result
    assert result["retrieved_chunks"] == 1
    assert len(result["citations"]) == 1

    get_settings.cache_clear()
