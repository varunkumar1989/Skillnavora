"""Cost and latency helpers."""
import time
from contextlib import contextmanager

from .config import settings


def request_cost(input_tokens: int, output_tokens: int, price_in_per_m: float | None = None, price_out_per_m: float | None = None) -> float:
    pin = settings.price_in_per_m if price_in_per_m is None else price_in_per_m
    pout = settings.price_out_per_m if price_out_per_m is None else price_out_per_m
    return input_tokens / 1_000_000 * pin + output_tokens / 1_000_000 * pout


def cost_per_successful_task(total_cost: float, successes: int) -> float:
    return float("inf") if successes == 0 else total_cost / successes


class Timer:
    """Collects named timings: with timer.part("retrieve"): ..."""

    def __init__(self):
        self.parts: dict[str, float] = {}

    @contextmanager
    def part(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.parts[name] = self.parts.get(name, 0.0) + time.perf_counter() - start

    def report(self) -> str:
        total = sum(self.parts.values()) or 1e-9
        return "\n".join(f"{k:<12} {v * 1000:8.2f} ms  {v / total:6.1%}" for k, v in self.parts.items())


def percentile(values: list[float], p: float) -> float:
    s = sorted(values)
    if not s:
        return 0.0
    i = min(len(s) - 1, int(round(p / 100 * (len(s) - 1))))
    return s[i]
