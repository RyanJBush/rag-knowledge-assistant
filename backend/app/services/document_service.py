from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
import uuid

from fastapi import UploadFile

from app.core.config import get_settings
from app.core.exceptions import AppError

ALLOWED_TYPES = {"application/pdf", "text/plain"}


class DocumentService:
    def __init__(self) -> None:
        settings = get_settings()
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.max_upload_bytes = settings.max_upload_mb * 1024 * 1024
        self.metadata_file = self.upload_dir / "documents.json"
        if not self.metadata_file.exists():
            self.metadata_file.write_text("[]", encoding="utf-8")

    def _load_metadata(self) -> list[dict]:
        return json.loads(self.metadata_file.read_text(encoding="utf-8"))

    def _save_metadata(self, items: list[dict]) -> None:
        self.metadata_file.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    async def save_upload(self, file: UploadFile) -> dict:
        if file.content_type not in ALLOWED_TYPES:
            raise AppError("unsupported_file_type", "Only PDF and TXT uploads are supported.", 400)

        if not file.filename:
            raise AppError("invalid_filename", "Filename is required.", 400)

        document_id = str(uuid.uuid4())
        suffix = Path(file.filename).suffix.lower()
        destination = self.upload_dir / f"{document_id}{suffix}"

        data = await file.read()
        if len(data) > self.max_upload_bytes:
            raise AppError("file_too_large", f"File exceeds {self.max_upload_bytes} bytes limit.", 400)

        destination.write_bytes(data)

        record = {
            "document_id": document_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "path": str(destination),
            "created_at": datetime.now(UTC).isoformat(),
            "chunks_indexed": 0,
        }
        items = self._load_metadata()
        items.append(record)
        self._save_metadata(items)
        return record

    def list_documents(self) -> list[dict]:
        return self._load_metadata()

    def update_chunks_indexed(self, document_id: str, chunks_indexed: int) -> None:
        docs = self._load_metadata()
        for item in docs:
            if item["document_id"] == document_id:
                item["chunks_indexed"] = chunks_indexed
                break
        self._save_metadata(docs)
