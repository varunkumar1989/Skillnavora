// Access to locked files: a signed 24-hour pass (cookie) that lists what the signed-in visitor may open.
// functions/_middleware.js checks the pass before serving any locked file or interactive handbook.
//
// Two modes, chosen in Cloudflare (Workers & Pages -> skillnavora -> Settings -> Variables and secrets):
//   PAYWALL  (text)   "on": every PDF, workbook, dataset and interactive handbook needs a purchase (or admin).
//                     The price list is assets/products.json.
//   PDF_GATE (text)   "on" (older mode, used only when PAYWALL is off): any email the owner approved gets every file.
//   PDF_SECRET (secret) long random text that signs the pass. Required in both modes. Without it nobody gets files.
//
// Who gets what: admins get everything. Emails the owner approved in the admin panel (table pdf_access) get the
// all-access pass free. Everyone else gets what they bought (table purchases, written only by the payment functions).
const SUPABASE_URL = "https://rnncabqtcxxivuyjwoja.supabase.co";
const SUPABASE_KEY = "sb_publishable_9sKPYxU3MHQfNT43n3d95A_bVLZi7BP"; // publishable key, safe to include
const COOKIE = "sn_pdf", PASS = "sn_pay", DAY = 24 * 60 * 60;

export const json = (o, status = 200, extra = {}) => new Response(JSON.stringify(o), { status, headers: { "content-type": "application/json", "cache-control": "no-store", ...extra } });
const b64u = bytes => btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const fromB64u = s => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/")), c => c.charCodeAt(0));
const enc = new TextEncoder();

async function hmacKey(secret) {
  return crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

// Signs any small object with an expiry. checkSigned returns the object, or null if forged or expired.
export async function signSigned(obj, secret, now = Date.now(), ttl = DAY) {
  const body = b64u(enc.encode(JSON.stringify({ ...obj, x: Math.floor(now / 1000) + ttl })));
  const sig = await crypto.subtle.sign("HMAC", await hmacKey(secret), enc.encode(body));
  return body + "." + b64u(sig);
}
export async function checkSigned(token, secret, now = Date.now()) {
  try {
    const [body, sig] = String(token || "").split(".");
    if (!body || !sig || !secret) return null;
    const ok = await crypto.subtle.verify("HMAC", await hmacKey(secret), fromB64u(sig), enc.encode(body));
    if (!ok) return null;
    const p = JSON.parse(new TextDecoder().decode(fromB64u(body)));
    return p.x > Math.floor(now / 1000) ? p : null;
  } catch { return null; }
}

// Older approval cookie (PDF_GATE mode): names the approved email.
export async function signToken(email, secret, now = Date.now()) { return signSigned({ e: email }, secret, now); }
export async function checkToken(token, secret, now = Date.now()) { const p = await checkSigned(token, secret, now); return p && p.e ? p.e : null; }

export function cookieFrom(request, name = COOKIE) {
  const m = (request.headers.get("cookie") || "").match(new RegExp("(?:^|;\\s*)" + name + "=([^;]+)"));
  return m ? m[1] : "";
}

// The pass in the request: { e: email, a: admin, p: [items] } or null.
export async function passFrom(request, env) {
  return env.PDF_SECRET ? checkSigned(cookieFrom(request, PASS), env.PDF_SECRET) : null;
}

// The signed-in visitor's email, checked with Supabase using their own sign-in token.
export async function userEmail(bearer, fetchImpl = fetch) {
  const r = await fetchImpl(SUPABASE_URL + "/auth/v1/user", { headers: { apikey: SUPABASE_KEY, authorization: "Bearer " + bearer } });
  if (!r.ok) return null;
  const u = await r.json();
  return u && u.email ? { email: String(u.email).toLowerCase(), id: u.id || null } : null;
}

const asUser = bearer => ({ apikey: SUPABASE_KEY, authorization: "Bearer " + bearer, accept: "application/json" });

// What this visitor may open. Every query uses their own token, so the database's row rules apply.
export async function entitlements(email, bearer, fetchImpl = fetch) {
  const [adm, appr, buys] = await Promise.all([
    fetchImpl(SUPABASE_URL + "/rest/v1/rpc/is_admin", { method: "POST", headers: { ...asUser(bearer), "content-type": "application/json" }, body: "{}" }),
    fetchImpl(SUPABASE_URL + "/rest/v1/pdf_access?select=email&email=eq." + encodeURIComponent(email), { headers: asUser(bearer) }),
    fetchImpl(SUPABASE_URL + "/rest/v1/purchases?select=product_id&status=eq.paid", { headers: asUser(bearer) }),
  ]);
  const admin = adm.ok ? (await adm.json()) === true : false;
  const approved = appr.ok ? ((await appr.json()) || []).length > 0 : false;
  const items = buys.ok ? ((await buys.json()) || []).map(r => r.product_id).filter(Boolean) : [];
  if (approved) items.push("all-access");
  return { admin, approved, products: [...new Set(items)].slice(0, 200) };
}

// Sets the pass (and the older approval cookie) after checking who the visitor is.
export async function issuePass(email, bearer, env, fetchImpl = fetch) {
  const ent = await entitlements(email, bearer, fetchImpl);
  const pass = await signSigned({ e: email, a: ent.admin, p: ent.products }, env.PDF_SECRET);
  const cookies = [`${PASS}=${pass}; Path=/; Max-Age=${DAY}; HttpOnly; Secure; SameSite=Lax`];
  if (ent.approved || ent.admin) cookies.push(`${COOKIE}=${await signToken(email, env.PDF_SECRET)}; Path=/; Max-Age=${DAY}; HttpOnly; Secure; SameSite=Lax`);
  return { ent, cookies };
}

export function withCookies(body, status, cookies) {
  const h = new Headers({ "content-type": "application/json", "cache-control": "no-store" });
  for (const c of cookies) h.append("set-cookie", c);
  return new Response(JSON.stringify(body), { status, headers: h });
}

export async function onRequestGet({ request, env }) {
  const pass = await passFrom(request, env);
  return json({ paywall: env.PAYWALL === "on", enforced: env.PAYWALL === "on" || env.PDF_GATE === "on",
                approved: !!(pass && (pass.a || (pass.p || []).length)), admin: !!(pass && pass.a), products: pass ? pass.p || [] : [] });
}

export async function onRequestPost({ request, env }) {
  if (!env.PDF_SECRET) return json({ ok: false, error: "not_configured" }, 503);
  const bearer = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  if (!bearer) return json({ ok: false, error: "signin_required" }, 401);
  const who = await userEmail(bearer);
  if (!who) return json({ ok: false, error: "signin_required" }, 401);
  const { ent, cookies } = await issuePass(who.email, bearer, env);
  // Older approval mode (access.html): a visitor the owner has not approved gets "not approved", as before.
  if (env.PAYWALL !== "on" && !(ent.approved || ent.admin)) return withCookies({ ok: false, error: "not_approved", approved: false }, 403, cookies);
  return withCookies({ ok: true, approved: ent.approved || ent.admin || ent.products.length > 0, admin: ent.admin, products: ent.products }, 200, cookies);
}

// Sign-out: removes the access pass from this browser.
export async function onRequestDelete() {
  return withCookies({ ok: true }, 200, [`${PASS}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`, `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`]);
}
