/* One-time code check for the details forms. The visitor confirms with a code sent to their email OR to their mobile by SMS.
   SNverify.choose({ email, phone, name }) resolves { channel, email|phone, token } once the code is right.
   Rejects with { cancelled: true } if the visitor closes the dialog.
   Email codes need the Supabase email template to include {{ .Token }}. SMS codes need an SMS provider in Supabase
   (Authentication -> Phone). The server (functions/api/lead.js) checks the signed-in user and marks the lead verified. */
(function () {
  const root = () => (document.body && document.body.dataset.root) || "/";
  const load = src => new Promise((ok, bad) => { const s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = () => bad(new Error("load")); document.head.appendChild(s); });
  let client;
  async function getClient() {
    if (client) return client;
    if (typeof AUTH === "undefined" || !AUTH.supabaseUrl) throw new Error("Code check is not available right now.");
    if (!window.supabase) await load(root() + "assets/vendor/supabase-2.117.3.js");
    client = window.supabase.createClient(AUTH.supabaseUrl, AUTH.supabaseKey, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false, flowType: "implicit" } });
    return client;
  }
  const friendly = (e, channel) => {
    const m = (e && e.message) || String(e || "");
    if (/rate limit|too many|security purposes/i.test(m)) return "Too many codes were sent just now. Please wait a minute and try again.";
    if (/expired|invalid|token/i.test(m)) return "That code is not right or has expired. Check the latest message, or send a new code.";
    if (/sms|phone|provider|twilio|unsupported/i.test(m) || channel === "phone" && /send|deliver/i.test(m)) return "Text messages are not available right now. Please use the email code instead.";
    if (/email/i.test(m) && /invalid/i.test(m)) return "Please check the email address.";
    return m || "Something went wrong. Please try again.";
  };

  function css() {
    if (document.getElementById("snv-css")) return;
    const st = document.createElement("style"); st.id = "snv-css";
    st.textContent = ".snv{position:fixed;inset:0;z-index:10001;background:rgba(15,12,30,.62);display:flex;align-items:center;justify-content:center;padding:16px}"
      + ".snv-b{background:var(--surface,#fff);color:var(--ink,#111);border-radius:18px;max-width:420px;width:100%;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,.3)}"
      + ".snv-b h2{margin:0 0 6px;font-size:21px}.snv-b p{margin:0 0 12px;color:var(--mu,#555);line-height:1.5}"
      + ".snv-b input{width:100%;font:600 22px/1 ui-monospace,Menlo,monospace;letter-spacing:.3em;text-align:center;padding:12px;border:1px solid var(--line,#ccc);border-radius:12px;background:var(--bg,#fff);color:inherit}"
      + ".snv-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.snv-row button{flex:1;min-width:120px;white-space:normal;line-height:1.25;overflow-wrap:anywhere}"
      + ".snv-x{background:none;border:0;color:var(--brand-ink,#4C1D95);text-decoration:underline;font-weight:600;cursor:pointer;padding:8px;margin:4px auto 0;display:block}"
      + ".snv-err{min-height:20px;margin-top:8px;color:#B42318;font-size:14px}.snv-ok{color:#166534}";
    document.head.appendChild(st);
  }
  function shell(title) {
    css();
    const el = document.createElement("div"); el.className = "snv"; el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); el.setAttribute("aria-labelledby", "snv-h");
    el.innerHTML = `<div class="snv-b"><h2 id="snv-h">${title}</h2><div id="snv-body"></div></div>`;
    document.body.appendChild(el);
    return el;
  }

  // Asks how to get the code when both an email and a phone are given. Resolves "email" or "phone", or rejects {cancelled}.
  function pick(email, phone) {
    return new Promise((resolve, reject) => {
      const el = shell("How should we send your code?");
      el.querySelector("#snv-body").innerHTML = `<p>Choose where to receive a 6-digit code. It takes less than a minute.</p>
        <div class="snv-row"><button class="btn btn-primary" type="button" id="snv-em"></button><button class="btn btn-line" type="button" id="snv-ph"></button></div>
        <button class="snv-x" type="button" id="snv-x">Cancel</button>`;
      el.querySelector("#snv-em").textContent = "Email me a code";
      el.querySelector("#snv-ph").textContent = "Text me a code";
      el.querySelector("#snv-em").addEventListener("click", () => { el.remove(); resolve("email"); });
      el.querySelector("#snv-ph").addEventListener("click", () => { el.remove(); resolve("phone"); });
      el.querySelector("#snv-x").addEventListener("click", () => { el.remove(); reject({ cancelled: true }); });
    });
  }

  // Shows the code box; resolves { token } once the code is right. send() sends a code; check(token) verifies it.
  function enterCode(where, send, check, channel) {
    return new Promise((resolve, reject) => {
      const el = shell(channel === "phone" ? "Check your phone" : "Check your email");
      el.querySelector("#snv-body").innerHTML = `<p id="snv-p"></p>
        <form id="snv-f" novalidate><label for="snv-code" style="display:block;font-weight:600;margin-bottom:6px">6-digit code</label>
        <input id="snv-code" inputmode="numeric" autocomplete="one-time-code" maxlength="10" required>
        <div class="snv-err" id="snv-e" aria-live="polite"></div>
        <div class="snv-row"><button class="btn btn-primary" type="submit">Verify</button><button class="btn btn-line" type="button" id="snv-r">New code</button></div>
        <button class="snv-x" type="button" id="snv-x">Cancel</button></form>`;
      const err = el.querySelector("#snv-e"), code = el.querySelector("#snv-code"), resend = el.querySelector("#snv-r");
      el.querySelector("#snv-p").textContent = where + " Enter it to confirm. " + (channel === "phone" ? "Texts can take a minute to arrive." : "Check spam if it does not arrive in a minute.");
      setTimeout(() => code.focus(), 30);
      let wait = 0; const tick = () => { resend.disabled = wait > 0; resend.textContent = wait > 0 ? "New code in " + wait + "s" : "New code"; if (wait > 0) { wait--; setTimeout(tick, 1000); } };
      wait = 60; tick();
      el.querySelector("#snv-x").addEventListener("click", () => { el.remove(); reject({ cancelled: true }); });
      resend.addEventListener("click", async () => { err.className = "snv-err"; err.textContent = ""; const r = await send(); if (r.error) err.textContent = friendly(r.error, channel); else { err.className = "snv-err snv-ok"; err.textContent = "New code sent."; wait = 60; tick(); } });
      el.querySelector("#snv-f").addEventListener("submit", async e => {
        e.preventDefault();
        const token = code.value.replace(/\D/g, "");
        if (token.length < 6) { err.textContent = "Please enter the code."; return; }
        const btn = e.target.querySelector("button[type=submit]"); btn.disabled = true; err.className = "snv-err"; err.textContent = "";
        const { data, error } = await check(token);
        btn.disabled = false;
        if (error || !data || !data.session) { err.textContent = friendly(error, channel); return; }
        el.remove(); resolve({ token: data.session.access_token });
      });
    });
  }

  // Email: sign in with a code sent to the address. Resolves { channel: "email", email, token }.
  async function ensure(email, name) {
    email = String(email || "").trim().toLowerCase();
    const c = await getClient();
    const { data: s } = await c.auth.getSession();
    if (s && s.session && s.session.user && (s.session.user.email || "").toLowerCase() === email && s.session.user.email_confirmed_at) {
      return { channel: "email", email, token: s.session.access_token };
    }
    const send = () => c.auth.signInWithOtp({ email, options: { shouldCreateUser: true, data: name ? { full_name: name } : undefined } });
    const first = await send();
    if (first.error) throw new Error(friendly(first.error, "email"));
    const r = await enterCode("We sent a code to " + email + ".", send, token => c.auth.verifyOtp({ email, token, type: "email" }), "email");
    return { channel: "email", email, token: r.token };
  }

  // Phone: sign in with a code sent by SMS. Resolves { channel: "phone", phone, token }.
  async function ensurePhone(phone, name) {
    const e164 = "+" + String(phone || "").replace(/\D/g, "");
    const c = await getClient();
    const { data: s } = await c.auth.getSession();
    const u = s && s.session && s.session.user;
    if (u && u.phone_confirmed_at && ("+" + String(u.phone || "").replace(/\D/g, "")) === e164) return { channel: "phone", phone: e164, token: s.session.access_token };
    const send = () => c.auth.signInWithOtp({ phone: e164, options: { shouldCreateUser: true, channel: "sms", data: name ? { full_name: name } : undefined } });
    const first = await send();
    if (first.error) throw new Error(friendly(first.error, "phone"));
    const r = await enterCode("We texted a code to " + e164 + ".", send, token => c.auth.verifyOtp({ phone: e164, token, type: "sms" }), "phone");
    return { channel: "phone", phone: e164, token: r.token };
  }

  // Both given: the visitor picks. Only one given: that one is used.
  async function choose({ email, phone, name }) {
    const hasEmail = !!String(email || "").trim(), hasPhone = String(phone || "").replace(/\D/g, "").length >= 10;
    if (!hasEmail && !hasPhone) throw new Error("Please add an email or a phone number.");
    const how = hasEmail && hasPhone ? await pick(email, phone) : hasEmail ? "email" : "phone";
    return how === "email" ? ensure(email, name) : ensurePhone(phone, name);
  }
  window.SNverify = { ensure, ensurePhone, choose };
})();
