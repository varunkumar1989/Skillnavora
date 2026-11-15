"""FastAPI service for the PDF chatbot.
Run locally:  uvicorn api.main:app --reload      then open http://127.0.0.1:8000/docs
Endpoints:    GET /health   POST /ask {"question": "..."}   POST /upload (a PDF file)"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from starter import __version__
from starter.config import settings
from starter.rag import answer, index_pdf

SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_policy.pdf")
app = FastAPI(title="AI Master Course PDF chatbot", version=__version__)
state = {"store": index_pdf(SAMPLE), "document": "sample_policy.pdf"}


class Ask(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    k: int = Field(default=3, ge=1, le=8)


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__, "mode": "offline" if settings.offline else "claude",
            "model": "offline-stand-in" if settings.offline else settings.model,
            "document": state["document"], "chunks": len(state["store"].items)}


@app.post("/ask")
def ask(body: Ask):
    try:
        return answer(state["store"], body.question, k=body.k)
    except RuntimeError as e:  # API problems are turned into readable messages in starter/llm.py
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    data = await file.read()
    if len(data) > 20 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="The PDF is larger than 20 MB.")
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, os.path.basename(file.filename))
        with open(path, "wb") as f:
            f.write(data)
        try:
            store = index_pdf(path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not read the PDF: {e}")
    if not store.items:
        raise HTTPException(status_code=400, detail="No text found. Scanned PDFs need OCR first.")
    state.update(store=store, document=file.filename)
    return {"document": file.filename, "chunks": len(store.items)}
