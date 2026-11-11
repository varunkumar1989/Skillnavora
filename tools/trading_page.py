"""Renders the Trading Terminal handbook (Master-Freelancing-Trading-Terminal/trading-terminal-handbook.md)
as a Master Freelancing chapter: body() for the site page, card()/section_html() for the listing,
and standalone_html() (images embedded) for the PDF."""
import base64
import html
import os
import re

import markdown

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Master-Freelancing-Trading-Terminal")
SRC = os.path.join(BASE, "trading-terminal-handbook.md")
PAGE = "trading-terminal-handbook.html"
PDF_NAME = "Trading-Terminal-Handbook.pdf"
IMG_PREFIX = "Master-Freelancing-Trading-Terminal/"   # images are relative to the site root on the website

STYLE = """<style>
.tt-doc h1{font-size:30px;margin:0 0 6px}.tt-doc h2{margin-top:34px;border-bottom:1px solid #e5e5e5;padding-bottom:6px}
.tt-doc h3{margin-top:24px}.tt-tw{display:block;width:100%;max-width:100%;overflow-x:auto;margin:12px 0}
.tt-doc table{border-collapse:collapse;width:100%;min-width:0;font-size:14px}
.tt-doc th,.tt-doc td{border:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}.tt-doc th{background:#f4f4f6}
.tt-doc pre{background:#0f1020;color:#e8e8f0;padding:12px;border-radius:8px;overflow-x:auto;font-size:13px}
.tt-doc code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.92em}
.tt-doc p code,.tt-doc li code,.tt-doc td code{background:#f1f1f5;padding:1px 4px;border-radius:4px}
.tt-doc blockquote{border-left:4px solid #b7791f;background:#fff8e6;margin:14px 0;padding:8px 14px;border-radius:0 8px 8px 0}
.tt-doc img{max-width:100%;height:auto;display:block;margin:14px auto;border:1px solid #e5e5e5;border-radius:10px;background:#fff}
.tt-doc figcaption,.tt-doc em{color:#56626c}
.tt-doc,.tt-tw,.tt-doc *{min-width:0;box-sizing:border-box}.tt-doc{width:100%;max-width:100%;overflow-wrap:anywhere}
.tt-toc{display:grid;gap:6px;margin:14px 0 26px;padding:0;list-style:none}
.tt-toc a{display:block;padding:10px 14px;border:1px solid #ddd;border-radius:8px;text-decoration:none;color:inherit}
.tt-note{background:#fff8e6;border:1px solid #f0d78c;padding:12px 14px;border-radius:8px;margin:16px 0}
</style>"""


def _read():
    with open(SRC, encoding="utf-8") as f:
        return f.read()


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _md(src, img_prefix):
    src = re.sub(r"\]\((images/)", "](" + img_prefix + "images/", src)
    lines, fixed = src.split("\n"), []
    for line in lines:
        if line.lstrip().startswith("|") and fixed and fixed[-1].strip() and not fixed[-1].lstrip().startswith("|"):
            fixed.append("")
        fixed.append(line)
    out = markdown.markdown("\n".join(fixed), extensions=["tables", "fenced_code", "sane_lists"])
    return out.replace("<table>", '<div class="tt-tw"><table>').replace("</table>", "</table></div>")


def _sections(src):
    parts = re.split(r"(?m)^(?=## )", src)
    intro, secs = parts[0], []
    for p in parts[1:]:
        secs.append((p.splitlines()[0][3:].strip(), p))
    return intro, secs


def body():
    src = _read()
    intro, secs = _sections(src)
    intro = re.sub(r"^# [^\n]*\n", "", intro, count=1)
    toc = "".join(f'<li><a href="#{_slug(h)}">{html.escape(h)}</a></li>' for h, _ in secs)
    rendered = "".join(f'<section id="{_slug(h)}" class="tt-doc">{_md(s, IMG_PREFIX)}</section>' for h, s in secs)
    note = ('<div class="tt-note"><b>Read first.</b> This chapter describes rules and a way to test them. It does not show that any strategy '
            'works. Charges, lot sizes, APIs and regulations must be checked on official pages. Options can lose all the premium paid, and '
            'selling options can lose more than was received.</div>')
    return (STYLE + '<section><div class="wrap"><div class="tt-doc">' + _md(intro, IMG_PREFIX) + '</div>' + note
            + '<h2 class="sec-h">Contents</h2><ol class="tt-toc">' + toc + '</ol></div></section>'
            + '<section><div class="wrap">' + rendered + '</div></section>')


def card(href=PAGE):
    return ('<a class="card" href="' + href + '" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px">'
            '<span class="ftag">Master Freelancing</span>'
            '<h3 style="margin:8px 0 6px">Personal Trading &amp; Analytics Terminal</h3>'
            '<p>Architecture, security, data, Black-Scholes Greeks, a 9/21 EMA strategy with a friction-adjusted backtest, guarded paper and live '
            'execution, and the regulatory checks. Includes tested reference code and strategy diagrams.</p>'
            '<span class="go">Open the chapter →</span></a>')


def section_html():
    return ('<section style="padding-top:24px"><div class="wrap"><h2 class="sec-h" style="margin:0 0 12px">Algorithmic trading systems</h2>'
            '<div class="grid g3">' + card() + '</div></div></section>')


def standalone_html():
    """Self-contained for the PDF: images embedded as data URIs so the print does not depend on paths."""
    src = _read()
    def embed(m):
        rel = m.group(1)
        path = os.path.join(BASE, rel.replace("images/", "images/", 1))
        if not os.path.exists(path):
            return m.group(0)
        mime = "image/svg+xml" if path.endswith(".svg") else "image/png"
        data = base64.b64encode(open(path, "rb").read()).decode()
        return f"](data:{mime};base64,{data})"
    src = re.sub(r"\]\((images/[^)]+)\)", embed, src)
    intro, secs = _sections(src)
    intro = re.sub(r"^# [^\n]*\n", "", intro, count=1)
    css = """@page{size:A4;margin:16mm 14mm 18mm}*{box-sizing:border-box}
body{font:10.2pt/1.5 'Segoe UI',Inter,Arial,sans-serif;color:#17142E;margin:0}
h1{font-size:24pt;color:#1f3a5f;margin:0 0 6px}h2{font-size:16.5pt;color:#1f3a5f;margin:22px 0 6px;border-bottom:1px solid #d6dde8;padding-bottom:4px;page-break-after:avoid}
h3{font-size:11.8pt;color:#2e5c8a;margin:14px 0 6px;page-break-after:avoid}p{margin:6px 0}ul,ol{margin:6px 0;padding-left:20px}li{margin:2px 0}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:8.8pt;page-break-inside:avoid}th,td{border:1px solid #cdd6e3;padding:4px 6px;text-align:left;vertical-align:top}
th{background:#eef3f9;color:#1f3a5f}pre{background:#0d1630;color:#e8edfb;border-radius:6px;padding:8px;font:8.2pt/1.4 Consolas,monospace;white-space:pre-wrap}
blockquote{background:#fff8e6;border-left:4px solid #b7791f;padding:6px 10px;margin:8px 0;border-radius:4px}
img{max-width:100%;height:auto;display:block;margin:10px auto;page-break-inside:avoid}
.mod{page-break-before:always}.cover{height:230mm;display:flex;flex-direction:column;justify-content:center}
.cover .k{letter-spacing:.14em;text-transform:uppercase;font-weight:700;font-size:9.5pt;color:#2e5c8a}
.cover h1{font-size:30pt}hr{border:0;border-top:1px solid #e5e5e5;margin:16px 0}"""
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Personal Trading &amp; Analytics Terminal</title>"
            f"<style>{css}</style></head><body>"
            "<section class='cover'><div class='k'>SkillNavora · Master Freelancing · Handbook</div>"
            "<h1>Personal Trading &amp; Analytics Terminal</h1>"
            "<p>Architecture, security, data, options analytics, a 9/21 EMA strategy, a friction-adjusted backtest, guarded execution and "
            "the regulatory checks. The strategy is not shown to work. Check every charge, rule and API before use.</p></section>"
            + _md(intro, "") + "".join(f'<section class="mod">{_md(s, "")}</section>' for _, s in secs) + "</body></html>")


if __name__ == "__main__":
    print(len(body()), "chars page;", len(standalone_html()), "chars handbook html")
