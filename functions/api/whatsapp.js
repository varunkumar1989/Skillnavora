// WhatsApp Business Cloud API webhook (no n8n, no AI key). Meta sends each incoming WhatsApp message here;
// we answer from the website's own answer file (assets/knowledge_qa.json), so the replies match the site.
//
// Cloudflare secrets (Pages → Settings → Variables and secrets, as "Secret"):
//   WHATSAPP_VERIFY_TOKEN      any long random text; the same text is entered in Meta
//   WHATSAPP_APP_SECRET        Meta app → App settings → Basic → App secret
//   WHATSAPP_TOKEN             permanent system user token (Business Settings → System users)
//   WHATSAPP_PHONE_NUMBER_ID   the WhatsApp number's Phone Number ID (Meta → WhatsApp → API Setup)
// Meta callback URL: https://www.skillnavora.in/api/whatsapp   (subscribe to the "messages" field)
//
// Answers flagged "confirm" in the answer file are not quoted until the owner has checked them: the reply says
// the team will confirm, and gives the page link instead.

const GRAPH = "https://graph.facebook.com/v21.0/";
const FALLBACK = "Thanks for your message. I could not find an exact answer to that. Our team will reply soon. " +
  "You can see our programmes and details at https://www.skillnavora.in/programs.html";
const CONFIRM = "Thanks for asking. Our team is confirming the latest details for this, and will reply soon. " +
  "You can check the current information at ";

const STOP = new Set("the a an is are of to for and or in on at what how do does i my we you your can which who when where it this that be with please tell me about".split(" "));

// Compare two strings in constant time (no timing hints for the signature check).
function sameText(a, b) {
  a = String(a || ""); b = String(b || "");
  if (a.length !== b.length || !a.length) return false;
  let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

async function hmacHex(secret, text) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(text));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
}

const words = s => String(s || "").toLowerCase().replace(/[^\p{L}\p{N}\s₹$]/gu, " ").split(/\s+/).filter(w => w && !STOP.has(w));

// Scores each answer by its keywords (phrases count more) and by the words it shares with the question.
export function match(text, rows) {
  const q = String(text || "").toLowerCase();
  const qw = new Set(words(text));
  let best = null, bestScore = 0;
  for (const r of rows || []) {
    let s = 0;
    for (const k of String(r.keywords || "").split(",").map(x => x.trim().toLowerCase()).filter(Boolean)) {
      if (k.includes(" ")) { if (q.includes(k)) s += 3; }
      else if (qw.has(k)) s += 2;
    }
    for (const w of words(r.question)) if (qw.has(w)) s += 1;
    if (s > bestScore) { bestScore = s; best = r; }
  }
  return bestScore >= 2 ? best : null;
}

async function answer(request, text) {
  const rows = await fetch(new URL("/assets/knowledge_qa.json", request.url)).then(r => (r.ok ? r.json() : [])).catch(() => []);
  const best = match(text, rows);
  if (!best) return FALLBACK;
  const link = best.link || "https://www.skillnavora.in";
  if (String(best.confirm || "").trim()) return CONFIRM + link;
  return (String(best.answer || "").trim() + "\n\nMore: " + link).slice(0, 3500);
}

async function send(env, to, body) {
  const r = await fetch(GRAPH + env.WHATSAPP_PHONE_NUMBER_ID + "/messages", {
    method: "POST",
    headers: { authorization: "Bearer " + env.WHATSAPP_TOKEN, "content-type": "application/json" },
    body: JSON.stringify({ messaging_product: "whatsapp", to, type: "text", text: { body: body.slice(0, 4000), preview_url: false } }),
  });
  return r.ok;
}

// Meta re-sends a message if our reply is slow. Remember each message id for a day so it is answered once.
async function seen(id) {
  try {
    const cache = caches.default, key = new Request("https://whatsapp-dedup.skillnavora.local/" + encodeURIComponent(id));
    if (await cache.match(key)) return true;
    await cache.put(key, new Response("1", { headers: { "cache-control": "max-age=86400" } }));
    return false;
  } catch { return false; }
}

// Meta checks the address once, when you save the webhook in Meta.
export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  if (u.searchParams.get("hub.mode") === "subscribe" && env.WHATSAPP_VERIFY_TOKEN &&
      sameText(u.searchParams.get("hub.verify_token"), env.WHATSAPP_VERIFY_TOKEN)) {
    return new Response(u.searchParams.get("hub.challenge") || "", { status: 200, headers: { "content-type": "text/plain" } });
  }
  return new Response("forbidden", { status: 403 });
}

// Each incoming message. Anything that is not a text message from a person is acknowledged and ignored.
export async function onRequestPost({ request, env }) {
  if (!env.WHATSAPP_APP_SECRET || !env.WHATSAPP_TOKEN || !env.WHATSAPP_PHONE_NUMBER_ID) {
    return new Response("not configured", { status: 503 });
  }
  const raw = await request.text();
  const sig = (request.headers.get("x-hub-signature-256") || "").replace(/^sha256=/, "");
  if (!sameText(await hmacHex(env.WHATSAPP_APP_SECRET, raw), sig)) return new Response("bad signature", { status: 401 });

  let body; try { body = JSON.parse(raw); } catch { return new Response("bad json", { status: 400 }); }
  for (const e of body.entry || []) for (const c of e.changes || []) {
    if (c.field !== "messages") continue;
    for (const m of (c.value && c.value.messages) || []) {
      if (m.type !== "text" || !m.text || !m.text.body || !m.from) continue;
      if (m.id && await seen(m.id)) continue;
      const reply = await answer(request, m.text.body);
      await send(env, m.from, reply);
    }
  }
  return new Response("ok", { status: 200 });
}
