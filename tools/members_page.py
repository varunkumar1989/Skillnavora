"""Members library (members.html): every interactive handbook shared as a Claude artifact, in one locked page.
The page is locked by functions/_middleware.js: only admins and people the owner approved (Admin -> Applications ->
Resource access) or who bought the all-access pass can open it. Everyone else is asked to sign in and request access.
After the site is built, run() points every public claude.ai artifact link at its entry here, so the artifact
addresses are only visible to members. To add an artifact, add it to ARTIFACTS."""
import html, os, re

E = lambda s: html.escape(str(s), quote=True)

# (group, artifact id, name, what it is)
ARTIFACTS = [
    ("PM handbooks", "51eByvQUgCYBHLAYmyGzVJ", "Product Management Master Handbook", "The complete interactive PM handbook."),
    ("PM handbooks", "XmhTL4Yv72bgmSFFuR2hzz", "PM handbook library", "All 68 PM handbook PDFs in one place."),
    ("PM handbooks", "MS8ypMH8oBvKv1yUh1cvnz", "Module 1: Product Thinking", "Interactive handbook for module 1."),
    ("PM handbooks", "DkwwfdWHRvKZLsdLcEbMpn", "Module 2: Strategy", "Interactive handbook for module 2."),
    ("PM handbooks", "K3T1UMe4CNJkCjKj7Ez8fx", "Module 3: Discovery", "Interactive handbook for module 3."),
    ("PM handbooks", "72TUSZifJJeTFbWomzQFyh", "Module 4: Framing and Prioritisation", "Interactive handbook for module 4."),
    ("PM handbooks", "Qtqufc9m3ynUAAYPpgD7Wv", "Module 5: UX Evaluation", "Interactive handbook for module 5."),
    ("PM handbooks", "DawNga87iUtE7ChHx1Gc5y", "Module 6: Communication", "Interactive handbook for module 6."),
    ("PM handbooks", "8v2C1aN7HkPE1g4xTjSEMd", "Module 7: Analytics and Metrics", "Interactive handbook for module 7."),
    ("PM handbooks", "TYRGzQiiB2heA8UthxbkhF", "Module 8: Growth and Monetisation", "Interactive handbook for module 8."),
    ("PM handbooks", "7nVGHVjD72D1CtiuDV264U", "Module 9: Tech for PMs", "Interactive handbook for module 9."),
    ("PM handbooks", "Eapbg7p1qQnsj44sU5di6r", "Module 10: LLM and RAG", "Interactive handbook for module 10."),
    ("PM handbooks", "HzNTTHDX2mBESFu3BpniQX", "Module 11: Vibe Coding", "Interactive handbook for module 11."),
    ("PM handbooks", "XJjeLHnBouyE9LnFdHmt2N", "Module 12: Agentic AI", "Interactive handbook for module 12."),
    ("AI and data", "73qLV99WGYBx7eWxZNXiyB", "AI Master Course: clickable handbook", "Six weeks, 26 subjects, diagrams, code and the coverage check."),
    ("AI and data", "N9KRxr9bwXhCeDquDZBdoD", "AI Master Course: handbook (static)", "The full handbook as one page."),
    ("AI and data", "7278116b7jCN2ny9XnmtVM", "Data Science & AI, DSA and GenAI handbooks", "The interactive handbook with every track, DSA and GenAI."),
    ("AI and data", "1CQnXt2uDQKmjK4ZS5hkVF", "Vaitis AI library", "763 AI tools and 25 step-by-step guides."),
    ("Other programmes", "YcVe9ENf1hZJfk1yTZcxMA", "Forward Deployed Engineer handbook", "From non-coder to enterprise AI builder."),
    ("Other programmes", "BW5nVs6WRq1mS1dxbhioXQ", "SFMC Academy", "Every module, topic and all 37 PDFs."),
    ("Digital marketing workshops", "LJrGBHbd5ohTQebDsXyo6p", "Digital marketing: interactive pictures", "Visual introduction to the course."),
    ("Digital marketing workshops", "XQhCWixR7eip5riUcSN3nd", "Market research workshop", "Practice workshop for chapter 2."),
    ("Digital marketing workshops", "6esoj7rdbTt4G7PRkEg6Kn", "Website build workshop", "Build workshop for chapter 3."),
    ("Digital marketing workshops", "EKRRKMWKMo4fLpVP8Wjqq5", "Email marketing workshop", "Workshop for chapter 4."),
    ("Digital marketing workshops", "VZpxqPbTXuyBqNfMotBTfi", "Copywriting workshop", "Workshop for chapter 5."),
    ("Digital marketing workshops", "HWRB6AY5q3oQVU6dCYD1gq", "SEO workshop", "Workshop for chapter 6."),
    ("Digital marketing workshops", "WYKuirtew4pDecTFwfkDKS", "YouTube planner", "Planner for chapter 7."),
]
ON_SITE = [("ai-master-course-handbook.html", "AI Master Course: clickable handbook", "The on-site copy of the AI Master Course handbook."),
           ("ai-academy-interactive.html", "AI Skills Academy: full class content", "Every AI skills class with its tabs and PDFs."),
           ("handbooks/index.html", "SkillNavora Handbooks", "PM, Data Science & AI, DSA and GenAI handbooks with every PDF."),
           ("study-library.html", "Study Library", "Every lesson, class and PDF, by programme.")]
IDS = {a[1] for a in ARTIFACTS}

CSS = """<style>
.mb-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:14px}
.mb-card{display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--surface);text-decoration:none;color:inherit;scroll-margin-top:100px;min-width:0}
.mb-card b{font-size:16px}.mb-card span{color:var(--mu);font-size:14px;line-height:1.5}.mb-card em{font-style:normal;font-weight:700;color:var(--brand-ink);font-size:13.5px;margin-top:auto}
.mb-card:target{outline:2px solid var(--brand);outline-offset:2px}
.mb-sec{margin-top:30px}.mb-sec h2{margin:4px 0 4px;font-size:22px}
</style>"""


def body():
    groups = []
    for g in dict.fromkeys(a[0] for a in ARTIFACTS):
        cards = "".join(f'<a class="mb-card" id="a-{aid}" href="https://claude.ai/artifact/{aid}" target="_blank" rel="noopener" data-nogate>'
                        f'<b>{E(n)}</b><span>{E(d)}</span><em>Open ↗</em></a>' for gg, aid, n, d in ARTIFACTS if gg == g)
        groups.append(f'<section class="mb-sec"><div class="kicker">Interactive handbooks</div><h2>{E(g)}</h2><div class="mb-grid">{cards}</div></section>')
    site = "".join(f'<a class="mb-card" href="{E(h)}"><b>{E(n)}</b><span>{E(d)}</span><em>Open →</em></a>' for h, n, d in ON_SITE)
    return CSS + f"""<section class="sn-search"><div class="wrap">
  <div class="kicker">Members</div><h1 class="sec-h" style="margin:6px 0 10px">Members library</h1>
  <p style="max-width:68ch">Every interactive handbook and workshop in one place. This page is for members: people the SkillNavora team has given access to, and all-access pass holders. Please do not share these links.</p>
  {"".join(groups)}
  <section class="mb-sec"><div class="kicker">On this site</div><h2>Handbooks and class content</h2><div class="mb-grid">{site}</div></section>
</div></section>"""


ART = re.compile(r'href="https://claude\.ai/artifact/([A-Za-z0-9]+)(#[^"]*)?"')


def run(out):
    """Point every public claude.ai artifact link at the members library. Returns the number of links changed."""
    n = 0
    for root, dirs, files in os.walk(out):
        rel_root = os.path.relpath(root, out)
        if rel_root.split(os.sep)[0] in (".git", "tools", "node_modules", "data-science", "handbook"):
            dirs[:] = []; continue
        for f in files:
            if not f.endswith(".html") or (rel_root == "." and f == "members.html"):
                continue
            p = os.path.join(root, f)
            s = open(p, encoding="utf-8").read()
            up = "../" * (0 if rel_root == "." else rel_root.count(os.sep) + 1)
            def sub(m):
                return f'href="{up}members.html#a-{m.group(1)}"' if m.group(1) in IDS else f'href="{up}members.html"'
            t, k = ART.subn(sub, s)
            if k:
                # these now open a page on this site, so drop the "new tab" marker that came with the external link
                t = re.sub(r'(href="(?:\.\./)*members\.html[^"]*")\s+target="_blank"(\s+rel="noopener(?: noreferrer)?")?', r"\1", t)
                open(p, "w", encoding="utf-8").write(t)
                n += k
    return n
