/* Engagement: top bar, counselling pop-up, "not sure?" pop-up, application form,
   AI chat assistant, and the program sections driven by config.js. */
(function () {
  const S = typeof SITE !== "undefined" ? SITE : {}, C = typeof COURSES !== "undefined" ? COURSES : [];
  const A = typeof AUTH !== "undefined" ? AUTH : {};
  const $ = id => document.getElementById(id), { esc, waLink, R } = window.SNsite;
  const store = { get(k) { try { return localStorage.getItem(k); } catch { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch {} },
                  sget(k) { try { return sessionStorage.getItem(k); } catch { return null; } }, sset(k, v) { try { sessionStorage.setItem(k, v); } catch {} } };
  const WA_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';
  const ok = (el, kind, text) => { if (!el) return; el.className = "notice " + kind; el.textContent = text; el.hidden = !text; };
  const pub = !document.body.hasAttribute("data-app");     // LMS, admin and login pages skip pop-ups

  /* ---------- Campaign tracking: remember where the visitor came from ---------- */
  (() => { if (store.sget("src")) return; const q = new URLSearchParams(location.search);
    const utm = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "ref"].filter(k => q.get(k)).map(k => k + "=" + q.get(k).slice(0, 40)).join("&");
    let ref = ""; try { const h = document.referrer && new URL(document.referrer).hostname; if (h && h !== location.hostname) ref = "referrer=" + h; } catch {}
    store.sset("src", (utm || ref || "direct").slice(0, 200)); })();

  /* ---------- Save a lead: Supabase (if set up) and/or Web3Forms email ---------- */
  async function saveLead(row) {
    row = { ...row, source: store.sget("src") || null };
    // The site's /api/lead function saves the lead and notifies the team by email/WhatsApp.
    try { const r = await fetch(R + "api/lead", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(row) });
      if (r.ok && (await r.json()).ok) return true; } catch {}
    if (row.kind === "contact") row = { ...row, kind: "counselling", message: "[Contact form] " + (row.message || "") };
    let saved = false;
    if (A.supabaseUrl && A.supabaseKey && !/^sb_secret_/.test(A.supabaseKey)) {
      try {
        const r = await fetch(A.supabaseUrl.replace(/\/$/, "") + "/rest/v1/applications", { method: "POST",
          headers: { apikey: A.supabaseKey, ...(A.supabaseKey.startsWith("sb_") ? {} : { Authorization: "Bearer " + A.supabaseKey }), "Content-Type": "application/json", Prefer: "return=minimal" },
          body: JSON.stringify(row) });
        saved = r.ok;
      } catch {}
    }
    if (S.web3formsKey) {
      try {
        const r = await fetch("https://api.web3forms.com/submit", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({ access_key: S.web3formsKey, subject: `New SkillNavora ${row.kind}: ${row.first_name} ${row.last_name || ""}`.trim(), ...row }) });
        saved = saved || (await r.json()).success === true;
      } catch {}
    }
    return saved;
  }
  window.SNsaveLead = r => saveLead(r);
  const summary = row => Object.entries({ Program: (C.find(c => c.id === row.course_id) || {}).name, Name: [row.first_name, row.last_name].filter(Boolean).join(" "), Phone: row.phone, Email: row.email, LinkedIn: row.linkedin, Experience: row.experience, Role: row.role, "Preferred time": row.preferred_time, Message: row.message }).filter(([, v]) => v).map(([k, v]) => k + ": " + v).join("\n");

  /* ---------- Top announcement bar ---------- */
  const tb = $("topbar"), T = typeof TOPBAR !== "undefined" ? TOPBAR : {};
  if (tb && T.text && store.sget("topbarClosed") !== "1") {
    tb.querySelector("b").textContent = T.text;
    const a = tb.querySelector("a.cta"); if (T.cta) { a.textContent = T.cta + " →"; a.href = R + (T.link || "apply.html"); } else a.hidden = true;
    const t = tb.querySelector(".tag"); if (T.tag) t.textContent = T.tag; else t.hidden = true;
    tb.hidden = false;
    tb.querySelector(".x").addEventListener("click", () => { tb.hidden = true; store.sset("topbarClosed", "1"); });
  }

  /* ---------- Modals ---------- */
  const open = id => { const m = $(id); if (!m) return; document.querySelectorAll(".modal.open").forEach(x => x.classList.remove("open")); m.classList.add("open"); m.querySelector("button,input,a")?.focus(); };
  const close = m => m.classList.remove("open");
  document.querySelectorAll(".modal").forEach(m => {
    m.addEventListener("click", e => { if (e.target === m || e.target.closest("[data-close]")) close(m); });
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") document.querySelectorAll(".modal.open").forEach(close); });

  // Counselling: every "counselling" button opens a 3-step form (qualification → experience
  // and program → contact details).
  const cf = $("f-counsel");
  let step = 1;
  const STEPS = 3;
  const goStep = n => { step = n;
    cf.querySelectorAll(".mstep").forEach(x => x.hidden = +x.dataset.step !== n);
    $("mc-bar").style.width = Math.round(n / STEPS * 100) + "%";
    $("mc-back").hidden = n === 1; $("mc-next").textContent = n === STEPS ? "Book my free call" : "Next →";
    ok($("mc-err"), "", ""); };
  if (cf) {
    $("mc-courses").innerHTML = C.map(c => `<label><input type="radio" name="course" value="${esc(c.id)}"> ${esc(c.name)}</label>`).join("") + '<label><input type="radio" name="course" value=""> Not sure yet</label>';
    if (S.booking) { $("counsel-book").hidden = false; $("counsel-book").href = /^https?:/.test(S.booking) ? S.booking : "https://" + S.booking; }
    $("mc-back").addEventListener("click", () => goStep(step - 1));
  }
  document.addEventListener("click", e => {
    const t = e.target.closest("[data-counsel],[data-st-counsel],[data-open-counsel]"); if (!t || !cf) return;
    e.preventDefault();
    const id = t.dataset.counsel || document.body.dataset.course || "";
    const r = cf.querySelector(`input[name=course][value="${CSS.escape(id)}"]`); if (id && r) r.checked = true;
    cf.hidden = false; $("counsel-done").hidden = true; goStep(1);
    open("m-counsel");
  });
  if (cf) cf.addEventListener("submit", async e => {
    e.preventDefault();
    const val = n => (cf.querySelector(`input[name=${n}]:checked`) || {}).value;
    const need = { 1: [["qual", "your qualification"], ["grad", "your graduation year"]], 2: [["exp", "your experience"], ["course", "a program"]] }[step] || [];
    const miss = need.find(([n]) => val(n) === undefined);
    if (miss) return ok($("mc-err"), "error", "Please choose " + miss[1] + ".");
    if (step < STEPS) return goStep(step + 1);
    const phone = (cf.cc.value + " " + cf.phone.value.trim()).trim();
    if (!cf.name.value.trim()) return ok($("mc-err"), "error", "Please enter your name.");
    if (!/^[0-9+ ()-]{7,20}$/.test(phone) || cf.phone.value.replace(/\D/g, "").length < 7) return ok($("mc-err"), "error", "Please enter a valid phone number.");
    const row = { kind: "counselling", course_id: val("course") || null, first_name: cf.name.value.trim(), phone, email: cf.email.value.trim() || null,
      experience: val("exp"), role: val("qual"), message: "Graduation year: " + val("grad"), preferred_time: cf.time.value };
    const b = $("mc-next"); b.disabled = true; b.textContent = "Booking…";
    const saved = await saveLead(row); b.disabled = false; b.textContent = "Book my free call";
    if (saved) { cf.hidden = true; $("counsel-done").hidden = false; }
    else window.open(waLink("Hi SkillNavora, I'd like a free counselling call.\n" + summary(row)), "_blank", "noopener");
  });

  // Hero sign-up card: Google sign-up (when switched on) or the quick form.
  const lf = $("f-lead");
  if (lf) {
    if (A.google && A.supabaseUrl) {
      $("lead-google").hidden = false; $("lead-or").hidden = false;
      const loadLib = () => window.supabase ? Promise.resolve() : new Promise((res, rej) => { const sc = document.createElement("script"); sc.src = R + "assets/vendor/supabase-2.117.3.js"; sc.onload = res; sc.onerror = rej; document.head.appendChild(sc); });
      $("lead-google").addEventListener("click", async () => {
        const c = (lf.querySelector("input[name=course]:checked") || {}).value || "";
        store.set("signupCourse", c);
        try { await loadLib(); } catch { return ok($("lead-err"), "error", "Couldn't start Google sign-in. Please check your connection and try again."); }
        const sb = window.supabase.createClient(A.supabaseUrl, A.supabaseKey, { auth: { flowType: "implicit" } });
        await sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo: location.origin + "/lms.html" } });
      });
    }
    lf.addEventListener("submit", async e => {
      e.preventDefault();
      const phone = (lf.cc.value + " " + lf.phone.value.trim()).trim();
      if (!lf.name.value.trim()) return ok($("lead-err"), "error", "Please enter your name.");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(lf.email.value.trim())) return ok($("lead-err"), "error", "Please enter a valid email.");
      if (!/^[0-9+ ()-]{7,20}$/.test(phone) || lf.phone.value.replace(/\D/g, "").length < 7) return ok($("lead-err"), "error", "Please enter a valid phone number.");
      const row = { kind: "counselling", course_id: (lf.querySelector("input[name=course]:checked") || {}).value || null, first_name: lf.name.value.trim(), email: lf.email.value.trim(), phone,
        message: "Free live class + counselling (home page)." + (lf.wa.checked ? " OK to send WhatsApp updates." : " No WhatsApp updates.") };
      const b = lf.querySelector("button[type=submit]"); b.disabled = true; b.textContent = "Booking…";
      const saved = await saveLead(row); b.disabled = false; b.textContent = "Book my free session →";
      if (saved) { lf.hidden = true; $("lead-google").hidden = true; $("lead-or").hidden = true; $("lead-done").hidden = false; }
      else window.open(waLink("Hi SkillNavora, I'd like a free live class and counselling session.\n" + summary(row)), "_blank", "noopener");
    });
  }

  // Stats band (only when switched on in config.js)
  const ST = typeof STATS !== "undefined" ? STATS : null;
  if (ST && ST.show && $("stats")) {
    $("statgrid").innerHTML = (ST.items || []).map(x => `<div><b>${esc(x.n)}</b><span>${esc(x.t)}</span></div>`).join("");
    if (ST.note) $("stats-note").textContent = ST.note;
    $("stats").hidden = false;
  }

  // "Not sure if this is for you?" after N minutes on the site (once a day).
  const mins = +S.popupMinutes || 0;
  if (pub && mins > 0 && $("m-unsure")) {
    if (!store.sget("t0")) store.sset("t0", String(Date.now()));
    const today = new Date().toDateString();
    const tick = () => {
      if (store.get("unsureShown") === today || document.querySelector(".modal.open") || document.hidden) return;
      if (Date.now() - +store.sget("t0") >= mins * 60000) { store.set("unsureShown", today); open("m-unsure"); clearInterval(timer); }
    };
    const timer = setInterval(tick, 5000); tick();
    $("unsure-wa").href = waLink("Hi SkillNavora, I have a few questions about your programs.");
  }
  $("unsure-call")?.addEventListener("click", () => open("m-counsel"));

  /* ---------- Application form (apply.html) ---------- */
  const af = $("f-apply");
  if (af) {
    const q = new URLSearchParams(location.search);
    af.course.innerHTML = C.map(c => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join("");
    if (C.some(c => c.id === q.get("program"))) af.course.value = q.get("program");
    const paint = () => { const c = C.find(x => x.id === af.course.value) || C[0];
      $("apply-sub").textContent = "Take the first step towards becoming a confident, job-ready professional in " + c.name + ".";
      $("apply-ticks").innerHTML = [c.duration ? c.duration + " program" : "", "Live classes", ...(c.highlights || []).slice(0, 2)].filter(Boolean).map(t => `<span>${esc(t)}</span>`).join(""); };
    af.course.addEventListener("change", paint); paint();
    af.addEventListener("submit", async e => {
      e.preventDefault();
      if (!af.querySelector("input[name=exp]:checked")) return ok($("apply-msg"), "error", "Please choose your experience.");
      const phone = (af.cc.value + " " + af.phone.value.trim()).trim();
      if (!/^[0-9+ ()-]{7,20}$/.test(phone)) return ok($("apply-msg"), "error", "Please enter a valid contact number.");
      const li = af.linkedin.value.trim();
      const row = { kind: "application", course_id: af.course.value, first_name: af.first.value.trim(), last_name: af.last.value.trim(), email: af.email.value.trim(), phone,
        linkedin: li || null, experience: af.querySelector("input[name=exp]:checked").value, role: af.role.value, message: af.why.value.trim() || null };
      const b = af.querySelector("button[type=submit]"); b.disabled = true; b.textContent = "Submitting…";
      const saved = await saveLead(row); b.disabled = false; b.textContent = "Submit application";
      const c = C.find(x => x.id === row.course_id) || {};
      if (!saved) { window.open(waLink("Hi SkillNavora, here is my application.\n" + summary(row)), "_blank", "noopener"); ok($("apply-msg"), "info", "We opened WhatsApp with your application. Just press send."); return; }
      af.hidden = true; const d = $("apply-done"); d.hidden = false;
      d.querySelector("[data-pay]").hidden = !c.pay; if (c.pay) d.querySelector("[data-pay]").href = c.pay;
      d.querySelector("[data-wa2]").href = waLink("Hi SkillNavora, I just applied for " + (c.name || "a program") + ". My name is " + row.first_name + ".");
      scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- Early-bird timer and discounts ---------- */
  const O = typeof OFFERS !== "undefined" ? OFFERS : null;
  if (O) {
    const end = O.earlyBirdEnds && new Date(O.earlyBirdEnds), live = end && end > Date.now();
    if (live && $("eb-box")) {
      $("eb-text").textContent = O.earlyBirdText || "Early-bird offer";
      $("eb-cd").innerHTML = ["d", "h", "m", "s"].map(u => `<span><b data-cd="${u}">00</b><small>${{ d: "days", h: "hours", m: "minutes", s: "seconds" }[u]}</small></span>`).join("");
      $("eb-date").textContent = "Offer ends " + end.toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" }) + ", 11:59 pm IST.";
      $("eb-box").hidden = false;
      const tick = () => { let ms = end - Date.now(); if (ms <= 0) { $("eb-box").hidden = true; return clearInterval(t); }
        const v = { d: Math.floor(ms / 864e5), h: Math.floor(ms / 36e5) % 24, m: Math.floor(ms / 6e4) % 60, s: Math.floor(ms / 1e3) % 60 };
        document.querySelectorAll("[data-cd]").forEach(el => { el.textContent = String(v[el.dataset.cd]).padStart(2, "0"); }); };
      const t = setInterval(tick, 1000); tick();
    }
    document.querySelectorAll("#offer-list").forEach(el => { el.innerHTML = (O.items || []).map(x => `<div class="offer"><b class="pct">${esc(x.pct)}</b><div><h3>${esc(x.title)}</h3><p>${esc(x.text)}</p></div></div>`).join(""); });
    if ($("offer-note")) $("offer-note").textContent = O.note || "";
    if (!live) document.querySelectorAll(".offers").forEach(el => el.classList.add("no-eb"));
  }

  /* ---------- Mentor and careers applications ---------- */
  document.querySelectorAll("form[data-lead]").forEach(f => {
    const kind = f.dataset.lead, msg = f.querySelector("[data-lead-msg]");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const v = n => (f.elements[n] ? f.elements[n].value : "").trim(), has = n => !!f.elements[n];
      const phone = (f.cc.value + " " + v("phone")).trim();
      if (!v("name")) return ok(msg, "error", "Please enter your name.");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email"))) return ok(msg, "error", "Please enter a valid email.");
      if (!/^[0-9+ ()-]{7,20}$/.test(phone) || v("phone").replace(/\D/g, "").length < 7) return ok(msg, "error", "Please enter a valid contact number.");
      if (has("linkedin") && f.elements.linkedin.required && !/^https?:\/\/\S+$/i.test(v("linkedin"))) return ok(msg, "error", "Please add your LinkedIn profile URL (starting with https://).");
      if ((has("role") && f.elements.role.required && !v("role")) || (has("experience") && f.elements.experience.required && !v("experience"))) return ok(msg, "error", "Please choose an option in each list.");
      if (f.elements.consent && !f.elements.consent.checked) return ok(msg, "error", "Please tick the box to agree to publishing your review.");
      const extra = v("extra"), label = { mentor: "Current role", career: "Resume / portfolio", referral: "Who you are referring", hire: "Company" }[kind] || "Before → after";
      const row = { kind, first_name: v("name"), email: v("email"), phone, linkedin: v("linkedin") || null, role: v("role") || null, experience: v("experience") || null,
        message: [f.dataset.kindLabel ? "[" + f.dataset.kindLabel + "]" : "", extra ? label + ": " + extra : "", v("message")].filter(Boolean).join("\n\n").slice(0, 2000) || null };
      const b = f.querySelector("button[type=submit]"), t = b.textContent; b.disabled = true; b.textContent = "Submitting…";
      const saved = await saveLead(row); b.disabled = false; b.textContent = t;
      if (!saved) { window.open(waLink(({ mentor: "Hi SkillNavora, I'd like to become a mentor.\n", referral: "Hi SkillNavora, I'd like to refer someone.\n", hire: "Hi SkillNavora, my company is hiring.\n" }[kind] || "Hi SkillNavora, I'd like to join your team.\n") + summary(row)), "_blank", "noopener"); return ok(msg, "info", "We opened WhatsApp with your details. Just press send."); }
      f.hidden = true; f.parentNode.querySelector("[data-lead-done]").hidden = false;
    });
  });
  const ROLES = (typeof CAREERS !== "undefined" ? CAREERS : []).filter(r => r && r.title);
  if (ROLES.length && $("open-roles")) {
    $("open-roles").innerHTML = (ROLES.map(r => `<div class="card role"><div><b>${esc(r.title)}</b><div class="meta">${esc([r.team, r.type, r.location].filter(Boolean).join(" · "))}</div>${r.text ? `<p>${esc(r.text)}</p>` : ""}</div><a class="btn btn-line btn-sm" href="#career-form">Apply</a></div>`).join(""));
    $("roles-empty").hidden = true;
  }

  /* ---------- Refer & earn ---------- */
  const RF = typeof REFERRAL !== "undefined" ? REFERRAL : {};
  document.querySelectorAll("[data-reward]").forEach(el => { const amt = el.dataset.reward === "hire" ? RF.hireReward : RF.learnerReward; el.textContent = amt ? "Earn " + amt : "Earn a cash reward"; });
  if ($("ref-terms")) $("ref-terms").textContent = RF.terms || "";

  /* ---------- Program sections from config ---------- */
  const set = (id, h) => { const el = $(id); if (el) el.innerHTML = h; };
  const P = C.find(x => x.id === document.body.dataset.course);
  const AUD = (P && P.audience) || (typeof AUDIENCE !== "undefined" ? AUDIENCE : null);
  if (AUD) set("audience", AUD.map(a => `<div class="card"><h3>${esc(a.title)}</h3><p>${esc(a.text)}</p></div>`).join(""));
  if (typeof MOAT !== "undefined") set("moat", MOAT.map((m, i) => `<div class="card"><span class="num">0${i + 1}</span><h3>${esc(m.title)}</h3><p>${esc(m.text)}</p></div>`).join(""));
  if (typeof COMPARE !== "undefined") set("compare", `<table><thead><tr><th>What you get</th><th class="them">Typical online courses</th><th class="us">SkillNavora</th></tr></thead><tbody>${COMPARE.map(r => `<tr><td><b>${esc(r.what)}</b><small>${esc(r.sub)}</small></td><td class="them"><span>${esc(r.others)}</span></td><td class="us">${esc(r.us)}</td></tr>`).join("")}</tbody></table>`);
  if (typeof JOB_ASSIST !== "undefined") { set("ja-program", JOB_ASSIST.program.map(x => `<li>${esc(x)}</li>`).join("")); set("ja-interview", JOB_ASSIST.interview.map(x => `<li>${esc(x)}</li>`).join("")); }
  const M = (typeof MENTORS !== "undefined" ? MENTORS : []).filter(m => m && m.name);
  if (M.length && $("mentors")) {
    set("mentors-list", M.map(m => `<div class="card mentor">${m.photo ? `<img src="${esc(R + m.photo)}" alt="" width="96" height="96">` : `<span class="ph">${esc(m.name.trim()[0])}</span>`}<b>${esc(m.name)}</b><div class="meta">${esc(m.role || "")}</div><div class="co">${esc(m.company || "")}</div>${m.note ? `<div class="meta">${esc(m.note)}</div>` : ""}${m.linkedin ? `<a class="meta" href="${esc(m.linkedin)}" target="_blank" rel="noopener">LinkedIn ↗</a>` : ""}</div>`).join(""));
    $("mentors").hidden = false;
  }
  const TL = typeof TOOL_LINKS !== "undefined" ? TOOL_LINKS : {};
  const host = u => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return ""; } };
  const groups = P ? P.toolGroups : (C[0] || {}).toolGroups;
  if (groups) set("toolgroups", groups.map(g => `<div class="card"><h3>${esc(g.name)}</h3><div class="chips">${g.tools.map(t => { const u = TL[t]; return u ? `<a class="tl" href="${esc(u)}" target="_blank" rel="noopener noreferrer" title="Open ${esc(t)} website"><b>${esc(t)} <i aria-hidden="true">↗</i></b><small>${esc(host(u))}</small></a>` : `<span>${esc(t)}</span>`; }).join("")}</div></div>`).join(""));
  const hl = P || C[0]; if (hl) set("p-hl", (hl.highlights || []).map(h => `<span>${esc(h)}</span>`).join(""));

  /* ---------- Reviews ---------- */
  const TS = (typeof TESTIMONIALS !== "undefined" ? TESTIMONIALS : []).filter(t => t && t.quote);
  const YT = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.8 15.1V8.9l5.7 3.1z"/></svg>';
  const LI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9z"/></svg>';
  // Quote text can mark highlights with ==like this==.
  const marks = q => { let n = 0; return esc(q).replace(/==(.+?)==/g, (m, x) => `<mark class="h${n++ % 2}">${x}</mark>`); };
  const side = x => x ? `<div><small>${esc(x.role || "")}</small><b>${esc(x.company || "")}</b></div>` : "";
  const rv = t => `<figure class="rv2"><figcaption class="rv2-h">${t.photo ? `<img src="${esc(R + t.photo)}" alt="" width="40" height="40">` : `<span class="av">${esc(t.name.trim()[0])}</span>`}<b>${esc(t.name)}</b>${t.linkedin ? `<a class="li" href="${esc(t.linkedin)}" target="_blank" rel="noopener" aria-label="${esc(t.name)} on LinkedIn">${LI}</a>` : ""}</figcaption>
    <blockquote>${marks(t.quote)}</blockquote>${t.video ? `<a class="yt" href="${esc(t.video)}" target="_blank" rel="noopener">${YT}Watch story</a>` : ""}
    ${t.from || t.to ? `<div class="rv2-move">${side(t.from)}<span class="arr" aria-hidden="true">››››</span>${side(t.to)}</div>` : (t.role || t.company ? `<div class="rv2-move"><div><small>${esc(t.role || "")}</small><b>${esc(t.company || "")}</b></div></div>` : "")}</figure>`;
  if ($("reviews-wall")) $("reviews-wall").innerHTML = TS.length ? TS.map(rv).join("") : '<p class="empty">Reviews from our first learners will appear here soon. Are you a learner? Share your story below.</p>';
  if (TS.length && $("home-reviews")) { set("home-reviews-list", TS.slice(0, 6).map(rv).join("")); $("home-reviews").hidden = false; }

  /* ---------- AI chat assistant ---------- */
  if (S.chatbot && pub && $("chat")) {
    const fab = $("chat-fab"), box = $("chat"), body = $("chat-b"), inp = $("chat-in");
    fab.hidden = false;
    let hist = []; try { hist = JSON.parse(store.sget("chat") || "[]"); } catch {}
    const add = (role, text, cls = "") => { const d = document.createElement("div"); d.className = (role === "user" ? "msg-u" : "msg-a") + (cls ? " " + cls : ""); d.textContent = text; body.appendChild(d); body.scrollTop = body.scrollHeight; return d; };
    const helpLinks = () => { const d = document.createElement("div"); d.className = "sugg";
      d.innerHTML = `<button type="button" data-open-counsel>Book a free counselling call</button><a class="btn btn-wa btn-sm" href="${esc(waLink("Hi SkillNavora, I have a question."))}" target="_blank" rel="noopener">${WA_SVG} WhatsApp us</a>`; body.appendChild(d); };
    const SUG = ["What's the fee for the PM program?", "Who is the PM program for?", "Which tools will I learn?", "Do you help with jobs?", "What makes SkillNavora different?"];
    function start() {
      body.innerHTML = "";
      add("assistant", "Hi! I'm the SkillNavora assistant. Ask me anything about our programs, fees, tools, schedule or career support.");
      { const a = document.createElement("a"); a.className = "chat-tutor"; a.href = R + "ai-tutor.html"; a.textContent = "📚 Study question (SQL, PM, GenAI, English)? Ask the AI Tutor →"; body.appendChild(a); }
      if (!hist.length) { const s = document.createElement("div"); s.className = "sugg"; s.innerHTML = SUG.map(q => `<button type="button">${esc(q)}</button>`).join(""); body.appendChild(s);
        s.addEventListener("click", e => { const b = e.target.closest("button"); if (b) { s.remove(); send(b.textContent); } }); }
      hist.forEach(m => add(m.role, m.content));
    }
    // Offline answer from the FAQs when the AI isn't set up or is unavailable.
    const STOP = new Set("what whats the for and you your are how can does with this that program programs skillnavora about tell will have from into get any".split(" "));
    const SYN = { fee: "fees price cost pay", fees: "fee price cost", price: "fee fees cost", cost: "fee fees price", job: "jobs placement career", jobs: "job placement career", placement: "job jobs career", tools: "tool jira figma claude", recording: "recordings", certificate: "certificate" };
    const local = q => { let w = q.toLowerCase().split(/[^a-z0-9]+/).filter(x => x.length > 2 && !STOP.has(x));
      w = [...new Set(w.flatMap(x => [x, ...(SYN[x] || "").split(" ").filter(Boolean)]))];
      let best = null, score = 0;
      (typeof FAQS !== "undefined" ? FAQS : []).forEach(f => { const qq = f.q.toLowerCase(), aa = f.a.toLowerCase();
        const n = w.reduce((t, x) => t + (qq.includes(x) ? 3 : 0) + (aa.includes(x) ? 1 : 0), 0); if (n > score) { score = n; best = f; } });
      return best && score >= 2 ? best.a : null; };
    let busy = false;
    async function send(text) {
      text = text.trim(); if (!text || busy) return; busy = true; inp.value = "";
      add("user", text); hist.push({ role: "user", content: text.slice(0, 1500) });
      const typing = add("assistant", "Typing…", "typing");
      let reply = null;
      try {
        const r = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-15).filter((m, i, a) => !(i === 0 && m.role !== "user")) }) });
        if (r.ok) reply = (await r.json()).reply;
      } catch {}
      typing.remove();
      if (reply) { add("assistant", reply); hist.push({ role: "assistant", content: reply.slice(0, 4000) }); }
      else { hist.pop(); const f = local(text); add("assistant", f ? f + "\n\nFor anything else, our team is happy to help:" : "I can't answer that right now. Our team is happy to help:"); helpLinks(); }
      store.sset("chat", JSON.stringify(hist)); busy = false; inp.focus();
    }
    fab.addEventListener("click", () => { box.classList.add("open"); fab.hidden = true; if (!body.children.length) start(); inp.focus(); });
    $("chat-x").addEventListener("click", () => { box.classList.remove("open"); fab.hidden = false; });
    $("chat-f").addEventListener("submit", e => { e.preventDefault(); send(inp.value); });
    inp.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(inp.value); } });
  }
})();
