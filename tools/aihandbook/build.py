import csv
"""Builds the AI Master Course handbook: HTML (for the artifact) and PDF (for the website).

Run:  python3 tools/aihandbook/build.py
Outputs:
  tools/aihandbook/out/handbook.html          (self-contained, used for the artifact)
  handbook/AI-Master-Course-Handbook.pdf      (linked from ai-master-course.html)
Every example's printed output is produced by running the file at build time.
"""
import html, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools", "vaitis"))
import content as C
import figures as F
import deep as D
import figs2 as F2

E = lambda s: html.escape(str(s), quote=True)
EX = os.path.join(HERE, "examples")


def run_example(name):
    src = open(os.path.join(EX, name), encoding="utf-8").read()
    out = subprocess.run([sys.executable, "-I", os.path.join(EX, name)], capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise SystemExit(f"example failed: {name}\n{out.stderr}")
    return src, out.stdout.rstrip()


# ----------------------------------------------------------------- illustrations (theme-aware SVG)
FIG = {
    "flow": lambda: F.pipeline("How a request travels from a user to an API and back", [
        ("👤", "User", "types a question"), ("🖥️", "Frontend", "web or chat page"), ("⚙️", "Backend", "your server code"),
        ("🔌", "API", "provider endpoint"), ("🗄️", "Server", "model runs"), ("📨", "Response", "JSON back"),], per_row=6, bw=135),
    "llm": lambda: F.pipeline("Inside one LLM call: text becomes tokens, the model predicts, text comes back", [
        ("✏️", "Your text", "prompt and question"), ("🔤", "Tokens", "pieces of words"), ("🔢", "Embeddings", "numbers for meaning"),
        ("🧠", "Transformer", "attention over tokens"), ("🎲", "Sampling", "temperature picks next"), ("💬", "Answer", "tokens back to text")], per_row=6, bw=135),
    "rag": lambda: F.pipeline("The RAG pipeline: from your documents to a cited answer", [
        ("📄", "Documents", "PDFs, policies, reports"), ("✂️", "Chunk", "split with overlap"), ("🔢", "Embed", "meaning vectors"),
        ("🗃️", "Vector store", "searchable index"), ("🔎", "Retrieve", "top-k chunks"), ("🧠", "LLM", "answers from context"), ("✅", "Answer", "with citations")], per_row=4, bw=170),
    "vector": lambda: F.hub("Keyword search versus semantic search", [
        ("🔤", "Keyword search", "matches exact words"), ("🙁", "Misses", "'holiday' vs 'leave'")],
        ("🧭", "Semantic search", "matches meaning via vectors"),
        [("✅", "Finds", "'paid time off' for 'annual leave'"), ("🔀", "Hybrid", "keywords + vectors, then rerank")], "Old way", "Better way"),
    "agent": lambda: F.pipeline("The agent loop: think, act, observe, repeat until done", [
        ("👤", "User goal", "clear request"), ("🧠", "Model decides", "next step"), ("🔧", "Tool call", "allowed tools only"),
        ("👁️", "Observe", "read the result"), ("🔁", "Repeat?", "step limit and stop rule"), ("🏁", "Final answer", "with sources")], per_row=6, bw=135, loop_label="until done or step limit"),
    "mcp": lambda: F.hub("MCP: one standard plug for many AI apps and many tools", [
        ("🧩", "Host app", "chat app or IDE"), ("🔌", "Client", "MCP connector inside host")],
        ("⚡", "MCP protocol", "discover, call, read"),
        [("🗂️", "Server: files", "tools and resources"), ("🗃️", "Server: CRM", "read-only first"), ("🎫", "Server: tickets", "write with approval")], "AI app side", "Services side"),
    "eval": lambda: F.pipeline("Evaluation loop: change, test on the golden set, decide", [
        ("📝", "Golden set", "20+ questions, known facts"), ("🤖", "Run system", "current prompt and model"), ("📏", "Score", "correct, grounded, cited"),
        ("📊", "Compare", "with last version"), ("🚦", "Release?", "meets the bar?"), ("🔁", "Improve", "back to the change")], per_row=6, bw=135, loop_label="every change"),
    "prod": lambda: F.pipeline("Production AI: log, monitor, version, roll back", [
        ("🧾", "Log", "prompt version, sources, tokens"), ("📈", "Monitor", "quality, cost, latency"), ("🏷️", "Version", "prompts and models"),
        ("🧪", "Regression test", "golden set on release"), ("🔐", "Protect", "keys and personal data"), ("↩️", "Roll back", "if quality drops")], per_row=6, bw=135),
    "lifecycle": lambda: F.pipeline("The AI product lifecycle", [
        ("🔍", "Discover", "problem and users"), ("🧪", "Prototype", "test with real users"), ("📏", "Evaluate", "quality bar agreed"),
        ("🚀", "Launch", "limited beta first"), ("📡", "Monitor", "metrics each week"), ("🔁", "Improve", "retrain prompts, data, UX")], per_row=6, bw=135, loop_label="keep improving"),
    "metrics": lambda: F.hub("Four metric families for an AI product", [
        ("🔬", "Technical", "accuracy, hallucination, latency"), ("📦", "Product", "activation, completion, escalation")],
        ("⭐", "North Star", "one metric that predicts value"),
        [("🙂", "Customer", "satisfaction and trust"), ("💰", "Business", "cost per task, time saved, ROI")], "Quality", "Value"),
    "system": lambda: F.pipeline("A production RAG system, end to end", [
        ("👥", "Users", "web or chat"), ("🛡️", "Gateway", "auth, limits, input checks"), ("🔎", "Retriever", "vector + keyword search"),
        ("🧠", "Model", "answers with context"), ("🔧", "Tools", "approved actions only"), ("📜", "Logs and evals", "quality and cost")], per_row=6, bw=135),
    "capstone": lambda: F.pipeline("Capstone milestones: each one must pass before the next", [
        ("1️⃣", "Chat with PDFs", "citations"), ("2️⃣", "Add a tool", "approved sources"), ("3️⃣", "Research agent", "step limit, report"),
        ("4️⃣", "Evaluate", "20 questions, costs"), ("5️⃣", "Deploy", "Streamlit, GitHub, secrets")], per_row=5, bw=150),
    "prd": lambda: F.pipeline("From idea to PRD: the sections every AI product needs", [
        ("💡", "Problem", "who and why"), ("🧭", "Users", "personas and journey"), ("📋", "Requirements", "functional and quality"),
        ("✅", "Acceptance", "testable criteria"), ("📏", "Evaluation", "release bar"), ("⚠️", "Risks", "register and mitigation")], per_row=6, bw=135),
}

CSS = """
@page{size:A4;margin:16mm 14mm 18mm 14mm}
*{box-sizing:border-box}
html{font-size:10.6pt}
body{font:10.6pt/1.55 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#0f1730;background:#fff;margin:0}
h1{font-size:26pt;line-height:1.1;margin:0 0 6pt;color:#0f1730;letter-spacing:-.01em}
h2{font-size:17pt;margin:0 0 6pt;color:#312e81}
h3{font-size:12.5pt;margin:12pt 0 4pt;color:#0f1730}
h4{font-size:10.6pt;margin:8pt 0 2pt;color:#3f37c9;text-transform:uppercase;letter-spacing:.06em}
p{margin:4pt 0}
.cover{height:262mm;display:flex;flex-direction:column;justify-content:space-between;padding:6mm;background:radial-gradient(160mm 90mm at 85% 8%,rgba(79,70,229,.22),transparent 70%),linear-gradient(160deg,#eef0ff,#ffffff 60%);border-radius:10mm}
.cover .kicker{font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#4f46e5;font-size:10pt}
.cover h1{font-size:40pt;margin-top:8mm}
.cover h1 span{color:#4f46e5}
.cover .sub{font-size:13pt;color:#3d4a6b;max-width:150mm}
.cover .foot{font-size:9pt;color:#56607a}
.pb{page-break-before:always;break-before:page}
.kicker{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#4f46e5;font-size:8.6pt}
.lead{font-size:12pt;color:#3d4a6b}
.box{border:1px solid #dfe4ee;border-radius:8px;padding:8px 11px;margin:8px 0;background:#f8faff}
.tip{border-left:4px solid #4f46e5;background:#f3f2ff}
.warn{border-left:4px solid #d97706;background:#fff7ed}
table{width:100%;border-collapse:collapse;margin:6pt 0;font-size:9.4pt;page-break-inside:auto}
th,td{border:1px solid #dfe4ee;padding:4pt 6pt;text-align:left;vertical-align:top}
th{background:#eef2fa;font-weight:700}
tr{page-break-inside:avoid}
pre{background:#0b1220;color:#e2e8f0;border-radius:6px;padding:8pt;font:8.6pt/1.45 "JetBrains Mono",ui-monospace,Consolas,monospace;white-space:pre-wrap;word-break:break-word;margin:4pt 0;page-break-inside:avoid}
code{font-family:"JetBrains Mono",ui-monospace,Consolas,monospace;font-size:.92em;background:#eef2fa;border-radius:3px;padding:0 3px}
pre code{background:none;padding:0;color:inherit}
.out pre{background:#f4f7ee;color:#1f2a14;border:1px solid #cfe0b0}
.pill{display:inline-block;font:700 8pt Inter,sans-serif;padding:1px 7px;border-radius:99px}
.p-cov{background:#dcfce7;color:#166534}.p-par{background:#fef3c7;color:#92400e}.p-gap{background:#fee2e2;color:#991b1b}
.fig{margin:8pt 0;page-break-inside:avoid;background:#fff;border:1px solid #dfe4ee;border-radius:10px;padding:6px}
.fig svg{width:100%;height:auto;display:block}
.fig figcaption{font-size:8.6pt;color:#56607a;text-align:center;margin-top:3pt;font-weight:600}
.fig .fg-card{fill:#fff;stroke:#c9d1e3;stroke-width:1.5}.fig .fg-hub{fill:#4f46e5}
.fig .fg-t{fill:#0f1730;font:700 14px Inter,sans-serif}.fig .fg-t-on{fill:#fff;font:700 14px Inter,sans-serif}
.fig .fg-s{fill:#55607a;font:400 12px Inter,sans-serif}.fig .fg-s-on{fill:#fff;opacity:.9;font:400 12px Inter,sans-serif}
.fig .fg-ico{font-size:20px}.fig .fg-arrow{stroke:#55607a;stroke-width:2;fill:none}.fig .fg-head{fill:#55607a}.fig .fg-lab{fill:#55607a;font:600 11.5px Inter,sans-serif}
.fig .fg-loop{stroke:#4f46e5}.fig .fg-cap{fill:#3f37c9;font:800 11.5px Inter,sans-serif}
.fig .fg-okbox{fill:#ecfdf3;stroke:#16a34a}.fig .fg-warnbox{fill:#fff7ed;stroke:#d97706}
.fig .fg-arrow.fg-warn{stroke:#d97706}.fig .fg-lab-warn{fill:#b45309!important}.fig .fg-ok{stroke:#16a34a}
.fig .fg-card,.fig .fg-hub{}
.fig .vx-fig-scroll{overflow:visible}.fig .vx-fig-hint{display:none}
.fig figure{margin:0}
.fig svg{min-width:0}
.fig .vx-fig figcaption{}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:6pt}
.tile{border:1px solid #dfe4ee;border-radius:8px;padding:7pt 9pt;background:#fff}
.tile b{color:#312e81}
.checklist li{margin:2pt 0}
.toc a{color:#0f1730;text-decoration:none}
.toc li{margin:1.5pt 0}
.small{font-size:8.8pt;color:#56607a}
.week-hdr{background:linear-gradient(135deg,#4f46e5,#0ea5b7);color:#fff;border-radius:10px;padding:10pt 14pt;margin:0 0 8pt}
.week-hdr h2{color:#fff;margin:2pt 0}
.week-hdr .kicker{color:#e0e7ff}
"""


def figure(key, caption=None):
    svg = FIG[key]()
    svg = svg.replace('class="vx-fig"', 'class="vx-fig"')
    return f'<div class="fig">{svg}</div>'


def subject_html(s):
    status, links = C.COVERAGE[s["n"]]
    pill = {"Covered": "p-cov", "Partial": "p-par", "Gap": "p-gap"}[status]
    tier = next(k for k, v in C.TIERS.items() if s["n"] in v)
    h = [f'<h2 id="s{s["n"]}">Subject {s["n"]}: {E(s["title"])}</h2>',
         f'<p class="small"><span class="pill {pill}">{status} on the website</span> &nbsp; Week {s["week"]} · {E(tier)}</p>']
    h.append(f'<h3>1. Understand</h3><p>{E(s["understand"])}</p>')
    h.append(f'<h3>2. Why it matters</h3><p>{E(s["why"])}</p>')
    h.append('<h3>3. How it works</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in s["how"]) + "</ul>")
    if s.get("figure"):
        h.append(figure(s["figure"]))
    for key in D.EXTRA_FIG.get(s["n"], []):
        h.append('<div class="fig">' + F2.render(key) + '</div>')
    if s.get("example"):
        src, out = run_example(s["example"])
        h.append(f'<h3>4. Practical implementation</h3><p class="small">File: <code>tools/aihandbook/examples/{E(s["example"])}</code></p>')
        h.append(f'<pre><code>{E(src)}</code></pre>')
        h.append('<h4>Expected output (produced by running the file)</h4>')
        h.append(f'<div class="out"><pre><code>{E(out)}</code></pre></div>')
        h.append('<h3>5. Code explained</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in s["explain"]) + "</ul>")
    else:
        h.append('<h3>4. Practical implementation</h3><p>Work through the steps above and keep the result in your portfolio repository.</p>')
        h.append('<h3>5. Code explained</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in s["explain"]) + "</ul>")
    h.append('<h3>5b. Deep dive</h3>' + "".join(f"<p>{E(x)}</p>" for x in D.DEEP.get(s["n"], [])))
    h.append(site_block(s))
    h.append(f'<h3>6. Testing</h3><p>{E(s["test"])}</p>')
    h.append('<h3>7. Troubleshooting</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in s["troubleshoot"]) + "</ul>")
    h.append('<h3>8. AI Product Manager perspective</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in s["pm"]) + "</ul>")
    h.append(f'<h3>9. Assignment</h3><p>{E(s["assignment"])}</p>')
    h.append('<h3>10. Interview preparation</h3>' + "".join(f'<p><b>Q: {E(q)}</b><br>{E(a)}</p>' for q, a in s["interview"]))
    site = links + links_extra(s)
    h.append('<h3>11. Pointers</h3><h4>On SkillNavora (free)</h4><ul>' + "".join(f'<li>{E(l)}: <span class="small">{E(u)}</span></li>' for l, u in site) + '</ul>'
             + '<h4>Official documentation (check the live page before use)</h4><ul>' + "".join(f'<li>{E(l)}: <span class="small">{E(u)}</span></li>' for l, u in D.OFFICIAL.get(s["n"], [])) + '</ul>')
    return "\n".join(h)


SITE = None


def site_block(s):
    """What the SkillNavora pages already teach for this subject (from site_extract.json)."""
    global SITE
    if SITE is None:
        import json as _j
        path = os.path.join(HERE, "site_extract.json")
        SITE = _j.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    pages = []
    for _, u in C.COVERAGE[s["n"]][1]:
        f = u.split("#")[0]
        if f in SITE and f not in [x for x, _ in pages]:
            pages.append((f, SITE[f]))
    if not pages:
        return ""
    out = ['<h3>5c. What the SkillNavora pages already teach</h3>',
           '<p class="small">Extracted from the pages on this website. Open the link to read the full lesson.</p>']
    for f, info in pages[:3]:
        secs = [x for x in info.get("sections", []) if x.get("text")][:5]
        title = info.get("title") or f
        out.append(f'<h4>{E(title)}</h4><p class="small"><a href="https://www.skillnavora.in/{E(f)}">https://www.skillnavora.in/{E(f)}</a>'
                   + (f' · {info["pages"]} pages' if info.get("pages") else "") + '</p>')
        if secs:
            out.append("<ul>" + "".join(f"<li><b>{E(x['heading'])}:</b> {E(x['text'])}</li>" for x in secs) + "</ul>")
    return "\n".join(out)


def links_extra(s):
    return [(l, u) for l, u in C.COVERAGE[s["n"]][1] if (l, u) not in s["links"]]


def coverage_table():
    rows = []
    for s in C.SUBJECTS:
        status, links = C.COVERAGE[s["n"]]
        pill = {"Covered": "p-cov", "Partial": "p-par", "Gap": "p-gap"}[status]
        rows.append(f"<tr><td>{s['n']}</td><td>{E(s['title'])}</td><td><span class='pill {pill}'>{status}</span></td><td>{E(links[0][0]) if links else ''}</td></tr>")
    return ("<table><thead><tr><th>#</th><th>Subject</th><th>Status</th><th>Main site content</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def build_html():
    parts = []
    # Cover
    parts.append(f'''<section class="cover"><div><div class="kicker">SkillNavora · Volume 1 · Complete handbook</div>
    <h1>AI Master Course<br><span>From beginner to AI application builder and AI PM</span></h1>
    <p class="sub">A six-week practical programme with explained code, real outputs, architecture diagrams, product templates, assessments and interview preparation. Written for non-coders who want to understand, build, evaluate and manage AI products.</p></div>
    <div class="foot">Version 1.0 · 15 November 2026 · Study commitment: 2 to 3 hours a day, 6 days a week, 1 revision day. Not a job guarantee.</div></section>''')
    # Contents
    toc = [("How to use this handbook", "how"), ("Part A. Coverage check and skill gaps", "x1"), ("Part B. Curriculum", "x2")]
    toc += [(f"Part D. Subject {s['n']}: {s['title']}", f"s{s['n']}") for s in C.SUBJECTS]
    toc += [("Part C. Six-week timetable", "x4"), ("Part E. Assessment and tracker", "x5"), ("Part F. Architecture library", "x6"),
            ("Part G. AI PM toolkit and templates", "x7"), ("Part H. Interview bank (volume 1)", "x8"), ("Part I. Advanced specialisation track", "x9"),
            ("Part J. Tool stack", "x10"), ("Part K. Success criteria and capstone", "x11")]
    parts.append('<section class="pb"><div class="kicker">Contents</div><h2>Contents</h2><ol class="toc">' + "".join(f'<li><a href="#{anchor}">{E(t)}</a></li>' for t, anchor in toc) + "</ol></section>")
    # How to use
    parts.append('''<section class="pb"><div class="kicker">Start here</div><h2 id="how">How to use this handbook</h2>
    <p>Each subject follows the same eleven steps: understand (analogy), why it matters, how it works, practical implementation, code explained, testing, troubleshooting, product perspective, assignment, interview questions and further reading.</p>
    <div class="box tip"><b>Rule for every topic:</b> reading an explanation does not count as learning it. Run the code, change it, and show your result.</div>
    <div class="box warn"><b>Check before you rely on a tool:</b> AI tools, model names, prices and free limits change often. Confirm them on the provider's official page the day you use them.</div>
    <p><b>Code examples are real.</b> The six example files in tools/aihandbook/examples run without an API key, and the outputs in this handbook were produced by running them when the handbook was built.</p>''')
    # Part A
    parts.append('<section class="pb"><div class="kicker">Part A</div><h2 id="x1">Coverage check and skill gaps</h2>'
                 '<p>This is what the SkillNavora site already contains for each subject, checked against the site content index. <b>Covered</b> means a dedicated lesson, guide or page exists. <b>Partial</b> means the topic is touched on in a broader page. <b>Gap</b> means there is no dedicated content yet; this handbook fills it.</p>'
                 + coverage_table() +
                 '<h3>What is missing on the site today</h3><ul>'
                 '<li><b>Chunking in depth</b> (Subject 6): only a PDF on vector databases touches it. This handbook is the first full treatment.</li>'
                 '<li><b>Hallucinations and guardrails</b> (Subject 14): covered in evaluation lessons, not as its own lesson.</li>'
                 '<li><b>FastAPI and Docker</b> (Subjects 15, 20, advanced D): mentioned in one or two pages only.</li>'
                 '<li><b>LangGraph and multi-agent orchestration</b> (Subject 12): one framework comparison lesson.</li>'
                 '<li><b>LLMOps and monitoring</b> (Subject 16): partly in Agent Orchestration &amp; Monitoring.</li>'
                 '<li><b>Mock-interview rounds and system design cases</b> (Subjects 23, 26): now covered by the mock-interview lesson with nine cases and model answers.</li></ul>'
                 '<h3>Skill gaps from the research file</h3>'
                 f'<div class="box warn"><b>{E(C.SKILL_NOTE)}</b></div>'
                 '<p>Skills mentioned most often in the research file, with the number of records that name them:</p>'
                 '<table><thead><tr><th>Skill</th><th>Records naming it</th><th>Share of records with requirements</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{E(r[0])}</td><td>{E(r[1])}</td><td>{E(r[2])}</td></tr>" for r in SKILL_ROWS) +
                 '</tbody></table>'
                 '<p class="small">Source: research/part3_skill_matrix.csv and research/part2_job_descriptions.csv in the SkillNavora repository.</p></section>')
    # Part B
    tiers = "".join(f"<tr><td>{E(k)}</td><td>{', '.join('S'+str(n) for n in v)}</td></tr>" for k, v in C.TIERS.items())
    weeks = "".join(f"<tr><td>Week {w['n']}</td><td>{E(w['title'])}</td><td>{E(w['outcome'])}</td><td>{', '.join('S'+str(n) for n in w['subjects'])}</td></tr>" for w in C.WEEKS)
    parts.append('<section class="pb"><div class="kicker">Part B</div><h2 id="x2">Curriculum</h2>'
                 '<p>Twenty-six subjects over six weeks. Foundations come first; advanced topics are kept optional so the core programme stays achievable.</p>'
                 '<table><thead><tr><th>Week</th><th>Main subject</th><th>Practical outcome</th><th>Subjects</th></tr></thead><tbody>' + weeks + '</tbody></table>'
                 '<h3>Curriculum by tier</h3><table><thead><tr><th>Tier</th><th>Subjects</th></tr></thead><tbody>' + tiers + '</tbody></table>'
                 '<p class="small">Optional specialisation (Part I) is not a prerequisite.</p></section>')
    # Part D
    parts.append('<section class="pb"><div class="kicker">Part D</div><h2 id="x3">Detailed subjects</h2><p>Each subject uses the same eleven steps. Work through them in order.</p></section>')
    cur_week = None
    for s in C.SUBJECTS:
        if s["week"] != cur_week:
            cur_week = s["week"]
            w = C.WEEKS[cur_week - 1]
            parts.append(f'<section class="pb"><div class="week-hdr"><div class="kicker">Week {w["n"]}</div><h2>{E(w["title"])}</h2><div>Outcome: {E(w["outcome"])}</div></div></section>')
        parts.append(f'<section>{subject_html(s)}</section>')
    # Part C timetable (placed after subjects, referenced from contents)
    parts.append('<section class="pb"><div class="kicker">Part C</div><h2 id="x4">Six-week daily timetable</h2>'
                 '<p>Each week has six study days and one revision day. Use 2 to 3 hours a day. Keep the same slot each day.</p>'
                 '<table><thead><tr><th>Day</th><th>Block 1 (learn)</th><th>Block 2 (build)</th><th>Block 3 (practise)</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{E(d)}</td><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for d, a, b, c in C.TIMETABLE)
                 + '</tbody></table><p>Week 1 lessons 1 to 4 finish by Day 5 of week 1 so the week-1 deliverable has room. Keep Day 7 free for catch-up.</p></section>')
    # Part E
    parts.append('<section class="pb"><div class="kicker">Part E</div><h2 id="x5">Assessment and progress tracker</h2>'
                 '<p>At the end of each week: 15 conceptual questions, 5 practical exercises, 1 mini-project, 1 architecture explanation and 1 interview simulation.</p>'
                 '<table><thead><tr><th>Area</th><th>Weight</th></tr></thead><tbody>'
                 '<tr><td>Conceptual understanding</td><td>15%</td></tr><tr><td>Coding and implementation</td><td>25%</td></tr>'
                 '<tr><td>AI application development</td><td>25%</td></tr><tr><td>Evaluation and troubleshooting</td><td>15%</td></tr>'
                 '<tr><td>Product documentation</td><td>10%</td></tr><tr><td>Interview explanation</td><td>10%</td></tr></tbody></table>'
                 '<h3>Progress tracker (copy into a spreadsheet)</h3>'
                 '<table><thead><tr><th>Subject</th><th>Learning status</th><th>Practical exercise</th><th>Assignment</th><th>Score</th><th>Weak areas</th><th>Revision needed?</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{s['n']}. {E(s['title'])}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" for s in C.SUBJECTS) +
                 '</tbody></table><div class="box tip"><b>Rule:</b> mark a subject complete only after you have shown the working result (a running file, a test log or a report), not after reading.</div></section>')
    # Part F
    arch = [("flow", "Request flow", "How a request travels from user to API and back."), ("llm", "LLM call", "What happens inside one model call."),
            ("rag", "RAG pipeline", "Documents to cited answers."), ("vector", "Semantic search", "Why meaning search finds more."),
            ("agent", "Agent loop", "Think, act, observe, repeat."), ("mcp", "MCP", "One standard for tools and data."),
            ("eval", "Evaluation loop", "Test every change against a golden set."), ("prod", "Production operations", "Log, monitor, version, roll back."),
            ("system", "Production RAG system", "A reference architecture."), ("capstone", "Capstone milestones", "Build in stages with gates.")]
    parts.append('<section class="pb"><div class="kicker">Part F</div><h2 id="x6">Architecture library</h2><p>Reusable diagrams. Redraw them by hand when you explain a system in an interview.</p>'
                 + "".join(f'<h3>{E(t)}</h3><p>{E(d)}</p>{figure(k)}' for k, t, d in arch) + '</section>')
    # Part G
    parts.append('<section class="pb"><div class="kicker">Part G</div><h2 id="x7">AI PM toolkit and templates</h2>'
                 '<h3>G1. PRD template</h3><ol>' + "".join(f"<li>{E(x)}</li>" for x in C.PRD_SECTIONS) + '</ol>'
                 '<h3>G2. System design template</h3><ol>' + "".join(f"<li>{E(x)}</li>" for x in C.SYSTEM_DESIGN_TEMPLATE) + '</ol>'
                 '<h3>G3. Metric families</h3><table><thead><tr><th>Family</th><th>Examples</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in C.METRICS) + '</tbody></table>'
                 '<h3>G4. User story and acceptance criteria</h3><div class="box"><p><b>User story:</b> As a support agent, I want a draft answer with its policy source, so that I can reply to a customer in under two minutes.</p>'
                 '<p><b>Acceptance criteria:</b> (1) every draft cites at least one approved source; (2) answer accuracy is 95% or higher on the golden set; (3) when no source is found, the draft says so and suggests escalation; (4) p95 latency under 8 seconds.</p></div>'
                 '<h3>G5. Release gate</h3><p>No release unless the golden set passes its bar, the risk register is reviewed, the rollback plan is written, and the owner has signed the decision.</p></section>')
    # Part H
    tech_rows = "".join(f"<tr><td>{i+1}</td><td>{E(a)}</td><td>{E(q)}</td><td>{E(b)}</td></tr>" for i, (a, q, b) in enumerate(C.TECH_BANK))
    pm_rows = "".join(f"<tr><td>{i+1}</td><td>{E(a)}</td><td>{E(q)}</td><td>{E(b)}</td></tr>" for i, (a, q, b) in enumerate(C.PM_BANK))
    parts.append('<section class="pb"><div class="kicker">Part H</div><h2 id="x8">Interview bank (volume 1)</h2>'
                 f'<p>This volume contains {len(C.TECH_BANK)} technical and {len(C.PM_BANK)} AI product management questions with short model answers. The full set is 100 technical and 50 AI PM questions; the nine system design cases with model answers are on the mock-interview page.</p>'
                 '<h3>H1. Technical questions</h3><table><thead><tr><th>#</th><th>Area</th><th>Question</th><th>Model answer</th></tr></thead><tbody>' + tech_rows + '</tbody></table>'
                 '<h3>H2. AI product management questions</h3><table><thead><tr><th>#</th><th>Area</th><th>Question</th><th>Model answer</th></tr></thead><tbody>' + pm_rows + '</tbody></table></section>')
    # Part I
    parts.append('<section class="pb"><div class="kicker">Part I</div><h2 id="x9">Advanced specialisation track (optional)</h2>'
                 f'<p>{E(C.ADVANCED_NOTE)}</p><table><thead><tr><th>Track</th><th>Topics</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in C.ADVANCED) + '</tbody></table></section>')
    # Part J
    parts.append('<section class="pb"><div class="kicker">Part J</div><h2 id="x10">Tool stack</h2>'
                 '<p>One beginner-friendly primary tool per category and one alternative. This list is a recommendation, not a verified price or feature comparison; check each official site before you start.</p>'
                 '<table><thead><tr><th>Category</th><th>Primary (beginner)</th><th>Alternative</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in C.TOOLS) + '</tbody></table></section>')
    # Part K
    parts.append('<section class="pb"><div class="kicker">Part K</div><h2 id="x11">Success criteria and capstone</h2>'
                 '<h3>Technical</h3><ul><li>Explain Python basics, APIs, tokens, embeddings and context windows.</li><li>Build a RAG app and explain tool calling and MCP.</li><li>Evaluate an AI app, find hallucinations and analyse latency and cost.</li><li>Deploy an AI application from GitHub.</li></ul>'
                 '<h3>Product</h3><ul><li>Identify valuable AI use cases and test feasibility.</li><li>Write an AI PRD with acceptance criteria and a release bar.</li><li>Define metrics across technical, product, customer and business families.</li><li>Explain governance and build a business case.</li></ul>'
                 '<h3>Portfolio</h3><ul><li>Three practical AI applications.</li><li>One end-to-end capstone (Subject 18) with a repository, PRD, architecture diagram and evaluation report.</li><li>A three-minute demo and an AI PM case study.</li></ul>'
                 '<h3>Career</h3><ul><li>Explain AI concepts simply.</li><li>Answer technical and product interview questions with trade-offs.</li><li>Present your projects clearly.</li></ul>'
                 '<div class="box tip"><b>Final principle:</b> the goal is not to know AI vocabulary, or to generate code you do not understand. It is to understand how AI works, build with it, measure it and manage it from discovery to production.</div></section>')
    body = "\n".join(parts)
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Master Course Handbook</title><style>{CSS}</style></head><body>{body}</body></html>'


def _load_skill_rows():
    """Skill counts come from research/part3_skill_matrix.csv (generated), so the handbook and the CSV always agree."""
    path = os.path.join(HERE, "..", "..", "research", "part3_skill_matrix.csv")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]
    return [(r[0], int(r[1]), r[3]) for r in rows[:14]]


SKILL_ROWS = _load_skill_rows()


def render_pdf(html_path, pdf_path):
    script = os.path.join(HERE, "render_pdf.js")
    env = dict(os.environ)
    out = subprocess.run(["node", script, html_path, pdf_path], capture_output=True, text=True, timeout=300, env=env)
    if out.returncode != 0:
        raise SystemExit("PDF render failed: " + out.stderr)
    print(out.stdout.strip())


if __name__ == "__main__":
    out_dir = os.path.join(HERE, "out"); os.makedirs(out_dir, exist_ok=True)
    html_path = os.path.join(out_dir, "handbook.html")
    doc = build_html()
    open(html_path, "w", encoding="utf-8").write(doc)
    pdf_dir = os.path.join(ROOT, "handbook"); os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, "AI-Master-Course-Handbook.pdf")
    render_pdf(html_path, pdf_path)
    print("html bytes", len(doc.encode()), "pdf bytes", os.path.getsize(pdf_path))
