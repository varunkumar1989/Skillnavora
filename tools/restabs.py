"""Builds the four tabs of the public Resources & AI tools page (resources.html)."""
import json, os, html

E = html.escape
DS_SITE = "/data-science/"      # where the built Data Science & AI handbook is hosted
DS_REPO = "https://github.com/varunkumar1989/data-science-and-ai"
CATALOG = "/home/user/data-science-and-ai/course/catalog.json"


def ext(label, desc, url, tag=None):
    t = f'<span class="ftag">{E(tag)}</span>' if tag else ""
    return f'<a class="card tool" href="{E(url)}" target="_blank" rel="noopener">{t}<h3 style="margin-top:8px">{E(label)} ↗</h3><p>{E(desc)}</p></a>'


def grid(items, cols="g4"):
    return f'<div class="grid {cols}">' + "".join(ext(*i) for i in items) + "</div>"


def h(t, sub=None):
    return f'<h3 class="h3s hb-h">{E(t)}</h3>' + (f'<p class="meta" style="margin:-4px 0 12px">{E(sub)}</p>' if sub else "")


def hero(kicker, title, text, acts):
    return (f'<div class="hb-hero"><div><div class="kicker">{E(kicker)}</div><h2 class="h2s" style="margin:4px 0 6px">{E(title)}</h2><p class="meta" style="margin:0 0 14px">{E(text)}</p>'
            f'<div class="hb-acts">{acts}</div></div></div>')


def btn(label, url, primary=False, gate=True, new=True):
    cls = "btn btn-primary btn-sm" if primary else "btn btn-line btn-sm"
    return f'<a class="{cls}" href="{E(url)}"' + (' target="_blank" rel="noopener"' if new else "") + (' data-gate="1"' if gate else "") + f'>{E(label)}</a>'


def catalog():
    if os.path.exists(CATALOG):
        return json.load(open(CATALOG))
    return {"tracks": []}


def lesson_rows(track):
    rows = []
    for L in track["lessons"]:
        rows.append(f'<div class="hb-row hb-multi"><span class="hb-n">{L["num"]}</span><span>{E(L["title"])}' + (f'<em>{E(L["live"])}</em>' if L.get("live") else "") +
                    f'</span><span class="hb-links"><a href="{DS_SITE}lessons/{L["file"]}" target="_blank" rel="noopener" data-gate="1">Read ↗</a>'
                    f'<a href="{DS_SITE}pdf/{L["track"]}/{L["pdf"]}" target="_blank" rel="noopener" data-gate="1">PDF ↗</a></span></div>')
    return "".join(rows)


def ds_tab(cfg):
    cat = catalog()
    tracks = cat["tracks"]
    n_les = sum(len(t["lessons"]) for t in tracks)
    art = cfg.get("dsa_artifact") or ""
    ds_art = cfg.get("ds_artifact") or ""
    acts = (btn("Open the handbook ↗", DS_SITE, True) + btn("All SkillNavora handbooks →", "handbooks/index.html", gate=False, new=False) + (btn("Interactive DSA handbook ↗", art) if art else "") + (btn("Interactive Data Science handbook ↗", ds_art) if ds_art else "") +
            btn("Complete handbook PDFs ↗", DS_SITE + "index.html#downloads") + btn("GitHub ↗", DS_REPO, gate=False))
    out = [hero("AI-First Data Engineer · free for registered learners", "Data Science & AI Handbook by Varun Kumar",
                f"{n_les or 100}+ class-wise lessons in Excel, SQL, Power BI, Tableau, AI for data analysis, Python, DSA, statistics and machine learning, with real outputs, diagrams, quizzes, practice datasets and a PDF for every lesson." if tracks else
                "Class-wise lessons in Excel, SQL, Power BI, Tableau, AI for data analysis, Python, DSA, statistics and machine learning, with real outputs, diagrams, quizzes, practice datasets and a PDF for every lesson.", acts)]
    out.append(f'<div data-res-tools="ai-de"></div>' if False else "")
    if tracks:
        out.append(h("Handbook tracks", "Every lesson opens in the handbook site and has its own PDF. You will be asked for your details once."))
        for t in tracks:
            if t["id"] in ("genai",):
                continue
            out.append(f'<details class="trk"><summary><b>{E(t["name"])}</b><span>{len(t["lessons"])} lessons</span>'
                       f'<a href="{DS_SITE}pdf/tracks/{t["track_pdf"]}" target="_blank" rel="noopener" data-gate="1" onclick="event.stopPropagation()">Track PDF ↗</a></summary><div class="hb-list">{lesson_rows(t)}</div></details>')
    out.append(h("Practice datasets and files", "Fictional data you can download for every Excel, SQL, Power BI, Python and ML exercise."))
    out.append(f'<div class="hb-acts" style="margin-bottom:6px">{btn("All practice datasets ↗", DS_SITE + "index.html#datasets")}{btn("Excel practice workbooks ↗", DS_SITE + "index.html#downloads")}</div>')
    out.append(h("Tools for data engineers", "Official sites for the tools used in the AI-First Data Engineer program."))
    out.append('<div class="tgroups" data-res-tools="ai-de"></div>')
    out.append(h("Practice online (free)", "Exercises, quizzes and coding challenges on trusted sites. Each link opens the original page."))
    out.append(grid([
        ("W3Schools Python exercises", "Fill-in-the-blank Python exercises with answers.", "https://www.w3schools.com/python/python_exercises.asp", "Python"),
        ("W3Schools Python quiz", "A multiple-choice Python quiz with score.", "https://www.w3schools.com/quiztest/quiztest.asp?qtest=PYTHON", "Python"),
        ("W3Schools Pandas exercises", "Short exercises on DataFrames.", "https://www.w3schools.com/python/pandas/pandas_exercises.asp", "pandas"),
        ("W3Schools Pandas quiz", "25 questions on pandas.", "https://www.w3schools.com/python/pandas/pandas_quiz.asp", "pandas"),
        ("W3Schools SQL exercises", "SQL practice with a built-in editor.", "https://www.w3schools.com/sql/sql_exercises.asp", "SQL"),
        ("W3Schools SQL quiz", "Test SQL basics.", "https://www.w3schools.com/quiztest/quiztest.asp?qtest=SQL", "SQL"),
        ("W3Schools DSA tutorial and exercises", "Data structures and algorithms explained with animations.", "https://www.w3schools.com/dsa/index.php", "DSA"),
        ("W3Schools Excel tutorial", "Excel formulas, charts and pivot tables.", "https://www.w3schools.com/excel/index.php", "Excel"),
        ("W3Schools Statistics tutorial", "Statistics for data science.", "https://www.w3schools.com/statistics/index.php", "Statistics"),
        ("W3Schools Data Science tutorial", "Python data science introduction.", "https://www.w3schools.com/datascience/default.asp", "Data science"),
        ("SQLBolt", "Interactive SQL lessons in the browser.", "https://sqlbolt.com/", "SQL"),
        ("LeetCode SQL 50", "50 curated SQL interview problems.", "https://leetcode.com/studyplan/top-sql-50/", "SQL"),
        ("HackerRank SQL", "SQL challenges with instant tests.", "https://www.hackerrank.com/domains/sql", "SQL"),
        ("StrataScratch", "Data-interview questions from real companies.", "https://www.stratascratch.com/", "Interview"),
        ("Kaggle Learn", "Free short courses: Python, pandas, SQL, ML.", "https://www.kaggle.com/learn", "Courses"),
        ("NeetCode roadmap", "A guided list of DSA problems.", "https://neetcode.io/roadmap", "DSA"),
    ]))
    out.append(h("Docs worth bookmarking"))
    out.append(grid([
        ("pandas user guide", "Official pandas documentation.", "https://pandas.pydata.org/docs/user_guide/index.html", "Docs"),
        ("scikit-learn user guide", "Machine-learning reference with examples.", "https://scikit-learn.org/stable/user_guide.html", "Docs"),
        ("T-SQL reference", "Microsoft's SQL Server language reference.", "https://learn.microsoft.com/en-us/sql/t-sql/language-reference", "Docs"),
        ("DAX reference", "Every DAX function with examples.", "https://learn.microsoft.com/en-us/dax/dax-function-reference", "Docs"),
        ("PostgreSQL docs", "The reference for PostgreSQL.", "https://www.postgresql.org/docs/", "Docs"),
        ("Apache Airflow docs", "Workflow orchestration.", "https://airflow.apache.org/docs/", "Docs"),
        ("dbt docs", "Transformations in the warehouse.", "https://docs.getdbt.com/", "Docs"),
        ("Spark docs", "PySpark and Spark SQL.", "https://spark.apache.org/docs/latest/", "Docs"),
    ]))
    return "".join(out)


def genai_tab(cfg):
    art = cfg.get("genai_artifact") or ""
    acts = btn("Open the GenAI handbook ↗", DS_SITE + "index.html#t-genai", True) + btn("GenAI Launchpad handbook (482-page PDF) →", "handbooks/index.html#genai", gate=False, new=False) + (btn("Interactive GenAI handbook ↗", art) if art else "") + btn("GenAI Launchpad program →", "program/genai-launchpad.html", gate=False, new=False)
    cat = catalog(); gt = [t for t in cat["tracks"] if t["id"] == "genai"]
    out = [hero("GenAI Launchpad · free for registered learners", "Generative & Agentic AI Handbook", "How LLMs work, prompting, APIs, embeddings and RAG, tool use, agents and MCP, evaluation, fine-tuning, responsible AI and your first AI apps, with runnable examples and a PDF for each lesson.", acts)]
    if gt:
        t = gt[0]
        out.append(h("Handbook lessons", "Read online or download the PDF for each lesson."))
        out.append(f'<details class="trk" open><summary><b>{E(t["name"])}</b><span>{len(t["lessons"])} lessons</span><a href="{DS_SITE}pdf/tracks/{t["track_pdf"]}" target="_blank" rel="noopener" data-gate="1" onclick="event.stopPropagation()">Track PDF ↗</a></summary><div class="hb-list">{lesson_rows(t)}</div></details>')
    out.append(h("Tools for GenAI Launchpad", "Official sites for the AI assistants, builders and automation tools taught in the program."))
    out.append('<div class="tgroups" data-res-tools="genai-launchpad"></div>')
    out.append(h("More AI tools to explore"))
    out.append(grid([
        ("Claude", "Anthropic's assistant for writing, analysis and code.", "https://claude.ai", "Assistant"),
        ("ChatGPT", "OpenAI's assistant.", "https://chatgpt.com", "Assistant"),
        ("Gemini", "Google's assistant with Workspace integration.", "https://gemini.google.com", "Assistant"),
        ("Microsoft Copilot", "AI built into Windows and Microsoft 365.", "https://copilot.microsoft.com", "Assistant"),
        ("Perplexity", "Answers with citations from the web.", "https://www.perplexity.ai", "Search"),
        ("NotebookLM", "Ask questions of your own documents.", "https://notebooklm.google", "Research"),
        ("Google AI Studio", "Try Gemini models and build with the API.", "https://aistudio.google.com", "Build"),
        ("Hugging Face", "Models, datasets and Spaces for open AI.", "https://huggingface.co", "Open models"),
        ("Ollama", "Run open models on your own computer.", "https://ollama.com", "Open models"),
        ("Cursor", "An AI code editor.", "https://cursor.com", "Code"),
        ("Lovable", "Build web apps by chatting.", "https://lovable.dev", "No-code"),
        ("Replit", "Build and host apps in the browser with AI.", "https://replit.com", "No-code"),
        ("n8n", "Open-source workflow automation with AI agents.", "https://n8n.io", "Automate"),
        ("Zapier", "Connect apps and add AI steps.", "https://zapier.com", "Automate"),
        ("Make", "Visual automations.", "https://www.make.com", "Automate"),
        ("Canva", "Design with AI helpers.", "https://www.canva.com", "Design"),
    ]))
    out.append(h("Learn more (free)"))
    out.append(grid([
        ("W3Schools Generative AI tutorial", "Plain-language introduction with prompt examples.", "https://www.w3schools.com/gen_ai/", "Start here"),
        ("Anthropic docs and courses", "Claude API, prompt engineering and MCP.", "https://www.anthropic.com/learn", "Courses"),
        ("Prompt engineering guide (Anthropic)", "Techniques that improve answers.", "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview", "Prompting"),
        ("Google prompting strategies for Gemini", "Prompt design guidance.", "https://ai.google.dev/gemini-api/docs/prompting-strategies", "Prompting"),
        ("OpenAI Cookbook", "Practical examples and guides.", "https://cookbook.openai.com/", "Code"),
        ("Hugging Face LLM course", "A free course on working with LLMs.", "https://huggingface.co/learn/llm-course", "Course"),
        ("DeepLearning.AI short courses", "Short free courses on LLM apps and agents.", "https://www.deeplearning.ai/short-courses/", "Courses"),
        ("Model Context Protocol", "The open standard for connecting AI to tools.", "https://modelcontextprotocol.io/", "Agents"),
    ]))
    return "".join(out)


PORTALS = [("LinkedIn Jobs", "Roles, alerts and recruiters.", "https://www.linkedin.com/jobs/", "Jobs"), ("Naukri", "India's largest job portal.", "https://www.naukri.com", "Jobs"), ("Indeed India", "Job search and company reviews.", "https://in.indeed.com", "Jobs"),
                     ("Wellfound", "Start-up jobs.", "https://wellfound.com", "Start-ups"), ("Instahyre", "Curated tech and product roles.", "https://www.instahyre.com", "Jobs"), ("Cutshort", "Tech and data roles with skills matching.", "https://cutshort.io", "Jobs"),
                     ("Hirist", "IT jobs in India.", "https://www.hirist.tech", "Jobs"), ("Internshala", "Internships and fresher jobs.", "https://internshala.com", "Freshers")]


def portals_html():
    return h("Job portals", "Search roles and set alerts on the biggest Indian and global job sites.") + grid(PORTALS)


def more_tab():
    out = [hero("Useful links", "Other resources & useful links", "Communities, newsletters, YouTube channels, certifications, free datasets and career tools, hand-picked for learners in product, data and AI.", "")]
    out.append(h("Communities"))
    out.append(grid([("Kaggle", "Competitions, notebooks and datasets.", "https://www.kaggle.com", "Data"), ("Stack Overflow", "Programming questions and answers.", "https://stackoverflow.com", "Code"), ("r/datascience", "Reddit community for data science.", "https://www.reddit.com/r/datascience/", "Community"),
                     ("r/ProductManagement", "Reddit community for PMs.", "https://www.reddit.com/r/ProductManagement/", "Community"), ("GitHub", "Host your portfolio and projects.", "https://github.com", "Portfolio"), ("Hugging Face forums", "Open-source AI community.", "https://discuss.huggingface.co", "AI"),
                     ("Mind the Product", "The product community.", "https://www.mindtheproduct.com", "Product"), ("Lenny's Newsletter", "Product and growth writing.", "https://www.lennysnewsletter.com", "Product")]))
    out.append(h("YouTube channels worth following"))
    out.append(grid([("StatQuest", "Statistics and machine learning explained clearly.", "https://www.youtube.com/@statquest", "Stats & ML"), ("3Blue1Brown", "Visual maths and neural networks.", "https://www.youtube.com/@3blue1brown", "Maths"),
                     ("freeCodeCamp", "Full-length courses on coding and data.", "https://www.youtube.com/@freecodecamp", "Courses"), ("Alex The Analyst", "Data analyst career and tutorials.", "https://www.youtube.com/@AlexTheAnalyst", "Data analyst"),
                     ("codebasics", "Data science and analytics in simple English.", "https://www.youtube.com/@codebasics", "Data science"), ("Krish Naik", "Data science and AI tutorials.", "https://www.youtube.com/@krishnaik06", "Data science"),
                     ("Andrej Karpathy", "How LLMs work, from scratch.", "https://www.youtube.com/@AndrejKarpathy", "LLMs"), ("SkillNavora", "Our own channel.", "https://www.youtube.com/@SkillNavora", "SkillNavora")]))
    out.append(h("Certifications and structured learning"))
    out.append(grid([("Microsoft Learn", "Free learning paths and certifications (PL-300 Power BI).", "https://learn.microsoft.com/training/", "Microsoft"), ("Google Cloud Skills Boost", "Hands-on cloud and data labs.", "https://www.cloudskillsboost.google", "Google"), ("AWS Skill Builder", "Free and paid AWS training.", "https://skillbuilder.aws", "AWS"),
                     ("Databricks Academy", "Lakehouse and Spark learning.", "https://www.databricks.com/learn", "Databricks"), ("Snowflake University", "Snowflake training.", "https://learn.snowflake.com", "Snowflake"), ("NPTEL", "Free IIT/IISc courses.", "https://nptel.ac.in", "India"),
                     ("SWAYAM", "Government of India online courses.", "https://swayam.gov.in", "India"), ("Skill India Digital", "Government skilling portal.", "https://www.skillindiadigital.gov.in", "India"), ("Coursera", "University and industry courses.", "https://www.coursera.org", "Courses"), ("edX", "University courses.", "https://www.edx.org", "Courses")]))
    out.append(h("Free datasets"))
    out.append(grid([("Kaggle Datasets", "Thousands of datasets.", "https://www.kaggle.com/datasets", "Data"), ("data.gov.in", "Open government data of India.", "https://www.data.gov.in", "India"), ("UCI Machine Learning Repository", "Classic ML datasets.", "https://archive.ics.uci.edu", "ML"),
                     ("OpenML", "Datasets and experiments.", "https://www.openml.org", "ML"), ("Hugging Face Datasets", "Datasets for AI.", "https://huggingface.co/datasets", "AI"), ("Our World in Data", "Charts and data on global topics.", "https://ourworldindata.org", "Data")]))
    out.append(h("Career tools"))
    out.append(grid([("Canva resume templates", "Design a clean resume.", "https://www.canva.com/resumes/templates/", "Resume"), ("Notion", "Notes, trackers and portfolios.", "https://www.notion.com", "Organise"), ("draw.io", "Free diagrams.", "https://www.drawio.com", "Diagrams"),
                     ("Figma", "Design and prototyping.", "https://www.figma.com", "Design"), ("GitHub Pages", "Host a portfolio site for free.", "https://pages.github.com", "Portfolio"), ("Streamlit Community Cloud", "Deploy a data app for free.", "https://streamlit.io/cloud", "Portfolio")]))
    return "".join(out)


def build(pm_html, cfg, scope=None):
    """Four resource tabs. scope=None: the Resources page (hash links #pm, #data, #genai, #more).
    scope="lms": the same tabs inside the LMS Resources panel, with their own ids and attributes so the LMS tab code ignores them."""
    tabs = [("pm", "Resources for PM"), ("data", "Resources for Data Engineers"), ("genai", "Resources for GenAI"), ("more", "Other resources & links")]
    pre, attr, cls = ("lr-", "data-rtab", "rpanel") if scope else ("", "data-tab", "panel")
    bar = f'<div class="tabs" role="tablist" id="{pre}res-tabs" aria-label="Resources">' + "".join(f'<button role="tab" id="{pre}t-{k}" aria-controls="{pre}p-{k}" {attr}="{k}" aria-selected="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n) in enumerate(tabs)) + "</div>"
    panels = {"pm": pm_html, "data": ds_tab(cfg), "genai": genai_tab(cfg), "more": more_tab()}
    body = "".join(f'<div class="{cls}" id="{pre}p-{k}" role="tabpanel" aria-labelledby="{pre}t-{k}"{"" if i == 0 else " hidden"}>{panels[k]}</div>' for i, (k, _) in enumerate(tabs))
    if scope:
        js = """<script>(function(){var tabs=[].slice.call(document.querySelectorAll('#lr-res-tabs [role=tab]')),panels=[].slice.call(document.querySelectorAll('.rpanel'));
function show(k){tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.rtab===k?'true':'false')});panels.forEach(function(p){p.hidden=p.id!=='lr-p-'+k})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.rtab)})});
var c=new URL(location).searchParams.get('res');show(c&&document.getElementById('lr-p-'+c)?c:'pm')})();</script>"""
        return bar + body + js
    js = """<script>(function(){var tabs=[].slice.call(document.querySelectorAll('#res-tabs [role=tab]')),panels=[].slice.call(document.querySelectorAll('.panel[role=tabpanel]'));
function show(k){if(!document.getElementById('p-'+k))k='pm';tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.tab===k?'true':'false')});panels.forEach(function(p){p.hidden=p.id!=='p-'+k})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.tab);try{history.replaceState(null,'','#'+t.dataset.tab)}catch(e){}})});
function fromHash(){show((location.hash||'#pm').slice(1))}window.addEventListener('hashchange',fromHash);fromHash()})();</script>"""
    return bar + body + js
