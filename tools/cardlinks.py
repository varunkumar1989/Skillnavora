"""Makes card titles clickable across the site.
A card is a <div> whose class contains "card". If its first h3/h4 title is plain text and the card has exactly one
link (href), the title is wrapped in that same link, so clicking the topic does what the card's button does.
Cards with several different links (for example a list of job portals) are left alone. Run after the site is generated."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ("/node_modules/", "/.git/", "/handbooks/pm/", "/data-science/", "/print/")
TAG = re.compile(r"<(/?)div\b[^>]*>", re.I)

def cards(s):
    """Yield (start, end) of each div with 'card' in its class, using a stack so nested divs are handled."""
    stack = []
    for m in TAG.finditer(s):
        if m.group(1):
            if stack:
                start, is_card = stack.pop()
                if is_card: yield start, m.end()
        else:
            cls = re.search(r'class="([^"]*)"', m.group(0))
            stack.append((m.start(), bool(cls and re.search(r"(^|[\s-])card(\s|$)|card\b", cls.group(1)))))

def fix(block):
    h = re.search(r"<(h[34])\b([^>]*)>(.*?)</\1>", block, re.S)
    if not h or "<a" in h.group(3) or "'+" in block or "${" in block: return block
    links = re.findall(r'<a\s[^>]*href="([^"]+)"[^>]*>', block)
    links = [u for u in links if not u.startswith(("#", "javascript:"))]
    if len(set(links)) != 1: return block
    tag = re.search(r'<a\s[^>]*href="' + re.escape(links[0]) + r'"[^>]*>', block).group(0)
    extra = ' target="_blank" rel="noopener"' if 'target="_blank"' in tag else ""
    inner = f'<a href="{links[0]}"{extra}>{h.group(3)}</a>'
    return block[:h.start(3)] + inner + block[h.end(3):]

def run():
    n_pages = n_cards = 0
    for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
        if any(x in f.replace(os.sep, "/") for x in SKIP): continue
        s = open(f, encoding="utf-8", errors="replace").read()
        out, changed = s, 0
        while True:  # one edit at a time, then re-scan, so positions of enclosing cards never go stale
            for a, b in cards(out):
                blk = out[a:b]; new = fix(blk)
                if new != blk:
                    out = out[:a] + new + out[b:]; changed += 1; break
            else:
                break
        if changed:
            open(f, "w", encoding="utf-8").write(out); n_pages += 1; n_cards += changed
    return n_pages, n_cards

if __name__ == "__main__": print(run())
