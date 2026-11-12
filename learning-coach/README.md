# SkillNavora learning coach (AI agent)

A Claude agent that quizzes you on the practice-test questions, explains mistakes with the hint and the lesson, and keeps your progress.

## What it does
- Picks a topic (or asks you to choose one).
- Asks one question at a time, using the same questions as the practice tests.
- When you answer wrong, it gives the hint and points to the lesson.
- Remembers what you have mastered in `progress.json` on your computer.

## Set up (once)
1. Install Python 3.10 or newer.
2. Install the Anthropic SDK: `pip install anthropic`
3. Get an API key from the Anthropic console and set it in your terminal (keep it private):
   - Mac or Linux: `export ANTHROPIC_API_KEY=your-key`
   - Windows PowerShell: `$env:ANTHROPIC_API_KEY="your-key"`

## Run
```
cd learning-coach
python3 agent.py
```
Type your answer, for example "start with AI product management", and follow the coach. Type `quit` to stop.

## Test the tools (no API key needed)
```
python3 -m unittest test_tools -v
```

## Files
- `coach_tools.py`: the tools the agent uses (topics, next question, check answer, progress). No AI here.
- `agent.py`: the Claude agent loop and the instructions for the coach.
- `test_tools.py`: tests for the tools.
- `progress.json`: created when you start answering. Stays on your computer; delete it to start again.

## Notes
- The questions come from `tools/practice_data.json` on the site, so updating a question there updates the coach.
- Model: `claude-sonnet-5-5`. Change `MODEL` in `agent.py` if you want another model.
- The agent calls the Claude API, so each conversation uses API credit.
