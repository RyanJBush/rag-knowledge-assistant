from pathlib import Path

from app.core.exceptions import AppError


SEPARATOR = "\n\n"


def extract_text(file_path: Path, content_type: str) -> tuple[str, list[dict]]:
    if content_type == "text/plain":
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        return text, [{"page": None, "start": 0, "end": len(text)}]

    if content_type == "application/pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise AppError(
                code="pdf_dependency_missing",
                message="PDF support requires the pypdf package.",
                status_code=500,
            ) from exc

        reader = PdfReader(str(file_path))
        pages: list[str] = []
        page_map: list[dict] = []
        cursor = 0
        for i, page in enumerate(reader.pages, start=1):
            page_text = (page.extract_text() or "").strip()
            if not page_text:
                continue

            start = cursor
            end = start + len(page_text)
            pages.append(page_text)
            page_map.append({"page": i, "start": start, "end": end})
            cursor = end + len(SEPARATOR)

        return SEPARATOR.join(pages), page_map

    raise AppError(code="unsupported_file_type", message=f"Unsupported file type: {content_type}")
