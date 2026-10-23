/* Admin panel. Every action is also checked by the database rules, so this
   page can't do anything a non-admin account isn't allowed to. */
(async function () {
  const { client, $, esc, safeUrl, date, notice, setupMessage, errText } = SN;
  const msg = $("app-msg");
  if (!client) { setupMessage(msg); return; }
  const s = await SN.session();
  if (!s) return location.replace("login.html?next=admin");
  $("signout").addEventListener("click", SN.signOut);
  const { data: isAdmin } = await client.rpc("is_admin");
  if (!isAdmin) { $("denied").hidden = false; return; }
  $("app").hidden = false;

  const STATUS = { submitted: ["Awaiting review", "wait"], reviewed: ["Reviewed", "good"], needs_changes: ["Needs changes", "warn"], open: ["Open", "wait"], done: ["Done", "good"] };
  const chip = st => { const [t, c] = STATUS[st] || [st, ""]; return `<span class="chip ${c}">${esc(t)}</span>`; };

  // Tabs
  const tabs = document.querySelectorAll("[data-tab]");
  const openTab = name => {
    tabs.forEach(t => t.setAttribute("aria-selected", t.dataset.tab === name));
    document.querySelectorAll(".panel").forEach(p => p.hidden = p.id !== "p-" + name);
  };
  tabs.forEach(t => t.addEventListener("click", () => openTab(t.dataset.tab)));

  let people = {}, subs = [], reqs = [], prog = {};
  const who = id => people[id] ? (people[id].full_name || people[id].email) : "Unknown";

  async function loadAll() {
    const [p, sb, rq, pr] = await Promise.all([
      client.from("profiles").select("*").order("created_at", { ascending: false }),
      client.from("submissions").select("*").order("created_at", { ascending: false }),
      client.from("requests").select("*").order("created_at", { ascending: false }),
      client.from("progress").select("user_id,week").eq("done", true)
    ]);
    const err = [p, sb, rq, pr].find(r => r.error);
    if (err) return notice(msg, "error", errText(err.error));
    people = Object.fromEntries(p.data.map(x => [x.id, x]));
    subs = sb.data; reqs = rq.data;
    prog = {}; pr.data.forEach(r => prog[r.user_id] = (prog[r.user_id] || 0) + 1);
    paint();
  }

  function paint() {
    const students = Object.values(people).filter(x => x.role === "student");
    const waiting = subs.filter(x => x.status === "submitted"), open = reqs.filter(x => x.status === "open");
    $("o-students").textContent = students.length;
    $("o-waiting").textContent = waiting.length;
    $("o-open").textContent = open.length;
    $("o-subs").textContent = subs.length;
    $("tab-subs-n").textContent = waiting.length ? " (" + waiting.length + ")" : "";
    $("tab-reqs-n").textContent = open.length ? " (" + open.length + ")" : "";
    paintStudents(); paintSubs(); paintReqs(); paintAdmins();
  }

  function paintStudents() {
    const q = $("search").value.trim().toLowerCase();
    const rows = Object.values(people).filter(x => !q || [x.full_name, x.email, x.phone, x.goal].join(" ").toLowerCase().includes(q));
    $("students").innerHTML = rows.length ? rows.map(x => {
      const n = prog[x.id] || 0, sc = subs.filter(y => y.user_id === x.id).length;
      return `<tr><td><b>${esc(x.full_name || "—")}</b>${x.role === "admin" ? ' <span class="chip good">Admin</span>' : ""}<div class="meta">${esc(x.email)}</div></td>
        <td>${esc(x.phone || "")}${x.linkedin ? `<div><a href="${safeUrl(/^https?:/i.test(x.linkedin) ? x.linkedin : "https://" + x.linkedin)}" target="_blank" rel="noopener noreferrer">LinkedIn</a></div>` : ""}</td>
        <td>${esc(x.goal || "")}</td>
        <td><div class="mini"><span style="width:${Math.round(n / 12 * 100)}%"></span></div><span class="meta">${n}/12 weeks</span></td>
        <td>${sc}</td><td class="meta">${date(x.created_at)}</td></tr>`;
    }).join("") : '<tr><td colspan="6" class="empty">No matching accounts.</td></tr>';
  }
  $("search").addEventListener("input", paintStudents);

  function paintSubs() {
    const filter = $("sub-filter").value;
    const rows = subs.filter(x => filter === "all" || x.status === filter);
    $("subs").innerHTML = rows.length ? rows.map(r => `<div class="item" data-id="${r.id}">
      <div class="item-h"><b>${esc(r.title)}</b>${chip(r.status)}</div>
      <div class="meta">${esc(who(r.user_id))} · ${r.week ? "Week " + r.week + " · " : ""}${date(r.created_at)} · <a href="${safeUrl(r.link)}" target="_blank" rel="noopener noreferrer">Open link</a></div>
      ${r.notes ? `<p>${esc(r.notes)}</p>` : ""}
      <div class="review">
        <label>Feedback<textarea data-f>${esc(r.feedback || "")}</textarea></label>
        <div class="row2"><label>Status<select data-s><option value="reviewed"${r.status === "reviewed" ? " selected" : ""}>Reviewed</option><option value="needs_changes"${r.status === "needs_changes" ? " selected" : ""}>Needs changes</option><option value="submitted"${r.status === "submitted" ? " selected" : ""}>Awaiting review</option></select></label>
        <button class="btn s" data-save>Save review</button></div>
      </div></div>`).join("") : '<p class="empty">Nothing here. 🎉</p>';
  }
  $("sub-filter").addEventListener("change", paintSubs);
  $("subs").addEventListener("click", async e => {
    if (!e.target.matches("[data-save]")) return;
    const box = e.target.closest(".item"), id = box.dataset.id;
    const upd = { feedback: box.querySelector("[data-f]").value.trim() || null, status: box.querySelector("[data-s]").value, reviewed_at: new Date().toISOString() };
    e.target.disabled = true;
    const { error } = await client.from("submissions").update(upd).eq("id", id);
    e.target.disabled = false;
    if (error) return notice(msg, "error", errText(error));
    Object.assign(subs.find(x => String(x.id) === id), upd);
    notice(msg, "ok", "Review saved. The student can see it on their dashboard.");
    paint();
  });

  function paintReqs() {
    const filter = $("req-filter").value;
    const rows = reqs.filter(x => filter === "all" || x.status === filter);
    $("reqs").innerHTML = rows.length ? rows.map(r => {
      const p = people[r.user_id] || {};
      return `<div class="item"><div class="item-h"><b>${esc(r.topic)}</b>${chip(r.status)}</div>
      <div class="meta">${esc(who(r.user_id))} · ${esc(p.email || "")}${p.phone ? " · " + esc(p.phone) : ""} · ${date(r.created_at)}</div><p>${esc(r.message)}</p>
      <button class="btn line" data-req="${r.id}" data-to="${r.status === "open" ? "done" : "open"}">${r.status === "open" ? "Mark as done" : "Reopen"}</button></div>`;
    }).join("") : '<p class="empty">No requests here.</p>';
  }
  $("req-filter").addEventListener("change", paintReqs);
  $("reqs").addEventListener("click", async e => {
    const id = e.target.dataset.req; if (!id) return;
    const { error } = await client.from("requests").update({ status: e.target.dataset.to }).eq("id", id);
    if (error) return notice(msg, "error", errText(error));
    reqs.find(x => String(x.id) === id).status = e.target.dataset.to; paint();
  });

  // Announcements
  async function loadNews() {
    const { data } = await client.from("announcements").select("*").order("created_at", { ascending: false });
    $("news").innerHTML = (data || []).length ? data.map(a => `<div class="item"><div class="item-h"><b>${esc(a.title)}</b><span class="meta">${date(a.created_at)}</span></div><p>${esc(a.body)}</p><button class="link-btn" data-del="${a.id}">Delete</button></div>`).join("") : '<p class="empty">No announcements yet.</p>';
  }
  $("f-news").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target;
    const { error } = await client.from("announcements").insert({ title: f.title.value.trim(), body: f.body.value.trim() });
    notice($("news-msg"), error ? "error" : "ok", error ? errText(error) : "Posted. Students see it on their dashboard.");
    if (!error) { f.reset(); loadNews(); }
  });
  $("news").addEventListener("click", async e => {
    const id = e.target.dataset.del; if (!id || !confirm("Delete this announcement?")) return;
    const { error } = await client.from("announcements").delete().eq("id", id);
    if (error) notice(msg, "error", errText(error)); else loadNews();
  });

  // Admins
  function paintAdmins() {
    $("admins").innerHTML = Object.values(people).filter(x => x.role === "admin").map(x => `<li><b>${esc(x.full_name || x.email)}</b> <span class="meta">${esc(x.email)}</span></li>`).join("");
  }
  $("f-role").addEventListener("submit", async e => {
    e.preventDefault(); const f = e.target;
    const { error } = await client.rpc("set_role", { target_email: f.email.value.trim(), new_role: f.role.value });
    notice($("role-msg"), error ? "error" : "ok", error ? errText(error) : "Done. " + f.email.value.trim() + " is now " + (f.role.value === "admin" ? "an admin." : "a student."));
    if (!error) { f.reset(); loadAll(); }
  });

  $("refresh").addEventListener("click", () => { loadAll(); loadNews(); });
  openTab("overview");
  await Promise.all([loadAll(), loadNews()]);
})();
