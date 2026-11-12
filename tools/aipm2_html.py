"""HTML for the AI Product Management 2 chapter PDFs and artifact pages, built from aipm2_content."""
import html
from aipm2_content import CHAPTERS, SITE, E, slug, self_check, related
from aipm2_guide import PRACTICE
from aipm2 import extras

PDF_CSS = """@page{size:A4;margin:16mm 15mm}*{box-sizing:border-box}
body{font:10.4pt/1.55 'Segoe UI',Inter,Arial,sans-serif;color:#17202a;margin:0}
h1,h2,h3{font-family:'Segoe UI',Inter,Arial,sans-serif;color:#0b5d52;line-height:1.25;margin:0}
h2{font-size:19pt;margin:0 0 4px}h3{font-size:11.5pt;margin:12px 0 2px;color:#0b5d52}p{margin:4px 0}
.cover{height:265mm;display:flex;flex-direction:column;justify-content:center;background:#0b3f3a;color:#fff;padding:24mm 18mm;border-radius:6px}
.cover .k{letter-spacing:.14em;text-transform:uppercase;font-weight:700;font-size:9.5pt;color:#7fe3cf}
.cover h1{color:#fff;font-size:30pt;margin:8px 0 12px}.cover p{color:#cfe8e2;font-size:12pt}
.chap{page-break-before:always}.lvl{display:inline-block;font-weight:700;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:99px;background:#0f8f7c;color:#fff;margin-bottom:6px}
.goal{color:#4b5a66;margin:4px 0 10px}.topic{border-left:3px solid #bfe9df;padding:2px 0 4px 10px;margin:8px 0;page-break-inside:avoid}
.topic .m{color:#2c3e4a;font-weight:600}.topic .d{margin-top:2px}
table{width:100%;border-collapse:collapse;font-size:9.2pt;margin:6px 0}th,td{border:1px solid #d3e7e2;padding:4px 6px;text-align:left;vertical-align:top}th{background:#e8f6f2;color:#0b5d52}
.box{background:#eefaf7;border:1px solid #bfe9df;border-radius:8px;padding:8px 12px;margin:10px 0;page-break-inside:avoid}
.ex{background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:8px 12px;margin:10px 0;page-break-inside:avoid}
ol,ul{margin:4px 0;padding-left:20px}li{margin:2px 0}.foot{font-size:8pt;color:#7a8791;margin-top:12px}
a{color:#0b5d52}"""

def _meta(s):
    return f"Chapter {s['n']:02d} of {len(CHAPTERS)} · {len(s['topics'])} topics"

def chapter_html(s, with_cover=True):
    """One chapter as a block of HTML (no document wrapper)."""
    topics = "".join(
        f'<div class="topic"><h3>{E(name)}</h3><p class="m">{E(short)}</p><p class="d">{E(detail)}</p></div>'
        for name, short, detail in s["topics"])
    terms = "".join(f"<tr><td><b>{E(name)}</b></td><td>{E(short)}</td></tr>" for name, short, _ in s["topics"])
    checks = "".join(f"<li>{E(q)}</li>" for q in self_check(s))
    rel = "".join(f'<li><a href="{SITE}{E(h)}">{E(t)}</a>: {E(d)}</li>' for h, t, d in related(s["n"]))
    cover = ""
    if with_cover:
        cover = (f'<div class="cover"><div class="k">AI Product Management 2 · Detailed course</div><h1>{E(s["title"])}</h1>'
                 f'<p>{E(s["overview"])}</p><p>{_meta(s)} · Edition 2026 · skillnavora.in</p></div>')
    return (cover + f'<section class="chap"><span class="lvl">Chapter {s["n"]:02d}</span><h2>{E(s["title"])}</h2>'
            f'<p class="goal">{E(s["overview"])}</p>{topics}'
            f'<h3>Summary of terms</h3><table><tr><th>Term</th><th>Meaning</th></tr>{terms}</table>'
            f'<div class="ex"><b>Practice exercise:</b> {E(PRACTICE[s["n"]])}</div>'
            f'<div class="box"><b>Self-check</b><ol>{checks}</ol></div>'
            f'<h3>Related SkillNavora material</h3><ul>{rel}</ul>'
            f'<p class="foot">© SkillNavora · skillnavora.in · Facts and tools change; check official sites before relying on a figure.</p></section>')

def document(title, body):
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{E(title)}</title><style>{PDF_CSS}</style></head><body>{body}</body></html>')

def contents_page():
    rows = "".join(f'<tr><td>{s["n"]:02d}</td><td><b>{E(s["title"])}</b></td><td>{len(s["topics"])}</td></tr>' for s in CHAPTERS)
    total = sum(len(s["topics"]) for s in CHAPTERS)
    return (f'<div class="cover"><div class="k">AI Product Management 2 · Complete edition</div><h1>AI Product Management: complete detailed course</h1>'
            f'<p>{len(CHAPTERS)} chapters · {total} topics · every topic explained, with a practice exercise and a self-check for each chapter.</p></div>'
            f'<section class="chap"><h2>Contents</h2><table><tr><th>Chapter</th><th>Subject</th><th>Topics</th></tr>{rows}</table>'
            f'<h3>How to use this course</h3><p>Read a chapter, write the summary of each topic in your own words, then complete the practice exercise. Use the self-check before moving on, and build the capstone projects in chapter 25 to show your work.</p></section>')

def artifact_page(s):
    """Standalone interactive page for one chapter, with clickable tabs."""
    topics = "".join(
        f'<details class="tp" id="t{i}"><summary>{i}. {E(name)}</summary><p class="m">{E(short)}</p><p>{E(detail)}</p></details>'
        for i, (name, short, detail) in enumerate(s["topics"], 1))
    terms = "".join(f"<tr><td><b>{E(name)}</b></td><td>{E(short)}</td></tr>" for name, short, _ in s["topics"])
    checks = "".join(f"<li>{E(q)}</li>" for q in self_check(s))
    rel = "".join(f'<li><a href="{SITE}{E(h)}" target="_blank" rel="noopener">{E(t)}</a> <span>{E(d)}</span></li>' for h, t, d in related(s["n"]))
    pdf = f"{SITE}handbook/aipm2/{slug(s['n'], s['title'])}.pdf"
    return f"""<meta name="claude:viewport-fit-sides" content="cover">
<title>AI PM {s['n']:02d} {html.escape(s['title'])}</title>
<style>
:root{{--bg:#f6f8f7;--surface:#fff;--fg:#17202a;--muted:#55656f;--line:#d9e4e0;--accent:#0b6e62;--accent-soft:#e3f3ef;--practice:#fff7ed;--practice-line:#fed7aa}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0f1a18;--surface:#17251f;--fg:#e4efeb;--muted:#9ab3ab;--line:#27382f;--accent:#5fd3bf;--accent-soft:#16312b;--practice:#2b2316;--practice-line:#5a4520;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f1a18;--surface:#17251f;--fg:#e4efeb;--muted:#9ab3ab;--line:#27382f;--accent:#5fd3bf;--accent-soft:#16312b;--practice:#2b2316;--practice-line:#5a4520;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px}}
.wrap{{max-width:880px;margin:0 auto}}
.kicker{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 6px}}
h1{{font-size:clamp(24px,4.5vw,32px);line-height:1.2;margin:0 0 8px;text-wrap:balance}}
.lead{{color:var(--muted);margin:0 0 14px;max-width:70ch}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid var(--line);margin:0 0 18px}}
.tabs button{{font-weight:600;font-size:14px;font-family:inherit;background:none;border:0;border-bottom:3px solid transparent;color:var(--muted);padding:10px 12px;cursor:pointer}}
.tabs button[aria-selected="true"]{{color:var(--fg);border-bottom-color:var(--accent)}}
.tabs button:focus-visible,a:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.panel[hidden]{{display:none!important}}
.find{{width:100%;max-width:420px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg);font:inherit;margin:0 0 12px}}
details.tp{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0}}
details.tp summary{{cursor:pointer;font-weight:600}}details.tp p{{margin:6px 0 0}}details.tp .m{{color:var(--accent);font-weight:600}}
table{{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface)}}th,td{{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}th{{background:var(--accent-soft)}}
.ex{{background:var(--practice);border:1px solid var(--practice-line);border-radius:10px;padding:14px 16px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0 0 12px}}
ol,ul{{padding-left:20px}}li{{margin:6px 0}}li span{{color:var(--muted);font-size:14px}}
a{{color:var(--accent)}}.dl{{display:inline-block;margin:8px 0 0;padding:9px 14px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600}}
</style>
<div class="wrap">
<p class="kicker">AI Product Management 2 · Chapter {s['n']:02d} of {len(CHAPTERS)}</p>
<h1>{html.escape(s['title'])}</h1>
<p class="lead">{html.escape(s['overview'])}</p>
<div class="tabs" role="tablist" aria-label="Chapter sections">
<button role="tab" aria-selected="true" aria-controls="p-topics" id="b-topics" data-p="topics">Topics</button>
<button role="tab" aria-selected="false" aria-controls="p-terms" id="b-terms" data-p="terms">Summary of terms</button>
<button role="tab" aria-selected="false" aria-controls="p-practice" id="b-practice" data-p="practice">Practice</button>
<button role="tab" aria-selected="false" aria-controls="p-check" id="b-check" data-p="check">Self-check</button>
<button role="tab" aria-selected="false" aria-controls="p-more" id="b-more" data-p="more">Download and links</button>
</div>
<section class="panel" id="p-topics" role="tabpanel" aria-labelledby="b-topics">
<input class="find" id="find" type="search" placeholder="Filter topics in this chapter" aria-label="Filter topics"><p class="lead" id="cnt"></p>
<div id="tlist">{topics}</div></section>
<section class="panel" id="p-terms" role="tabpanel" aria-labelledby="b-terms" hidden><table><tr><th>Term</th><th>Meaning</th></tr>{terms}</table></section>
<section class="panel" id="p-practice" role="tabpanel" aria-labelledby="b-practice" hidden><div class="ex"><b>Practice exercise</b><p>{html.escape(PRACTICE[s['n']])}</p></div></section>
<section class="panel" id="p-check" role="tabpanel" aria-labelledby="b-check" hidden><div class="card"><b>Self-check</b><ol>{checks}</ol></div></section>
<section class="panel" id="p-more" role="tabpanel" aria-labelledby="b-more" hidden>
<div class="card"><b>Full chapter PDF</b><p class="lead">Print-ready, with every topic, the term summary, the practice exercise and the self-check.</p><a class="dl" href="{pdf}" target="_blank" rel="noopener">Open the chapter PDF ↗</a></div>
<div class="card"><b>Related SkillNavora material</b><ul>{rel}</ul></div></section>
</div>
<script>
(function(){{var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
function show(k){{tabs.forEach(function(t){{var on=t.dataset.p===k;t.setAttribute('aria-selected',on?'true':'false');document.getElementById('p-'+t.dataset.p).hidden=!on}})}}
tabs.forEach(function(t){{t.addEventListener('click',function(){{show(t.dataset.p)}});}});
var f=document.getElementById('find'),c=document.getElementById('cnt');
function run(){{var v=f.value.trim().toLowerCase(),n=0;[].slice.call(document.querySelectorAll('#tlist details')).forEach(function(d){{var m=!v||d.textContent.toLowerCase().indexOf(v)>-1;d.hidden=!m;if(m)n++}});c.textContent=v?n+' matching topics':''}}
f.addEventListener('input',run);}})();
</script>"""
