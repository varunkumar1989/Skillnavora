# Week 3, Subjects 9-10: an agent loop with tools, tested with a scripted "model"
import json

TOOLS = {
    "get_leave_balance": lambda employee_id: {"employee_id": employee_id, "days_left": 14},
    "book_meeting": lambda title: {"status": "booked", "title": title},
}

def scripted_model(history):
    # A real model decides the next step. This script shows the decisions it would make.
    if not any(m["role"] == "tool" for m in history):
        return {"action": "tool", "name": "get_leave_balance", "args": {"employee_id": "E42"}}
    return {"action": "final", "text": "You have 14 days of leave left."}

def run_agent(user_request, max_steps=5):
    history = [{"role": "user", "content": user_request}]
    for step in range(max_steps):
        decision = scripted_model(history)
        if decision["action"] == "final":
            return decision["text"]
        result = TOOLS[decision["name"]](**decision["args"])
        history.append({"role": "tool", "content": json.dumps(result)})
        print(f"step {step + 1}: called {decision['name']} -> {result}")
    return "Stopped: step limit reached"

print("Answer:", run_agent("How much leave do I have left?"))
