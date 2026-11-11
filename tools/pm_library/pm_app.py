"""PM Handbook Library artifact: every AI Product Management PDF, clickable, readable inside the page.
Input: data.json (modules, libraries, extra) built from the site's handbook folders. Output: pm_library.html."""
import json, os, sys
DATA, PARTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
D = json.load(open(DATA)); P = json.load(open(PARTS))
for m in D["modules"]:
    for _, d in m["docs"]: d.pop("path", None) if False else None
SITE = "https://skillnavora.in/"
css = P["css"].replace("--accent:#0b6fbd", "--accent:#5b37c9").replace("--accent-soft:#e6f1fb", "--accent-soft:#efeafe")
HTML = "<title>AI Product Management Handbook Library</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n" + css + r"""
<header class="hero"><div class="wrap">
<div class="kicker">SkillNavora · AI Product Management</div>
<h1>AI Product Management Handbook Library</h1>
<p class="lead">Every PM handbook PDF in one place: 31 modules with their chapter PDFs, detailed PDFs and class slides, the libraries, and the complete master handbook. Click any PDF to read it inside this page.</p>
</div></header>
<nav class="tabs" aria-label="Library sections"><div class="wrap" id="tabs"></div></nav>
<main><div class="wrap" id="view" aria-live="polite"></div></main>
<script>
const D = __DATA__;
const SITE = "__SITE__";
const GROUPS = [["core","Product Core","Product Core"],["ai","AI Tools Lab","AI Tools Lab"],["biz","Business AI Stack","Business AI Stack"]];
const TABS = [["overview","Overview"],["core","Product Core (1–12)"],["ai","AI Tools Lab (13–23)"],["biz","Business AI Stack (24–31)"],["libraries","Libraries"],["pdfs","All PDFs"]];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const card = (href, lbl, title, text, more="Open →") => `<a class="card" href="#${href}"><span class="lbl">${esc(lbl)}</span><b>${esc(title)}</b>${text ? `<p>${esc(text)}</p>` : ""}<span class="more">${esc(more)}</span></a>`;
const docRow = (label, d) => `<div class="topic" style="padding:12px 16px"><div class="kick">${esc(label)} · ${d.pages} pages · ${d.mb} MB</div>
  <div class="btns"><button type="button" class="btn primary" data-view="${esc(d.file)}">View ${esc(label)} here</button><a class="btn" href="${SITE}read.html?doc=${esc(d.site)}" target="_blank" rel="noopener">Read on skillnavora.in</a></div>
  ${d.toc.length ? `<details><summary class="small muted" style="cursor:pointer">What is inside (${d.toc.length})</summary><ol>${d.toc.map(t => `<li>${esc(t)}</li>`).join("")}</ol></details>` : `<p class="small muted">Slide deck (images); open it to read the slides.</p>`}</div>`;
""" + P["viewer"] + r"""
const groupOf = k => GROUPS.find(g => g[0] === k)[1];
const V = {
  overview() {
    const n = D.modules.reduce((a, m) => a + m.docs.length, 0) + D.libraries.length + D.extra.length;
    return `<h2>What is in the library</h2><div class="box def">The Product Management Master Handbook by Varun Kumar: 12 Product Core modules, an 11-module AI Tools Lab and the 8-chapter Business AI Stack, with detailed PDFs and class slides for the core modules, five libraries and the complete handbook. ${n} PDFs in total.</div>
    <div class="grid">${card("core","Modules 1–12","Product Core","Chapter, detailed PDF, class slides and interactive handbook for each module.")}
    ${card("ai","Modules 13–23","AI Tools Lab","Claude, Claude Code, Lovable, Replit, Figma, Notion, automation, chatbots and voice agents.")}
    ${card("biz","Modules 24–31","Business AI Stack","Dashboards, CRM, WhatsApp, deployment, Jira, digital marketing and lead generation.")}
    ${card("libraries","5 libraries","Libraries","Frameworks, case studies, projects, interviews and the AI tools lab.")}
    ${card("pdfs", n + " PDFs","All PDFs","Every PDF in one list, each opens inside this page.")}</div>
    <h2>Complete handbook and guides</h2>${D.extra.map(e => docRow(e.title, e.doc)).join("")}`;
  },
  group(k) {
    const g = groupOf(k), mods = D.modules.filter(m => m.group === g);
    return `<h2>${esc(g)}</h2><div class="grid">${mods.map(m => card("module-" + m.n, "Module " + m.n + " · " + m.docs.length + " PDFs", m.title, m.docs.map(d => d[0]).join(" · "), "Open module →")).join("")}</div>`;
  },
  module(n) {
    const m = D.modules.find(x => x.n == n); if (!m) return V.overview();
    const k = GROUPS.find(g => g[1] === m.group)[0];
    const lab = m.lab ? `<p><a class="btn" href="${SITE}${esc(m.lab)}" target="_blank" rel="noopener">Open the interactive handbook for Module ${m.n} ↗</a></p>` : "";
    const nav = `<div class="btns">${m.n > 1 ? `<a class="btn" href="#module-${m.n-1}">← Module ${m.n-1}</a>` : ""}${m.n < 31 ? `<a class="btn" href="#module-${m.n+1}">Module ${m.n+1} →</a>` : ""}</div>`;
    return `<a class="back" href="#${k}">← ${esc(m.group)}</a><div class="kick">Module ${m.n} · ${esc(m.group)}</div><h2>${esc(m.title)}</h2>${lab}${m.docs.map(([l, d]) => docRow(l, d)).join("")}${nav}`;
  },
  libraries() { return `<h2>Libraries</h2>${D.libraries.map(l => `<h3>${esc(l.title)}</h3><p class="muted">${esc(l.desc)}</p>${docRow(l.title, l.doc)}`).join("")}`; },
  pdfs() {
    const rows = [];
    D.modules.forEach(m => m.docs.forEach(([l, d]) => rows.push([`Module ${m.n}: ${m.title}`, l, d])));
    D.libraries.forEach(l => rows.push(["Library", l.title, l.doc])); D.extra.forEach(e => rows.push(["Handbook", e.title, e.doc]));
    return `<h2>All PDFs (${rows.length})</h2><input class="search" id="pq" type="search" placeholder="Search PDFs" aria-label="Search PDFs">
    <div class="tablewrap"><table><tr><th>Module or group</th><th>PDF</th><th>Pages</th><th>Open</th></tr>${rows.map(([a,b,d]) => `<tr data-s="${esc((a+" "+b).toLowerCase())}"><td>${esc(a)}</td><td>${esc(b)}</td><td>${d.pages}</td><td class="btns" style="margin:0"><button type="button" class="btn primary" data-view="${esc(d.file)}">View here</button> <a class="btn" href="${SITE}read.html?doc=${esc(d.site)}" target="_blank" rel="noopener">On site</a></td></tr>`).join("")}</table></div>`;
  },
};
function route() {
  const h = (location.hash || "#overview").slice(1); let tab = h, html;
  if (h.startsWith("module-")) { const m = D.modules.find(x => x.n == +h.slice(7)); tab = m ? GROUPS.find(g => g[1] === m.group)[0] : "overview"; html = V.module(+h.slice(7)); }
  else if (GROUPS.some(g => g[0] === h)) html = V.group(h);
  else if (V[h] && TABS.some(t => t[0] === h)) html = V[h]();
  else { tab = "overview"; html = V.overview(); }
  document.getElementById("tabs").innerHTML = TABS.map(([k,n]) => `<a href="#${k}"${k === tab ? ' aria-current="page"' : ""}>${n}</a>`).join("");
  document.getElementById("view").innerHTML = html; window.scrollTo(0, 0);
  const q = document.getElementById("pq");
  if (q) q.addEventListener("input", () => { const v = q.value.trim().toLowerCase(); document.querySelectorAll("tr[data-s]").forEach(r => r.classList.toggle("hidden", v !== "" && r.dataset.s.indexOf(v) < 0)); });
}
document.addEventListener("click", e => {
  const v = e.target.closest("[data-view]"); if (!v) return;
  const f = v.dataset.view; let box = document.getElementById("viewer"); if (box) box.remove();
  box = document.createElement("div"); box.id = "viewer";
  box.innerHTML = `<div class="viewer-bar"><span>${esc(f)}</span><span class="vctl"><button type="button" class="btn vprev">‹ Prev</button> <span class="vstat">Loading…</span> <button type="button" class="btn vnext">Next ›</button></span></div><div class="vcanvas viewer-pages"></div>`;
  const anchor = v.closest(".tablewrap") || v.closest(".topic") || v.parentElement; anchor.insertAdjacentElement("afterend", box);
  openViewer(f, box); box.scrollIntoView({behavior: "smooth", block: "start"});
});
window.addEventListener("hashchange", route); route();
</script>
"""
for m in D["modules"]:
    for _, d in m["docs"]: d["site"] = d.pop("path")
for l in D["libraries"] + D["extra"]: l["doc"]["site"] = l["doc"].pop("path")
out = HTML.replace("__DATA__", json.dumps(D, ensure_ascii=False).replace("</", "<\\/")).replace("__SITE__", SITE)
open(OUT, "w", encoding="utf-8").write(out); print("written", OUT, len(out))
