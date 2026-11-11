"""Retrieval-augmented generation (RAG) with no extra services.

STATUS: chunking and retrieval are tested offline by test_offline.py. The final answer call
uses grok_client.chat and is untested against the live API.

Retrieval here is keyword scoring (BM25-style) so the example runs anywhere. In production you
would usually use embeddings and a vector database (Module 8, chapter 8.4). Whether xAI offers an
embeddings endpoint was not verified; many teams use a separate embeddings provider.
"""
import math
import re
from collections import Counter

from grok_client import chat

WORD = re.compile(r"[a-z0-9]+")
STOP = set("a an the and or of to in on for is are was were be by with as at it this that from your you we our".split())


def tokenize(text):
    return [w for w in WORD.findall(text.lower()) if w not in STOP]


def chunk(text, source, max_words=120, overlap=20):
    """Split text into overlapping chunks of about max_words words, keeping the source name."""
    words = text.split()
    chunks, start, n = [], 0, 1
    while start < len(words):
        piece = " ".join(words[start:start + max_words])
        chunks.append({"id": f"{source}#{n}", "source": source, "text": piece})
        if start + max_words >= len(words):
            break
        start += max_words - overlap
        n += 1
    return chunks


class Index:
    """A tiny BM25 index over chunks."""

    def __init__(self, chunks, k1=1.5, b=0.75):
        self.chunks = chunks
        self.docs = [Counter(tokenize(c["text"])) for c in chunks]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(w for d in self.docs for w in d)
        n = len(self.docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}
        self.k1, self.b = k1, b

    def search(self, query, k=3):
        q = tokenize(query)
        scores = []
        for i, d in enumerate(self.docs):
            s = 0.0
            for w in q:
                if w in d:
                    tf = d[w]
                    s += self.idf[w] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            scores.append((s, i))
        scores.sort(reverse=True)
        return [self.chunks[i] | {"score": round(s, 3)} for s, i in scores[:k] if s > 0]


def build_prompt(question, hits):
    context = "\n\n".join(f"[{h['id']}] {h['text']}" for h in hits)
    return [
        {"role": "system", "content": "Answer only from the context. Cite chunk ids in square brackets. "
                                      "If the answer is not in the context, reply exactly: I could not find this in the documents."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]


def answer(index, question, k=3):
    hits = index.search(question, k=k)
    if not hits:
        return "I could not find this in the documents.", [], {}
    text, usage = chat(build_prompt(question, hits), max_tokens=300)
    return text, hits, usage


if __name__ == "__main__":
    policy = ("Returns are accepted within 30 days of delivery if the item is unused. "
              "Refunds are paid to the original payment method within 5 to 7 working days. "
              "Sale items can be exchanged but not refunded. Delivery takes 3 to 5 days in metro cities.")
    idx = Index(chunk(policy, "returns-policy"))
    print(answer(idx, "Can I get a refund on a sale item?"))
