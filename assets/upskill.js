/* Upskill for free: Quiz zone, Challenges and Practice with AI. */
(function () {
  const $ = id => document.getElementById(id);
  const { esc } = window.SNsite;
  const page = document.body.dataset.page;
  const store = { get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
                  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} } };

  /* =============================== QUIZ ZONE =============================== */
  if (page === "quiz") {
    const list = $("quiz-list"), play = $("quiz-play");
    const best = store.get("quizBest", {});
    function renderList() {
      list.innerHTML = QUIZZES.map(q => `<div class="card"><div class="row" style="display:flex;gap:8px"><span class="tag">${esc(q.track)}</span><span class="tag g">${esc(q.level)}</span></div>
        <h3 style="margin-top:6px">${esc(q.title)}</h3><p>${q.questions.length} questions · about ${Math.ceil(q.questions.length * .75)} minutes</p>
        ${best[q.id] != null ? `<span class="best">Your best: ${best[q.id]} / ${q.questions.length}</span>` : ""}
        <button class="btn btn-primary btn-sm" style="align-self:flex-start;margin-top:auto" data-start="${esc(q.id)}">${best[q.id] != null ? "Try again" : "Start quiz"} →</button></div>`).join("");
    }
    renderList();
    list.addEventListener("click", e => { const id = e.target.closest("[data-start]")?.dataset.start; if (id) start(QUIZZES.find(q => q.id === id)); });
    const startFromHash = () => { const q = QUIZZES.find(x => "#" + x.id === location.hash); if (q) start(q); };
    startFromHash();

    let quiz, i, score, answers;
    function start(q) { quiz = q; i = 0; score = 0; answers = []; list.hidden = true; $("quiz-intro").hidden = true; play.hidden = false; show(); scrollTo({ top: play.offsetTop - 90, behavior: "smooth" }); }
    function show() {
      const it = quiz.questions[i];
      play.innerHTML = `<div class="card qcard"><div class="meta" style="display:flex;justify-content:space-between"><span>${esc(quiz.title)}</span><span>Question ${i + 1} of ${quiz.questions.length}</span></div>
        <div class="qprog"><span style="width:${i / quiz.questions.length * 100}%"></span></div>
        <p class="qq">${esc(it.q)}</p><div class="opts">${it.o.map((o, k) => `<button class="opt" data-k="${k}"><span class="k">${"ABCD"[k]}</span><span>${esc(o)}</span></button>`).join("")}</div>
        <div id="why"></div><div class="qnav"><button class="btn btn-line btn-sm" id="q-quit">Quit</button><button class="btn btn-primary btn-sm" id="q-next" hidden>${i + 1 === quiz.questions.length ? "See results" : "Next question"} →</button></div></div>`;
      play.querySelector(".opts").addEventListener("click", e => {
        const b = e.target.closest(".opt"); if (!b) return; const k = +b.dataset.k;
        play.querySelectorAll(".opt").forEach(x => { x.disabled = true; if (+x.dataset.k === it.a) x.classList.add("right"); });
        if (k !== it.a) b.classList.add("wrong"); else score++;
        answers.push(k);
        $("why").innerHTML = `<div class="why"><b>${k === it.a ? "Correct!" : "Not quite."}</b> ${esc(it.why)}</div>`;
        $("q-next").hidden = false; $("q-next").focus();
      });
      $("q-next").addEventListener("click", () => { i++; i < quiz.questions.length ? show() : finish(); });
      $("q-quit").addEventListener("click", reset);
    }
    async function finish() {
      const n = quiz.questions.length, pct = Math.round(score / n * 100);
      if (best[quiz.id] == null || score > best[quiz.id]) { best[quiz.id] = score; store.set("quizBest", best); }
      const C = 2 * Math.PI * 62;
      play.innerHTML = `<div class="card qcard center"><svg class="score-ring" viewBox="0 0 150 150"><circle cx="75" cy="75" r="62" fill="none" stroke="var(--line)" stroke-width="12"/><circle cx="75" cy="75" r="62" fill="none" stroke="url(#sg)" stroke-width="12" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - score / n)}" transform="rotate(-90 75 75)"/><defs><linearGradient id="sg"><stop offset="0" stop-color="#1f5eff"/><stop offset="1" stop-color="#ff7a1a"/></linearGradient></defs><text x="75" y="84" text-anchor="middle" font-family="Plus Jakarta Sans,Arial" font-weight="800" font-size="30" fill="currentColor">${score}/${n}</text></svg>
        <h2 class="sec-h" style="font-size:28px">${pct >= 80 ? "Excellent work! 🎉" : pct >= 50 ? "Good effort!" : "Keep practising!"}</h2>
        <p class="meta" id="saved">${pct}% correct.</p>
        <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px"><button class="btn btn-primary btn-sm" id="q-again">Try again</button><button class="btn btn-line btn-sm" id="q-all">All quizzes</button></div>
        <details style="text-align:left;margin-top:22px"><summary style="cursor:pointer;font-weight:700">Review answers</summary><ol style="padding-left:20px">${quiz.questions.map((q, k) => `<li style="margin:12px 0"><b>${esc(q.q)}</b><br><span class="meta">Correct: ${esc(q.o[q.a])}${answers[k] !== q.a ? ` · You chose: ${esc(q.o[answers[k]])}` : " ✓"}</span></li>`).join("")}</ol></details></div>`;
      $("q-again").addEventListener("click", () => start(quiz));
      $("q-all").addEventListener("click", reset);
      // Save to the LMS when signed in (counts towards achievements).
      if (typeof SN !== "undefined" && SN.client && await SN.session()) {
        const { error } = await SN.client.from("quiz_attempts").insert({ quiz_id: quiz.id, score, total: n });
        if (!error) $("saved").textContent = pct + "% correct. Saved to your LMS achievements.";
      } else if (typeof SN !== "undefined" && SN.client) $("saved").innerHTML = `${pct}% correct. <a href="login.html">Log in</a> to save your scores and earn badges.`;
    }
    function reset() { play.hidden = true; list.hidden = false; $("quiz-intro").hidden = false; renderList(); history.replaceState(null, "", location.pathname); }
  }

  /* =============================== CHALLENGES =============================== */
  if (page === "challenges") {
    const grid = $("chal-list"), tracks = ["All", ...new Set(CHALLENGES.map(c => c.track))];
    $("chal-filters").innerHTML = tracks.map((t, i) => `<button type="button" aria-pressed="${i === 0}" data-t="${esc(t)}">${esc(t)}</button>`).join("");
    const render = t => grid.innerHTML = CHALLENGES.filter(c => t === "All" || c.track === t).map(c => `<article class="card chal" id="${esc(c.id)}">
      <div class="row"><span class="tag">${esc(c.track)}</span><span class="tag g">${esc(c.level)}</span><span class="meta">⏱ ${esc(c.time)}</span></div>
      <h3>${esc(c.title)}</h3><p>${esc(c.brief)}</p><div><b style="font-size:14px">What to submit</b><ul>${c.deliver.map(d => `<li>${esc(d)}</li>`).join("")}</ul></div>
      <a class="btn btn-primary btn-sm" style="align-self:flex-start;margin-top:auto" href="lms.html?tab=submissions&challenge=${encodeURIComponent(c.id)}">Submit your solution →</a></article>`).join("");
    render("All");
    $("chal-filters").addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; $("chal-filters").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); render(b.dataset.t); });
  }

  /* ============================ PRACTICE WITH AI ============================ */
  if (page === "practice") {
    const role = $("pr-role"), type = $("pr-type"), qEl = $("pr-q"), ans = $("pr-answer");
    role.innerHTML = Object.keys(PRACTICE).map(r => `<option>${esc(r)}</option>`).join("");
    const fillTypes = () => { type.innerHTML = Object.keys(PRACTICE[role.value]).map(t => `<option>${esc(t)}</option>`).join(""); next(); };
    let current = "";
    function next() { const pool = PRACTICE[role.value][type.value]; let q; do { q = pool[Math.floor(Math.random() * pool.length)]; } while (pool.length > 1 && q === current); current = q; qEl.textContent = q; ans.value = store.get("practice:" + q, ""); resetTimer(); }
    role.addEventListener("change", fillTypes); type.addEventListener("change", next); $("pr-next").addEventListener("click", next);
    ans.addEventListener("input", () => store.set("practice:" + current, ans.value));
    // Timer
    let secs = 300, t = null; const tEl = $("pr-timer"), tb = $("pr-start");
    const paint = () => tEl.textContent = String(Math.floor(secs / 60)).padStart(2, "0") + ":" + String(secs % 60).padStart(2, "0");
    function resetTimer() { clearInterval(t); t = null; secs = +$("pr-mins").value * 60; paint(); tb.textContent = "Start timer"; }
    tb.addEventListener("click", () => { if (t) { clearInterval(t); t = null; tb.textContent = "Resume"; return; } tb.textContent = "Pause";
      t = setInterval(() => { secs--; paint(); if (secs <= 0) { clearInterval(t); t = null; tb.textContent = "Start timer"; tEl.textContent = "Time's up!"; } }, 1000); });
    $("pr-mins").addEventListener("change", resetTimer); $("pr-reset").addEventListener("click", resetTimer);
    // AI feedback prompt
    const prompt = () => `You are an experienced interviewer for ${role.value} roles. Evaluate my answer to this ${type.value.toLowerCase()} interview question.\n\nQuestion: ${current}\n\nMy answer:\n${ans.value.trim() || "(I haven't written an answer yet. Ask me clarifying questions first, then let me answer, and then evaluate me.)"}\n\nPlease give: 1) a score out of 10, 2) what was strong, 3) what was missing or weak, 4) a model answer outline, and 5) two follow-up questions an interviewer would ask. Be specific and honest.`;
    const open = base => window.open(base + encodeURIComponent(prompt()), "_blank", "noopener");
    $("pr-claude") && $("pr-claude").addEventListener("click", () => open("https://claude.ai/new?q="));
    $("pr-chatgpt") && $("pr-chatgpt").addEventListener("click", () => open("https://chatgpt.com/?q="));
    $("pr-copy").addEventListener("click", async () => { try { await navigator.clipboard.writeText(prompt()); $("pr-copied").textContent = "Copied! Paste it into any AI assistant."; } catch { $("pr-copied").textContent = "Couldn't copy. Select the text and copy it manually."; } });
    fillTypes();
  }
})();
