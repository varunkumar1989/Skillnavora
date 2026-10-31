"""AI Studio pages: ai.html (hub), ai-tutor.html, prd-writer.html, speaking-coach.html,
plus assets/ai-index.txt (the course index the AI Tutor uses to link learners to lessons)."""
import html, json, os, re
E = html.escape

AI_NAV = [  # (path, name, small, svg path)
    ("ai.html", "AI Studio", "All AI tools in one place, free", '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/>'),
    ("ai-academy.html", "AI Skills Academy", "All AI skills courses: lessons, PDFs, interactive", '<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>'),
    ("ai-skills-map.html", "AI Skills Map", "Every AI skill and where to learn it", '<circle cx="12" cy="12" r="10"/><path d="M16.2 7.8l-2 6.4-6.4 2 2-6.4z"/>'),
    ("ai-tutor.html", "AI Tutor", "Ask any study question, 24×7", '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.7A8.5 8.5 0 1 1 21 11.5z"/>'),
    ("prd-writer.html", "AI PRD / BRD / FRD Writer", "Write any requirements document with AI", '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>'),
    ("pm-toolkit.html", "AI PM Toolkit", "13 PM capabilities: discovery, sizing, A/B tests…", '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>'),
    ("prd-library.html", "PRD library: 120 ideas", "Template, examples, write any idea with AI", '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M8 7h8M8 11h6"/>'),
    ("brd-frd.html", "BRD & FRD for business analysts", "Templates, 25 project ideas, learn from the best", '<path d="M3 3h18v18H3z"/><path d="M3 9h18M9 21V9"/>'),
    ("speaking-coach.html", "AI Speaking Coach", "English, public speaking, interviews", '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>'),
    ("practice.html", "AI mock interview", "Answer a question, get a score", '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'),
    ("web-automation.html", "Web Automation & Playwright MCP", "Webhooks, triggers, browser automation", '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>'),
    ("ai-builder-tools.html", "AI Builder Tools how-to", "Claude, ChatGPT/Codex, Gemini, Lovable", '<path d="M12 2l3 7h7l-5.5 4 2 7-6.5-4.5L5.5 20l2-7L2 9h7z"/>'),
    ("ai-engineer.html", "AI Engineer path", "Everything an AI engineer does", '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
    ("study-library.html", "Study Library", "All study material in one page", '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M8 7h8M8 11h6"/>')
]

CSS = """<style>
.ai-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.ai-card{display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:var(--shadow);transition:transform .15s,border-color .15s}
.ai-card:hover{transform:translateY(-2px);border-color:var(--brand)}.ai-card .ic{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,#6C4CF5,#22D3EE);color:#fff}
.ai-card .ic svg{width:24px;height:24px}.ai-card h3{margin:6px 0 0;font-size:20px}.ai-card p{margin:0;color:var(--mu);font-size:15px}.ai-card ul{margin:4px 0 0;padding-left:18px;color:var(--mu);font-size:14px}.ai-card .go{margin-top:auto;font-weight:700;color:var(--brand)}
.ai-badge{display:inline-block;font:700 11px var(--body);letter-spacing:.06em;text-transform:uppercase;background:rgba(108,76,245,.12);color:#6C4CF5;border-radius:99px;padding:4px 10px;width:max-content}
.ai-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;counter-reset:s}.ai-steps div{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 18px}.ai-steps b{display:block;margin-bottom:4px}
.ai-steps div::before{counter-increment:s;content:counter(s);display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--brand);color:#fff;font-weight:800;margin-bottom:8px}
.ai-wrap{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:22px;align-items:start}
.ai-side{position:sticky;top:84px;display:flex;flex-direction:column;gap:12px}
.ai-side .card{padding:18px}.ai-side h3{font-size:15px;margin:0 0 8px}
.ai-chips{display:flex;flex-wrap:wrap;gap:8px}.ai-chips button{border:1px solid var(--line);background:var(--surface-2);color:var(--ink);border-radius:99px;padding:7px 12px;font:600 13.5px var(--body);cursor:pointer;text-align:left}
.ai-chips button:hover,.ai-chips button[aria-pressed=true]{border-color:var(--brand);background:rgba(108,76,245,.1)}
.ai-chat{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow);min-height:70vh}
.ai-log{flex:1;overflow:auto;padding:20px;display:flex;flex-direction:column;gap:14px;max-height:68vh}
.ai-m{max-width:88%;padding:12px 16px;border-radius:16px;line-height:1.6;overflow-wrap:anywhere}.ai-m.u{align-self:flex-end;background:var(--brand);color:#fff;border-bottom-right-radius:4px;white-space:pre-wrap}
.ai-m.a{align-self:flex-start;background:var(--surface-2);border:1px solid var(--line);border-bottom-left-radius:4px}
.ai-form{display:flex;gap:10px;padding:14px;border-top:1px solid var(--line);align-items:flex-end}.ai-form textarea{flex:1;min-height:52px;max-height:200px;resize:vertical;border:1px solid var(--line);border-radius:14px;padding:12px 14px;font:inherit;background:var(--bg);color:var(--ink)}
.ai-out h1,.ai-out h2,.ai-out h3{line-height:1.3;margin:14px 0 6px}.ai-out h1{font-size:24px}.ai-out h2{font-size:19px}.ai-out h3{font-size:16.5px}.ai-out p{margin:6px 0}.ai-out ul,.ai-out ol{margin:6px 0;padding-left:22px}
.ai-out pre{background:#0d1630;color:#e8edfb;border-radius:12px;padding:12px 14px;overflow:auto;font:13.5px/1.5 ui-monospace,Consolas,monospace}.ai-out code{font:13.5px ui-monospace,Consolas,monospace;background:rgba(108,76,245,.1);border-radius:6px;padding:1px 5px}.ai-out pre code{background:none;padding:0}
.ai-out table{border-collapse:collapse;width:100%;margin:8px 0;font-size:14px;display:block;overflow:auto}.ai-out th,.ai-out td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}.ai-out th{background:var(--surface-2)}
.ai-out a{color:var(--brand);font-weight:600}.ai-out blockquote{margin:8px 0;padding:6px 12px;border-left:3px solid var(--brand);color:var(--mu)}
.ai-dots::after{content:"…";animation:aidot 1s steps(3) infinite}@keyframes aidot{0%{content:"."}50%{content:".."}100%{content:"..."}}
.ai-note{font-size:13px;color:var(--mu);margin:8px 0 0}
.ai-err{background:rgba(220,38,38,.08);border:1px solid rgba(220,38,38,.3);border-radius:12px;padding:10px 14px;font-size:14.5px}
.ai-grid2{display:grid;grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:22px;align-items:start}
.ai-f{display:flex;flex-direction:column;gap:12px}.ai-f label{display:flex;flex-direction:column;gap:5px;font-weight:600;font-size:14px}
.ai-f input,.ai-f select,.ai-f textarea{border:1px solid var(--line);border-radius:12px;padding:10px 12px;font:400 15px var(--body);background:var(--bg);color:var(--ink)}.ai-f textarea{min-height:84px;resize:vertical}
.ai-doc{background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:24px 28px;box-shadow:var(--shadow);min-height:60vh}
.ai-acts{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}
.ai-empty{color:var(--mu);text-align:center;padding:60px 10px}.ai-empty b{display:block;font-size:20px;color:var(--ink);margin-bottom:6px}
.sc-modes{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}.sc-modes button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:14px;padding:10px 14px;font:700 14.5px var(--body);cursor:pointer;text-align:left}
.sc-modes button small{display:block;font:500 12px var(--body);color:var(--mu)}.sc-modes button[aria-pressed=true]{background:linear-gradient(135deg,#6C4CF5,#22D3EE);color:#fff;border-color:transparent}.sc-modes button[aria-pressed=true] small{color:#eef}
.sc-q{font-size:20px;font-weight:700;line-height:1.4;margin:6px 0 10px}
.sc-mic{width:96px;height:96px;border-radius:50%;border:0;background:linear-gradient(135deg,#6C4CF5,#22D3EE);color:#fff;cursor:pointer;display:grid;place-items:center;margin:10px auto;box-shadow:0 0 0 10px rgba(108,76,245,.12)}
.sc-mic svg{width:40px;height:40px}.sc-mic.rec{background:#dc2626;animation:scp 1.2s infinite}@keyframes scp{50%{box-shadow:0 0 0 18px rgba(220,38,38,.15)}}
.sc-time{text-align:center;font:700 22px ui-monospace,monospace}.sc-live{min-height:90px;border:1px dashed var(--line);border-radius:14px;padding:12px 14px;margin:12px 0;color:var(--ink);background:var(--bg)}
.sc-live:empty::before{content:attr(data-ph);color:var(--mu);font-style:italic;pointer-events:none}.sc-metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:12px 0}.sc-metrics div{background:var(--surface-2);border:1px solid var(--line);border-radius:14px;padding:10px 12px;text-align:center}
.sc-metrics b{display:block;font-size:22px}.sc-metrics small{color:var(--mu);font-size:12.5px}
.sc-target{font-size:20px;line-height:1.7}.sc-target .ok{background:#DCFCE7;color:#166534;border-radius:6px;padding:0 3px}.sc-target .miss{background:#FEE2E2;color:#991B1B;border-radius:6px;padding:0 3px;text-decoration:underline wavy}
.sc-center{text-align:center}
@media (max-width:860px){.ai-wrap,.ai-grid2{grid-template-columns:1fr}.ai-side{position:static}.ai-log{max-height:none}.ai-chat{min-height:0}.ai-doc{padding:18px}}
</style>"""

FEATURES = [
    ("ai-academy.html", 1, "AI Skills Academy", "Every AI skills course in one place: the 7 core skills plus AI strategy, AI UX, pricing, ML products, governance, platforms, product ops and multimodal AI.",
     ["14 courses, basic to advanced", "Lessons + PDFs + interactive versions", "In the PM and GenAI programs"], "Open the academy"),
    ("ai-skills-map.html", 2, "AI Skills Map", "Every AI skill in one map: what to learn first, the full catalogue of AI capabilities, and where to learn each on SkillNavora, plus what employers ask for.",
     ["7-skill learning order", "Every capability mapped to lessons", "Job-description skills by role"], "Open the map"),
    ("ai-tutor.html", 3, "AI Tutor", "Your 24×7 study buddy. Ask anything about product management, Excel, SQL, Python, Power BI, Tableau, ML, GenAI, agents, careers or English.",
     ["Explains with examples and code", "Links you to the right SkillNavora lesson", "Hindi / Hinglish supported"], "Ask a question"),
    ("prd-writer.html", 4, "AI PRD / BRD / FRD Writer", "Describe a product idea or business project and get a complete PRD, BRD or FRD in a minute, framed the way top companies write them.",
     ["PRD for product managers", "BRD and FRD for business analysts", "Revise by asking; download Word, Markdown or PDF"], "Write a document"),
    ("pm-toolkit.html", 5, "AI PM Toolkit", "Pick a PM capability, add your context, review the result: problem discovery, opportunity sizing, A/B test design, API planning, launch plans, metrics and more.",
     ["13 capabilities in one place", "Ready-to-use deliverables", "Refine by asking; download Word"], "Open the toolkit"),
    ("prd-library.html", 6, "PRD library: 120 ideas", "Learn to frame PRDs from the best: a section-by-section template, examples, common mistakes and 120 product ideas across 15 industries.",
     ["Write any idea with AI in one click", "Best guides, templates and apps", "Free Word template"], "Open the PRD library"),
    ("brd-frd.html", 7, "BRD & FRD guide", "For business analysts: BRD vs FRD vs PRD, templates, BA techniques and 25 real project ideas from banking to GenAI.",
     ["BRD and FRD templates", "25 project ideas with requirements", "Best BA guides and apps"], "Open the BRD & FRD guide"),
    ("speaking-coach.html", 8, "AI Speaking Coach", "Speak into your mic and get instant coaching on English, public speaking and interview answers, like a personal coach.",
     ["Fluency, grammar and pace scores", "Filler words and pauses counted", "Pronunciation drills with listen-and-repeat"], "Start speaking"),
    ("practice.html", 9, "AI mock interview", "Get a real PM, data or GenAI interview question, answer it against the clock and get a score with a model answer.",
     ["Score out of 10", "Gaps and a model answer", "Likely follow-up questions"], "Practise an interview"),
    ("web-automation.html", 10, "Web Automation & Playwright MCP", "Webhooks, triggers, browser automation with Playwright, the Playwright MCP for Claude, and every major platform: Selenium, Puppeteer, Browser Use, Stagehand, Apify, n8n, Zapier, Make.",
     ["10 classes + PDF", "Secure webhook receivers", "Let Claude use a real browser"], "Open the course"),
    ("ai-builder-tools.html", 11, "AI Builder Tools how-to", "What Claude, Claude Code, ChatGPT and Codex, Gemini and Lovable can do and how: create a website, add pages, connect tools and other websites.",
     ["10 classes + PDF", "Website to custom domain", "Connect Zapier, n8n, webhooks"], "Open the course"),
    ("ai-engineer.html", 12, "AI Engineer path", "Everything an AI engineer goes through: foundations, LLM engineering, RAG, agents and MCP, fine-tuning, evals, LLMOps, security, system design, roadmap and interviews.",
     ["12 classes + PDF", "12-month roadmap, 10 projects", "Under Resources, Other programs"], "Open the path"),
    ("study-library.html", 13, "Study Library", "Every program, handbook, lesson, course, practice set, tool and PDF in one page with 11 tabs and a filter. Pair it with the 4-tab Study Hub.",
     ["11 tabs, one filter", "All 129 lessons + every course", "Free with your details"], "Open the library"),
    ("study-hub.html", 0, "Study Hub (4 tabs)", "AI Product Management, AI for Data Engineers, AI Engineer and GenAI Launchpad: curriculum, lessons, classes, practice and PDFs per path.",
     ["4 program tabs", "Every class one click away", "Netlify front page"], "Open the hub")
]

def ico(i):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{AI_NAV[i][3]}</svg>'

def hub():
    cards = "".join(f'''<a class="ai-card" href="{p}"><span class="ic">{ico(i)}</span><span class="ai-badge">Free</span><h3>{E(n)}</h3><p>{E(d)}</p><ul>{"".join(f"<li>{E(x)}</li>" for x in L)}</ul><span class="go">{E(c)} →</span></a>'''
                    for p, i, n, d, L, c in FEATURES)
    more = '''<a class="ai-card" href="lab.html"><span class="ai-badge">Practice</span><h3>Practice Lab</h3><p>Run real SQL, Excel formulas and Python in your browser, spot the trap and see the fix.</p><span class="go">Open the lab →</span></a>
<a class="ai-card" href="questions.html"><span class="ai-badge">Interview prep</span><h3>Top 100 interview questions</h3><p>Model answers for PM, Data & AI and GenAI, each linked to the lesson that teaches it.</p><span class="go">See questions →</span></a>
<a class="ai-card" href="handbooks/index.html"><span class="ai-badge">Handbooks</span><h3>Handbooks & PDFs</h3><p>PM Master Handbook, Data Science & AI handbook and GenAI Launchpad, free with your details.</p><span class="go">Open handbooks →</span></a>'''
    return CSS + f'''<section style="padding-top:36px"><div class="wrap">
<h2 class="sec-h" style="font-size:28px">Your AI learning assistants</h2><p class="sub">Everything runs right here on SkillNavora. No other AI app or account needed.</p>
<div class="ai-cards">{cards}</div></div></section>
<section style="padding-top:8px"><div class="wrap"><h2 class="sec-h" style="font-size:24px">How it works</h2>
<div class="ai-steps"><div><b>Pick a tool</b>Tutor for questions, PRD Writer for documents, Speaking Coach for English and interviews.</div><div><b>Share your details once</b>After two free tries, tell us your name and email to unlock everything, like our handbooks.</div><div><b>Learn by doing</b>Ask follow-ups, revise, re-record. Your work stays on your device.</div><div><b>Go deeper</b>Each answer links to the SkillNavora lesson, test or live class that teaches it.</div></div>
<p class="ai-note">AI can make mistakes; check important facts. Don't share passwords, financial or private company data. Answers come from leading AI models (Google Gemini, Llama via Groq or Cloudflare, Anthropic Claude or OpenAI ChatGPT) through SkillNavora's secure server, and every answer has buttons to continue in your favourite AI app. <a href="privacy.html">Privacy policy</a>.</p></div></section>
<section style="padding-top:8px"><div class="wrap"><h2 class="sec-h" style="font-size:24px">More free ways to practise</h2><div class="ai-cards">{more}</div></div></section>'''

TUTOR_SUG = {
    "All": ["Explain the difference between a PM and a project manager", "What is RAG in GenAI, in simple words?", "Write a SQL query to find the top 3 customers by revenue", "How do I prepare for a product sense interview?"],
    "Product management": ["How do I prioritise a backlog with RICE?", "What metrics would you track for Swiggy Instamart?", "How do I write good user stories?", "Explain North Star metric with an example"],
    "Data & AI": ["VLOOKUP vs XLOOKUP vs INDEX-MATCH", "Explain SQL window functions with an example", "What is overfitting and how do I prevent it?", "When should I use Power BI vs Tableau?"],
    "GenAI & agents": ["What is an AI agent and how is it different from a chatbot?", "Explain MCP (Model Context Protocol) simply", "How do I evaluate an LLM feature?", "Write a good prompt for summarising customer reviews"],
    "English & speaking": ["How can I stop saying 'um' when I speak?", "Correct my sentence: I am having 5 years experience in sales", "Give me 5 phrases to disagree politely in a meeting", "How do I introduce myself in an interview?"],
    "Careers": ["How do I switch from engineering to product management?", "What projects should I add to a data analyst resume?", "How do I answer 'Why should we hire you?'", "Make me a 30-day plan to learn SQL"],
}

def tutor():
    tabs = "".join(f'<button type="button" data-topic="{E(k)}" aria-pressed="{str(i == 0).lower()}">{E(k)}</button>' for i, k in enumerate(TUTOR_SUG))
    return CSS + f'''<section style="padding-top:24px"><div class="wrap ai-wrap" data-ai="tutor">
<aside class="ai-side"><div class="card"><h3>Topic</h3><div class="ai-chips" id="tu-topics">{tabs}</div></div>
<div class="card"><h3>Try asking</h3><div class="ai-chips" id="tu-sug"></div></div>
<div class="card"><h3>Tips</h3><p class="ai-note" style="margin:0">Ask follow-ups like "give an example", "explain in Hindi" or "quiz me on this". <a href="ai.html">More AI tools →</a></p></div></aside>
<div class="ai-chat"><div class="ai-log ai-out" id="tu-log" aria-live="polite"></div>
<form class="ai-form" id="tu-form"><textarea id="tu-in" maxlength="6000" placeholder="Ask any study or career question…" aria-label="Your question"></textarea><div style="display:flex;flex-direction:column;gap:6px"><button class="btn btn-primary btn-sm" type="submit">Ask</button><button class="btn btn-line btn-sm" type="button" id="tu-new">New chat</button></div></form></div>
<script type="application/json" id="tu-data">{json.dumps(TUTOR_SUG)}</script></div></section>'''

PRD_EX = [
    {"name": "SplitKaro", "type": "Consumer mobile app", "idea": "A UPI-based app for college students to split hostel, food and trip expenses and settle up in one tap.", "users": "College students in India, 18–24, living in hostels or shared flats", "problem": "Groups track shared spends on WhatsApp and Excel; people forget who owes what and settling is awkward.", "goals": "Reach 50,000 monthly active users in 6 months; 60% of groups settle within 7 days", "constraints": "Must work on low-end Android phones; follow NPCI/UPI and DPDP rules"},
    {"name": "AI Support Copilot", "type": "AI / GenAI feature", "idea": "An AI assistant inside our customer-support tool that drafts replies to tickets using our help-centre articles and past tickets.", "users": "Support agents at a B2B SaaS company handling 5,000 tickets a day", "problem": "Agents spend 6 minutes per ticket searching docs; answers are inconsistent", "goals": "Cut average handling time by 30% with CSAT not dropping", "constraints": "No customer PII sent to third parties without masking; agents approve every reply"},
    {"name": "KiranaPay Credit", "type": "B2B / fintech", "idea": "Buy-now-pay-later for small kirana shops to buy stock from distributors, repaid daily from UPI collections.", "users": "Kirana shop owners in tier-2 and tier-3 cities and their distributors", "problem": "Shops run out of working capital and lose sales; distributors take credit risk informally", "goals": "₹50 crore disbursed in year 1 with under 2% defaults", "constraints": "RBI digital lending guidelines; NBFC partner; Hindi and regional language support"},
]

def prd():
    types = ["Consumer mobile app", "Web product / SaaS", "AI / GenAI feature", "B2B / fintech", "Marketplace", "Internal tool", "Feature in an existing product"]
    opts = "".join(f"<option>{E(t)}</option>" for t in types)
    ex = "".join(f'<button type="button" data-ex="{i}">{E(e["name"])}</button>' for i, e in enumerate(PRD_EX))
    return CSS + f'''<section style="padding-top:24px"><div class="wrap ai-grid2" data-ai="prd">
<div class="card"><form class="ai-f" id="prd-form">
<div><b style="font-size:14px">Document</b><div class="ai-chips" id="prd-doc" style="margin-top:6px"><button type="button" data-doc="prd" aria-pressed="true">PRD · product</button><button type="button" data-doc="brd" aria-pressed="false">BRD · business</button><button type="button" data-doc="frd" aria-pressed="false">FRD · functional</button></div><p class="ai-note" id="prd-docnote">Product Requirements Document: for product managers. <a href="prd-library.html">PRD library</a></p></div>
<div><b style="font-size:14px">Fill an example</b><div class="ai-chips" id="prd-ex" style="margin-top:6px">{ex}</div></div>
<label><span data-l="name">Product or feature name</span><input name="name" maxlength="80" placeholder="e.g. SplitKaro"></label>
<label>Type<select name="type">{opts}</select></label>
<label><span data-l="idea">Your idea</span> <span class="ai-note" style="margin:0">(required)</span><textarea name="idea" maxlength="2000" required placeholder="What are you building, in 1–3 sentences?"></textarea></label>
<label><span data-l="users">Target users</span><input name="users" maxlength="300" placeholder="Who is it for?"></label>
<label>Problem<textarea name="problem" maxlength="1500" placeholder="What pain does it solve? Any data or evidence?"></textarea></label>
<label>Goals<input name="goals" maxlength="400" placeholder="e.g. 10k users in 3 months, 20% conversion"></label>
<label>Constraints<input name="constraints" maxlength="400" placeholder="Budget, timeline, tech, regulations"></label>
<label>Detail level<select name="depth"><option value="standard">Standard (2–3 pages)</option><option value="detailed">Detailed (interview / real project)</option><option value="one-pager">One-pager</option></select></label>
<button class="btn btn-primary" type="submit" id="prd-go">✨ Write my PRD</button>
<p class="ai-note">Tip: you can edit the result by asking for changes below it. Learn how to write PRDs yourself in the <a href="handbooks/pm/index.html">PM Handbook</a>.</p></form></div>
<div><div class="ai-acts" id="prd-acts" hidden><button class="btn btn-line btn-sm" type="button" data-act="copy">Copy</button><button class="btn btn-line btn-sm" type="button" data-act="doc">Download Word</button><button class="btn btn-line btn-sm" type="button" data-act="md">Download Markdown</button><button class="btn btn-line btn-sm" type="button" data-act="print">Print / Save PDF</button></div>
<div class="ai-doc ai-out" id="prd-out"><div class="ai-empty"><b>Your document will appear here</b>Choose PRD, BRD or FRD, fill in your idea (or pick an example) and press Write.</div></div>
<form class="ai-form" id="prd-rev" hidden style="border:1px solid var(--line);border-radius:16px;margin-top:12px;background:var(--surface)"><textarea id="prd-rin" maxlength="2000" placeholder="Ask for a change, e.g. 'Add a pricing section' or 'Make the metrics more specific'"></textarea><button class="btn btn-primary btn-sm" type="submit">Update</button></form>
</div></div></section>'''

SPEAK = {
    "intro": {"name": "Tell me about yourself", "small": "Interview opener", "q": ["Tell me about yourself.", "Walk me through your resume.", "Why do you want to switch careers?", "What are your strengths and weaknesses?"]},
    "english": {"name": "Daily English", "small": "Speak for 1 minute", "q": ["Describe your favourite city in India and why you like it.", "Talk about a book, film or series that changed how you think.", "What did you do last weekend?", "Describe a challenge you faced at work or college and how you solved it.", "Should students learn AI in school? Give your opinion.", "Describe your ideal job."]},
    "hr": {"name": "HR interview", "small": "Behavioural, STAR", "q": ["Tell me about a time you handled a conflict in a team.", "Describe a failure and what you learned from it.", "Why should we hire you?", "Where do you see yourself in five years?", "Tell me about a time you led without authority."]},
    "pm": {"name": "PM interview", "small": "Product sense, metrics", "q": ["How would you improve Google Maps for auto-rickshaw drivers?", "Swiggy orders dropped 10% last week. How would you investigate?", "What is your favourite product and why?", "Design an app to help senior citizens pay bills.", "How would you measure success for WhatsApp Channels?"]},
    "data": {"name": "Data / AI interview", "small": "Explain technical ideas", "q": ["Explain a JOIN to a non-technical manager.", "Walk me through a data project you are proud of.", "How would you explain overfitting to a business stakeholder?", "What is RAG and when would you use it?"]},
    "present": {"name": "Presentation", "small": "1–2 minute talk", "q": ["Pitch your product idea to an investor in 60 seconds.", "Give a 1-minute status update to your leadership team.", "Present one insight from data and the decision you recommend.", "Introduce yourself to a new team in a meeting."]},
    "free": {"name": "Free speech", "small": "Any topic you choose", "q": ["Speak about any topic you like for 1–2 minutes. Type your topic below (optional), then tap the mic.", "Free speech: talk about something you know well — your job, a hobby, a book, a film or your city.", "Free speech: explain an idea you care about as if teaching a friend."]},
    "shadow": {"name": "Shadowing", "small": "Listen, then repeat", "q": ["Thank you for the opportunity. I'm really excited about this role.", "Could you please share the agenda before the meeting?", "In my last project, I led a team of five and delivered the launch two weeks early.", "I'd like to clarify the requirements before we start.", "Let me walk you through the key numbers from last quarter.", "That's a great question. Let me think about it for a moment.", "I disagree slightly, and here's why: the data shows a different trend.", "We reduced customer complaints by thirty percent in three months.", "Would it be possible to reschedule our call to Thursday afternoon?", "I'm a quick learner, and I enjoy solving problems with data."]},
    "engint": {"name": "English interview", "small": "Common interview questions", "q": ["Introduce yourself in one minute.", "What are your greatest strengths?", "Tell me about a weakness and how you're improving it.", "Why do you want to work for our company?", "Describe your current role and responsibilities.", "Tell me about a challenge you faced and how you handled it.", "How do you handle pressure and tight deadlines?", "Describe a time you worked in a team to achieve a goal.", "What do you do to keep learning new skills?", "Why are you looking for a change?", "Where do you see yourself in three years?", "Do you have any questions for us?"]},
    "drill": {"name": "Pronunciation drill", "small": "Listen and repeat", "q": ["We will review the very valuable video on Wednesday.", "I think these three things are worth thinking through together.", "The development of the product depends on data analysis.", "Please send the schedule for the vegetable delivery by evening.", "Our company's revenue grew faster than we expected this quarter.", "I would like to develop a comfortable, reliable environment."]},
}

def speaking():
    modes = "".join(f'<button type="button" data-mode="{k}" aria-pressed="{str(k == "intro").lower()}">{E(v["name"])}<small>{E(v["small"])}</small></button>' for k, v in SPEAK.items())
    return CSS + f'''<section style="padding-top:24px"><div class="wrap" data-ai="speak">
<div class="sc-modes" id="sc-modes">{modes}</div>
<div class="ai-grid2"><div class="card">
<div class="kicker" id="sc-kicker">Your question</div><p class="sc-q" id="sc-q"></p><div class="sc-target" id="sc-target" hidden></div><label id="sc-topicw" hidden style="display:flex;flex-direction:column;gap:4px;font-weight:600;font-size:14px;margin:4px 0 10px">Your topic (optional)<input id="sc-topic" maxlength="120" placeholder="e.g. Why I love cricket, My dream job, AI in education" style="border:1px solid var(--line);border-radius:10px;padding:9px 12px;font:inherit;background:var(--bg);color:var(--ink)"></label>
<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn btn-line btn-sm" type="button" id="sc-next">New question ↻</button><button class="btn btn-line btn-sm" type="button" id="sc-listen">🔊 Listen</button>
<select id="sc-lang" aria-label="Accent" style="border:1px solid var(--line);border-radius:10px;padding:6px 10px;background:var(--surface);color:var(--ink)"><option value="en-IN">English (India)</option><option value="en-US">English (US)</option><option value="en-GB">English (UK)</option></select></div>
<div class="sc-center"><button class="sc-mic" id="sc-mic" type="button" aria-label="Start speaking"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/></svg></button>
<div class="sc-time" id="sc-time">00:00</div><p class="ai-note" id="sc-status">Tap the mic and answer out loud. Tap again to stop.</p></div>
<div class="sc-live" id="sc-live" contenteditable="true" role="textbox" aria-multiline="true" data-ph="Your words will appear here as you speak. No mic? Type your answer here instead." aria-label="Your answer (transcript, you can edit or type)"></div>
<div class="sc-metrics" id="sc-metrics" hidden></div>
<button class="btn btn-primary" type="button" id="sc-go" style="width:100%">Get AI feedback</button>
<p class="ai-note">Speech recognition runs in your browser (best in Chrome or Edge). Audio is not recorded or stored; only the text is sent for feedback.</p></div>
<div><div class="ai-acts" id="sc-acts" hidden><button class="btn btn-line btn-sm" type="button" id="sc-say">🔊 Hear the better version</button><button class="btn btn-line btn-sm" type="button" id="sc-again">Try again</button></div>
<div class="ai-doc ai-out" id="sc-out"><div class="ai-empty"><b>Your coaching report will appear here</b>Scores for fluency, grammar, structure and delivery, the exact words to fix, a better version and your next drill.</div></div></div></div>
<section class="card" id="learn-english" style="margin-top:22px"><h2 style="margin:0 0 6px;font-size:22px">Learn and practise English speaking</h2>
<p class="ai-note" style="margin:0 0 12px">Practise a little every day: 10 minutes of shadowing, one free speech, and one interview answer, then read your AI feedback.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px">
<div><h3 style="font-size:16px;margin:0 0 6px">How to shadow (5 steps)</h3><ol style="margin:0;padding-left:18px;color:var(--mu)"><li>Pick a short clip (BBC Learning English, TED, a news anchor).</li><li>Listen once without reading.</li><li>Listen again with the transcript; mark stress and pauses.</li><li>Play 1 sentence, pause, repeat it out loud copying rhythm and intonation.</li><li>Record yourself here in <b>Shadowing</b> mode and compare.</li></ol></div>
<div><h3 style="font-size:16px;margin:0 0 6px">Daily 15-minute plan</h3><ul style="margin:0;padding-left:18px;color:var(--mu)"><li>5 min shadowing (Shadowing mode)</li><li>5 min free speech on any topic (Free speech mode)</li><li>5 min one interview answer (English interview mode) and fix the 3 suggestions</li></ul></div>
<div><h3 style="font-size:16px;margin:0 0 6px">Free videos and websites</h3><ul style="margin:0;padding-left:18px">
<li><a href="https://www.bbc.co.uk/learningenglish/" target="_blank" rel="noopener">BBC Learning English</a> · <a href="https://www.youtube.com/@bbclearningenglish" target="_blank" rel="noopener">YouTube</a></li>
<li><a href="https://www.youtube.com/@rachelsenglish" target="_blank" rel="noopener">Rachel's English</a>: pronunciation and shadowing</li>
<li><a href="https://www.youtube.com/@EnglishwithLucy" target="_blank" rel="noopener">English with Lucy</a>: vocabulary and speaking</li>
<li><a href="https://learningenglish.voanews.com/" target="_blank" rel="noopener">VOA Learning English</a>: slow news with transcripts</li>
<li><a href="https://www.ted.com/talks" target="_blank" rel="noopener">TED Talks</a>: transcripts for shadowing</li>
<li><a href="https://www.cambridgeenglish.org/learning-english/" target="_blank" rel="noopener">Cambridge English</a>: free practice</li>
<li><a href="https://www.toastmasters.org/" target="_blank" rel="noopener">Toastmasters</a>: speaking clubs in India</li></ul></div></div>
<p class="ai-note" style="margin:12px 0 0">Full guide: <a href="guides/public-speaking.html">Public Speaking complete guide</a> · <a href="questions.html">Top interview questions</a></p></section>
<script type="application/json" id="sc-data">{json.dumps(SPEAK)}</script></div></section>'''

def write_index(out):
    """assets/ai-index.txt: one line per lesson or page, for the AI Tutor's Learn-more links."""
    L = []
    cat = json.load(open(os.path.join(out, "data-science/catalog.json")))
    for t in cat["tracks"]:
        L.append(f"## {t['name']}: {t['desc']}")
        for x in t["lessons"]:
            L.append(f"{x['title']} | /data-science/{x['page']} | {t['name']}")
    L.append("## Product Management Master Handbook")
    pm = os.path.join(out, "handbooks/pm")
    for f in sorted(os.listdir(pm)):
        if not f.endswith(".html"): continue
        m = re.search(r"<title>([^<·]+)", open(os.path.join(pm, f), encoding="utf-8").read())
        if m: L.append(f"{m.group(1).strip()} | /handbooks/pm/{f} | Product management")
    L += ["## Practice and other pages",
          "Practice Lab (run SQL, Excel, Python; PM and GenAI scenarios) | /lab.html | practice",
          "Practice tests by topic | /tests.html | practice",
          "Top 100 interview questions: PM, Data & AI, GenAI | /questions.html | interview",
          "AI mock interview with feedback | /practice.html | interview",
          "AI Speaking Coach (English, public speaking, interviews) | /speaking-coach.html | speaking",
          "AI Engineer: the complete path: role, foundations, ML, LLM engineering, RAG, agents, fine-tuning, evals, LLMOps, security, system design, roadmap, projects, interviews (12 classes + PDF) | /ai-engineer.html | AI engineer, career",
          "Web Automation: webhooks (signatures, idempotency), triggers (cron, events, polling), Playwright, Playwright MCP with Claude, Selenium, Puppeteer, Cypress, Browser Use, Stagehand, Skyvern, Browserbase, Apify, n8n, Zapier, Make, Pipedream, RPA (10 classes + PDF) | /web-automation.html | PM, GenAI, automation",
          "AI Builder Tools: Claude, Claude Code, ChatGPT & Codex, Gemini, Lovable: create websites, pages, connect tools and other websites, publish on a domain (10 classes + PDF) | /ai-builder-tools.html | PM, GenAI, tools",
          "Study Library: all study material in one page (11 tabs) | /study-library.html | all programs",
          "Study Hub: AI PM, AI for Data Engineers, AI Engineer, GenAI Launchpad in one page with four tabs | /study-hub.html | all programs",
          "AI Skills Academy: all AI skills courses in one place | /ai-academy.html | PM, GenAI",
          "AI Product Strategy (moats, flywheels, build vs buy) | /ai-product-strategy.html | PM",
          "Designing AI Experiences (AI UX) | /ai-ux-design.html | PM, design",
          "Pricing & Monetising AI Products | /ai-pricing.html | PM",
          "Machine Learning Products for PMs | /ml-products.html | PM, data",
          "AI Governance & Responsible AI (EU AI Act, DPDP) | /ai-governance.html | PM, GenAI",
          "Platform & API Product Management | /platform-api-pm.html | PM",
          "Product Operations | /product-ops.html | PM",
          "Multimodal AI & AI Media (images, voice, video) | /multimodal-ai.html | PM, GenAI",
          "Speaking Coach modes: free speech, shadowing, English interview | /speaking-coach.html | English, speaking",
          "AI Skills Map: full catalogue of AI skills mapped to SkillNavora lessons, 7-skill learning order, job-description skills | /ai-skills-map.html | all programs",
          "Prompt & Context Engineering: evidence-based requests, structured outputs, task decomposition, context compression, documents and OCR, attribution, knowledge graphs (8 classes + PDF) | /context-engineering.html | PM, GenAI",
          "AI Skills & Templates: Agent Skills, Projects, Custom GPTs, Gems, PM skill library, testing skills, case study to PRD to presentation project (8 classes + PDF) | /ai-skills.html | PM, GenAI",
          "Agent Orchestration & Monitoring: workflows vs agents, routing, parallel, orchestrator-workers, state, approvals, multi-agent, cost, monitoring (8 classes + PDF) | /agent-orchestration.html | PM, GenAI",
          "Browser Automation & AI Agents: scripts vs RPA vs AI agents, Playwright, computer use, deep research agents, workflows, safety, evals (8 classes + PDF) | /browser-automation.html | PM, GenAI",
          "Your AI Second Brain: PARA, CODE, NotebookLM, Notion, Obsidian, context engineering, AI memory, MCP (8 classes + PDF) | /ai-second-brain.html | PM, GenAI, productivity",
          "AI Evals for Product Managers: what evals are, rubrics, golden datasets, LLM-as-judge, error analysis, RAG and agent evals, safety, A/B tests, monitoring (10 classes + PDF) | /ai-evals.html | product management, AI",
          "AI PM Toolkit: problem discovery, opportunity sizing, A/B test design, API planning, launch, metrics, research, competitive analysis, user stories, roadmap, RCA, stakeholder update | /pm-toolkit.html | product management",
          "AI PRD / BRD / FRD Writer | /prd-writer.html | product management, business analysis",
          "PRD library: template, framing guide, 120 PRD ideas, best guides and apps | /prd-library.html | product management",
          "BRD & FRD guide for business analysts: templates, BA techniques, 25 project ideas | /brd-frd.html | business analysis",
          "Tool tutorials: Figma, n8n, Make, Zapier, Replit, Claude Code | /tools.html | tools",
          "Handbooks and PDFs hub | /handbooks/index.html | handbooks",
          "Resources & AI tools (links, newsletters, job portals) | /resources.html | resources",
          "Programs: AI Product Management, AI for Data Engineers, GenAI Launchpad | /programs.html | programs",
          "Free counselling call / contact | /contact.html | contact"]
    open(os.path.join(out, "assets/ai-index.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return len(L)

# ------------------------------------------------------------------ AI PM Toolkit
# (id, name, one-line, svg path, [(field, label, placeholder)], example values)
PM_TOOLS = [
    ("discovery", "Customer problem discovery", "Frame the real customer problem before building.", '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
     [("product", "Product or area", "e.g. Grocery delivery app for tier-2 cities"), ("signal", "What you've noticed", "Complaints, data, a hunch…"), ("users", "Who you think is affected", "e.g. Working parents ordering weekly")],
     {"product": "Grocery delivery app in tier-2 cities", "signal": "Repeat orders dropped 12% in 2 months; reviews mention 'items missing' and 'late delivery'", "users": "Families doing weekly grocery orders"}),
    ("prd", "PRD and specification writing", "Draft a complete product requirements document.", '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>', [], {}),
    ("sizing", "Opportunity sizing and prioritization", "Estimate the market and rank opportunities.", '<path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/>',
     [("product", "Opportunity", "e.g. Pet-care subscription in Indian metros"), ("market", "Market facts you know", "Population, price, adoption…"), ("options", "Options to prioritise (optional)", "One per line")],
     {"product": "Monthly pet-food and vet-care subscription in Indian metros", "market": "About 3 crore pet dogs in India; ~40% in metros; average spend ₹2,500/month", "options": "Pet food subscription\nVet teleconsults\nGrooming at home\nPet insurance"}),
    ("experiment", "Hypothesis and experiment design", "Design a measurable A/B test.", '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
     [("change", "Change you want to test", "e.g. Show delivery time on the home screen"), ("metric", "Metric and current baseline", "e.g. Checkout conversion 3.2%"), ("traffic", "Traffic per day", "e.g. 40,000 users/day")],
     {"change": "Show the estimated delivery time on product cards", "metric": "Checkout conversion 3.2%", "traffic": "40,000 visitors per day"}),
    ("api", "API design and integration planning", "Plan a robust API integration.", '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
     [("goal", "What needs to integrate", "e.g. Our app with a payment gateway"), ("systems", "Systems involved", "e.g. Mobile app, backend, Razorpay"), ("needs", "Key needs", "Refunds, webhooks, retries…")],
     {"goal": "Accept UPI and card payments in our food-ordering app with refunds", "systems": "Android/iOS app, Node.js backend, payment gateway, order service", "needs": "Webhooks for payment status, partial refunds, idempotent retries"}),
    ("launch", "Launch and channel planning", "Plan a measurable product launch.", '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/>',
     [("product", "What you're launching", "e.g. Credit-score coach feature"), ("audience", "Target audience", "e.g. First-time borrowers, 21–30"), ("budget", "Budget and date", "e.g. ₹10 lakh, launch 15 Jan")],
     {"product": "Credit-score coach inside a fintech app", "audience": "First-time borrowers aged 21–30 in metros", "budget": "₹10 lakh, launch in 6 weeks"}),
    ("metrics", "Metrics and North Star", "Define the North Star, inputs and guardrails.", '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
     [("product", "Product", "e.g. Language-learning app"), ("model", "Business model", "e.g. Freemium subscription"), ("stage", "Stage", "e.g. 6 months after launch, 50k users")],
     {"product": "Spoken English learning app", "model": "Freemium with ₹299/month subscription", "stage": "8 months after launch, 60,000 monthly users"}),
    ("research", "User research plan", "Plan interviews, screeners and surveys.", '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
     [("question", "What you want to learn", "e.g. Why trial users don't convert"), ("users", "Who to talk to", "e.g. Trial users from the last 30 days"), ("time", "Time and budget", "e.g. 2 weeks, ₹20,000")],
     {"question": "Why do free-trial users of our HR app not convert to paid?", "users": "HR managers at 20–200 person companies who started a trial in the last 30 days", "time": "2 weeks, ₹20,000 for incentives"}),
    ("competitive", "Competitive analysis", "Map competitors and find your edge.", '<path d="M18 20V10M12 20V4M6 20v-6"/>',
     [("product", "Your product", "e.g. Online spoken-English coaching"), ("competitors", "Competitors you know", "Names, one per line"), ("segment", "Your target segment", "e.g. Job seekers in tier-2 cities")],
     {"product": "AI spoken-English coaching app", "competitors": "ELSA Speak\nDuolingo\nCambly\nLocal coaching centres", "segment": "Job seekers aged 20–28 in tier-2 Indian cities"}),
    ("stories", "User stories and acceptance criteria", "Break a feature into testable stories.", '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
     [("feature", "Feature", "e.g. Save cart and resume on another device"), ("users", "Users", "e.g. Logged-in shoppers"), ("rules", "Rules or limits", "Anything the team must respect")],
     {"feature": "Split a restaurant bill with friends in the app", "users": "Diners paying with UPI", "rules": "Max 10 people; payer gets reminders; works if a friend has no app"}),
    ("roadmap", "Roadmap and strategy", "Turn goals into a Now / Next / Later roadmap.", '<path d="M3 6h18M3 12h12M3 18h6"/>',
     [("product", "Product", "e.g. B2B invoicing SaaS"), ("goals", "Company goals this year", "e.g. 2x revenue, enter SMB segment"), ("ideas", "Ideas on the table", "One per line")],
     {"product": "Invoicing and payments SaaS for Indian SMEs", "goals": "Double ARR; cut churn from 4% to 2.5% monthly", "ideas": "WhatsApp payment reminders\nGST e-invoicing\nMobile app\nAccountant multi-client view\nBank reconciliation"}),
    ("rca", "Metric drop root-cause analysis", "Investigate why a key metric fell.", '<path d="M22 17l-8.5-8.5-5 5L2 7"/><path d="M16 17h6v-6"/>',
     [("metric", "Which metric dropped, by how much", "e.g. Daily orders -15% week on week"), ("product", "Product context", "e.g. Food delivery app, 6 cities"), ("changes", "Recent changes you know of", "Releases, pricing, campaigns…")],
     {"metric": "Daily active users fell 15% week on week", "product": "Food delivery app in 6 cities", "changes": "New app version released Monday; delivery fee raised by ₹10 in 2 cities"}),
    ("update", "Stakeholder update", "Write a crisp leadership update.", '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
     [("project", "Project", "e.g. Checkout revamp"), ("status", "What happened since last update", "Progress, metrics, blockers"), ("ask", "What you need", "Decision, budget, help")],
     {"project": "Checkout revamp", "status": "Design done, 60% built; payment-failure rate down from 4% to 2.6% in beta; QA is 1 week behind", "ask": "Approve 1 extra QA engineer for 3 weeks"}),
]

def pm_toolkit():
    cards = "".join(f'''<article class="ai-card pt-card" data-cap="{c}"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ic}</svg></span><h3>{E(n)}</h3><p>{E(d)}</p>
<span style="display:flex;justify-content:space-between;gap:8px;margin-top:auto;padding-top:8px">{'<a class="go" href="prd-writer.html">Use capability →</a><a class="go" style="color:var(--mu)" href="prd-library.html">Read more →</a>' if c == "prd" else '<button type="button" class="go pt-use" style="background:none;border:0;padding:0;cursor:pointer;font:inherit;font-weight:700">Use capability →</button>'}</span></article>'''
                    for c, n, d, ic, F, X in PM_TOOLS)
    data = {c: {"name": n, "desc": d, "fields": F, "ex": X} for c, n, d, ic, F, X in PM_TOOLS if c != "prd"}
    return CSS + f'''<style>.pt-steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0 0 26px}}.pt-steps div{{border:1px solid var(--line);border-radius:14px;padding:12px 14px;background:var(--surface);font-weight:700}}.pt-steps span{{font:700 12px ui-monospace,monospace;color:var(--brand);margin-right:8px}}.pt-steps div.on{{border-color:var(--brand);box-shadow:0 0 0 3px rgba(108,76,245,.15)}}
.pt-card{{cursor:pointer}}@media (max-width:640px){{.pt-steps{{grid-template-columns:1fr}}}}</style>
<section style="padding-top:28px"><div class="wrap" data-ai="pm">
<div class="pt-steps"><div id="pt-s1" class="on"><span>01</span>Pick a capability</div><div id="pt-s2"><span>02</span>Add your context</div><div id="pt-s3"><span>03</span>Review the result</div></div>
<div id="pt-pick"><h2 class="sec-h" style="font-size:26px">What do you need to do?</h2><p class="sub">{len(PM_TOOLS)} PM capabilities. Start with the work in front of you.</p><div class="ai-cards">{cards}</div></div>
<div id="pt-work" hidden><button class="btn btn-line btn-sm" type="button" id="pt-back">← All capabilities</button>
<div class="ai-grid2" style="margin-top:14px"><div class="card"><form class="ai-f" id="pt-form"><div><div class="kicker">Capability</div><h3 id="pt-name" style="margin:4px 0 2px;font-size:20px"></h3><p class="ai-note" id="pt-desc" style="margin:0"></p></div>
<button type="button" class="btn btn-line btn-sm" id="pt-ex" style="align-self:flex-start">Fill an example</button><div id="pt-fields" class="ai-f"></div>
<label>Anything else (optional)<textarea name="extra" maxlength="3000" placeholder="Data, constraints, links, what you've tried…"></textarea></label>
<button class="btn btn-primary" type="submit">✨ Run capability</button></form></div>
<div><div class="ai-acts" id="pt-acts" hidden><button class="btn btn-line btn-sm" type="button" data-act="copy">Copy</button><button class="btn btn-line btn-sm" type="button" data-act="doc">Download Word</button><button class="btn btn-line btn-sm" type="button" data-act="md">Download Markdown</button></div>
<div class="ai-doc ai-out" id="pt-out"><div class="ai-empty"><b>Your result will appear here</b>Add your context (or use the example) and press Run.</div></div>
<form class="ai-form" id="pt-rev" hidden style="border:1px solid var(--line);border-radius:16px;margin-top:12px;background:var(--surface)"><textarea id="pt-rin" maxlength="2000" placeholder="Refine it, e.g. 'Use ₹ and Indian market data' or 'Add a risks section'"></textarea><button class="btn btn-primary btn-sm" type="submit">Refine</button></form></div></div></div>
<script type="application/json" id="pt-data">{json.dumps(data)}</script></div></section>'''
