import os, re
from . import extras
_D = os.path.dirname(os.path.abspath(__file__))

def load():
    """Return [{'n': 1, 'title':..., 'overview':..., 'topics': [(name, text), ...]}, ...] in order."""
    subs = []
    for f in sorted(x for x in os.listdir(_D) if re.fullmatch(r"c\d\.txt", x)):
        for line in open(os.path.join(_D, f), encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("@S|"):
                _, n, title, ov = line.split("|", 3)
                subs.append({"n": int(n), "title": title, "overview": ov, "topics": []})
            else:
                name, text = line.split(" :: ", 1)
                subs[-1]["topics"].append((name.strip(), text.strip()))
    return sorted(subs, key=lambda s: s["n"])

def load_detailed():
    """Subjects with detailed explanations: [{'n','title','overview','topics': [(name, short, detail)]}], in order.
    Every topic must have a detail line in aipm2/details/dNN.txt with the same name, in the same order."""
    subs = load()
    det = {}
    for f in sorted(x for x in os.listdir(os.path.join(_D, "details")) if re.fullmatch(r"d\d\d\.txt", x)):
        n = int(f[1:3])
        det[n] = []
        for line in open(os.path.join(_D, "details", f), encoding="utf-8"):
            line = line.rstrip("\n")
            if line.strip():
                name, text = line.split(" :: ", 1)
                det[n].append((name.strip(), text.strip()))
    out = []
    for s in subs:
        d = det.get(s["n"], [])
        if [x for x, _ in d] != [x for x, _ in s["topics"]]:
            raise ValueError(f"details out of step with topics in subject {s['n']}")
        out.append({**s, "topics": [(name, short, dt) for (name, short), (_, dt) in zip(s["topics"], d)]})
    return out


def pdf_name(n, title):
    """File name of a chapter PDF, e.g. AIPM2-01-Product-Management-Foundations.pdf"""
    return f"AIPM2-{n:02d}-" + "".join(c if c.isalnum() else "-" for c in title).strip("-").replace("--", "-") + ".pdf"
