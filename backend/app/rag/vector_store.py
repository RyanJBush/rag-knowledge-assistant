from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.config import get_settings


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = (sum(x * x for x in a) ** 0.5) or 1.0
    norm_b = (sum(x * x for x in b) ** 0.5) or 1.0
    return dot / (norm_a * norm_b)


class LocalVectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.store_path = Path(settings.vector_store_dir)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.store_path / "index.json"
        if not self.index_file.exists():
            self.index_file.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        return json.loads(self.index_file.read_text(encoding="utf-8"))

    def _save(self, records: list[dict[str, Any]]) -> None:
        self.index_file.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    def upsert(self, records: list[dict[str, Any]]) -> None:
        current = self._load()
        existing_ids = {record["id"] for record in records}
        filtered = [row for row in current if row["id"] not in existing_ids]
        filtered.extend(records)
        self._save(filtered)

    def query(self, embedding: list[float], top_k: int) -> list[dict[str, Any]]:
        records = self._load()
        ranked = []
        for row in records:
            score = _cosine(embedding, row["embedding"])
            ranked.append({"score": score, **row})
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:top_k]
