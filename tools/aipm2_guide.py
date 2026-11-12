"""Builds the standalone 'AI PM Master Guide' page (published as an Artifact) from tools/aipm2/*.txt.
Usage: python3 tools/aipm2_guide.py OUTPUT.html
"""
import html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aipm2
from aipm2 import extras
import aipm2_page
E = html.escape
SUBJECTS = aipm2.load()
SITE = "https://www.skillnavora.in/"

PRACTICE = {
 1: "Write a one-page job description for the PM of a product you use, then list three decisions that PM owns and three they only influence.",
 2: "Run five 20-minute interviews about one problem. Write the top three pains with a quote each and a hypothesis you could test this week.",
 3: "Score ten backlog ideas with RICE and again with ICE. Explain every place the rankings differ.",
 4: "Sketch a three-screen flow in Figma for one task, test it with three people, and record what confused them.",
 5: "Write a two-page PRD with user stories, Given/When/Then acceptance criteria and three edge cases for a feature you choose.",
 6: "Break one epic into stories small enough for a sprint, estimate them with planning poker and draft the sprint goal.",
 7: "Write SQL for a weekly signup-to-activation funnel and week-1 retention on a sample dataset, and state what decision each result supports.",
 8: "Define a north star and five input metrics for a product, with exact formulas and the guardrail for each.",
 9: "Build a small model of revenue, CAC, LTV and payback for a subscription product with best, base and worst cases.",
 10: "Call a public REST API in Postman, read the JSON response, and draw the client, server and database flow for that request.",
 11: "Train a simple classifier on a public dataset and report precision, recall and F1 at two thresholds. Say which one the business should pick.",
 12: "Compare two models on twenty of your own tasks, noting quality, latency and cost per task.",
 13: "Write a system prompt with a role, rules and JSON output, then version it and test five variations on a fixed set of inputs.",
 14: "Build a small RAG assistant over ten documents and measure retrieval precision and recall on twenty questions.",
 15: "Design an agent that books meetings. List its tools, permissions, approval points and what happens when a tool fails.",
 16: "Draw the architecture of an AI feature with model, retrieval, database, monitoring and fallback. Write the build, buy or partner decision for each part.",
 17: "Create a golden set of fifty cases for one AI feature, define a rubric, and score two prompt versions.",
 18: "Run a risk review for one AI feature covering privacy, bias, injection and misuse. Assign an owner and mitigation to each risk.",
 19: "Redesign one AI screen so it shows sources, admits uncertainty and lets the user undo and correct the output.",
 20: "Estimate unit economics for an AI feature: tokens per task, cost per task, price, margin and the usage level where it stops being profitable.",
 21: "Pick one tool per category (assistant, builder, automation, vector store, observability) and write when you would use it and when you would not.",
 22: "Map stakeholders for a launch, then write the executive update: decision needed, recommendation, risks, and next steps in under 200 words.",
 23: "Choose the specialisation you are targeting. List the five skills it weights most and your current gap on each.",
 24: "Teardown one product from this list using public sources: users, job, business model, metrics you would watch, and one change you would make.",
 25: "Pick one capstone and complete every item of the deliverable checklist. Present it in ten minutes.",
 26: "Take a real job description, extract the required skills, mark your gaps, and run two timed mock interviews on the weakest ones.",
}

def build():
    nav = "".join(f'<a href="#s{s["n"]:02d}" data-n="{s["n"]}"><span>{s["n"]:02d}</span>{E(s["title"])}</a>' for s in SUBJECTS)
    phases = "".join(
        f'<div class="ph"><h3>{E(name)}</h3><p>{", ".join(next(s["title"] for s in SUBJECTS if s["n"] == n) for n in ns)}</p></div>'
        for name, ns in extras.PHASES)
    secs = []
    for s in SUBJECTS:
        rows = "".join(f'<li data-t="{E((n + " " + t).lower(), quote=True)}"><h4>{E(n)}</h4><p>{E(t)}</p></li>' for n, t in s["topics"])
        extra = ""
        if s["n"] == 25:
            extra = '<h3>Every capstone must include</h3><ul class="chk">' + "".join(f"<li>{E(x)}</li>" for x in extras.CAPSTONE_CHECKLIST) + "</ul>"
        secs.append(f'<section class="subj" id="s{s["n"]:02d}"><header><p class="eyebrow">Subject {s["n"]:02d} of {len(SUBJECTS)} · {len(s["topics"])} topics</p><h2>{E(s["title"])}</h2><p class="ov">{E(s["overview"])}</p></header>'
                    f'<ol class="tp">{rows}</ol>{extra}<aside class="pr"><b>Practice</b><p>{E(PRACTICE[s["n"]])}</p></aside></section>')
    existing = "".join(f'<a class="ex" href="{SITE}{E(h)}" target="_blank" rel="noopener"><small>Subjects {E(sj)}</small><b>{E(t)}</b><span>{E(d)}</span></a>' for h, t, d, sj in aipm2_page.EXISTING)
    outcomes = "".join(f"<li>{E(o)}</li>" for o in extras.OUTCOMES)
    n_topics = sum(len(s["topics"]) for s in SUBJECTS)
    return f"""<title>AI PM Master Guide</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap">
<style>
/* Layout: sticky subject rail on the left (a horizontal scroller on phones), one long reading column on the right. */
:root{{--bg:#f7f8fa;--surface:#ffffff;--fg:#14212b;--muted:#5a6a77;--line:#dde3e8;--accent:#0b6e6e;--accent-soft:#e2f1f0;--note:#fff6dd;--note-line:#ecd58a;
--display:"Space Grotesk","Segoe UI",system-ui,sans-serif;--body:Inter,system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0f171d;--surface:#16212a;--fg:#e6edf2;--muted:#9aabb8;--line:#27363f;--accent:#4fc3bd;--accent-soft:#12302f;--note:#2b2514;--note-line:#5a4d1f;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f171d;--surface:#16212a;--fg:#e6edf2;--muted:#9aabb8;--line:#27363f;--accent:#4fc3bd;--accent-soft:#12302f;--note:#2b2514;--note-line:#5a4d1f;color-scheme:dark}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--fg);font:16px/1.6 var(--body);padding-block:0;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
h1,h2,h3,h4{{font-family:var(--display);line-height:1.2;text-wrap:balance;margin:0}}
a{{color:var(--accent)}}a:focus-visible,input:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.wrap{{max-width:1180px;margin:0 auto}}
.top{{padding-block:32px 8px}}.top .eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 8px}}
.top h1{{font-size:clamp(28px,5vw,44px)}}.top .sub{{color:var(--muted);max-width:62ch;margin:10px 0 0;font-size:17px}}
.kpi{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}.kpi div{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:8px 14px}}
.kpi b{{display:block;font:700 22px var(--display);font-variant-numeric:tabular-nums}}.kpi span{{font-size:13px;color:var(--muted)}}
.note{{background:var(--note);border:1px solid var(--note-line);border-radius:10px;padding:12px 14px;font-size:14.5px;margin:0 0 18px;max-width:80ch}}
.find{{width:100%;max-width:520px;padding:11px 13px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--fg);font:inherit}}
#count{{font-size:13px;color:var(--muted);margin-left:8px}}
.layout{{display:grid;grid-template-columns:260px minmax(0,1fr);gap:36px;margin-top:22px;align-items:start}}
.rail{{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto;display:flex;flex-direction:column;gap:2px;padding-right:6px}}
.rail a{{display:flex;gap:10px;padding:6px 8px;border-radius:8px;text-decoration:none;color:var(--muted);font-size:13.5px;line-height:1.35}}
.rail a span{{font:600 12px var(--display);min-width:20px;color:var(--accent);padding-top:1px;font-variant-numeric:tabular-nums}}
.rail a:hover,.rail a.on{{background:var(--accent-soft);color:var(--fg)}}
main{{min-width:0}}
.intro{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:0 0 34px}}
.ph{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}.ph h3{{font-size:15px;margin-bottom:4px;color:var(--accent)}}.ph p{{margin:0;font-size:13.5px;color:var(--muted)}}
.subj{{padding-top:30px;margin-top:6px;border-top:1px solid var(--line);scroll-margin-top:12px}}
.subj .eyebrow{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 6px}}
.subj h2{{font-size:clamp(23px,3.4vw,30px)}}.ov{{color:var(--muted);max-width:70ch;margin:8px 0 16px}}
.tp{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:10px;counter-reset:t}}
.tp li{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px 14px;counter-increment:t;min-width:0}}
.tp h4{{font-size:15px;font-weight:600}}.tp h4::before{{content:counter(t) ". ";color:var(--accent);font-variant-numeric:tabular-nums}}
.tp p{{margin:4px 0 0;font-size:14.5px;color:var(--muted)}}
.subj h3{{font-size:17px;margin:20px 0 8px}}.chk{{columns:2;column-gap:28px;padding-left:20px;margin:0}}
.pr{{margin-top:16px;background:var(--accent-soft);border-radius:10px;padding:12px 16px}}.pr b{{font:700 13px var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}}.pr p{{margin:4px 0 0}}
.end{{padding-top:34px;margin-top:34px;border-top:1px solid var(--line)}}.end h2{{font-size:26px;margin-bottom:10px}}
.exg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:10px;margin-top:12px}}
.ex{{display:flex;flex-direction:column;gap:2px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px 14px;text-decoration:none;color:var(--fg);min-width:0}}
.ex small{{color:var(--accent);font-weight:600}}.ex span{{color:var(--muted);font-size:14px}}.ex:hover{{border-color:var(--accent)}}
footer{{padding-block:34px 48px;color:var(--muted);font-size:13.5px}}
@media (max-width:860px){{.layout{{grid-template-columns:minmax(0,1fr);gap:16px}}.rail{{position:static;flex-direction:row;overflow-x:auto;max-height:none;padding:0 0 8px}}.rail a{{white-space:nowrap}}.chk{{columns:1}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
</style>
<div class="wrap">
<div class="top"><p class="eyebrow">SkillNavora · AI Product Management</p><h1>{E(extras.TITLE)}: complete guide</h1>
<p class="sub">{E(extras.SUBTITLE)}. Every subject and topic of the detailed curriculum, explained in a line, with a practice task for each subject.</p>
<div class="kpi"><div><b>{len(SUBJECTS)}</b><span>subjects</span></div><div><b>{n_topics}</b><span>topics</span></div><div><b>12</b><span>capstone projects</span></div><div><b>{len(extras.OUTCOMES)}</b><span>outcomes</span></div></div>
<p class="note">Definitions are short study notes, not full lessons. Tool and model details change quickly, so check the official sites. The case study subject lists what to research from public sources and makes no claims about any company's internal data.</p>
<input id="find" class="find" type="search" placeholder="Search all topics, for example RAG, pricing, SQL" aria-label="Search topics"><span id="count"></span></div>
<div class="layout"><nav class="rail" aria-label="Subjects">{nav}</nav>
<main><div class="intro">{phases}</div>
{"".join(secs)}
<section class="end" id="outcomes"><h2>Course completion outcomes</h2><p>By completing the curriculum, learners should be able to:</p><ul>{outcomes}</ul><p><b>Positioning:</b> {E(extras.POSITIONING)}</p></section>
<section class="end" id="existing"><h2>Your existing SkillNavora AI PM material</h2><p>Everything already published that supports these subjects, linked to the matching subject numbers. These open on skillnavora.in.</p><div class="exg">{existing}</div></section>
</main></div>
<footer>SkillNavora · AI Product Management. This guide is one of two variants of the AI PM course so the two can be compared.</footer></div>
<script>
(function(){{var q=document.getElementById('find'),c=document.getElementById('count');
var secs=[].slice.call(document.querySelectorAll('section.subj'));
q.addEventListener('input',function(){{var v=q.value.trim().toLowerCase(),n=0;
secs.forEach(function(s){{var hit=0;[].slice.call(s.querySelectorAll('.tp li')).forEach(function(li){{var m=!v||li.dataset.t.indexOf(v)>-1;li.hidden=!m;if(m)hit++}});
var t=s.querySelector('h2').textContent.toLowerCase();s.hidden=!!v&&!hit&&t.indexOf(v)<0;if(!s.hidden)n+=hit}});
c.textContent=v?n+' matching topics':''}});
var links=[].slice.call(document.querySelectorAll('.rail a'));
if('IntersectionObserver' in window){{var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{links.forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)}})}}}})}},{{rootMargin:'-20% 0px -70% 0px'}});secs.forEach(function(s){{io.observe(s)}})}}
}})();
</script>"""

if __name__ == "__main__":
    open(sys.argv[1], "w", encoding="utf-8").write(build())
