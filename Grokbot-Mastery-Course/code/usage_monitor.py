"""Token tracking, cost monitoring, budget alerts and model routing (Capstone 3).

STATUS: tested offline by test_offline.py. Uses the standard library only (sqlite3).
Prices come from tools/token_cost_calculator.py and are third-party, unverified figures.
"""
import datetime as dt
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from token_cost_calculator import cost  # noqa: E402

SCHEMA = """CREATE TABLE IF NOT EXISTS usage (
    ts TEXT, feature TEXT, model TEXT, input_tokens INT, cached_tokens INT,
    output_tokens INT, tool_calls INT, cost_usd REAL, ok INT)"""
TOOL_PRICE = 5.00 / 1000  # per call, third-party figure


class UsageMonitor:
    def __init__(self, path=":memory:", daily_budget_usd=10.0, alert=print):
        self.db = sqlite3.connect(path)
        self.db.execute(SCHEMA)
        self.daily_budget = daily_budget_usd
        self.alert = alert
        self._alerted = set()

    def record(self, feature, model, input_tokens, output_tokens, cached_tokens=0, tool_calls=0, ok=True, when=None):
        c = cost(model, input_tokens, output_tokens, cached_tokens) + tool_calls * TOOL_PRICE
        ts = (when or dt.datetime.now()).isoformat(timespec="seconds")
        self.db.execute("INSERT INTO usage VALUES (?,?,?,?,?,?,?,?,?)",
                        (ts, feature, model, input_tokens, cached_tokens, output_tokens, tool_calls, c, int(ok)))
        self._check_budget(ts[:10])
        return c

    def spent_on(self, day):
        return self.db.execute("SELECT COALESCE(SUM(cost_usd),0) FROM usage WHERE substr(ts,1,10)=?", (day,)).fetchone()[0]

    def _check_budget(self, day):
        spent = self.spent_on(day)
        for level in (0.5, 0.8, 1.0):
            key = (day, level)
            if spent >= self.daily_budget * level and key not in self._alerted:
                self._alerted.add(key)
                self.alert(f"ALERT {day}: ${spent:.2f} spent, {int(level*100)}% of the ${self.daily_budget:.2f} daily budget")

    def over_budget(self, day=None):
        day = day or dt.date.today().isoformat()
        return self.spent_on(day) >= self.daily_budget

    def report(self, day):
        rows = self.db.execute("""SELECT feature, COUNT(*), SUM(input_tokens), SUM(output_tokens),
                                  ROUND(SUM(cost_usd),4), ROUND(100.0*SUM(ok)/COUNT(*),1)
                                  FROM usage WHERE substr(ts,1,10)=? GROUP BY feature ORDER BY 5 DESC""", (day,)).fetchall()
        return [dict(zip(["feature", "requests", "input_tokens", "output_tokens", "cost_usd", "success_pct"], r)) for r in rows]


def route(task_text, cheap="grok-4.3", strong="grok-4.7"):
    """Send short, simple requests to a cheaper model and harder ones to a stronger model.

    The rule is deliberately simple; replace it with a classifier once you have test data.
    """
    hard_words = ("analyse", "analyze", "compare", "plan", "strategy", "contract", "calculate", "why")
    if len(task_text.split()) > 150 or any(w in task_text.lower() for w in hard_words):
        return strong
    return cheap


if __name__ == "__main__":
    m = UsageMonitor(daily_budget_usd=0.05)
    for i in range(30):
        q = "Where is my order?" if i % 3 else "Compare plan A and plan B for my business"
        model = route(q)
        m.record("support", model, 1500, 300)
    print(m.report(dt.date.today().isoformat()))
