"""Read a PDF page by page with pypdf. Returns a list of {"page": n, "text": ...}.
Scanned PDFs (images) return little or no text: run OCR first."""
from pypdf import PdfReader


def load_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").replace(" ", " ")
        pages.append({"page": i, "text": text})
    return pages
