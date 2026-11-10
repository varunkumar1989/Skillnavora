"""One PDF per SFMC module (detailed lessons + every subtopic explained) and a merged complete handbook."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sfmc_build import E, CSS, FOOT, OUT, cover, topic, LABS, CAPSTONES, CAP_SECTIONS, INTERVIEW, ROADMAP, QUICK
from sfmc_content import MODULES
from sfmc_subtopics import SUB
from sfmc_notes_a import NA
from sfmc_notes_b import NB
from sfmc_notes_c import NC
NOTES = {**NA, **NB, **NC}

def module_body(num, title, level, summary, topics):
    out = [f'<h1>Module {num}: {E(title)}</h1><p><b>Level:</b> {E(level)}. {E(summary)}</p>',
           '<h2>Contents</h2><ol>' + "".join(f"<li>{E(sec)}</li>" for sec, _ in SUB[num]) + '</ol>']
    if topics:
        out.append('<h2>Detailed lessons</h2>' + "".join(topic(t, num) for t in topics))
    for sec, items in SUB[num]:
        code = sec.split()[0]
        out.append(f'<h2>{E(sec)}: every topic explained</h2>' + "".join(f'<p><b>{E(it)}.</b> {E(nt)}</p>' for it, nt in zip(items, NOTES[code])))
    if num == 25:
        out.append('<h2>Lab list</h2><table><tr><th>Lab</th><th>Title</th><th>Requirement</th></tr>' + "".join(f"<tr><td>{E(c)}</td><td>{E(n)}</td><td>{'Needs a provisioned SFMC account' if k=='account' else 'Simulated or paper practice'}</td></tr>" for c, n, k in LABS) + '</table>')
    if num == 26:
        out.append('<h2>Project briefs</h2>' + "".join(f'<h3>{E(t)}</h3><p>{E(d)}</p>' for t, d in CAPSTONES) + '<h3>Every project must include</h3><ol>' + "".join(f"<li>{E(s)}</li>" for s in CAP_SECTIONS) + '</ol>')
    if num == 27:
        out.append("".join(f'<h3>{E(g)}</h3><ol>' + "".join(f"<li>{E(q)}</li>" for q in qs) + '</ol>' for g, qs in INTERVIEW))
    if num == 28:
        out.append('<h2>12-month roadmap</h2><table><tr><th>Stage</th><th>Topics</th><th>Study time</th><th>Milestone</th><th>Assessment</th></tr>' + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td></tr>" for a, b, c, d, e in ROADMAP) + '</table>')
    return "".join(out)

def run():
    from playwright.sync_api import sync_playwright
    import pymupdf
    os.makedirs(OUT, exist_ok=True)
    files = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        pg = b.new_page()
        for num, title, level, summary, topics in MODULES:
            fn = f"SFMC-Module-{num:02d}.pdf"
            n_sub = sum(len(i) for _, i in SUB[num])
            cov = cover(f"Module {num} handbook", f"Module {num}: {title}", f"{len(SUB[num])} sections, {n_sub} topics explained, plus the detailed lessons, examples, exercises and official links.")
            pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><title>{E(fn)}</title><style>{CSS}</style></head><body>{cov}{module_body(num, title, level, summary, topics)}</body></html>', wait_until="load")
            pg.pdf(path=os.path.join(OUT, fn), format="A4", print_background=True, display_header_footer=True, header_template="<span></span>", footer_template=FOOT, margin={"top":"16mm","bottom":"18mm","left":"15mm","right":"15mm"})
            files.append((fn, f"Module {num}: {title}"))
        b.close()
    full = pymupdf.open(); toc = []
    order = ["SFMC-01-Master-Handbook.pdf"] + [f for f, _ in files] + ["SFMC-02-SQL-Handbook.pdf", "SFMC-03-AMPscript-and-HTML-Handbook.pdf", "SFMC-04-Journey-and-Automation-Handbook.pdf", "SFMC-05-Interview-Handbook.pdf", "SFMC-06-Capstone-Projects.pdf", "SFMC-07-12-Month-Roadmap.pdf", "SFMC-08-Quick-Reference.pdf"]
    for fn in order:
        d = pymupdf.open(os.path.join(OUT, fn)); toc.append([1, fn.replace(".pdf", "").replace("-", " "), full.page_count + 1]); full.insert_pdf(d)
    full.set_toc(toc); full.save(os.path.join(OUT, "SFMC-Complete-Handbook.pdf"), garbage=4, deflate=True)
    print("modules", len(files), "complete handbook pages", full.page_count)

if __name__ == "__main__":
    run()
