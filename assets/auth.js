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

  // Lets the handbook PDFs (/handbook/*) check that the visitor is logged in.
  if (client && client.auth.onAuthStateChange) client.auth.onAuthStateChange((_e, s) => {
    const sec = location.protocol === "https:" ? "; Secure" : "";
    document.cookie = s && s.access_token ? "sn_hb=" + encodeURIComponent(s.access_token) + "; Path=/handbook; Max-Age=" + Math.max(60, (s.expires_at || 0) - Math.floor(Date.now() / 1000)) + "; SameSite=Lax" + sec
                        : "sn_hb=; Path=/handbook; Max-Age=0; SameSite=Lax" + sec;
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
