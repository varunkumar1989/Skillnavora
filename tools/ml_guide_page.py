"""ML class guide (Machine Learning using Python): hub page ml-class-guide.html and companion
lessons ml-guide-<slug>.html, placed in the AI for Data Engineers track.
Data: tools/mlguide/class_log.py (class log, extend it as new classes happen) and
tools/mlguide/guide_lessons.py (companion lessons). Outputs: tools/mlguide/outputs.json
(run tools/mlguide/capture.py after changing any example). Existing lessons are not changed."""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mlguide"))
import class_log as K
import guide_lessons as GL
from ai_lessons_page import CSS as LESSON_CSS, flow

E = lambda s: html.escape(str(s), quote=True)
ROOT = os.path.dirname(HERE)
OUT = json.load(open(os.path.join(HERE, "mlguide", "outputs.json")))
CAT = json.load(open(os.path.join(ROOT, "data-science", "catalog.json")))
TRACKS = {t["id"]: t for t in CAT["tracks"]}
PREFIX = {"ml": "ml", "py": "python", "de": "data-engineering", "gov": "governance"}
GUIDE = {l["slug"]: l for l in GL.LESSONS}
ZIP = "handbook/ML-Class-Guide-Code.zip"
HUB = "ml-class-guide.html"


def gpath(slug):
    return f"ml-guide-{slug}.html"


def ref(r):
    """Turn a reference such as 'ml:4' or 'guide:customer-360' into (label, href, kind)."""
    kind, key = r.split(":", 1)
    if kind in PREFIX:
        t = TRACKS[PREFIX[kind]]
        l = next(x for x in t["lessons"] if x["n"] == int(key))
        return f"{t['name']} {l['n']}: {l['title']}", "data-science/" + l["page"], "handbook"
    if kind == "guide":
        return f"Guide: {GUIDE[key]['title']}", gpath(key), "guide"
    if kind == "ai":
        return "AI Master Course: Deploying with FastAPI and Docker" if key == "fastapi-docker" else key, f"ai-lesson-{key}.html", "handbook"
    if kind == "track":
        return f"{TRACKS[key]['name']} track", f"data-science/index.html#t-{key}", "handbook"
    raise ValueError(r)


def links(refs):
    return " · ".join(f'<a href="{E(h)}">{E(lbl)}</a>' for lbl, h, _ in map(ref, refs))


HUB_CSS = """
.mg-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0}
.mg-stats div{border:1px solid var(--line);border-radius:14px;padding:12px 14px;background:var(--surface)}
.mg-stats b{display:block;font-size:26px;color:var(--brand-ink)}
.mg-class summary{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.mg-class summary .n{font:800 12px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--brand-ink)}
.mg-class .sum{margin:8px 0 10px;color:var(--mu)}
.mg-pill{font:700 11px var(--body);padding:2px 8px;border-radius:99px;white-space:nowrap}
.mg-ok{background:#dcfce7;color:#166534}.mg-new{background:#e0e7ff;color:#3730a3}.mg-gap{background:#fee2e2;color:#991b1b}
.al td a{display:inline}
"""


def status(refs):
    if not refs:
        return '<span class="mg-pill mg-gap">Gap</span>'
    kinds = {ref(r)[2] for r in refs}
    return '<span class="mg-pill mg-new">Covered + new guide</span>' if "guide" in kinds and "handbook" in kinds else \
           '<span class="mg-pill mg-new">New guide</span>' if kinds == {"guide"} else '<span class="mg-pill mg-ok">Covered</span>'


def hub_body():
    topics = [t for c in K.CLASSES for t in c["topics"]]
    gaps = [t for t in topics if not t[1]]
    classes = []
    for c in K.CLASSES:
        rows = "".join(f"<tr><td>{E(t)}</td><td>{status(r)}</td><td>{links(r) if r else 'Not yet covered: add a reference in tools/mlguide/class_log.py'}</td></tr>" for t, r in c["topics"])
        gl = [l for l in GL.LESSONS if c["n"] in l["classes"]]
        extra = ("<p><b>Companion lessons for this class:</b> " + " · ".join(f'<a href="{gpath(l["slug"])}">{E(l["title"])}</a>' for l in gl) + "</p>") if gl else ""
        classes.append(f'<details class="mg-class" id="class-{c["n"]}"><summary><span class="n">Class {c["n"]}</span> {E(c["title"])}</summary>'
                       f'<p class="sum">{E(c["summary"])}</p><div class="al-tw"><table><thead><tr><th>Topic taught in class</th><th>Status</th><th>Where to study it</th></tr></thead><tbody>{rows}</tbody></table></div>{extra}</details>')
    cards = "".join(f'<a class="al-card" href="{gpath(l["slug"])}"><small>Classes {", ".join(map(str, l["classes"]))}</small><b>{E(l["title"])}</b><small>{E(l["lead"][:130].rsplit(" ", 1)[0])}…</small></a>' for l in GL.LESSONS)
    comp = "".join(f"<tr><td>{E(t)}</td><td>{status(r)}</td><td>{links(r)}</td></tr>" for t, r in K.COMPLETENESS)
    res = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>: {E(d)}</li>' for t, u, d in K.RESOURCES)
    return f"""<style>{LESSON_CSS}{HUB_CSS}</style><div class="al">
<section class="al-hero"><div class="wrap">
 <div class="al-crumb"><a href="program/ai-data-engineering.html">AI-First Data Engineer</a> &rsaquo; <a href="data-science/index.html#t-ml">Statistics &amp; Machine Learning</a> &rsaquo; Class guide</div>
 <div class="kicker">AI for Data Engineers · Machine Learning using Python</div>
 <h1>Machine learning class guide: every class, every topic, where to study it</h1>
 <p class="lead">Each live class is listed with the topics it covered and the exact lesson that teaches each one in depth. Topics the handbook did not cover now have companion lessons with runnable code and real output. New classes are added here as they happen.</p>
 <div class="al-btns"><a class="btn btn-primary" href="#classes">Start with Class 1</a><a class="btn btn-line" href="{ZIP}" download>Download the companion code</a><a class="btn btn-line" href="data-science/index.html#t-ml">Statistics &amp; ML track (30 lessons)</a></div>
</div></section>
<section class="al-sec"><div class="wrap">
 <div class="mg-stats"><div><b>{len(K.CLASSES)}</b>classes mapped</div><div><b>{len(topics)}</b>topics checked</div><div><b>{len(topics) - len(gaps)}</b>topics covered</div><div><b>{len(GL.LESSONS)}</b>new companion lessons</div><div><b>{len(gaps)}</b>open gaps</div></div>
 <div class="al-box tip"><b>How to use this guide.</b> After each class, open that class below, read the linked lesson for every topic, run the code, then do the lesson's practice questions. Companion lessons (purple badge) fill topics the main handbook did not teach.</div>
 <h2 id="classes">Class by class</h2>{"".join(classes)}
 <h2 id="companion" style="margin-top:26px">Companion lessons</h2>
 <p>Each one covers class topics that were missing or only touched on in the handbook, with a plain-English explanation, a step-by-step diagram, runnable Python, its real output, common mistakes, an assignment and interview questions.</p>
 <div class="al-grid">{cards}</div>
 <h2 id="complete" style="margin-top:26px">Is the course complete? The full syllabus checklist</h2>
 <p>Beyond the topics taught in class so far, a complete Machine Learning using Python course also needs these. Every item is already taught in the handbook or a companion lesson.</p>
 <div class="al-tw"><table><thead><tr><th>Topic</th><th>Status</th><th>Lesson</th></tr></thead><tbody>{comp}</tbody></table></div>
 <h2 id="resources" style="margin-top:26px">Best free resources for this course</h2><ul>{res}</ul>
 <h2 id="practice" style="margin-top:26px">Practice and interviews</h2>
 <p>Use the <a href="lab.html#data">Practice Lab</a> for exercises, <a href="data-science/lessons/career-06-business-scenario-interviews-seven-problems-and-answer-frame.html">business scenario interviews</a> for case questions, and the <a href="ml-guide-car-sales-regression.html">car-sales case</a> as a model for the weekly regression assignments.</p>
 <p class="meta" style="font-size:13.5px;color:var(--mu)">Class notes are summarised in our own words. Datasets in the companion code are synthetic, built to match the shape of the class cases.</p>
</div></section></div>"""


def lesson_body(l):
    i = GL.LESSONS.index(l)
    prev_l = GL.LESSONS[i - 1] if i else None
    next_l = GL.LESSONS[i + 1] if i + 1 < len(GL.LESSONS) else None
    after_lbl, after_href, _ = ref(f"ml:{l['track_after']}")
    src = open(os.path.join(HERE, "mlguide", "examples", l["code"]), encoding="utf-8").read().rstrip()
    cls = ", ".join(f'<a href="{HUB}#class-{n}">Class {n}</a>' for n in l["classes"])
    s = [f"""<style>{LESSON_CSS}</style><div class="al">
<section class="al-hero"><div class="wrap">
 <div class="al-crumb"><a href="program/ai-data-engineering.html">AI-First Data Engineer</a> &rsaquo; <a href="{HUB}">ML class guide</a> &rsaquo; Companion lesson {i + 1} of {len(GL.LESSONS)}</div>
 <div class="kicker">Covers {cls}</div>
 <h1>{E(l['title'])}</h1>
 <p class="lead">{E(l['lead'])}</p>
 <div class="al-btns"><a class="btn btn-primary" href="{ZIP}" download>Download the code</a><a class="btn btn-line" href="{HUB}">All classes</a><a class="btn btn-line" href="{after_href}">Related handbook lesson</a></div>
 <p class="al-crumb" style="margin-top:10px">Best read after <a href="{after_href}">{E(after_lbl)}</a> in the Data Science &amp; AI handbook.</p>
</div></section>
<section class="al-sec"><div class="wrap al-body">
 <div class="al-box tip"><b>In plain words.</b> {E(l['analogy'])}</div>
 <h2>1. Why it matters</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in l['why'])}</ul>
 <h2>2. Key ideas</h2><div class="al-terms">{"".join(f"<div><b>{E(t)}</b>{E(d)}</div>" for t, d in l['concepts'])}</div>
 <h2>3. Step by step</h2>{flow(l['diagram'], 160)}<ol>{"".join(f"<li>{E(x)}</li>" for x in l['steps'])}</ol>
 <h2>4. Code you can run</h2><p>Install once: <code>pip install numpy pandas scipy scikit-learn statsmodels</code>, then run <code>python {E(l['code'])}</code>. The data is generated inside the script, so it runs anywhere.</p>
 <div class="al-cap">{E(l['code'])}</div><pre><code>{E(src)}</code></pre>
 <div class="al-cap">Real output (captured when this page was built)</div><pre class="out"><code>{E(OUT[l['code'].split('_')[0]])}</code></pre>
 <h2>5. Reading the output</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in l['explain'])}</ul>
 <h2>6. Common mistakes</h2><div class="al-tw"><table><thead><tr><th>Mistake</th><th>Do this instead</th></tr></thead><tbody>{"".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in l['mistakes'])}</tbody></table></div>
 <h2>7. Assignment</h2><div class="al-box">{E(l['assignment'])}</div>
 <h2>8. Interview questions</h2>{"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in l['interview'])}
 <h2>9. Go further</h2><ul>{"".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in l['links'])}<li><a href="{after_href}">{E(after_lbl)}</a> (handbook)</li></ul>"""]
    nav = '<div class="al-nav">'
    nav += f'<a class="btn btn-line" href="{gpath(prev_l["slug"])}">&larr; {E(prev_l["title"])}</a>' if prev_l else f'<a class="btn btn-line" href="{HUB}">&larr; Class guide</a>'
    nav += f'<a class="btn btn-primary" href="{gpath(next_l["slug"])}">{E(next_l["title"])} &rarr;</a>' if next_l else f'<a class="btn btn-primary" href="{HUB}#complete">Syllabus checklist &rarr;</a>'
    s.append(nav + "</div></div></section></div>")
    return "".join(s)


def pages():
    """(path, title, description, body) for gen_site."""
    out = [(HUB, "Machine learning class guide: every class mapped to lessons · SkillNavora",
            "Machine Learning using Python, class by class: what each class covered, where to study every topic, companion lessons with runnable code, a full syllabus checklist and free resources.", hub_body())]
    for l in GL.LESSONS:
        out.append((gpath(l["slug"]), f"{l['title']} · ML class guide · SkillNavora", l["lead"][:155], lesson_body(l)))
    return out


def card_html(prefix=""):
    """A small link block for the Data Engineer program page and the study library."""
    return (f'<a class="btn btn-primary" href="{prefix}{HUB}">Machine learning class guide</a>')
