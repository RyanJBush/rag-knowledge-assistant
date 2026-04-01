import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class Embedder:
    _model: SentenceTransformer | None = None

    def __init__(self) -> None:
        if Embedder._model is None:
            Embedder._model = SentenceTransformer(settings.embedding_model)

    def encode(self, texts: list[str]) -> np.ndarray:
        return Embedder._model.encode(texts, convert_to_numpy=True)  # type: ignore[union-attr]
