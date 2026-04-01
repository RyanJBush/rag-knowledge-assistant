import io

import PyPDF2


def parse_document(content: bytes, file_type: str) -> str:
    if file_type == ".pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        texts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                texts.append(text)
        return "\n".join(texts)
    elif file_type == ".txt":
        return content.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
