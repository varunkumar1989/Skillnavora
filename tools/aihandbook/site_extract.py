"""Reads the SkillNavora pages linked from the handbook and extracts what they already teach.

For each page: the title, and for up to N sections (h2/h3) the heading plus the first sentence
of the text under it. The output is grounded in the site, so the handbook can say
"the lesson covers X" with a link. Run:  python3 tools/aihandbook/site_extract.py
Writes tools/aihandbook/site_extract.json
"""
import html, json, os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import content as C

MAX_SECTIONS = 10


class Pages(HTMLParser):
    """Collects headings (h2/h3) and the first sentence of the paragraph that follows each."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.sections = []; self._cur = None; self._in = None; self._want_p = False; self._buf = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "nav", "header", "footer"):
            self._skip += 1
        if self._skip:
            return
        if tag == "title":
            self._in = "title"; self._buf = []
        elif tag in ("h2", "h3"):
            self._in = "h"; self._buf = []; self._level = tag
        elif tag in ("p", "li") and self._cur is not None and not self._cur.get("text") and self._want_p:
            self._in = "p"; self._buf = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "nav", "header", "footer") and self._skip:
            self._skip -= 1; return
        if self._skip:
            return
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        if tag == "title" and self._in == "title":
            self.title = text; self._in = None
        elif tag in ("h2", "h3") and self._in == "h":
            if text and len(self.sections) < MAX_SECTIONS * 3:
                self._cur = {"heading": text, "level": self._level, "text": ""}; self.sections.append(self._cur)
                self._want_p = True
            self._in = None
        elif tag in ("p", "li") and self._in == "p":
            first = first_sentence(text)
            if first and self._cur is not None and not self._cur["text"]:
                self._cur["text"] = first
            self._want_p = False; self._in = None

    def handle_data(self, data):
        if self._skip:
            return
        if self._in in ("title", "h", "p"):
            self._buf.append(data)


def first_sentence(text):
    if len(text) < 40 or text.lower().startswith(("open ", "note:", "tip:", "source:")):
        return ""
    m = re.match(r"(.{40,300}?[.!?])(\s|$)", text)
    s = (m.group(1) if m else text[:220]).strip()
    return s


def extract(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    p = Pages(); p.feed(raw)
    secs = [s for s in p.sections if s["text"] or s["level"] == "h2"][:MAX_SECTIONS]
    return {"title": re.sub(r"\s*[·|]\s*SkillNavora$", "", p.title), "sections": secs}


def pdf_info(path):
    import subprocess
    try:
        pages = re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout)
        txt = subprocess.run(["pdftotext", "-f", "1", "-l", "1", path, "-"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return {"title": os.path.basename(path), "sections": [], "pages": None}
    sents = [x for x in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", txt)) if len(x) > 50 and not re.search(r"\b[A-Z] [A-Z] [A-Z]\b", x)]
    name = os.path.basename(path).replace(".pdf", "").replace("_", " ").replace("-", " ")
    return {"title": name, "pages": int(pages.group(1)) if pages else None,
            "sections": [{"heading": "Opening of the PDF", "level": "h2", "text": x[:260]} for x in sents[:3]]}


def all_paths():
    seen = []
    for k, (st, links) in C.COVERAGE.items():
        for _, u in links:
            f = u.split("#")[0]
            if f not in seen and os.path.exists(os.path.join(ROOT, f)) and f.endswith((".html", ".pdf")):
                seen.append(f)
    for s in C.SUBJECTS:
        for _, u in s["links"]:
            f = u.split("#")[0]
            if f.endswith(".html") and f not in seen and os.path.exists(os.path.join(ROOT, f)):
                seen.append(f)
    return seen


if __name__ == "__main__":
    out = {}
    for f in all_paths():
        full = os.path.join(ROOT, f)
        out[f] = pdf_info(full) if f.endswith(".pdf") else extract(full)
    path = os.path.join(HERE, "site_extract.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("pages", len(out), "sections", sum(len(v["sections"]) for v in out.values()), "->", path)
