/* AI Studio for lesson, handbook and lab pages. Generated from assets/site.js by tools/studio_inject.py;
   do not edit by hand. */
/* Ask AI side tab: on every page, a tab on the left edge opens AI Studio shortcuts and a quick question box. */
(function () {
  if (document.body.hasAttribute("data-app") || /admin\.html$/.test(location.pathname) || document.getElementById("askai")) return;
  const R = (function () {
    const s = (document.currentScript && document.currentScript.src) || (document.querySelector('script[src*="assets/studio.js"]') || {}).src || "";
    return s ? s.replace(/assets\/studio\.js.*$/, "") : "/";
  })();
  const SITE = { instagramDM: "https://ig.me/m/skillnavora" };
  const T = [["ai-tutor.html", "💬", "AI Tutor", "Ask any study question"], ["prd-writer.html", "📝", "PRD / BRD / FRD Writer", "Write requirements with AI"],
    ["pm-toolkit.html", "🧰", "AI PM Toolkit", "Discovery, sizing, A/B tests…"], ["speaking-coach.html", "🎤", "Speaking Coach", "English & interviews"],
    ["practice.html", "🎯", "AI mock interview", "Get scored"], ["ai.html", "✨", "All of AI Studio", "Every free AI tool"]];
  const css = document.createElement("style");
  css.textContent = `#askai-tab{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:9990;writing-mode:vertical-rl;rotate:180deg;border:0;border-radius:0 12px 12px 0;padding:14px 9px;background:linear-gradient(180deg,#54e0c4,#2fbfa6);color:#04211c;font:800 17px/1.1 var(--body,system-ui);letter-spacing:.04em;cursor:pointer;box-shadow:0 8px 24px rgba(10,60,50,.35)}
#askai-tab:hover{padding-left:12px}#askai{position:fixed;left:0;top:0;bottom:0;width:min(340px,88vw);z-index:9995;background:var(--surface,#fff);color:var(--ink,#0d1630);border-right:1px solid var(--line,#e1e6f0);box-shadow:16px 0 50px rgba(13,27,24,.25);transform:translateX(-105%);transition:transform .22s ease;display:flex;flex-direction:column;padding:18px;gap:12px;overflow:auto}
#askai.open{transform:none}#askai-bg{position:fixed;inset:0;z-index:9994;background:rgba(7,16,15,.35);display:none}#askai-bg.open{display:block}
#askai h2{font-size:19px;margin:0}#askai .x{position:absolute;right:12px;top:10px;border:0;background:none;font-size:24px;cursor:pointer;color:inherit}
#askai form{display:flex;flex-direction:column;gap:8px}#askai textarea{min-height:70px;border:1px solid var(--line,#e1e6f0);border-radius:12px;padding:10px 12px;font:inherit;background:var(--bg,#f5f7fc);color:inherit;resize:vertical}
#askai a.t{display:flex;gap:10px;align-items:center;text-decoration:none;color:inherit;border:1px solid var(--line,#e1e6f0);border-radius:12px;padding:9px 12px}#askai a.t:hover{border-color:var(--brand,#6C4CF5)}#askai a.t span{font-size:20px}#askai a.t small{display:block;color:var(--mu,#55607a);font-size:12.5px}
@media (max-width:760px){#askai-tab{top:auto;bottom:16px;left:12px;transform:none;rotate:none;writing-mode:horizontal-tb;border-radius:99px;padding:10px 16px;font-size:14px;box-shadow:0 8px 20px rgba(10,60,50,.3)}#askai-tab:hover{padding-left:16px}body.has-sticky #askai-tab{bottom:92px}}@media print{#askai-tab,#askai{display:none}}`;
  css.textContent += '\n/* Standalone AI Studio (lesson and handbook pages): own colours for light and dark */\n#askai,#askai-tab{--surface:#ffffff;--ink:#0d1630;--mu:#55607a;--line:#e1e6f0;--bg:#f5f7fc;--brand:#6C4CF5;--on-brand:#ffffff;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}\n@media (prefers-color-scheme: dark){html:not([data-theme="light"]) #askai{--surface:#0d1b18;--ink:#ebf6f3;--mu:#9fb6b1;--line:#1d3a36;--bg:#07100f;--brand:#54e0c4;--on-brand:#04211c}}\nhtml[data-theme="dark"] #askai{--surface:#0d1b18;--ink:#ebf6f3;--mu:#9fb6b1;--line:#1d3a36;--bg:#07100f;--brand:#54e0c4;--on-brand:#04211c}\n#askai,#askai *{box-sizing:border-box}\n#askai{font-size:15px;line-height:1.5}\n#askai .kicker{font:700 12px/1.2 inherit;letter-spacing:.14em;text-transform:uppercase;color:var(--brand)}\n#askai .btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;font:600 13px/1.2 inherit;font-family:inherit;border-radius:99px;padding:7px 12px;cursor:pointer;border:1px solid var(--line);background:var(--surface);color:var(--ink);text-decoration:none}\n#askai .btn-primary{background:var(--brand);border-color:var(--brand);color:var(--on-brand);padding:10px 14px;font-size:14px}\n#askai .btn:hover{border-color:var(--brand)}\n#askai a{color:var(--brand)}\n#askai a.t{color:var(--ink)}\n#askai .ig-dm{display:inline-block;padding:9px 14px;border-radius:10px;color:#fff!important;font-weight:600;text-decoration:none;background:linear-gradient(45deg,#f09433,#dc2743 50%,#bc1888)}\n#askai textarea{width:100%}\n#askai a.t b{font-size:15px;font-weight:700;line-height:1.3}\n#askai a.t small{font-size:12.5px;line-height:1.35}\n#askai h2{font-weight:800;letter-spacing:-.01em}\n';
  document.head.appendChild(css);
  const tab = document.createElement("button"); tab.id = "askai-tab"; tab.type = "button"; tab.textContent = "✨ AI Studio"; tab.setAttribute("aria-controls", "askai"); tab.setAttribute("aria-expanded", "false");
  const bg = document.createElement("div"); bg.id = "askai-bg";
  const box = document.createElement("aside"); box.id = "askai"; box.setAttribute("aria-label", "AI Studio");
  box.innerHTML = `<button class="x" type="button" aria-label="Close">×</button><div><div class="kicker" style="font-size:12px">Free</div><h2>AI Studio</h2></div>
<div id="askai-quick" style="display:flex;flex-wrap:wrap;gap:6px"><button class="btn btn-line btn-sm" type="button" data-q="What is the fee for AI-First Product Management?">Fee: AI PM</button><button class="btn btn-line btn-sm" type="button" data-q="What is the fee for AI-First Data Engineer?">Fee: Data Eng</button><button class="btn btn-line btn-sm" type="button" data-q="What free courses and resources are there?">Free courses</button><button class="btn btn-line btn-sm" type="button" data-q="Why should I join SkillNavora?">Why join?</button><button class="btn btn-line btn-sm" type="button" data-q="Do you guarantee a job or placement?">Jobs?</button><button class="btn btn-line btn-sm" type="button" data-q="How can I contact SkillNavora?">Contact</button></div>
<div id="askai-ans" role="status" aria-live="polite" hidden style="border:1px solid var(--line,#e1e6f0);border-radius:12px;padding:12px;background:var(--bg,#f5f7fc);font-size:14.5px;line-height:1.55"></div>
<form><textarea maxlength="2000" placeholder="Ask about fees, programmes, free courses, careers… or anything else" aria-label="Your question"></textarea><button class="btn btn-primary btn-sm" type="submit">Get answer →</button></form>
${T.map(([h, i, n, s]) => `<a class="t" href="${R + h}"><span>${i}</span><span><b>${n}</b><small>${s}</small></span></a>`).join("")}`;
  document.body.append(tab, bg, box);
  const set = o => { box.classList.toggle("open", o); bg.classList.toggle("open", o); tab.setAttribute("aria-expanded", o); if (o) setTimeout(() => box.querySelector("textarea").focus(), 60); };
  tab.addEventListener("click", () => set(true)); bg.addEventListener("click", () => set(false)); box.querySelector(".x").addEventListener("click", () => set(false));
  document.addEventListener("keydown", e => { if (e.key === "Escape") set(false); });
  const ta = box.querySelector("textarea");
  box.querySelector("form").addEventListener("submit", e => { e.preventDefault(); const q = ta.value.trim(); const path = location.pathname.split("/").filter(Boolean).slice(-2).join("/");
    const u = new URL(R + "ai-tutor.html", location.href); if (q) u.searchParams.set("q", q); if (path && !/ai-tutor/.test(path)) u.searchParams.set("page", "/" + location.pathname.replace(/^\/+/, ""));
    location.href = u.href; });
  ta.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); box.querySelector("form").requestSubmit(); } });

  /* Answers for the panel: Q&A first (same knowledge as the WhatsApp agent), then the page, lesson and PDF index. */
  let KB = null, CONTENT = null;
  const ans = box.querySelector("#askai-ans");
  const norm = w => (w.length > 3 && w.endsWith("s") && !w.endsWith("ss") ? w.slice(0, -1) : w);
  const words = t => String(t).toLowerCase().split(/[^a-z0-9]+/).filter(w => w.length > 2).map(norm);
  function scoreQA(row, msg) {
    let n = 0;
    String(row.keywords || "").split(/[,|]/).map(p => p.trim().toLowerCase()).filter(p => p.length >= 3).forEach(p => { if (msg.indexOf(p) > -1) n += 3; });
    const mw = new Set(words(msg)); words(row.question || "").forEach(w => { if (mw.has(w)) n += 1; });
    return n;
  }
  function bestQA(msg) { let top = null, s = 0; KB.forEach(r => { if (r.topic === "Fallback") return; const v = scoreQA(r, msg); if (v > s) { s = v; top = r; } }); return s >= 3 ? top : null; }
  const FILLER = new Set(['tell','about','what','where','which','when','how','does','with','from','this','that','have','there','give','show','find','info','information','please','want','need','know','know','can','you','your','the','and','for','are','was','about','topic','explain','any','all','more','some','should','would','could','will','its','them','they','lesson','course','page']);
  function bestContent(msg) {
    const mw = new Set(words(msg).filter(w => !FILLER.has(w)));
    return CONTENT.map(c => { let n = 0; new Set(words(c.title)).forEach(w => { if (mw.has(w)) n += 3; }); new Set(words(c.desc)).forEach(w => { if (mw.has(w)) n += 1; }); return { c, n }; })
      .filter(x => x.n >= 3).sort((a, b) => b.n - a.n).slice(0, 3).map(x => x.c);
  }
  function show(parts) {
    ans.hidden = false; ans.innerHTML = "";
    parts.forEach(part => {
      if (part.links) {
        part.links.forEach(l => { const a = document.createElement("a"); a.href = l.link; a.target = "_blank"; a.rel = "noopener"; a.className = "t"; a.style.marginTop = "6px";
          const b = document.createElement("span"); b.textContent = l.type === "PDF" ? "📄" : l.type === "Lesson" ? "🎓" : "🔗";
          const t = document.createElement("span"); const strong = document.createElement("b"); strong.textContent = l.title; const sm = document.createElement("small"); sm.textContent = l.type; t.appendChild(strong); t.appendChild(sm);
          a.appendChild(b); a.appendChild(t); ans.appendChild(a); });
      } else if (part.link) {
        const a = document.createElement("a"); a.href = part.link; a.target = "_blank"; a.rel = "noopener"; a.textContent = part.linkText || "Open the page"; a.style.display = "block"; a.style.margin = "6px 0"; ans.appendChild(a);
      } else { const p = document.createElement("p"); p.style.margin = "0 0 6px"; p.textContent = part.text; ans.appendChild(p); }
    });
  }
  async function ensure() {
    if (!KB) KB = await fetch(R + "assets/knowledge_qa.json").then(r => r.json());
    if (!CONTENT) CONTENT = await fetch(R + "assets/content_index.json").then(r => r.json()).catch(() => []);
  }
  async function answer(q) {
    const msg = String(q).toLowerCase().trim();
    await ensure();
    if (/\b(where|find|pdf|pdfs|file|files|download|handbook|notes|template|link)\b/.test(msg)) {
      const first = bestContent(msg);
      if (first.length) { show([{ text: "Here is where to find it:" }, { links: first }]); return true; }
    }
    const r = bestQA(msg);
    if (r) {
      const parts = [{ text: r.answer }];
      if (r.confirm) parts.push({ text: "(A counsellor will confirm the latest details before you enrol.)" });
      if (r.link) parts.push({ text: "Open the page", link: r.link });
      show(parts);
      return true;
    }
    const found = bestContent(msg);
    if (found.length) {
      show([{ text: "Here is where to find it:" }, { links: found }]);
      return true;
    }
    return false;
  }
  box.querySelectorAll("#askai-quick [data-q]").forEach(b => b.addEventListener("click", () => { ta.value = b.dataset.q; answer(b.dataset.q).catch(() => show([{ text: "Sorry, the answers are unavailable right now. Please try again." }])); }));
  function noAnswer(q) {
    ans.hidden = false; ans.innerHTML = "";
    const p = document.createElement("p"); p.style.margin = "0 0 8px";
    p.textContent = "I couldn't find that on the website. Message us on Instagram and someone from our team will reply to you directly.";
    try { navigator.clipboard.writeText(q).then(() => { p.textContent += " Your question is copied, so you can paste it there."; }, () => {}); } catch (err) {}
    const ig = document.createElement("a"); ig.href = (typeof SITE !== "undefined" && SITE.instagramDM) || "https://ig.me/m/skillnavora"; ig.target = "_blank"; ig.rel = "noopener"; ig.className = "ig-dm";
    ig.textContent = "💬 Chat with our team on Instagram";
    const tu = new URL(R + "ai-tutor.html", location.href); tu.searchParams.set("q", q);
    const t = document.createElement("a"); t.href = tu.href; t.textContent = "Study question? Ask the AI Tutor →"; t.style.cssText = "display:block;margin-top:8px;font-size:.9em";
    ans.appendChild(p); ans.appendChild(ig); ans.appendChild(t);
  }
  const originalSubmit = box.querySelector("form");
  originalSubmit.addEventListener("submit", e => {
    const q = ta.value.trim();
    if (!q) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    answer(q).then(ok => { if (!ok) noAnswer(q); }).catch(() => noAnswer(q));
  }, true);
})();
