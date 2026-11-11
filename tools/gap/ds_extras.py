"""Data Science & AI: quick reference, glossary and supplements (data-science-extras.html).

This page replaces the old course gap check. Everything the gap check held is here, in the
AI for Data Engineers (Data Science & AI) programme:
  Quick Reference (PDF 14), Glossary (PDF 15), Supplement A (data engineering and cloud),
  Supplement B (Excel, SQL, business, governance, production Python) and
  Supplement C (interviews, capstones, roadmap) with the printable 12-month tracker (PDF 13).
build_pdfs() writes the six PDFs into handbook/data-science-extras/; build() writes the page.
"""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gap_build as GB
import gap_page as GP
from gap_supplement_a import A_SECTIONS
from gap_supplement_b import B_SECTIONS
from gap_supplement_c import C_SECTIONS
from ds_reference import CHEATS, GLOSSARY, TRACKER

E = lambda t: html.escape(str(t), quote=True)
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = "data-science-extras.html"
DIR = "handbook/data-science-extras"
PDFS = {"reference": f"{DIR}/DS-14-Quick-Reference-and-Cheat-Sheets.pdf",
        "glossary": f"{DIR}/DS-15-Data-Science-and-AI-Glossary.pdf",
        "tracker": f"{DIR}/DS-13-12-Month-Roadmap-Tracker.pdf",
        "toolslab": f"{DIR}/DS-10-AI-and-No-Code-Tools-Lab.pdf",
        "workbook": f"{DIR}/DS-11-Capstone-Projects-and-Portfolio-Workbook.pdf",
        "A": f"{DIR}/DS-Supplement-A-Data-Engineering-Warehousing-Cloud.pdf",
        "B": f"{DIR}/DS-Supplement-B-Excel-SQL-Business-Governance-Python.pdf",
        "C": f"{DIR}/DS-Supplement-C-Interviews-Capstones-Roadmap.pdf"}
TAG = "Part of the AI for Data Engineers (Data Science & AI) programme."
FOOT = ('<div style="font-size:7.5pt;width:100%;padding:0 15mm;color:#6b6788;display:flex;justify-content:space-between;font-family:Arial">'
        '<span>© SkillNavora · Data Science & AI</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
EXTRA_CSS = """
.sheet { break-inside:auto; } .sheet h2 { break-after:avoid; } code { font-family:Consolas,'Courier New',monospace; font-size:8pt; background:#f5f3ff; padding:0 2pt; border-radius:2pt; word-break:break-word; }
.letter { font-size:16pt; color:#5a35c8; margin:12pt 0 3pt; border-bottom:2px solid #e3dff5; break-after:avoid; }
.acr { display:block; color:#0b7a75; font-size:7.6pt; font-weight:700; }
.month { border:1px solid #e3dff5; border-radius:6pt; padding:7pt 10pt; margin:8pt 0; break-inside:avoid; }
.month h3 { margin:0 0 3pt; } .box { display:inline-block; width:8pt; height:8pt; border:1px solid #5a35c8; margin-right:5pt; vertical-align:-1pt; }
.lines { border-bottom:1px solid #ccc; height:14pt; }
"""


def _cover(kicker, title, sub):
    return GB.cover(kicker, title, sub).replace(E(GB.TAG), E(TAG))


# ---------------------------------------------------------------- PDF bodies
def cheats_body():
    out = ['<h1>Quick Reference and Cheat Sheets</h1><p class="note">The formulas, commands and terms used across the course, on one page each. '
           'Exact syntax can differ between tool versions; check the official documentation for your version.</p>']
    for title, intro, rows in CHEATS:
        trs = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td><code>{E(c)}</code></td></tr>" for a, b, c in rows)
        out.append(f'<section class="sheet"><h2>{E(title)}</h2><p>{E(intro)}</p><table><tr><th style="width:22%">Item</th><th style="width:38%">What it does</th><th>Example</th></tr>{trs}</table></section>')
    return "".join(out)


def glossary_body():
    out = [f'<h1>Data Science and AI Glossary</h1><p class="note">{len(GLOSSARY)} terms and acronyms with a simple definition, a real example and related terms, in A to Z order.</p>']
    letter = None
    rows = []
    def flush():
        if rows:
            out.append('<table><tr><th style="width:20%">Term</th><th style="width:34%">Meaning</th><th style="width:28%">Example</th><th>Related</th></tr>' + "".join(rows) + "</table>")
            rows.clear()
    for term, acr, d, ex, rel in GLOSSARY:
        L = term[0].upper()
        if L != letter:
            flush(); letter = L; out.append(f'<div class="letter">{E(L)}</div>')
        a = f'<span class="acr">{E(acr)}</span>' if acr else ""
        rows.append(f"<tr><td><b>{E(term)}</b>{a}</td><td>{E(d)}</td><td>{E(ex)}</td><td>{E(rel)}</td></tr>")
    flush()
    return "".join(out)


def tracker_body():
    out = ['<h1>12-Month Roadmap and Tracker</h1><p class="note">Print this and tick each item as you finish it. Hours are a guide for a learner working alongside a job. '
           'The plan follows the course modules; it makes no promise of employment or salary.</p>']
    for when, focus, modules, hours, tasks, milestone, assessment in TRACKER:
        t = "".join(f'<li style="list-style:none"><span class="box"></span>{E(x)}</li>' for x in tasks)
        out.append(f'<div class="month"><h3>{E(when)}: {E(focus)}</h3><p><b>Study:</b> {E(modules)}. <b>About {hours} hours a week.</b></p>'
                   f'<ul style="padding-left:0">{t}<li style="list-style:none"><span class="box"></span><b>Milestone:</b> {E(milestone)}</li>'
                   f'<li style="list-style:none"><span class="box"></span><b>Assessment:</b> {E(assessment)}</li></ul>'
                   '<p><b>Start date:</b> ________ &nbsp; <b>Finish date:</b> ________ &nbsp; <b>Hours logged:</b> ________</p><div class="lines"></div><div class="lines"></div></div>')
    weeks = "".join(f"<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>" for i in range(1, 53))
    out.append('<h2>Weekly log</h2><table><tr><th style="width:8%">Week</th><th style="width:34%">What I studied</th><th style="width:10%">Hours</th><th style="width:30%">What I built or practised</th><th>Done</th></tr>' + weeks + "</table>")
    return "".join(out)


def build_pdfs():
    from playwright.sync_api import sync_playwright
    out_dir = os.path.join(ROOT, DIR)
    os.makedirs(out_dir, exist_ok=True)
    jobs = [
        ("reference", _cover("PDF 14", "Quick Reference and Cheat Sheets", "Excel, SQL, DAX, Python, pandas, statistics, ML metrics, APIs and MCP, AI and LLM terms, Git and the command line."), cheats_body()),
        ("glossary", _cover("PDF 15", "Data Science and AI Glossary", f"{len(GLOSSARY)} terms and acronyms in plain English, each with an example and related terms."), glossary_body()),
        ("tracker", _cover("PDF 13", "12-Month Roadmap and Tracker", "The beginner roadmap as a printable tracker: monthly goals, milestones, assessments and a weekly log."), tracker_body()),
        ("toolslab", _cover("PDF 10", "AI and No-Code Tools Laboratory", "Setup checklist, the full SkillNavora tutorial for each tool category, the tools directory and the tool evaluation sheet."),
         GB.supp_body("AI and No-Code Tools Laboratory", "Use with the Tools track lessons and the complete tutorials on skillnavora.in.", [s for s in C_SECTIONS if s[0] in ("C11", "C7")])),
        ("workbook", _cover("PDF 11", "Capstone Projects and Portfolio Workbook", "Eight capstone briefs, the portfolio checklist and fill-in templates from project charter to README."),
         GB.supp_body("Capstone Projects and Portfolio Workbook", "Pick a brief, then fill in the templates as you work; they become your write-up.", [s for s in C_SECTIONS if s[0] in ("C4", "C12")])),
        ("A", _cover("Supplement A", "Data Engineering, warehousing, pipelines and cloud", "Data engineering fundamentals, warehousing and lakehouses, orchestration, data quality, cloud, Fabric and Databricks, containers and data architecture."),
         GB.supp_body("Supplement A: Data Engineering, Warehousing, Pipelines and Cloud", "Each topic explains what it is, why it matters, where it is used, how it works, a worked example, a tool, an exercise, common mistakes and an interview question.", A_SECTIONS)),
        ("B", _cover("Supplement B", "Excel, SQL, business, governance and production topics", "Excel automation, SQL extras, business problem-solving, requirements, governance and privacy, production Python, recommendation systems, APIs, Linux and documentation."),
         GB.supp_body("Supplement B: Excel, SQL, Business, Governance and Production Python", "Written for the same learner and in the same structure as Supplement A.", B_SECTIONS)),
        ("C", _cover("Supplement C", "Interviews, capstones, agents, tools and a 12-month roadmap", "Interview questions and scenarios, eight capstone briefs, agents, context engineering, the tools directory, the roadmap and a readiness check."),
         GB.supp_body("Supplement C: Interviews, capstones, agents, tools and roadmap", "Career and assessment material with answer frameworks and briefs you can build from.", C_SECTIONS)),
    ]
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        pg = b.new_page()
        for key, cov, body in jobs:
            fn = os.path.join(ROOT, PDFS[key])
            pg.set_content(GB.doc(os.path.basename(fn), cov + body).replace("</style>", EXTRA_CSS + "</style>", 1), wait_until="load")
            pg.pdf(path=fn, format="A4", print_background=True, display_header_footer=True, header_template="<span></span>",
                   footer_template=FOOT, margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})
            print("built", PDFS[key])
        b.close()


# ---------------------------------------------------------------- web page
def _pdf_btn(key, label):
    return f'<a class="btn btn-primary btn-sm" href="read.html?doc={PDFS[key]}">{E(label)}</a>'


def reference_panel():
    out = []
    for title, intro, rows in CHEATS:
        trs = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td><code>{E(c)}</code></td></tr>" for a, b, c in rows)
        out.append(f'<details class="gt"{" open" if not out else ""} data-search="{E((title + " " + " ".join(r[0] for r in rows)).lower())}"><summary>{E(title)} <em class="meta">({len(rows)})</em></summary>'
                   f'<p>{E(intro)}</p><div style="overflow-x:auto"><table class="qt"><tr><th>Item</th><th>What it does</th><th>Example</th></tr>{trs}</table></div></details>')
    return "".join(out)


def glossary_panel():
    rows = "".join(f'<tr data-search="{E((t + " " + a + " " + d).lower())}"><td><b>{E(t)}</b>' + (f'<br><small>{E(a)}</small>' if a else "")
                   + f'</td><td>{E(d)}</td><td>{E(ex)}</td><td>{E(rel)}</td></tr>' for t, a, d, ex, rel in GLOSSARY)
    return f'<div style="overflow-x:auto"><table class="qt gl"><tr><th>Term</th><th>Meaning</th><th>Example</th><th>Related</th></tr>{rows}</table></div>'


def tracker_panel():
    cards = "".join(
        f'<details class="gt"><summary><span class="gc">{E(w)}</span> {E(f)}</summary><p><b>Study:</b> {E(m)}. About {h} hours a week.</p>'
        f'<ul>{"".join(f"<li>{E(x)}</li>" for x in tasks)}</ul><p><b>Milestone:</b> {E(ms)}</p><p><b>Assessment:</b> {E(a)}</p></details>'
        for w, f, m, h, tasks, ms, a in TRACKER)
    return '<h3 class="gsec">12-month roadmap and tracker</h3>' + cards


def build(page, uhero, out):
    tabs = [("reference", "Quick Reference"), ("glossary", "Glossary"), ("A", "Data Engineering & Cloud"), ("B", "Excel, SQL, Business & Governance"), ("C", "Interviews, Capstones & Roadmap")]
    bars = {"reference": _pdf_btn("reference", "Quick reference and cheat sheets (PDF)"),
            "glossary": _pdf_btn("glossary", "Data Science and AI glossary (PDF)"),
            "A": _pdf_btn("A", "Supplement A (PDF)"), "B": _pdf_btn("B", "Supplement B (PDF)"),
            "C": _pdf_btn("C", "Supplement C (PDF)") + " " + _pdf_btn("tracker", "12-month roadmap tracker (PDF)") + " " + _pdf_btn("toolslab", "AI & no-code tools lab (PDF)") + " " + _pdf_btn("workbook", "Capstone workbook (PDF)")}
    panels = {"reference": reference_panel(), "glossary": glossary_panel(), "A": GP.supp_panel(A_SECTIONS, "A"),
              "B": GP.supp_panel(B_SECTIONS, "B"), "C": tracker_panel() + GP.supp_panel(C_SECTIONS, "C")}
    css = """<style>
.gap-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}.gap-tabs button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:99px;padding:9px 15px;font:600 14px var(--body);cursor:pointer}
.gap-tabs button[aria-selected=true]{background:var(--brand);color:#fff;border-color:var(--brand)}
.gap-search{width:100%;max-width:420px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink);font:500 15px var(--body);margin:0 0 14px}
details.gt{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 14px;margin:8px 0}details.gt>summary{cursor:pointer;font:700 16px var(--display)}
details.gt h4{margin:12px 0 4px;font:700 12px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--teal,#0b7a75)}details.gt p{margin:4px 0 8px}details.gt ul{margin:4px 0 8px;padding-left:20px}
.gc{display:inline-block;font:700 12px var(--body);background:var(--brand-soft,#efeafe);color:var(--brand);border-radius:99px;padding:2px 8px;margin-right:6px}
.ex{background:#fff7e8;color:#3d2a00;border-left:4px solid #d98a00;padding:8px 10px;border-radius:8px}
.gsec{margin:22px 0 4px;font:700 19px var(--display)}table.qt{width:100%;border-collapse:collapse;font-size:14px}
table.qt th,table.qt td{border:1px solid var(--line);padding:8px 9px;text-align:left;vertical-align:top}table.qt th{background:var(--surface)}
table.qt code{font-size:12.5px;white-space:pre-wrap;word-break:break-word}table.gl{min-width:640px}
.pdfbar{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}.gap-hidden{display:none!important}
</style>"""
    bar = '<div class="gap-tabs" role="tablist" id="dsx-bar" aria-label="Data Science and AI extras">' + "".join(
        f'<button role="tab" data-gt="{k}" aria-controls="dsx-{k}" aria-selected="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n) in enumerate(tabs)) + "</div>"
    body = "".join(
        f'<div class="gap-panel" id="dsx-{k}" role="tabpanel"{"" if i == 0 else " hidden"}><div class="pdfbar">{bars[k]}</div>'
        f'<input class="gap-search" type="search" placeholder="Search this tab" aria-label="Search this tab">{panels[k]}</div>'
        for i, (k, _) in enumerate(tabs))
    keys = [k for k, _ in tabs]
    js = ("<script>(function(){var bar=document.getElementById('dsx-bar');if(!bar)return;var tabs=[].slice.call(bar.querySelectorAll('[role=tab]')),keys=" + str(keys).replace("'", '"') + ";"
          "function show(k){tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.gt===k?'true':'false')});document.querySelectorAll('.gap-panel').forEach(function(p){p.hidden=p.id!=='dsx-'+k})}"
          "tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.gt);try{history.replaceState(null,'','#'+t.dataset.gt)}catch(e){}})});"
          "function fromHash(){var h=(location.hash||'#reference').slice(1);if(h==='audit')h='reference';show(keys.indexOf(h)<0?'reference':h)}window.addEventListener('hashchange',fromHash);fromHash();"
          "document.querySelectorAll('.gap-panel').forEach(function(p){var s=p.querySelector('.gap-search');if(!s)return;s.addEventListener('input',function(){var q=s.value.trim().toLowerCase();"
          "p.querySelectorAll('details.gt,tr[data-search]').forEach(function(d){var t=(d.getAttribute('data-search')||d.textContent).toLowerCase();d.classList.toggle('gap-hidden',q&&t.indexOf(q)<0)})})})})();</script>")
    hero = uhero("AI for Data Engineers · Data Science & AI", 'Quick reference, glossary <span class="g">and supplements</span>',
                 "Cheat sheets, a glossary of data and AI terms, the 12-month tracker, and supplements on data engineering, cloud, Excel, SQL, governance, interviews and capstones. Each one is also a PDF.")
    main = f'{css}<section style="padding-top:24px"><div class="wrap"><a class="btn btn-line btn-sm" href="programme-data.html" style="margin:0 0 14px;display:inline-block">← AI for Data Engineers</a>{bar}{body}</div></section>{js}'
    page(PAGE, "Data Science & AI: quick reference, glossary and supplements · SkillNavora",
         "Cheat sheets for Excel, SQL, DAX, Python, pandas, statistics and ML metrics; a data science and AI glossary; a 12-month tracker; and supplements on data engineering, cloud, governance, interviews and capstones.",
         hero + main, "programme-data.html")
    # the old course gap check address forwards here, keeping the supplement tab
    open(os.path.join(out, "course-gap-check.html"), "w", encoding="utf-8").write(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Data Science & AI extras · SkillNavora</title><meta name="robots" content="noindex">'
        f'<link rel="canonical" href="https://www.skillnavora.in/{PAGE[:-5]}"><meta http-equiv="refresh" content="0; url={PAGE}">'
        f'<script>location.replace("{PAGE}"+location.hash)</script></head><body><p>This page moved to <a href="{PAGE}">Data Science & AI: quick reference, glossary and supplements</a>.</p></body></html>')


if __name__ == "__main__":
    build_pdfs()
