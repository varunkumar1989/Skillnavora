"""A minimal in-memory vector store with metadata filters, save and load.
Good for learning and small apps; use Chroma, pgvector or Qdrant for real volumes."""
import json

from .chunking import Chunk
from .embeddings import cosine, embed


class VectorStore:
    def __init__(self):
        self.items: list[dict] = []

    def add(self, chunks: list[Chunk]) -> int:
        for c in chunks:
            self.items.append({"id": c.id, "text": c.text, "meta": c.meta, "vec": embed(c.text)})
        return len(chunks)

    def search(self, query: str, k: int = 3, where: dict | None = None) -> list[dict]:
        q = embed(query)
        pool = [it for it in self.items if not where or all(it["meta"].get(key) == val for key, val in where.items())]
        scored = sorted(({**it, "score": cosine(q, it["vec"])} for it in pool), key=lambda x: x["score"], reverse=True)
        return [{k2: v for k2, v in s.items() if k2 != "vec"} for s in scored[:k]]

    def save(self, path: str):
        json.dump(self.items, open(path, "w", encoding="utf-8"))

    @classmethod
    def load(cls, path: str) -> "VectorStore":
        store = cls()
        store.items = json.load(open(path, encoding="utf-8"))
        return store
