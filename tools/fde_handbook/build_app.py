
"""Build the interactive FDE handbook artifact (single HTML page + PDFs published alongside)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_pdfs as B
from build_curriculum import MODULES, VOLUMES, JOBS, PROJECTS, EXTRA_PDFS, ADDITIONS

stage_files = {n: f"FDE-Stage-{n}-{name.split()[0]}.pdf" for n, name, _, _ in B.STAGES}
data = {
 "tagline": B.TAGLINE,
 "tracks": B.TRACKS,
 "stages": [{"n": n, "name": name, "outcome": oc, "pdf": stage_files[n], "topics": tp} for n, name, oc, tp in B.STAGES],
 "modules": [{"n": int(num), "title": title, "pdf": f"FDE-Module-{int(num):02d}.pdf",
              "sections": [{"id": sn, "title": st, "def": B.SEC[sn][2], "how": B.SEC[sn][3], "example": B.SEC[sn][4], "res": B.SEC[sn][5],
                            "topics": [[tp, nt] for tp, nt in zip(topics, B.NOTES[sn])]} for sn, st, topics in subs]}
             for num, title, subs in MODULES],
 "tools": B.TOOLS, "stacks": B.STACKS, "jobs": JOBS, "volumes": VOLUMES, "additions": ADDITIONS,
 "pdfs": [["FDE-Complete-Handbook.pdf", "Complete handbook (all guides in one PDF, 239 pages)"], ["FDE-00-Programme-Guide.pdf", "Programme guide: role, tracks, roadmap, tools, careers"]]
         + [[stage_files[n], f"Stage {n}: {name}"] for n, name, _, _ in B.STAGES]
         + [[f"FDE-Module-{int(num):02d}.pdf", f"Module {num}: {title}"] for num, title, _ in MODULES],
}
SITE = "https://skillnavora.in/read.html?doc=handbook/fde/"

HTML = r"""<title>FDE Handbook</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: sticky tab bar over a single reading column; detail views replace the list views via #hash routing */
:root{--bg:#f6f4fc;--surface:#ffffff;--fg:#1d1a2e;--muted:#5d5878;--line:#e2ddf3;--accent:#5b37c9;--accent-soft:#efeafe;--teal:#0a7a74;--teal-soft:#e5f7f4;--amber:#a86200;--amber-soft:#fff4e2;--code-bg:#1e1b2e;--code-fg:#f1eeff;--on-accent:#ffffff;
--display:"Space Grotesk",system-ui,sans-serif;--body:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#13111c;--surface:#1c1a29;--fg:#efecfb;--muted:#b3adcf;--line:#353150;--accent:#b7a3ff;--accent-soft:#2a2445;--teal:#4fd6c4;--teal-soft:#13302d;--amber:#ffbf5c;--amber-soft:#33270f;--code-bg:#0d0c14;--code-fg:#ece8ff;--on-accent:#17112e;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13111c;--surface:#1c1a29;--fg:#efecfb;--muted:#b3adcf;--line:#353150;--accent:#b7a3ff;--accent-soft:#2a2445;--teal:#4fd6c4;--teal-soft:#13302d;--amber:#ffbf5c;--amber-soft:#33270f;--code-bg:#0d0c14;--code-fg:#ece8ff;--on-accent:#17112e;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:15px/1.6 var(--body);margin:0;padding-block:0 48px}
.wrap{max-width:980px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header.hero{background:var(--surface);border-bottom:1px solid var(--line)}
header.hero .wrap{padding-block:26px 20px}
.kick{font:700 11.5px/1.3 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--teal)}
h1{font:700 clamp(23px,4vw,32px)/1.18 var(--display);margin:8px 0 8px;text-wrap:balance}
.tag{font-weight:600;color:var(--accent);margin:0 0 6px;max-width:68ch}
.lead{color:var(--muted);margin:0;max-width:68ch}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--surface)}
nav.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--surface);border-bottom:1px solid var(--line)}
nav.tabs .wrap{display:flex;gap:4px;overflow-x:auto;scrollbar-width:thin;padding-block:8px}
nav.tabs a{flex:none;padding:8px 13px;border-radius:999px;color:var(--muted);text-decoration:none;font-weight:600;font-size:14px;white-space:nowrap}
nav.tabs a:hover{background:var(--accent-soft);color:var(--fg)}
nav.tabs a[aria-current="page"]{background:var(--accent);color:var(--on-accent)}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--teal);outline-offset:2px}
main .wrap{padding-block:22px}
h2{font:700 21px/1.3 var(--display);margin:26px 0 10px;text-wrap:balance}
h3{font:700 17px/1.3 var(--display);margin:18px 0 6px}
h4{font:700 12px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--teal);margin:16px 0 6px}
p{margin:6px 0 10px}
.muted{color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:12px}
a.card{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 15px;color:inherit;text-decoration:none;min-width:0;transition:border-color .15s,transform .15s}
a.card:hover{border-color:var(--accent);transform:translateY(-1px)}
.card .lbl{font:700 11.5px/1.2 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.card b{font:700 16.5px/1.3 var(--display)}
.card .more{margin-top:auto;font-weight:600;color:var(--accent);font-size:14px}
.card p{margin:0;color:var(--muted);font-size:14px}
.back{display:inline-block;margin:0 0 6px;color:var(--accent);font-weight:600;text-decoration:none}
.box{border-radius:10px;padding:10px 13px;margin:6px 0 10px}
.def{background:var(--accent-soft)}
.why{background:var(--teal-soft)}
.ex{background:var(--amber-soft)}
pre{background:var(--code-bg);color:var(--code-fg);border-radius:10px;padding:12px 14px;overflow-x:auto;font:12.5px/1.5 var(--mono);margin:6px 0 12px}
ul,ol{padding-left:22px;margin:4px 0 10px}
li{margin:3px 0}
details.topic{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:4px 16px;margin:10px 0}
details.topic>summary{cursor:pointer;font:700 17px/1.35 var(--display);padding:10px 0;list-style-position:outside}
details.topic[open]>summary{border-bottom:1px solid var(--line);margin-bottom:6px}
.qa{margin:6px 0 10px}.qa .q{font-weight:700}
.btns{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}
.btn{display:inline-block;padding:8px 14px;border-radius:10px;font-weight:600;font-size:14px;text-decoration:none;border:1.5px solid var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);color:var(--on-accent)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:640px}
th,td{padding:9px 11px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{font-weight:700;background:var(--accent-soft)}
tr:last-child td{border-bottom:0}
.tn{margin:8px 0}.tn b{color:var(--accent)}
.pill{display:inline-block;font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;background:var(--teal-soft);color:var(--teal);margin-right:6px}
.toolgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,290px),1fr));gap:10px}
.tool{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;min-width:0}
.tool b{font:700 15.5px/1.3 var(--display)}
.tool p{margin:4px 0;font-size:14px}
.filter{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
.filter button{font:600 13px var(--body);padding:6px 11px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}
.filter button[aria-pressed="true"]{background:var(--accent);color:var(--on-accent);border-color:var(--accent)}
.res a{color:var(--accent);overflow-wrap:anywhere}
.small{font-size:13px}
.viewer{width:100%;height:78vh;min-height:360px;border:1px solid var(--line);border-radius:12px;background:#fff;margin:6px 0 14px;display:block}
.viewer-bar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:0 0 4px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
<header class="hero"><div class="wrap">
<div class="kick">SkillNavora · Forward Deployed Engineering</div>
<h1>AI Forward Deployed Engineer, Enterprise AI Architect &amp; AI Automation Business Handbook</h1>
<p class="tag" id="tagline"></p>
<p class="lead">Seven stages, 14 modules, four career tracks, three industry projects and 23 PDF handbooks. Tap any card to open its full detail.</p>
</div></header>
<nav class="tabs" aria-label="Handbook sections"><div class="wrap" id="tabs"></div></nav>
<main><div class="wrap" id="view" aria-live="polite"></div></main>
<script>
const D = __DATA__;
const SITE = "__SITE__";
const TABS = [["overview","Overview"],["tracks","Tracks"],["roadmap","Roadmap"],["modules","Modules"],["projects","Projects"],["tools","Tools"],["careers","Careers"],["pdfs","PDF library"]];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const ul = a => "<ul>" + a.map(x => `<li>${esc(x)}</li>`).join("") + "</ul>";
const ol = a => "<ol>" + a.map(x => `<li>${esc(x)}</li>`).join("") + "</ol>";
const links = r => '<ul class="res">' + r.map(([n,u]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(n)}</a></li>`).join("") + "</ul>";
const pdfBtns = (f, label) => `<div class="btns"><button type="button" class="btn primary" data-view="${esc(f)}">View ${esc(label)} PDF here</button><a class="btn" href="pdf/${esc(f)}" target="_blank" rel="noopener">Open in new tab</a><a class="btn" href="${SITE}${esc(f)}" target="_blank" rel="noopener">Read on skillnavora.in</a></div>`;
const card = (href, lbl, title, text, more="Open details →") => `<a class="card" href="#${href}"><span class="lbl">${esc(lbl)}</span><b>${esc(title)}</b>${text ? `<p>${esc(text)}</p>` : ""}<span class="more">${esc(more)}</span></a>`;

function topicBlock(t, open) {
  const qa = t.qa.map(([q,a]) => `<div class="qa"><div class="q">Q. ${esc(q)}</div><div>A. ${esc(a)}</div></div>`).join("");
  return `<details class="topic"${open ? " open" : ""}><summary>${esc(t.t)}</summary>
  <h4>Definition</h4><div class="box def">${esc(t.what)}</div>
  <h4>Why it matters</h4><div class="box why">${esc(t.why)}</div>
  <h4>How it works</h4>${ul(t.how)}<h4>Step-by-step</h4>${ol(t.steps)}
  ${t.code ? `<h4>Example code / template</h4><pre><code>${esc(t.code)}</code></pre>` : ""}
  <h4>Common mistakes</h4>${ul(t.mistakes)}<h4>Interview questions and answers</h4>${qa}
  <h4>Hands-on exercise</h4><div class="box ex">${esc(t.exercise)}</div><h4>Resources</h4>${links(t.res)}</details>`;
}

const V = {
  overview() {
    const cmp = [["Understanding business problems","High","Medium","High"],["Coding","Usually limited","High","High"],["AI development","Conceptual / technical","High","High"],["Customer interaction","High","Variable","Very high"],["Deployment","Coordinates","Builds and deploys","Owns customer deployment"],["Business outcomes","Product outcomes","Technical outcomes","Deployment and business outcomes"],["Integration","Coordinates","Implements","Designs and implements"],["Troubleshooting","Product issues","Technical issues","Customer and production issues"]];
    return `<h2>What a Forward Deployed Engineer is</h2>
    <div class="box def">A Forward Deployed Engineer (FDE) works directly with customers to understand their problems, then builds, deploys and supports software and AI solutions on the customer's own systems and data, and owns the outcome. It combines software engineering, AI engineering, solutions architecture, product thinking and consulting. Palantir popularised the role; AI companies and consultancies now hire for it.</div>
    <p class="muted small">Role definitions vary between companies. Compensation depends on skills, experience, location and employer; no salary or placement is promised.</p>
    <div class="tablewrap"><table><tr><th>Dimension</th><th>Product Manager</th><th>AI Engineer</th><th>Forward Deployed Engineer</th></tr>${cmp.map(r=>"<tr>"+r.map(c=>`<td>${esc(c)}</td>`).join("")+"</tr>").join("")}</table></div>
    <h2>Start here</h2><div class="grid">
    ${card("tracks","4 career tracks","Choose your track","FDE, Solutions Architect, AI Product Manager, AI Automation Consultant.")}
    ${card("roadmap","7 stages","Follow the roadmap","From programming basics to interviews and launching a business.")}
    ${card("modules","14 modules","Look up any topic","Every topic in the curriculum explained, with examples and resources.")}
    ${card("projects","3 projects","Build industry projects","Real estate, education and financial services, built and deployed.")}
    ${card("tools","48 tools","Know every tool","What each tool is, what it is for, cost model and docs.")}
    ${card("pdfs","23 PDFs","Open the PDF library","Programme guide, 7 stage handbooks, 14 module handbooks and the complete handbook.")}
    </div>
    <h2>Volume plan</h2>${ol(D.volumes.map(([n,t]) => `Volume ${n}: ${t}`))}
    <h2>Additions on top of the original brief</h2>${ul(D.additions)}${pdfBtns("FDE-00-Programme-Guide.pdf","programme guide")}`;
  },
  tracks() {
    return `<h2>Four career tracks</h2><p class="muted">The foundation is shared; each track sets what to study deeply and what to build.</p><div class="grid">${D.tracks.map(t => card("track-" + t.k.toLowerCase(), "Track " + t.k, t.name, t.summary)).join("")}</div>`;
  },
  track(k) {
    const t = D.tracks.find(x => x.k.toLowerCase() === k); if (!t) return V.tracks();
    return `<a class="back" href="#tracks">← All tracks</a><div class="kick">Track ${esc(t.k)}</div><h2>${esc(t.name)}</h2>
    <div class="box def">${esc(t.summary)}</div><h4>Who it is for</h4><p>${esc(t.who)}</p><h4>The role</h4><p>${esc(t.role)}</p>
    <h4>A typical week</h4>${ul(t.day)}<h4>Skills to build</h4>${ul(t.skills)}<h4>Modules to prioritise</h4><p>${esc(t.modules)}</p>
    <h4>Portfolio projects</h4>${ul(t.projects)}<h4>Job titles to search</h4>${ul(t.titles)}<h4>What interviews test</h4>${ul(t.interview)}<h4>90-day plan</h4>${ul(t.plan)}
    ${pdfBtns("FDE-00-Programme-Guide.pdf","programme guide")}`;
  },
  roadmap() {
    return `<h2>Learning roadmap: seven stages</h2><p class="muted">Each stage opens a full handbook: definition, why it matters, how it works, steps, code, mistakes, interview Q&amp;A, exercise and resources for every topic.</p>
    <div class="grid">${D.stages.map(s => card("stage-" + s.n, "Stage " + s.n, s.name, "Topics: " + s.topics.map(t => t.t).join(", ") + ". Outcome: " + s.outcome + ".", "Open stage handbook →")).join("")}</div>`;
  },
  stage(n) {
    const s = D.stages.find(x => x.n == n); if (!s) return V.roadmap();
    const nav = `<div class="btns">${s.n > 1 ? `<a class="btn" href="#stage-${s.n-1}">← Stage ${s.n-1}</a>` : ""}${s.n < 7 ? `<a class="btn" href="#stage-${s.n+1}">Stage ${s.n+1} →</a>` : ""}</div>`;
    return `<a class="back" href="#roadmap">← All stages</a><div class="kick">Stage ${s.n}</div><h2>${esc(s.name)}</h2><p><b>Outcome:</b> ${esc(s.outcome)}</p>${pdfBtns(s.pdf, "Stage " + s.n)}
    <p class="muted small">Tap a topic to expand or collapse it.</p>${s.topics.map((t,i) => topicBlock(t, i === 0)).join("")}${nav}`;
  },
  modules() {
    return `<h2>Complete curriculum: 14 modules</h2><p class="muted">Each module explains every listed topic with how it works, a worked example and resources.</p>
    <div class="grid">${D.modules.map(m => card("module-" + m.n, "Module " + m.n, m.title, m.sections.map(s => s.id + " " + s.title).join(" · "), "Open module →")).join("")}</div>`;
  },
  module(n) {
    const m = D.modules.find(x => x.n == n); if (!m) return V.modules();
    const nav = `<div class="btns">${m.n > 1 ? `<a class="btn" href="#module-${m.n-1}">← Module ${m.n-1}</a>` : ""}${m.n < 14 ? `<a class="btn" href="#module-${m.n+1}">Module ${m.n+1} →</a>` : ""}</div>`;
    return `<a class="back" href="#modules">← All modules</a><div class="kick">Module ${m.n}</div><h2>${esc(m.title)}</h2>${pdfBtns(m.pdf, "Module " + m.n)}
    ${m.sections.map((s,i) => `<details class="topic"${i === 0 ? " open" : ""}><summary>${esc(s.id)} ${esc(s.title)}</summary>
      <h4>Definition</h4><div class="box def">${esc(s.def)}</div><h4>How it works</h4>${ul(s.how)}
      <h4>Every topic explained</h4>${s.topics.map(([tp, nt]) => `<div class="tn"><b>${esc(tp)}.</b> ${esc(nt)}</div>`).join("")}
      <h4>Worked example</h4><div class="box ex">${esc(s.example)}</div><h4>Resources</h4>${links(s.res)}</details>`).join("")}${nav}`;
  },
  projects() {
    const s = D.stages.find(x => x.n == 6);
    return `<h2>Enterprise projects: built and deployed</h2><p class="muted">Each project includes the problem, architecture, build steps, core code, risks, interview questions and beginner, intermediate and advanced versions (under "Hands-on exercise").</p>${pdfBtns(s.pdf, "Stage 6")}
    ${s.topics.map((t,i) => topicBlock(t, i === 0)).join("")}
    <h2>Also in the capstone</h2><p>Choose a business problem and complete discovery, requirements, architecture, database design, APIs, model selection, RAG, agents, frontend, backend, integration, authentication and authorisation, security, testing, evaluation, cloud deployment, monitoring, documentation, a client presentation, an ROI framework and a final demonstration.</p>`;
  },
  tools(cat) {
    const cats = [...new Set(D.tools.map(t => t[0]))];
    const list = D.tools.filter(t => !cat || t[0] === cat);
    return `<h2>Tool directory</h2><p class="muted">What each tool is, what it is used for, how it is priced, and its official documentation. Learn one option per category first.</p>
    <div class="filter" role="group" aria-label="Filter by category"><button type="button" data-cat="" aria-pressed="${!cat}">All</button>${cats.map(c => `<button type="button" data-cat="${esc(c)}" aria-pressed="${c === cat}">${esc(c)}</button>`).join("")}</div>
    <div class="toolgrid">${list.map(([c,n,w,u,p,l]) => `<div class="tool"><span class="pill">${esc(c)}</span><b>${esc(n)}</b><p><b>What it is:</b> ${esc(w)}</p><p><b>Used for:</b> ${esc(u)}</p><p class="muted"><b>Cost:</b> ${esc(p)}</p><p class="res"><a href="${esc(l)}" target="_blank" rel="noopener">Official docs ↗</a></p></div>`).join("")}</div>
    <h2>Recommended stacks</h2>${D.stacks.map(([a,b]) => `<h3>${esc(a)}</h3><p>${esc(b)}</p>`).join("")}`;
  },
  careers() {
    const s = D.stages.find(x => x.n == 7);
    return `<h2>Career and business readiness</h2><p class="muted">Interviews, architecture presentations, discovery, demos, agency packaging, SaaS MVP and sales, each in full detail.</p>${pdfBtns(s.pdf, "Stage 7")}
    ${s.topics.map((t,i) => topicBlock(t, i === 0)).join("")}
    <h2>Job links</h2><p class="muted small">Postings open and close often; confirm each role is still open.</p>
    <div class="tablewrap"><table><tr><th>Organisation</th><th>Role</th><th>Link</th></tr>${D.jobs.map(([a,b,u]) => `<tr><td>${esc(a)}</td><td>${esc(b)}</td><td class="res"><a href="${esc(u)}" target="_blank" rel="noopener">Open posting ↗</a></td></tr>`).join("")}</table></div>`;
  },
  pdfs() {
    return `<h2>PDF library</h2><p class="muted">23 PDFs. "Open" opens the file in a new tab; "Read on skillnavora.in" opens it in the site's reader.</p>
    <div class="tablewrap"><table><tr><th>Handbook</th><th>Open</th></tr>${D.pdfs.map(([f,l]) => `<tr><td>${esc(l)}</td><td><button type="button" class="btn primary" data-view="${esc(f)}">View here</button> <a class="btn" href="pdf/${esc(f)}" target="_blank" rel="noopener">New tab</a> <a class="btn" href="${SITE}${esc(f)}" target="_blank" rel="noopener">Read on site</a></td></tr>`).join("")}</table></div>`;
  },
};

let toolCat = "";
function route() {
  const h = (location.hash || "#overview").slice(1);
  let tab = h, html;
  if (h.startsWith("track-")) { tab = "tracks"; html = V.track(h.slice(6)); }
  else if (h.startsWith("stage-")) { tab = "roadmap"; html = V.stage(+h.slice(6)); }
  else if (h.startsWith("module-")) { tab = "modules"; html = V.module(+h.slice(7)); }
  else if (h === "tools") html = V.tools(toolCat);
  else if (V[h] && TABS.some(t => t[0] === h)) html = V[h]();
  else { tab = "overview"; html = V.overview(); }
  document.getElementById("tabs").innerHTML = TABS.map(([k,n]) => `<a href="#${k}"${k === tab ? ' aria-current="page"' : ""}>${n}</a>`).join("");
  document.getElementById("view").innerHTML = html;
  const cur = document.querySelector('nav.tabs a[aria-current="page"]'); if (cur) cur.scrollIntoView({block: "nearest", inline: "nearest"});
  window.scrollTo(0, 0);
}
document.addEventListener("click", e => {
  const v = e.target.closest("[data-view]");
  if (v) {
    const f = v.dataset.view, host = v.closest(".btns") || v.parentElement;
    let box = document.getElementById("viewer");
    if (box) box.remove();
    box = document.createElement("div"); box.id = "viewer";
    box.innerHTML = `<div class="viewer-bar"><span>${esc(f)}</span><a href="pdf/${esc(f)}" target="_blank" rel="noopener">Open in new tab ↗</a></div><iframe class="viewer" title="${esc(f)}" src="pdf/${esc(f)}"></iframe>`;
    host.insertAdjacentElement("afterend", box);
    box.scrollIntoView({behavior: "smooth", block: "start"});
    return;
  }
  const b = e.target.closest(".filter button"); if (!b) return;
  toolCat = b.dataset.cat; document.getElementById("view").innerHTML = V.tools(toolCat);
});
document.getElementById("tagline").textContent = D.tagline;
window.addEventListener("hashchange", route);
route();
</script>
"""

out = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")).replace("__SITE__", SITE)
path = os.path.join(os.path.dirname(__file__), "fde_curriculum.html")
open(path, "w", encoding="utf-8").write(out)
print("app written", len(out))
