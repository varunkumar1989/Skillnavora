"""Chapter content for the AI Product Management 2 course: one chapter (subject) per PDF and per artifact.

Shared by tools/aipm2_pdfs.py (PDF HTML) and tools/aipm2_artifacts.py (artifact pages), so both read the same text.
"""
import html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aipm2
from aipm2 import extras
from aipm2_page import EXISTING
from aipm2_guide import PRACTICE
E = html.escape
CHAPTERS = aipm2.load_detailed()
SITE = "https://www.skillnavora.in/"

def slug(n, title):
    return aipm2.pdf_name(n, title)[:-4]

def self_check(s):
    """Three prompts that cover the start, middle and end of the chapter."""
    t = s["topics"]
    picks = [t[0], t[len(t) // 2], t[-1]]
    return [f"Explain {name} in two sentences to a non-technical stakeholder, then say what you would measure for it."
            for name, _, _ in picks]

def related(n):
    return [(h, t, d) for h, t, d, sj in EXISTING if str(n) in [x.strip() for x in sj.replace("-", ",").split(",")] or sj == "all"]
