"""SkillNavora learning coach: a Claude agent that quizzes you using the practice-test questions.

Setup (once):   pip install anthropic
Run:            export ANTHROPIC_API_KEY=your-key   (never paste the key into a file or chat)
                python3 agent.py
"""
import json, os, sys
import coach_tools as ct

MODEL = "claude-sonnet-5-5"

SYSTEM = """You are a friendly learning coach for SkillNavora students.
- Quiz the learner with next_question, one at a time. Ask them to pick a choice by its number.
- After each answer call check_answer. If right, praise briefly and move on. If wrong, explain the hint in plain words, mention the lesson, then offer the next question.
- Keep questions in the topic the learner picks. If they have no preference, start with list_topics.
- Use progress_summary when they ask how they are doing.
- Use short, plain sentences. Do not invent answers or facts: the correct answer and hint come only from check_answer."""

TOOL_SCHEMAS = [
    {"name": "list_topics", "description": "List quiz topics with question counts. Optional segment: pm, data, genai or other.",
     "input_schema": {"type": "object", "properties": {"segment": {"type": "string", "enum": ["pm", "data", "genai", "other"]}}}},
    {"name": "next_question", "description": "Get a quiz question the learner has not yet answered correctly. Optional segment and topic.",
     "input_schema": {"type": "object", "properties": {"segment": {"type": "string"}, "topic": {"type": "string"}}}},
    {"name": "check_answer", "description": "Check the learner's choice (0-based index) for a question id.",
     "input_schema": {"type": "object", "properties": {"id": {"type": "integer"}, "choice": {"type": "integer"}}, "required": ["id", "choice"]}},
    {"name": "progress_summary", "description": "Show how many questions the learner has attempted and mastered, by segment.",
     "input_schema": {"type": "object", "properties": {}}},
]

def run_tool(name, args):
    """Run one of the coach tools and return its result as JSON text for the model."""
    fn = ct.TOOLS.get(name)
    if fn is None:
        return json.dumps({"error": f"unknown tool {name}"})
    try:
        return json.dumps(fn(**args), ensure_ascii=False)
    except (TypeError, ValueError, IndexError, KeyError) as e:
        return json.dumps({"error": str(e)})

def main():
    try:
        import anthropic
    except ImportError:
        sys.exit("Install the SDK first: pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Set ANTHROPIC_API_KEY in your environment first.")
    client = anthropic.Anthropic()
    messages = []
    print("SkillNavora learning coach. Type 'quit' to stop.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ("quit", "exit", ""):
            break
        messages.append({"role": "user", "content": user})
        while True:
            resp = client.messages.create(model=MODEL, max_tokens=1024, system=SYSTEM, tools=TOOL_SCHEMAS, messages=messages)
            messages.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason != "tool_use":
                text = "".join(b.text for b in resp.content if b.type == "text")
                print(f"\nCoach: {text}\n")
                break
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": run_tool(block.name, block.input)})
            messages.append({"role": "user", "content": results})

if __name__ == "__main__":
    main()
