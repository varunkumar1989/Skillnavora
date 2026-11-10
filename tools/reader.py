"""In-site document reader.
1. Writes assets/reader-groups.json: which PDFs belong together and their order, for Previous/Next.
2. Points every link to a handbook, class, brochure or data-science PDF at read.html?doc=... so the document
   opens inside the site (with Back, Previous and Next) instead of a new browser tab.
Run after the site is generated. External links are not changed (they keep opening in a new tab)."""
import glob, json, os, re
from urllib.parse import quote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = re.compile(r'^(handbook|classes|brochures|data-science/pdf)/[^?#]+\.pdf$', re.I)
SKIP_DIRS = ("node_modules", "/print/", "/.git/")

def group_of(p):
    name = p.split("/")[-1]
    if p.startswith("handbook/"):
        if name.startswith("Guide-"): return "guides"
        if re.match(r"Module-(2[4-9]|3[01])-", name): return "chapters"
        if name.startswith("Module-"): return "modules"
        return "handbook-library"
    if p.startswith("classes/"): return "classes"
    if p.startswith("brochures/"): return "brochures"
    parts = p.split("/")
    return "ds-" + (parts[2] if len(parts) > 3 else "root")

def build_groups():
    paths = []
    for pat in ["handbook/*.pdf", "classes/*.pdf", "brochures/*.pdf", "data-science/pdf/*.pdf", "data-science/pdf/*/*.pdf", "data-science/pdf/*/*/*.pdf"]:
        for f in glob.glob(os.path.join(ROOT, pat)):
            if os.path.isfile(f): paths.append(os.path.relpath(f, ROOT).replace(os.sep, "/"))
    groups, of = {}, {}
    for p in sorted(set(paths)):
        if not ALLOWED.match(p): continue
        g = group_of(p); groups.setdefault(g, []).append(p); of[p] = g
    return {"groups": groups, "of": of}

def rewrite_links(G):
    of = G["of"]; n = 0
    for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
        if any(x in f for x in SKIP_DIRS) or os.path.basename(f) == "read.html": continue
        s = open(f, encoding="utf-8", errors="replace").read()
        here = os.path.dirname(f)
        def fix(m):
            tag = m.group(0); h = re.search(r'href="([^"#?]+\.pdf)"', tag)
            if not h or re.match(r"^(https?:|mailto:|tel:)", h.group(1)): return tag
            if h.group(1).startswith("/"): rel = h.group(1).lstrip("/")
            else: rel = os.path.relpath(os.path.normpath(os.path.join(here, h.group(1))), ROOT).replace(os.sep, "/")
            if rel not in of: return tag
            to_read = os.path.relpath(os.path.join(ROOT, "read.html"), here).replace(os.sep, "/")
            new = tag.replace(h.group(0), f'href="{to_read}?doc={quote(rel)}"')
            return re.sub(r'\s+target="_blank"', "", new)
        new_s = re.sub(r"<a\s[^>]*>", fix, s)
        if new_s != s:
            open(f, "w", encoding="utf-8").write(new_s); n += 1
    return n

def run():
    G = build_groups()
    with open(os.path.join(ROOT, "assets", "reader-groups.json"), "w", encoding="utf-8") as fh:
        json.dump(G, fh, ensure_ascii=False, separators=(",", ":"))
    return len(G["of"]), rewrite_links(G)

if __name__ == "__main__":
    docs, pages = run()
    print("documents:", docs, "| pages updated:", pages)
