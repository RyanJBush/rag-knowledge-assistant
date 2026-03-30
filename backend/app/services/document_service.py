import logging
from datetime import datetime, timezone

from app.core.config import settings
from app.db.metadata import save_document
from app.rag.chunker import chunk_text
from app.rag.embedder import Embedder
from app.rag.parser import parse_document
from app.rag.retriever import Retriever
from app.schemas.document import DocumentUploadResponse

logger = logging.getLogger(__name__)


def process_document(
    file_content: bytes,
    filename: str,
    file_type: str,
    document_id: str,
) -> DocumentUploadResponse:
    text = parse_document(file_content, file_type)
    chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)

    embedder = Embedder()
    chunk_texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(chunk_texts)

    retriever = Retriever()
    retriever.load()
    retriever.add_documents(
        embeddings=embeddings,
        document_id=document_id,
        chunks=chunks,
        source_filename=filename,
    )
    retriever.save()

    safe_filename = f"{document_id}{file_type}"
    save_document(
        document_id=document_id,
        filename=safe_filename,
        original_filename=filename,
        file_type=file_type,
        uploaded_at=datetime.now(timezone.utc).isoformat(),
        chunk_count=len(chunks),
        status="processed",
    )

    return DocumentUploadResponse(
        document_id=document_id,
        filename=filename,
        chunk_count=len(chunks),
        status="processed",
    )
