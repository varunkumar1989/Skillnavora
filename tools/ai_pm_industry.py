"""AI Product Management: industry research page (research/*.csv) plus the release management section.

Built from the research files so every number matches the data. Requirements come from search summaries;
the page says so, and lists what could not be verified. Adds to the AI PM programme; no existing chapter changes.
"""
import csv, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ai_pm_interview
E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "ai-pm-industry-research.html"
# job postings whose source link returned "page not found" when re-checked (the record stays; the dead link is not shown)
CLOSED = {"J05", "J14", "J17", "J18", "J19", "J20", "J22"}
CLOSED_CHECKED = "12 Nov 2026"

def _read(name):
    with open(os.path.join(ROOT, "research", name), encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _table(headers, rows):
    th = "".join(f"<th>{E(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div style="overflow-x:auto"><table class="ap-t"><tr>{th}</tr>{body}</table></div>'

def build(page, uhero, out):
    courses = _read("part1_courses.csv")
    jobs = _read("part2_job_descriptions.csv")
    skills = _read("part3_skill_matrix.csv")
    with_req = [j for j in jobs if "requirements not shown" not in j["requirements_stated"].lower() and "title only" not in j["requirements_stated"].lower()]
    css = """<style>
.ap-t{width:100%;border-collapse:collapse;font-size:14px;min-width:560px}.ap-t th,.ap-t td{border:1px solid var(--line);padding:8px 9px;text-align:left;vertical-align:top}
.ap-t th{background:var(--surface)}.ap-note{background:#fff8e6;border:1px solid #f0d78c;padding:12px 14px;border-radius:10px;margin:14px 0;color:#3d2a00}
.ap-sec{margin-top:30px}.ap-kpi{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}.ap-kpi div{border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:150px;background:var(--surface)}
.ap-kpi b{display:block;font:800 26px var(--display)}
</style>"""
    kpi = (f'<div class="ap-kpi"><div><b>{len(courses)}</b>institutional courses recorded</div>'
           f'<div><b>{len(jobs)}</b>job records</div><div><b>{len(with_req)}</b>with stated requirements</div>'
           f'<div><b>{len(jobs)-len(with_req)}</b>title-only (excluded from counts)</div></div>')
    course_rows = [[E(c["institution"]), E(c["course"]), E(c["duration"] or "not stated"), f'<span>{E(c["evidence_status"].split(" - ")[0])}</span>',
                    f'<a href="{E(c["official_url"])}" target="_blank" rel="noopener">Official page ↗</a>'] for c in courses]
    skill_rows = [[E(s["skill"]), E(s["records_mentioning"]), E(s["share_of_records_with_requirements"])] for s in skills]
    job_rows = [[E(j["id"]), E(j["company"]), E(j["job_title"]), E(j["location"] or "not shown"), E(j["role_family"]),
                 E(j["requirements_stated"]), (f'<span class="meta">Posting closed (checked {CLOSED_CHECKED})</span>' if j["id"] in CLOSED else f'<a href="{E(j["source_url"])}" target="_blank" rel="noopener">Source ↗</a>'), E(j["evidence_level"].split(" - ")[0])]
                for j in jobs]
    body = f"""{css}
<section style="padding-top:28px"><div class="wrap">
<div class="ap-note"><b>How to read this.</b> The job figures come from search summaries, not full postings: the career sites could not be opened from the research session. Counts exclude title-only records. Course fields are marked as found, partial or not found; nothing has been filled in with guesses.</div>
{kpi}
<h2 class="sec-h ap-sec">Institutional courses</h2>
{_table(["Institution","Course","Duration","Syllabus status","Official link"], course_rows)}
<h2 class="sec-h ap-sec">Skills employers name most</h2>
<p class="sub">Counts are records (out of {len(with_req)} with stated requirements) whose summary names the skill.</p>
{_table(["Skill","Records","Share of records with requirements"], skill_rows)}
<h2 class="sec-h ap-sec">Release management (gap closed)</h2>
<p class="sub">Listed in the course outline, not taught anywhere on the site before this page. Definitions below are general practice, not quoted from any employer.</p>
<div class="ap-note" style="background:#f5f3ff;border-color:#e3dff5;color:#1d1b2e">
<p><b>Release management</b> is the planning and control of when a product change reaches users: scope the release, test it, roll it out in stages, watch the metrics, and roll back if needed.</p>
<ol><li><b>Scope:</b> agree the release contents and the release date with engineering.</li>
<li><b>Verify:</b> testing, sign-off, and a go/no-go check against the acceptance criteria.</li>
<li><b>Roll out:</b> staged release (for example 5%, 25%, 100%) with a feature flag where possible.</li>
<li><b>Monitor:</b> error rates, latency and the business metrics you set before release.</li>
<li><b>Recover:</b> a rollback or fix plan written before the release, not after.</li>
<li><b>Communicate:</b> release notes for users and support, and a status note for stakeholders.</li></ol>
<p><b>Practice:</b> write a one-page release plan for a change in a product you use, including the rollout stages, the metrics you would watch and the rollback trigger.</p>
</div>
{ai_pm_interview.section()}
<h2 class="sec-h ap-sec">Job records</h2>
{_table(["ID","Company","Title as listed","Location","Role family","Requirements stated (summary)","Source","Evidence"], job_rows)}
</div></section>"""
    page(PAGE, "AI Product Management: industry research and skills · SkillNavora",
         "What institutional courses and job descriptions show employers want from product managers and AI product managers, with the skill matrix and the release management gap.",
         uhero("AI Product Management · Research", 'Industry <span class="g">research</span>', "Courses, job records and the skills employers name most, from research completed in November 2026. Figures come from search summaries and are labelled as such.") + body, "programme-pm.html")
