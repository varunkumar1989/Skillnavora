"""A small web chatbot: an HTML page (frontend) talking to a Python server (backend).

STATUS: tested offline by test_offline.py with GROK_MOCK=1. Live API use is untested.

Why a backend? The API key must stay on the server. If the browser called the API directly,
anyone could open the page source, copy the key and spend your money.

Run:
    GROK_MOCK=1 python3 web_chat.py      then open http://localhost:8000
"""
import json
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from chatbot import ChatSession

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Navi support chat</title><style>
body{font:16px system-ui,sans-serif;max-width:640px;margin:0 auto;padding:16px;background:#fafafa;color:#111}
#log{border:1px solid #ddd;background:#fff;border-radius:8px;padding:12px;min-height:300px;white-space:pre-wrap}
.u{color:#1e40af;margin:8px 0}.b{color:#065f46;margin:8px 0}form{display:flex;gap:8px;margin-top:12px}
input{flex:1;padding:10px;border:1px solid #ccc;border-radius:6px}button{padding:10px 16px;border:0;border-radius:6px;background:#111;color:#fff}
</style></head><body><h1>Navi support chat</h1><div id="log"></div>
<form id="f"><input id="q" maxlength="2000" autocomplete="off" placeholder="Ask about returns, refunds or delivery" required><button>Send</button></form>
<script>
const log=document.getElementById('log'),f=document.getElementById('f'),q=document.getElementById('q');
function add(cls,t){const d=document.createElement('div');d.className=cls;d.textContent=t;log.appendChild(d);log.scrollTop=log.scrollHeight}
f.onsubmit=async e=>{e.preventDefault();const text=q.value;q.value='';add('u','You: '+text);
 try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
  const j=await r.json();add('b','Navi: '+(j.answer||j.error))}catch(err){add('b','Navi: connection problem, please retry.')}};
</script></body></html>"""

SESSIONS = {}          # session id -> ChatSession (in memory; use a database in production)
RATE = {}              # client address -> list of request times
MAX_PER_MINUTE = 10


def allowed(client, now=None):
    """Simple per-visitor rate limit: at most MAX_PER_MINUTE requests in 60 seconds."""
    now = now or time.time()
    times = [t for t in RATE.get(client, []) if now - t < 60]
    if len(times) >= MAX_PER_MINUTE:
        RATE[client] = times
        return False
    RATE[client] = times + [now]
    return True


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json", cookie=None):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        if cookie:
            self.send_header("Set-Cookie", f"sid={cookie}; HttpOnly; SameSite=Strict; Path=/")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/chat":
            return self._send(404, json.dumps({"error": "not found"}))
        if not allowed(self.client_address[0]):
            return self._send(429, json.dumps({"error": "Too many messages. Please wait a minute."}))
        length = int(self.headers.get("Content-Length", 0))
        if length > 10_000:
            return self._send(413, json.dumps({"error": "Message too large."}))
        try:
            message = json.loads(self.rfile.read(length) or b"{}").get("message", "")
        except json.JSONDecodeError:
            return self._send(400, json.dumps({"error": "Invalid request."}))
        cookies = dict(c.strip().split("=", 1) for c in self.headers.get("Cookie", "").split(";") if "=" in c)
        sid = cookies.get("sid")
        new_cookie = None
        if sid not in SESSIONS:
            sid = new_cookie = uuid.uuid4().hex
            SESSIONS[sid] = ChatSession(monthly_budget_usd=1.0)
        answer = SESSIONS[sid].ask(message)
        self._send(200, json.dumps({"answer": answer}), cookie=new_cookie)

    def log_message(self, fmt, *args):  # keep the console quiet; log usage elsewhere
        pass


def serve(port=8000):
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    print("Open http://localhost:8000")
    serve()
