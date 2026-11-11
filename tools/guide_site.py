"""Shared renderer for Markdown guides on the site: page body, cards, and a printable standalone HTML.

Usage: body(md_path), card(href, title, text), standalone_html(md_path, title)
"""
import html
import os
import re

import markdown

STYLE = """<style>
.gd-doc h1{font-size:30px;margin:0 0 6px}.gd-doc h2{margin-top:34px;border-bottom:1px solid #e5e5e5;padding-bottom:6px;scroll-margin-top:16px}
.gd-doc h3{margin-top:24px}.gd-tw{display:block;width:100%;max-width:100%;overflow-x:auto;margin:12px 0}
.gd-doc table{border-collapse:collapse;width:100%;min-width:0;font-size:14px}
.gd-doc th,.gd-doc td{border:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}.gd-doc th{background:#f4f4f6}
.gd-doc pre{background:#0f1020;color:#e8e8f0;padding:12px;border-radius:8px;overflow-x:auto;font-size:13px}
.gd-doc code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.92em}
.gd-doc p code,.gd-doc li code,.gd-doc td code{background:#f1f1f5;padding:1px 4px;border-radius:4px}
.gd-doc blockquote{border-left:4px solid #6C4CF5;background:#f7f5ff;margin:14px 0;padding:8px 14px;border-radius:0 8px 8px 0}
.gd-doc,.gd-tw,.gd-doc *{min-width:0;box-sizing:border-box}.gd-doc{width:100%;max-width:100%;overflow-wrap:anywhere}
.gd-toc{display:grid;gap:6px;margin:14px 0 26px;padding:0;list-style:none}
.gd-toc a{display:block;padding:10px 14px;border:1px solid #ddd;border-radius:8px;text-decoration:none;color:inherit}
.gd-note{background:#fff8e6;border:1px solid #f0d78c;padding:12px 14px;border-radius:8px;margin:16px 0}
</style>"""


def _read(md_path):
    with open(md_path, encoding="utf-8") as f:
        return f.read()


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _md(src):
    lines, fixed = src.split("\n"), []
    for line in lines:
        if line.lstrip().startswith("|") and fixed and fixed[-1].strip() and not fixed[-1].lstrip().startswith("|"):
            fixed.append("")
        fixed.append(line)
    out = markdown.markdown("\n".join(fixed), extensions=["tables", "fenced_code", "sane_lists"])
    return out.replace("<table>", '<div class="gd-tw"><table>').replace("</table>", "</table></div>")


def _sections(src):
    parts = re.split(r"(?m)^(?=## )", src)
    intro, secs = parts[0], []
    for p in parts[1:]:
        secs.append((p.splitlines()[0][3:].strip(), p))
    return intro, secs


def _intro(intro):
    return re.sub(r"^# [^\n]*\n", "", intro, count=1)


def body(md_path, note):
    src = _read(md_path)
    intro, secs = _sections(src)
    toc = "".join(f'<li><a href="#{_slug(h)}">{html.escape(h)}</a></li>' for h, _ in secs)
    rendered = "".join(f'<section id="{_slug(h)}" class="gd-doc">{_md(s)}</section>' for h, s in secs)
    return (STYLE + '<section><div class="wrap"><div class="gd-doc">' + _md(_intro(intro)) + '</div>'
            f'<div class="gd-note"><b>Read first.</b> {html.escape(note)}</div>'
            '<h2 class="sec-h">Contents</h2><ol class="gd-toc">' + toc + '</ol></div></section>'
            '<section><div class="wrap">' + rendered + '</div></section>')


def card(href, title, text, tag="AI guide"):
    return ('<a class="card" href="' + href + '" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px">'
            f'<span class="ftag">{html.escape(tag)}</span><h3 style="margin:8px 0 6px">{html.escape(title)}</h3>'
            f'<p>{html.escape(text)}</p><span class="go">Open the guide →</span></a>')


def standalone_html(md_path, title, accent="#3b3b98"):
    src = _read(md_path)
    intro, secs = _sections(src)
    css = f"""@page{{size:A4;margin:16mm 14mm 18mm}}*{{box-sizing:border-box}}
body{{font:10.2pt/1.5 'Segoe UI',Inter,Arial,sans-serif;color:#17142E;margin:0}}
h1{{font-size:24pt;color:{accent};margin:0 0 6px}}h2{{font-size:16.5pt;color:{accent};margin:22px 0 6px;border-bottom:1px solid #d9d9e6;padding-bottom:4px;page-break-after:avoid}}
h3{{font-size:11.8pt;color:#4a4a8a;margin:14px 0 6px;page-break-after:avoid}}p{{margin:6px 0}}ul,ol{{margin:6px 0;padding-left:20px}}li{{margin:2px 0}}
table{{width:100%;border-collapse:collapse;margin:8px 0;font-size:8.8pt;page-break-inside:avoid}}th,td{{border:1px solid #d0d0dd;padding:4px 6px;text-align:left;vertical-align:top}}
th{{background:#efeff7;color:{accent}}}pre{{background:#0d1630;color:#e8edfb;border-radius:6px;padding:8px;font:8.2pt/1.4 Consolas,monospace;white-space:pre-wrap}}
blockquote{{background:#f7f5ff;border-left:4px solid #6C4CF5;padding:6px 10px;margin:8px 0;border-radius:4px}}
.mod{{page-break-before:always}}.cover{{height:230mm;display:flex;flex-direction:column;justify-content:center}}
.cover .k{{letter-spacing:.14em;text-transform:uppercase;font-weight:700;font-size:9.5pt;color:#6C4CF5}}.cover h1{{font-size:30pt}}hr{{border:0;border-top:1px solid #e5e5e5;margin:16px 0}}"""
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<title>{html.escape(title)}</title><style>{css}</style></head><body>"
            f"<section class='cover'><div class='k'>SkillNavora · AI guide · Handbook</div><h1>{html.escape(title)}</h1></section>"
            + _md(_intro(intro)) + "".join(f'<section class="mod">{_md(s)}</section>' for _, s in secs) + "</body></html>")
