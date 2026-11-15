// Razorpay webhook: records a purchase even if the buyer closes the tab before the browser confirms it,
// and marks refunds. Set it up in Razorpay Dashboard -> Account & Settings -> Webhooks:
//   URL     https://www.skillnavora.in/api/razorpay-webhook
//   Secret  any long random text; save the same text in Cloudflare as RAZORPAY_WEBHOOK_SECRET
//   Events  order.paid, refund.processed
import { json } from "./pdf-access.js";
import { recordPurchase, hmacHex, sameText, SUPABASE_URL } from "./checkout.js";
import { priceOf } from "../../assets/paywall-core.js";
import catalog from "../../assets/products.json";

async function markRefunded(env, paymentId) {
  const key = env.SUPABASE_SERVICE_KEY;
  const headers = { apikey: key, "content-type": "application/json", prefer: "return=minimal" };
  if (key.includes(".")) headers.authorization = "Bearer " + key;
  const r = await fetch(SUPABASE_URL + "/rest/v1/purchases?razorpay_payment_id=eq." + encodeURIComponent(paymentId),
    { method: "PATCH", headers, body: JSON.stringify({ status: "refunded" }) });
  return r.ok;
}

export async function onRequestPost({ request, env }) {
  if (!env.RAZORPAY_WEBHOOK_SECRET || !env.SUPABASE_SERVICE_KEY) return json({ ok: false, error: "not_configured" }, 503);
  const raw = await request.text();
  const expected = await hmacHex(env.RAZORPAY_WEBHOOK_SECRET, raw);
  if (!sameText(expected, request.headers.get("x-razorpay-signature"))) return json({ ok: false, error: "bad_signature" }, 400);

  let ev; try { ev = JSON.parse(raw); } catch { return json({ ok: false, error: "bad_request" }, 400); }
  const p = ev.payload || {};
  if (ev.event === "order.paid") {
    const order = (p.order || {}).entity || {}, pay = (p.payment || {}).entity || {};
    const notes = order.notes || {};
    if (!priceOf(notes.item, catalog) || !notes.email || !pay.id) return json({ ok: true, ignored: true });
    const saved = await recordPurchase(env, {
      email: String(notes.email).toLowerCase(), user_id: notes.user_id || null, product_id: notes.item, amount_paise: pay.amount,
      currency: pay.currency || "INR", razorpay_order_id: order.id || pay.order_id, razorpay_payment_id: pay.id, status: "paid" });
    return saved ? json({ ok: true }) : json({ ok: false, error: "record_failed" }, 500);
  }
  if (ev.event === "refund.processed") {
    const refund = (p.refund || {}).entity || {};
    if (refund.payment_id) return (await markRefunded(env, refund.payment_id)) ? json({ ok: true }) : json({ ok: false }, 500);
  }
  return json({ ok: true, ignored: true });
}
