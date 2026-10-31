/* SkillNavora AI Studio: AI Tutor, AI PRD Writer, AI Speaking Coach and AI interview feedback.
   Talks to /api/ai (Cloudflare function holding the Claude key). Nothing secret lives here. */
(function () {
  "use strict";
  const $ = id => document.getElementById(id);
  const R = document.body.dataset.root || "";
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const ls = { get: k => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch {} } };
  const ss = { get: k => { try { return sessionStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { sessionStorage.setItem(k, v); } catch {} } };

  /* ---------- Safe Markdown → HTML (escape first, then format) ---------- */
  function inline(t) {
    return t.replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<i>$2</i>")
      .replace(/(^|\W)_([^_]+)_(?=\W|$)/g, "$1<i>$2</i>")
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, txt, url) => {
        const u = url.replace(/&amp;/g, "&");
        if (/^\//.test(u)) return `<a href="${esc(R + u.slice(1))}">${txt}</a>`;
        if (/^https:\/\//i.test(u)) return `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${txt}</a>`;
        return txt;
      });
  }
  function md(src) {
    const lines = esc(src).split("\n"), out = [];
    let i = 0;
    while (i < lines.length) {
      let l = lines[i];
      if (/^```/.test(l)) { const buf = []; i++; while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]); i++; out.push(`<pre><code>${buf.join("\n")}</code></pre>`); continue; }
      let m;
      if ((m = l.match(/^(#{1,4})\s+(.*)/))) { const n = Math.min(m[1].length, 3); out.push(`<h${n}>${inline(m[2])}</h${n}>`); i++; continue; }
      if (/^\s*\|.*\|\s*$/.test(l) && i + 1 < lines.length && /^\s*\|?[\s:-]+\|[\s|:-]*$/.test(lines[i + 1])) {
        const row = s => s.trim().replace(/^\||\|$/g, "").split("|").map(c => inline(c.trim()));
        const head = row(l); i += 2; const body = [];
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) body.push(row(lines[i++]));
        out.push(`<table><thead><tr>${head.map(c => `<th>${c}</th>`).join("")}</tr></thead><tbody>${body.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table>`); continue;
      }
      if (/^\s*[-*•]\s+/.test(l)) { const buf = []; while (i < lines.length && /^\s*[-*•]\s+/.test(lines[i])) buf.push(`<li>${inline(lines[i++].replace(/^\s*[-*•]\s+/, ""))}</li>`); out.push(`<ul>${buf.join("")}</ul>`); continue; }
      if (/^\s*\d+[.)]\s+/.test(l)) { const buf = []; while (i < lines.length && /^\s*\d+[.)]\s+/.test(lines[i])) buf.push(`<li>${inline(lines[i++].replace(/^\s*\d+[.)]\s+/, ""))}</li>`); out.push(`<ol>${buf.join("")}</ol>`); continue; }
      if (/^&gt;\s?/.test(l)) { out.push(`<blockquote>${inline(l.replace(/^&gt;\s?/, ""))}</blockquote>`); i++; continue; }
      if (/^(-{3,}|\*{3,})$/.test(l.trim())) { out.push("<hr>"); i++; continue; }
      if (!l.trim()) { i++; continue; }
      const buf = [l]; i++;
      while (i < lines.length && lines[i].trim() && !/^(#{1,4}\s|```|\s*[-*•]\s|\s*\d+[.)]\s|&gt;|\s*\|)/.test(lines[i])) buf.push(lines[i++]);
      out.push(`<p>${inline(buf.join("<br>"))}</p>`);
    }
    return out.join("");
  }

  /* ---------- Access: two free tries, then the same details form as the handbooks ---------- */
  const FREE = 2;
  function canUse() {
    const g = window.SNgate;
    if (!g || g.has()) return true;
    const n = +(ls.get("sn_ai_n") || 0);
    if (n < FREE) { ls.set("sn_ai_n", String(n + 1)); return true; }
    g.ask(location.pathname.split("/").pop() + "#unlocked");
    return false;
  }

  /* ---------- API ---------- */
  const ERR = {
    not_configured: "The AI is being switched on right now. Please try again in a little while, or book a free counselling call for help.",
    limit: "You've reached today's free AI limit. Please come back tomorrow, or book a free counselling call.",
    busy: "Lots of learners are using the AI right now. Please try again in a minute.",
    refusal: "Sorry, I can't help with that. Try asking a learning or career question.",
    bad_request: "That message is too long or empty. Please shorten it and try again.",
    forbidden: "Please use the AI tools on skillnavora.in.",
  };
  async function ask(mode, messages, onText, extra) {
    let r;
    try { r = await fetch(R + "api/ai", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(Object.assign({ mode, messages }, extra || {})) }); }
    catch { throw new Error("Network problem. Check your internet connection and try again."); }
    const ct = r.headers.get("content-type") || "";
    if (!r.ok || ct.includes("application/json")) {
      let code = ""; try { code = (await r.json()).error; } catch {}
      if (r.status === 404 || r.status === 405) code = "not_configured";
      throw new Error(ERR[code] || "Something went wrong. Please try again.");
    }
    const rd = r.body.getReader(), dec = new TextDecoder(); let text = "";
    for (;;) { const { done, value } = await rd.read(); if (done) break; text += dec.decode(value, { stream: true }); onText && onText(text); }
    return text;
  }
  const errBox = msg => `<div class="ai-err">${esc(msg)}</div>`;
  const download = (name, data, type) => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([data], { type })); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); };

  const root = document.querySelector("[data-ai]"), kind = root && root.dataset.ai;

  /* ================================ AI TUTOR ================================ */
  if (kind === "tutor") {
    const log = $("tu-log"), inp = $("tu-in"), SUG = JSON.parse($("tu-data").textContent);
    let topic = "All", hist = []; try { hist = JSON.parse(ss.get("sn_tutor") || "[]"); } catch {}
    const params = new URLSearchParams(location.search), page = params.get("page");
    const bubble = (role, html) => { const d = document.createElement("div"); d.className = "ai-m " + (role === "user" ? "u" : "a"); d.innerHTML = html; log.appendChild(d); log.scrollTop = log.scrollHeight; return d; };
    const sugg = () => { $("tu-sug").innerHTML = SUG[topic].map(q => `<button type="button">${esc(q)}</button>`).join(""); };
    function welcome() {
      log.innerHTML = "";
      bubble("assistant", md("Hi! I'm **Navora**, your SkillNavora AI Tutor. Ask me anything about **product management, Excel, SQL, Python, Power BI, Tableau, machine learning, GenAI, agents, careers or English**. I'll explain with examples and point you to the right lesson." + (page ? "\n\nI can also see the page you came from, so you can ask about it." : "")));
      hist.forEach(m => bubble(m.role, m.role === "user" ? esc(m.content) : md(m.content)));
    }
    let busy = false;
    async function send(q) {
      q = q.trim(); if (!q || busy) return;
      if (!canUse()) return;
      busy = true; inp.value = "";
      bubble("user", esc(q));
      const content = (topic !== "All" ? `[Topic: ${topic}] ` : "") + q;
      hist.push({ role: "user", content });
      const a = bubble("assistant", '<span class="ai-dots">Thinking</span>');
      try {
        const text = await ask("tutor", hist.slice(-12), t => { a.innerHTML = md(t); log.scrollTop = log.scrollHeight; }, page ? { page } : null);
        hist.push({ role: "assistant", content: text.slice(0, 20000) || "…" });
      } catch (e) { hist.pop(); a.innerHTML = errBox(e.message); }
      ss.set("sn_tutor", JSON.stringify(hist.slice(-20))); busy = false; inp.focus();
    }
    $("tu-topics").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; topic = b.dataset.topic; $("tu-topics").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); sugg(); });
    $("tu-sug").addEventListener("click", e => { const b = e.target.closest("button"); if (b) send(b.textContent); });
    $("tu-form").addEventListener("submit", e => { e.preventDefault(); send(inp.value); });
    inp.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(inp.value); } });
    $("tu-new").addEventListener("click", () => { hist = []; ss.set("sn_tutor", "[]"); welcome(); inp.focus(); });
    sugg(); welcome();
    if (params.get("q")) send(params.get("q"));
  }

  /* ============================== AI PRD WRITER ============================= */
  if (kind === "prd") {
    const f = $("prd-form"), out = $("prd-out"), acts = $("prd-acts"), rev = $("prd-rev");
    const EX = [
      { name: "SplitKaro", type: "Consumer mobile app", idea: "A UPI-based app for college students to split hostel, food and trip expenses and settle up in one tap.", users: "College students in India, 18–24, living in hostels or shared flats", problem: "Groups track shared spends on WhatsApp and Excel; people forget who owes what and settling is awkward.", goals: "Reach 50,000 monthly active users in 6 months; 60% of groups settle within 7 days", constraints: "Must work on low-end Android phones; follow NPCI/UPI and DPDP rules" },
      { name: "AI Support Copilot", type: "AI / GenAI feature", idea: "An AI assistant inside our customer-support tool that drafts replies to tickets using our help-centre articles and past tickets.", users: "Support agents at a B2B SaaS company handling 5,000 tickets a day", problem: "Agents spend 6 minutes per ticket searching docs; answers are inconsistent", goals: "Cut average handling time by 30% with CSAT not dropping", constraints: "No customer PII sent to third parties without masking; agents approve every reply" },
      { name: "KiranaPay Credit", type: "B2B / fintech", idea: "Buy-now-pay-later for small kirana shops to buy stock from distributors, repaid daily from UPI collections.", users: "Kirana shop owners in tier-2 and tier-3 cities and their distributors", problem: "Shops run out of working capital and lose sales; distributors take credit risk informally", goals: "₹50 crore disbursed in year 1 with under 2% defaults", constraints: "RBI digital lending guidelines; NBFC partner; Hindi and regional language support" }];
    let hist = [], doc = ls.get("sn_prd") || "", busy = false;
    const show = () => { out.innerHTML = md(doc); acts.hidden = rev.hidden = !doc; };
    if (doc) { try { hist = JSON.parse(ls.get("sn_prd_h") || "[]"); } catch {} show(); }
    $("prd-ex").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; const x = EX[+b.dataset.ex]; for (const k in x) if (f.elements[k]) f.elements[k].value = x[k]; });
    async function run(messages, label) {
      if (busy || !canUse()) return; busy = true;
      const btns = [f.querySelector("button[type=submit]"), rev.querySelector("button")]; btns.forEach(b => { b.disabled = true; });
      out.innerHTML = `<p class="ai-dots">${esc(label)}</p>`; acts.hidden = true;
      try {
        const text = await ask("prd", messages, t => { out.innerHTML = md(t); });
        doc = text; hist = messages.concat({ role: "assistant", content: text }).slice(-6);
        if (hist[0].role !== "user") hist = hist.slice(1);
        ls.set("sn_prd", doc); ls.set("sn_prd_h", JSON.stringify(hist)); show();
      } catch (e) { out.innerHTML = errBox(e.message) + (doc ? md(doc) : ""); acts.hidden = rev.hidden = !doc; }
      btns.forEach(b => { b.disabled = false; }); busy = false;
    }
    f.addEventListener("submit", e => {
      e.preventDefault();
      const v = n => f.elements[n].value.trim();
      if (v("idea").length < 10) { out.innerHTML = errBox("Please describe your idea in at least one sentence."); f.elements.idea.focus(); return; }
      const depth = { standard: "Standard length (about 2–3 pages).", detailed: "Detailed: thorough enough for a real project or a PM interview take-home.", "one-pager": "A one-pager: keep every section to 1–3 bullets." }[v("depth")];
      const brief = `Write a PRD.\nName: ${v("name") || "(suggest a name)"}\nType: ${v("type")}\nIdea: ${v("idea")}\nTarget users: ${v("users") || "(infer)"}\nProblem: ${v("problem") || "(infer)"}\nGoals: ${v("goals") || "(propose)"}\nConstraints: ${v("constraints") || "(none given)"}\nLength: ${depth}`;
      run([{ role: "user", content: brief }], "Writing your PRD");
    });
    rev.addEventListener("submit", e => {
      e.preventDefault(); const q = $("prd-rin").value.trim(); if (!q || !doc) return;
      const base = hist.length ? hist : [{ role: "user", content: "Here is my PRD." }, { role: "assistant", content: doc }];
      $("prd-rin").value = "";
      run(base.concat({ role: "user", content: "Update the PRD: " + q + "\nReturn the complete updated PRD." }), "Updating your PRD");
    });
    acts.addEventListener("click", async e => {
      const b = e.target.closest("button"); if (!b || !doc) return;
      const title = (doc.match(/^#\s+(.+)/m) || [, "PRD"])[1].replace(/[^\w\- ]+/g, "").trim().slice(0, 60) || "PRD";
      if (b.dataset.act === "copy") { try { await navigator.clipboard.writeText(doc); b.textContent = "Copied ✓"; setTimeout(() => b.textContent = "Copy", 1500); } catch {} }
      if (b.dataset.act === "md") download(title + ".md", doc, "text/markdown");
      if (b.dataset.act === "doc") download(title + ".doc", `<html><head><meta charset="utf-8"><title>${esc(title)}</title><style>body{font-family:Calibri,Arial,sans-serif;line-height:1.5}table{border-collapse:collapse}td,th{border:1px solid #999;padding:4px 8px}</style></head><body>${md(doc)}<p style="color:#888;font-size:11px">Written with SkillNavora AI PRD Writer · skillnavora.in</p></body></html>`, "application/msword");
      if (b.dataset.act === "print") { const w = window.open("", "_blank"); if (!w) return; w.document.write(`<!doctype html><html><head><meta charset="utf-8"><title>${esc(title)}</title><style>body{font:15px/1.55 Arial,sans-serif;max-width:800px;margin:30px auto;padding:0 20px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:5px 8px;text-align:left}h1{font-size:26px}h2{font-size:19px;margin-top:22px}</style></head><body>${md(doc)}<p style="color:#888;font-size:11px">Written with SkillNavora AI PRD Writer · skillnavora.in</p></body></html>`); w.document.close(); w.focus(); setTimeout(() => w.print(), 300); }
    });
  }

  /* ============================ AI SPEAKING COACH =========================== */
  if (kind === "speak") {
    const DATA = JSON.parse($("sc-data").textContent);
    const live = $("sc-live"), mic = $("sc-mic"), out = $("sc-out"), qEl = $("sc-q"), tgt = $("sc-target"), status = $("sc-status");
    let mode = "intro", q = "", rec = null, on = false, t0 = 0, tick = null, finalTxt = "", lastRes = 0, pauses = 0, elapsed = 0, busy = false, better = "";
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const words = s => (s.toLowerCase().match(/[a-z']+/g) || []);
    const FILLERS = /\b(um+|uh+|umm+|hmm+|er+|ah+|basically|actually|literally|you know|i mean|kind of|sort of)\b/gi;
    const placeholder = () => { live.innerHTML = '<i>Your words will appear here as you speak. No mic? Type your answer here instead.</i>'; };
    const text = () => live.querySelector("i") ? "" : live.innerText.trim();
    function pick(next) {
      const pool = DATA[mode].q; let n; do { n = pool[Math.floor(Math.random() * pool.length)]; } while (next && pool.length > 1 && n === q); q = n;
      const drill = mode === "drill";
      $("sc-kicker").textContent = drill ? "Read this sentence aloud" : "Your question";
      qEl.hidden = drill; tgt.hidden = !drill; qEl.textContent = q; tgt.textContent = q;
      finalTxt = ""; elapsed = 0; pauses = 0; placeholder(); $("sc-metrics").hidden = true; $("sc-time").textContent = "00:00";
    }
    const fmt = s => String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(Math.floor(s % 60)).padStart(2, "0");
    function metrics() {
      const t = text(), w = words(t).length, mins = Math.max(elapsed, 1) / 60, fill = (t.match(FILLERS) || []).length;
      const wpm = elapsed ? Math.round(w / mins) : 0;
      const m = { words: w, seconds: Math.round(elapsed), wpm, fillers: fill, long_pauses: pauses };
      const pace = !wpm ? "—" : wpm < 110 ? "Slow" : wpm > 170 ? "Fast" : "Good";
      $("sc-metrics").innerHTML = `<div><b>${w}</b><small>words</small></div><div><b>${fmt(elapsed)}</b><small>time</small></div><div><b>${wpm || "—"}</b><small>words / min · ${pace}</small></div><div><b>${fill}</b><small>filler words</small></div><div><b>${pauses}</b><small>long pauses</small></div>`;
      $("sc-metrics").hidden = !w;
      if (mode === "drill" && w) {
        const said = new Set(words(t)); let ok = 0;
        tgt.innerHTML = q.split(/(\s+)/).map(tok => { const k = (tok.toLowerCase().match(/[a-z']+/) || [""])[0]; if (!k) return esc(tok); const hit = said.has(k); ok += hit; return `<span class="${hit ? "ok" : "miss"}">${esc(tok)}</span>`; }).join("");
        const total = words(q).length; m.drill_accuracy = Math.round(100 * ok / total);
        $("sc-metrics").innerHTML += `<div><b>${m.drill_accuracy}%</b><small>words recognised</small></div>`;
      }
      return m;
    }
    function stop() { on = false; mic.classList.remove("rec"); mic.setAttribute("aria-label", "Start speaking"); clearInterval(tick); try { rec && rec.stop(); } catch {} status.textContent = text() ? "Done. Edit the text if needed, then press Get AI feedback." : "Tap the mic and answer out loud."; metrics(); }
    function start() {
      if (!SR) { status.textContent = "Voice input isn't supported in this browser. Please use Chrome or Edge, or type your answer below."; live.focus(); return; }
      rec = new SR(); rec.lang = $("sc-lang").value; rec.continuous = true; rec.interimResults = true;
      finalTxt = ""; pauses = 0; t0 = Date.now(); lastRes = t0; on = true;
      rec.onresult = e => {
        const now = Date.now(); if (now - lastRes > 2500 && finalTxt) pauses++; lastRes = now;
        let interim = "";
        for (let i = e.resultIndex; i < e.results.length; i++) { const r = e.results[i]; if (r.isFinal) finalTxt += r[0].transcript.trim() + " "; else interim += r[0].transcript; }
        live.innerHTML = esc(finalTxt) + (interim ? `<span style="opacity:.55">${esc(interim)}</span>` : "");
      };
      rec.onerror = e => { if (e.error === "not-allowed" || e.error === "service-not-allowed") { status.textContent = "Microphone access was blocked. Allow the mic in your browser's address bar, or type your answer."; stop(); } };
      rec.onend = () => { if (on) { try { rec.start(); } catch { stop(); } } };
      try { rec.start(); } catch { status.textContent = "Couldn't start the microphone. Please try again."; return; }
      mic.classList.add("rec"); mic.setAttribute("aria-label", "Stop"); status.textContent = "Listening… speak naturally. Tap again to stop.";
      live.innerHTML = ""; tick = setInterval(() => { elapsed = (Date.now() - t0) / 1000; $("sc-time").textContent = fmt(elapsed); }, 250);
    }
    mic.addEventListener("click", () => on ? stop() : start());
    live.addEventListener("focus", () => { if (live.querySelector("i")) live.innerHTML = ""; });
    live.addEventListener("blur", () => { if (!live.innerText.trim()) placeholder(); });
    $("sc-modes").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; if (on) stop(); mode = b.dataset.mode; $("sc-modes").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); pick(); });
    $("sc-next").addEventListener("click", () => { if (on) stop(); pick(true); });
    const say = s => { if (!window.speechSynthesis) return; speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(s); u.lang = $("sc-lang").value; u.rate = .95; speechSynthesis.speak(u); };
    $("sc-listen").addEventListener("click", () => say(q));
    $("sc-say").addEventListener("click", () => say(better || ""));
    $("sc-again").addEventListener("click", () => { finalTxt = ""; elapsed = 0; placeholder(); $("sc-metrics").hidden = true; $("sc-acts").hidden = true; window.scrollTo({ top: root.offsetTop - 80, behavior: "smooth" }); });
    $("sc-go").addEventListener("click", async () => {
      if (on) stop();
      const t = text();
      if (words(t).length < 3) { out.innerHTML = errBox("Say or type at least one full sentence first."); return; }
      if (busy || !canUse()) return; busy = true;
      const m = metrics(), btn = $("sc-go"); btn.disabled = true;
      const msg = `MODE: ${DATA[mode].name}\n${mode === "drill" ? "TARGET SENTENCE (learner read this aloud): " : "QUESTION: "}${q}\nDELIVERY METRICS: ${JSON.stringify(m)}${m.seconds ? "" : " (typed, not spoken: skip pace feedback)"}\nTRANSCRIPT:\n${t.slice(0, 6000)}`;
      out.innerHTML = '<p class="ai-dots">Listening back to your answer</p>'; $("sc-acts").hidden = true;
      try {
        const r = await ask("speak", [{ role: "user", content: msg }], x => { out.innerHTML = md(x); });
        const bv = r.split(/###\s*Better version/i)[1]; better = bv ? bv.split(/\n###\s/)[0].replace(/[*_#>`]/g, "").trim() : "";
        $("sc-acts").hidden = false; $("sc-say").hidden = !better || !window.speechSynthesis;
        out.scrollIntoView({ behavior: "smooth", block: "start" });
      } catch (e) { out.innerHTML = errBox(e.message); }
      btn.disabled = false; busy = false;
    });
    pick();
  }

  /* ===================== Practice with AI: feedback right here ===================== */
  if ($("pr-ai")) {
    const out = $("pr-ai-out"); let busy = false;
    $("pr-ai").addEventListener("click", async () => {
      const a = $("pr-answer").value.trim(), q = $("pr-q").textContent.trim();
      if (a.length < 20) { out.hidden = false; out.innerHTML = errBox("Write your answer first (at least a few sentences)."); return; }
      if (busy || !canUse()) return; busy = true; out.hidden = false; out.innerHTML = '<p class="ai-dots">Reviewing your answer</p>';
      const msg = `Role: ${$("pr-role").value}\nQuestion type: ${$("pr-type").value}\nQuestion: ${q}\nMy answer:\n${a.slice(0, 6000)}`;
      try { await ask("interview", [{ role: "user", content: msg }], t => { out.innerHTML = md(t); }); }
      catch (e) { out.innerHTML = errBox(e.message); }
      busy = false;
    });
  }
})();
