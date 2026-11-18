"""Final SEO pass, run at the end of gen_site.py after every page (from every generator) is written.

1. sitemap.xml lists every public page (skips pages marked noindex and private folders).
2. Pages without a search description get one, taken from the page's first paragraph.
3. Pages without a social share image get the brand image and Open Graph / Twitter tags.
4. The three programme pages get Course structured data (name, description, provider, fee) for Google.
5. The home page gets Organization structured data.
Safe to run repeatedly: it only adds what is missing."""
import datetime, html, json, os, re, subprocess

DOMAIN = "https://www.skillnavora.in"
OG = f"{DOMAIN}/assets/og.png"
SKIP_DIRS = {".git", "tools", "functions", "node_modules", "assets", "supabase", "whatsapp-agent", "research"}
SKIP_FILES = {"404.html", "tests.html"}
SKIP_PARTS = ("/downloads/",)          # downloadable starter projects, not pages for search
AUTO = 'data-seo="auto"'                 # marks descriptions written here, so later runs can improve them
NOT_A_SUMMARY = re.compile(r"^(tap|fill|choose|click|describe|formula|hypothesis|simulate|select|drag|watch|type|enter)\b|hypothetical|illustrative|invented|change(s)? (often|frequently)|not (real|screenshots|transcripts|research)", re.I)
NOINDEX = re.compile(r'<meta[^>]+name="robots"[^>]+noindex', re.I)
E = lambda s: html.escape(str(s), quote=True)


def pages(out):
    for root, dirs, files in os.walk(out):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                yield p, os.path.relpath(p, out).replace(os.sep, "/")


def clean_url(rel):
    if rel == "index.html":
        return DOMAIN + "/"
    if rel.endswith("/index.html"):
        return f"{DOMAIN}/{rel[:-len('index.html')]}"
    return f"{DOMAIN}/{rel[:-5]}"          # Cloudflare serves /page for page.html


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def describe(page, title, rel=""):
    """A one-sentence description: from the title for handbook modules and labs, else the first paragraph that reads
    like a summary (not an instruction or a disclaimer), else from the title."""
    topic = title.split(" · ")[0].strip()
    if rel.startswith("handbooks/pm/"):
        return f"{topic} in the free SkillNavora Product Management Master Handbook: clear explanations, worked examples and practice."
    if rel.startswith("labs/"):
        return f"Interactive practice lab: {topic}. Learn product management by doing, free on SkillNavora."
    body = page.split("<body", 1)[-1]
    body = re.sub(r"<(script|style|nav|header)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.S | re.I):
        t = text_of(m.group(1))
        if len(t) >= 60 and not NOT_A_SUMMARY.search(t):
            return (t[:152].rsplit(" ", 1)[0] + "…") if len(t) > 155 else t
    return f"{topic}: free study material on SkillNavora, with lessons, guides and AI-first programs."


def courses(out):
    js = ("const src=require('fs').readFileSync(process.argv[1],'utf8');"
          "process.stdout.write(JSON.stringify(new Function(src+';return COURSES')()));")
    try:
        return json.loads(subprocess.run(["node", "-e", js, os.path.join(out, "assets", "config.js")],
                                         capture_output=True, text=True, check=True).stdout)
    except Exception:
        return []


def course_ld(c):
    price = re.sub(r"[^\d]", "", str(c.get("feeINR", "")))
    data = {"@context": "https://schema.org", "@type": "Course", "name": c["name"],
            "description": c.get("tagline") or c.get("short") or c["name"],
            "url": f"{DOMAIN}/{c['page'][:-5]}",
            "provider": {"@type": "Organization", "name": "SkillNavora", "sameAs": DOMAIN},
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                                  "description": f"{c.get('duration', '')}, {c.get('format', 'live online classes')}".strip(", ")}}
    if price:
        data["offers"] = {"@type": "Offer", "price": price, "priceCurrency": "INR", "category": "Paid",
                          "url": f"{DOMAIN}/{c['page'][:-5]}"}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


ORG_LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "EducationalOrganization", "name": "SkillNavora", "url": DOMAIN,
    "logo": f"{DOMAIN}/assets/skillnavora-lockup.png",
    "sameAs": ["https://www.linkedin.com/company/skillnavora", "https://www.instagram.com/skillnavora/",
               "https://www.youtube.com/@SkillNavora", "https://x.com/skillnavora"]}) + "</script>"


def run(out):
    stats = {"sitemap": 0, "descriptions": 0, "share_tags": 0, "course_data": 0}
    by_page = {c["page"]: c for c in courses(out) if c.get("page")}
    urls = []
    for path, rel in sorted(pages(out), key=lambda x: x[1]):
        if rel in SKIP_FILES or any(x in "/" + rel for x in SKIP_PARTS) or rel.endswith("-demo.html"):
            continue
        page = open(path, encoding="utf-8", errors="ignore").read()
        if "<head" not in page:
            continue
        if NOINDEX.search(page):
            continue
        urls.append(clean_url(rel))
        m = re.search(r"<title>(.*?)</title>", page, re.S | re.I)
        title = text_of(m.group(1)) if m else "SkillNavora"
        add = []
        desc_m = re.search(r'<meta\s+name="description"\s+(?:data-seo="auto"\s+)?content="([^"]*)"', page, re.I)
        desc = desc_m.group(1) if desc_m and len(desc_m.group(1)) >= 20 and AUTO not in desc_m.group(0) else ""
        if not desc:
            desc = describe(page, title, rel)
            new_tag = f'<meta name="description" {AUTO} content="{E(desc)}"'
            if desc_m:
                if desc_m.group(0) != new_tag:
                    page = page.replace(desc_m.group(0), new_tag, 1)
                    open(path, "w", encoding="utf-8").write(page)
            else:
                add.append(new_tag + ">")
            stats["descriptions"] += 1
        if "og:image" not in page:
            tags = []
            if "og:title" not in page:
                tags.append(f'<meta property="og:title" content="{E(title)}">')
            if "og:description" not in page:
                tags.append(f'<meta property="og:description" content="{E(desc)}">')
            tags += [f'<meta property="og:type" content="website">',
                     f'<meta property="og:url" content="{clean_url(rel)}">',
                     f'<meta property="og:image" content="{OG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">']
            if "twitter:card" not in page:
                tags.append(f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG}">')
            add += tags
            stats["share_tags"] += 1
        if rel in by_page:
            ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
            existing = None
            if ld:
                try: existing = json.loads(ld.group(1))
                except Exception: existing = None
            if isinstance(existing, dict) and existing.get("@type") == "Course":
                # Course data already there (from gen_site): add the page address and the fee if missing.
                fresh = json.loads(course_ld(by_page[rel])[len('<script type="application/ld+json">'):-len("</script>")])
                changed = False
                for k in ("url", "offers"):
                    if k not in existing and k in fresh:
                        existing[k] = fresh[k]; changed = True
                if changed:
                    page = page.replace(ld.group(0), '<script type="application/ld+json">' + json.dumps(existing, ensure_ascii=False) + "</script>", 1)
                    open(path, "w", encoding="utf-8").write(page)
                    stats["course_data"] += 1
            else:
                add.append(course_ld(by_page[rel]))
                stats["course_data"] += 1
        if rel == "index.html" and "EducationalOrganization" not in page:
            add.append(ORG_LD)
        if add:
            page = page.replace("</head>", "\n".join(add) + "\n</head>", 1)
            open(path, "w", encoding="utf-8").write(page)
    today = datetime.date.today().isoformat()
    with open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{E(u)}</loc><lastmod>{today}</lastmod></url>\n")
        f.write("</urlset>\n")
    stats["sitemap"] = len(urls)
    return stats
