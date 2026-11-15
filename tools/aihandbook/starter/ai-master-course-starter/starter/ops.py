"""LLMOps basics: a request log with personal data removed, prompt versions, and a release gate."""
import json
import os
import time
import uuid

from .guardrails import redact_pii

PROMPTS = {
    "rag-answer@v1": "Answer only from the sources. Cite the source tag for each claim. If the sources do not contain the answer, say you don't know.",
    "rag-answer@v2": ("You answer questions about company documents. Use only the numbered sources. After each claim, cite its tag "
                      "like [S1]. If the sources do not contain the answer, reply exactly: I don't know. The documents I was given do not answer this question."),
}


def get_prompt(name_version: str) -> str:
    return PROMPTS[name_version]


def log_request(path: str, **fields) -> dict:
    """Append one JSON line. Text fields are redacted before writing."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    record = {"id": str(uuid.uuid4())[:8], "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
    for k, v in fields.items():
        record[k] = redact_pii(v)[0] if isinstance(v, str) else v
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
    return record


def read_log(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def release_gate(new: dict, old: dict, bars: dict) -> tuple[bool, list[str]]:
    """Block a release if any metric is below its bar or worse than the last release by more
    than the allowed drop. bars = {"accuracy": (0.9, 0.02), ...} means minimum 0.9 and at most 0.02 worse."""
    problems = []
    for metric, (minimum, allowed_drop) in bars.items():
        value, before = new.get(metric, 0.0), old.get(metric, 0.0)
        if value < minimum:
            problems.append(f"{metric} {value:.2f} is below the bar {minimum:.2f}")
        if before - value > allowed_drop:
            problems.append(f"{metric} fell from {before:.2f} to {value:.2f}")
    return (not problems), problems
