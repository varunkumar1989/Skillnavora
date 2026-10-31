"""Interactive AI Skills Academy: one generator for (a) the page on skillnavora.in (same tab, site header,
details form, Ask AI) and (b) the Claude artifact copy."""
import html, os, re
import course_builder, evals_course as ev, course_context, course_skills, course_brain, course_browser, course_orch, skillsmap, courses_more as M
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
EV = {"slug": "evals", "pdf": "AI_Evals_for_Product_Managers.pdf", "page": "ai-evals.html", "title": "AI Evals for Product Managers", "classes": ev.CLASSES, "qa": ev.QA, "cheat": ev.CHEAT,
      "oneline": "An eval is a repeatable test that measures how well an AI feature does its job on a fixed set of examples, with a clear way to score each answer. It's the quality bar, the launch gate and the product spec for AI."}
CORE = [("context", course_context.COURSE, "Skill 1 of 7"), ("skills", course_skills.COURSE, "Skill 2 of 7"), ("brain", course_brain.COURSE, "Skill 3 of 7"), ("evals", EV, "Skill 5 of 7"), ("browser", course_browser.COURSE, "Skill 6 of 7"), ("orch", course_orch.COURSE, "Skill 7 of 7")]
ADV = [(C["slug"], C, "Advanced AI PM") for C in M.ALL]
ALL = [("builder-tools", course_builder.COURSE, "AI tools")] + CORE + ADV
TABS = [("map", "Start here")] + [(k, "AI Builder Tools" if k == "builder-tools" else C["title"].replace(" for Product Managers", "").replace(" for PMs", "")) for k, C, _ in ALL]
LV = {"basic": "Basic", "intermediate": "Intermediate", "advanced": "Advanced"}

def _a(href, label, site):
    """Link: on the website, internal links stay in the same tab; external ones open a new tab."""
    if href.startswith("http"): return f'<a href="{E(href)}" target="_blank" rel="noopener">{label} ↗</a>'
    return f'<a href="{E(site + href)}"' + ("" if not site.startswith("http") else ' target="_blank" rel="noopener"') + f'>{label}</a>'

def _fix(h, site):
    if not site.startswith("http"): return h
    return re.sub(r'href="(?!https?:|#)([^"]+)"', lambda m: f'href="{site}{m.group(1)}" target="_blank" rel="noopener"', h)

def body(site):
    def course_tab(key, C, label):
        toc = "".join(f'<a href="#{key}-c{i}" class="toc-i"><span class="lv lv-{lv}">{LV[lv]}</span>{E(t)}</a>' for i, (lv, t, *_) in enumerate(C["classes"], 1))
        cls = "".join(f'''<article class="cls" id="{key}-c{i}"><div class="cls-h"><span class="lv lv-{lv}">{LV[lv]} · Class {i}</span><h3>{E(t)}</h3><p class="goal">{E(g)}</p></div><div class="cls-b">{_fix(b, site)}</div>
<div class="take"><b>Key takeaways</b><ul>{"".join(f"<li>{E(x)}</li>" for x in tk)}</ul></div><div class="ex"><b>Practice:</b> {E(ex)}</div></article>''' for i, (lv, t, g, b, tk, ex) in enumerate(C["classes"], 1))
        qa = "".join(f"<details class='qa'><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in C["qa"])
        cheat = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in C["cheat"])
        ext = site.startswith("http")
        btn = lambda h, t, pri=False: f'<a class="btn{" pri" if pri else ""}" href="{E(site + h)}"' + (' target="_blank" rel="noopener"' if ext else "") + f'>{t}{" ↗" if ext else ""}</a>'
        return f'''<section class="tab" id="{key}" hidden><header class="th"><p class="eyebrow">{label} · {len(C["classes"])} classes · basic to advanced</p><h2>{E(C["title"])}</h2><p class="lede">{E(C["oneline"])}</p>
<div class="acts">{btn("handbook/" + C["pdf"], "Download the PDF", True)}{btn(C["page"], "Course page")}{btn("ai-tutor.html", "Ask the AI Tutor")}</div></header>
<div class="grid2"><nav class="toc" aria-label="Classes">{toc}<a href="#{key}-qa" class="toc-i"><span class="lv lv-tool">Prep</span>Interview questions</a></nav><div class="main">{cls}
<article class="cls" id="{key}-cheat"><div class="cls-h"><span class="lv lv-tool">Toolkit</span><h3>Cheat sheet</h3></div><div class="tw"><table>{cheat}</table></div></article>
<article class="cls" id="{key}-qa"><div class="cls-h"><span class="lv lv-tool">Interview prep</span><h3>{len(C["qa"])} interview questions with answers</h3></div>{qa}</article></div></div></section>'''
    path = "".join(f'<li><span class="n">{i}</span><div><b>{E(n)}</b><p>{E(w)}</p><p class="ln">' + " · ".join(_a(h, E(t), site) for t, h in links) + "</p></div></li>" for i, (n, w, links) in enumerate(skillsmap.PATH, 1))
    groups = "".join(f'<details class="grp"{" open" if i < 2 else ""}><summary>{E(g)} <span>({len(items)})</span></summary><div class="tw"><table><tr><th>Capability</th><th>Learn it</th></tr>' + "".join(f'<tr><td><b>{E(c)}</b></td><td>' + " · ".join(_a(h, E(t), site) for t, h in links) + "</td></tr>" for c, links in items) + "</table></div></details>" for i, (g, items) in enumerate(skillsmap.CAT))
    jd = "".join(f'<div class="jd"><h4>{E(r)}</h4><ul>' + "".join(f"<li>{E(x)}</li>" for x in sk) + "</ul></div>" for r, sk, _ in skillsmap.JD)
    cards = "".join(f'<a class="cc" href="#{k}"><span>{E(l)}</span><b>{E(C["title"])}</b></a>' for k, C, l in ALL)
    mp = f'''<section class="tab" id="map"><header class="th"><p class="eyebrow">Start here</p><h2>The AI skills map</h2><p class="lede">A <b>skill</b> is a reusable method; a <b>tool</b> gives access or performs an action; <b>evals, memory and context</b> are parts of the system around them. Learn the seven core skills in order, then go deeper with the advanced AI product courses.</p></header>
<div class="ccs">{cards}</div><h3 class="sh">Learn these first, in this order</h3><ol class="path">{path}</ol><h3 class="sh">Full catalogue</h3><input id="q" type="search" placeholder="Search a skill: RAG, OCR, routing, pricing…" aria-label="Search skills">{groups}
<h3 class="sh">What AI-era job descriptions ask for</h3><div class="jds">{jd}</div></section>'''
    nav = "".join(f'<a href="#{k}" data-t="{k}">{E(n)}</a>' for k, n in TABS)
    foot_link = _a("ai-academy.html", "skillnavora.in/ai-academy", site)
    return (f'<div class="a-wrap"><div class="a-top"><p class="eyebrow">SkillNavora · AI Product Management &amp; GenAI Launchpad</p><h1>AI Skills <span>Academy</span></h1><p>{len(ALL)} courses from basic to advanced: the 7 core AI skills plus advanced AI product management, with illustrated classes, takeaways, practice and interview questions.</p></div>'
            f'<nav class="a-tabs" aria-label="Courses">{nav}</nav>{mp}' + "".join(course_tab(k, C, l) for k, C, l in ALL) + f'<p class="foot">© SkillNavora · {foot_link} · Free PDFs on every course.</p></div>')

def script():
    return ("<script>(function(){var ids=" + repr([k for k, _ in TABS]) + ";var hh=document.querySelector('header.top');if(hh)document.documentElement.style.setProperty('--a-hh',hh.offsetHeight+'px');"
            "function show(){var h=(location.hash||'#map').slice(1),k=ids.indexOf(h)>-1?h:null,el=null;if(!k){el=document.getElementById(h);var t=el&&el.closest('.tab');k=t?t.id:'map'}"
            "document.querySelectorAll('.tab').forEach(function(s){s.hidden=s.id!==k});document.querySelectorAll('nav.a-tabs a').forEach(function(a){a.setAttribute('aria-current',a.dataset.t===k?'true':'false');if(a.dataset.t===k&&a.scrollIntoView)a.scrollIntoView({block:'nearest',inline:'nearest'})});"
            "if(el&&!el.classList.contains('tab'))el.scrollIntoView();else{var w=document.querySelector('.a-wrap');window.scrollTo(0,w&&location.hash?w.offsetTop-10:0)}}"
            "window.addEventListener('hashchange',show);show();var q=document.getElementById('q');q.addEventListener('input',function(){var t=q.value.toLowerCase();document.querySelectorAll('#map .grp').forEach(function(g){var n=0;g.querySelectorAll('tr').forEach(function(r,i){if(!i)return;var ok=!t||r.textContent.toLowerCase().indexOf(t)>-1;r.hidden=!ok;if(ok)n++});g.hidden=!n;if(t)g.open=true})})})();</script>")

EXTRA = ('.ccs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;margin:16px 0 4px}.cc{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 12px}'
         '.cc:hover{border-color:var(--brand)}.cc span{font:700 11px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--brand2)}figure.ill{max-width:100%}figure.ill svg text{font-family:Inter,system-ui,sans-serif}')

def artifact_style():
    s = open(os.path.join(HERE, "academy_style.css")).read().replace(".wrap{", ".a-wrap{").replace(".top{", ".a-top{").replace(".top h1", ".a-top h1").replace(".top h1 span", ".a-top h1 span").replace(".top p", ".a-top p")
    s = s.replace(".ccs{", "/*").replace("figure.ill svg text{font-family:Inter,system-ui,sans-serif}", "*/") if ".ccs{" in s else s
    return s + EXTRA

def _split_rules(css):
    """Split top-level CSS into (selector, body) items; @media blocks returned with nested items."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0: break
        sel = css[i:j].strip(); depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
        inner = css[j + 1:k - 1]; out.append((sel, inner)); i = k
    return out

def site_style():
    """Scope the academy CSS under .acad and map its colour tokens to the website's theme tokens."""
    src = artifact_style()
    keep = []
    for sel, inner in _split_rules(src):
        if sel.startswith(":root") or sel.startswith("body") or "prefers-color-scheme" in sel: continue
        if sel.startswith("@media"):
            nested = "".join(f"{_scope(s2)}{{{b2}}}" for s2, b2 in _split_rules(inner)); keep.append(f"{sel}{{{nested}}}")
        else: keep.append(f"{_scope(sel)}{{{inner}}}")
    tokens = (".acad{--surface2:var(--surface-2,#eef2fa);--brand:#5b4ee8;--brand2:#0e9fb8;--ok:#16a34a;--mid:#d97706;--adv:#db2777;--code:#10142e;--codeink:#e6eaff;"
              "--display:'Plus Jakarta Sans',system-ui,sans-serif;--body:'Inter',system-ui,sans-serif;--mono:ui-monospace,Consolas,monospace;font:15.5px/1.6 var(--body);color:var(--ink);padding-block:10px 40px}"
              "")
    over = (".acad nav.a-tabs{top:var(--a-hh,68px);background:var(--bg,#f5f7fc);z-index:30}.acad .toc{top:calc(var(--a-hh,68px) + 70px)}"
            ".acad .btn.pri{color:#fff}.acad nav.a-tabs a[aria-current=\"true\"]{color:#fff}.acad .path .n{color:#fff}")
    return "<style>" + tokens + "".join(keep) + over + "</style>"

def _scope(sel):
    return ",".join(".acad " + s.strip() if not s.strip().startswith(".acad") else s.strip() for s in sel.split(","))

def site_html():
    return site_style() + '<section class="acad"><div class="wrap">' + body("") + "</div></section>" + script()

def artifact_html():
    return ('<title>SkillNavora AI Skills Academy</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap">\n'
            f"<style>{artifact_style()}</style>\n" + body("https://www.skillnavora.in/") + script())
