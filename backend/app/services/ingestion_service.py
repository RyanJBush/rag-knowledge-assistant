from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.rag.chunker import chunk_text
from app.rag.embedder import embed_texts
from app.rag.parser import extract_text
from app.rag.vector_store import LocalVectorStore


class IngestionService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.vector_store = LocalVectorStore()

    def ingest_document(self, document_record: dict) -> int:
        text, page_map = extract_text(Path(document_record["path"]), document_record["content_type"])
        if not text.strip():
            raise AppError("empty_document", "Extracted document text is empty.", 400)

        chunks = chunk_text(
            text=text,
            chunk_size=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )
        if not chunks:
            raise AppError("chunking_failed", "No chunks could be produced.", 500)

        embeddings = embed_texts([chunk["text"] for chunk in chunks])

        records = []
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            page = None
            for page_info in page_map:
                if page_info["start"] <= chunk["start"] <= page_info["end"]:
                    page = page_info.get("page")
                    break
            records.append(
                {
                    "id": f"{document_record['document_id']}::{chunk['chunk_id']}",
                    "embedding": embedding,
                    "metadata": {
                        "document_id": document_record["document_id"],
                        "source": document_record["filename"],
                        "chunk_id": chunk["chunk_id"],
                        "snippet": chunk["text"][:240],
                        "page": page,
                    },
                    "text": chunk["text"],
                }
            )

        self.vector_store.upsert(records)
        return len(records)
