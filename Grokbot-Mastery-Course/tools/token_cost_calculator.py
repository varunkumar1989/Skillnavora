"""Token and API cost calculator for the Grokbot Mastery Course.

Run:  python3 token_cost_calculator.py          (prints every worked example in the course)
      python3 token_cost_calculator.py --test   (runs the self-checks)

PRICES below are THIRD-PARTY figures (aggregator sites found by web search on 2026-11-11).
They were NOT verified against xAI's official pricing page, which could not be reached from
the environment used to write the course. Replace them with the official figures from
https://docs.x.ai/docs/models before budgeting.

Token counts from words are ESTIMATES. The ratio of tokens to words depends on the model's
tokenizer and the language. Measure real counts from the `usage` field of an API response.
"""
import sys

# USD per 1,000,000 tokens. Source: third-party aggregators (see course references). Unverified.
PRICES = {
    "grok-4.7":       {"input": 2.00, "output": 6.00, "cached_input": 0.50,
                       "long_input": 4.00, "long_output": 12.00, "long_threshold": 200_000},
    "grok-4.3":       {"input": 1.25, "output": 2.50, "cached_input": 0.20},
    "grok-build-0.1": {"input": 1.00, "output": 2.00, "cached_input": None},
}
TOOL_PRICE_PER_1000_CALLS = 5.00  # server-side Web Search / X Search, third-party figure, unverified

TOKENS_PER_WORD = 4 / 3  # common estimate for English (about 0.75 words per token); varies by tokenizer


def words_to_tokens(words, ratio=TOKENS_PER_WORD):
    """Estimated tokens for a number of English words, rounded up."""
    t = words * ratio
    return int(t) if t == int(t) else int(t) + 1


def cost(model, input_tokens, output_tokens, cached_input_tokens=0):
    """Cost in USD for one request.

    cached_input_tokens is the part of input_tokens served from the prompt cache.
    Long-context pricing applies to the whole request when the prompt exceeds the threshold.
    """
    p = PRICES[model]
    if cached_input_tokens > input_tokens:
        raise ValueError("cached tokens cannot exceed input tokens")
    in_price, out_price = p["input"], p["output"]
    if p.get("long_threshold") and input_tokens > p["long_threshold"]:
        in_price, out_price = p["long_input"], p["long_output"]
    cached_price = p["cached_input"] if p["cached_input"] is not None else in_price
    fresh = input_tokens - cached_input_tokens
    return (fresh / 1_000_000 * in_price
            + cached_input_tokens / 1_000_000 * cached_price
            + output_tokens / 1_000_000 * out_price)


def conversation(turns, system_tokens, user_tokens, answer_tokens):
    """Token totals for a chat that resends the full history on every turn.

    Turn n (1-based) sends: system prompt + n user messages + (n-1) previous answers.
    Returns (per_turn_inputs, total_input, total_output).
    """
    per_turn = [system_tokens + n * user_tokens + (n - 1) * answer_tokens for n in range(1, turns + 1)]
    return per_turn, sum(per_turn), turns * answer_tokens


def monthly(model, requests_per_day, input_tokens, output_tokens, days=30, cached_share=0.0):
    """Monthly cost for a steady workload."""
    cached = int(input_tokens * cached_share)
    return requests_per_day * days * cost(model, input_tokens, output_tokens, cached)


def _usd(x):
    return f"${x:,.4f}" if x < 1 else f"${x:,.2f}"


def examples():
    m = "grok-4.7"
    print("All prices: third-party, unverified, USD per 1M tokens. Model used:", m, PRICES[m])
    print()
    t100 = words_to_tokens(100)
    print(f"1. 100-word prompt  -> about {t100} tokens; input cost {_usd(cost(m, t100, 0))}")
    t1000 = words_to_tokens(1000)
    print(f"2. 1,000-word document -> about {t1000} tokens; summarise it in 300 tokens: {_usd(cost(m, t1000, 300))}")
    per, tin, tout = conversation(10, 300, 50, 200)
    print(f"3. 10-turn chat (system 300, user 50, answer 200 tokens each): inputs per turn {per}")
    print(f"   total input {tin:,} tokens, total output {tout:,} tokens, cost {_usd(cost(m, tin, tout))}")
    print(f"   if each turn sent only the new message (no history): input {10*(300+50):,} tokens")
    print(f"4. System prompt 300 vs 3,000 tokens, 10,000 requests: "
          f"{_usd(10_000*cost(m, 300+50, 200))} vs {_usd(10_000*cost(m, 3000+50, 200))}")
    print(f"5. Short vs long answer (500 input): 150 tokens {_usd(cost(m, 500, 150))} vs 1,500 tokens {_usd(cost(m, 500, 1500))}")
    print(f"6. Unneeded context: 2,000 relevant vs 20,000 pasted tokens, 300 output: "
          f"{_usd(cost(m, 2000, 300))} vs {_usd(cost(m, 20000, 300))}")
    print(f"7. Caching: 20,000-token prompt with 18,000 cached: {_usd(cost(m, 20000, 300, 18000))} (no cache {_usd(cost(m, 20000, 300))})")
    print(f"8. Long context: 250,000-token prompt, 1,000 output: {_usd(cost(m, 250_000, 1000))} (rate switches above 200K)")
    print()
    print("Monthly estimates (support bot: 1,500 input, 300 output tokens per request):")
    for name, rpd in (("light", 50), ("moderate", 500), ("heavy", 5000)):
        print(f"   {name:9s} {rpd:>5} requests/day: grok-4.7 {_usd(monthly(m, rpd, 1500, 300))}"
              f" | grok-4.3 {_usd(monthly('grok-4.3', rpd, 1500, 300))}"
              f" | grok-4.7 with 60% cached input {_usd(monthly(m, rpd, 1500, 300, cached_share=0.6))}")
    print(f"   plus web-search tool calls: 1,000 calls = ${TOOL_PRICE_PER_1000_CALLS:.2f}")


def _test():
    assert words_to_tokens(100) == 134 and words_to_tokens(1000) == 1334 and words_to_tokens(3) == 4
    assert abs(cost("grok-4.7", 100_000, 0) - 0.20) < 1e-9           # $2 per 1M, below the threshold
    assert abs(cost("grok-4.7", 0, 1_000_000) - 6.00) < 1e-9
    assert abs(cost("grok-4.7", 100_000, 0, 100_000) - 0.05) < 1e-9  # cached at $0.50 per 1M
    assert abs(cost("grok-4.7", 250_000, 0) - 1.00) < 1e-9          # long rate $4 per 1M
    assert abs(cost("grok-build-0.1", 1000, 1000, 500) - 0.003) < 1e-12  # no cache price: full rate
    per, tin, tout = conversation(10, 300, 50, 200)
    assert per[0] == 350 and per[-1] == 300 + 500 + 1800 and tin == 14_750 and tout == 2_000
    assert abs(cost("grok-4.7", 14_750, 2_000) - 0.0415) < 1e-12
    assert abs(monthly("grok-4.7", 50, 1500, 300) - 50 * 30 * (1500 * 2 + 300 * 6) / 1e6) < 1e-9
    try:
        cost("grok-4.7", 10, 0, 20); raise AssertionError("expected ValueError")
    except ValueError:
        pass
    print("all calculator tests passed")


if __name__ == "__main__":
    _test() if "--test" in sys.argv else examples()
