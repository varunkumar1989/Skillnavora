"""SkillNavora Study Library: one artifact that indexes ALL study material on skillnavora.in (programs, handbooks, every lesson,
AI skills academy, practice, tools, PDFs) and explains how to deploy the whole site on Netlify."""
import html, json, os, re, glob
import learnsites, academy_interactive as AI
import course_aiengineer
E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.skillnavora.in/"
PROGRAMS = json.load(open("/tmp/claude-0/-home-user/20ecdeba-c201-50e4-9856-79c86c6b1138/scratchpad/aiacad/programs.json"))
CAT = json.load(open(os.path.join(ROOT, "data-science/catalog.json")))
LESSON_SRC = "/home/user/data-science-and-ai/course/source/lessons"

def fm(path):
    t = open(path, encoding="utf-8").read(); m = re.match(r"---\n(.*?)\n---", t, re.S)
    d = {"outcomes": []}; cur = None
    for line in (m.group(1) if m else "").split("\n"):
        if re.match(r"^\s+- ", line): d["outcomes"].append(line.strip()[2:].strip().strip('"')); continue
        k = re.match(r"^(\w+):\s*(.*)$", line)
        if k and k.group(1) != "outcomes": cur = k.group(1); d[cur] = k.group(2).strip().strip('"')
    return d

def a(href, text, new=True):
    return f'<a href="{E(SITE + href if not href.startswith("http") else href)}" target="_blank" rel="noopener">{text} ↗</a>'
def link_btn(href, text, pri=False):
    return f'<a class="btn{" pri" if pri else ""}" href="{E(SITE + href if not href.startswith("http") else href)}" target="_blank" rel="noopener">{E(text)} ↗</a>'

def tab(key, eyebrow, title, lede, acts, inner):
    return f'<section class="tab" id="{key}" hidden><header class="th"><p class="eyebrow">{E(eyebrow)}</p><h2>{E(title)}</h2><p class="lede">{lede}</p><div class="acts">{acts}</div></header>{inner}</section>'

def t_start():
    cards = "".join(f'<a class="cc" href="#{k}"><span>{E(s)}</span><b>{E(t)}</b></a>' for k, s, t in [
        ("programs", "3 programs", "Programs & curricula"), ("pm", "23 modules", "PM Master Handbook"), ("ds", f"{sum(len(t['lessons']) for t in CAT['tracks'])} lessons", "Data Science & AI handbook"),
        ("genai", "482-page PDF", "GenAI Launchpad"), ("academy", f"{len(AI.ALL)} courses", "AI Skills Academy"), ("engineer", "12 classes", "AI Engineer path"),
        ("practice", "867 questions", "Practice & interview prep"), ("tools", "147 sites", "Tools & learning sites"), ("pdfs", "all PDFs", "Downloads"), ("netlify", "deploy free", "Netlify guide")])
    return tab("start", "Start here", "SkillNavora Study Library", "Everything on skillnavora.in in one place: programs, handbooks, every lesson, AI skills courses, practice and interview prep, tools and learning sites, and every PDF. Each item links to the full material on the website.",
               link_btn("", "Open skillnavora.in", True) + link_btn("ai-academy-interactive.html", "Interactive AI Academy") + link_btn("ai-skills-map.html", "AI Skills Map"),
               f'<div class="ccs">{cards}</div><h3 class="sh">Suggested order</h3><ol class="path">'
               + "".join(f'<li><span class="n">{i}</span><div><b>{E(n)}</b><p>{E(w)}</p></div></li>' for i, (n, w) in enumerate([
                   ("Pick your program", "AI Product Management, AI for Data Engineers or GenAI Launchpad."), ("Learn the 7 core AI skills", "Context engineering, skills & templates, second brain, research and analysis, evals, automation, orchestration."),
                   ("Practise", "Practice Lab, 867 test questions and Top 100 interview questions per program."), ("Build", "AI Builder Tools, Web Automation and the AI Engineer path: projects for your portfolio."), ("Prepare for jobs", "Resume, GitHub, interview prep, job board and mock interviews.")], 1)) + "</ol>")

def t_programs():
    out = ""
    for P in PROGRAMS:
        mods = "".join(f"<li class='item'><b>{E(m['title'])}</b><br><span class='mu'>{E(' · '.join(m['topics']))}</span></li>" for m in P["curriculum"])
        outs = "".join(f"<li>{E(o)}</li>" for o in P["outcomes"]); proj = "".join(f"<li>{E(x)}</li>" for x in (P.get("projects") or []))
        out += (f'<details class="grp" open><summary>{E(P["name"])} <span>({len(P["curriculum"])} modules · {E(P.get("duration", ""))})</span></summary><p class="mu">{E(P["short"])}</p><div class="acts">{link_btn(P["page"], "Program page", True)}</div>'
                f'<h4>What you will be able to do</h4><ul>{outs}</ul><h4>Curriculum</h4><ol class="items">{mods}</ol>' + (f"<h4>Projects</h4><ul>{proj}</ul>" if proj else "") + "</details>")
    return tab("programs", "Programs", "Programs & curricula", "Every module and topic of the three flagship programs, with outcomes and projects.", link_btn("programs.html", "Compare programs"), out)

def t_pm():
    rows = ""
    for f in sorted(glob.glob(os.path.join(ROOT, "handbooks/pm/m*.html"))):
        m = re.search(r"<title>([^<·]+)", open(f, encoding="utf-8").read()); n = os.path.basename(f)
        if m: rows += f"<li class='item'>{a('handbooks/pm/' + n, E(m.group(1).strip()))}</li>"
    extra = "".join(f"<li class='item'>{a('handbooks/pm/' + n, E(t))}</li>" for n, t in [("frameworks.html", "Frameworks library"), ("cases.html", "Case studies"), ("glossary.html", "Glossary"), ("interview.html", "Interview preparation"), ("appendix.html", "Appendix")])
    ai = "".join(f"<li class='item'>{a(h, E(t))}</li>" for h, t in [("prd-library.html", "PRD library: template + 120 ideas"), ("prd-writer.html", "AI PRD / BRD / FRD Writer"), ("pm-toolkit.html", "AI PM Toolkit (13 capabilities)"), ("brd-frd.html", "BRD & FRD guide (25 projects)"), ("ai-evals.html", "AI Evals for PMs")])
    return tab("pm", "AI Product Management", "PM Master Handbook", "23 interactive modules from fundamentals to AI foundations, Claude, Claude Code, Lovable, automation and voice agents, plus frameworks, cases and interview prep.",
               link_btn("handbooks/pm/index.html", "Open the PM handbook", True) + link_btn("handbooks/index.html#pm", "Handbooks hub"),
               f'<h3 class="sh">Modules</h3><ol class="items">{rows}</ol><h3 class="sh">Reference</h3><ul class="items">{extra}</ul><h3 class="sh">PM tools built into SkillNavora</h3><ul class="items">{ai}</ul>')

def t_ds():
    out = ""
    for t in CAT["tracks"]:
        src = os.path.join(LESSON_SRC, t["id"]); meta = {}
        for f in glob.glob(src + "/*.md"):
            d = fm(f)
            if d.get("num"): meta[int(d["num"])] = d
        items = ""
        for l in t["lessons"]:
            d = meta.get(l["num"], {}); outs = "".join(f"<li>{E(o)}</li>" for o in d.get("outcomes", [])[:3])
            items += (f"<li class='item'><b>{l['num']}. {a('data-science/' + l['page'], E(l['title']))}</b> <span class='tag'>{E(d.get('level', ''))}</span> <span class='tag'>{E(d.get('duration', ''))}</span><br><span class='mu'>{E(d.get('summary', ''))}</span>"
                      + (f"<ul>{outs}</ul>" if outs else "") + f"<span class='mu'>PDF: {a('data-science/' + l['pdf_path'], 'download')}</span></li>")
        out += f'<details class="grp"><summary>{E(t["name"])} <span>({len(t["lessons"])} lessons)</span></summary><p class="mu">{E(t["desc"])}</p><div class="acts">{link_btn("data-science/" + t["pdf"], "Track PDF")}</div><ol class="items">{items}</ol></details>'
    return tab("ds", "AI for Data Engineers · Data Science & AI", "Data Science & AI handbook", f"{sum(len(t['lessons']) for t in CAT['tracks'])} lessons in {len(CAT['tracks'])} tracks: Excel, SQL, Power BI, Tableau, Python, statistics and ML, GenAI, agents, tools, careers and the other programs. Every lesson has real data, quizzes, exercises, interview questions and a PDF.",
               link_btn("data-science/index.html", "Open the handbook", True) + link_btn("lab.html", "Practice Lab"), out)

def t_genai():
    cur = next(p for p in PROGRAMS if p["id"] == "genai-launchpad")["curriculum"]
    mods = "".join(f"<li class='item'><b>{E(m['title'])}</b><br><span class='mu'>{E(' · '.join(m['topics']))}</span></li>" for m in cur)
    cs = "".join(f"<li class='item'>{a(C['page'], E(C['title']))} <span class='mu'>{E(C['oneline'][:150])}…</span></li>" for k, C, _ in AI.ALL)
    return tab("genai", "GenAI Launchpad", "GenAI Launchpad", "Practical GenAI for every professional: the 482-page handbook, curriculum, and every AI skills course.", link_btn("handbooks/index.html#genai", "GenAI handbook", True) + link_btn("handbooks/genai/SkillNavora_GenAI_Launchpad_Handbook.pdf", "Handbook PDF") + link_btn("program/genai-launchpad.html", "Program page"),
               f'<h3 class="sh">Curriculum</h3><ol class="items">{mods}</ol><h3 class="sh">Courses that sit with it</h3><ul class="items">{cs}</ul>')

def t_academy():
    out = ""
    for k, C, label in AI.ALL:
        cl = "".join(f"<li><span class='tag'>{E(lv)}</span> {E(t)}: <span class='mu'>{E(g)}</span></li>" for lv, t, g, *_ in C["classes"])
        out += (f'<details class="grp"><summary>{E(C["title"])} <span>({len(C["classes"])} classes)</span></summary><p class="mu">{E(C["oneline"])}</p><div class="acts">{link_btn("ai-academy-interactive.html#" + k, "Interactive lessons", True)}{link_btn("handbook/" + C["pdf"], "PDF")}{link_btn(C["page"], "Course page")}</div><ol class="items">{cl}</ol></details>')
    return tab("academy", "AI skills", "AI Skills Academy", f"{len(AI.ALL)} illustrated courses from basic to advanced: AI tools, the 7 core AI skills and advanced AI product management, each with classes, templates, cheat sheets, interview questions and a PDF.",
               link_btn("ai-academy.html", "Open the Academy", True) + link_btn("ai-skills-map.html", "AI Skills Map"), out)

def t_engineer():
    C = course_aiengineer.COURSE; cl = "".join(f"<li><span class='tag'>{E(lv)}</span> <b>{E(t)}</b><br><span class='mu'>{E(g)}</span></li>" for lv, t, g, *_ in C["classes"])
    stack = "".join(f"<tr><td><b>{E(x)}</b></td><td>{E(y)}</td></tr>" for x, y in C["cheat"])
    return tab("engineer", "Resources · Other programs", "AI Engineer: the complete path", E(C["oneline"]), link_btn("ai-academy-interactive.html#ai-engineer", "Interactive lessons", True) + link_btn("handbook/" + C["pdf"], "PDF") + link_btn("resources.html#other", "In Resources"),
               f'<h3 class="sh">12 classes</h3><ol class="items">{cl}</ol><h3 class="sh">Tool stack</h3><div class="tw"><table>{stack}</table></div>')

def t_practice():
    items = [("tests.html", "Practice tests: 867 questions + 39 exercises", "Every handbook lesson, with hints when you are wrong"), ("questions.html", "Top 100 interview questions per program", "PM, Data & AI, GenAI (+ other programs) with model answers"),
             ("lab.html", "Practice Lab: 61 challenges", "Run SQL, Excel and Python in the browser; Power BI, Tableau, ML traps; AI PM and GenAI scenarios"), ("practice.html", "AI mock interview", "Answer a question, get a score and model answer"),
             ("speaking-coach.html", "AI Speaking Coach", "Free speech, shadowing, English interview, presentations"), ("ai-tutor.html", "AI Tutor", "Ask any study question"), ("quiz.html", "Quiz zone", "Quick quizzes"), ("challenges.html", "Challenges", "Real-world problems"),
             ("prd-library.html", "PRD library", "120 PRD ideas and a template"), ("brd-frd.html", "BRD & FRD guide", "25 BA project ideas"), ("jobs.html", "Job board and portals", "Openings, alerts and job portals")]
    return tab("practice", "Practice & interviews", "Practice & interview prep", "Test yourself, practise speaking and interviews, and prepare for jobs.", link_btn("tests.html", "Start a practice test", True),
               "<ul class='items'>" + "".join(f"<li class='item'>{a(h, E(t))}<br><span class='mu'>{E(d)}</span></li>" for h, t, d in items) + "</ul>")

def t_tools():
    out = ""
    for k, n, blurb, groups in learnsites.LEARN:
        g = "".join(f"<h4>{E(gn)}</h4><ul class='items'>" + "".join(f"<li class='item'>{a(u, E(nm))} <span class='tag'>{E(tg)}</span><br><span class='mu'>{E(w)}</span></li>" for nm, w, u, tg in its) + "</ul>" for gn, its in groups)
        out += f'<details class="grp"><summary>{E(n)} <span>({sum(len(i) for _, i in groups)} sites)</span></summary><p class="mu">{E(blurb)}</p>{g}</details>'
    return tab("tools", "Tools & learning sites", "Tools & learning sites", f"{learnsites.count()} hand-picked sites with direct tutorial links, grouped by program, plus the tool tutorials page.", link_btn("resources.html#learn", "Learning sites tab", True) + link_btn("tools.html", "Tool tutorials"), out)

def t_pdfs():
    groups = [("Handbooks (complete)", ["data-science/pdf/*.pdf", "handbooks/genai/*.pdf", "handbook/Complete-PM*.pdf", "handbook/*Handbook*.pdf"]), ("Data Science & AI: track PDFs", ["data-science/pdf/tracks/*.pdf"]),
              ("AI skills courses", ["handbook/AI_*.pdf", "handbook/Agent_*.pdf", "handbook/Browser_*.pdf", "handbook/Prompt_*.pdf", "handbook/Designing_*.pdf", "handbook/Pricing_*.pdf", "handbook/ML_*.pdf", "handbook/Platform_*.pdf", "handbook/Product_*.pdf", "handbook/Multimodal_*.pdf", "handbook/Web_*.pdf"]),
              ("Templates", ["handbook/templates/*"]), ("Program brochures", ["brochures/*.pdf"])]
    out, seen = "", set()
    for gname, pats in groups:
        fs = []
        for p in pats: fs += glob.glob(os.path.join(ROOT, p))
        fs = [f for f in sorted(set(fs)) if f not in seen]; seen |= set(fs)
        if fs: out += f'<details class="grp"><summary>{E(gname)} <span>({len(fs)})</span></summary><ul class="items">' + "".join(f"<li class='item'>{a(os.path.relpath(f, ROOT), E(os.path.basename(f)))} <span class='tag'>{os.path.getsize(f) / 1048576:.1f} MB</span></li>" for f in fs) + "</ul></details>"
    return tab("pdfs", "Downloads", "Every PDF and template", "Handbooks, track PDFs, course PDFs, templates and brochures. PDFs open after a short details form (admins skip it).", link_btn("handbooks/index.html", "Handbooks hub", True), out)

def t_netlify():
    steps = ["Open <b>app.netlify.com</b> → <b>Add new site</b> → <b>Import an existing project</b> → GitHub → choose the <b>skillnavora</b> repository.",
             "Branch to deploy: <b>main</b>. Build command: leave empty. Publish directory: <b>.</b> (a single dot). The <code>netlify.toml</code> in the repository already says this.",
             "Click <b>Deploy</b>. Every page, lesson, PDF and course loads from Netlify, and every push to GitHub redeploys automatically. On Netlify the front page is the <b>Study Hub</b> with four tabs: AI Product Management, AI for Data Engineers, AI Engineer and GenAI Launchpad (the normal website home is at <code>/home</code>).",
             "Optional: <b>Domain management</b> → add your domain and follow the DNS steps; HTTPS turns on automatically.",
             "Drag-and-drop alternative: download the repository as a ZIP from GitHub, unzip, and drop the folder onto <b>app.netlify.com/drop</b> (very large PDFs may take a few minutes)."]
    notes = ["<b>Works on Netlify:</b> all study material: programs, handbooks, every lesson and PDF, the AI Skills Academy and interactive pages, practice tests, Practice Lab, PRD library, tools and learning sites, the details form (it falls back to WhatsApp/email if the lead API is missing).",
             "<b>Needs Cloudflare Pages (or a rewrite):</b> the live AI tools (AI Tutor, PRD Writer, PM Toolkit, Speaking Coach feedback) and the lead API run as Cloudflare Pages Functions in <code>functions/api/</code>. On Netlify, keep these on Cloudflare and point to them, or ask to have them converted to Netlify Functions.",
             "<b>Files:</b> the study material is roughly 350 MB, mostly PDFs. Netlify's free plan allows this; keep individual files under 100 MB (all are well below).",
             "Security headers and redirects: the existing <code>_headers</code> and <code>_redirects</code> files use Netlify's format too, so they work as they are."]
    return tab("netlify", "Deploy", "Put all the study material on Netlify", "The whole website is static HTML, so Netlify can host every lesson, PDF and course straight from your GitHub repository.", link_btn("https://app.netlify.com/start", "Open Netlify", True) + link_btn("https://docs.netlify.com/site-deploys/create-deploys/", "Netlify docs"),
               '<h3 class="sh">Steps</h3><ol class="path">' + "".join(f'<li><span class="n">{i}</span><div>{s}</div></li>' for i, s in enumerate(steps, 1)) + '</ol><h3 class="sh">What to know</h3><ul class="items">' + "".join(f"<li class='item'>{n}</li>" for n in notes) + "</ul>")

TABS = [("start", "Start here", t_start), ("programs", "Programs", t_programs), ("pm", "PM handbook", t_pm), ("ds", "Data Science & AI", t_ds), ("genai", "GenAI Launchpad", t_genai), ("academy", "AI Skills Academy", t_academy),
        ("engineer", "AI Engineer", t_engineer), ("practice", "Practice & interviews", t_practice), ("tools", "Tools & learning sites", t_tools), ("pdfs", "Downloads", t_pdfs), ("netlify", "Netlify", t_netlify)]

EXTRA = (".mu{color:var(--mu);font-size:13.5px}.tag{display:inline-block;font:600 11px var(--body);border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--mu);margin-left:4px}"
         "ol.items,ul.items{display:grid;gap:8px;padding-left:20px;margin:8px 0}ol.items>li,ul.items>li{padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:var(--surface)}ol.items{list-style:decimal}ul.items{list-style:none;padding-left:0}"
         ".grp{margin-bottom:10px}.grp h4,.sh+h4{margin:12px 0 4px;font:700 15px var(--display)}.grp .acts{margin:8px 0}.th h2{margin-bottom:6px}.ccs{margin:6px 0 12px}"
         "#flt{width:100%;max-width:520px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;font:inherit;background:var(--surface);color:var(--ink);margin:0 0 14px}")

def html_page():
    style = AI.artifact_style().replace("nav.tabs", "nav.a-tabs") + EXTRA
    nav = "".join(f'<a href="#{k}" data-t="{k}">{E(n)}</a>' for k, n, _ in TABS)
    body = "".join(fn() for _, _, fn in TABS)
    ids = [k for k, _, _ in TABS]
    js = ("<script>(function(){var ids=" + json.dumps(ids) + ";function show(){var h=(location.hash||'#start').slice(1),k=ids.indexOf(h)>-1?h:'start';document.querySelectorAll('.tab').forEach(function(s){s.hidden=s.id!==k});"
          "document.querySelectorAll('nav.a-tabs a').forEach(function(a){a.setAttribute('aria-current',a.dataset.t===k?'true':'false');if(a.dataset.t===k&&a.scrollIntoView)a.scrollIntoView({block:'nearest',inline:'nearest'})});window.scrollTo(0,0);filter()}"
          "function filter(){var q=document.getElementById('flt').value.toLowerCase();var v=document.querySelector('.tab:not([hidden])');if(!v)return;v.querySelectorAll('details.grp').forEach(function(g){var n=0;g.querySelectorAll('.item,li').forEach(function(i){var ok=!q||i.textContent.toLowerCase().indexOf(q)>-1;i.style.display=ok?'':'none';if(ok)n++});g.style.display=(!q||n||g.querySelector('summary').textContent.toLowerCase().indexOf(q)>-1)?'':'none';if(q&&n)g.open=true});"
          "v.querySelectorAll(':scope > ol.items > li, :scope > ul.items > li').forEach(function(i){i.style.display=(!q||i.textContent.toLowerCase().indexOf(q)>-1)?'':'none'})}"
          "window.addEventListener('hashchange',show);document.getElementById('flt').addEventListener('input',filter);show()})();</script>")
    return ('<title>SkillNavora Study Library</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap">\n'
            f"<style>{style}</style>\n"
            f'<div class="a-wrap"><div class="a-top"><p class="eyebrow">skillnavora.in · all study material</p><h1>SkillNavora <span>Study Library</span></h1><p>One page that covers every program, handbook, lesson, course, practice set, tool and PDF on the website.</p></div>'
            f'<nav class="a-tabs" aria-label="Sections">{nav}</nav><input id="flt" type="search" placeholder="Filter this section: SQL, RAG, Tableau, PRD, Claude…" aria-label="Filter this section">{body}'
            f'<p class="foot">© SkillNavora · <a href="{SITE}" target="_blank" rel="noopener">skillnavora.in</a></p></div>' + js)
