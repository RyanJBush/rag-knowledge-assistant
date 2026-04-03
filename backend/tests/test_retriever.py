from unittest.mock import patch

import numpy as np
import pytest

from app.rag.retriever import INDEX_FILE, META_FILE, Retriever

_DIM = 4


def _random_embeddings(n: int, dim: int = _DIM) -> np.ndarray:
    rng = np.random.default_rng(42)
    return rng.random((n, dim)).astype(np.float32)


@pytest.fixture()
def tmp_retriever(tmp_path):
    """Return a Retriever whose storage is pointed at a temp directory."""
    with patch("app.rag.retriever.settings") as mock_settings:
        mock_settings.vector_store_dir = tmp_path
        r = Retriever()
        # Manually set the paths to use tmp_path
        r.index_path = tmp_path / INDEX_FILE
        r.meta_path = tmp_path / META_FILE
        yield r


def test_build_index(tmp_retriever):
    tmp_retriever.build_index(_DIM)
    assert tmp_retriever.index is not None
    assert tmp_retriever.index.ntotal == 0


def test_add_documents_populates_index(tmp_retriever):
    embeddings = _random_embeddings(3)
    chunks = [
        {"chunk_index": 0, "text": "first chunk"},
        {"chunk_index": 1, "text": "second chunk"},
        {"chunk_index": 2, "text": "third chunk"},
    ]
    tmp_retriever.add_documents(embeddings, "doc-1", chunks, "test.txt")
    assert tmp_retriever.index.ntotal == 3
    assert len(tmp_retriever.metadata) == 3


def test_add_documents_metadata_fields(tmp_retriever):
    embeddings = _random_embeddings(1)
    chunks = [{"chunk_index": 0, "text": "hello world"}]
    tmp_retriever.add_documents(embeddings, "doc-42", chunks, "file.txt")
    meta = tmp_retriever.metadata[0]
    assert meta["document_id"] == "doc-42"
    assert meta["chunk_index"] == 0
    assert meta["chunk_text"] == "hello world"
    assert meta["source_filename"] == "file.txt"


def test_search_empty_index_returns_empty(tmp_retriever):
    query = _random_embeddings(1)
    results = tmp_retriever.search(query, top_k=5)
    assert results == []


def test_search_returns_results(tmp_retriever):
    embeddings = _random_embeddings(5)
    chunks = [{"chunk_index": i, "text": f"chunk {i}"} for i in range(5)]
    tmp_retriever.add_documents(embeddings, "doc-1", chunks, "doc.txt")

    query = embeddings[:1]
    results = tmp_retriever.search(query, top_k=3)
    assert len(results) == 3
    assert all("score" in r for r in results)
    assert all("chunk_text" in r for r in results)


def test_search_top_k_clamped_to_total(tmp_retriever):
    embeddings = _random_embeddings(2)
    chunks = [{"chunk_index": i, "text": f"chunk {i}"} for i in range(2)]
    tmp_retriever.add_documents(embeddings, "doc-1", chunks, "doc.txt")

    results = tmp_retriever.search(embeddings[:1], top_k=10)
    assert len(results) == 2


def test_search_result_has_score_field(tmp_retriever):
    embeddings = _random_embeddings(1)
    chunks = [{"chunk_index": 0, "text": "only chunk"}]
    tmp_retriever.add_documents(embeddings, "doc-1", chunks, "doc.txt")

    results = tmp_retriever.search(embeddings, top_k=1)
    assert isinstance(results[0]["score"], float)


def test_save_and_load_roundtrip(tmp_retriever, tmp_path):
    embeddings = _random_embeddings(3)
    chunks = [{"chunk_index": i, "text": f"chunk {i}"} for i in range(3)]
    tmp_retriever.add_documents(embeddings, "doc-1", chunks, "source.txt")
    tmp_retriever.save()

    assert tmp_retriever.index_path.exists()
    assert tmp_retriever.meta_path.exists()

    # Load into a fresh retriever pointing at the same temp dir
    with patch("app.rag.retriever.settings") as mock_settings:
        mock_settings.vector_store_dir = tmp_path
        r2 = Retriever()
        r2.index_path = tmp_retriever.index_path
        r2.meta_path = tmp_retriever.meta_path
        r2.load()

    assert r2.index is not None
    assert r2.index.ntotal == 3
    assert len(r2.metadata) == 3


def test_save_empty_index_writes_meta_only(tmp_retriever):
    # save() should not crash when index is None, and should still write metadata
    tmp_retriever.save()
    assert tmp_retriever.meta_path.exists()


def test_load_missing_files_is_a_noop(tmp_retriever):
    # load() with no files on disk should leave index=None and metadata=[]
    tmp_retriever.load()
    assert tmp_retriever.index is None
    assert tmp_retriever.metadata == []


def test_multiple_add_documents_accumulates(tmp_retriever):
    e1 = _random_embeddings(2)
    e2 = _random_embeddings(2)
    chunks1 = [{"chunk_index": i, "text": f"doc1 chunk {i}"} for i in range(2)]
    chunks2 = [{"chunk_index": i, "text": f"doc2 chunk {i}"} for i in range(2)]
    tmp_retriever.add_documents(e1, "doc-1", chunks1, "a.txt")
    tmp_retriever.add_documents(e2, "doc-2", chunks2, "b.txt")
    assert tmp_retriever.index.ntotal == 4
    assert len(tmp_retriever.metadata) == 4
