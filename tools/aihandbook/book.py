"""Assembles every PDF in the AI Master Course set.

Outputs (handbook/):
  AI-Master-Course-Handbook.pdf              full handbook (all parts)
  AI-Master-Course-Week-1-...-Week-6-...pdf  one PDF per week (subjects, pointers, glossary)
  AI-Master-Course-Interview-Bank.pdf        interview questions and answers
  AI-Master-Course-PM-Toolkit.pdf            templates and the AI PM subjects
Run: python3 tools/aihandbook/book.py
"""
import html, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import build as B
import content as C
import deep as D

E = lambda s: html.escape(str(s), quote=True)
OUT = os.path.join(HERE, "out")
PDFDIR = os.path.join(ROOT, "handbook")

WEEK_FILES = {
    1: "AI-Master-Course-Week-1-Python-APIs-LLM.pdf",
    2: "AI-Master-Course-Week-2-RAG-Embeddings-Vector-DB.pdf",
    3: "AI-Master-Course-Week-3-Agents-Tools-MCP.pdf",
    4: "AI-Master-Course-Week-4-Evaluation-LLMOps.pdf",
    5: "AI-Master-Course-Week-5-End-to-End-Project.pdf",
    6: "AI-Master-Course-Week-6-AI-PM-Interviews.pdf",
}
PM_SUBJECTS = [17, 19, 21, 22, 23]


def glossary_html(numbers=None):
    rows = [g for g in D.GLOSSARY if numbers is None or g[2] in numbers]
    rows.sort(key=lambda g: g[0].lower())
    body = "".join(f"<tr><td><b>{E(t)}</b></td><td>{E(m)}</td><td>Subject {n}</td></tr>" for t, m, n in rows)
    return ('<section class="pb"><div class="kicker">Part L</div><h2>Glossary</h2>'
            f'<p>{len(rows)} terms in plain English, with the subject that introduces each one.</p>'
            '<table><thead><tr><th>Term</th><th>Meaning</th><th>Introduced in</th></tr></thead><tbody>' + body + '</tbody></table></section>')


def wrap(title, body, cover_line):
    cover = (f'<section class="cover"><div><div class="kicker">SkillNavora · AI Master Course</div>'
             f'<h1>{E(title)}</h1><p class="sub">{E(cover_line)}</p></div>'
             '<div class="foot">Version 1.1 · 15 November 2026 · Check every tool, price and link on its official page before use. Not a job guarantee.</div></section>')
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{B.CSS}</style></head><body>{cover}{body}</body></html>'


def week_doc(n):
    w = C.WEEKS[n - 1]
    subs = [s for s in C.SUBJECTS if s["n"] in w["subjects"]]
    body = (f'<section class="pb"><div class="week-hdr"><div class="kicker">Week {n}</div><h2>{E(w["title"])}</h2><div>Outcome: {E(w["outcome"])}</div></div></section>')
    for s in subs:
        body += f'<section class="pb">{B.subject_html(s)}</section>'
    body += glossary_html({s["n"] for s in subs})
    return wrap(f"Week {n}: {w['title']}", body, f"AI Master Course, Week {n}. Outcome: {w['outcome']}.")


def interview_doc():
    body = ('<section class="pb"><div class="kicker">Interview bank</div><h2>Technical and AI product management questions</h2>'
            f'<p>{len(C.TECH_BANK)} technical and {len(C.PM_BANK)} AI product questions with model answers. Practise aloud, then compare with the answer. Full set of 100 technical and 50 AI PM questions in volume 2.</p>'
            '<h3>Technical</h3><table><thead><tr><th>#</th><th>Area</th><th>Question</th><th>Model answer</th></tr></thead><tbody>'
            + "".join(f"<tr><td>{i+1}</td><td>{E(a)}</td><td>{E(q)}</td><td>{E(b)}</td></tr>" for i, (a, q, b) in enumerate(C.TECH_BANK))
            + '</tbody></table><h3>AI product management</h3><table><thead><tr><th>#</th><th>Area</th><th>Question</th><th>Model answer</th></tr></thead><tbody>'
            + "".join(f"<tr><td>{i+1}</td><td>{E(a)}</td><td>{E(q)}</td><td>{E(b)}</td></tr>" for i, (a, q, b) in enumerate(C.PM_BANK))
            + '</tbody></table></section>')
    body += ('<section class="pb"><div class="kicker">Practice</div><h2>Subject interview questions with pointers</h2>'
             + "".join(f'<h3>Subject {s["n"]}: {E(s["title"])}</h3>' + "".join(f'<p><b>Q: {E(q)}</b><br>{E(a)}</p>' for q, a in s["interview"]) for s in C.SUBJECTS)
             + '</section>')
    return wrap("Interview Bank", body, "Technical and AI product management questions with model answers, plus per-subject questions.")


def pm_doc():
    body = ('<section class="pb"><div class="kicker">AI PM toolkit</div><h2>Templates and metrics</h2>'
            '<h3>G1. PRD template</h3><ol>' + "".join(f"<li>{E(x)}</li>" for x in C.PRD_SECTIONS) + '</ol>'
            '<h3>G2. System design template</h3><ol>' + "".join(f"<li>{E(x)}</li>" for x in C.SYSTEM_DESIGN_TEMPLATE) + '</ol>'
            '<h3>G3. Metric families</h3><table><thead><tr><th>Family</th><th>Examples</th></tr></thead><tbody>'
            + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in C.METRICS) + '</tbody></table>'
            '<h3>G4. Release gate</h3><p>No release unless the golden set passes its bar, the risk register is reviewed, the rollback plan is written, and the owner has signed the decision.</p>'
            '<h3>G5. Prototype and figure index</h3>' + "".join(f'<div class="fig">{B.F2.render(k)}</div>' for k in ["funnel", "prd_map", "release_gate"]) + '</section>')
    for n in PM_SUBJECTS:
        s = next(x for x in C.SUBJECTS if x["n"] == n)
        body += f'<section class="pb">{B.subject_html(s)}</section>'
    body += glossary_html(set(PM_SUBJECTS))
    return wrap("AI PM Toolkit", body, "PRD, metrics and release templates, with the AI product management subjects and their glossary.")


def full_doc():
    doc = B.build_html()
    return doc.replace("</body>", glossary_html() + "</body>")


def pdf(html_text, name):
    os.makedirs(OUT, exist_ok=True); os.makedirs(PDFDIR, exist_ok=True)
    hp = os.path.join(OUT, name.replace(".pdf", ".html"))
    open(hp, "w", encoding="utf-8").write(html_text)
    pp = os.path.join(PDFDIR, name)
    out = subprocess.run(["node", os.path.join(HERE, "render_pdf.js"), hp, pp], capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        raise SystemExit(f"PDF failed for {name}: {out.stderr}")
    return pp


if __name__ == "__main__":
    made = []
    made.append(pdf(full_doc(), "AI-Master-Course-Handbook.pdf"))
    for n, name in WEEK_FILES.items():
        made.append(pdf(week_doc(n), name))
    made.append(pdf(interview_doc(), "AI-Master-Course-Interview-Bank.pdf"))
    made.append(pdf(pm_doc(), "AI-Master-Course-PM-Toolkit.pdf"))
    for m in made:
        print(os.path.basename(m), os.path.getsize(m))
