import io


def test_upload_txt(client):
    content = b"This is a test document with enough content to create at least one chunk."
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.txt", io.BytesIO(content), "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert data["chunk_count"] >= 1
    assert "document_id" in data


def test_list_documents(client):
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_upload_invalid_type(client):
    content = b"some content"
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.csv", io.BytesIO(content), "text/csv")},
    )
    assert response.status_code == 400
