"""AI Product Management 2: the detailed 26-subject AI PM curriculum as a separate programme page (A/B variant).

Content comes from tools/aipm2/*.txt so the site page and the standalone guide artifact share one source.
The original AI Product Management programme (programme-pm) is not changed.
"""
import html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aipm2
from aipm2 import extras
E = html.escape
SUBJECTS = aipm2.load()
N_TOPICS = sum(len(s["topics"]) for s in SUBJECTS)
GUIDE_URL = "https://claude.ai/artifact/PLACEHOLDER"   # replaced by the published artifact link (see GUIDE_LINK_FILE)
_LINK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aipm2", "guide_url.txt")

def guide_url():
    try:
        u = open(_LINK_FILE).read().strip()
        return u or None
    except OSError:
        return None

# existing SkillNavora AI PM material, mapped to the subjects it supports
EXISTING = [
    ("programme-pm.html", "AI Product Management (original programme)", "The programme you already have: PM Master Handbook, PRD and BRD templates, interview prep.", "1-9, 26"),
    ("handbooks/pm/index.html", "Interactive PM Handbook", "23 modules: product core, AI tools lab, frameworks, case studies and interview prep.", "1-9, 26"),
    ("product-ops.html", "Product Operations", "Free PDF, basic to advanced.", "1, 22"),
    ("product-design-for-pms.html", "Product Design for PMs", "UX, prototyping and design collaboration.", "4"),
    ("prd-library.html", "PRD library", "Template, framing guide and 120 PRD ideas.", "5"),
    ("prd-writer.html", "AI PRD Writer", "Draft a PRD with AI.", "5"),
    ("brd-frd.html", "BRD and FRD guide", "Business and functional requirement documents.", "5"),
    ("system-design-for-pms.html", "System Design and Databases for PMs", "Architecture, databases and trade-offs.", "10, 16"),
    ("platform-api-pm.html", "Platform and API Product Management", "API products, versioning and developer experience.", "10, 23"),
    ("ml-products.html", "Machine Learning Products for PMs", "ML concepts, metrics and lifecycle.", "11, 12"),
    ("context-engineering.html", "Prompt and Context Engineering", "13 classes with templates.", "13"),
    ("ai-agents-guide.html", "How AI Agents Work", "Single and multi-agent systems, context and evals.", "15"),
    ("agent-orchestration.html", "Agent Orchestration and Monitoring", "Orchestrating and observing agents.", "15, 17"),
    ("ai-evals.html", "AI Evals for Product Managers", "Evaluation methods and datasets.", "17"),
    ("ai-governance.html", "AI Governance and Responsible AI", "Risk, safety and compliance.", "18"),
    ("ai-ux-design.html", "Designing AI Experiences (AI UX)", "Trust, uncertainty and human-AI interaction.", "19"),
    ("ai-product-strategy.html", "AI Product Strategy", "Opportunities, positioning and strategy.", "20"),
    ("ai-pricing.html", "Pricing and Monetising AI Products", "Pricing models and unit economics.", "20"),
    ("ai-academy.html", "AI Skills Academy", "Every AI skills course in one place.", "13, 15, 17, 21"),
    ("questions.html", "Top 100 interview questions", "Practice questions with answers.", "26"),
    ("ai-pm-industry-research.html#interview-guide", "AI PM interview guide (27 questions)", "Model answers tied to job-description research.", "26"),
    ("ai-pm-industry-research.html", "AI PM industry research", "Courses, job records and skills employers name most.", "26"),
    ("tests.html", "Practice tests", "Timed tests by programme.", "26"),
    ("quiz.html", "Quiz zone", "Short quizzes.", "26"),
    ("practice-hub.html", "Interview prep hub", "Questions, tests and quizzes.", "26"),
    ("pm-toolkit.html", "AI PM Toolkit", "Templates and helpers for PM work.", "5, 26"),
    ("ai-tutor.html", "AI Tutor", "Ask questions on any topic.", "all"),
    ("study-library.html", "Study Library", "Every lesson, class and PDF by programme.", "all"),
]

TOOLS = [  # (name, description, official url) - official sites; check them for current features
    ("ChatGPT", "OpenAI assistant.", "https://chatgpt.com/"), ("Claude", "Anthropic assistant and API.", "https://claude.ai/"),
    ("Gemini", "Google assistant and models.", "https://gemini.google.com/"), ("Perplexity", "Answer engine with citations.", "https://www.perplexity.ai/"),
    ("NotebookLM", "Ask questions of your own sources.", "https://notebooklm.google.com/"), ("Cursor", "AI code editor.", "https://cursor.com/"),
    ("Lovable", "Prompt-to-app builder.", "https://lovable.dev/"), ("Replit", "Browser IDE with an AI agent.", "https://replit.com/"),
    ("Bolt", "Prompt-to-app builder.", "https://bolt.new/"), ("n8n", "Workflow automation.", "https://n8n.io/"),
    ("Make", "Visual automation.", "https://www.make.com/"), ("Zapier", "No-code automation.", "https://zapier.com/"),
    ("LangChain", "LLM application framework.", "https://www.langchain.com/"), ("LangGraph", "Stateful agent workflows.", "https://www.langchain.com/langgraph"),
    ("LlamaIndex", "Data and retrieval framework.", "https://www.llamaindex.ai/"), ("CrewAI", "Multi-agent framework.", "https://www.crewai.com/"),
    ("Pinecone", "Managed vector database.", "https://www.pinecone.io/"), ("Weaviate", "Open-source vector database.", "https://weaviate.io/"),
    ("Chroma", "Lightweight vector store.", "https://www.trychroma.com/"), ("Postman", "API testing and docs.", "https://www.postman.com/"),
    ("GitHub", "Code hosting and collaboration.", "https://github.com/"), ("Figma", "Design and prototyping.", "https://www.figma.com/"),
    ("Jira", "Issue and sprint tracking.", "https://www.atlassian.com/software/jira"), ("Linear", "Issue tracking.", "https://linear.app/"),
    ("Notion", "Docs and wikis.", "https://www.notion.com/"), ("Mixpanel", "Product analytics.", "https://mixpanel.com/"),
    ("Amplitude", "Product analytics.", "https://amplitude.com/"), ("LangSmith", "LLM tracing and evals.", "https://www.langchain.com/langsmith"),
    ("Arize Phoenix", "Open-source LLM observability.", "https://phoenix.arize.com/"), ("MLflow", "Experiment tracking and model registry.", "https://mlflow.org/"),
    ("Amazon Bedrock", "Managed foundation models on AWS.", "https://aws.amazon.com/bedrock/"), ("Azure AI Foundry", "AI platform on Azure.", "https://azure.microsoft.com/products/ai-foundry"),
    ("Google Vertex AI", "AI platform on Google Cloud.", "https://cloud.google.com/vertex-ai"),
    ("Anthropic: Building effective agents", "Agent design patterns.", "https://www.anthropic.com/engineering/building-effective-agents"),
    ("NIST AI Risk Management Framework", "Risk framework for AI.", "https://www.nist.gov/itl/ai-risk-management-framework"),
]

CSS = """<style>
.a2-note{background:#f5f3ff;border:1px solid #e3dff5;color:#1d1b2e;border-radius:12px;padding:14px 16px;margin:0 0 18px}
.a2-kpi{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 18px}.a2-kpi div{border:1px solid var(--line);border-radius:12px;padding:10px 16px;min-width:130px;background:var(--surface)}
.a2-kpi b{display:block;font:800 24px var(--display)}
.a2-find{width:100%;max-width:520px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;background:var(--surface);color:inherit;margin:0 0 12px}
.a2-sub{border:1px solid var(--line);border-radius:12px;margin:10px 0;background:var(--surface)}
.a2-sub>summary{cursor:pointer;padding:13px 16px;font-weight:700;list-style:none;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.a2-sub>summary::-webkit-details-marker{display:none}.a2-sub>summary .n{font:800 13px var(--display);color:var(--brand,#6C4CF5)}
.a2-sub>summary .c{margin-left:auto;font-weight:500;font-size:13px;opacity:.7}
.a2-body{padding:0 16px 14px}.a2-body p.ov{margin:0 0 10px;opacity:.85}
.a2-tp{margin:0;padding:0;list-style:none;counter-reset:t}.a2-tp li{padding:8px 0;border-top:1px solid var(--line);counter-increment:t}
.a2-tp li b::before{content:counter(t) ". ";opacity:.55;font-weight:600}.a2-tp li span{display:block;opacity:.85;font-size:14.5px;margin-top:2px}
.a2-ph{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px}.a2-ph a{border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;background:var(--surface)}
.a2-chk{columns:2;column-gap:28px;padding-left:18px}@media(max-width:640px){.a2-chk{columns:1}}
.a2-ex{display:block;text-decoration:none}.a2-ex .sj{font-size:12px;opacity:.7}
</style>"""

def _subject(s, open_=False):
    items = "".join(f"<li data-t=\"{E((n + ' ' + t).lower(), quote=True)}\"><b>{E(n)}</b><span>{E(t)}</span></li>" for n, t in s["topics"])
    extra = ""
    if s["n"] == 25:
        extra = ("<h4 style=\"margin:14px 0 6px\">Every capstone must include</h4><ul class=\"a2-chk\">" + "".join(f"<li>{E(x)}</li>" for x in extras.CAPSTONE_CHECKLIST) + "</ul>")
    return (f'<details class="a2-sub" id="a2-s{s["n"]:02d}"{" open" if open_ else ""}><summary><span class="n">SUBJECT {s["n"]:02d}</span>{E(s["title"])}'
            f'<span class="c">{len(s["topics"])} topics</span></summary><div class="a2-body"><p class="ov">{E(s["overview"])}</p><ol class="a2-tp" style="list-style:none">{items}</ol>{extra}</div></details>')

def content():
    g = guide_url()
    guide_btn = (f'<a class="btn btn-primary btn-sm" href="{E(g)}" target="_blank" rel="noopener" data-nogate>Open the complete guide ↗</a>' if g else "")
    phases = "".join(f'<a href="#a2-s{ns[0]:02d}">{E(name)}: {ns[0]}-{ns[-1]}</a>' for name, ns in extras.PHASES)
    existing = "".join(
        f'<a class="card a2-ex" href="{E(h)}"><span class="ftag">Subjects {E(sj)}</span><h3 style="margin:6px 0 2px;font-size:16px">{E(t)}</h3><p style="margin:0">{E(d)}</p><span class="go">Open →</span></a>'
        for h, t, d, sj in EXISTING)
    js = """<script>(function(){var q=document.getElementById('a2-find');if(!q)return;var subs=[].slice.call(document.querySelectorAll('.a2-sub'));
function run(){var v=q.value.trim().toLowerCase(),shown=0;subs.forEach(function(d){var hit=0;[].slice.call(d.querySelectorAll('.a2-tp li')).forEach(function(li){var m=!v||li.dataset.t.indexOf(v)>-1;li.hidden=!m;if(m)hit++});
var t=d.querySelector('summary').textContent.toLowerCase();d.hidden=!!v&&!hit&&t.indexOf(v)<0;if(v&&hit)d.open=true;if(!d.hidden)shown+=hit});
var o=document.getElementById('a2-count');if(o)o.textContent=v?shown+' matching topics':''}
q.addEventListener('input',run)})();</script>"""
    return (CSS
        + f'<div class="a2-note"><b>Detailed AI PM course.</b> The full {len(SUBJECTS)}-subject, {N_TOPICS}-topic curriculum, from product management fundamentals to generative AI, LLMs and agentic AI product leadership. '
          f'It sits next to the original <a href="programme-pm.html">AI Product Management</a> programme, which is unchanged, so you can compare the two. '
          f'Section 3 maps your existing SkillNavora AI PM material onto these subjects.</div>'
        + f'<div class="a2-kpi"><div><b>{len(SUBJECTS)}</b>subjects</div><div><b>{N_TOPICS}</b>topics</div><div><b>12</b>capstone projects</div><div><b>{len(extras.OUTCOMES)}</b>outcomes</div></div>'
        + f'<div class="hb-acts" style="margin:0 0 18px">{guide_btn}<a class="btn btn-line btn-sm" href="ai-pm-industry-research.html#interview-guide">Interview guide</a><a class="btn btn-line btn-sm" href="programme-pm.html">Original AI PM programme</a></div>'
        + '<h2 class="sec-h">1. Course curriculum</h2>'
        + f'<p class="meta" style="margin:-4px 0 12px">{E(extras.TITLE)}: {E(extras.SUBTITLE)}.</p>'
        + f'<div class="a2-ph">{phases}</div>'
        + '<input id="a2-find" class="a2-find" type="search" placeholder="Search all topics, e.g. RAG, pricing, SQL" aria-label="Search topics"><span id="a2-count" class="meta" style="margin-left:8px"></span>'
        + "".join(_subject(s, s["n"] == 1) for s in SUBJECTS)
        + '<h2 class="sec-h" style="margin-top:30px">2. Course completion outcomes</h2><p class="meta" style="margin:-4px 0 8px">By completing the curriculum, learners should be able to:</p><ul>'
        + "".join(f"<li>{E(o)}</li>" for o in extras.OUTCOMES) + f'</ul><p><b>Positioning:</b> {E(extras.POSITIONING)}</p>'
        + '<h2 class="sec-h" style="margin-top:30px">3. Your existing AI PM material, mapped to this course</h2>'
        + '<p class="meta" style="margin:-4px 0 12px">Everything already on SkillNavora that supports these subjects. Nothing here was changed.</p>'
        + f'<div class="grid g3">{existing}</div>' + js)

def tools():
    cards = "".join(f'<a class="card" href="{E(u)}" target="_blank" rel="noopener" style="display:block;text-decoration:none"><span class="ftag">Tool</span>'
                    f'<h3 style="margin:6px 0 2px;font-size:16px">{E(n)}</h3><p style="margin:0">{E(d)}</p><span class="go">Official site ↗</span></a>' for n, d, u in TOOLS)
    return f'<h2 class="sec-h">Tools and learning links</h2><p class="meta" style="margin:-4px 0 12px">The tools named in Subject 21 and related guides, linked to their official sites. Features change quickly, so check each site.</p><div class="grid g3">{cards}</div>'
