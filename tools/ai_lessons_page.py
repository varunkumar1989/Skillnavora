"""AI Master Course: the seven gap-filling lesson pages (ai-lesson-<slug>.html).
Content: tools/aihandbook/lessons.py. Code: the starter project. Outputs: lesson_outputs.json
(captured by tools/aihandbook/capture_lessons.py). Existing lessons are not changed."""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "aihandbook"))
import lessons as L

E = lambda s: html.escape(str(s), quote=True)
OUT = json.load(open(os.path.join(HERE, "aihandbook", "lesson_outputs.json")))
PROJ = os.path.join(HERE, "aihandbook", "starter", "ai-master-course-starter")
RUN = {"fastapi-docker": "uvicorn api.main:app --reload", "pdf-chatbot": "python examples/l6_pdf_chatbot.py"}
HUE = {2: 215, 4: 30, 5: 330, 6: 195}

CSS = """
.al{--r:16px}
.al-hero{padding:40px 0 22px;background:radial-gradient(800px 340px at 85% 0%,color-mix(in srgb,var(--brand) 14%,transparent),transparent 65%)}
.al-hero h1{font-size:clamp(30px,4.8vw,50px);line-height:1.06;margin:8px 0 12px;text-wrap:balance}
.al-hero .lead{max-width:66ch}
.al-crumb{font-size:13.5px;color:var(--mu)}
.al-crumb a{text-decoration:none}
.al-btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.al-sec{padding:18px 0}
.al-sec h2{font-size:clamp(22px,3vw,28px);margin:4px 0 10px}
.al-body{max-width:820px}
.al-body p,.al-body li{line-height:1.65}
.al-box{border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;background:var(--surface);margin:12px 0}
.al-box.tip{background:color-mix(in srgb,var(--brand) 7%,var(--surface))}
.al-terms{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.al-terms div{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:var(--surface)}
.al-terms b{display:block;color:var(--brand-ink);margin-bottom:3px}
.al-flow{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:10px 0 4px}
.al-flow span{padding:9px 12px;border-radius:10px;font:600 13.5px var(--body);background:hsl(var(--h) 70% 95%);color:hsl(var(--h) 60% 25%);border:1px solid hsl(var(--h) 55% 80%)}
.al-flow i{font-style:normal;color:var(--mu);font-weight:700}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .al-flow span{background:hsl(var(--h) 35% 20%);color:hsl(var(--h) 70% 88%);border-color:hsl(var(--h) 35% 35%)}}
:root[data-theme=dark] .al-flow span{background:hsl(var(--h) 35% 20%);color:hsl(var(--h) 70% 88%);border-color:hsl(var(--h) 35% 35%)}
.al pre{background:#0f172a;color:#e2e8f0;border-radius:12px;padding:14px 16px;overflow:auto;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;margin:8px 0;max-height:520px}
.al pre.out{background:#052e16;color:#dcfce7}
.al-cap{font:700 12px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--mu);margin-top:12px}
.al table{border-collapse:collapse;width:100%;font-size:14.5px}
.al th,.al td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
.al th{background:var(--surface)}
.al-tw{overflow-x:auto}
.al details{border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:8px 0;background:var(--surface)}
.al summary{cursor:pointer;font-weight:700}
.al-case ol{margin:6px 0 0;padding-left:20px}
.al-case li{margin:4px 0}
.al-nav{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:16px;margin-top:10px}
.al-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.al-card{border:1px solid var(--line);border-radius:var(--r);padding:16px;background:var(--surface);text-decoration:none;color:inherit;display:block;box-shadow:var(--shadow)}
.al-card b{display:block;font-size:16.5px;margin:4px 0}
.al-card small{color:var(--mu)}
"""


def path(lesson):
    return f"ai-lesson-{lesson['slug']}.html"


def flow(steps, hue):
    parts = []
    for i, s in enumerate(steps):
        if i:
            parts.append('<i aria-hidden="true">&rarr;</i>')
        parts.append(f"<span>{E(s)}</span>")
    return f'<div class="al-flow" style="--h:{hue}" role="img" aria-label="{E(" then ".join(steps))}">' + "".join(parts) + "</div>"


def code_block(rel):
    src = open(os.path.join(PROJ, rel), encoding="utf-8").read().rstrip()
    return f'<div class="al-cap">{E(rel)} (in the starter project)</div><pre><code>{E(src)}</code></pre>'


def sd_cases_html():
    out = []
    for i, (title, parts) in enumerate(L.SD_CASES, 1):
        items = "".join(f"<li><b>{E(step)}:</b> {E(text)}</li>" for step, text in zip(L.SD_STEPS, parts))
        out.append(f'<details class="al-case" id="case-{i}"><summary>Case {i}. {E(title)}</summary><ol>{items}</ol></details>')
    return "".join(out)


def lesson_body(lesson):
    idx = L.LESSONS.index(lesson)
    hue = HUE.get(lesson["week"], 265)
    prev_l = L.LESSONS[idx - 1] if idx else None
    next_l = L.LESSONS[idx + 1] if idx + 1 < len(L.LESSONS) else None
    s = []
    s.append(f"""<style>{CSS}</style><div class="al">
<section class="al-hero"><div class="wrap">
 <div class="al-crumb"><a href="ai-master-course.html">AI Master Course</a> &rsaquo; <a href="ai-master-course.html#week-{lesson['week']}">Week {lesson['week']}</a> &rsaquo; New lesson {idx + 1} of {len(L.LESSONS)}</div>
 <div class="kicker">Week {lesson['week']} · extends Subject {lesson['subject']}</div>
 <h1>{E(lesson['title'])}</h1>
 <p class="lead">{E(lesson['lead'])}</p>
 <div class="al-btns"><a class="btn btn-primary" href="{L.ZIP}" download>Download the starter project (code)</a><a class="btn btn-line" href="ai-master-course-practice.html#key-{lesson['subject']}">Quiz and answer key</a><a class="btn btn-line" href="ai-master-course-handbook.html">Clickable handbook</a></div>
</div></section>
<section class="al-sec"><div class="wrap al-body">
 <div class="al-box tip"><b>In plain words.</b> {E(lesson['analogy'])}</div>
 <h2 id="why">1. Why it matters</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in lesson['why'])}</ul>
 <h2 id="concepts">2. Key ideas</h2><div class="al-terms">{"".join(f"<div><b>{E(t)}</b>{E(d)}</div>" for t, d in lesson['concepts'])}</div>
 <h2 id="how">3. How it works, step by step</h2>{flow(lesson['diagram'], hue)}<ol>{"".join(f"<li>{E(x)}</li>" for x in lesson['steps'])}</ol>""")
    if lesson.get("code"):
        s.append(f'<h2 id="code">4. Code you can run</h2><p>Run it from the starter project folder: <code>{E(RUN.get(lesson["slug"], "python " + lesson["code"]))}</code>. It runs offline for free; add an API key in <code>.env</code> to use Claude.</p>')
        s.append(code_block(lesson["code"]))
        if lesson.get("extra_code"):
            s.append(code_block(lesson["extra_code"][1]))
        s.append(f'<div class="al-cap">Real output (offline mode, captured when this page was built)</div><pre class="out"><code>{E(OUT[lesson["output"]])}</code></pre>')
        s.append('<h2 id="explain">5. What the code does</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in lesson["explain"]) + "</ul>")
    if lesson.get("rubric"):
        rows = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in lesson["rubric"])
        s.append('<h2 id="rubric">4. Scoring rubric</h2><div class="al-tw"><table><thead><tr><th>Criterion</th><th>1</th><th>2</th><th>3 (hireable)</th><th>4</th></tr></thead><tbody>' + rows + "</tbody></table></div>")
        s.append('<h2 id="cases">5. Nine system design cases with model answers</h2><p>Try each case for 45 minutes before you open the model answer. Each answer follows the eight-step template: ' + E(", ".join(L.SD_STEPS)) + ".</p>" + sd_cases_html())
        s.append('<p>For Round 1 and Round 3 questions, use the <a href="ai-master-course-practice.html#bank">interview bank</a>: 100 technical and 50 AI PM questions with model answers.</p>')
    s.append('<h2 id="mistakes">6. Common mistakes and fixes</h2><div class="al-tw"><table><thead><tr><th>Problem</th><th>Fix</th></tr></thead><tbody>' + "".join(f"<tr><td>{E(p)}</td><td>{E(f)}</td></tr>" for p, f in lesson["mistakes"]) + "</tbody></table></div>")
    s.append('<h2 id="pm">7. Product manager view</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in lesson["pm"]) + "</ul>")
    s.append(f'<h2 id="assignment">8. Assignment</h2><div class="al-box">{E(lesson["assignment"])}</div><p>Check your work against the <a href="ai-master-course-practice.html#key-{lesson["subject"]}">model answer for Subject {lesson["subject"]}</a>.</p>')
    if lesson["interview"]:
        s.append('<h2 id="interview">9. Interview questions</h2>' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in lesson["interview"]))
    s.append('<h2 id="links">10. Go further (official sources)</h2><ul>' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in lesson["links"]) + "</ul>")
    nav = '<div class="al-nav">'
    nav += f'<a class="btn btn-line" href="{path(prev_l)}">&larr; {E(prev_l["title"])}</a>' if prev_l else '<a class="btn btn-line" href="ai-master-course.html#new-lessons">&larr; All new lessons</a>'
    nav += f'<a class="btn btn-primary" href="{path(next_l)}">{E(next_l["title"])} &rarr;</a>' if next_l else '<a class="btn btn-primary" href="ai-master-course-practice.html">Quizzes and answer keys &rarr;</a>'
    s.append(nav + "</div></div></section></div>")
    return "".join(s)


def hub_section():
    """Cards for the course page: the seven new lessons, the starter project and the practice page."""
    cards = "".join(f'<a class="al-card" href="{path(l)}"><small>Week {l["week"]} · Subject {l["subject"]}</small><b>{E(l["title"])}</b><small>{E(l["lead"][:120].rsplit(" ", 1)[0])}…</small></a>' for l in L.LESSONS)
    return f"""<style>{CSS}</style><section class="amc-sec al" id="new-lessons"><div class="wrap">
  <div class="kicker">New lessons</div><h2>Seven lessons that fill the gaps</h2>
  <p class="amc-note">Each lesson has a plain-English explanation, key ideas, a step-by-step diagram, runnable code with its real output, common mistakes, a product view, an assignment with a model answer and interview questions.</p>
  <div class="al-grid">{cards}</div>
  <div class="amc-cta" style="margin-top:16px"><div><h2 style="margin:0 0 4px">Starter project and practice</h2><p class="amc-note" style="margin:0">All the course code in one download: runs offline for free, calls Claude once you add an API key. Includes a Streamlit app, a FastAPI service, a Dockerfile, an eval set and 13 tests.</p></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-primary" href="{L.ZIP}" download>Download starter project</a><a class="btn btn-line" href="ai-master-course-practice.html">Quizzes, answer keys, interview bank</a></div></div>
</div></section>"""
