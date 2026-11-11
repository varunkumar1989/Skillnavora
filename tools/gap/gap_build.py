"""Builds the course gap PDFs (audit + three supplements) into handbook/gap/ and the review page data."""
import base64, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
from gap_audit import AUDIT, COUNTS
from gap_supplement_a import A_SECTIONS
from gap_supplement_b import B_SECTIONS
from gap_supplement_c import C_SECTIONS

E = lambda t: html.escape(str(t), quote=True)
OUT = os.path.join(ROOT, "handbook", "gap")
LOGO = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "assets", "skillnavora-lockup.png"), "rb").read()).decode()
TAG = "Course gap check: supplement to the Data Science, AI and Data Engineering course. Existing lessons are unchanged."

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
body { font-family: 'Inter','Segoe UI',Arial,sans-serif; color:#1d1b2e; font-size:10pt; line-height:1.5; margin:0; }
h1 { font-size:21pt; color:#2b1a66; margin:0 0 6pt; } h2 { font-size:15pt; color:#2b1a66; margin:16pt 0 6pt; border-bottom:2px solid #e3dff5; padding-bottom:3pt; break-after:avoid; }
h3 { font-size:11.5pt; color:#5a35c8; margin:12pt 0 4pt; break-after:avoid; } h4 { font-size:9pt; color:#0b7a75; text-transform:uppercase; letter-spacing:.04em; margin:7pt 0 2pt; break-after:avoid; }
p { margin:3pt 0 6pt; } ul,ol { margin:2pt 0 6pt; padding-left:16pt; } li { margin:1.5pt 0; } a { color:#5a35c8; word-break:break-word; }
.cover { height:238mm; display:flex; flex-direction:column; justify-content:space-between; padding:8mm 4mm; background:linear-gradient(160deg,#f5f3ff 0%,#fff 55%,#e9fbf8 100%); border-radius:6mm; break-after:page; }
.cover img { height:14mm; }
.cover .kick { font-size:10pt; letter-spacing:.14em; text-transform:uppercase; color:#0b7a75; font-weight:700; }
.cover .sub { font-size:12.5pt; color:#3d3a55; max-width:150mm; } .cover .tag { font-size:10.5pt; font-weight:700; color:#5a35c8; margin-top:10pt; }
.note { font-size:8.6pt; color:#5b5876; }
.topic { break-inside:avoid-page; border:1px solid #e3dff5; border-radius:6pt; padding:7pt 10pt; margin:8pt 0; }
.def { background:#f5f3ff; border-left:4px solid #6a3fd1; padding:5pt 8pt; border-radius:3pt; }
.why { background:#ecfbf8; border-left:4px solid #0b7a75; padding:5pt 8pt; border-radius:3pt; }
.ex { background:#fff7e8; border-left:4px solid #d98a00; padding:5pt 8pt; border-radius:3pt; }
table { width:100%; border-collapse:collapse; font-size:8.4pt; margin:4pt 0 8pt; } th,td { border:1px solid #ddd8f2; padding:3.5pt 5pt; vertical-align:top; text-align:left; } th { background:#f5f3ff; color:#2b1a66; }
tr { break-inside:avoid; }
.COVERED { color:#0a6b2a; font-weight:700; } .PARTIAL { color:#9a5b00; font-weight:700; } .MISSING { color:#b3261e; font-weight:700; }
"""
FOOT = ('<div style="font-size:7.5pt;width:100%;padding:0 15mm;color:#6b6788;display:flex;justify-content:space-between;font-family:Arial">'
        '<span>© SkillNavora · Course gap check</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')


def cover(kicker, title, sub):
    return (f'<section class="cover"><div><img src="{LOGO}" alt="SkillNavora"></div><div><div class="kicker">{E(kicker)}</div>'
            f'<h1 style="font-size:28pt;margin-top:8pt">{E(title)}</h1><div class="sub">{E(sub)}</div><div class="tag">{E(TAG)}</div></div>'
            '<div class="note">Varun Kumar · SkillNavora · skillnavora.in<br>Edition: November 2026. Official links point to the provider\'s own site. The sandbox used to write this could not open them, so check each link before you share it.</div></section>')


def topic(t):
    qa = f'<h4>Interview question</h4><p>{E(t["interview"])}</p>'
    links = "".join(f'<li><a href="{E(u)}">{E(n)}</a></li>' for n, u in t["links"])
    return (f'<div class="topic"><div class="note">{E(t["code"])}</div><h3>{E(t["title"])}</h3>'
            f'<h4>What is it?</h4><div class="def">{E(t["what"])}</div>'
            f'<h4>Why is it important?</h4><div class="why">{E(t["why"])}</div>'
            f'<h4>Where is it used in industry?</h4><p>{E(t["industry"])}</p>'
            f'<h4>How does it work?</h4><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + '</ul>'
            f'<h4>Practical example</h4><div class="ex">{E(t["example"])}</div>'
            f'<h4>Tool or software</h4><p>{E(t["tool"])}</p>'
            f'<h4>Hands-on exercise</h4><p>{E(t["exercise"])}</p>'
            f'<h4>Common mistakes</h4><p>{E(t["mistake"])}</p>{qa}'
            f'<h4>Official and further reading</h4><ul>{links}</ul></div>')


def audit_body():
    rows = "".join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td class="{c}">{c}</td><td>{E(d)}</td><td>{E(e)}</td><td>{E(f)}</td></tr>' for a, b, c, d, e, f in AUDIT)
    summary = (f'<p><b>Summary:</b> {COUNTS["COVERED"]} areas covered, {COUNTS["PARTIAL"]} partly covered, {COUNTS["MISSING"]} missing. '
               'The three supplements fill the missing and partial areas. Existing lessons, PDFs and tabs were not changed.</p>')
    prop = ("<h2>Proposed additions for your approval</h2><p>These are added as supplements, not as edits to existing lessons. You approve each one before any change to the course itself.</p><ul>"
            "<li>Done: a Data Engineering &amp; Cloud track (15 lessons) with PDFs. Still to add: hands-on labs for Airflow, dbt, Spark, Kafka and one cloud.</li>"
            "<li>Done: a Governance, Privacy &amp; Business Consulting track (5 lessons) covering B3, B4 and B5.</li>"
            "<li>Done: Excel automation (B1) as lessons 13 to 16; SQL topics (B2) as lessons 16 to 20; Fabric and Databricks (A10) as Power BI lessons 7 and 8; production Python (B6) as Python lessons 30 and 31; recommenders and regression metrics (B7) as ML lessons 29 and 30; agent APIs, OAuth, MCP and frameworks as Agents lessons 7 to 11.</li>"
            "<li>Done: the eight capstone briefs (C4) as career lesson 8 and the 12-month roadmap (C8) as career lesson 10. A printable workbook and tracker are still to be added.</li>"
            "<li>Partly done: the tools directory and evaluation sheet are in the tools track (lesson 3). Hands-on no-code tutorials for each category are still to be written.</li></ul>")
    return ('<h1>Course gap audit</h1><p>This audit checks the Data Science, AI and Data Engineering master prompt against the existing course, topic by topic. Each row says whether the area is covered, partly covered or missing, and what the supplement adds.</p>'
            + summary + '<h2>Coverage by prompt module</h2>'
            + '<table><tr><th>Prompt module</th><th>Course home</th><th>Status</th><th>What the course covers</th><th>What is missing or partial</th><th>Where the supplement covers it</th></tr>' + rows + '</table>'
            + prop)


def supp_body(title, intro, sections):
    toc = "".join(f'<li>{E(c)} {E(n)}</li>' for c, n, _ in sections for _ in [0])
    body = f'<h1>{E(title)}</h1><p>{E(intro)}</p><h2>Contents</h2><ul>' + "".join(f"<li>{E(c)} · {E(n)}</li>" for c, n, _ in sections) + '</ul>'
    for c, n, items in sections:
        body += f'<h2>{E(c)} {E(n)}</h2>'
        if items and isinstance(items[0], dict):
            body += "".join(topic(t) for t in items)
        else:
            body += '<table><tr><th>Item</th><th>Answer</th></tr>' + "".join(f'<tr><td>{E(q)}</td><td>{E(a)}</td></tr>' for q, a in items) + '</table>'
    return body


def doc(title, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'


def build():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ("Gap-0-Course-Gap-Audit.pdf", cover("Audit", "Course gap audit", "The master prompt checked topic by topic against the existing course, with the status of every area."), audit_body()),
        ("Gap-A-Data-Engineering-Warehousing-Cloud.pdf", cover("Supplement A", "Data Engineering, warehousing, pipelines and cloud", "Fills course Modules 8 to 10 of the master prompt, which the course does not yet have."),
         supp_body("Supplement A: Data Engineering, Warehousing, Pipelines and Cloud", "Each topic explains what it is, why it matters, where it is used, how it works, a worked example, a tool, an exercise, common mistakes, an interview question and official reading.", A_SECTIONS)),
        ("Gap-B-Excel-SQL-Business-Governance-Python.pdf", cover("Supplement B", "Missing Excel, SQL, business, governance and production topics", "Fills the gaps in course Modules 1, 2, 6, 7 and 13, and the governance and business modules of the prompt."),
         supp_body("Supplement B: Gap topics for the existing modules", "Topics the audit marks as partial or missing, written for the same learner and in the same structure as Supplement A.", B_SECTIONS)),
        ("Gap-C-Interviews-Capstones-Roadmap.pdf", cover("Supplement C", "Interviews, capstones, agents, tools and a 12-month roadmap", "Interview questions and scenarios, eight capstone briefs, the 12-month roadmap and the career readiness check."),
         supp_body("Supplement C: Interviews, capstones, agents, tools and roadmap", "The career and assessment material from the master prompt, with answer frameworks and briefs you can build from.", C_SECTIONS)),
    ]
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        pg = b.new_page()
        for fn, cov, body in jobs:
            pg.set_content(doc(fn, cov + body), wait_until="load")
            pg.pdf(path=os.path.join(OUT, fn), format="A4", print_background=True, display_header_footer=True,
                   header_template="<span></span>", footer_template=FOOT, margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
            print("built", fn)
        b.close()
    return [j[0] for j in jobs]


if __name__ == "__main__":
    build()
