"""Simple, explainable guardrails. Each check returns (ok, reason).
These are teaching versions: pattern checks catch obvious cases, not every attack."""
import re

INJECTION_PATTERNS = [
    r"(ignore|forget|disregard) (all |any |the |your |of )*(previous |prior |above |earlier )?(instructions|rules|guidelines)",
    r"disregard (the|your) (system|previous) (prompt|instructions)",
    r"(reveal|print|show|repeat|output) (me )?(the|your) (system prompt|hidden instructions|instructions|api key)",
    r"you are now (in )?(developer|dan|jailbreak) mode",
    r"act as .* without (any )?restrictions",
]
PII_PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "phone": r"(?<!\d)(?:\+?\d{1,3}[\s-]?)?\d{10}(?!\d)",
    "card": r"(?<!\d)(?:\d[ -]?){13,16}(?!\d)",
}


def check_injection(text: str) -> tuple[bool, str]:
    for p in INJECTION_PATTERNS:
        if re.search(p, text, re.I):
            return False, f"possible prompt injection: matches '{p}'"
    return True, "no injection pattern found"


def redact_pii(text: str) -> tuple[str, list[str]]:
    found = []
    for name, p in PII_PATTERNS.items():
        if re.search(p, text):
            found.append(name)
            text = re.sub(p, f"[{name.upper()} REMOVED]", text)
    return text, found


def grounded(answer: str, sources: list[str], min_overlap: float = 0.5) -> tuple[bool, float]:
    """Share of the answer's content words that appear in the sources. A low share suggests
    the answer contains claims the sources do not support (a possible hallucination)."""
    words = [w for w in re.findall(r"[a-z0-9]+", answer.lower()) if len(w) > 3]
    if not words:
        return True, 1.0
    source_words = set(re.findall(r"[a-z0-9]+", " ".join(sources).lower()))
    share = sum(1 for w in words if w in source_words) / len(words)
    return share >= min_overlap, round(share, 2)
