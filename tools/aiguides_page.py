"""Complete guides (Claude, ChatGPT, Git & GitHub): hub pages, one page per lesson, the PDFs and the artifact sources.
Content: tools/aiguides/*.py. Renderer: tools/aiguides/render.py. Called from tools/gen_site.py."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "aiguides"))
import render as R


def pages():
    """(path, title, description, body, active) for every guide page."""
    out = []
    for g in R.guides():
        n = len(g["lessons"])
        out.append((f"{g['id']}-guide.html", f"{g['title']} · SkillNavora",
                    f"{g['title']}: {g['subtitle'].lower()}. {n} lessons with steps, real examples, quick checks and official sources, checked {g['checked']}.",
                    R.hub_body(g), "tools.html"))
        for i, l in enumerate(g["lessons"], 1):
            out.append((f"{g['id']}-{l['slug']}.html", f"{l['title']} · {g['title']} · SkillNavora",
                        l["lead"][:155], R.lesson_page_body(g, i), "tools.html"))
        out.append((f"{g['id']}-complete-guide-interactive.html", f"{g['title']}: interactive · SkillNavora",
                    f"The {g['title']} as one interactive page, with progress you can mark in this browser.",
                    R.book_html(g, interactive=True), "tools.html"))
    return out


def build_pdfs(root):
    """Writes handbook/<Guide>.pdf for each guide (A4, page numbers, real footer)."""
    rendered = R.write_all()
    made = {}
    for g in R.guides():
        src = rendered[g["id"]][0]
        dst = os.path.join(root, g["pdf"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        subprocess.run(["node", os.path.join(root, "tools", "aihandbook", "render_pdf.js"), src, dst, "", g["title"]],
                       check=True, timeout=600)
        made[g["id"]] = dst
    return made


def hub_card():
    """A banner for the Tool tutorials page linking the three guides."""
    cards = "".join(
        f'<a class="g-card" href="{g["id"]}-guide.html" style="text-decoration:none;color:inherit;display:block;border:1px solid var(--line);border-radius:16px;padding:16px;background:var(--surface)">'
        f'<small style="color:var(--mu)">{len(g["lessons"])} lessons · checked {g["checked"]}</small><b style="display:block;font-size:17px;margin:4px 0">{g["title"]}</b>'
        f'<small style="color:var(--mu)">{g["subtitle"]}</small></a>'
        for g in R.guides())
    return ('<section style="padding:24px 0 0"><div class="wrap"><div class="kicker">New · complete guides</div>'
            '<h2 style="margin:4px 0 6px">Claude, ChatGPT, and Git &amp; GitHub: complete guides</h2>'
            '<p class="meta" style="margin:0 0 14px;max-width:70ch">Step-by-step lessons on memory, skills, connectors, plugins, Projects, plugins for ChatGPT, Codex, Git and GitHub, checked against official documentation in November 2026. Each guide has a PDF and an interactive version.</p>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px">{cards}</div></div></section>')


if __name__ == "__main__":
    root = os.path.dirname(HERE)
    print(build_pdfs(root))
