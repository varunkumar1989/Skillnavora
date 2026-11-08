// PDF and handbook access: a signed-in visitor whose email the owner approved (table pdf_access, approved in the
// admin panel) gets a 24-hour signed cookie. functions/_middleware.js checks that cookie before serving any PDF or file.
//
// Cloudflare settings (Workers & Pages -> skillnavora -> Settings -> Variables and secrets):
//   PDF_SECRET  (secret)  long random text used to sign the cookie. Required when PDF_GATE is on.
//   PDF_GATE    (text)    "on" to enforce the check. Leave unset while setting up; nothing is blocked until then.
const SUPABASE_URL = "https://rnncabqtcxxivuyjwoja.supabase.co";
const SUPABASE_KEY = "sb_publishable_9sKPYxU3MHQfNT43n3d95A_bVLZi7BP"; // publishable key, safe to include
const COOKIE = "sn_pdf", DAY = 24 * 60 * 60;

const json = (o, status = 200, extra = {}) => new Response(JSON.stringify(o), { status, headers: { "content-type": "application/json", "cache-control": "no-store", ...extra } });
const b64u = bytes => btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const fromB64u = s => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/")), c => c.charCodeAt(0));
const enc = new TextEncoder();

async function hmacKey(secret) {
  return crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

// Creates a cookie value that names the approved email and expires in 24 hours.
export async function signToken(email, secret, now = Date.now()) {
  const body = b64u(enc.encode(JSON.stringify({ e: email, x: Math.floor(now / 1000) + DAY })));
  const sig = await crypto.subtle.sign("HMAC", await hmacKey(secret), enc.encode(body));
  return body + "." + b64u(sig);
}

// Returns the approved email if the cookie is genuine and not expired, otherwise null.
export async function checkToken(token, secret, now = Date.now()) {
  try {
    const [body, sig] = String(token || "").split(".");
    if (!body || !sig) return null;
    const ok = await crypto.subtle.verify("HMAC", await hmacKey(secret), fromB64u(sig), enc.encode(body));
    if (!ok) return null;
    const p = JSON.parse(new TextDecoder().decode(fromB64u(body)));
    return p.x > Math.floor(now / 1000) && p.e ? p.e : null;
  } catch { return null; }
}

export function cookieFrom(request) {
  const m = (request.headers.get("cookie") || "").match(new RegExp("(?:^|;\\s*)" + COOKIE + "=([^;]+)"));
  return m ? m[1] : "";
}

// The signed-in visitor's email, checked with Supabase (their own sign-in token).
async function userEmail(bearer, fetchImpl = fetch) {
  const r = await fetchImpl(SUPABASE_URL + "/auth/v1/user", { headers: { apikey: SUPABASE_KEY, authorization: "Bearer " + bearer } });
  if (!r.ok) return null;
  const u = await r.json();
  return u && u.email ? String(u.email).toLowerCase() : null;
}

// Approved only if the owner has added this email to pdf_access. The visitor's own token is used, so row security applies.
async function isApproved(email, bearer, fetchImpl = fetch) {
  const r = await fetchImpl(SUPABASE_URL + "/rest/v1/pdf_access?select=email&email=eq." + encodeURIComponent(email), {
    headers: { apikey: SUPABASE_KEY, authorization: "Bearer " + bearer, accept: "application/json" } });
  if (!r.ok) return false;
  const rows = await r.json();
  return Array.isArray(rows) && rows.length > 0;
}

export async function onRequestGet({ request, env }) {
  const enforced = env.PDF_GATE === "on";
  const secret = env.PDF_SECRET || "";
  const email = secret ? await checkToken(cookieFrom(request), secret) : null;
  return json({ enforced, approved: !!email });
}

export async function onRequestPost({ request, env }) {
  const secret = env.PDF_SECRET || "";
  if (!secret) return json({ ok: false, error: "not_configured" }, 503);
  const bearer = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  if (!bearer) return json({ ok: false, error: "signin_required" }, 401);
  const email = await userEmail(bearer);
  if (!email) return json({ ok: false, error: "signin_required" }, 401);
  if (!(await isApproved(email, bearer))) return json({ ok: false, error: "not_approved", approved: false }, 403);
  const token = await signToken(email, secret);
  return json({ ok: true, approved: true }, 200, {
    "set-cookie": `${COOKIE}=${token}; Path=/; Max-Age=${DAY}; HttpOnly; Secure; SameSite=Lax` });
}
