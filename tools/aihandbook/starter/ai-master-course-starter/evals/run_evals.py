"""Run the golden set and print a scorecard plus a release-gate verdict.
Run: python evals/run_evals.py           (exit code 1 if the release gate fails, so CI can use it)"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from starter.ops import release_gate
from starter.rag import answer, index_pdf

BARS = {"answer_accuracy": (0.80, 0.05), "citation_page_correct": (0.80, 0.05), "refusal_correct": (1.0, 0.0)}


def run(golden_path=os.path.join(ROOT, "evals", "golden.jsonl"), pdf=os.path.join(ROOT, "data", "sample_policy.pdf")):
    store = index_pdf(pdf)
    rows = [json.loads(line) for line in open(golden_path) if line.strip()]
    answerable = refusals = correct = cited = refused_ok = 0
    failures = []
    for row in rows:
        r = answer(store, row["question"], log=False)
        if row["expect"] in ("REFUSE", "BLOCK"):
            refusals += 1
            ok = bool(r.get("blocked")) if row["expect"] == "BLOCK" else (r.get("refused") or bool(r.get("blocked")))
            refused_ok += ok
        else:
            answerable += 1
            ok = row["expect"].lower() in r["answer"].lower() and not r.get("refused")
            correct += ok
            tag = r["answer"].rsplit("[", 1)[-1].rstrip("]") if "[" in r["answer"] else None
            page = next((s["page"] for s in r.get("sources", []) if s["tag"] == tag), None)
            cited += page == row.get("page")
        if not ok:
            failures.append((row["question"], row["expect"], r["answer"]))
    scores = {
        "answer_accuracy": correct / max(answerable, 1),
        "citation_page_correct": cited / max(answerable, 1),
        "refusal_correct": refused_ok / max(refusals, 1),
    }
    return scores, failures


if __name__ == "__main__":
    scores, failures = run()
    for name, value in scores.items():
        print(f"{name:<24} {value:.2f}  (bar {BARS[name][0]:.2f})")
    for q, expect, got in failures:
        print(f"FAIL: {q}\n      expected: {expect}\n      got: {got}")
    baseline_path = os.path.join(ROOT, "evals", "baseline.json")
    baseline = json.load(open(baseline_path)) if os.path.exists(baseline_path) else scores
    ok, problems = release_gate(scores, baseline, BARS)
    print("RELEASE GATE:", "PASS" if ok else "FAIL " + "; ".join(problems))
    sys.exit(0 if ok else 1)
