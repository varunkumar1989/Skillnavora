"""Builds the SFMC handbooks into handbook/sfmc/ from sfmc_content.py plus the capstone, roadmap, quick reference and interview material."""
import base64, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
from sfmc_content import MODULES, LABS

E = lambda t: html.escape(str(t), quote=True)
OUT = os.path.join(ROOT, "handbook", "sfmc")
LOGO = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "assets", "skillnavora-lockup.png"), "rb").read()).decode()
TAG = "Salesforce Marketing Cloud (SFMC) Academy. Verify product names, editions, licences and certifications on Salesforce's official pages."

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
body { font-family:'Inter','Segoe UI',Arial,sans-serif; color:#1d1b2e; font-size:10pt; line-height:1.5; margin:0; }
h1 { font-size:21pt; color:#2b1a66; margin:0 0 6pt; } h2 { font-size:15pt; color:#2b1a66; margin:16pt 0 6pt; border-bottom:2px solid #e3dff5; padding-bottom:3pt; break-after:avoid; }
h3 { font-size:11.5pt; color:#5a35c8; margin:12pt 0 4pt; break-after:avoid; } h4 { font-size:8.8pt; color:#0b7a75; text-transform:uppercase; letter-spacing:.04em; margin:7pt 0 2pt; break-after:avoid; }
p { margin:3pt 0 6pt; } ul,ol { margin:2pt 0 6pt; padding-left:16pt; } li { margin:1.5pt 0; } a { color:#5a35c8; word-break:break-word; }
.cover { height:238mm; display:flex; flex-direction:column; justify-content:space-between; padding:8mm 4mm; background:linear-gradient(160deg,#f5f3ff 0%,#fff 55%,#e9fbf8 100%); border-radius:6mm; break-after:page; }
.cover img { height:14mm; } .kick { font-size:10pt; letter-spacing:.14em; text-transform:uppercase; color:#0b7a75; font-weight:700; }
.sub { font-size:12.5pt; color:#3d3a55; max-width:150mm; } .tag { font-size:10.5pt; font-weight:700; color:#5a35c8; margin-top:10pt; } .note { font-size:8.6pt; color:#5b5876; }
.topic { break-inside:avoid-page; border:1px solid #e3dff5; border-radius:6pt; padding:7pt 10pt; margin:8pt 0; }
.def { background:#f5f3ff; border-left:4px solid #6a3fd1; padding:5pt 8pt; border-radius:3pt; }
.why { background:#ecfbf8; border-left:4px solid #0b7a75; padding:5pt 8pt; border-radius:3pt; }
.ex { background:#fff7e8; border-left:4px solid #d98a00; padding:5pt 8pt; border-radius:3pt; }
pre { background:#1e1b2e; color:#f2f0ff; padding:7pt 9pt; border-radius:5pt; font:7.8pt/1.42 'JetBrains Mono',Consolas,'Courier New',monospace; white-space:pre-wrap; word-break:break-word; margin:4pt 0 8pt; }
table { width:100%; border-collapse:collapse; font-size:8.4pt; margin:4pt 0 8pt; } th,td { border:1px solid #ddd8f2; padding:3.5pt 5pt; vertical-align:top; text-align:left; } th { background:#f5f3ff; color:#2b1a66; }
tr { break-inside:avoid; }
"""
FOOT = ('<div style="font-size:7.5pt;width:100%;padding:0 15mm;color:#6b6788;display:flex;justify-content:space-between;font-family:Arial">'
        '<span>© SkillNavora · SFMC Academy</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')


def cover(kicker, title, sub):
    return (f'<section class="cover"><div><img src="{LOGO}" alt="SkillNavora"></div><div><div class="kick">{E(kicker)}</div>'
            f'<h1 style="font-size:27pt;margin-top:8pt">{E(title)}</h1><div class="sub">{E(sub)}</div><div class="tag">{E(TAG)}</div></div>'
            '<div class="note">Varun Kumar · SkillNavora · skillnavora.in<br>Edition: November 2026. Practice labs marked "account" need a provisioned Marketing Cloud account. Other labs use sample files or paper.</div></section>')


def topic(t, module_no):
    links = "".join(f'<li><a href="{E(u)}">{E(n)}</a></li>' for n, u in t["links"])
    code = f'<h4>Code example, with line-by-line notes</h4><pre>{E(t["code"])}</pre>' if t.get("code") else ""
    lic = f'<p class="note"><b>Licence and edition:</b> {E(t["licence"])}</p>' if t.get("licence") else ""
    return (f'<div class="topic"><div class="note">Module {module_no}</div><h3>{E(t["t"])}</h3>'
            f'<h4>What is it?</h4><div class="def">{E(t["what"])}</div><h4>Why is it important?</h4><div class="why">{E(t["why"])}</div>'
            f'<h4>How does it work and the steps</h4><ol>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + '</ol>'
            f'<h4>Real-world example</h4><div class="ex">{E(t["example"])}</div>{code}{lic}'
            f'<h4>Common errors</h4><p>{E(t["mistake"])}</p><h4>Interview question</h4><p>{E(t["interview"])}</p>'
            f'<h4>Hands-on exercise</h4><p>{E(t["exercise"])}</p><h4>Official documentation and further reading</h4><ul>{links}</ul></div>')


def module_block(num, title, level, summary, topics, only_codes=False):
    head = f'<h2>Module {num}: {E(title)}</h2><p><b>Level:</b> {E(level)}. {E(summary)}</p>'
    body = "".join(topic(t, num) for t in topics if (not only_codes or t.get("code")))
    return head + body


def labs_block():
    rows = "".join(f"<tr><td>{E(c)}</td><td>{E(n)}</td><td>{'Needs a provisioned SFMC account' if k == 'account' else 'Simulated or paper practice'}</td></tr>" for c, n, k in LABS)
    return '<h2>Practical labs (Module 25)</h2><p>Each lab lists the objective, scenario, prerequisites, tools, dataset, steps, code, expected output, validation, common errors and assessment in the full lab workbook (next batch). Use this list to plan.</p><table><tr><th>Lab</th><th>Title</th><th>Requirement</th></tr>' + rows + '</table>'


CAPSTONES = [
 ("Project 1: End-to-end email marketing automation", "Customer data, segmentation, email design, AMPscript, campaign execution and performance reporting."),
 ("Project 2: Customer onboarding journey", "Customer data, Journey Builder, email, SMS, decision splits and performance tracking."),
 ("Project 3: E-commerce abandoned cart automation", "Transactional data, SQL segmentation, journey entry, personalised recommendations and multi-channel follow-up."),
 ("Project 4: Customer retention and re-engagement", "Engagement analysis with SQL and data views, segmentation, journey automation and KPI measurement."),
 ("Project 5: Enterprise Customer 360", "CRM data, contact model, data extensions, integration, Data Cloud architecture and unified profiles."),
 ("Project 6: API-driven marketing automation", "API architecture, authentication, external system integration, triggered messaging and error handling."),
 ("Project 7: Advanced personalisation engine", "Customer behaviour, AMPscript, dynamic content, segmentation and personalised journeys."),
 ("Project 8: AI-powered marketing automation platform", "SFMC data, AI integration, segmentation, campaign recommendations, automated reporting, human approval, security and monitoring."),
]
CAP_SECTIONS = ["Business problem", "Target users", "Project scope", "Functional requirements", "Non-functional requirements", "Solution architecture", "Data model", "Data flow diagram", "Technology stack", "Implementation steps", "SQL and AMPscript code where applicable", "Testing", "Screenshots or demo evidence", "KPIs", "Business impact", "Limitations", "Future enhancements", "Technical documentation", "Portfolio presentation", "Demo video"]

ROADMAP = [
 ("Stage 1 · Months 1 to 2", "CRM and marketing fundamentals, Salesforce ecosystem, SFMC basics (Modules 1 to 3)", "About 8 hours a week", "Lifecycle map, metrics calculations, business unit design", "Explain the lifecycle and metrics in an interview-style answer"),
 ("Stage 2 · Months 3 to 4", "Contacts, data architecture, data extensions, import and cleaning (Modules 4 and 5)", "About 10 hours a week", "Customer data extension with keys and a clean import", "Import a file with planted duplicates and fix it"),
 ("Stage 3 · Months 5 to 6", "SQL for SFMC, HTML and CSS, JavaScript basics, AMPscript (Modules 6, 9 and 10)", "About 12 hours a week", "Ten SQL queries, a responsive email, ten AMPscript personalisations", "Code review and a timed SQL test"),
 ("Stage 4 · Months 7 to 8", "Email Studio, Content Builder, Journey Builder, Automation Studio (Modules 7, 8, 11 and 12)", "About 12 hours a week", "Welcome journey, abandoned cart journey, scheduled automation", "Journey and automation walkthrough"),
 ("Stage 5 · Months 9 to 10", "CloudPages, Mobile Studio, personalisation, analytics, APIs and integrations (Modules 13 to 18)", "About 12 hours a week", "CloudPage form, REST integration, API-triggered email", "API demo with Postman and error handling"),
 ("Stage 6 · Month 11", "Data Cloud, advanced automation, security, deliverability, testing and architecture (Modules 19 to 23)", "About 10 hours a week", "Architecture document and a troubleshooting report", "Architecture presentation and scenario answers"),
 ("Stage 7 · Month 12", "AI in marketing, capstone projects, portfolio, interviews and certification planning (Modules 24, 26 to 28)", "About 15 hours a week", "Two capstone projects published with demo videos", "Three mock interviews and a certification plan"),
]

INTERVIEW = [
 ("SFMC fundamentals", ["What is SFMC?", "Explain SFMC architecture.", "What is a MID?", "What is a business unit?", "Explain contact key versus subscriber key."]),
 ("Data extensions", ["What is a sendable data extension?", "What is a primary key?", "Explain data retention.", "What is a shared data extension?"]),
 ("SQL", ["Explain SQL joins.", "Write a query to identify inactive subscribers.", "Explain ROW_NUMBER.", "Explain data views.", "How would you optimise a query?"]),
 ("Email Studio", ["Explain subscriber statuses.", "What are send classifications?", "Explain triggered sends.", "What is suppression management?"]),
 ("AMPscript", ["What is AMPscript?", "Explain Lookup and LookupRows.", "Explain AttributeValue.", "Write a personalised email.", "How do you troubleshoot AMPscript errors?"]),
 ("Journey Builder", ["Explain entry sources.", "What is a Decision Split?", "What is an Engagement Split?", "Explain journey re-entry.", "How do you troubleshoot journey entry failures?"]),
 ("Automation Studio", ["Explain SQL Query Activity.", "What is a File Transfer Activity?", "How do you create a scheduled automation?", "How do you troubleshoot automation failures?"]),
 ("CloudPages", ["What are CloudPages?", "Explain RequestParameter.", "How do you capture form data?", "How do you protect customer information?"]),
 ("APIs", ["Explain REST versus SOAP.", "What is OAuth 2.0?", "What are installed packages?", "How do you integrate an external system?"]),
 ("Architecture", ["Design a multi-business-unit SFMC solution.", "Explain customer data architecture.", "How do you integrate Sales Cloud and SFMC?", "How would you design an enterprise marketing automation platform?"]),
 ("AI", ["How can AI improve marketing automation?", "Explain predictive personalisation.", "How can an AI assistant integrate with SFMC?", "How do you ensure customer data security?"]),
 ("Scenarios", ["A campaign has a high bounce rate. How do you investigate?", "An email send failed. What steps would you take?", "A journey is not accepting new contacts. How do you troubleshoot?", "A customer receives duplicate emails. How would you identify the root cause?", "A SQL query is returning duplicate records. How would you fix it?", "An automation failed during a production run. How would you handle it?", "A business needs customer data from multiple systems. How would you design the integration?", "A customer wants personalised communications across email and SMS. How would you build the journey?"]),
 ("Behavioural", ["Tell me about yourself.", "Describe an SFMC implementation.", "Explain a difficult production issue.", "Describe a technical problem you solved.", "How do you handle stakeholders?", "How do you manage urgent campaign requests?", "Explain your approach to testing and quality."]),
]

QUICK = [
 ("SQL in SFMC", "SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, JOIN types, CASE WHEN, COUNT, SUM, AVG, MIN, MAX, ROW_NUMBER. Check the SFMC SQL restrictions before use."),
 ("AMPscript functions", "VAR, SET, IF/ELSEIF/ELSE/ENDIF, FOR, Lookup, LookupRows, LookupOrderedRows, RowCount, Row, Field, InsertDE, UpdateDE, UpsertDE, DeleteDE, AttributeValue, ProperCase, Concat, Substring, Empty, v()."),
 ("Data views", "_Subscribers, _Sent, _Open, _Click, _Bounce, _Unsubscribe, _Job, _Journey, _JourneyActivity, _SMSMessageTracking, _Complaint, _BusinessUnitUnsubscribes. Keys and retention limits are in the official data view documentation."),
 ("Journey Builder", "Entry sources (data extension, API event, Salesforce data, audience); activities (email, SMS, push, wait, update contact); splits (decision, engagement, random); exit criteria; re-entry rules."),
 ("Automation Studio", "SQL Query, Data Extract, File Transfer, Import File, Filter, Script, Verification, send and wait activities; schedule and file-trigger starts."),
 ("Deliverability", "SPF (authorised senders), DKIM (signature), DMARC (policy and reports), hard and soft bounces, complaints, suppression, sender and domain reputation, inbox placement."),
 ("APIs", "REST (JSON over HTTP), SOAP (XML with WSDL), OAuth 2.0 client credentials, installed package, access token, bearer header, scopes, rate limits, pagination, webhooks."),
 ("Troubleshooting checklist", "Confirm impact; check the error and the log; check recent changes; reproduce with a test contact; check data and keys; fix; verify; document the root cause."),
]
