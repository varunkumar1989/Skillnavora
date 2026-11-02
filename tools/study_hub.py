"""Study Hub (study-hub.html): all study material in one page with four tabs: AI Product Management, AI for Data Engineers,
AI Engineer, GenAI Launchpad. Every item is a link inside the same site, so it works on Cloudflare and on Netlify
(netlify.toml serves this page at the front door on Netlify)."""
import glob, html, json, os, re, subprocess
import academy_interactive as AI
import course_aiengineer, learnsites, tooltuts, skillsmap
E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = json.load(open(os.path.join(ROOT, "data-science/catalog.json")))
LESSON_SRC = "/home/user/data-science-and-ai/course/source/lessons"
COURSES = {k: (C, lab) for k, C, lab in AI.ALL}

def programs():
    js = ("const vm=require('vm'),fs=require('fs');const c={};vm.createContext(c);vm.runInContext(fs.readFileSync('assets/config.js','utf8')+';this.o=COURSES.map(x=>({id:x.id,page:x.page,name:x.name,short:x.short,duration:x.duration,outcomes:x.outcomes,curriculum:x.curriculum}));',c);console.log(JSON.stringify(c.o))")
    return {p["id"]: p for p in json.loads(subprocess.run(["node", "-e", js], cwd=ROOT, capture_output=True, text=True, check=True).stdout)}

def fm(path):
    t = open(path, encoding="utf-8").read(); m = re.match(r"---\n(.*?)\n---", t, re.S); d = {}
    for line in (m.group(1) if m else "").split("\n"):
        k = re.match(r"^(\w+):\s*(.*)$", line)
        if k and k.group(1) != "outcomes": d[k.group(1)] = k.group(2).strip().strip('"')
    return d

def lnk(href, text): return f'<a href="{E(href)}">{text}</a>'
def btn(href, text, pri=False, blank=False):
    return f'<a class="hb{" pri" if pri else ""}" href="{E(href)}"' + (' target="_blank" rel="noopener"' if blank or href.startswith("http") else "") + f'>{E(text)}</a>'

def course_block(key, open_=False):
    C, lab = COURSES[key]
    cls = "".join(f'<li><a href="ai-academy-interactive.html#{key}-c{i}"><span class="lv lv-{lv}">{lv.title()}</span> Class {i}: {E(t)}</a><small>{E(g)}</small></li>' for i, (lv, t, g, *_) in enumerate(C["classes"], 1))
    return (f'<details class="hg"{" open" if open_ else ""}><summary>{E(C["title"])} <em>({len(C["classes"])} classes)</em></summary><p class="mu">{E(C["oneline"])}</p>'
            f'<div class="acts">{btn("ai-academy-interactive.html#" + key, "All classes (interactive)", True)}{btn(C["page"], "Course page")}{btn("handbook/" + C["pdf"], "PDF")}</div><ol class="cl">{cls}</ol></details>')

def curriculum(P):
    mods = "".join(f"<li><b>{E(m['title'])}</b><small>{E(' · '.join(m['topics']))}</small></li>" for m in P["curriculum"])
    outs = "".join(f"<li>{E(o)}</li>" for o in P["outcomes"])
    return (f'<h3>Curriculum: {len(P["curriculum"])} modules · {E(P.get("duration", ""))}</h3><details class="hg"><summary>What you will be able to do</summary><ul>{outs}</ul></details>'
            f'<details class="hg" open><summary>All modules and topics</summary><ol class="cl">{mods}</ol></details>')

def tracks(ids, title="Lessons"):
    out = f"<h3>{E(title)}</h3>"
    for t in CAT["tracks"]:
        if t["id"] not in ids: continue
        meta = {}
        for f in glob.glob(os.path.join(LESSON_SRC, t["id"], "*.md")):
            d = fm(f)
            if d.get("num"): meta[int(d["num"])] = d
        li = "".join(f'<li><a href="data-science/{E(l["page"])}">{l["num"]}. {E(l["title"])}</a>' + (f'<small><span class="tag">{E(meta[l["num"]].get("level", ""))}</span> <span class="tag">{E(meta[l["num"]].get("duration", ""))}</span> {E(meta[l["num"]].get("summary", ""))}</small>' if l["num"] in meta else "") + f'<small><a href="data-science/{E(l["pdf_path"])}">PDF</a></small></li>' for l in t["lessons"])
        out += f'<details class="hg"><summary>{E(t["name"])} <em>({len(t["lessons"])} lessons)</em></summary><p class="mu">{E(t["desc"])}</p><div class="acts">{btn("data-science/" + t["pdf"], "Track PDF")}</div><ol class="cl">{li}</ol></details>'
    return out

def pm_modules():
    rows = ""
    for f in sorted(glob.glob(os.path.join(ROOT, "handbooks/pm/m*.html"))):
        m = re.search(r"<title>([^<·]+)", open(f, encoding="utf-8").read())
        if m: rows += f'<li><a href="handbooks/pm/{os.path.basename(f)}">{E(m.group(1).strip())}</a></li>'
    ref = "".join(f'<li><a href="handbooks/pm/{n}">{E(t)}</a></li>' for n, t in [("frameworks.html", "Frameworks library"), ("cases.html", "Case studies"), ("glossary.html", "Glossary"), ("interview.html", "Interview preparation"), ("appendix.html", "Appendix")])
    return f'<h3>PM Master Handbook (23 modules)</h3><details class="hg" open><summary>Modules <em>(23)</em></summary><div class="acts">{btn("handbooks/pm/index.html", "Open the PM handbook", True)}</div><ol class="cl">{rows}</ol></details><details class="hg"><summary>Reference: frameworks, cases, glossary, interview prep</summary><ul class="cl">{ref}</ul></details>'

def pdfs(globs):
    fs = []
    for g in globs: fs += glob.glob(os.path.join(ROOT, g))
    fs = sorted(set(fs))
    return '<h3>PDFs and downloads</h3><ul class="cl pdf">' + "".join(f'<li><a href="{E(os.path.relpath(f, ROOT))}">{E(os.path.basename(f))}</a><small>{os.path.getsize(f) / 1048576:.1f} MB</small></li>' for f in fs) + "</ul>"

def practice(seg, extra=()):
    items = [(f"tests.html#{seg}", "Practice tests", "Questions from every lesson with hints"), (f"questions.html#{seg}", "Top 100 interview questions", "With model answers"), (f"lab.html#{seg}", "Practice Lab", "Run SQL, Excel, Python and decision scenarios"), ("ai-tutor.html", "AI Tutor", "Ask any study question"), ("practice.html", "AI mock interview", "Answer and get scored")] + list(extra)
    return '<h3>Practice and interview prep</h3><ul class="cl">' + "".join(f'<li><a href="{E(h)}">{E(t)}</a><small>{E(d)}</small></li>' for h, t, d in items) + "</ul>"

def block(tab_id, eyebrow, title, lede, acts, parts):
    return f'<section class="htab" id="{tab_id}" hidden><p class="eyebrow">{E(eyebrow)}</p><h2>{E(title)}</h2><p class="lede">{lede}</p><div class="acts">{acts}</div>{"".join(parts)}</section>'

def tools_tab():
    d = tooltuts.data(); sites = d["l"]
    def ours(name):
        out = []
        for lab, path in tooltuts.OURS.get(name, []):
            href = skillsmap.L(path[3:]) if path.startswith("ds:") else path
            out.append(f'<a href="{E(href)}">{E(lab)}</a>')
        return out
    feat = "".join(f'<li><a href="{h}">{E(t)}</a><small>{E(w)}</small></li>' for h, t, w in [
        ("zapier-tutorial.html", "Zapier: complete tutorial", "Zaps, filters, paths, webhooks, AI steps, templates, project + PDF"), ("make-tutorial.html", "Make: complete tutorial", "Scenarios, routers, iterators, HTTP/JSON, error handling, project + PDF"),
        ("replit-tutorial.html", "Replit: complete tutorial", "Agent builds, database, secrets, deploy, GitHub, project + PDF"), ("lovable-tutorial.html", "Lovable: complete tutorial", "Prompts, Supabase, login, GitHub, domain, project + PDF"),
        ("ai-academy-interactive.html#builder-tools", "AI Builder Tools (Claude, ChatGPT/Codex, Gemini, Lovable)", "What each tool does and how to build a website end to end"),
        ("ai-academy-interactive.html#web-automation", "Web Automation: webhooks, triggers, Playwright MCP", "n8n, Zapier, Make, Pipedream, Apify, Playwright and more"),
        ("data-science/index.html#tools", "n8n and Figma: complete tutorials", "In the Data Science & AI handbook (AI & No-Code Tools Lab)"), ("tools.html", "Tool tutorials page", "Every tool with its official site, free tutorial and our lesson")])
    out = f'<h3>Our complete tutorials</h3><div class="gsec"><ul class="cl">{feat}</ul></div><h3>Every tool, with its tutorial</h3><p class="mu">{sum(len(g["tools"]) for c in d["c"] for g in c["g"])} tool entries across the three programs. <b>Free tutorial</b> opens the official learning page; <b>Official site</b> opens the product; <b>Our lessons</b> open the SkillNavora lesson (after details).</p>'
    seen = set()
    for c in d["c"]:
        body = ""
        for g in c["g"]:
            rows = ""
            for name in g["tools"]:
                site, learn, mine = sites.get(name), tooltuts.LEARN.get(name), ours(name)
                links = (f'<a href="{E(learn)}" target="_blank" rel="noopener">Free tutorial ↗</a>' if learn else "") + (f' <a href="{E(site)}" target="_blank" rel="noopener">Official site ↗</a>' if site else "")
                rows += f'<li><b>{E(name)}</b><small>{links}</small>' + (f'<small class="gsec">Our lessons: ' + " · ".join(mine) + "</small>" if mine else "") + "</li>"
            body += f'<h4 style="margin:14px 0 6px;font:700 15px var(--display)">{E(g["name"])}</h4><ul class="cl">{rows}</ul>'
        out += f'<details class="hg"{" open" if not seen else ""}><summary>{E(c["name"])}</summary>{body}</details>'; seen.add(c["id"])
    return out

def G(x): return f'<div class="gsec">{x}</div>'

def build():
    P = programs()
    all_courses = [k for k in COURSES if k != "ai-engineer"]
    aipm = block("aipm", "AI Product Management", "AI-First Product Management", E(P["ai-pm"]["short"]), btn("program/ai-product-management.html", "Program page", True) + btn("prd-library.html", "PRD library") + btn("pm-toolkit.html", "AI PM Toolkit") + btn("brd-frd.html", "BRD & FRD guide"),
                 [curriculum(P["ai-pm"]), G(pm_modules()), G("<h3>AI courses and classes (click any class)</h3>" + "".join(course_block(k) for k in all_courses)),
                  practice("pm", [("prd-writer.html", "AI PRD / BRD / FRD Writer", "Write requirements documents with AI")]), G(pdfs(["handbook/Complete-PM*.pdf", "handbook/AI_*.pdf", "handbook/Prompt_*.pdf", "handbook/Designing_*.pdf", "handbook/Pricing_*.pdf", "handbook/Product_*.pdf", "handbook/Platform_*.pdf", "handbook/Multimodal_*.pdf", "handbook/ML_*.pdf", "handbook/Agent_*.pdf", "handbook/Browser_*.pdf", "handbook/Web_*.pdf", "handbook/templates/*", "brochures/*product*.pdf"]))])
    de_ids = ["excel", "sql", "python", "powerbi", "tableau", "ai-analytics", "ml", "genai", "agents", "tools", "career"]
    aide = block("aide", "AI for Data Engineers", "AI-First Data Engineer / Data Science & AI", E(P["ai-de"]["short"]), btn("program/ai-data-engineering.html", "Program page", True) + btn("data-science/index.html", "Data Science & AI handbook") + btn("lab.html#data", "Practice Lab") + btn("brd-frd.html", "BRD & FRD guide"),
                 [curriculum(P["ai-de"]), G(tracks(de_ids, "Data Science & AI handbook: every lesson")), G("<h3>AI courses and classes (click any class)</h3>" + "".join(course_block(k) for k in ["context", "evals", "web-automation", "orch", "builder-tools", "ml-products", "ai-governance", "brain"])),
                  practice("data"), G(pdfs(["data-science/pdf/*.pdf", "data-science/pdf/tracks/*.pdf", "handbook/AI_Evals*.pdf", "handbook/Web_*.pdf", "handbook/Agent_*.pdf", "brochures/*data*.pdf"]))])
    ae = course_aiengineer.COURSE
    free = "".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(n)} ↗</a></li>' for n, u in ae["links"])
    aieng = block("aieng", "AI Engineer", "AI Engineer: the complete path", E(ae["oneline"]), btn("ai-engineer.html", "Course page", True) + btn("handbook/" + ae["pdf"], "PDF") + btn("resources.html#other", "In Resources › Other programs"),
                  [G(course_block("ai-engineer", True)), G(tracks(["python", "sql", "ml", "genai", "agents", "career"], "Lessons that teach the foundations")),
                   G("<h3>Related AI courses and classes</h3>" + "".join(course_block(k) for k in ["context", "evals", "orch", "web-automation", "browser", "builder-tools", "ml-products", "ai-governance", "platform-pm", "ai-strategy"])),
                   practice("genai", [("questions.html#data", "Data & ML interview questions", "SQL, Python, ML")]), f'<h3>Free courses and reading</h3><ul class="cl">{free}</ul>', G(pdfs(["handbook/AI_Engineer*.pdf", "handbook/Agent_*.pdf", "handbook/Web_*.pdf", "handbook/AI_Evals*.pdf", "handbook/Prompt_*.pdf", "handbooks/genai/*.pdf"]))])
    gl = P["genai-launchpad"]
    genai = block("genai", "GenAI Launchpad", "GenAI Launchpad", E(gl["short"]), btn("program/genai-launchpad.html", "Program page", True) + btn("handbooks/genai/SkillNavora_GenAI_Launchpad_Handbook.pdf", "Handbook PDF (482 pages)") + btn("ai-academy.html", "AI Skills Academy") + btn("ai-skills-map.html", "AI Skills Map"),
                  [curriculum(gl), G(tracks(["genai", "agents", "tools", "ai-analytics"], "GenAI and agents lessons")), G("<h3>AI courses and classes (click any class)</h3>" + "".join(course_block(k) for k in all_courses)),
                   practice("genai"), G(pdfs(["handbooks/genai/*.pdf", "handbook/AI_*.pdf", "handbook/Prompt_*.pdf", "handbook/Agent_*.pdf", "handbook/Browser_*.pdf", "handbook/Web_*.pdf", "brochures/*genai*.pdf"]))])
    tools = block("tools", "Tools", "Tools & tutorials", "Every tool used in the programs with its free tutorial, official site and our lessons, plus our complete tutorials for Zapier, Make, Replit, Lovable, n8n and Figma.", btn("tools.html", "Tool tutorials page", True) + btn("resources.html#learn", "147 learning sites") + btn("ai-academy-interactive.html#builder-tools", "AI Builder Tools"), [tools_tab()])
    tabs = [("aipm", "AI Product Management"), ("aide", "AI for Data Engineers"), ("aieng", "AI Engineer"), ("genai", "GenAI Launchpad"), ("tools", "Tools & tutorials")]
    nav = "".join(f'<button type="button" role="tab" data-t="{k}" aria-selected="false">{E(n)}</button>' for k, n in tabs)
    css = """<style>.hub{padding-block:18px 50px}.hub .htabs{position:sticky;top:var(--a-hh,68px);z-index:30;background:var(--bg);display:flex;gap:8px;overflow-x:auto;padding-block:12px;border-bottom:1px solid var(--line);margin-bottom:20px}
.hub .htabs button{flex:none;cursor:pointer;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:9px 16px;font:700 14.5px var(--body)}.hub .htabs button[aria-selected=true]{background:#5b4ee8;border-color:#5b4ee8;color:#fff}
.hub .eyebrow{font:700 12px var(--body);letter-spacing:.1em;text-transform:uppercase;color:#0e9fb8;margin:0}.hub h2{font:800 clamp(24px,3.4vw,32px)/1.2 var(--display);margin:4px 0 6px}.hub h3{font:700 19px var(--display);margin:24px 0 8px}
.hub .lede,.hub .mu{color:var(--mu)}.hub .acts{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.hub .hb{text-decoration:none;font:600 14px var(--body);padding:8px 13px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink)}.hub .hb.pri{background:#5b4ee8;border-color:#5b4ee8;color:#fff}
.hub details.hg{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:10px 16px;margin-bottom:10px}.hub details.hg>summary{cursor:pointer;font:700 16px var(--display)}.hub details.hg>summary em{font-style:normal;font-weight:500;color:var(--mu)}
.hub ol.cl,.hub ul.cl{display:grid;gap:6px;margin:10px 0;padding-left:0;list-style:none}.hub ol.cl>li,.hub ul.cl>li{display:flex;flex-direction:column;gap:2px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--bg)}
.hub .cl a{font-weight:600;color:#5b4ee8;text-decoration:none}.hub .cl a:hover{text-decoration:underline}.hub small{color:var(--mu);font-size:13px}.hub .tag{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:0 7px;font-size:11px;font-weight:600}
.hub .lv{font:700 10.5px var(--body);letter-spacing:.06em;text-transform:uppercase;margin-right:6px}.hub .lv-basic{color:#16a34a}.hub .lv-intermediate{color:#d97706}.hub .lv-advanced{color:#db2777}.hub ul.pdf li{flex-direction:row;justify-content:space-between;gap:10px}.hub .htab ul{padding-left:20px;color:var(--mu)}.hub .cl li{min-width:0}.hub .cl a{overflow-wrap:anywhere;min-width:0}.hub ul.pdf li{flex-wrap:wrap}.hub .htab{min-width:0}.hub .note{background:var(--surface);border:1px solid var(--line);border-left:4px solid #5b4ee8;border-radius:10px;padding:10px 14px;color:var(--mu);margin:0 0 16px}</style>"""
    js = ("<script>(function(){var ids=" + json.dumps([k for k, _ in tabs]) + ";var hh=document.querySelector('header.top');if(hh)document.documentElement.style.setProperty('--a-hh',hh.offsetHeight+'px');"
          "document.querySelectorAll('.hub .gsec a[href]').forEach(function(a){var h=a.getAttribute('href');if(!/^(https?:|#|mailto|tel)/.test(h))a.setAttribute('data-gate','1')});"
          "function show(){var h=(location.hash||'#aipm').slice(1),k=ids.indexOf(h)>-1?h:'aipm';document.querySelectorAll('.htab').forEach(function(s){s.hidden=s.id!==k});document.querySelectorAll('.htabs button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.t===k?'true':'false')})}"
          "document.querySelectorAll('.htabs button').forEach(function(b){b.addEventListener('click',function(){location.hash=b.dataset.t;window.scrollTo(0,0)})});window.addEventListener('hashchange',show);show()})();</script>")
    return css + f'<section class="hub"><div class="wrap"><div class="htabs" role="tablist" aria-label="Programs">{nav}</div><p class="note"><a href="study-library.html" style="font-weight:700;color:#5b4ee8">Study Library (all 11 sections on one page)</a> · Free access: enter your details once and every lesson, class, course and PDF in these tabs opens. Admins skip the form.</p>{aipm}{aide}{aieng}{genai}{tools}</div></section>' + js
