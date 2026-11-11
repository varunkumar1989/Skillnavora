"""Minimal client for an OpenAI-compatible chat completions API such as xAI's Grok API.

STATUS: the offline logic (retries, stream parsing, usage) is tested by test_offline.py.
The live call is UNTESTED: no xAI API key or network access to xAI was available when this
course was written. Before use, confirm on https://docs.x.ai:
  - the base URL (assumed https://api.x.ai/v1)
  - the endpoint path (assumed /chat/completions)
  - the exact model ID (set GROK_MODEL; "grok-4.7" below is a placeholder)
  - the names of the usage fields in the response

Uses only the Python standard library.

Environment variables:
  XAI_API_KEY   your secret key (never hard-code it)
  XAI_BASE_URL  optional, default https://api.x.ai/v1
  GROK_MODEL    optional, default grok-4.7 (placeholder; check the models page)
  GROK_MOCK=1   offline mode: no network, canned answers, for learning and tests
"""
import json
import os
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
MODEL = os.environ.get("GROK_MODEL", "grok-4.7")
RETRY_STATUS = {429, 500, 502, 503, 504}


class APIError(Exception):
    def __init__(self, status, body):
        super().__init__(f"HTTP {status}: {body[:300]}")
        self.status, self.body = status, body


def _headers():
    key = os.environ.get("XAI_API_KEY")
    if not key:
        raise RuntimeError("Set the XAI_API_KEY environment variable (see Module 6, chapter 6.6).")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _post(path, payload, stream=False, timeout=60):
    req = urllib.request.Request(BASE_URL + path, data=json.dumps(payload).encode(),
                                 headers=_headers(), method="POST")
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        raise APIError(e.code, e.read().decode("utf-8", "replace"))


def with_retries(fn, attempts=4, base_delay=1.0, sleep=time.sleep):
    """Call fn(); on rate-limit or server errors wait 1s, 2s, 4s ... and try again."""
    for i in range(attempts):
        try:
            return fn()
        except APIError as e:
            if e.status not in RETRY_STATUS or i == attempts - 1:
                raise
            sleep(base_delay * (2 ** i))


def parse_sse_lines(lines):
    """Turn server-sent-event lines into (text_pieces, usage).

    Each data line holds a JSON chunk; the stream ends with 'data: [DONE]'.
    Usage, when sent, usually arrives in the last chunk.
    """
    pieces, usage = [], None
    for raw in lines:
        line = raw.decode() if isinstance(raw, bytes) else raw
        line = line.strip()
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        chunk = json.loads(data)
        for choice in chunk.get("choices", []):
            delta = choice.get("delta", {}).get("content")
            if delta:
                pieces.append(delta)
        if chunk.get("usage"):
            usage = chunk["usage"]
    return pieces, usage


def _mock_reply(messages, max_tokens):
    last = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    text = f"(mock answer) You asked: {last[:80]}"
    prompt_tokens = sum(len(m["content"].split()) for m in messages) * 4 // 3 + 4 * len(messages)
    completion = min(max_tokens or 200, len(text.split()) * 4 // 3 + 1)
    return text, {"prompt_tokens": prompt_tokens, "completion_tokens": completion,
                  "total_tokens": prompt_tokens + completion}


def chat(messages, model=None, max_tokens=400, temperature=0.3, stream=False, on_token=None):
    """Send a chat request. Returns (answer_text, usage_dict)."""
    if os.environ.get("GROK_MOCK") == "1":
        text, usage = _mock_reply(messages, max_tokens)
        if on_token:
            for w in text.split(" "):
                on_token(w + " ")
        return text, usage

    payload = {"model": model or MODEL, "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature}
    if stream:
        payload["stream"] = True
        # Many OpenAI-compatible APIs send usage at the end of a stream only when asked.
        payload["stream_options"] = {"include_usage": True}

        def go():
            resp = _post("/chat/completions", payload, stream=True)
            pieces = []
            usage = None
            for raw in resp:
                p, u = parse_sse_lines([raw])
                for piece in p:
                    pieces.append(piece)
                    if on_token:
                        on_token(piece)
                usage = u or usage
            return "".join(pieces), usage or {}
        return with_retries(go)

    def go():
        body = json.loads(_post("/chat/completions", payload).read())
        return body["choices"][0]["message"]["content"], body.get("usage", {})
    return with_retries(go)


if __name__ == "__main__":
    answer, usage = chat([
        {"role": "system", "content": "You are a concise assistant. Answer in one sentence."},
        {"role": "user", "content": "What is a token in a language model?"},
    ])
    print(answer)
    print("usage:", usage)
