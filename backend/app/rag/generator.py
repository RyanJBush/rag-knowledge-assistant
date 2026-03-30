from abc import ABC, abstractmethod
from typing import Any

from app.core.config import settings


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, query: str, chunks: list[dict[str, Any]]) -> str:
        pass


class ExtractiveLLMProvider(BaseLLMProvider):
    def generate(self, query: str, chunks: list[dict[str, Any]]) -> str:
        if not chunks:
            return "No relevant information found for your query."

        combined = "\n\n".join(c["chunk_text"] for c in chunks)
        return f"Based on the retrieved documents:\n\n{combined}"


def get_llm_provider() -> BaseLLMProvider:
    if settings.llm_provider == "extractive":
        return ExtractiveLLMProvider()
    return ExtractiveLLMProvider()
