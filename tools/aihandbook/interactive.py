"""Clickable prototype of the AI Master Course handbook (single HTML file).

Sidebar navigation, search, progress ticks saved in the browser, copy buttons,
step-through diagrams and links to every PDF. Used for the website page
(ai-master-course-handbook.html) and the artifact.
Run: python3 tools/aihandbook/interactive.py
"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import build as B
import content as C
import deep as D
import figs2 as F2
import book as BK

E = lambda s: html.escape(str(s), quote=True)

INTERACTIVE_CSS = """
:root{--bg:#f5f7fc;--surface:#fff;--surface-2:#eef2fa;--ink:#0d1630;--mu:#55607a;--line:#e1e6f0;--brand:#4f46e5;--brand-ink:#3f37c9;--brand-soft:#ecebff;--on:#fff;--ok:#16a34a;--warn:#d97706;--code:#0b1220;--codefg:#e2e8f0;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0b1020;--surface:#121a2e;--surface-2:#18213a;--ink:#e8ecf7;--mu:#9aa5c0;--line:#26304a;--brand:#8b84ff;--brand-ink:#a9a4ff;--brand-soft:#221f4a;--on:#0b1020;--code:#060a14;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0b1020;--surface:#121a2e;--surface-2:#18213a;--ink:#e8ecf7;--mu:#9aa5c0;--line:#26304a;--brand:#8b84ff;--brand-ink:#a9a4ff;--brand-soft:#221f4a;--on:#0b1020;--code:#060a14;color-scheme:dark}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--brand-ink)}
.top{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--surface);border-bottom:1px solid var(--line)}
.top b{font-size:15px}.top .sp{flex:1}
.top button,.top a.btn{font:600 13px Inter,system-ui,sans-serif;border:1px solid var(--line);background:var(--surface-2);color:var(--ink);border-radius:9px;padding:7px 11px;cursor:pointer;text-decoration:none}
#menu-btn{display:none}
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);min-height:calc(100vh - 52px)}
nav.side{position:sticky;top:52px;align-self:start;height:calc(100vh - 52px);overflow:auto;background:var(--surface);border-right:1px solid var(--line);padding:12px 10px}
nav.side input{width:100%;font:14px Inter,system-ui,sans-serif;padding:9px 11px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);margin-bottom:10px}
nav.side h4{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--brand-ink);margin:14px 6px 4px}
nav.side a{display:flex;gap:8px;align-items:center;padding:7px 9px;border-radius:9px;color:var(--ink);text-decoration:none;font-size:14px}
nav.side a:hover{background:var(--surface-2)}
nav.side a.on{background:var(--brand-soft);color:var(--brand-ink);font-weight:700}
nav.side .d{width:9px;height:9px;border-radius:50%;flex:none;background:var(--line)}
nav.side .d.done{background:var(--ok)}nav.side .d.part{background:var(--warn)}
main{padding:22px clamp(14px,3vw,40px) 60px;min-width:0;max-width:980px}
.view{display:none}.view.on{display:block}
.kicker{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--brand-ink);font-size:12px}
h1{font-size:clamp(28px,4vw,40px);line-height:1.12;margin:6px 0 10px}
h2{font-size:clamp(22px,3vw,28px);margin:6px 0 8px;color:var(--ink)}
h3{font-size:18px;margin:20px 0 6px}
h4{font-size:13px;margin:12px 0 4px;color:var(--brand-ink);text-transform:uppercase;letter-spacing:.06em}
p,li{font-size:15.5px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:12px 0}
.hero{background:linear-gradient(135deg,var(--brand-soft),var(--surface));border:1px solid var(--line);border-radius:20px;padding:22px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:12px 0}
.tile{display:block;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px;text-decoration:none;color:var(--ink)}
.tile:hover{border-color:var(--brand)}
.tile b{display:block;color:var(--brand-ink);margin-bottom:4px}
.pill{display:inline-block;font:700 11.5px Inter,sans-serif;padding:2px 9px;border-radius:99px;margin-left:6px;vertical-align:middle}
.p-cov{background:#dcfce7;color:#166534}.p-par{background:#fef3c7;color:#92400e}.p-gap{background:#fee2e2;color:#991b1b}
.ticks{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0 4px}
.ticks label{display:flex;gap:8px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:8px 12px;font-weight:600;font-size:14px;cursor:pointer}
.ticks input{width:18px;height:18px;accent-color:var(--brand)}
.bar{height:12px;border-radius:99px;background:var(--surface-2);border:1px solid var(--line);overflow:hidden;margin:8px 0}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brand),#0ea5b7);transition:width .3s}
pre{position:relative;background:var(--code);color:var(--codefg);border-radius:12px;padding:14px;overflow:auto;font:13.5px/1.5 "JetBrains Mono",ui-monospace,Consolas,monospace;margin:8px 0}
pre code{background:none;color:inherit}
.copy{position:absolute;top:8px;right:8px;font:600 12px Inter,sans-serif;border:1px solid #3b4660;background:#1d2740;color:#e2e8f0;border-radius:8px;padding:4px 9px;cursor:pointer}
.out pre{background:#f4f7ee;color:#1f2a14;border:1px solid #cfe0b0}
.fig{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:10px;margin:12px 0}
.fig svg{width:100%;height:auto;display:block}
.fig figcaption{font-size:13px;color:var(--mu);text-align:center;margin-top:6px;font-weight:600}
.fg-card{fill:var(--surface);stroke:var(--line);stroke-width:1.5}.fg-hub{fill:var(--brand)}.fg-okbox{fill:color-mix(in srgb,#16a34a 14%,var(--surface));stroke:#16a34a}.fg-warnbox{fill:color-mix(in srgb,#f59e0b 16%,var(--surface));stroke:#d97706}.fg-okbox,.fg-warnbox{stroke-width:1.5}
.fg-t{fill:var(--ink);font:700 14px Inter,sans-serif}.fg-t-on{fill:var(--on);font:700 14px Inter,sans-serif}
.fg-s{fill:var(--mu);font:400 12px Inter,sans-serif}.fg-s-on{fill:var(--on);opacity:.9;font:400 12px Inter,sans-serif}
.fg-ico{font-size:20px}.fg-arrow{stroke:var(--mu);stroke-width:2;fill:none}.fg-head{fill:var(--mu)}.fg-lab{fill:var(--mu);font:600 11.5px Inter,sans-serif}.fg-cap{fill:var(--brand-ink);font:800 11.5px Inter,sans-serif}
.steps{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.steps button{font:600 13px Inter,sans-serif;border:1px solid var(--line);background:var(--surface-2);color:var(--ink);border-radius:99px;padding:6px 12px;cursor:pointer}
.steps button.on{background:var(--brand);border-color:var(--brand);color:var(--on)}
.stepbox{min-height:44px;background:var(--surface-2);border-radius:12px;padding:10px 12px;font-size:15px}
.note{border-left:4px solid var(--brand);background:var(--brand-soft);border-radius:10px;padding:10px 14px;margin:10px 0}
.warn{border-left:4px solid var(--warn);background:color-mix(in srgb,#f59e0b 12%,var(--surface));border-radius:10px;padding:10px 14px;margin:10px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}th{background:var(--surface-2)}
.gl input{width:100%;font:15px Inter,sans-serif;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink);margin:8px 0}
.dl{display:flex;flex-wrap:wrap;gap:10px}
.dl a{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 14px;text-decoration:none;color:var(--ink);min-width:200px;flex:1}
.dl a:hover{border-color:var(--brand)}.dl small{color:var(--mu)}
.sub-h{font-size:15px;color:var(--mu);margin:0 0 10px}
.pb,.week-hdr,.cover{all:unset}
.fig .vx-fig{border:0;padding:0;margin:0;background:none}
.fig .vx-fig-hint{display:none}
@media (max-width:640px){.fig .vx-fig-hint{display:block;font-size:12px;color:var(--mu);text-align:center;margin:0 0 6px}.fig{overflow-x:auto}.fig svg{min-width:600px}}
@media (max-width:860px){.layout{grid-template-columns:1fr}nav.side{position:fixed;left:0;top:52px;width:280px;max-width:86vw;transform:translateX(-105%);transition:transform .2s;z-index:30;box-shadow:0 10px 30px rgba(0,0,0,.25)}nav.side.open{transform:none}#menu-btn{display:inline-block}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
"""

INTERACTIVE_JS = r"""
(function(){
  var KEY='aihb.progress.v1';
  var prog={}; try{prog=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){prog={}}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(prog))}catch(e){}}
  var views=[].slice.call(document.querySelectorAll('.view'));
  var links=[].slice.call(document.querySelectorAll('nav.side a[data-view]'));
  var side=document.querySelector('nav.side');
  function show(id){
    if(!document.getElementById('v-'+id)) id='start';
    views.forEach(function(v){v.classList.toggle('on',v.id==='v-'+id)});
    links.forEach(function(a){a.classList.toggle('on',a.dataset.view===id)});
    window.scrollTo(0,0); if(side) side.classList.remove('open');
  }
  function route(){ show((location.hash||'#start').slice(1)); }
  window.addEventListener('hashchange',route); route();
  document.getElementById('menu-btn').addEventListener('click',function(){side.classList.toggle('open')});
  // progress: three ticks per subject
  function subjectState(n){var p=prog['s'+n]||{}; return (p.read?1:0)+(p.code?1:0)+(p.assign?1:0)}
  function refreshProgress(){
    var done=0, total=26;
    for(var n=1;n<=total;n++){ var c=subjectState(n); if(c===3) done++;
      var d=document.querySelector('nav.side a[data-view="s'+n+'"] .d'); if(d){ d.className='d '+(c===3?'done':(c>0?'part':'')); } }
    var bar=document.getElementById('total-bar'); if(bar) bar.style.width=Math.round(done*100/total)+'%';
    var t=document.getElementById('total-txt'); if(t) t.textContent=done+' of '+total+' subjects complete (all three ticks)';
  }
  document.querySelectorAll('.ticks input[data-s]').forEach(function(cb){
    var n=cb.dataset.s, k=cb.dataset.k; cb.checked=!!(prog['s'+n]&&prog['s'+n][k]);
    cb.addEventListener('change',function(){ prog['s'+n]=prog['s'+n]||{}; prog['s'+n][k]=cb.checked; save(); refreshProgress(); });
  });
  refreshProgress();
  // copy buttons
  document.querySelectorAll('pre').forEach(function(pre){
    if(pre.closest('.out')) return;
    var b=document.createElement('button'); b.className='copy'; b.type='button'; b.textContent='Copy';
    b.addEventListener('click',function(){ var t=pre.innerText; var done=function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1400)};
      if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(done,function(){})} else {var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done()}catch(e){}ta.remove()} });
    pre.appendChild(b);
  });
  // step-through diagrams
  document.querySelectorAll('.stepper').forEach(function(st){
    var items=JSON.parse(st.dataset.items||'[]'), buttons=st.querySelector('.steps'), box=st.querySelector('.stepbox');
    items.forEach(function(it,i){
      var b=document.createElement('button'); b.type='button'; b.textContent=(i+1)+'. '+it[0];
      b.addEventListener('click',function(){ [].forEach.call(buttons.children,function(x){x.classList.remove('on')}); b.classList.add('on'); box.textContent=it[1]; });
      buttons.appendChild(b);
    });
    if(buttons.firstChild) buttons.firstChild.click();
  });
  // search: subjects and glossary
  var q=document.getElementById('q');
  q.addEventListener('input',function(){
    var v=q.value.trim().toLowerCase();
    links.forEach(function(a){ a.style.display=(!v||a.textContent.toLowerCase().indexOf(v)>-1)?'':'none'; });
    var g=document.getElementById('gl-q');
    if(g && document.getElementById('v-glossary').classList.contains('on')){}
  });
  var gq=document.getElementById('gl-q');
  if(gq){ gq.addEventListener('input',function(){ var v=gq.value.trim().toLowerCase();
    document.querySelectorAll('#glossary-body tr').forEach(function(tr){ tr.style.display=(!v||tr.textContent.toLowerCase().indexOf(v)>-1)?'':'none'; }); }); }
  // theme toggle
  var tb=document.getElementById('theme');
  tb.addEventListener('click',function(){ var cur=document.documentElement.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); var nx=cur==='dark'?'light':'dark'; document.documentElement.setAttribute('data-theme',nx); try{localStorage.setItem('aihb.theme',nx)}catch(e){} });
  try{var th=localStorage.getItem('aihb.theme'); if(th) document.documentElement.setAttribute('data-theme',th);}catch(e){}
})();
"""


def stepper_for(key):
    steps = D.FIG_DETAIL.get(key)
    if not steps:
        return ""
    # Labels come from the diagram's own step text order; keep short labels for buttons
    labels = ["Start", "Next", "Then", "Check", "Decide", "Finish", "Extra", "More"]
    items = [[f"{labels[min(i, len(labels)-1)]}", t] for i, t in enumerate(steps)]
    return f'<div class="stepper" data-items="{E(json.dumps(items))}"><div class="sub-h">Click each step to see what happens.</div><div class="steps"></div><div class="stepbox"></div></div>'


def fig_block(key):
    return f'<div class="fig">{B.figure(key)}{stepper_for(key)}</div>' if key in B.FIG else f'<div class="fig">{F2.render(key)}</div>'


def subject_view(s):
    status, _ = C.COVERAGE[s["n"]]
    pill = {"Covered": "p-cov", "Partial": "p-par", "Gap": "p-gap"}[status]
    tier = next(k for k, v in C.TIERS.items() if s["n"] in v)
    body = B.subject_html(s)
    # replace static figure blocks with interactive ones (figure + stepper)
    if s.get("figure"):
        static = f'<div class="fig">{B.figure(s["figure"])}</div>'
        body = body.replace(static, f'<div class="fig">{B.figure(s["figure"])}{stepper_for(s["figure"])}</div>', 1)
    head = (f'<div class="kicker">Week {s["week"]} · {E(tier)}</div><h1>Subject {s["n"]}: {E(s["title"])}</h1>'
            f'<p class="sub-h"><span class="pill {pill}">{status} on the website</span></p>'
            '<div class="ticks">'
            f'<label><input type="checkbox" data-s="{s["n"]}" data-k="read"> I read and understood it</label>'
            f'<label><input type="checkbox" data-s="{s["n"]}" data-k="code"> I ran the code or steps</label>'
            f'<label><input type="checkbox" data-s="{s["n"]}" data-k="assign"> I did the assignment</label></div>')
    return f'<div class="view" id="v-s{s["n"]}">{head}{body}</div>'


def nav_links():
    out = []
    out.append(("start", "Start here", None))
    out.append(("coverage", "Coverage check", None))
    out.append(("curriculum", "Curriculum", None))
    for w in C.WEEKS:
        out.append((f"w{w['n']}", f"Week {w['n']}: {w['title']}", None))
        for n in w["subjects"]:
            s = next(x for x in C.SUBJECTS if x["n"] == n)
            out.append((f"s{n}", f"{n}. {s['title']}", n))
    out += [("timetable", "Six-week timetable", None), ("assessment", "Assessment and tracker", None), ("architecture", "Architecture library", None),
            ("toolkit", "AI PM toolkit", None), ("interview", "Interview bank", None), ("advanced", "Advanced track", None),
            ("tools", "Tool stack", None), ("glossary", "Glossary", None), ("downloads", "Downloads (PDF)", None), ("pointers", "All pointers", None)]
    return out


def build_page(artifact=False):
    nav = []
    cur = None
    for vid, label, n in nav_links():
        if vid.startswith("w") and vid[1:].isdigit():
            nav.append(f'<h4>Week {vid[1:]}</h4>')
            continue
        if vid.startswith("s") and n:
            nav.append(f'<a href="#s{n}" data-view="s{n}"><span class="d"></span>{E(label)}</a>')
        else:
            nav.append(f'<a href="#{vid}" data-view="{vid}">{E(label)}</a>')
    # Views
    views = []
    weeks_cards = "".join(f'<a class="tile" href="#w{w["n"]}"><b>Week {w["n"]}</b>{E(w["title"])}<div class="sub-h" style="margin:6px 0 0">Outcome: {E(w["outcome"])}</div></a>' for w in C.WEEKS)
    views.append(f'''<div class="view" id="v-start"><div class="hero"><div class="kicker">AI Master Course · Volume 1 · Clickable handbook</div>
      <h1>From beginner to AI application builder and AI PM</h1>
      <p>Six weeks, 26 subjects. Each subject explains the idea with an analogy, shows the code and its real output, adds a deep dive with pointers, and ends with an assignment and interview questions.</p>
      <div class="bar" aria-hidden="true"><i id="total-bar"></i></div><p id="total-txt" class="sub-h">0 of 26 subjects complete</p>
      <p class="sub-h">Progress is saved in this browser. Tick the three boxes on each subject as you go.</p></div>
      <h3>Choose a week</h3><div class="grid">{weeks_cards}</div>
      <div class="note"><b>Check before you rely on a tool:</b> AI tools, model names, prices and free limits change. Confirm them on the provider's official page before use.</div></div>''')
    cov_rows = "".join(f'<tr><td>{s["n"]}</td><td><a href="#s{s["n"]}">{E(s["title"])}</a></td><td><span class="pill {({"Covered":"p-cov","Partial":"p-par","Gap":"p-gap"})[C.COVERAGE[s["n"]][0]]}">{C.COVERAGE[s["n"]][0]}</span></td><td>{E(C.COVERAGE[s["n"]][1][0][0]) if C.COVERAGE[s["n"]][1] else ""}</td></tr>' for s in C.SUBJECTS)
    views.append(f'<div class="view" id="v-coverage"><div class="kicker">Check</div><h1>Coverage check</h1><p>What the SkillNavora site already contains for each subject. Covered = dedicated lesson or guide; Partial = touched on in a broader page; Gap = no dedicated content yet.</p><table><thead><tr><th>#</th><th>Subject</th><th>Status</th><th>Main site content</th></tr></thead><tbody>{cov_rows}</tbody></table>'
                 f'<div class="warn"><b>Evidence limit:</b> {E(C.SKILL_NOTE)}</div></div>')
    tiers = "".join(f'<div class="card"><b>{E(k)}</b><p class="sub-h" style="margin:4px 0 0">{", ".join("Subject "+str(n) for n in v)}</p></div>' for k, v in C.TIERS.items())
    wk = "".join(f'<div class="card"><b>Week {w["n"]}: {E(w["title"])}</b><p class="sub-h" style="margin:4px 0 0">{E(w["outcome"])}</p><p><a href="#w{w["n"]}">Open week {w["n"]}</a></p></div>' for w in C.WEEKS)
    views.append(f'<div class="view" id="v-curriculum"><div class="kicker">Structure</div><h1>Curriculum</h1><p>Foundations first; advanced topics optional.</p><h3>By tier</h3>{tiers}<h3>By week</h3>{wk}</div>')
    for w in C.WEEKS:
        views.append(f'<div class="view" id="v-w{w["n"]}"><div class="kicker">Week {w["n"]}</div><h1>{E(w["title"])}</h1><p>Outcome: {E(w["outcome"])}</p>'
                     '<div class="grid">' + "".join(f'<a class="tile" href="#s{n}"><b>Subject {n}</b>{E(next(x for x in C.SUBJECTS if x["n"]==n)["title"])}</a>' for n in w["subjects"]) + '</div></div>')
    for s in C.SUBJECTS:
        views.append(subject_view(s))
    tt = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a, b, c, d in C.TIMETABLE)
    views.append(f'<div class="view" id="v-timetable"><div class="kicker">Plan</div><h1>Six-week timetable</h1><p>Six study days and one revision day each week, 2 to 3 hours a day.</p><table><thead><tr><th>Day</th><th>Block 1 (learn)</th><th>Block 2 (build)</th><th>Block 3 (practise)</th></tr></thead><tbody>{tt}</tbody></table></div>')
    views.append('<div class="view" id="v-assessment"><div class="kicker">Assess</div><h1>Assessment and tracker</h1><p>End of each week: 15 conceptual questions, 5 practical exercises, 1 mini-project, 1 architecture explanation, 1 interview simulation.</p>'
                 '<table><thead><tr><th>Area</th><th>Weight</th></tr></thead><tbody><tr><td>Conceptual understanding</td><td>15%</td></tr><tr><td>Coding and implementation</td><td>25%</td></tr><tr><td>AI application development</td><td>25%</td></tr><tr><td>Evaluation and troubleshooting</td><td>15%</td></tr><tr><td>Product documentation</td><td>10%</td></tr><tr><td>Interview explanation</td><td>10%</td></tr></tbody></table>'
                 '<p>Mark a subject complete only after you show the working result (a running file, a test log or a report). Your ticks on each subject are the tracker in this browser.</p></div>')
    arch = [("flow", "Request flow"), ("llm", "LLM call"), ("rag", "RAG pipeline"), ("vector", "Semantic search"), ("agent", "Agent loop"), ("mcp", "MCP"),
            ("eval", "Evaluation loop"), ("prod", "Production operations"), ("system", "Production RAG system"), ("capstone", "Capstone milestones")]
    arch_html = "".join(f'<h3>{E(t)}</h3>{fig_block(k)}' for k, t in arch)
    arch_html += "".join(f'<h3>Extra: {E(k.replace("_"," "))}</h3><div class="fig">{F2.render(k)}</div>' for k in ["embedding_space", "chunk_overlap", "cosine", "attention", "tool_cycle", "mcp_flow", "permissions", "guardrails", "release_gate", "cost_bars", "latency", "lifecycle_loop", "system_layers", "funnel", "prd_map", "repo_tree", "timeline_6w"])
    views.append(f'<div class="view" id="v-architecture"><div class="kicker">Architecture</div><h1>Architecture library</h1><p>Click through the steps of each main diagram.</p>{arch_html}</div>')
    tk = "".join(f"<li>{E(x)}</li>" for x in C.PRD_SECTIONS)
    sd = "".join(f"<li>{E(x)}</li>" for x in C.SYSTEM_DESIGN_TEMPLATE)
    mt = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in C.METRICS)
    views.append(f'<div class="view" id="v-toolkit"><div class="kicker">PM</div><h1>AI PM toolkit</h1><h3>PRD template</h3><ol>{tk}</ol><h3>System design template</h3><ol>{sd}</ol><h3>Metric families</h3><table><thead><tr><th>Family</th><th>Examples</th></tr></thead><tbody>{mt}</tbody></table>'
                 f'<h3>User story example</h3><div class="card"><p><b>As a support agent</b>, I want a draft answer with its policy source, so that I can reply to a customer in under two minutes.</p><p><b>Acceptance criteria:</b> every draft cites an approved source; 95% or higher accuracy on the golden set; says so and suggests escalation when no source is found; p95 latency under 8 seconds.</p></div>'
                 f'<h3>Release gate</h3>{fig_block("release_gate")}</div>')
    tech = "".join(f"<tr><td>{i+1}</td><td>{E(a)}</td><td>{E(q)}</td><td>{E(b)}</td></tr>" for i, (a, q, b) in enumerate(C.TECH_BANK))
    pm = "".join(f"<tr><td>{i+1}</td><td>{E(a)}</td><td>{E(q)}</td><td>{E(b)}</td></tr>" for i, (a, q, b) in enumerate(C.PM_BANK))
    views.append(f'<div class="view" id="v-interview"><div class="kicker">Interview</div><h1>Interview bank (volume 1)</h1><p>{len(C.TECH_BANK)} technical and {len(C.PM_BANK)} AI product questions. Full set of 100 and 50 in volume 2.</p><h3>Technical</h3><table><thead><tr><th>#</th><th>Area</th><th>Question</th><th>Model answer</th></tr></thead><tbody>{tech}</tbody></table><h3>AI product management</h3><table><thead><tr><th>#</th><th>Area</th><th>Question</th><th>Model answer</th></tr></thead><tbody>{pm}</tbody></table></div>')
    adv = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in C.ADVANCED)
    views.append(f'<div class="view" id="v-advanced"><div class="kicker">Optional</div><h1>Advanced specialisation track</h1><p>{E(C.ADVANCED_NOTE)}</p><table><thead><tr><th>Track</th><th>Topics</th></tr></thead><tbody>{adv}</tbody></table></div>')
    tools = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in C.TOOLS)
    views.append(f'<div class="view" id="v-tools"><div class="kicker">Stack</div><h1>Tool stack</h1><p>Recommendation only. Check each official site for current features and prices.</p><table><thead><tr><th>Category</th><th>Primary (beginner)</th><th>Alternative</th></tr></thead><tbody>{tools}</tbody></table></div>')
    gl = "".join(f"<tr><td><b>{E(t)}</b></td><td>{E(m)}</td><td>Subject {n}</td></tr>" for t, m, n in sorted(D.GLOSSARY, key=lambda g: g[0].lower()))
    views.append(f'<div class="view gl" id="v-glossary"><div class="kicker">Reference</div><h1>Glossary</h1><input id="gl-q" type="search" placeholder="Search terms (for example: token, cosine, MCP)"><table><thead><tr><th>Term</th><th>Meaning</th><th>Introduced</th></tr></thead><tbody id="glossary-body">{gl}</tbody></table></div>')
    pdfs = [("AI-Master-Course-Handbook.pdf", "Full handbook", "All 26 subjects, diagrams, pointers, glossary (93 pages)")]
    pdfs += [(name, f"Week {n} PDF", C.WEEKS[n - 1]["title"]) for n, name in BK.WEEK_FILES.items()]
    pdfs += [("AI-Master-Course-Interview-Bank.pdf", "Interview bank PDF", "Technical and AI PM questions with answers"), ("AI-Master-Course-PM-Toolkit.pdf", "PM toolkit PDF", "PRD, metrics, release gate and PM subjects")]
    dl = "".join(f'<a href="handbook/{E(f)}" download><b>{E(t)}</b><small>{E(d)}</small></a>' for f, t, d in pdfs)
    views.append(f'<div class="view" id="v-downloads"><div class="kicker">PDF</div><h1>Downloads</h1><p>Every PDF in the set. Each one is also linked from the course page.</p><div class="dl">{dl}</div>'
                 '<h3>Also on SkillNavora</h3><div class="grid"><a class="tile" href="ai-master-course.html"><b>Course overview</b>Six weeks at a glance</a><a class="tile" href="ai-jobs-2027.html"><b>AI Jobs 2027 roadmap</b>Role tracks and a 7-week sprint</a><a class="tile" href="ai-skills-map.html"><b>AI Skills Map</b>Every AI skill and where to learn it</a></div></div>')
    ptr = []
    for s in C.SUBJECTS:
        ptr.append(f"<h3>Subject {s['n']}: {E(s['title'])}</h3><ul>" + "".join(f'<li>{E(l)}: <span class="sub-h">{E(u)}</span></li>' for l, u in (s["links"] + [x for x in C.COVERAGE[s["n"]][1] if x not in s["links"]])) + "".join(f'<li>{E(l)} (official): <span class="sub-h">{E(u)}</span></li>' for l, u in D.OFFICIAL.get(s["n"], [])) + "</ul>")
    views.append('<div class="view" id="v-pointers"><div class="kicker">Reference</div><h1>All pointers</h1><p>Site pointers are checked against the content index. Official pointers point to documentation roots; confirm the page before use.</p>' + "".join(ptr) + "</div>")
    head_title = "AI Master Course Handbook"
    artifact_note = "" if not artifact else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="claude:viewport-fit-sides" content="cover"><title>{head_title}</title>
<style>{INTERACTIVE_CSS}</style></head><body>
<div class="top"><button id="menu-btn" type="button" aria-label="Menu">☰ Menu</button><b>AI Master Course · Clickable handbook</b><span class="sp"></span>
<button id="theme" type="button" aria-label="Toggle dark mode">◐</button><a class="btn" href="#downloads">Download PDFs</a></div>
<div class="layout"><nav class="side" aria-label="Handbook sections"><input id="q" type="search" placeholder="Filter sections" aria-label="Filter sections">{"".join(nav)}</nav>
<main>{"".join(views)}</main></div>
<script>{INTERACTIVE_JS}</script></body></html>'''


def as_artifact(page):
    """Artifact viewers cannot download files, so PDF and site links open the live website in a new tab."""
    site = "https://www.skillnavora.in/"
    page = page.replace('href="handbook/', f'href="{site}handbook/')
    page = page.replace(' download>', ' target="_blank" rel="noopener">')
    for f in ["ai-master-course.html", "ai-jobs-2027.html", "ai-skills-map.html"]:
        page = page.replace(f'href="{f}"', f'href="{site}{f}" target="_blank" rel="noopener"')
    return page


if __name__ == "__main__":
    out_dir = os.path.join(HERE, "out"); os.makedirs(out_dir, exist_ok=True)
    page = build_page()
    p2 = os.path.join(ROOT, "ai-master-course-handbook.html"); open(p2, "w", encoding="utf-8").write(page)
    art = as_artifact(page)
    p1 = os.path.join(out_dir, "interactive.html"); open(p1, "w", encoding="utf-8").write(art)
    print("site bytes", len(page.encode()), "artifact bytes", len(art.encode()))
