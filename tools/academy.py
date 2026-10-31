"""AI Skills Academy: one section that holds every AI/PM mini-course (page + PDF + interactive artifact tab)."""
import html
import course_builder, course_webauto, course_aiengineer, evals_course as ev, course_context, course_skills, course_brain, course_browser, course_orch, courses_more as M
E = html.escape
ARTIFACT = "ai-academy-interactive.html"   # on skillnavora.in, opens in the same tab
EVALS = {"slug": "evals", "title": "AI Evals for Product Managers", "page": "ai-evals.html", "pdf": "AI_Evals_for_Product_Managers.pdf", "classes": ev.CLASSES,
         "intro": "Measure, improve and safely launch AI features: criteria, datasets, LLM-as-judge, RAG and agent evals, safety, monitoring."}
CORE = [("1", course_context.COURSE, "context"), ("2", course_skills.COURSE, "skills"), ("3", course_brain.COURSE, "brain"), ("5", EVALS, "evals"), ("6", course_browser.COURSE, "browser"), ("7", course_orch.COURSE, "orch")]
ADV = [(C, C["slug"]) for C in M.ALL]
RESEARCH = ("4", "Research & data analysis", "data-science/index.html", "SQL, Excel, Python, Power BI, statistics and AI for analysts in the Data Science & AI handbook.")

def card(C, tab, num=None, R=""):
    n = f'<span class="ac-n">Skill {num}</span>' if num else '<span class="ac-n">Advanced AI PM</span>'
    return (f'<article class="ac-card">{n}<h3>{E(C["title"])}</h3><p>{E(C["intro"])}</p><span class="ac-meta">{len(C["classes"])} classes · basic to advanced · PDF</span>'
            f'<div class="ac-acts"><a class="btn btn-primary btn-sm" href="{R}{C["page"]}">Open lessons</a><a class="btn btn-line btn-sm" href="{R}handbook/{C["pdf"]}">PDF</a>'
            f'<a class="btn btn-line btn-sm" href="{R}{ARTIFACT}#{tab}">Interactive</a></div></article>')

CSS = """<style>.ac-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}.ac-card{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px}
.ac-card h3{margin:0;font-size:18px}.ac-card p{margin:0;color:var(--mu);font-size:14.5px}.ac-n{font:700 11px var(--body);letter-spacing:.08em;text-transform:uppercase;color:#6C4CF5}.ac-meta{font-size:12.5px;color:var(--mu)}
.ac-acts{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto;padding-top:8px}.ac-h{font-size:22px;margin:22px 0 10px}</style>"""

def grid(R=""):
    core = [card(C, t, n, R) for n, C, t in CORE]
    core.insert(3, f'<article class="ac-card"><span class="ac-n">Skill 4</span><h3>{E(RESEARCH[1])}</h3><p>{E(RESEARCH[3])}</p><span class="ac-meta">Full handbook · 129 lessons</span><div class="ac-acts"><a class="btn btn-primary btn-sm" href="{R}{RESEARCH[2]}">Open handbook</a><a class="btn btn-line btn-sm" href="{R}ai-skills-map.html">Skills map</a></div></article>')
    tools = card(course_builder.COURSE, "builder-tools", None, R).replace('<span class="ac-n">Advanced AI PM</span>', '<span class="ac-n">AI tools · start here</span>')
    tools += card(course_webauto.COURSE, "web-automation", None, R).replace('<span class="ac-n">Advanced AI PM</span>', '<span class="ac-n">AI tools · automation</span>')
    career = card(course_aiengineer.COURSE, "ai-engineer", None, R).replace('<span class="ac-n">Advanced AI PM</span>', '<span class="ac-n">Career path · Other programs</span>')
    return (CSS + '<h3 class="ac-h">AI Engineer career path (everything an AI engineer does)</h3><div class="ac-grid">' + career + '</div>'
            + '<h3 class="ac-h">AI tools: build and automate with Claude, ChatGPT, Codex, Gemini, Lovable and Playwright</h3><div class="ac-grid">' + tools + '</div>'
            + '<h3 class="ac-h">The 7 core AI skills (learn in this order)</h3><div class="ac-grid">' + "".join(core) + '</div>'
            '<h3 class="ac-h">Advanced AI product management</h3><div class="ac-grid">' + "".join(card(C, t, None, R) for C, t in ADV) + "</div>")

def hub():
    return f"""<section style="padding-top:28px"><div class="wrap">
<div class="card" style="border:2px solid #6C4CF5;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between"><div style="max-width:720px"><b>One place for every AI skill course.</b> Each course has lessons on the website, a free PDF and an interactive version. Part of the <a href="program/ai-product-management.html">AI Product Management</a> and <a href="program/genai-launchpad.html">GenAI Launchpad</a> programs.</div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn btn-primary" href="ai-skills-map.html">AI Skills Map</a><a class="btn btn-line" href="{ARTIFACT}">Interactive academy</a></div></div>
{grid()}</div></section>"""

def program_section(cid):
    who = "AI product managers" if cid == "ai-pm" else "every professional using GenAI"
    return f"""<section id="academy" class="tint"><div class="wrap"><div class="kicker">Included free · AI Skills Academy</div><h2 class="sec-h">AI skills courses for {who}</h2>
<p class="sub" style="max-width:760px">Every course comes with lessons, a PDF and an interactive version: the 7 core AI skills plus advanced AI product topics. <a href="../ai-academy.html">Open the AI Skills Academy →</a></p>{grid("../")}</div></section>"""
