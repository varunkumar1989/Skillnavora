// Test the matcher outside n8n: node n8n/test_match.js
const fs = require("fs");
const path = require("path");
const rows = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "knowledge_qa.json"), "utf8"));
const src = fs.readFileSync(path.join(__dirname, "match_answer.js"), "utf8");
const questions = [
  "what is the fee for ai product management",
  "how much does the data engineer course cost",
  "do you guarantee a job",
  "is there a free excel course",
  "how long is the genai course",
  "why should i join skillnavora",
  "how can i contact you on whatsapp",
  "tell me about dinosaurs",
];
for (const q of questions) {
  const input = [{ json: { message: q } }, ...rows.map(r => ({ json: r }))];
  const run = new Function("$input", "return (async()=>{" + src + "})()");
  const $input = { first: () => input[0], all: () => input };
  run($input).then(out => console.log(`Q: ${q}\n  score ${out[0].json.score} | matched: ${out[0].json.matched_question}\n  A: ${out[0].json.reply.split("\n")[0].slice(0, 160)}\n`));
}
