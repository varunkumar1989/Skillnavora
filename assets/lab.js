/* SkillNavora Practice Lab: run SQL (SQLite), Excel formulas and Python in the browser, spot the trap, see the fix.
   SQL uses sql.js (assets/vendor), Excel uses fast-formula-parser (assets/vendor), Python uses Pyodide (loaded from jsDelivr on first use). */
(function () {
  const D = JSON.parse(document.getElementById("lab-data").textContent);
  const ROOT = document.body.dataset.root || "";
  const $ = id => document.getElementById(id);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const LVL = { Basic: 1, Intermediate: 2, Advanced: 3 };
  let seg = "data", sec = "All", lvl = "All", current = null;

  /* ---------- engines ---------- */
  let sqlP = null, pyP = null;
  const sqlEngine = () => sqlP || (sqlP = new Promise((res, rej) => {
    const s = document.createElement("script"); s.src = ROOT + "assets/vendor/sql-wasm.js";
    s.onload = () => window.initSqlJs({ locateFile: f => ROOT + "assets/vendor/" + f }).then(res, rej); s.onerror = () => rej(new Error("SQL engine did not load")); document.head.appendChild(s);
  }));
  const pyEngine = () => pyP || (pyP = new Promise((res, rej) => {
    const base = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
    const s = document.createElement("script"); s.src = base + "pyodide.js";
    s.onload = () => window.loadPyodide({ indexURL: base }).then(res, rej); s.onerror = () => rej(new Error("Python engine did not load. Check your internet connection.")); document.head.appendChild(s);
  }));
  function runSQL(ch, code) {
    return sqlEngine().then(SQL => {
      const db = new SQL.Database();
      (ch.tables || []).forEach(t => {
        db.run(`CREATE TABLE ${t.name} (${t.cols.join(", ")})`);
        const st = db.prepare(`INSERT INTO ${t.name} VALUES (${t.cols.map(() => "?").join(",")})`);
        t.rows.forEach(r => st.run(r)); st.free();
      });
      const out = db.exec(code); db.close();
      if (!out.length) return { table: { cols: ["result"], rows: [["(no rows returned)"]] }, value: "no rows" };
      const last = out[out.length - 1];
      const v = last.values.length === 1 && last.values[0].length === 1 ? last.values[0][0] : last.values.length + " rows";
      return { table: { cols: last.columns, rows: last.values }, value: v };
    });
  }
  function runExcel(ch, code) { try { return runExcel1(ch, code); } catch (e) { return Promise.reject(e); } }
  function runExcel1(ch, code) {
    const t = ch.tables[0], grid = [t.cols].concat(t.rows);
    const val = (r, c) => { const x = (grid[r - 1] || [])[c - 1]; return x === "" || x == null ? null : x; };
    const p = new window.FormulaParser({ onCell: ({ row, col }) => val(row, col), onRange: ({ from, to }) => { const o = []; for (let r = from.row; r <= to.row; r++) { const a = []; for (let c = from.col; c <= to.col; c++) a.push(val(r, c)); o.push(a); } return o; } });
    let v = p.parse(String(code).trim().replace(/^=/, ""), { sheet: "Sheet1", row: 1, col: 1 });
    if (v && typeof v === "object" && "_error" in v) throw new Error(v._error || "Formula error");
    if (Array.isArray(v)) v = v.flat ? v.flat(2)[0] : v[0];
    if (typeof v === "number") v = Math.round(v * 10000) / 10000;
    return Promise.resolve({ value: v });
  }
  function runPython(ch, code) {
    return pyEngine().then(py => { let out = []; py.setStdout({ batched: s => out.push(s) }); py.setStderr({ batched: s => out.push(s) });
      return py.runPythonAsync(code).then(() => ({ text: out.join("\n") || "(no output)" }), e => { const m = String(e.message || e).trim().split("\n").filter(Boolean); throw new Error(m[m.length - 1]); }); });
  }

  /* ---------- rendering ---------- */
  const tableHTML = t => `<div class="lb-tw"><table class="lb-t"><caption>${esc(t.name || "")}</caption><thead><tr>${t.cols.map(c => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${t.rows.map(r => `<tr>${r.map(v => `<td>${v == null ? "<i>NULL</i>" : esc(v)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  const excelGrid = t => { const L = "ABCDEFGHIJ"; return `<div class="lb-tw"><table class="lb-t lb-x"><thead><tr><th></th>${t.cols.map((_, i) => `<th>${L[i]}</th>`).join("")}</tr></thead><tbody><tr><th>1</th>${t.cols.map(c => `<td><b>${esc(c)}</b></td>`).join("")}</tr>${t.rows.map((r, i) => `<tr><th>${i + 2}</th>${r.map(v => `<td>${v === "" || v == null ? "" : esc(v)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`; };
  const fmt = v => typeof v === "number" ? v.toLocaleString("en-IN", { maximumFractionDigits: 4 }) : String(v);

  function list() {
    const items = D.c.filter(c => c.seg === seg && (sec === "All" || c.sec === sec) && (lvl === "All" || c.level === lvl)).sort((a, b) => LVL[a.level] - LVL[b.level]);
    const secs = [...new Set(D.c.filter(c => c.seg === seg).map(c => c.sec))];
    $("lb-chips").innerHTML = ["All"].concat(secs).map(s => `<button type="button" class="lb-chip" aria-pressed="${s === sec}" data-sec="${esc(s)}">${esc(s)} <small>${D.c.filter(c => c.seg === seg && (s === "All" || c.sec === s)).length}</small></button>`).join("");
    $("lb-list").innerHTML = items.map(c => `<button type="button" class="lb-card" data-id="${c.id}"><span class="lb-meta"><span class="lb-lv lv${LVL[c.level]}">${c.level}</span>${esc(c.sec)} · ${esc(c.tagline)}</span><b>${esc(c.title)}</b><span class="lb-q">${esc(c.q)}</span></button>`).join("") || '<p class="meta">No challenges for this filter yet.</p>';
    const asg = (sec === "All" ? secs : [sec]).flatMap(s => (D.a[s] || []).map(a => [s].concat(a)));
    $("lb-assign").innerHTML = asg.length ? `<h3 class="h3s">Free assignments and more practice</h3><div class="lb-as">${asg.map(([s, n, u]) => `<a href="${esc(u)}" target="_blank" rel="noopener"><small>${esc(s)}</small>${esc(n)} ↗</a>`).join("")}</div>` : "";
    $("lb-prompt").hidden = seg !== "genai";
    document.querySelectorAll(".lb-chip").forEach(b => b.onclick = () => { sec = b.dataset.sec; list(); });
    document.querySelectorAll(".lb-card").forEach(b => b.onclick = () => open(b.dataset.id));
  }

  function open(id) {
    const ch = D.c.find(c => c.id === id); current = ch;
    const peers = D.c.filter(c => c.seg === ch.seg && (sec === "All" || c.sec === sec) && (lvl === "All" || c.level === lvl)).sort((a, b) => LVL[a.level] - LVL[b.level]);
    const i = peers.indexOf(ch), box = $("lb-play");
    const editable = ["sql", "excel", "python"].includes(ch.engine);
    let body = `<div class="lb-top"><span class="lb-pill">${esc(ch.sec)} · ${i + 1} of ${peers.length} · ${esc(ch.title)}</span><span class="lb-lv lv${LVL[ch.level]}">${ch.level}</span></div><h2 class="lb-h">${esc(ch.q)}</h2>`;
    (ch.tables || []).forEach(t => body += ch.engine === "excel" ? excelGrid(t) : tableHTML(t));
    if (ch.engine === "scenario") {
      body += `<div class="lb-opts">${ch.options.map((o, k) => `<button type="button" data-k="${k}">${esc(o)}</button>`).join("")}</div><div class="lb-fb" hidden></div>`;
    } else {
      body += editable ? `<label class="lb-edl">${ch.engine === "excel" ? "Formula (edit it and run)" : ch.engine === "sql" ? "SQL query (edit it and run)" : "Python code (edit it and run)"}</label><textarea class="lb-ed" spellcheck="false" rows="${Math.min(12, ch.code.split("\n").length + 2)}">${esc(ch.code)}</textarea>`
                       : `<pre class="lb-code">${esc(ch.code)}</pre>`;
      body += editable ? `<button type="button" class="lb-run">▶ Run</button><p class="lb-note">${ch.engine === "python" ? "Runs in your browser (first run downloads Python, about 10 MB)." : "Runs in your browser. Edit it, or just run it first."}</p>` : "";
      body += `<div class="lb-out" ${editable ? "hidden" : ""}>${editable ? "" : `<div class="lb-res"><small>result</small><b>${esc(ch.result)}</b></div>`}</div>`;
      body += `<div class="lb-decide" ${editable ? "hidden" : ""}><h3>${esc(ch.ask)}</h3><div class="lb-dbtn"><button type="button" data-d="right">👍 Looks right</button><button type="button" data-d="off">🤔 Something's off</button></div></div><div class="lb-fb" hidden></div>`;
    }
    body += `<div class="lb-foot"><button type="button" class="lb-link" data-hint>Need a hint?</button><span class="lb-hint" hidden>💡 ${esc(ch.hint)}</span><span style="flex:1"></span>${i > 0 ? `<button type="button" class="lb-link" data-go="${peers[i - 1].id}">← Previous</button>` : ""}${i < peers.length - 1 ? `<button type="button" class="lb-next" data-go="${peers[i + 1].id}">Next challenge →</button>` : ""}</div>`;
    box.innerHTML = body; box.hidden = false; box.scrollIntoView({ behavior: "smooth", block: "start" });
    box.querySelector("[data-hint]").onclick = e => { e.target.hidden = true; box.querySelector(".lb-hint").hidden = false; };
    box.querySelectorAll("[data-go]").forEach(b => b.onclick = () => open(b.dataset.go));
    const fb = box.querySelector(".lb-fb");
    const reveal = (good, intro) => { fb.hidden = false; fb.className = "lb-fb " + (good ? "good" : "warn");
      fb.innerHTML = `<b>${intro}</b><p>${esc(ch.trap)}</p>` + (ch.engine !== "scenario" && ch.fix !== ch.code ? `<p class="lb-fixh">The fix:</p><pre class="lb-code">${esc(ch.fix)}</pre>` + (editable ? `<button type="button" class="lb-link" data-fix>Load the fix into the editor and run it</button>` : "") : "");
      const fx = fb.querySelector("[data-fix]"); if (fx) fx.onclick = () => { box.querySelector(".lb-ed").value = ch.fix; run(); }; };
    if (ch.engine === "scenario") {
      box.querySelectorAll(".lb-opts button").forEach(b => b.onclick = () => { const ok = +b.dataset.k === ch.best; b.classList.add(ok ? "ok" : "no");
        if (ok) { box.querySelectorAll(".lb-opts button").forEach(x => x.disabled = true); reveal(true, "✅ Great answer!"); }
        else { fb.hidden = false; fb.className = "lb-fb warn"; fb.innerHTML = `<b>Not the best choice. Try again.</b><p>💡 ${esc(ch.hint)}</p>`; } });
      return;
    }
    box.querySelectorAll("[data-d]").forEach(b => b.onclick = () => { const ok = b.dataset.d === ch.answer;
      reveal(ok, ok ? (ch.answer === "off" ? "✅ Well spotted, there is a trap!" : "✅ Correct, this one is right!") : (ch.answer === "off" ? "❌ Look again: there is a trap." : "❌ Actually, this one is correct.")); });
    const out = box.querySelector(".lb-out"), dec = box.querySelector(".lb-decide");
    function run() {
      const code = box.querySelector(".lb-ed").value, btn = box.querySelector(".lb-run");
      btn.disabled = true; btn.textContent = ch.engine === "python" ? "Loading Python…" : "Running…"; out.hidden = false; out.innerHTML = '<p class="meta">Running…</p>';
      const p = ch.engine === "sql" ? runSQL(ch, code) : ch.engine === "excel" ? runExcel(ch, code) : runPython(ch, code);
      p.then(r => {
        out.innerHTML = r.table ? `<div class="lb-res"><small>result</small>${r.table.rows.length === 1 && r.table.cols.length === 1 ? `<b>${esc(fmt(r.value))}</b>` : tableHTML(r.table)}</div>`
          : r.text != null ? `<div class="lb-res"><small>output</small><pre class="lb-pyout">${esc(r.text)}</pre></div>` : `<div class="lb-res"><small>result</small><b>${esc(fmt(r.value))}</b></div>`;
        dec.hidden = false;
      }, e => { out.innerHTML = `<div class="lb-res lb-err"><small>error</small><pre class="lb-pyout">${esc(e.message || e)}</pre><p class="meta">Errors are part of learning: read the message, fix the code and run again.</p></div>`; dec.hidden = false; })
        .finally(() => { btn.disabled = false; btn.textContent = "▶ Run"; });
    }
    if (editable) { box.querySelector(".lb-run").onclick = run; box.querySelector(".lb-ed").addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") run(); if (e.key === "Tab") { e.preventDefault(); const t = e.target, s = t.selectionStart; t.value = t.value.slice(0, s) + "    " + t.value.slice(t.selectionEnd); t.selectionStart = t.selectionEnd = s + 4; } }); }
  }

  /* ---------- prompt checker (GenAI) ---------- */
  const RUBRIC = [
    [/\b(you are|act as|as an?|role)\b/i, "Role", "Tell the AI who to be, e.g. 'You are a friendly maths teacher'."],
    [/\b(write|create|summari[sz]e|explain|list|draft|classify|translate|plan|make|give)\b/i, "Clear task", "Start with an action word: write, explain, list, summarise…"],
    [/\b(for|because|about|my|our|context|audience|students?|customers?|class|manager)\b/i, "Context", "Say who it is for and why, e.g. 'for a class 5 student'."],
    [/\b(\d+\s*(words|lines|points|bullets|sentences)|table|bullet|json|format|steps?|under|short)\b/i, "Format & length", "Say how the answer should look: '5 bullet points', 'under 100 words', 'a table'."],
    [/\b(example|e\.g\.|like this|such as)\b/i, "Example", "Show one example of what you want."],
    [/\b(don't|do not|avoid|only|must|tone|simple|polite|friendly)\b/i, "Rules & tone", "Add rules: 'use simple words', 'don't use jargon', 'polite tone'."]];
  $("lb-pcheck") && ($("lb-pcheck").onclick = () => { const t = $("lb-ptext").value.trim(); if (!t) { $("lb-pres").innerHTML = '<p class="meta">Type a prompt first.</p>'; return; }
    const hits = RUBRIC.map(([re, n, tip]) => ({ n, tip, ok: re.test(t) })), score = hits.filter(h => h.ok).length;
    $("lb-pres").innerHTML = `<div class="lb-score">Prompt score: <b>${score} / ${RUBRIC.length}</b> ${score >= 5 ? "🌟 Excellent" : score >= 3 ? "👍 Good, can be better" : "✏️ Needs more detail"}</div><ul class="lb-rub">${hits.map(h => `<li class="${h.ok ? "ok" : "no"}">${h.ok ? "✅" : "➕"} <b>${h.n}</b>${h.ok ? "" : ` — ${esc(h.tip)}`}</li>`).join("")}</ul>`; });

  /* ---------- tabs, filters, deep links ---------- */
  document.querySelectorAll(".lb-seg").forEach(b => b.onclick = () => { seg = b.dataset.seg; sec = "All"; document.querySelectorAll(".lb-seg").forEach(x => x.setAttribute("aria-selected", x === b)); $("lb-play").hidden = true; list(); });
  $("lb-level").onchange = e => { lvl = e.target.value; list(); };
  function route() {
    const h = decodeURIComponent((location.hash || "").slice(1)), byId = D.c.find(c => c.id === h);
    if (byId) seg = byId.seg; else if (["pm", "data", "genai"].includes(h)) { seg = h; sec = "All"; } else if (D.c.some(c => c.sec.toLowerCase() === h.toLowerCase())) { const c = D.c.find(c => c.sec.toLowerCase() === h.toLowerCase()); seg = c.seg; sec = c.sec; }
    document.querySelectorAll(".lb-seg").forEach(x => x.setAttribute("aria-selected", x.dataset.seg === seg));
    list(); if (byId) open(byId.id);
  }
  window.addEventListener("hashchange", route); route();
  window.SNlab = { runSQL, runExcel, open };
})();
