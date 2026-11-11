"""Builds the extra handbooks: PM glossary, tokens and pricing, Vibe Coding addendum, and the AI data engineering
course completion addendum (gap-check material mapped to each course module, without changing existing lessons)."""
import base64, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "gap"))
from extras_content import PM_GLOSSARY, TOKEN_PRICES, PRICE_SOURCE, PRICE_DATE, TOKEN_LINKS, VIBE_GAPS
from gap_audit import AUDIT
from gap_supplement_a import A_SECTIONS
from gap_supplement_b import B_SECTIONS
from gap_supplement_c import C_SECTIONS
from gap_build import CSS, FOOT, topic as gap_topic
E = lambda t: html.escape(str(t), quote=True)
LOGO = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "assets", "skillnavora-lockup.png"), "rb").read()).decode()
PM_OUT = os.path.join(ROOT, "handbook", "pm-extras"); COURSE_OUT = os.path.join(ROOT, "handbook", "course-additions")

def cover(kicker, title, sub, tag):
    return (f'<section class="cover"><div><img src="{LOGO}" alt="SkillNavora" style="height:14mm"></div><div><div class="kick">{E(kicker)}</div>'
            f'<h1 style="font-size:27pt;margin-top:8pt">{E(title)}</h1><div class="sub">{E(sub)}</div><div class="tag">{E(tag)}</div></div>'
            '<div class="note">Varun Kumar · SkillNavora · skillnavora.in<br>Edition: November 2026. Links point to official sites; check them before you share.</div></section>')

def glossary_body():
    letters = {}
    for term, d, ex in sorted(PM_GLOSSARY, key=lambda x: x[0].lower()):
        letters.setdefault(term[0].upper(), []).append((term, d, ex))
    body = '<h1>Product Manager Glossary: keywords and definitions</h1><p>Every term a product manager needs, with a plain definition and an example. Terms are grouped by first letter.</p>'
    body += '<h2>Index</h2><p>' + " · ".join(f'<a href="#{k}">{k}</a>' for k in letters) + '</p>'
    for k, items in letters.items():
        body += f'<h2 id="{k}">{k}</h2>'
        for term, d, ex in items:
            body += f'<div class="topic" style="padding:5pt 9pt;margin:4pt 0"><b>{E(term)}</b><br>{E(d)}<br><span class="note"><b>Example:</b> {E(ex)}</span></div>'
    return body

def tokens_body():
    rows = "".join(f"<tr><td>{E(n)}</td><td>{E(i)}</td><td>${p_in:.2f}</td><td>${p_out:.2f}</td><td>{E(note)}</td></tr>" for n, i, p_in, p_out, note in TOKEN_PRICES)
    sample_in, sample_out = 2000, 1000
    ex_rows = "".join(f"<tr><td>{E(n)}</td><td>${(sample_in*p_in + sample_out*p_out)/1e6:.4f}</td><td>${((sample_in*p_in + sample_out*p_out)/1e6)*1000:.2f}</td></tr>" for n, i, p_in, p_out, note in TOKEN_PRICES)
    links = "".join(f'<li><a href="{E(u)}">{E(n)}</a></li>' for n, u in TOKEN_LINKS)
    return f'''<h1>Tokens, Pricing and Tokenization</h1>
<p>This handbook explains what a token is, how models read it, how you are charged, and how to choose between Haiku, Sonnet, Opus and Fable. It also shows a worked example from an AI app builder such as Lovable.</p>
<h2>1. What is a token?</h2><div class="def">A token is a small piece of text that a language model reads or writes. A short common word is usually one token; a long or unusual word can be several. Spaces, punctuation and numbers also count.</div>
<h4>How tokenization works</h4><p>Before a model reads your text, a tokenizer splits it into tokens. The split depends on the model's tokenizer, so the same sentence can produce different counts on different models. You can count exactly with the official token-counting endpoint before you send a request.</p>
<div class="ex">Example: the sentence "Build a login page." is about 6 tokens: "Build", " a", " login", " page", "." and the newline or padding that the API adds. Count your real text, not this estimate.</div>
<h4>Input and output tokens</h4><ul><li><b>Input tokens</b> are everything you send: your instruction, the system prompt, the files you attach, and the earlier messages in the conversation.</li><li><b>Output tokens</b> are everything the model writes back: the answer, the code, or the explanation.</li></ul>
<p>Output is usually priced higher than input. Long chats cost more each turn because the earlier messages are sent again with each new request.</p>
<h2>2. How the price is calculated</h2><div class="def">Cost = (input tokens / 1,000,000 × input price) + (output tokens / 1,000,000 × output price). Prices are per million tokens.</div>
<h2>3. Current prices by model</h2><p class="note">{E(PRICE_DATE)} Source: <a href="{E(PRICE_SOURCE)}">{E(PRICE_SOURCE)}</a></p>
<table><tr><th>Model</th><th>Model ID</th><th>Input per million tokens</th><th>Output per million tokens</th><th>What it is for</th></tr>{rows}</table>
<h2>4. Worked example: what one request costs</h2><p>Sample request: 2,000 input tokens and 1,000 output tokens. Costs are per request and per 1,000 requests.</p>
<table><tr><th>Model</th><th>Cost of one request</th><th>Cost of 1,000 requests</th></tr>{ex_rows}</table>
<p class="note">Haiku 5.5 prices above apply to prompts up to 100K tokens. Batch processing is priced at half price for jobs that do not need an instant answer. Prompt caching makes repeated context cheaper to re-send.</p>
<h2>5. Haiku, Sonnet, Opus or Fable: which to use</h2>
<ul><li><b>Haiku 5.5</b>: fast and cheapest. Use for classification, extraction, short replies, routing and high-volume tasks. Test quality on your own examples first.</li>
<li><b>Sonnet 5.5</b>: the balanced choice for everyday coding, agents and business tasks where quality and cost both matter.</li>
<li><b>Opus 5.5</b>: stronger reasoning and coding for harder tasks at a higher price.</li>
<li><b>Fable 5.2</b>: the most capable widely released model, for the hardest reasoning and long agentic work. It has the highest price in this table.</li></ul>
<p>Start with the cheapest model that passes your own test set. Move up only when a measured quality gap justifies the higher cost.</p>
<h2>6. Ways to use fewer tokens</h2><ul><li>Keep instructions short and specific; remove repeated text.</li><li>Start a new chat for each new feature so old messages are not resent every turn.</li><li>Cap the output length when you only need a short answer.</li><li>Use prompt caching for long, unchanged context such as a product manual.</li><li>Use batch processing for reports and overnight jobs that do not need instant answers.</li><li>Count tokens before you send a long document.</li></ul>
<h2>7. Example: an AI app builder (Lovable-style)</h2>
<p>You ask an AI app builder to "add a login page and a 'forgot password' link". The request uses tokens in three places:</p>
<ol><li><b>Input:</b> your new message, the app's current code and design context that the builder sends with it, and the earlier messages in the chat.</li><li><b>Output:</b> the code changes the builder writes back, which can be long for a whole page.</li><li><b>Credits:</b> the builder's own plan may charge credits per action or per message. Those credits are a separate charge from the model's per-token price. Check Lovable's current pricing on its own site.</li></ol>
<div class="ex">Practical rule: keep one chat per feature, ask for one change at a time, and review the diff before you accept it. Smaller, focused requests use fewer tokens and are easier to debug.</div>
<p>This is the same reasoning you use when you see the model prices above: the longer the context and the longer the output, the higher the cost.</p>
<h2>8. Tokenization exercise</h2><ol><li>Paste a 500-word product brief into the token-counting endpoint, then count it again after you cut it to 250 words.</li><li>Compute the monthly cost for 2,000 requests a day, each with 3,000 input and 400 output tokens, on Haiku 5.5 and on Sonnet 5.5.</li><li>Choose one model for a customer-support summary bot and justify the choice with cost and quality measures.</li></ol>
<h2>9. Official links to learn more</h2><ul>{links}</ul>'''

def vibe_body():
    rows = "".join(f'<div class="topic" style="padding:6pt 10pt"><b>{E(t)}</b><br>{E(d)}<br><span class="note">Where to learn it: {E(w)}</span></div>' for t, d, w in VIBE_GAPS)
    return f'''<h1>Vibe Coding for Non-Coders: coverage check and addendum</h1>
<p>This addendum checks the Vibe Coding module (Module 11) against what a non-coder needs, and adds what is missing. The original chapter and class slides are unchanged.</p>
<h2>What the module already covers</h2><ul><li>What vibe coding is and how to describe an app in plain English.</li><li>Lovable and other app builders, with step-by-step prompts.</li><li>Previewing and testing a generated app; debugging error messages.</li><li>Connecting a database (Supabase), login and user accounts, saving code to GitHub.</li><li>Deploying and publishing; API keys and secrets basics; privacy basics.</li><li>When a non-coder needs a developer; beginner exercises and project examples.</li></ul>
<h2>What was missing and is added here</h2>{rows}
<h2>Non-coder safety checklist before you publish</h2><ol><li>No secret keys (API keys, passwords) in any code that runs in the browser.</li><li>Real login, and a rule that each user can see only their own data.</li><li>Test the app on a phone and a laptop, and with a second account.</li><li>A backup of your project and a copy of your data.</li><li>Know who to call when something breaks in production, and what you will do then.</li></ol>
<h2>Exercise</h2><p>Build a one-page booking form in an app builder, then write three sentences that explain its cost in tokens and credits, its data and its privacy risks.</p>'''

def course_body():
    """Each course module gets the supplement sections listed for it (existing lessons are not changed)."""
    ALL = [(c, n, items) for c, n, items in A_SECTIONS + B_SECTIONS + C_SECTIONS]
    mapping = [
     ("Module 1: Advanced Excel", "Excel automation, Flash Fill, Text to Columns and Excel project briefs.", ["B1"]),
     ("Module 2: SQL", "Recursive CTEs, percentiles, cohort and churn queries, incremental loads and database platforms.", ["B2"]),
     ("Module 3: Power BI", "Microsoft Fabric, lakehouses and semantic models.", ["A10"]),
     ("Module 4: AI for Data Analysis", "AI analysis checklist and model choice (see the Tokens and Pricing Handbook for costs).", ["C6"]),
     ("Module 5: Python for Data Science", "Automation, logging, type hints and packaging.", ["B6"]),
     ("Module 6: Statistics and Machine Learning", "Recommendation systems and regression metrics (MAE, RMSE, R-squared).", ["B7"]),
     ("Module 7: Agents, MCP and APIs", "OpenAPI, OAuth 2.0, MCP security, integration examples and agent evaluation.", ["B8", "C5"]),
     ("Module 8: No-code and AI tools lab", "Tool evaluation sheet and tool directory.", ["C7"]),
     ("Module 9: Capstone, portfolio and interviews", "Eight capstone briefs, interview bank, business scenarios, STAR answers and the readiness check.", ["C1", "C2", "C3", "C4", "C9"]),
     ("Added: Data Engineering and Cloud", "ETL and ELT, pipelines, warehouses and lakehouses, medallion architecture, Airflow, dbt, Spark, Kafka, data quality, cloud services, Docker, Kubernetes and CI/CD.", ["A1", "A2", "A3", "A4", "A9", "A11", "A12"]),
     ("Added: Governance, privacy and business consulting", "Governance and privacy (GDPR, India's DPDP Act), responsible AI, business problem-solving, requirements and communication.", ["B3", "B4", "B5"]),
     ("Added: Linux, documentation, troubleshooting and roadmap", "Command line, technical documentation, production troubleshooting and the 12-month roadmap.", ["B9", "B10", "C8"]),
    ]
    body = ('<h1>AI Data Engineering course: completion addendum</h1><p>This addendum adds the topics the course was missing, mapped to each course module. The existing lessons, handbooks and PDFs are unchanged. Every entry is taken from the Course Gap Check supplements.</p>'
            '<h2>Coverage before and after</h2><table><tr><th>Prompt module</th><th>Course home</th><th>Status</th></tr>'
            + "".join(f'<tr><td>{E(r[0])}</td><td>{E(r[1])}</td><td>{E(r[2])}</td></tr>' for r in AUDIT) + '</table>')
    for title, summary, codes in mapping:
        body += f'<h2>{E(title)}</h2><p><b>What is added:</b> {E(summary)}</p>'
        for code, name, items in ALL:
            if code not in codes: continue
            body += f'<h3>{E(code)} {E(name)}</h3>'
            if items and isinstance(items[0], dict):
                body += "".join(gap_topic(t) for t in items)
            else:
                body += '<table><tr><th>Item</th><th>Answer</th></tr>' + "".join(f'<tr><td>{E(q)}</td><td>{E(a)}</td></tr>' for q, a in items) + '</table>'
    return body

def build():
    from playwright.sync_api import sync_playwright
    jobs = [
     (PM_OUT, "PM-Glossary-Handbook.pdf", cover("Product Management", "PM Glossary Handbook", "Keywords and definitions every product manager should know, each with an example.", "Read the definitions, then use the terms in your next PRD or stand-up."), glossary_body()),
     (PM_OUT, "Tokens-Pricing-and-Tokenization-Handbook.pdf", cover("AI and cost", "Tokens, Pricing and Tokenization", "What a token is, what each Claude model costs, a worked example and an app-builder example.", "Learn how tokens are counted, priced and reduced."), tokens_body()),
     (PM_OUT, "Vibe-Coding-Non-Coder-Addendum.pdf", cover("Module 11 addendum", "Vibe Coding for Non-Coders: addendum", "The coverage check of Module 11, with the missing topics and a safety checklist.", "Read after Module 11."), vibe_body()),
     (COURSE_OUT, "AI-Data-Engineering-Course-Completion-Addendum.pdf", cover("Course addendum", "AI Data Engineering: completion addendum", "The gap-check topics added to each course module, with the sources used.", "Existing lessons stay as they are; this addendum adds to them."), course_body()),
    ]
    os.makedirs(PM_OUT, exist_ok=True); os.makedirs(COURSE_OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"]); pg = b.new_page()
        for out, fn, cov, body in jobs:
            pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><title>{E(fn)}</title><style>{CSS}</style></head><body>{cov}{body}</body></html>', wait_until="load")
            pg.pdf(path=os.path.join(out, fn), format="A4", print_background=True, display_header_footer=True, header_template="<span></span>", footer_template=FOOT, margin={"top":"16mm","bottom":"18mm","left":"15mm","right":"15mm"})
            print("built", os.path.join(out, fn))
        b.close()

if __name__ == "__main__":
    build()
