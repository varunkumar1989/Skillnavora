"""Three ways to split a document into chunks, each chunk carrying metadata for citations."""
import re
from dataclasses import dataclass, field


@dataclass
class Chunk:
    id: str
    text: str
    meta: dict = field(default_factory=dict)


def fixed_size(text: str, size_words: int = 60, overlap: int = 15, meta: dict | None = None) -> list[Chunk]:
    """Cut every `size_words` words, repeating `overlap` words between neighbours."""
    if overlap >= size_words:
        raise ValueError("overlap must be smaller than size_words")
    words = text.split()
    step = size_words - overlap
    chunks = []
    for i, start in enumerate(range(0, max(1, len(words) - overlap), step)):
        piece = words[start:start + size_words]
        if piece:
            chunks.append(Chunk(f"fixed-{i}", " ".join(piece), {**(meta or {}), "start_word": start}))
    return chunks


def recursive(text: str, max_words: int = 80, meta: dict | None = None) -> list[Chunk]:
    """Split by paragraphs first; only split a paragraph into sentences when it is too long.
    Keeps related sentences together, which usually retrieves better than fixed cuts."""
    chunks, buf = [], []

    def flush():
        if buf:
            chunks.append(Chunk(f"rec-{len(chunks)}", " ".join(buf), dict(meta or {})))
            buf.clear()

    for para in [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]:
        sentences = re.split(r"(?<=[.!?])\s+", para) if len(para.split()) > max_words else [para]
        for s in sentences:
            if len(" ".join(buf + [s]).split()) > max_words:
                flush()
            buf.append(s)
        flush()
    return chunks


def by_heading(text: str, meta: dict | None = None) -> list[Chunk]:
    """Split on headings (lines that are short and have no full stop). The heading becomes
    metadata, so answers can cite 'section: Leave'."""
    chunks, heading, body = [], "Introduction", []
    for line in text.splitlines():
        s = line.strip()
        if s and len(s.split()) <= 6 and not s.endswith((".", ":", ";")) and s[0].isupper():
            if body:
                chunks.append(Chunk(f"sec-{len(chunks)}", " ".join(body), {**(meta or {}), "section": heading}))
            heading, body = s, []
        elif s:
            body.append(s)
    if body:
        chunks.append(Chunk(f"sec-{len(chunks)}", " ".join(body), {**(meta or {}), "section": heading}))
    return chunks
