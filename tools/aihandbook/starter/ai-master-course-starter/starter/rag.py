"""The PDF chatbot pipeline: index a PDF, retrieve chunks, answer with citations, refuse
when the documents do not cover the question."""
from .chunking import recursive
from .config import settings
from .costs import Timer, request_cost
from .guardrails import check_injection, grounded, redact_pii
from .llm import chat
from .ops import get_prompt, log_request
from .pdf_loader import load_pdf
from .store import VectorStore

PROMPT_VERSION = "rag-answer@v2"
DONT_KNOW = "I don't know. The documents I was given do not answer this question."


def index_pdf(path: str, store: VectorStore | None = None, max_words: int = 80) -> VectorStore:
    store = store or VectorStore()
    name = path.replace("\\", "/").split("/")[-1]
    for page in load_pdf(path):
        chunks = recursive(page["text"], max_words=max_words, meta={"file": name, "page": page["page"]})
        for c in chunks:
            c.id = f"{name}-p{page['page']}-{c.id}"
        store.add(chunks)
    return store


def build_prompt(question: str, hits: list[dict]) -> str:
    sources = "\n".join(f"[S{i + 1}] {h['text']}" for i, h in enumerate(hits))
    return f"SOURCES:\n{sources}\n\nQUESTION: {question}"


def answer(store: VectorStore, question: str, k: int = 3, log: bool = True) -> dict:
    timer = Timer()
    ok, why = check_injection(question)
    if not ok:
        return {"answer": "I can't help with that request.", "sources": [], "blocked": why}
    with timer.part("retrieve"):
        hits = store.search(question, k=k)
    if not hits or hits[0]["score"] < settings.min_retrieval_score:
        result = {"answer": DONT_KNOW, "sources": [], "refused": True, "top_score": round(hits[0]["score"], 3) if hits else 0}
    else:
        with timer.part("generate"):
            reply = chat(get_prompt(PROMPT_VERSION), build_prompt(question, hits))
        text, _ = redact_pii(reply.text)
        is_grounded, share = grounded(text, [h["text"] for h in hits])
        result = {
            "answer": text,
            "sources": [{"tag": f"S{i + 1}", "file": h["meta"].get("file"), "page": h["meta"].get("page"), "score": round(h["score"], 3)} for i, h in enumerate(hits)],
            "grounded": is_grounded, "grounded_share": share,
            "tokens": {"input": reply.input_tokens, "output": reply.output_tokens},
            "cost_usd": round(request_cost(reply.input_tokens, reply.output_tokens), 6),
            "model": reply.model, "refused": text.startswith("I don't know"),
        }
    result["timings_ms"] = {k: round(v * 1000, 2) for k, v in timer.parts.items()}
    if log:
        log_request(settings.log_path, question=question, prompt_version=PROMPT_VERSION, answer=result["answer"],
                    sources=[s["tag"] + ":" + str(s["page"]) for s in result.get("sources", [])],
                    refused=result.get("refused", False), timings_ms=result["timings_ms"], tokens=result.get("tokens"))
    return result
