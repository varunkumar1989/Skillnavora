
"""Build all FDE handbook PDFs: programme guide, 7 stage handbooks, 14 module handbooks, complete handbook."""
import html as H, os, sys, base64
sys.path.insert(0, os.path.dirname(__file__))
from build_curriculum import MODULES, VOLUMES, JOBS
from content_a import MODS_A
from content_b import MODS_B
from notes_a import NOTES_A
from notes_b import NOTES_B
from stages_12 import STAGE1, STAGE2
from stages_34 import STAGE3, STAGE4
from stages_567 import STAGE5, STAGE6, STAGE7
from tracks_tools import TRACKS, TOOLS, STACKS

E = lambda t: H.escape(str(t), quote=True)
OUT = os.path.join(os.path.dirname(__file__), "pdf")
os.makedirs(OUT, exist_ok=True)
TAGLINE = "From Non-Coder to Enterprise AI Builder: Learn, Build, Deploy, Get Hired and Launch Your AI Business."
LOGO = open("/home/user/skillnavora/assets/skillnavora-logo.svg", encoding="utf-8").read()
LOGO_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO.encode()).decode()

NOTES = {**NOTES_A, **NOTES_B}
SEC = {s[0]: s for m in MODS_A + MODS_B for s in m[2]}
STAGES = [
 (1, "Programming foundations", "Understand programming; build simple applications", STAGE1),
 (2, "Applied AI", "Build practical LLM-powered applications", STAGE2),
 (3, "Agent development", "Build tool-using agents and automated workflows", STAGE3),
 (4, "Application development", "Build complete AI-powered applications", STAGE4),
 (5, "Production deployment", "Deploy secure, scalable applications", STAGE5),
 (6, "Enterprise projects", "Demonstrate end-to-end project ownership", STAGE6),
 (7, "Professional and entrepreneurial readiness", "Prepare for employment and independent business", STAGE7),
]

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
* { box-sizing: border-box; }
body { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; color: #1d1b2e; font-size: 10.2pt; line-height: 1.5; margin: 0; }
h1, h2, h3, h4 { font-family: 'Space Grotesk', 'Inter', Arial, sans-serif; color: #2b1a66; line-height: 1.25; }
h1 { font-size: 22pt; margin: 0 0 6pt; }
h2 { font-size: 15.5pt; margin: 18pt 0 6pt; padding-bottom: 4pt; border-bottom: 2px solid #e3dff5; break-after: avoid; }
h3 { font-size: 12pt; margin: 12pt 0 4pt; color: #5a35c8; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 9pt 0 3pt; color: #0b7a75; text-transform: uppercase; letter-spacing: .04em; break-after: avoid; }
p { margin: 3pt 0 6pt; }
ul, ol { margin: 2pt 0 6pt; padding-left: 16pt; }
li { margin: 1.5pt 0; }
a { color: #5a35c8; text-decoration: none; word-break: break-word; }
.cover { height: 255mm; display: flex; flex-direction: column; justify-content: space-between; padding: 8mm 4mm; break-after: page;
  background: linear-gradient(160deg, #f5f3ff 0%, #ffffff 55%, #e9fbf8 100%); border-radius: 6mm; }
.cover img { width: 70mm; }
.cover .kick { font-size: 10pt; letter-spacing: .14em; text-transform: uppercase; color: #0b7a75; font-weight: 700; }
.cover h1 { font-size: 30pt; color: #2b1a66; margin: 8pt 0; }
.cover .sub { font-size: 13pt; color: #3d3a55; max-width: 150mm; }
.cover .tag { font-size: 12pt; font-weight: 700; color: #5a35c8; margin-top: 10pt; max-width: 160mm; }
.cover .by { font-size: 11pt; color: #3d3a55; }
.def { background: #f5f3ff; border-left: 4px solid #6a3fd1; padding: 7pt 10pt; border-radius: 4pt; margin: 6pt 0 8pt; }
.why { background: #ecfbf8; border-left: 4px solid #0b7a75; padding: 7pt 10pt; border-radius: 4pt; margin: 6pt 0 8pt; }
.ex { background: #fff7e8; border-left: 4px solid #d98a00; padding: 7pt 10pt; border-radius: 4pt; margin: 6pt 0 8pt; }
pre { background: #1e1b2e; color: #f2f0ff; padding: 8pt 10pt; border-radius: 5pt; font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
  font-size: 7.9pt; line-height: 1.42; white-space: pre-wrap; word-break: break-word; margin: 4pt 0 8pt; }
.qa { margin: 4pt 0 6pt; }
.qa .q { font-weight: 700; color: #2b1a66; }
.topic { break-before: page; }
.topic:first-of-type { break-before: auto; }
.lbl { font-size: 8pt; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #6a3fd1; }
table { width: 100%; border-collapse: collapse; font-size: 8.8pt; margin: 4pt 0 10pt; }
th, td { border: 1px solid #ddd8f2; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f5f3ff; color: #2b1a66; }
tr { break-inside: avoid; }
.toc li { margin: 2pt 0; }
.tn { margin: 5pt 0 7pt; }
.tn b { color: #2b1a66; }
.note { font-size: 8.8pt; color: #5b5876; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8pt; }
.card { border: 1px solid #ddd8f2; border-radius: 5pt; padding: 7pt 9pt; break-inside: avoid; }
"""

FOOTER = ('<div style="font-size:7.5pt;width:100%;padding:0 15mm;color:#6b6788;display:flex;justify-content:space-between;font-family:Arial">'
          '<span>© SkillNavora · FDE, Enterprise AI Architect &amp; AI Automation Business Handbook</span>'
          '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')


def cover(kick, title, sub):
    return (f'<section class="cover"><div><img src="{LOGO_URI}" alt="SkillNavora"></div>'
            f'<div><div class="kick">{E(kick)}</div><h1>{E(title)}</h1><div class="sub">{E(sub)}</div>'
            f'<div class="tag">{E(TAGLINE)}</div></div>'
            f'<div class="by">Varun Kumar · SkillNavora · skillnavora.in<br><span class="note">Edition: November 2026. '
            'Links point to official documentation where available; check them for the latest versions. Financial figures are hypothetical examples, not advice.</span></div></section>')


def ul(items): return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"
def ol(items): return "<ol>" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ol>"
def links(res): return "<ul>" + "".join(f'<li><a href="{E(u)}">{E(n)}</a> <span class="note">{E(u)}</span></li>' for n, u in res) + "</ul>"


def topic_html(n, i, t, page_break=True):
    qa = "".join(f'<div class="qa"><div class="q">Q. {E(q)}</div><div>A. {E(a)}</div></div>' for q, a in t["qa"])
    code = f'<h4>Example code / template</h4><pre>{E(t["code"])}</pre>' if t["code"] else ""
    return (f'<div class="{"topic" if page_break else ""}"><div class="lbl">Stage {n} · Topic {i}</div><h2>{E(t["t"])}</h2>'
            f'<h4>Definition</h4><div class="def">{E(t["what"])}</div>'
            f'<h4>Why it matters</h4><div class="why">{E(t["why"])}</div>'
            f'<h4>How it works</h4>{ul(t["how"])}'
            f'<h4>Step-by-step</h4>{ol(t["steps"])}{code}'
            f'<h4>Common mistakes</h4>{ul(t["mistakes"])}'
            f'<h4>Interview questions and answers</h4>{qa}'
            f'<h4>Hands-on exercise</h4><div class="ex">{E(t["exercise"])}</div>'
            f'<h4>Official and recommended resources</h4>{links(t["res"])}</div>')


def stage_body(n, name, outcome, topics):
    toc = "<ol class='toc'>" + "".join(f"<li>{E(t['t'])}</li>" for t in topics) + "</ol>"
    intro = (f'<h1>Stage {n}: {E(name)}</h1><p><b>Outcome:</b> {E(outcome)}</p>'
             f'<p>This handbook covers each topic of Stage {n} with a definition, why it matters, how it works, step-by-step instructions, '
             'example code or templates, common mistakes, interview questions with answers, a hands-on exercise and official resources.</p>'
             f'<h3>Topics in this stage</h3>{toc}')
    return intro + "".join(topic_html(n, i, t) for i, t in enumerate(topics, 1))


def module_body(num, title, subs):
    toc = "<ol class='toc'>" + "".join(f"<li>{E(sn)} {E(st)}</li>" for sn, st, _ in subs) + "</ol>"
    out = [f'<h1>Module {num}: {E(title)}</h1><p>Every section below explains the concept, how it works, each listed topic in detail, a worked example and where to learn more.</p><h3>Sections</h3>{toc}']
    for sn, st, topics in subs:
        _, _, definition, how, example, res = SEC[sn]
        notes = NOTES[sn]
        tn = "".join(f'<div class="tn"><b>{E(tp)}.</b> {E(nt)}</div>' for tp, nt in zip(topics, notes))
        out.append(f'<div class="topic"><div class="lbl">Module {num} · Section {sn}</div><h2>{E(sn)} {E(st)}</h2>'
                   f'<h4>Definition</h4><div class="def">{E(definition)}</div>'
                   f'<h4>How it works</h4>{ul(how)}'
                   f'<h4>Every topic explained</h4>{tn}'
                   f'<h4>Worked example</h4><div class="ex">{E(example)}</div>'
                   f'<h4>Resources</h4>{links(res)}</div>')
    return "".join(out)


def guide_body():
    stages = "".join(f'<div class="card"><div class="lbl">Stage {n}</div><b>{E(nm)}</b><p class="note">Topics: {E(", ".join(t["t"] for t in tp))}</p><p class="note"><b>Outcome:</b> {E(oc)}</p></div>' for n, nm, oc, tp in STAGES)
    tracks = ""
    for t in TRACKS:
        tracks += (f'<div class="topic"><div class="lbl">Track {t["k"]}</div><h2>{E(t["name"])}</h2><div class="def">{E(t["summary"])}</div>'
                   f'<h4>Who it is for</h4><p>{E(t["who"])}</p><h4>The role</h4><p>{E(t["role"])}</p>'
                   f'<h4>A typical week</h4>{ul(t["day"])}<h4>Skills to build</h4>{ul(t["skills"])}'
                   f'<h4>Modules to prioritise</h4><p>{E(t["modules"])}</p><h4>Portfolio projects</h4>{ul(t["projects"])}'
                   f'<h4>Job titles to search</h4>{ul(t["titles"])}<h4>What interviews test</h4>{ul(t["interview"])}'
                   f'<h4>90-day plan</h4>{ul(t["plan"])}</div>')
    tools = "".join(f"<tr><td>{E(c)}</td><td><b>{E(n)}</b></td><td>{E(w)}</td><td>{E(u)}</td><td>{E(p)}</td><td><a href='{E(l)}'>docs</a></td></tr>" for c, n, w, u, p, l in TOOLS)
    stacks = "".join(f"<h4>{E(a)}</h4><p>{E(b)}</p>" for a, b in STACKS)
    vols = "<ol class='toc'>" + "".join(f"<li>Volume {n}: {E(t)}</li>" for n, t in VOLUMES) + "</ol>"
    jobs = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td><a href='{E(u)}'>{E(u)}</a></td></tr>" for a, b, u in JOBS)
    cmp_rows = [("Understanding business problems", "High", "Medium", "High"), ("Product strategy", "High", "Medium", "Medium–High"), ("Coding", "Usually limited", "High", "High"),
                ("AI development", "Conceptual / technical", "High", "High"), ("Customer interaction", "High", "Variable", "Very high"), ("Deployment", "Coordinates", "Builds and deploys", "Owns customer deployment"),
                ("Business outcomes", "Product outcomes", "Technical outcomes", "Deployment and business outcomes"), ("Architecture", "Product level", "Technical", "Enterprise and application"),
                ("Integration", "Coordinates", "Implements", "Designs and implements"), ("Troubleshooting", "Product issues", "Technical issues", "Customer and production issues")]
    cmp = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in cmp_rows)
    return (f'<h1>Programme guide</h1>'
            '<h2>What a Forward Deployed Engineer is</h2>'
            '<div class="def">A Forward Deployed Engineer (FDE) works directly with customers to understand their problems, then builds, deploys and supports software and AI solutions on the customer\'s own systems and data, and owns the outcome. Palantir popularised the role; AI companies and consultancies such as OpenAI, Anthropic and Accenture now hire for it. It combines software engineering, AI engineering, solutions architecture, product thinking and consulting.</div>'
            '<p>Role definitions vary between companies, so read each job description carefully. Compensation depends on skills, experience, location, employer and proven production work; this programme makes no salary or placement promise.</p>'
            f'<table><tr><th>Dimension</th><th>Product Manager</th><th>AI Engineer</th><th>Forward Deployed Engineer</th></tr>{cmp}</table>'
            '<h2>Who this programme is for</h2><p>Absolute beginners, non-coders, working professionals, graduates, developers, analysts, product managers, consultants and entrepreneurs. It starts from zero and ends at production-ready, customer-facing work, with two outcomes: employment as an FDE or related role, and launching an AI automation agency or B2B AI SaaS.</p>'
            f'<h2>Learning roadmap: seven stages</h2><div class="grid2">{stages}</div>'
            '<p>Each stage has its own detailed handbook (Stage 1 to Stage 7 PDFs). The 14 module handbooks explain every topic in the curriculum.</p>'
            f'<h2>Volume plan</h2>{vols}'
            f'<h2>Four career tracks</h2><p>Choose one track to focus on; the shared foundation is the same.</p>{tracks}'
            f'<div class="topic"><h2>Tool directory: what each tool is and what it is for</h2><p class="note">You do not need every tool. Learn one option per category first, then compare.</p>'
            f'<table><tr><th>Category</th><th>Tool</th><th>What it is</th><th>Used for</th><th>Cost model</th><th>Link</th></tr>{tools}</table>'
            f'<h2>Recommended stacks</h2>{stacks}</div>'
            f'<div class="topic"><h2>Career preparation: job links</h2><p>Use current postings to compare required skills with this curriculum. Postings open and close often; confirm each role is still open.</p>'
            f'<table><tr><th>Organisation</th><th>Role</th><th>Link</th></tr>{jobs}</table>'
            '<h2>How to use these handbooks</h2><ol><li>Read the Programme guide and pick a track.</li><li>Work through the stage handbooks in order; do every exercise.</li>'
            '<li>Use the module handbooks as the reference for any topic.</li><li>Build the three Stage 6 projects at the level that suits you (beginner, intermediate, advanced).</li>'
            '<li>Use Stage 7 to prepare interviews, demos, offers and sales.</li></ol></div>')


def doc(title, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'


def build():
    from playwright.sync_api import sync_playwright
    jobs = [("FDE-00-Programme-Guide.pdf", cover("Programme guide", "AI Forward Deployed Engineer, Enterprise AI Architect & AI Automation Business Handbook", "The role, four career tracks, the seven-stage roadmap, the volume plan, the tool directory and career links."), guide_body())]
    for n, name, oc, tp in STAGES:
        jobs.append((f"FDE-Stage-{n}-{name.split()[0]}.pdf".replace(":", ""), cover(f"Stage {n} handbook", f"Stage {n}: {name}", f"Outcome: {oc}. Topics: " + ", ".join(t["t"] for t in tp) + "."), stage_body(n, name, oc, tp)))
    for num, title, subs in MODULES:
        jobs.append((f"FDE-Module-{int(num):02d}.pdf", cover(f"Module {num} handbook", f"Module {num}: {title}", f"{len(subs)} sections, every topic explained with how it works, examples and resources."), module_body(num, title, subs)))
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        pg = b.new_page()
        for fn, cov, body in jobs:
            pg.set_content(doc(fn, cov + body), wait_until="load")
            pg.pdf(path=os.path.join(OUT, fn), format="A4", print_background=True, display_header_footer=True,
                   header_template="<span></span>", footer_template=FOOTER,
                   margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
            print("built", fn)
        b.close()
    # complete handbook = all PDFs merged
    import pymupdf
    full = pymupdf.open()
    toc = []
    for fn, _, _ in jobs:
        d = pymupdf.open(os.path.join(OUT, fn))
        toc.append([1, fn.replace(".pdf", "").replace("FDE-", "").replace("-", " "), full.page_count + 1])
        full.insert_pdf(d)
    full.set_toc(toc)
    full.save(os.path.join(OUT, "FDE-Complete-Handbook.pdf"), garbage=4, deflate=True)
    print("built complete handbook", full.page_count, "pages")
    return [j[0] for j in jobs] + ["FDE-Complete-Handbook.pdf"]


if __name__ == "__main__":
    build()
