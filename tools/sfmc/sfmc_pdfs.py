"""Creates the SFMC handbook PDFs in handbook/sfmc/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sfmc_build import *
from sfmc_content import MODULES

def write(jobs):
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        pg = b.new_page()
        for fn, cov, body, title in jobs:
            pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>{cov}{body}</body></html>', wait_until="load")
            pg.pdf(path=os.path.join(OUT, fn), format="A4", print_background=True, display_header_footer=True, header_template="<span></span>", footer_template=FOOT, margin={"top":"16mm","bottom":"18mm","left":"15mm","right":"15mm"})
            print("built", fn)
        b.close()

def intro():
    return ('<h1>Start here</h1><p>Salesforce Marketing Cloud (SFMC) is a platform for email, mobile, journeys and automation. Marketing Cloud Engagement is the product most SFMC developers and administrators work in. Related Salesforce products (Marketing Cloud Personalization, Marketing Cloud Intelligence, Data Cloud and editions such as Growth and Advanced) have their own names, licences and features. Check every product, edition and feature on Salesforce\'s official pages before you promise it to a customer.</p>'
            '<h2>How to learn with this handbook</h2><ol><li>Read the module, then the topic, in order.</li><li>Do the exercise on paper or with sample files.</li><li>Use an SFMC sandbox or test business unit for labs marked "account".</li><li>Answer the interview question out loud.</li></ol>')

def run():
    cov = lambda k, t, s: cover(k, t, s)
    mods = "".join(module_block(n, t, lvl, s, tps) for n, t, lvl, s, tps in MODULES)
    master = intro() + mods + labs_block()
    sql = [m for m in MODULES if m[0] == 6][0]
    amp = [m for m in MODULES if m[0] in (8, 9, 10)]
    jb = [m for m in MODULES if m[0] in (11, 12)]
    sql_b = module_block(6, sql[1], sql[2], sql[3], sql[4]) + '<h2>Quick reference: SQL in SFMC</h2><table><tr><th>Area</th><th>Items</th></tr>' + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in QUICK[:1]) + '</table>'
    amp_b = "".join(module_block(n, t, l, s, tp) for n, t, l, s, tp in amp if n in (8, 9, 10)) + '<h2>Quick reference: AMPscript</h2><table><tr><th>Area</th><th>Items</th></tr>' + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in QUICK[1:2]) + '</table>'
    jb_b = "".join(module_block(n, t, l, s, tp) for n, t, l, s, tp in jb) + '<h2>Quick reference: Journey Builder and Automation Studio</h2><table><tr><th>Area</th><th>Items</th></tr>' + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in [QUICK[3], QUICK[4]]) + '</table>'
    interview = '<h1>Interview questions</h1><p>The full question bank from the master prompt. Each question is linked to the module that teaches it. Model answers are added in the next batch; use the module topic to build your answer.</p>' + "".join(
        f'<h2>{E(g)}</h2><ol>' + "".join(f"<li>{E(q)}</li>" for q in qs) + '</ol>' for g, qs in INTERVIEW)
    cap = '<h1>Capstone projects</h1><p>Eight projects. Each must include the sections below and a demo video. The full workbook with templates and rubrics follows in the next batch.</p>' + "".join(
        f'<h2>{E(t)}</h2><p>{E(d)}</p>' for t, d in CAPSTONES) + '<h2>Every project must include</h2><ol>' + "".join(f"<li>{E(s)}</li>" for s in CAP_SECTIONS) + '</ol>'
    road = '<h1>12-month learning roadmap</h1><p>A realistic plan for a beginner studying part time. Adjust the hours to your time. The programme makes no promise of employment or any salary.</p><table><tr><th>Stage</th><th>Topics</th><th>Study time</th><th>Practical milestone</th><th>Assessment</th></tr>' + "".join(
        f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td></tr>" for a, b, c, d, e in ROADMAP) + '</table>'
    quick = '<h1>Quick reference</h1><table><tr><th>Area</th><th>Items</th></tr>' + "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in QUICK) + '</table>'
    write([
        ("SFMC-01-Master-Handbook.pdf", cov("Master handbook", "Salesforce Marketing Cloud: the complete handbook", "All 28 modules with every topic, the product naming notes and the practical lab list."), master, "SFMC Master Handbook"),
        ("SFMC-02-SQL-Handbook.pdf", cov("Handbook 2", "SQL for Salesforce Marketing Cloud", "SQL fundamentals, joins, aggregates, data views and the code examples explained line by line."), sql_b, "SQL for SFMC"),
        ("SFMC-03-AMPscript-and-HTML-Handbook.pdf", cov("Handbook 3", "AMPscript, HTML email and CloudPages basics", "Syntax, variables, data extension lookups, responsive email and the code explained line by line."), amp_b, "AMPscript and HTML"),
        ("SFMC-04-Journey-and-Automation-Handbook.pdf", cov("Handbook 4", "Journey Builder and Automation Studio", "Entry sources, activities, splits, re-entry, testing, activities, scheduling and monitoring."), jb_b, "Journey Builder and Automation Studio"),
        ("SFMC-05-Interview-Handbook.pdf", cov("Handbook 5", "SFMC interview question bank", "Technical, scenario and behavioural questions from the master prompt, linked to the modules that teach them."), interview, "SFMC interviews"),
        ("SFMC-06-Capstone-Projects.pdf", cov("Handbook 6", "Capstone projects and portfolio", "Eight project briefs and the portfolio standard."), cap, "SFMC capstones"),
        ("SFMC-07-12-Month-Roadmap.pdf", cov("Handbook 7", "12-month SFMC learning roadmap", "Seven stages with study time, milestones and assessments."), road, "SFMC roadmap"),
        ("SFMC-08-Quick-Reference.pdf", cov("Handbook 8", "SFMC quick reference", "SQL, AMPscript, data views, Journey Builder, Automation Studio, deliverability, APIs and troubleshooting."), quick, "SFMC quick reference"),
    ])

if __name__ == "__main__":
    run()
