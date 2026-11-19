"""Renders the three complete guides three ways from the same lesson data:
  1. website pages: a hub page per guide and one page per lesson (called from tools/aiguides_page.py)
  2. PDF: one printable book per guide (rendered by tools/aihandbook/render_pdf.js)
  3. artifact: the same book as one self-contained HTML file (no external scripts)."""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from md import E

GUIDES = None


def guides():
    global GUIDES
    if GUIDES is None:
        import claude, chatgpt, git
        GUIDES = [claude.GUIDE, chatgpt.GUIDE, git.GUIDE]
    return GUIDES


# One stylesheet used by every output. Colours come from tokens, so light and dark both work.
CSS = """
:root{--g-bg:#ffffff;--g-fg:#14162b;--g-mu:#56607a;--g-line:#e3e6f0;--g-surf:#f6f7fb;--g-acc:#5b36ee;--g-acc-soft:#eeeafd;--g-code-bg:#0f172a;--g-code-fg:#e2e8f0;--g-out-bg:#052e16;--g-out-fg:#dcfce7;--g-warn:#b45309;--g-warn-soft:#fff7ed;--g-tip-soft:#eef7ff;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--g-bg:#0b0d1a;--g-fg:#eef0fa;--g-mu:#a7aec8;--g-line:#262b45;--g-surf:#141829;--g-acc:#a592ff;--g-acc-soft:#221d46;--g-code-bg:#050813;--g-code-fg:#dbe4f5;--g-out-bg:#052e16;--g-out-fg:#dcfce7;--g-warn:#fbbf24;--g-warn-soft:#2a2110;--g-tip-soft:#132238;color-scheme:dark}}
:root[data-theme=dark]{--g-bg:#0b0d1a;--g-fg:#eef0fa;--g-mu:#a7aec8;--g-line:#262b45;--g-surf:#141829;--g-acc:#a592ff;--g-acc-soft:#221d46;--g-code-bg:#050813;--g-code-fg:#dbe4f5;--g-out-bg:#052e16;--g-out-fg:#dcfce7;--g-warn:#fbbf24;--g-warn-soft:#2a2110;--g-tip-soft:#132238;color-scheme:dark}
html,body{background:var(--g-bg);color:var(--g-fg)}
body{margin:0;font:16px/1.65 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;padding:0 max(16px,env(safe-area-inset-left,0px)) 0 max(16px,env(safe-area-inset-right,0px))}
.gw{max-width:860px;margin:0 auto;padding:34px 0 56px}
h1{font-size:clamp(28px,4.4vw,44px);line-height:1.1;margin:6px 0 10px;text-wrap:balance;letter-spacing:-.01em}
h2{font-size:clamp(21px,2.6vw,26px);margin:34px 0 10px;text-wrap:balance}
h3{font-size:18px;margin:22px 0 8px}
p,li{line-height:1.7}
a{color:var(--g-acc)}
.g-kicker{font:700 12px/1.2 Inter,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--g-acc)}
.g-lead{font-size:18px;color:var(--g-mu);max-width:66ch}
.g-meta{font-size:13.5px;color:var(--g-mu);margin-top:8px}
.g-crumb{font-size:13.5px;color:var(--g-mu);margin-bottom:6px}
.g-box{border:1px solid var(--g-line);border-radius:14px;padding:14px 16px;background:var(--g-acc-soft);margin:14px 0}
.g-flow{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:12px 0}
.g-flow span{padding:8px 11px;border-radius:10px;font:600 13.5px/1.3 Inter,system-ui,sans-serif;background:var(--g-surf);border:1px solid var(--g-line)}
.g-flow i{font-style:normal;color:var(--g-mu);font-weight:700}
.g-terms{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:10px 0}
.g-terms div{border:1px solid var(--g-line);border-radius:12px;padding:11px 13px;background:var(--g-surf)}
.g-terms b{display:block;color:var(--g-acc);margin-bottom:3px}
pre{background:var(--g-code-bg);color:var(--g-code-fg);border-radius:12px;padding:13px 15px;overflow:auto;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;margin:8px 0;white-space:pre;max-width:100%}
pre.g-term{background:#0b1220;color:#d6e4ff}
code{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--g-surf);border:1px solid var(--g-line);border-radius:6px;padding:1px 5px}
pre code{background:none;border:0;padding:0;color:inherit}
.g-cap{font:700 12px/1.2 Inter,system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--g-mu);margin-top:12px}
.g-tw{overflow-x:auto;margin:10px 0}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{border:1px solid var(--g-line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--g-surf)}
.g-note{border-radius:12px;padding:12px 14px;margin:14px 0;border:1px solid var(--g-line);background:var(--g-tip-soft)}
.g-warn{background:var(--g-warn-soft);border-color:color-mix(in srgb,var(--g-warn) 45%,var(--g-line))}
.g-info{background:var(--g-tip-soft)}
.g-steps{padding-left:22px}
.g-steps li{margin:6px 0}
.g-menu{font-weight:700;color:var(--g-acc)}
.g-quiz details{border:1px solid var(--g-line);border-radius:12px;padding:10px 14px;margin:8px 0;background:var(--g-surf)}
.g-quiz summary{cursor:pointer;font-weight:700}
.g-nav{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;border-top:1px solid var(--g-line);margin-top:34px;padding-top:16px}
.g-nav a{display:inline-block;padding:10px 14px;border:1px solid var(--g-line);border-radius:999px;text-decoration:none;background:var(--g-surf);max-width:100%}
.g-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:14px 0}
.g-card{display:block;border:1px solid var(--g-line);border-radius:14px;padding:15px 16px;background:var(--g-surf);text-decoration:none;color:inherit}
.g-card b{display:block;font-size:16px;margin:4px 0}
.g-card small{color:var(--g-mu)}
.g-toc li{margin:4px 0}
.g-book .g-part{page-break-before:always;break-before:page}
.g-book .g-lesson{page-break-before:always;break-before:page}
@media print{body{font-size:11.5pt}.gw{padding:0;max-width:none}pre{white-space:pre-wrap;word-break:break-word}.g-card,.g-nav,.g-noprint{display:none}a{color:inherit;text-decoration:none}}
@media (max-width:520px){.gw{padding-top:22px}.g-terms{grid-template-columns:1fr}}
"""


def _blocks(css):
    """Splits CSS into (selector, body) top-level blocks; @media keeps its nested body."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        sel = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        out.append((sel, css[j + 1:k - 1]))
        i = k
    return out


def scope(css, prefix):
    """Prefixes every selector with prefix. Drops html/body rules (they belong to the page, not the guide)
    and keeps :root colour tokens unchanged."""
    res = []
    for sel, body in _blocks(css):
        if not sel:
            continue
        if sel.startswith("@media"):
            res.append(f"{sel}{{{scope(body, prefix)}}}")
        elif sel.startswith(":root"):
            res.append(f"{sel}{{{body}}}")
        elif sel.startswith("html") or sel.startswith("body"):
            continue
        else:
            res.append(", ".join(f"{prefix} {x.strip()}" for x in sel.split(",")) + "{" + body + "}")
    return "".join(res)


SITE_CSS = scope(CSS, "#gsite")


def _flow(steps):
    parts = []
    for i, s in enumerate(steps):
        if i:
            parts.append("<i aria-hidden='true'>&rarr;</i>")
        parts.append(f"<span>{E(s)}</span>")
    return f'<div class="g-flow" role="img" aria-label="{E(" then ".join(steps))}">' + "".join(parts) + "</div>"


def lesson_inner(g, l, idx, total, site_nav=None):
    """One lesson's body. site_nav = (prev, next) tuples of (href, title) for website navigation."""
    s = []
    s.append(f'<div class="g-crumb">{E(g["title"])} &rsaquo; Lesson {idx} of {total} &middot; about {l["minutes"]} minutes</div>')
    s.append(f'<div class="g-kicker">Lesson {idx}</div><h1>{E(l["title"])}</h1><p class="g-lead">{E(l["lead"])}</p>')
    s.append(f'<div class="g-meta">Checked against official sources in {E(g["checked"])}. Lessons build on each other.</div>')
    s.append(f'<div class="g-box"><b>In plain words.</b> {E(l["plain"])}</div>')
    s.append('<h2>Key ideas</h2><div class="g-terms">' + "".join(f"<div><b>{E(t)}</b>{E(d)}</div>" for t, d in l["ideas"]) + "</div>")
    s.append("<h2>How it works</h2>" + _flow(l["flow"]))
    for i, (head, body) in enumerate(l["body"], 1):
        s.append(f'<h2 id="s{i}">{i}. {E(head)}</h2>' + body)
    s.append('<h2>Common mistakes and fixes</h2><div class="g-tw"><table><thead><tr><th>Mistake</th><th>Fix</th></tr></thead><tbody>'
             + "".join(f"<tr><td>{E(m)}</td><td>{E(f)}</td></tr>" for m, f in l["mistakes"]) + "</tbody></table></div>")
    s.append(f'<h2>Practice</h2><ol class="g-steps">' + "".join(f"<li>{E(p)}</li>" for p in l["practice"]) + "</ol>")
    s.append('<h2>Quick check</h2><div class="g-quiz">' + "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in l["quiz"]) + "</div>")
    s.append('<h2>Go further (official sources)</h2><ul>' + "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in l["links"]) + "</ul>")
    return "".join(s)


def lesson_page_body(g, idx):
    """Website version of one lesson, with previous/next navigation."""
    ls = g["lessons"]
    l = ls[idx - 1]
    nav = '<div class="g-nav">'
    nav += (f'<a href="{g["id"]}-{ls[idx-2]["slug"]}.html">&larr; {E(ls[idx-2]["title"])}</a>' if idx > 1 else f'<a href="{g["id"]}-guide.html">&larr; {E(g["title"])}</a>')
    nav += (f'<a href="{g["id"]}-{ls[idx]["slug"]}.html">{E(ls[idx]["title"])} &rarr;</a>' if idx < len(ls) else f'<a href="{g["id"]}-guide.html">Back to the guide &rarr;</a>')
    nav += "</div>"
    return f'<style>{SITE_CSS}</style><div id="gsite"><main class="gw">' + lesson_inner(g, l, idx, len(ls)) + nav + "</main></div>"


def hub_body(g):
    """Website hub for one guide: intro, a lesson grid, the PDF and the artifact."""
    cards = "".join(
        f'<a class="g-card" href="{g["id"]}-{l["slug"]}.html"><small>Lesson {i} &middot; about {l["minutes"]} min</small><b>{E(l["title"])}</b><small>{E(l["lead"][:110].rsplit(" ", 1)[0])}…</small></a>'
        for i, l in enumerate(g["lessons"], 1))
    return (f'<style>{SITE_CSS}</style><div id="gsite"><main class="gw"><div class="g-kicker">Complete guide &middot; checked {E(g["checked"])}</div>'
            f'<h1>{E(g["title"])}</h1><p class="g-lead">{E(g["intro"])}</p>'
            f'<p class="g-meta"><a href="{E(g["pdf"])}" download>Download the PDF guide</a> &middot; <a href="{g["id"]}-complete-guide-interactive.html">Open the interactive version</a></p>'
            f'<h2>Lessons</h2><div class="g-grid">{cards}</div>'
            f'<h2>Sources</h2><p class="g-meta">Checked against: ' + ", ".join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}</a>' for t, u in g["sources"]) + '. Features and menus change; the lesson pages say what was checked.</p></main></div>')


def book_html(g, interactive=False):
    """One self-contained document: cover, contents, every lesson. Used for the PDF and the artifact."""
    ls = g["lessons"]
    toc = "".join(f'<li><a href="#lesson-{i}">{i}. {E(l["title"])}</a> <span class="g-meta">({l["minutes"]} min)</span></li>' for i, l in enumerate(ls, 1))
    parts = [f'<section class="g-part"><div class="g-kicker">{E(g["subtitle"])}</div><h1>{E(g["title"])}</h1><p class="g-lead">{E(g["intro"])}</p>'
             f'<div class="g-box"><b>Checked against official sources in {E(g["checked"])}.</b> Menu names and limits can change. Where a feature is plan-dependent, the lesson says so.</div>'
             f'<h2>Contents</h2><ol class="g-toc">{toc}</ol>'
             f'<p class="g-meta">Sources: ' + ", ".join(f'{E(t)} ({E(u)})' for t, u in g["sources"]) + '</p></section>']
    for i, l in enumerate(ls, 1):
        parts.append(f'<section class="g-lesson" id="lesson-{i}">' + lesson_inner(g, l, i, len(ls)) + "</section>")
    body = "".join(parts)
    if interactive:
        script = """<script>
(function(){
  var KEY='sn-guide-progress-'+document.body.dataset.guide;
  var done={}; try{done=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  document.querySelectorAll('.g-lesson').forEach(function(sec){
    var id=sec.id, btn=document.createElement('button');
    btn.type='button'; btn.className='g-noprint'; btn.style.cssText='margin:6px 0 0;padding:8px 14px;border-radius:999px;border:1px solid var(--g-line);background:var(--g-surf);color:var(--g-fg);font:600 14px Inter,system-ui,sans-serif;cursor:pointer';
    function paint(){btn.textContent=done[id]?'✓ Lesson complete (click to undo)':'Mark lesson complete';}
    btn.addEventListener('click',function(){done[id]=!done[id];try{localStorage.setItem(KEY,JSON.stringify(done))}catch(e){};paint();bar();});
    paint(); var h=sec.querySelector('h1'); if(h) h.after(btn);
  });
  document.querySelectorAll('.g-quiz details').forEach(function(d){d.addEventListener('toggle',function(){});});
  function bar(){var n=Object.keys(done).filter(function(k){return done[k]}).length,t=document.querySelectorAll('.g-lesson').length;var el=document.getElementById('g-progress');if(el)el.textContent=n+' of '+t+' lessons complete (saved in this browser only)';}
  var top=document.getElementById('g-top'); if(top){var p=document.createElement('p');p.id='g-progress';p.className='g-meta';top.appendChild(p);} bar();
})();
</script>"""
    else:
        script = ""
    progress = '<div id="g-top" class="g-noprint"></div>' if interactive else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(g["title"])}</title><meta name="description" content="{E(g["intro"][:150])}">
<style>{CSS}</style></head>
<body data-guide="{E(g["id"])}"><main class="gw g-book">{progress}{body}</main>{script}</body></html>"""


def artifact_html(g):
    """The interactive guide without its own document wrapper (the Artifact skeleton supplies it)."""
    full = book_html(g, interactive=True)
    head_style = full[full.index("<style>"):full.index("</style>") + len("</style>")]
    body = full[full.index("<body"):]
    body = body[body.index(">") + 1:body.rindex("</body>")]
    return ('<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<title>{E(g["title"])}</title>\n' + head_style + "\n" + body)


def write_all(outdir=None):
    """Writes the three guide books to tools/aiguides/out/ (the PDF source and the artifact source)."""
    out = outdir or os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    paths = {}
    for g in guides():
        p = os.path.join(out, f"{g['id']}-guide.html")
        open(p, "w", encoding="utf-8").write(book_html(g))
        q = os.path.join(out, f"{g['id']}-complete-guide-interactive.html")
        open(q, "w", encoding="utf-8").write(book_html(g, interactive=True))
        a = os.path.join(out, f"{g['id']}-artifact.html")
        open(a, "w", encoding="utf-8").write(artifact_html(g))
        paths[g["id"]] = (p, q, a)
    return paths


if __name__ == "__main__":
    print(write_all())
