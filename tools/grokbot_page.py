"""Renders the Grokbot Mastery Course (Markdown in Grokbot-Mastery-Course/) into one site page.

Used by gen_site.py: grokbot_page.body() returns the HTML for grokbot-course.html, and
tab_card() returns the card shown in the AI Skills Academy.
"""
import html
import os
import re

import markdown

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Grokbot-Mastery-Course")

# Reading order for the page. Each entry: (heading shown, path relative to ROOT).
ORDER = [
    ("Course overview: what Grokbot means", "01-Course-Overview.md"),
    ("Module 1: Introduction and AI fundamentals", "02-Foundations/module-01-introduction-and-ai-fundamentals.md"),
    ("Module 2: Platform architecture", "03-Platform-Architecture/module-02-platform-architecture.md"),
    ("Module 3: Tokens and token economics", "04-Tokens-and-Token-Economics/module-03-tokens-and-token-economics.md"),
    ("Module 4: Pricing and subscriptions", "05-Pricing-and-Subscriptions/module-04-pricing-subscriptions-and-fees.md"),
    ("Module 5: Prompt engineering", "06-Prompt-Engineering/module-05-prompt-engineering.md"),
    ("Module 6: API integration", "07-API-Development/module-06-api-integration-fundamentals.md"),
    ("Module 7: Chatbots and automation", "08-Chatbots-and-Automation/module-07-chatbots-and-automation.md"),
    ("Module 8: Agents and advanced workflows", "09-AI-Agents-and-Advanced-Workflows/module-08-agents-and-advanced-workflows.md"),
    ("Module 9: Business applications", "10-Business-Applications/module-09-business-applications.md"),
    ("Module 10: Production and security", "11-Production-and-Security/module-10-production-security-optimisation.md"),
    ("Capstone projects", "12-Capstone-Projects/capstone-projects.md"),
    ("Walkthrough: build a D2C agent team with Grok Bot", "15-Video-Walkthrough-D2C-Agent-Team/video-walkthrough-d2c-agent-team.md"),
    ("Exercises and final assessment", "13-Exercises-and-Assessments/final-assessment.md"),
    ("Glossary", "14-Glossary-and-References/glossary.md"),
    ("Pricing tables, references and verification checklist", "14-Glossary-and-References/references.md"),
]

STYLE = """<style>
.gm-toc{display:grid;gap:6px;margin:14px 0 26px;padding:0;list-style:none}
.gm-toc a{display:block;padding:10px 14px;border:1px solid #ddd;border-radius:8px;text-decoration:none;color:inherit}
.gm-doc h2{margin-top:34px;border-bottom:1px solid #e5e5e5;padding-bottom:6px}
.gm-doc h3{margin-top:22px}
.gm-doc,.gm-tw,.gm-doc *{min-width:0;box-sizing:border-box}
.gm-doc{width:100%;max-width:100%;overflow-wrap:anywhere}
.gm-tw{display:block;width:100%;max-width:100%;overflow-x:auto;margin:12px 0}
.gm-doc table{border-collapse:collapse;width:100%;min-width:0;font-size:14px}
.gm-doc th,.gm-doc td{border:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}
.gm-doc th{background:#f4f4f6}
.gm-doc pre{background:#0f1020;color:#e8e8f0;padding:12px;border-radius:8px;overflow-x:auto;font-size:13px;line-height:1.5}
.gm-doc code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.92em}
.gm-doc p code,.gm-doc li code,.gm-doc td code{background:#f1f1f5;padding:1px 4px;border-radius:4px}
.gm-doc blockquote{border-left:4px solid #6C4CF5;background:#f7f5ff;margin:14px 0;padding:8px 14px;border-radius:0 8px 8px 0}
.gm-note{background:#fff8e6;border:1px solid #f0d78c;padding:12px 14px;border-radius:8px;margin:16px 0}
</style>"""

INTRO = """<div class="gm-note"><b>Read first.</b> xAI's official pages could not be verified when this course was written.
Prices and product facts are labelled <b>[Third-party]</b>, <b>[General]</b>, <b>[Estimate]</b> or <b>[Unverified]</b>.
Confirm every price on xAI's pricing page before you budget. The token calculator and the offline code tests are checked;
the live API calls are not yet tested.</div>"""

EXTRA_LINKS = """<p>Code, calculator and tests: the <code>Grokbot-Mastery-Course/</code> folder in the SkillNavora repository
(<code>tools/token_cost_calculator.py</code>, <code>code/test_offline.py</code> and the chatbot, RAG, agent and monitoring examples).</p>"""


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _render(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        src = f.read()
    html_out = markdown.markdown(src, extensions=["tables", "fenced_code", "sane_lists"])
    # <https://...> autolinks show the full address as text; show the site name instead, opening in a new tab
    html_out = re.sub(r'<a href="(https?://([^"/]+)[^"]*)">\1</a>',
                      lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(2).removeprefix("www.")} ↗</a>', html_out)
    # wrap tables so wide ones scroll inside their own box instead of widening the phone page
    return html_out.replace("<table>", '<div class="gm-tw"><table>').replace("</table>", "</table></div>")


def body():
    sections, toc = [], []
    for heading, path in ORDER:
        sid = _slug(heading)
        toc.append(f'<li><a href="#{sid}">{html.escape(heading)}</a></li>')
        sections.append(f'<section id="{sid}" class="gm-doc"><h1>{html.escape(heading)}</h1>{_render(path)}</section>')
    return (STYLE + '<section><div class="wrap">' + INTRO + EXTRA_LINKS
            + '<h2 class="sec-h">Contents</h2><ol class="gm-toc">' + "".join(toc) + "</ol></div></section>"
            + '<section><div class="wrap">' + "".join(sections) + "</div></section>")


def tab_card(href="grokbot-course.html", icon_svg=""):
    return (f'<a class="ai-card" href="{href}"><span class="ic">{icon_svg}</span>'
            '<h3>Grokbot Mastery Course</h3><p>From zero to commercial AI solutions: what Grok Bot is, tokens and real API costs, '
            'prompting, API code, chatbots, agents, RAG, business cases, production and security, with three capstone projects.</p>'
            '<span class="go">Start the course →</span></a>')


if __name__ == "__main__":
    out = body()
    print(len(out), "characters;", out.count('class="gm-doc"'), "sections")
