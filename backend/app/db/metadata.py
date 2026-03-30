import sqlite3
from typing import Any

from app.core.config import settings


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(settings.db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                uploaded_at TEXT NOT NULL,
                chunk_count INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_document(
    document_id: str,
    filename: str,
    original_filename: str,
    file_type: str,
    uploaded_at: str,
    chunk_count: int,
    status: str,
) -> None:
    with _get_conn() as conn:
        conn.execute(
            """INSERT INTO documents
               (id, filename, original_filename, file_type, uploaded_at, chunk_count, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                document_id,
                filename,
                original_filename,
                file_type,
                uploaded_at,
                chunk_count,
                status,
            ),
        )
        conn.commit()


def get_document(document_id: str) -> dict[str, Any] | None:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM documents WHERE id = ?", (document_id,)
        ).fetchone()
        return dict(row) if row else None


def list_documents() -> list[dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM documents ORDER BY uploaded_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def delete_document(document_id: str) -> None:
    with _get_conn() as conn:
        conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        conn.commit()
