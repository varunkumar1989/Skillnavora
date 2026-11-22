"""Rebuilds assets/search-index.json from every public page, so site search finds lessons, handbook chapters and
guides as well as programme pages. Each entry: u (path), t (title), d (description), k (main headings from the page,
so searching for a topic finds the lesson that teaches it). Runs at the end of gen_site.py, after all pages exist.
Pages skipped: marked noindex, the search page itself, and private or demo pages (same rules as the sitemap)."""
import html, json, os, re
import seo_post as S

SKIP_EXTRA = {"search.html", "access.html", "login.html", "members.html", "admin.html", "teach.html", "buy.html",
              "lms.html", "thanks.html", "404.html"}
H = re.compile(r"<h[12][^>]*>(.*?)</h[12]>", re.S | re.I)


def entry(out, rel, src):
    if NOINDEX_RX.search(src[:4000]):
        return None
    t = re.search(r"<title>(.*?)</title>", src, re.S | re.I)
    title = html.unescape(t.group(1)).strip() if t else rel
    title = re.sub(r"\s*[·|]\s*SkillNavora$", "", title)
    m = re.search(r'<meta name="description" content="([^"]*)"', src, re.I)
    desc = html.unescape(m.group(1)).strip() if m else ""
    if not desc:
        desc = S.describe(src, title, rel)
    heads = []
    body = src.split("<body", 1)[-1]
    for h in H.finditer(body):
        x = S.text_of(h.group(1))
        if x and x not in heads and len(x) < 120:
            heads.append(x)
        if len(heads) >= 25:
            break
    u = "/" + ("" if rel == "index.html" else rel)
    e = {"u": u, "t": title, "d": desc}
    if heads:
        e["k"] = " · ".join(heads)[:600]
    return e


NOINDEX_RX = re.compile(r'<meta[^>]+name="robots"[^>]+noindex', re.I)


def run(out):
    entries = []
    for p, rel in S.pages(out):
        if os.path.basename(rel) in SKIP_EXTRA or any(part in rel for part in S.SKIP_PARTS):
            continue
        src = open(p, encoding="utf-8", errors="ignore").read()
        e = entry(out, rel, src)
        if e:
            entries.append(e)
    entries.sort(key=lambda x: x["u"])
    with open(os.path.join(out, "assets", "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))
    return {"entries": len(entries), "with_headings": sum(1 for x in entries if "k" in x)}
