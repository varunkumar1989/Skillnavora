"""Lesson 1: compare chunking strategies on the sample PDF by retrieval recall at 3.
Run: python examples/l1_chunking.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starter.chunking import by_heading, fixed_size, recursive
from starter.pdf_loader import load_pdf
from starter.store import VectorStore

PDF = os.path.join(os.path.dirname(__file__), "..", "data", "sample_policy.pdf")
GOLDEN = [  # question, a phrase that must be inside a retrieved chunk
    ("How many days of paid leave do I get each year?", "20 days of paid leave"),
    ("How much unused leave can I carry forward?", "carried forward up to 5 days"),
    ("When must expense claims be submitted?", "within 30 days"),
    ("What is the daily meal limit when travelling?", "1,500 rupees per day"),
    ("How many days a week can I work remotely?", "up to 3 days a week"),
    ("How long must a laptop password be?", "at least 14 characters"),
    ("What is the yearly learning budget?", "40,000 rupees"),
    ("When do I need a doctor's note for sick leave?", "longer than 2 days"),
]

text = "\n\n".join(p["text"] for p in load_pdf(PDF))
strategies = {
    "fixed 40 words, overlap 0": fixed_size(text, 40, 0),
    "fixed 40 words, overlap 10": fixed_size(text, 40, 10),
    "recursive, max 60 words": recursive(text, 60),
    "by heading": by_heading(text),
}

for name, chunks in strategies.items():
    store = VectorStore(); store.add(chunks)
    found = sum(any(phrase in hit["text"].replace("\n", " ") for hit in store.search(q, k=3)) for q, phrase in GOLDEN)
    avg = sum(len(c.text.split()) for c in chunks) / len(chunks)
    print(f"{name:<28} chunks={len(chunks):>3}  avg words={avg:5.1f}  recall@3={found}/{len(GOLDEN)}")

print("\nExample chunk with metadata (by heading):")
c = strategies["by heading"][2]
print(c.meta, "|", c.text[:90] + "...")
