import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.db.metadata import list_documents
from app.schemas.document import DocumentInfo, DocumentUploadResponse
from app.services.document_service import process_document

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_TYPES = {".pdf", ".txt"}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or ""
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if suffix not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {suffix} not supported. Use .pdf or .txt",
        )

    content = await file.read()
    document_id = str(uuid.uuid4())
    result = process_document(content, filename, suffix, document_id)
    return result


@router.get("", response_model=list[DocumentInfo])
async def get_documents():
    return list_documents()
