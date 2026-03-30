from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService

router = APIRouter(prefix="/query", tags=["query"])
query_service = QueryService()


@router.post("", response_model=QueryResponse)
def query_documents(payload: QueryRequest) -> QueryResponse:
    result = query_service.ask(payload.question, payload.top_k)
    return QueryResponse(**result)
