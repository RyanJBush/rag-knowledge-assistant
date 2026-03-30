import os

import pytest
from fastapi.testclient import TestClient

# Prevent huggingface_hub from making network requests during tests.
# The model will be created locally with mean pooling, which is sufficient
# for integration tests that only need consistent embedding dimensions.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


@pytest.fixture(scope="session", autouse=True)
def preload_embedder():
    """Pre-load the embedding model in synchronous (non-async) context.

    sentence-transformers network retries interact badly with the anyio event
    loop used by Starlette's TestClient.  Loading the model once here — before
    any async context is active — lets huggingface_hub fail gracefully, after
    which SentenceTransformer falls back to creating a local mean-pooling model.
    Subsequent calls reuse the cached class-level ``Embedder._model``.
    """
    # Temporarily allow network so the fallback model-creation path runs;
    # then re-enable offline mode so no further network calls are attempted.
    os.environ.pop("HF_HUB_OFFLINE", None)
    os.environ.pop("TRANSFORMERS_OFFLINE", None)
    try:
        from app.rag.embedder import Embedder

        Embedder()  # populates Embedder._model; network errors are caught internally
    except Exception:
        pass
    finally:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"


@pytest.fixture(scope="session")
def client(preload_embedder):
    from app.main import app

    with TestClient(app) as c:
        yield c
