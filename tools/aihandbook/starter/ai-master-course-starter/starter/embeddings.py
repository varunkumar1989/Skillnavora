"""Text -> vector. The default is a small, free, offline embedding (hashed word and word-pair
counts) so the course runs without any account. It understands shared words, not meaning:
swap in a real embedding model for production (see the lesson on embeddings)."""
import hashlib
import math
import re

DIM = 512
STOP = set("the a an and or of to in on for is are was be with by at as it this that from your you we our".split())


def _tokens(text: str) -> list[str]:
    words = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]
    words = [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in words]
    return words + [a + "_" + b for a, b in zip(words, words[1:])]


def embed(text: str) -> list[float]:
    vec = [0.0] * DIM
    for tok in _tokens(text):
        h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
        vec[h % DIM] += 1.0 if (h >> 8) % 2 == 0 else -1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))
