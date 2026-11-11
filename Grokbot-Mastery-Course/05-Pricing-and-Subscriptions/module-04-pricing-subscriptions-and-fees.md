# Module 4: Pricing, Subscription Plans and Fees

**Level:** Beginner · **Time:** about 2 hours · **Prices checked:** 11 November 2026, from search results only

> **Read before using any number in this module.** xAI's pricing pages could not be opened from the environment used to write this course. Every price below is **[Third-party]** unless marked otherwise, and sources **disagree**. Plan names and prices have changed several times in 2026. Confirm on xAI's official pages (listed at the end) and at the signed-in checkout before you buy or quote a price to a client.

---

## Chapter 4.1 Two completely different ways to pay

### Pillar 1: Core objective
Never confuse a **subscription** with **API billing** again.

### Pillar 2: Key concepts

| | Subscription (app) | API (pay-as-you-go) |
|---|---|---|
| What you get | Access to Grok chat, and on some plans Grok Bot agents | Programmatic access to Grok models for your own software |
| How you pay | Fixed monthly or annual fee per person or seat | Per token used, plus tool-call fees, billed to an API account |
| Usage limits | A usage allowance; reported to be a **shared weekly pool** across Grok products since June 2026 | Rate limits per minute, plus whatever balance or spend limit you set |
| Where | grok.com, X, mobile and desktop apps | xAI developer console and API |
| Good for | Individuals and teams using AI themselves | Products, automations and integrations |

> **Rule.** **A subscription fee does not include API credits.** Paying for a Grok plan does not let your website call the Grok API for free, and an API balance does not unlock subscription features. If a provider ever bundles credits, it will say so explicitly on its official pricing page. Assume nothing.

> **Analogy.** A subscription is a gym membership: a fixed fee, use it within the fair-use rules. The API is a taxi meter: you pay for exactly the distance travelled.

### Pillar 4: Pitfalls
- Building a customer-facing chatbot on a personal subscription account. That is not what subscriptions are for and may breach the terms; use the API.
- Budgeting an agent workload on "unlimited" assumptions. Reviewers report Grok Bot usage running out quickly **[Third-party]**.

---

## Chapter 4.2 Subscription plans (individuals, teams and business)

### Pillar 2: Key concepts

Two naming schemes appear in third-party sources. Sources suggest xAI has been moving towards a single "X Subscription" covering Grok and X, but this could not be confirmed.

**Scheme A: SuperGrok plans** **[Third-party]**

| Parameter | Free | SuperGrok Lite | SuperGrok | SuperGrok Plus | SuperGrok Heavy |
|---|---|---|---|---|---|
| Monthly fee | $0 | $10 (inconsistently reported) | **$30** (most sources agree) | $100 (inconsistently reported) | **$300** (most sources agree; promotional $99 for 3 months reported) |
| Annual fee | – | Not verified | Not verified | Not verified | Not verified |
| Included features | Basic Grok chat with limits | Not verified | Higher limits, newer models | Not verified | Highest limits and the heaviest models |
| Usage limits | Not verified | Not verified | Shared weekly usage pool (reported since June 2026) | Same | Same |
| API access | No | No | No | No | No (API is billed separately) |
| Token pricing | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Best suited for | Trying Grok | Light users | Regular individual users | Power users | Heavy research and agent use |

**Scheme B: X Subscription tiers and Grok Bot** **[Official xAI page, seen only as a search-engine summary; prices third-party]**

According to a search summary of xAI's "Plans and usage" documentation (<https://docs.x.ai/x-subscription/pricing>), **Grok Bot is included on the Premium, Super and Ultra tiers, for individuals and for team seats, and is not included on Plus or Free**. Grok Bot usage draws from the seat's **shared weekly usage pool**, not a separate allowance.

| Parameter | Plus | Premium | Super | Ultra |
|---|---|---|---|---|
| Monthly fee | Not verified | Reported $30, but other sources differ | Reported $100, but other sources differ | Reported $200, $300 in another source |
| Annual fee | Not verified | Not verified | Not verified | Not verified |
| Grok Bot | **No** | **Yes** | **Yes** | **Yes** |
| Usage limits | Shared weekly pool | Shared weekly pool | Shared weekly pool | Shared weekly pool |
| API access | No | No | No | No |
| Best suited for | Grok chat only | First agents | Daily agent use | Heavy agent use |

Reports also mention Grok Bot being reachable through **Cursor** plans (for example a $60 Cursor Pro+ plan, and a limited free trial), where the larger of the two weekly allowances applies and they do not stack **[Third-party]**.

**Business and enterprise** **[Third-party]**
| Parameter | Grok Business | Grok Enterprise |
|---|---|---|
| Fee | **$30 per seat per month** (reported launch early 2026) | Custom quote |
| Features | Team workspace, admin controls (details not verified) | Enterprise security, data terms, support (not verified) |
| API access | Separate | Separate or contracted |
| Best for | Small teams | Large organisations with compliance needs |

### Pillar 3: SOP: verify a plan before buying
1. Open xAI's plans page and the X Subscription pricing page.
2. Sign in and go to checkout: the signed-in price includes your region's currency and taxes.
3. Find the usage-limit wording: daily, weekly or monthly; per product or shared.
4. Check whether Grok Bot is included in that tier.
5. Check the data terms for business use.
6. Save a screenshot with the date for your records.

### Pillar 4: Pitfalls
- Comparing a promotional price with a list price.
- Assuming limits stay the same: limits were reported changed on 21 August 2026, ten days after Grok Bot launched **[Third-party]**.
- Ignoring regional taxes: Indian buyers pay GST on foreign digital services; checkout prices may differ from US list prices.

---

## Chapter 4.3 API pricing (developer, pay-as-you-go)

### Pillar 2: Key concepts

**Model-specific charges per 1,000,000 tokens** **[Third-party]**

| Model | Input | Cached input | Output | Context | Long-context rate |
|---|---|---|---|---|---|
| Grok 4.7 (reported flagship) | $2.00 | $0.50 | $6.00 | 500K | $4.00 / $12.00 above 200K prompt tokens |
| Grok 4.3 | $1.25 | $0.20 | $2.50 | 1M | Not reported |
| Grok Build 0.1 (coding) | $1.00 | Not reported | $2.00 | Not reported | Not reported |

**Additional usage charges** **[Third-party]**
- Server-side tools such as **Web Search** and **X Search**: **$5 per 1,000 calls**, on top of tokens.
- Images, audio and other modalities: **not verified**.

**Disagreements between sources**
- One source says all Grok text models share the same per-token rates; others list different rates per model.
- Sources disagree on which model is the current flagship (Grok 4.6 in August, Grok 4.7 from September 2026) and on release dates.
- A price change in August 2026 is reported by a pricing tracker; details could not be opened.

**Rate limits.** Requests per minute and tokens per minute depend on your account and usage tier, shown in the developer console. **Not verified.**

**Billing.** Typically prepaid credits or a monthly invoice with a spending limit, set in the console. **Not verified.** Set a spending limit from day one.

### Pillar 3: SOP: set up API billing safely
1. Create an xAI developer account at the official console.
2. Add a payment method or credits.
3. **Set a monthly spending limit** and an alert at 50% and 80%.
4. Create a separate API key for each project, so you can see and revoke spend per project.
5. Log tokens and cost for every request in your app (Module 10).

---

## Chapter 4.4 Estimated monthly expenses

### API: a support assistant (1,500 input + 300 output tokens per reply) **[Estimate, third-party prices]**

| Usage | Replies per day | Grok 4.7 | Grok 4.3 | Grok 4.7 with 60% of input cached |
|---|---|---|---|---|
| Light | 50 | **$7.20** | **$3.94** | **$5.17** |
| Moderate | 500 | **$72.00** | **$39.37** | **$51.75** |
| Heavy | 5,000 | **$720.00** | **$393.75** | **$517.50** |

Add $5 per 1,000 web-search calls if the assistant searches. All figures from `tools/token_cost_calculator.py`.

### Subscription: who pays what **[Third-party prices]**
| Profile | Likely plan | Monthly cost |
|---|---|---|
| Student trying Grok | Free | $0 |
| Professional using chat daily | SuperGrok | about $30 |
| Founder running 3–5 Grok Bot agents | A tier that includes Grok Bot (Premium or above in Scheme B) | about $30–$200, depending on the tier and actual limits |
| 10-person team | Grok Business | about $300 (10 × $30) |
| Product with a public chatbot | API | per usage, as in the table above |

### Pillar 4: Pitfalls
- Forgetting tool fees, retries and failed requests, which still use tokens.
- Forgetting development and testing usage: budget an extra 10–20% for it **[Estimate]**.

## Module 4 exercises

**Level 1.** Write a one-paragraph explanation, for a manager, of why a SuperGrok subscription does not pay for a website chatbot.

**Level 2.** Price three options for a 10-person sales team: chat only, Grok Bot agents, and an API-based internal tool at 200 requests a day.

**Level 3.** Build a pricing sheet for a client: API cost at light, moderate and heavy usage, tool fees, a 20% buffer, your margin, and a note listing which prices were verified on the official page.

## Knowledge check
1. Does a SuperGrok subscription include API credits?
2. According to the search summary of xAI's docs, which tiers include Grok Bot?
3. What is the reported fee for web search tool calls?
4. Why should you check the signed-in checkout price?
5. What is the cost of 500 moderate-usage replies a day on Grok 4.7, and what assumptions sit behind it?

**Answers:** (1) No, they are billed separately. (2) Premium, Super and Ultra, not Plus or Free. (3) $5 per 1,000 calls. (4) It shows your region's currency, taxes and any promotions. (5) $72 per month, assuming 1,500 input and 300 output tokens per reply, 30 days, and the unverified $2 / $6 prices.

## Sources for this module
- xAI X Subscription plans and usage (official; seen via search summary): <https://docs.x.ai/x-subscription/pricing>
- xAI models and pricing (official; not reachable): <https://docs.x.ai/docs/models>
- Cursor help, Grok Bot plans: <https://cursor.com/help/grok-bot/plans>
- eesel.ai, Grok Bot pricing: <https://www.eesel.ai/blog/grok-bot-pricing>
- Betanews, Grok Bot usage limits: <https://betanews.com/article/grok-bot-usage-limits/>
- AI Builder Club, Grok Bot pricing: <https://www.aibuilderclub.com/blog/grok-bot-pricing>
- Runtime Wire, Cursor Pro+ and free trial: <https://runtimewire.com/article/grok-bot-cursor-pro-plus-free-trial-expansion>
- AI Pricing Guru, August 2026 launch pricing: <https://www.aipricing.guru/news/xai-grok-bot-launch-pricing-impact-august-2026/>
- Let's Data Science, unified Grok and X pricing: <https://letsdatascience.com/news/spacexai-considers-unified-grok-and-x-pricing-a2810bd3>
- Build Fast with AI, SuperGrok explained: <https://www.buildfastwithai.com/blogs/supergrok-explained-pricing-limits-is-it-worth-it-2026>
- Business Today, SuperGrok Lite: <https://www.businesstoday.in/technology/story/xai-makes-grok-affordable-with-new-supergrok-lite-plan-check-price-and-what-it-offers-522462-2026-03-26>
- Suprmind, Grok pricing: <https://www.suprmind.ai/hub/grok/pricing/>
- Hi-Tech, SuperGrok Heavy $300: <https://hi-tech.ua/en/elon-musks-supergrok-heavy-ai-plan-costs-300-per-month/>
- MorphLLM, Grok API pricing: <https://www.morphllm.com/grok-api-pricing>
- BenchLM, Grok API pricing: <https://www.benchlm.ai/xai/api-pricing>
- Costbench, August 2026 price change: <https://costbench.com/changelog/xai-api-price-increase-2026-08/>
- Price Per Token, Grok 4.7: <https://pricepertoken.com/pricing-page/model/xai-grok-4.7>
