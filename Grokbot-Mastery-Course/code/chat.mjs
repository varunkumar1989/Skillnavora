// Node.js 18+ example: one chat request, then a streamed request.
// STATUS: syntax-checked with `node --check`. UNTESTED against the live API (no key or network access).
// Confirm the base URL, endpoint and model ID on https://docs.x.ai before running.
//   XAI_API_KEY=... GROK_MODEL=... node chat.mjs
const BASE_URL = process.env.XAI_BASE_URL ?? "https://api.x.ai/v1";
const MODEL = process.env.GROK_MODEL ?? "grok-4.7"; // placeholder model ID
const KEY = process.env.XAI_API_KEY;
if (!KEY) { console.error("Set XAI_API_KEY first."); process.exit(1); }

const messages = [
  { role: "system", content: "You are a concise assistant. Answer in one sentence." },
  { role: "user", content: "What is a context window?" },
];

async function post(body) {
  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res;
}

// 1. Normal request
const res = await post({ model: MODEL, messages, max_tokens: 200 });
const data = await res.json();
console.log(data.choices[0].message.content);
console.log("usage:", data.usage);

// 2. Streamed request: print tokens as they arrive (server-sent events)
const stream = await post({ model: MODEL, messages, max_tokens: 200, stream: true });
const decoder = new TextDecoder();
let buffer = "";
for await (const part of stream.body) {
  buffer += decoder.decode(part, { stream: true });
  const lines = buffer.split("\n");
  buffer = lines.pop();
  for (const line of lines) {
    if (!line.startsWith("data:")) continue;
    const payload = line.slice(5).trim();
    if (payload === "[DONE]") { process.stdout.write("\n"); continue; }
    const delta = JSON.parse(payload).choices?.[0]?.delta?.content;
    if (delta) process.stdout.write(delta);
  }
}
