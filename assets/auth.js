/* Shared login helpers for login, dashboard and admin pages.
   Needs assets/config.js (AUTH) and the Supabase library loaded first. */
const SN = (function () {
  const cfg = typeof AUTH !== "undefined" ? AUTH : {};
  const $ = id => document.getElementById(id);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = u => /^https?:\/\//i.test(String(u || "")) ? esc(u) : "#";
  const date = d => d ? new Date(d).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : "";

  // Refuse secret keys: they bypass every database rule and must never be in a web page.
  const isSecret = k => /^sb_secret_/.test(k) || (() => {
    try { return JSON.parse(atob(k.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))).role === "service_role"; } catch { return false; }
  })();

  let client = null, problem = "";
  if (!cfg.supabaseUrl || !cfg.supabaseKey) problem = "setup";
  else if (isSecret(cfg.supabaseKey)) problem = "secret";
  else if (!window.supabase) problem = "library";
  else client = window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseKey, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: "implicit" }
  });

  // Any signed-in admin (login, LMS, dashboard or admin page) gets full access: the visitor details form and the
  // GitHub request form are skipped for them on every page of the site.
  if (client) client.auth.getSession().then(async ({ data }) => {
    try {
      if (!data || !data.session) return;
      const { data: adm } = await client.rpc("is_admin");
      if (adm) localStorage.setItem("sn_admin", JSON.stringify({ t: Date.now(), email: data.session.user.email || "" }));
      else localStorage.removeItem("sn_admin");
    } catch {}
  });

  function notice(el, kind, text) {
    if (!el) return;
    el.className = "notice " + kind; el.textContent = text; el.hidden = !text;
  }

  function setupMessage(el) {
    const msgs = {
      setup: "Student and admin logins are coming soon. Please check back shortly, or contact us on WhatsApp.",
      secret: "Login is switched off: the key in assets/config.js is a secret key. Replace it with the publishable (anon) key.",
      library: "Couldn't load the login service. Check your internet connection and refresh the page."
    };
    notice(el, problem === "setup" ? "info" : "error", msgs[problem] || "");
  }

  async function session() {
    if (!client) return null;
    const { data } = await client.auth.getSession();
    return data.session;
  }

  async function profile(uid) {
    const { data } = await client.from("profiles").select("*").eq("id", uid).single();
    return data;
  }

  async function signOut() {
    try { localStorage.removeItem("sn_admin"); } catch {}
    if (client) await client.auth.signOut();
    location.href = "login.html";
  }

  // Friendlier wording for common Supabase errors.
  function errText(e) {
    const m = (e && e.message) || String(e);
    if (/Invalid login credentials/i.test(m)) return "Wrong email or password.";
    if (/Email not confirmed/i.test(m)) return "Please confirm your email first: check your inbox for the link we sent.";
    if (/already registered/i.test(m)) return "An account with this email already exists. Sign in instead.";
    if (/Password should be/i.test(m)) return "Please use a password of at least 8 characters.";
    if (/rate limit/i.test(m)) return "Too many attempts. Please wait a minute and try again.";
    return m;
  }

  return { client, problem, $, esc, safeUrl, date, notice, setupMessage, session, profile, signOut, errText };
})();
