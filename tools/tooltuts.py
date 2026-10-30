"""Tool tutorials page: every tool taught in the programs, with its official site, a free official tutorial and our own lesson."""
import json, os, subprocess, html
E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Free official learning pages for each tool (help centres, academies, docs quick-starts).
LEARN = {
    "Jira": "https://www.atlassian.com/software/jira/guides", "Confluence": "https://www.atlassian.com/software/confluence/guides",
    "Asana": "https://academy.asana.com/", "Notion": "https://www.notion.com/help/guides", "Linear": "https://linear.app/docs",
    "Trello": "https://trello.com/guide", "ClickUp": "https://university.clickup.com/", "Productboard": "https://support.productboard.com/",
    "Aha!": "https://www.aha.io/support", "Figma": "https://help.figma.com/", "FigJam": "https://help.figma.com/", "Miro": "https://academy.miro.com/",
    "Balsamiq": "https://balsamiq.com/learn/", "Whimsical": "https://whimsical.com/help", "Slack": "https://slack.com/help",
    "Loom": "https://support.loom.com/", "Mixpanel": "https://docs.mixpanel.com/", "Amplitude": "https://academy.amplitude.com/",
    "Google Analytics 4": "https://skillshop.withgoogle.com/", "SQL": "https://www.w3schools.com/sql/", "Excel / Google Sheets": "https://support.microsoft.com/en-us/excel",
    "Looker Studio": "https://support.google.com/looker-studio", "Hotjar": "https://help.hotjar.com/", "Microsoft Clarity": "https://learn.microsoft.com/en-us/clarity/",
    "Typeform": "https://help.typeform.com/", "Google Forms": "https://support.google.com/docs/answer/6281888", "Maze": "https://help.maze.co/",
    "Dovetail": "https://docs.dovetail.com/", "Postman": "https://academy.postman.com/", "Claude": "https://www.anthropic.com/learn",
    "ChatGPT": "https://help.openai.com/", "Gemini": "https://support.google.com/gemini", "Perplexity": "https://www.perplexity.ai/hub/getting-started",
    "NotebookLM": "https://support.google.com/notebooklm", "Microsoft Copilot": "https://support.microsoft.com/copilot",
    "Claude Code": "https://docs.claude.com/en/docs/claude-code/overview", "Cursor": "https://docs.cursor.com/", "GitHub": "https://skills.github.com/",
    "Lovable": "https://docs.lovable.dev/", "Bolt": "https://support.bolt.new/", "v0": "https://vercel.com/docs/v0", "Replit": "https://docs.replit.com/",
    "Figma Make": "https://help.figma.com/", "n8n": "https://docs.n8n.io/courses/", "Zapier": "https://learn.zapier.com/", "Make": "https://academy.make.com/",
    "Python": "https://docs.python.org/3/tutorial/", "pandas": "https://pandas.pydata.org/docs/getting_started/", "Jupyter": "https://docs.jupyter.org/",
    "Git": "https://git-scm.com/book", "Apache Airflow": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/", "dbt": "https://learn.getdbt.com/",
    "Apache Spark": "https://spark.apache.org/docs/latest/quick-start.html", "Apache Kafka": "https://kafka.apache.org/quickstart",
    "Docker": "https://docs.docker.com/get-started/", "Snowflake": "https://learn.snowflake.com/", "BigQuery": "https://cloud.google.com/bigquery/docs/quickstarts",
    "Databricks": "https://www.databricks.com/learn", "AWS": "https://skillbuilder.aws/", "PostgreSQL": "https://www.postgresql.org/docs/current/tutorial.html",
    "GitHub Copilot": "https://docs.github.com/en/copilot", "Pinecone": "https://docs.pinecone.io/", "Canva": "https://www.canva.com/designschool/",
    "WhatsApp Business": "https://business.whatsapp.com/resources",
}
# Our own lessons: (label, path from the site root). DS lessons are looked up by id prefix in the catalog.
PM = lambda n, t: (f"PM handbook · Module {n}: {t}", f"handbooks/pm/m{n:02d}.html")
OURS = {
    "Claude": [PM(14, "Claude for daily work"), ("GenAI lesson: prompt engineering", "ds:genai-02")], "Claude Code": [PM(15, "Claude Code")],
    "Lovable": [PM(16, "Lovable")], "Replit": [PM(17, "Replit and app builders")], "Bolt": [PM(17, "Replit and app builders")], "v0": [PM(17, "Replit and app builders")],
    "Figma": [("Complete Figma tutorial", "ds:tools-01"), PM(18, "Figma and AI design tools")], "FigJam": [("Complete Figma tutorial (FigJam)", "ds:tools-01")],
    "Figma Make": [("Complete Figma tutorial (Figma Make)", "ds:tools-01"), PM(18, "Figma and AI design tools")],
    "Notion": [PM(19, "Notion and PRD tools")], "Confluence": [PM(19, "Notion and PRD tools")],
    "n8n": [("Complete n8n tutorial", "ds:tools-02"), PM(20, "Zapier, Make and n8n")], "Zapier": [PM(20, "Zapier, Make and n8n")], "Make": [PM(20, "Zapier, Make and n8n")],
    "WhatsApp Business": [PM(21, "AI chatbots for business")], "Slack": [PM(21, "AI chatbots for business")],
    "ChatGPT": [("GenAI lesson: prompt engineering", "ds:genai-02"), PM(13, "AI tools landscape")], "Gemini": [("AI in Excel & Office", "ds:ai-analytics-03"), PM(13, "AI tools landscape")],
    "Microsoft Copilot": [("AI in Excel & Office", "ds:ai-analytics-03")], "Perplexity": [PM(13, "AI tools landscape")], "NotebookLM": [PM(13, "AI tools landscape")],
    "Cursor": [PM(11, "Vibe coding")], "GitHub Copilot": [("GenAI for data work", "ds:genai-11")], "GitHub": [("Modules, packages and Git", "ds:python-13"), ("Portfolio, GitHub and resume", "ds:career-01")],
    "Git": [("Modules, packages and Git", "ds:python-13")], "SQL": [("SQL track (15 lessons)", "ds:sql-01")], "PostgreSQL": [("SQL track (15 lessons)", "ds:sql-01"), ("Python and SQL", "ds:python-23")],
    "Excel / Google Sheets": [("Advanced Excel track (12 lessons)", "ds:excel-01")], "Python": [("Python track (29 lessons)", "ds:python-01")],
    "pandas": [("pandas I–IV", "ds:python-16")], "Jupyter": [("Introduction to Python and Jupyter", "ds:python-01")], "Docker": [("AI with SQL: Docker, Metabase, MinusX", "ds:ai-analytics-02")],
    "Pinecone": [("Embeddings and vector search", "ds:genai-04"), ("RAG", "ds:genai-05")], "Mixpanel": [PM(7, "Product analytics and metrics")],
    "Amplitude": [PM(7, "Product analytics and metrics")], "Google Analytics 4": [PM(7, "Product analytics and metrics")], "Looker Studio": [PM(7, "Product analytics and metrics")],
    "Hotjar": [PM(3, "Problem discovery and research")], "Microsoft Clarity": [PM(3, "Problem discovery and research")], "Typeform": [PM(3, "Problem discovery and research")],
    "Google Forms": [PM(3, "Problem discovery and research")], "Maze": [PM(5, "UX and design collaboration")], "Dovetail": [PM(3, "Problem discovery and research")],
    "Jira": [PM(4, "Problem framing and prioritization")], "Linear": [PM(4, "Problem framing and prioritization")], "Productboard": [PM(4, "Problem framing and prioritization")],
    "Miro": [PM(5, "UX and design collaboration")], "Balsamiq": [PM(5, "UX and design collaboration")], "Whimsical": [PM(5, "UX and design collaboration")],
    "Postman": [PM(9, "Tech 101 and system design"), ("APIs, JSON and web scraping", "ds:python-24")],
}


def data():
    js = "global.window={};const fs=require('fs');eval(fs.readFileSync(process.argv[1],'utf8').replace(/^const /gm,'var '));console.log(JSON.stringify({c:COURSES.map(c=>({id:c.id,name:c.name,g:c.toolGroups||[]})),l:typeof TOOL_LINKS!=='undefined'?TOOL_LINKS:{}}))"
    out = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets/config.js")], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def build():
    d = data()
    cat = json.load(open(os.path.join(ROOT, "data-science/catalog.json")))
    page_of = {f'{t["id"]}-{L["num"]:02d}': L["page"] for t in cat["tracks"] for L in t["lessons"]}
    def href(p):
        return "data-science/" + page_of[p[3:]] if p.startswith("ds:") and p[3:] in page_of else p
    seen, sections = set(), []
    for c in d["c"]:
        cards = []
        for g in c["g"]:
            for t in g["tools"]:
                ours = "".join(f'<a class="tt-our" href="{E(href(p))}">{E(lbl)} →</a>' for lbl, p in OURS.get(t, []) if not p.startswith("ds:") or p[3:] in page_of)
                site, learn = d["l"].get(t, ""), LEARN.get(t, "")
                cards.append(f'<div class="card tt" data-s="{E((t + " " + g["name"]).lower())}"><div class="tt-h"><b>{E(t)}</b><span class="ftag">{E(g["name"])}</span></div>'
                             + (f'<div class="tt-ours">{ours}</div>' if ours else '<p class="meta" style="margin:0">Use the official tutorial below; a SkillNavora lesson is coming.</p>')
                             + '<div class="tt-acts">' + (f'<a href="{E(learn)}" target="_blank" rel="noopener">Free tutorial ↗</a>' if learn else "")
                             + (f'<a href="{E(site)}" target="_blank" rel="noopener">Official site ↗</a>' if site else "") + "</div></div>")
                seen.add(t)
        sections.append(f'<section class="tt-sec" id="tt-{E(c["id"])}"><h2 class="h2s">{E(c["name"])}</h2><div class="grid g3">{"".join(cards)}</div></section>')
    css = """<style>.tt{display:flex;flex-direction:column;gap:10px}.tt-h{display:flex;justify-content:space-between;gap:8px;align-items:baseline}.tt-h b{font-size:16px}
.tt-ours{display:flex;flex-direction:column;gap:4px}.tt-our{font-weight:600;font-size:14px}.tt-acts{display:flex;flex-wrap:wrap;gap:12px;font-size:13.5px;margin-top:auto}
.tt-sec{margin-top:36px}.tt-sec h2{margin-bottom:14px}#tt-q{width:100%;max-width:420px;padding:10px 14px;border:1px solid var(--line,#ddd);border-radius:999px;font:inherit}</style>"""
    js = """<script>(function(){var q=document.getElementById('tt-q');q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();document.querySelectorAll('.tt').forEach(function(c){c.hidden=v&&c.dataset.s.indexOf(v)<0});});})();</script>"""
    jump = " · ".join(f'<a href="#tt-{E(c["id"])}">{E(c["name"])}</a>' for c in d["c"])
    return css + f'<p class="meta" style="margin:0 0 14px">{len(seen)} tools · jump to: {jump}</p><input id="tt-q" type="search" placeholder="Search a tool, e.g. Figma, n8n, SQL…" aria-label="Search tools">' + "".join(sections) + js, len(seen)
