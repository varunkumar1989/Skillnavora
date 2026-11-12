"""Builds the four tabs of the public Resources & AI tools page (resources.html)."""
import json, os, html

E = html.escape
import learnsites
DS_SITE = "/data-science/"      # where the built Data Science & AI handbook is hosted
DS_REPO = "https://github.com/varunkumar1989/data-science-and-ai"
CATALOG = "/home/user/data-science-and-ai/course/catalog.json"
if not os.path.exists(CATALOG):  # no source checkout (e.g. a fresh clone): use the published copy in this repo
    CATALOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data-science", "catalog.json")


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
            if t["id"] in ("genai",) or t.get("extra"):
                continue   # Other programs have their own tab
            out.append(f'<details class="trk"><summary><b>{E(t["name"])}</b><span>{len(t["lessons"])} lessons</span>'
                       f'<a href="{DS_SITE}pdf/tracks/{t["track_pdf"]}" target="_blank" rel="noopener" data-gate="1" onclick="event.stopPropagation()">Track PDF ↗</a></summary><div class="hb-list">{lesson_rows(t)}</div></details>')
    out.append(h("Practice datasets and files", "Fictional data you can download for every Excel, SQL, Power BI, Python and ML exercise."))
    out.append(f'<div class="hb-acts" style="margin-bottom:6px">{btn("All practice datasets ↗", DS_SITE + "index.html#datasets")}{btn("Excel practice workbooks ↗", DS_SITE + "index.html#downloads")}</div>')
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


JOB_ALERTS = [("LinkedIn job alerts", "Save a search and get daily emails.", "https://www.linkedin.com/jobs/", "Alerts"), ("Naukri job alerts", "Create alerts by role, city and salary.", "https://www.naukri.com/", "Alerts"),
              ("foundit (Monster India)", "Jobs and alerts across India.", "https://www.foundit.in/", "Jobs"), ("Glassdoor", "Jobs, salaries and company reviews.", "https://www.glassdoor.co.in/", "Research"),
              ("Y Combinator: Work at a Startup", "Jobs at YC start-ups worldwide.", "https://www.workatastartup.com/", "Start-ups"), ("Remotive", "Remote tech jobs.", "https://remotive.com/", "Remote"),
              ("We Work Remotely", "Remote jobs board.", "https://weworkremotely.com/", "Remote"), ("Google Jobs search", "Search all boards at once.", "https://www.google.com/search?q=product+manager+jobs+india&ibp=htl;jobs", "Search")]
PORTALS = [("LinkedIn Jobs", "Roles, alerts and recruiters.", "https://www.linkedin.com/jobs/", "Jobs"), ("Naukri", "India's largest job portal.", "https://www.naukri.com", "Jobs"), ("Indeed India", "Job search and company reviews.", "https://in.indeed.com", "Jobs"),
                     ("Wellfound", "Start-up jobs.", "https://wellfound.com", "Start-ups"), ("Instahyre", "Curated tech and product roles.", "https://www.instahyre.com", "Jobs"), ("Cutshort", "Tech and data roles with skills matching.", "https://cutshort.io", "Jobs"),
                     ("Hirist", "IT jobs in India.", "https://www.hirist.tech", "Jobs"), ("Internshala", "Internships and fresher jobs.", "https://internshala.com", "Freshers")]


def portals_html():
    return (h("Job portals", "Search roles and set alerts on the biggest Indian and global job sites.") + grid(PORTALS)
            + h("Latest jobs and daily job alerts", "Set an alert once and get new openings in your inbox every day.") + grid(JOB_ALERTS))


def more_tab():
    out = [hero("Useful links", "Other resources & useful links", "Communities, newsletters, YouTube channels, certifications, free datasets and career tools, hand-picked for learners in product, data and AI.", "")]
    out.append('<div id="news"></div>' + h("Daily newsletters & latest AI and tech news", "Subscribe to stay current. Each opens the publisher's own site."))
    out.append(grid(NEWS))
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


QUICK = {
    "pm": [("Study Library (all material)", "study-library.html#aipm"), ("Learning sites for PM", "#learn-pm"), ("AI builder tools (how-to)", "ai-builder-tools.html"), ("Webhooks & Playwright MCP", "web-automation.html"), ("AI Skills Academy", "ai-academy.html"), ("AI Skills Map", "ai-skills-map.html"), ("Context engineering (PDF)", "context-engineering.html"), ("AI skills & templates (PDF)", "ai-skills.html"), ("Orchestration (PDF)", "agent-orchestration.html"), ("PRD library (120 ideas)", "prd-library.html"), ("AI PRD Writer", "prd-writer.html"), ("AI PM Toolkit", "pm-toolkit.html"), ("AI Evals (PDF)", "ai-evals.html"), ("Browser automation (PDF)", "browser-automation.html"), ("AI second brain (PDF)", "ai-second-brain.html"), ("PM handbook", "handbooks/index.html#pm"), ("Top 100 PM questions", "questions.html#pm"), ("AI product sense Q&A (86)", "questions.html#aips"), ("PM practice test", "tests.html#pm"), ("Practice Lab", "lab.html#pm"), ("Tool tutorials", "tools.html#tt-ai-pm"), ("AI Agents & MCP for PMs", "handbooks/index.html#genai")],
    "data": [("SQL, Excel & Python practice sites", "#learn-data"), ("BRD & FRD (business analyst)", "brd-frd.html"), ("Data Science & AI handbook", "data-science/index.html"), ("DSA", "handbooks/index.html#dsa"), ("Top 100 data questions", "questions.html#data"), ("Data practice test", "tests.html#data"), ("Practice Lab: run SQL, Excel, Python", "lab.html#data"), ("Tool tutorials", "tools.html#tt-ai-de"), ("Job board", "jobs.html")],
    "genai": [("Study Library (all material)", "study-library.html#genai"), ("GenAI learning sites", "#learn-genai"), ("AI builder tools (how-to)", "ai-builder-tools.html"), ("Webhooks & Playwright MCP", "web-automation.html"), ("AI Skills Academy", "ai-academy.html"), ("AI Skills Map", "ai-skills-map.html"), ("Context engineering (PDF)", "context-engineering.html"), ("AI skills & templates (PDF)", "ai-skills.html"), ("Orchestration (PDF)", "agent-orchestration.html"), ("AI Evals (PDF)", "ai-evals.html"), ("Browser automation (PDF)", "browser-automation.html"), ("AI second brain (PDF)", "ai-second-brain.html"), ("GenAI Launchpad handbook", "handbooks/index.html#genai"), ("Top 100 GenAI questions", "questions.html#genai"), ("GenAI practice test", "tests.html#genai"), ("Practice Lab + prompt checker", "lab.html#genai"), ("Tool tutorials", "tools.html#tt-genai-launchpad"), ("Claude Code tutorial", "handbooks/index.html#genai")],
    "other": [("Study Library (AI Engineer tab)", "study-library.html#aieng"), ("Learning sites", "#learn-other"), ("AI Engineer", "#op-ai-engineer"), ("SFMC", "#op-sfmc"), ("Digital marketing", "#op-marketing"), ("Content creation", "#op-content"), ("FDE", "#op-fde"), ("Public speaking", "#op-speaking"), ("Practice test", "tests.html#other"), ("Interview questions", "questions.html#other")],
    "more": [("Newsletters & AI news", "#news"), ("Job alerts", "jobs.html#portals-box"), ("Communities", "#more"), ("Free datasets", "#more"), ("Other programs", "handbooks/index.html#other")],
}


def quick(k):
    return '<nav class="qlinks" aria-label="Quick links"><b>Quick links</b>' + "".join(f'<a href="{E(u)}">{E(t)}</a>' for t, u in QUICK[k]) + "</nav>"


NEWS = [("TLDR AI", "Daily 5-minute AI and tech news.", "https://tldr.tech/ai", "AI news"), ("The Rundown AI", "Daily AI news and tools.", "https://www.therundown.ai/", "AI news"),
        ("Ben's Bites", "AI news and how people use it.", "https://www.bensbites.com/", "AI news"), ("The Batch (DeepLearning.AI)", "Weekly AI news by Andrew Ng's team.", "https://www.deeplearning.ai/the-batch/", "AI weekly"),
        ("Lenny's Newsletter", "Product, growth and careers.", "https://www.lennysnewsletter.com/", "Product"), ("Product Hunt Daily", "New products every day.", "https://www.producthunt.com/newsletters", "Product"),
        ("Data Elixir", "Weekly data science picks.", "https://dataelixir.com/", "Data"), ("Data Engineering Weekly", "Data engineering news.", "https://www.dataengineeringweekly.com/", "Data"),
        ("Inc42", "Indian start-up and tech news.", "https://inc42.com/", "India tech"), ("YourStory", "Indian start-ups and founders.", "https://yourstory.com/", "India tech"),
        ("Morning Brew", "Daily business news.", "https://www.morningbrew.com/", "Business"), ("Import AI", "Weekly AI research digest.", "https://importai.substack.com/", "AI research")]


OTHER = [  # (track id, guide page, free official courses)
    ("sfmc", "guides/sfmc.html", [("Trailhead: Marketing Cloud Engagement", "Free official Salesforce modules and badges.", "https://trailhead.salesforce.com/", "Course"),
                                   ("AMPscript guide", "Salesforce Developers reference.", "https://developer.salesforce.com/docs/marketing/marketing-cloud-ampscript/guide/", "Docs"),
                                   ("Marketing Cloud help", "Official product documentation.", "https://help.salesforce.com/", "Docs"),
                                   ("Salesforce certifications", "Exam guides for Email Specialist, Admin, Developer, Consultant.", "https://trailhead.salesforce.com/credentials/administratoroverview", "Certification")]),
    ("marketing", "guides/digital-marketing.html", [("Google Skillshop", "Free Google Ads and Analytics certifications.", "https://skillshop.withgoogle.com/", "Certification"),
                                                     ("Meta Blueprint", "Free Facebook and Instagram ads courses.", "https://www.facebook.com/business/learn", "Course"),
                                                     ("HubSpot Academy", "Free inbound, SEO, email and content courses.", "https://academy.hubspot.com/", "Course"),
                                                     ("Google Search Central: SEO starter guide", "Official SEO basics.", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide", "Docs")]),
    ("content", "guides/content-creation.html", [("YouTube Creators", "Official lessons on growing a channel.", "https://www.youtube.com/creators/", "Course"),
                                                  ("Instagram for Creators", "Reels, growth and monetisation tips.", "https://creators.instagram.com/", "Guide"),
                                                  ("Canva Design School", "Free design courses and templates.", "https://www.canva.com/designschool/", "Course"),
                                                  ("CapCut tutorials", "Video editing basics.", "https://www.capcut.com/resource", "Tool")]),
    ("fde", "guides/fde.html", [("Anthropic: Building effective agents", "How production AI agents are designed.", "https://www.anthropic.com/engineering/building-effective-agents", "Guide"),
                                 ("Claude and Agent SDK docs", "Build and deploy AI solutions.", "https://docs.claude.com/", "Docs"),
                                 ("Model Context Protocol", "Connect AI to customer systems.", "https://modelcontextprotocol.io/", "Docs"),
                                 ("DeepLearning.AI short courses", "Free courses on RAG, agents and evaluation.", "https://www.deeplearning.ai/short-courses/", "Course")]),
    ("speaking", "guides/public-speaking.html", [("Toastmasters International", "Practice speaking with feedback in clubs near you.", "https://www.toastmasters.org/", "Practice"),
                                                  ("TED talks", "Learn from great speakers.", "https://www.ted.com/", "Watch"),
                                                  ("Microsoft Speaker Coach", "AI feedback on pace and fillers in PowerPoint.", "https://support.microsoft.com/office/rehearse-your-slide-show-with-speaker-coach-cd7fc941-5c3b-498c-a225-83ef3f64f07b", "Tool"),
                                                  ("Yoodli AI speech coach", "Practise talks and interviews with AI feedback.", "https://yoodli.ai/", "Tool")]),
]


FDE_ART = "https://claude.ai/artifact/YcVe9ENf1hZJfk1yTZcxMA"
FDE_STAGES = [(1, "Programming", "Programming foundations"), (2, "Applied", "Applied AI"), (3, "Agent", "Agent development"), (4, "Application", "Application development"),
              (5, "Production", "Production deployment"), (6, "Enterprise", "Enterprise projects"), (7, "Professional", "Career and business readiness")]


def fde_box():
    """FDE handbook block: the interactive handbook (Claude artifact) and the 23 PDFs in handbook/fde/."""
    rd = lambda f: f"read.html?doc=handbook/fde/{f}"
    art = f'<a class="btn btn-primary btn-sm" href="{FDE_ART}" target="_blank" rel="noopener" data-nogate>Open the interactive FDE handbook ↗</a>'
    top = art + btn("Complete handbook PDF (239 pages)", rd("FDE-Complete-Handbook.pdf"), new=False) + btn("Programme guide PDF", rd("FDE-00-Programme-Guide.pdf"), new=False)
    stages = "".join(btn(f"Stage {n}: {t}", rd(f"FDE-Stage-{n}-{w}.pdf"), new=False) for n, w, t in FDE_STAGES)
    mods = "".join(btn(f"Module {n}", rd(f"FDE-Module-{n:02d}.pdf"), new=False) for n in range(1, 15))
    return ('<div class="card" style="margin:14px 0 6px;border:2px solid var(--brand,#6C4CF5)"><div class="kicker">FDE handbook</div>'
            '<h3 style="margin:6px 0 4px;font-size:19px">From Non-Coder to Enterprise AI Builder: Learn, Build, Deploy, Get Hired and Launch Your AI Business.</h3>'
            '<p class="meta" style="margin:0 0 10px">Four career tracks, a seven-stage roadmap, 14 modules with every topic explained, three industry projects, a 48-tool directory and interview, demo, agency and sales preparation.</p>'
            f'<div class="hb-acts" style="margin:0 0 10px">{top}</div><p class="meta" style="margin:6px 0 6px"><b>Stage handbooks</b></p><div class="hb-acts" style="margin:0 0 10px">{stages}</div>'
            f'<p class="meta" style="margin:6px 0 6px"><b>Module handbooks</b></p><div class="hb-acts">{mods}</div></div>')


def course_card():
    """The Complete Digital Marketing Course: one course block under Digital Marketing.
    Chapters 1 and 2 are ready and link to their PDF pages (lessons open on their own page).
    Chapters 3 to 19 are shown as coming soon until their PDF is ready. Data: tools/dm_course.json."""
    import json as _j
    D = _j.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dm_course.json")))
    def rd(file, page): return f"read.html?doc={file}&page={page}"
    c1, c2 = D["ch1"], D["ch2"]
    P1 = c1["pages"]; P2 = c2["pages"]
    L1 = [("How to use the course: 4 paths", P1["1-paths"]), ("4 free tools to make content", P1["1-tools"]), ("Study habits and workbook", P1["1-workbook"]),
          ("Questions people ask first", P1["1-faq"]), ("30,000-foot view of digital marketing", P1["1-funnel"])]
    L2 = [("2.1 Why market research works", P2["2-1"]), ("2.2 Set up a Google Forms survey", P2["2-2"]), ("2.3 Share your survey", P2["2-3"]),
          ("2.4 Read the answers in Google Sheets", P2["2-4"]), ("2.5 Get feedback without a survey", P2["2-5"]), ("2.6 Assignment and checklist", P2["2-6"])]
    def lessons(items, file):
        return '<ul class="mf-ll" style="margin:6px 0 0;padding-left:18px">' + "".join(f'<li><a href="{E(rd(file, pg))}">{E(t)}</a> <span class="meta">· page {pg}</span></li>' for t, pg in items) + "</ul>"
    ch = [
      ("1", "Introduction", "Ready", lessons(L1, c1["file"]), btn("Open Chapter 1 (PDF)", rd(c1["file"], 1), True, gate=False, new=False) + btn("Interactive pictures ↗", "https://claude.ai/artifact/LJrGBHbd5ohTQebDsXyo6p", gate=False)),
      ("2", "Market Research", "Ready", lessons(L2, c2["file"]), btn("Open Chapter 2 (PDF)", rd(c2["file"], 1), True, gate=False, new=False) + btn("Practice workshop ↗", "https://claude.ai/artifact/XQhCWixR7eip5riUcSN3nd", gate=False)),
    ]
    import os as _o
    _P3 = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "ch3_pages.json")))
    _f3 = "handbook/Skillnavora-Chapter-3-Make-A-Website.pdf"
    L3 = [("3.1 Why use WordPress?", _P3["3.1"]), ("3.2 WordPress.org or WordPress.com?", _P3["3.2"]), ("3.3 Build the site in five steps", _P3["3.3"]), ("3.4 Free business email", _P3["3.4"]), ("3.5 Business email in Gmail", _P3["3.5"]), ("3.6 Free SSL (https)", _P3["3.6"]), ("3.7 Verify your domain (deadline)", _P3["3.7"]), ("3.8 Assignment and final project", _P3["3.8"])]
    ch.append(("3", "Make a Website (WordPress)", "Ready", lessons(L3, _f3), btn("Open Chapter 3 (PDF)", rd(_f3, 1), True, gate=False, new=False) + btn("Build workshop ↗", "https://claude.ai/artifact/6esoj7rdbTt4G7PRkEg6Kn", gate=False)))
    _P4 = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "ch4_pages.json")))
    _f4 = "handbook/Skillnavora-Chapter-4-Email-Marketing.pdf"
    L4 = [("4.1 Why email is your owned channel", _P4["4.1"]), ("4.2 Create the email account", _P4["4.2"]), ("4.3 Why not just use Gmail?", _P4["4.3"]), ("4.4 Opt-in forms and pop-ups", _P4["4.4"]), ("4.5 Subject lines that get opened", _P4["4.5"]), ("4.6 Create and send a campaign", _P4["4.6"]), ("4.7 Measure the results", _P4["4.7"]), ("4.8 Assignment and resources", _P4["4.8"])]
    ch.append(("4", "Email Marketing and List Building", "Ready", lessons(L4, _f4), btn("Open Chapter 4 (PDF)", rd(_f4, 1), True, gate=False, new=False) + btn("Email workshop ↗", "https://claude.ai/artifact/EKRRKMWKMo4fLpVP8Wjqq5", gate=False)))
    _P5 = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "ch5_pages.json")))
    _f5 = "handbook/Skillnavora-Chapter-5-Copywriting.pdf"
    L5 = [("5.1 Write faster with AI", _P5["5.1"]), ("5.2 What is copywriting?", _P5["5.2"]), ("5.3 The AIDA formula", _P5["5.3"]), ("5.4 Eleven headline rules", _P5["5.4"]), ("5.5 Features into benefits", _P5["5.5"]), ("5.6 Five CTA rules", _P5["5.6"]), ("5.7 Write like your customers talk", _P5["5.7"]), ("5.8 Assignment: 25 headlines", _P5["5.8"])]
    ch.append(("5", "Conversion Copywriting", "Ready", lessons(L5, _f5), btn("Open Chapter 5 (PDF)", rd(_f5, 1), True, gate=False, new=False) + btn("Copywriting workshop ↗", "https://claude.ai/artifact/VZpxqPbTXuyBqNfMotBTfi", gate=False)))
    _P6 = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "ch6_pages.json")))
    _f6 = "handbook/Skillnavora-Chapter-6-SEO.pdf"
    _T6 = [("6.1", "What SEO is"), ("6.2", "The four strategic questions"), ("6.3", "Five metrics to measure SEO"), ("6.4", "Homepage SEO"), ("6.5", "Google Search Console setup"), ("6.6", "Website speed"), ("6.7", "Mobile SEO"), ("6.8", "Keyword funnel"), ("6.9", "Brainstorming keywords"), ("6.10", "Filtering keywords"), ("6.11", "Competitor analysis"), ("6.12", "Titles, URLs and descriptions"), ("6.13", "Image optimisation"), ("6.14", "Content and headings"), ("6.15", "Internal and external links"), ("6.16", "Backlinks that matter"), ("6.17", "Outreach and reclaiming links"), ("6.18", "Content that earns links"), ("6.19", "Publishing on high-authority platforms"), ("6.20", "The Poster Boy Formula"), ("6.21", "Student questions, part 1"), ("6.22", "Student questions, part 2"), ("6.23", "Local SEO and Business Profile"), ("6.24", "Final assignment and quiz")]
    L6 = [(n + " " + tt, _P6[n]) for n, tt in _T6]
    ch.append(("6", "Search Engine Optimization (SEO)", "Ready", lessons(L6, _f6), btn("Open Chapter 6 (PDF)", rd(_f6, 1), True, gate=False, new=False) + btn("SEO workshop ↗", "https://claude.ai/artifact/HWRB6AY5q3oQVU6dCYD1gq", gate=False)))
    _P7 = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "ch7_pages.json")))
    _f7 = "handbook/Skillnavora-Chapter-7-YouTube-Marketing.pdf"
    _T7 = [("7.1", "YouTube marketing overview"), ("7.2", "Create a channel (personal or brand)"), ("7.3", "Best free YouTube tools"), ("7.4", "Grow subscribers honestly"), ("7.5", "Three channel strategies"), ("7.6", "Video gear"), ("7.7", "Record and edit your first video"), ("7.8", "Ideas from competitor analysis"), ("7.9", "Ideas from keyword research"), ("7.10", "YouTube SEO"), ("7.11", "Custom thumbnails"), ("7.12", "Banner and profile picture"), ("7.13", "Cards and end screens"), ("7.14", "Comments and community"), ("7.15", "Monetisation and sponsorships"), ("7.16", "Analytics: retention and CTR"), ("7.17", "Capstone assignment")]
    L7 = [(n + " " + tt, _P7[n]) for n, tt in _T7]
    ch.append(("7", "YouTube Marketing", "Ready", lessons(L7, _f7), btn("Open Chapter 7 (PDF)", rd(_f7, 1), True, gate=False, new=False) + btn("YouTube planner ↗", "https://claude.ai/artifact/WYKuirtew4pDecTFwfkDKS", gate=False)))
    rest = ["Facebook marketing", "Twitter (X) marketing", "Quora marketing", "Google Ads", "Google Analytics", "Instagram marketing", "Pinterest marketing", "LinkedIn marketing", "Facebook ads", "App marketing", "Old content", "Conclusion"]
    for i, t in enumerate(rest, 8):
        ch.append((str(i), t, "Coming soon", "", ""))
    cards = "".join(
        f'<div class="card" style="min-width:0"><div class="kicker">Chapter {n} · {E(st)}</div><h3 class="h3s">{E(t)}</h3>'
        + (f'{lst}<div class="hb-acts" style="margin-top:10px">{acts}</div>' if lst else '<p class="meta">Being written. It will appear here with its PDF and lessons.</p>')
        + '</div>'
        for n, t, st, lst, acts in ch)
    return ('<h3 class="h3s hb-h" style="margin-top:22px">The Complete Digital Marketing Course</h3>'
            '<p class="meta" style="margin:-4px 0 12px;max-width:72ch">By Varun, for SkillNavora. The full course has 19 chapters, written in simple English. Chapters 1 to 7 are ready now. Each lesson link opens the right page of its PDF.</p>'
            '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))">' + cards + '</div>')


def ai_tab():
    """AI and product tools: every tool link on the site, in one tab. The groups come from config.js (toolGroups), so names, order and links stay in one place."""
    out = [hero("Tools · free official websites", "AI and product tools",
                "Every tool we teach or recommend, grouped by what you use it for. Each name opens the tool's own official website in a new tab.", "")]
    out.append('<div class="tgroups ai-groups" data-res-tools="ai-pm"></div>')
    out.append(h("Tools for data engineers", "Official sites for the tools used in the AI-First Data Engineer program."))
    out.append('<div class="tgroups ai-groups" data-res-tools="ai-de"></div>')
    out.append(h("Tools for GenAI Launchpad", "Official sites for the AI assistants, builders and automation tools taught in the program."))
    out.append('<div class="tgroups ai-groups" data-res-tools="genai-launchpad"></div>')
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
    return "".join(out)


def other_tab(part="all"):
    """part="dm": only the Digital marketing section. part="rest": everything except Digital marketing. part="all": both (unused by the tabs)."""
    cat = catalog(); tr = {t["id"]: t for t in cat["tracks"]}
    if part == "dm":
        out = []
    else:
        out = [hero("Other programs · free complete guides", "SFMC, Digital Marketing, Content Creation, FDE and Public Speaking",
                "Each program has a complete basic-to-advanced guide with worked examples, quizzes and interview questions, a PDF, practice tests and the best free official courses.",
                btn("Practice test", "tests.html#other", True, gate=False, new=False) + btn("Interview questions", "questions.html#other", gate=False, new=False))]
    import course_aiengineer as _ae
    _C = _ae.COURSE
    if part != "dm":
      out.append('<section class="op-sec" id="op-ai-engineer">' + h("AI Engineer: the complete path", "Everything an AI engineer goes through: foundations, ML, LLM engineering, RAG, agents and MCP, fine-tuning, evals, LLMOps and deployment, data, security, system design, a 12-month roadmap, 10 projects and interview prep.")
               + '<div class="hb-acts" style="margin:0 0 12px">' + btn("Open the AI Engineer course", "ai-engineer.html", True, gate=False, new=False) + btn("PDF ↗", "handbook/" + _C["pdf"], new=False)
               + btn("Interactive (all tabs)", "ai-academy-interactive.html#ai-engineer", gate=False, new=False) + btn("Interview questions", "questions.html#genai", gate=False, new=False) + "</div>"
               + '<p class="meta" style="margin:8px 0 6px"><b>Click a class to read it:</b></p><div class="hb-acts" style="margin:0 0 14px">' + "".join(btn(f"{i}. {c[1]}", f"ai-academy-interactive.html#ai-engineer-c{i}", gate=False, new=False) for i, c in enumerate(_C["classes"], 1)) + "</div>"
               + grid([("Hugging Face LLM course", "Free: transformers, fine-tuning, agents.", "https://huggingface.co/learn/llm-course", "Course"), ("LLM Zoomcamp", "Free 10-week hands-on LLM engineering (DataTalks.Club).", "https://github.com/DataTalksClub/llm-zoomcamp", "Course"),
                       ("MLOps Zoomcamp", "Free MLOps course: pipelines, deployment, monitoring.", "https://github.com/DataTalksClub/mlops-zoomcamp", "Course"), ("DeepLearning.AI short courses", "Free 1-hour courses on RAG, agents, evals.", "https://www.deeplearning.ai/short-courses/", "Course"),
                       ("Karpathy: Zero to Hero", "Build neural nets and GPT from scratch.", "https://karpathy.ai/zero-to-hero.html", "Course"), ("Full Stack Deep Learning", "Production ML and LLM engineering.", "https://fullstackdeeplearning.com/", "Course"),
                       ("OWASP Top 10 for LLM apps", "Security risks and controls.", "https://genai.owasp.org/", "Guide"), ("Anthropic: Building effective agents", "Agent design patterns.", "https://www.anthropic.com/research/building-effective-agents", "Guide")]) + "</section>")
    for tid, page, links in OTHER:
        t = tr.get(tid)
        if not t: continue
        if (part == "dm") != (tid in ("marketing", "content")): continue
        L = t["lessons"][0]
        out.append(f'<section class="op-sec" id="op-{tid}">' + h(t["name"], t["desc"]) + '<div class="hb-acts" style="margin:0 0 12px">'
                   + btn("Open the complete guide", page, True, gate=False, new=False) + btn("Guide PDF ↗", DS_SITE + "pdf/" + L["track"] + "/" + L["pdf"])
                   + btn("Read as a lesson ↗", DS_SITE + "lessons/" + L["file"], gate=False) + "</div>" + grid(links)
                   + (course_card() if tid == "marketing" else "") + (fde_box() if tid == "fde" else "") + "</section>")
    return "".join(out)


DATA_TOOLS = [
    ("Power BI Desktop", "Build dashboards and reports. Free download for Windows.", "https://powerbi.microsoft.com/desktop/", "Download"),
    ("Python", "Programming language for data analysis. Install the latest 3.x release.", "https://www.python.org/downloads/", "Download"),
    ("Anaconda (Python + Jupyter)", "Installs Python, Jupyter Notebook and the data libraries in one step.", "https://www.anaconda.com/download", "Download"),
    ("Jupyter Notebook", "Interactive notebooks for Python, charts and analysis.", "https://jupyter.org/install", "Install guide"),
    ("Tableau Public", "Free dashboards and visual analytics.", "https://www.tableau.com/products/public/download", "Download"),
    ("DBeaver (SQL client)", "Free universal database tool for writing and running SQL.", "https://dbeaver.io/download/", "Download"),
    ("PostgreSQL", "Free relational database to practise SQL on your own computer.", "https://www.postgresql.org/download/", "Download"),
    ("pgAdmin", "Graphical admin and query tool for PostgreSQL.", "https://www.pgadmin.org/download/", "Download"),
    ("VS Code", "Code editor for Python, SQL and notebooks.", "https://code.visualstudio.com/download", "Download"),
    ("Git", "Version control for your data projects and portfolio.", "https://git-scm.com/downloads", "Download"),
    ("Google Colab (no install)", "Run Python notebooks in your browser, free.", "https://colab.research.google.com/", "Open"),
]


def data_tools():
    """Tools for data work with download or install links. Official download pages only."""
    return (h("Tools for data work: download or open", "Install these once and you can follow every lesson. Each link goes to the official download page.")
            + grid([(n, d, u, t) for n, d, u, t in DATA_TOOLS]))


def source_html(pm_html, cfg):
    """Every programme block the Learning platform pages are built from (not published as its own page)."""
    feat = lambda kick, h, p, btns: (f'<div class="card" style="margin:0 0 22px;border:2px solid var(--brand,#6C4CF5);background:linear-gradient(135deg,rgba(108,76,245,.07),rgba(34,211,238,.07))">'
        f'<div class="kicker">{kick}</div><h3 style="margin:6px 0 6px;font-size:21px">{h}</h3><p style="margin:0 0 12px;color:var(--mu)">{p}</p><div style="display:flex;flex-wrap:wrap;gap:8px">'
        + "".join(f'<a class="btn {"btn-primary" if i == 0 else "btn-line"} btn-sm" href="{u}">{t}</a>' for i, (t, u) in enumerate(btns)) + '</div></div>')
    prd_box = feat("PRD documents", "PRD library: template, framing guide and 120 PRD ideas", "Learn how top PMs frame a PRD, download the free template, and turn any of 120 ideas across 15 industries into a full PRD with AI.",
                   [("Open the PRD library", "prd-library.html"), ("✨ AI PRD Writer", "prd-writer.html"), ("PRD template (Word)", "handbook/templates/SkillNavora_PRD_Template.doc"), ("AI Evals for PMs (PDF)", "ai-evals.html")])
    ba_box = feat("Business analyst", "BRD &amp; FRD: templates, techniques and 25 project ideas", "BRD vs FRD vs PRD, section-by-section templates, a traced sample, BA techniques and real projects from banking to GenAI.",
                  [("Open the BRD &amp; FRD guide", "brd-frd.html"), ("✨ Write a BRD with AI", "prd-writer.html?doc=brd"), ("✨ Write an FRD with AI", "prd-writer.html?doc=frd")])
    ds_extras_box = feat("Data Science &amp; AI", "Quick reference, glossary, 12-month tracker and supplements",
                         "Cheat sheets for Excel, SQL, DAX, Python, pandas, statistics and ML metrics; a glossary of data and AI terms; a printable 12-month tracker; and supplements on data engineering, cloud, Excel, SQL, governance, interviews and capstones.",
                         [("Open quick reference &amp; supplements", "data-science-extras.html"), ("Cheat sheets (PDF)", "read.html?doc=handbook/data-science-extras/DS-14-Quick-Reference-and-Cheat-Sheets.pdf"),
                          ("Glossary (PDF)", "read.html?doc=handbook/data-science-extras/DS-15-Data-Science-and-AI-Glossary.pdf"), ("12-month tracker (PDF)", "read.html?doc=handbook/data-science-extras/DS-13-12-Month-Roadmap-Tracker.pdf")])
    ctx_box = feat("Context window", "Context window: what a model can see at once",
                   "The context window is the most tokens a model can consider in one request. It covers your prompt, any documents you paste, the conversation so far and the reply. Anything outside it is invisible to the model. For PMs: a longer window fits more material but costs more and can slow responses; put the most important facts near the instructions; use retrieval (RAG) rather than pasting whole libraries; and test answers on long inputs, where quality can drop.",
                   [("Context engineering course", "context-engineering.html"), ("Context windows in the AI PM 2 course", "programme-pm2.html#a2-s12"), ("Tokens and context in the Grokbot course", "grokbot-course.html")])
    return ('<div id="sec-pm">' + quick("pm") + prd_box + ctx_box + pm_html + '</div><div id="sec-genai">' + quick("genai") + genai_tab(cfg) + '</div><div id="sec-data">' + quick("data") + ds_tab(cfg) + ba_box + ds_extras_box + '</div>'
            + other_tab("dm") + '<div id="sec-ai">' + ai_tab() + '</div><div id="sec-data-tools">' + data_tools() + '</div>' + other_tab("rest") + learnsites.tab("", keys=("pm", "data", "genai", "build")))  # the groups the Learning platform uses


# Old Free resources addresses: send each to its one home on the Learning platform
LEGACY = {"pm": "programme-pm.html", "sec-pm": "programme-pm.html", "learn-pm": "programme-pm.html#tools", "genai": "programme-genai.html", "sec-genai": "programme-genai.html",
          "learn-genai": "programme-genai.html#tools", "data": "programme-data.html", "sec-data": "programme-data.html", "learn-data": "programme-data.html#tools",
          "ai": "programme-tool-tutorials.html", "sec-ai": "programme-tool-tutorials.html", "learn-build": "programme-no-code.html#tools", "dm": "programme-digital-marketing.html",
          "op-marketing": "programme-digital-marketing.html", "op-content": "programme-digital-marketing.html", "op-ai-engineer": "programme-ai-engineer.html", "op-fde": "programme-fde.html",
          "op-sfmc": "programme-sfmc.html", "op-speaking": "programme-public-speaking.html", "other": "learning-platform.html", "handbooks": "learning-platform.html",
          "library": "study-library.html", "links": "resources.html#tools", "learn": "resources.html#tools", "dsa": "handbooks/index.html#dsa"}


def _card(href, name, desc, tag, new=False):
    t = ' target="_blank" rel="noopener"' if new or href.startswith("http") else ""
    return (f'<a class="card" href="{E(href)}"{t} style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px"><span class="ftag">{E(tag)}</span>'
            f'<h3 style="margin:8px 0 6px">{E(name)}{" ↗" if t else ""}</h3><p>{E(desc)}</p><span class="go">Open →</span></a>')


def _cards(items, cols="g3"):
    return f'<div class="grid {cols}">' + "".join(_card(*i) for i in items) + "</div>"


def programmes_tab():
    import topic_pages
    items = [(f"{slug}.html", short, topic_pages.DESC[slug], group) for slug, title, short, group, *_ in topic_pages.TOPICS]
    extra = [("ai-academy.html", "AI courses", "Every AI skills course with lessons, PDFs and interactive versions.", "AI courses"),
             ("study-library.html", "Study Library", "Every lesson, class and PDF, listed once under its programme.", "Library"),
             ("handbooks/index.html", "SkillNavora Handbooks", "PM, Data Science & AI, DSA and GenAI handbooks with every PDF.", "Handbooks"),
             ("master-freelancing.html", "Master Freelancing", "Freelance skills, portfolios and client work, department by department.", "Freelancing"),
             ("public-speaking.html", "Public Speaking Practice", "Speak on a topic you did not expect, free speech, shadowing and everyday English, with AI feedback.", "Practice"),
             ("public-speaking.html#ps-tabs-guide", "Complete Public Speaking Guide", "The complete guide: confidence, structure, storytelling, slides, Q&A, video and a 30-day plan.", "Guide")]
    return (h("Programmes", "Each programme's handbooks, lessons, tools and learning links live on its own page on the Learning platform. Pick one to go straight to it.")
            + _cards(items) + h("Libraries, handbooks and more") + _cards(extra))


def tools_tab():
    return (h("Tools", "Every tool for each programme is on that programme's page; these pages collect them.")
            + _cards([("tools-and-resources.html", "Tools for every programme", "One index: open any programme's tools and learning links.", "Tools"),
                      ("tools.html", "Tool tutorials", "Every tool we teach: free official tutorial, official site and our lesson.", "Tutorials"),
                      ("ai.html", "AI Studio", "Free AI tutor, PRD writer, speaking coach and practice.", "AI Studio")])
            + h("Learning sites for coding and other skills", "Coding, DSA, cloud and marketing sites that are not part of a single programme.")
            + learnsites.tab("", keys=("code", "other"))
            + '<div id="more" style="scroll-margin-top:90px"></div>' + quick("more") + more_tab())


def context_tab():
    import course_context
    return (h("Our course", "Prompt & Context Engineering: system prompts, structured outputs, retrieval, context budgets, prompt injection and a capstone.")
            + _cards([("context-engineering.html", "Prompt & Context Engineering", "13 classes from basic to advanced, with templates and interview questions.", "Course"),
                      ("handbook/Prompt_and_Context_Engineering.pdf", "Course PDF", "All 13 context engineering classes, templates and a patterns cheat sheet to print.", "PDF"),
                      ("ai-academy-interactive.html#context", "Interactive version", "Click through each context engineering class with takeaways and exercises.", "Interactive")])
            + h("Related lessons", "Where context engineering is used in other SkillNavora material.")
            + _cards([("data-science/lessons/genai-02-prompt-engineering-in-depth-patterns-templates-few-shot-reas.html", "Prompt engineering in depth", "Patterns, templates, few-shot and reasoning prompts.", "Lesson"),
                      ("ai-skills.html", "AI Skills & Templates", "Package context into reusable skills and templates.", "Course"),
                      ("ai-second-brain.html", "Your AI Second Brain", "Give AI the right context about you and your work.", "Course")])
            + h("Official guides") + grid([(n, "Official documentation and guides.", u, "Guide") for n, u in course_context.COURSE["links"]]))


def evals_tab():
    import evals_course
    return (h("Our course", "AI Evals for Product Managers: criteria, golden sets, metrics, LLM judges, RAG and agent evals, safety and online evals.")
            + _cards([("ai-evals.html", "AI Evals for Product Managers", "13 classes from basic to advanced, with a metrics cheat sheet and interview questions.", "Course"),
                      ("handbook/AI_Evals_for_Product_Managers.pdf", "Course PDF", "All 13 evals classes, the metrics cheat sheet and eval templates to print.", "PDF"),
                      ("ai-academy-interactive.html#evals", "Interactive version", "Click through each evals class with takeaways and exercises.", "Interactive")])
            + h("Related lessons")
            + _cards([("data-science/lessons/genai-09-evaluating-llm-applications-and-building-guardrails-test-set.html", "Evaluating LLM applications", "Test sets, metrics and guardrails, with code.", "Lesson"),
                      ("data-science/lessons/agents-11-agent-evaluation-and-monitoring-measuring-whether-an-agent-w.html", "Agent evaluation and monitoring", "Measuring whether an agent works.", "Lesson"),
                      ("agent-orchestration.html", "Agent Orchestration & Monitoring", "Testing and monitoring workflows in production.", "Course")])
            + h("Official guides and tools") + grid([(n, "Documentation and guides.", u, "Guide") for n, u in evals_course.LINKS]))


def rag_tab():
    L = "data-science/lessons/"
    return (h("How LLMs work", "Tokens, embeddings, transformers and choosing a model.")
            + _cards([(L + "genai-01-how-large-language-models-work-tokens-embeddings-transformer.html", "How large language models work", "Tokens, embeddings and transformers, explained.", "Lesson"),
                      ("ai-models-guide.html", "AI Models and Platforms", "Grok, ChatGPT, Claude, Gemini, Lovable and app builders: what each does and how to choose.", "Guide"),
                      ("handbooks/genai/SkillNavora_Tokens_Context_Cost_Guide.pdf", "Tokens, context and cost guide", "How tokens, context windows and prices work.", "PDF")])
            + h("Retrieval-augmented generation (RAG)", "Search your documents and answer from them, with sources.")
            + _cards([(L + "genai-04-embeddings-and-vector-search-meaning-as-numbers-similarity-a.html", "Embeddings and vector search", "Meaning as numbers, similarity and vector databases.", "Lesson"),
                      (L + "genai-05-retrieval-augmented-generation-rag-build-evaluate-and-improv.html", "RAG: build, evaluate and improve", "A working RAG pipeline in Python, step by step.", "Lesson"),
                      ("ai-academy-interactive.html#context-c6", "Retrieval for PMs", "The decisions a PM owns: scope, chunks, freshness and permissions.", "Class"),
                      ("ai-academy-interactive.html#evals-c9", "Evaluating RAG", "Measure retrieval and answers separately.", "Class"),
                      (L + "genai-10-customising-models-prompting-vs-rag-vs-fine-tuning-lora-dist.html", "Prompting vs RAG vs fine-tuning", "When to use each, with costs and trade-offs.", "Lesson"),
                      (L + "genai-06-tool-use-and-function-calling-letting-llms-query-data-call-a.html", "Tool use and function calling", "Let LLMs query data and call APIs.", "Lesson")])
            + h("Agents built on LLMs")
            + _cards([("ai-agents-guide.html", "How AI Agents Work", "Single agents, multi-agent systems, context and evals.", "Guide"),
                      (L + "genai-08-model-context-protocol-mcp-connecting-ai-assistants-to-your.html", "Model Context Protocol (MCP)", "Connect AI assistants to your tools and data.", "Lesson"),
                      ("grokbot-course.html", "Grokbot course", "Grok API, chatbots, agents and RAG, from zero to commercial.", "Course")])
            + h("Learn more outside SkillNavora")
            + grid([("DeepLearning.AI short courses", "1-hour courses on LLMs, RAG and agents", "https://www.deeplearning.ai/short-courses/", "Course"),
                    ("Hugging Face Learn", "LLM, agents and NLP courses", "https://huggingface.co/learn", "Course"),
                    ("OpenAI Cookbook", "Code examples for LLM apps", "https://cookbook.openai.com/", "Code"),
                    ("Ragas docs", "Evaluate RAG pipelines", "https://docs.ragas.io/", "Evals")]))


def _drop_repeats(html_s, exclude):
    """Remove external link cards whose site is already on the Learning platform, and any group left empty."""
    import re
    if not exclude: return html_s
    ex = {u.rstrip("/") for u in exclude}
    card = re.compile(r'<a class="(card tool|ls-i)" href="(https?://[^"]+)"[^>]*>.*?</a>', re.S)
    html_s = card.sub(lambda m: "" if m.group(2).rstrip("/") in ex else m.group(0), html_s)
    html_s = re.sub(r'<div class="ls-g">[^<]*</div><div class="ls-grid"></div>', "", html_s)
    html_s = re.sub(r'<h3 class="h3s hb-h">[^<]*</h3>(<p class="meta"[^>]*>[^<]*</p>)?<div class="grid g4"></div>', "", html_s)
    return html_s


def build(pm_html, cfg, scope=None, exclude=None):
    """Free resources: five tabs. Programme content lives on the Learning platform; this page links to it once."""
    tabs = [("programmes", "Programmes"), ("tools", "Tools & Learning Sites"), ("context", "Context Engineering"), ("evals", "Evals"), ("rag", "LLMs & RAG")]
    pre, attr, cls = ("lr-", "data-rtab", "rpanel") if scope else ("", "data-tab", "panel")
    bar = f'<div class="tabs" role="tablist" id="{pre}res-tabs" aria-label="Free resources">' + "".join(f'<button role="tab" id="{pre}t-{k}" aria-controls="{pre}p-{k}" {attr}="{k}" aria-selected="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, (k, n) in enumerate(tabs)) + "</div>"
    panels = {"programmes": programmes_tab(), "tools": tools_tab(), "context": context_tab(), "evals": evals_tab(), "rag": rag_tab()}
    panels = {k: _drop_repeats(v, exclude) for k, v in panels.items()}
    if scope:
        panels = {k: v.replace('href="#more"', 'href="resources.html#more"').replace('href="#news"', 'href="resources.html#news"') for k, v in panels.items()}
    body = "".join(f'<div class="{cls}" id="{pre}p-{k}" role="tabpanel" aria-labelledby="{pre}t-{k}"{"" if i == 0 else " hidden"}>{panels[k]}</div>' for i, (k, _) in enumerate(tabs))
    if scope:
        js = """<script>(function(){var tabs=[].slice.call(document.querySelectorAll('#lr-res-tabs [role=tab]')),panels=[].slice.call(document.querySelectorAll('.rpanel'));
function show(k){tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.rtab===k?'true':'false')});panels.forEach(function(p){p.hidden=p.id!=='lr-p-'+k})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.rtab)})});
var c=new URL(location).searchParams.get('res');show(c&&document.getElementById('lr-p-'+c)?c:'programmes')})();</script>"""
        return bar + body + js
    bar = '<div id="res-back" hidden style="margin:0 0 12px"><button type="button" class="btn btn-line btn-sm" id="res-back-btn">← Back to the previous tab</button></div>' + bar
    legacy = "<script>(function(){var m=" + json.dumps(LEGACY) + ",h=(location.hash||'').slice(1);if(m[h]&&!document.getElementById('p-'+h)&&!document.getElementById(h))location.replace(m[h])})();</script>"
    js = """<script>(function(){var tabs=[].slice.call(document.querySelectorAll('#res-tabs [role=tab]')),panels=[].slice.call(document.querySelectorAll('.panel[role=tabpanel]')),back=document.getElementById('res-back'),bb=document.getElementById('res-back-btn'),cur=null,stack=[];
function render(){if(back)back.hidden=stack.length===0}
function show(k,push){if(!document.getElementById('p-'+k))k='programmes';if(push&&cur&&cur!==k)stack.push(cur);cur=k;tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.tab===k?'true':'false')});panels.forEach(function(p){p.hidden=p.id!=='p-'+k});render()}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.tab,true);try{history.replaceState(null,'','#'+t.dataset.tab)}catch(e){}})});
if(bb)bb.addEventListener('click',function(){var prev=stack.pop();if(prev){show(prev,false);try{history.replaceState(null,'','#'+prev)}catch(e){}}});
function fromHash(push){var h=(location.hash||'#programmes').slice(1),el=document.getElementById(h);if(document.getElementById('p-'+h)){show(h,push);return}var p=el&&el.closest('.panel[role=tabpanel]');show(p?p.id.slice(2):'programmes',push);if(el)el.scrollIntoView()}
window.addEventListener('hashchange',function(){fromHash(true)});fromHash(false)})();</script>"""
    return legacy + bar + body + js
