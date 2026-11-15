"""Lesson 3: where the time goes, what a request costs, and what caching saves.
Run: python examples/l3_latency_cost.py"""
import functools, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starter.costs import Timer, cost_per_successful_task, percentile, request_cost
from starter.rag import answer, index_pdf

PDF = os.path.join(os.path.dirname(__file__), "..", "data", "sample_policy.pdf")

timer = Timer()
with timer.part("index"):
    store = index_pdf(PDF)
with timer.part("answer"):
    r = answer(store, "When must expense claims be submitted?", log=False)
print("1) Timings for one cold request (offline mode)")
print(timer.report())
print("   inside answer():", r["timings_ms"])

print("\n2) Cost of one request at three illustrative price points (per 1M tokens)")
tokens_in, tokens_out = 1800, 250
for name, pin, pout in [("large model", 4.00, 20.00), ("mid model", 2.00, 10.00), ("small model", 0.10, 0.50)]:
    print(f"   {name:<12} ${request_cost(tokens_in, tokens_out, pin, pout):.5f} per request  -> ${request_cost(tokens_in, tokens_out, pin, pout) * 10000:.2f} per 10,000 requests")

print("\n3) Cost per successful task (what managers care about)")
for name, cost_each, success_rate in [("cheap but weak", 0.0005, 0.60), ("dearer but accurate", 0.0020, 0.95)]:
    n = 1000
    print(f"   {name:<20} ${cost_per_successful_task(cost_each * n, int(n * success_rate)):.5f} per correct answer ({success_rate:.0%} pass)")

print("\n4) Caching repeated questions")
@functools.lru_cache(maxsize=256)
def cached_answer(q: str) -> str:
    return answer(store, q, log=False)["answer"]

times = []
for i in range(5):
    t = time.perf_counter(); cached_answer("How many days a week can I work remotely?"); times.append((time.perf_counter() - t) * 1000)
print(f"   first call {times[0]:.3f} ms, repeat calls about {sum(times[1:]) / 4:.4f} ms (cache hits: {cached_answer.cache_info().hits})")
print(f"   p50 {percentile(times, 50):.4f} ms, p95 {percentile(times, 95):.3f} ms")
