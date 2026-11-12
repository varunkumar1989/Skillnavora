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
