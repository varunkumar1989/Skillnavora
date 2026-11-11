# Module 9: Business Applications and Commercial Deployment

**Level:** Intermediate to advanced · **Time:** about 3 hours

> **All financial figures in this module are illustrative.** Token volumes are assumptions; prices are third-party and unverified (Module 4). Costs were computed with `tools/token_cost_calculator.py` over 30 days. "Business value" lines describe the kind of benefit to measure, **not** results achieved by any real company.

## How to read each case
Every case lists: business problem · AI solution · tools and integrations · workflow · token estimate · API cost · value to measure · limits and risks. Grok Bot suits cases where a no-code agent working inside existing apps is enough; the API suits cases built into your own product.

---

## 9.1 Customer support automation
- **Problem:** 600 repetitive questions a day (returns, delivery, refunds) delay replies.
- **Solution:** a RAG support bot answering from the policy, handing off to a person when unsure.
- **Tools:** Grok API, help-desk integration (Zendesk, Freshdesk), RAG index, `chatbot.py` patterns.
- **Workflow:** message → retrieve policy → answer with citation → confidence check → reply or hand off → log.
- **Tokens:** 2,500 input + 300 output per reply; 45M input and 5.4M output tokens a month.
- **API cost [Estimate]:** Grok 4.3 **$69.75/month**; **$41.40** with 60% of input cached.
- **Value to measure:** share of tickets resolved without a person, first-response time, customer satisfaction.
- **Risks:** wrong policy answers; customers sharing personal data; must offer an easy route to a human.

## 9.2 Lead generation and qualification
- **Problem:** sales reps spend hours reading website enquiries.
- **Solution:** classify and score each enquiry, extract fields to the CRM, draft a first reply.
- **Tools:** Grok API or a Grok Bot agent watching an inbox; CRM (HubSpot, Zoho); form webhook.
- **Workflow:** form submitted → extract JSON (name, budget, need, timeline) → score → CRM → draft email for rep approval.
- **Tokens:** 100 leads/day × (1,200 in + 250 out).
- **API cost [Estimate]:** Grok 4.3 **$6.37/month**; **$4.48** with caching.
- **Value to measure:** time to first contact; conversion of high-score leads.
- **Risks:** biased scoring; automated emails sent without review; consent and data-protection rules for contacting leads.

## 9.3 Real estate automation
- **Problem:** agents write listing descriptions and answer the same buyer questions.
- **Solution:** generate listings from structured property data; an enquiry assistant that answers from listing facts and books visits.
- **Tools:** Grok API, property database, calendar booking, WhatsApp Business API.
- **Workflow:** property record → description draft → agent edits → publish; enquiry → answer from facts → offer slots.
- **Tokens:** 15 listings/day × (900 in + 600 out).
- **API cost [Estimate]:** Grok 4.7 **$2.43/month** for listings.
- **Value to measure:** time per listing; enquiry response time; visits booked.
- **Risks:** invented features (a "sea view" that does not exist) create legal exposure; a human must approve every listing.

## 9.4 E-commerce
- **Problem:** thousands of product pages need descriptions, FAQs and translations.
- **Solution:** batch generation from product attributes, with a style guide and checks.
- **Tools:** Grok API, product catalogue export, spreadsheet or PIM system.
- **Workflow:** attributes → description + 3 FAQs (JSON) → validation (length, banned claims) → review sample → publish.
- **Tokens:** 200 products/day × (700 in + 350 out).
- **API cost [Estimate]:** Grok 4.3 **$10.50/month**; **$8.29** with caching.
- **Value to measure:** pages published per week; search traffic and conversion on updated pages.
- **Risks:** duplicate-sounding copy; wrong specifications; regulated claims (health, safety).

## 9.5 Sales and marketing
- **Problem:** personalised outreach and campaign copy take too long.
- **Solution:** draft emails and posts from account notes and campaign briefs; the marketer edits and approves.
- **Tools:** Grok API or Grok Bot with Gmail; CRM; brand guide in the system prompt.
- **Workflow:** brief + account notes → 2 drafts → human edit → send via the email platform.
- **Tokens:** 80 drafts/day × (1,500 in + 500 out).
- **API cost [Estimate]:** Grok 4.7 **$14.40/month**; **$12.24** with caching.
- **Value to measure:** drafts per hour; reply rates compared with a control group.
- **Risks:** spam and email-marketing law; tone errors; never auto-send at scale without review.

## 9.6 Data analysis
- **Problem:** managers wait days for simple data questions.
- **Solution:** natural-language questions turned into SQL against a read-only reporting database, with the query shown for checking.
- **Tools:** Grok API with tool calling; read-only database user; schema description in the prompt.
- **Workflow:** question → generate SQL → validate (SELECT only, row limit) → run → summarise result → show SQL and numbers.
- **Tokens:** 60 questions/day × (4,000 in, mostly schema + 600 out).
- **API cost [Estimate]:** Grok 4.7 **$20.88/month**; **$13.32** with 70% cached (the schema is a stable prefix).
- **Value to measure:** questions answered without an analyst; accuracy on a test set of 30 known questions.
- **Risks:** wrong joins give plausible but wrong numbers; access to sensitive data; always show the query.

## 9.7 Internal knowledge assistant
- **Problem:** staff cannot find policies, SOPs and past decisions.
- **Solution:** a RAG assistant over the company handbook, with citations and access control.
- **Tools:** Grok API, document store, index (`rag_assistant.py` to start, a vector database later), single sign-on.
- **Workflow:** question → retrieve permitted documents only → answer with citations → feedback button.
- **Tokens:** 300 questions/day × (3,500 in + 400 out).
- **API cost [Estimate]:** Grok 4.7 **$84.60/month**; **$65.70** with caching.
- **Value to measure:** time to find answers; HR and IT ticket volume.
- **Risks:** leaking documents to people who should not see them; outdated documents.

## 9.8 Document processing
- **Problem:** invoices and forms are typed in by hand.
- **Solution:** extract fields to JSON, validate totals, flag exceptions for a person.
- **Tools:** OCR or PDF text extraction, Grok API, accounting system API.
- **Workflow:** document → text → JSON fields → checks (totals add up, GST number format) → post or flag.
- **Tokens:** 400 documents/day × (2,000 in + 250 out).
- **API cost [Estimate]:** Grok 4.3 **$37.50/month**; **$29.94** with caching.
- **Value to measure:** documents per hour; error rate compared with manual entry.
- **Risks:** misread numbers; never post payments without validation rules and sampling.

## 9.9 Workflow automation (email triage)
- **Problem:** a shared inbox receives 1,000 emails a day.
- **Solution:** classify, route, and draft replies for routine mail; a Grok Bot agent or an n8n workflow with the API.
- **Tools:** Grok Bot with Gmail and Slack **[Third-party features]**, or n8n + Grok API.
- **Workflow:** new email → classify (8 labels) → route to team → draft reply for routine ones → daily Slack summary.
- **Tokens:** 1,000 emails/day × (800 in + 120 out).
- **API cost [Estimate]:** Grok 4.3 **$39.00/month**; **$23.88** with caching. With Grok Bot, cost is instead the plan fee, subject to its weekly usage pool.
- **Value to measure:** time to route; emails handled per person.
- **Risks:** misrouted urgent emails; keep a "needs a person" label and daily review.

## 9.10 AI-powered SaaS product
- **Problem:** a SaaS company wants an AI writing feature for 1,000 active users.
- **Solution:** an in-app assistant with usage quotas per plan, built on the API.
- **Tools:** Grok API, the product's backend, `usage_monitor.py`-style metering, billing system.
- **Workflow:** user request → quota check → route model → generate → meter tokens → bill or deduct quota.
- **Tokens:** 1,000 users × 5 requests/day × (1,200 in + 500 out).
- **API cost [Estimate]:** Grok 4.7 **$810/month**; **$675** with caching; about **$0.68–$0.81 per user per month**.
- **Pricing check:** if the feature is sold at ₹499 (about $6) per user per month, AI cost would be roughly 11–14% of that price, before hosting, support and taxes **[Estimate; exchange rate assumed]**.
- **Value to measure:** feature adoption, retention of users who use it, gross margin per user.
- **Risks:** heavy users wreck margins without quotas; provider price changes; dependency on one provider.

---

## 9.11 From case to commercial offer

1. **Discovery:** process, volume, current cost in staff hours.
2. **Pilot:** 2–4 weeks, one process, a test set, a success metric agreed in writing.
3. **Costing:** the calculator with verified prices + 20% buffer + hosting + monitoring + your time.
4. **Proposal:** scope, what is automated and what stays human, risks, monthly running cost, support.
5. **Launch and review:** monthly report of usage, cost, quality and incidents.

## Module 9 exercises

**Level 1.** Pick one case and rewrite it for your own industry.

**Level 2.** Re-run the cost for case 7 with your own volumes using `monthly()`, at two models.

**Level 3.** Write a one-page commercial proposal for case 1 or 8: scope, pilot plan, metrics, monthly cost with buffer, risks and human checks.

## Knowledge check
1. Why are these figures illustrative?
2. Which two cases benefit most from caching, and why?
3. In which cases must every output be approved by a person?
4. What protects a SaaS margin from heavy users?

**Answers:** (1) Volumes are assumptions and prices are unverified. (2) Data analysis and support: large stable prefixes (schema, policy). (3) Real estate listings, outbound sales emails, financial postings (any external or financial action). (4) Per-plan quotas and metering.
