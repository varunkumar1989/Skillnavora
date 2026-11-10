"""Review page for the course gap check: audit table, one tab per supplement, every topic expandable, search."""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gap_audit import AUDIT, COUNTS
from gap_supplement_a import A_SECTIONS
from gap_supplement_b import B_SECTIONS
from gap_supplement_c import C_SECTIONS
E = lambda t: html.escape(str(t), quote=True)

PDFS = {"audit": "handbook/gap/Gap-0-Course-Gap-Audit.pdf", "A": "handbook/gap/Gap-A-Data-Engineering-Warehousing-Cloud.pdf",
        "B": "handbook/gap/Gap-B-Excel-SQL-Business-Governance-Python.pdf", "C": "handbook/gap/Gap-C-Interviews-Capstones-Roadmap.pdf"}


def topic_html(t):
    links = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in t["links"])
    how = "".join(f"<li>{E(x)}</li>" for x in t["how"])
    return (f'<details class="gt" data-search="{E((t["title"]+" "+t["what"]).lower())}"><summary><span class="gc">{E(t["code"])}</span> {E(t["title"])}</summary>'
            f'<h4>What is it?</h4><p>{E(t["what"])}</p><h4>Why is it important?</h4><p>{E(t["why"])}</p>'
            f'<h4>Where is it used in industry?</h4><p>{E(t["industry"])}</p><h4>How does it work?</h4><ul>{how}</ul>'
            f'<h4>Practical example</h4><p class="ex">{E(t["example"])}</p><h4>Tool or software</h4><p>{E(t["tool"])}</p>'
            f'<h4>Hands-on exercise</h4><p>{E(t["exercise"])}</p><h4>Common mistakes</h4><p>{E(t["mistake"])}</p>'
            f'<h4>Interview question</h4><p>{E(t["interview"])}</p><h4>Official and further reading</h4><ul>{links}</ul></details>')


def qa_html(items):
    return '<table class="qt"><tr><th>Item</th><th>Answer</th></tr>' + "".join(f'<tr><td>{E(q)}</td><td>{E(a)}</td></tr>' for q, a in items) + '</table>'


def supp_panel(sections, key):
    out = []
    for code, name, items in sections:
        body = "".join(topic_html(t) for t in items) if items and isinstance(items[0], dict) else qa_html(items)
        out.append(f'<h3 class="gsec">{E(code)} {E(name)}</h3>{body}')
    return "".join(out)


def audit_panel():
    rows = "".join(f'<tr data-search="{E((a+" "+b+" "+c+" "+d+" "+e).lower())}"><td>{E(a)}</td><td>{E(b)}</td><td class="st {c}">{c}</td><td>{E(d)}</td><td>{E(e)}</td><td>{E(f)}</td></tr>' for a, b, c, d, e, f in AUDIT)
    return (f'<p class="meta"><b>{COUNTS["COVERED"]}</b> covered · <b>{COUNTS["PARTIAL"]}</b> partly covered · <b>{COUNTS["MISSING"]}</b> missing. '
            'The supplements fill the partial and missing areas. No existing lesson, PDF or tab was changed.</p>'
            '<div style="overflow-x:auto"><table class="at"><tr><th>Prompt module</th><th>Course home</th><th>Status</th><th>What the course covers</th><th>What is missing or partial</th><th>Where the supplement covers it</th></tr>'
            + rows + '</table></div>')


def build(page, uhero, out):
    styles = """<style>
.gap-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}.gap-tabs button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:99px;padding:9px 15px;font:600 14px var(--body);cursor:pointer}
.gap-tabs button[aria-selected=true]{background:var(--brand);color:#fff;border-color:var(--brand)}
.gap-search{width:100%;max-width:420px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink);font:500 15px var(--body);margin:0 0 14px}
details.gt{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 14px;margin:8px 0}details.gt>summary{cursor:pointer;font:700 16px var(--display);list-style-position:outside}
details.gt h4{margin:12px 0 4px;font:700 12px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--teal,#0b7a75)}details.gt p{margin:4px 0 8px}details.gt ul{margin:4px 0 8px;padding-left:20px}
.gc{display:inline-block;font:700 12px var(--body);background:var(--brand-soft,#efeafe);color:var(--brand);border-radius:99px;padding:2px 8px;margin-right:6px}
.ex{background:#fff7e8;color:#3d2a00;border-left:4px solid #d98a00;padding:8px 10px;border-radius:8px}
.gsec{margin:22px 0 4px;font:700 19px var(--display)}table.at,table.qt{width:100%;border-collapse:collapse;font-size:14px;min-width:680px}table.qt{min-width:0}
table.at th,table.at td,table.qt th,table.qt td{border:1px solid var(--line);padding:8px 9px;text-align:left;vertical-align:top}table.at th{background:var(--surface)}
.st{font-weight:700}.COVERED{color:#0a6b2a}.PARTIAL{color:#9a5b00}.MISSING{color:#b3261e}
.pdfbar{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}.gap-hidden{display:none!important}
</style>"""
    tabs = [("audit", "Coverage audit"), ("A", "Data Engineering & Cloud (Supplement A)"), ("B", "Excel, SQL, Business & Governance (Supplement B)"), ("C", "Interviews, Capstones & Roadmap (Supplement C)")]
    bar = '<div class="gap-tabs" role="tablist" id="gap-bar">' + "".join(f'<button role="tab" data-gt="{k}" aria-selected="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n) in enumerate(tabs)) + "</div>"
    panels = {"audit": audit_panel(), "A": supp_panel(A_SECTIONS, "A"), "B": supp_panel(B_SECTIONS, "B"), "C": supp_panel(C_SECTIONS, "C")}
    body = "".join(
        f'<div class="gap-panel" id="gp-{k}" role="tabpanel"{"" if i == 0 else " hidden"}>'
        + (f'<div class="pdfbar"><a class="btn btn-primary btn-sm" href="read.html?doc={PDFS[k]}">Read this supplement as a PDF</a></div>' if k != "audit" else '<div class="pdfbar"><a class="btn btn-primary btn-sm" href="read.html?doc=' + PDFS["audit"] + '">Read the audit as a PDF</a></div>')
        + (f'<input class="gap-search" type="search" placeholder="Search topics in this tab" aria-label="Search topics">' if k != "audit" else "")
        + panels[k] + "</div>" for i, (k, _) in enumerate(tabs))
    js = """<script>(function(){var bar=document.getElementById('gap-bar');if(!bar)return;var tabs=[].slice.call(bar.querySelectorAll('[role=tab]'));
function show(k){tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.gt===k?'true':'false')});document.querySelectorAll('.gap-panel').forEach(function(p){p.hidden=p.id!=='gp-'+k})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.gt);try{history.replaceState(null,'','#'+t.dataset.gt)}catch(e){}})});
function fromHash(){var h=(location.hash||'#audit').slice(1);show(['audit','A','B','C'].indexOf(h)<0?'audit':h)}window.addEventListener('hashchange',fromHash);fromHash();
document.querySelectorAll('.gap-panel').forEach(function(p){var s=p.querySelector('.gap-search');if(!s)return;s.addEventListener('input',function(){var q=s.value.trim().toLowerCase();p.querySelectorAll('details.gt').forEach(function(d){d.classList.toggle('gap-hidden',q!==''&&d.dataset.search.indexOf(q)<0)})})});
})();</script>"""
    hero = uhero("Course gap check · Data Science, AI & Data Engineering", 'What the course <span class="g">covers</span> and what it adds',
                 "The master prompt checked against the existing course, module by module. Every topic opens on this page and as a PDF. Existing lessons and PDFs are unchanged.")
    main = f'{styles}<section style="padding-top:24px"><div class="wrap">{bar}{body}</div></section>{js}'
    page("course-gap-check.html", "Course gap check: Data Science, AI & Data Engineering · SkillNavora",
         "Checks the Data Science, AI and Data Engineering master prompt against the course, with the missing topics added as supplements.", hero + main, "course-gap-check.html")
