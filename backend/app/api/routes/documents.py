from fastapi import APIRouter, File, UploadFile

from app.schemas.document import DocumentIngestResponse, DocumentItem, DocumentListResponse
from app.services.document_service import DocumentService
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/documents", tags=["documents"])

document_service = DocumentService()
ingestion_service = IngestionService()


@router.post("/upload", response_model=DocumentIngestResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentIngestResponse:
    record = await document_service.save_upload(file)
    chunks_indexed = ingestion_service.ingest_document(record)
    document_service.update_chunks_indexed(record["document_id"], chunks_indexed)

    return DocumentIngestResponse(
        document_id=record["document_id"],
        filename=record["filename"],
        chunks_indexed=chunks_indexed,
    )


@router.get("", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    docs = [DocumentItem(**doc) for doc in document_service.list_documents()]
    return DocumentListResponse(documents=docs)
