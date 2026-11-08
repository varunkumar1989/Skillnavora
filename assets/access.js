/* Handbook and PDF access: sign in, request access, then check whether the owner has approved the email.
   Approval is checked by /api/pdf-access. Requests are saved as "Resource access" leads for the owner (Admin -> Applications). */
(function () {
  const $ = id => document.getElementById(id);
  const msg = $("acc-msg");
  const say = (t, bad) => { msg.className = "notice" + (bad ? " error" : ""); msg.textContent = t; };
  // Only same-site paths can be opened after approval (no outside links).
  const raw = new URLSearchParams(location.search).get("next") || "";
  const next = /^\/[^/\\]/.test(raw) && !/^\/\//.test(raw) ? raw : "/handbooks/index.html";
  const root = document.body.dataset.root || "";

  const SN = window.SN;
  if (!SN || !SN.client) { say("Sign-in is unavailable right now. Please try again later.", true); return; }

  (async () => {
    const s = await SN.session();
    if (!s) {
      const a = $("acc-signin");
      a.href = root + "login.html?next=" + encodeURIComponent("access.html?next=" + encodeURIComponent(next));
      a.hidden = false;
      say("Sign in first. Then you can request access.");
      return;
    }
    $("acc-who").textContent = "Signed in as " + s.user.email;
    $("acc-req").hidden = false; $("acc-check").hidden = false;
    $("acc-req").elements.name.value = (s.user.user_metadata && s.user.user_metadata.full_name) || "";

    // Approved already? Then the server sets the access cookie and we continue to the file.
    const check = async () => {
      const r = await fetch(root + "api/pdf-access", { method: "POST", headers: { authorization: "Bearer " + s.access_token } });
      if (r.ok) { say("Access approved. Opening your file…"); location.href = next; return; }
      if (r.status === 403) say("Your request is not approved yet. You will get the files by email, or within 24 hours once approved.", false);
      else if (r.status === 401) say("Please sign in again.", true);
      else say("We could not check your access right now. Please try again.", true);
    };
    $("acc-check").addEventListener("click", check);
    await check();

    $("acc-req").addEventListener("submit", async e => {
      e.preventDefault();
      const f = e.target, v = n => f.elements[n].value.trim();
      if (!v("name")) return say("Please enter your name.", true);
      if (v("phone").replace(/\D/g, "").length < 7) return say("Please enter a valid phone number.", true);
      if (v("reason").length < 5) return say("Please tell us briefly why you need the files.", true);
      const b = f.querySelector("button[type=submit]"); b.disabled = true;
      const row = { kind: "resource", first_name: v("name"), email: s.user.email, phone: v("phone"),
        message: ("[PDF access request] " + v("reason") + " | Page: " + next).slice(0, 1900), source: "access-request" };
      try {
        const r = await fetch(root + "api/lead", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(row) });
        const j = await r.json();
        if (!j.ok) throw new Error("not saved");
        say("Request sent. You will get the files by email, or within 24 hours once the owner approves.");
        f.hidden = true;
      } catch { say("We could not send your request. Please try again, or message us on WhatsApp.", true); }
      b.disabled = false;
    });
  })();
})();
