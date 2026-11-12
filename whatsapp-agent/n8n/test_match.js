// Test the matcher outside n8n: node whatsapp-agent/n8n/test_match.js
const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..", "..");
const rows = JSON.parse(fs.readFileSync(path.join(root, "assets", "knowledge_qa.json"), "utf8"));
const content = JSON.parse(fs.readFileSync(path.join(root, "assets", "content_index.json"), "utf8"));
const src = fs.readFileSync(path.join(__dirname, "match_answer.js"), "utf8");
const ctx = { helpers: { httpRequest: async () => content } };
const wa = q => ({ messaging_product: "whatsapp", contacts: [{ wa_id: "919800000000" }], messages: [{ from: "919800000000", type: "text", text: { body: q } }] });
const fb = q => ({ body: { object: "page", entry: [{ messaging: [{ sender: { id: "12345" }, message: { text: q } }] }] } });
const cases = [
  ["chat", { chatInput: "what is the fee for ai product management" }],
  ["whatsapp", wa("hey")],
  ["whatsapp", wa("how much does the data engineer course cost")],
  ["whatsapp", wa("where is the PRD template")],
  ["messenger", fb("do you guarantee a job")],
  ["messenger", fb("prompt injection")],
  ["whatsapp", wa("tell me about dinosaurs")],
];
(async () => {
  for (const [kind, msg] of cases) {
    const input = [{ json: msg }, ...rows.map(r => ({ json: r }))];
    const run = new Function("$input", "return (async()=>{" + src + "})()");
    const $input = { first: () => input[0], all: () => input };
    const out = (await run.call(ctx, $input))[0].json;
    console.log(`[${kind}] to=${out.to} channel=${out.channel} score=${out.score} matched=${out.matched_question}\n  ${out.reply.replace(/\n/g, " / ").slice(0, 170)}\n`);
  }
})();
