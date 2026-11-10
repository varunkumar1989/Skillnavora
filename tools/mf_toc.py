"""Reads the contents links inside each Master Freelancing PDF and writes tools/mf_toc.json:
for every PDF, the chapter titles and the page each one starts on. gen_site.py uses it to make profession names clickable.
Run after rebuilding a textbook:  python3 tools/mf_toc.py"""
import json, os, glob, pymupdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}
for path in sorted(glob.glob(os.path.join(ROOT, "handbook", "Master-Freelancing-*.pdf"))):
    d = pymupdf.open(path); items = []
    for p in d:
        for l in p.get_links():
            if l.get("kind") in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED) and l.get("page", -1) >= 0 and p.number < 6:
                t = " ".join(p.get_textbox(l["from"]).split())
                if t:
                    first = d[l["page"]].get_text()
                    lead = ""
                    blocks = [" ".join(b[4].split()) for b in d[l["page"]].get_text("blocks")]
                    for bi, b in enumerate(blocks):
                        if (b == t or b.endswith(" " + t)) and bi + 1 < len(blocks):
                            j = bi + 1
                            if "What the profession means" in blocks[bi + 1:bi + 4]:
                                j = blocks.index("What the profession means", bi + 1) + 1
                            lead = blocks[j] if j < len(blocks) else ""
                            if lead and not lead.endswith(".") and j + 1 < len(blocks): lead += " " + blocks[j + 1]
                            break
                    items.append({"id": l.get("nameddest", ""), "title": t, "page": l["page"] + 1, "profession": "What the profession means" in first, "lead": lead[:220]})
    seen = set(); clean = []
    for i in items:
        if (i["id"] or i["title"]) not in seen: seen.add(i["id"] or i["title"]); clean.append(i)
    out["handbook/" + os.path.basename(path)] = clean
json.dump(out, open(os.path.join(ROOT, "tools", "mf_toc.json"), "w"), indent=1, ensure_ascii=False)
for k, v in out.items(): print(k, len(v), v[:2])
