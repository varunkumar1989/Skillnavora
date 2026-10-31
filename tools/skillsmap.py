"""AI Skills Map (ai-skills-map.html): the full AI skills catalogue mapped to where each is taught on SkillNavora,
the recommended 7-skill learning order, and skills that AI-era job descriptions ask for."""
import html, json, os
E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cat = json.load(open(os.path.join(ROOT, "data-science/catalog.json")))
_pages = {f"{t['id']}-{l['num']:02d}": "data-science/" + l["page"] for t in _cat["tracks"] for l in t["lessons"]}
def L(key):  # lesson by id prefix like "genai-02"
    return _pages.get(key, "data-science/index.html")
PM = lambda n: f"handbooks/pm/m{n:02d}.html"

C = {"ctx": ("Prompt & Context Engineering", "context-engineering.html"), "skills": ("AI Skills & Templates", "ai-skills.html"), "brain": ("AI Second Brain", "ai-second-brain.html"),
     "evals": ("AI Evals", "ai-evals.html"), "browser": ("Browser Automation & AI Agents", "browser-automation.html"), "orch": ("Agent Orchestration & Monitoring", "agent-orchestration.html"),
     "toolkit": ("AI PM Toolkit", "pm-toolkit.html"), "prdlib": ("PRD library", "prd-library.html"), "brd": ("BRD & FRD guide", "brd-frd.html"), "lab": ("Practice Lab", "lab.html")}

PATH = [("Prompt and context engineering", "Make requests precise and evidence-based.", [C["ctx"], ("Prompt engineering in depth", L("genai-02"))]),
        ("Skill and template creation", "Standardise your recurring PM work.", [C["skills"], C["prdlib"]]),
        ("Second brain and retrieval", "Reuse your learning material and project knowledge.", [C["brain"], ("RAG lesson", L("genai-05"))]),
        ("Research and data analysis", "Turn information into supported decisions.", [("Data Science & AI handbook", "data-science/index.html"), ("AI for analysts", L("ai-analytics-01"))]),
        ("Evals", "Check whether outputs meet your standards.", [C["evals"], ("Evaluating LLM apps", L("genai-09"))]),
        ("API and browser automation", "Connect the assistant to real workflows.", [C["browser"], ("APIs without code", L("agents-01"))]),
        ("Orchestration and monitoring", "Run longer workflows reliably.", [C["orch"], ("n8n tutorial", L("tools-02"))])]

# (group, [(capability, [(label, href), ...])])
CAT = [
 ("1. Instructions, context and knowledge", [
  ("Prompt engineering", [C["ctx"], ("Prompt engineering lesson", L("genai-02")), ("PM handbook: Claude for PMs", PM(14))]),
  ("Context engineering", [C["ctx"], ("Second Brain: class 5", C["brain"][1])]), ("Skill creation", [C["skills"]]), ("Template creation", [C["skills"], C["prdlib"], C["brd"]]),
  ("Structured output", [C["ctx"], ("LLM APIs: structured output", L("genai-03"))]), ("Task decomposition", [C["ctx"], C["orch"]]), ("Context compression", [C["ctx"]]),
  ("Document ingestion", [C["ctx"]]), ("OCR", [C["ctx"]]), ("Knowledge organisation", [C["brain"]]), ("Semantic search", [("Embeddings & vector search", L("genai-04"))]),
  ("RAG", [("RAG lesson", L("genai-05")), ("PM handbook: LLMs & RAG", PM(10))]), ("Source attribution", [C["ctx"], C["evals"]]), ("Persistent memory", [C["brain"]]),
  ("Second-brain management", [C["brain"]]), ("Knowledge graphs", [C["ctx"]])]),
 ("2. Research and analysis", [
  ("Web search & multi-source research", [C["browser"]]), ("Source credibility & fact checking", [C["browser"], C["ctx"]]), ("Competitive analysis", [C["toolkit"]]),
  ("Market research & sizing", [C["toolkit"], ("PM handbook: discovery & research", PM(3))]), ("Literature review", [C["brain"]]), ("Customer-feedback & interview synthesis", [C["toolkit"], C["brain"]]),
  ("Survey analysis", [("Statistics lessons", L("ml-01"))]), ("Quantitative data analysis", [("Python EDA", L("python-22")), ("Statistics", L("ml-01"))]),
  ("SQL analysis", [("SQL track", L("sql-01")), C["lab"]]), ("Spreadsheet analysis", [("Excel track", L("excel-01")), ("AI in Excel", L("ai-analytics-03"))]),
  ("Experiment analysis", [("Hypothesis testing", L("ml-04")), C["toolkit"]]), ("Scenario analysis", [C["toolkit"]])]),
 ("3. Web browsing and action automation", [
  ("Browser navigation, extraction, forms, downloads, uploads", [C["browser"]]), ("Multi-step website workflows", [C["browser"]]), ("Browser testing & screenshot comparison", [C["browser"]]),
  ("Desktop & file automation", [C["browser"]]), ("API integration", [("APIs without code", L("agents-01")), ("LLM APIs from Python", L("genai-03"))]),
  ("Tool calling", [("Tool use & function calling", L("genai-06"))]), ("MCP integration", [("MCP lesson", L("genai-08")), ("MCP without code", L("agents-02"))]),
  ("Scheduled & event-driven automation", [C["orch"], ("n8n tutorial", L("tools-02")), ("Connect apps", L("agents-04"))]), ("Monitoring & alerts", [C["orch"]]), ("Approval workflows", [C["orch"], C["browser"]])]),
 ("4. Evals, testing and reliability", [
  ("Eval datasets, rubrics, grading", [C["evals"]]), ("Human & AI-assisted grading", [C["evals"]]), ("Factuality & retrieval evaluation", [C["evals"], ("RAG lesson", L("genai-05"))]),
  ("Instruction-following & tool-use evaluation", [C["evals"]]), ("Task-completion & browser-agent evaluation", [C["evals"], C["browser"]]), ("Visual evaluation", [C["skills"]]),
  ("Regression & robustness testing", [C["evals"]]), ("Prompt-injection & permission-boundary testing", [C["evals"], C["browser"]]), ("Cost & latency evaluation", [C["evals"], C["orch"]]),
  ("Trace analysis & production monitoring", [C["evals"], C["orch"]])]),
 ("5. Agent coordination and workflow design", [
  ("Workflow orchestration, routing", [C["orch"]]), ("Planning, replanning, state, checkpointing", [C["orch"]]), ("Parallel execution & multi-agent coordination", [C["orch"], ("AI agents lesson", L("genai-07"))]),
  ("Human-in-the-loop & error recovery", [C["orch"]]), ("Caching, model selection, cost management", [C["orch"]])]),
 ("6. Writing, design and media", [
  ("Summarisation, business writing, editing", [C["ctx"], ("PM handbook: communication", PM(6))]), ("Translation & localisation", [C["ctx"]]), ("Document & presentation generation", [C["skills"]]),
  ("Data visualisation", [("Visualisation lessons", L("python-20")), ("Power BI", L("powerbi-01"))]), ("UI/UX analysis & interface design", [("Figma tutorial", L("tools-01")), ("PM handbook: UX", PM(5))]),
  ("Image, audio, video and speech", [("Content creation guide", L("content-01")), ("Voice agents", L("agents-06")), ("Learning sites: AI media tools", "resources.html#learn-genai")])]),
 ("7. Software and data engineering", [
  ("Code generation, debugging, review, refactoring, tests", [("Claude Code tutorial", L("agents-05")), ("PM handbook: Claude Code", PM(15)), ("AI coding assistants", L("genai-11"))]),
  ("Documentation & API development", [("Shipping a GenAI app", L("genai-12"))]), ("Database design & data pipelines", [("ER diagrams", L("sql-02")), ("Python & SQL", L("python-23"))]),
  ("Deployment, security review, dependencies", [("PM handbook: Claude Code", PM(15)), ("Shipping a GenAI app", L("genai-12"))])]),
 ("8. Product-management skills you can package", [
  ("Problem framing, personas, JTBD, journeys", [C["toolkit"], ("PM handbook: problem framing", PM(4))]), ("PRD creation", [("AI PRD Writer", "prd-writer.html"), C["prdlib"], C["skills"]]),
  ("Prioritisation & roadmaps", [C["toolkit"], ("PM handbook: strategy", PM(2))]), ("Metrics design & experiment planning", [C["toolkit"], ("PM handbook: analytics", PM(7))]),
  ("Product teardown & launch planning", [C["toolkit"], ("PM handbook: launch & growth", PM(8))]), ("Stakeholder communication, decision logs, weekly reports", [C["toolkit"], C["brain"], C["skills"]])]),
 ("9. Advanced AI product management", [
  ("AI product strategy, moats, data flywheels, build vs buy", [("AI Product Strategy", "ai-product-strategy.html")]), ("AI UX: trust, explainability, feedback, failure design", [("Designing AI Experiences", "ai-ux-design.html")]),
  ("Pricing, packaging and unit economics of AI", [("Pricing & Monetising AI", "ai-pricing.html")]), ("Recommendation, classification and ML lifecycle", [("ML Products for PMs", "ml-products.html")]),
  ("AI governance, regulation (EU AI Act, DPDP), risk assessment", [("AI Governance & Responsible AI", "ai-governance.html")]), ("Platforms, APIs, developer experience, ecosystems", [("Platform & API PM", "platform-api-pm.html")]),
  ("Product operations: rituals, tools, insight pipelines", [("Product Operations", "product-ops.html")]), ("Multimodal AI: vision, image, voice, video, deepfake safety", [("Multimodal AI & AI Media", "multimodal-ai.html")])]),
]

JD = [  # skills that AI-era job descriptions commonly list (synthesised from typical postings)
 ("AI Product Manager", ["Define AI product strategy, use cases and success metrics", "Write PRDs for LLM/RAG/agent features with evals and guardrails", "Work with data science on model choice, cost and latency trade-offs",
  "Prompt and context design; prototyping with AI tools", "Experimentation (A/B tests) and product analytics (SQL, Mixpanel/Amplitude)", "Responsible AI: privacy, safety, bias", "Stakeholder communication and roadmaps"],
  [C["evals"], C["ctx"], C["skills"], C["toolkit"], ("PM program", "program/ai-product-management.html")]),
 ("Data / AI Analyst", ["SQL, Excel and Python for analysis", "Dashboards (Power BI / Tableau)", "Statistics and experiment analysis", "Using GenAI for analysis, text-to-SQL and automation", "Communicating insights to stakeholders"],
  [("Data Science & AI handbook", "data-science/index.html"), ("AI for analysts", L("ai-analytics-01")), C["lab"]]),
 ("GenAI / AI Automation Specialist", ["Build workflows with n8n, Make, Zapier and LLM APIs", "RAG, tool calling and MCP integrations", "Agents with approvals and monitoring", "Evaluating and improving AI outputs", "Browser and API automation"],
  [C["orch"], C["browser"], ("MCP lesson", L("genai-08")), C["evals"]]),
 ("Business Analyst (AI-era)", ["Requirements: BRD, FRD, user stories, acceptance criteria", "Process mapping and gap analysis", "Data analysis with SQL/Excel/Power BI", "Using AI for documentation, research and synthesis"],
  [C["brd"], C["ctx"], ("SQL track", L("sql-01"))]),
]

def page():
    path = "".join(f'<li class="card" style="list-style:none;display:flex;gap:14px;align-items:flex-start"><span style="flex:none;width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#6C4CF5,#22D3EE);color:#fff;display:grid;place-items:center;font-weight:800">{i}</span><span><b style="font-size:17px">{E(n)}</b><br><span style="color:var(--mu)">{E(w)}</span><br>'
                   + " · ".join(f'<a href="{E(h)}">{E(t)}</a>' for t, h in links) + "</span></li>" for i, (n, w, links) in enumerate(PATH, 1))
    groups = "".join(f'<details class="card sm-g" open><summary style="cursor:pointer;font:700 18px var(--display,inherit)">{E(g)} <span class="meta">({len(items)})</span></summary><div class="sm-t"><table><thead><tr><th>Capability</th><th>Learn it on SkillNavora</th></tr></thead><tbody>'
                     + "".join(f'<tr><td><b>{E(c)}</b></td><td>' + " · ".join(f'<a href="{E(h)}">{E(t)}</a>' for t, h in links) + "</td></tr>" for c, links in items) + "</tbody></table></div></details>" for g, items in CAT)
    jd = "".join(f'<div class="card"><h3 style="margin:0 0 6px">{E(r)}</h3><ul style="margin:0 0 8px;padding-left:18px;color:var(--mu)">' + "".join(f"<li>{E(x)}</li>" for x in sk) + "</ul><b style='font-size:13px'>Learn it:</b> " + " · ".join(f'<a href="{E(h)}">{E(t)}</a>' for t, h in links) + "</div>" for r, sk, links in JD)
    n = sum(len(i) for _, i in CAT)
    return f"""<style>.sm-t{{overflow:auto;margin-top:10px}}.sm-t table{{width:100%;border-collapse:collapse;font-size:14.5px}}.sm-t th,.sm-t td{{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}.sm-t th{{background:var(--surface-2)}}.sm-t a,.card a{{color:var(--brand);font-weight:600}}
.sm-q{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}}.sm-q input{{flex:1;min-width:220px;border:1px solid var(--line);border-radius:12px;padding:11px 14px;font:inherit;background:var(--surface);color:var(--ink)}}</style>
<section style="padding-top:28px"><div class="wrap">
<div class="card" style="border:2px solid #6C4CF5;margin-bottom:24px"><b>How the pieces fit:</b> a <b>skill</b> is a reusable method; a <b>tool</b> gives access or performs an action; <b>evals, memory and context management</b> are parts of the system around them. They work together. There's no fixed list of "all AI skills": you can create a new skill for any repeatable task.</div>
<h2 class="sec-h" style="font-size:26px">Learn these first, in this order</h2><p class="sub">Seven skills that make you effective with AI at work, each linked to its SkillNavora course.</p><ol style="display:grid;gap:10px;padding:0;margin:0 0 30px">{path}</ol>
<h2 class="sec-h" style="font-size:26px">The full AI skills catalogue ({n} capabilities)</h2><p class="sub">Every capability, and where to learn it on SkillNavora.</p>
<div class="sm-q"><input id="sm-q" type="search" placeholder="Search a skill, e.g. RAG, OCR, routing, PRD…" aria-label="Search skills"></div>
<div style="display:grid;gap:12px" id="sm-list">{groups}</div>
<h2 class="sec-h" style="font-size:26px;margin-top:30px">What AI-era job descriptions ask for</h2><p class="sub">Skills that commonly appear in job postings for these roles, and where to learn each.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px">{jd}</div>
</div></section>
<script>(function(){{var q=document.getElementById('sm-q');q.addEventListener('input',function(){{var t=q.value.toLowerCase();document.querySelectorAll('#sm-list .sm-g').forEach(function(g){{var any=0;g.querySelectorAll('tbody tr').forEach(function(r){{var ok=!t||r.textContent.toLowerCase().indexOf(t)>-1;r.hidden=!ok;if(ok)any++}});g.hidden=!any;if(t)g.open=true}})}})}})();</script>"""
