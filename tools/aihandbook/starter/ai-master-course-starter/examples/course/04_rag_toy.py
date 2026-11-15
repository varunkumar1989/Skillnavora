# Week 2, Subjects 5-8: chunking, toy embeddings, cosine similarity, top-k retrieval.
# Real systems use an embedding model (a neural network). This toy version counts words,
# so you can see the maths without any API key.
import math, re
from collections import Counter

DOCUMENT = """Employees get 20 days of paid leave per year. Unused leave can be carried forward up to 5 days.
Expense claims must be submitted within 30 days with receipts. Travel is booked through the approved portal.
Remote work is allowed up to 3 days a week with manager approval. Laptops must use disk encryption."""

def chunk(text, size_words=12, overlap=3):
    words = text.split()
    step = size_words - overlap
    return [" ".join(words[i:i + size_words]) for i in range(0, len(words), step)]

def embed(text):
    words = re.findall(r"[a-z]+", text.lower())
    return Counter(words)

def cosine(a, b):
    dot = sum(a[w] * b[w] for w in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0

def retrieve(question, chunks, k=2):
    q = embed(question)
    scored = [(cosine(q, embed(c)), i, c) for i, c in enumerate(chunks)]
    return sorted(scored, reverse=True)[:k]

chunks = chunk(DOCUMENT)
print("Number of chunks:", len(chunks))
for score, i, text in retrieve("How many days of paid leave do I get?", chunks):
    print(f"score={score:.2f} chunk={i}: {text[:60]}...")
