# Capstone Projects

Each project lists: problem · requirements · architecture · stack · steps · sample code · testing · security · token estimate · monthly cost · evaluation criteria. Costs are **[Estimate]** with third-party, unverified prices, computed with `tools/token_cost_calculator.py`.

---

## Project 1 (Beginner): A simple Grok-powered support chatbot

**Problem.** A small online shop answers the same questions about returns, refunds and delivery every day.

**Requirements**
- Answers in under 80 words from the shop's policy, in the customer's language.
- Remembers the conversation within a session.
- Says "I don't know" and offers a person when unsure.
- Costs are logged; a session cannot exceed its budget.

**Architecture**
```
Customer ─► Web page (HTML) ─► Python backend (web_chat.py)
                                  ├─ ChatSession (history budget, cost log)
                                  └─ grok_client.chat ─► xAI Grok API
```

**Stack.** Python 3.10+, standard library, `code/chatbot.py`, `code/web_chat.py`, `code/grok_client.py`.

**Implementation steps**
1. Write the shop's policy (300–500 words) into `SYSTEM_PROMPT`.
2. Run `python3 test_offline.py`; all tests must pass.
3. Run `GROK_MOCK=1 python3 web_chat.py`; chat in the browser.
4. Set `XAI_API_KEY` and `GROK_MODEL`; run live; compare answers with the policy.
5. Write 20 test questions with expected answers; record pass/fail.

**Sample code.** `ChatSession.ask()` in `code/chatbot.py`; `Handler.do_POST()` in `code/web_chat.py`.

**Testing.** Offline unit tests; 20-question quality test; 5 prompt-injection attempts; 12 messages in a minute to confirm the rate limit.

**Security.** Key only on the server; HttpOnly session cookie; input length limit; per-visitor rate limit; no customer data stored beyond the session.

**Token estimate.** A 6-turn chat with a 250-token system prompt, 40-token questions and 150-token answers sends 290, 480, 670, 860, 1,050 and 1,240 input tokens: **4,590 input + 900 output tokens per chat**.

**Monthly cost.** 50 chats a day: **$11.98 on Grok 4.3**, **$21.87 on Grok 4.7**.

**Evaluation criteria**
| Criterion | Pass mark |
|---|---|
| Quality test | ≥ 18 of 20 correct |
| Refuses or hands off when the policy has no answer | 5 of 5 |
| Injection attempts resisted | 5 of 5 |
| Cost logged per request | Yes |
| Key absent from the page source | Yes |

---

## Project 2 (Intermediate): A document question-answering assistant

**Problem.** A team needs answers from 30 internal documents (HR policy, SOPs, product manuals) with sources.

**Requirements**
- Load PDF or text documents; chunk and index them.
- Answer only from the documents, citing chunk IDs; say "not found" otherwise.
- Keep conversation context for follow-up questions ("and for part-time staff?").
- Re-index when a document changes.

**Architecture**
```
Documents ─► text extraction ─► chunk() ─► Index (BM25; embeddings later)
User ─► question + last 2 turns ─► Index.search ─► top 3 chunks
     ─► grounded prompt ─► Grok API ─► answer + [doc#chunk] citations ─► UI
```

**Stack.** Python, `code/rag_assistant.py`, a PDF text extractor, optionally a vector database and an embeddings provider.

**Implementation steps**
1. Extract text from each document; store source name and date.
2. Chunk (120 words, 20 overlap) and build the index.
3. Write 20 questions with the correct source chunk; measure retrieval hit rate (target ≥ 85%).
4. Add conversation context: include the last two turns in the search query and the prompt.
5. Add the answer call; check citations on 20 answers.
6. Add a re-index command and a "last updated" date in the UI.

**Sample code.** `chunk()`, `Index.search()`, `build_prompt()` and `answer()` in `code/rag_assistant.py`.

**Testing.** Retrieval hit rate; citation accuracy (cited chunk really contains the answer); "not found" on 5 questions outside the documents; follow-up question handling.

**Security.** Documents filtered by the user's access level before retrieval; no confidential documents in the index without approval; logs redacted.

**Token estimate.** About **1,000 input tokens** per question (system 120 + three chunks of about 160 tokens + history and question) and **250 output tokens**.

**Monthly cost.** 200 questions a day on Grok 4.7: **$21.00**, or **$18.30** with 30% of input cached.

**Evaluation criteria**
| Criterion | Pass mark |
|---|---|
| Retrieval hit rate | ≥ 85% |
| Answers with a correct citation | ≥ 90% |
| Honest "not found" | 5 of 5 |
| Follow-ups resolved with context | ≥ 4 of 5 |
| Access control test (restricted document never cited for a normal user) | Pass |

---

## Project 3 (Advanced): A business automation system with token tracking and cost control

**Problem.** A services company receives 1,000 emails a day: enquiries, invoices, complaints and spam. It wants them classified, routed, summarised and, for routine cases, answered in draft, with costs kept under a budget.

**Requirements**
- Classify every email; extract fields for enquiries and invoices.
- Route simple emails to a cheaper model and complex ones to a stronger model.
- Draft replies for routine emails; a person approves before sending.
- Look up the web for company details on new enquiries (limited to 50 searches a day).
- Track tokens, tool calls and cost per feature; alert at 50/80/100% of the daily budget.
- Daily report to Slack.

**Architecture**
```
Gmail (trigger) ─► Orchestrator (n8n or Python worker)
   ├─ route() ─► Grok 4.3: classify + extract (all emails)
   ├─ complex cases ─► Grok 4.7: analysis + draft reply
   ├─ enquiries ─► web search tool (capped) ─► company summary
   ├─ CRM / accounting APIs (via tools with authorisation checks)
   ├─ approval queue (person approves drafts)
   └─ UsageMonitor ─► SQLite/PostgreSQL ─► daily report ─► Slack
```
*Grok Bot alternative:* a Grok Bot agent connected to Gmail and Slack can run the triage and summaries without code **[Third-party features]**, subject to its plan's weekly usage pool; use the API version when you need routing, metering and approvals under your control.

**Stack.** Python worker or n8n; `code/usage_monitor.py`, `code/agent_tools.py`, `code/grok_client.py`; Gmail API; Slack webhook; database.

**Implementation steps**
1. Build the classifier prompt with 8 labels and JSON output; test on 100 labelled past emails (target ≥ 90% accuracy).
2. Implement `route()` rules; measure cost and accuracy for each model on the test set.
3. Implement extraction with JSON validation and retry.
4. Add the approval queue for drafts and any tool that writes to external systems.
5. Wrap every model call with `UsageMonitor.record()`; set the daily budget; send alerts to Slack.
6. Add the daily report (`report()`), and a weekly quality review of 30 sampled emails.
7. Load test with a day's backlog; confirm the budget stops non-essential work when reached.

**Sample code.** `route()` and `UsageMonitor` in `code/usage_monitor.py`; the approval gate in `code/agent_tools.py`.

**Testing.** Classification accuracy; extraction field accuracy; approval gate (no email sent without approval); budget alerts fire once per level; failure handling (API errors retried, then queued).

**Security.** Least-privilege Gmail scopes; drafts only, no auto-send; secrets in a vault; tool authorisation; audit log of approvals; personal data retention policy.

**Token estimate.**
- Triage: 1,000 emails/day × (800 in + 120 out) on Grok 4.3, 60% of input cached.
- Escalations: 300/day × (2,500 in + 400 out) on Grok 4.7, 50% cached.
- Search: 50 calls/day.

**Monthly cost.** Triage **$23.88** + escalations **$49.73** + search **$7.50** = **$81.11**; with a 20% buffer **$97.33**.

**Evaluation criteria**
| Criterion | Pass mark |
|---|---|
| Classification accuracy | ≥ 90% on 100 emails |
| Extraction accuracy (per field) | ≥ 95% |
| Drafts sent without approval | 0 |
| Budget alerts and stop behaviour | Verified in test |
| Daily report delivered | 7 days in a row |
| Cost per processed email reported | Yes |

---

## Submission checklist (all projects)
- Repository with code, README and `.env.example` (no real keys).
- Test results (offline tests and quality test set).
- Cost sheet with the **date and source** of the prices used.
- Security notes and known limitations.
- A 5-minute demo video or written walkthrough.
