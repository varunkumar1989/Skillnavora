"""Tools for the SkillNavora learning coach. No AI here: pure Python over the practice-test data.

The agent (agent.py) calls these functions. Progress is stored in progress.json next to this file.
"""
import json, html, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "tools", "practice_data.json")
PROGRESS = os.path.join(HERE, "progress.json")
SEGMENTS = {"pm": "AI Product Management", "data": "Data Science & AI", "genai": "GenAI, Agents & AI Tools", "other": "Other programs"}

def _clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(str(s)))).strip()

def _load():
    with open(DATA, encoding="utf-8") as f:
        items = json.load(f)["tests"]
    for i, x in enumerate(items):
        x["id"] = i
        x["answer"] = int(x["a"])
    return items

QUESTIONS = _load()

def _progress():
    try:
        with open(PROGRESS, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}

def _save(p):
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=1)

def list_topics(segment=None):
    """Topics with the number of questions in each, optionally for one segment (pm, data, genai, other)."""
    counts = {}
    for x in QUESTIONS:
        if segment and x["seg"] != segment:
            continue
        counts[(x["seg"], x["topic"])] = counts.get((x["seg"], x["topic"]), 0) + 1
    return [{"segment": s, "segment_name": SEGMENTS.get(s, s), "topic": t, "questions": n} for (s, t), n in sorted(counts.items())]

def next_question(segment=None, topic=None):
    """A question the learner has not answered correctly yet, chosen at random from the matching pool."""
    prog = _progress()
    pool = [x for x in QUESTIONS if (not segment or x["seg"] == segment) and (not topic or x["topic"] == topic)]
    if not pool:
        return {"error": "No questions match. Use list_topics to see the options."}
    unseen = [x for x in pool if not prog.get(str(x["id"]), {}).get("correct")]
    x = random.choice(unseen or pool)
    return {"id": x["id"], "topic": x["topic"], "question": _clean(x["q"]),
            "choices": [_clean(c) for c in x["o"]]}

def check_answer(id, choice):
    """Check the learner's choice (0-based index). Returns right or wrong, the correct answer, a hint and the lesson link."""
    if not 0 <= int(id) < len(QUESTIONS):
        return {"error": f"No question with id {id}. Use next_question to get a valid id."}
    x = QUESTIONS[int(id)]
    if not 0 <= int(choice) < len(x["o"]):
        return {"error": f"Choice must be between 0 and {len(x['o']) - 1}."}
    right = int(choice) == x["answer"]
    prog = _progress()
    rec = prog.setdefault(str(id), {"attempts": 0, "correct": False})
    rec["attempts"] += 1
    rec["correct"] = rec["correct"] or right
    _save(prog)
    return {"correct": right, "answer": _clean(x["o"][x["answer"]]), "hint": _clean(x.get("h", "")),
            "lesson": _clean(x.get("lesson", "")), "lesson_page": x.get("page", "")}

def progress_summary():
    """How many questions the learner has answered, and how many they have got right, by segment."""
    prog = _progress()
    out = {}
    for x in QUESTIONS:
        seg = x["seg"]
        r = prog.get(str(x["id"]))
        s = out.setdefault(seg, {"segment_name": SEGMENTS.get(seg, seg), "questions": 0, "attempted": 0, "mastered": 0})
        s["questions"] += 1
        if r:
            s["attempted"] += 1
            s["mastered"] += 1 if r["correct"] else 0
    return out

TOOLS = {
    "list_topics": list_topics,
    "next_question": next_question,
    "check_answer": check_answer,
    "progress_summary": progress_summary,
}
