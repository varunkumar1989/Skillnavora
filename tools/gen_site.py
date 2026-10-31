import re
#!/usr/bin/env python3
"""Generate the SkillNavora LMS site into /home/user/skillnavora."""
import os, re, html, shutil, json

OUT = "/home/user/skillnavora"
DOMAIN = "https://www.skillnavora.in"
E = html.escape
SB = ('<script src="{r}assets/vendor/supabase-2.117.3.js"></script>'
      '<script src="{r}assets/auth.js"></script>')

PROGRAMS = [("ai-pm", "program/ai-product-management.html", "AI-First Product Management", "Become a confident, AI-first PM",
             '<path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/>'),
            ("ai-de", "program/ai-data-engineering.html", "AI-First Data Engineer", "Build data pipelines and AI data platforms",
             '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>'),
            ("genai-launchpad", "program/genai-launchpad.html", "GenAI Launchpad", "Practical GenAI for every professional",
             '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>')]
OTHER_PROGRAMS = [("guides/sfmc.html", "SFMC training", "Salesforce Marketing Cloud: Email Studio to Journey Builder", '<path d="M17.5 19a4.5 4.5 0 1 0-1.4-8.8A6 6 0 0 0 4.5 13 3.5 3.5 0 0 0 6 19z"/>'),
           ("guides/digital-marketing.html", "Digital marketing", "SEO, ads, social, email and analytics, end to end", '<path d="M3 11l18-8-8 18-2-8z"/>'),
           ("guides/content-creation.html", "Content creation", "Strategy, writing, video, design and AI for creators", '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
           ("guides/fde.html", "Forward Deployed Engineer", "The FDE role: customers, AI deployment and integrations", '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>'),
           ("guides/public-speaking.html", "Public speaking", "Speak with confidence: talks, meetings, interviews and video", '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>')]
ABOUT = [("about.html", "About SkillNavora", "Our story, mission and team", '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>'),
         ("about.html#team", "SkillNavora team", "Meet our founder and mentors", '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'),
         ("about.html#why-us", "Why us", "What makes SkillNavora different", '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21.2l8.8-8.8a5.5 5.5 0 0 0 0-7.8z"/>'),
         ("reviews.html", "Reviews", "What learners say", '<path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"/>'),
         ("blogs.html", "Blog", "Guides, case studies and career advice", '<path d="M4 4h16v16H4z"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
         ("contact.html", "Contact us", "Talk to our team", '<path d="M4 4h16v16H4z"/><path d="M22 6l-10 7L2 6"/>')]
UPSKILL = [("", "Practice & test yourself", "", ""),
           ("tests.html", "Practice tests", "W3Schools-style tests with hints and solutions", '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'),
           ("questions.html", "Top 100 questions", "Interview questions with answers for PM, data and GenAI", '<circle cx="12" cy="12" r="10"/><path d="M12 16v.01M12 13a2 2 0 1 0-2-2"/>'),
           ("quiz.html", "Quiz zone", "Test yourself with quick quizzes", '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/>'),
           ("challenges.html", "Challenges", "Solve real product and AI problems", '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/>'),
           ("practice.html", "Practice with AI", "Mock interview questions with AI feedback", '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.7A8.5 8.5 0 1 1 21 11.5z"/>'),
           ("events.html", "Events", "Free live sessions, workshops and masterclasses", '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
           ("", "Resources & AI tools", "", ""),
           ("resources.html", "Resources & AI tools", "All handbooks, PDFs, AI tools and useful links in four tabs", '<path d="M3 7h18M3 12h18M3 17h18"/><circle cx="7" cy="7" r="1"/><circle cx="7" cy="12" r="1"/><circle cx="7" cy="17" r="1"/>'),
           ("tools.html", "Tool tutorials", "Every tool in our programs: free tutorial, official site and our lesson", '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>'),
           ("handbooks/index.html", "SkillNavora Handbooks", "Data Science, Tableau, GenAI, DSA and PM handbooks with every PDF", '<path d="M2 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H2z"/><path d="M22 4h-7a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h8z"/>'),
           ("resources.html#pm", "Resources for PM", "Handbook, templates, tools and interview practice", '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>'),
           ("resources.html#data", "Resources for Data Engineers", "Data Science & AI handbook, DSA, practice and tools", '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>'),
           ("resources.html#genai", "Resources for GenAI", "GenAI handbook, AI tools and free courses", '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>'),
           ("resources.html#more", "Other resources & links", "Communities, YouTube, certifications and datasets", '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>')]
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M6 9l6 6 6-6"/></svg>'
SVG = lambda p, w=2: f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'

G = '<svg width="20" height="20" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5a5.6 5.6 0 0 1-2.4 3.6v3h3.9c2.2-2.1 3.5-5.1 3.5-8.8z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.3v3.1A12 12 0 0 0 12 24z"/><path fill="#FBBC05" d="M5.3 14.3a7.2 7.2 0 0 1 0-4.6V6.6H1.3a12 12 0 0 0 0 10.8z"/><path fill="#EA4335" d="M12 4.8c1.8 0 3.3.6 4.6 1.8l3.4-3.4A12 12 0 0 0 1.3 6.6l4 3.1c.9-2.8 3.6-4.9 6.7-4.9z"/></svg>'
urls = []
import hashlib
VER = {f: hashlib.md5(open(os.path.join(OUT, "assets", f), "rb").read()).hexdigest()[:8] for f in os.listdir(os.path.join(OUT, "assets")) if f.endswith((".css", ".js", ".svg"))}


TOPBAR_HTML = '''<div class="topbar" id="topbar" hidden><div class="wrap"><span class="dot"></span><b></b><a class="cta" href="#">Apply now →</a><span class="tag"></span><button class="x" type="button" aria-label="Close announcement">×</button></div></div>
'''
ART = '''<svg viewBox="0 0 200 120" aria-hidden="true"><circle cx="40" cy="30" r="18" fill="#fff" stroke="#e1e6f0"/><circle cx="40" cy="25" r="6" fill="#55607a"/><path d="M29 41a11 11 0 0 1 22 0" fill="#55607a"/><circle cx="53" cy="42" r="5" fill="#22c55e" stroke="#fff" stroke-width="2"/>
<rect x="55" y="38" width="88" height="48" rx="14" fill="#0d1630"/><path d="M70 86l-4 16 18-16z" fill="#0d1630"/><circle cx="84" cy="62" r="5" fill="#8a96b5"/><circle cx="99" cy="62" r="5" fill="#8a96b5"/><circle cx="114" cy="62" r="5" fill="#8a96b5"/>
<rect x="120" y="62" width="76" height="42" rx="12" fill="#fff" stroke="#e1e6f0"/><rect x="132" y="75" width="48" height="5" rx="2.5" fill="#cdd5e6"/><rect x="132" y="87" width="34" height="5" rx="2.5" fill="#cdd5e6"/>
<path d="M165 26l2 6 6 2-6 2-2 6-2-6-6-2 6-2z" fill="#ff8a3d"/><path d="M22 74l1.5 4 4 1.5-4 1.5-1.5 4-1.5-4-4-1.5 4-1.5z" fill="#ff8a3d" opacity=".7"/></svg>'''
MODALS_HTML = f'''<div class="modal" id="m-counsel" role="dialog" aria-modal="true" aria-labelledby="mc-h"><div class="mbox wide">
  <div class="mside">
    <h2>Have questions about the course unanswered?</h2>
    <div class="kicker" style="color:#cfe0ff">Our recommendation</div>
    <p class="mside-sub">Talk to the founder</p>
    <div class="mperson"><div class="ring"><img src="{{r}}assets/varun.jpg" alt="Varun Kumar" width="150" height="150"></div>
      <div class="pcard"><div class="pt">Free 1:1 · 15 minutes · No sales pitch</div><div class="pb"><b>Varun Kumar</b><span>Founder, SkillNavora · Product Manager</span></div></div></div>
  </div>
  <div class="mform">
    <div class="mhead"><h2 id="mc-h">Talk to a counsellor</h2><button class="mclose" type="button" data-close aria-label="Close">×</button></div>
    <div class="mprog"><span id="mc-bar"></span></div>
    <form id="f-counsel" novalidate>
      <div class="mstep" data-step="1">
        <fieldset><legend><span class="req">Select your highest qualification</span></legend><div class="radios">
          {''.join(f'<label><input type="radio" name="qual" value="{q}"> {q}</label>' for q in ["12th", "Diploma", "Undergraduate", "Postgraduate"])}</div></fieldset>
        <fieldset><legend><span class="req">Select your graduation year</span></legend><div class="radios">
          {''.join(f'<label><input type="radio" name="grad" value="{q}"> {q}</label>' for q in ["Before 2015", "2015 – 2020", "2021 – 2025", "2026 or later", "Haven't joined college yet"])}</div></fieldset>
      </div>
      <div class="mstep" data-step="2" hidden>
        <fieldset><legend><span class="req">Your work experience</span></legend><div class="radios">
          {''.join(f'<label><input type="radio" name="exp" value="{q}"> {q}</label>' for q in ["Student / Fresher", "0 – 2 years", "2 – 5 years", "5 – 10 years", "10+ years"])}</div></fieldset>
        <fieldset><legend><span class="req">Which program interests you?</span></legend><div class="radios" id="mc-courses"></div></fieldset>
      </div>
      <div class="mstep" data-step="3" hidden>
        <label><span class="req">Name</span><input name="name" maxlength="80" autocomplete="name" placeholder="Enter your name"></label>
        <label><span class="req">Phone number</span><span class="phone"><select name="cc" aria-label="Country code"><option value="+91">🇮🇳 +91</option><option value="+971">🇦🇪 +971</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option></select><input name="phone" inputmode="tel" maxlength="15" autocomplete="tel-national" placeholder="98765 43210"></span></label>
        <label>Email <span class="meta">(optional)</span><input name="email" type="email" maxlength="200" autocomplete="email" placeholder="you@gmail.com"></label>
        <label>Best time to call<select name="time"><option>Morning (9–12)</option><option>Afternoon (12–5)</option><option selected>Evening (5–9)</option><option>Weekend</option></select></label>
      </div>
      <p class="notice error" id="mc-err" hidden role="alert"></p>
      <div class="mfoot"><button class="btn btn-line" type="button" id="mc-back" hidden>← Back</button><button class="btn btn-primary" type="submit" id="mc-next">Next →</button></div>
      <a class="meta" id="counsel-book" href="#" target="_blank" rel="noopener" hidden style="display:block;text-align:center;margin-top:10px">Or pick a time on our calendar →</a>
    </form>
    <div id="counsel-done" class="done-box" hidden><div class="big">🎉</div><h3>You're booked in!</h3><p class="meta">We'll call you at your preferred time. You can also message us on WhatsApp any time.</p></div>
  </div></div></div>
<div class="modal" id="m-unsure" role="dialog" aria-modal="true" aria-labelledby="mu-h"><div class="mbox">
  <button class="mclose" type="button" data-close aria-label="Close">×</button>
  <div class="art">{ART}</div>
  <div class="in"><h2 id="mu-h">Not sure if this is for you?</h2><div class="rule"></div>
    <p>Find out by connecting 1:1 with our team and ask any questions you have.</p>
    <button class="btn btn-dark" type="button" id="unsure-call">Book a free 1:1 call →</button>
    <a class="btn btn-wa" id="unsure-wa" href="#" target="_blank" rel="noopener">{WA} Ask on WhatsApp</a>
    <div class="mnote"><i>✓</i>15 minutes · No sales pitch · Free</div>
    <button class="mskip" type="button" data-close>I'm just browsing</button>
  </div></div></div>
<a class="refab" href="{{r}}refer.html" aria-label="Refer and earn" title="Refer &amp; earn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12v10H4V12"/><path d="M2 7h20v5H2zM12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg><span>Refer &amp; earn</span></a>
<button class="chat-fab" id="chat-fab" type="button" hidden aria-label="Ask SkillNavora AI"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/></svg><span>Ask AI</span></button>
<div class="chat" id="chat" role="dialog" aria-label="SkillNavora AI assistant">
  <div class="chat-h"><img src="{{r}}assets/logo-s.svg" alt="" width="32" height="32"><span><b>SkillNavora assistant</b><small>Answers about programs, fees and careers</small></span><button type="button" id="chat-x" aria-label="Close chat">×</button></div>
  <div class="chat-b" id="chat-b" aria-live="polite"></div>
  <form class="chat-f" id="chat-f"><textarea id="chat-in" rows="1" maxlength="1500" placeholder="Ask a question…" aria-label="Your question"></textarea><button type="submit" aria-label="Send"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg></button></form>
  <div class="chat-n">AI answers can be wrong. Confirm fees and dates with a counsellor.</div>
</div>'''


import aipages, academy

def page(path, title, desc, body, active=None, scripts="", noindex=False, attrs="", sticky=False, wa=True, footer=True, app=False):
    r = "../" * path.count("/")
    canon = DOMAIN + "/" + ("" if path == "index.html" else path.replace(".html", ""))
    cur = lambda h: ' aria-current="page"' if h.split('#')[0] == active else ""
    prog_menu = "".join(f'<a href="{r}{p}"{cur(p)}><span class="dd-ico">{SVG(ic)}</span><span><b data-course-name="{cid}">{E(n)}</b><small>{E(s)}</small></span></a>' for cid, p, n, s, ic in PROGRAMS)
    RARR = '<svg class="dd-arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg>'
    item = lambda p, n, sm, ic: f'<a href="{r}{p}"{cur(p)}><span class="dd-ico">{SVG(ic)}</span><span><b>{E(n)}</b><small>{E(sm)}</small></span></a>'
    sub = lambda n, sm, ic, items: (f'<div class="dd-sub"><button type="button" class="dd-subt" aria-expanded="false"><span class="dd-ico">{SVG(ic)}</span><span><b>{E(n)}</b><small>{E(sm)}</small></span>{RARR}</button>'
                                    f'<div class="dd-subm">{"".join(item(*x) for x in items)}</div></div>')
    other_menu = "".join(f'<a href="{r}{p}"{cur(p)}><span class="dd-ico">{SVG(ic)}</span><span><b>{E(n)}</b><small>{E(sm)}</small></span></a>' for p, n, sm, ic in OTHER_PROGRAMS)
    about_menu = "".join(f'<a href="{r}{p}"{cur(p)}><span class="dd-ico">{SVG(ic)}</span><span><b>{E(n)}</b><small>{E(sm)}</small></span></a>' for p, n, sm, ic in ABOUT)
    U = {p: (p, n, sm, ic) for p, n, sm, ic in UPSKILL if p}
    Q = lambda h, n, sm: ("questions.html#" + h, n, sm, U["questions.html"][3])
    up_menu = (sub("Resources & AI tools", "Handbooks, PDFs, tools and links by course", U["resources.html"][3],
                   [U[k] for k in ("resources.html#pm", "resources.html#data", "resources.html#genai")] + [("resources.html#other", "Resources for Other programs", "SFMC, digital marketing, content, FDE, public speaking", '<path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/>')] + [("resources.html#learn", "Learning sites by program", "140+ tutorials: SQL, PM, GenAI, no-code, coding", '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>')] + [("ai-builder-tools.html", "AI builder tools: how-to", "Claude, ChatGPT/Codex, Gemini, Lovable: build sites & connect tools", '<path d="M12 2l3 7h7l-5.5 4 2 7-6.5-4.5L5.5 20l2-7L2 9h7z"/>')] + [U[k] for k in ("tools.html", "handbooks/index.html", "resources.html#more")])
               + sub("Practice & interview prep", "Tests, top 100 questions, quizzes and mock interviews", U["tests.html"][3],
                     [("lab.html", "Practice Lab: run code", "SQL, Excel, Python, Power BI, PM and GenAI challenges", U["tests.html"][3]), U["tests.html"], Q("pm", "Top 100 questions: PM", "AI product management interview questions"), Q("data", "Top 100 questions: Data", "Data science, SQL, Excel, Power BI, ML"),
                      Q("genai", "Top 100 questions: GenAI", "GenAI, agents, MCP and AI tools"), U["quiz.html"], U["challenges.html"], U["practice.html"]])
               + item(*U["events.html"]))
    on = lambda group: " on" if active in group else ""
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>/* One address for everyone: logins are saved per address, so skillnavora.in and skillnavora.pages.dev move to www.skillnavora.in */if(/^(skillnavora\.in|skillnavora\.pages\.dev)$/.test(location.hostname))location.replace("https://www.skillnavora.in"+location.pathname+location.search+location.hash)</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">'}
<meta property="og:type" content="website"><meta property="og:site_name" content="SkillNavora">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{DOMAIN}/assets/og.png">
<meta name="theme-color" content="#050c22">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="icon" href="{r}assets/logo-s.svg" type="image/svg+xml"><link rel="icon" href="{r}assets/favicon-64.png" type="image/png" sizes="64x64"><link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{r}assets/site.css">
</head>
<body data-root="{r}"{attrs}{' data-app' if app else ''}>
{TOPBAR_HTML if not app and not path.startswith("program/") else ""}<header class="top"><div class="wrap">
  <a class="brand" href="{r}index.html" aria-label="SkillNavora home"><img src="{r}assets/logo-s.svg" alt="" width="36" height="36"><span><i class="c">S</i>kill<em><i class="c">N</i>avora</em></span></a>
  <nav class="nav" id="nav" aria-label="Main">
    <div class="dd{on([p for _, p, *_ in PROGRAMS] + ['programs.html', 'business.html'])}"><button type="button" aria-expanded="false">Programs {CHEV}</button><div class="dd-menu">{prog_menu}{sub("Other programs", "SFMC, digital marketing, FDE, public speaking, content", '<path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/>', OTHER_PROGRAMS + [("programs.html", "All programs", "Compare programs, fees and FAQs", '<path d="M4 6h16M4 12h16M4 18h10"/>')])}<a href="{r}business.html"{cur('business.html')}><span class="dd-ico">{SVG('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>')}</span><span><b>For business</b><small>AI training for teams and colleges</small></span></a></div></div>
    <div class="dd{on([p.split('#')[0] for p, *_ in UPSKILL if p])}"><button type="button" aria-expanded="false">Upskill for free {CHEV}</button><div class="dd-menu">{up_menu}</div></div>
    <div class="dd{on([p for p, *_ in aipages.AI_NAV if p != 'practice.html'])}"><button type="button" aria-expanded="false">AI Studio <span class="nav-new">Free</span> {CHEV}</button><div class="dd-menu">{"".join(item(*x) for x in aipages.AI_NAV)}</div></div>
    <div class="dd{on(['jobs.html', 'refer.html', 'hire.html'])}"><button type="button" aria-expanded="false">Job board {CHEV}</button><div class="dd-menu">
      <a href="{r}jobs.html#portals-box"><span class="dd-ico">{SVG('<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/>')}</span><span><b>Job portals</b><small>LinkedIn, Naukri, Wellfound and more</small></span></a>
      <a href="{r}jobs.html"{cur('jobs.html')}><span class="dd-ico">{SVG('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>')}</span><span><b>Job board</b><small>Product, AI and data engineering openings</small></span></a>
      <a href="{r}refer.html"{cur('refer.html')}><span class="dd-ico">{SVG('<path d="M20 12v10H4V12"/><path d="M2 7h20v5H2zM12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>')}</span><span><b>Refer &amp; earn</b><small>Refer learners or candidates, earn rewards</small></span></a>
      <a href="{r}hire.html"{cur('hire.html')}><span class="dd-ico">{SVG('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>')}</span><span><b>Hire from us</b><small>Is your company hiring? Get in touch</small></span></a></div></div>
    <a href="#" data-community hidden>Community</a>
    <div class="dd{on(['careers.html', 'mentor.html'])}"><button type="button" aria-expanded="false">Careers {CHEV}</button><div class="dd-menu"><a href="{r}careers.html"{cur('careers.html')}><span class="dd-ico">{SVG('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>')}</span><span><b>Join our team</b><small>Open roles at SkillNavora</small></span></a><a href="{r}mentor.html"{cur('mentor.html')}><span class="dd-ico">{SVG('<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>')}</span><span><b>Become a mentor</b><small>Guide learners, run sessions and mock interviews</small></span></a></div></div>
    <div class="dd{on(['about.html', 'reviews.html', 'blogs.html', 'contact.html'] + (['blogs.html'] if path.startswith('blog/') else []))}"><button type="button" aria-expanded="false">About Us {CHEV}</button><div class="dd-menu">{about_menu}</div></div>
  </nav>
  <div class="tools">
    <button class="icon-btn theme" type="button" aria-label="Switch light or dark mode">{SVG('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>').replace('<svg', '<svg class="sun"')}{SVG('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>').replace('<svg', '<svg class="moon"')}</button>
    <div class="dd login-dd"><button type="button" class="btn-login" id="nav-login" aria-expanded="false"><span>Log in</span> {CHEV}</button><div class="dd-menu">
      <a href="{r}login.html" id="nav-student"><span class="dd-ico">{SVG('<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>')}</span><span><b>Student login</b><small>Your LMS, courses, handbook and resources</small></span></a>
      <a href="{r}login.html?role=admin&amp;next=admin.html"><span class="dd-ico">{SVG('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>')}</span><span><b>Admin login</b><small>For the SkillNavora team</small></span></a></div></div>
    <button class="icon-btn burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{SVG('<path d="M3 6h18M3 12h18M3 18h18"/>')}</button>
  </div>
</div></header>
"""
    foot = f"""
<footer><div class="wrap">
  <div class="cols">
    <div><a class="brand" href="{r}index.html"><img src="{r}assets/logo-s.svg" alt="" width="32" height="32"><span><i class="c">S</i>kill<em><i class="c">N</i>avora</em></span></a>
      <p>AI-first programs in product management, data engineering and generative AI, with live classes, an LMS and career support.</p>
      <div class="follow"><h4>Follow us</h4><div id="social" class="soc"></div></div></div>
    <div><h4>Programs</h4><ul>{''.join(f'<li><a href="{r}{p}" data-course-name="{cid}">{E(n)}</a></li>' for cid, p, n, *_ in PROGRAMS)}<li><a href="{r}programs.html">All programs and FAQs</a></li></ul></div>
    <div><h4>Upskill for free</h4><ul>{''.join(f'<li><a href="{r}{p}">{E(n)}</a></li>' for p, n, *_ in UPSKILL if p)}<li><a href="{r}blogs.html">Blogs</a></li><li><a href="{r}refer.html">Refer &amp; earn</a></li><li><a href="{r}hire.html">Hire from us</a></li><li><a href="{r}jobs.html">Job board</a></li><li><a href="{r}business.html">For business</a></li></ul></div>
    <div><h4>Contact us</h4><ul id="fcontact"></ul><ul style="margin-top:14px"><li><a href="{r}mentor.html">Become a mentor</a></li><li><a href="{r}careers.html">Careers</a></li><li><a href="{r}login.html">Member login</a></li><li><a href="{r}privacy.html">Privacy policy</a></li><li><a href="{r}terms.html">Terms and conditions</a></li><li><a href="{r}refund.html">Cancellation and refund policy</a></li></ul></div>
  </div>
  <div class="base"><span>© <span id="yr"></span> SkillNavora. All rights reserved.</span><span class="madeby">Made with care in India</span></div>
</div></footer>""" if footer else ""
    sticky_html = """
<div class="sticky" id="sticky" aria-label="Enrol"><div class="wrap">
  <span class="cohort"><i></i><span>Enrolling</span></span>
  <div class="info"><b></b><span></span></div>
  <div class="acts"><a class="btn btn-ghost btn-sm" data-st-counsel href="#counselling">Talk to counsellor</a><a class="btn btn-primary btn-sm" data-st-enroll href="#">Enroll now →</a></div>
</div></div>""" if sticky else ""
    tail = f"""{foot}
{sticky_html}
{'<a class="callfab" id="callfab" hidden aria-label="Call us" title="Call us"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></a>' if wa else ''}{f'<a class="wa" id="wa" hidden target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><span>{WA}</span><em class="t">Chat on WhatsApp</em></a>' if wa else ''}
{MODALS_HTML.replace('{r}', r) if not app else ''}
<script src="{r}assets/config.js"></script>
<script src="{r}assets/site.js"></script>{scripts.replace('{r}', r)}{f'<script src="{r}assets/gate.js"></script>' if app else f'<script src="{r}assets/engage.js"></script><script src="{r}assets/gate.js"></script>'}
</body>
</html>
"""
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    doc = head + "<main>\n" + body.replace("{R}", r) + "\n</main>" + tail
    doc = re.sub(r'((?:href|src)="(?:\.\./)*assets/([a-z0-9-]+\.(?:css|js|svg)))"', lambda m: f'{m.group(1)}?v={VER[m.group(2)]}"', doc)
    open(full, "w").write(doc)
    if not noindex and path != "404.html":
        urls.append(canon)


def sec(kicker, h, sub="", inner="", cls="", center=False, sid=""):
    return f"""<section{f' id="{sid}"' if sid else ''}{f' class="{cls}"' if cls else ''}><div class="wrap{' center' if center else ''}">
  <div class="kicker">{kicker}</div><h2 class="sec-h">{h}</h2>{f'<p class="sub">{sub}</p>' if sub else ''}
  {inner}
</div></section>"""


def band(h, p, btns):
    return f'<section class="tight"><div class="wrap"><div class="band"><div><h2>{h}</h2><p>{p}</p></div><div class="acts">{btns}</div></div></div></section>'


FAQ_BLOCK = f"""<div class="faq-tools"><div class="search">{SVG('<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>')}<input id="faq-q" type="search" placeholder="Search for a question…" aria-label="Search questions"></div><div class="fchips" id="faq-chips"></div></div><div class="faq" id="faq"></div>
<p class="center meta" style="margin-top:28px"><i>Still have questions? We're happy to help.</i></p>
<div class="center" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn btn-primary" href="{{R}}programs.html">Apply now</a><a class="btn btn-line" data-counsel href="#">Join a counselling session</a></div>"""

STEPS = """<div class="steps">
  <div class="step"><h3>Talk to a counsellor</h3><p>A free call to understand your background and pick the right program.</p></div>
  <div class="step"><h3>Learn live</h3><p>Live classes with instructors, recordings in your LMS and weekly assignments.</p></div>
  <div class="step"><h3>Build your portfolio</h3><p>Projects, a capstone and feedback on every submission.</p></div>
  <div class="step"><h3>Get job-ready</h3><p>Resume reviews, mock interviews and referrals through our network.</p></div>
</div>"""

TESTI = """<section id="testimonials" class="tint" hidden><div class="wrap center"><div class="kicker">Reviews</div><h2 class="sec-h">What our learners say</h2><div class="grid g3" id="testimonials-list" style="text-align:left;margin-top:30px"></div></div></section>"""

# ================================================================ SHARED SECTIONS (v3)
AUD = lambda cls="": sec("Who is this for", "Built for where you are today", "Whether you're starting out, working full-time, switching careers or aiming for a bigger role and salary.", '<div class="grid g4 aud" id="audience"></div>', cls=cls, center=True)
MOAT_S = lambda cls="", course="PM course": sec("Our moat", "What makes SkillNavora different", f"The things you won't find together in a typical {course}.", '<div class="moat" id="moat"></div>', cls=cls)
CMP_S = lambda cls="": sec("What's included", "Everything you get with SkillNavora", "", '<div class="cmp table-wrap" id="compare"></div>', cls=cls)
TOOLS_S = lambda h="Every tool a modern PM needs", cls="", sub="Hands-on with the tools product teams use every day, from Jira and Figma to Claude and Claude Code.": sec("Tools you'll master", h, sub, '<div class="tgroups" id="toolgroups"></div>', cls=cls)
JA_S = lambda cls="": sec("Get job-ready", "Job assistance program and intensive interview preparation", "Capstone, mock tests and interview preparation, so you finish the program ready to apply.", '''<div class="ja">
  <div class="card dark"><h3>Job assistance program</h3><ul class="checks" id="ja-program" style="margin-top:14px"></ul></div>
  <div class="card"><h3>Intensive interview preparation</h3><ul class="checks" id="ja-interview" style="margin-top:14px"></ul></div></div>''', cls=cls)
MENTORS_S = '<section id="mentors" hidden><div class="wrap center"><div class="kicker">Mentors</div><h2 class="sec-h">Learn from leaders at top companies</h2><p class="sub">Mentors and guest speakers who build products every day.</p><div class="mentors" id="mentors-list" style="text-align:left"></div></div></section>'
REVIEWS_S = '<section id="home-reviews" class="tint" hidden><div class="wrap"><div class="center"><div class="kicker">Testimonials and reviews</div><h2 class="sec-h">Careers that changed, <span class="g">in their own words.</span></h2></div><div class="reviews" id="home-reviews-list" style="margin-top:30px"></div><p class="center"><a class="btn btn-line btn-sm" href="{R}reviews.html">All reviews →</a></p></div></section>'

BIG_LOGO = '<div class="biglogo"><img src="{r}assets/logo-s.svg" alt="SkillNavora logo" width="240" height="240"><div class="brand"><span><i class="c">S</i>kill<em><i class="c">N</i>avora</em></span></div></div>'
COMPASS_SIDE = '''  <div class="hero-art side" aria-hidden="true">''' + BIG_LOGO.replace("{r}", "") + '''</div>
'''
FREE_TRACKS = [("AI for Product Managers", "LLMs, RAG, vibe coding and agentic AI, explained for PMs.", "3 modules", "AI Product"),
               ("Claude for daily PM work", "PRDs, research, analysis and stakeholder updates with Claude.", "1 module", "AI Tools"),
               ("Claude Code: basic to advanced", "Build and ship real apps and websites with an AI coding agent.", "1 module", "Build with AI"),
               ("Lovable and AI app builders", "Turn an idea into a working prototype without writing code.", "2 modules", "No-code"),
               ("Automation with Zapier, Make and n8n", "Automate repetitive work and connect your tools with AI.", "1 module", "Automation"),
               ("Chatbots and voice agents", "Build WhatsApp, Slack, web chatbots and voice agents for businesses.", "2 modules", "AI Agents")]
FREE_COURSES_S = sec("Free AI courses", "Start learning AI for free", "Self-paced courses from the SkillNavora PM Master Handbook by Varun Kumar. Free for everyone, no login needed.",
  '<div class="grid g3">' + "".join(f'<a class="card fcourse" href="resources.html"><span class="ftag">{E(t)}</span><h3>{E(n)}</h3><p>{E(d)}</p><div class="fmeta"><span>Free</span><span>{E(m)}</span><span>Self-paced</span></div><span class="go">Start free →</span></a>' for n, d, m, t in FREE_TRACKS) + '</div>', sid="free-courses")
WORKSHOPS = [("AI tools every PM should know", "A live tour of the AI tools product teams use, with real examples.", "90 min"),
             ("Build a website with Claude Code", "Go from idea to a live website in one session, step by step.", "2 hours"),
             ("Crack PM interviews with AI", "Practise product sense and metrics questions with AI feedback.", "90 min")]
WORKSHOPS_S = sec("Free live workshops", "Learn live, for free", "Short, hands-on live sessions on the skills that matter right now. Join one before you decide on a program.",
  '<div class="grid g3">' + "".join(f'<div class="card wshop"><span class="live">● Live online</span><h3>{E(n)}</h3><p>{E(d)}</p><div class="fmeta"><span>Free</span><span>{E(dur)}</span></div><div class="wacts"><a class="btn btn-primary btn-sm" href="events.html">See dates</a><a class="btn btn-line btn-sm" data-wa="Hi SkillNavora, please notify me about the free workshop: {E(n)}" href="#">Notify me</a></div></div>' for n, d, dur in WORKSHOPS) + '</div>', cls="tint", sid="workshops")

OFFERS_S = """<section id="offers" class="offers-s"><div class="wrap"><div class="offers">
  <div class="disc"><div class="kicker">Scholarships</div><h2 class="sec-h">Scholarships <span class="g">up to 100%</span></h2><p class="meta" style="margin:-4px 0 0">Talk to a counsellor to check what you're eligible for.</p>
    <div class="dgrid2" id="offer-list"></div><p class="meta" id="offer-note" style="margin:14px 0 0"></p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px"><a class="btn btn-primary btn-sm" data-counsel href="#counselling">Check my eligibility →</a><a class="btn btn-line btn-sm" data-wa="Hi SkillNavora, I'd like to know about the scholarship (up to 100%)." href="#">Ask on WhatsApp</a></div></div>
</div></div></section>"""
COMPANIES = ["Google", "Microsoft", "Amazon", "Flipkart", "Swiggy", "Zomato", "Razorpay", "PhonePe", "Paytm", "CRED", "Meesho", "Zepto", "Atlassian", "Adobe", "Salesforce", "Uber", "Ola", "Myntra", "Nykaa", "Freshworks", "Zoho", "PayPal", "Walmart", "Intuit"]
def _row(names): return "".join(f'<span>{E(n)}</span>' for n in names)
MARQUEE_S = f"""<section class="logos-s" aria-label="Companies"><div class="wrap"><h2 class="sec-h center" style="font-size:clamp(22px,2.6vw,30px)">Build the skills <span class="g">top companies</span> hire for</h2>
  <div class="marquee"><div class="track">{_row(COMPANIES[:12])}{_row(COMPANIES[:12])}</div></div>
  <div class="marquee rev"><div class="track">{_row(COMPANIES[12:])}{_row(COMPANIES[12:])}</div></div>
  <p class="meta center" style="margin:14px 0 0;font-size:12.5px">Companies hiring for product, data and AI roles. SkillNavora isn't affiliated with these companies.</p></div></section>"""
PS_ITEMS = [('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/>', "Resume review", "Perfect your resume with detailed feedback from mentors, so you don't miss out on getting shortlisted for your dream role."),
            ('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>', "1:1 mock interviews with mentors", "Crack interviews at top tech companies by practising with industry professionals and getting honest feedback."),
            ('<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M12 11.5l-5.5 5.5M12 11.5l5.5 5.5"/>', "Practise real-world interview questions", "Practise from our bank of real interview questions on product sense, metrics, strategy, RCA and guesstimates."),
            ('<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 13l2 2 4-4"/>', "Referrals to hiring companies", "When you're job-ready, we refer you to open roles through our network of product leaders and hiring managers.")]
PLACE_S = f"""<section class="place-s" id="placement"><div class="wrap">
  <h2 class="sec-h" style="max-width:20ch">1 Year Placement Support to Get Your Dream Job</h2>
  <p class="sub" style="margin-bottom:34px">Clear the cut-off marks in your capstone project to get access to 1 year of placement support.</p>
  <div class="pgrid">{"".join(f'<div class="pitem"><span class="pico">{SVG(ic)}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for ic, t, d in PS_ITEMS)}</div>
  <p class="meta" style="margin:26px 0 0;font-size:12.5px">Placement support helps you prepare and apply. It is not a job guarantee.</p>
</div></section>"""
REFER_S = """<section class="refer-s"><div class="wrap"><div class="refer-band">
  <div><div class="kicker">Refer &amp; earn</div><h2 class="sec-h">Know someone who should be here?</h2><p class="sub" style="margin:0">Refer a friend to a SkillNavora program, or a candidate to one of our hiring partners, and earn a reward when it works out.</p></div>
  <div class="acts"><a class="btn btn-primary" href="refer.html">Refer &amp; earn →</a><a class="btn btn-line" href="hire.html">Hiring? Get in touch</a></div></div></div></section>"""
LEARN_S = '''<section class="learn-s" aria-label="How you'll learn"><div class="wrap"><div class="learn">
  <div><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4M10 8.5v5l4-2.5z"/></svg><span><b>Live weekend classes</b><small>Learn with instructors, ask questions live</small></span></div>
  <div><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/></svg><span><b>Recordings in your LMS</b><small>Rewatch any class, any time</small></span></div>
  <div><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg><span><b>Assignments with feedback</b><small>Weekly work on 25+ real case studies</small></span></div>
  <div><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg><span><b>Quizzes and mock tests</b><small>Check what you've learnt every week</small></span></div>
  <div><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/></svg><span><b>Capstone and career support</b><small>Build a portfolio and prepare for interviews</small></span></div>
</div></div></section>'''
STATS_S = '<section class="stats-band" id="stats" hidden><div class="wrap"><div class="statgrid" id="statgrid"></div><p class="meta center" id="stats-note" style="margin:14px 0 0"></p></div></section>'
# ================================================================ HOME
up_cards = "".join(f'<a class="card tool" href="{p}"><div class="ico{" g" if i % 2 else ""}">{SVG(ic)}</div><h3>{E(n)}</h3><p>{E(s)}</p><span class="go">Start free →</span></a>' for i, (p, n, s, ic) in enumerate(x for x in UPSKILL if x[0]))
home = f"""<div class="hero split"><div class="wrap"><div>
  <a class="pill" id="announce" href="programs.html" hidden><i></i><b></b> →</a>
  <h1>Become a confident, <span class="g">job-ready</span> AI&#8209;first professional</h1>
  <p class="lead">Live, hands-on programs in product management, data engineering and generative AI. Work on 25+ real-world case studies, build your own AI product, and get job assistance until you're ready to apply.</p>
  <div class="acts"><a class="btn btn-primary" data-enroll="ai-pm" href="apply.html">Apply now →</a><a class="btn btn-ghost" data-counsel href="#counselling">Join a free counselling session</a></div>
  <div class="hl"><span>25+ real-world case studies</span><span>Capstone and mock tests</span><span>Monthly 1:1 with a CEO or Head of Product</span><span>Job assistance program</span></div>
  <div class="quick"><span>Quick links →</span><a href="#programs">Programs</a><a href="#who">Who it's for</a><a href="#why">Why us</a><a href="#tools">Tools</a><a href="#jobready">Job assistance</a><a href="#faqs">FAQs</a></div>
  </div>
  <div class="hero-form card" id="lead">
    <h3>Book a free live class and counselling session</h3>
    <button class="gbtn alt" id="lead-google" type="button" hidden>{G}Sign up with Google</button>
    <div class="or" id="lead-or" hidden>or</div>
    <form id="f-lead" class="form" novalidate>
      <label><span class="req">Name</span><input name="name" maxlength="80" autocomplete="name" placeholder="Enter your name"></label>
      <label><span class="req">Email</span><input name="email" type="email" maxlength="200" autocomplete="email" placeholder="you@gmail.com"></label>
      <label><span class="req">Phone number</span><span class="phone"><select name="cc" aria-label="Country code"><option value="+91">🇮🇳 +91</option><option value="+971">🇦🇪 +971</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option></select><input name="phone" inputmode="tel" maxlength="15" autocomplete="tel-national" placeholder="98765 43210"></span></label>
      <fieldset><legend><span class="req">Your program of interest</span></legend><div class="radios row">
        <label><input type="radio" name="course" value="ai-pm" checked> AI Product Management</label>
        <label><input type="radio" name="course" value="ai-de"> Data Engineer</label>
        <label><input type="radio" name="course" value="genai-launchpad"> GenAI Launchpad</label></div></fieldset>
      <label class="chk"><input type="checkbox" name="wa" checked> Send me updates on WhatsApp</label>
      <p class="notice error" id="lead-err" hidden role="alert"></p>
      <button class="btn btn-primary" type="submit">Book my free session →</button>
      <p class="meta center" style="margin:0;font-size:12.5px">By continuing, you agree to our <a href="terms.html">terms</a> and <a href="privacy.html">privacy policy</a>.</p>
    </form>
    <div id="lead-done" class="done-box" hidden><div class="big">🎉</div><h3>You're in!</h3><p class="meta">We'll call you soon to schedule your free live class and counselling session.</p><a class="btn btn-line btn-sm" data-wa="Hi SkillNavora, I just booked a free session." href="#">Message us on WhatsApp</a></div>
  </div>
</div></div>
{LEARN_S}
{MARQUEE_S}
{sec("Programs", "Our flagship programs", "Choose your track. Every program includes live classes, case studies, assignments with feedback, a capstone and career support.", '<div class="courses" id="courses"></div>', sid="programs")}
{OFFERS_S.replace("{R}", "")}
{sec("Your learning journey", "How you'll learn at SkillNavora", "A clear, guided path from your first counselling call to your first PM interview.", STEPS)}
{AUD("tint").replace('<section', '<section id="who"', 1)}
{MOAT_S().replace('<section', '<section id="why"', 1)}
{STATS_S}
{CMP_S("tint")}
{TOOLS_S().replace('<section', '<section id="tools"', 1)}
{PLACE_S}
{REFER_S}
{JA_S("tint").replace('<section', '<section id="jobready"', 1)}
{FREE_COURSES_S}
{WORKSHOPS_S}
{sec("Upskill for free", "Practise every day, for free", "Sharpen your skills between classes, or try SkillNavora before you enrol.", f'<div class="grid g4">{up_cards}</div>')}
{MENTORS_S}
{REVIEWS_S}
<section><div class="wrap founder">
  <img src="assets/varun.jpg" alt="Varun Kumar, founder of SkillNavora" width="200" height="200">
  <div><div class="kicker">Founder</div><h2 class="sec-h" style="margin-bottom:4px">Varun Kumar</h2><p class="meta">Product manager and founder of SkillNavora</p>
    <blockquote>“SkillNavora exists to help you learn by doing: real problems, real feedback and the AI tools teams use today.”</blockquote>
    <a class="btn btn-line btn-sm" data-wa="Hi Varun, I'd like to know more about SkillNavora." href="#">Message Varun</a></div>
</div></section>
{sec("FAQs", "Got questions? We have answers.", "Everything you need to know before joining SkillNavora.", FAQ_BLOCK, cls="tint", center=True, sid="faqs")}
{band("Not sure which program fits you?", "Book a free 1:1 counselling session. We'll look at your background and goals and suggest the right path.", '<a class="btn btn-primary" data-counsel href="#counselling">Book free counselling</a><a class="btn btn-ghost" data-wa="Hi SkillNavora!" href="#">Chat on WhatsApp</a>')}
"""
page("index.html", "SkillNavora · AI-first programs in product, data engineering and GenAI",
     "Live AI-first programs in product management, data engineering and generative AI: 25+ real-world case studies, capstone, mock tests, job assistance and monthly 1:1s with a CEO or Head of Product.", home, "index.html", sticky=True)

HB_CORE = [("01","Fundamentals","Fundamentals of Product Management"),("02","Strategy","Product Strategy and Strategic Thinking"),("03","Discovery","Problem Discovery and Market Research"),("04","Prioritization","Problem Framing and Prioritization"),("05","UX-Design","UX and Design Collaboration"),("06","Communication","Effective Communication and Stakeholder Management"),("07","Analytics","Product Analytics and Metrics"),("08","Growth","Product Launch, Growth, and Monetization"),("09","Tech-System-Design","Tech 101 and System Design for PMs"),("10","LLM-RAG","LLMs, RAGs, and AI Foundations"),("11","Vibe-Coding","Vibe Coding for Product Managers"),("12","Agentic-AI","Agentic AI and AI Systems")]
HB_AI = [("13","AI-Tools-Landscape","AI Tools Landscape and Your Starter Stack"),("14","Claude-Daily-Work","Claude for Daily PM Work"),("15","Claude-Code","Claude Code: Basic to Advanced"),("16","Lovable","Lovable: Basic to Advanced"),("17","Replit-and-App-Builders","Replit and Other AI App Builders"),("18","Figma","Figma and AI Design Tools"),("19","Notion-and-PRD-Tools","Notion, PRD Tools and AI Documentation"),("20","Automation","Automation with Zapier, Make and n8n"),("21","Business-Chatbots","AI Chatbots for Business"),("22","Voice-Agents","Voice Agents for Businesses"),("23","Learning-Paths","Learning Paths, Courses and Communities")]
HB_LIB = [("Framework-Library","Framework Library","29 frameworks with worked examples and templates"),("Case-Study-Library","Case Study Library","12 product case studies"),("Practical-Projects","Practical Projects and Portfolio","5 end-to-end portfolio projects"),("Interview-Handbook","Interview Handbook","100+ PM interview questions with model answers"),("AI-Tools-Lab","AI Tools Lab","Every AI tools class with step-by-step labs")]
HB_ART = "https://claude.ai/artifact/51eByvQUgCYBHLAYmyGzVJ"
HB_EXTRA = {"06": [("classes/week-06-effective-communication.html", "Class slides"), ("classes/week-06-effective-communication.pdf", "Slides PDF")]}
def _hb_row(n, f, t):
    if n not in HB_EXTRA: return f'<a class="hb-row" href="handbook/Module-{n}-{f}.pdf" target="_blank" rel="noopener"><span class="hb-n">{int(n)}</span><span>{t}</span><small>PDF ↗</small></a>'
    links = [(f"handbook/Module-{n}-{f}.pdf", "PDF")] + HB_EXTRA[n]
    return f'<div class="hb-row hb-multi"><span class="hb-n">{int(n)}</span><span>{t}<em>Handbook chapter + 67-slide class deck</em></span><span class="hb-links">' + "".join(f'<a href="{u}" target="_blank" rel="noopener">{l} ↗</a>' for u, l in links) + '</span></div>'
def _hb_mods(rows): return "".join(_hb_row(n, f, t) for n, f, t in rows)
HB_LIBROWS = "".join(f'<a class="hb-row" href="handbook/{f}.pdf" target="_blank" rel="noopener"><span class="hb-n">★</span><span>{t}<em>{d}</em></span><small>PDF ↗</small></a>' for f, t, d in HB_LIB)
CLASSROWS = '<a class="hb-row" href="classes/week-06-effective-communication.html" target="_blank" rel="noopener"><span class="hb-n">6</span><span>Week 6 · Effective Communication as a PM<em>67-slide class deck: frameworks, templates, case study, assignment and interview prep</em></span><small>Slides ↗</small></a><a class="hb-row" href="classes/week-06-effective-communication.pdf" target="_blank" rel="noopener"><span class="hb-n">6</span><span>Week 6 · Effective Communication as a PM<em>Same deck as a PDF to download</em></span><small>PDF ↗</small></a>'
HB_PANEL = f'''    <div class="panel" id="p-handbook" hidden>
      <div class="hb-hero"><div><div class="kicker">Free for everyone</div><h2 class="h2s" style="margin:4px 0 6px">Product Management Master Handbook</h2>
        <p class="meta" style="margin:0 0 14px">23 modules, 570 pages: the 12 Product Core modules, an 11-class AI Tools Lab, frameworks, case studies, projects and interview prep. Created by Varun Kumar.</p>
        <div class="hb-acts"><a class="btn btn-primary btn-sm" href="{HB_ART}" target="_blank" rel="noopener">Open the interactive handbook ↗</a><a class="btn btn-line btn-sm" href="handbook/Complete-PM-Master-Handbook.pdf" target="_blank" rel="noopener">Complete handbook PDF (570 pages, 22 MB) ↗</a></div></div></div>
      <h3 class="h3s hb-h">Product Core modules</h3><div class="hb-list">{_hb_mods(HB_CORE)}</div>
      <h3 class="h3s hb-h">AI Tools Lab</h3><div class="hb-list">{_hb_mods(HB_AI)}</div>
      <h3 class="h3s hb-h">Libraries</h3><div class="hb-list">{HB_LIBROWS}</div>
      <p class="meta" style="margin-top:18px">The handbook is also on the Resources &amp; AI tools page, free for every visitor.</p>
    </div>
'''



# ================================================================ ALL PROGRAMS
allp = f"""<div class="hero"><div class="wrap">
  <div class="kicker">Programs</div><h1>Pick your <span class="g">AI&#8209;first</span> career track</h1>
  <p class="lead">Three live programs with assignments, a capstone and career support. Compare them below, or talk to a counsellor for advice.</p>
  <div class="acts"><a class="btn btn-ghost" data-counsel href="#">Talk to a counsellor</a></div>
</div></div>
<section><div class="wrap"><div class="courses" id="courses"></div></div></section>
{OFFERS_S.replace("{R}", "")}
{AUD("tint")}
{MOAT_S()}
{CMP_S("tint")}
{JA_S()}
{sec("FAQs", "Got questions? We have answers.", "", FAQ_BLOCK, center=True, sid="faqs")}"""
page("programs.html", "Programs · SkillNavora", "Compare SkillNavora's AI-First Product Management, AI-First Data Engineer and GenAI Launchpad programs.", allp, "programs.html", sticky=True)

# ================================================================ PROGRAM PAGES
INSTRUCTOR_S = """<section id="instructor"><div class="wrap"><div class="kicker">Your instructor</div><h2 class="sec-h">Learn from a practising product leader</h2>
  <div class="inst card"><img src="../assets/varun.jpg" alt="Varun Kumar" width="168" height="168" loading="lazy">
    <div><h3>Varun Kumar</h3><p class="meta" style="margin:2px 0 12px">Founder and lead instructor, SkillNavora · Product manager</p>
    <p>Varun designed this program around the way product teams work today: real problems, honest feedback and the AI tools PMs use every day. He wrote the 570-page SkillNavora PM Master Handbook that every learner gets, and personally reviews capstone projects.</p>
    <div class="inst-acts"><a class="btn btn-line btn-sm" href="https://www.linkedin.com/in/" data-li target="_blank" rel="noopener">LinkedIn ↗</a><a class="btn btn-line btn-sm" href="../resources.html">Read the PM Handbook</a></div></div></div>
  <p class="meta" style="margin-top:14px">Guest mentors and speakers are announced for each cohort.</p></div></section>"""
TOOLS_SUB = {"ai-pm": "Hands-on with the tools product teams use every day, from Jira and Figma to Claude and Claude Code.",
             "ai-de": "Hands-on with the tools data engineering teams use every day, from SQL, Python and Airflow to Spark, Snowflake and AI assistants.",
             "genai-launchpad": "Hands-on with the AI tools professionals use every day, with no coding needed."}

ART = "https://claude.ai/artifact/7278116b7jCN2ny9XnmtVM"
def _hbsec(kicker, title, text, links):
    btns = "".join(f'<a class="btn {"btn-primary" if i == 0 else "btn-line"} btn-sm" href="{h}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""}>{E(t)}</a>' for i, (t, h) in enumerate(links))
    return f'<section id="handbooks"><div class="wrap"><div class="kicker">{E(kicker)}</div><h2 class="sec-h">{E(title)}</h2><p class="meta" style="max-width:70ch">{E(text)}</p><div class="acts" style="flex-wrap:wrap;gap:10px;margin-top:18px">{btns}</div></div></section>'
PROG_HB = {
    "ai-de": _hbsec("Free handbooks", "Data Science & AI and DSA handbooks",
                    "116 class-wise lessons (Excel, SQL, Power BI, Tableau, Python, DSA, statistics, machine learning, GenAI and career) with real outputs, diagrams, quizzes, practice datasets and a PDF for every lesson. Share your details once to open any PDF or file.",
                    [("Open the Data Science & AI handbook", "../data-science/index.html"), ("DSA handbook (interactive) ↗", ART + "#dsa"), ("All SkillNavora handbooks", "../handbooks/index.html"),
                     ("Complete handbook PDFs", "../data-science/index.html#downloads"), ("Resources for Data Engineers", "../resources.html#data")]),
    "genai-launchpad": _hbsec("Free handbook", "GenAI Launchpad Handbook",
                    "LLMs, prompting, APIs, embeddings, RAG, tool use, agents, MCP, evaluation, fine-tuning, GenAI for data work and a capstone app, plus the AI Tools Lab, in one 482-page PDF and interactive lessons.",
                    [("Open the GenAI Launchpad handbook", "../handbooks/index.html#genai"), ("Interactive handbook ↗", ART + "#genai"), ("GenAI lessons", "../data-science/index.html#t-genai"), ("Resources for GenAI", "../resources.html#genai")]),
}
for cid, path, name, short, _ in PROGRAMS:
    import json as _j
    _ld = _j.dumps({"@context": "https://schema.org", "@type": "Course", "name": name, "description": short,
                    "provider": {"@type": "Organization", "name": "SkillNavora", "sameAs": DOMAIN},
                    "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "instructor": {"@type": "Person", "name": "Varun Kumar"}}})
    body = f"""<script type="application/ld+json">{_ld}</script><div class="hero split prog"><div class="wrap"><div>
  <a class="pill" href="../programs.html"><i></i><b>SkillNavora program</b></a>
  <h1 id="p-name">{E(name)}</h1>
  <p class="lead" id="p-tagline"></p>
  <div class="acts"><a class="btn btn-primary" data-enroll="{cid}" href="../apply.html?program={cid}">Enroll now →</a><a class="btn btn-ghost" data-counsel="{cid}" href="#counselling">Join a counselling session</a></div>
  <p class="fine" id="p-fine"></p>
  <div class="hl" id="p-hl"></div>
  <div class="quick"><span>Quick links →</span><a href="#curriculum">Curriculum</a><a href="#tools">Tools</a><a href="#instructor">Instructor</a><a href="#jobready">Job assistance</a><a href="#fees">Fees</a><a href="#faqs">FAQs</a></div>
  </div>
  <aside class="glance" aria-label="Program at a glance"><div class="glance-cover" id="p-cover"></div>
    <ul class="glance-list" id="p-glance"></ul>
    <a class="btn btn-line btn-block" href="../brochures/{cid}.pdf" download>{SVG('<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>')}Download brochure (PDF)</a></aside>
</div></div>
{AUD()}
<section id="outcomes" class="tint"><div class="wrap"><div class="kicker">Outcomes</div><h2 class="sec-h">What you'll be able to do</h2><ul class="checks two" id="p-outcomes" style="margin-top:24px"></ul></div></section>
{PROG_HB.get(cid, '')}
{sec("Curriculum", "What you'll learn", "Each module mixes live classes, real-world case studies, hands-on assignments and feedback. Recordings and materials stay in your LMS.", '<div class="mods" id="p-curriculum"></div>', sid="curriculum")}
{academy.program_section(cid) if cid in ("ai-pm", "genai-launchpad") else ""}
{TOOLS_S("Tools you'll use", "tint", TOOLS_SUB.get(cid, TOOLS_SUB["ai-pm"])).replace('<section', '<section id="tools"', 1)}
{INSTRUCTOR_S}
{sec("Projects", "Build a portfolio recruiters notice", "", '<div class="grid g3" id="p-projects"></div>')}
{MOAT_S("tint", "PM course" if cid == "ai-pm" else "online course").replace('<section', '<section id="why"', 1)}
{CMP_S()}
{PLACE_S}
{JA_S("tint").replace('<section', '<section id="jobready"', 1)}
{MENTORS_S}
{OFFERS_S.replace("{R}", "../").replace('id="offers"', 'id="offers-p"')}
<section id="fees"><div class="wrap"><div class="kicker">Fees and schedule</div><h2 class="sec-h" id="schedule">Invest in your career</h2>
  <div class="fee" style="margin-top:28px"><div class="l"><div class="kicker" style="color:#9fbaff">Program fee</div><div class="price" id="p-price"></div><p id="p-feenote"></p>
    <p id="p-early" class="pill" style="margin-top:16px;white-space:normal" hidden></p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-primary" data-enroll="{cid}" href="../apply.html?program={cid}">Enroll now →</a><a class="btn btn-ghost" data-counsel="{cid}" href="#counselling">Talk to counsellor</a></div></div>
  <div class="r"><h3 style="font-size:19px">Schedule</h3><ul class="checks" id="p-schedule" style="gap:10px"></ul></div></div>
</div></section>
{REVIEWS_S}
{sec("FAQs", "Got questions? We have answers.", "Everything you need to know before joining.", FAQ_BLOCK, cls="tint", center=True, sid="faqs")}
{band("Ready to start?", "Apply for the next cohort, or talk to a counsellor first. It's free.", f'<a class="btn btn-primary" data-enroll="{cid}" href="../apply.html?program={cid}">Enroll now →</a><a class="btn btn-ghost" data-counsel="{cid}" href="#counselling">Talk to counsellor</a>')}
"""
    page(path, f"{name} · SkillNavora", f"{name}: {short}. Curriculum, tools, case studies, fees, job assistance and FAQs.", body, path, attrs=f' data-course="{cid}"', sticky=True)

# ================================================================ UPSKILL PAGES
def uhero(k, h, lead):
    return f'<div class="hero"><div class="wrap"><div class="kicker">{k}</div><h1>{h}</h1><p class="lead">{lead}</p></div></div>'

UP_JS = '<script src="{r}assets/content.js"></script>'
quiz = uhero("Upskill for free · Quiz zone", 'Quiz <span class="g">zone</span>', "Quick quizzes on product management, metrics and AI. See explanations for every answer, and log in to save your scores and earn badges.") + """
<section><div class="wrap"><div id="quiz-intro"><h2 class="sec-h" style="font-size:28px">Pick a quiz</h2><p class="sub">Each quiz takes about 6 minutes.</p></div>
<div class="grid g4 qlist" id="quiz-list"></div><div id="quiz-play" hidden></div></div></section>"""
page("quiz.html", "Quiz zone · SkillNavora", "Free quizzes on product management, metrics, AI and prompting, with explanations.", quiz, "quiz.html",
     UP_JS + SB + '<script src="{r}assets/upskill.js"></script>', attrs=' data-page="quiz"')

chal = uhero("Upskill for free · Challenges", 'Real-world <span class="g">challenges</span>', "Solve problems like the ones PMs and engineers face at work. Submit your solution in the LMS to get feedback and earn the Challenger badge.") + """
<section><div class="wrap"><div class="filters" id="chal-filters"></div><div class="grid g3" id="chal-list"></div></div></section>"""
page("challenges.html", "Challenges · SkillNavora", "Free product, AI and engineering challenges with clear briefs. Submit solutions for feedback.", chal, "challenges.html",
     UP_JS + '<script src="{r}assets/upskill.js"></script>', attrs=' data-page="challenges"')

prac = uhero("AI Studio · AI mock interview", 'Practice with <span class="g">AI</span>', "Get a real interview question, answer it against the clock, then get a score, a model answer and follow-up questions from our AI coach, right here.") + aipages.CSS + f"""
<section><div class="wrap practice">
  <div class="card form">
    <label>I'm preparing for<select id="pr-role"></select></label>
    <label>Question type<select id="pr-type"></select></label>
    <label>Time limit<select id="pr-mins"><option value="3">3 minutes</option><option value="5" selected>5 minutes</option><option value="10">10 minutes</option><option value="15">15 minutes</option></select></label>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px"><span class="timer" id="pr-timer">05:00</span><span style="display:flex;gap:8px"><button class="btn btn-primary btn-sm" id="pr-start" type="button">Start timer</button><button class="btn btn-line btn-sm" id="pr-reset" type="button">Reset</button></span></div>
    <div><b style="font-size:14px">A strong answer usually</b><ul class="rubric"><li>Clarifies the goal and the user first</li><li>Structures the answer in clear steps</li><li>Considers trade-offs and risks</li><li>Ends with metrics or next steps</li></ul></div>
  </div>
  <div class="card">
    <div class="kicker">Your question</div><p class="qbox" id="pr-q"></p>
    <label>Your answer <span class="meta">(saved on this device)</span><textarea id="pr-answer" style="min-height:220px" placeholder="Think out loud: clarify, structure, decide, measure…"></textarea></label>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
      <button class="btn btn-primary btn-sm" id="pr-ai" type="button">✨ Get AI feedback</button>
      <button class="btn btn-line btn-sm" id="pr-copy" type="button">Copy prompt</button>
      <button class="btn btn-line btn-sm" id="pr-next" type="button" style="margin-left:auto">New question ↻</button></div>
    <p class="meta" id="pr-copied" aria-live="polite" style="margin:10px 0 0"></p>
    <div class="ai-doc ai-out" id="pr-ai-out" hidden style="margin-top:16px;min-height:0"></div>
    <p class="meta" style="margin:10px 0 0">Feedback is generated right here by SkillNavora's AI coach. Don't include private or company data. More tools in <a href="ai.html">AI Studio</a>.</p>
  </div>
</div></section>"""
page("practice.html", "Practice with AI · SkillNavora", "Free AI mock interview practice for product managers, data engineers and GenAI professionals.", prac, "practice.html",
     UP_JS + '<script src="{r}assets/upskill.js"></script><script src="{r}assets/ai.js"></script>', attrs=' data-page="practice"')

FW = [("RICE", "Prioritise a backlog", "Reach × Impact × Confidence ÷ Effort. Score each idea, then sanity-check the ranking."),
      ("Kano", "Decide which features delight", "Classify features as Must-be, Performance, Attractive, Indifferent or Reverse using a short survey."),
      ("MoSCoW", "Scope a release", "Must have, Should have, Could have, Won't have (this time)."),
      ("Jobs-to-be-done", "Understand motivation", "When [situation], I want to [motivation], so I can [outcome]."),
      ("AARRR (Pirate metrics)", "Map the growth funnel", "Acquisition, Activation, Retention, Referral, Revenue."),
      ("HEART", "Measure user experience", "Happiness, Engagement, Adoption, Retention, Task success, each with goals, signals and metrics."),
      ("North Star metric", "Align the team", "One metric that captures the value users get, supported by input metrics the team can move."),
      ("Five whys", "Find the root cause", "Ask 'why?' repeatedly until you reach a cause you can act on."),
      ("CIRCLES", "Answer product design questions", "Comprehend, Identify users, Report needs, Cut through prioritisation, List solutions, Evaluate trade-offs, Summarise.")]
PRD = """PRD: [Feature name]
Owner: [Name] · Status: Draft · Last updated: [Date]

1. Problem
   Who has the problem, what it is, and the evidence (data, interviews, tickets).

2. Goal and success metrics
   Primary metric (with baseline and target), secondary metrics, guardrails.

3. Users and use cases
   Target segment, top 3 user stories: "As a [user], I want [action] so that [benefit]."

4. Solution
   What we'll build (link designs), what's out of scope, open questions.

5. AI behaviour (if applicable)
   Inputs, model, prompt/approach, what it must never do, human review,
   evaluation set and pass criteria, cost per request.

6. Launch plan
   Experiment design, rollout stages, support and comms, rollback criteria.

7. Risks and dependencies
   Technical, legal/privacy, operational; owners and mitigations."""
FREE = [("Anthropic Academy", "Free courses on Claude, Claude Code, the API and MCP", "https://www.anthropic.com/learn"),
        ("DeepLearning.AI short courses", "Free 1–2 hour courses on LLMs, RAG and agents", "https://www.deeplearning.ai/short-courses/"),
        ("Figma Learn", "Official Figma tutorials and design basics", "https://help.figma.com"),
        ("n8n courses", "Free Level 1 and 2 automation courses", "https://docs.n8n.io/courses/"),
        ("Make Academy", "Free automation courses with badges", "https://academy.make.com"),
        ("Google Analytics Academy", "Free analytics fundamentals", "https://skillshop.withgoogle.com")]

CASES = [('Klook_UX_Evaluation_Redesign.pdf', 'Klook UX Evaluation Redesign'), ('Noon_UAE_UX_Heuristic_Evaluation.pdf', 'Noon UAE UX Heuristic Evaluation'), ('Nykaa_UX_Analysis_Final_PPT.pdf', 'Nykaa UX Analysis Final PPT'), ('Nykaa_User_Journey_Detailed.pdf', 'Nykaa User Journey Detailed'), ('OYO_UX_Evaluation_v3_10_Pages.pdf', 'OYO UX Evaluation v3 10 Pages'), ('OYO_UX_Evaluation_v3_Detailed_Report.pdf', 'OYO UX Evaluation v3 Detailed Report'), ('SkillOS_Detailed_PDF.pdf', 'SkillOS Detailed PDF'), ('SkillOS_PS_Presentation_Detailed.pdf', 'SkillOS PS Presentation Detailed'), ('Slack_Channel_Creation_UX_7_Pages.pdf', 'Slack Channel Creation UX 7 Pages'), ('Slack_UX_Detailed_Report_37_Pages.pdf', 'Slack UX Detailed Report 37 Pages'), ('Uber_Find_My_Ride_Case_Study_5_Page.pdf', 'Uber Find My Ride Case Study 5 Page'), ('Zepto_AOV_Varun_10_Slides.pdf', 'Zepto AOV Varun 10 Slides'), ('Zepto_AOV_Varun_Kumar_5_Slides.pdf', 'Zepto AOV Varun Kumar 5 Slides'), ('Zepto_AOV_Varun_detailed_16_slide.pdf', 'Zepto AOV Varun detailed 16 slide'), ('Zomato_UX_Deck_10_Pages.pdf', 'Zomato UX Deck 10 Pages'), ('Zomato_UX_Deck_19_Pages.pdf', 'Zomato UX Deck 19 Pages')]
def _pages(f):
    m = re.search(r"(\d+)[ _](Pages?|Slides?|Page)", f, re.I); return (m.group(1) + " " + ("slides" if "lide" in m.group(2) else "pages")) if m else "PDF"
INTERVIEW_LINKS = [("NextLeap", "PM interview question bank", "Product design, strategy, metrics, RCA and more, by topic.", "https://nextleap.app/interview-preparation/product-management/questions"),
  ("NextLeap", "Guesstimate questions", "Guesstimates asked at top tech companies.", "https://nextleap.app/interview-preparation/product-management/questions/topic/guesstimates"),
  ("HelloPM", "PM interview preparation", "A free guide to every PM interview round.", "https://hellopm.co/resources-for-product-management-interview/"),
  ("HelloPM", "Root cause analysis (RCA) guide", "Step-by-step approach with worked examples.", "https://hellopm.co/how-to-approach-rca-questions/")]
DSA_ARTIFACT = 'https://claude.ai/artifact/7278116b7jCN2ny9XnmtVM#dsa'      # paste the Claude artifact link of the DSA handbook here
DS_ARTIFACT = 'https://claude.ai/artifact/7278116b7jCN2ny9XnmtVM#data-science'       # Data Science & AI handbook artifact link
GENAI_ARTIFACT = 'https://claude.ai/artifact/7278116b7jCN2ny9XnmtVM#genai'    # GenAI handbook artifact link
RES_PANEL = f'''    <div class="panel" id="p-resources" hidden>
      <div class="hb-hero"><div><div class="kicker">Free for everyone</div><h2 class="h2s" style="margin:4px 0 6px">Resources &amp; AI tools</h2>
        <p class="meta" style="margin:0">Every AI and product tool with its official website, the complete PM Master Handbook, interview practice, the PM frameworks cheat sheet, a PRD template and hand-picked free courses.</p></div></div>
      <h3 class="h3s hb-h">AI and product tools</h3><div class="tgroups" id="res-tools"></div>
      <h3 class="h3s hb-h">PM Master Handbook by Varun Kumar</h3><p class="meta" style="margin:-4px 0 12px">23 modules and 570 pages: 12 Product Core modules, an 11-class AI Tools Lab, frameworks, case studies, projects and interview prep.</p>
      <div class="hb-acts" style="margin-bottom:14px"><a class="btn btn-primary btn-sm" href="{HB_ART}" target="_blank" rel="noopener">Open the interactive handbook ↗</a><a class="btn btn-line btn-sm" href="handbook/Complete-PM-Master-Handbook.pdf" target="_blank" rel="noopener">Complete handbook PDF (570 pages, 22 MB) ↗</a></div>
      <h3 class="h3s hb-h" style="font-size:16px">Product Core modules</h3><div class="hb-list">{_hb_mods(HB_CORE)}</div>
      <h3 class="h3s hb-h" style="font-size:16px">AI Tools Lab</h3><div class="hb-list">{_hb_mods(HB_AI)}</div>
      <h3 class="h3s hb-h" style="font-size:16px">Libraries</h3><div class="hb-list">{HB_LIBROWS}</div>
      <h3 class="h3s hb-h">PM interview practice (free, on the original sites)</h3><p class="meta" style="margin:-4px 0 12px">Hand-picked public question banks and guides from other PM communities. Each link opens the original page in a new tab.</p>
      <div class="grid g4">{''.join(f'<a class="card tool" href="{u}" target="_blank" rel="noopener"><span class="ftag">{E(src)}</span><h3 style="margin-top:8px">{E(t)} ↗</h3><p>{E(d)}</p></a>' for src, t, d, u in INTERVIEW_LINKS)}</div>
      <h3 class="h3s hb-h">PM frameworks cheat sheet</h3>
      <div class="card table-wrap" style="padding:8px 16px"><table class="fw"><thead><tr><th>Framework</th><th>Use it to</th><th>How it works</th></tr></thead><tbody>{''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td class="meta">{E(c)}</td></tr>' for a, b, c in FW)}</tbody></table></div>
      <h3 class="h3s hb-h">PRD template</h3>
      <div class="card"><div class="tpl" id="prd">{E(PRD)}</div><button class="btn btn-line btn-sm" style="margin-top:14px" type="button" onclick="navigator.clipboard.writeText(document.getElementById('prd').innerText).then(()=>this.textContent='Copied ✓')">Copy template</button></div>
      <h3 class="h3s hb-h">Free courses</h3>
      <div class="grid g3">{''.join(f'<a class="card tool" href="{u}" target="_blank" rel="noopener"><h3>{E(a)} ↗</h3><p>{E(b)}</p></a>' for a, b, u in FREE)}</div>
    </div>
'''
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import restabs
_pm = RES_PANEL
_pm = _pm[_pm.index('<h3 class="h3s hb-h">AI and product tools</h3>'):_pm.rindex('</div>')]
_pm = _pm.replace('<div class="tgroups" id="res-tools"></div>', '<div class="tgroups" data-res-tools="ai-pm"></div>')
_pm = _pm.replace('PM Master Handbook by Varun Kumar</h3>', 'PM Master Handbook by Varun Kumar</h3>')
_hero = ('<div class="hb-hero"><div><div class="kicker">AI-First Product Management</div><h2 class="h2s" style="margin:4px 0 6px">Resources for Product Managers</h2>'
         '<p class="meta" style="margin:0">The PM Master Handbook, AI and product tools with their official websites, interview practice, a frameworks cheat sheet, a PRD template and free courses.</p></div></div>')
res = uhero("Upskill for free · Resources & AI tools", 'Resources <span class="g">&amp; AI tools</span>', "Handbooks, PDFs, tools, practice sites and useful links for product managers, data engineers and GenAI learners. Register once with your details to open any handbook, PDF or file.") + f"""
<section style="padding-top:36px"><div class="wrap">
{restabs.build(_hero + _pm, dict(dsa_artifact=DSA_ARTIFACT, ds_artifact=DS_ARTIFACT, genai_artifact=GENAI_ARTIFACT))}
</div></section>
"""
LMS_RES = ('    <div class="panel" id="p-resources" hidden>\n      <div class="hb-hero"><div><div class="kicker">Free for everyone</div><h2 class="h2s" style="margin:4px 0 6px">Resources &amp; AI tools</h2>'
           '<p class="meta" style="margin:0">Choose a course tab: PM, Data Engineers, GenAI or other links. Every handbook, PDF and tool for that course is listed in its tab.</p></div></div>\n'
           + restabs.build(_hero + _pm, dict(dsa_artifact=DSA_ARTIFACT, ds_artifact=DS_ARTIFACT, genai_artifact=GENAI_ARTIFACT), scope="lms") + "\n    </div>\n")
import tooltuts
_tt_html, _tt_n = tooltuts.build()
tt = uhero("Upskill for free · Resources & AI tools", 'Tool <span class="g">tutorials</span>', f"All {_tt_n} tools taught in our programs: a free official tutorial, the official website and the SkillNavora lesson for each, including complete Figma and n8n tutorials.") + f"""
<section style="padding-top:28px"><div class="wrap">{_tt_html}</div></section>"""
_tt_banner = '<section style="padding:24px 0 0"><div class="wrap"><div class="card" style="border:2px solid #6C4CF5;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between"><div style="max-width:720px"><div class="kicker">New · step-by-step course</div><b style="font-size:18px">AI Builder Tools: Claude, Claude Code, ChatGPT &amp; Codex, Gemini, Lovable</b><p class="meta" style="margin:4px 0 0">What each tool can do and how: create a website, add pages, connect tools and other websites, publish on your own domain.</p></div><div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn btn-primary" href="ai-builder-tools.html">Open the course</a><a class="btn btn-line" href="ai-academy-interactive.html#builder-tools">Interactive</a><a class="btn btn-line" href="handbook/AI_Builder_Tools.pdf">PDF</a></div></div></div></section>'
_tt_i = tt.find('</div></div>') + len('</div></div>') if tt.startswith('<div class="hero"') else 0
page("tools.html", "Tool tutorials · SkillNavora", "Free tutorials for every AI, product, design, automation and data tool in SkillNavora programs, including complete Figma and n8n tutorials.", tt[:_tt_i] + _tt_banner + tt[_tt_i:], "tools.html")
import practice
_pt_html, _pt_n = practice.tests_page()
page("tests.html", "Practice tests · SkillNavora", "Free practice tests for product management, data science, SQL, Excel, Python, Power BI, GenAI, agents and more, with hints and solutions.",
     uhero("Upskill for free · Practice & test yourself", 'Practice <span class="g">tests</span>', f"{_pt_n} questions and exercises from every SkillNavora handbook. Get a hint when you are wrong, then try again.") + f"""<section style="padding-top:28px"><div class="wrap">{_pt_html}</div></section>""", "tests.html")
_iv_html, _iv_n = practice.questions_page()
page("questions.html", "Top 100 interview questions · SkillNavora", "The top 100 interview questions with model answers for AI product management, data science and AI, and GenAI and agents.",
     uhero("Upskill for free · Practice & test yourself", 'Top 100 <span class="g">interview questions</span>', "For AI Product Management, Data Science & AI, and GenAI & Agents, with model answers and the lesson that teaches each topic.") + f"""<section style="padding-top:28px"><div class="wrap">{_iv_html}</div></section>""", "questions.html")
GUIDE_TRACK = {"guides/sfmc.html": "sfmc", "guides/digital-marketing.html": "marketing", "guides/content-creation.html": "content", "guides/fde.html": "fde", "guides/public-speaking.html": "speaking"}
_cat = json.load(open(os.path.join(OUT, "data-science/catalog.json")))
_tr = {t["id"]: t for t in _cat["tracks"]}
for _gp, _tid in GUIDE_TRACK.items():
    _t = _tr.get(_tid)
    if not _t or not _t["lessons"]: continue
    _L = _t["lessons"][0]
    _src = "../data-science/" + _L["page"]; _pdf = "../data-science/" + _t["pdf"]
    _body = uhero("Programs · Other programs", E(_t["name"]), E(_t["desc"])) + f"""
<section style="padding-top:24px"><div class="wrap">
  <div class="acts" style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px"><a class="btn btn-primary" href="{_pdf}">Complete guide PDF</a><a class="btn btn-line" href="../contact.html">Ask about live training</a><a class="btn btn-line" href="../tests.html#other">Practice test</a><a class="btn btn-line" href="../questions.html#other">Interview questions</a></div>
  {'<div class="card" style="margin:0 0 16px;border:2px solid #6C4CF5"><b>Practise with the AI Speaking Coach:</b> <a href="../speaking-coach.html#free">Free speech (any topic)</a> · <a href="../speaking-coach.html#shadow">Shadowing</a> · <a href="../speaking-coach.html#engint">English interview practice</a> · <a href="../speaking-coach.html#drill">Pronunciation drills</a> · <a href="../speaking-coach.html#learn-english">Free videos &amp; websites to learn English</a></div>' if _tid == "speaking" else ""}
  <p class="meta" style="margin:0 0 12px">The complete guide is below. It opens right here: scroll inside it, or download the PDF.</p>
  <iframe class="guide-frame" src="{_src}" title="{E(_t['name'])} complete guide" loading="lazy" style="width:100%;height:85vh;border:1px solid var(--line,#e2dcf3);border-radius:16px;background:#fff"></iframe>
</div></section>"""
    page(_gp, f"{_t['name']} complete guide · SkillNavora", _t["desc"], _body, _gp)
import labpage
_lb_html, _lb_n = labpage.build()
page("lab.html", "Practice Lab · SkillNavora", "Free practice lab: run SQL, Excel formulas and Python in your browser, spot the trap and see the fix. AI PM and GenAI real-life scenarios with hints.",
     uhero("Upskill for free · Practice & interview prep", 'Practice <span class="g">Lab</span>', f"{_lb_n} hands-on challenges from basic to advanced. Run real SQL, Excel formulas and Python in your browser, spot the trap before your interviewer does, and see the fix. Free, no sign-up.")
     + f"""<section style="padding-top:24px"><div class="wrap">{_lb_html}</div></section>""", "lab.html", '<script src="{r}assets/vendor/formula-parser.min.js"></script><script src="{r}assets/lab.js"></script>')
_AIJS = '<script src="{r}assets/ai.js"></script>'
aipages.write_index(OUT)
page("ai.html", "AI Studio: free AI Tutor, PRD Writer and Speaking Coach · SkillNavora", "Free AI tools for learners: an AI Tutor for PM, data and GenAI questions, an AI PRD Writer, an AI Speaking Coach for English and interviews, and AI mock interviews.",
     uhero("Free · Built into SkillNavora", 'AI <span class="g">Studio</span>', "Your AI tutor, PRD writer, speaking coach and interview coach, all in one place. Ask, write, speak and practise without leaving SkillNavora.") + aipages.hub(), "ai.html")
page("ai-tutor.html", "AI Tutor · SkillNavora", "Ask the SkillNavora AI Tutor any question on product management, Excel, SQL, Python, Power BI, Tableau, machine learning, GenAI, agents, careers or English.",
     uhero("AI Studio · AI Tutor", 'Ask <span class="g">Navora</span>, your AI Tutor', "Clear answers with examples, code and the right SkillNavora lesson, 24×7. English, Hindi or Hinglish.") + aipages.tutor(), "ai-tutor.html", _AIJS)
page("prd-writer.html", "AI PRD Writer · SkillNavora", "Free AI PRD writer: turn a product idea into a complete product requirements document with personas, user stories, requirements, metrics and a launch plan.",
     uhero("AI Studio · AI PRD Writer", 'Idea to <span class="g">PRD</span> in a minute', "Describe your product idea. Get a complete PRD with users, stories, requirements, success metrics and launch plan, then refine it by asking.") + aipages.prd(), "prd-writer.html", _AIJS)
page("pm-toolkit.html", "AI PM Toolkit · SkillNavora", "Free AI PM toolkit: customer problem discovery, opportunity sizing and prioritization, A/B test design, API integration planning, launch planning, metrics, user research, competitive analysis, user stories, roadmaps and stakeholder updates.",
     uhero("AI Studio · AI PM Toolkit", 'Find your next <span class="g">PM superpower</span>', "Pick a capability, add your context, review the result. 13 product-management capabilities that turn your situation into a ready-to-use deliverable.") + aipages.pm_toolkit(), "pm-toolkit.html", _AIJS)
page("speaking-coach.html", "AI Speaking Coach · SkillNavora", "Free AI speaking coach: practise English, public speaking and interview answers out loud and get scores for fluency, grammar, structure and pace.",
     uhero("AI Studio · AI Speaking Coach", 'Speak with <span class="g">confidence</span>', "Answer out loud. Get instant scores for fluency, grammar, structure and pace, the exact words to fix, a better version to listen to, and your next drill.") + aipages.speaking(), "speaking-coach.html", _AIJS)
import reqdocs
reqdocs.write_templates(OUT)
_prdl, _prdn = reqdocs.prd_library()
page("prd-library.html", "PRD library: template, examples and 120 PRD ideas · SkillNavora", "Learn to write PRDs: a section-by-section PRD template with examples, framing tips, common mistakes, 120 PRD ideas across 15 industries and the best guides and apps.",
     uhero("Resources for PM · PRD library", f'PRD <span class="g">library</span>', f"How top product managers frame a PRD, a free template, and {_prdn} ideas across 15 industries you can turn into a full PRD with AI in one click.") + _prdl, "prd-library.html")
page("brd-frd.html", "BRD & FRD guide for business analysts · SkillNavora", "BRD vs FRD vs PRD, BRD and FRD templates, a traced sample, business analysis techniques, 25 project ideas and the best BA guides and tools.",
     uhero("Resources for Data Engineers · Business analyst", 'BRD &amp; <span class="g">FRD</span> guide', f"For business and data analysts: what goes into a Business Requirements Document and a Functional Requirements Document, free templates, and {len(reqdocs.BRD_IDEAS)} real project ideas to practise with AI.") + reqdocs.brd_frd(), "brd-frd.html")
import evals_course
page("ai-evals.html", "AI Evals for Product Managers: free PDF, basic to advanced · SkillNavora", "What AI evals are and how product managers use them: success criteria, golden datasets, LLM-as-judge, error analysis, RAG and agent evals, safety, A/B tests and monitoring. 10 classes and a free PDF.",
     uhero("AI Product Management · AI Evals", 'AI <span class="g">Evals</span> for Product Managers', "How to measure, improve and safely launch AI features. 10 classes from basic to advanced, with templates, a metrics cheat sheet and interview questions.") + evals_course.web_page(), "ai-evals.html")
import coursekit, course_browser, course_brain, course_context, course_skills, course_orch, skillsmap
_K = 'AI Product Management · GenAI Launchpad'
for _C, _hero in [(course_browser.COURSE, (_K, 'Browser <span class="g">Automation</span> &amp; AI Agents')),
                  (course_brain.COURSE, (_K, 'Your AI <span class="g">Second Brain</span>')),
                  (course_context.COURSE, (_K + ' · Skill 1 of 7', 'Prompt &amp; <span class="g">Context</span> Engineering')),
                  (course_skills.COURSE, (_K + ' · Skill 2 of 7', 'AI <span class="g">Skills</span> &amp; Templates')),
                  (course_orch.COURSE, (_K + ' · Skill 7 of 7', 'Agent <span class="g">Orchestration</span> &amp; Monitoring'))] + [(_M, (_K + ' · Advanced AI PM', E(_M["title"]))) for _M in __import__("courses_more").ALL] + [(__import__("course_builder").COURSE, (_K + ' · AI tools', 'AI <span class="g">Builder</span> Tools')), (__import__("course_webauto").COURSE, (_K + ' · AI tools', 'Web <span class="g">Automation</span>: Webhooks, Triggers &amp; Playwright MCP')), (__import__("course_aiengineer").COURSE, ('Other programs · Career path', 'AI <span class="g">Engineer</span>: the complete path'))]:
    page(_C["page"], _C["title"] + ": free PDF, basic to advanced · SkillNavora", _C["intro"], uhero(_hero[0], _hero[1], _C["intro"]) + coursekit.web_page(_C), _C["page"])
page("ai-academy.html", "AI Skills Academy: every AI skills course in one place · SkillNavora", "All SkillNavora AI skills courses in one section: the 7 core AI skills and advanced AI product management topics, each with lessons, a PDF and an interactive version.",
     uhero("AI Product Management · GenAI Launchpad", 'AI Skills <span class="g">Academy</span>', "Every AI skills course in one place: lessons, free PDFs and interactive versions, from prompting and context to strategy, AI UX, pricing, governance and more.") + academy.hub(), "ai-academy.html")
import academy_interactive, study_hub, study_library
page("ai-academy-interactive.html", "Interactive AI Skills Academy · SkillNavora", "All AI skills courses as one interactive page: tabs for every course, illustrated classes, takeaways, practice, cheat sheets and interview questions.",
     academy_interactive.site_html(), "ai-academy.html")
page("study-library.html", "SkillNavora Study Library: all study material in one place", "Every program, handbook, lesson, AI skills course, practice set, tool, learning site and PDF on SkillNavora in one page with 11 tabs and a filter.",
     study_library.site_html(), "study-library.html")
page("study-hub.html", "Study Hub: AI PM, Data Engineer, AI Engineer, GenAI Launchpad · SkillNavora", "All SkillNavora study material in one place with four tabs: AI Product Management, AI for Data Engineers, AI Engineer and GenAI Launchpad, with every lesson, class, PDF and practice set.",
     uhero("Study Hub", 'All your study material, <span class="g">one place</span>', "Pick your path: AI Product Management, AI for Data Engineers, AI Engineer or GenAI Launchpad. Every lesson, class, PDF and practice set is one click away.") + study_hub.build(), "study-hub.html")
page("ai-skills-map.html", "AI Skills Map: every AI skill and where to learn it · SkillNavora", "The complete AI skills catalogue for professionals: prompting, context, skills, second brain, research, evals, automation, orchestration, media, engineering and PM skills, mapped to free SkillNavora lessons, plus what job descriptions ask for.",
     uhero("AI Studio · AI Skills Map", 'Every <span class="g">AI skill</span>, one map', "What to learn first, the full catalogue of AI skills, and exactly where to learn each one on SkillNavora, plus the skills employers ask for in AI-era job descriptions.") + skillsmap.page(), "ai-skills-map.html")
page("resources.html", "Resources & AI tools · SkillNavora", "Handbooks, PDFs, AI tools, practice sites and useful links for product managers, data engineers and GenAI learners.", res, "resources.html")

# ================================================================ CONTACT
contact = uhero("Contact us", 'We\'re here to <span class="g">help</span>', "Questions about programs, fees or schedules? WhatsApp is the fastest way to reach us, or send a message below.") + """
<section><div class="wrap cgrid">
  <ul class="clist" id="clist"></ul>
  <form id="form" class="card form">
    <h3 style="font-size:20px">Send a message</h3>
    <div class="row2"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input name="email" type="email" required autocomplete="email"></label></div>
    <label><span class="req">Phone / WhatsApp</span><input name="phone" required inputmode="tel" maxlength="20" autocomplete="tel" placeholder="+91 98765 43210"></label>
    <label>I'm interested in<select name="interest"><option>AI-First Product Management</option><option>AI-First Data Engineer</option><option>GenAI Launchpad</option><option>Corporate or college training</option><option>Something else</option></select></label>
    <label>Message<textarea name="message" required placeholder="Tell us about your background and goals"></textarea></label>
    <input type="checkbox" name="botcheck" hidden>
    <button class="btn btn-primary" type="submit">Send message</button>
    <p class="meta" id="msg" aria-live="polite" style="margin:0"></p>
  </form>
</div></section>"""
WHY_US = [
    ("AI-first, not AI-added", "Every program is built around how teams work in 2026: Claude, ChatGPT, Copilot, agents, MCP and no-code automation are part of every module, not a bonus lecture at the end."),
    ("Taught by a working product leader", "You learn from people who ship products at large companies today, so the frameworks, interview questions and case studies match what hiring managers actually ask."),
    ("Free handbooks you can keep", "A 570-page PM Master Handbook, a 1,200+ page Data Science & AI handbook and a GenAI Launchpad handbook, with a PDF for every lesson, free for every registered learner."),
    ("Learn by doing", "Real outputs from runnable code, datasets, Excel workbooks, Power BI and Tableau case studies, n8n and Figma projects and a capstone in every track, so you finish with proof of work."),
    ("Practice that tells you why", "Practice tests with hints and worked solutions, 100 top interview questions for each career path, mock interviews with AI feedback and real product challenges."),
    ("Portfolio and job support", "Resume and LinkedIn reviews, portfolio projects on GitHub and Tableau Public, a curated job board, referrals and interview preparation until you are job-ready."),
    ("Small live cohorts", "Live classes with doubt-clearing, recordings in the LMS, assignments with feedback and a community of peers from product, data and engineering."),
    ("Built for Indian careers", "Examples in rupees, Indian companies and datasets, salary and offer guidance for the Indian market, and classes timed for working professionals."),
]
CMP = [("Curriculum", "Updated for 2026: AI agents, MCP, Claude Code, n8n", "Often pre-GenAI syllabus"), ("Teaching", "Working product and data leaders", "Full-time trainers"),
       ("Materials", "Free handbooks and PDFs for every lesson", "Slides only, locked after the course"), ("Practice", "Tests with hints, 100 questions per path, AI mock interviews", "Few graded exercises"),
       ("Outcome", "Portfolio, GitHub, Tableau Public and job board", "Certificate only")]
about = uhero("About Us", 'About <span class="g">SkillNavora</span>', "An all-in-one place to learn AI-first product management, data science and AI, and generative AI: live programs, free handbooks, practice tests and career support.") + f"""
<section style="padding-top:32px"><div class="wrap about-hero-grid">
  <div><div class="kicker">Our mission</div><h2 class="sec-h">Make every professional AI-first</h2>
    <p class="sub">SkillNavora started with a simple observation: most courses teach yesterday's job. Product managers, analysts and engineers now work with AI assistants, agents and automation every day, and learners need practical, honest training for that world. We combine live classes with free, detailed handbooks so anyone can learn at their own pace and come back to the material for years.</p></div>
  <div class="card" style="padding:22px"><h3 style="margin:0 0 10px">What you will find here</h3><ul class="checks"><li>Three flagship programs: AI-First PM, AI-First Data Engineer, GenAI Launchpad</li><li>Other programs: SFMC, digital marketing, content creation, Forward Deployed Engineer</li><li>Free handbooks, tool tutorials, practice tests and interview questions</li><li>Job board, referrals and portfolio support</li></ul></div>
</div></section>
<section id="team" class="tint"><div class="wrap"><div class="kicker">SkillNavora team</div><h2 class="sec-h">Meet our founder</h2>
  <div class="card founder" style="padding:24px;margin-top:20px"><img src="assets/varun.jpg" alt="Varun Kumar" width="160" height="160" loading="lazy">
    <div><h3 style="margin:0">Varun Kumar</h3><p class="meta" style="margin:4px 0 12px"><b>Founder &amp; CEO, SkillNavora</b> · Gurgaon, India</p>
    <p style="margin:0 0 10px">Varun works in Product at American Express (Amex) and brings more than a decade of experience building products and leading cross-functional teams. He founded SkillNavora to give learners the practical, AI-first training he wishes he had had: real frameworks, real case studies and the tools modern product and data teams use every day.</p>
    <p style="margin:0">He wrote the SkillNavora PM Master Handbook and designs the curriculum for every program, and he mentors learners on product thinking, interviews and career moves into product and AI roles.</p>
    <div class="acts" style="margin-top:14px"><a class="btn btn-line btn-sm" href="https://www.linkedin.com/in/varun-pm01" target="_blank" rel="noopener">LinkedIn ↗</a></div></div></div>
</div></section>
<section id="why-us"><div class="wrap"><div class="kicker">Why us</div><h2 class="sec-h">Why learners choose SkillNavora</h2>
  <div class="why-grid" style="margin-top:22px">{''.join(f'<div class="why-card"><div class="n">{i:02d}</div><h3>{E(t)}</h3><p class="meta" style="margin:0">{E(d)}</p></div>' for i, (t, d) in enumerate(WHY_US, 1))}</div>
  <h3 class="h3s" style="margin-top:36px">SkillNavora compared with a typical course</h3>
  <div class="card table-wrap" style="padding:8px 16px;margin-top:12px"><table class="cmp"><thead><tr><th></th><th>SkillNavora</th><th>Typical course</th></tr></thead><tbody>{''.join(f'<tr><th>{E(a)}</th><td>{E(b)}</td><td class="meta">{E(c)}</td></tr>' for a, b, c in CMP)}</tbody></table></div>
</div></section>
<section class="tint"><div class="wrap"><div class="grid g3">
  <a class="card tool" href="reviews.html"><h3>Reviews →</h3><p>Read what learners say about the programs and mentors.</p></a>
  <a class="card tool" href="blogs.html"><h3>Blog →</h3><p>Guides on becoming a PM, AI tools, case studies and data careers.</p></a>
  <a class="card tool" href="contact.html"><h3>Contact us →</h3><p>WhatsApp, call or email the team about programs, fees and batches.</p></a>
</div></div></section>"""
page("about.html", "About Us · SkillNavora", "About SkillNavora: our mission, founder and CEO Varun Kumar, and why learners choose our AI-first programs in product management, data science and generative AI.", about, "about.html")
page("contact.html", "Contact us · SkillNavora", "Contact SkillNavora on WhatsApp, phone or email about programs, fees and schedules.", contact, "contact.html")

# ================================================================ AUTH + LMS + ADMIN
login = f"""<div class="auth-page"><div class="auth-split">
  <div class="auth-side">
    <a class="logo" href="index.html" aria-label="SkillNavora home"><img src="assets/logo-s.svg" alt="" width="36" height="36"><span><i class="c">S</i>kill<em><i class="c">N</i>avora</em></span></a>
    <div><h2>Welcome back ✨</h2><p>Live, AI-first programs to accelerate your career in product, data engineering and GenAI.</p>
    <ul class="checks"><li>25+ real-world case studies</li><li>Recordings, pre-reads and assignments in one place</li><li>Monthly 1:1 with a CEO or Head of Product</li></ul></div>
    <a class="side-link" href="programs.html">Explore programs →</a>
  </div>
  <div class="auth-card">
    <a class="logo mob" href="index.html" aria-label="SkillNavora home"><img src="assets/logo-s.svg" alt="" width="36" height="36"><span><i class="c">S</i>kill<em><i class="c">N</i>avora</em></span></a>
    <h1 id="auth-title">Log in to your account</h1>
    <p class="meta" id="auth-sub" style="margin:0">Enter your email and we'll send you a sign-in link.</p>
    <p id="auth-msg" class="notice" hidden role="status" style="margin-top:16px;text-align:left"></p>
    <div id="auth-forms">
      <form id="s-email" class="form"><form id="f-email" class="form" style="display:contents">
      </form></form>
    </div>
  </div>
</div></div>"""
login = login.replace('''      <form id="s-email" class="form"><form id="f-email" class="form" style="display:contents">
      </form></form>''', f'''      <div id="s-email"><form id="f-email" class="form">
        <label id="name-row" hidden>Full name<input name="full_name" maxlength="120" autocomplete="name"></label>
        <label>Email<input name="email" type="email" required autocomplete="email" placeholder="you@gmail.com"></label>
        <button type="submit">Email me a sign-in link</button></form></div>
      <div id="s-code" hidden><form id="f-code" class="form">
        <div class="notice info" style="text-align:left">📩 We've emailed a sign-in link to <b id="code-to"></b>. Open the email and click <b>Sign in</b>. You'll be logged in automatically.</div>
        <p class="meta" style="margin:0">Didn't get it? Check your spam folder. If your email shows a code instead, enter it here:</p>
        <label>Code from the email<input name="token" required inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{{6,8}}" maxlength="8" placeholder="123456" class="otp"></label>
        <button type="submit">Verify and continue</button>
        <button type="button" class="linkbtn" data-step="s-email">← Use a different email</button></form></div>
      <div id="s-phone" hidden><form id="f-phone" class="form">
        <label>Mobile number<span class="otp-row"><select name="cc" aria-label="Country code"><option value="+91">🇮🇳 +91</option><option value="+971">🇦🇪 +971</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option><option value="+65">🇸🇬 +65</option></select><input name="phone" required inputmode="tel" autocomplete="tel-national" placeholder="98765 43210"></span></label>
        <button type="submit" id="phone-go">Get OTP</button></form></div>
      <div id="s-pcode" hidden><form id="f-pcode" class="form">
        <p class="meta" style="margin:0">We sent an OTP to <b id="pcode-to"></b>.</p>
        <label>OTP<input name="token" required inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{{4,8}}" maxlength="8" placeholder="123456" class="otp"></label>
        <button type="submit">Verify and continue</button>
        <button type="button" class="linkbtn" data-step="s-phone">← Change number</button></form></div>
      <div id="s-pass" hidden><form id="f-pass" class="form">
        <label>Email<input name="email" type="email" required autocomplete="email"></label>
        <label>Password<input name="password" type="password" required autocomplete="current-password"></label>
        <button type="submit">Log in</button>
        <button type="button" class="linkbtn" data-step="s-forgot">Forgot your password?</button></form></div>
      <div id="s-signpw" hidden><form id="f-signpw" class="form">
        <label>Full name<input name="full_name" required maxlength="120" autocomplete="name"></label>
        <label>Email<input name="email" type="email" required autocomplete="email" placeholder="you@gmail.com"></label>
        <label>Create a password<input name="password" type="password" required minlength="8" autocomplete="new-password" placeholder="At least 8 characters"></label>
        <button type="submit">Create account</button></form></div>
      <div id="s-setpw" hidden><form id="f-setpw" class="form">
        <div class="notice ok" style="text-align:left">✅ You're signed in. Set a password so you can log in with your email and password next time.</div>
        <label>New password<input name="password" type="password" required minlength="8" autocomplete="new-password" placeholder="At least 8 characters"></label>
        <button type="submit">Save password and continue</button>
        <button type="button" class="linkbtn" id="setpw-skip">Skip for now</button></form></div>
      <div id="s-forgot" hidden><form id="f-forgot" class="form">
        <label>Email<input name="email" type="email" required autocomplete="email"></label>
        <button type="submit">Send reset link</button>
        <button type="button" class="linkbtn" data-step="s-pass">← Back</button></form></div>
      <div id="s-choose" hidden><div class="choose">
        <a href="lms.html"><span class="ci">{SVG('<rect x="3" y="3" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="14" y="13" width="7" height="8" rx="1.5"/>')}</span><b>My course dashboard</b><span>→</span></a>
        <a href="admin.html" id="go-admin" hidden><span class="ci">{SVG('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>')}</span><b>Admin panel</b><span>→</span></a>
        <a href="programs.html"><span class="ci">{SVG('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>')}</span><b>Explore SkillNavora programs</b><span>→</span></a>
      </div></div>
      <div id="methods">
        <div class="or">or</div>
        <button class="gbtn alt" id="m-google" type="button" hidden>{G}Continue with Google</button>
        <button class="gbtn alt" id="m-wa" type="button" hidden><span style="color:#25d366;display:inline-flex">{WA.replace('width="18" height="18"','width="20" height="20"')}</span>Continue with WhatsApp</button>
        <button class="gbtn alt" id="m-phone" type="button" hidden data-step="s-phone">{SVG('<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>')}Continue with mobile number</button>
        <button class="gbtn alt" id="m-pass" type="button" data-step="s-pass">{SVG('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>')}Log in with password</button>
        <button class="gbtn alt" id="m-signpw" type="button" data-step="s-signpw">{SVG('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>')}Sign up with email and password</button>
        <button class="gbtn alt" id="m-email" type="button" data-step="s-email">{SVG('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>')}Continue with email</button>
      </div>
      <p class="meta" id="switch" style="margin:18px 0 0"></p>
    </div>
    <p class="meta" style="margin:14px 0 0">Need help? <a data-wa="Hi SkillNavora, I need help logging in." href="contact.html">Contact support</a></p>
''')
page("login.html", "Log in · SkillNavora", "Log in to your SkillNavora learning dashboard.", login, "login.html", SB + '<script src="{r}assets/login.js"></script>', noindex=True, footer=False, wa=False, app=True)

reset = """<div class="auth-page"><div class="auth-card"><div class="logo"><img src="assets/logo-s.svg" alt=""><span><i class="c">S</i>kill<em><i class="c">N</i>avora</em></span></div><h1>Set a new password</h1>
  <p id="auth-msg" class="notice" hidden role="status" style="margin-top:16px;text-align:left"></p>
  <form id="f-reset" class="form"><label>New password <span class="meta">(at least 8 characters)</span><input name="password" type="password" required minlength="8" autocomplete="new-password"></label>
  <label>Confirm new password<input name="confirm" type="password" required minlength="8" autocomplete="new-password"></label><button type="submit">Save new password</button></form></div></div>"""
page("reset.html", "Reset password · SkillNavora", "Set a new password.", reset, None, SB + '<script src="{r}assets/reset.js"></script>', noindex=True, footer=False, wa=False, app=True)

# Old dashboard links (e.g. in emails) go to the LMS.
page("dashboard.html", "SkillNavora LMS", "Redirecting to your LMS.", '<section><div class="wrap"><p>Taking you to your LMS… <a href="lms.html">Continue</a></p></div></section><script>location.replace("lms.html"+location.search)</script>', None, noindex=True, footer=False, wa=False, app=True)

lms = f"""<div class="lms-head"><div class="wrap">
  <div><div class="kicker" style="color:#c9bdff">My learning</div><h1 id="hello">Welcome!</h1><p>Your courses, live events, submissions and achievements in one place.</p>
    <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap"><a class="btn btn-ghost btn-sm" id="to-admin" href="admin.html" hidden>Admin panel</a><button class="btn btn-ghost btn-sm" data-signout type="button">Log out</button></div></div>
  <div class="milestone"><div><small>Achievements</small><span id="ring-text"></span></div><div id="ring"></div></div>
</div></div>
<section style="padding-top:26px"><div class="wrap">
  <p id="app-msg" class="notice" hidden role="status" style="margin-bottom:18px"></p>
  <div id="app" hidden>
    <div class="tabs" id="tabbar" role="tablist">
      <button role="tab" data-tab="overview">Overview</button><button role="tab" data-tab="courses">My courses</button><button role="tab" data-tab="handbook">PM Handbook</button><button role="tab" data-tab="resources">Resources &amp; AI tools</button><button role="tab" data-tab="events">My events</button>
      <button role="tab" data-tab="submissions">Submissions</button><button role="tab" data-tab="achievements">Achievements</button><button role="tab" data-tab="profile">Profile</button>
    </div>

    <div class="panel" id="p-overview">
      <div class="dgrid"><div class="col">
        <div><h2 class="h2s">Continue learning</h2><div class="list" id="ov-continue"></div></div>
        <div><h2 class="h2s">Upcoming events</h2><div class="list" id="ov-events"></div></div>
      </div><div class="col">
        <div class="card"><h3 class="h3s">Announcements</h3><div class="list" id="ov-news"></div></div>
        <div class="card hirecard"><span class="hc-ico">🤝</span><div><h3 class="h3s" style="margin:0 0 4px">Is your company hiring?</h3><p class="meta" style="margin:0 0 10px">Let us know and we'll send across the best profiles!</p><a class="btn btn-line btn-sm" href="hire.html">Get in touch →</a></div></div>
        <div class="card hirecard"><span class="hc-ico">🎁</span><div><h3 class="h3s" style="margin:0 0 4px">Refer &amp; earn</h3><p class="meta" style="margin:0 0 10px">Refer a friend or a candidate and earn a reward.</p><a class="btn btn-line btn-sm" href="refer.html">Refer now →</a></div></div>
        <div class="card"><h3 class="h3s">Need help?</h3>
          <form id="f-help" class="form"><label>Topic<select name="topic"><option>Book a 1:1 session</option><option>Resume or portfolio review</option><option>Mock interview</option><option>Help with an assignment</option><option>Something else</option></select></label>
          <label>Message<textarea name="message" required maxlength="4000" placeholder="What do you need, and when suits you?"></textarea></label><button class="btn btn-primary btn-sm" type="submit">Send request</button><p id="rq-msg" class="notice" hidden role="status"></p></form>
          <div class="list" id="rq-list" style="margin-top:14px"></div></div>
      </div></div>
      <h2 class="h2s" style="margin-top:40px">Our flagship programs</h2><div class="courses" id="ov-courses"></div>
    </div>

    <div class="panel" id="p-courses" hidden><h2 class="h2s">My courses</h2><div class="grid g2" id="mc-list"></div>
      <h2 class="h2s" style="margin-top:40px">Explore more programs</h2><div class="courses" id="mc-all"></div></div>

{HB_PANEL}{LMS_RES}    <div class="panel" id="p-events" hidden><h2 class="h2s">Upcoming</h2><div class="events" id="ev-up"></div><h2 class="h2s" style="margin-top:40px">Completed</h2><div class="events" id="ev-done"></div></div>

    <div class="panel" id="p-submissions" hidden><div class="dgrid">
      <div class="card"><h3 class="h3s">Submit your work</h3>
        <form id="f-submit" class="form"><label>For<select name="target"></select></label>
          <label>Title<input name="title" required maxlength="200" placeholder="e.g. UPI onboarding teardown"></label>
          <label>Link to your work<input name="link" type="url" required placeholder="https://… (Google Drive, Figma, GitHub, Notion)"></label>
          <label>Notes <span class="meta">(optional)</span><textarea name="notes" maxlength="4000" placeholder="What would you like feedback on?"></textarea></label>
          <button class="btn btn-primary" type="submit">Submit for review</button><p id="s-msg" class="notice" hidden role="status"></p></form>
        <p class="meta" style="margin:14px 0 0">Looking for something to work on? Try the <a href="challenges.html">free challenges</a>.</p></div>
      <div><h3 class="h3s">My submissions</h3><div class="list" id="s-list"></div></div>
    </div></div>

    <div class="panel" id="p-achievements" hidden><h2 class="h2s">Achievements</h2><p class="meta" style="margin:-8px 0 22px">Stand out by earning badges as you reach milestones.</p><div class="badges" id="ach"></div>
      <h2 class="h2s" style="margin-top:40px">Quiz scores</h2><div class="list" id="ach-quiz" style="max-width:640px"></div></div>

    <div class="panel" id="p-profile" hidden><div class="card" style="max-width:640px"><h3 class="h3s">My profile</h3>
      <form id="f-profile" class="form"><label>Full name<input name="full_name" maxlength="120" autocomplete="name"></label><label>Email<input name="email" disabled></label>
        <label>Phone or WhatsApp<input name="phone" maxlength="30" autocomplete="tel"></label><label>LinkedIn<input name="linkedin" maxlength="300" placeholder="https://www.linkedin.com/in/…"></label>
        <label>My goal<textarea name="goal" maxlength="1000" placeholder="e.g. Move into an AI PM role in 6 months"></textarea></label><button class="btn btn-primary" type="submit">Save profile</button><p id="pf-msg" class="notice" hidden role="status"></p></form></div></div>
  </div>

  <div id="course-view" hidden>
    <button class="btn btn-line btn-sm" id="cv-back" type="button">← My courses</button>
    <h1 id="cv-name" style="font-size:clamp(26px,3.6vw,36px);margin:20px 0 14px"></h1><div id="cv-prog" style="max-width:520px;margin-bottom:26px"></div>
    <div class="mods cmods" id="cv-mods"></div>
  </div>
</div></section>"""
page("lms.html", "My learning · SkillNavora", "Your SkillNavora LMS.", lms, "lms.html", '<script src="{r}assets/content.js"></script>' + SB + '<script src="{r}assets/lms.js"></script>', noindex=True, app=True)

admin = f"""<div class="lms-head"><div class="wrap"><div><div class="kicker" style="color:#c9bdff">Admin</div><h1>Admin panel</h1><p>Manage students, courses, events and reviews.</p></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn btn-ghost btn-sm" id="refresh" type="button">Refresh</button><a class="btn btn-ghost btn-sm" href="lms.html">My LMS</a><button class="btn btn-ghost btn-sm" data-signout type="button">Log out</button></div></div></div>
<section style="padding-top:26px"><div class="wrap">
  <p id="app-msg" class="notice" hidden role="status" style="margin-bottom:18px"></p>
  <div id="denied" class="card" hidden><h3 class="h3s">You don't have admin access yet</h3><p>You're signed in as <b id="denied-email"></b>, which is a student account.</p>
    <p class="meta" style="margin:0 0 8px">To make this account an admin, open your Supabase project → <b>SQL Editor</b> → <b>New query</b>, paste this, click <b>Run</b>, then click <b>Refresh</b> above:</p>
    <pre class="tpl" id="denied-sql" style="white-space:pre-wrap"></pre>
    <button class="btn btn-line btn-sm" type="button" onclick="navigator.clipboard.writeText(document.getElementById('denied-sql').innerText).then(()=>this.textContent='Copied ✓')">Copy SQL</button>
    <p class="meta" style="margin:14px 0 0">Signed in with the wrong account? Use <b>Log out</b> above and log in with your admin email. Or go to <a href="lms.html">your LMS</a>.</p></div>
  <div id="app" hidden>
    <div class="tabs" role="tablist">
      <button role="tab" data-tab="overview">Overview</button><button role="tab" data-tab="students">Students</button><button role="tab" data-tab="enrol">Enrolments</button><button role="tab" data-tab="materials">Course materials</button>
      <button role="tab" data-tab="subs">Submissions<span class="n" id="n-subs" hidden></span></button><button role="tab" data-tab="events">Events</button>
      <button role="tab" data-tab="apps">Applications<span class="n" id="n-apps" hidden></span></button><button role="tab" data-tab="reqs">Requests<span class="n" id="n-reqs" hidden></span></button><button role="tab" data-tab="jobs">Job board</button><button role="tab" data-tab="news">Announcements</button><button role="tab" data-tab="admins">Admins</button><button role="tab" data-tab="health">Site check</button>
    </div>
    <div class="panel" id="p-overview">
      <div class="statrow"><div class="card stat"><small>Students</small><b id="o-students">0</b></div><div class="card stat"><small>Enrolments</small><b id="o-enr">0</b></div><div class="card stat"><small>Awaiting review</small><b id="o-waiting">0</b></div><div class="card stat"><small>Open requests</small><b id="o-open">0</b></div><div class="card stat"><small>New applications</small><b id="o-apps">0</b></div></div>
      <div class="dgrid"><div class="card table-wrap"><h3 class="h3s">Programs</h3><table class="tbl" style="min-width:480px"><thead><tr><th>Program</th><th>Students</th><th>Materials</th><th>Submissions</th></tr></thead><tbody id="o-courses"></tbody></table></div>
        <div class="card"><h3 class="h3s">Upcoming events: <span id="o-events">0</span></h3><ul class="checks"><li>Enrol paid students in <b>Enrolments</b>.</li><li>Add recordings and slides in <b>Course materials</b> after each class.</li><li>Review new work in <b>Submissions</b>.</li><li>Schedule live sessions in <b>Events</b>.</li></ul></div></div>
    </div>
    <div class="panel" id="p-students" hidden><div class="card"><label style="max-width:360px;margin-bottom:14px">Search<input id="st-q" type="search" placeholder="Name, email, phone or goal"></label>
      <div class="table-wrap"><table class="tbl"><thead><tr><th>Name</th><th>Contact</th><th>Goal</th><th>Progress</th><th>Submissions</th><th>Joined</th></tr></thead><tbody id="st-rows"></tbody></table></div></div></div>
    <div class="panel" id="p-enrol" hidden><div class="card" style="margin-bottom:20px"><h3 class="h3s">Enrol a student</h3><p class="meta" style="margin:-6px 0 14px">They need to create an account first. Enrolled students get the course, its materials and assignments in their LMS.</p>
      <form id="f-enrol" class="form"><div class="row2"><label>Student's account email<input name="email" type="email" required></label><label>Program<select name="course" data-courses></select></label></div><button class="btn btn-primary" type="submit" style="align-self:flex-start">Enrol student</button><p id="en-msg" class="notice" hidden role="status"></p></form></div>
      <div class="card table-wrap"><table class="tbl"><thead><tr><th>Student</th><th>Program</th><th>Status</th><th>Since</th><th></th></tr></thead><tbody id="en-rows"></tbody></table></div></div>
    <div class="panel" id="p-materials" hidden><div class="dgrid"><div class="card"><h3 class="h3s">Add a recording, slides or link</h3>
      <form id="f-mat" class="form"><label>Program<select name="course" data-courses></select></label><label>Module<select name="module"></select></label>
        <div class="row2"><label>Type<select name="kind"><option value="recording">Recording</option><option value="slides">Slides</option><option value="reading">Reading</option><option value="assignment">Assignment brief</option><option value="link">Other link</option><option value="preread">Pre-course material</option></select></label><label>Title<input name="title" required maxlength="200" placeholder="e.g. Class 3 recording"></label></div>
        <label>Link<input name="url" type="url" required placeholder="https://… (YouTube unlisted, Google Drive, Notion)"></label><button class="btn btn-primary" type="submit">Add to course</button><p id="mat-msg" class="notice" hidden role="status"></p></form>
      <p class="meta" style="margin:14px 0 0">Only students enrolled in the program can see these links. For private videos, use links that require sign-in (e.g. Google Drive shared with the student) or unlisted videos.</p></div>
      <div><h3 class="h3s">Materials in this program</h3><div class="list" id="mat-list"></div></div></div></div>
    <div class="panel" id="p-subs" hidden><div class="card"><label style="max-width:300px;margin-bottom:14px">Show<select id="sub-filter"><option value="submitted">Awaiting review</option><option value="needs_changes">Needs changes</option><option value="reviewed">Reviewed</option><option value="all">All</option></select></label><div class="list" id="sub-list"></div></div></div>
    <div class="panel" id="p-events" hidden><div class="dgrid"><div class="card"><h3 class="h3s">Create an event</h3>
      <form id="f-event" class="form"><label>Title<input name="title" required maxlength="200" placeholder="e.g. Build agentic workflows with n8n"></label><label>Description<textarea name="description" maxlength="4000"></textarea></label>
        <div class="row2"><label>Starts<input name="starts" type="datetime-local" required></label><label>Ends<input name="ends" type="datetime-local"></label></div>
        <label>Join link <span class="meta">(Google Meet, Zoom)</span><input name="join_url" type="url" placeholder="https://meet.google.com/…"></label><button class="btn btn-primary" type="submit">Create event</button><p id="ev-msg" class="notice" hidden role="status"></p></form></div>
      <div><h3 class="h3s">All events</h3><div class="list" id="ev-list"></div></div></div></div>
    <div class="panel" id="p-apps" hidden><div class="card"><div class="row2" style="max-width:520px;margin-bottom:14px"><label>Type<select id="app-kind"><option value="all">All</option><option value="application">Applications</option><option value="counselling">Counselling calls</option><option value="mentor">Mentor applications</option><option value="career">Careers applications</option><option value="contact">Contact form</option><option value="referral">Referrals</option><option value="hire">Hiring enquiries</option><option value="resource">Resource access (handbook / PDF visitors)</option></select></label><label>Status<select id="app-status"><option value="new">New</option><option value="contacted">Contacted</option><option value="enrolled">Enrolled</option><option value="closed">Closed</option><option value="all">All</option></select></label></div><div class="list" id="app-list"></div></div></div>
    <div class="panel" id="p-jobs" hidden><div class="dgrid"><div class="card"><h3 class="h3s">Add a job</h3><p class="meta" style="margin:-6px 0 14px">Paste openings from LinkedIn or company career pages. They appear on the public Job board.</p>
      <form id="f-job" class="form"><div class="row2"><label>Job title<input name="title" required maxlength="160" placeholder="e.g. Associate Product Manager"></label><label>Company<input name="company" required maxlength="120"></label></div>
        <div class="row2"><label>Location<input name="location" maxlength="120" placeholder="Bengaluru, India"></label><label>Category<select name="category"><option value="product">Product</option><option value="ai">AI</option><option value="data">Data Engineering</option></select></label></div>
        <div class="row2"><label>Experience<input name="experience" maxlength="40" placeholder="e.g. 0-2 years"></label><label>Type<select name="job_type"><option>Full time</option><option>Internship</option><option>Contract</option><option>Remote</option></select></label></div>
        <label>Job link<input name="url" type="url" required placeholder="https://www.linkedin.com/jobs/view/…"></label><label>Company logo link <span class="meta">(optional)</span><input name="logo" type="url" placeholder="https://…/logo.png"></label>
        <button class="btn btn-primary" type="submit">Add job</button><p id="job-msg" class="notice" hidden role="status"></p></form></div>
      <div><h3 class="h3s">All jobs</h3><div class="list" id="job-rows"></div></div></div></div>
    <div class="panel" id="p-reqs" hidden><div class="card"><label style="max-width:300px;margin-bottom:14px">Show<select id="req-filter"><option value="open">Open</option><option value="done">Done</option><option value="all">All</option></select></label><div class="list" id="req-list"></div></div></div>
    <div class="panel" id="p-news" hidden><div class="dgrid"><div class="card"><h3 class="h3s">Post an announcement</h3><form id="f-news" class="form"><label>Title<input name="title" required maxlength="200"></label><label>Message<textarea name="body" required maxlength="8000"></textarea></label><button class="btn btn-primary" type="submit">Post to all students</button><p id="news-msg" class="notice" hidden role="status"></p></form></div><div><h3 class="h3s">Posted</h3><div class="list" id="news-list"></div></div></div></div>
    <div class="panel" id="p-admins" hidden><div class="dgrid"><div class="card"><h3 class="h3s">Give or remove admin access</h3><p class="meta" style="margin:-6px 0 14px">Admins can see every student's details and work.</p>
      <form id="f-role" class="form"><label>Their account email<input name="email" type="email" required></label><label>Make them<select name="role"><option value="admin">Admin</option><option value="student">Student (remove admin)</option></select></label><button class="btn btn-primary" type="submit">Save</button><p id="role-msg" class="notice" hidden role="status"></p></form></div>
      <div><h3 class="h3s">Current admins</h3><div class="list" id="adm-list"></div></div></div></div>
    <div class="panel" id="p-health" hidden><div class="card"><h3 class="h3s">Site check</h3>
      <p class="meta" style="margin:-6px 0 14px">Tests every page, handbook PDF, class file and form on skillnavora.in from your browser, and counts handbook visitors. While you are signed in as an admin, the visitor details form is skipped for you on every page, so your own visits are not counted. Visitors still fill it once.</p>
      <div class="acts" style="margin-bottom:14px"><button class="btn btn-primary btn-sm" type="button" id="hc-run">Run site check</button></div>
      <div id="hc-sum" class="dgrid"></div><div class="list" id="hc-list" style="margin-top:14px"></div>
      <script type="application/json" id="hc-urls">{{HEALTH_URLS}}</script></div></div>
  </div>
</div></section>"""
def _health_urls():
    import glob as _g, json as _js
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pages = ["index.html", "programs.html", "resources.html", "handbooks/index.html", "handbooks/pm/index.html", "data-science/index.html", "lms.html", "jobs.html", "blogs.html", "contact.html", "program/ai-data-engineering.html", "program/genai-launchpad.html", "program/ai-product-management.html"]
    pages += sorted(os.path.relpath(f, root) for f in _g.glob(root + "/data-science/lessons/*.html"))
    files = sorted(os.path.relpath(f, root) for pat in ("handbook/*.pdf", "handbooks/genai/*.pdf", "brochures/*.pdf", "classes/*.pdf", "data-science/pdf/**/*.pdf", "data-science/files/**/*.xlsx", "data-science/datasets/**/*.csv") for f in _g.glob(root + "/" + pat, recursive=True))
    return _js.dumps({"pages": pages, "files": files}).replace("</", "<\\/")
admin = admin.replace("{HEALTH_URLS}", _health_urls())
page("admin.html", "Admin · SkillNavora", "SkillNavora admin panel.", admin, "admin.html", '<script src="{r}assets/content.js"></script>' + SB + '<script src="{r}assets/admin.js"></script>', noindex=True, wa=False, app=True)

# ================================================================ APPLY + JOB BOARD
EXP = [("0 – 1 year", "Student / Fresher"), ("1 – 3 years", "Early career"), ("3 – 5 years", "Mid level"), ("5 – 8 years", "Senior"), ("8 – 12 years", "Lead / Manager"), ("12+ years", "Leadership")]
ROLES = ["Student / Fresher", "Software engineer", "QA / Testing", "Data / Analytics", "Designer (UX/UI)", "Business analyst", "Product / Project manager", "Sales / Marketing", "Operations / Customer success", "Consulting", "Founder / Entrepreneur", "Other"]
apply = f"""<div class="apply-wrap"><div class="wrap">
  <div class="apply-head"><span class="tag">Application</span><h1>Apply for the next cohort</h1><p id="apply-sub"></p><div class="ticks" id="apply-ticks"></div></div>
  <div class="apply-card">
    <form id="f-apply" class="form" novalidate>
      <label>Program<select name="course"></select></label>
      <div class="row2"><label><span class="req">First name</span><input name="first" required maxlength="80" autocomplete="given-name" placeholder="e.g. Ankit"></label><label><span class="req">Last name</span><input name="last" required maxlength="80" autocomplete="family-name" placeholder="e.g. Sharma"></label></div>
      <div class="row2"><label><span class="req">Email address</span><input name="email" type="email" required maxlength="200" autocomplete="email" placeholder="you@gmail.com"></label>
        <label><span class="req">Contact number</span><span class="phone"><select name="cc" aria-label="Country code"><option value="+91">🇮🇳 +91</option><option value="+971">🇦🇪 +971</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option><option value="+65">🇸🇬 +65</option></select><input name="phone" required inputmode="tel" maxlength="15" autocomplete="tel-national" placeholder="98765 43210"></span></label></div>
      <label>LinkedIn profile URL<input name="linkedin" type="url" maxlength="300" placeholder="https://linkedin.com/in/yourprofile"></label>
      <fieldset><legend><span class="req">Your experience</span></legend><div class="exp">{''.join(f'<label><input type="radio" name="exp" value="{E(a)}"><span>{E(a)}<small>{E(b)}</small></span></label>' for a, b in EXP)}</div></fieldset>
      <label><span class="req">What best describes your most recent role?</span><select name="role" required><option value="">Select a role</option>{''.join(f'<option>{E(x)}</option>' for x in ROLES)}</select></label>
      <label>Why do you want to join this program?<textarea name="why" maxlength="2000" placeholder="Tell us about your goals and what you hope to achieve…"></textarea></label>
      <p id="apply-msg" class="notice" hidden role="status"></p>
      <button class="btn submit" type="submit">Submit application</button>
      <p class="meta center" style="margin:0">By applying you agree to our <a href="terms.html">terms</a> and <a href="privacy.html">privacy policy</a>. We'll never share your details.</p>
    </form>
    <div id="apply-done" class="done-box" hidden><div class="big">🎉</div><h2 class="sec-h" style="font-size:26px">Application received!</h2>
      <p class="meta">Thank you. A counsellor will call you soon to understand your goals and share the next steps, the schedule and scholarship options.</p>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:18px"><a class="btn btn-primary" data-pay href="#" target="_blank" rel="noopener" hidden>Reserve your seat (pay now) →</a><a class="btn btn-line" data-wa2 href="#" target="_blank" rel="noopener">Message us on WhatsApp</a><a class="btn btn-line" href="quiz.html">Try a free quiz</a></div></div>
  </div>
</div></div>"""
page("apply.html", "Apply for the next cohort · SkillNavora", "Apply for SkillNavora's AI-First Product Management, AI-First Data Engineer or GenAI Launchpad cohort.", apply, "apply.html")

jobs = f"""<div class="hero"><div class="wrap jobs-head"><div class="kicker">Job board</div><h1>Open <span class="g">roles</span></h1>
  <p class="lead" style="margin-bottom:0">A curated feed of product, AI and data engineering openings at top companies, sourced from LinkedIn and company career pages.</p>
  <div class="jobs-search">{SVG('<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>')}<input id="job-q" type="search" placeholder="Search by role, company or location…" aria-label="Search jobs"></div>
  <a class="alert-pill" id="job-alerts" href="#" target="_blank" rel="noopener">🔔 Get regular updates about new openings →</a>
</div></div>
<section style="padding-top:36px"><div class="wrap">
  <div class="center"><div class="seg2" id="job-tabs" role="group" aria-label="Category"></div></div>
  <div class="jobs-bar"><div><h2 id="job-count">Openings</h2><p class="meta" style="margin:4px 0 0">An open list of roles at companies hiring now. Clicking a job opens the original post.</p></div>
    <div class="filters2"><select id="job-exp" aria-label="Experience"></select><select id="job-loc" aria-label="Location"></select></div></div>
  <div class="jobs-grid" id="job-list"></div>
  <p class="empty" id="job-empty" hidden style="margin-top:18px">No matching openings here yet. Try another filter, or use the LinkedIn searches below.</p>
  <h2 class="sec-h" style="font-size:24px;margin-top:48px">More on LinkedIn</h2><p class="meta" style="margin:0 0 14px">Fresh openings from the last 7 days in India. Opens LinkedIn in a new tab.</p>
  <div class="li-links" id="li-searches"></div>
  <div class="portals card" id="portals-box">
    <div class="portals-h"><div><h2 class="sec-h" style="font-size:24px;margin:0">Search every job portal</h2><p class="meta" style="margin:6px 0 0">Type a role once and open live results on LinkedIn and other top job sites. Anyone can view these jobs; each site opens in a new tab.</p></div>
      <form id="portal-f" class="portal-f"><input id="portal-q" aria-label="Role to search" placeholder="e.g. Product Manager"><select id="portal-loc" aria-label="Location"><option>India</option><option>Bengaluru</option><option>Mumbai</option><option>Delhi NCR</option><option>Hyderabad</option><option>Pune</option><option>Chennai</option><option>Remote</option></select></form></div>
    <div class="portal-grid" id="portal-list"></div>
  </div>
  <div style="margin-top:28px">{restabs.portals_html()}</div>
</div></section>
{band("Want to be job-ready for these roles?", "Our job assistance program helps with your resume, portfolio, interview preparation and referrals.", '<a class="btn btn-primary" href="programs.html">Explore programs →</a><a class="btn btn-ghost" data-counsel href="#counselling">Talk to a counsellor</a>')}"""
page("jobs.html", "Job board · PM and AI jobs · SkillNavora", "Curated product manager, AI and data engineering jobs in India, with quick LinkedIn searches for the latest openings.", jobs, "jobs.html", '<script src="{r}assets/jobs.js"></script>')

# ================================================================ EVENTS, REVIEWS, BUSINESS
ev = uhero("Events", 'Live <span class="g">events</span> and workshops', "Free masterclasses, build-along workshops and demo days. Register to get the joining link.") + """
<section><div class="wrap"><h2 class="sec-h" style="font-size:28px">Upcoming</h2><div class="events" id="pub-events" style="margin-top:22px"></div>
<h2 class="sec-h" style="font-size:28px;margin-top:56px">Past events</h2><div class="events" id="pub-past" style="margin-top:22px"></div></div></section>""" + band("Never miss a session", "Learners get every live class, workshop and demo day in their LMS, with recordings.", '<a class="btn btn-primary" href="programs.html">Explore programs →</a><a class="btn btn-ghost" data-wa="Hi SkillNavora, please tell me about upcoming events." href="#">Get event updates</a>')
page("events.html", "Events · SkillNavora", "Free live events, workshops and masterclasses on AI, product management and data engineering.", ev, "events.html")

# ================================================================ MENTOR + CAREERS
CC_OPTS = '<option value="+91">🇮🇳 +91</option><option value="+971">🇦🇪 +971</option><option value="+1">🇺🇸 +1</option><option value="+44">🇬🇧 +44</option><option value="+65">🇸🇬 +65</option>'
def lead_form(kind, title, role_label, roles, exp_opts, msg_label, msg_ph, extra_label, extra_ph, button, done_h, done_p):
    return f"""<div class="apply-card" id="{kind}-form">
    <form class="form" data-lead="{kind}" novalidate>
      <h2 class="sec-h" style="font-size:24px;margin:0 0 4px">{title}</h2>
      <div class="row2"><label><span class="req">Full name</span><input name="name" required maxlength="80" autocomplete="name" placeholder="e.g. Priya Sharma"></label>
        <label><span class="req">Email address</span><input name="email" type="email" required maxlength="200" autocomplete="email" placeholder="you@gmail.com"></label></div>
      <div class="row2"><label><span class="req">Contact number</span><span class="phone"><select name="cc" aria-label="Country code">{CC_OPTS}</select><input name="phone" required inputmode="tel" maxlength="15" autocomplete="tel-national" placeholder="98765 43210"></span></label>
        <label><span class="req">LinkedIn profile URL</span><input name="linkedin" type="url" required maxlength="300" placeholder="https://linkedin.com/in/yourprofile"></label></div>
      <div class="row2"><label><span class="req">{role_label}</span><select name="role" required><option value="">Select</option>{''.join(f'<option>{E(x)}</option>' for x in roles)}</select></label>
        <label><span class="req">Years of experience</span><select name="experience" required><option value="">Select</option>{''.join(f'<option>{E(x)}</option>' for x in exp_opts)}</select></label></div>
      <label>{extra_label}<input name="extra" maxlength="200" placeholder="{extra_ph}"></label>
      <label>{msg_label}<textarea name="message" maxlength="1500" placeholder="{msg_ph}"></textarea></label>
      <p class="notice" data-lead-msg hidden role="status"></p>
      <button class="btn submit" type="submit">{button}</button>
      <p class="meta center" style="margin:0">By submitting you agree to our <a href="privacy.html">privacy policy</a>. We'll never share your details.</p>
    </form>
    <div class="done-box" data-lead-done hidden><div class="big">🎉</div><h2 class="sec-h" style="font-size:26px">{done_h}</h2><p class="meta">{done_p}</p></div>
  </div>"""

EXP_YRS = ["0–1 years", "1–3 years", "3–5 years", "5–8 years", "8–12 years", "12+ years"]
M_WHY = '''<div class="grid g4">
  <div class="card"><h3>Shape careers</h3><p>Help career switchers, freshers and working professionals land their next role.</p></div>
  <div class="card"><h3>Flexible time</h3><p>Choose how you help and how many hours a month you can give, around your job.</p></div>
  <div class="card"><h3>Build your brand</h3><p>A mentor profile on SkillNavora and features across our sessions and social channels.</p></div>
  <div class="card"><h3>A network of leaders</h3><p>Meet product, engineering and AI leaders who mentor alongside you.</p></div></div>'''
M_WAYS = '''<div class="grid g3">
  <div class="card"><h3>1:1 mentorship</h3><p>Monthly calls with a small group of learners to review progress, portfolios and career plans.</p></div>
  <div class="card"><h3>Mock interviews</h3><p>Run product sense, metrics, strategy or system design mock interviews with feedback.</p></div>
  <div class="card"><h3>Guest sessions</h3><p>Lead a live masterclass or a free workshop on a topic you know well.</p></div>
  <div class="card"><h3>Assignment and case reviews</h3><p>Give written feedback on case studies, PRDs and assignments.</p></div>
  <div class="card"><h3>Capstone judging</h3><p>Join demo days and help judge the AI products learners build.</p></div>
  <div class="card"><h3>Curriculum input</h3><p>Help keep modules current with how teams really work today.</p></div></div>'''
M_FORM = lead_form("mentor", "Apply to be a mentor", "Your area of expertise", ["Product management", "AI product management", "Data engineering", "AI / machine learning", "Design / UX", "Data and analytics", "Growth and marketing", "Leadership and careers", "Other"], EXP_YRS[2:], "What would you like to mentor on?", "Topics, companies you've worked at, and how you'd like to help…", "Current role and company", "e.g. Senior PM at a fintech company", "Submit mentor application", "Thanks for applying!", "We'll review your profile and reach out within a few days to set up an intro call.")
mentor = uhero("Become a mentor", 'Mentor the next generation of <span class="g">AI-first builders</span>', "Share what you've learnt building products, and help learners grow into confident product managers, engineers and AI builders.") + f"""
{sec("Why mentor with us", "Give back, and grow while you do it", "", M_WHY)}
{sec("Ways to mentor", "Pick what suits you", "", M_WAYS, cls="tint")}
<section id="apply-mentor"><div class="wrap mgrid">
  <div><div class="kicker">Who we're looking for</div><h2 class="sec-h">You'd be a great fit if you</h2>
    <ul class="checks" style="margin:18px 0 28px"><li>Have 4+ years in product management, engineering, design, data or AI</li><li>Have shipped products people use, at a startup or a large company</li><li>Enjoy explaining ideas simply and giving honest, kind feedback</li><li>Can give at least a few hours a month</li></ul>
    <div class="kicker">How it works</div>
    <ol class="mflow"><li><b>Apply</b><span>Fill in the form. It takes about 3 minutes.</span></li><li><b>Intro call</b><span>A 20-minute chat with our founder about your experience and how you'd like to help.</span></li><li><b>Trial session</b><span>Run one session or review with learners.</span></li><li><b>Start mentoring</b><span>Get your profile, schedule and learner group.</span></li></ol>
  </div>
  {M_FORM}
</div></section>"""
page("mentor.html", "Become a mentor · SkillNavora", "Mentor learners at SkillNavora: 1:1 mentorship, mock interviews, guest sessions and capstone reviews.", mentor, "mentor.html")

C_LIFE = '''<div class="grid g4">
  <div class="card"><h3>Learners first</h3><p>Every decision starts with what helps a learner get better and get hired.</p></div>
  <div class="card"><h3>Learn by doing</h3><p>We use the AI tools we teach, every day, and share what works.</p></div>
  <div class="card"><h3>Ownership</h3><p>Small team, real responsibility from week one.</p></div>
  <div class="card"><h3>Remote friendly</h3><p>Work with us online, with flexible hours for most roles.</p></div></div>'''
C_FORM = lead_form("career", "Apply to join SkillNavora", "Team you'd like to join", ["Teaching assistant", "Curriculum and content", "Admissions and counselling", "Marketing and growth", "Engineering", "Operations", "Internship", "Other"], EXP_YRS, "Why do you want to join us?", "Tell us about yourself and what you'd love to work on…", "Resume or portfolio link", "Google Drive, Notion or website link", "Submit application", "Application received!", "Thank you for your interest. We'll get back to you if there's a good fit.")
careers = uhero("Careers", 'Build the future of <span class="g">learning with us</span>', "We're a small team helping people learn AI-first skills by doing. If you love teaching, building or helping people grow, we'd like to hear from you.") + f"""
{sec("Life at SkillNavora", "How we work", "", C_LIFE)}
<section class="tint" id="apply-career"><div class="wrap mgrid">
  <div><div class="kicker">Open roles</div><h2 class="sec-h">Teams we hire for</h2>
    <div id="open-roles" class="roles"></div>
    <p class="meta" id="roles-empty">We don't have specific openings listed right now, but we're always happy to meet great people. Send a general application and tell us where you'd like to help.</p>
    <div class="chips" style="margin-top:14px"><span>Teaching assistants</span><span>Curriculum and content</span><span>Admissions and counselling</span><span>Marketing and growth</span><span>Engineering</span><span>Operations</span><span>Internships</span></div>
  </div>
  {C_FORM}
</div></section>"""
page("careers.html", "Careers · SkillNavora", "Join SkillNavora: roles in teaching, curriculum, admissions, marketing, engineering and operations.", careers, "careers.html")


# ================================================================ BLOGS
import json as _json
POSTS = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "blogposts.json")))
os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)
_pcards = "".join(f"""<a class="card post" href="blog/{p['slug']}.html"><span class="ftag">Product management</span><h3>{E(p['title'])}</h3><p>{E(p['desc'])}</p><div class="fmeta"><span>Varun Kumar</span><span>{p['mins']} min read</span></div><span class="go">Read article →</span></a>""" for p in POSTS)
blogs = uhero("Blogs", 'Insights for <span class="g">AI-first careers</span>', "Practical guides on product management, AI tools and getting hired, by the SkillNavora team.") + f"""
<section style="padding-top:36px"><div class="wrap"><div class="grid g3">{_pcards}</div></div></section>""" + band("Want to go deeper?", "Get the free 570-page PM Master Handbook, or join a live program.", '<a class="btn btn-primary" href="resources.html">Free resources →</a><a class="btn btn-ghost" href="programs.html">Explore programs</a>')
page("blogs.html", "Blogs · SkillNavora", "Guides on product management, AI tools and PM interviews from SkillNavora.", blogs, "blogs.html")
for i, p in enumerate(POSTS):
    nxt = POSTS[(i + 1) % len(POSTS)]
    body = f"""<div class="hero"><div class="wrap" style="max-width:820px">
  <a class="pill" href="../blogs.html"><i></i><b>Blogs</b></a><h1 style="font-size:clamp(32px,4.6vw,48px);max-width:22ch">{E(p['title'])}</h1>
  <p class="lead">By Varun Kumar · {p['mins']} min read</p></div></div>
<section style="padding-top:44px"><div class="wrap"><article class="article prose" style="max-width:760px;margin:0 auto">{p['body']}
<div class="card" style="margin-top:40px;padding:24px"><div class="kicker">Next article</div><h3 style="margin:6px 0 10px"><a href="{nxt['slug']}.html" style="color:inherit">{E(nxt['title'])} →</a></h3><a class="btn btn-primary btn-sm" href="../programs.html">Explore programs</a></div>
</article></div></section>"""
    page(f"blog/{p['slug']}.html", f"{p['title']} · SkillNavora", p['desc'], body, f"blog/{p['slug']}.html")


# ================================================================ REFER & EARN / HIRE FROM US
def simple_form(kind, title, fields, button, done_h, done_p, label=""):
    return f"""<div class="apply-card" id="{kind}-form">
    <form class="form" data-lead="{kind}"{f' data-kind-label="{label}"' if label else ''} novalidate>
      <h2 class="sec-h" style="font-size:24px;margin:0 0 4px">{title}</h2>
      {fields}
      <p class="notice" data-lead-msg hidden role="status"></p>
      <button class="btn submit" type="submit">{button}</button>
      <p class="meta center" style="margin:0">By submitting you agree to our <a href="privacy.html">privacy policy</a>.</p>
    </form>
    <div class="done-box" data-lead-done hidden><div class="big">🎉</div><h2 class="sec-h" style="font-size:26px">{done_h}</h2><p class="meta">{done_p}</p></div>
  </div>"""
_you = f"""<div class="row2"><label><span class="req">Your name</span><input name="name" required maxlength="80" autocomplete="name"></label>
        <label><span class="req">Your email</span><input name="email" type="email" required maxlength="200" autocomplete="email"></label></div>
      <label><span class="req">Your phone / WhatsApp</span><span class="phone"><select name="cc" aria-label="Country code">{CC_OPTS}</select><input name="phone" required inputmode="tel" maxlength="15" autocomplete="tel-national"></span></label>"""
REF_FORM = simple_form("referral", "Refer someone", _you + """
      <label><span class="req">What are you referring?</span><select name="role" required><option value="">Select</option><option>A learner for a SkillNavora program</option><option>A candidate for a job opening</option><option>A company that's hiring</option></select></label>
      <label><span class="req">Their name, phone and email</span><input name="extra" required maxlength="200" placeholder="e.g. Rahul Mehta, +91 98765 43210, rahul@gmail.com"></label>
      <label>Their LinkedIn (optional)<input name="linkedin" type="url" maxlength="300" placeholder="https://linkedin.com/in/..."></label>
      <label>Anything we should know?<textarea name="message" maxlength="1500" placeholder="Which program or role, and why they'd be a great fit"></textarea></label>
      <label class="chk"><input type="checkbox" name="consent" required> The person I'm referring knows and is happy for SkillNavora to contact them</label>""",
  "Submit referral", "Thank you for the referral!", "We'll reach out to them and keep you posted on your reward.")
HIRE_FORM = simple_form("hire", "Is your company hiring? Get in touch", """<div class="row2"><label><span class="req">Name</span><input name="name" required maxlength="80" autocomplete="name"></label>
        <label><span class="req">Work email</span><input name="email" type="email" required maxlength="200" autocomplete="email"></label></div>
      <div class="row2"><label><span class="req">Phone number</span><span class="phone"><select name="cc" aria-label="Country code">""" + CC_OPTS + """</select><input name="phone" required inputmode="tel" maxlength="15" autocomplete="tel-national"></span></label>
        <label><span class="req">Name of your organisation</span><input name="extra" required maxlength="200" autocomplete="organization"></label></div>
      <div class="row2"><label><span class="req">Roles you're hiring for</span><select name="role" required><option value="">Select</option><option>Product manager / APM</option><option>Data engineer / analyst</option><option>AI / GenAI roles</option><option>Interns</option><option>Other</option></select></label>
        <label><span class="req">Number of openings</span><select name="experience" required><option value="">Select</option><option>1</option><option>2–5</option><option>6–10</option><option>10+</option></select></label></div>
      <label>Job description link (optional)<input name="linkedin" type="url" maxlength="300" placeholder="https://..."></label>
      <label>Anything else?<textarea name="message" maxlength="1500" placeholder="Location, experience level, timeline"></textarea></label>""",
  "Get in touch", "Thanks! We'll be in touch.", "Our team will share matching profiles within a few working days.")
REF_STEPS = [("Share a referral", "Tell us about a friend who wants to upskill, a candidate for a role, or a company that's hiring."),
             ("We take it from there", "Our team reaches out, counsels them and keeps you updated."),
             ("Get rewarded", "When your referral enrols or gets hired, you receive your reward by UPI or bank transfer.")]
refer = uhero("Refer & earn", 'Refer and <span class="g">earn rewards</span>', "Know someone who wants to grow their career, or a company that's hiring? Refer them to SkillNavora and earn a reward when it works out.") + f"""
<section><div class="wrap"><div class="grid g3">{''.join(f'<div class="card step2"><span class="num2">{i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(REF_STEPS))}</div></div></section>
<section class="tint"><div class="wrap">
  <div class="kicker">Ways to earn</div><h2 class="sec-h">Two ways to refer</h2>
  <div class="grid g2" style="margin-top:22px">
    <div class="card earn"><span class="ftag">Refer a learner</span><h3>Friends who want to upskill</h3><p>Refer someone to AI-First Product Management, AI-First Data Engineer or GenAI Launchpad.</p><b class="amt" data-reward="learner"></b></div>
    <div class="card earn"><span class="ftag">Refer a candidate</span><h3>People for open roles</h3><p>Refer a candidate for a role at one of our hiring partners. If they're hired, you earn a reward.</p><b class="amt" data-reward="hire"></b></div>
  </div></div></section>
<section id="refer-now"><div class="wrap mgrid">
  <div><div class="kicker">Refer now</div><h2 class="sec-h">It takes a minute</h2><ul class="checks" style="margin-top:16px"><li>No limit on how many people you refer</li><li>We only contact people who agree to it</li><li>Track your referral on WhatsApp or email</li></ul>
    <p class="meta" id="ref-terms" style="margin-top:18px"></p></div>
  {REF_FORM}
</div></section>"""
page("refer.html", "Refer & earn · SkillNavora", "Refer learners or candidates to SkillNavora and earn a reward.", refer, "refer.html")

hire = uhero("Hire from SkillNavora", 'Hire <span class="g">job-ready</span> talent', "Product managers, data engineers and AI professionals trained on real projects. Tell us what you need and we'll share matching profiles.") + f"""
<section><div class="wrap"><div class="grid g3">
  <div class="card"><h3>Pre-screened profiles</h3><p>Learners with portfolios, capstone projects and mock-interview feedback.</p></div>
  <div class="card"><h3>No hiring fee</h3><p>We help our learners find great roles. There's no fee for companies to hire them.</p></div>
  <div class="card"><h3>Fast shortlists</h3><p>Share a role and get a shortlist of matching profiles within a few working days.</p></div></div></div></section>
<section class="tint" id="hire-now"><div class="wrap mgrid">
  <div><div class="kicker">For companies</div><h2 class="sec-h">Is your company hiring?</h2><p class="sub">Let us know and we'll send across the best profiles for your roles: product, data engineering and AI.</p>
    <ul class="checks"><li>Product managers and APMs</li><li>Data engineers and analysts</li><li>GenAI and automation roles</li><li>Interns and freshers</li></ul></div>
  {HIRE_FORM}
</div></section>"""
page("hire.html", "Hire from SkillNavora", "Hire job-ready product, data engineering and AI talent from SkillNavora. No hiring fee.", hire, "hire.html")

rv = uhero("Testimonials and reviews", 'Careers that changed, <span class="g">in their own words.</span>', "Real stories from SkillNavora learners.") + """
<section><div class="wrap"><div class="reviews" id="reviews-wall"></div></div></section>
<section class="tint" id="share"><div class="wrap mgrid">
  <div><div class="kicker">Are you a SkillNavora learner?</div><h2 class="sec-h">Share your story</h2>
    <p class="sub">Tell us how the program helped you. With your permission, we'll feature your review here with your name, photo and role change.</p>
    <ul class="checks"><li>Your review is checked by our team before it appears</li><li>We only publish what you agree to</li><li>Add your LinkedIn so others can see your journey</li></ul></div>
  <div class="apply-card" id="review-form">
    <form class="form" data-lead="contact" data-kind-label="Learner review" novalidate>
      <h2 class="sec-h" style="font-size:24px;margin:0 0 4px">Write a review</h2>
      <div class="row2"><label><span class="req">Full name</span><input name="name" required maxlength="80" autocomplete="name"></label>
        <label><span class="req">Email address</span><input name="email" type="email" required maxlength="200" autocomplete="email"></label></div>
      <div class="row2"><label><span class="req">Contact number</span><span class="phone"><select name="cc" aria-label="Country code">""" + CC_OPTS + """</select><input name="phone" required inputmode="tel" maxlength="15" autocomplete="tel-national"></span></label>
        <label><span class="req">LinkedIn profile URL</span><input name="linkedin" type="url" required maxlength="300" placeholder="https://linkedin.com/in/yourprofile"></label></div>
      <div class="row2"><label><span class="req">Program</span><select name="role" required><option value="">Select</option><option>AI-First Product Management</option><option>AI-First Data Engineer</option><option>GenAI Launchpad</option></select></label>
        <label><span class="req">Role change</span><select name="experience" required><option value="">Select</option><option>Got a new role</option><option>Got promoted</option><option>Switched career</option><option>Still learning</option></select></label></div>
      <label>Before → after (role and company)<input name="extra" maxlength="200" placeholder="e.g. Business Analyst, Infosys → APM, Razorpay"></label>
      <label><span class="req">Your review</span><textarea name="message" required maxlength="1500" placeholder="What did you learn? What changed for you?"></textarea></label>
      <label class="chk"><input type="checkbox" name="consent" required> I agree to SkillNavora publishing this review with my name, photo and LinkedIn</label>
      <p class="notice" data-lead-msg hidden role="status"></p>
      <button class="btn submit" type="submit">Submit review</button>
    </form>
    <div class="done-box" data-lead-done hidden><div class="big">🙏</div><h2 class="sec-h" style="font-size:26px">Thank you!</h2><p class="meta">We'll review it and let you know before it goes live.</p></div>
  </div>
</div></section>""" + band("Start your own story", "Join a program, build a portfolio and get career support.", '<a class="btn btn-primary" href="programs.html">Explore programs →</a>')
page("reviews.html", "Reviews · SkillNavora", "Reviews and stories from SkillNavora learners.", rv, "reviews.html")

biz = uhero("For business", 'AI upskilling for <span class="g">your team</span>', "Practical, hands-on training that helps product, engineering and business teams use AI tools safely and productively.") + f"""
{sec("Training tracks", "Built around your team's work", "Every engagement is tailored to your tools, data policies and goals.", '''<div class="grid g3">
  <div class="card"><h3>GenAI for every team</h3><p>Prompting, AI assistants for daily work, automation and responsible AI use.</p></div>
  <div class="card"><h3>AI for product teams</h3><p>Discovery, PRDs, prototyping and shipping AI features with the right metrics and guardrails.</p></div>
  <div class="card"><h3>AI for engineering teams</h3><p>Coding agents, building with LLM APIs, RAG, agents and evaluation.</p></div>
</div>''')}
{sec("Formats", "Choose what fits", "", '''<div class="grid g3">
  <div class="card"><h3>Workshops</h3><p>Half-day or full-day hands-on sessions, online or on site.</p></div>
  <div class="card"><h3>Team cohorts</h3><p>Multi-week programs with assignments and a capstone on your own use case.</p></div>
  <div class="card"><h3>College programs</h3><p>Career-focused sessions for students in product, engineering and AI.</p></div>
</div>''', cls="tint")}
<section><div class="wrap cgrid">
  <div><div class="kicker">Talk to us</div><h2 class="sec-h">Plan training for your team</h2><p class="sub">Tell us about your team and goals, and we'll suggest a plan and pricing.</p><ul class="clist" id="clist"></ul></div>
  <form id="form" class="card form">
    <h3 style="font-size:20px">Enquire about team training</h3>
    <div class="row2"><label>Name<input name="name" required autocomplete="name"></label><label>Work email<input name="email" type="email" required autocomplete="email"></label></div>
    <div class="row2"><label>Company or college<input name="company" required autocomplete="organization"></label><label><span class="req">Phone / WhatsApp</span><input name="phone" required inputmode="tel" maxlength="20" autocomplete="tel" placeholder="+91 98765 43210"></label></div>
    <label>Interested in<select name="interest"><option>GenAI for every team</option><option>AI for product teams</option><option>AI for engineering teams</option><option>College program</option><option>Not sure yet</option></select></label>
    <label>Team size and goals<textarea name="message" required placeholder="e.g. 25 product managers, want to prototype with AI and write better PRDs"></textarea></label>
    <input type="checkbox" name="botcheck" hidden>
    <button class="btn btn-primary" type="submit">Send enquiry</button>
    <p class="meta" id="msg" aria-live="polite" style="margin:0"></p>
  </form>
</div></section>"""
page("business.html", "For business · SkillNavora", "AI upskilling workshops and team cohorts for product, engineering and business teams, and college programs.", biz, "business.html")

# ================================================================ POLICIES + 404
def policy(path, title, h, body):
    page(path, f"{title} · SkillNavora", f"SkillNavora {title.lower()}.", uhero("Policies", h, "Last updated: 23 October 2026") + f'<section><div class="wrap prose">{body}</div></section>', path)

policy("privacy.html", "Privacy policy", "Privacy policy", """
<h2>What we collect</h2><p>Information you give us: your name, email, phone and messages when you contact us, and your profile, course progress, submissions, quiz scores and event registrations when you use the LMS.</p>
<h2>How we use it</h2><p>To run your programs and LMS account, reply to you, review your work, send updates about your courses, and improve our programs. We don't sell or rent your information.</p>
<h2>Services we use</h2><ul><li>Cloudflare Pages hosts the website and may log basic technical data such as IP addresses for security.</li><li>Supabase stores LMS accounts and data. Passwords are handled by Supabase and never visible to us.</li><li>Google sign-in (if you use it), Web3Forms for contact-form messages, a scheduling tool for counselling calls, Google Fonts, and WhatsApp (Meta) when you message us. Each follows its own privacy policy.</li></ul>
<p>This site doesn't use advertising or tracking cookies. Your browser stores your login session and preferences such as light or dark mode.</p>
<h2>Your choices</h2><p>You can update your profile in the LMS, and ask us to export or delete your account and data by emailing <a data-email href="contact.html">us</a>.</p>""")
policy("terms.html", "Terms and conditions", "Terms and conditions", """
<h2>Using this website</h2><p>By using skillnavora.in and the SkillNavora LMS you agree to these terms. Please use the site lawfully and don't try to access accounts or data that aren't yours.</p>
<h2>Accounts</h2><p>Keep your login details private. You're responsible for activity on your account. We may suspend accounts that misuse the platform.</p>
<h2>Programs</h2><p>Program content, schedules and fees are described on each program page and confirmed in writing before you pay. We may update curricula to keep them current.</p>
<h2>Course material</h2><p>Recordings, slides and other materials are for your personal learning. Please don't share, sell or republish them.</p>
<h2>Your work</h2><p>You keep ownership of the projects you submit. You give us permission to review them and, only with your consent, to showcase them.</p>
<h2>Career support</h2><p>We help you prepare for jobs, but we can't guarantee interviews, offers or salaries.</p>
<h2>Contact</h2><p>Questions about these terms? <a href="contact.html">Contact us</a>.</p>""")
policy("refund.html", "Cancellation and refund policy", "Cancellation and refund policy", """
<p>Cancellation and refund terms for each program, including any deadlines and how refunds are paid, are shared in writing before you pay and apply to your enrolment.</p>
<h2>How to request a cancellation or refund</h2><p>Email us from the address you registered with, including your name, program and cohort, and the reason for your request. We reply within 3 working days.</p>
<h2>Free resources</h2><p>Quizzes, challenges, practice and resources are free and need no payment.</p>
<h2>Questions</h2><p><a href="contact.html">Contact us</a> before you enrol if you'd like to understand the terms for your program.</p>""")
# email links on policy pages
for p in ("privacy.html",):
    s = open(f"{OUT}/{p}").read().replace("</body>", '<script>document.querySelectorAll("[data-email]").forEach(a=>{if(SITE.email){a.href="mailto:"+SITE.email;a.textContent=SITE.email}})</script></body>')
    open(f"{OUT}/{p}", "w").write(s)

nf = uhero("Page not found", "This page took a wrong turn", "It may have moved. Try one of these instead.") + '<section><div class="wrap" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-line" href="/programs.html">Programs</a><a class="btn btn-line" href="/quiz.html">Quiz zone</a><a class="btn btn-line" href="/lms.html">LMS</a></div></section>'
page("404.html", "Page not found · SkillNavora", "Page not found.", nf)
s = open(f"{OUT}/404.html").read()
s = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:)([^"]+)"', r'\1="/\2"', s)
open(f"{OUT}/404.html", "w").write(s)

# ================================================================ cleanup + SEO
for old in ["blog.html", "case-studies.html", "mentoring.html", "assets/dashboard.js"]:
    if os.path.exists(f"{OUT}/{old}"): os.remove(f"{OUT}/{old}")
pass  # blog/ is generated by the BLOGS section
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{u}</loc><lastmod>2026-10-23</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print("\n".join(urls))
