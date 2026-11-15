/* Mentor (teacher) dashboard, teach.html. Shows only the courses an admin assigned to this mentor.
   Admins can open it too and see every course. Every action is also checked by the database rules
   (supabase/schema.sql, mentor section), so this page cannot do anything those rules do not allow. */
(async function () {
  const { client, $, esc, safeUrl, date, notice, setupMessage, errText } = SN;
  const msg = $("tch-msg");
  if (!client) { setupMessage(msg); return; }
  const s = await SN.session();
  if (!s) return location.replace("login.html?next=teach.html");
  document.querySelectorAll("[data-signout]").forEach(b => b.addEventListener("click", SN.signOut));
  const uid = s.user.id;
  const { data: isAdmin } = await client.rpc("is_admin");
  const prof = await SN.profile(uid);
  if (!isAdmin && (!prof || prof.role !== "mentor")) { $("tch-denied").hidden = false; return; }
  $("tch-app").hidden = false;

  const cname = id => (COURSES.find(c => c.id === id) || {}).name || id;
  const STATUS = { submitted: ["Awaiting review", "wait"], reviewed: ["Reviewed", "good"], needs_changes: ["Needs changes", "warn"] };
  const chip = st => { const [t, c] = STATUS[st] || [st, ""]; return `<span class="chip ${c}">${esc(t)}</span>`; };
  const KINDS = ["recording", "slides", "reading", "assignment", "link", "preread"];

  let myCourses = [], enr = [], mats = [], subs = [], people = {};

  async function load() {
    // Mentors: the courses assigned to them. Admins: every course.
    if (isAdmin) myCourses = COURSES.map(c => c.id);
    else {
      const { data: ci } = await client.from("course_instructors").select("course_id").eq("user_id", uid);
      myCourses = [...new Set((ci || []).map(r => r.course_id))];
    }
    const q = await Promise.all([
      client.from("profiles").select("id,full_name,email"),
      client.from("enrollments").select("user_id,course_id,status,created_at"),
      client.from("materials").select("*").order("module", { ascending: true }).order("created_at", { ascending: true }),
      client.from("submissions").select("*").order("created_at", { ascending: false })
    ]);
    const bad = q.find(r => r.error); if (bad) notice(msg, "error", errText(bad.error));
    let p; [p, enr, mats, subs] = q.map(r => r.data || []);
    people = Object.fromEntries(p.map(x => [x.id, x]));
    paint();
  }
  const who = id => people[id] ? (people[id].full_name || people[id].email) : "Student";
  const mine = list => list.filter(x => myCourses.includes(x.course_id));

  function paint() {
    const awaiting = mine(subs).filter(x => x.status === "submitted").length;
    $("tch-overview").innerHTML = myCourses.length ? myCourses.map(cid => {
      const students = enr.filter(e => e.course_id === cid && e.status === "active");
      const m = mats.filter(x => x.course_id === cid).length;
      const w = subs.filter(x => x.course_id === cid && x.status === "submitted").length;
      return `<article class="card"><h3 class="h3s">${esc(cname(cid))}</h3>
        <p class="meta">${students.length} enrolled · ${m} materials · <b>${w}</b> assignment${w === 1 ? "" : "s"} awaiting review</p>
        <details><summary>Students (${students.length})</summary><div class="list">${students.length ? students.map(e => `<div class="item"><b>${esc(who(e.user_id))}</b> <span class="meta">${esc((people[e.user_id] || {}).email || "")}</span></div>`).join("") : '<p class="meta">No students yet.</p>'}</div></details></article>`;
    }).join("") : '<div class="card"><p>No courses assigned to you yet. An admin assigns courses from the Admin panel, under Teachers.</p></div>';
    $("tch-awaiting").textContent = awaiting ? `${awaiting} assignment${awaiting === 1 ? "" : "s"} waiting for your review` : "No assignments waiting for review";
    fillCourseSelect();
    renderMaterials();
    renderReview();
  }

  function fillCourseSelect() {
    const opts = myCourses.map(cid => `<option value="${esc(cid)}">${esc(cname(cid))}</option>`).join("");
    document.querySelectorAll("select[data-mycourses]").forEach(sel => { const v = sel.value; sel.innerHTML = opts; if (myCourses.includes(v)) sel.value = v; });
  }

  function renderMaterials() {
    const cid = $("mat-course").value || myCourses[0];
    const list = mats.filter(x => x.course_id === cid);
    $("mat-list").innerHTML = list.length ? list.map(x => `<div class="item"><div class="item-h"><b>Module ${x.module}: ${esc(x.title)}</b><span class="meta">${esc(x.kind)}</span></div>
      <p class="meta"><a href="${safeUrl(x.url)}" target="_blank" rel="noopener">${esc(x.url)}</a></p><button class="link-btn" type="button" data-delmat="${x.id}">Remove</button></div>`).join("")
      : '<p class="meta">No materials for this course yet.</p>';
  }
  $("mat-course").addEventListener("change", renderMaterials);
  $("f-mat").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target;
    const url = f.url.value.trim();
    if (!/^https?:\/\//i.test(url)) return notice($("mat-msg"), "error", "The link must start with https://");
    const { error } = await client.from("materials").insert({ course_id: f.course.value, module: +f.module.value, title: f.title.value.trim(), url, kind: f.kind.value });
    if (error) return notice($("mat-msg"), "error", errText(error));
    notice($("mat-msg"), "ok", "Added. Enrolled students see it straight away.");
    f.title.value = ""; f.url.value = ""; await load();
  });
  document.addEventListener("click", async e => {
    const b = e.target.closest("[data-delmat]"); if (!b) return;
    if (!confirm("Remove this material? Students will no longer see it.")) return;
    const { error } = await client.from("materials").delete().eq("id", b.dataset.delmat);
    if (error) notice($("mat-msg"), "error", errText(error)); else load();
  });

  function renderReview() {
    const filter = $("rev-filter").value;
    const list = mine(subs).filter(x => filter === "all" || x.status === "submitted");
    $("rev-list").innerHTML = list.length ? list.map(x => `<details class="item" ${x.status === "submitted" ? "open" : ""}>
      <summary><b>${esc(who(x.user_id))}</b> · ${esc(cname(x.course_id))} · ${esc(x.title)} ${chip(x.status)}</summary>
      <p><a href="${safeUrl(x.link)}" target="_blank" rel="noopener">Open the submission</a> · <span class="meta">${date(x.created_at)}</span></p>
      ${x.notes ? `<p class="meta">${esc(x.notes)}</p>` : ""}
      <form class="form" data-review="${x.id}"><label>Status<select name="status"><option value="reviewed"${x.status === "reviewed" ? " selected" : ""}>Reviewed (good work)</option><option value="needs_changes"${x.status === "needs_changes" ? " selected" : ""}>Needs changes</option></select></label>
      <label>Feedback for the student<textarea name="feedback" rows="3" maxlength="8000">${esc(x.feedback || "")}</textarea></label>
      <button class="btn btn-primary btn-sm" type="submit">Save review</button></form></details>`).join("")
      : '<p class="meta">Nothing to show here.</p>';
  }
  $("rev-filter").addEventListener("change", renderReview);
  document.addEventListener("submit", async e => {
    const f = e.target.closest("[data-review]"); if (!f) return;
    e.preventDefault();
    const { error } = await client.from("submissions").update({ status: f.status.value, feedback: f.feedback.value.trim() || null, reviewed_at: new Date().toISOString() }).eq("id", f.dataset.review);
    if (error) notice($("rev-msg"), "error", errText(error)); else { notice($("rev-msg"), "ok", "Review saved. The student sees your feedback in their LMS."); load(); }
  });

  // Tabs
  const tabs = document.querySelectorAll("[data-tab]");
  const openTab = n => { tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.tab === n)); document.querySelectorAll(".panel").forEach(p => p.hidden = p.id !== "p-" + n); };
  tabs.forEach(t => t.addEventListener("click", () => openTab(t.dataset.tab)));

  $("refresh") && $("refresh").addEventListener("click", load);
  await load();
})();
