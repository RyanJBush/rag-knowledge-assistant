import pickle
from typing import Any

import faiss
import numpy as np

from app.core.config import settings

INDEX_FILE = "faiss.index"
META_FILE = "faiss_meta.pkl"


class Retriever:
    def __init__(self) -> None:
        self.index: faiss.Index | None = None
        self.metadata: list[dict[str, Any]] = []
        self.index_path = settings.vector_store_dir / INDEX_FILE
        self.meta_path = settings.vector_store_dir / META_FILE

    def build_index(self, dim: int) -> None:
        self.index = faiss.IndexFlatL2(dim)

    def add_documents(
        self,
        embeddings: np.ndarray,
        document_id: str,
        chunks: list[dict[str, Any]],
        source_filename: str,
    ) -> None:
        if self.index is None:
            self.build_index(embeddings.shape[1])

        self.index.add(embeddings.astype(np.float32))  # type: ignore[union-attr]

        for chunk in chunks:
            self.metadata.append({
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "chunk_text": chunk["text"],
                "source_filename": source_filename,
            })

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> list[dict[str, Any]]:
        if self.index is None or self.index.ntotal == 0:
            return []

        k = min(top_k, self.index.ntotal)
        distances, indices = self.index.search(
            query_embedding.astype(np.float32), k
        )

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            result = dict(self.metadata[idx])
            result["score"] = float(dist)
            results.append(result)

        return results

    def save(self) -> None:
        settings.vector_store_dir.mkdir(parents=True, exist_ok=True)
        if self.index is not None:
            faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self) -> None:
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        if self.meta_path.exists():
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)  # noqa: S301
