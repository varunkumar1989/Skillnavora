"""Week 1: your first model call. Offline it uses the stand-in; with ANTHROPIC_API_KEY set it calls Claude.
Run: python examples/w1_first_call.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starter.config import settings
from starter.costs import request_cost
from starter.llm import chat

SYSTEM = "You are a concise assistant for new employees. Answer in at most two sentences."
SOURCES = "SOURCES:\n[S1] Employees get 20 days of paid leave each calendar year. Unused leave can be carried forward up to 5 days.\n\n"

print("Mode:", "offline stand-in (no key set)" if settings.offline else f"Claude ({settings.model})")
reply = chat(SYSTEM, SOURCES + "QUESTION: How many paid leave days can I carry forward?")
print("Answer:  ", reply.text)
print("Tokens:  ", reply.input_tokens, "in /", reply.output_tokens, "out", "(estimated)" if reply.offline else "")
print(f"Latency:  {reply.latency_s * 1000:.0f} ms")
print(f"Cost:     ${request_cost(reply.input_tokens, reply.output_tokens):.6f}")
