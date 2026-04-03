import pytest

from app.rag.chunker import chunk_text


def test_chunk_basic():
    text = " ".join(["word"] * 1000)
    chunks = chunk_text(text, chunk_size=100, chunk_overlap=10)
    assert len(chunks) > 0
    assert all("text" in c and "chunk_index" in c for c in chunks)


def test_chunk_small_text():
    text = "Hello world"
    chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 1
    assert chunks[0]["chunk_index"] == 0


def test_chunk_overlap():
    words = list(range(200))
    text = " ".join(str(w) for w in words)
    chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
    assert len(chunks) >= 2


def test_chunk_empty():
    chunks = chunk_text("", chunk_size=100, chunk_overlap=10)
    assert chunks == []


@pytest.mark.parametrize(
    ("chunk_size", "chunk_overlap"),
    [
        (100, 100),
        (100, 150),
        (100, -1),
        (0, 0),
    ],
)
def test_chunk_invalid_configuration(chunk_size, chunk_overlap):
    with pytest.raises(ValueError):
        chunk_text("some text to chunk", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
