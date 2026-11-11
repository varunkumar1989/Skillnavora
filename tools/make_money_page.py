"""Renders the 'Make Money with AI' course (Make-Money-AI-Course/make-money-ai-course.md).

body()            HTML for make-money-course.html (site page, uses the site's page() wrapper)
card()            one card linking to the course (used in Learning Platform, Master Freelancing, Tool tutorials)
section_html()    a full-width section holding the card (for pages that have no card grid of their own)
standalone_html() a self-contained printable document (for the PDF and the handbook)
"""
import html
import os
import re

import markdown

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Make-Money-AI-Course")
SRC = os.path.join(ROOT, "make-money-ai-course.md")
PAGE = "make-money-course.html"
PDF_NAME = "Make-Money-with-AI-Course.pdf"

STYLE = """<style>
.mm-doc h1{font-size:30px;margin:0 0 6px}
.mm-doc h2{margin-top:34px;border-bottom:1px solid #e5e5e5;padding-bottom:6px}
.mm-doc h3{margin-top:26px}
.mm-tw{display:block;width:100%;max-width:100%;overflow-x:auto;margin:12px 0}
.mm-doc table{border-collapse:collapse;width:100%;min-width:0;font-size:14px}
.mm-doc th,.mm-doc td{border:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}
.mm-doc th{background:#f4f4f6}
.mm-doc pre{background:#0f1020;color:#e8e8f0;padding:12px;border-radius:8px;overflow-x:auto;font-size:13px}
.mm-doc code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.92em}
.mm-doc p code,.mm-doc li code,.mm-doc td code{background:#f1f1f5;padding:1px 4px;border-radius:4px}
.mm-doc blockquote{border-left:4px solid #0f8f7c;background:#eefaf7;margin:14px 0;padding:8px 14px;border-radius:0 8px 8px 0}
.mm-doc hr{border:0;border-top:1px solid #e5e5e5;margin:28px 0}
.mm-doc,.mm-tw,.mm-doc *{min-width:0;box-sizing:border-box}
.mm-doc{width:100%;max-width:100%;overflow-wrap:anywhere}
.mm-toc{display:grid;gap:6px;margin:14px 0 26px;padding:0;list-style:none}
.mm-toc a{display:block;padding:10px 14px;border:1px solid #ddd;border-radius:8px;text-decoration:none;color:inherit}
.mm-note{background:#fff8e6;border:1px solid #f0d78c;padding:12px 14px;border-radius:8px;margin:16px 0}
</style>"""


def _read():
    with open(SRC, encoding="utf-8") as f:
        return f.read()


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _md(src):
    # Python-Markdown needs a blank line before a table; add one where a table row follows a text line
    lines = src.split("\n")
    fixed = []
    for i, line in enumerate(lines):
        is_row = line.lstrip().startswith("|")
        prev = fixed[-1] if fixed else ""
        if is_row and prev.strip() and not prev.lstrip().startswith("|"):
            fixed.append("")
        fixed.append(line)
    src = "\n".join(fixed)
    out = markdown.markdown(src, extensions=["tables", "fenced_code", "sane_lists"])
    return out.replace("<table>", '<div class="mm-tw"><table>').replace("</table>", "</table></div>")


def _sections(src):
    """Split the Markdown at level-2 headings. Returns (intro_markdown, [(heading, markdown)])."""
    parts = re.split(r"(?m)^(?=## )", src)
    intro, sections = parts[0], []
    for p in parts[1:]:
        heading = p.splitlines()[0][3:].strip()
        sections.append((heading, p))
    return intro, sections


def body():
    src = _read()
    intro, sections = _sections(src)
    toc = "".join(f'<li><a href="#{_slug(h)}">{html.escape(h)}</a></li>' for h, _ in sections)
    rendered = "".join(f'<section id="{_slug(h)}" class="mm-doc">{_md(s)}</section>' for h, s in sections)
    note = ('<div class="mm-note"><b>Read first.</b> This course is based on one video. Income claims, client results and audience '
            'numbers in it are the creator\'s claims and are not verified. Items are marked [Video], [Estimate], [Check] or [Opinion]. '
            'Check every platform rule, price and limit before you act.</div>')
    return (STYLE + '<section><div class="wrap">'
            f'<div class="mm-doc">{_md(intro)}</div>{note}'
            '<h2 class="sec-h">Contents</h2><ol class="mm-toc">' + toc + '</ol></div></section>'
            '<section><div class="wrap">' + rendered + '</div></section>')


def card(href=PAGE):
    return ('<a class="card" href="' + href + '" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px">'
            '<span class="ftag">Make Money</span>'
            '<h3 style="margin:8px 0 6px">Make Money with AI</h3>'
            '<p>From zero to your first paying client while working part time: the AI offer, a credibility stack, '
            'signal-based outreach, and discovery calls. 11 chapters, a capstone, and a glossary of every term.</p>'
            '<span class="go">Open the course →</span></a>')


def section_html():
    return ('<section style="padding-top:24px"><div class="wrap"><h2 class="sec-h" style="margin:0 0 12px">Make Money with AI</h2>'
            '<div class="grid g3">' + card() + '</div></div></section>')


def standalone_html():
    """A self-contained document for printing to PDF. No site CSS; a cover and page breaks between modules."""
    src = _read()
    intro, sections = _sections(src)
    body_html = "".join(f'<section class="mod">{_md(s)}</section>' for _, s in sections)
    intro_html = _md(intro)
    css = """@page{size:A4;margin:16mm 14mm 18mm}*{box-sizing:border-box}
body{font:10.4pt/1.5 'Segoe UI',Inter,Arial,sans-serif;color:#17142E;margin:0}
h1{font-size:24pt;color:#0b5d52;margin:0 0 6px}h2{font-size:17pt;color:#0b5d52;margin:24px 0 6px;border-bottom:1px solid #d6ebe6;padding-bottom:4px;page-break-after:avoid}
h3{font-size:12pt;color:#0f8f7c;margin:16px 0 6px;page-break-after:avoid}p{margin:6px 0}ul,ol{margin:6px 0;padding-left:20px}li{margin:2px 0}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;page-break-inside:avoid}th,td{border:1px solid #cfe5df;padding:4px 6px;text-align:left;vertical-align:top}
th{background:#e6f6f2;color:#0b5d52}pre{background:#0d1630;color:#e8edfb;border-radius:6px;padding:8px;font:8.5pt/1.4 Consolas,monospace;white-space:pre-wrap}
blockquote{background:#eefaf7;border-left:4px solid #0f8f7c;padding:6px 10px;margin:8px 0;border-radius:4px}
.mod{page-break-before:always}.cover{height:240mm;display:flex;flex-direction:column;justify-content:center}
.cover .k{letter-spacing:.14em;text-transform:uppercase;font-weight:700;font-size:9.5pt;color:#0f8f7c}
.cover h1{font-size:32pt;color:#0b5d52}hr{border:0;border-top:1px solid #e5e5e5;margin:18px 0}"""
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Make Money with AI</title>"
            f"<style>{css}</style></head><body>"
            "<section class='cover'><div class='k'>SkillNavora · Make Money · Handbook</div>"
            "<h1>Make Money with AI: From Zero Skills to Your First Paying Client</h1>"
            "<p>Based on the video 'The AI Roadmap You Need To Make Money at Night (Even if You Have a 9-5)'. "
            "Claims in the video are not verified. Check every platform rule and price before you act.</p></section>"
            + intro_html + body_html + "</body></html>")


if __name__ == "__main__":
    print(len(body()), "chars page body;", len(standalone_html()), "chars handbook html")
