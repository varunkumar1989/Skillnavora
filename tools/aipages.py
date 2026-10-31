"""AI Studio pages: ai.html (hub), ai-tutor.html, prd-writer.html, speaking-coach.html,
plus assets/ai-index.txt (the course index the AI Tutor uses to link learners to lessons)."""
import html, json, os, re
E = html.escape

AI_NAV = [  # (path, name, small, svg path)
    ("ai.html", "AI Studio", "All AI tools in one place, free", '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/>'),
    ("ai-tutor.html", "AI Tutor", "Ask any study question, 24×7", '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.7A8.5 8.5 0 1 1 21 11.5z"/>'),
    ("prd-writer.html", "AI PRD Writer", "Turn an idea into a full PRD", '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>'),
    ("speaking-coach.html", "AI Speaking Coach", "English, public speaking, interviews", '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>'),
    ("practice.html", "AI mock interview", "Answer a question, get a score", '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'),
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
.sc-live i{color:var(--mu)}.sc-metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:12px 0}.sc-metrics div{background:var(--surface-2);border:1px solid var(--line);border-radius:14px;padding:10px 12px;text-align:center}
.sc-metrics b{display:block;font-size:22px}.sc-metrics small{color:var(--mu);font-size:12.5px}
.sc-target{font-size:20px;line-height:1.7}.sc-target .ok{background:#DCFCE7;color:#166534;border-radius:6px;padding:0 3px}.sc-target .miss{background:#FEE2E2;color:#991B1B;border-radius:6px;padding:0 3px;text-decoration:underline wavy}
.sc-center{text-align:center}
@media (max-width:860px){.ai-wrap,.ai-grid2{grid-template-columns:1fr}.ai-side{position:static}.ai-log{max-height:none}.ai-chat{min-height:0}.ai-doc{padding:18px}}
</style>"""

FEATURES = [
    ("ai-tutor.html", 1, "AI Tutor", "Your 24×7 study buddy. Ask anything about product management, Excel, SQL, Python, Power BI, Tableau, ML, GenAI, agents, careers or English.",
     ["Explains with examples and code", "Links you to the right SkillNavora lesson", "Hindi / Hinglish supported"], "Ask a question"),
    ("prd-writer.html", 2, "AI PRD Writer", "Describe a product idea and get a complete, interview-ready PRD in a minute: users, stories, requirements, metrics and launch plan.",
     ["10 standard PRD sections", "Revise any section by asking", "Download as Word, Markdown or PDF"], "Write a PRD"),
    ("speaking-coach.html", 3, "AI Speaking Coach", "Speak into your mic and get instant coaching on English, public speaking and interview answers, like a personal coach.",
     ["Fluency, grammar and pace scores", "Filler words and pauses counted", "Pronunciation drills with listen-and-repeat"], "Start speaking"),
    ("practice.html", 4, "AI mock interview", "Get a real PM, data or GenAI interview question, answer it against the clock and get a score with a model answer.",
     ["Score out of 10", "Gaps and a model answer", "Likely follow-up questions"], "Practise an interview"),
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
<p class="ai-note">AI can make mistakes; check important facts. Don't share passwords, financial or private company data. Answers are generated by Claude, an AI model by Anthropic, through SkillNavora's secure server. <a href="privacy.html">Privacy policy</a>.</p></div></section>
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
<div><b style="font-size:14px">Fill an example</b><div class="ai-chips" id="prd-ex" style="margin-top:6px">{ex}</div></div>
<label>Product or feature name<input name="name" maxlength="80" placeholder="e.g. SplitKaro"></label>
<label>Type<select name="type">{opts}</select></label>
<label>Your idea <span class="ai-note" style="margin:0">(required)</span><textarea name="idea" maxlength="2000" required placeholder="What are you building, in 1–3 sentences?"></textarea></label>
<label>Target users<input name="users" maxlength="300" placeholder="Who is it for?"></label>
<label>Problem<textarea name="problem" maxlength="1500" placeholder="What pain does it solve? Any data or evidence?"></textarea></label>
<label>Goals<input name="goals" maxlength="400" placeholder="e.g. 10k users in 3 months, 20% conversion"></label>
<label>Constraints<input name="constraints" maxlength="400" placeholder="Budget, timeline, tech, regulations"></label>
<label>Detail level<select name="depth"><option value="standard">Standard (2–3 pages)</option><option value="detailed">Detailed (interview / real project)</option><option value="one-pager">One-pager</option></select></label>
<button class="btn btn-primary" type="submit">✨ Write my PRD</button>
<p class="ai-note">Tip: you can edit the result by asking for changes below it. Learn how to write PRDs yourself in the <a href="handbooks/pm/index.html">PM Handbook</a>.</p></form></div>
<div><div class="ai-acts" id="prd-acts" hidden><button class="btn btn-line btn-sm" type="button" data-act="copy">Copy</button><button class="btn btn-line btn-sm" type="button" data-act="doc">Download Word</button><button class="btn btn-line btn-sm" type="button" data-act="md">Download Markdown</button><button class="btn btn-line btn-sm" type="button" data-act="print">Print / Save PDF</button></div>
<div class="ai-doc ai-out" id="prd-out"><div class="ai-empty"><b>Your PRD will appear here</b>Fill in your idea (or pick an example) and press "Write my PRD".</div></div>
<form class="ai-form" id="prd-rev" hidden style="border:1px solid var(--line);border-radius:16px;margin-top:12px;background:var(--surface)"><textarea id="prd-rin" maxlength="2000" placeholder="Ask for a change, e.g. 'Add a pricing section' or 'Make the metrics more specific'"></textarea><button class="btn btn-primary btn-sm" type="submit">Update PRD</button></form>
</div></div></section>'''

SPEAK = {
    "intro": {"name": "Tell me about yourself", "small": "Interview opener", "q": ["Tell me about yourself.", "Walk me through your resume.", "Why do you want to switch careers?", "What are your strengths and weaknesses?"]},
    "english": {"name": "Daily English", "small": "Speak for 1 minute", "q": ["Describe your favourite city in India and why you like it.", "Talk about a book, film or series that changed how you think.", "What did you do last weekend?", "Describe a challenge you faced at work or college and how you solved it.", "Should students learn AI in school? Give your opinion.", "Describe your ideal job."]},
    "hr": {"name": "HR interview", "small": "Behavioural, STAR", "q": ["Tell me about a time you handled a conflict in a team.", "Describe a failure and what you learned from it.", "Why should we hire you?", "Where do you see yourself in five years?", "Tell me about a time you led without authority."]},
    "pm": {"name": "PM interview", "small": "Product sense, metrics", "q": ["How would you improve Google Maps for auto-rickshaw drivers?", "Swiggy orders dropped 10% last week. How would you investigate?", "What is your favourite product and why?", "Design an app to help senior citizens pay bills.", "How would you measure success for WhatsApp Channels?"]},
    "data": {"name": "Data / AI interview", "small": "Explain technical ideas", "q": ["Explain a JOIN to a non-technical manager.", "Walk me through a data project you are proud of.", "How would you explain overfitting to a business stakeholder?", "What is RAG and when would you use it?"]},
    "present": {"name": "Presentation", "small": "1–2 minute talk", "q": ["Pitch your product idea to an investor in 60 seconds.", "Give a 1-minute status update to your leadership team.", "Present one insight from data and the decision you recommend.", "Introduce yourself to a new team in a meeting."]},
    "drill": {"name": "Pronunciation drill", "small": "Listen and repeat", "q": ["We will review the very valuable video on Wednesday.", "I think these three things are worth thinking through together.", "The development of the product depends on data analysis.", "Please send the schedule for the vegetable delivery by evening.", "Our company's revenue grew faster than we expected this quarter.", "I would like to develop a comfortable, reliable environment."]},
}

def speaking():
    modes = "".join(f'<button type="button" data-mode="{k}" aria-pressed="{str(k == "intro").lower()}">{E(v["name"])}<small>{E(v["small"])}</small></button>' for k, v in SPEAK.items())
    return CSS + f'''<section style="padding-top:24px"><div class="wrap" data-ai="speak">
<div class="sc-modes" id="sc-modes">{modes}</div>
<div class="ai-grid2"><div class="card">
<div class="kicker" id="sc-kicker">Your question</div><p class="sc-q" id="sc-q"></p><div class="sc-target" id="sc-target" hidden></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn btn-line btn-sm" type="button" id="sc-next">New question ↻</button><button class="btn btn-line btn-sm" type="button" id="sc-listen">🔊 Listen</button>
<select id="sc-lang" aria-label="Accent" style="border:1px solid var(--line);border-radius:10px;padding:6px 10px;background:var(--surface);color:var(--ink)"><option value="en-IN">English (India)</option><option value="en-US">English (US)</option><option value="en-GB">English (UK)</option></select></div>
<div class="sc-center"><button class="sc-mic" id="sc-mic" type="button" aria-label="Start speaking"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/></svg></button>
<div class="sc-time" id="sc-time">00:00</div><p class="ai-note" id="sc-status">Tap the mic and answer out loud. Tap again to stop.</p></div>
<div class="sc-live" id="sc-live" contenteditable="true" aria-label="Your answer (transcript, you can edit or type)"><i>Your words will appear here as you speak. No mic? Type your answer here instead.</i></div>
<div class="sc-metrics" id="sc-metrics" hidden></div>
<button class="btn btn-primary" type="button" id="sc-go" style="width:100%">Get AI feedback</button>
<p class="ai-note">Speech recognition runs in your browser (best in Chrome or Edge). Audio is not recorded or stored; only the text is sent for feedback.</p></div>
<div><div class="ai-acts" id="sc-acts" hidden><button class="btn btn-line btn-sm" type="button" id="sc-say">🔊 Hear the better version</button><button class="btn btn-line btn-sm" type="button" id="sc-again">Try again</button></div>
<div class="ai-doc ai-out" id="sc-out"><div class="ai-empty"><b>Your coaching report will appear here</b>Scores for fluency, grammar, structure and delivery, the exact words to fix, a better version and your next drill.</div></div></div></div>
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
          "AI PRD Writer | /prd-writer.html | product management",
          "Tool tutorials: Figma, n8n, Make, Zapier, Replit, Claude Code | /tools.html | tools",
          "Handbooks and PDFs hub | /handbooks/index.html | handbooks",
          "Resources & AI tools (links, newsletters, job portals) | /resources.html | resources",
          "Programs: AI Product Management, AI for Data Engineers, GenAI Launchpad | /programs.html | programs",
          "Free counselling call / contact | /contact.html | contact"]
    open(os.path.join(out, "assets/ai-index.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return len(L)
