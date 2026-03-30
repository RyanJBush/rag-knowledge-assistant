from pydantic import BaseModel, Field


class DocumentIngestResponse(BaseModel):
    document_id: str
    filename: str
    chunks_indexed: int
    status: str = "indexed"


class DocumentItem(BaseModel):
    document_id: str
    filename: str
    content_type: str
    created_at: str
    chunks_indexed: int = Field(ge=0)


class DocumentListResponse(BaseModel):
    documents: list[DocumentItem]
