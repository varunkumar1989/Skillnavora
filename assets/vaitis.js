/* Vaitis by SkillNavora: free AI library (vaitis.html).
   1. Sign-up gate: saves a "resource" lead via /api/lead, then opens the library.
      Visitors who already shared details on SkillNavora (sn_access) or admins skip it.
   2. Library: guides, 763 AI tools in 26 categories, saved items.
      Deep links: #guides, #g-001, #tools, #tools-<category-slug>, #saved.
   This is visitor tracking, not security: the data files are public. */
(function () {
  const root = document.getElementById("vx"); if (!root) return;
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = u => /^https?:\/\//i.test(u || "") ? u : "#";
  const get = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  const API = "/api/lead";
  const isAdmin = () => { try { const a = JSON.parse(get("sn_admin") || "null"); return !!a && Date.now() - a.t < 30 * 864e5; } catch (e) { return false; } };
  const unlocked = () => isAdmin() || !!get("vaitis_access") || !!get("sn_access");
  const gate = $("#vx-gate"), app = $("#vx-app");

  /* ---------------- sign-up gate ---------------- */
  const TZ = { "Asia/Kolkata": "IN", "Asia/Calcutta": "IN", "Asia/Dubai": "AE", "Asia/Singapore": "SG", "Asia/Riyadh": "SA", "Asia/Kathmandu": "NP", "Asia/Dhaka": "BD", "Asia/Colombo": "LK", "Asia/Karachi": "PK", "Africa/Lagos": "NG", "Africa/Johannesburg": "ZA", "Asia/Manila": "PH", "Asia/Kuala_Lumpur": "MY", "Asia/Qatar": "QA", "Asia/Kuwait": "KW", "Asia/Muscat": "OM", "Europe/London": "GB", "Europe/Dublin": "IE", "Europe/Berlin": "DE", "Europe/Paris": "FR", "Europe/Amsterdam": "NL", "Australia/Sydney": "AU", "Australia/Melbourne": "AU", "Pacific/Auckland": "NZ", "America/Toronto": "CA", "America/Vancouver": "CA" };
  const sel = $("#vx-country"), dial = $("#vx-dial");
  const showDial = () => { const o = sel.selectedOptions[0]; dial.textContent = (o && o.dataset.dial) || "+"; };
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    const c = TZ[tz] || (/^America\//.test(tz) ? "US" : "");
    if (c && sel.querySelector(`option[value="${c}"]`)) { sel.value = c; $("#vx-detected").textContent = "(detected)"; }
  } catch (e) {}
  showDial(); sel.addEventListener("change", () => { $("#vx-detected").textContent = ""; showDial(); });

  $("#vx-form").addEventListener("submit", async e => {
    e.preventDefault();
    const f = e.target, err = $("#vx-err"), d = Object.fromEntries(new FormData(f));
    const phone = String(d.phone || "").replace(/[^0-9]/g, "");
    const problems = [];
    if (!String(d.name || "").trim()) problems.push("your name");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(d.email || "").trim())) problems.push("a valid email");
    if (phone.length < 6 || phone.length > 14) problems.push("a valid phone number");
    if (!d.coding) problems.push("whether you know coding");
    if (!d.role) problems.push("what describes you");
    if (!d.experience) problems.push("your years of experience");
    if (problems.length) { err.hidden = false; err.textContent = "Please add " + problems.join(", ") + "."; return; }
    err.hidden = true;
    const btn = $(".vx-go", f); btn.disabled = true; btn.textContent = "Opening your library…";
    const parts = String(d.name).trim().split(/\s+/);
    const country = sel.selectedOptions[0] ? sel.selectedOptions[0].textContent : "";
    const row = {
      kind: "resource", first_name: parts[0], last_name: parts.slice(1).join(" "), email: String(d.email).trim(),
      phone: ((sel.selectedOptions[0] && sel.selectedOptions[0].dataset.dial) || "") + phone, role: d.role, experience: d.experience,
      message: `Vaitis AI library sign-up. Knows coding: ${d.coding}. Country: ${country}. Email updates: ${d.updates ? "yes" : "no"}. Newsletter: ${d.newsletter ? "yes" : "no"}.`,
      source: "vaitis.html"
    };
    try { await fetch(API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(row), keepalive: true }); } catch (e2) {}
    const rec = JSON.stringify({ t: Date.now(), via: "vaitis", name: parts[0] });
    set("vaitis_access", rec); if (!get("sn_access")) set("sn_access", rec);
    open();
  });

  /* ---------------- library ---------------- */
  let META, TOOLS, GUIDES, state = { tab: "guides", cat: "", price: "", gcat: "", q: "", limit: 60 };
  const saved = () => { try { return JSON.parse(get("vaitis_saved") || "[]"); } catch (e) { return []; } };
  const isSaved = k => saved().includes(k);
  const toggleSave = k => { const s = saved(); const i = s.indexOf(k); i < 0 ? s.push(k) : s.splice(i, 1); set("vaitis_saved", JSON.stringify(s)); countSaved(); return i < 0; };
  const countSaved = () => { const n = $("#vx-saved-n"); if (n) n.textContent = saved().length; };
  const view = $("#vx-view");
  const v = n => root.dataset["v" + n[0].toUpperCase() + n.slice(1)] || "";
  const load = n => fetch(`assets/vaitis/${n}.json?v=${v(n)}`).then(r => { if (!r.ok) throw new Error(n); return r.json(); });
  const words = s => String(s || "").toLowerCase().split(/[^a-z0-9+#.]+/).filter(Boolean);
  const match = (q, text) => { const t = String(text).toLowerCase(); return words(q).every(w => t.includes(w)); };
  const PRICE = { free: ["Fully free", "vx-p-free"], freeplan: ["Free plan", "vx-p-plan"], paid: ["Paid", "vx-p-paid"], unknown: ["See site", "vx-p-unk"] };
  const tile = name => { const h = [...name].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7) % 360; return `<span class="vx-tile" style="--h:${h}" aria-hidden="true">${esc(name.replace(/[^A-Za-z0-9]/g, "").slice(0, 1).toUpperCase() || "•")}</span>`; };
  const star = (k, label) => `<button type="button" class="vx-save${isSaved(k) ? " on" : ""}" data-save="${esc(k)}" aria-pressed="${isSaved(k)}" aria-label="Save ${esc(label)}" title="Save">${isSaved(k) ? "★" : "☆"}</button>`;

  const THEME = { "Career and Jobs": [210, "💼"], "Marketing": [330, "📣"], "Sales": [150, "🤝"], "Vibe Coding": [265, "🧑‍💻"], "Content Creation": [15, "🎬"],
    "Business and Startups": [35, "🚀"], "AI Agents": [190, "🤖"], "Research": [175, "🌍"], "AI Tools": [245, "🧰"], "Automation": [125, "⚙️"],
    "Prompting": [290, "🪄"], "Data and Analytics": [200, "📊"], "Video Generation": [350, "🎞️"] };
  const theme = c => THEME[c] || [230, "✨"];
  const stepCount = g => g.steps.filter(s => /^Step \d+:/.test(s)).length;
  function guideCard(g) {
    const [h, emo] = theme(g.cat);
    return `<article class="vx-card vx-gcard"><a class="vx-cover" href="#g-${esc(g.id)}" style="--h:${h}" aria-hidden="true" tabindex="-1"><span class="vx-emo">${emo}</span><b>Guide ${esc(g.id)}</b><small>${stepCount(g)} steps</small></a><div class="vx-card-top"><span class="vx-cat">${esc(g.cat)}</span>${star("g:" + g.id, g.title)}</div>
      <h3><a href="#g-${esc(g.id)}">${esc(g.title)}</a></h3><p>${esc(g.summary)}</p>
      <div class="vx-meta"><span>⏱ ${esc(g.time)}</span><span>📶 ${esc(g.level)}</span></div>
      <a class="vx-more" href="#g-${esc(g.id)}">Open step-by-step guide →</a></article>`;
  }
  function toolCard(t) {
    const [pl, pc] = PRICE[t.price] || PRICE.unknown;
    return `<article class="vx-card vx-tcard"><div class="vx-card-top">${tile(t.name)}<div class="vx-tname"><h3>${esc(t.name)}</h3><small>${esc(t.label)}</small></div>${star("t:" + t.id, t.name)}</div>
      <p>${esc(t.desc)}</p>
      <div class="vx-meta"><span class="vx-price ${pc}" title="${esc(t.pricing)}">${esc(pl)}</span><a class="vx-catlink" href="#tools-${esc(t.slug)}">${esc(t.cat)}</a></div>
      <a class="vx-more" href="${esc(safeUrl(t.url))}" target="_blank" rel="noopener nofollow">Visit ${esc(t.domain || "website")} ↗</a></article>`;
  }

  function renderGuides() {
    const q = state.q, list = GUIDES.filter(g => (!state.gcat || g.cat === state.gcat) && (!q || match(q, [g.title, g.summary, g.cat, g.tools.join(" "), g.html.replace(/<[^>]+>/g, " ")].join(" "))));
    const chips = ["", ...META.guideCats].map(c => `<button type="button" class="vx-chip${state.gcat === c ? " on" : ""}" data-gcat="${esc(c)}">${c ? esc(c) : "All guides"}</button>`).join("");
    view.innerHTML = `<div class="vx-chips" role="group" aria-label="Guide categories">${chips}</div>
      <p class="vx-count">${list.length} of ${GUIDES.length} guides${q ? ` for “${esc(q)}”` : ""}</p>
      <div class="vx-grid">${list.map(guideCard).join("") || `<p class="vx-mu">No guides match. Try the AI Tools tab.</p>`}</div>`;
  }
  function renderGuide(id) {
    const g = GUIDES.find(x => x.id === id); if (!g) { location.hash = "#guides"; return; }
    const toc = g.steps.map((s, i) => `<li><a href="#g-${esc(g.id)}" data-jump="s${i + 1}">${esc(s.replace(/^Step \d+:\s*/, ""))}</a></li>`).join("");
    const tl = g.tools.map(n => { const t = TOOLS.find(x => x.name === n); return t ? `<a class="vx-chip" href="${esc(safeUrl(t.url))}" target="_blank" rel="noopener nofollow">${esc(n)} ↗</a>` : ""; }).join("");
    const links = g.links.map(l => `<li><a href="${esc(safeUrl(l.url))}" target="_blank" rel="noopener nofollow">${esc(l.label)} ↗</a></li>`).join("");
    const i = GUIDES.indexOf(g), nx = GUIDES[(i + 1) % GUIDES.length];
    view.innerHTML = `<div class="vx-guide"><a class="vx-back" href="#guides">← All guides</a>
      <header class="vx-ghead"><div class="vx-banner" style="--h:${theme(g.cat)[0]}"><span class="vx-emo" aria-hidden="true">${theme(g.cat)[1]}</span><div class="vx-card-top"><span class="vx-cat">${esc(g.cat)} · Guide ${esc(g.id)}</span>${star("g:" + g.id, g.title)}</div>
        <h2>${esc(g.title)}</h2><p class="vx-lead">${esc(g.summary)}</p>
        <div class="vx-chipsrow"><span>🪜 ${stepCount(g)} steps</span><span>🖼️ ${(g.html.match(/<svg/g) || []).length} illustration${(g.html.match(/<svg/g) || []).length === 1 ? "" : "s"}</span><span>📋 ${(g.html.match(/vx-copy/g) || []).length} copy-ready blocks</span></div></div>
        <div class="vx-facts"><div><small>Time</small><b>${esc(g.time)}</b></div><div><small>Cost</small><b>${esc(g.cost)}</b></div><div><small>Level</small><b>${esc(g.level)}</b></div></div></header>
      <div class="vx-glayout"><aside class="vx-toc"><b>In this guide</b><ol>${toc}</ol>${links ? `<b>Tools and links</b><ul class="vx-links">${links}</ul>` : ""}</aside>
      <div class="vx-gbody">${g.html}${tl ? `<div class="vx-used"><b>Tools from the library used here:</b> ${tl}</div>` : ""}
      <a class="vx-next" href="#g-${esc(nx.id)}"><small>Next guide</small><b>${esc(nx.title)} →</b></a></div></div></div>`;
    window.scrollTo({ top: root.offsetTop - 70 });
  }
  function renderTools() {
    const q = state.q;
    const base = TOOLS.filter(t => (!state.cat || t.slug === state.cat) && (!q || match(q, [t.name, t.label, t.cat, t.domain].join(" "))));
    const pc = base.reduce((a, t) => (a[t.price] = (a[t.price] || 0) + 1, a), {});
    let list = base.filter(t => !state.price || t.price === state.price);
    const cur = META.categories.find(c => c.slug === state.cat);
    const side = [`<button type="button" class="vx-cat-b${!state.cat ? " on" : ""}" data-cat=""><span>🧰 All tools</span><b>${TOOLS.length}</b></button>`]
      .concat(META.categories.map(c => `<button type="button" class="vx-cat-b${state.cat === c.slug ? " on" : ""}" data-cat="${esc(c.slug)}"><span>${c.icon} ${esc(c.name)}</span><b>${c.count}</b></button>`)).join("");
    const opts = `<option value="">All categories (${TOOLS.length})</option>` + META.categories.map(c => `<option value="${esc(c.slug)}"${state.cat === c.slug ? " selected" : ""}>${esc(c.name)} (${c.count})</option>`).join("");
    const pchips = [["", `Any price (${base.length})`], ["freeplan", `Free plan (${pc.freeplan || 0})`], ["free", `Fully free (${pc.free || 0})`], ["paid", `Paid only (${pc.paid || 0})`]]
      .map(([k, l]) => `<button type="button" class="vx-chip${state.price === k ? " on" : ""}" data-price="${k}">${esc(l)}</button>`).join("");
    const shown = list.slice(0, state.limit);
    view.innerHTML = `<div class="vx-tlayout"><nav class="vx-side" aria-label="Tool categories">${side}</nav>
      <div><label class="vx-catsel"><span>Category</span><select id="vx-catsel">${opts}</select></label>
      ${cur ? `<div class="vx-cathead"><h2>${cur.icon} ${esc(cur.name)}</h2><p>${esc(cur.desc)}</p></div>` : `<div class="vx-cathead"><h2>🧰 All ${TOOLS.length} AI tools</h2><p>Every tool in the library, sorted by category. Pick a category or search by name or task.</p></div>`}
      <div class="vx-chips" role="group" aria-label="Price">${pchips}</div>
      <p class="vx-count">${list.length} tools${q ? ` for “${esc(q)}”` : ""}</p>
      <div class="vx-grid vx-tgrid">${shown.map(toolCard).join("") || `<p class="vx-mu">No tools match. Clear the search or choose another category.</p>`}</div>
      ${list.length > shown.length ? `<p class="vx-center"><button type="button" class="btn btn-line" id="vx-moreb">Show more (${list.length - shown.length} left)</button></p>` : ""}</div></div>`;
  }
  function renderSaved() {
    const s = saved(), gs = GUIDES.filter(g => s.includes("g:" + g.id)), ts = TOOLS.filter(t => s.includes("t:" + t.id));
    view.innerHTML = !s.length ? `<div class="vx-empty"><p>Nothing saved yet.</p><p class="vx-mu">Tap ☆ on any guide or tool to keep it here. Saved items stay on this device.</p></div>`
      : `${gs.length ? `<h2 class="vx-h3">Saved guides</h2><div class="vx-grid">${gs.map(guideCard).join("")}</div>` : ""}${ts.length ? `<h2 class="vx-h3">Saved tools</h2><div class="vx-grid vx-tgrid">${ts.map(toolCard).join("")}</div>` : ""}`;
  }
  function setTab(t) { state.tab = t; $$(".vx-tabs [data-tab]").forEach(b => b.setAttribute("aria-selected", String(b.dataset.tab === t))); }
  function route() {
    if (!GUIDES) return;
    const h = decodeURIComponent(location.hash.slice(1));
    if (/^g-\d+$/.test(h)) { setTab("guides"); return renderGuide(h.slice(2)); }
    if (h.startsWith("tools")) { setTab("tools"); const c = h.slice(6); state.cat = META.categories.some(x => x.slug === c) ? c : ""; state.limit = 60; return renderTools(); }
    if (h === "saved") { setTab("saved"); return renderSaved(); }
    setTab("guides"); renderGuides();
  }

  view.addEventListener("click", e => {
    const s = e.target.closest("[data-save]");
    if (s) { e.preventDefault(); const on = toggleSave(s.dataset.save); s.classList.toggle("on", on); s.textContent = on ? "★" : "☆"; s.setAttribute("aria-pressed", String(on)); if (state.tab === "saved") renderSaved(); return; }
    const c = e.target.closest(".vx-copy");
    if (c) { const txt = c.closest(".vx-code").querySelector("code").textContent; const done = () => { c.textContent = "Copied ✓"; setTimeout(() => (c.textContent = "Copy"), 1600); };
      const fallback = () => { const t = document.createElement("textarea"); t.value = txt; t.setAttribute("readonly", ""); t.style.cssText = "position:fixed;left:-9999px"; document.body.appendChild(t); t.select(); try { if (document.execCommand("copy")) done(); } catch (e2) {} t.remove(); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(txt).then(done, fallback); else fallback(); return; }
    const j = e.target.closest("[data-jump]");
    if (j) { e.preventDefault(); const el = document.getElementById(j.dataset.jump); if (el) el.scrollIntoView({ behavior: "smooth", block: "start" }); return; }
    const gc = e.target.closest("[data-gcat]"); if (gc) { state.gcat = gc.dataset.gcat; return renderGuides(); }
    const cb = e.target.closest("[data-cat]"); if (cb) { location.hash = cb.dataset.cat ? "#tools-" + cb.dataset.cat : "#tools"; return; }
    const pc = e.target.closest("[data-price]"); if (pc) { state.price = pc.dataset.price; state.limit = 60; return renderTools(); }
    if (e.target.id === "vx-moreb") { state.limit += 60; renderTools(); }
  });
  view.addEventListener("change", e => { if (e.target.id === "vx-catsel") location.hash = e.target.value ? "#tools-" + e.target.value : "#tools"; });
  $$(".vx-tabs [data-tab]").forEach(b => b.addEventListener("click", () => { location.hash = "#" + b.dataset.tab; }));
  let qt; $("#vx-q").addEventListener("input", e => { clearTimeout(qt); qt = setTimeout(() => { state.q = e.target.value.trim(); state.limit = 60;
    if (state.tab === "saved" || /^#g-/.test(location.hash)) { location.hash = "#" + (state.tab === "saved" ? "tools" : "guides"); return; }
    state.tab === "tools" ? renderTools() : renderGuides(); }, 150); });
  window.addEventListener("hashchange", route);

  function open() {
    gate.hidden = true; app.hidden = false; countSaved();
    try { const a = JSON.parse(get("vaitis_access") || get("sn_access") || "{}"); if (a.name) $("#vx-hello").textContent = `Welcome, ${a.name}. Your free AI library`; } catch (e) {}
    if (GUIDES) return route();
    Promise.all([load("meta"), load("tools"), load("guides")]).then(([m, t, g]) => { META = m; TOOLS = t; GUIDES = g; route(); })
      .catch(() => { view.innerHTML = `<p class="vx-err">The library couldn't load. Check your connection and refresh the page.</p>`; });
  }
  if (unlocked()) open(); else { gate.hidden = false; app.hidden = true; }
})();
