# Module 6: API Integration and Development Fundamentals

**Level:** Beginner to intermediate · **Time:** about 4 hours · **Code:** `code/grok_client.py`, `code/chat.mjs`, `code/curl_examples.sh`

> **Code status.** The examples follow the **OpenAI-compatible chat completions format**, which xAI's API has supported **[General, from xAI documentation before 2026; re-check]**. The assumed base URL is `https://api.x.ai/v1`. The offline logic is tested (`code/test_offline.py`, 21 tests passing). **The live calls are untested**, because no API key or network access to xAI was available. Before running, confirm the base URL, endpoint paths, model IDs and response fields on <https://docs.x.ai>. xAI also publishes its own SDK; check the docs for its current package name and usage.

---

## Chapter 6.1 What an API is

### Pillar 1: Core objective
Explain APIs, endpoints and keys to a non-programmer, then make your first call.

### Pillar 2: Key concepts

**Topic 6.1.1 API.** An **Application Programming Interface** is an agreed way for one program to ask another for something. You send a **request**; you get a **response**.

> **Analogy.** A restaurant menu (the API documentation) lists what you can order and how. The waiter (HTTP) carries your order (request) to the kitchen (the Grok model) and brings back your dish (response). Your loyalty card (API key) proves who pays.

**Topic 6.1.2 Endpoint.** A specific web address for one kind of request, for example `https://api.x.ai/v1/chat/completions` for chat answers **[assumed; verify]**.

**Topic 6.1.3 API key.** A long secret string that identifies your account. Anyone who has it can spend your money. Treat it like a bank PIN.

**Topic 6.1.4 Authentication.** Proving who you are on every request, here by sending the key in a header: `Authorization: Bearer <your key>`.

---

## Chapter 6.2 HTTP requests and responses

### Pillar 2: Key concepts

| Part | Meaning | Example |
|---|---|---|
| Method | What you want to do | `GET` read something; `POST` send data to create a result |
| URL | Where | `https://api.x.ai/v1/chat/completions` |
| Headers | Labels on the envelope | `Authorization`, `Content-Type: application/json` |
| Body (payload) | The content, in JSON | `{"model": "...", "messages": [...]}` |
| Status code | How it went | `200` OK, `400` bad request, `401` bad key, `429` too many requests, `500` server error |

**GET versus POST.** Listing available models is a `GET` (no body). Asking for a chat answer is a `POST` (the body carries your messages).

### Pillar 3: A request and its response
**Request body**
```json
{
  "model": "grok-4.7",
  "max_tokens": 150,
  "messages": [
    {"role": "system", "content": "Answer in one sentence."},
    {"role": "user", "content": "What is an API key?"}
  ]
}
```
**Response body (shape; values illustrative)**
```json
{
  "id": "resp_123",
  "model": "grok-4.7",
  "choices": [{"index": 0, "message": {"role": "assistant", "content": "An API key is a secret code that identifies you to a service."}, "finish_reason": "stop"}],
  "usage": {"prompt_tokens": 27, "completion_tokens": 14, "total_tokens": 41}
}
```
`finish_reason` tells you why the answer stopped: `stop` (complete) or `length` (hit `max_tokens`, so the answer may be cut off).

---

## Chapter 6.3 JSON fundamentals

| JSON type | Example |
|---|---|
| Object | `{"name": "Asha", "age": 29}` |
| Array | `["red", "green"]` |
| String | `"hello"` (double quotes only) |
| Number | `42`, `3.5` |
| Boolean | `true`, `false` |
| Null | `null` |

Common errors: single quotes, trailing commas, unescaped quotes inside strings. Always build JSON with a library (`json.dumps` in Python, `JSON.stringify` in JavaScript), never by joining strings.

---

## Chapter 6.4 Setting up your development environment

### Pillar 3: SOP
1. Install **VS Code** (code editor) and **Python 3.10+**. Optional: **Node.js 18+**.
2. Create an xAI developer account and an API key in the official console.
3. Set a spending limit in the console (Module 4).
4. Store the key in an **environment variable** (Chapter 6.6), not in code.
5. Download this course's `code/` folder and run the offline tests:
   ```bash
   cd code
   python3 test_offline.py        # 21 tests, no key needed
   GROK_MOCK=1 python3 chatbot.py # practice with canned answers
   ```
6. Then run a live call:
   ```bash
   export XAI_API_KEY="your key"         # Windows PowerShell: $env:XAI_API_KEY="your key"
   export GROK_MODEL="model id from docs.x.ai"
   python3 grok_client.py
   ```
**Expected output:** a one-sentence answer and a `usage` line with token counts.

---

## Chapter 6.5 Making calls in Python, Node.js and cURL

**Python** (`code/grok_client.py`, standard library only)
```python
from grok_client import chat
answer, usage = chat([
    {"role": "system", "content": "Answer in one sentence."},
    {"role": "user", "content": "What is a context window?"},
], max_tokens=150)
print(answer, usage)
```

**Python with the OpenAI SDK** (works with OpenAI-compatible APIs; **untested** with xAI)
```python
import os
from openai import OpenAI
client = OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")
r = client.chat.completions.create(model=os.environ["GROK_MODEL"], max_tokens=150,
        messages=[{"role": "user", "content": "What is a token?"}])
print(r.choices[0].message.content, r.usage)
```

**Node.js**: see `code/chat.mjs` (normal and streamed requests).

**cURL**: see `code/curl_examples.sh` (chat, streaming, list models).

---

## Chapter 6.6 Environment variables and secure key management

### Pillar 2: Key concepts
An **environment variable** is a named value set outside your code, read at run time: `os.environ["XAI_API_KEY"]`. It keeps secrets out of files you might share.

### Pillar 3: SOP
1. Local: put `XAI_API_KEY=...` in a `.env` file and add `.env` to `.gitignore`. Load it with a library such as `python-dotenv`, or export it in your shell.
2. Server: use the hosting platform's secret settings (for example, environment variables in the dashboard).
3. One key per project and environment (development, production).
4. Rotate keys every few months and immediately if exposed.
5. Never put a key in browser JavaScript, mobile app code, screenshots or chat messages.

### Pillar 4: Pitfalls
- Committing a key to GitHub: automated scanners find exposed keys within minutes. Revoke it at once.
- Logging full request headers: logs then contain your key.

---

## Chapter 6.7 Rate limits, errors and retries

| Status | Meaning | What to do |
|---|---|---|
| 400 | Bad request (invalid JSON, wrong field) | Fix the request; do not retry |
| 401 / 403 | Missing, wrong or unauthorised key | Check the key; do not retry |
| 404 | Wrong URL or model ID | Check the endpoint and model name |
| 413 / context error | Request too large | Shorten input or history |
| 429 | Rate limit or quota exceeded | Wait and retry with **exponential backoff** (1 s, 2 s, 4 s…) |
| 500–504 | Server problem | Retry with backoff; show a friendly message |

`with_retries()` in `grok_client.py` implements backoff and is tested to retry on 429 but not on 401.

---

## Chapter 6.8 Parsing responses and streaming

- Read the answer from `choices[0].message.content`.
- Check `finish_reason`; if it is `length`, the answer was cut off.
- Read and log `usage` for cost tracking.
- **Streaming:** set `"stream": true`. The response arrives as server-sent events: lines `data: {json chunk}` ending with `data: [DONE]`. Each chunk carries a small piece of text in `choices[0].delta.content`. `parse_sse_lines()` in `grok_client.py` is tested on a sample stream.

### Pillar 4: Pitfalls
- Assuming the response always has text: tool calls may return `content: null` (Module 8).
- Not setting a timeout: a stuck request can hang your app.

## Module 6 exercises

**Level 1.** Run `python3 test_offline.py` and `GROK_MOCK=1 python3 chatbot.py`. Explain what each test checks.

**Level 2.** With a live key, call the API from Python and cURL with the same prompt. Compare the `usage` numbers and compute the cost with the calculator.

**Level 3.** Add a timeout setting, a request ID and structured logging (time, model, tokens, cost, status) to `grok_client.py`, with tests.

## Knowledge check
1. What is the difference between an endpoint and an API key?
2. Which HTTP method sends a chat request?
3. Which status codes should be retried?
4. Why must the key never be in browser code?
5. What does `finish_reason: "length"` mean?

**Answers:** (1) An endpoint is the address; the key proves who you are and who pays. (2) POST. (3) 429 and 5xx, with backoff. (4) Anyone can read it and spend your money. (5) The answer hit the `max_tokens` limit and may be incomplete.
