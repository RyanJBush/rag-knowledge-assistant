from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    status: str


class DocumentInfo(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_type: str
    uploaded_at: str
    chunk_count: int
    status: str
