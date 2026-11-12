"""Build the AI PM 2 chapter outputs: PDF per chapter, one complete PDF, and one artifact HTML per chapter.

Usage: python3 tools/aipm2_build.py OUT_DIR
  OUT_DIR/html/*.html   printable HTML (rendered to PDF with Chromium)
  OUT_DIR/artifacts/*.html  interactive chapter pages for publishing as artifacts
The PDFs are written to handbook/aipm2/ by render step (see aipm2_render.js).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aipm2_html as H
from aipm2_content import CHAPTERS, slug

def main(out):
    hdir, adir = os.path.join(out, "html"), os.path.join(out, "artifacts")
    os.makedirs(hdir, exist_ok=True); os.makedirs(adir, exist_ok=True)
    jobs = []
    for s in CHAPTERS:
        name = slug(s["n"], s["title"])
        p = os.path.join(hdir, name + ".html")
        open(p, "w", encoding="utf-8").write(H.document(f"AI PM 2 · {s['title']}", H.chapter_html(s)))
        jobs.append({"src": p, "pdf": name + ".pdf"})
        open(os.path.join(adir, name + ".html"), "w", encoding="utf-8").write(H.artifact_page(s))
    body = H.contents_page() + "".join(H.chapter_html(s, with_original=False) for s in CHAPTERS) + H.original_section()
    full = os.path.join(hdir, "AIPM2-Complete-Course.html")
    open(full, "w", encoding="utf-8").write(H.document("AI PM 2 · Complete course", body))
    jobs.append({"src": full, "pdf": "AIPM2-Complete-Course.pdf"})
    json.dump(jobs, open(os.path.join(out, "jobs.json"), "w"), indent=1)
    print("chapters", len(CHAPTERS), "pdf jobs", len(jobs))

if __name__ == "__main__":
    main(sys.argv[1])
