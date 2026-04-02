from unittest.mock import patch

import pytest

from app.db.metadata import (
    delete_document,
    get_document,
    init_db,
    list_documents,
    save_document,
)


@pytest.fixture()
def tmp_db(tmp_path):
    """Point the metadata module at a fresh temp SQLite database."""
    db_file = tmp_path / "test_metadata.db"
    with patch("app.db.metadata.settings") as mock_settings:
        mock_settings.db_path = db_file
        init_db()
        yield mock_settings


def _save(tmp_db, doc_id="doc-1", filename="file.txt", original="original.txt",
          file_type=".txt", uploaded_at="2024-01-01T00:00:00+00:00",
          chunk_count=3, status="processed"):
    save_document(
        document_id=doc_id,
        filename=filename,
        original_filename=original,
        file_type=file_type,
        uploaded_at=uploaded_at,
        chunk_count=chunk_count,
        status=status,
    )


def test_init_db_creates_table(tmp_db):
    # If table creation failed, save_document would raise; this just confirms
    # init_db runs without error and the table is queryable.
    docs = list_documents()
    assert isinstance(docs, list)


def test_save_and_get_document(tmp_db):
    _save(tmp_db, doc_id="abc-123")
    doc = get_document("abc-123")
    assert doc is not None
    assert doc["id"] == "abc-123"
    assert doc["filename"] == "file.txt"
    assert doc["original_filename"] == "original.txt"
    assert doc["file_type"] == ".txt"
    assert doc["chunk_count"] == 3
    assert doc["status"] == "processed"


def test_get_document_missing_returns_none(tmp_db):
    result = get_document("nonexistent-id")
    assert result is None


def test_list_documents_returns_all(tmp_db):
    _save(tmp_db, doc_id="doc-1", uploaded_at="2024-01-01T00:00:00+00:00")
    _save(tmp_db, doc_id="doc-2", uploaded_at="2024-01-02T00:00:00+00:00")
    docs = list_documents()
    assert len(docs) == 2


def test_list_documents_ordered_newest_first(tmp_db):
    _save(tmp_db, doc_id="older", uploaded_at="2024-01-01T00:00:00+00:00")
    _save(tmp_db, doc_id="newer", uploaded_at="2024-06-01T00:00:00+00:00")
    docs = list_documents()
    assert docs[0]["id"] == "newer"
    assert docs[1]["id"] == "older"


def test_list_documents_empty_db(tmp_db):
    docs = list_documents()
    assert docs == []


def test_delete_document(tmp_db):
    _save(tmp_db, doc_id="to-delete")
    delete_document("to-delete")
    assert get_document("to-delete") is None


def test_delete_nonexistent_document_is_noop(tmp_db):
    # Deleting something that does not exist should not raise.
    delete_document("does-not-exist")


def test_save_document_all_fields_stored(tmp_db):
    save_document(
        document_id="full-test",
        filename="safe_full-test.pdf",
        original_filename="my doc.pdf",
        file_type=".pdf",
        uploaded_at="2025-03-15T12:30:00+00:00",
        chunk_count=42,
        status="processed",
    )
    doc = get_document("full-test")
    assert doc["filename"] == "safe_full-test.pdf"
    assert doc["original_filename"] == "my doc.pdf"
    assert doc["file_type"] == ".pdf"
    assert doc["uploaded_at"] == "2025-03-15T12:30:00+00:00"
    assert doc["chunk_count"] == 42
