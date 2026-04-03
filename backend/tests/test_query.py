import io


def test_query(client):
    # Upload a document first to ensure there are indexed chunks
    content = (
        b"Python is a programming language. "
        b"It is widely used for data science and web development. "
        b"FastAPI is a modern web framework for building APIs with Python."
    )
    client.post(
        "/api/v1/documents/upload",
        files={"file": ("query_test.txt", io.BytesIO(content), "text/plain")},
    )

    response = client.post(
        "/api/v1/query",
        json={"question": "What is Python?", "top_k": 3},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert "query" in data
    assert data["query"] == "What is Python?"


def test_query_empty_index(client):
    # Query should work even when there may or may not be results
    response = client.post(
        "/api/v1/query",
        json={"question": "nonexistent topic xyz123", "top_k": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data


def test_query_custom_top_k(client):
    content = b" ".join([b"word"] * 200)
    client.post(
        "/api/v1/documents/upload",
        files={"file": ("topk_test.txt", io.BytesIO(content), "text/plain")},
    )
    response = client.post(
        "/api/v1/query",
        json={"question": "word", "top_k": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["citations"]) <= 2


def test_query_citation_fields(client):
    content = b"Machine learning is a subset of artificial intelligence."
    client.post(
        "/api/v1/documents/upload",
        files={"file": ("citation_test.txt", io.BytesIO(content), "text/plain")},
    )
    response = client.post(
        "/api/v1/query",
        json={"question": "What is machine learning?", "top_k": 1},
    )
    assert response.status_code == 200
    data = response.json()
    if data["citations"]:
        citation = data["citations"][0]
        for field in ("document_id", "source_filename", "chunk_index", "snippet", "score"):
            assert field in citation, f"Missing citation field: {field}"
        assert isinstance(citation["chunk_index"], int)
        assert isinstance(citation["score"], float)
        assert isinstance(citation["snippet"], str)


def test_query_missing_question_returns_422(client):
    response = client.post("/api/v1/query", json={})
    assert response.status_code == 422


def test_query_answer_is_string(client):
    response = client.post(
        "/api/v1/query",
        json={"question": "test question"},
    )
    assert response.status_code == 200
    assert isinstance(response.json()["answer"], str)


def test_query_citations_is_list(client):
    response = client.post(
        "/api/v1/query",
        json={"question": "test"},
    )
    assert response.status_code == 200
    assert isinstance(response.json()["citations"], list)
