"""Shared builder for SkillNavora mini-courses: PDF (headless Chromium) + web page. A course is a dict:
{slug, pdf, title, kicker, intro, classes:[(level,title,goal,body_html,takeaways,exercise)], cheat:[(term,meaning)], cheat_title,
 qa:[(q,a)], glossary:[(term,meaning)], links:[(name,url)], templates_html, tutor_q, toolkit_link}"""
import html, os, json, subprocess, tempfile
E = html.escape
LEVEL = {"basic": ("Basic", "#16a34a"), "intermediate": ("Intermediate", "#d97706"), "advanced": ("Advanced", "#db2777")}

PDF_CSS = """@page{size:A4}*{box-sizing:border-box}body{font:10.6pt/1.55 'Segoe UI',Inter,Arial,sans-serif;color:#17142E;margin:0}
h1,h2,h3{font-family:'Segoe UI',Inter,Arial,sans-serif;color:#2E3192;line-height:1.25}h2{font-size:20pt;margin:0 0 4px}h3{font-size:12.5pt;margin:16px 0 6px;color:#3b2bb5}
p{margin:6px 0}ul,ol{margin:6px 0;padding-left:20px}li{margin:2px 0}table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9.6pt;page-break-inside:avoid}
th,td{border:1px solid #d8d3ee;padding:5px 7px;text-align:left;vertical-align:top}th{background:#efedfb;color:#2E3192}
pre{background:#0d1630;color:#e8edfb;border-radius:8px;padding:9px 11px;font:8.9pt/1.45 Consolas,'Courier New',monospace;white-space:pre-wrap;page-break-inside:avoid}
.box{background:#f4f1ff;border-left:4px solid #6C4CF5;padding:8px 12px;border-radius:6px;margin:8px 0}.flow{background:#ecfeff;border:1px solid #a5f3fc;border-radius:8px;padding:8px 12px;font-weight:600;color:#155e75}
.cover{height:255mm;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(135deg,#2E3192,#6C4CF5 55%,#22D3EE);color:#fff;padding:24mm;border-radius:10px;page-break-after:always}
.cover h1{color:#fff;font-size:34pt;margin:10px 0}.cover p{font-size:13pt;color:#e6e3ff}.cover .k{letter-spacing:.14em;text-transform:uppercase;font-weight:700;font-size:10pt}
.class{page-break-before:always}.lvl{display:inline-block;font-weight:700;font-size:8.5pt;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:99px;color:#fff;margin-bottom:6px}
.goal{color:#55607a;font-size:11pt;margin:0 0 10px}.take{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:8px 12px;margin-top:10px;page-break-inside:avoid}.ex{background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:8px 12px;margin-top:8px;page-break-inside:avoid}
.toc td{border:0;border-bottom:1px solid #eee;padding:6px}.small{font-size:9pt;color:#55607a}.foot{font-size:8.5pt;color:#888;margin-top:14px}"""


def _classes(C):
    out = []
    for i, (lv, title, goal, body, take, ex) in enumerate(C["classes"], 1):
        ln, col = LEVEL[lv]
        out.append(f'<section class="class"><span class="lvl" style="background:{col}">{ln} · Class {i}</span><h2>{E(title)}</h2><p class="goal">{E(goal)}</p>{body}'
                   f'<div class="take"><b>Key takeaways</b><ul>' + "".join(f"<li>{E(t)}</li>" for t in take) + f'</ul></div><div class="ex"><b>Practice exercise:</b> {E(ex)}</div></section>')
    return "".join(out)

def pdf_html(C):
    toc = "".join(f'<tr><td>Class {i}</td><td><b>{E(t)}</b></td><td>{LEVEL[lv][0]}</td></tr>' for i, (lv, t, *_) in enumerate(C["classes"], 1))
    cheat = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in C["cheat"])
    qa = "".join(f"<p><b>Q{i}. {E(q)}</b><br>{E(a)}</p>" for i, (q, a) in enumerate(C["qa"], 1))
    glo = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in C["glossary"])
    links = "".join(f'<li>{E(n)}: <a href="{E(u)}">{E(u)}</a></li>' for n, u in C["links"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{E(C['title'])} · SkillNavora</title><style>{PDF_CSS}</style></head><body>
<div class="cover"><div class="k">{E(C['kicker'])}</div><h1>{E(C['title'])}</h1><p>{E(C['intro'])}</p><p class="small" style="color:#d9e8ff">Edition 2026 · skillnavora.in</p></div>
<h2>How to use this guide</h2><p>Each class has goals, concepts with Indian examples, key takeaways and a practice exercise, from basic to advanced. Finish with the final project to build something you can show in interviews.</p>
<table class="toc"><tr><th></th><th>Class</th><th>Level</th></tr>{toc}<tr><td></td><td><b>Toolkit:</b> templates, {E(C['cheat_title']).lower()}, glossary, {len(C['qa'])} interview questions, further reading</td><td></td></tr></table>
{_classes(C)}
<section class="class"><span class="lvl" style="background:#2E3192">Toolkit</span><h2>Templates</h2>{C['templates_html']}</section>
<section class="class"><span class="lvl" style="background:#2E3192">Toolkit</span><h2>{E(C['cheat_title'])}</h2><table><tr><th>Term / tool</th><th>Meaning / use</th></tr>{cheat}</table><h2 style="margin-top:18px">Glossary</h2><table>{glo}</table></section>
<section class="class"><span class="lvl" style="background:#2E3192">Interview prep</span><h2>{len(C['qa'])} interview questions with answers</h2>{qa}</section>
<section class="class"><span class="lvl" style="background:#2E3192">Learn more</span><h2>Further reading and tools</h2><ul>{links}</ul>
<p class="foot">© SkillNavora · skillnavora.in · Part of the AI Product Management and GenAI Launchpad programs. Practise with the free AI Tutor, AI PM Toolkit and Practice Lab on skillnavora.in.</p></section></body></html>"""

def web_page(C):
    cards = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><span style="font:700 11px var(--body);letter-spacing:.06em;text-transform:uppercase;color:{LEVEL[lv][1]}">{LEVEL[lv][0]} · Class {i}</span><h3 style="margin:0;font-size:18px">{E(t)}</h3><p style="margin:0;color:var(--mu)">{E(g)}</p><ul style="margin:4px 0 0;padding-left:18px;color:var(--mu);font-size:14px">' + "".join(f"<li>{E(x)}</li>" for x in tk) + "</ul></div>"
                    for i, (lv, t, g, _, tk, _) in enumerate(C["classes"], 1))
    qa = "".join(f"<details class='card' style='padding:14px 18px'><summary style='cursor:pointer;font-weight:700'>{E(q)}</summary><p style='margin:8px 0 0;color:var(--mu)'>{E(a)}</p></details>" for q, a in C["qa"][:8])
    from urllib.parse import quote
    return f"""<section style="padding-top:28px"><div class="wrap">
<div class="card" style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;border:2px solid #6C4CF5;margin-bottom:26px"><div style="max-width:640px"><div class="kicker">Free PDF · {len(C['classes'])} classes · basic to advanced</div><h2 style="margin:6px 0">{E(C['title'])}</h2><p style="margin:0;color:var(--mu)">{E(C['intro'])}</p></div>
<div style="display:flex;flex-direction:column;gap:8px"><a class="btn btn-primary" href="handbook/{E(C['pdf'])}">Download the PDF</a><a class="btn btn-line" href="ai-tutor.html?q={quote(C['tutor_q'])}">Ask the AI Tutor</a>{C.get('extra_btn','')}</div></div>
<h2 class="sec-h" style="font-size:26px">In one line</h2><p class="sub" style="max-width:820px">{E(C['oneline'])}</p>
<h2 class="sec-h" style="font-size:24px;margin-top:26px">The {len(C['classes'])} classes</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px">{cards}</div>
<h2 class="sec-h" style="font-size:24px;margin-top:30px">Interview questions</h2><div style="display:grid;gap:10px">{qa}</div><p class="meta" style="margin-top:10px">All {len(C['qa'])} questions with answers, templates and the cheat sheet are in the PDF.</p>
</div></section>"""

def build_pdf(C, out_dir):
    os.makedirs(os.path.join(out_dir, "handbook"), exist_ok=True)
    src = os.path.join(tempfile.gettempdir(), "sn_" + C["slug"] + ".html"); open(src, "w", encoding="utf-8").write(pdf_html(C))
    dst = os.path.join(out_dir, "handbook", C["pdf"])
    foot = E(C["title"]) + " · SkillNavora"
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+{json.dumps(src)});
await p.pdf({{path:{json.dumps(dst)},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
footerTemplate:{json.dumps('<div style="font-size:8px;color:#888;width:100%;padding:0 15mm;display:flex;justify-content:space-between"><span>' + foot + '</span><span class="pageNumber"></span></div>')},margin:{{top:'14mm',bottom:'16mm',left:'15mm',right:'15mm'}}}});await b.close()}})();"""
    env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
    subprocess.run(["node", "-e", js], check=True, env=env)
    return dst

# ---------------------------------------------------------------- illustrations (inline SVG, work in PDF, web and artifact)
_PAL = ["#6C4CF5", "#0E9FB8", "#16A34A", "#D97706", "#DB2777", "#2E3192"]
def _wrap(text, n):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines[:4]
def _txt(x, y, text, n=16, size=12, color="#14112a", weight=600):
    ls = _wrap(text, n); y0 = y - (len(ls) - 1) * (size * 0.6)
    return "".join(f'<text x="{x}" y="{y0 + i * size * 1.2:.1f}" text-anchor="middle" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{E(l)}</text>' for i, l in enumerate(ls))
def _fig(svg, w, h, caption, maxw=None):
    return (f'<figure class="ill" style="margin:12px auto;{"max-width:%dpx;" % maxw if maxw else ""}padding:10px;background:#ffffff;border:1px solid #e3e0f2;border-radius:12px;page-break-inside:avoid">'
            f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{E(caption)}" style="display:block;max-width:100%;height:auto">{svg}</svg>'
            f'<figcaption style="font:600 12px Inter,Segoe UI,Arial,sans-serif;color:#55607a;text-align:center;margin-top:4px">{E(caption)}</figcaption></figure>')
def ill_flow(steps, caption):
    n = len(steps); per = min(n, 4); rows = (n + per - 1) // per; bw, bh, gx, gy = 150, 62, 34, 30
    W = per * bw + (per - 1) * gx + 20; H = rows * bh + (rows - 1) * gy + 20; s = ""
    for i, st in enumerate(steps):
        r, c = divmod(i, per); x = 10 + c * (bw + gx); y = 10 + r * (bh + gy); col = _PAL[i % len(_PAL)]
        s += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="12" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-width="2"/>'
        s += f'<circle cx="{x + 14}" cy="{y + 14}" r="10" fill="{col}"/><text x="{x + 14}" y="{y + 18}" text-anchor="middle" font-family="Inter,Arial" font-size="11" font-weight="800" fill="#fff">{i + 1}</text>'
        s += _txt(x + bw / 2 + 6, y + bh / 2 + 4, st, 17, 12)
        if i < n - 1:
            if c < per - 1: s += f'<path d="M{x + bw + 4} {y + bh / 2} h{gx - 10}" stroke="#8a86a8" stroke-width="2" fill="none" marker-end="url(#ah)"/>'
            else: s += f'<path d="M{x + bw / 2} {y + bh + 4} v{gy - 10}" stroke="#8a86a8" stroke-width="2" fill="none" marker-end="url(#ah)"/>'
    defs = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#8a86a8"/></marker></defs>'
    return _fig(defs + s, W, H, caption)
def ill_cycle(steps, caption):
    import math
    n = len(steps); W = H = 420; cx = cy = 210; R = 140; s = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#c9c4ea" stroke-width="3" stroke-dasharray="6 6"/>'
    for i, st in enumerate(steps):
        a = -math.pi / 2 + 2 * math.pi * i / n; x = cx + R * math.cos(a); y = cy + R * math.sin(a); col = _PAL[i % len(_PAL)]
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="52" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2"/>' + _txt(x, y + 4, st, 13, 11.5)
    return _fig(s, W, H, caption, 340)
def ill_quad(xlab, ylab, quads, caption):
    W, H = 460, 380; s = '<rect x="60" y="20" width="380" height="300" fill="#faf9ff" stroke="#c9c4ea"/><path d="M250 20 V320 M60 170 H440" stroke="#c9c4ea" stroke-width="2"/>'
    pos = [(155, 95), (345, 95), (155, 245), (345, 245)]
    for i, ((x, y), q) in enumerate(zip(pos, quads)): s += _txt(x, y, q, 22, 12.5, _PAL[[2, 0, 4, 3][i]], 700)
    s += _txt(250, 348, xlab + " →", 50, 12, "#55607a"); s += f'<text x="22" y="170" transform="rotate(-90 22 170)" text-anchor="middle" font-family="Inter,Arial" font-size="12" fill="#55607a">{E(ylab)} →</text>'
    return _fig(s, W, H, caption)
def ill_stack(layers, caption):
    W = 460; bh = 46; H = len(layers) * (bh + 8) + 12; s = ""
    for i, (name, desc) in enumerate(layers):
        y = 6 + i * (bh + 8); inset = i * 14; col = _PAL[i % len(_PAL)]
        s += f'<rect x="{10 + inset}" y="{y}" width="{W - 20 - 2 * inset}" height="{bh}" rx="10" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2"/>'
        s += f'<text x="{W / 2}" y="{y + 19}" text-anchor="middle" font-family="Inter,Arial" font-size="13" font-weight="800" fill="#14112a">{E(name)}</text><text x="{W / 2}" y="{y + 36}" text-anchor="middle" font-family="Inter,Arial" font-size="11" fill="#55607a">{E(desc)}</text>'
    return _fig(s, W, H, caption)
