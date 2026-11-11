"""All handbook PDFs as two artifacts (the folder is over the 256 MB per-version limit).
Writes manifest.json (file lists with sizes and page counts) and one HTML page per artifact part."""
import json, os, sys
import pymupdf
ROOT = "/home/user/skillnavora"; HB = os.path.join(ROOT, "handbook")
OUT = sys.argv[1]; PARTS = sys.argv[2]
LIMIT = 130 * 1048576  # two parts, each under the 256 MB limit
files = []
for dp, _, fns in os.walk(HB):
    for fn in fns:
        if fn.lower().endswith(".pdf"):
            p = os.path.join(dp, fn); rel = os.path.relpath(p, ROOT)
            files.append((rel, os.path.getsize(p)))
files.sort()
parts = [[]]; size = 0
for rel, sz in files:
    if size + sz > LIMIT and parts[-1]: parts.append([]); size = 0
    parts[-1].append((rel, sz)); size += sz
man = []
for i, part in enumerate(parts, 1):
    entries = []
    for rel, sz in part:
        try: pages = pymupdf.open(os.path.join(ROOT, rel)).page_count
        except Exception: pages = None
        entries.append({"rel": rel, "name": rel[len("handbook/"):], "safe": rel.replace("/", "__"), "mb": round(sz / 1048576, 2), "pages": pages,
                        "folder": os.path.dirname(rel[len("handbook/"):]) or "(top level)"})
    man.append({"part": i, "parts": len(parts), "entries": entries, "mb": round(sum(s for _, s in part) / 1048576, 1)})
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), ensure_ascii=False)
print("files", len(files), "parts", len(parts), [(m["part"], len(m["entries"]), m["mb"]) for m in man])
