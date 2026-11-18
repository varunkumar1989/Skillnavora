"""Removes the founder's personal name, profile link and employer from every HTML page, for the time being.
The owner asked for the profile to be taken off the site until permissions are in place. Runs at the end of
gen_site.py so it also covers pages that are copied in, not generated (the Data Science lessons, the PM handbook,
the labs). Bylines become "SkillNavora" or "the SkillNavora team".

Sample data that used the first name in code examples (a SQL row, a Python string) now uses "Vikram", the same on
every line of a page so code and output still match. PDF files are not changed by this step.

To bring the profile back later, remove the call in gen_site.py and restore the sections from git history."""
import os, re

SKIP_DIRS = {".git", "tools", "functions", "node_modules", "supabase", "whatsapp-agent"}
COMPANY_LI = "https://www.linkedin.com/company/skillnavora"

RULES = [
    (re.compile(r"(?i)(handbooks?) by Varun Kumar"), r"\1"),
    (re.compile(r"SkillNavora · by Varun Kumar"), "SkillNavora"),
    (re.compile(r"(Created by)((?:\s*<[^>]+>)*)\s*Varun Kumar"), r"\1\2SkillNavora"),
    (re.compile(r"Written by Varun Kumar"), "Written by the SkillNavora team"),
    (re.compile(r"written by Varun Kumar for SkillNavora"), "written for SkillNavora"),
    (re.compile(r"By Varun, for SkillNavora"), "By SkillNavora"),
    (re.compile(r"By Varun Kumar"), "By the SkillNavora team"),
    (re.compile(r"Varun Kumar · SkillNavora · "), "SkillNavora · "),
    (re.compile(r" · Varun Kumar(?=\s*<)"), " · SkillNavora"),
    (re.compile(r"https://www\.linkedin\.com/in/varun-pm01/?"), COMPANY_LI),
    (re.compile(r"American Express \(Amex\)|American Express|\bAmex\b"), "a large financial services company"),
    (re.compile(r"Varun Kumar"), "SkillNavora team"),
    (re.compile(r"\bVarun\b"), "Vikram"),     # sample data in code examples, changed the same way everywhere on a page
]


def run(out):
    pages = changed = 0
    for root, dirs, files in os.walk(out):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if not f.endswith(".html"):
                continue
            pages += 1
            p = os.path.join(root, f)
            s = open(p, encoding="utf-8", errors="ignore").read()
            if "Varun" not in s and "Amex" not in s and "American Express" not in s:
                continue
            t = s
            for rx, rep in RULES:
                t = rx.sub(rep, t)
            if t != s:
                open(p, "w", encoding="utf-8").write(t)
                changed += 1
    return {"pages": pages, "changed": changed}
