"""Builds the WhatsApp agent knowledge workbook from the website's own data (config.js, search index, data-science catalog)."""
import json, re, html
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

import os, subprocess, tempfile
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = tempfile.gettempdir()
# read the site's own config (assets/config.js) through Node, so the workbook always matches the website
_js = r"""const fs=require('fs');const src=fs.readFileSync(process.argv[1],'utf8');
const names=["SITE","COURSES","FAQS","OFFERS","JOB_ASSIST","MOAT","AUDIENCE","COMPARE","SUPPORT","REFERRAL","STATS"];
const d=new Function(src+';return {'+names.map(n=>n+':(typeof '+n+'!=="undefined"?'+n+':null)').join(',')+'};')();
process.stdout.write(JSON.stringify(d));"""
cfg = json.loads(subprocess.run(["node", "-e", _js, os.path.join(R, "assets", "config.js")], capture_output=True, text=True, check=True).stdout)
BASE = "https://www.skillnavora.in"
search = json.load(open(f"{R}/assets/search-index.json", encoding="utf-8"))
cat = json.load(open(f"{R}/data-science/catalog.json", encoding="utf-8"))
clean = lambda s: re.sub(r"\s+", " ", html.unescape(str(s))).strip()

HEAD = PatternFill("solid", fgColor="1F1B3A")
FONT_H = Font(bold=True, color="FFFFFF")
FLAG = PatternFill("solid", fgColor="FFF4CC")

def sheet(wb, title, headers, rows, widths=None, flag_col=None):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for c in ws[1]:
        c.fill, c.font = HEAD, FONT_H
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append([clean(x) if isinstance(x, str) else x for x in r])
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
        if flag_col is not None and str(row[flag_col].value or "").startswith("CONFIRM"):
            for c in row: c.fill = FLAG
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for i, h in enumerate(headers, 1):
        w = (widths or {}).get(h, 28)
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws

wb = Workbook(); wb.remove(wb.active)

# 0. README
readme = [
 ["Purpose", "Knowledge base for the SkillNavora WhatsApp agent. Every answer the agent gives should come from these tabs, with the source link."],
 ["Source", "Built from the SkillNavora website: assets/config.js (programmes, fees, FAQs, offers), the site search index (all public pages), and the data-science course catalogue (free lessons)."],
 ["Last built", "Generated from the website data; rebuild with: python3 whatsapp-agent/build_kb.py"],
 ["How to use", "1) Find the question's topic in Agent_Lookup. 2) Open that tab. 3) Answer in plain words with the source link. 4) If the row is marked CONFIRM, say the detail is being confirmed and offer a counsellor call."],
 ["Yellow rows", "Need owner confirmation before the agent quotes them. See the Needs_Confirmation tab."],
 ["Never say", "That any job, placement or salary is guaranteed. Placement statistics (the hidden 'students placed' and 'highest package' numbers are NOT used here). Any discount other than the published scholarship and student offers."],
 ["Always say", "Fees are shown in USD and INR as listed. Scholarships are decided after a test and a counselling call. Career guidance is not job placement."],
 ["Secrets", "API keys, the Web3Forms key and chatbot settings are deliberately excluded from this file."],
 ["Escalation", "Anything not in this file: offer a free counselling call (booking link on the website) or WhatsApp support."],
]
sheet(wb, "START_HERE", ["Item", "Detail"], readme, {"Item": 18, "Detail": 110})

# 1. Programmes
prog_rows = []
page_of = {"ai-pm": f"{BASE}/program/ai-product-management.html", "ai-de": f"{BASE}/program/ai-data-engineering.html", "genai-launchpad": f"{BASE}/program/genai-launchpad.html"}
for c in cfg["COURSES"]:
    prog_rows.append([c["name"], c["tagline"], c["duration"], c["format"], c["fee"], c["feeINR"], c["feeNote"],
                      "; ".join(c["highlights"]), c.get("cohort") or "CONFIRM: start date not published", page_of.get(c["id"], "")])
sheet(wb, "Programmes", ["Programme", "What it is", "Duration", "Format", "Fee (USD)", "Fee (INR)", "What the fee includes", "Highlights", "Cohort / start", "Page"],
      prog_rows, {"What it is": 45, "What the fee includes": 45, "Highlights": 55, "Page": 50, "Cohort / start": 30}, flag_col=8)

# 2. Fees and offers
fee_rows = []
for c in cfg["COURSES"]:
    fee_rows.append([c["name"], c["fee"], c["feeINR"], "Full fee, as listed on the website", "CONFIRM: exchange rate and fee to be confirmed before each cohort" if c["id"] in ("ai-pm",) else ""])
for o in cfg["OFFERS"]["items"]:
    fee_rows.append(["Offer: " + o["title"], o.get("pct", ""), "", o["text"], "CONFIRM: scholarship and offer rules need owner sign-off" if "Up to" in o.get("pct", "") or "scholarship" in o["title"].lower() else ""])
fee_rows.append(["Offers in general", "", "", cfg["STATS"].get("note", ""), ""])
fee_rows.append(["Early-bird pricing", "", "", "No early-bird pricing is currently published on the website.", ""])
sheet(wb, "Fees_and_Offers", ["Item", "Price or percentage", "Price (INR)", "Detail", "Note"], fee_rows,
      {"Item": 34, "Detail": 70, "Note": 50}, flag_col=4)

# 3. Why join
why = []
for c in cfg["COMPARE"]:
    why.append(["Comparison", c["what"], c["sub"], c.get("us", ""), c.get("others", "")])
for m in cfg["MOAT"]:
    why.append(["Why SkillNavora", m["title"], "", m["text"], ""])
for a in cfg["AUDIENCE"]:
    why.append(["Who it is for", a["title"], "", a["text"], ""])
sheet(wb, "Why_Join", ["Type", "Point", "Detail", "SkillNavora", "Typical alternatives"], why,
      {"Point": 36, "Detail": 30, "SkillNavora": 70, "Typical alternatives": 40})

# 4. Career support
cs = []
for x in cfg["JOB_ASSIST"]["program"]: cs.append(["Job assistance: program", x])
for x in cfg["JOB_ASSIST"]["interview"]: cs.append(["Job assistance: interview prep", x])
for s in cfg["SUPPORT"]: cs.append(["Support", s["title"] + ": " + s["text"]])
cs.append(["Important", "This is career guidance, not job placement. No job, interview or salary is guaranteed."])
cs.append(["Referral", "Referral rewards: " + cfg["REFERRAL"]["terms"]])
sheet(wb, "Career_Support", ["Area", "What is included"], cs, {"Area": 30, "What is included": 110})

# 5. FAQ
faq_rows = [[f["c"], f["q"], f["a"], f"{BASE}/programs.html", "" ] for f in cfg["FAQS"]]
sheet(wb, "FAQ", ["Category", "Question", "Answer", "Link", "Note"], faq_rows, {"Question": 40, "Answer": 90, "Link": 36})

# 6. Website pages (every public page)
pages = []
for e in search:
    url = BASE + (e["u"] if e["u"] != "/" else "/")
    pages.append([e["t"], url, e["d"]])
sheet(wb, "Website_Pages", ["Page title", "Link", "What the page covers"], pages, {"Page title": 50, "Link": 55, "What the page covers": 90})

# 7. Free lessons (data-science catalogue)
free = []
for t in cat["tracks"]:
    for l in t["lessons"]:
        free.append([t["name"], l["num"], l["title"], f"{BASE}/data-science/{l['page']}", f"{BASE}/data-science/{l['pdf_path']}", l.get("live", "")])
sheet(wb, "Free_Lessons", ["Track", "Lesson no.", "Lesson title", "Read online", "PDF", "Live class (if any)"], free,
      {"Track": 30, "Lesson title": 60, "Read online": 60, "PDF": 60})

# 8. Contact
s = cfg["SITE"]
contact = [
 ["WhatsApp", "+" + s["whatsapp"], f"https://wa.me/{s['whatsapp']}"],
 ["Email", s["email"], "mailto:" + s["email"]],
 ["Phone", "+" + s["phone"], ""],
 ["Founder on LinkedIn", "Varun Kumar", s["founderLinkedin"]],
 ["SkillNavora LinkedIn", "", s["linkedin"]],
 ["Instagram", "", s["instagram"]],
 ["YouTube", "", s["youtube"]],
 ["X (Twitter)", "", s["twitter"]],
 ["Facebook", "", s["facebook"]],
 ["Free counselling booking", "CONFIRM: no booking link set in site settings", s["booking"] or "CONFIRM"],
 ["Office address", "CONFIRM: no address set in site settings", s["address"] or "CONFIRM"],
 ["Community / Telegram", "Not set", ""],
]
sheet(wb, "Contact", ["Channel", "Detail", "Link"], contact, {"Channel": 28, "Detail": 40, "Link": 60}, flag_col=1)

# 9. Agent lookup: question keywords -> tab
lookup = [
 ["fee, fees, price, cost, how much, INR, rupees, dollars, EMI", "Fees_and_Offers", "Fees and offers"],
 ["programme, program, course, which course, AI PM, data engineer, GenAI, syllabus, what will I learn", "Programmes", "Programme details"],
 ["free, free course, free lesson, free resource, PDF, tutorial, without paying", "Free_Lessons and Website_Pages", "Free resources"],
 ["why join, why skillnavora, better, difference, compare, who is it for, student, fresher, career switch", "Why_Join", "Reasons to join"],
 ["job, placement, placed, interview, resume, LinkedIn, salary, hire, referral, guarantee", "Career_Support and FAQ", "Career support (never a guarantee)"],
 ["certificate, recording, live class, timing, schedule, weekend, attend, alongside job", "FAQ", "Delivery and schedule"],
 ["scholarship, discount, offer, early bird, student discount, refund", "Fees_and_Offers", "Offers"],
 ["contact, call, WhatsApp, email, address, booking, counselling, talk to someone", "Contact", "Contact and counselling"],
 ["anything else", "Website_Pages", "Search the page list and offer a link or a counselling call"],
]
sheet(wb, "Agent_Lookup", ["Words a learner might use", "Tab to answer from", "Answer type"], lookup, {"Words a learner might use": 70, "Tab to answer from": 30, "Answer type": 40})

# 10. Needs confirmation
conf = [
 ["Scholarship 'up to 100%'", "Shown on the website banner and offers. Confirm the eligibility rules and seat limits in writing before the agent quotes it."],
 ["Monthly 1:1 with a CEO or Head of Product", "Shown as a benefit. Confirm how often it happens and who runs it for each cohort."],
 ["25+ real-world case studies", "Shown as a benefit. The Case Study Library PDF lists 12 cases. Confirm how the 25+ is counted, or change the number."],
 ["Cohort start dates", "Not published for any programme. The agent should not invent dates."],
 ["INR fees", "Fees converted to rupees on the site (for example $2,000 = ₹1,74,000) imply different exchange rates. Confirm the INR amounts."],
 ["Counselling booking link and office address", "Not set in the site settings. The agent should not give a link or address until these are added."],
 ["Placement statistics", "Hidden on the site (config show = false). Do not use unless verified and published."],
]
sheet(wb, "Needs_Confirmation", ["Item", "Why it needs confirming"], conf, {"Item": 40, "Why it needs confirming": 100})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SkillNavora_WhatsApp_Agent_Knowledge.xlsx")
wb.save(OUT)
print("sheets:", wb.sheetnames)
print({ws.title: ws.max_row-1 for ws in wb.worksheets})
