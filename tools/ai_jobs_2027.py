"""AI Jobs 2027: a roadmap page (ai-jobs-2027.html).

Seven role tracks, a 7-week sprint for the rest of 2026 with a saved checklist,
a quarter-by-quarter plan for 2027, the skills every AI role asks for, portfolio
projects and a job-search routine. Every resource links to free SkillNavora material.
"""
import html, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vaitis"))
import figures

E = lambda s: html.escape(str(s), quote=True)

ROLES = [
    {"id": "aipm", "icon": "🧭", "name": "AI Product Manager", "hue": 265,
     "what": "Decides which AI features to build, writes the requirements and evaluation plan, and works with engineers to ship and measure them.",
     "skills": ["Product sense and user research", "PRDs with success metrics", "How LLMs, RAG and agents work", "AI evals and guardrails", "APIs and data basics", "Prompt and context engineering"],
     "projects": ["A PRD for an AI feature with an evaluation plan", "A clickable prototype built with a no-code AI builder", "A teardown of an AI product: what works, what to fix, how to measure"],
     "sprint": ["Finish the AI PM 2 foundations and the APIs lesson", "Write 2 PRDs from the PRD library ideas, each with metrics and evals", "Take the PM practice test and the AI product sense questions"],
     "y2027": ["Apply to APM, PM and AI PM roles with your 2 PRDs and teardown", "Learn evals and agent design deeply", "Lead one real AI feature at work or in a freelance project"],
     "links": [("AI Product Management 2 (free course)", "programme-pm2.html"), ("APIs for PMs", "apis-for-pms.html"), ("PRD library", "prd-library.html"), ("AI Evals", "ai-evals.html"), ("AI PM job research", "ai-pm-industry-research.html"), ("PM interview questions", "questions.html#pm")]},
    {"id": "aieng", "icon": "🛠️", "name": "AI Engineer (LLM apps)", "hue": 215,
     "what": "Builds products on top of AI models: chat and search over documents (RAG), agents that use tools, evaluations, and the cost and speed work to run them.",
     "skills": ["Python and APIs", "Embeddings and vector search", "RAG pipelines", "Agents, tool calling and MCP", "Evals and monitoring", "Cost, latency and deployment"],
     "projects": ["A RAG chatbot over real documents, with an evaluation set", "An agent that uses 2 or 3 tools to finish a task", "A deployed app with logging, rate limits and a cost report"],
     "sprint": ["Python for Data Science lessons 1 to 10", "Generative AI & Agentic AI track", "Build a small RAG app on free AI (FreeLLMAPI guide)"],
     "y2027": ["Ship 2 deployed projects on GitHub with READMEs", "Learn agent orchestration and MCP servers", "Apply to AI engineer, LLM engineer and applied AI roles"],
     "links": [("AI Engineer programme", "programme-ai-engineer.html"), ("Python track", "data-science/index.html#t-python"), ("GenAI & Agentic AI track", "data-science/index.html#t-genai"), ("How AI agents work", "ai-agents-guide.html"), ("Context engineering", "context-engineering.html"), ("Free AI for coding (guide 25)", "vaitis.html#g-025")]},
    {"id": "data", "icon": "📊", "name": "Data Analyst with AI", "hue": 195,
     "what": "Answers business questions with data, using SQL, spreadsheets and dashboards, and uses AI to clean data, write queries faster and explain findings.",
     "skills": ["SQL", "Advanced Excel", "Power BI or Tableau", "Python basics", "AI-assisted analysis", "Data storytelling"],
     "projects": ["A sales dashboard built with SQL and Power BI", "An AI-assisted analysis notebook with a clear recommendation", "A one-page business case from a public dataset"],
     "sprint": ["SQL for Data Analysis lessons 1 to 12", "Power BI track", "AI for Data Analysis lessons"],
     "y2027": ["Publish 3 dashboards with short write-ups", "Add Python and statistics", "Apply to data analyst, BI analyst and business analyst roles"],
     "links": [("SQL track", "data-science/index.html#t-sql"), ("Excel track", "data-science/index.html#t-excel"), ("Power BI track", "data-science/index.html#t-powerbi"), ("AI for Data Analysis", "data-science/index.html#t-ai-analytics"), ("Live dashboard from a folder (guide 18)", "vaitis.html#g-018"), ("Practice tests", "tests.html")]},
    {"id": "de", "icon": "🔧", "name": "Data Engineer for AI", "hue": 160,
     "what": "Builds the pipelines and warehouses that feed analytics and AI, including the document and vector pipelines behind RAG.",
     "skills": ["SQL and Python", "Pipelines and orchestration (Airflow, dbt)", "Cloud warehouses (Snowflake, BigQuery, Databricks)", "Spark and streaming", "Data quality and governance", "Embedding and vector pipelines"],
     "projects": ["A batch ELT pipeline into a cloud warehouse", "A streaming pipeline with Kafka", "A document-to-vector pipeline for a RAG app"],
     "sprint": ["SQL track to the window-functions lessons", "Data Engineering & Cloud track lessons 1 to 6", "Build one small ELT pipeline end to end"],
     "y2027": ["Finish the streaming and lakehouse projects", "Add a cloud certification if your target employers ask for it", "Apply to data engineer and analytics engineer roles"],
     "links": [("AI-First Data Engineer", "program/ai-data-engineering.html"), ("Data Engineering & Cloud track", "data-science/index.html#t-data-engineering"), ("SQL track", "data-science/index.html#t-sql"), ("Python track", "data-science/index.html#t-python")]},
    {"id": "fde", "icon": "🤝", "name": "Forward Deployed / Solutions Engineer", "hue": 30,
     "what": "Works directly with customers to set up and adapt AI products for their business. Half engineer, half consultant.",
     "skills": ["Coding with AI tools", "APIs and integrations", "Discovery with customers", "Clear writing and demos", "Prototyping fast", "Security and data basics"],
     "projects": ["A working integration between an AI model and a business tool", "A recorded 5-minute customer demo", "A solution design document for a real company problem"],
     "sprint": ["Forward Deployed Engineer lesson", "Webhooks and automation lessons", "Practise a demo with the Speaking Coach"],
     "y2027": ["Build 2 customer-style integrations", "Practise discovery calls and demos every week", "Apply to FDE, solutions engineer and AI deployment roles"],
     "links": [("Forward Deployed Engineer", "programme-fde.html"), ("Webhooks and automation", "web-automation.html"), ("AI builder tools", "ai-builder-tools.html"), ("Speaking Coach", "speaking-coach.html")]},
    {"id": "auto", "icon": "⚙️", "name": "AI Automation Specialist", "hue": 135,
     "what": "Connects apps with AI to remove repetitive work: chatbots, lead follow-up, document processing and reports, often with n8n, Zapier or Make.",
     "skills": ["n8n, Zapier or Make", "Webhooks and APIs", "AI agents and prompts", "WhatsApp and Instagram bots", "Browser automation", "Pricing and scoping client work"],
     "projects": ["A WhatsApp or Instagram auto-reply bot", "A lead-follow-up automation", "A scraping-to-dashboard workflow for a small business"],
     "sprint": ["Webhooks, triggers and Playwright lesson", "Browser automation guide", "Build the SkillNavora-style chatbot from the Vaitis guides"],
     "y2027": ["Get 2 or 3 small paid projects or freelance clients", "Package one automation as a repeatable service", "Apply to automation, RevOps and AI operations roles"],
     "links": [("Webhooks and automation", "web-automation.html"), ("Browser automation", "browser-automation.html"), ("Scrape into a dashboard (guide 14)", "vaitis.html#g-014"), ("AI sales agent (guide 3)", "vaitis.html#g-003"), ("Make money with AI", "make-money-course.html")]},
    {"id": "gov", "icon": "🛡️", "name": "AI Governance & Responsible AI", "hue": 350,
     "what": "Helps companies use AI safely and legally: risk reviews, policies, data privacy, fairness and evaluation of AI systems.",
     "skills": ["AI risk and policy frameworks", "Data privacy law basics", "Evaluating AI systems", "Documentation and audits", "Stakeholder communication", "Business consulting"],
     "projects": ["An AI use policy for a small company", "A risk assessment of a real AI feature", "An evaluation report for a chatbot"],
     "sprint": ["AI governance guide", "Governance, Privacy & Business Consulting track", "AI Evals guide"],
     "y2027": ["Write 2 case studies on AI risk", "Learn the main regulations in your target market", "Apply to AI governance, risk and compliance roles"],
     "links": [("AI governance", "ai-governance.html"), ("Governance track", "data-science/index.html#t-governance"), ("AI Evals", "ai-evals.html")]},
]

WEEKS = [
    ("Week 1", "16–22 Nov", "Choose your track and set up", ["Pick one role track on this page", "Check your skills on the AI Skills Map", "Block 60 to 90 minutes a day in your calendar", "Set up a free AI tutor and coding assistant"]),
    ("Week 2", "23–29 Nov", "AI foundations everyone needs", ["Learn how LLMs, tokens and context work", "Practise prompt and context engineering", "Learn API basics (requests, JSON, status codes)", "Save 10 prompts you'll reuse"]),
    ("Week 3", "30 Nov–6 Dec", "Core skill of your track", ["Finish the first lessons of your track", "Take one practice test and note weak topics", "Use AI to explain anything you got wrong"]),
    ("Week 4", "7–13 Dec", "Build portfolio project 1", ["Pick the smallest useful version of project 1", "Build it with AI help", "Publish it (GitHub, Notion or a PDF) with a short write-up"]),
    ("Week 5", "14–20 Dec", "Evals, safety and project 2", ["Learn how to test AI output (evals)", "Add a simple evaluation to project 1", "Start project 2"]),
    ("Week 6", "21–27 Dec", "Resume, LinkedIn and story", ["Run your resume past the 7-reviewer panel", "Rewrite your LinkedIn headline and About section", "Write your 60-second 'why AI, why me' story"]),
    ("Week 7", "28–31 Dec", "Review and launch plan", ["Do one mock interview and score it", "List 30 target companies and roles", "Set your 2027 weekly targets"]),
]

YEAR = [
    ("Q1", "Jan–Mar 2027", "Apply and interview", "10 to 15 targeted applications a week, one mock interview a week, finish projects 2 and 3, message 5 people a week in your target companies."),
    ("Q2", "Apr–Jun 2027", "Deepen", "Go deep on one advanced area for your track (agents and MCP, evals, cloud data or automation). Add one real-world project: freelance, volunteer or at work."),
    ("Q3", "Jul–Sep 2027", "Specialise", "Choose a domain (fintech, health, e-commerce, education, SaaS) and write two case studies in it. Domain knowledge plus AI skills stands out."),
    ("Q4", "Oct–Dec 2027", "Grow", "Mentor someone, publish what you learned, and aim for a promotion, a better role or your first paying clients."),
]

BASE = [
    ("💬", "Prompt and context engineering", "Get reliable output from any AI tool.", "context-engineering.html"),
    ("🔌", "APIs and automation basics", "How apps and AI tools talk to each other.", "apis-for-pms.html"),
    ("🧪", "AI evals", "Prove an AI feature works before you ship it.", "ai-evals.html"),
    ("🤖", "Agents and MCP", "How AI agents plan, use tools and hand off work.", "ai-agents-guide.html"),
    ("📈", "Data literacy", "Read, question and present numbers.", "data-science/index.html#t-sql"),
    ("🛡️", "Responsible AI", "Privacy, bias and safe use at work.", "ai-governance.html"),
    ("🗣️", "Communication", "Explain AI work to non-technical people.", "speaking-coach.html"),
    ("🧰", "Daily AI tools", "763 tools and 25 step-by-step guides.", "vaitis.html"),
]

ROUTINE = [
    ("10–15", "targeted applications a week, each with a tailored resume"),
    ("5", "messages a week to people in your target companies"),
    ("1", "mock interview a week, scored and reviewed"),
    ("1", "portfolio update or post a week about what you built"),
]

CSS = """
.aj{--aj-r:18px}
.aj-hero{padding:46px 0 34px;background:radial-gradient(900px 400px at 85% 0%,color-mix(in srgb,var(--brand) 16%,transparent),transparent 65%)}
.aj-hero h1{font-size:clamp(34px,5.6vw,60px);line-height:1.04;margin:10px 0 12px;text-wrap:balance}
.aj-hero .lead{max-width:62ch}
.aj-count{display:flex;gap:14px;flex-wrap:wrap;margin-top:22px}
.aj-count div{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:12px 18px;min-width:130px;box-shadow:var(--shadow)}
.aj-count b{display:block;font-size:34px;line-height:1.05;font-variant-numeric:tabular-nums;color:var(--brand-ink)}
.aj-count small{color:var(--mu)}
.aj-note{font-size:13.5px;color:var(--mu);margin-top:12px}
.aj-sec{padding:34px 0}
.aj-sec h2{font-size:clamp(24px,3.4vw,34px);margin:6px 0 8px}
.aj-sub{color:var(--mu);max-width:70ch;margin:0 0 18px}
.aj-roles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-bottom:16px}
.aj-role{display:flex;flex-direction:column;gap:6px;align-items:flex-start;text-align:left;border:1px solid var(--line);background:var(--surface);border-radius:14px;padding:12px;cursor:pointer;font:600 14px var(--body);color:var(--ink)}
.aj-role span{font-size:24px}.aj-role[aria-selected="true"]{border-color:var(--brand);box-shadow:0 0 0 2px color-mix(in srgb,var(--brand) 35%,transparent);background:var(--brand-soft)}
.aj-panel{border-radius:var(--aj-r);overflow:hidden;border:1px solid var(--line);background:var(--surface);box-shadow:var(--shadow)}
.aj-band{padding:22px;color:#fff;background:radial-gradient(260px 180px at 92% 10%,rgba(255,255,255,.25),transparent 70%),linear-gradient(135deg,hsl(var(--h) 72% 46%),hsl(calc(var(--h) + 45) 70% 38%))}
.aj-band h3{margin:0 0 6px;font-size:24px;color:#fff}.aj-band p{margin:0;max-width:70ch;color:rgba(255,255,255,.93)}
.aj-cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;padding:20px 22px}
.aj-cols h4{margin:0 0 8px;font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--brand-ink)}
.aj-cols ul{margin:0;padding-left:20px}.aj-cols li{margin:4px 0}
.aj-links{display:flex;flex-wrap:wrap;gap:8px;padding:0 22px 22px}
.aj-links a{font:600 13.5px var(--body);border:1px solid var(--line);border-radius:99px;padding:6px 12px;text-decoration:none;background:var(--surface-2)}
.aj-progress{display:flex;align-items:center;gap:12px;margin:0 0 16px;font-weight:600}
.aj-bar{flex:1;height:10px;border-radius:99px;background:var(--surface-2);overflow:hidden;border:1px solid var(--line)}
.aj-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brand),color-mix(in srgb,var(--brand) 55%,#0ea5b7));transition:width .3s}
.aj-weeks{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.aj-week{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;min-width:0}
.aj-week.now{border-color:var(--brand);box-shadow:0 0 0 2px color-mix(in srgb,var(--brand) 30%,transparent)}
.aj-week header{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.aj-week header b{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--brand-ink)}
.aj-week header small{color:var(--mu);font-variant-numeric:tabular-nums}
.aj-week h3{margin:6px 0 10px;font-size:17px}
.aj-week label{display:flex;flex-direction:row;gap:9px;align-items:flex-start;font-weight:500;font-size:14.5px;margin:7px 0;cursor:pointer}
.aj-week input{width:18px;height:18px;margin:2px 0 0;flex:none;accent-color:var(--brand)}
.aj-week label:has(input:checked) span{text-decoration:line-through;color:var(--mu)}
.aj-tag{display:inline-block;font:700 11px var(--body);padding:2px 8px;border-radius:99px;background:var(--brand);color:var(--on-brand);margin-left:6px;vertical-align:middle}
.aj-year{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.aj-q{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;border-top:5px solid var(--brand)}
.aj-q b{font-size:26px;color:var(--brand-ink)}.aj-q small{display:block;color:var(--mu)}.aj-q h3{margin:6px 0;font-size:18px}.aj-q p{margin:0;font-size:14.5px}
.aj-base{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.aj-base a{display:flex;gap:12px;align-items:flex-start;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px}
.aj-base a:hover{border-color:var(--brand)}.aj-base span{font-size:24px}.aj-base small{display:block;color:var(--mu)}
.aj-routine{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.aj-routine div{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px}
.aj-routine b{display:block;font-size:30px;color:var(--brand-ink);font-variant-numeric:tabular-nums}
.aj-cta{border-radius:22px;padding:26px;background:linear-gradient(135deg,var(--brand-soft),var(--surface));border:1px solid var(--line);display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;align-items:center}
.aj-cta h2{margin:0 0 4px}
/* timeline illustration (same drawing style as the Vaitis guides) */
.vx-fig{margin:6px 0;background:linear-gradient(180deg,var(--surface),var(--surface-2));border:1px solid var(--line);border-radius:18px;padding:14px 12px 10px}
.vx-fig-scroll{overflow-x:auto}.vx-fig svg{display:block;width:100%;min-width:620px;height:auto}
.vx-fig figcaption{font-size:13px;color:var(--mu);text-align:center;margin-top:8px;font-weight:600}
.vx-fig-hint{display:none;font-size:12px;color:var(--mu);text-align:center;margin:0 0 6px}
.fg-card{fill:var(--surface);stroke:var(--line);stroke-width:1.5}.fg-hub{fill:var(--brand)}
.fg-t{fill:var(--ink);font:700 14px var(--body)}.fg-t-on{fill:var(--on-brand);font:700 14px var(--body)}
.fg-s{fill:var(--mu);font:400 12px var(--body)}.fg-s-on{fill:var(--on-brand);opacity:.88;font:400 12px var(--body)}
.fg-ico{font-size:20px}.fg-arrow{stroke:var(--mu);stroke-width:2;fill:none;opacity:.8}.fg-head{fill:var(--mu)}.fg-lab{fill:var(--mu);font:600 11.5px var(--body)}
@media (max-width:900px){.aj-year,.aj-routine{grid-template-columns:repeat(2,minmax(0,1fr))}.aj-cols{grid-template-columns:1fr}}
@media (max-width:640px){.vx-fig-hint{display:block}}
@media (max-width:520px){.aj-year,.aj-routine{grid-template-columns:1fr}.aj-count div{min-width:0;flex:1}}
"""

JS = r"""<script>
(function(){
  var root=document.getElementById('aj'); if(!root) return;
  var get=function(k){try{return localStorage.getItem(k)}catch(e){return null}}, set=function(k,v){try{localStorage.setItem(k,v)}catch(e){}};
  // Countdown to 1 January 2027 (visitor's local time)
  function tick(){var now=new Date(), end=new Date(2027,0,1), d=Math.max(0,Math.ceil((end-now)/864e5));
    var el=document.getElementById('aj-days'); if(el) el.textContent=d;
    var w=document.getElementById('aj-weeks-left'); if(w) w.textContent=Math.max(0,Math.ceil(d/7));
    var h=document.getElementById('aj-hours'); if(h) h.textContent=(d*1.5).toFixed(0);
    if(d===0){var t=document.getElementById('aj-days-l'); if(t) t.textContent='2027 is here. Start with Q1 below.';}}
  tick();
  // Highlight the current sprint week
  var starts=[[10,16],[10,23],[10,30],[11,7],[11,14],[11,21],[11,28]], today=new Date(), wk=-1;
  starts.forEach(function(s,i){var a=new Date(2026,s[0],s[1]), b=new Date(2026,s[0],s[1]+7); if(i===6) b=new Date(2027,0,1); if(today>=a&&today<b) wk=i;});
  if(today<new Date(2026,10,16)) wk=0;
  document.querySelectorAll('.aj-week').forEach(function(w,i){ if(i===wk){ w.classList.add('now'); var b=w.querySelector('header b'); if(b) b.insertAdjacentHTML('beforeend','<span class="aj-tag">This week</span>'); }});
  // Saved checklist
  var KEY='aj2027_done', done={}; try{done=JSON.parse(get(KEY)||'{}')}catch(e){done={}}
  var boxes=[].slice.call(document.querySelectorAll('.aj-week input[type=checkbox]'));
  function prog(){var n=boxes.filter(function(b){return b.checked}).length, p=Math.round(n*100/boxes.length);
    document.getElementById('aj-bar').style.width=p+'%'; document.getElementById('aj-pct').textContent=n+' of '+boxes.length+' tasks done ('+p+'%)';}
  boxes.forEach(function(b){ if(done[b.id]) b.checked=true; b.addEventListener('change',function(){ done[b.id]=b.checked; set(KEY,JSON.stringify(done)); prog(); }); });
  prog();
  // Role tabs (remembered; #role-<id> links work too)
  var tabs=[].slice.call(document.querySelectorAll('.aj-role')), panels=[].slice.call(document.querySelectorAll('.aj-panel'));
  function show(id){ if(!document.getElementById('role-'+id)) id=tabs[0].dataset.role;
    tabs.forEach(function(t){t.setAttribute('aria-selected',String(t.dataset.role===id))}); panels.forEach(function(p){p.hidden=p.id!=='role-'+id}); set('aj2027_role',id); }
  tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.role)})});
  var h=(location.hash||'').replace('#role-',''); show(location.hash.indexOf('#role-')===0?h:(get('aj2027_role')||tabs[0].dataset.role));
})();
</script>"""


def body():
    tabs = "".join(f'<button type="button" class="aj-role" role="tab" data-role="{r["id"]}" aria-controls="role-{r["id"]}" aria-selected="false"><span aria-hidden="true">{r["icon"]}</span>{E(r["name"])}</button>' for r in ROLES)
    panels = ""
    for r in ROLES:
        ul = lambda xs: "<ul>" + "".join(f"<li>{E(x)}</li>" for x in xs) + "</ul>"
        panels += (f'<div class="aj-panel" id="role-{r["id"]}" role="tabpanel" hidden>'
                   f'<div class="aj-band" style="--h:{r["hue"]}"><h3>{r["icon"]} {E(r["name"])}</h3><p>{E(r["what"])}</p></div>'
                   f'<div class="aj-cols"><div><h4>Skills employers ask for</h4>{ul(r["skills"])}</div><div><h4>Portfolio projects</h4>{ul(r["projects"])}</div>'
                   f'<div><h4>Your focus for the rest of 2026</h4>{ul(r["sprint"])}</div><div><h4>Your 2027 plan</h4>{ul(r["y2027"])}</div></div>'
                   f'<div class="aj-links">' + "".join(f'<a href="{E(u)}">{E(t)} →</a>' for t, u in r["links"]) + '</div></div>')
    weeks = ""
    for i, (w, d, t, items) in enumerate(WEEKS):
        checks = "".join(f'<label><input type="checkbox" id="aj-w{i+1}-{j+1}"><span>{E(x)}</span></label>' for j, x in enumerate(items))
        weeks += f'<article class="aj-week"><header><b>{E(w)}</b><small>{E(d)}</small></header><h3>{E(t)}</h3>{checks}</article>'
    year = "".join(f'<div class="aj-q"><b>{q}</b><small>{E(d)}</small><h3>{E(t)}</h3><p>{E(p)}</p></div>' for q, d, t, p in YEAR)
    base = "".join(f'<a href="{E(u)}"><span aria-hidden="true">{i}</span><div><b>{E(t)}</b><small>{E(s)}</small></div></a>' for i, t, s, u in BASE)
    routine = "".join(f'<div><b>{E(n)}</b>{E(t)}</div>' for n, t in ROUTINE)
    timeline = figures.pipeline("Your path from today to an AI job in 2027", [
        ("📍", "Today", "pick a track"), ("🏃", "7-week sprint", "16 Nov to 31 Dec 2026"), ("📨", "Q1 2027", "apply and interview"),
        ("📚", "Q2 2027", "deepen one area"), ("🎯", "Q3 2027", "specialise in a domain"), ("🚀", "Q4 2027", "grow and lead")], per_row=6, bw=150)
    return f"""<style>{CSS}</style>
<div class="aj" id="aj">
<section class="aj-hero"><div class="wrap">
  <div class="kicker">Career roadmap · 2027</div>
  <h1>Get ready for <span class="g">AI jobs in 2027</span></h1>
  <p class="lead">Pick one AI role, follow a 7-week sprint to the end of 2026, then a quarter-by-quarter plan for 2027. Every step links to free SkillNavora lessons, guides and practice.</p>
  <div class="aj-count" aria-live="polite">
    <div><b id="aj-days">47</b><small id="aj-days-l">days left in 2026</small></div>
    <div><b id="aj-weeks-left">7</b><small>weeks to sprint</small></div>
    <div><b id="aj-hours">70</b><small>hours at 90 minutes a day</small></div>
  </div>
  <p class="aj-note">This is a learning plan, not a job guarantee. Hiring depends on your market, experience and the roles open at the time.</p>
</div></section>

<section class="aj-sec"><div class="wrap">{timeline}</div></section>

<section class="aj-sec" id="tracks"><div class="wrap">
  <div class="kicker">Step 1</div><h2>Choose your AI role</h2>
  <p class="aj-sub">Seven roles that AI teams hire for. Pick the one closest to your background; you can switch later. Each track shows the skills employers list, the projects to build and where to learn for free.</p>
  <div class="aj-roles" role="tablist" aria-label="AI roles">{tabs}</div>
  {panels}
</div></section>

<section class="aj-sec" id="sprint"><div class="wrap">
  <div class="kicker">Step 2</div><h2>The 7-week sprint to 31 December 2026</h2>
  <p class="aj-sub">About 60 to 90 minutes a day. Tick tasks as you finish them; your progress is saved in this browser.</p>
  <div class="aj-progress"><span id="aj-pct">0 tasks done</span><div class="aj-bar" aria-hidden="true"><i id="aj-bar"></i></div></div>
  <div class="aj-weeks">{weeks}</div>
</div></section>

<section class="aj-sec" id="baseline"><div class="wrap">
  <div class="kicker">Everyone needs these</div><h2>The AI baseline for every role</h2>
  <p class="aj-sub">Whatever track you choose, these eight skills show up again and again in AI job descriptions.</p>
  <div class="aj-base">{base}</div>
</div></section>

<section class="aj-sec" id="year"><div class="wrap">
  <div class="kicker">Step 3</div><h2>Your 2027, quarter by quarter</h2>
  <div class="aj-year">{year}</div>
</div></section>

<section class="aj-sec" id="search"><div class="wrap">
  <div class="kicker">Step 4</div><h2>A weekly job-search routine</h2>
  <p class="aj-sub">Steady weekly numbers beat one big push. Use the guides below to save time on each one.</p>
  <div class="aj-routine">{routine}</div>
  <div class="aj-links" style="padding:16px 0 0">
    <a href="vaitis.html#g-016">Resume: 7-reviewer panel →</a><a href="vaitis.html#g-001">Applications with ChatGPT agent →</a><a href="vaitis.html#g-012">LinkedIn with Claude →</a>
    <a href="questions.html">Interview questions →</a><a href="tests.html">Practice tests →</a><a href="practice.html">AI mock interview →</a><a href="jobs.html">Job board →</a>
  </div>
</div></section>

<section class="aj-sec"><div class="wrap"><div class="aj-cta">
  <div><h2>Want a guided path?</h2><p class="aj-sub" style="margin:0">Live programmes with mentors, projects and career guidance. Free counselling call to pick the right one.</p></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-primary" href="programs.html">See programmes</a><a class="btn btn-line" href="contact.html">Book a free call</a></div>
</div></div></section>
</div>
{JS}"""
