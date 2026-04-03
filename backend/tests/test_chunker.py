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
def test_chunk_whitespace_only():
    chunks = chunk_text("   \n\t  ", chunk_size=100, chunk_overlap=10)
    assert chunks == []


def test_chunk_single_word():
    chunks = chunk_text("hello", chunk_size=100, chunk_overlap=10)
    assert len(chunks) == 1
    assert chunks[0]["text"] == "hello"
    assert chunks[0]["chunk_index"] == 0


def test_chunk_exact_boundary():
    # 10 words with chunk_size=10 should produce exactly one chunk.
    text = " ".join(["word"] * 10)
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
    assert len(chunks) == 1


def test_chunk_indices_are_sequential():
    text = " ".join(["w"] * 300)
    chunks = chunk_text(text, chunk_size=100, chunk_overlap=10)
    for expected_idx, chunk in enumerate(chunks):
        assert chunk["chunk_index"] == expected_idx


def test_chunk_overlap_content():
    # With overlap, the tail of one chunk should appear at the head of the next.
    words = [str(i) for i in range(20)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=5)
    assert len(chunks) >= 2
    # Last 5 words of chunk 0 should be the first 5 words of chunk 1.
    tail = chunks[0]["text"].split()[-5:]
    head = chunks[1]["text"].split()[:5]
    assert tail == head


def test_chunk_text_field_is_string():
    text = " ".join(["word"] * 50)
    chunks = chunk_text(text, chunk_size=20, chunk_overlap=5)
    assert all(isinstance(c["text"], str) for c in chunks)
