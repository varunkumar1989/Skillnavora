/* Email verification with a one-time code. SNverify.ensure(email, name) shows a small dialog, emails a 6-digit
   code (Supabase email sign-in), checks it, and resolves with { email, token }. The visitor is then signed in,
   and the server (functions/api/lead.js) marks their details as "Email verified" by checking that sign-in.
   Rejects with { cancelled: true } if the visitor closes the dialog.
   Needs the Supabase email template to include {{ .Token }} (see supabase/README.md). */
(function () {
  const root = () => (document.body && document.body.dataset.root) || "/";
  const load = src => new Promise((ok, bad) => { const s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = () => bad(new Error("load")); document.head.appendChild(s); });
  let client;
  async function getClient() {
    if (client) return client;
    if (typeof AUTH === "undefined" || !AUTH.supabaseUrl) throw new Error("Email check is not available right now.");
    if (!window.supabase) await load(root() + "assets/vendor/supabase-2.117.3.js");
    client = window.supabase.createClient(AUTH.supabaseUrl, AUTH.supabaseKey, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false, flowType: "implicit" } });
    return client;
  }
  const friendly = e => {
    const m = (e && e.message) || String(e || "");
    if (/rate limit|too many|security purposes/i.test(m)) return "Too many codes were sent just now. Please wait a minute and try again.";
    if (/expired|invalid|token/i.test(m)) return "That code is not right or has expired. Check the latest email, or send a new code.";
    if (/email/i.test(m) && /invalid/i.test(m)) return "Please check the email address.";
    return m || "Something went wrong. Please try again.";
  };

  function dialog() {
    const st = document.createElement("style");
    st.textContent = ".snv{position:fixed;inset:0;z-index:10001;background:rgba(15,12,30,.62);display:flex;align-items:center;justify-content:center;padding:16px}"
      + ".snv-b{background:var(--surface,#fff);color:var(--ink,#111);border-radius:18px;max-width:420px;width:100%;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,.3)}"
      + ".snv-b h2{margin:0 0 6px;font-size:21px}.snv-b p{margin:0 0 12px;color:var(--mu,#555);line-height:1.5}"
      + ".snv-b input{width:100%;font:600 22px/1 ui-monospace,Menlo,monospace;letter-spacing:.3em;text-align:center;padding:12px;border:1px solid var(--line,#ccc);border-radius:12px;background:var(--bg,#fff);color:inherit}"
      + ".snv-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.snv-row button{flex:1;min-width:120px}"
      + ".snv-row button{white-space:normal;line-height:1.25}"
      + ".snv-x{background:none;border:0;color:var(--brand-ink,#4C1D95);text-decoration:underline;font-weight:600;cursor:pointer;padding:8px;margin:4px auto 0;display:block}"
      + ".snv-err{min-height:20px;margin-top:8px;color:#B42318;font-size:14px}.snv-ok{color:#166534}";
    document.head.appendChild(st);
    const el = document.createElement("div"); el.className = "snv"; el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); el.setAttribute("aria-labelledby", "snv-h");
    el.innerHTML = `<div class="snv-b"><h2 id="snv-h">Check your email</h2><p id="snv-p"></p>
      <form id="snv-f" novalidate><label for="snv-code" style="display:block;font-weight:600;margin-bottom:6px">6-digit code</label>
      <input id="snv-code" inputmode="numeric" autocomplete="one-time-code" maxlength="10" required>
      <div class="snv-err" id="snv-e" aria-live="polite"></div>
      <div class="snv-row"><button class="btn btn-primary" type="submit">Verify</button><button class="btn btn-line" type="button" id="snv-r">Send a new code</button></div>
      <button class="snv-x" type="button" id="snv-x">Use a different email</button></form></div>`;
    document.body.appendChild(el);
    return el;
  }

  async function ensure(email, name) {
    email = String(email || "").trim().toLowerCase();
    const c = await getClient();
    // Already signed in with this email and it is confirmed: nothing to do.
    const { data: s } = await c.auth.getSession();
    if (s && s.session && s.session.user && (s.session.user.email || "").toLowerCase() === email && s.session.user.email_confirmed_at) {
      return { email, token: s.session.access_token };
    }
    const send = () => c.auth.signInWithOtp({ email, options: { shouldCreateUser: true, data: name ? { full_name: name } : undefined } });
    const first = await send();
    if (first.error) throw new Error(friendly(first.error));
    return new Promise((resolve, reject) => {
      const el = dialog(), err = el.querySelector("#snv-e"), code = el.querySelector("#snv-code"), resend = el.querySelector("#snv-r");
      el.querySelector("#snv-p").textContent = "We sent a code to " + email + ". Enter it to confirm this is your email. Check spam if it does not arrive in a minute.";
      setTimeout(() => code.focus(), 30);
      let wait = 0; const tick = () => { resend.disabled = wait > 0; resend.textContent = wait > 0 ? "New code in " + wait + "s" : "Send a new code"; if (wait > 0) { wait--; setTimeout(tick, 1000); } };
      wait = 60; tick();
      const close = () => el.remove();
      el.querySelector("#snv-x").addEventListener("click", () => { close(); reject({ cancelled: true }); });
      resend.addEventListener("click", async () => { err.className = "snv-err"; err.textContent = ""; const r = await send(); if (r.error) err.textContent = friendly(r.error); else { err.className = "snv-err snv-ok"; err.textContent = "New code sent."; wait = 60; tick(); } });
      el.querySelector("#snv-f").addEventListener("submit", async e => {
        e.preventDefault();
        const token = code.value.replace(/\D/g, "");
        if (token.length < 6) { err.textContent = "Please enter the code from the email."; return; }
        const btn = e.target.querySelector("button[type=submit]"); btn.disabled = true; err.className = "snv-err"; err.textContent = "";
        const { data, error } = await c.auth.verifyOtp({ email, token, type: "email" });
        btn.disabled = false;
        if (error || !data || !data.session) { err.textContent = friendly(error); return; }
        close(); resolve({ email, token: data.session.access_token });
      });
    });
  }
  window.SNverify = { ensure };
})();
