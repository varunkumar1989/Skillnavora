# Module 7: Building AI Chatbots and Automation

**Level:** Intermediate · **Time:** about 4 hours · **Code:** `code/chatbot.py`, `code/web_chat.py`

> Code status: tested offline in mock mode (`code/test_offline.py`). The live API call is untested; see Module 6.

---

## Chapter 7.1 Creating a basic chatbot

### Pillar 1: Core objective
Build a terminal chatbot that remembers the conversation, stays within a token budget and tracks its cost.

### Pillar 2: Key concepts
A chatbot = **system prompt** + **message history** + **a loop** that sends history to the model and appends each answer.

```
loop:
  read user message ─► validate ─► add to history ─► trim history to budget
  ─► send [system + history] ─► receive answer + usage ─► add answer to history
  ─► log tokens and cost ─► show answer
```

### Pillar 3: SOP
1. Open `code/chatbot.py`. Read `SYSTEM_PROMPT`, `ChatSession.ask()` and `_trim()`.
2. Run offline: `GROK_MOCK=1 python3 chatbot.py`. Type questions, then `cost`.
3. Change `history_budget` to 200 and ask ten questions; notice older turns are dropped.
4. Run live with your key and model ID.
5. **Expected output:** short answers within 80 words; `cost` shows requests and dollars spent.
6. **Test:** `python3 test_offline.py` (checks trimming, validation, budget and failure handling).

### Pillar 4: Pitfalls
- No input validation: a user pastes a 50-page document and your bill jumps. `max_user_chars` blocks this.
- No error handling: one network error crashes the bot. `ask()` catches errors and keeps the session usable.

---

## Chapter 7.2 Connecting a frontend to an AI backend

### Pillar 2: Key concepts
- **Frontend:** what the user sees (HTML page, app).
- **Backend:** your server, which holds the API key and calls the model.
- The browser **never** calls the AI API directly, because the key would be exposed.

```
Browser (HTML + JS) ──POST /api/chat {message}──► Your server (Python)
                                                  ├─ rate limit per visitor
                                                  ├─ session (cookie) → ChatSession
                                                  └─ calls Grok API with the secret key
Browser ◄──────────── {answer} ───────────────────┘
```

### Pillar 3: SOP
1. Run `GROK_MOCK=1 python3 web_chat.py` and open <http://localhost:8000>.
2. Send messages; each browser gets its own session through an `HttpOnly` cookie.
3. Send more than 10 messages in a minute: you get "Too many messages" (HTTP 429).
4. View the page source: the API key is not there (a test checks this).

---

## Chapter 7.3 Managing conversation history and context

| Strategy | How | Good for | Risk |
|---|---|---|---|
| Keep last k turns | Drop oldest pairs | Short support chats | Forgets early facts |
| Token budget | Drop until under N tokens (used in `ChatSession`) | Predictable cost | Same as above |
| Summarise | Replace old turns with a summary written by the model | Long sessions | Summary loses details; costs a call |
| Facts block | Keep key facts (name, order ID) in a separate pinned message | Support and sales | Must be updated correctly |
| Retrieval | Store old turns, retrieve relevant ones | Very long histories | More engineering |

Cost effect: Module 3, example 3 shows why history policy matters.

---

## Chapter 7.4 Integrating external APIs

A chatbot becomes useful when it can look things up: order status, stock, appointments. Two approaches:
1. **Fixed integration:** your code always calls the order API when it detects an order number, and puts the result into the prompt. Simple and predictable.
2. **Tool calling:** the model decides when to call a tool (Module 8, `code/agent_tools.py`).

Start with the fixed approach; move to tool calling when there are many possible actions.

---

## Chapter 7.5 Handling user input and errors

| Input problem | Handling |
|---|---|
| Empty message | Ask for a question (no API call) |
| Very long message | Reject or truncate with a message |
| Abuse or off-topic | System prompt rules plus a polite refusal |
| Personal data (card numbers) | Mask with a pattern before sending; tell users not to share it |
| Prompt injection ("ignore your instructions") | See Module 10; never give the bot powers it should not have |

---

## Chapter 7.6 Managing token usage and controlling expenses

1. Short system prompt; `max_tokens` on every call.
2. History budget per session.
3. **Budget per session** (`monthly_budget_usd` in `ChatSession`) and per day for the whole app (`code/usage_monitor.py`).
4. Route simple questions to a cheaper model (`route()` in `usage_monitor.py`).
5. Cache common answers (FAQ) without calling the model.
6. Log tokens and cost for every request.

**Example [Estimate]:** a support bot answering 600 questions a day, 2,500 input and 300 output tokens each, costs about **$69.75 a month on Grok 4.3, or $41.40 with 60% of input cached** (third-party prices; Module 9 case 1).

---

## Chapter 7.7 Deploying a chatbot

### Pillar 3: SOP
1. Choose hosting: a small cloud server or a platform that runs Python web apps.
2. Set `XAI_API_KEY` and `GROK_MODEL` in the host's secret settings.
3. Serve over **HTTPS** only.
4. Replace in-memory sessions with a database or cache (Redis, PostgreSQL) so restarts do not lose chats and several servers can share them.
5. Use a production web server (for example gunicorn or uvicorn behind a proxy) instead of Python's built-in `http.server`, which is for learning only.
6. Add monitoring (Chapter 7.8) before launch.

### Pillar 4: Pitfalls
- Deploying `web_chat.py` unchanged to the internet: its sessions and rate limits are in memory and per process.
- No spending limit on the API account.

---

## Chapter 7.8 Testing and monitoring

**Before launch**
- A test set of 30 real questions with expected answers; target pass rate agreed with the business.
- Red-team test: 10 attempts to break rules or extract the system prompt.
- Load test: expected peak messages per minute.

**After launch**
- Daily: requests, errors, cost, average tokens.
- Weekly: read 20 random conversations; score quality.
- Alerts: cost at 50/80/100% of budget; error rate above 5%.

## Module 7 exercises

**Level 1.** Change the system prompt in `chatbot.py` for a different business, run it offline, and test five questions.

**Level 2.** Add a "facts block" to `ChatSession` that keeps the customer's name and order ID even when history is trimmed. Add a test.

**Level 3.** Deploy `web_chat.py` behind HTTPS with a real session store, and add a daily cost dashboard from `usage_monitor.py`.

## Knowledge check
1. Why must the backend, not the browser, call the AI API?
2. Name three history strategies.
3. What does a per-session budget protect against?
4. Why is the built-in `http.server` not suitable for production?
5. What should you monitor daily?

**Answers:** (1) To keep the key secret. (2) Last k turns, token budget, summarisation (also facts block, retrieval). (3) One user or a bug running up a large bill. (4) It is single-purpose for learning, lacks production hardening, and keeps state per process. (5) Requests, errors, cost and average tokens.
