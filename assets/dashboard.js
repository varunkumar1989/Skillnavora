/* Student dashboard: progress, assignments, requests, announcements, profile. */
(async function () {
  const { client, $, esc, safeUrl, date, notice, setupMessage, errText } = SN;
  const app = $("app"), msg = $("app-msg");
  if (!client) { setupMessage(msg); return; }
  const s = await SN.session();
  if (!s) return location.replace("login.html?next=dashboard");
  const uid = s.user.id;

  const WEEKS = ["Set up your AI toolkit and personal AI policy", "Claude projects and an interview-synthesis artifact",
    "Gmail and Calendar morning brief, Slack weekly update", "Landing page in Claude Code, deployed from GitHub",
    "Three-screen Figma prototype tested with two users", "Lovable MVP with database and login",
    "Notion product hub and a PRD with tickets", "Zapier and Make automations", "n8n AI email triage and an MCP tool",
    "Telegram and WhatsApp bot with human handoff", "Voice receptionist with a booking tool",
    "Capstone: AI front desk, case study and demo"];
  const STATUS = { submitted: ["Awaiting review", "wait"], reviewed: ["Reviewed", "good"], needs_changes: ["Needs changes", "warn"], open: ["Open", "wait"], done: ["Done", "good"] };
  const chip = st => { const [t, c] = STATUS[st] || [st, ""]; return `<span class="chip ${c}">${esc(t)}</span>`; };

  $("signout").addEventListener("click", SN.signOut);
  const me = await SN.profile(uid) || {};
  $("hello").textContent = "Welcome" + (me.full_name ? ", " + me.full_name.split(" ")[0] : "") + "!";
  if (me.role === "admin") $("to-admin").hidden = false;
  app.hidden = false;

  // Profile
  const pf = $("f-profile");
  ["full_name", "phone", "linkedin", "goal"].forEach(k => pf[k].value = me[k] || "");
  pf.email.value = s.user.email;
  pf.addEventListener("submit", async e => {
    e.preventDefault();
    const upd = { full_name: pf.full_name.value.trim(), phone: pf.phone.value.trim(), linkedin: pf.linkedin.value.trim(), goal: pf.goal.value.trim() };
    const { error } = await client.from("profiles").update(upd).eq("id", uid);
    notice($("profile-msg"), error ? "error" : "ok", error ? errText(error) : "Profile saved.");
    if (!error && upd.full_name) $("hello").textContent = "Welcome, " + upd.full_name.split(" ")[0] + "!";
  });

  // Progress
  let done = new Set();
  async function loadProgress() {
    const { data } = await client.from("progress").select("week,done").eq("user_id", uid);
    done = new Set((data || []).filter(r => r.done).map(r => r.week));
    $("weeks").innerHTML = WEEKS.map((t, i) => `<label class="wkc${done.has(i + 1) ? " on" : ""}"><input type="checkbox" data-week="${i + 1}"${done.has(i + 1) ? " checked" : ""}><span><small>Week ${i + 1}</small>${esc(t)}</span></label>`).join("");
    paintProgress();
  }
  function paintProgress() {
    const n = done.size, pct = Math.round(n / 12 * 100);
    $("p-count").textContent = n + " / 12"; $("p-bar").style.width = pct + "%"; $("p-pct").textContent = pct + "% complete";
    $("p-bar").parentElement.setAttribute("aria-valuenow", pct);
  }
  $("weeks").addEventListener("change", async e => {
    const cb = e.target; if (!cb.dataset.week) return;
    const week = +cb.dataset.week, on = cb.checked;
    cb.closest(".wkc").classList.toggle("on", on);
    on ? done.add(week) : done.delete(week); paintProgress();
    const { error } = await client.from("progress").upsert({ user_id: uid, week, done: on, updated_at: new Date().toISOString() });
    if (error) { notice(msg, "error", "Couldn't save your progress: " + errText(error)); cb.checked = !on; on ? done.delete(week) : done.add(week); paintProgress(); }
  });

  // Submissions
  const sf = $("f-submit");
  sf.week.innerHTML = '<option value="">Other</option>' + WEEKS.map((t, i) => `<option value="${i + 1}">Week ${i + 1}: ${esc(t)}</option>`).join("");
  async function loadSubs() {
    const { data, error } = await client.from("submissions").select("*").eq("user_id", uid).order("created_at", { ascending: false });
    if (error) return notice(msg, "error", errText(error));
    $("s-count").textContent = data.length;
    $("s-wait").textContent = data.filter(r => r.status === "submitted").length + " awaiting review";
    $("subs").innerHTML = data.length ? data.map(r => `<div class="item">
      <div class="item-h"><b>${esc(r.title)}</b>${chip(r.status)}</div>
      <div class="meta">${r.week ? "Week " + r.week + " · " : ""}${date(r.created_at)} · <a href="${safeUrl(r.link)}" target="_blank" rel="noopener noreferrer">Open link</a></div>
      ${r.notes ? `<p>${esc(r.notes)}</p>` : ""}
      ${r.feedback ? `<div class="fb"><small>Feedback${r.reviewed_at ? " · " + date(r.reviewed_at) : ""}</small>${esc(r.feedback)}</div>` : ""}
      ${r.status === "submitted" ? `<button class="link-btn" data-del="${r.id}">Withdraw</button>` : ""}
    </div>`).join("") : '<p class="empty">No submissions yet. Finish a week\'s assignment and share the link above.</p>';
  }
  sf.addEventListener("submit", async e => {
    e.preventDefault();
    const row = { week: sf.week.value ? +sf.week.value : null, title: sf.title.value.trim(), link: sf.link.value.trim(), notes: sf.notes.value.trim() || null };
    if (!/^https?:\/\//i.test(row.link)) return notice($("submit-msg"), "error", "Please paste a full link starting with https://");
    const { error } = await client.from("submissions").insert(row);
    notice($("submit-msg"), error ? "error" : "ok", error ? errText(error) : "Submitted! You'll see feedback here once it's reviewed.");
    if (!error) { sf.reset(); loadSubs(); }
  });
  $("subs").addEventListener("click", async e => {
    const id = e.target.dataset.del; if (!id || !confirm("Withdraw this submission?")) return;
    const { error } = await client.from("submissions").delete().eq("id", id);
    if (error) notice(msg, "error", errText(error)); else loadSubs();
  });

  // Requests
  const rf = $("f-request");
  async function loadReqs() {
    const { data } = await client.from("requests").select("*").eq("user_id", uid).order("created_at", { ascending: false });
    const rows = data || [];
    $("r-open").textContent = rows.filter(r => r.status === "open").length;
    $("reqs").innerHTML = rows.length ? rows.map(r => `<div class="item"><div class="item-h"><b>${esc(r.topic)}</b>${chip(r.status)}</div><div class="meta">${date(r.created_at)}</div><p>${esc(r.message)}</p></div>`).join("") : '<p class="empty">No requests yet.</p>';
  }
  rf.addEventListener("submit", async e => {
    e.preventDefault();
    const { error } = await client.from("requests").insert({ topic: rf.topic.value, message: rf.message.value.trim() });
    notice($("request-msg"), error ? "error" : "ok", error ? errText(error) : "Request sent. We'll get back to you soon.");
    if (!error) { rf.reset(); loadReqs(); }
  });

  // Announcements
  async function loadNews() {
    const { data } = await client.from("announcements").select("*").order("created_at", { ascending: false }).limit(5);
    $("news").innerHTML = (data || []).length ? data.map(a => `<div class="item"><div class="item-h"><b>${esc(a.title)}</b><span class="meta">${date(a.created_at)}</span></div><p>${esc(a.body)}</p></div>`).join("") : '<p class="empty">No announcements yet.</p>';
  }

  await Promise.all([loadProgress(), loadSubs(), loadReqs(), loadNews()]);
})();
