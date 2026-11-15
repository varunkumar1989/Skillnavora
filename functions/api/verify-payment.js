// Finishes a payment after Razorpay Checkout succeeds in the browser.
// 1. Checks Razorpay's signature (proves the payment details were not made up in the browser).
// 2. Reads the order and payment back from Razorpay and checks they belong to this signed-in buyer and are paid.
// 3. Records the purchase and gives the buyer a fresh access pass, so the file opens straight away.
import { json, userEmail, issuePass, withCookies } from "./pdf-access.js";
import { RZP, basicAuth, paymentsReady, recordPurchase, hmacHex, sameText } from "./checkout.js";
import { priceOf } from "../../assets/paywall-core.js";
import catalog from "../../assets/products.json";

export async function onRequestPost({ request, env }) {
  if (!paymentsReady(env)) return json({ ok: false, error: "payments_not_configured" }, 503);
  const bearer = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const who = bearer ? await userEmail(bearer) : null;
  if (!who) return json({ ok: false, error: "signin_required" }, 401);

  let b; try { b = await request.json(); } catch { return json({ ok: false, error: "bad_request" }, 400); }
  const orderId = String(b.razorpay_order_id || ""), paymentId = String(b.razorpay_payment_id || "");
  if (!/^order_\w{6,40}$/.test(orderId) || !/^pay_\w{6,40}$/.test(paymentId)) return json({ ok: false, error: "bad_request" }, 400);

  const expected = await hmacHex(env.RAZORPAY_KEY_SECRET, orderId + "|" + paymentId);
  if (!sameText(expected, b.razorpay_signature)) return json({ ok: false, error: "bad_signature" }, 400);

  const auth = { authorization: basicAuth(env) };
  const [or, pr] = await Promise.all([fetch(RZP + "/orders/" + orderId, { headers: auth }), fetch(RZP + "/payments/" + paymentId, { headers: auth })]);
  if (!or.ok || !pr.ok) return json({ ok: false, error: "lookup_failed" }, 502);
  const order = await or.json();
  let payment = await pr.json();
  const notes = order.notes || {};
  if (String(notes.email || "").toLowerCase() !== who.email) return json({ ok: false, error: "not_your_order" }, 403);
  if (payment.order_id !== orderId) return json({ ok: false, error: "mismatch" }, 400);
  if (!priceOf(notes.item, catalog)) return json({ ok: false, error: "not_for_sale" }, 400);

  // Razorpay captures automatically when the account is set to auto-capture; capture here if it is still only authorised.
  if (payment.status === "authorized") {
    const cr = await fetch(RZP + "/payments/" + paymentId + "/capture", { method: "POST", headers: { ...auth, "content-type": "application/json" },
      body: JSON.stringify({ amount: payment.amount, currency: payment.currency }) });
    if (cr.ok) payment = await cr.json();
  }
  if (payment.status !== "captured") return json({ ok: false, error: "not_paid", status: payment.status }, 402);

  const saved = await recordPurchase(env, {
    email: who.email, user_id: who.id || null, product_id: notes.item, amount_paise: payment.amount, currency: payment.currency,
    razorpay_order_id: orderId, razorpay_payment_id: paymentId, status: "paid" });
  if (!saved) return json({ ok: false, error: "record_failed", payment_id: paymentId }, 500);

  const { ent, cookies } = await issuePass(who.email, bearer, env);
  return withCookies({ ok: true, item: notes.item, products: ent.products }, 200, cookies);
}
