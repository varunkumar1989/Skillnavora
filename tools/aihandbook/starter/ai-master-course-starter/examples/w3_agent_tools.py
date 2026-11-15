"""Week 3: an agent that uses tools. With ANTHROPIC_API_KEY set, Claude decides which tool to call;
without a key, a scripted stand-in makes the same decisions so you can follow the loop for free.
Run: python examples/w3_agent_tools.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starter.config import settings

# 1) The tools: plain Python functions plus a description the model reads.
LEAVE = {"E42": 14, "E7": 3}


def get_leave_balance(employee_id: str) -> dict:
    if employee_id not in LEAVE:
        return {"error": f"unknown employee {employee_id}"}
    return {"employee_id": employee_id, "days_left": LEAVE[employee_id]}


def request_leave(employee_id: str, days: int) -> dict:
    if LEAVE.get(employee_id, 0) < days:
        return {"status": "rejected", "reason": "not enough leave"}
    LEAVE[employee_id] -= days
    return {"status": "submitted", "days": days, "days_left": LEAVE[employee_id]}


FUNCTIONS = {"get_leave_balance": get_leave_balance, "request_leave": request_leave}
TOOLS = [
    {"name": "get_leave_balance", "description": "Get how many paid leave days an employee has left.",
     "input_schema": {"type": "object", "properties": {"employee_id": {"type": "string"}}, "required": ["employee_id"]}},
    {"name": "request_leave", "description": "Submit a leave request. Only call after checking the balance.",
     "input_schema": {"type": "object", "properties": {"employee_id": {"type": "string"}, "days": {"type": "integer", "minimum": 1}},
                      "required": ["employee_id", "days"]}},
]
TASK = "I am employee E42. If I have at least 5 days left, request 5 days of leave and tell me my new balance."
MAX_STEPS = 6  # a hard stop so a confused agent cannot loop for ever


def run_tool(name: str, args: dict) -> str:
    print(f"   tool call: {name}({args})")
    result = FUNCTIONS[name](**args) if name in FUNCTIONS else {"error": f"no tool {name}"}
    print(f"   tool result: {result}")
    return json.dumps(result)


def offline_agent():
    """Scripted decisions: the same steps a model would take, for free."""
    balance = json.loads(run_tool("get_leave_balance", {"employee_id": "E42"}))
    if balance["days_left"] >= 5:
        done = json.loads(run_tool("request_leave", {"employee_id": "E42", "days": 5}))
        return f"Done: 5 days requested. You now have {done['days_left']} days left."
    return f"You only have {balance['days_left']} days left, so I did not submit a request."


def claude_agent():
    import anthropic
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": TASK}]
    for step in range(MAX_STEPS):
        response = client.messages.create(model=settings.model, max_tokens=2000, tools=TOOLS, messages=messages,
                                          output_config={"effort": settings.effort})
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
        messages.append({"role": "assistant", "content": response.content})
        results = [{"type": "tool_result", "tool_use_id": b.id, "content": run_tool(b.name, b.input)}
                   for b in response.content if b.type == "tool_use"]
        messages.append({"role": "user", "content": results})
    return "Stopped: the agent hit the step limit."


if __name__ == "__main__":
    print("Task:", TASK)
    print("Mode:", "offline script" if settings.offline else f"Claude ({settings.model})")
    print("Final answer:", offline_agent() if settings.offline else claude_agent())
