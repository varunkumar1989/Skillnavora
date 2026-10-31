"""Practice Lab page (lab.html): ChaturIQ-style challenges that run SQL, Excel and Python in the browser."""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab_data as L
E = html.escape
CSS = """<style>
.lb-segs{display:flex;flex-wrap:wrap;gap:10px;margin:4px 0 14px}.lb-seg{border:1px solid var(--line,#e2dcf3);background:var(--card,#fff);color:inherit;border-radius:14px;padding:12px 18px;font:700 15px var(--display,inherit);cursor:pointer;text-align:left}
.lb-seg small{display:block;font:500 12.5px var(--body,inherit);opacity:.7}.lb-seg[aria-selected=true]{background:linear-gradient(135deg,#6C4CF5,#22D3EE);color:#fff;border-color:transparent}
.lb-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:16px}.lb-chip{border:1px solid var(--line,#e2dcf3);background:var(--card,#fff);color:inherit;border-radius:999px;padding:8px 14px;font:600 14px var(--body,inherit);cursor:pointer}
.lb-chip small{opacity:.6}.lb-chip[aria-pressed=true]{background:#2E3192;color:#fff;border-color:#2E3192}.lb-bar select{margin-left:auto;padding:8px 12px;border:1px solid var(--line,#e2dcf3);border-radius:10px;font:inherit;background:var(--card,#fff);color:inherit}
.lb-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:22px;align-items:start}
.lb-list{display:flex;flex-direction:column;gap:10px;max-height:78vh;overflow:auto;padding-right:4px}
.lb-card{display:flex;flex-direction:column;gap:4px;text-align:left;border:1px solid var(--line,#e2dcf3);background:var(--card,#fff);color:inherit;border-radius:16px;padding:14px 16px;cursor:pointer;font:inherit}
.lb-card:hover{border-color:#6C4CF5;box-shadow:0 8px 24px rgba(108,76,245,.12)}.lb-card b{color:#2E3192;font-size:16px}.lb-q{font-size:13.5px;opacity:.75}
.lb-meta{font-size:12.5px;opacity:.75;display:flex;gap:8px;align-items:center}.lb-lv{font:700 11px var(--display,inherit);letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:999px}
.lv1{background:#DCFCE7;color:#166534}.lv2{background:#FEF3C7;color:#92400E}.lv3{background:#FCE7F3;color:#9D174D}
.lb-play{position:sticky;top:80px;border:1px solid var(--line,#e2dcf3);background:var(--card,#fff);border-radius:22px;padding:20px;box-shadow:0 18px 50px rgba(30,20,80,.10)}
.lb-top{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:10px}.lb-pill{background:rgba(46,49,146,.08);border-radius:999px;padding:6px 12px;font:600 13px var(--body,inherit)}
.lb-h{font-size:19px;margin:6px 0 14px;line-height:1.35}
.lb-tw{overflow:auto;border:1px solid var(--line,#e2dcf3);border-radius:14px;margin-bottom:12px}.lb-t{border-collapse:collapse;width:100%;font:14px ui-monospace,Consolas,monospace}
.lb-t caption{text-align:left;padding:6px 12px;font:600 12px var(--body,inherit);opacity:.6}.lb-t th,.lb-t td{padding:8px 12px;border-bottom:1px solid var(--line,#eee);text-align:left;white-space:nowrap}.lb-t th{background:rgba(46,49,146,.05)}.lb-t i{opacity:.55}
.lb-x th{background:#F1F5F9;color:#475569;font-weight:600;text-align:center}
.lb-edl{display:block;font:600 13px var(--body,inherit);margin:4px 0 6px;opacity:.75}
.lb-ed,.lb-code{width:100%;box-sizing:border-box;font:15px/1.55 ui-monospace,Consolas,monospace;background:#F8FAFC;color:#14112a;border:1px solid var(--line,#e2dcf3);border-radius:14px;padding:12px 14px;white-space:pre;overflow:auto;resize:vertical;margin:0 0 10px}
.lb-run{width:100%;border:0;border-radius:14px;padding:14px;font:700 17px var(--display,inherit);background:#059669;color:#fff;cursor:pointer;box-shadow:0 0 0 6px rgba(5,150,105,.12)}.lb-run:disabled{opacity:.7}
.lb-note{text-align:center;font-size:13px;opacity:.65;margin:8px 0 12px}
.lb-res{border:1px solid var(--line,#e2dcf3);border-radius:14px;padding:12px 16px;background:rgba(46,49,146,.03);margin-bottom:12px}.lb-res small{display:block;font:13px ui-monospace,monospace;opacity:.6}.lb-res b{font:700 28px ui-monospace,monospace}
.lb-err{background:rgba(220,38,38,.06)}.lb-pyout{margin:4px 0 0;font:14px/1.5 ui-monospace,monospace;white-space:pre-wrap}
.lb-decide h3{font-size:17px;margin:4px 0 10px}.lb-dbtn{display:grid;grid-template-columns:1fr 1fr;gap:10px}.lb-dbtn button,.lb-opts button{border:1px solid var(--line,#e2dcf3);background:var(--card,#fff);color:inherit;border-radius:14px;padding:12px;font:600 15px var(--body,inherit);cursor:pointer}
.lb-dbtn button:hover,.lb-opts button:hover{border-color:#6C4CF5}.lb-opts{display:grid;gap:10px}.lb-opts button{text-align:left}.lb-opts button.ok{background:#DCFCE7;border-color:#16a34a}.lb-opts button.no{background:#FEE2E2;border-color:#dc2626}
.lb-fb{margin-top:12px;border-radius:14px;padding:12px 14px}.lb-fb.good{background:#DCFCE7}.lb-fb.warn{background:#FEF3C7}.lb-fb p{margin:6px 0}.lb-fixh{font-weight:700}
.lb-fb{color:#1f2937}.lb-foot{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:14px}.lb-link{background:none;border:0;color:#2E3192;text-decoration:underline;font:inherit;cursor:pointer;padding:0}
.lb-next{border:0;border-radius:10px;padding:9px 14px;background:#2E3192;color:#fff;font:600 14px var(--body,inherit);cursor:pointer}.lb-hint{font-size:14px}
.lb-as{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:10px}.lb-as a{display:block;border:1px solid var(--line,#e2dcf3);border-radius:12px;padding:10px 12px;font-weight:600;text-decoration:none;background:var(--card,#fff)}.lb-as small{display:block;opacity:.6;font-weight:500}
.lb-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 22px}.lb-steps div{border:1px solid var(--line,#e2dcf3);border-radius:16px;padding:14px;background:var(--card,#fff)}.lb-steps b{display:block;font-size:16px}.lb-steps span{font-size:13.5px;opacity:.75}
.lb-prompt{border:1px solid var(--line,#e2dcf3);border-radius:18px;padding:18px;margin:22px 0;background:linear-gradient(135deg,rgba(108,76,245,.06),rgba(34,211,238,.06))}
.lb-prompt textarea{width:100%;box-sizing:border-box;min-height:110px;border:1px solid var(--line,#e2dcf3);border-radius:12px;padding:12px;font:15px/1.5 var(--body,inherit);background:var(--card,#fff);color:inherit}
.lb-score{font-size:16px;margin:10px 0}.lb-rub{list-style:none;padding:0;margin:0;display:grid;gap:6px}.lb-rub li.no{opacity:.85}
@media (max-width:900px){.lb-grid{grid-template-columns:1fr}.lb-play{position:static}.lb-list{max-height:none}.lb-steps{grid-template-columns:1fr}}
</style>"""


def build():
    data = json.dumps({"c": L.C, "a": L.ASSIGN}, ensure_ascii=False).replace("</", "<\\/")
    n = {k: sum(c["seg"] == k for c in L.C) for k in ("pm", "data", "genai")}
    body = CSS + f"""
<div class="lb-steps"><div><b>1 · Run</b><span>Press Run. Code runs in your browser, no sign-up.</span></div><div><b>2 · Watch</b><span>See the real result the code gives.</span></div><div><b>3 · Decide</b><span>Is it right? Spot the trap, get a hint, see the fix.</span></div></div>
<div class="lb-segs" role="tablist">
  <button type="button" role="tab" class="lb-seg" data-seg="data">AI for Data Engineers<small>Excel, SQL, Power BI, Tableau, Python, ML · {n['data']} challenges</small></button>
  <button type="button" role="tab" class="lb-seg" data-seg="pm">AI Product Management<small>Real PM interview scenarios · {n['pm']} challenges</small></button>
  <button type="button" role="tab" class="lb-seg" data-seg="genai">GenAI Launchpad<small>Real-life AI scenarios + prompt checker · {n['genai']} challenges</small></button>
</div>
<div class="lb-bar"><div id="lb-chips" style="display:flex;flex-wrap:wrap;gap:8px"></div><select id="lb-level" aria-label="Level"><option value="All">All levels</option><option>Basic</option><option>Intermediate</option><option>Advanced</option></select></div>
<div class="lb-prompt" id="lb-prompt" hidden><h3 class="h3s" style="margin-top:0">✍️ Prompt checker</h3><p class="meta" style="margin:0 0 10px">Write a prompt for any AI tool. The checker looks for the 6 parts of a great prompt and tells you what to add.</p>
  <textarea id="lb-ptext" aria-label="Your prompt" placeholder="Example: You are a friendly maths teacher. Explain fractions to a class 5 student using a pizza example, in 5 short bullet points. Use simple words."></textarea>
  <button type="button" class="btn btn-primary btn-sm" id="lb-pcheck" style="margin-top:10px">Check my prompt</button><div id="lb-pres"></div></div>
<div class="lb-grid"><div><div class="lb-list" id="lb-list"></div></div><div><div class="lb-play" id="lb-play"><h3 style="margin-top:0">Pick a challenge</h3><p class="meta">Choose any card on the left. Start with Basic, then move to Intermediate and Advanced.</p></div></div></div>
<div id="lb-assign" style="margin-top:28px"></div>
<script type="application/json" id="lab-data">{data}</script>"""
    return body, len(L.C)
