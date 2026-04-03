from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=4, ge=1, le=10)


class Citation(BaseModel):
    document_id: str
    source: str
    chunk_id: str
    snippet: str
    score: float
    page: int | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: int
