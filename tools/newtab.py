"""Run after the site is generated: every external link opens in a new tab (target="_blank", rel="noopener").
Covers static pages that are not produced by gen_site.py (the interactive PM handbook and the academy)."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWN = re.compile(r'^https?://(www\.)?(skillnavora\.in|skillnavora\.pages\.dev)', re.I)
A = re.compile(r'<a\s[^>]*>')

def fix_tag(tag):
    h = re.search(r'href="([^"]+)"', tag)
    if not h or not h.group(1).startswith(("http://", "https://")) or OWN.match(h.group(1)): return tag
    if 'target=' in tag: return tag
    return tag[:-1] + ' target="_blank" rel="noopener">' if tag.endswith(">") else tag

def run():
    n = 0
    files = glob.glob(os.path.join(ROOT, "handbooks/pm/*.html")) + [os.path.join(ROOT, "ai-academy-interactive.html")]
    for f in files:
        if not os.path.exists(f): continue
        s = open(f, encoding="utf-8").read()
        new = A.sub(lambda m: fix_tag(m.group(0)), s)
        if new != s: open(f, "w", encoding="utf-8").write(new); n += 1
    return n

if __name__ == "__main__":
    print("pages updated:", run())
