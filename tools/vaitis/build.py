"""Builds the Vaitis library data used by vaitis.html.

Inputs (in this folder):
  guides/NNN.md     step-by-step guides written for SkillNavora (header lines, '---', then Markdown)
  tool_facts.json   factual tool list: name, category, short label (tag), pricing, link
Outputs (assets/vaitis/):
  guides.json       guide metadata + rendered HTML
  tools.json        tools with a SkillNavora description and pricing group
  meta.json         categories (with counts and descriptions) and totals

Run: python3 tools/vaitis/build.py   (gen_site.py runs it too)
"""
import glob, hashlib, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "assets", "vaitis")

E = lambda s: html.escape(str(s), quote=True)
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and")).strip("-")

# ---------------------------------------------------------------- categories (SkillNavora wording)
CATS = [
    ("AI Agents & Automation", "🤖", "automate repetitive work and run AI agents that take actions across your apps", "Agents and workflow tools that do multi-step work for you: research, outreach, data entry and app-to-app automation."),
    ("Productivity & Notes", "🗂️", "organise notes, tasks, email and documents and get through daily work faster", "Note-taking, task, inbox and document tools with AI built in."),
    ("Video Generation", "🎬", "create videos, ads and avatar clips from text, images or a script", "Text-to-video, image-to-video and AI avatar tools."),
    ("Marketing & Sales", "📣", "find leads, write campaigns and close more sales", "Lead generation, outreach, CRM and campaign tools."),
    ("Chatbots & Assistants", "💬", "ask questions, write, research and code with a general AI assistant", "General-purpose assistants and model hubs for everyday work."),
    ("Image Generation", "🖼️", "turn a prompt or photo into images, art, headshots and characters", "Text-to-image and image-to-image generators."),
    ("Audio, Voice & Music", "🎙️", "make voiceovers, clone voices, edit podcasts and create music", "Text-to-speech, voice cloning, podcast and music tools."),
    ("SEO & AI Search", "🔎", "rank in Google and get mentioned in AI search answers", "SEO research, content optimisation and AI-search (GEO) visibility tools."),
    ("No-Code & App Builders", "🧩", "build websites and apps without writing code", "Describe an app or site and publish a working version."),
    ("Writing & Copywriting", "✍️", "draft and polish blogs, emails, scripts and marketing copy", "Writing assistants and copywriting tools."),
    ("Coding & Development", "💻", "write, review and ship code with an AI pair programmer", "Coding agents, AI code editors and developer APIs."),
    ("Education & Learning", "🎓", "study, revise and teach with AI tutors and course tools", "Tutors, flashcards, course builders and study helpers."),
    ("Design & Creative", "🎨", "design logos, graphics, 3D and interiors with AI help", "Design suites and creative tools with AI features."),
    ("Social Media", "📱", "plan, write and schedule social posts and grow an audience", "Social scheduling, content and analytics tools."),
    ("Image Editing", "🪄", "remove backgrounds, upscale, retouch and transform photos", "AI photo editors and enhancers."),
    ("Video Editing & Clips", "✂️", "edit footage, add captions and cut long videos into short clips", "AI video editors, captioning and clipping tools."),
    ("AI Detection & Humanisers", "🕵️", "check whether text is AI-written or make drafts read more naturally", "AI-content detectors and rewriting tools. Use them honestly and within your school's or employer's rules."),
    ("Advertising", "🎯", "create, test and optimise ads", "Ad creative, targeting and optimisation tools."),
    ("Data & Analytics", "📊", "analyse data, build dashboards and ask questions in plain English", "Analytics, BI and spreadsheet AI tools."),
    ("Meetings & Transcription", "📝", "record, transcribe and summarise meetings and calls", "Meeting assistants, transcription and note-taking tools."),
    ("Finance & Accounting", "💰", "manage bookkeeping, invoices, budgets and investing research", "Accounting, finance and investing tools."),
    ("Careers & Recruiting", "💼", "write resumes, prepare for interviews and hire faster", "Job-search, resume, interview and recruiting tools."),
    ("Presentations & Slides", "📽️", "turn ideas or documents into finished slide decks", "AI presentation and document designers."),
    ("Translation", "🌐", "translate text, documents, audio and video", "Translation and dubbing tools."),
    ("E-commerce", "🛒", "run an online store: product content, photos and support", "Store, product and e-commerce support tools."),
    ("Health", "🩺", "track health and wellbeing", "Health and wellbeing tools. Not a substitute for a doctor."),
]
CAT = {c[0]: {"name": c[0], "icon": c[1], "use": c[2], "desc": c[3], "slug": slug(c[0])} for c in CATS}

# ---------------------------------------------------------------- tools
def build_tools():
    facts = json.load(open(os.path.join(HERE, "tool_facts.json"), encoding="utf-8"))
    tools = []
    for t in facts:
        c = CAT[t["category"]]
        label = (t.get("tag") or "").strip()
        lab = label[:1].upper() + label[1:] if label else t["category"]
        free = t.get("free") or ""
        group = {"free": "free", "freemium": "freeplan", "paid": "paid"}.get(free, "unknown")
        pricing = t.get("pricing") or "Check the website for pricing"
        tools.append({
            "id": t["id"], "name": t["name"], "cat": t["category"], "slug": c["slug"], "label": lab,
            "desc": f"{lab}. Use {t['name']} to {c['use']}.",
            "pricing": pricing, "price": group, "url": t["url"], "domain": t.get("domain") or "",
        })
    tools.sort(key=lambda x: (x["cat"], x["name"].lower()))
    return tools

# ---------------------------------------------------------------- guides (small Markdown renderer for our own files)
def inline(s):
    s = E(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\"'=>/])(https?://[^\s<)]+[^\s<).,;:])", r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    return s

KIND = {"prompt": "Prompt", "cmd": "Command", "link": "Open in browser", "sql": "SQL", "json": "Config", "toml": "Config", "python": "Python"}

def render(md):
    lines = md.split("\n"); out = []; i = 0; steps = []
    para = []
    def flush():
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^```(\w+)\s*(.*)$", ln)
        if m:
            flush(); kind, label = m.group(1), m.group(2).strip()
            body = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"): body.append(lines[i]); i += 1
            i += 1
            text = "\n".join(body)
            k = KIND.get(kind, kind.title())
            href = text.strip() if kind == "link" and re.match(r"^https?://\S+$", text.strip()) else ""
            open_btn = f'<a class="vx-open" href="{E(href)}" target="_blank" rel="noopener">Open ↗</a>' if href else ""
            out.append(f'<div class="vx-code vx-{E(kind)}"><div class="vx-code-h"><span><b>{E(k)}</b>{(" · " + E(label)) if label else ""}</span>{open_btn}<button type="button" class="vx-copy">Copy</button></div><pre><code>{E(text)}</code></pre></div>')
            continue
        if ln.startswith("## "):
            flush()
            if steps: out.append("</section>")
            title = ln[3:].strip(); steps.append(title)
            sm = re.match(r"^Step (\d+):\s*(.*)$", title)
            badge = sm.group(1) if sm else ("✓" if title.lower().startswith(("what you need", "what it is")) else "+")
            shown = sm.group(2) if sm else title
            cls = "vx-step" + ("" if sm else " vx-aside")
            out.append(f'<section class="{cls}" id="s{len(steps)}"><h3><span class="vx-n">{E(badge)}</span>{inline(shown)}</h3>')
            i += 1; continue
        if ln.startswith("!> ") or ln.startswith("> "):
            flush(); warn = ln.startswith("!>"); txt = ln[3:] if warn else ln[2:]
            out.append(f'<div class="vx-note {"vx-warn" if warn else "vx-tip"}"><span aria-hidden="true">{"⚠️" if warn else "💡"}</span><div>{inline(txt)}</div></div>')
            i += 1; continue
        if ln.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith("|"): rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows if not re.match(r"^\|[\s\-|:]+\|$", r.strip())]
            head, body = cells[0], cells[1:]
            out.append('<div class="vx-table"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
            continue
        if re.match(r"^(- |\d+\. )", ln):
            flush(); ordered = bool(re.match(r"^\d+\. ", ln)); items = []
            while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if not ln.strip(): flush(); i += 1; continue
        para.append(ln.strip()); i += 1
    flush()
    if steps: out.append("</section>")
    return "\n".join(out), steps

# Tool names that are also everyday words (not counted as a mention)
COMMON = {"Make", "Adapt", "Rival", "Notion AI", "Copy", "Write", "Read", "Scale", "Polish", "Arena", "Council", "Harvey", "Taste"}

def build_guides(tool_names):
    guides = []
    for f in sorted(glob.glob(os.path.join(HERE, "guides", "*.md"))):
        raw = open(f, encoding="utf-8").read()
        head, md = raw.split("\n---\n", 1)
        meta = dict(l.split(": ", 1) for l in head.strip().split("\n"))
        links = [dict(zip(("label", "url"), x.strip().split("|", 1))) for x in meta.get("links", "").split(";") if "|" in x]
        body, steps = render(md)
        text = re.sub(r"<[^>]+>", " ", html.unescape(body)) + " " + " ".join(l["label"] for l in links)
        used = sorted({n for n in tool_names if len(n) > 3 and n not in COMMON and re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", text)})
        guides.append({"id": meta["id"], "title": meta["title"], "cat": meta["category"], "summary": meta["summary"],
                       "time": meta.get("time", ""), "cost": meta.get("cost", ""), "level": meta.get("level", ""),
                       "date": "2026-11-13", "links": links, "steps": steps, "tools": used[:12], "html": body})
    return guides

def main():
    os.makedirs(OUT, exist_ok=True)
    tools = build_tools()
    guides = build_guides([t["name"] for t in tools])
    counts = {}
    for t in tools: counts[t["cat"]] = counts.get(t["cat"], 0) + 1
    cats = sorted(({**CAT[n], "count": counts.get(n, 0)} for n in CAT), key=lambda c: -c["count"])
    price = {}
    for t in tools: price[t["price"]] = price.get(t["price"], 0) + 1
    meta = {"tools": len(tools), "guides": len(guides), "categories": cats, "price": price,
            "guideCats": sorted({g["cat"] for g in guides})}
    for name, data in (("tools", tools), ("guides", guides), ("meta", meta)):
        with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    return meta

def versions():
    return {n: hashlib.md5(open(os.path.join(OUT, n + ".json"), "rb").read()).hexdigest()[:8] for n in ("tools", "guides", "meta")}

if __name__ == "__main__":
    m = main()
    print("tools", m["tools"], "guides", m["guides"], "categories", len(m["categories"]), "price", m["price"])
