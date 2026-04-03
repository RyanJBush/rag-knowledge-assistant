import io

import PyPDF2
from fastapi import HTTPException

PDF_READ_EXCEPTIONS = (
    PyPDF2.errors.EmptyFileError,
    PyPDF2.errors.PdfReadError,
    PyPDF2.errors.PdfStreamError,
)


def parse_document(content: bytes, file_type: str) -> str:
    if file_type == ".pdf":
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(content))
        except PDF_READ_EXCEPTIONS as exc:
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file. Please upload a readable, non-corrupted PDF.",
            ) from exc

        if reader.is_encrypted:
            try:
                decrypt_result = reader.decrypt("")
            except PyPDF2.errors.PdfReadError as exc:
                raise HTTPException(
                    status_code=400,
                    detail="Encrypted PDF files are not supported.",
                ) from exc
            if decrypt_result == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Encrypted PDF files are not supported.",
                )

        texts = []
        try:
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
        except (PyPDF2.errors.PdfReadError, KeyError, TypeError) as exc:
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from PDF. Please upload a valid PDF.",
            ) from exc
        return "\n".join(texts)
    elif file_type == ".txt":
        return content.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
