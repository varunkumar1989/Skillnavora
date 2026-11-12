// n8n "Code" node (JavaScript, run once for all items).
// Input 1: the incoming WhatsApp message in $json.message (text), e.g. from the WhatsApp trigger.
// Input 2: all rows of the knowledge sheet (tab "knowledge_qa"), one item per row, with the columns
//          id, topic, keywords, question, answer, link, confirm.
// Output: one item with the reply text ready for the WhatsApp send node.

const message = String(($input.first().json.message ?? $input.first().json.text ?? "")).toLowerCase().trim();
const rows = $input.all().map(i => i.json).filter(r => r.question && r.answer);

const words = s => s.toLowerCase().split(/[^a-z0-9₹$]+/).filter(w => w.length > 2);
const msgWords = new Set(words(message));

function score(row) {
  let s = 0;
  // keyword phrases: "AI PM|product management" counts as separate phrases; comma-separated alternatives
  const phrases = String(row.keywords || "").split(/[,|]/).map(p => p.trim().toLowerCase()).filter(Boolean);
  for (const p of phrases) {
    if (p.length >= 3 && message.includes(p)) s += 3;
  }
  // overlap with the question text
  for (const w of words(row.question || "")) if (msgWords.has(w)) s += 1;
  return s;
}

const ranked = rows.filter(r => r.topic !== "Fallback").map(r => ({ r, s: score(r) })).sort((a, b) => b.s - a.s);
const best = ranked[0];
const fallback = rows.find(r => r.topic === "Fallback");

let reply;
if (!best || best.s < 3) {
  reply = fallback ? fallback.answer + (fallback.link ? "\n" + fallback.link : "") : "Sorry, I don't have that information yet.";
} else {
  const r = best.r;
  reply = r.answer;
  if (r.confirm && String(r.confirm).trim()) {
    reply += "\n\nWe are confirming this detail. A counsellor will reply with the latest information.";
  }
  if (r.link) reply += "\n" + r.link;
}

return [{ json: { reply, matched_question: best && best.s >= 3 ? best.r.question : null, score: best ? best.s : 0 } }];
