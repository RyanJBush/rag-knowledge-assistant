from app.rag.chunker import chunk_text
from app.rag.generator import generate_answer


def test_chunk_text_returns_chunks() -> None:
    text = "A" * 2000
    chunks = chunk_text(text=text, chunk_size=500, overlap=100)
    assert len(chunks) >= 4
    assert chunks[0]["chunk_id"] == "chunk-0"


def test_generator_returns_answer_with_context() -> None:
    answer = generate_answer("What is the policy?", ["Policy requires MFA for all users."])
    assert "What is the policy?" in answer
    assert "MFA" in answer
