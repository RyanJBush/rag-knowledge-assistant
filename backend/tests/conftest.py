from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

# Embedding dimension used by all-MiniLM-L6-v2.
_EMBED_DIM = 384


def _make_mock_st():
    """Return a MagicMock that behaves like SentenceTransformer for tests."""
    mock = MagicMock()
    mock.get_sentence_embedding_dimension.return_value = _EMBED_DIM

    def _encode(texts, **kwargs):
        n = len(texts) if isinstance(texts, list) else 1
        return np.random.rand(n, _EMBED_DIM).astype(np.float32)

    mock.encode.side_effect = _encode
    return mock


@pytest.fixture(scope="session", autouse=True)
def mock_sentence_transformer():
    """Patch SentenceTransformer globally for the entire test session.

    This avoids any network I/O (HuggingFace downloads) and the httpx
    closed-client error that occurs when sentence-transformers retries
    inside Starlette's async TestClient context.
    """
    mock_st = _make_mock_st()
    with patch("sentence_transformers.SentenceTransformer", return_value=mock_st):
        # Pre-populate the class-level cache so Embedder() never calls the
        # real SentenceTransformer constructor inside an async context.
        from app.rag.embedder import Embedder

        Embedder._model = mock_st
        yield mock_st


@pytest.fixture(scope="session")
def client(mock_sentence_transformer):
    from app.main import app

    with TestClient(app) as c:
        yield c
