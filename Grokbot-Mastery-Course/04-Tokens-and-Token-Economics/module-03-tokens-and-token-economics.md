# Module 3: Tokens, Context Windows and Token Economics

**Level:** Beginner to advanced · **Time:** about 4 hours · **Tool:** `tools/token_cost_calculator.py`

> **Prices in this module are third-party and unverified.** They come from aggregator websites found by web search on 11 November 2026, because xAI's pricing page could not be opened. The **arithmetic** is checked by the course calculator. Replace the prices with the official ones from <https://docs.x.ai/docs/models> before you budget.

Prices used: **Grok 4.7: $2.00 input, $6.00 output, $0.50 cached input per 1M tokens; $4.00 / $12.00 when the prompt exceeds 200,000 tokens. Grok 4.3: $1.25 input, $2.50 output, $0.20 cached input.** **[Third-party]**

---

## Chapter 3.1 What a token is

### Pillar 1: Core objective
Explain tokens to a non-technical person and estimate them for any text.

### Pillar 2: Key concepts

**Topic 3.1.1 Definition.** A **token** is a piece of text the model reads or writes: a whole word, part of a word, a number fragment, a space or a punctuation mark. Models process and bill in tokens.

```
"Tokenisation isn't hard!"  →  [Token][isation][ isn]['t][ hard][!]   (illustrative split)
```
The exact split depends on the model's **tokenizer**, so the same sentence can be a different number of tokens in Grok, GPT and Claude.

**Topic 3.1.2 Why tokens instead of words?** Words are an open set (new names, typos, languages, code). Splitting text into a fixed vocabulary of sub-word pieces lets one model handle any text. Common words become one token; rare words split into several.

**Topic 3.1.3 How text becomes tokens.** Most modern tokenizers use **byte-pair encoding (BPE)** or a similar method: start from characters or bytes, and merge the pairs that appear most often in training text into single tokens, repeatedly, until the vocabulary reaches a set size. Each token has an ID number; the model actually works with these numbers.

**Topic 3.1.4 Characters, words and tokens.**

| Unit | "The invoice is overdue." | Rule of thumb for English **[Estimate]** |
|---|---|---|
| Characters | 23 | about 4 characters per token |
| Words | 4 | about 0.75 words per token |
| Tokens | about 5–6 | about 1.33 tokens per word |

Other languages, code and numbers often use **more** tokens per word. Hindi, Tamil or Japanese text can use several times more tokens than the same meaning in English, depending on the tokenizer. Always measure.

### Pillar 3: SOP: measure tokens for real
1. Estimate first: words × 1.33.
2. Send the text to the API once and read the `usage` object in the response (for example `prompt_tokens`, `completion_tokens`, and a cached-token count where reported).
3. If xAI offers a tokenize endpoint or SDK function, use it to count without generating an answer; check the API reference **[Unverified]**.
4. Record actual tokens per word for your own content type; use that ratio from now on.

### Pillar 4: Pitfalls
- Using a tokenizer from another vendor to count Grok tokens: it will be close but not exact.
- Forgetting that spaces, line breaks, JSON brackets and Markdown symbols are tokens too.

---

## Chapter 3.2 Input, output and hidden tokens

### Pillar 1: Core objective
Know every category of token that appears on the bill.

### Pillar 2: Key concepts

| Category | What it is | Billed as |
|---|---|---|
| **Input tokens** | Everything you send: system prompt, history, user message, documents, tool definitions | Input rate |
| **System prompt tokens** | Your fixed instructions, resent every request | Input rate (cached rate if cached) |
| **Conversation history tokens** | Earlier turns resent for context | Input rate |
| **Cached input tokens** | Repeated prompt prefix the provider recognises and serves from cache | Lower cached rate, if supported (reported $0.50 vs $2.00 per 1M for Grok 4.7 **[Third-party]**) |
| **Output tokens** | The answer the model writes | Output rate (usually 3× or more the input rate) |
| **Reasoning tokens** | Internal "thinking" some models do before answering | Commonly billed as output; **how xAI reports and bills them is unverified** |
| **Tool-call tokens** | The model's request to call a function, and the tool result you send back | Output and input respectively |
| **Image, audio tokens** | Non-text inputs converted to tokens | Depends on the model; check docs **[Unverified]** |

**Topic 3.2.1 Context window versus token limits.**
- **Context window:** total tokens (input + output) one request can hold.
- **Max output tokens:** the cap on the answer, which you can lower with `max_tokens`.
- **Rate limits:** tokens or requests per minute your account may use (Module 4).

Formula: **input tokens + output tokens ≤ context window**.

### Pillar 3: SOP: read the usage block
1. Make one request.
2. Log `prompt_tokens`, cached tokens, `completion_tokens` and any reasoning-token field.
3. Multiply each by its rate and add them up.
4. Compare with the billing console a day later. If they differ, look for reasoning or tool tokens.

### Pillar 4: Pitfalls
- Ignoring reasoning tokens: a short visible answer can still use many billed tokens.
- Ignoring server-side tool fees: web search and X search are reported at **$5 per 1,000 calls** in addition to tokens **[Third-party]**.

---

## Chapter 3.3 The cost formula

### Pillar 2: Key concepts

**Basic formula**

> **API cost = (input tokens ÷ 1,000,000 × input price) + (output tokens ÷ 1,000,000 × output price)**

**With caching**

> **Cost = (uncached input ÷ 1M × input price) + (cached input ÷ 1M × cached price) + (output ÷ 1M × output price)**

**With long-context pricing (as reported for Grok 4.7)**: if the prompt is above 200,000 tokens, use $4.00 input and $12.00 output for the request **[Third-party]**. Check the official rule: whether the higher rate applies to the whole request or only the excess.

**Plus tools**: + (tool calls ÷ 1,000 × tool price).

### Pillar 3: Worked example by hand
A 1,334-token prompt with a 300-token answer on Grok 4.7:
- Input: 1,334 ÷ 1,000,000 × $2.00 = $0.002668
- Output: 300 ÷ 1,000,000 × $6.00 = $0.001800
- **Total: $0.004468 ≈ $0.0045** (matches the calculator)

---

## Chapter 3.4 Mandatory worked examples

All results below are printed by `python3 tools/token_cost_calculator.py` **[Estimate, third-party prices]**.

### Example 1: a 100-word prompt
100 words × 1.33 ≈ **134 tokens**. Input cost on Grok 4.7: 134 ÷ 1M × $2 = **$0.0003**. At this scale, one prompt is a fraction of a cent; cost comes from volume.

### Example 2: a 1,000-word document
1,000 words ≈ **1,334 tokens**. Summarising it in a 300-token answer costs **$0.0045**. Summarising 10,000 such documents a month costs about **$45**.

### Example 3: a conversation of 10 consecutive prompts
Assume a 300-token system prompt, 50-token user messages and 200-token answers. Every turn resends the system prompt and all previous messages.

| Turn | Input tokens sent | Why |
|---|---|---|
| 1 | 350 | 300 system + 50 user |
| 2 | 600 | + previous user (50) + previous answer (200) + new user (50) |
| 3 | 850 | grows by 250 each turn |
| 4 | 1,100 | |
| 5 | 1,350 | |
| 6 | 1,600 | |
| 7 | 1,850 | |
| 8 | 2,100 | |
| 9 | 2,350 | |
| 10 | 2,600 | |
| **Total** | **14,750 input**, 2,000 output | **$0.0415** on Grok 4.7 |

If each turn sent only the system prompt and the new message, input would be **3,500** tokens. History made input **4.2 times larger**.

**Formula for turn n:** input = S + n × U + (n − 1) × A, where S = system tokens, U = user tokens, A = answer tokens. Total input over N turns = N × S + U × N(N+1)/2 + A × N(N−1)/2. Input grows with the **square** of the number of turns.

### Example 4: how a long system prompt increases input usage
10,000 requests, each with a 50-token question and a 200-token answer:
- 300-token system prompt: **$19.00**
- 3,000-token system prompt: **$73.00**

The extra 2,700 tokens are sent 10,000 times: 27 million extra input tokens.

### Example 5: short versus long responses
Same 500-token input:
- 150-token answer: **$0.0019**
- 1,500-token answer: **$0.0100**

Output costs three times input per token here, so long answers are the fastest way to raise a bill. Set `max_tokens` and ask for concise formats.

### Example 6: unnecessary context
Answering a question with 2,000 relevant tokens costs **$0.0058**; pasting a whole 20,000-token document to answer the same question costs **$0.0418**, over **7 times** more, and can lower accuracy.

### Example 7: caching
A 20,000-token prompt where 18,000 tokens are a repeated, cached prefix (for example a fixed policy document): **$0.0148** instead of **$0.0418**. Put stable content (instructions, reference documents) at the **start** of the prompt and the changing question at the **end**, so the prefix can be cached. Confirm on xAI's documentation whether caching is automatic and how long cached content lasts **[Unverified]**.

### Example 8: long-context pricing
A 250,000-token prompt with a 1,000-token answer is above the reported 200K threshold: **$1.01** at $4 / $12. Splitting it into chunks under 200K, or retrieving only the relevant parts, avoids the higher rate.

---

## Chapter 3.5 Token optimisation techniques

| Technique | Saves | How |
|---|---|---|
| Trim the system prompt | Input × every request | Remove repetition; keep rules short |
| Cap history | Input, grows per turn | Keep last k turns; summarise older ones |
| Retrieve, don't paste | Input | Send only relevant chunks (RAG) |
| Cache stable prefixes | Input price | Fixed content first |
| Limit output | Output (expensive) | `max_tokens`, "answer in 3 bullets" |
| Use structured output | Output and retries | JSON schemas reduce rambling and re-asks |
| Route to cheaper models | Price per token | Small model for easy tasks |
| Batch work | Requests, overhead | Classify 20 items per request |
| Avoid needless tool calls | Tool fees | Call search only when needed |
| Monitor | Surprises | Log tokens and cost per request |

### Pillar 4: Pitfalls
- Over-trimming instructions until quality drops. Re-run your test set after every cut.
- Summarising history so aggressively that the bot forgets the customer's order number.

---

## Chapter 3.6 Using the token and API cost calculator

The calculator in `tools/token_cost_calculator.py` provides:
- `words_to_tokens(words)`: estimate tokens from words.
- `cost(model, input_tokens, output_tokens, cached_input_tokens)`: cost of one request, with caching and long-context pricing.
- `conversation(turns, system, user, answer)`: token totals for a chat with full history.
- `monthly(model, requests_per_day, input, output, days, cached_share)`: monthly estimate.

```bash
python3 tools/token_cost_calculator.py --test   # self-checks
python3 tools/token_cost_calculator.py          # prints all worked examples
```

```python
from token_cost_calculator import cost, monthly
print(cost("grok-4.7", 1500, 300))            # one support reply
print(monthly("grok-4.7", 500, 1500, 300))    # 500 replies a day for 30 days -> 72.0
```

To use official prices, edit the `PRICES` dictionary at the top of the file.

---

## Module 3 exercises

**Level 1.** Count the words in three of your own emails. Estimate their tokens and the cost of sending each as input to Grok 4.7.

**Level 2.** Your bot has a 600-token system prompt, 80-token questions and 250-token answers. Use the formula to compute total input for a 15-turn chat, then check it with `conversation()`.

**Level 3.** Design a history policy (keep last 4 turns plus a 150-token summary) and calculate the saving for 30-turn chats at 1,000 chats a day, using `cost()` and your own loop.

## Knowledge check
1. Why can the same sentence be a different number of tokens on two models?
2. Which is usually more expensive per token: input or output?
3. Why does a 10-turn chat cost more than 10 times a single question?
4. Where should stable content go in a prompt to benefit from caching?
5. What is the total cost of 2,000 input and 500 output tokens at $2 / $6 per 1M?

**Answers:** (1) Each model has its own tokenizer. (2) Output. (3) History is resent each turn, so input grows quadratically. (4) At the start, as a fixed prefix. (5) 2,000 × 2 ÷ 1M + 500 × 6 ÷ 1M = $0.004 + $0.003 = **$0.007**.
