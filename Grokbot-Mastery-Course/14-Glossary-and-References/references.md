# Pricing Tables, References and Verification Checklist

**Prices recorded:** 11 November 2026, from web-search results. **None verified on xAI's official pages**, which could not be opened from the environment used to write the course.

## 1. Pricing reference tables

### API, per 1,000,000 tokens **[Third-party]**
| Model | Input | Cached input | Output | Context | Notes |
|---|---|---|---|---|---|
| Grok 4.7 | $2.00 | $0.50 | $6.00 | 500K | $4.00 / $12.00 above 200K prompt tokens |
| Grok 4.3 | $1.25 | $0.20 | $2.50 | 1M | Single source |
| Grok Build 0.1 | $1.00 | – | $2.00 | – | Coding model |
| Web Search / X Search tools | $5 per 1,000 calls | | | | On top of tokens |

### Subscriptions **[Third-party; sources disagree]**
| Plan | Reported monthly price | Grok Bot included? |
|---|---|---|
| Free | $0 | No |
| SuperGrok Lite | $10 (inconsistent) | Not verified |
| SuperGrok | $30 | Not verified |
| SuperGrok Plus | $100 (inconsistent) | Not verified |
| SuperGrok Heavy | $300 | Not verified |
| X Subscription Plus | Not verified | No (per search summary of xAI docs) |
| X Subscription Premium / Super / Ultra | $30 / $100 / $200 reported, with other figures elsewhere | Yes (per search summary of xAI docs) |
| Grok Business | $30 per seat | Not verified |
| Grok Enterprise | Custom | Not verified |

### Token rules of thumb **[Estimate]**
| Content | Tokens |
|---|---|
| 1 English word | about 1.33 |
| 100 words | about 134 |
| 1,000 words | about 1,334 |
| 1 page (500 words) | about 667 |
| 300-page book (90,000 words) | about 120,000 |

## 2. Verification checklist (do this before budgeting or teaching)
- [ ] Open <https://docs.x.ai/docs/models>: record each model ID, context window, input/cached/output prices, and any long-context rule. Update `tools/token_cost_calculator.py`.
- [ ] Confirm how cached input is billed and whether caching is automatic.
- [ ] Confirm how reasoning tokens are reported and billed.
- [ ] Confirm server-side tool prices (web search, X search).
- [ ] Confirm image and audio token accounting for the models you use.
- [ ] Confirm the base URL, chat endpoint, streaming format and usage field names; run `code/grok_client.py` live.
- [ ] Confirm structured-output and embeddings support.
- [ ] Open <https://docs.x.ai/x-subscription/pricing> and the Grok Bot docs: record plans, prices, Grok Bot inclusion and usage limits.
- [ ] Check the signed-in checkout price in your region, including taxes.
- [ ] Read the data-use and retention terms for the API and business plans.
- [ ] Replace every **[Third-party]** label you have verified with **[Official, checked on DATE]**.

## 3. Official xAI sources (not reachable when the course was written)
- Grok Bot announcement: <https://x.ai/news/introducing-grok-bot>
- Grok Bot documentation: <https://docs.x.ai/grok-bot/overview>
- Models and pricing: <https://docs.x.ai/docs/models>
- X Subscription plans and usage: <https://docs.x.ai/x-subscription/pricing>
- xAI documentation home: <https://docs.x.ai>

## 4. Third-party sources used
**Grok Bot product**
- MindStudio: <https://www.mindstudio.ai/blog/grokbot-xai-agent-app>
- No Code Founders: <https://www.nocodefounders.com/guides/grokbot-explained-simply>
- Zapier: <https://zapier.com/blog/grok-bot/>
- Flavio Copes: <https://flaviocopes.com/grok-bot/>
- Createwith: <https://www.createwith.com/blog/we-both-tried-grokbot-we-disagree>
- T2 Online: <https://t2online.in/tech/tech-news/xai-launches-grok-bot-to-handle-tasks-across-apps-and-websites/2007230>
- Efficient App, Grok Bot vs Claude: <https://efficient.app/compare/grok-bot-vs-claude>

**Grok Bot plans and limits**
- Cursor help: <https://cursor.com/help/grok-bot/plans>
- eesel.ai: <https://www.eesel.ai/blog/grok-bot-pricing>
- Betanews: <https://betanews.com/article/grok-bot-usage-limits/>
- AI Builder Club: <https://www.aibuilderclub.com/blog/grok-bot-pricing>
- Runtime Wire: <https://runtimewire.com/article/grok-bot-cursor-pro-plus-free-trial-expansion>
- AI Pricing Guru: <https://www.aipricing.guru/news/xai-grok-bot-launch-pricing-impact-august-2026/>
- Let's Data Science: <https://letsdatascience.com/news/spacexai-considers-unified-grok-and-x-pricing-a2810bd3>

**Subscriptions**
- Build Fast with AI: <https://www.buildfastwithai.com/blogs/supergrok-explained-pricing-limits-is-it-worth-it-2026>
- Business Today, SuperGrok Lite: <https://www.businesstoday.in/technology/story/xai-makes-grok-affordable-with-new-supergrok-lite-plan-check-price-and-what-it-offers-522462-2026-03-26>
- Suprmind: <https://www.suprmind.ai/hub/grok/pricing/>
- Hi-Tech: <https://hi-tech.ua/en/elon-musks-supergrok-heavy-ai-plan-costs-300-per-month/>
- Tech.co: <https://tech.co/news/grok-ai-pricing>

**API pricing**
- MorphLLM: <https://www.morphllm.com/grok-api-pricing>
- BenchLM: <https://www.benchlm.ai/xai/api-pricing>
- Costbench changelog: <https://costbench.com/changelog/xai-api-price-increase-2026-08/>
- Price Per Token, Grok 4.7: <https://pricepertoken.com/pricing-page/model/xai-grok-4.7>
- Mem0: <https://mem0.ai/blog/xai-grok-api-pricing>
- AnotherWrapper, Grok 4.3: <https://anotherwrapper.com/llm-pricing/grok-4.3>

**Crawler**
- Botcrawl: <https://botcrawl.com/bots/grokbot>
- Promptwatch: <https://promptwatch.com/bots/grokbot>

## 5. General references

> These were not opened in the environment used to write the course. Check each link before relying on it.

- Anthropic, Building effective agents: <https://www.anthropic.com/research/building-effective-agents>
- OWASP Top 10 for LLM Applications: <https://genai.owasp.org/>
- India's Digital Personal Data Protection Act, 2023: <https://www.meity.gov.in/data-protection-framework>
- MDN, HTTP overview: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview>
- MDN, Server-sent events: <https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events>
