"""Lesson 4: request logs with personal data removed, prompt versions and a release gate.
Run: python examples/l4_llmops.py"""
import collections, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starter.ops import get_prompt, log_request, read_log, release_gate

log_path = os.path.join(tempfile.mkdtemp(), "requests.jsonl")

print("1) Structured log lines (personal data removed)")
log_request(log_path, question="My email is ravi@example.com, how many leave days?", prompt_version="rag-answer@v2", latency_ms=420, tokens={"input": 1650, "output": 60}, refused=False)
log_request(log_path, question="What is the dress code?", prompt_version="rag-answer@v2", latency_ms=95, tokens=None, refused=True)
log_request(log_path, question="Expense deadline?", prompt_version="rag-answer@v1", latency_ms=610, tokens={"input": 1700, "output": 90}, refused=False)
for rec in read_log(log_path):
    print("  ", {k: rec[k] for k in ("question", "prompt_version", "latency_ms", "refused")})

print("\n2) A daily summary from the log")
rows = read_log(log_path)
lat = sorted(r["latency_ms"] for r in rows)
print(f"   requests={len(rows)}  refusal rate={sum(r['refused'] for r in rows) / len(rows):.0%}  max latency={lat[-1]} ms")
print("   by prompt version:", dict(collections.Counter(r["prompt_version"] for r in rows)))

print("\n3) Prompt versions are stored like code")
for v in ("rag-answer@v1", "rag-answer@v2"):
    print(f"   {v}: {get_prompt(v)[:70]}...")

print("\n4) Release gate: compare the new version with the last release")
bars = {"accuracy": (0.90, 0.02), "refusal_correct": (0.95, 0.0)}
last = {"accuracy": 0.93, "refusal_correct": 1.00}
for label, new in [("candidate A", {"accuracy": 0.94, "refusal_correct": 1.00}), ("candidate B", {"accuracy": 0.95, "refusal_correct": 0.75})]:
    ok, problems = release_gate(new, last, bars)
    print(f"   {label}: {'RELEASE' if ok else 'BLOCKED'} {problems if problems else ''}")
