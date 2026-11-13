"""Flat question-and-answer list for n8n: one row per question, generated from the website's data (assets/config.js and the course catalogue).
Run: python3 whatsapp-agent/build_qa.py   -> writes knowledge_qa.csv and knowledge_qa.json next to this file."""
import csv, json, os, re, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
BASE = "https://www.skillnavora.in"
JS = r"""const fs=require('fs');const src=fs.readFileSync(process.argv[1],'utf8');
const names=["SITE","COURSES","FAQS","OFFERS","JOB_ASSIST","MOAT","COMPARE","SUPPORT","REFERRAL","STATS"];
const d=new Function(src+';return {'+names.map(n=>n+':(typeof '+n+'!=="undefined"?'+n+':null)').join(',')+'};')();
process.stdout.write(JSON.stringify(d));"""
cfg = json.loads(subprocess.run(["node", "-e", JS, os.path.join(ROOT, "assets", "config.js")], capture_output=True, text=True, check=True).stdout)
cat = json.load(open(os.path.join(ROOT, "data-science", "catalog.json"), encoding="utf-8"))
clean = lambda s: re.sub(r"\s+", " ", html.unescape(str(s))).strip()

rows = []
def add(topic, keywords, question, answer, link, confirm=""):
    rows.append({"id": len(rows) + 1, "topic": topic, "keywords": keywords, "question": question,
                 "answer": clean(answer), "link": link, "confirm": confirm})

page = {"ai-pm": f"{BASE}/program/ai-product-management.html", "ai-de": f"{BASE}/program/ai-data-engineering.html",
        "genai-launchpad": f"{BASE}/program/genai-launchpad.html"}
short = {"ai-pm": "AI PM|product management|AI product manager|PM course", "ai-de": "data engineer|data engineering|AI data",
         "genai-launchpad": "GenAI|genai launchpad|generative AI|AI launchpad"}

# All fees at once, for "what is the fee?" without a programme name (placed first so it wins ties)
add("Fees", "fee,fees,price,cost,how much,pricing,charges", "What are the fees for the programmes?",
    "Here are our programme fees: " + " ".join(f"{c['name']}: {c['fee']} (about {c['feeINR']})." for c in cfg["COURSES"]) + " Which one are you interested in? I can share what it includes.",
    f"{BASE}/programs.html", "CONFIRM: fee and INR amount before each cohort")

# Who each programme is for ("is this right for me?")
for c in cfg["COURSES"]:
    k, u = c["id"], page.get(c["id"], BASE)
    aud = c.get("audience") or []
    if aud:
        add("Who it is for", f"who is it for,who is this for,right for me,suitable,suit me,fit for me,am i eligible,eligible,eligibility,background,can i join,good for me,{short[k]}",
            f"Who is {c['name']} for?", f"{c['name']} is a good fit for: " + " ".join(f"{a['title']}: {a['text']}" for a in aud) + " Tell me a little about your background and I can point you to the right next step.", u)

# Programmes: fee, length, format, what is included, highlights, cohort
for c in cfg["COURSES"]:
    k, u = c["id"], page.get(c["id"], BASE)
    n = c["name"]
    add("Fees", f"fee,fees,price,cost,how much,rupees,dollars,{short[k]}", f"What is the fee for {n}?",
        f"{n} costs {c['fee']} (about {c['feeINR']} in INR) as listed on the website. {c['feeNote']}", u, "CONFIRM: fee and INR amount before each cohort" if k == "ai-pm" else "")
    add("Programme", f"duration,how long,weeks,{short[k]}", f"How long is the {n} programme?",
        f"{n} runs for {c['duration']}. Format: {c['format']}.", u)
    add("Programme", f"learn,syllabus,curriculum,what will I learn,{short[k]}", f"What will I learn in {n}?",
        f"{c['tagline']}. Highlights: {'; '.join(c['highlights'])}.", u)
    add("Fees", f"included,what is included,fee includes,{short[k]}", f"What is included in the {n} fee?", c["feeNote"], u)
    add("Schedule", f"start date,cohort,when does it start,batch,{short[k]}", f"When does the {n} cohort start?",
        "Start dates are not published on the website yet. A counsellor will share the next cohort date.", u, "CONFIRM: no cohort date published")

# Overviews: broad questions such as "what does this programme offer" (placed before the detailed rows)
for c in cfg["COURSES"]:
    k, u = c["id"], page.get(c["id"], BASE)
    n = c["name"]
    add("Overview", f"offer,offers,offering,what does,what do i get,overview,benefit,what is in,{short[k]}",
        f"What does the {n} programme offer?",
        f"{n}: {c['tagline']}. Duration {c['duration']}, {c['format'].lower()}. Fee {c['fee']} (about {c['feeINR']} in INR), which includes {c['feeNote'].replace('Includes ', '').rstrip('.')}. Highlights: {'; '.join(c['highlights'])}.", u)
add("Overview", "about skillnavora,what is skillnavora,who are you,what do you offer,overview", "What does SkillNavora offer?",
    f"{cfg['SITE']['name']} runs live, AI-first programmes in product management, data engineering and generative AI, with recordings, hands-on projects, capstones, mock tests and career guidance (not job placement). Several free resources are also available: lessons, PDFs, practice tests and free workshops.", BASE)
add("Instructors", "instructor,instructors,teacher,teachers,trainer,faculty,mentor,mentors,who teaches,who will teach",
    "Who teaches the programmes and who are the mentors?",
    "Live classes are taught by instructors, and you can ask them questions during live classes, in 1:1 mentorship, and through the learning system. The AI-First Product Management programme includes a monthly 1:1 counselling session with a CEO or Head of Product.", f"{BASE}/programs.html",
    "CONFIRM: owner to confirm the instructor and mentor line-up before listing names")

add("Certificate", "certificate,certificates,certification,completion,diploma,proof of completion", "Do I get a certificate?",
    "Yes. You get a certificate when you complete the programme and the capstone.", f"{BASE}/programs.html")

# Offers and scholarships
for o in cfg["OFFERS"]["items"]:
    add("Offers", "scholarship,discount,offer,student,concession,reduced fee,free seat",
        f"Is there a {o['title'].lower()}?", f"{o['title']}: {o['text']} ({o.get('pct','')}).", f"{BASE}/programs.html",
        "CONFIRM: owner must confirm eligibility and seat limits" if "100" in o.get("pct", "") or "scholarship" in o["title"].lower() else "")
add("Offers", "early bird,early,discount date", "Is there early-bird pricing?", "No early-bird pricing is published on the website right now.", f"{BASE}/programs.html")
add("Offers", "refund,money back", "Can I get a refund?", "Please ask a counsellor for the refund policy for your programme before you pay.", f"{BASE}/refund.html", "CONFIRM: refund rules to be checked against refund.html")

# Why join
add("Why join", "why join,why skillnavora,why should I join,benefit,reason", "Why should I join SkillNavora?",
    " ".join(f"{m['title']}: {m['text']}" for m in cfg["MOAT"]), f"{BASE}/programs.html")
for cmp in cfg["COMPARE"]:
    add("Why join", f"compare,difference,better,{cmp['what'].lower()}", f"How is SkillNavora different on {cmp['what'].lower()}?",
        f"SkillNavora: {cmp.get('us','')}. Typical alternatives: {cmp.get('others','')}.", f"{BASE}/programs.html")
add("Who it is for", "who is this for,eligible,student,fresher,working,career switch,salary hike,right for me,suitable,background,can i join," + short["ai-pm"],
    "Who is this programme for?", "AI-First Product Management is a good fit for: " + " ".join(f"{x}" for x in ["Students and freshers: build PM skills and a portfolio before your first job.",
    "Working professionals: learn on weekends with live classes and recordings.",
    "Career switchers: move into product from engineering, design, sales, operations or consulting.",
    "Salary hike and promotion: grow into senior PM and AI PM roles with stronger skills."]), f"{BASE}/programs.html")

# Career
add("Career", "job,placement,placed,guarantee,job guarantee,will I get a job,salary", "Do you guarantee a job or placement?",
    "No. SkillNavora offers career guidance, not job placement, and no job, interview or salary is guaranteed.", f"{BASE}/programs.html")
add("Career", "resume,linkedin,career guidance,job search", "What career support is included?",
    "Program: " + " ".join(cfg["JOB_ASSIST"]["program"]) + " Interview prep: " + " ".join(cfg["JOB_ASSIST"]["interview"]), f"{BASE}/programs.html")
add("Career", "interview,mock test,mock interview,question bank", "How do you prepare me for interviews?",
    " ".join(cfg["JOB_ASSIST"]["interview"]), f"{BASE}/practice-hub.html")
add("Career", "referral,refer,reward,refer a friend", "How does the referral reward work?", cfg["REFERRAL"]["terms"], f"{BASE}/refer.html", "CONFIRM: reward amounts are not published")

# FAQ (every FAQ from the website)
for f in cfg["FAQS"]:
    add("FAQ", f"{f['c'].lower()},{f['q'].lower()}", f["q"], f["a"], f"{BASE}/programs.html")

# Free courses and lessons
for t in cat["tracks"]:
    lessons = len(t["lessons"])
    add("Free courses", f"free,free course,free lesson,{t['name'].lower()},{t['id']}", f"Is there a free {t['name']} course?",
        f"Yes. {t['name']} has {lessons} free lessons, each with a read-online page and a PDF. {clean(t.get('desc',''))}",
        f"{BASE}/data-science/index.html")
add("Free courses", "free,free course,free resources,free tools,without paying", "What free courses and resources are there?",
    "Free data-science and AI lessons (" + str(sum(len(t['lessons']) for t in cat['tracks'])) + " lessons across " + str(len(cat['tracks'])) +
    " tracks), free PM handbook PDFs, a free AI tutor, practice tests, and free live workshops. Ask us for the link you need.", f"{BASE}/learning-platform.html")
add("Free courses", "free live,workshop,webinar,event", "Are there free live sessions?", "Yes. See the events page for upcoming free live sessions and their dates.", f"{BASE}/events.html", "CONFIRM: dates change, check the events page")

# Contact
s = cfg["SITE"]
add("Contact", "contact,whatsapp,phone,call,email,talk to someone,counselling,counseling",
    "How can I contact SkillNavora?", f"WhatsApp: +{s['whatsapp']}. Email: {s['email']}. You can also book a free counselling session on the website.",
    f"https://wa.me/{s['whatsapp']}")
add("Contact", "address,office,location", "Where is SkillNavora located?", "The office address is not published on the website yet.", f"{BASE}/contact.html", "CONFIRM: address not set")
add("Contact", "social,instagram,youtube,linkedin,twitter,facebook", "What are your social media links?",
    f"Instagram: {s['instagram']}. YouTube: {s['youtube']}. LinkedIn: {s['linkedin']}. X: {s['twitter']}. Facebook: {s['facebook']}.", BASE)

# Vaitis free AI library
add("Free courses", "vaitis,b100x,ai tools,ai tool,tools list,ai library,which ai tool,best ai tools,free ai tools,ai tools for,prompts,workflows,step by step guide,guides",
    "Where can I find AI tools, prompts and step-by-step AI guides?",
    "Vaitis (B100x with AI) is SkillNavora's free AI library: 763 AI tools in 26 categories with pricing, plus 25 step-by-step guides with ready-to-copy prompts and commands (AI sales agent, Instagram manager, resume panel, scraping dashboards, free AI routers and more). Sign up free once to open it.",
    f"{BASE}/vaitis.html")

# Small talk: thanks and goodbye
add("Thanks", "thanks,thank you,thank u,thankyou,thx,ty,ok thanks,okay thanks,bye,goodbye,see you",
    "Thank you", "You're welcome! 😊 If anything else comes up, just message here. You can also book a free counselling call whenever you're ready.", f"{BASE}/contact.html")

# Fallback
add("Fallback", "", "Anything else", "I don't have that information yet. Message us on Instagram and someone from our team will reply to you directly.",
    "https://ig.me/m/skillnavora", "")

with open(os.path.join(HERE, "knowledge_qa.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
with open(os.path.join(HERE, "knowledge_qa.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
# Same answers for the website's Ask AI panel (loaded on demand, no AI call needed for these)
site_rows = [{k: r[k] for k in ("id", "topic", "keywords", "question", "answer", "link", "confirm")} for r in rows]
with open(os.path.join(ROOT, "assets", "knowledge_qa.json"), "w", encoding="utf-8") as f:
    json.dump(site_rows, f, ensure_ascii=False, separators=(",", ":"))
print("rows:", len(rows), "| topics:", sorted({r["topic"] for r in rows}))
# Content index: every public page, free lesson and PDF, so the Ask AI panel can point to the right place for any topic
import glob, urllib.parse
content = []
for e in json.load(open(os.path.join(ROOT, "assets", "search-index.json"), encoding="utf-8")):
    content.append({"title": clean(e["t"]), "desc": clean(e.get("d", "")), "link": BASE + e["u"], "type": "Page"})
for t in cat["tracks"]:
    for l in t["lessons"]:
        content.append({"title": clean(l["title"]), "desc": f"Free lesson, {t['name']}", "link": f"{BASE}/data-science/{l['page']}", "type": "Lesson"})
        content.append({"title": clean(l["title"]), "desc": f"PDF of the free lesson, {t['name']}", "link": f"{BASE}/data-science/{l['pdf_path']}", "type": "PDF"})
seen = set()
for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.pdf"), recursive=True)):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel.startswith(("node_modules/", ".git/", "data-science/pdf/")):   # lesson PDFs are already listed above
        continue
    name = os.path.splitext(os.path.basename(rel))[0].replace("-", " ").replace("_", " ")
    if name in seen:
        continue
    seen.add(name)
    content.append({"title": name, "desc": "PDF in " + os.path.dirname(rel).replace("/", " / ") if os.path.dirname(rel) else "PDF", "link": BASE + "/" + urllib.parse.quote(rel), "type": "PDF"})
with open(os.path.join(ROOT, "assets", "content_index.json"), "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, separators=(",", ":"))
print("content index:", len(content), "entries")

