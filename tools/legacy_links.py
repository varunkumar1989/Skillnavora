"""After the site is built: point every old Free resources anchor (resources.html#pm, #data, #op-fde ...)
at its one home on the Learning platform. Current Free resources tabs (programmes, tools, context, evals, rag)
and the page's own anchors (#more, #news) are left alone. Keeps any ../ prefix on nested pages."""
import os, re, json
import restabs

CURRENT = {"programmes", "tools", "context", "evals", "rag", "more", "news"}
PAT = re.compile(r'href="((?:\.\./)*|/)resources\.html#([^"]+)"')


def run(out):
    n = 0
    for root, _, files in os.walk(out):
        if any(part in root for part in ("/handbook", "/.git", "/node_modules")):
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            s = open(p, encoding="utf-8").read()
            def sub(m):
                key = m.group(2)
                if key in CURRENT or key not in restabs.LEGACY:
                    return m.group(0)
                return f'href="{m.group(1)}{restabs.LEGACY[key]}"'
            t, k = PAT.subn(sub, s)
            if t != s:
                open(p, "w", encoding="utf-8").write(t)
                n += k
    return n
