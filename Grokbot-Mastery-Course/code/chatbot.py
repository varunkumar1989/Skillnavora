"""A chatbot session with history management, a token budget and cost tracking.

STATUS: logic tested offline by test_offline.py (GROK_MOCK=1). Live API use is untested.

Run in a terminal:
    GROK_MOCK=1 python3 chatbot.py        # offline practice
    XAI_API_KEY=... python3 chatbot.py    # live (after checking the base URL and model ID)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from grok_client import chat, MODEL  # noqa: E402
from token_cost_calculator import cost, PRICES, words_to_tokens  # noqa: E402

SYSTEM_PROMPT = ("You are Navi, a friendly support assistant for an online shoe shop. "
                 "Returns are accepted within 30 days. Refunds take 5-7 working days. "
                 "If you do not know, say so and offer to connect the customer to a person. "
                 "Answer in at most 80 words.")


def estimate_tokens(text):
    return words_to_tokens(len(text.split())) + 4  # +4 for per-message formatting overhead (estimate)


class ChatSession:
    """Keeps the system prompt, the last turns that fit the budget, and a running cost."""

    def __init__(self, system_prompt=SYSTEM_PROMPT, history_budget=1500, max_answer_tokens=200,
                 model=None, max_user_chars=2000, monthly_budget_usd=None):
        self.system = {"role": "system", "content": system_prompt}
        self.history = []                 # list of {"role", "content"}
        self.history_budget = history_budget
        self.max_answer_tokens = max_answer_tokens
        self.model = model or MODEL
        self.max_user_chars = max_user_chars
        self.monthly_budget_usd = monthly_budget_usd
        self.spent_usd = 0.0
        self.log = []                     # one dict per request: tokens and cost

    def _trim(self):
        """Drop the oldest user/assistant pair until the history fits the token budget."""
        while self.history and sum(estimate_tokens(m["content"]) for m in self.history) > self.history_budget:
            self.history = self.history[2:] if len(self.history) >= 2 else []

    def ask(self, user_text, on_token=None):
        user_text = (user_text or "").strip()
        if not user_text:
            return "Please type a question."
        if len(user_text) > self.max_user_chars:
            return f"That message is too long. Please keep it under {self.max_user_chars} characters."
        if self.monthly_budget_usd is not None and self.spent_usd >= self.monthly_budget_usd:
            return "The assistant has reached its usage budget. Please contact support by email."

        self.history.append({"role": "user", "content": user_text})
        self._trim()
        messages = [self.system] + self.history
        try:
            answer, usage = chat(messages, model=self.model, max_tokens=self.max_answer_tokens,
                                 stream=on_token is not None, on_token=on_token)
        except Exception as e:  # network, auth or API error: keep the session usable
            self.history.pop()
            self.log.append({"error": str(e)})
            return "Sorry, I could not reach the assistant just now. Please try again in a minute."

        self.history.append({"role": "assistant", "content": answer})
        inp = usage.get("prompt_tokens", 0)
        out = usage.get("completion_tokens", 0)
        price_key = self.model if self.model in PRICES else "grok-4.7"
        c = cost(price_key, inp, out)
        self.spent_usd += c
        self.log.append({"input_tokens": inp, "output_tokens": out, "cost_usd": round(c, 6)})
        return answer


def main():
    s = ChatSession(monthly_budget_usd=float(os.environ.get("CHAT_BUDGET_USD", "5")))
    print("Navi support bot. Type 'quit' to stop, 'cost' to see usage.")
    while True:
        try:
            q = input("you> ")
        except EOFError:
            break
        if q.strip().lower() == "quit":
            break
        if q.strip().lower() == "cost":
            print(f"requests: {len(s.log)}  spent: ${s.spent_usd:.4f}")
            continue
        print("bot>", s.ask(q))


if __name__ == "__main__":
    main()
