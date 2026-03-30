def chunk_text(text: str, chunk_size: int, overlap: int) -> list[dict]:
    chunks: list[dict] = []
    normalized = " ".join(text.split())

    if not normalized:
        return chunks

    step = max(chunk_size - overlap, 1)
    index = 0
    chunk_id = 0

    while index < len(normalized):
        snippet = normalized[index : index + chunk_size]
        chunks.append(
            {
                "chunk_id": f"chunk-{chunk_id}",
                "text": snippet,
                "start": index,
                "end": min(index + chunk_size, len(normalized)),
            }
        )
        chunk_id += 1
        index += step

    return chunks
