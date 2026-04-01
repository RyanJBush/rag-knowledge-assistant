from pydantic import BaseModel


class Citation(BaseModel):
    document_id: str
    source_filename: str
    chunk_index: int
    snippet: str
    score: float


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    query: str
