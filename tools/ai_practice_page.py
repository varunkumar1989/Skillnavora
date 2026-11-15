"""AI Master Course practice page (ai-master-course-practice.html): interview bank (100 technical,
50 AI PM), 15-question quiz for each week (90), answer keys for all 26 subject assignments, and the
seven new lessons' expected results. Content: tools/aihandbook/{content,practice,lessons}.py."""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "aihandbook"))
import content as C
import volume2 as P
import lessons as L

E = lambda s: html.escape(str(s), quote=True)

CSS = """
.ap{--r:16px}
.ap-hero{padding:40px 0 22px;background:radial-gradient(800px 340px at 85% 0%,color-mix(in srgb,var(--brand) 14%,transparent),transparent 65%)}
.ap-hero h1{font-size:clamp(30px,4.8vw,50px);line-height:1.06;margin:8px 0 12px}
.ap-nav{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0 0}
.ap-nav a{padding:7px 12px;border:1px solid var(--line);border-radius:99px;text-decoration:none;font-size:14px;background:var(--surface)}
.ap-sec{padding:18px 0}
.ap-sec h2{font-size:clamp(22px,3vw,28px);margin:4px 0 10px}
.ap-qs{display:flex;flex-direction:column;gap:8px}
.ap-qs details{border:1px solid var(--line);border-radius:12px;padding:10px 14px;background:var(--surface)}
.ap-qs summary{cursor:pointer;font-weight:600}
.ap-qs summary small{color:var(--mu);font-weight:500;margin-left:6px}
.ap-qs p{margin:8px 0 0;line-height:1.6}
.ap-filter{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0 12px}
.ap-filter input,.ap-filter select{padding:9px 12px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:inherit;min-width:180px}
.ap-quiz{border:1px solid var(--line);border-radius:var(--r);padding:16px;background:var(--surface);margin:10px 0}
.ap-quiz fieldset{border:0;padding:0;margin:0 0 6px}
.ap-quiz legend{font-weight:700;margin-bottom:6px}
.ap-quiz label{display:block;padding:5px 0;cursor:pointer}
.ap-res{font-weight:700;margin-top:8px;min-height:1.4em}
.ap-note{font-size:13.5px;color:var(--mu)}
.ap pre{background:#0f172a;color:#e2e8f0;border-radius:12px;padding:12px 14px;overflow:auto;font:13px/1.55 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap}
.ap-key{border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;background:var(--surface);margin:10px 0;scroll-margin-top:90px}
.ap-key h3{margin:0 0 6px;font-size:17px}
.ap-key p{margin:0;line-height:1.6}
.ap-score{display:inline-flex;gap:6px;align-items:center;padding:6px 12px;border-radius:99px;background:color-mix(in srgb,var(--brand) 12%,var(--surface));font-weight:700}
.ap-btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
button.ap-b{padding:9px 14px;border-radius:10px;border:1px solid var(--line);background:var(--brand);color:#fff;font:600 14px var(--body);cursor:pointer}
button.ap-b.alt{background:var(--surface);color:var(--ink)}
"""

KEYS_TEXT_SAMPLE = {}  # filled below


def bank_block(title, items, label):
    rows = "".join(f'<details data-q="{E((q + " " + a).lower())}"><summary>{E(q)}<small>{E(t)}</small></summary><p>{E(a)}</p></details>'
                   for t, q, a in items)
    return f"""<div class="ap-qs" id="{label}-list">{rows}</div>"""


def quiz_block(week):
    qs = P.QUIZ[week]
    out = []
    for i, (q, opts, ans, why) in enumerate(qs):
        name = f"w{week}q{i}"
        labels = "".join(f'<label><input type="radio" name="{name}" value="{j}"> {E(o)}</label>' for j, o in enumerate(opts))
        out.append(f'<fieldset data-ans="{ans}" data-why="{E(why)}" data-name="{name}"><legend>{i + 1}. {E(q)}</legend>{labels}<div class="ap-res"></div></fieldset>')
    return f'<div class="ap-quiz" data-week="{week}"><form onsubmit="return false">{"".join(out)}</form><div class="ap-btns"><button type="button" class="ap-b" data-check="{week}">Check answers</button><button type="button" class="ap-b alt" data-reset="{week}">Reset</button></div><p class="ap-score" id="score-{week}" aria-live="polite"></p></div>'


def keys_block():
    out = []
    for s in C.SUBJECTS:
        n = s["n"]
        ans = P.KEYS[n]
        out.append(f'<div class="ap-key" id="key-{n}"><h3>Subject {n}: {E(s["title"])}</h3><p class="ap-note">Assignment: {E(s["assignment"])}</p><pre>{E(ans)}</pre></div>')
    lk = "".join(f'<div class="ap-key" id="lesson-key-{slug}"><h3>New lesson: {E(slug.replace("-", " ").capitalize())}</h3><p>{E(text)}</p></div>' for slug, text in P.LESSON_KEYS.items())
    return "".join(out) + '<h3 style="margin-top:22px">Answer keys for the new lessons</h3>' + lk


def body():
    tech_items = [(t, q, a) for t, q, a in C.TECH_BANK]
    pm_items = [(t, q, a) for t, q, a in C.PM_BANK]
    weeks = "".join(f'<a href="#quiz-w{w}">Week {w}</a>' for w in range(1, 7))
    quizzes = "".join(f'<h3 id="quiz-w{w}" style="margin-top:20px">Week {w}: 15 questions</h3>{quiz_block(w)}' for w in range(1, 7))
    return f"""<style>{CSS}</style><div class="ap">
<section class="ap-hero"><div class="wrap">
  <div class="kicker">AI Master Course · practice</div>
  <h1>Interview bank, weekly quizzes and answer keys</h1>
  <p class="lead" style="max-width:66ch">{len(tech_items)} technical and {len(pm_items)} AI product questions with model answers, 90 quiz questions with explanations (15 per week), and a model answer for every subject assignment. Use the search box to find a topic.</p>
  <nav class="ap-nav" aria-label="On this page"><a href="#bank">Interview bank</a><a href="#quizzes">Quizzes</a><a href="#keys">Answer keys</a><a href="ai-master-course.html">Back to the course</a></nav>
</div></section>
<section class="ap-sec" id="bank"><div class="wrap">
  <div class="kicker">Interview bank</div><h2>{len(tech_items)} technical questions</h2>
  <div class="ap-filter"><input id="ap-search" type="search" placeholder="Search questions and answers" aria-label="Search the question bank"><select id="ap-topic" aria-label="Filter by topic"><option value="">All topics</option>{"".join(f"<option>{E(t)}</option>" for t in sorted({t for t, _, _ in tech_items}))}</select></div>
  <p class="ap-note" id="ap-count"></p>
  {bank_block("tech", tech_items, "tech")}
  <h2 style="margin-top:28px">{len(pm_items)} AI product management questions</h2>
  {bank_block("pm", pm_items, "pm")}
  <p class="ap-note" style="margin-top:12px">System design: nine cases with model answers are on each system design lesson page, under the mock-interview lesson: <a href="ai-lesson-mock-interviews.html#cases">open the cases</a>.</p>
</div></section>
<section class="ap-sec" id="quizzes"><div class="wrap">
  <div class="kicker">Quizzes</div><h2>90 questions, 15 per week</h2>
  <p class="ap-note">Answer, then press Check. Each answer shows why it is right. Score yourself: 12 or more out of 15 means you are ready for the week's assessment.</p>
  <div class="ap-nav">{weeks}</div>
  {quizzes}
</div></section>
<section class="ap-sec" id="keys"><div class="wrap">
  <div class="kicker">Answer keys</div><h2>Model answers for the 26 assignments</h2>
  <p class="ap-note">Each key shows what a strong answer contains. Compare your work with the key; the marking notes say what to check. Use a key only after you have tried the assignment.</p>
  {keys_block()}
</div></section>
</div>
<script>
(function(){{
  var q=document.getElementById('ap-search'),t=document.getElementById('ap-topic'),c=document.getElementById('ap-count');
  function run(){{
    var s=(q.value||'').toLowerCase().trim(),tp=t.value,n=0,all=document.querySelectorAll('#tech-list details,#pm-list details');
    all.forEach(function(d){{
      var ok=(!s||d.getAttribute('data-q').indexOf(s)>-1)&&(!tp||d.querySelector('small').textContent===tp);
      d.style.display=ok?'':'none'; if(ok)n++;
    }});
    c.textContent=n+' of '+all.length+' shown';
  }}
  q.addEventListener('input',run); t.addEventListener('change',run); run();
  document.querySelectorAll('[data-check]').forEach(function(b){{
    b.addEventListener('click',function(){{
      var w=b.getAttribute('data-check'),box=b.closest('.ap-quiz'),ok=0,total=0;
      box.querySelectorAll('fieldset').forEach(function(f){{
        total++; var sel=f.querySelector('input:checked'),res=f.querySelector('.ap-res'),a=+f.getAttribute('data-ans');
        if(!sel){{res.textContent='Not answered. Correct answer: option '+(a+1)+'. '+f.getAttribute('data-why');res.style.color='';return;}}
        var right=(+sel.value)===a; if(right)ok++;
        res.textContent=(right?'Correct. ':'Not quite. ')+f.getAttribute('data-why');
        res.style.color=right?'#166534':'#991b1b';
      }});
      document.getElementById('score-'+w).textContent='Score: '+ok+' of '+total;
    }});
  }});
  document.querySelectorAll('[data-reset]').forEach(function(b){{
    b.addEventListener('click',function(){{
      var box=b.closest('.ap-quiz'); box.querySelectorAll('input').forEach(function(i){{i.checked=false;}});
      box.querySelectorAll('.ap-res').forEach(function(r){{r.textContent='';}});
      box.querySelector('.ap-score').textContent='';
    }});
  }});
}})();
</script>"""


def page_meta():
    return ("AI Master Course practice: 100 technical and 50 AI PM interview questions, 90 weekly quiz questions and answer keys · SkillNavora",
            "Interview bank with model answers, a 15-question quiz for each of the six weeks with explanations, and model answers for all 26 course assignments.")
