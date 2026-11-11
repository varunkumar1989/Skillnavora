"""SFMC academy dashboard: three tabs, module and topic expanders, search, completion ticks (per-viewer, browser only)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sfmc_content import MODULES, LABS
from sfmc_build import E, INTERVIEW

PDFS = [
 ("SFMC-01-Master-Handbook.pdf", "Master handbook (all 28 modules)"), ("SFMC-02-SQL-Handbook.pdf", "SQL handbook"),
 ("SFMC-03-AMPscript-and-HTML-Handbook.pdf", "AMPscript and HTML handbook"), ("SFMC-04-Journey-and-Automation-Handbook.pdf", "Journey Builder and Automation handbook"),
 ("SFMC-05-Interview-Handbook.pdf", "Interview question bank"), ("SFMC-06-Capstone-Projects.pdf", "Capstone projects"),
 ("SFMC-07-12-Month-Roadmap.pdf", "12-month roadmap"), ("SFMC-08-Quick-Reference.pdf", "Quick reference"),
]
TOOLS = [
 ("1. Salesforce official platform", [("Salesforce Help: Marketing Cloud Engagement", "https://help.salesforce.com/s/products/marketing-cloud-engagement", "Official", "Product documentation for every studio."), ("Salesforce product pages", "https://www.salesforce.com/marketing/", "Official", "Product names and editions.")]),
 ("2. Trailhead learning", [("Trailhead", "https://trailhead.salesforce.com/", "Official, free", "Guided modules and badges."), ("Trailhead credentials (certifications)", "https://trailhead.salesforce.com/credentials/overview", "Official", "Current certification names and exam guides.")]),
 ("3. Marketing Cloud Engagement", [("SFMC developer documentation", "https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/get-started-rest.html", "Official", "REST, SOAP and the guides for each studio.")]),
 ("4. SQL practice", [("SQLBolt (interactive SQL lessons)", "https://sqlbolt.com/", "Third-party, free", "Practise SQL basics in the browser."), ("Mode SQL tutorial", "https://mode.com/sql-tutorial/", "Third-party, free", "Joins, aggregates and cohort examples.")]),
 ("5. AMPscript development", [("AMPscript guide (Salesforce docs)", "https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/ampscript.html", "Official", "Functions and syntax.")]),
 ("6. HTML and CSS development", [("MDN: HTML basics", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content", "Third-party, free", "Learn HTML from the basics."), ("Can I email (client support tables)", "https://www.caniemail.com/", "Third-party, free", "Which email clients support which CSS.")]),
 ("7. JavaScript development", [("MDN JavaScript guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "Third-party, free", "JavaScript for forms and pages.")]),
 ("8. API testing", [("Postman Learning Center", "https://learning.postman.com/docs/introduction/overview/", "Third-party, free tier", "Build and test API requests.")]),
 ("9. Data integration", [("Salesforce developer docs", "https://developer.salesforce.com/docs", "Official", "APIs and integration guides.")]),
 ("10. Data Cloud", [("Salesforce Data Cloud documentation", "https://help.salesforce.com/s/products/data-cloud", "Official", "Data streams, identity resolution and activation.")]),
 ("11. Marketing analytics", [("Google Analytics help (web analytics)", "https://support.google.com/analytics", "Official (Google), free", "Web traffic and conversions.")]),
 ("12. Email testing and deliverability", [("Google: email sender guidelines", "https://support.google.com/a/answer/81126", "Official (Google)", "Sender authentication and bulk-sender rules."), ("Litmus (email testing)", "https://www.litmus.com/", "Third-party, paid", "Preview email clients (paid plans).")]),
 ("13. AI development", [("Anthropic API docs", "https://docs.claude.com/", "Official", "Calling Claude from an integration."), ("OpenAI API docs", "https://platform.openai.com/docs", "Official", "Calling OpenAI models from an integration.")]),
 ("14. Automation tools", [("n8n docs", "https://docs.n8n.io/", "Third-party, freemium", "Workflow automation with API calls.")]),
 ("15. Documentation and troubleshooting", [("GitHub Docs", "https://docs.github.com/", "Official", "Version control and project documentation."), ("Visual Studio Code", "https://code.visualstudio.com/docs", "Official", "Editor for HTML, AMPscript and SQL files.")]),
 ("16. Certifications and interview preparation", [("Salesforce Trailhead credentials", "https://trailhead.salesforce.com/credentials/overview", "Official", "Check active certification names here."), ("SkillNavora interview questions", "https://skillnavora.in/questions.html", "SkillNavora", "Practice questions for data and marketing roles.")]),
]
OTHER = [
 ("Digital Marketing", "programme-digital-marketing.html", "Prerequisite: channels, funnels and campaign metrics."),
 ("Data Science & AI: SQL and Power BI", "resources.html#data", "Next: SQL depth and dashboards for reporting roles."),
 ("AI Engineer", "resources.html#op-ai-engineer", "Next: APIs, integrations and AI features."),
 ("Forward Deployed Engineer (FDE)", "programme-fde.html", "Career path: customer-facing technical implementation."),
 ("Data Science & AI quick reference", "data-science-extras.html", "Cheat sheets, glossary and supplements for the wider data course."),
]

def topic_block(mno, idx, t):
    tid = f"sfmc-{mno}-{idx}"
    links = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in t["links"])
    code = f'<h4>Code example</h4><pre><code>{E(t["code"])}</code></pre>' if t.get("code") else ""
    lic = f'<p class="gnote"><b>Licence and edition:</b> {E(t["licence"])}</p>' if t.get("licence") else ""
    return (f'<details class="gt" data-search="{E((t["t"]+" "+t["what"]).lower())}"><summary><label class="tick"><input type="checkbox" data-track="{tid}" aria-label="Mark topic complete"></label> {E(t["t"])}</summary>'
            f'<h4>What is it?</h4><p>{E(t["what"])}</p><h4>Why is it important?</h4><p>{E(t["why"])}</p>'
            f'<h4>How does it work and the steps</h4><ol>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + '</ol>'
            f'<h4>Real-world example</h4><p class="ex">{E(t["example"])}</p>{code}{lic}'
            f'<h4>Common errors</h4><p>{E(t["mistake"])}</p><h4>Interview question</h4><p>{E(t["interview"])}</p>'
            f'<h4>Hands-on exercise</h4><p>{E(t["exercise"])}</p><h4>Official documentation and further reading</h4><ul>{links}</ul></details>')

def module_block(num, title, level, summary, topics):
    pdf = {1:"SFMC-01-Master-Handbook.pdf",6:"SFMC-02-SQL-Handbook.pdf",8:"SFMC-03-AMPscript-and-HTML-Handbook.pdf",9:"SFMC-03-AMPscript-and-HTML-Handbook.pdf",10:"SFMC-03-AMPscript-and-HTML-Handbook.pdf",11:"SFMC-04-Journey-and-Automation-Handbook.pdf",12:"SFMC-04-Journey-and-Automation-Handbook.pdf",26:"SFMC-06-Capstone-Projects.pdf",28:"SFMC-07-12-Month-Roadmap.pdf",27:"SFMC-05-Interview-Handbook.pdf"}.get(num, "SFMC-01-Master-Handbook.pdf")
    tps = "".join(topic_block(num, i, t) for i, t in enumerate(topics, 1))
    return (f'<details class="mod" data-search="{E((title+" "+summary).lower())}"><summary><span class="mn">Module {num}</span> {E(title)} <span class="lvl">{E(level)}</span></summary>'
            f'<p class="meta">{E(summary)}</p><p><a class="btn btn-line btn-sm" href="read.html?doc=handbook/sfmc/{pdf}">Read this module in the handbook PDF</a></p>{tps}</details>')

def build(page, uhero, out):
    styles = """<style>
.sf-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}.sf-tabs button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:99px;padding:9px 15px;font:600 14px var(--body);cursor:pointer}
.sf-tabs button[aria-selected=true]{background:var(--brand);color:#fff;border-color:var(--brand)}
.sf-search{width:100%;max-width:420px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink);font:500 15px var(--body);margin:0 0 14px}
details.mod{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 14px;margin:10px 0}details.mod>summary{cursor:pointer;font:700 17px var(--display)}
.mn{display:inline-block;background:var(--brand);color:#fff;border-radius:99px;padding:2px 9px;font-size:12px;margin-right:6px}.lvl{color:var(--mu);font-size:13px;font-weight:600;margin-left:6px}
details.gt{background:var(--bg,transparent);border:1px solid var(--line);border-radius:12px;padding:8px 12px;margin:8px 0}details.gt>summary{cursor:pointer;font:700 15px var(--display);list-style-position:outside}
details.gt h4{margin:10px 0 3px;font:700 11.5px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--teal,#0b7a75)}details.gt p{margin:3px 0 6px}details.gt ol,details.gt ul{margin:3px 0 6px;padding-left:20px}
.tick{display:inline-block;margin-right:6px;vertical-align:middle}.tick input{width:18px;height:18px}
.ex{background:#fff7e8;color:#3d2a00;border-left:4px solid #d98a00;padding:7px 10px;border-radius:8px}
pre{background:#1e1b2e;color:#f1eeff;border-radius:10px;padding:10px 12px;overflow-x:auto;font:12.5px/1.5 'JetBrains Mono',Consolas,monospace}
.gnote{font-size:13px;color:var(--mu)}.gap-hidden{display:none!important}
table.tl{width:100%;border-collapse:collapse;font-size:14px}table.tl th,table.tl td{border:1px solid var(--line);padding:8px 9px;text-align:left;vertical-align:top}
.prog{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 12px}.prog .pct{font-weight:700}
</style>"""
    tabs = [("content", "Programme Content"), ("other", "Other Programmes"), ("tools", "Tools & Learning Links")]
    bar = '<div class="sf-tabs" role="tablist" id="sf-bar">' + "".join(f'<button role="tab" data-sf="{k}" aria-selected="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n) in enumerate(tabs)) + "</div>"
    mods = "".join(module_block(n, t, lvl, s, tp) for n, t, lvl, s, tp in MODULES)
    labs = '<details class="mod"><summary><span class="mn">Module 25</span> Practical labs and real-world scenarios</summary><p class="meta">Twenty labs. Labs marked "account" need a provisioned Marketing Cloud account; others are simulated or paper practice.</p><table class="tl"><tr><th>Lab</th><th>Title</th><th>Requirement</th></tr>' + "".join(f"<tr><td>{E(c)}</td><td>{E(n)}</td><td>{'Account needed' if k=='account' else 'Simulated / paper'}</td></tr>" for c, n, k in LABS) + '</table></details>'
    interview = '<details class="mod"><summary><span class="mn">Module 27</span> Interview question bank</summary><p class="meta">Full bank in the interview handbook PDF. Questions by area:</p>' + "".join(f'<h4>{E(g)}</h4><ol>' + "".join(f"<li>{E(q)}</li>" for q in qs) + '</ol>' for g, qs in INTERVIEW) + '</details>'
    progress = ('<div class="prog"><span>Topics ticked: <span class="pct" id="sf-done">0</span> of <span id="sf-total">0</span></span>'
                '<span class="meta">Ticks are saved in this browser only.</span></div>')
    content = (progress + f'<input class="sf-search" type="search" placeholder="Search modules and topics" aria-label="Search" id="sf-q">' + mods + labs + interview)
    other = ('<h2 class="sec-h">Related programmes</h2><p class="meta">Prerequisites and next paths. Each opens on its own page.</p><div class="grid g3">'
             + "".join(f'<a class="card" href="{E(h)}" style="text-decoration:none"><h3 style="margin:6px 0 4px">{E(n)}</h3><p>{E(d)}</p><span class="go">Open →</span></a>' for n, h, d in OTHER) + '</div>'
             + '<h2 class="sec-h" style="margin-top:20px">Career pathways</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in ["SFMC Email Marketing Specialist", "SFMC Campaign Specialist", "SFMC Developer", "SFMC Consultant", "SFMC Technical Consultant", "SFMC Administrator", "SFMC Automation Specialist", "SFMC Solution Architect", "Salesforce Marketing Cloud Data Specialist", "Marketing Automation Architect"]) + '</ul>')
    tools = ('<h2 class="sec-h">Tools and learning links</h2><p class="meta">Official sites are labelled Official. Third-party resources are labelled clearly. Prices and free tiers change; check the provider\'s page. Last checked dates are shown in the handbook; please re-check before you buy anything.</p>'
             + "".join(f'<h3 class="gsec">{E(cat)}</h3><div class="grid g3">' + "".join(f'<a class="card tool" href="{E(u)}" target="_blank" rel="noopener"><span class="ftag">{E(tag)}</span><h3 style="margin-top:6px">{E(n)} ↗</h3><p>{E(d)}</p></a>' for n, u, tag, d in items) + '</div>' for cat, items in TOOLS))
    body = "".join(f'<div class="sf-panel" id="sp-{k}" role="tabpanel"{"" if i == 0 else " hidden"}>{c}</div>' for i, (k, c) in enumerate([("content", content), ("other", other), ("tools", tools)]))
    js = """<script>(function(){
var bar=document.getElementById('sf-bar');if(!bar)return;var tabs=[].slice.call(bar.querySelectorAll('[role=tab]'));
function show(k){if(['content','other','tools'].indexOf(k)<0)k='content';tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.sf===k?'true':'false')});document.querySelectorAll('.sf-panel').forEach(function(p){p.hidden=p.id!=='sp-'+k})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.sf);try{history.replaceState(null,'','#'+t.dataset.sf)}catch(e){}})});
function fromHash(){show((location.hash||'#content').slice(1))}window.addEventListener('hashchange',fromHash);fromHash();
var q=document.getElementById('sf-q');if(q)q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();document.querySelectorAll('#sp-content details.mod, #sp-content details.gt').forEach(function(d){d.classList.toggle('gap-hidden',v!==''&&(d.dataset.search||'').indexOf(v)<0)})});
var KEY='sfmc-academy-ticks';function read(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}}
function write(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
var st=read();var boxes=[].slice.call(document.querySelectorAll('input[data-track]'));
function count(){var n=boxes.filter(function(b){return b.checked}).length;var a=document.getElementById('sf-done'),c=document.getElementById('sf-total');if(a)a.textContent=n;if(c)c.textContent=boxes.length}
boxes.forEach(function(b){b.checked=!!st[b.dataset.track];b.addEventListener('click',function(e){e.stopPropagation()});b.addEventListener('change',function(){st[b.dataset.track]=b.checked;write(st);count()})});count();
})();</script>"""
    hero = uhero("SFMC Academy · Salesforce Marketing Cloud", 'Salesforce Marketing Cloud <span class="g">complete guide</span>',
                 "Twenty-eight modules from CRM basics to architecture and certification. Open a module, then a topic. Each topic gives the explanation, steps, examples, exercises and official links.")
    top = ('<div class="card" style="margin:0 0 16px;border:2px solid var(--brand,#6C4CF5)"><div class="kicker">Interactive academy</div>'
           '<h3 style="margin:6px 0 4px">Open the SFMC Academy with every module, topic and all 37 PDFs</h3>'
           '<p class="meta" style="margin:0 0 10px">The interactive version has all 28 modules with every topic explained, detailed lessons with code, labs, projects, interviews, the roadmap and a PDF library that opens each handbook inside the page.</p>'
           '<div class="hb-acts"><a class="btn btn-primary btn-sm" href="https://claude.ai/artifact/BW5nVs6WRq1mS1dxbhioXQ" target="_blank" rel="noopener" data-nogate>Open the interactive SFMC Academy ↗</a>'
           '<a class="btn btn-line btn-sm" href="read.html?doc=handbook/sfmc/SFMC-Complete-Handbook.pdf">Complete handbook PDF (205 pages)</a></div></div>')
    main = f'{styles}<section style="padding-top:24px"><div class="wrap">{top}{bar}{body}</div></section>{js}'
    page("sfmc-academy.html", "SFMC Academy: Salesforce Marketing Cloud complete guide · SkillNavora",
         "A complete Salesforce Marketing Cloud learning guide: 28 modules, SQL, AMPscript, journeys, automations, APIs, interviews and certification planning.", hero + main, "sfmc-academy.html")
