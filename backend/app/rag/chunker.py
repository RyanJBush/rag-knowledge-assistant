from typing import Any


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[dict[str, Any]]:
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append({
            "text": " ".join(chunk_words),
            "chunk_index": chunk_index,
        })
        if end == len(words):
            break
        start += chunk_size - chunk_overlap
        chunk_index += 1

    return chunks
