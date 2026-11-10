"""Builds the interactive SFMC Academy artifact page (single HTML + PDFs published alongside under pdf/)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sfmc_content import MODULES, LABS
from sfmc_subtopics import SUB
from sfmc_notes_a import NA
from sfmc_notes_b import NB
from sfmc_notes_c import NC
from sfmc_build import CAPSTONES, CAP_SECTIONS, INTERVIEW, ROADMAP, QUICK
from sfmc_page import TOOLS, OTHER

NOTES = {**NA, **NB, **NC}
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")
SITE = "https://skillnavora.in/read.html?doc=handbook/sfmc/"
CAREERS = ["SFMC Email Marketing Specialist", "SFMC Campaign Specialist", "SFMC Developer", "SFMC Consultant", "SFMC Technical Consultant", "SFMC Administrator", "SFMC Automation Specialist", "SFMC Solution Architect", "Salesforce Marketing Cloud Data Specialist", "Marketing Automation Architect"]

data = {
 "modules": [{"n": n, "title": t, "level": lvl, "summary": s, "pdf": f"SFMC-Module-{n:02d}.pdf",
              "lessons": tps,
              "sections": [{"title": sec, "items": [[it, nt] for it, nt in zip(items, NOTES[sec.split()[0]])]} for sec, items in SUB[n]]}
             for n, t, lvl, s, tps in MODULES],
 "labs": LABS, "capstones": CAPSTONES, "cap_sections": CAP_SECTIONS, "interview": INTERVIEW, "roadmap": ROADMAP, "quick": QUICK,
 "tools": [[cat, items] for cat, items in TOOLS], "other": OTHER, "careers": CAREERS,
 "pdfs": [["SFMC-Complete-Handbook.pdf", "Complete handbook (all handbooks in one PDF)"], ["SFMC-01-Master-Handbook.pdf", "Master handbook (all 28 modules)"]]
         + [[f"SFMC-Module-{n:02d}.pdf", f"Module {n}: {t}"] for n, t, *_ in MODULES]
         + [["SFMC-02-SQL-Handbook.pdf", "SQL for SFMC"], ["SFMC-03-AMPscript-and-HTML-Handbook.pdf", "AMPscript, HTML email and CloudPages"],
            ["SFMC-04-Journey-and-Automation-Handbook.pdf", "Journey Builder and Automation Studio"], ["SFMC-05-Interview-Handbook.pdf", "Interview question bank"],
            ["SFMC-06-Capstone-Projects.pdf", "Capstone projects"], ["SFMC-07-12-Month-Roadmap.pdf", "12-month roadmap"], ["SFMC-08-Quick-Reference.pdf", "Quick reference"]],
}

HTML = r"""<title>SFMC Academy</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: sticky tab bar over one reading column; module and topic views replace list views via #hash routing */
:root{--bg:#f6f4fc;--surface:#ffffff;--fg:#1d1a2e;--muted:#5d5878;--line:#e2ddf3;--accent:#0b6fbd;--accent-soft:#e6f1fb;--teal:#0a7a74;--teal-soft:#e5f7f4;--amber:#a86200;--amber-soft:#fff4e2;--code-bg:#1e1b2e;--code-fg:#f1eeff;--on-accent:#ffffff;
--display:"Space Grotesk",system-ui,sans-serif;--body:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12141c;--surface:#1b1e29;--fg:#eceffb;--muted:#aab2cf;--line:#323850;--accent:#7cc0ff;--accent-soft:#1b2b40;--teal:#4fd6c4;--teal-soft:#13302d;--amber:#ffbf5c;--amber-soft:#33270f;--code-bg:#0d0c14;--code-fg:#ece8ff;--on-accent:#0b1a2b;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#12141c;--surface:#1b1e29;--fg:#eceffb;--muted:#aab2cf;--line:#323850;--accent:#7cc0ff;--accent-soft:#1b2b40;--teal:#4fd6c4;--teal-soft:#13302d;--amber:#ffbf5c;--amber-soft:#33270f;--code-bg:#0d0c14;--code-fg:#ece8ff;--on-accent:#0b1a2b;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:15px/1.6 var(--body);margin:0;padding-block:0 48px}
.wrap{max-width:980px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header.hero{background:var(--surface);border-bottom:1px solid var(--line)}header.hero .wrap{padding-block:26px 20px}
.kick{font:700 11.5px/1.3 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--teal)}
h1{font:700 clamp(23px,4vw,32px)/1.18 var(--display);margin:8px 0 8px;text-wrap:balance}
.lead{color:var(--muted);margin:0;max-width:70ch}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--surface)}
nav.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--surface);border-bottom:1px solid var(--line)}
nav.tabs .wrap{display:flex;gap:4px;overflow-x:auto;padding-block:8px}
nav.tabs a{flex:none;padding:8px 13px;border-radius:999px;color:var(--muted);text-decoration:none;font-weight:600;font-size:14px;white-space:nowrap}
nav.tabs a:hover{background:var(--accent-soft);color:var(--fg)}nav.tabs a[aria-current="page"]{background:var(--accent);color:var(--on-accent)}
a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid var(--teal);outline-offset:2px}
main .wrap{padding-block:22px}
h2{font:700 21px/1.3 var(--display);margin:26px 0 10px;text-wrap:balance}h3{font:700 17px/1.3 var(--display);margin:18px 0 6px}
h4{font:700 12px/1.3 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--teal);margin:14px 0 6px}
p{margin:6px 0 10px}.muted{color:var(--muted)}.small{font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:12px}
a.card{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 15px;color:inherit;text-decoration:none;min-width:0;transition:border-color .15s}
a.card:hover{border-color:var(--accent)}.card .lbl{font:700 11.5px/1.2 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.card b{font:700 16.5px/1.3 var(--display)}.card p{margin:0;color:var(--muted);font-size:14px}.card .more{margin-top:auto;font-weight:600;color:var(--accent);font-size:14px}
.back{display:inline-block;margin:0 0 6px;color:var(--accent);font-weight:600;text-decoration:none}
.box{border-radius:10px;padding:10px 13px;margin:6px 0 10px}.def{background:var(--accent-soft)}.why{background:var(--teal-soft)}.ex{background:var(--amber-soft)}
pre{background:var(--code-bg);color:var(--code-fg);border-radius:10px;padding:12px 14px;overflow-x:auto;font:12.5px/1.5 var(--mono);margin:6px 0 12px}
ul,ol{padding-left:22px;margin:4px 0 10px}li{margin:3px 0}
details.topic{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:4px 16px;margin:10px 0;min-width:0;overflow-wrap:anywhere}
pre code{overflow-wrap:normal}
details.topic>summary{cursor:pointer;font:700 16.5px/1.35 var(--display);padding:10px 0}
details.topic[open]>summary{border-bottom:1px solid var(--line);margin-bottom:6px}
.tn{margin:8px 0}.tn b{color:var(--accent)}
.btns{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}
.btn{display:inline-block;padding:8px 14px;border-radius:10px;font:600 14px var(--body);text-decoration:none;border:1.5px solid var(--accent);color:var(--accent);background:transparent;cursor:pointer}
.btn.primary{background:var(--accent);color:var(--on-accent)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:620px}th,td{padding:9px 11px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--accent-soft)}tr:last-child td{border-bottom:0}
.pill{display:inline-block;font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;background:var(--teal-soft);color:var(--teal);margin-right:6px}
.search{width:100%;max-width:440px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--fg);font:500 15px var(--body);margin:4px 0 12px}
.hidden{display:none!important}.tick{width:18px;height:18px;vertical-align:middle;margin-right:6px}
.prog{font-weight:700}
.viewer-bar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:0 0 4px}.vctl{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.viewer-pages{width:100%;max-height:82vh;overflow:auto;border:1px solid var(--line);border-radius:12px;background:#fff;padding:8px;margin:6px 0 14px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
<header class="hero"><div class="wrap">
<div class="kick">SkillNavora · Salesforce Marketing Cloud</div>
<h1>SFMC Academy: the complete Salesforce Marketing Cloud guide</h1>
<p class="lead">Twenty-eight modules from CRM basics to architecture, AI and certification. Every topic is explained, with detailed lessons, code, labs, capstone projects, interview questions and 37 PDF handbooks you can read inside this page. Check product names, editions and certifications on Salesforce's official pages before you rely on them.</p>
</div></header>
<nav class="tabs" aria-label="Academy sections"><div class="wrap" id="tabs"></div></nav>
<main><div class="wrap" id="view" aria-live="polite"></div></main>
<script>
const D = __DATA__;
const SITE = "__SITE__";
const TABS = [["overview","Overview"],["modules","Modules"],["labs","Labs"],["projects","Projects"],["interviews","Interviews"],["roadmap","Roadmap"],["tools","Tools & links"],["pdfs","PDF library"]];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const ul = a => "<ul>" + a.map(x => `<li>${esc(x)}</li>`).join("") + "</ul>";
const ol = a => "<ol>" + a.map(x => `<li>${esc(x)}</li>`).join("") + "</ol>";
const links = r => '<ul>' + r.map(([n,u]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(n)}</a></li>`).join("") + "</ul>";
const pdfBtns = (f, label) => `<div class="btns"><button type="button" class="btn primary" data-view="${esc(f)}">View ${esc(label)} PDF here</button><a class="btn" href="${SITE}${esc(f)}" target="_blank" rel="noopener">Read on skillnavora.in</a></div>`;
const card = (href, lbl, title, text, more="Open →") => `<a class="card" href="#${href}"><span class="lbl">${esc(lbl)}</span><b>${esc(title)}</b>${text ? `<p>${esc(text)}</p>` : ""}<span class="more">${esc(more)}</span></a>`;
let ticks = {}; try { ticks = JSON.parse(localStorage.getItem("sfmc-academy-ticks") || "{}"); } catch (e) {}
const saveTicks = () => { try { localStorage.setItem("sfmc-academy-ticks", JSON.stringify(ticks)); } catch (e) {} };
const totalTopics = D.modules.reduce((a, m) => a + m.sections.reduce((b, s) => b + s.items.length, 0), 0);
const doneCount = () => Object.values(ticks).filter(Boolean).length;

const PDFJS_BASE = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/";
let pdfLib = null;
function loadPdfLib() {
  if (pdfLib) return Promise.resolve(pdfLib);
  return new Promise((resolve, reject) => {
    const s = document.createElement("script"); s.src = PDFJS_BASE + "pdf.min.js";
    s.onload = () => { window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_BASE + "pdf.worker.min.js"; pdfLib = window.pdfjsLib; resolve(pdfLib); };
    s.onerror = () => reject(new Error("the PDF viewer library did not load")); document.head.appendChild(s);
  });
}
async function openViewer(f, box) {
  const stat = box.querySelector(".vstat"), host = box.querySelector(".vcanvas"); let doc = null, n = 1;
  const draw = async () => {
    stat.textContent = "Page " + n + " of " + doc.numPages;
    const page = await doc.getPage(n), base = page.getViewport({scale: 1});
    const vp = page.getViewport({scale: Math.max(260, host.clientWidth - 16) / base.width}), dpr = window.devicePixelRatio || 1;
    const canvas = document.createElement("canvas"); canvas.width = Math.floor(vp.width * dpr); canvas.height = Math.floor(vp.height * dpr);
    canvas.style.width = vp.width + "px"; canvas.style.height = vp.height + "px"; canvas.style.display = "block"; canvas.style.margin = "0 auto";
    await page.render({canvasContext: canvas.getContext("2d"), viewport: vp, transform: dpr !== 1 ? [dpr, 0, 0, dpr, 0, 0] : null}).promise;
    host.innerHTML = ""; host.appendChild(canvas);
  };
  box.querySelector(".vprev").onclick = () => { if (doc && n > 1) { n--; draw(); } };
  box.querySelector(".vnext").onclick = () => { if (doc && n < doc.numPages) { n++; draw(); } };
  try {
    const lib = await loadPdfLib(); const res = await fetch("pdf/" + f);
    if (!res.ok) throw new Error("the file could not be fetched (" + res.status + ")");
    doc = await lib.getDocument({data: new Uint8Array(await res.arrayBuffer())}).promise; await draw();
  } catch (err) { host.innerHTML = ""; stat.textContent = "This PDF could not be shown here: " + err.message + ". Use “Read on skillnavora.in” next to the button."; }
}

function lessonBlock(t, open) {
  const code = t.code ? `<h4>Code example, with line-by-line notes</h4><pre><code>${esc(t.code)}</code></pre>` : "";
  const lic = t.licence ? `<p class="small muted"><b>Licence and edition:</b> ${esc(t.licence)}</p>` : "";
  return `<details class="topic"${open ? " open" : ""}><summary>${esc(t.t)}</summary>
  <h4>What is it?</h4><div class="box def">${esc(t.what)}</div><h4>Why is it important?</h4><div class="box why">${esc(t.why)}</div>
  <h4>How does it work and the steps</h4>${ol(t.how)}<h4>Real-world example</h4><div class="box ex">${esc(t.example)}</div>${code}${lic}
  <h4>Common errors</h4><p>${esc(t.mistake)}</p><h4>Interview question</h4><p>${esc(t.interview)}</p>
  <h4>Hands-on exercise</h4><p>${esc(t.exercise)}</p><h4>Official documentation and further reading</h4>${links(t.links)}</details>`;
}

const V = {
  overview() {
    return `<h2>What this academy covers</h2>
    <div class="box def">Salesforce Marketing Cloud (SFMC) is Salesforce's platform for email, SMS, push, journeys, automation and landing pages. Marketing Cloud Engagement is the product most SFMC professionals work in. Related products (Personalization, Intelligence, Data Cloud, and editions such as Growth and Advanced) have their own names, licences and features. Check them on Salesforce's official pages before you design a solution.</div>
    <p><b>Progress:</b> <span class="prog" id="ov-done">${doneCount()}</span> of ${totalTopics} topics ticked. Ticks are saved in this browser only.</p>
    <div class="grid">
    ${card("modules","28 modules","Study the modules","Every topic explained, detailed lessons, code and exercises.")}
    ${card("labs","20 labs","Practise in labs","Which labs need an SFMC account and which are simulated.")}
    ${card("projects","8 projects","Build capstone projects","Briefs and the portfolio standard.")}
    ${card("interviews","Question bank","Prepare for interviews","Technical, scenario and behavioural questions.")}
    ${card("roadmap","12 months","Follow the roadmap","Stages with study time, milestones and assessments.")}
    ${card("pdfs","37 PDFs","Open the PDF library","Complete handbook, master handbook, 28 module handbooks and 7 focused handbooks.")}
    </div><h2>Career pathways</h2>${ul(D.careers)}
    <h2>Related programmes</h2><ul>${D.other.map(([n,h,d]) => `<li><a href="https://skillnavora.in/${esc(h)}" target="_blank" rel="noopener">${esc(n)}</a>: ${esc(d)}</li>`).join("")}</ul>`;
  },
  modules() {
    return `<h2>Modules</h2><p class="muted">Open a module, then a topic. Search finds modules by title or summary.</p>
    <input class="search" id="mq" type="search" placeholder="Search modules" aria-label="Search modules">
    <div class="grid" id="mgrid">${D.modules.map(m => `<div data-s="${esc((m.title + " " + m.summary).toLowerCase())}">${card("module-" + m.n, "Module " + m.n + " · " + m.level, m.title, m.summary, "Open module →")}</div>`).join("")}</div>`;
  },
  module(n) {
    const m = D.modules.find(x => x.n == n); if (!m) return V.modules();
    const nav = `<div class="btns">${m.n > 1 ? `<a class="btn" href="#module-${m.n-1}">← Module ${m.n-1}</a>` : ""}${m.n < 28 ? `<a class="btn" href="#module-${m.n+1}">Module ${m.n+1} →</a>` : ""}</div>`;
    const lessons = m.lessons.length ? `<h3>Detailed lessons</h3>${m.lessons.map((t,i) => lessonBlock(t, i === 0)).join("")}` : "";
    const secs = m.sections.map((s, si) => `<details class="topic"${si === 0 && !m.lessons.length ? " open" : ""}><summary>${esc(s.title)}: every topic explained (${s.items.length})</summary>${s.items.map(([it, nt], ii) => {
      const id = `m${m.n}-s${si}-i${ii}`;
      return `<div class="tn"><label><input class="tick" type="checkbox" data-id="${id}"${ticks[id] ? " checked" : ""}> <b>${esc(it)}.</b></label> ${esc(nt)}</div>`; }).join("")}</details>`).join("");
    return `<a class="back" href="#modules">← All modules</a><div class="kick">Module ${m.n} · ${esc(m.level)}</div><h2>${esc(m.title)}</h2><p>${esc(m.summary)}</p>${pdfBtns(m.pdf, "Module " + m.n)}${lessons}<h3>Every topic in this module</h3>${secs}${nav}`;
  },
  labs() {
    return `<h2>Practical labs</h2><p class="muted">Labs marked "account" need a provisioned Marketing Cloud account; never practise in production. The others are simulated or paper practice.</p>
    <div class="tablewrap"><table><tr><th>Lab</th><th>Title</th><th>Requirement</th></tr>${D.labs.map(([c,n,k]) => `<tr><td>${esc(c)}</td><td>${esc(n)}</td><td><span class="pill">${k === "account" ? "Account needed" : "Simulated"}</span></td></tr>`).join("")}</table></div>${pdfBtns("SFMC-Module-25.pdf", "labs module")}`;
  },
  projects() {
    return `<h2>Capstone projects</h2>${D.capstones.map(([t,d]) => `<details class="topic"><summary>${esc(t)}</summary><p>${esc(d)}</p></details>`).join("")}<h3>Every project must include</h3>${ol(D.cap_sections)}${pdfBtns("SFMC-06-Capstone-Projects.pdf", "capstone")}`;
  },
  interviews() {
    return `<h2>Interview question bank</h2><p class="muted">Use the module lessons to build your answers. Model answers for every question are not yet written.</p>${D.interview.map(([g, qs]) => `<details class="topic"><summary>${esc(g)} (${qs.length})</summary>${ol(qs)}</details>`).join("")}${pdfBtns("SFMC-05-Interview-Handbook.pdf", "interview")}`;
  },
  roadmap() {
    return `<h2>12-month roadmap</h2><p class="muted">A part-time plan. The programme makes no promise of employment or any salary.</p><div class="tablewrap"><table><tr><th>Stage</th><th>Topics</th><th>Study time</th><th>Milestone</th><th>Assessment</th></tr>${D.roadmap.map(r => "<tr>" + r.map(c => `<td>${esc(c)}</td>`).join("") + "</tr>").join("")}</table></div>
    <h2>Quick reference</h2>${D.quick.map(([a,b]) => `<h3>${esc(a)}</h3><p>${esc(b)}</p>`).join("")}${pdfBtns("SFMC-07-12-Month-Roadmap.pdf", "roadmap")}`;
  },
  tools() {
    return `<h2>SFMC tools and learning links</h2><p class="muted">Official sites are labelled Official; third-party resources are labelled. Check prices and free tiers on the provider's page.</p>${D.tools.map(([cat, items]) => `<h3>${esc(cat)}</h3><div class="grid">${items.map(([n,u,tag,d]) => `<a class="card" href="${esc(u)}" target="_blank" rel="noopener"><span class="lbl">${esc(tag)}</span><b>${esc(n)} ↗</b><p>${esc(d)}</p></a>`).join("")}</div>`).join("")}`;
  },
  pdfs() {
    return `<h2>PDF library</h2><p class="muted">${D.pdfs.length} PDFs. "View here" opens the PDF inside this page.</p>
    <div class="tablewrap"><table><tr><th>Handbook</th><th>Open</th></tr>${D.pdfs.map(([f,l]) => `<tr><td>${esc(l)}</td><td><button type="button" class="btn primary" data-view="${esc(f)}">View here</button> <a class="btn" href="${SITE}${esc(f)}" target="_blank" rel="noopener">Read on site</a></td></tr>`).join("")}</table></div>`;
  },
};

function route() {
  const h = (location.hash || "#overview").slice(1); let tab = h, html;
  if (h.startsWith("module-")) { tab = "modules"; html = V.module(+h.slice(7)); }
  else if (V[h] && TABS.some(t => t[0] === h)) html = V[h]();
  else { tab = "overview"; html = V.overview(); }
  document.getElementById("tabs").innerHTML = TABS.map(([k,n]) => `<a href="#${k}"${k === tab ? ' aria-current="page"' : ""}>${n}</a>`).join("");
  document.getElementById("view").innerHTML = html; window.scrollTo(0, 0);
  const q = document.getElementById("mq");
  if (q) q.addEventListener("input", () => { const v = q.value.trim().toLowerCase(); document.querySelectorAll("#mgrid > div").forEach(d => d.classList.toggle("hidden", v !== "" && d.dataset.s.indexOf(v) < 0)); });
}
document.addEventListener("change", e => { const t = e.target.closest("input.tick"); if (!t) return; ticks[t.dataset.id] = t.checked; saveTicks(); });
document.addEventListener("click", e => {
  const v = e.target.closest("[data-view]"); if (!v) return;
  const f = v.dataset.view, host = v.closest(".btns") || v.parentElement;
  let box = document.getElementById("viewer"); if (box) box.remove();
  box = document.createElement("div"); box.id = "viewer";
  box.innerHTML = `<div class="viewer-bar"><span>${esc(f)}</span><span class="vctl"><button type="button" class="btn vprev">‹ Prev</button> <span class="vstat">Loading…</span> <button type="button" class="btn vnext">Next ›</button></span></div><div class="vcanvas viewer-pages"></div>`;
  (host.closest("tr") ? host.closest(".tablewrap") : host).insertAdjacentElement("afterend", box); openViewer(f, box);
  box.scrollIntoView({behavior: "smooth", block: "start"});
});
window.addEventListener("hashchange", route); route();
</script>
"""

os.makedirs(OUTDIR, exist_ok=True)
out = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")).replace("__SITE__", SITE)
path = os.path.join(OUTDIR, "sfmc_academy.html")
open(path, "w", encoding="utf-8").write(out)
print("written", path, len(out))
