"""A tool-calling agent loop with a step limit and human approval for risky actions.

STATUS: the loop, approval gate and step limit are tested offline by test_offline.py using a
scripted fake model. The live call (call_model) follows the OpenAI-compatible "tools" format and
is UNTESTED against xAI's API; confirm the request and response shape on https://docs.x.ai.

How tool calling works:
1. You describe tools (name, purpose, JSON parameters) in the request.
2. The model replies either with text (done) or with tool_calls (name + JSON arguments).
3. Your code runs the tool, adds the result as a "tool" message, and asks the model again.
4. Repeat until the model answers or the step limit is reached.
"""
import json

from grok_client import _post, with_retries, MODEL

ORDERS = {"88213": {"status": "shipped", "amount": 2499}, "4471": {"status": "delivered", "amount": 899}}

TOOLS = [
    {"type": "function", "function": {
        "name": "get_order_status", "description": "Look up the status of an order by its id.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "issue_refund", "description": "Refund an order. Needs human approval.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}},
                       "required": ["order_id", "reason"]}}},
]
RISKY = {"issue_refund"}


def get_order_status(order_id):
    o = ORDERS.get(order_id)
    return {"order_id": order_id, "status": o["status"]} if o else {"error": "order not found"}


def issue_refund(order_id, reason):
    o = ORDERS.get(order_id)
    return {"refunded": order_id, "amount": o["amount"], "reason": reason} if o else {"error": "order not found"}


IMPLEMENTATIONS = {"get_order_status": get_order_status, "issue_refund": issue_refund}


def call_model(messages):
    """One request with tools. Returns the assistant message dict (may contain tool_calls)."""
    payload = {"model": MODEL, "messages": messages, "tools": TOOLS, "tool_choice": "auto", "max_tokens": 400}
    return with_retries(lambda: json.loads(_post("/chat/completions", payload).read())["choices"][0]["message"])


def run_agent(task, model=call_model, approve=lambda name, args: False, max_steps=5):
    """Run the loop. `approve(name, args)` must return True before any risky tool runs."""
    messages = [{"role": "system", "content": "You are a support agent. Use tools to check facts. "
                                              "Never claim an action happened unless a tool confirmed it."},
                {"role": "user", "content": task}]
    trace = []
    for step in range(max_steps):
        msg = model(messages)
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        if not calls:
            trace.append({"step": step, "final": msg.get("content", "")})
            return msg.get("content", ""), trace
        for call in calls:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            if name not in IMPLEMENTATIONS:
                result = {"error": f"unknown tool {name}"}
            elif name in RISKY and not approve(name, args):
                result = {"error": "not approved by a human; tell the customer a person will review it"}
            else:
                result = IMPLEMENTATIONS[name](**args)
            trace.append({"step": step, "tool": name, "args": args, "result": result})
            messages.append({"role": "tool", "tool_call_id": call.get("id", name), "content": json.dumps(result)})
    trace.append({"stopped": f"step limit {max_steps} reached"})
    return "I need a person to look at this. A team member will follow up.", trace


if __name__ == "__main__":
    def ask_human(name, args):
        return input(f"Approve {name} {args}? [y/N] ").strip().lower() == "y"
    print(run_agent("Where is order 88213? If it is delayed, refund it.", approve=ask_human))
