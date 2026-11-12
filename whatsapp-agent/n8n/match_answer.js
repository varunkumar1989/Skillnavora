// n8n "Code" node (JavaScript, "Run Once for All Items"). Free: no AI model needed.
// Works after any of these triggers (it looks for the message itself):
//   - "WhatsApp Trigger"            (WhatsApp Business Cloud)  -> messages[0].text.body
//   - "Webhook" named "Messenger Webhook" (Facebook Messenger / Instagram) -> entry[0].messaging[0].message.text
//   - "When chat message received"  (n8n test chat)            -> chatInput
// Input items: the knowledge rows from the HTTP Request node
//   (GET https://www.skillnavora.in/assets/knowledge_qa.json) or from the Google Sheet.
// Output: one item { reply, to, channel, matched_question, score } for the send node.

function fromNode(name) { try { return $(name).first().json; } catch (e) { return null; } }
function pick(j) {
  if (!j) return null;
  const wa = j.messages?.[0] || j.body?.entry?.[0]?.changes?.[0]?.value?.messages?.[0];
  if (wa) return { text: wa.text?.body || wa.button?.text || wa.interactive?.button_reply?.title || "", to: wa.from, channel: "whatsapp" };
  const fb = (j.body || j).entry?.[0]?.messaging?.[0];
  if (fb) return { text: fb.message?.text || fb.postback?.title || "", to: fb.sender?.id, channel: "messenger" };
  const t = j.chatInput ?? j.message ?? j.text;
  if (typeof t === "string") return { text: t, to: j.sessionId || null, channel: "chat" };
  return null;
}
const hasNodes = typeof $ === "function";
const incoming = (hasNodes && (pick(fromNode("WhatsApp Trigger")) || pick(fromNode("Messenger Webhook")) || pick(fromNode("When chat message received"))))
  || pick($input.first().json) || { text: "", to: null, channel: "chat" };
const message = String(incoming.text || "").toLowerCase().trim();
const rows = $input.all().map(i => i.json).filter(r => r.question && r.answer);

const norm = w => (w.length > 3 && w.endsWith("s") && !w.endsWith("ss") ? w.slice(0, -1) : w);
const words = s => String(s || "").toLowerCase().split(/[^a-z0-9₹$]+/).filter(w => w.length > 2).map(norm);
const FILLER = new Set(["tell", "about", "what", "where", "which", "when", "how", "doe", "does", "with", "from", "this", "that", "have", "there", "give", "show", "find", "info", "information", "please", "want", "need", "know", "can", "you", "your", "the", "and", "for", "are", "was", "topic", "explain", "any", "all", "more", "some", "should", "would", "could", "will", "its", "them", "they", "lesson", "course", "page"]);
const msgWords = new Set(words(message));

function score(row) {
  let s = 0;
  const phrases = String(row.keywords || "").split(/[,|]/).map(p => p.trim().toLowerCase()).filter(Boolean);
  for (const p of phrases) if (p.length >= 3 && message.includes(p)) s += 3;
  for (const w of words(row.question)) if (msgWords.has(w)) s += 1;
  return s;
}

const greeting = /^(hi|hey|hello|hii+|namaste|good (morning|afternoon|evening))\b/.test(message);
const ranked = rows.filter(r => r.topic !== "Fallback").map(r => ({ r, s: score(r) })).sort((a, b) => b.s - a.s);
const best = ranked[0];
const fallback = rows.find(r => r.topic === "Fallback");

let reply, matched = null;
if (greeting && (!best || best.s < 3)) {
  reply = "Hi! I can answer questions about SkillNavora programmes, fees, free courses, careers and where to find any lesson or PDF. What would you like to know?";
} else if (best && best.s >= 3) {
  const r = best.r; matched = r.question;
  reply = r.answer;
  if (r.confirm && String(r.confirm).trim()) reply += "\n\nWe are confirming this detail. A counsellor will reply with the latest information.";
  if (r.link) reply += "\n" + r.link;
} else {
  // Not in the Q&A: look for the page, lesson or PDF that covers the topic.
  let content = [];
  try {
    if (this && this.helpers && this.helpers.httpRequest) {
      content = await this.helpers.httpRequest({ url: "https://www.skillnavora.in/assets/content_index.json", json: true });
    }
  } catch (e) { content = []; }
  const cw = new Set([...msgWords].filter(w => !FILLER.has(w)));
  const hits = (Array.isArray(content) ? content : []).map(c => {
    let n = 0; words(c.title).forEach(w => { if (cw.has(w)) n += 3; }); words(c.desc).forEach(w => { if (cw.has(w)) n += 1; });
    return { c, n };
  }).filter(x => x.n >= 3).sort((a, b) => b.n - a.n).slice(0, 3).map(x => x.c);
  if (hits.length) {
    reply = "Here is where to find it:\n" + hits.map(c => `• ${c.title} (${c.type})\n${c.link}`).join("\n");
    matched = "content: " + hits[0].title;
  } else {
    reply = fallback ? fallback.answer + (fallback.link ? "\n" + fallback.link : "") : "Sorry, I don't have that information yet.";
  }
}

return [{ json: { reply, to: incoming.to, channel: incoming.channel, matched_question: matched, score: best ? best.s : 0 } }];
