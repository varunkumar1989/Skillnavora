"""Offline tests for the course code. No network or API key needed.

Run:  python3 test_offline.py
"""
import datetime as dt
import json
import os
import sys
import threading
import time
import unittest
import urllib.request

os.environ["GROK_MOCK"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))

import grok_client  # noqa: E402
from grok_client import APIError, parse_sse_lines, with_retries  # noqa: E402
from chatbot import ChatSession  # noqa: E402
from rag_assistant import Index, chunk, answer  # noqa: E402
from agent_tools import run_agent  # noqa: E402
from usage_monitor import UsageMonitor, route  # noqa: E402
import web_chat  # noqa: E402


class ClientTests(unittest.TestCase):
    def test_sse_parsing(self):
        lines = ['data: {"choices":[{"delta":{"content":"Hel"}}]}',
                 '', ': keep-alive comment',
                 'data: {"choices":[{"delta":{"content":"lo"}}]}',
                 'data: {"choices":[],"usage":{"prompt_tokens":9,"completion_tokens":2}}',
                 'data: [DONE]', 'data: {"choices":[{"delta":{"content":"ignored"}}]}']
        pieces, usage = parse_sse_lines(lines)
        self.assertEqual("".join(pieces), "Hello")
        self.assertEqual(usage["completion_tokens"], 2)

    def test_retries_then_success(self):
        calls, waits = [], []

        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise APIError(429, "rate limited")
            return "ok"
        self.assertEqual(with_retries(flaky, sleep=waits.append), "ok")
        self.assertEqual(waits, [1.0, 2.0])

    def test_no_retry_on_auth_error(self):
        def bad():
            raise APIError(401, "bad key")
        with self.assertRaises(APIError):
            with_retries(bad, sleep=lambda s: None)

    def test_missing_key_message(self):
        os.environ.pop("XAI_API_KEY", None)
        with self.assertRaises(RuntimeError):
            grok_client._headers()

    def test_mock_chat_returns_usage(self):
        text, usage = grok_client.chat([{"role": "user", "content": "hello there"}])
        self.assertIn("hello there", text)
        self.assertGreater(usage["prompt_tokens"], 0)


class ChatbotTests(unittest.TestCase):
    def test_history_trimmed_to_budget(self):
        s = ChatSession(history_budget=120)
        for i in range(30):
            s.ask(f"Question number {i} about returns and refunds for my order")
        self.assertLessEqual(len(s.history), 12)
        self.assertEqual(s.history[-1]["role"], "assistant")
        self.assertEqual(len(s.log), 30)
        self.assertGreater(s.spent_usd, 0)

    def test_input_validation_and_budget(self):
        s = ChatSession(max_user_chars=20, monthly_budget_usd=0.0)
        self.assertIn("type a question", s.ask("   "))
        self.assertIn("too long", s.ask("x" * 50))
        self.assertIn("budget", s.ask("hi"))

    def test_api_failure_keeps_session_usable(self):
        s = ChatSession()
        original = grok_client.chat
        import chatbot
        chatbot.chat = lambda *a, **k: (_ for _ in ()).throw(APIError(500, "down"))
        try:
            self.assertIn("could not reach", s.ask("hello"))
            self.assertEqual(s.history, [])
        finally:
            chatbot.chat = original


class RagTests(unittest.TestCase):
    def setUp(self):
        policy = ("Returns are accepted within 30 days of delivery if the item is unused. "
                  "Refunds are paid within 5 to 7 working days. Sale items can be exchanged but not refunded. ")
        shipping = "Delivery takes 3 to 5 days in metro cities and up to 9 days elsewhere. " * 3
        self.idx = Index(chunk(policy, "returns") + chunk(shipping, "shipping", max_words=20, overlap=5))

    def test_chunk_overlap_and_ids(self):
        cs = chunk(" ".join(str(i) for i in range(50)), "doc", max_words=20, overlap=5)
        self.assertEqual([c["id"] for c in cs], ["doc#1", "doc#2", "doc#3"])
        self.assertEqual(cs[1]["text"].split()[0], "15")

    def test_retrieves_right_source(self):
        self.assertEqual(self.idx.search("refund sale item")[0]["source"], "returns")
        self.assertEqual(self.idx.search("how many days delivery metro")[0]["source"], "shipping")

    def test_no_match_is_honest(self):
        text, hits, _ = answer(self.idx, "quantum chromodynamics")
        self.assertEqual(hits, [])
        self.assertIn("could not find", text)


class AgentTests(unittest.TestCase):
    @staticmethod
    def scripted(*replies):
        it = iter(replies)
        return lambda messages: next(it)

    @staticmethod
    def tool_call(name, args):
        return {"role": "assistant", "content": None,
                "tool_calls": [{"id": "c1", "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}]}

    def test_lookup_then_answer(self):
        model = self.scripted(self.tool_call("get_order_status", {"order_id": "88213"}),
                              {"role": "assistant", "content": "Your order has shipped."})
        text, trace = run_agent("Where is 88213?", model=model)
        self.assertEqual(text, "Your order has shipped.")
        self.assertEqual(trace[0]["result"]["status"], "shipped")

    def test_refund_blocked_without_approval(self):
        model = self.scripted(self.tool_call("issue_refund", {"order_id": "4471", "reason": "late"}),
                              {"role": "assistant", "content": "A person will review your refund."})
        text, trace = run_agent("Refund 4471", model=model)
        self.assertIn("not approved", trace[0]["result"]["error"])

    def test_refund_runs_with_approval(self):
        model = self.scripted(self.tool_call("issue_refund", {"order_id": "4471", "reason": "late"}),
                              {"role": "assistant", "content": "Refunded."})
        _, trace = run_agent("Refund 4471", model=model, approve=lambda n, a: True)
        self.assertEqual(trace[0]["result"]["refunded"], "4471")

    def test_step_limit(self):
        loop = lambda messages: self.tool_call("get_order_status", {"order_id": "88213"})  # noqa: E731
        text, trace = run_agent("loop forever", model=loop, max_steps=3)
        self.assertIn("person", text)
        self.assertIn("step limit", trace[-1]["stopped"])


class MonitorTests(unittest.TestCase):
    def test_costs_alerts_and_report(self):
        alerts = []
        m = UsageMonitor(daily_budget_usd=0.01, alert=alerts.append)
        day = dt.datetime(2026, 11, 11, 10, 0)
        for _ in range(3):
            c = m.record("support", "grok-4.7", 1500, 300, when=day)
        self.assertAlmostEqual(c, 0.0048)
        self.assertTrue(any("100%" in a for a in alerts))
        self.assertEqual(len([a for a in alerts if "50%" in a]), 1)  # each level alerts once
        rep = m.report("2026-11-11")
        self.assertEqual(rep[0]["requests"], 3)
        self.assertTrue(m.over_budget("2026-11-11"))

    def test_tool_fee_added(self):
        m = UsageMonitor(alert=lambda s: None)
        self.assertAlmostEqual(m.record("research", "grok-4.7", 0, 0, tool_calls=10), 0.05)

    def test_routing(self):
        self.assertEqual(route("Where is my order?"), "grok-4.3")
        self.assertEqual(route("Compare these two contracts"), "grok-4.7")


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = web_chat.ThreadingHTTPServer(("127.0.0.1", 0), web_chat.Handler)
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def post(self, body):
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}/api/chat", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            r = urllib.request.urlopen(req)
            return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_page_and_chat(self):
        html = urllib.request.urlopen(f"http://127.0.0.1:{self.port}/").read().decode()
        self.assertIn("Navi support chat", html)
        self.assertNotIn("XAI_API_KEY", html)  # the key never reaches the browser
        web_chat.RATE.clear()
        status, body = self.post({"message": "Can I return shoes?"})
        self.assertEqual(status, 200)
        self.assertIn("mock answer", body["answer"])

    def test_rate_limit(self):
        web_chat.RATE.clear()
        codes = [self.post({"message": "hi"})[0] for _ in range(web_chat.MAX_PER_MINUTE + 2)]
        self.assertEqual(codes.count(429), 2)

    def test_rate_window_expires(self):
        web_chat.RATE.clear()
        now = time.time()
        for _ in range(web_chat.MAX_PER_MINUTE):
            web_chat.allowed("x", now - 61)
        self.assertTrue(web_chat.allowed("x", now))


if __name__ == "__main__":
    unittest.main(verbosity=1)
