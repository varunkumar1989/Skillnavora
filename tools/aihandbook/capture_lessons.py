"""Run the starter project's lesson examples offline and save their real outputs to
lesson_outputs.json, which the lesson pages and the handbook show.
Run with a Python that has the starter requirements installed:
    python tools/aihandbook/capture_lessons.py"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "starter", "ai-master-course-starter")
ENV = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

L5 = r'''
import json, sys
sys.path.insert(0, ".")
from fastapi.testclient import TestClient
from api.main import app
c = TestClient(app)
print("GET /health ->", json.dumps(c.get("/health").json()))
r = c.post("/ask", json={"question": "How long must laptop passwords be?"})
d = r.json()
print("POST /ask ->", r.status_code, json.dumps({"answer": d["answer"], "sources": d["sources"][:1], "refused": d["refused"]}))
r = c.post("/ask", json={"question": "x"})
print("POST /ask (too short) ->", r.status_code, r.json()["detail"][0]["msg"])
r = c.post("/upload", files={"file": ("notes.txt", b"hello", "text/plain")})
print("POST /upload notes.txt ->", r.status_code, r.json()["detail"])
'''

out = {}
for key, cmd in [("l1", ["examples/l1_chunking.py"]), ("l2", ["examples/l2_guardrails.py"]), ("l3", ["examples/l3_latency_cost.py"]),
                 ("l4", ["examples/l4_llmops.py"]), ("l6", ["examples/l6_pdf_chatbot.py"]), ("l5", ["-c", L5]),
                 ("w1", ["examples/w1_first_call.py"]), ("w3", ["examples/w3_agent_tools.py"]), ("evals", ["evals/run_evals.py"])]:
    r = subprocess.run([sys.executable] + cmd, cwd=PROJ, env=ENV, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        sys.exit(f"{key} failed:\n{r.stderr}")
    out[key] = r.stdout.rstrip()
    print(f"captured {key}: {len(out[key].splitlines())} lines")
subprocess.run(["rm", "-rf", os.path.join(PROJ, "logs")])
json.dump(out, open(os.path.join(HERE, "lesson_outputs.json"), "w"), indent=1, ensure_ascii=False)
