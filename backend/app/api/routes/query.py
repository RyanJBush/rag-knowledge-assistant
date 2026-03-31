from fastapi import APIRouter

from app.rag.embedder import Embedder
from app.rag.generator import get_llm_provider
from app.rag.retriever import Retriever
from app.schemas.query import Citation, QueryRequest, QueryResponse

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query(request: QueryRequest):
    embedder = Embedder()
    retriever = Retriever()
    retriever.load()

    query_embedding = embedder.encode([request.question])
    results = retriever.search(query_embedding, top_k=request.top_k)

    provider = get_llm_provider()
    answer = provider.generate(request.question, results)

    citations = [
        Citation(
            document_id=r["document_id"],
            source_filename=r["source_filename"],
            chunk_index=r["chunk_index"],
            snippet=r["chunk_text"][:200],
            score=float(r["score"]),
        )
        for r in results
    ]

    return QueryResponse(answer=answer, citations=citations, query=request.question)
