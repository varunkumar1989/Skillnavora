/* Admin panel. Every action is also checked by the database rules, so this
   page can't do anything a non-admin account isn't allowed to. */
(async function () {
  const { client, $, esc, safeUrl, date, notice, setupMessage, errText } = SN;
  const msg = $("app-msg");
  if (!client) { setupMessage(msg); return; }
  const s = await SN.session();
  if (!s) return location.replace("login.html?next=admin.html");
  document.querySelectorAll("[data-signout]").forEach(b => b.addEventListener("click", SN.signOut));
  const { data: isAdmin, error: adminErr } = await client.rpc("is_admin");
  if (!isAdmin) {
    // Show which account is signed in, and the exact SQL that makes it an admin.
    const email = (s.user && s.user.email) || "";
    $("denied-email").textContent = email || "(no email on this account)";
    $("denied-sql").textContent = adminErr
      ? "-- The database tables are missing. Run supabase/schema.sql first, then run this again."
      : "insert into public.profiles (id, email)\n  select id, email from auth.users where email = '" + email.replace(/'/g, "''") + "'\n  on conflict (id) do nothing;\nupdate public.profiles set role = 'admin'\n  where id = (select id from auth.users where email = '" + email.replace(/'/g, "''") + "');";
    $("refresh").addEventListener("click", () => location.reload());
    $("denied").hidden = false; return;
  }
  $("app").hidden = false;

  const COURSE = id => COURSES.find(c => c.id === id);
  const cname = id => (COURSE(id) || {}).name || id || "";
  const STATUS = { submitted: ["Awaiting review", "wait"], reviewed: ["Reviewed", "good"], needs_changes: ["Needs changes", "warn"], open: ["Open", "wait"], done: ["Done", "good"] };
  const chip = st => { const [t, c] = STATUS[st] || [st, ""]; return `<span class="chip ${c}">${esc(t)}</span>`; };
  const ok = (el, error, text) => { notice($(el), error ? "error" : "ok", error ? errText(error) : text); return !error; };
  const courseOpts = COURSES.map(c => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join("");
  document.querySelectorAll("select[data-courses]").forEach(sel => sel.innerHTML = courseOpts);

  // Tabs
  const tabs = document.querySelectorAll("[data-tab]");
  const openTab = n => { tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.tab === n)); document.querySelectorAll(".panel").forEach(p => p.hidden = p.id !== "p-" + n); };
  tabs.forEach(t => t.addEventListener("click", () => openTab(t.dataset.tab)));

  let people = {}, enr = [], prog = [], subs = [], reqs = [], events = [], regs = [], mats = [], news = [], apps = [], jobs = [];
  const who = id => people[id] ? (people[id].full_name || people[id].email) : "Unknown";
  async function load() {
    const q = await Promise.all([
      client.from("profiles").select("*").order("created_at", { ascending: false }),
      client.from("enrollments").select("*"), client.from("course_progress").select("*").eq("done", true),
      client.from("submissions").select("*").order("created_at", { ascending: false }),
      client.from("requests").select("*").order("created_at", { ascending: false }),
      client.from("events").select("*").order("starts_at", { ascending: false }),
      client.from("event_registrations").select("*"),
      client.from("materials").select("*").order("created_at", { ascending: true }),
      client.from("announcements").select("*").order("created_at", { ascending: false }),
      client.from("applications").select("*").order("created_at", { ascending: false }),
      client.from("jobs").select("*").order("posted_on", { ascending: false })
    ]);
    const bad = q.find(r => r.error); if (bad) notice(msg, "error", errText(bad.error));
    let p; [p, enr, prog, subs, reqs, events, regs, mats, news, apps, jobs] = q.map(r => r.data || []);
    people = Object.fromEntries(p.map(x => [x.id, x]));
    paint();
  }

  function paint() {
    const waiting = subs.filter(x => x.status === "submitted").length, open = reqs.filter(x => x.status === "open").length;
    const up = events.filter(e => new Date(e.starts_at) > new Date()).length;
    $("o-students").textContent = Object.values(people).filter(x => x.role === "student").length;
    $("o-enr").textContent = enr.length; $("o-waiting").textContent = waiting; $("o-open").textContent = open; $("o-events").textContent = up;
    $("n-subs").textContent = waiting || ""; $("n-subs").hidden = !waiting; $("n-reqs").textContent = open || ""; $("n-reqs").hidden = !open;
    $("o-courses").innerHTML = COURSES.map(c => { const e = enr.filter(x => x.course_id === c.id);
      return `<tr><td><b>${esc(c.name)}</b><div class="meta">${esc(c.id)}</div></td><td>${e.length}</td><td>${mats.filter(m => m.course_id === c.id).length}</td><td>${subs.filter(x => x.course_id === c.id).length}</td></tr>`; }).join("");
    const fresh = apps.filter(a => a.status === "new").length;
    $("o-apps").textContent = fresh; $("n-apps").textContent = fresh || ""; $("n-apps").hidden = !fresh;
    students(); enrolments(); materials(); submissions(); eventsTab(); requests(); announcements(); admins(); applications(); jobsTab();
  }

  /* ---------- Students ---------- */
  function students() {
    const q = $("st-q").value.trim().toLowerCase();
    const rows = Object.values(people).filter(x => !q || [x.full_name, x.email, x.phone, x.goal].join(" ").toLowerCase().includes(q));
    $("st-rows").innerHTML = rows.length ? rows.map(x => { const e = enr.filter(y => y.user_id === x.id);
      return `<tr><td><b>${esc(x.full_name || "—")}</b>${x.role === "admin" ? ' <span class="chip good">Admin</span>' : ""}<div class="meta">${esc(x.email)}</div></td>
      <td>${esc(x.phone || "")}${x.linkedin ? `<div><a href="${safeUrl(/^https?:/i.test(x.linkedin) ? x.linkedin : "https://" + x.linkedin)}" target="_blank" rel="noopener noreferrer">LinkedIn</a></div>` : ""}</td>
      <td>${esc(x.goal || "")}</td><td>${e.map(y => { const c = COURSE(y.course_id), n = prog.filter(p => p.user_id === x.id && p.course_id === y.course_id).length, t = c ? c.curriculum.length : 1;
        return `<div style="margin-bottom:6px"><span class="meta">${esc(cname(y.course_id))}</span><div class="bar mini"><span style="width:${Math.round(n / t * 100)}%"></span></div></div>`; }).join("") || '<span class="meta">Not enrolled</span>'}</td>
      <td>${subs.filter(y => y.user_id === x.id).length}</td><td class="meta">${date(x.created_at)}</td></tr>`; }).join("") : '<tr><td colspan="6" class="empty">No matching accounts.</td></tr>';
  }
  $("st-q").addEventListener("input", students);

  /* ---------- Enrolments ---------- */
  function enrolments() {
    $("en-rows").innerHTML = enr.length ? enr.map(e => `<tr><td><b>${esc(who(e.user_id))}</b><div class="meta">${esc((people[e.user_id] || {}).email || "")}</div></td><td>${esc(cname(e.course_id))}</td><td>${chip(e.status === "active" ? "open" : "done").replace("Open", "Active")}</td><td class="meta">${date(e.created_at)}</td>
      <td><button class="btn btn-line btn-sm" data-enstatus="${esc(e.user_id)}|${esc(e.course_id)}|${e.status === "active" ? "completed" : "active"}">${e.status === "active" ? "Mark completed" : "Reactivate"}</button> <button class="link-btn" data-unenrol="${esc(e.user_id)}|${esc(e.course_id)}">Remove</button></td></tr>`).join("") : '<tr><td colspan="5" class="empty">No enrolments yet.</td></tr>';
  }
  $("f-enrol").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const { error } = await client.rpc("enroll", { target_email: f.email.value.trim(), course: f.course.value });
    if (ok("en-msg", error, `Enrolled ${f.email.value.trim()} in ${cname(f.course.value)}. They'll see it in their LMS.`)) { f.email.value = ""; load(); } });

  /* ---------- Materials ---------- */
  function materials() {
    const cid = $("f-mat").course.value, c = COURSE(cid);
    $("f-mat").module.innerHTML = c ? c.curriculum.map((m, i) => `<option value="${i}">Module ${i + 1}: ${esc(m.title)}</option>`).join("") : "";
    const rows = mats.filter(m => m.course_id === cid);
    $("mat-list").innerHTML = rows.length ? rows.map(m => `<div class="item"><div class="item-h"><b>${esc(m.title)}</b><span class="chip">${esc(m.kind)}</span></div><div class="meta">Module ${m.module + 1}${c && c.curriculum[m.module] ? ": " + esc(c.curriculum[m.module].title) : ""} · <a href="${safeUrl(m.url)}" target="_blank" rel="noopener noreferrer">Open</a></div><button class="link-btn" data-delmat="${m.id}">Delete</button></div>`).join("") : '<p class="empty">No materials for this course yet.</p>';
  }
  $("f-mat").course.addEventListener("change", materials);
  $("f-mat").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const row = { course_id: f.course.value, module: +f.module.value, title: f.title.value.trim(), url: f.url.value.trim(), kind: f.kind.value };
    const { error } = await client.from("materials").insert(row);
    if (ok("mat-msg", error, "Added. Enrolled students can see it now.")) { const keep = f.module.value; f.title.value = ""; f.url.value = ""; await load(); f.module.value = keep; } });

  /* ---------- Submissions ---------- */
  function submissions() {
    const filter = $("sub-filter").value, rows = subs.filter(x => filter === "all" || x.status === filter);
    $("sub-list").innerHTML = rows.length ? rows.map(r => { const ch = CHALLENGES.find(x => x.id === r.item);
      const where = r.kind === "challenge" ? "Challenge" + (ch ? ": " + ch.title : "") : cname(r.course_id) + " · Module " + (+r.item + 1);
      return `<div class="item" data-id="${r.id}"><div class="item-h"><b>${esc(r.title)}</b>${chip(r.status)}</div>
      <div class="meta">${esc(who(r.user_id))} · ${esc(where)} · ${date(r.created_at)} · <a href="${safeUrl(r.link)}" target="_blank" rel="noopener noreferrer">Open link</a></div>
      ${r.notes ? `<p>${esc(r.notes)}</p>` : ""}
      <div class="review"><label>Feedback<textarea data-f>${esc(r.feedback || "")}</textarea></label>
      <div class="row2"><label>Status<select data-s>${["reviewed", "needs_changes", "submitted"].map(v => `<option value="${v}"${(r.status === "submitted" ? v === "reviewed" : r.status === v) ? " selected" : ""}>${STATUS[v][0]}</option>`).join("")}</select></label><button class="btn btn-primary btn-sm" data-save>Save review</button></div></div></div>`; }).join("") : '<p class="empty">Nothing here. 🎉</p>';
  }
  $("sub-filter").addEventListener("change", submissions);
  $("sub-list").addEventListener("click", async e => { if (!e.target.matches("[data-save]")) return; const box = e.target.closest(".item"), id = box.dataset.id;
    const upd = { feedback: box.querySelector("[data-f]").value.trim() || null, status: box.querySelector("[data-s]").value, reviewed_at: new Date().toISOString() };
    e.target.disabled = true; const { error } = await client.from("submissions").update(upd).eq("id", id); e.target.disabled = false;
    if (error) return notice(msg, "error", errText(error));
    Object.assign(subs.find(x => String(x.id) === id), upd); notice(msg, "ok", "Review saved. The student can see it in their LMS."); paint(); });

  /* ---------- Events ---------- */
  function eventsTab() {
    $("ev-list").innerHTML = events.length ? events.map(ev => { const r = regs.filter(x => x.event_id === ev.id), rated = r.filter(x => x.rating);
      const avg = rated.length ? (rated.reduce((a, x) => a + x.rating, 0) / rated.length).toFixed(1) : null;
      return `<div class="item"><div class="item-h"><b>${esc(ev.title)}</b><span class="meta">${new Date(ev.starts_at).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}</span></div>
      <div class="meta">${r.length} registered${avg ? ` · ★ ${avg} from ${rated.length} rating${rated.length > 1 ? "s" : ""}` : ""}${ev.join_url ? ` · <a href="${safeUrl(ev.join_url)}" target="_blank" rel="noopener noreferrer">Join link</a>` : ""}</div>
      ${ev.description ? `<p>${esc(ev.description)}</p>` : ""}<button class="link-btn" data-delev="${ev.id}">Delete</button></div>`; }).join("") : '<p class="empty">No events yet.</p>';
  }
  $("f-event").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const row = { title: f.title.value.trim(), description: f.description.value.trim() || null, starts_at: new Date(f.starts.value).toISOString(), ends_at: f.ends.value ? new Date(f.ends.value).toISOString() : null, join_url: f.join_url.value.trim() || null };
    const { error } = await client.from("events").insert(row);
    if (ok("ev-msg", error, "Event created. Students can register in their LMS.")) { f.reset(); load(); } });

  /* ---------- Requests ---------- */
  function requests() {
    const filter = $("req-filter").value, rows = reqs.filter(x => filter === "all" || x.status === filter);
    $("req-list").innerHTML = rows.length ? rows.map(r => { const p = people[r.user_id] || {};
      return `<div class="item"><div class="item-h"><b>${esc(r.topic)}</b>${chip(r.status)}</div><div class="meta">${esc(who(r.user_id))} · ${esc(p.email || "")}${p.phone ? " · " + esc(p.phone) : ""} · ${date(r.created_at)}</div><p>${esc(r.message)}</p>
      <button class="btn btn-line btn-sm" style="margin-top:10px" data-req="${r.id}" data-to="${r.status === "open" ? "done" : "open"}">${r.status === "open" ? "Mark as done" : "Reopen"}</button></div>`; }).join("") : '<p class="empty">No requests here.</p>';
  }
  $("req-filter").addEventListener("change", requests);

  /* ---------- Announcements ---------- */
  function announcements() {
    $("news-list").innerHTML = news.length ? news.map(a => `<div class="item"><div class="item-h"><b>${esc(a.title)}</b><span class="meta">${date(a.created_at)}</span></div><p>${esc(a.body)}</p><button class="link-btn" data-delnews="${a.id}">Delete</button></div>`).join("") : '<p class="empty">No announcements yet.</p>';
  }
  $("f-news").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const { error } = await client.from("announcements").insert({ title: f.title.value.trim(), body: f.body.value.trim() });
    if (ok("news-msg", error, "Posted. Students see it on their LMS overview.")) { f.reset(); load(); } });

  /* ---------- Admins ---------- */
  function admins() { $("adm-list").innerHTML = Object.values(people).filter(x => x.role === "admin").map(x => `<div class="item"><b>${esc(x.full_name || x.email)}</b> <span class="meta">${esc(x.email)}</span></div>`).join(""); }
  $("f-role").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const { error } = await client.rpc("set_role", { target_email: f.email.value.trim(), new_role: f.role.value });
    if (ok("role-msg", error, `Done. ${f.email.value.trim()} is now ${f.role.value === "admin" ? "an admin" : "a student"}.`)) { f.reset(); load(); } });

  /* ---------- Shared click actions ---------- */
  document.addEventListener("click", async e => {
    const t = e.target; let error, q;
    if (t.dataset.req) ({ error } = await client.from("requests").update({ status: t.dataset.to }).eq("id", t.dataset.req));
    else if (t.dataset.enstatus) { const [u, c, st] = t.dataset.enstatus.split("|"); ({ error } = await client.from("enrollments").update({ status: st }).eq("user_id", u).eq("course_id", c)); }
    else if (t.dataset.unenrol) { if (!confirm("Remove this enrolment? The student loses access to the course materials.")) return; const [u, c] = t.dataset.unenrol.split("|"); ({ error } = await client.from("enrollments").delete().eq("user_id", u).eq("course_id", c)); }
    else if ((q = t.dataset.delmat || t.dataset.delev || t.dataset.delnews)) { if (!confirm("Delete this? This can't be undone.")) return;
      const table = t.dataset.delmat ? "materials" : t.dataset.delev ? "events" : "announcements"; ({ error } = await client.from(table).delete().eq("id", q)); }
    else return;
    if (error) return notice(msg, "error", errText(error));
    load();
  });


  /* ---------- Applications and counselling requests ---------- */
  const APP = { new: ["New", "wait"], contacted: ["Contacted", ""], enrolled: ["Enrolled", "good"], closed: ["Closed", ""] };
  function applications() {
    const k = $("app-kind").value, st = $("app-status").value;
    const rows = apps.filter(a => (k === "all" || a.kind === k) && (st === "all" || a.status === st));
    const tel = p => String(p || "").replace(/[^0-9+]/g, "");
    $("app-list").innerHTML = rows.length ? rows.map(a => `<div class="item"><div class="item-h"><b>${esc([a.first_name, a.last_name].filter(Boolean).join(" "))} · ${({ counselling: "Counselling call", mentor: "Mentor application", career: "Careers application", contact: "Contact form", referral: "Referral", hire: "Hiring enquiry" })[a.kind] || "Application"}</b><span class="chip ${APP[a.status][1]}">${APP[a.status][0]}</span></div>
      <div class="meta">${esc(cname(a.course_id) || "Program not chosen")} · ${date(a.created_at)}${a.preferred_time ? " · Prefers " + esc(a.preferred_time) : ""}${a.source ? " · Source: " + esc(a.source) : ""}</div>
      <p>${[a.experience && "Experience: " + a.experience, a.role && "Role: " + a.role].filter(Boolean).map(esc).join(" · ")}${a.message ? "\n" + esc(a.message) : ""}</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:center">
        <a class="btn btn-primary btn-sm" href="tel:${esc(tel(a.phone))}">Call ${esc(a.phone)}</a>
        <a class="btn btn-line btn-sm" href="https://wa.me/${esc(tel(a.phone).replace(/^\+/, "").replace(/^(\d{10})$/, "91$1"))}" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        ${a.email ? `<a class="btn btn-line btn-sm" href="mailto:${esc(a.email)}">Email</a>` : ""}
        ${a.linkedin ? `<a class="btn btn-line btn-sm" href="${safeUrl(/^https?:/i.test(a.linkedin) ? a.linkedin : "https://" + a.linkedin)}" target="_blank" rel="noopener noreferrer">LinkedIn</a>` : ""}
        <select data-appstatus="${a.id}" style="width:auto;margin-left:auto" aria-label="Status">${Object.entries(APP).map(([v, [t]]) => `<option value="${v}"${a.status === v ? " selected" : ""}>${t}</option>`).join("")}</select></div></div>`).join("") : '<p class="empty">No applications here yet.</p>';
  }
  ["app-kind", "app-status"].forEach(id => $(id).addEventListener("change", applications));
  $("app-list").addEventListener("change", async e => { const id = e.target.dataset.appstatus; if (!id) return;
    const { error } = await client.from("applications").update({ status: e.target.value }).eq("id", id);
    if (error) return notice(msg, "error", errText(error));
    apps.find(x => String(x.id) === id).status = e.target.value; paint(); });

  /* ---------- Job board ---------- */
  function jobsTab() {
    $("job-rows").innerHTML = jobs.length ? jobs.map(j => `<div class="item"><div class="item-h"><b>${esc(j.title)} · ${esc(j.company)}</b><span class="chip ${j.active ? "good" : ""}">${j.active ? "Live" : "Hidden"}</span></div>
      <div class="meta">${esc(j.category)} · ${esc(j.location || "")} · ${esc(j.experience || "")} · posted ${esc(j.posted_on)} · <a href="${safeUrl(j.url)}" target="_blank" rel="noopener noreferrer">Open</a></div>
      <div style="display:flex;gap:12px;margin-top:8px"><button class="link-btn" style="color:var(--brand-ink)" data-jobtoggle="${j.id}" data-on="${j.active ? "0" : "1"}">${j.active ? "Hide" : "Show"}</button><button class="link-btn" data-deljob="${j.id}">Delete</button></div></div>`).join("") : '<p class="empty">No jobs yet. Add openings you find on LinkedIn or company career pages.</p>';
  }
  $("f-job").addEventListener("submit", async e => { e.preventDefault(); const f = e.target;
    const row = { title: f.title.value.trim(), company: f.company.value.trim(), location: f.location.value.trim() || null, category: f.category.value, experience: f.experience.value.trim() || null, job_type: f.job_type.value, url: f.url.value.trim(), logo: f.logo.value.trim() || null };
    const { error } = await client.from("jobs").insert(row);
    if (ok("job-msg", error, "Job added. It's live on the Job board.")) { f.reset(); load(); } });
  document.addEventListener("click", async e => { const t = e.target; let error;
    if (t.dataset.jobtoggle) ({ error } = await client.from("jobs").update({ active: t.dataset.on === "1" }).eq("id", t.dataset.jobtoggle));
    else if (t.dataset.deljob) { if (!confirm("Delete this job?")) return; ({ error } = await client.from("jobs").delete().eq("id", t.dataset.deljob)); }
    else return;
    if (error) return notice(msg, "error", errText(error)); load(); });

  $("refresh").addEventListener("click", load);
  openTab("overview");
  load();
})();
