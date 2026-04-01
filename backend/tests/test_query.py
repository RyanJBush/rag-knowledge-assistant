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
