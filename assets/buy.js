/* Buy page (buy.html): prices from assets/products.json, Razorpay checkout, and opening the file after payment.
   Visitors arrive here from a locked file (buy.html?for=/handbook/...pdf) or from the Handbooks menu.
   The server decides prices and access; this page only shows them and starts the checkout. */
import { classify, allowed, priceOf } from "./paywall-core.js";

const { client, $, esc } = SN;
const msg = $("buy-msg");
const say = (text, kind = "error") => { msg.className = "notice " + kind; msg.textContent = text; msg.hidden = !text; };
const inr = n => "₹" + Number(n).toLocaleString("en-IN");
const params = new URLSearchParams(location.search);
const rawFor = params.get("for") || "";
const target = /^\/[^/\\]/.test(rawFor) && !rawFor.includes("..") ? rawFor : "";
let cat, ent = null;

async function token() {
  if (!client) return null;
  const s = await SN.session();
  return s ? s.access_token : null;
}

// Ask the server for a fresh pass; returns { admin, products } or null if not signed in.
async function refreshPass() {
  const t = await token(); if (!t) return null;
  try {
    const r = await fetch("api/pdf-access", { method: "POST", headers: { authorization: "Bearer " + t } });
    const j = await r.json().catch(() => ({}));
    return r.ok || j.products ? { admin: !!j.admin, products: j.products || [] } : null;
  } catch { return null; }
}

function card(p, highlight) {
  const off = p.discount_pct ? `<span class="buy-off">${p.discount_pct}% off</span>` : "";
  return `<article class="buy-card${highlight ? " is-for" : ""}" id="p-${esc(p.id)}">
    ${highlight ? '<span class="buy-tag">Unlocks your file</span>' : ""}
    <h3>${esc(p.name)}</h3><p>${esc(p.desc)}</p>
    <div class="buy-price"><b>${inr(p.inr)}</b>${p.inr_list > p.inr ? ` <s>${inr(p.inr_list)}</s>` : ""} ${off}</div>
    <div class="buy-usd">About $${p.usd} outside India</div>
    <button class="btn btn-primary" type="button" data-buy="${esc(p.id)}">Buy now</button></article>`;
}

function render() {
  const forInfo = target ? classify(target, cat) : null;
  const forProduct = forInfo && forInfo.kind === "locked" ? forInfo.product : "";
  // Products first by relevance: the one that unlocks the requested file, then the rest in list order.
  const list = [...cat.products].sort((a, b) => (b.id === forProduct) - (a.id === forProduct));
  $("buy-grid").innerHTML = list.map(p => card(p, p.id === forProduct)).join("");

  const box = $("buy-for");
  if (!forInfo) { box.hidden = true; return; }
  const name = decodeURIComponent(target.split("/").pop()).replace(/\.[a-z0-9]+$/i, "").replace(/[-_]+/g, " ");
  if (forInfo.kind === "private") { box.innerHTML = `<h2>This file is not for sale</h2><p>It is for the SkillNavora team only.</p>`; box.hidden = false; return; }
  if (forInfo.kind !== "locked") { box.hidden = true; return; }
  if (ent && allowed(forInfo, ent)) {
    box.innerHTML = `<h2>You have access</h2><p>“${esc(name)}” is included in your purchases.</p><a class="btn btn-primary" href="${esc(target)}">Open it</a>`;
    box.hidden = false; return;
  }
  const prod = cat.products.find(p => p.id === forProduct);
  const single = forInfo.single ? priceOf("file:" + forInfo.path, cat) : null;
  box.innerHTML = `<h2>“${esc(name)}” is a paid file</h2>
    <p>It is part of <b>${esc(prod ? prod.name : "the all-access pass")}</b>. Buy the complete handbook${single ? ", or just this PDF" : ""}.</p>
    <div class="buy-acts">${prod ? `<button class="btn btn-primary" type="button" data-buy="${esc(prod.id)}">${esc(prod.name)}: ${inr(prod.inr)}</button>` : ""}
    ${single ? `<button class="btn btn-line" type="button" data-buy="${esc(single.item)}">Just this PDF: ${inr(single.inr)}</button>` : ""}</div>`;
  box.hidden = false;
}

function loadRazorpay() {
  if (window.Razorpay) return Promise.resolve();
  return new Promise((ok, bad) => {
    const s = document.createElement("script"); s.src = "https://checkout.razorpay.com/v1/checkout.js";
    s.onload = ok; s.onerror = () => bad(new Error("Could not load the payment window. Check your connection and try again."));
    document.head.appendChild(s);
  });
}

function opened() {
  say("Payment received. Your access is ready.", "ok");
  if (target) setTimeout(() => { location.href = target; }, 900); else render();
}

async function buy(item, btn) {
  const t = await token();
  if (!t) { location.href = "login.html?next=" + encodeURIComponent("buy.html" + location.search); return; }
  btn.disabled = true; const label = btn.textContent; btn.textContent = "Opening checkout…"; say("");
  try {
    const r = await fetch("api/checkout", { method: "POST", headers: { authorization: "Bearer " + t, "content-type": "application/json" }, body: JSON.stringify({ item }) });
    const j = await r.json().catch(() => ({}));
    if (j.owned) { ent = await refreshPass(); return opened(); }
    if (!r.ok) {
      const why = { payments_not_configured: "Online payments are not switched on yet. Please contact us on WhatsApp to buy.", signin_required: "Please sign in again, then try once more.",
                    not_for_sale: "This item is not for sale.", order_failed: "The payment service did not respond. Please try again in a minute." }[j.error];
      return say(why || "Something went wrong starting the payment. Please try again.");
    }
    await loadRazorpay();
    const rzp = new window.Razorpay({
      key: j.key, amount: j.amount, currency: j.currency, order_id: j.order_id, name: "SkillNavora", description: j.name,
      prefill: { email: j.email }, theme: { color: "#6C4CF5" },
      handler: async resp => {
        say("Confirming your payment…", "info");
        const v = await fetch("api/verify-payment", { method: "POST", headers: { authorization: "Bearer " + t, "content-type": "application/json" }, body: JSON.stringify(resp) });
        const vj = await v.json().catch(() => ({}));
        if (v.ok) { ent = { admin: false, products: vj.products || [] }; return opened(); }
        say(vj.error === "record_failed"
          ? `Your payment went through but we could not save it. Please send us this payment ID on WhatsApp: ${vj.payment_id}`
          : "We could not confirm the payment. If money was taken, contact us with your payment ID and we will sort it out.");
      },
      modal: { ondismiss: () => say("Payment cancelled. You have not been charged.", "info") },
    });
    rzp.on("payment.failed", e => say("The payment failed: " + ((e && e.error && e.error.description) || "please try another method.")));
    rzp.open();
  } catch (e) { say(e.message || "Something went wrong. Please try again."); }
  finally { btn.disabled = false; btn.textContent = label; }
}

document.addEventListener("click", e => { const b = e.target.closest("[data-buy]"); if (b) buy(b.dataset.buy, b); });
$("buy-refresh").addEventListener("click", async () => {
  const got = await refreshPass();
  if (!got) { location.href = "login.html?next=" + encodeURIComponent("buy.html" + location.search); return; }
  ent = got; render();
  say(got.admin ? "Admin account: every file is open to you." : got.products.length ? "Access refreshed." : "No purchases found for this account yet.", got.products.length || got.admin ? "ok" : "info");
});

(async () => {
  try { cat = await (await fetch("assets/products.json", { cache: "no-store" })).json(); }
  catch { return say("Could not load prices. Please refresh the page."); }
  render();
  const who = await token();
  $("buy-who").textContent = who ? "" : "You will be asked to sign in or create a free account before paying.";
  if (who) { ent = await refreshPass(); render(); }
})();
