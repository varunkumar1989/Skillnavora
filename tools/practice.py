"""Render the Practice tests page (tests.html) and the Top 100 questions page (questions.html) from practice_data.json."""
import json, os, html
E = html.escape
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "practice_data.json"), encoding="utf-8"))
SEGS = [k for k in D["segments"]]

CSS = """<style>
.pt-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}.pt-tabs button{border:1px solid var(--line,#e2dcf3);background:var(--card,#fff);color:inherit;border-radius:999px;padding:9px 16px;font:600 14px var(--display,inherit);cursor:pointer}
.pt-tabs button[aria-selected=true]{background:linear-gradient(135deg,#7C3AED,#22D3EE);border-color:transparent;color:#fff}
.pt-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:16px}.pt-bar select,.pt-bar input{padding:9px 12px;border:1px solid var(--line,#e2dcf3);border-radius:10px;font:inherit;background:var(--card,#fff);color:inherit;max-width:100%}
.pt-score{margin-left:auto;font:700 14px var(--display,inherit);padding:8px 14px;border-radius:999px;background:rgba(124,58,237,.1)}
.pt-q{border:1px solid var(--line,#e2dcf3);border-radius:16px;padding:18px;margin-bottom:14px;background:var(--card,#fff)}
.pt-q h3{font-size:16.5px;margin:0 0 4px}.pt-q .src{font-size:12.5px;color:var(--muted,#6b6880);margin-bottom:12px}
.pt-o{display:grid;gap:8px}.pt-o button{text-align:left;border:1px solid var(--line,#e2dcf3);background:transparent;color:inherit;border-radius:10px;padding:10px 12px;font:inherit;cursor:pointer}
.pt-o button:hover{border-color:#7C3AED}.pt-o button.ok{background:rgba(22,163,74,.12);border-color:#16a34a}.pt-o button.no{background:rgba(220,38,38,.1);border-color:#dc2626;text-decoration:line-through}
.pt-fb{margin-top:10px;font-size:14px;padding:10px 12px;border-radius:10px}.pt-fb.hint{background:rgba(234,179,8,.14)}.pt-fb.good{background:rgba(22,163,74,.12)}
.pt-x code,.pt-q code{background:rgba(124,58,237,.08);padding:1px 5px;border-radius:5px}
.pt-ex pre{background:#14112a;color:#e9e6ff;padding:12px;border-radius:10px;overflow:auto;font-size:14px}
.pt-ex .row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.pt-ex input{flex:1 1 220px;padding:9px 12px;border:1px solid var(--line,#e2dcf3);border-radius:10px;font:14px ui-monospace,Consolas,monospace;background:var(--card,#fff);color:inherit}
.pt-ex button,.pt-q .sa{border:0;border-radius:10px;padding:9px 14px;font:600 14px var(--display,inherit);cursor:pointer;background:#7C3AED;color:#fff}.pt-q .sa{background:transparent;color:#7C3AED;padding:6px 0;margin-top:8px}
.iv details{border:1px solid var(--line,#e2dcf3);border-radius:14px;margin-bottom:10px;background:var(--card,#fff)}.iv summary{cursor:pointer;padding:14px 16px;font-weight:600;list-style:none;display:flex;gap:12px}
.iv summary::-webkit-details-marker{display:none}.iv summary .n{font:700 13px var(--display,inherit);color:#7C3AED;min-width:2.4em}.iv .ans{padding:0 16px 14px 52px;color:var(--muted,#55526a)}
.iv .ans a{font-size:13px}.pt-hide{display:none!important}
@media (max-width:640px){.iv .ans{padding-left:16px}}
</style>"""


def tabs(prefix, counts):
    return '<div class="pt-tabs" role="tablist">' + "".join(f'<button role="tab" data-seg="{k}" aria-selected="{"true" if i == 0 else "false"}">{E(D["segments"][k])} <small>({counts[k]})</small></button>' for i, k in enumerate(SEGS) if counts[k]) + "</div>"


def tests_page():
    counts = {k: sum(t["seg"] == k for t in D["tests"]) + sum(e["seg"] == k for e in D["exercises"]) for k in SEGS}
    data = json.dumps({"t": D["tests"], "x": D["exercises"]}, ensure_ascii=False).replace("</", "<\\/")
    js = """<script>(function(){var D=JSON.parse(document.getElementById('pt-data').textContent),seg='pm',score={ok:0,tot:0};
var $=function(id){return document.getElementById(id)},topic=$('pt-topic'),mode=$('pt-mode'),list=$('pt-list');
function upd(){$('pt-score').textContent='Score '+score.ok+' / '+score.tot}
function norm(s){return String(s).toLowerCase().replace(/\\s+/g,'').replace(/;$/,'')}
function topics(){var ts=[];D.t.forEach(function(q){if(q.seg===seg&&ts.indexOf(q.topic)<0)ts.push(q.topic)});topic.innerHTML='<option value="">All topics</option>'+ts.map(function(t){return '<option>'+t.replace(/</g,'&lt;')+'</option>'}).join('');}
function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
function render(){score={ok:0,tot:0};upd();
 if(mode.value==='x'){var xs=D.x.filter(function(x){return x.seg===seg});list.innerHTML=xs.length?xs.map(function(x,i){return '<div class="pt-q pt-ex" data-i="'+i+'"><h3>'+x.q+'</h3><div class="src">'+x.topic+' · fill in the blank</div><pre>'+x.code+'</pre><div class="row"><input aria-label="Your answer" placeholder="Type the missing part"><button type="button" data-chk>Check</button></div><button class="sa" type="button" data-sa>Show answer</button><div class="pt-fb" hidden></div></div>'}).join(''):'<p class="meta">No exercises for this segment yet; try the quiz mode.</p>';
  list.querySelectorAll('.pt-ex').forEach(function(card){var x=xs[+card.dataset.i],fb=card.querySelector('.pt-fb'),inp=card.querySelector('input'),done=false;
   function check(){var ok=x.ans.some(function(a){return norm(a)===norm(inp.value)});if(!done){score.tot++;if(ok)score.ok++;done=ok;upd()}fb.hidden=false;fb.className='pt-fb '+(ok?'good':'hint');fb.innerHTML=ok?'Correct! '+x.ans[0]:'Not quite. Hint: '+x.h}
   card.querySelector('[data-chk]').addEventListener('click',check);inp.addEventListener('keydown',function(e){if(e.key==='Enter')check()});
   card.querySelector('[data-sa]').addEventListener('click',function(){fb.hidden=false;fb.className='pt-fb good';fb.innerHTML='Answer: <code>'+x.ans[0].replace(/</g,'&lt;')+'</code>'})});return}
 var qs=D.t.filter(function(q){return q.seg===seg&&(!topic.value||q.topic===topic.value)});qs=shuffle(qs.slice()).slice(0,mode.value==='all'?qs.length:10);
 list.innerHTML=qs.map(function(q,i){return '<div class="pt-q" data-i="'+i+'"><h3>'+(i+1)+'. '+q.q+'</h3><div class="src">'+q.topic+' · <a href="'+q.page+'">'+q.lesson+'</a></div><div class="pt-o">'+q.o.map(function(o,j){return '<button type="button" data-j="'+j+'">'+o+'</button>'}).join('')+'</div><button class="sa" type="button" data-sa>Show answer</button><div class="pt-fb" hidden></div></div>'}).join('');
 list.querySelectorAll('.pt-q').forEach(function(card){var q=qs[+card.dataset.i],fb=card.querySelector('.pt-fb'),tried=false,solved=false;
  card.querySelectorAll('.pt-o button').forEach(function(b){b.addEventListener('click',function(){if(solved)return;var ok=+b.dataset.j===q.a;
   if(!tried){score.tot++;if(ok)score.ok++;tried=true;upd()}b.classList.add(ok?'ok':'no');fb.hidden=false;
   if(ok){solved=true;fb.className='pt-fb good';fb.innerHTML='Correct! '+(q.h||'')}else{fb.className='pt-fb hint';fb.innerHTML='Not quite, try again. Hint: '+(q.h||'Re-read the lesson linked above.')}})});
  card.querySelector('[data-sa]').addEventListener('click',function(){solved=true;card.querySelectorAll('.pt-o button')[q.a].classList.add('ok');fb.hidden=false;fb.className='pt-fb good';fb.innerHTML='Answer: '+q.o[q.a]+(q.h?' — '+q.h:'')})});}
document.querySelectorAll('.pt-tabs button').forEach(function(b){b.addEventListener('click',function(){seg=b.dataset.seg;document.querySelectorAll('.pt-tabs button').forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false')});topics();render()})});
topic.addEventListener('change',render);mode.addEventListener('change',function(){topic.disabled=mode.value==='x';render()});$('pt-new').addEventListener('click',render);
var h=(location.hash||'').slice(1);if(h&&D.t.some(function(q){return q.seg===h})){seg=h;document.querySelectorAll('.pt-tabs button').forEach(function(x){x.setAttribute('aria-selected',x.dataset.seg===h?'true':'false')})}topics();render()})();</script>"""
    body = (CSS + f'<p class="meta" style="margin:0 0 14px">{len(D["tests"])} questions from every handbook lesson and {len(D["exercises"])} fill-in-the-blank exercises. Pick a course, a topic and a mode. A wrong answer shows a hint so you can try again; "Show answer" reveals the solution.</p>'
            + tabs("pt", counts) + '<div class="pt-bar"><select id="pt-topic" aria-label="Topic"></select><select id="pt-mode" aria-label="Mode"><option value="10">Quiz: 10 random questions</option><option value="all">Quiz: all questions in topic</option><option value="x">Fill-in-the-blank exercises</option></select>'
            + '<button class="btn btn-line btn-sm" type="button" id="pt-new">New set</button><span class="pt-score" id="pt-score">Score 0 / 0</span></div><div id="pt-list"></div>'
            + f'<script type="application/json" id="pt-data">{data}</script>' + js)
    return body, len(D["tests"]) + len(D["exercises"])


def questions_page():
    iv = D["interview"]; counts = {k: len(iv.get(k, [])) for k in SEGS}
    secs = "".join(f'<div class="iv" data-seg="{k}"{"" if i == 0 else " hidden"}>' + "".join(
        f'<details data-s="{E((q["q"] + " " + q["topic"]).lower())}"><summary><span class="n">{n:02d}</span><span>{q["q"]}</span></summary><div class="ans">{q["a"]}<br><a href="{E(q["page"])}">Learn it: {E(q["topic"])} →</a></div></details>'
        for n, q in enumerate(iv[k], 1)) + "</div>" for i, k in enumerate([k for k in SEGS if counts[k]]))
    js = """<script>(function(){var tabs=document.querySelectorAll('.pt-tabs button'),secs=document.querySelectorAll('.iv'),q=document.getElementById('iv-q');
function show(k){tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.seg===k?'true':'false')});secs.forEach(function(s){s.hidden=s.dataset.seg!==k})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.seg)})});
q.addEventListener('input',function(){var v=q.value.trim().toLowerCase();document.querySelectorAll('.iv details').forEach(function(d){d.classList.toggle('pt-hide',!!v&&d.dataset.s.indexOf(v)<0)})});
var h=(location.hash||'').slice(1);if(document.querySelector('.iv[data-seg="'+h+'"]'))show(h)})();</script>"""
    body = (CSS + '<p class="meta" style="margin:0 0 14px">The 100 most important interview questions for each career path, with model answers and a link to the lesson that teaches the topic. Click a question to see the answer.</p>'
            + tabs("iv", counts) + '<div class="pt-bar"><input id="iv-q" type="search" placeholder="Search questions, e.g. SQL, RAG, metrics…" aria-label="Search questions" style="flex:1 1 280px"></div>' + secs + js)
    return body, counts
