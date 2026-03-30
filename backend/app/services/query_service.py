from app.core.exceptions import AppError
from app.rag.embedder import embed_texts
from app.rag.generator import generate_answer
from app.rag.vector_store import LocalVectorStore


class QueryService:
    def __init__(self) -> None:
        self.vector_store = LocalVectorStore()

    def ask(self, question: str, top_k: int) -> dict:
        query_embedding = embed_texts([question])[0]
        matches = self.vector_store.query(query_embedding, top_k=top_k)

        if not matches:
            raise AppError(
                "no_documents_indexed",
                "No indexed chunks found. Upload and index documents first.",
                404,
            )

        contexts = [match["text"] for match in matches]
        answer = generate_answer(question, contexts)

        citations = [
            {
                "document_id": match["metadata"]["document_id"],
                "source": match["metadata"]["source"],
                "chunk_id": match["metadata"]["chunk_id"],
                "snippet": match["metadata"]["snippet"],
                "score": round(float(match["score"]), 4),
                "page": match["metadata"].get("page"),
            }
            for match in matches
        ]

        return {
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": len(matches),
        }
