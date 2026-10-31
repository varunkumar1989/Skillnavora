"""Learning sites tab (Resources): the best free and paid sites to learn and practise, grouped by program,
each with a direct link to its tutorial or practice page."""
import html
E = html.escape

# program id -> (program name, blurb, [(group, [(name, what you learn, direct tutorial URL, tag)])])
LEARN = [
 ("pm", "AI Product Management", "Product sense, PRDs, metrics, analytics, design and interview prep.", [
  ("PM interview practice", [
   ("Product Management Exercises", "PM interview questions with answers from the community", "https://www.productmanagementexercises.com/", "Freemium"),
   ("Exponent: PM interview course", "Mock interviews, product sense, execution and estimation", "https://www.tryexponent.com/courses/pm", "Freemium"),
   ("IGotAnOffer: PM interview guides", "Company-specific PM interview guides (Google, Meta, Amazon)", "https://igotanoffer.com/blogs/product-manager", "Free guides"),
   ("Stellar Peers", "Free PM interview guides and frameworks", "https://www.stellarpeers.com/", "Freemium"),
   ("SkillNavora Top 100 PM questions", "Model answers linked to our lessons", "questions.html#pm", "Free"),
   ("SkillNavora AI mock interview", "Answer a PM question and get a score", "practice.html", "Free"),
  ]),
  ("Learn product management", [
   ("Product School: free resources", "Templates, e-books and talks from PMs at top companies", "https://productschool.com/resources", "Free"),
   ("Lenny's Newsletter", "The most-read PM newsletter: growth, PRDs, careers", "https://www.lennysnewsletter.com/", "Freemium"),
   ("SVPG articles (Marty Cagan)", "Product discovery and empowered teams", "https://www.svpg.com/articles/", "Free"),
   ("Mind the Product", "Articles and talks on every PM topic", "https://www.mindtheproduct.com/", "Freemium"),
   ("Atlassian Agile Coach", "Agile, Scrum, Kanban, roadmaps and user stories", "https://www.atlassian.com/agile", "Free"),
   ("Scrum.org: What is Scrum", "The Scrum framework from the source", "https://www.scrum.org/resources/what-is-scrum", "Free"),
   ("Reforge", "Advanced growth and product strategy programs", "https://www.reforge.com/", "Paid"),
  ]),
  ("PRDs and documents", [
   ("ChatPRD", "AI assistant that drafts and reviews PRDs", "https://www.chatprd.ai/", "Freemium"),
   ("SkillNavora PRD library", "Template, framing guide and 120 PRD ideas", "prd-library.html", "Free"),
   ("SkillNavora AI PRD / BRD / FRD Writer", "Write any requirements document with AI", "prd-writer.html", "Free"),
   ("SkillNavora AI PM Toolkit", "Discovery, sizing, A/B tests, launch plans and more", "pm-toolkit.html", "Free"),
   ("PowerChords by Lazo", "PM capabilities: discovery, PRDs, sizing, launch", "https://powerchords.lazo.tools/", "Freemium"),
   ("Notion PRD templates", "Ready PRD templates to duplicate", "https://www.notion.com/templates/category/product-requirements-doc", "Free"),
  ]),
  ("Product tools: delivery and docs", [
   ("Jira guides", "Boards, backlogs, sprints and reports", "https://www.atlassian.com/software/jira/guides", "Free"),
   ("Confluence guides", "Docs, PRDs and team spaces", "https://www.atlassian.com/software/confluence/guides", "Free"),
   ("Linear docs", "Issues, cycles and projects for fast teams", "https://linear.app/docs", "Free"),
   ("Trello guide", "Kanban boards for simple projects", "https://trello.com/guide", "Free"),
   ("Productboard support", "Feedback, prioritisation and roadmaps", "https://support.productboard.com/", "Free"),
   ("Aha! roadmapping guide", "Strategy, roadmaps and requirements", "https://www.aha.io/roadmapping/guide", "Free"),
  ]),
  ("Product analytics", [
   ("Mixpanel docs", "Events, funnels, retention and cohorts", "https://docs.mixpanel.com/", "Free"),
   ("Amplitude Academy", "Product analytics courses and certification", "https://academy.amplitude.com/", "Free"),
   ("Google Analytics 4 (Skillshop)", "Official GA4 courses and certification", "https://skillshop.withgoogle.com/", "Free"),
   ("Hotjar help", "Heatmaps, recordings and surveys", "https://help.hotjar.com/", "Free"),
   ("Microsoft Clarity", "Free heatmaps and session recordings", "https://learn.microsoft.com/en-us/clarity/", "Free"),
  ]),
  ("Design and research", [
   ("Figma Learn", "Interface design, prototyping and Dev Mode", "https://help.figma.com/hc/en-us", "Free"),
   ("Miro Academy", "Workshops, journey maps and story maps", "https://academy.miro.com/", "Free"),
   ("Balsamiq: learn wireframing", "Wireframing basics and UI patterns", "https://balsamiq.com/learn/", "Free"),
   ("Nielsen Norman Group articles", "UX research and usability, from the experts", "https://www.nngroup.com/articles/", "Free"),
   ("Google UX Design Certificate", "Beginner UX course (Coursera)", "https://www.coursera.org/professional-certificates/google-ux-design", "Paid / aid"),
  ]),
 ]),
 ("data", "AI for Data Engineers (Data Science & AI)", "SQL, Excel, Python, Power BI, Tableau, statistics, ML and data interviews.", [
  ("SQL: learn", [
   ("W3Schools MySQL", "MySQL from SELECT to JOINs with a try-it editor", "https://www.w3schools.com/mysql/default.asp", "Free"),
   ("W3Schools SQL", "SQL basics with examples and quizzes", "https://www.w3schools.com/sql/", "Free"),
   ("SQLBolt", "Interactive SQL lessons in the browser", "https://sqlbolt.com/", "Free"),
   ("SQLZoo", "Step-by-step SQL tutorial with live practice", "https://sqlzoo.net/wiki/SQL_Tutorial", "Free"),
   ("Mode SQL tutorial", "SQL for analysts, basic to advanced", "https://mode.com/sql-tutorial/", "Free"),
   ("Select Star SQL", "An interactive SQL book with real data", "https://selectstarsql.com/", "Free"),
   ("Khan Academy: Intro to SQL", "Video lessons and challenges", "https://www.khanacademy.org/computing/computer-programming/sql", "Free"),
  ]),
  ("SQL: practise and interviews", [
   ("DataLemur", "SQL and data-science interview questions from real companies", "https://datalemur.com/", "Freemium"),
   ("LeetCode: SQL 50", "50 essential SQL interview problems", "https://leetcode.com/studyplan/top-sql-50/", "Free"),
   ("HackerRank SQL", "SQL practice from easy to hard, with badges", "https://www.hackerrank.com/domains/sql", "Free"),
   ("W3Schools SQL exercises", "Quick fill-in-the-blank SQL drills", "https://www.w3schools.com/sql/sql_exercises.asp", "Free"),
   ("w3resource SQL exercises", "Hundreds of solved SQL exercises", "https://www.w3resource.com/sql-exercises/", "Free"),
   ("StrataScratch", "Real interview questions in SQL and Python", "https://www.stratascratch.com/", "Freemium"),
   ("Interview Query", "Data-science and analytics interview prep", "https://www.interviewquery.com/", "Freemium"),
   ("SkillNavora Practice Lab", "Run SQL in the browser and spot the trap", "lab.html#data", "Free"),
  ]),
  ("Excel", [
   ("Microsoft Excel training", "Official Excel video training", "https://support.microsoft.com/en-us/excel", "Free"),
   ("Exceljet functions", "Every Excel function explained with examples", "https://exceljet.net/functions", "Free"),
   ("Chandoo.org", "Excel, dashboards and Power Query tutorials", "https://chandoo.org/", "Free"),
   ("W3Schools Excel", "Excel basics and formulas", "https://www.w3schools.com/excel/", "Free"),
  ]),
  ("Python and pandas", [
   ("W3Schools Python", "Python basics with a try-it editor", "https://www.w3schools.com/python/", "Free"),
   ("Kaggle Learn: Python & pandas", "Short hands-on courses with notebooks", "https://www.kaggle.com/learn", "Free"),
   ("Official Python tutorial", "The Python language, from the source", "https://docs.python.org/3/tutorial/", "Free"),
   ("pandas getting started", "Official pandas tutorials", "https://pandas.pydata.org/docs/getting_started/", "Free"),
   ("freeCodeCamp: Data Analysis with Python", "Free certification with projects", "https://www.freecodecamp.org/learn/data-analysis-with-python/", "Free"),
   ("Project Jupyter", "Notebooks for data analysis", "https://docs.jupyter.org/", "Free"),
  ]),
  ("Power BI and Tableau", [
   ("Microsoft Learn: Power BI", "Official Power BI learning paths", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "Free"),
   ("Tableau free training", "Official Tableau training videos", "https://www.tableau.com/learn/training", "Free"),
   ("Tableau Public", "Publish dashboards and learn from others", "https://public.tableau.com/", "Free"),
   ("SQLBI (DAX)", "DAX and data modelling articles and videos", "https://www.sqlbi.com/", "Freemium"),
  ]),
  ("Statistics and machine learning", [
   ("Google Machine Learning Crash Course", "Fast ML introduction with exercises", "https://developers.google.com/machine-learning/crash-course", "Free"),
   ("Coursera: Machine Learning (Andrew Ng)", "The classic ML specialization", "https://www.coursera.org/specializations/machine-learning-introduction", "Paid / audit"),
   ("Khan Academy Statistics", "Statistics and probability, step by step", "https://www.khanacademy.org/math/statistics-probability", "Free"),
   ("scikit-learn tutorials", "Official ML library tutorials", "https://scikit-learn.org/stable/tutorial/index.html", "Free"),
   ("fast.ai", "Practical deep learning for coders", "https://course.fast.ai/", "Free"),
   ("Kaggle competitions", "Practise on real datasets and notebooks", "https://www.kaggle.com/competitions", "Free"),
   ("StatQuest (YouTube)", "Statistics and ML explained simply", "https://www.youtube.com/@statquest", "Free"),
  ]),
  ("Business analysis", [
   ("SkillNavora BRD & FRD guide", "Templates, techniques and 25 project ideas", "brd-frd.html", "Free"),
   ("IIBA BABOK", "The business analysis standard", "https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/", "Paid"),
   ("Modern Analyst", "BA articles, templates and interview questions", "https://www.modernanalyst.com/", "Free"),
  ]),
 ]),
 ("genai", "GenAI Launchpad", "Prompting, LLM apps, agents, MCP and the everyday AI tools.", [
  ("Learn GenAI", [
   ("Claude prompt engineering guide", "Official prompting techniques from Anthropic", "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview", "Free"),
   ("Anthropic Learn", "Courses and guides for using Claude", "https://www.anthropic.com/learn", "Free"),
   ("DeepLearning.AI short courses", "1-hour courses on LLMs, RAG and agents", "https://www.deeplearning.ai/short-courses/", "Free"),
   ("Hugging Face Learn", "LLM, agents and NLP courses", "https://huggingface.co/learn", "Free"),
   ("Prompting Guide", "Prompt techniques with examples", "https://www.promptingguide.ai/", "Free"),
   ("Learn Prompting", "Beginner-friendly prompt engineering course", "https://learnprompting.org/", "Freemium"),
   ("Google AI Essentials", "Practical AI skills for work (Coursera)", "https://grow.google/ai-essentials/", "Paid / aid"),
   ("Elements of AI", "AI basics for everyone, no coding", "https://www.elementsofai.com/", "Free"),
  ]),
  ("Build with LLMs and agents", [
   ("OpenAI Cookbook", "Code examples for LLM apps", "https://cookbook.openai.com/", "Free"),
   ("LangChain Academy", "Free courses on LangGraph and agents", "https://academy.langchain.com/", "Free"),
   ("Model Context Protocol (MCP)", "Connect AI assistants to tools and data", "https://modelcontextprotocol.io/", "Free"),
   ("Claude Code docs", "Agentic coding in the terminal", "https://docs.claude.com/en/docs/claude-code/overview", "Free"),
   ("GitHub Copilot docs", "AI pair programming", "https://docs.github.com/en/copilot", "Freemium"),
   ("Cursor docs", "AI code editor", "https://docs.cursor.com/", "Freemium"),
  ]),
  ("AI assistants (help centres)", [
   ("Claude", "Writing, analysis, coding, projects", "https://support.anthropic.com/", "Freemium"),
   ("ChatGPT", "OpenAI's assistant: help and guides", "https://help.openai.com/", "Freemium"),
   ("Google Gemini", "Gemini help centre", "https://support.google.com/gemini", "Freemium"),
   ("Perplexity", "AI search with sources", "https://www.perplexity.ai/hub/getting-started", "Freemium"),
   ("NotebookLM", "Chat with your documents, audio overviews", "https://support.google.com/notebooklm", "Free"),
   ("DeepSeek", "Open-weight AI models and chat", "https://www.deepseek.com/", "Free"),
   ("Grok", "xAI's assistant", "https://x.ai/grok", "Freemium"),
  ]),
  ("AI for meetings and writing", [
   ("Otter.ai help", "Meeting transcription and summaries", "https://help.otter.ai/", "Freemium"),
   ("Fireflies.ai", "AI meeting notes and search", "https://fireflies.ai/", "Freemium"),
   ("Grammarly", "AI writing help", "https://www.grammarly.com/", "Freemium"),
   ("Microsoft Copilot", "AI in Word, Excel, PowerPoint and Teams", "https://support.microsoft.com/copilot", "Paid"),
  ]),
  ("AI images, video and voice", [
   ("Midjourney docs", "Prompting for AI images", "https://docs.midjourney.com/", "Paid"),
   ("Adobe Firefly", "AI images and generative fill", "https://www.adobe.com/products/firefly.html", "Freemium"),
   ("Leonardo.Ai", "AI images and assets", "https://leonardo.ai/", "Freemium"),
   ("Ideogram", "AI images with good text in images", "https://ideogram.ai/", "Freemium"),
   ("Runway Academy", "AI video tutorials", "https://academy.runwayml.com/", "Free"),
   ("ElevenLabs docs", "AI voice generation and voice agents", "https://elevenlabs.io/docs", "Freemium"),
  ]),
 ]),
 ("build", "No-code, design and automation", "Build apps, websites and automations without heavy coding (for every program).", [
  ("App builders", [
   ("Lovable docs", "Build web apps by chatting", "https://docs.lovable.dev/", "Freemium"),
   ("Replit docs", "Build and deploy apps with AI", "https://docs.replit.com/", "Freemium"),
   ("Bolt", "Build full-stack apps in the browser", "https://support.bolt.new/", "Freemium"),
   ("v0 by Vercel", "Generate UI and apps from prompts", "https://vercel.com/docs/v0", "Freemium"),
   ("Bubble Academy", "No-code web apps", "https://bubble.io/academy", "Free"),
   ("Webflow University", "Design and build websites", "https://university.webflow.com/", "Free"),
  ]),
  ("Automation", [
   ("n8n courses", "Workflow automation and AI agents", "https://docs.n8n.io/courses/", "Free"),
   ("Zapier Learn", "Automate apps without code", "https://learn.zapier.com/", "Free"),
   ("Make Academy", "Visual automation scenarios", "https://academy.make.com/", "Free"),
   ("Apify Academy", "Web scraping and automation", "https://docs.apify.com/academy", "Free"),
   ("SkillNavora n8n tutorial", "Our complete n8n guide", "tools.html", "Free"),
  ]),
  ("Design and content", [
   ("Canva Design School", "Design basics and Canva tutorials", "https://www.canva.com/designschool/", "Free"),
   ("Adobe Express", "Quick social graphics and videos", "https://www.adobe.com/express/learn", "Freemium"),
   ("Frame.io", "Video review and collaboration", "https://help.frame.io/", "Freemium"),
   ("Epidemic Sound", "Royalty-free music for videos", "https://www.epidemicsound.com/", "Paid"),
  ]),
 ]),
 ("code", "Coding and DSA interviews", "Data structures, algorithms, Git and coding practice (used in Data and GenAI tracks).", [
  ("Practise", [
   ("LeetCode", "Coding interview problems by company and topic", "https://leetcode.com/problemset/", "Freemium"),
   ("NeetCode roadmap", "The 150 most important problems, with videos", "https://neetcode.io/roadmap", "Free"),
   ("HackerRank", "Coding practice and certifications", "https://www.hackerrank.com/", "Free"),
   ("GeeksforGeeks DSA", "DSA tutorials and practice", "https://www.geeksforgeeks.org/", "Free"),
   ("SkillNavora DSA handbook", "Our DSA guide", "handbooks/index.html#dsa", "Free"),
  ]),
  ("Learn to code", [
   ("Harvard CS50", "The best intro to computer science", "https://cs50.harvard.edu/x/", "Free"),
   ("freeCodeCamp", "Free certifications in web, Python and data", "https://www.freecodecamp.org/learn", "Free"),
   ("The Odin Project", "Full-stack web development path", "https://www.theodinproject.com/", "Free"),
   ("GitHub Skills", "Learn Git and GitHub hands-on", "https://skills.github.com/", "Free"),
   ("Pro Git book", "Git explained, free online", "https://git-scm.com/book", "Free"),
  ]),
 ]),
 ("other", "Other programs", "SFMC, digital marketing, content creation, FDE and public speaking.", [
  ("SFMC and CRM", [
   ("Salesforce Trailhead", "Free official Salesforce and Marketing Cloud trails", "https://trailhead.salesforce.com/", "Free"),
   ("HubSpot Academy", "Inbound marketing, email and CRM courses", "https://academy.hubspot.com/", "Free"),
  ]),
  ("Digital marketing", [
   ("Google Skillshop", "Google Ads and Analytics certifications", "https://skillshop.withgoogle.com/", "Free"),
   ("Meta Blueprint", "Facebook and Instagram ads courses", "https://www.facebookblueprint.com/", "Free"),
   ("Semrush Academy", "SEO, content and PPC courses", "https://www.semrush.com/academy/", "Free"),
   ("Ahrefs Academy", "SEO courses for beginners", "https://ahrefs.com/academy", "Free"),
  ]),
  ("Content creation", [
   ("YouTube Creators", "Official tips for growing a channel", "https://www.youtube.com/creators/", "Free"),
   ("Canva Design School", "Design for social media", "https://www.canva.com/designschool/", "Free"),
   ("LinkedIn Creator tips", "Grow on LinkedIn", "https://www.linkedin.com/help/linkedin/answer/a522537", "Free"),
  ]),
  ("Forward Deployed Engineering", [
   ("AWS Skill Builder", "Cloud fundamentals and architecture", "https://skillbuilder.aws/", "Free"),
   ("Postman Academy", "APIs and integrations", "https://academy.postman.com/", "Free"),
   ("Docker get started", "Containers for deploying apps", "https://docs.docker.com/get-started/", "Free"),
  ]),
  ("Public speaking and English", [
   ("Toastmasters", "Practise speaking in clubs across India", "https://www.toastmasters.org/", "Paid"),
   ("BBC Learning English", "Free English lessons, grammar and pronunciation", "https://www.bbc.co.uk/learningenglish/", "Free"),
   ("Cambridge English: learning", "Free English activities", "https://www.cambridgeenglish.org/learning-english/", "Free"),
   ("TED: talks on speaking", "Learn from the best talks", "https://www.ted.com/topics/communication", "Free"),
   ("SkillNavora AI Speaking Coach", "Speak and get instant feedback", "speaking-coach.html", "Free"),
  ]),
 ]),
]

CSS = """<style>.ls-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}.ls-chips button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:99px;padding:8px 14px;font:600 14px var(--body);cursor:pointer}
.ls-chips button[aria-pressed=true]{background:var(--brand);color:#fff;border-color:var(--brand)}.ls-prog{margin:0 0 30px}.ls-prog>h3{font-size:22px;margin:0 0 4px}.ls-prog>p{margin:0 0 12px;color:var(--mu)}
.ls-g{font:700 13px var(--body);text-transform:uppercase;letter-spacing:.06em;color:var(--mu);margin:16px 0 8px}.ls-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.ls-i{display:flex;flex-direction:column;gap:3px;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 14px}.ls-i:hover{border-color:var(--brand)}
.ls-i b{color:var(--ink)}.ls-i small{color:var(--mu);font-size:13px}.ls-i em{font:700 10.5px var(--body);font-style:normal;text-transform:uppercase;letter-spacing:.05em;color:#6C4CF5}.ls-i .go{font:600 12.5px var(--body);color:var(--brand);margin-top:2px}</style>"""

def count():
    return sum(len(items) for _, _, _, groups in LEARN for _, items in groups)

def tab(pre=""):
    chips = f'<button type="button" data-ls="all" aria-pressed="true">All programs</button>' + "".join(f'<button type="button" data-ls="{k}" aria-pressed="false">{E(n)}</button>' for k, n, _, _ in LEARN)
    secs = []
    for k, n, blurb, groups in LEARN:
        g = "".join(f'<div class="ls-g">{E(gn)}</div><div class="ls-grid">' + "".join(
            f'<a class="ls-i" href="{E(u)}"' + (' target="_blank" rel="noopener"' if u.startswith("http") else "") + f'><em>{E(t)}</em><b>{E(nm)}</b><small>{E(w)}</small><span class="go">{"Open tutorial ↗" if u.startswith("http") else "Open →"}</span></a>'
            for nm, w, u, t in items) + "</div>" for gn, items in groups)
        secs.append(f'<section class="ls-prog" id="{pre}learn-{k}" data-ls="{k}"><h3>{E(n)}</h3><p>{E(blurb)}</p>{g}</section>')
    js = f"""<script>(function(){{var r=document.getElementById('{pre}ls'),c=r.querySelector('.ls-chips');c.addEventListener('click',function(e){{var b=e.target.closest('button');if(!b)return;[].forEach.call(c.children,function(x){{x.setAttribute('aria-pressed',x===b)}});[].forEach.call(r.querySelectorAll('.ls-prog'),function(s){{s.hidden=b.dataset.ls!=='all'&&s.dataset.ls!==b.dataset.ls}})}});window.addEventListener('hashchange',function(){{var t=document.getElementById(location.hash.slice(1));if(t&&r.contains(t)){{c.children[0].click();t.scrollIntoView()}}}})}})();</script>"""
    return (CSS + f'<div id="{pre}ls"><p class="meta" style="margin:0 0 12px">{count()} hand-picked sites to learn and practise, sorted by program. Each link opens the tutorial or practice page directly.</p>'
            f'<div class="ls-chips" role="group" aria-label="Filter by program">{chips}</div>' + "".join(secs) + "</div>" + js)
