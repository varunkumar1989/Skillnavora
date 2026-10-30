// Fee-Clear Cart — teaching prototype. Fictional data; the "fee service" is simulated locally.
const MENU = [
  { id: "biryani", name: "Veg biryani", price: 260 },
  { id: "raita", name: "Raita", price: 60 },
  { id: "paneer", name: "Paneer wrap", price: 180 },
  { id: "lassi", name: "Sweet lassi", price: 90 },
];
const PLATFORM_FEE = 5;
const TAX_RATE = 0.05; // illustrative, not a statement of any real tax rule

const cart = loadCart();
const $ = (id) => document.getElementById(id);
const inr = (n) => "₹" + Math.round(n).toLocaleString("en-IN");

function loadCart() {
  try { return JSON.parse(localStorage.getItem("feeclear.cart")) || {}; } catch (e) { return {}; }
}
function saveCart() {
  try { localStorage.setItem("feeclear.cart", JSON.stringify(cart)); } catch (e) { /* storage may be blocked */ }
}

// Simulated fee service: resolves after a short delay, or fails on demand.
function fetchDeliveryFee(area) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (area === "fail") reject(new Error("fee service unavailable"));
      else resolve(area === "near" ? 25 : 45);
    }, 300);
  });
}

function renderMenu() {
  $("menu").innerHTML = "";
  MENU.forEach((item) => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${item.name} <strong>${inr(item.price)}</strong></span>`;
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = "Add";
    b.setAttribute("aria-label", `Add ${item.name}`);
    b.addEventListener("click", () => { cart[item.id] = (cart[item.id] || 0) + 1; saveCart(); render(); });
    li.appendChild(b);
    $("menu").appendChild(li);
  });
}

let feeState = { status: "idle", fee: null };

async function refreshFee() {
  feeState = { status: "loading", fee: null };
  renderSummary();
  try {
    const fee = await fetchDeliveryFee($("area").value);
    feeState = { status: "ok", fee };
  } catch (e) {
    feeState = { status: "error", fee: null }; // never invent a number
  }
  renderSummary();
}

function subtotal() {
  return Object.entries(cart).reduce((s, [id, q]) => s + MENU.find((m) => m.id === id).price * q, 0);
}

function renderLines() {
  const ids = Object.keys(cart).filter((id) => cart[id] > 0);
  $("empty").hidden = ids.length > 0;
  $("lines").innerHTML = "";
  ids.forEach((id) => {
    const m = MENU.find((x) => x.id === id);
    const li = document.createElement("li");
    li.innerHTML = `<span>${m.name} × ${cart[id]}</span><span>${inr(m.price * cart[id])}</span>`;
    const rm = document.createElement("button");
    rm.type = "button";
    rm.textContent = "Remove one";
    rm.setAttribute("aria-label", `Remove one ${m.name}`);
    rm.addEventListener("click", () => { cart[id] -= 1; if (cart[id] <= 0) delete cart[id]; saveCart(); render(); });
    li.appendChild(rm);
    $("lines").appendChild(li);
  });
}

function renderSummary() {
  const sub = subtotal();
  const s = $("summary");
  if (sub === 0) { s.innerHTML = ""; $("pay").disabled = true; $("pay").textContent = "Pay"; $("feeError").hidden = true; return; }
  const tax = sub * TAX_RATE;
  let feeText = "Loading…", total = null;
  if (feeState.status === "ok") { feeText = inr(feeState.fee) + " (est.)"; total = sub + feeState.fee + PLATFORM_FEE + tax; }
  if (feeState.status === "error") feeText = "Estimate unavailable";
  s.innerHTML = `
    <dt>Subtotal</dt><dd>${inr(sub)}</dd>
    <dt>Delivery fee</dt><dd>${feeText}</dd>
    <dt>Platform fee</dt><dd>${inr(PLATFORM_FEE)}</dd>
    <dt>Taxes (est.)</dt><dd>${inr(tax)}</dd>
    <dt class="total">Estimated total</dt><dd class="total">${total === null ? "—" : inr(total)}</dd>`;
  $("feeError").hidden = feeState.status !== "error";
  $("pay").disabled = total === null;
  $("pay").textContent = total === null ? "Pay" : `Pay ${inr(total)}`;
}

function render() { renderLines(); renderSummary(); if (subtotal() > 0 && feeState.status === "idle") refreshFee(); }

$("area").addEventListener("change", refreshFee);
$("retry").addEventListener("click", refreshFee);
$("pay").addEventListener("click", () => {
  $("result").textContent = "Simulated order placed. No payment was taken — this is a prototype.";
  console.info("[prototype event] pay_clicked", { subtotal: subtotal(), area: $("area").value }); // no personal data
});

renderMenu();
render();
