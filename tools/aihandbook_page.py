"""AI Master Course: web overview page (ai-master-course.html).

Shows the six weeks, the 26 subjects with their status on the site and a link to the
first lesson or guide for each. The full handbook is the PDF in handbook/ and the artifact.
"""
import html, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "aihandbook"))
import content as C

E = lambda s: html.escape(str(s), quote=True)
PILL = {"Covered": ("#dcfce7", "#166534"), "Partial": ("#fef3c7", "#92400e"), "Gap": ("#fee2e2", "#991b1b")}

CSS = """
.amc{--r:18px}
.amc-hero{padding:46px 0 30px;background:radial-gradient(900px 380px at 85% 0%,color-mix(in srgb,var(--brand) 16%,transparent),transparent 65%)}
.amc-hero h1{font-size:clamp(34px,5.4vw,58px);line-height:1.04;margin:10px 0 12px;text-wrap:balance}
.amc-hero .lead{max-width:64ch}
.amc-btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.amc-sec{padding:28px 0}
.amc-sec h2{font-size:clamp(24px,3.2vw,32px);margin:6px 0 10px}
.amc-weeks{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.amc-week{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;min-width:0}
.amc-week header{padding:16px 18px;color:#fff;background:linear-gradient(135deg,hsl(var(--h) 72% 46%),hsl(calc(var(--h) + 40) 70% 38%))}
.amc-week header b{font:800 12px var(--body);letter-spacing:.08em;text-transform:uppercase;opacity:.9}
.amc-week header h3{margin:4px 0 2px;color:#fff;font-size:19px}
.amc-week header small{opacity:.92}
.amc-week ol{margin:0;padding:12px 18px 16px 36px;display:flex;flex-direction:column;gap:6px}
.amc-week li{font-size:14.5px}
.amc-week li a{text-decoration:none;font-weight:600}
.amc-pill{font:700 11px var(--body);padding:2px 8px;border-radius:99px;margin-left:6px;vertical-align:middle}
.amc-tiers{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.amc-tiers div{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px}
.amc-tiers b{display:block;color:var(--brand-ink)}
.amc-cta{border-radius:22px;padding:24px;background:linear-gradient(135deg,var(--brand-soft),var(--surface));border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.amc-note{font-size:13.5px;color:var(--mu)}
@media (max-width:600px){.amc-week li{font-size:14px}}
"""

HUE = [265, 215, 160, 30, 330, 195]


def body():
    weeks = []
    for w in C.WEEKS:
        items = []
        for n in w["subjects"]:
            s = next(x for x in C.SUBJECTS if x["n"] == n)
            status, links = C.COVERAGE[n]
            bg, fg = PILL[status]
            href = links[0][1] if links else "ai-master-course.html"
            items.append(f'<li><a href="{E(href)}">{E(s["title"])}</a><span class="amc-pill" style="background:{bg};color:{fg}">{status}</span></li>')
        weeks.append(f'<article class="amc-week" id="week-{w["n"]}" style="--h:{HUE[w["n"]-1]}"><header><b>Week {w["n"]}</b><h3>{E(w["title"])}</h3><small>Outcome: {E(w["outcome"])}</small></header><ol>' + "".join(items) + '</ol></article>')
    tiers = "".join(f'<div><b>{E(k)}</b>{", ".join("S"+str(n) for n in v)}</div>' for k, v in C.TIERS.items())
    return f"""<style>{CSS}</style>
<div class="amc">
<section class="amc-hero"><div class="wrap">
  <div class="kicker">AI Master Course · Volume 1</div>
  <h1>From beginner to <span class="g">AI application builder</span> and AI PM</h1>
  <p class="lead">A six-week practical programme: Python and APIs, RAG and vector databases, agents and MCP, evaluation and LLMOps, one deployed capstone, then AI product management and interview practice. Every subject has a plain-English explanation, real code with real outputs, a product perspective, an assignment and interview questions.</p>
  <div class="amc-btns">
    <a class="btn btn-primary" href="ai-master-course-handbook.html">Open the clickable handbook</a>
    <a class="btn btn-line" href="handbook/AI-Master-Course-Handbook.pdf" download>Full handbook PDF (93 pages)</a>
    <a class="btn btn-line" href="ai-jobs-2027.html">Back to the AI Jobs 2027 roadmap</a>
  </div>
  <p class="amc-note">Study commitment: 2 to 3 hours a day, 6 days a week, 1 revision day (about 72 to 108 hours). This is a learning plan, not a job guarantee.</p>
</div></section>
<section class="amc-sec"><div class="wrap">
  <div class="kicker">Six weeks</div><h2>Week by week</h2>
  <p class="amc-note">Each subject links to the closest free SkillNavora lesson or guide. The badge shows how complete that coverage is today: Covered, Partial or Gap (the handbook fills gaps).</p>
  <div class="amc-weeks">{"".join(weeks)}</div>
</div></section>
<section class="amc-sec"><div class="wrap">
  <div class="kicker">PDFs</div><h2>Download the PDFs</h2>
  <p class="amc-note">One PDF per week, plus the interview bank and the AI PM toolkit. Each PDF has its own pointers and glossary.</p>
  <div class="amc-tiers">
    <div><b>Full handbook</b><a href="handbook/AI-Master-Course-Handbook.pdf" download>AI-Master-Course-Handbook.pdf</a></div>
    <div><b>Week 1: Python, APIs, LLM</b><a href="handbook/AI-Master-Course-Week-1-Python-APIs-LLM.pdf" download>Download</a></div>
    <div><b>Week 2: RAG and vector DB</b><a href="handbook/AI-Master-Course-Week-2-RAG-Embeddings-Vector-DB.pdf" download>Download</a></div>
    <div><b>Week 3: Agents, tools, MCP</b><a href="handbook/AI-Master-Course-Week-3-Agents-Tools-MCP.pdf" download>Download</a></div>
    <div><b>Week 4: Evaluation and LLMOps</b><a href="handbook/AI-Master-Course-Week-4-Evaluation-LLMOps.pdf" download>Download</a></div>
    <div><b>Week 5: End-to-end project</b><a href="handbook/AI-Master-Course-Week-5-End-to-End-Project.pdf" download>Download</a></div>
    <div><b>Week 6: AI PM and interviews</b><a href="handbook/AI-Master-Course-Week-6-AI-PM-Interviews.pdf" download>Download</a></div>
    <div><b>Interview bank</b><a href="handbook/AI-Master-Course-Interview-Bank.pdf" download>Download</a></div>
    <div><b>AI PM toolkit</b><a href="handbook/AI-Master-Course-PM-Toolkit.pdf" download>Download</a></div>
  </div>
  <h2 style="margin-top:22px">Curriculum by tier</h2>
  <div class="amc-tiers">{tiers}</div>
  <p class="amc-note">Optional specialisation (advanced LLMs, advanced RAG, LangGraph agents, production AI, AI product leadership) is in Part I of the handbook and is not required to finish the programme.</p>
</div></section>
<section class="amc-sec"><div class="wrap"><div class="amc-cta">
  <div><h2 style="margin:0 0 4px">Start with the handbook</h2><p class="amc-note" style="margin:0">Every subject, code example, architecture diagram, PM template, interview question and the coverage check are in one PDF.</p></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-primary" href="handbook/AI-Master-Course-Handbook.pdf" download>Download PDF</a><a class="btn btn-line" href="ai-skills-map.html">AI Skills Map</a></div>
</div></div></section>
</div>"""
