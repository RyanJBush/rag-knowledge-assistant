import io

import PyPDF2


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


def test_upload_invalid_pdf(client):
    content = b"not a real pdf"
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("bad.pdf", io.BytesIO(content), "application/pdf")},
    )
    assert response.status_code == 400


def test_upload_encrypted_pdf(client):
    output = io.BytesIO()
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.encrypt("secret")
    writer.write(output)
    output.seek(0)

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("encrypted.pdf", output, "application/pdf")},
def test_upload_pdf(client):
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    pdf_bytes = buf.getvalue()

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("sample.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert "document_id" in data


def test_upload_response_fields(client):
    content = b"Document with predictable structure."
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("fields_test.txt", io.BytesIO(content), "text/plain")},
    )
    data = response.json()
    assert "document_id" in data
    assert "filename" in data
    assert "chunk_count" in data
    assert "status" in data
    assert isinstance(data["chunk_count"], int)


def test_list_documents_response_fields(client):
    # Ensure at least one document is in the list before checking fields.
    content = b"Some text for field validation."
    client.post(
        "/api/v1/documents/upload",
        files={"file": ("list_fields.txt", io.BytesIO(content), "text/plain")},
    )
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) >= 1
    doc = docs[0]
    for field in ("id", "filename", "original_filename", "file_type", "uploaded_at",
                  "chunk_count", "status"):
        assert field in doc, f"Missing field: {field}"


def test_upload_no_extension_rejected(client):
    content = b"no extension file"
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("noextension", io.BytesIO(content), "application/octet-stream")},
    )
    assert response.status_code == 400
