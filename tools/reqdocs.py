"""PRD library (prd-library.html) and BRD & FRD guide (brd-frd.html), plus Word templates."""
import html, os
from urllib.parse import urlencode
from reqdocs_data import (PRD_IDEAS, PRD_SECTIONS, PRD_MISTAKES, PRD_LINKS, BRD_FRD_COMPARE, BRD_SECTIONS,
                          FRD_SECTIONS, BA_TECHNIQUES, BRD_IDEAS, BA_LINKS)
E = html.escape

TYPE = {"SaaS & B2B": "Web product / SaaS", "AI & GenAI products": "AI / GenAI feature", "Fintech & payments": "B2B / fintech",
        "Logistics & supply chain": "Web product / SaaS", "HR tech & jobs": "Web product / SaaS"}
TPL_DIR = "handbook/templates"

CSS = """<style>
.rq-nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px}.rq-nav a{border:1px solid var(--line);background:var(--surface);border-radius:99px;padding:8px 14px;font:600 14px var(--body);text-decoration:none;color:var(--ink)}.rq-nav a:hover{border-color:var(--brand)}
.rq-sec{margin:0 0 40px}.rq-sec>h2{font-size:26px;margin:0 0 6px}.rq-sec>p.sub{margin:0 0 16px;color:var(--mu)}
.rq-tbl{width:100%;border-collapse:collapse;background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;font-size:14.5px}
.rq-tbl th,.rq-tbl td{border-bottom:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}.rq-tbl th{background:var(--surface-2);font-weight:700}.rq-tw{overflow:auto;border-radius:16px}
.rq-tbl td:first-child{font-weight:700;white-space:nowrap}.rq-tbl td.ex{color:var(--mu);font-style:italic}
.rq-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;padding:0;list-style:none}.rq-list li{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.rq-tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 14px}.rq-tools input{flex:1;min-width:220px;border:1px solid var(--line);border-radius:12px;padding:11px 14px;font:inherit;background:var(--surface);color:var(--ink)}
.rq-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}.rq-chips button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:99px;padding:7px 12px;font:600 13.5px var(--body);cursor:pointer}.rq-chips button[aria-pressed=true]{background:var(--brand);color:#fff;border-color:var(--brand)}
.rq-ideas{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.rq-idea{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px}.rq-idea .n{font:700 12px var(--body);color:var(--mu)}
.rq-idea h3{font-size:16.5px;margin:0}.rq-idea p{margin:0;font-size:14.5px;color:var(--mu)}.rq-idea .m{font-size:13.5px}.rq-idea .m b{color:var(--ink)}.rq-idea .tag{font:700 11px var(--body);text-transform:uppercase;letter-spacing:.05em;color:#6C4CF5}
.rq-idea .acts{margin-top:auto;display:flex;gap:8px;flex-wrap:wrap;padding-top:6px}
.rq-links{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}.rq-links a{display:block;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.rq-links a:hover{border-color:var(--brand)}.rq-links b{display:block;color:var(--brand)}.rq-links small{color:var(--mu)}
.rq-cta{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 0}
.rq-count{font-size:14px;color:var(--mu)}
</style>"""

FILTER_JS = """<script>(function(){var q=document.getElementById('rq-q'),ch=document.getElementById('rq-ch'),cards=[].slice.call(document.querySelectorAll('.rq-idea')),cnt=document.getElementById('rq-n'),cur='All';
function run(){var t=(q.value||'').toLowerCase(),n=0;cards.forEach(function(c){var ok=(cur==='All'||c.dataset.ind===cur)&&(!t||c.textContent.toLowerCase().indexOf(t)>-1);c.hidden=!ok;if(ok)n++});cnt.textContent=n+' ideas'}
q.addEventListener('input',run);ch.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;cur=b.dataset.i;[].forEach.call(ch.children,function(x){x.setAttribute('aria-pressed',x===b)});run()});run()})();</script>"""

def links(groups):
    return "".join(f'<h3 style="margin:18px 0 10px">{E(g)}</h3><div class="rq-links">' + "".join(
        f'<a href="{E(u)}"{"" if not u.startswith("http") else " target=\"_blank\" rel=\"noopener\""}><b>{E(n)}{" ↗" if u.startswith("http") else " →"}</b><small>{E(d)}</small></a>' for n, u, d in L) + "</div>" for g, L in groups)

def writer(doc, **kw):
    return "prd-writer.html?" + urlencode({"doc": doc, **kw})

def word_doc(title, sections, intro):
    rows = "".join(f"<h2>{E(h)}</h2><p style='color:#666'><i>{E(g)}</i></p><p>&nbsp;</p>" for h, g, *_ in sections)
    return f"""<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><title>{E(title)}</title>
<style>body{{font-family:Calibri,Arial,sans-serif;font-size:11pt;line-height:1.45}}h1{{font-size:22pt;color:#2E3192}}h2{{font-size:14pt;color:#2E3192;border-bottom:1px solid #ccc}}table{{border-collapse:collapse}}td{{border:1px solid #999;padding:4px 10px}}</style></head>
<body><h1>{E(title)}</h1><p>{E(intro)}</p><table><tr><td>Document owner</td><td></td></tr><tr><td>Version / status</td><td>v0.1 · Draft</td></tr><tr><td>Reviewers / approvers</td><td></td></tr><tr><td>Last updated</td><td></td></tr></table>
{rows}<p style="color:#888;font-size:9pt">Template from SkillNavora · skillnavora.in · Write it faster with the free AI writer: skillnavora.in/prd-writer</p></body></html>"""

def write_templates(out):
    d = os.path.join(out, TPL_DIR); os.makedirs(d, exist_ok=True)
    files = {"SkillNavora_PRD_Template.doc": word_doc("Product Requirements Document (PRD) – <Product name>", PRD_SECTIONS, "Replace the grey guidance under each heading with your content."),
             "SkillNavora_BRD_Template.doc": word_doc("Business Requirements Document (BRD) – <Project name>", BRD_SECTIONS, "Business language only: the why, the goals and the business needs."),
             "SkillNavora_FRD_Template.doc": word_doc("Functional Requirements Document (FRD) – <System name>", FRD_SECTIONS, "Every requirement numbered, testable and traced to a business requirement.")}
    for f, c in files.items(): open(os.path.join(d, f), "w", encoding="utf-8").write(c)
    return files

def prd_library():
    n_ideas = sum(len(v) for v in PRD_IDEAS.values())
    tpl = "".join(f"<tr><td>{E(h)}</td><td>{E(g)}</td><td class='ex'>{E(x)}</td></tr>" for h, g, x in PRD_SECTIONS)
    chips = '<button type="button" data-i="All" aria-pressed="true">All industries</button>' + "".join(f'<button type="button" data-i="{E(k)}" aria-pressed="false">{E(k)}</button>' for k in PRD_IDEAS)
    cards, i = [], 0
    for ind, L in PRD_IDEAS.items():
        for t, p, m in L:
            i += 1
            u = writer("prd", name=t, idea=p, type=TYPE.get(ind, "Consumer mobile app"), goals="Improve: " + m)
            cards.append(f'<article class="rq-idea" data-ind="{E(ind)}"><span class="n">#{i} · <span class="tag">{E(ind)}</span></span><h3>{E(t)}</h3><p>{E(p)}</p><span class="m">North Star: <b>{E(m)}</b></span>'
                         f'<div class="acts"><a class="btn btn-primary btn-sm" href="{E(u)}">✨ Write this PRD with AI</a><a class="btn btn-line btn-sm" href="{E("ai-tutor.html?" + urlencode({"q": "How would I frame the problem, users and success metrics for a PRD on: " + t}))}">Ask the tutor</a></div></article>')
    mist = "".join(f"<li>❌ {E(x)}</li>" for x in PRD_MISTAKES)
    return CSS + f"""<section style="padding-top:28px"><div class="wrap">
<nav class="rq-nav" aria-label="On this page"><a href="#template">PRD template</a><a href="#framing">How to frame it</a><a href="#ideas">{n_ideas} PRD ideas</a><a href="#mistakes">Common mistakes</a><a href="#learn">Learn from the best</a><a href="brd-frd.html">BRD & FRD →</a></nav>
<div class="rq-sec" id="template"><h2>The PRD template, section by section</h2><p class="sub">What each section should answer, with a worked example (SplitKaro, a UPI bill-split app).</p>
<div class="rq-tw"><table class="rq-tbl"><thead><tr><th>Section</th><th>What to write</th><th>Example</th></tr></thead><tbody>{tpl}</tbody></table></div>
<div class="rq-cta"><a class="btn btn-primary" href="{TPL_DIR}/SkillNavora_PRD_Template.doc">Download PRD template (Word)</a><a class="btn btn-line" href="prd-writer.html">✨ Write a PRD with AI</a><a class="btn btn-line" href="handbooks/index.html#pm">PM handbook</a></div></div>
<div class="rq-sec" id="framing"><h2>How to frame a PRD like top PMs</h2><p class="sub">Use this order of thinking before you write a single requirement.</p>
<ul class="rq-list"><li><b>1. Problem before solution.</b> Who is hurting, how often, how do you know? Add data or quotes.</li><li><b>2. One clear goal.</b> A North Star metric with baseline and target, plus guardrails.</li><li><b>3. Say what you won't do.</b> Non-goals stop scope creep.</li><li><b>4. Stories with acceptance criteria.</b> "As a…, I want…, so that…" + Given / When / Then.</li><li><b>5. Edge cases and states.</b> Empty, error, offline, slow network, accessibility.</li><li><b>6. Measure and launch.</b> Experiment design, rollout %, what success looks like in 30/60/90 days.</li><li><b>7. Risks and open questions.</b> Each with an owner and a date.</li><li><b>8. Keep it short and alive.</b> 2–5 pages, link designs and research, update as decisions change.</li></ul></div>
<div class="rq-sec" id="ideas"><h2>{n_ideas} PRD ideas across {len(PRD_IDEAS)} industries</h2><p class="sub">Practise framing PRDs for interviews and portfolios. Click <b>Write this PRD with AI</b> to get a full draft, then improve it yourself.</p>
<div class="rq-tools"><input id="rq-q" type="search" placeholder="Search ideas, e.g. UPI, AI, health…" aria-label="Search ideas"><span class="rq-count" id="rq-n"></span></div>
<div class="rq-chips" id="rq-ch">{chips}</div><div class="rq-ideas">{"".join(cards)}</div></div>
<div class="rq-sec" id="mistakes"><h2>Common PRD mistakes</h2><ul class="rq-list">{mist}</ul></div>
<div class="rq-sec" id="learn"><h2>Learn from the best</h2><p class="sub">Trusted guides, real templates and the apps product teams use to write PRDs.</p>{links(PRD_LINKS)}</div>
</div></section>""" + FILTER_JS, n_ideas

def brd_frd():
    cmp_rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in BRD_FRD_COMPARE)
    brd = "".join(f"<tr><td>{E(h)}</td><td>{E(g)}</td></tr>" for h, g in BRD_SECTIONS)
    frd = "".join(f"<tr><td>{E(h)}</td><td>{E(g)}</td></tr>" for h, g in FRD_SECTIONS)
    tech = "".join(f"<li><b>{E(a)}</b><br><span style='color:var(--mu)'>{E(b)}</span></li>" for a, b in BA_TECHNIQUES)
    doms = sorted({d for _, d, *_ in BRD_IDEAS})
    chips = '<button type="button" data-i="All" aria-pressed="true">All domains</button>' + "".join(f'<button type="button" data-i="{E(k)}" aria-pressed="false">{E(k)}</button>' for k in doms)
    cards = []
    for i, (t, dom, prob, br, fr, kpi) in enumerate(BRD_IDEAS, 1):
        kw = dict(name=t, idea=prob + ". Goal: " + br, users="(infer stakeholders for " + dom + ")", problem=prob, goals=br + "; KPI: " + kpi)
        cards.append(f'<article class="rq-idea" data-ind="{E(dom)}"><span class="n">#{i} · <span class="tag">{E(dom)}</span></span><h3>{E(t)}</h3><p><b>Problem:</b> {E(prob)}</p>'
                     f'<p><b>Business need (BRD):</b> {E(br)}</p><p><b>Key functions (FRD):</b> {E(fr)}</p><span class="m">KPI: <b>{E(kpi)}</b></span>'
                     f'<div class="acts"><a class="btn btn-primary btn-sm" href="{E(writer("brd", **kw))}">✨ Write BRD</a><a class="btn btn-line btn-sm" href="{E(writer("frd", **dict(kw, idea=fr)))}">✨ Write FRD</a></div></article>')
    sample = """<div class="rq-tw"><table class="rq-tbl"><thead><tr><th>ID</th><th>Requirement</th><th>Type</th><th>Traces to</th></tr></thead><tbody>
<tr><td>BR-01</td><td>Eligible personal loans must be approved within 24 hours of a complete application.</td><td>Business (BRD)</td><td>Objective 1</td></tr>
<tr><td>FR-01</td><td>The system shall verify PAN and Aadhaar through e-KYC APIs and show the result within 10 seconds.</td><td>Functional (FRD)</td><td>BR-01</td></tr>
<tr><td>FR-02</td><td>The system shall auto-reject applications with a bureau score below 650 and show the reason code.</td><td>Functional (FRD)</td><td>BR-01</td></tr>
<tr><td>AC-02</td><td><i>Given</i> a bureau score of 640, <i>when</i> the application is submitted, <i>then</i> status = Rejected and reason = "Low credit score".</td><td>Acceptance criteria</td><td>FR-02 → TC-014</td></tr>
</tbody></table></div>"""
    return CSS + f"""<section style="padding-top:28px"><div class="wrap">
<nav class="rq-nav" aria-label="On this page"><a href="#compare">BRD vs FRD vs PRD</a><a href="#brd">BRD template</a><a href="#frd">FRD template</a><a href="#sample">Sample requirements</a><a href="#techniques">BA techniques</a><a href="#ideas">{len(BRD_IDEAS)} project ideas</a><a href="#learn">Learn from the best</a><a href="prd-library.html">PRD library →</a></nav>
<div class="rq-sec" id="compare"><h2>BRD vs FRD vs PRD</h2><p class="sub">Business analysts usually write the BRD first (why and what the business needs), then the FRD (what the system must do). Product managers write PRDs.</p>
<div class="rq-tw"><table class="rq-tbl"><thead><tr><th></th><th>BRD</th><th>FRD</th><th>PRD</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
<div class="rq-cta"><a class="btn btn-primary" href="prd-writer.html?doc=brd">✨ Write a BRD with AI</a><a class="btn btn-primary" href="prd-writer.html?doc=frd">✨ Write an FRD with AI</a></div></div>
<div class="rq-sec" id="brd"><h2>BRD template</h2><div class="rq-tw"><table class="rq-tbl"><thead><tr><th>Section</th><th>What to write</th></tr></thead><tbody>{brd}</tbody></table></div>
<div class="rq-cta"><a class="btn btn-line" href="{TPL_DIR}/SkillNavora_BRD_Template.doc">Download BRD template (Word)</a></div></div>
<div class="rq-sec" id="frd"><h2>FRD template</h2><div class="rq-tw"><table class="rq-tbl"><thead><tr><th>Section</th><th>What to write</th></tr></thead><tbody>{frd}</tbody></table></div>
<div class="rq-cta"><a class="btn btn-line" href="{TPL_DIR}/SkillNavora_FRD_Template.doc">Download FRD template (Word)</a></div></div>
<div class="rq-sec" id="sample"><h2>Sample: from business need to test case</h2><p class="sub">Digital loan origination at an NBFC. Notice how each functional requirement traces back to a business requirement and forward to a test.</p>{sample}</div>
<div class="rq-sec" id="techniques"><h2>Business analysis techniques to use</h2><ul class="rq-list">{tech}</ul>
<div class="rq-cta"><a class="btn btn-line" href="data-science/index.html">Data Science & AI handbook</a><a class="btn btn-line" href="lab.html">Practice Lab (SQL, Excel, Power BI)</a><a class="btn btn-line" href="questions.html#data">Data interview questions</a></div></div>
<div class="rq-sec" id="ideas"><h2>{len(BRD_IDEAS)} BRD / FRD project ideas</h2><p class="sub">Real projects business analysts work on. Write the BRD first, then the FRD, then compare with the template.</p>
<div class="rq-tools"><input id="rq-q" type="search" placeholder="Search projects, e.g. loan, warehouse, GenAI…" aria-label="Search projects"><span class="rq-count" id="rq-n"></span></div>
<div class="rq-chips" id="rq-ch">{chips}</div><div class="rq-ideas">{"".join(cards)}</div></div>
<div class="rq-sec" id="learn"><h2>Learn from the best</h2><p class="sub">The BA standard, trusted templates and the tools analysts use every day.</p>{links(BA_LINKS)}</div>
</div></section>""" + FILTER_JS
