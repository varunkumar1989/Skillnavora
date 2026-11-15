// Starts a payment: creates a Razorpay order for one item at the price in assets/products.json.
// The browser sends only the item; the amount always comes from the price list here.
//
// Cloudflare secrets (Workers & Pages -> skillnavora -> Settings -> Variables and secrets):
//   RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET   from Razorpay Dashboard -> Account & Settings -> API keys
//                                           (use Test mode keys first; switch to Live keys when ready)
//   SUPABASE_SERVICE_KEY                   Supabase -> Project Settings -> API keys -> secret key. Used only on the
//                                           server to record purchases; never put it in the website's files.
//   PDF_SECRET                             signs the access pass (see pdf-access.js)
import { json, userEmail, entitlements } from "./pdf-access.js";
import { priceOf, classify, allowed } from "../../assets/paywall-core.js";
import catalog from "../../assets/products.json";

export const RZP = "https://api.razorpay.com/v1";
export const SUPABASE_URL = "https://rnncabqtcxxivuyjwoja.supabase.co";
export const basicAuth = env => "Basic " + btoa(env.RAZORPAY_KEY_ID + ":" + env.RAZORPAY_KEY_SECRET);
export const paymentsReady = env => !!(env.RAZORPAY_KEY_ID && env.RAZORPAY_KEY_SECRET && env.SUPABASE_SERVICE_KEY && env.PDF_SECRET);

// Does the buyer already own this item (or something that includes it)?
function alreadyOwns(item, ent) {
  if (ent.admin) return true;
  const owned = new Set(ent.products);
  if (owned.has("all-access") || owned.has(item)) return true;
  if (item.startsWith("file:")) return allowed(classify("/" + item.slice(5), catalog), ent);
  return false;
}

export async function onRequestPost({ request, env }) {
  if (!paymentsReady(env)) return json({ ok: false, error: "payments_not_configured" }, 503);
  const bearer = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const who = bearer ? await userEmail(bearer) : null;
  if (!who) return json({ ok: false, error: "signin_required" }, 401);

  let body; try { body = await request.json(); } catch { return json({ ok: false, error: "bad_request" }, 400); }
  const price = priceOf(body && body.item, catalog);
  if (!price) return json({ ok: false, error: "not_for_sale" }, 400);

  const ent = await entitlements(who.email, bearer);
  if (alreadyOwns(price.item, ent)) return json({ ok: true, owned: true });

  const receipt = ("sn-" + Date.now().toString(36) + "-" + crypto.getRandomValues(new Uint32Array(1))[0].toString(36)).slice(0, 40);
  const r = await fetch(RZP + "/orders", {
    method: "POST",
    headers: { authorization: basicAuth(env), "content-type": "application/json" },
    body: JSON.stringify({ amount: price.inr * 100, currency: "INR", receipt, notes: { item: price.item, email: who.email, user_id: who.id || "" } }),
  });
  if (!r.ok) return json({ ok: false, error: "order_failed" }, 502);
  const order = await r.json();
  return json({ ok: true, key: env.RAZORPAY_KEY_ID, order_id: order.id, amount: order.amount, currency: order.currency,
                name: price.name, email: who.email });
}

// Records a paid purchase (server only, with the secret key). Safe to call twice for the same payment.
export async function recordPurchase(env, row) {
  const key = env.SUPABASE_SERVICE_KEY;
  const headers = { apikey: key, "content-type": "application/json", prefer: "resolution=merge-duplicates,return=minimal" };
  if (key.includes(".")) headers.authorization = "Bearer " + key; // older JWT-style service keys also need this header
  const r = await fetch(SUPABASE_URL + "/rest/v1/purchases?on_conflict=razorpay_payment_id", { method: "POST", headers, body: JSON.stringify(row) });
  return r.ok;
}

// Hex HMAC-SHA256, used for Razorpay's payment and webhook signatures.
export async function hmacHex(secret, text) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(text));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
}

// Compares two strings in constant time.
export function sameText(a, b) {
  a = String(a || ""); b = String(b || "");
  if (a.length !== b.length || !a.length) return false;
  let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}
