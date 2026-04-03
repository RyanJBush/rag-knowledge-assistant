import io

import PyPDF2
import pytest

from app.rag.parser import parse_document


def _make_pdf(text: str) -> bytes:
    """Create a minimal in-memory PDF containing *text* on one page."""
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    # PyPDF2's add_blank_page does not embed text; use an existing text-bearing
    # page approach via a minimal raw PDF instead.
    # Build the smallest valid PDF that contains a text stream.
    stream = text.encode("latin-1", errors="replace")
    raw = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]"
        b" /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        + b"4 0 obj\n<< /Length "
        + str(len(b"BT /F1 12 Tf 72 720 Td (" + stream + b") Tj ET")).encode()
        + b" >>\nstream\n"
        b"BT /F1 12 Tf 72 720 Td (" + stream + b") Tj ET\n"
        b"endstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000266 00000 n \n"
        b"0000000400 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n460\n%%EOF\n"
    )
    return raw


def test_parse_txt_basic():
    content = b"Hello world"
    result = parse_document(content, ".txt")
    assert result == "Hello world"


def test_parse_txt_empty():
    result = parse_document(b"", ".txt")
    assert result == ""


def test_parse_txt_utf8_with_replacement():
    # Byte that is invalid UTF-8 (0xff) should be replaced rather than raising.
    content = b"Hello \xff world"
    result = parse_document(content, ".txt")
    assert "Hello" in result
    assert "world" in result


def test_parse_txt_multiline():
    content = b"Line one\nLine two\nLine three"
    result = parse_document(content, ".txt")
    assert "Line one" in result
    assert "Line three" in result


def test_parse_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported file type"):
        parse_document(b"data", ".csv")


def test_parse_unsupported_type_docx():
    with pytest.raises(ValueError, match="Unsupported file type"):
        parse_document(b"data", ".docx")


def test_parse_pdf_returns_string():
    # Use a minimal PDF created by PyPDF2's writer (no text pages).
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    pdf_bytes = buf.getvalue()

    result = parse_document(pdf_bytes, ".pdf")
    # Blank pages produce no text; result should be an empty string, not an error.
    assert isinstance(result, str)


def test_parse_pdf_empty_pages_returns_empty_string():
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    result = parse_document(buf.getvalue(), ".pdf")
    assert result == ""
