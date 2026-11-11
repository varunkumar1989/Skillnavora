# Exercises and Final Assessment

Module exercises (three levels each) are at the end of every module. This file adds a consolidated assignment list and the final assessment.

## Assignments

| # | Assignment | Modules | Level |
|---|---|---|---|
| A1 | Agent-fit analysis of five tasks in your work | 1 | Beginner |
| A2 | Cost a 15-turn chat with the formula, then with the calculator | 3 | Beginner |
| A3 | Explain subscription vs API billing to a manager in 150 words | 4 | Beginner |
| A4 | Few-shot classifier with a 20-item test | 5 | Intermediate |
| A5 | Live API call in Python and cURL, with usage-based cost | 6 | Intermediate |
| A6 | Facts block added to `ChatSession` with a test | 7 | Intermediate |
| A7 | New risky tool in `agent_tools.py` with approval tests | 8 | Advanced |
| A8 | One-page commercial proposal for a business case | 9 | Advanced |
| A9 | Ten prompt-injection tests and a hardening plan | 10 | Advanced |
| A10 | One capstone project, submitted with the checklist | All | Advanced |

## Final assessment

**Part A: 20 multiple-choice questions (1 mark each)**

1. "Grokbot" most often refers to: (a) a Groq product (b) xAI's agent app Grok Bot (c) a GitHub library (d) an X ads tool → **b**
2. A Grok subscription includes API credits: (a) always (b) never (c) only if the official pricing page explicitly says so (d) on annual plans → **c**
3. Tokens are used because: (a) words are too short (b) a fixed sub-word vocabulary handles any text (c) billing is easier (d) they are faster to type → **b**
4. Usually more expensive per token: (a) input (b) output (c) cached input (d) they are equal → **b**
5. Input tokens in a chat that resends history grow: (a) not at all (b) linearly per turn, so the total grows quadratically (c) only at turn 1 (d) randomly → **b**
6. At $2 / $6 per 1M, 2,000 input + 500 output tokens cost: (a) $0.004 (b) $0.007 (c) $0.010 (d) $0.016 → **b**
7. To benefit from prompt caching, put stable content: (a) at the end (b) at the start (c) in the user message (d) in images → **b**
8. The system prompt is sent: (a) once per account (b) once per chat (c) with every request (d) only on errors → **c**
9. HTTP status to retry with backoff: (a) 401 (b) 400 (c) 429 (d) 404 → **c**
10. The API key belongs: (a) in browser JavaScript (b) in a public repository (c) in a server-side secret or environment variable (d) in the system prompt → **c**
11. `finish_reason: "length"` means: (a) success (b) the answer hit `max_tokens` (c) the key expired (d) rate limit → **b**
12. In tool calling, the tool is run by: (a) the model (b) your code (c) xAI's servers always (d) the user → **b**
13. RAG reduces hallucination by: (a) a bigger model (b) answering only from retrieved sources with citations (c) more temperature (d) longer answers → **b**
14. A step limit in an agent loop prevents: (a) tool use (b) endless loops and runaway cost (c) streaming (d) caching → **b**
15. Prompt injection is best limited by: (a) one rule in the system prompt (b) least-privilege tools and human approval (c) longer prompts (d) a larger context window → **b**
16. Authorisation answers: (a) who are you (b) what may you do (c) how fast (d) which model → **b**
17. Reported Grok Bot usage comes from: (a) unlimited use (b) a shared weekly usage pool (c) API credits (d) per-email fees → **b** [third-party]
18. Server-side web search on the API is reported to cost: (a) free (b) $5 per 1,000 calls (c) $5 per call (d) included in output tokens → **b** [third-party]
19. A good model-selection method is: (a) leaderboard rank (b) cheapest model that passes your own test set (c) newest model (d) largest context → **b**
20. Before switching model versions you should: (a) delete logs (b) re-run the test set and compare quality and cost (c) raise `max_tokens` (d) rotate the key → **b**

**Part B: Calculations (5 marks each; show working)**
1. A bot has a 400-token system prompt, 60-token questions and 200-token answers. Total input tokens for an 8-turn chat? *(Answer: 8 × 400 + 60 × 36 + 200 × 28 = 3,200 + 2,160 + 5,600 = **10,960**.)*
2. Cost of that chat at $2 / $6 per 1M with 1,600 output tokens? *(10,960 × 2 ÷ 1M + 1,600 × 6 ÷ 1M = 0.02192 + 0.0096 = **$0.03152**.)*
3. Monthly cost of 300 requests a day, 1,000 input and 200 output tokens, at $1.25 / $2.50, 30 days? *(9,000 requests × (1,000 × 1.25 + 200 × 2.5) ÷ 1M = 9,000 × 0.00175 = **$15.75**.)*

**Part C: Design question (25 marks)**
Design an AI assistant for a hospital's appointment desk. Include: Grok Bot vs API choice with reasons, architecture, tools and approvals, data-privacy measures, test plan, token and cost estimate with stated assumptions, and the human checks you would never remove.

**Part D: Capstone (40 marks)** marked against the project's evaluation criteria.

**Pass mark:** 60 of 100 (Part A 20 + Part B 15 + Part C 25 + Part D 40 = 100).
