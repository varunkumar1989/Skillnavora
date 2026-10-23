/* Student LMS: Overview, My courses (and course view), My events, Submissions, Achievements, Profile. */
(async function () {
  const { client, $, esc, safeUrl, date, notice, setupMessage, errText } = SN;
  const msg = $("app-msg");
  if (!client) { setupMessage(msg); return; }
  const s = await SN.session();
  if (!s) return location.replace("login.html?next=" + encodeURIComponent("lms.html" + location.search));
  const uid = s.user.id, params = new URLSearchParams(location.search);
  const COURSE = id => COURSES.find(c => c.id === id);
  const STATUS = { submitted: ["Awaiting review", "wait"], reviewed: ["Reviewed", "good"], needs_changes: ["Needs changes", "warn"], open: ["Open", "wait"], done: ["Done", "good"] };
  const chip = st => { const [t, c] = STATUS[st] || [st, ""]; return `<span class="chip ${c}">${esc(t)}</span>`; };
  const time = d => new Date(d).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
  document.querySelectorAll("[data-signout]").forEach(b => b.addEventListener("click", SN.signOut));

  let me = {}, enr = [], prog = [], subs = [], events = [], regs = [], quiz = [], news = [], mats = [], reqs = [];
  async function load() {
    const q = await Promise.all([
      client.from("profiles").select("*").eq("id", uid).single(),
      client.from("enrollments").select("*").eq("user_id", uid),
      client.from("course_progress").select("*").eq("user_id", uid),
      client.from("submissions").select("*").eq("user_id", uid).order("created_at", { ascending: false }),
      client.from("events").select("*").order("starts_at", { ascending: true }),
      client.from("event_registrations").select("*").eq("user_id", uid),
      client.from("quiz_attempts").select("*").eq("user_id", uid),
      client.from("announcements").select("*").order("created_at", { ascending: false }).limit(5),
      client.from("materials").select("*").order("created_at", { ascending: true }),
      client.from("requests").select("*").eq("user_id", uid).order("created_at", { ascending: false })
    ]);
    const bad = q.find(r => r.error && r.error.message !== "not single");
    if (bad) notice(msg, "error", errText(bad.error));
    [me, enr, prog, subs, events, regs, quiz, news, mats, reqs] = q.map((r, i) => r.data || (i === 0 ? {} : []));
  }
  await load();
  $("app").hidden = false;
  const { data: isAdmin } = await client.rpc("is_admin");
  if (isAdmin) $("to-admin").hidden = false;

  /* ---------- helpers ---------- */
  const modsDone = cid => new Set(prog.filter(p => p.course_id === cid && p.done).map(p => p.module));
  const pct = cid => { const c = COURSE(cid); return c ? Math.round(modsDone(cid).size / c.curriculum.length * 100) : 0; };
  const past = e => new Date(e.ends_at || e.starts_at) < new Date();
  const myReg = id => regs.find(r => r.event_id === id);

  /* ---------- badges ---------- */
  function badges() {
    const prof = [me.full_name, me.phone, me.goal].filter(Boolean).length;
    const maxPct = Math.max(0, ...enr.map(e => pct(e.course_id)));
    const anyMod = prog.filter(p => p.done).length;
    const quizzes = new Set(quiz.filter(a => a.score / a.total >= .8).map(a => a.quiz_id)).size;
    const attended = regs.filter(r => { const e = events.find(x => x.id === r.event_id); return e && past(e); }).length;
    return [
      { t: "Getting started", d: "Complete your profile: name, phone and goal", v: prof, n: 3, c: ["#f6c66d", "#e8a93a"] },
      { t: "First steps", d: "Complete your first course module", v: Math.min(anyMod, 1), n: 1, c: ["#a78bfa", "#7457ff"] },
      { t: "Halfway there", d: "Reach 50% in any course", v: Math.min(maxPct, 50), n: 50, c: ["#7dd3fc", "#3b82f6"], unit: "%" },
      { t: "Course finisher", d: "Complete every module of a course", v: maxPct, n: 100, c: ["#6ee7b7", "#0f9f6e"], unit: "%" },
      { t: "Folio maker", d: "Submit 3 projects or challenges", v: Math.min(subs.length, 3), n: 3, c: ["#fca5a5", "#e25d8f"] },
      { t: "Challenger", d: "Submit a solution to a free challenge", v: Math.min(subs.filter(x => x.kind === "challenge").length, 1), n: 1, c: ["#fdba74", "#ea580c"] },
      { t: "Quiz whiz", d: "Score 80%+ on 3 different quizzes", v: Math.min(quizzes, 3), n: 3, c: ["#c4b5fd", "#8b5cf6"] },
      { t: "Event regular", d: "Attend 3 live events", v: Math.min(attended, 3), n: 3, c: ["#93c5fd", "#6366f1"] }
    ];
  }
  const medal = (b, i) => `<svg class="medal" viewBox="0 0 80 80" aria-hidden="true"><defs><linearGradient id="m${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${b.c[0]}"/><stop offset="1" stop-color="${b.c[1]}"/></linearGradient></defs><path d="M40 4l30 10v22c0 20-13 33-30 40C23 69 10 56 10 36V14z" fill="url(#m${i})"/><path d="M40 12l23 8v16c0 15-10 26-23 32-13-6-23-17-23-32V20z" fill="#fff" opacity=".22"/><path d="M40 24l4.5 9.5 10.5 1.3-7.7 7.2 2 10.4L40 47.3l-9.3 5.1 2-10.4-7.7-7.2 10.5-1.3z" fill="#fff"/></svg>`;

  /* ---------- header ---------- */
  function header() {
    $("hello").textContent = "Welcome" + (me.full_name ? ", " + me.full_name.split(" ")[0] : "") + "!";
    const B = badges(), got = B.filter(b => b.v >= b.n).length, C = 2 * Math.PI * 30;
    $("ring").innerHTML = `<svg class="ring" viewBox="0 0 72 72"><circle cx="36" cy="36" r="30" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="7"/><circle cx="36" cy="36" r="30" fill="none" stroke="#f5a65b" stroke-width="7" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - got / B.length)}" transform="rotate(-90 36 36)"/><text x="36" y="42" text-anchor="middle" font-family="Plus Jakarta Sans,Arial" font-weight="800" font-size="18" fill="#fff">${got}</text></svg>`;
    $("ring-text").textContent = got === B.length ? "All badges earned. Amazing!" : `${B.length - got} badges to go`;
  }

  /* ---------- tabs ---------- */
  const tabs = document.querySelectorAll("[data-tab]");
  function openTab(name) {
    $("course-view").hidden = true; $("tabbar").hidden = false;
    tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.tab === name));
    document.querySelectorAll(".panel").forEach(p => p.hidden = p.id !== "p-" + name);
    const u = new URL(location); u.searchParams.set("tab", name); u.searchParams.delete("course"); history.replaceState(null, "", u);
  }
  tabs.forEach(t => t.addEventListener("click", () => openTab(t.dataset.tab)));

  /* ---------- Overview ---------- */
  function overview() {
    const active = enr.map(e => COURSE(e.course_id)).filter(Boolean);
    $("ov-continue").innerHTML = active.length ? active.map(c => learnerCard(c)).join("") : `<p class="empty">You're not enrolled in a program yet. Explore the programs below, or <a href="#" data-goto="submissions">try a free challenge</a>.</p>`;
    const up = events.filter(e => !past(e)).slice(0, 3);
    $("ov-events").innerHTML = up.length ? up.map(eventCard).join("") : '<p class="empty">No upcoming events right now.</p>';
    $("ov-news").innerHTML = news.length ? news.map(a => `<div class="item"><div class="item-h"><b>${esc(a.title)}</b><span class="meta">${date(a.created_at)}</span></div><p>${esc(a.body)}</p></div>`).join("") : '<p class="empty">No announcements yet.</p>';
    $("ov-courses").innerHTML = COURSES.map((c, i) => `<article class="course">${SNcover(i, c.name, c.badge)}<div class="body"><h3>${esc(c.name)}</h3><p>${esc(c.short)}</p><div class="acts">${enr.some(e => e.course_id === c.id) ? `<a class="btn btn-primary btn-sm" href="?course=${c.id}" data-course="${c.id}">Go to course →</a>` : `<a class="btn btn-primary btn-sm" href="${esc(c.page)}">Learn more →</a>`}</div></div></article>`).join("");
    $("rq-list").innerHTML = reqs.length ? reqs.slice(0, 4).map(r => `<div class="item"><div class="item-h"><b>${esc(r.topic)}</b>${chip(r.status)}</div><div class="meta">${date(r.created_at)}</div></div>`).join("") : "";
  }
  const learnerCard = c => `<div class="learner"><div class="top-row"><span class="badge-ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></span><div><small>You are a learner in</small><b>${esc(c.name)}</b></div></div>
    <div class="bottom"><div style="flex:1;min-width:160px"><div class="meta" style="margin-bottom:6px">${modsDone(c.id).size} of ${c.curriculum.length} modules · ${pct(c.id)}%</div><div class="bar"><span style="width:${pct(c.id)}%"></span></div></div><a class="btn btn-primary btn-sm" href="?course=${c.id}" data-course="${c.id}">Go to course →</a></div></div>`;

  /* ---------- My courses ---------- */
  function courses() {
    const active = enr.map(e => COURSE(e.course_id)).filter(Boolean);
    $("mc-list").innerHTML = active.length ? active.map(learnerCard).join("") : `<p class="empty">No courses yet. Once you enrol, your program appears here with its recordings, materials and assignments.</p>`;
    $("mc-all").innerHTML = COURSES.filter(c => !enr.some(e => e.course_id === c.id)).map((c, i) => `<article class="course">${SNcover(COURSES.indexOf(c), c.name, c.badge)}<div class="body"><h3>${esc(c.name)}</h3><p>${esc(c.short)}</p><div class="acts"><a class="btn btn-primary btn-sm" href="${esc(c.page)}">Learn more →</a></div></div></article>`).join("");
  }

  /* ---------- Course view ---------- */
  function openCourse(cid) {
    const c = COURSE(cid);
    if (!c || !enr.some(e => e.course_id === cid)) { openTab("courses"); return notice(msg, "error", "You're not enrolled in that course yet."); }
    $("tabbar").hidden = true; document.querySelectorAll(".panel").forEach(p => p.hidden = true); $("course-view").hidden = false;
    const u = new URL(location); u.searchParams.set("course", cid); u.searchParams.delete("tab"); history.replaceState(null, "", u);
    const done = modsDone(cid), KIND = { recording: "Recording", slides: "Slides", reading: "Reading", assignment: "Assignment", link: "Link" };
    $("cv-name").textContent = c.name;
    $("cv-prog").innerHTML = `<div class="meta" style="margin-bottom:6px">${done.size} of ${c.curriculum.length} modules complete · ${pct(cid)}%</div><div class="bar"><span style="width:${pct(cid)}%"></span></div>`;
    $("cv-mods").innerHTML = c.curriculum.map((m, i) => { const mm = mats.filter(x => x.course_id === cid && x.module === i);
      return `<details class="mod${done.has(i) ? " done" : ""}"${i === 0 ? " open" : ""}><summary><input type="checkbox" data-mod="${i}" aria-label="Mark module ${i + 1} complete"${done.has(i) ? " checked" : ""}><span class="n">${String(i + 1).padStart(2, "0")}</span><span>${esc(m.title)}</span></summary>
        <ul>${(m.topics || []).map(t => `<li>${esc(t)}</li>`).join("")}</ul>
        <ul class="mats">${mm.map(x => `<li><span class="k">${KIND[x.kind] || "Link"}</span> <a href="${safeUrl(x.url)}" target="_blank" rel="noopener noreferrer">${esc(x.title)} ↗</a></li>`).join("") || '<li class="meta">Materials appear here after each live class.</li>'}
        <li><a href="?tab=submissions&course_id=${cid}&module=${i}" data-submit="${cid}|${i}">Submit this module's assignment →</a></li></ul></details>`; }).join("");
  }
  $("cv-mods").addEventListener("click", e => { if (e.target.matches("input[type=checkbox]")) e.stopPropagation(); });
  $("cv-mods").addEventListener("change", async e => {
    const cb = e.target; if (!cb.dataset.mod) return; const cid = new URLSearchParams(location.search).get("course"), m = +cb.dataset.mod;
    const { error } = await client.from("course_progress").upsert({ user_id: uid, course_id: cid, module: m, done: cb.checked, updated_at: new Date().toISOString() });
    if (error) { cb.checked = !cb.checked; return notice(msg, "error", "Couldn't save progress: " + errText(error)); }
    const row = prog.find(p => p.course_id === cid && p.module === m); if (row) row.done = cb.checked; else prog.push({ course_id: cid, module: m, done: cb.checked });
    cb.closest(".mod").classList.toggle("done", cb.checked);
    $("cv-prog").innerHTML = `<div class="meta" style="margin-bottom:6px">${modsDone(cid).size} of ${COURSE(cid).curriculum.length} modules complete · ${pct(cid)}%</div><div class="bar"><span style="width:${pct(cid)}%"></span></div>`;
    header();
  });
  $("cv-back").addEventListener("click", () => { openTab("courses"); paintAll(); });

  /* ---------- Events ---------- */
  function eventCard(e) {
    const d = new Date(e.starts_at), r = myReg(e.id), isPast = past(e);
    let foot;
    if (!isPast) foot = r ? `<span>You're registered ✓</span><span style="display:flex;gap:8px">${e.join_url ? `<a class="btn btn-primary btn-sm" href="${safeUrl(e.join_url)}" target="_blank" rel="noopener noreferrer">Join</a>` : ""}<button class="btn btn-line btn-sm" data-unreg="${e.id}">Cancel</button></span>` : `<span>Free for learners</span><button class="btn btn-primary btn-sm" data-reg="${e.id}">Register</button>`;
    else foot = r ? `<span>How was the session?</span><span class="stars" data-rate="${e.id}">${[1, 2, 3, 4, 5].map(n => `<button aria-label="${n} star${n > 1 ? "s" : ""}" data-n="${n}" class="${r.rating >= n ? "on" : ""}">★</button>`).join("")}</span>` : `<span class="meta">Completed</span>`;
    return `<div class="event"><div class="top-row"><div class="cal"><small>${d.toLocaleDateString("en-IN", { month: "short" })}</small><b>${d.getDate()}</b></div><div><h4>${esc(e.title)}</h4><div class="meta">${time(e.starts_at)}${e.ends_at ? " – " + time(e.ends_at) : ""}</div>${e.description ? `<p class="meta" style="margin:6px 0 0">${esc(e.description)}</p>` : ""}</div></div><div class="bottom">${foot}</div></div>`;
  }
  function eventsTab() {
    const up = events.filter(e => !past(e)), done = events.filter(e => past(e) && myReg(e.id)).reverse();
    $("ev-up").innerHTML = up.length ? up.map(eventCard).join("") : '<p class="empty">No upcoming events. New live sessions are announced here.</p>';
    $("ev-done").innerHTML = done.length ? done.map(eventCard).join("") : '<p class="empty">Events you attend show up here so you can rate them.</p>';
  }
  document.addEventListener("click", async e => {
    const t = e.target.closest("[data-reg],[data-unreg],[data-n],[data-course],[data-goto],[data-submit]"); if (!t) return;
    if (t.dataset.course) { e.preventDefault(); return openCourse(t.dataset.course); }
    if (t.dataset.goto) { e.preventDefault(); return openTab(t.dataset.goto); }
    if (t.dataset.submit) { e.preventDefault(); const [cid, m] = t.dataset.submit.split("|"); openTab("submissions"); prefill(cid, m); return; }
    let error;
    if (t.dataset.reg) ({ error } = await client.from("event_registrations").insert({ event_id: +t.dataset.reg }));
    else if (t.dataset.unreg) ({ error } = await client.from("event_registrations").delete().eq("event_id", +t.dataset.unreg));
    else if (t.dataset.n) { const id = +t.closest("[data-rate]").dataset.rate; ({ error } = await client.from("event_registrations").update({ rating: +t.dataset.n }).eq("event_id", id)); }
    if (error) return notice(msg, "error", errText(error));
    regs = (await client.from("event_registrations").select("*").eq("user_id", uid)).data || [];
    paintAll();
  });

  /* ---------- Submissions ---------- */
  const sf = $("f-submit");
  function fillTargets() {
    const opts = [];
    enr.forEach(e => { const c = COURSE(e.course_id); if (c) c.curriculum.forEach((m, i) => opts.push([`a|${c.id}|${i}`, `${c.name} · Module ${i + 1}: ${m.title}`])); });
    CHALLENGES.forEach(c => opts.push([`c||${c.id}`, `Free challenge: ${c.title}`]));
    sf.target.innerHTML = opts.map(([v, t]) => `<option value="${esc(v)}">${esc(t)}</option>`).join("");
  }
  function prefill(cid, m) { const v = cid ? `a|${cid}|${m}` : `c||${m}`; if ([...sf.target.options].some(o => o.value === v)) sf.target.value = v; sf.title.focus(); }
  function subsTab() {
    $("s-list").innerHTML = subs.length ? subs.map(r => { const c = COURSE(r.course_id), ch = CHALLENGES.find(x => x.id === r.item);
      const where = r.kind === "challenge" ? "Challenge" + (ch ? ": " + ch.title : "") : (c ? c.name + " · Module " + (+r.item + 1) : "Assignment");
      return `<div class="item"><div class="item-h"><b>${esc(r.title)}</b>${chip(r.status)}</div>
      <div class="meta">${esc(where)} · ${date(r.created_at)} · <a href="${safeUrl(r.link)}" target="_blank" rel="noopener noreferrer">Open link</a></div>
      ${r.notes ? `<p>${esc(r.notes)}</p>` : ""}${r.feedback ? `<div class="fb"><small>Feedback${r.reviewed_at ? " · " + date(r.reviewed_at) : ""}</small>${esc(r.feedback)}</div>` : ""}
      ${r.status === "submitted" ? `<button class="link-btn" data-del="${r.id}">Withdraw</button>` : ""}</div>`; }).join("") : '<p class="empty">Nothing submitted yet.</p>';
  }
  sf.addEventListener("submit", async e => {
    e.preventDefault(); const [k, cid, item] = sf.target.value.split("|");
    const row = { kind: k === "c" ? "challenge" : "assignment", course_id: cid || null, item, title: sf.title.value.trim(), link: sf.link.value.trim(), notes: sf.notes.value.trim() || null };
    if (!/^https?:\/\//i.test(row.link)) return notice($("s-msg"), "error", "Please paste a full link starting with https://");
    const { error } = await client.from("submissions").insert(row);
    notice($("s-msg"), error ? "error" : "ok", error ? errText(error) : "Submitted! Feedback will appear here once it's reviewed.");
    if (!error) { sf.reset(); subs = (await client.from("submissions").select("*").eq("user_id", uid).order("created_at", { ascending: false })).data || []; paintAll(); }
  });
  $("s-list").addEventListener("click", async e => { const id = e.target.dataset.del; if (!id || !confirm("Withdraw this submission?")) return;
    const { error } = await client.from("submissions").delete().eq("id", id); if (error) return notice(msg, "error", errText(error));
    subs = subs.filter(x => String(x.id) !== id); paintAll(); });

  /* ---------- Achievements ---------- */
  function achievements() {
    $("ach").innerHTML = badges().map((b, i) => { const ok = b.v >= b.n; return `<div class="badge${ok ? "" : " locked"}">${medal(b, i)}<h4>${esc(b.t)}</h4><p>${esc(b.d)}</p>${ok ? '<span class="earned">✓ Earned</span>' : `<div class="bar"><span style="width:${Math.round(b.v / b.n * 100)}%"></span></div><div class="meta" style="margin-top:6px">${b.v}${b.unit || ""} / ${b.n}${b.unit || ""}</div>`}</div>`; }).join("");
    const best = {}; quiz.forEach(a => { if (!best[a.quiz_id] || a.score > best[a.quiz_id].score) best[a.quiz_id] = a; });
    $("ach-quiz").innerHTML = Object.keys(best).length ? Object.values(best).map(a => { const q = QUIZZES.find(x => x.id === a.quiz_id); return `<div class="item"><div class="item-h"><b>${esc(q ? q.title : a.quiz_id)}</b><span class="chip ${a.score / a.total >= .8 ? "good" : ""}">${a.score} / ${a.total}</span></div></div>`; }).join("") : `<p class="empty">Take a quiz in the <a href="quiz.html">Quiz zone</a> to see your scores here.</p>`;
  }

  /* ---------- Profile and help ---------- */
  const pf = $("f-profile");
  function profile() { ["full_name", "phone", "linkedin", "goal"].forEach(k => pf[k].value = me[k] || ""); pf.email.value = s.user.email; }
  pf.addEventListener("submit", async e => { e.preventDefault();
    const upd = { full_name: pf.full_name.value.trim(), phone: pf.phone.value.trim(), linkedin: pf.linkedin.value.trim(), goal: pf.goal.value.trim() };
    const { error } = await client.from("profiles").update(upd).eq("id", uid);
    notice($("pf-msg"), error ? "error" : "ok", error ? errText(error) : "Profile saved.");
    if (!error) { Object.assign(me, upd); header(); achievements(); } });
  $("f-help").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const { error } = await client.from("requests").insert({ topic: f.topic.value, message: f.message.value.trim() });
    notice($("rq-msg"), error ? "error" : "ok", error ? errText(error) : "Request sent. We'll get back to you soon.");
    if (!error) { f.reset(); reqs = (await client.from("requests").select("*").eq("user_id", uid).order("created_at", { ascending: false })).data || []; overview(); } });

  function paintAll() { header(); overview(); courses(); eventsTab(); subsTab(); achievements(); profile(); }
  fillTargets(); paintAll();
  const ch = params.get("challenge"), cid = params.get("course_id");
  if (params.get("course")) openCourse(params.get("course"));
  else { openTab(params.get("tab") || "overview"); if (ch) prefill(null, ch); else if (cid) prefill(cid, params.get("module")); }
})();
