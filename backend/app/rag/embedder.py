from __future__ import annotations

from functools import lru_cache
import hashlib

from app.core.config import get_settings


@lru_cache
def _try_sentence_transformer():
    try:
        from sentence_transformers import SentenceTransformer

        settings = get_settings()
        return SentenceTransformer(settings.embedding_model)
    except Exception:
        return None


def _deterministic_embedding(text: str, dimensions: int = 384) -> list[float]:
    seed = hashlib.sha256(text.encode("utf-8")).digest()
    values: list[float] = []
    while len(values) < dimensions:
        seed = hashlib.sha256(seed).digest()
        for byte in seed:
            values.append((byte / 255.0) * 2 - 1)
            if len(values) >= dimensions:
                break
    return values


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = _try_sentence_transformer()
    if model is not None:
        vectors = model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]
    return [_deterministic_embedding(text) for text in texts]
