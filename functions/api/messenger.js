// Facebook Messenger and Instagram direct message webhook (no n8n). Meta sends each message here; we answer from
// the website's answer file (assets/knowledge_qa.json) and save every question to the lead table, with its channel,
// so the team can follow up and see what people ask.
//
// Cloudflare secrets (Pages → Settings → Variables and secrets, as "Secret"):
//   META_VERIFY_TOKEN   any long random text; the same text is entered in Meta
//   META_APP_SECRET     App settings → Basic → App secret (falls back to WHATSAPP_APP_SECRET, same app)
//   META_PAGE_TOKEN     the Page access token of the connected Facebook Page (permanent, from a System User)
//   SUPABASE_SERVICE_KEY (already set) saves the leads
// Meta callback URL: https://www.skillnavora.in/api/messenger  (subscribe to "messages" for Messenger and Instagram)
//
// Until the app is published and Meta approves the Messenger/Instagram permissions, Meta sends real messages only
// from test users. Replies are not sent to anyone else until then.

import { match } from "./whatsapp.js";

const GRAPH = "https://graph.facebook.com/v21.0/";
const SUPABASE_URL = "https://rnncabqtcxxivuyjwoja.supabase.co";
const FALLBACK = "Thanks for your message. I don't have that answer yet, so someone from our team will reply to you here shortly. " +
  "You can also book a free counselling call at https://www.skillnavora.in/contact.html";
const CONFIRM = "Thanks for asking. Our team is confirming the latest details for this, and will reply soon. You can check the current information at ";

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
const appSecret = env => env.META_APP_SECRET || env.WHATSAPP_APP_SECRET;

async function answer(request, text) {
  const rows = await fetch(new URL("/assets/knowledge_qa.json", request.url)).then(r => (r.ok ? r.json() : [])).catch(() => []);
  const best = match(text, rows);
  if (!best) return FALLBACK;
  const link = best.link || "https://www.skillnavora.in";
  if (String(best.confirm || "").trim()) return CONFIRM + link;
  return (String(best.answer || "").trim() + "\n\nMore: " + link).slice(0, 1900);
}

// Sends a Messenger/Instagram reply through the connected Page.
async function send(env, recipientId, text) {
  const r = await fetch(GRAPH + "me/messages", {
    method: "POST",
    headers: { authorization: "Bearer " + env.META_PAGE_TOKEN, "content-type": "application/json" },
    body: JSON.stringify({ recipient: { id: recipientId }, messaging_type: "RESPONSE", message: { text: text.slice(0, 1900) } }),
  });
  return r.ok;
}

// Saves the question as a lead: channel, sender id, and the message, so the team can follow up.
async function saveLead(env, channel, senderId, text, answered) {
  const key = env.SUPABASE_SERVICE_KEY;
  if (!key) return false;
  const row = {
    kind: "application", first_name: channel === "instagram" ? "Instagram user" : "Messenger user", source: channel,
    message: `[${channel === "instagram" ? "Instagram DM" : "Messenger"} from ${senderId}${answered ? "" : ", not answered automatically"}] ${String(text).slice(0, 1800)}`,
    status: "new",
  };
  const headers = { apikey: key, "content-type": "application/json", prefer: "return=minimal" };
  if (key.includes(".")) headers.authorization = "Bearer " + key;
  const r = await fetch(SUPABASE_URL + "/rest/v1/applications", { method: "POST", headers, body: JSON.stringify(row) }).catch(() => null);
  return !!(r && r.ok);
}

// Meta re-sends a message if the reply is slow. Remember each message id for a day so it is answered once.
async function seen(id) {
  try {
    const cache = caches.default, key = new Request("https://messenger-dedup.skillnavora.local/" + encodeURIComponent(id));
    if (await cache.match(key)) return true;
    await cache.put(key, new Response("1", { headers: { "cache-control": "max-age=86400" } }));
    return false;
  } catch { return false; }
}

// Meta checks the address once, when you save the webhook.
export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  if (u.searchParams.get("hub.mode") === "subscribe" && env.META_VERIFY_TOKEN &&
      sameText(u.searchParams.get("hub.verify_token"), env.META_VERIFY_TOKEN)) {
    return new Response(u.searchParams.get("hub.challenge") || "", { status: 200, headers: { "content-type": "text/plain" } });
  }
  return new Response("forbidden", { status: 403 });
}

// Each incoming message. Echoes, read receipts, reactions and non-text messages are acknowledged and ignored.
export async function onRequestPost({ request, env }) {
  if (!appSecret(env) || !env.META_PAGE_TOKEN) return new Response("not configured", { status: 503 });
  const raw = await request.text();
  const sig = (request.headers.get("x-hub-signature-256") || "").replace(/^sha256=/, "");
  if (!sameText(await hmacHex(appSecret(env), raw), sig)) return new Response("bad signature", { status: 401 });

  let body; try { body = JSON.parse(raw); } catch { return new Response("bad json", { status: 400 }); }
  if (body.object !== "page" && body.object !== "instagram") return new Response("ignored", { status: 200 });
  const channel = body.object === "instagram" ? "instagram" : "messenger";

  for (const e of body.entry || []) for (const m of e.messaging || []) {
    if (m.message && m.message.is_echo) continue;          // our own replies
    const text = m.message && m.message.text;
    if (!text || !m.sender || !m.sender.id) continue;      // no text (read, delivery, reaction, attachment)
    if (m.message.mid && await seen(m.message.mid)) continue;
    const reply = await answer(request, text);
    const answered = reply !== FALLBACK && !reply.startsWith(CONFIRM);
    await saveLead(env, channel, m.sender.id, text, answered);
    await send(env, m.sender.id, reply);
  }
  return new Response("ok", { status: 200 });
}
