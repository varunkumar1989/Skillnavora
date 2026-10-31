"""Run after the site is generated: every PM handbook page loads the details gate and locks until details are given."""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<script src="../../data-science/assets/gate.js?v=lock1"></script>'

def inject():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "handbooks/pm/*.html"))):
        s = open(f, encoding="utf-8").read(); o = s
        if "data-science/assets/gate.js" not in s: s = s.replace("</body>", TAG + "</body>", 1)
        if "data-gate-lock" not in s: s = re.sub(r"<body(?=[\s>])", '<body data-gate-lock="PM Master Handbook"', s, count=1)
        if s != o: open(f, "w", encoding="utf-8").write(s); n += 1
    return n
