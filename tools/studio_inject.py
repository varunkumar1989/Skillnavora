"""AI Studio on pages that don't load the main site script (lessons, handbooks, labs).

1. Builds assets/studio.js from the AI Studio block in assets/site.js, so both stay identical
   in behaviour (answers from knowledge_qa.json and content_index.json, links to pages and PDFs,
   Instagram fallback). The standalone copy works out the site root from its own address and
   brings its own light/dark colours, because lesson pages use a different stylesheet.
2. Adds <script src=".../assets/studio.js"> to every such page (idempotent).
Run by gen_site.py after the site is generated.
"""
import glob, hashlib, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "/* Ask AI side tab"
SKIP = ("handbooks/pm/downloads/", "handbooks/genai/hr-portal-demo.html")  # starter files and a demo app

ROOT_JS = r'''const R = (function () {
    const s = (document.currentScript && document.currentScript.src) || (document.querySelector('script[src*="assets/studio.js"]') || {}).src || "";
    return s ? s.replace(/assets\/studio\.js.*$/, "") : "/";
  })();
  const SITE = { instagramDM: "https://ig.me/m/skillnavora" };'''

EXTRA_CSS = r'''
/* Standalone AI Studio (lesson and handbook pages): own colours for light and dark */
#askai,#askai-tab{--surface:#ffffff;--ink:#0d1630;--mu:#55607a;--line:#e1e6f0;--bg:#f5f7fc;--brand:#6C4CF5;--on-brand:#ffffff;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@media (prefers-color-scheme: dark){html:not([data-theme="light"]) #askai{--surface:#0d1b18;--ink:#ebf6f3;--mu:#9fb6b1;--line:#1d3a36;--bg:#07100f;--brand:#54e0c4;--on-brand:#04211c}}
html[data-theme="dark"] #askai{--surface:#0d1b18;--ink:#ebf6f3;--mu:#9fb6b1;--line:#1d3a36;--bg:#07100f;--brand:#54e0c4;--on-brand:#04211c}
#askai,#askai *{box-sizing:border-box}
#askai{font-size:15px;line-height:1.5}
#askai .kicker{font:700 12px/1.2 inherit;letter-spacing:.14em;text-transform:uppercase;color:var(--brand)}
#askai .btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;font:600 13px/1.2 inherit;font-family:inherit;border-radius:99px;padding:7px 12px;cursor:pointer;border:1px solid var(--line);background:var(--surface);color:var(--ink);text-decoration:none}
#askai .btn-primary{background:var(--brand);border-color:var(--brand);color:var(--on-brand);padding:10px 14px;font-size:14px}
#askai .btn:hover{border-color:var(--brand)}
#askai a{color:var(--brand)}
#askai a.t{color:var(--ink)}
#askai .ig-dm{display:inline-block;padding:9px 14px;border-radius:10px;color:#fff!important;font-weight:600;text-decoration:none;background:linear-gradient(45deg,#f09433,#dc2743 50%,#bc1888)}
#askai textarea{width:100%}
#askai a.t b{font-size:15px;font-weight:700;line-height:1.3}
#askai a.t small{font-size:12.5px;line-height:1.35}
#askai h2{font-weight:800;letter-spacing:-.01em}
'''


def build():
    src = open(os.path.join(ROOT, "assets", "site.js"), encoding="utf-8").read()
    a = src.index(START)
    b = src.index("\n})();", a) + len("\n})();")
    block = src[a:b]
    old_r = 'const R = (window.SNsite && window.SNsite.R) || document.body.dataset.root || "";'
    assert block.count(old_r) == 1, "AI Studio block changed: update tools/studio_inject.py"
    block = block.replace(old_r, ROOT_JS)
    old_css = "document.head.appendChild(css);"
    assert block.count(old_css) == 1
    block = block.replace(old_css, "css.textContent += " + repr(EXTRA_CSS).replace("\\'", "'") + ";\n  " + old_css)
    out = ("/* AI Studio for lesson, handbook and lab pages. Generated from assets/site.js by tools/studio_inject.py;\n"
           "   do not edit by hand. */\n" + block + "\n")
    path = os.path.join(ROOT, "assets", "studio.js")
    open(path, "w", encoding="utf-8").write(out)
    return hashlib.md5(out.encode()).hexdigest()[:8]


def pages():
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        if rel.startswith(("node_modules/", ".git/")) or "/node_modules/" in rel or rel.startswith(SKIP): continue
        s = open(f, encoding="utf-8", errors="ignore").read()
        if "assets/site.js" in s or "</body>" not in s: continue
        if re.search(r'http-equiv="refresh"|location\.replace\(', s[:3000], re.I) and len(s) < 6000: continue  # redirect stubs
        yield f, rel, s


def inject():
    ver = build()
    n = 0
    # Remove the tag from redirect stubs added by earlier runs
    for f in glob.glob(os.path.join(ROOT, "*.html")):
        t = open(f, encoding="utf-8", errors="ignore").read()
        if "assets/studio.js" in t and len(t) < 6000 and re.search(r'http-equiv="refresh"|location\.replace\(', t[:3000], re.I):
            open(f, "w", encoding="utf-8").write(re.sub(r'<script src="[./]*assets/studio\.js\?v=[a-f0-9]+" defer></script>', "", t)); n += 1
    for f, rel, s in pages():
        prefix = "../" * rel.count("/")
        tag = f'<script src="{prefix}assets/studio.js?v={ver}" defer></script>'
        o = s
        s = re.sub(r'<script src="[./]*assets/studio\.js\?v=[a-f0-9]+" defer></script>', tag, s)
        if "assets/studio.js" not in s:
            s = s.replace("</body>", tag + "</body>", 1)
        if s != o:
            open(f, "w", encoding="utf-8").write(s); n += 1
    return n


if __name__ == "__main__":
    print("pages updated with AI Studio:", inject())
