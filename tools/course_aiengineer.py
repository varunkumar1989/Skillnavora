"""Course: AI Engineer, the complete path (role, foundations, ML, LLM engineering, RAG, agents, fine-tuning, evals, LLMOps, data, security, system design, career)."""
import skillsmap as _sm
from coursekit import ill_flow, ill_stack, ill_cycle, ill_quad

def L(key, label):  # link to an existing SkillNavora lesson
    return f'<a href="{_sm.L(key)}">{label}</a>'

COURSE = {
 "slug": "ai-engineer", "pdf": "AI_Engineer_Complete_Path.pdf", "page": "ai-engineer.html",
 "title": "AI Engineer: The Complete Path", "kicker": "SkillNavora · Other programs · Career path",
 "intro": "Everything an AI engineer goes through, from first day to production: the role, Python and software foundations, ML basics, LLM engineering, RAG, agents and MCP, fine-tuning, evals, LLMOps and deployment, data pipelines, security and governance, system design, collaboration, and a 12-month roadmap with projects and interview prep.",
 "oneline": "An AI engineer builds, ships and runs AI-powered software: calling and customising models, connecting them to data and tools, testing quality, deploying reliably, keeping cost, safety and security under control, and improving the system with real usage.",
 "tutor_q": "What does an AI engineer do day to day and what should I learn first?",
 "extra_btn": '<a class="btn btn-line" href="resources.html#other">All Other programs resources</a>',
 "cheat_title": "AI engineer tool stack",
 "classes": [
  ("basic", "The AI engineer role and the lifecycle", "Know what the job is, how it differs from neighbouring roles, and the lifecycle you'll work in.", ill_cycle(["Define problem & success", "Data & context", "Build (prompt, RAG, agent, model)", "Evaluate", "Deploy & monitor", "Improve"], "The AI engineering lifecycle") + r"""
<table><tr><th>Role</th><th>Mainly does</th></tr>
<tr><td><b>AI engineer</b></td><td>Builds products on top of models: LLM apps, RAG, agents, evals, deployment</td></tr>
<tr><td>ML engineer</td><td>Trains and serves custom models, feature pipelines, MLOps</td></tr>
<tr><td>Data scientist</td><td>Analysis, experiments, modelling, insights</td></tr>
<tr><td>Data engineer</td><td>Pipelines, warehouses, data quality</td></tr>
<tr><td>Software engineer</td><td>Application backend/frontend, systems</td></tr>
<tr><td>Forward-deployed engineer</td><td>Builds AI solutions at customer sites</td></tr>
<tr><td>Prompt / context engineer</td><td>Designs instructions and context; a skill inside AI engineering</td></tr></table>
<h3>A typical week</h3><ul><li>Clarify a use case with the PM; define success metrics and an eval set.</li><li>Prototype with a model API; build retrieval and tools; iterate on failures.</li><li>Write services, tests and CI; deploy; watch dashboards for quality, cost and latency.</li><li>Review incidents, update evals, tune prompts, retrieval and models; document decisions.</li></ul>
<p>Learn it here: """ + L("genai-01", "How LLMs work") + " · " + L("genai-12", "Building and shipping a GenAI app") + r""" · <a href="fde-program-link-placeholder"></a></p>""".replace('<a href="fde-program-link-placeholder"></a>', '<a href="guides/fde.html">Forward Deployed Engineer guide</a>'),
   ["AI engineering = software engineering + models + evals + operations.", "Work in a loop: define, build, evaluate, deploy, improve.", "Neighbouring roles overlap; know the boundaries."],
   "Write a one-page 'day in the life' of an AI engineer for a support-copilot project, with 5 tasks."),

  ("basic", "Foundations: Python, software engineering, Git, APIs, Linux", "Build the engineering base that every AI system sits on.", ill_stack([("Python", "language, packaging, virtual envs, typing, async"), ("Software craft", "clean code, tests, debugging, design"), ("Git & GitHub", "branches, pull requests, CI"), ("APIs & the web", "HTTP, REST, JSON, auth, webhooks"), ("Linux & cloud shell", "terminal, processes, SSH, env vars")], "Engineering foundations") + r"""
<table><tr><th>Skill</th><th>Be able to…</th></tr>
<tr><td>Python</td><td>Write functions/classes, use virtualenvs and pip/uv, read/write files and JSON, handle errors, use <code>async</code> for many API calls</td></tr>
<tr><td>Testing</td><td>pytest, fixtures, mocking API calls, writing tests before you ship</td></tr>
<tr><td>Git</td><td>Branch, commit, rebase/merge, open pull requests, resolve conflicts</td></tr>
<tr><td>HTTP/APIs</td><td>Call REST APIs, handle auth, rate limits, retries with backoff, webhooks</td></tr>
<tr><td>SQL & data</td><td>Joins, aggregates, window functions, indexes; pandas for analysis</td></tr>
<tr><td>Terminal</td><td>Navigate, grep, curl, environment variables, secrets handling</td></tr></table>
<h3>Starter script: call a model API with retries</h3><pre>import os, time, requests
def call(prompt, tries=3):
    for i in range(tries):
        r = requests.post(URL, headers={"Authorization": f"Bearer {os.environ['API_KEY']}"},
                          json={"model": MODEL, "messages": [{"role": "user", "content": prompt}]}, timeout=60)
        if r.status_code == 200: return r.json()
        if r.status_code in (429, 500, 502, 503): time.sleep(2 ** i); continue
        r.raise_for_status()
    raise RuntimeError("model API unavailable")</pre>
<p>Learn it here: """ + L("python-01", "Python track (29 lessons)") + " · " + L("sql-01", "SQL track") + " · " + L("agents-01", "APIs without code") + " · " + L("python-24", "APIs, JSON and web scraping") + " · " + L("python-23", "Python and SQL") + "</p>",
   ["Python + testing + Git + HTTP are non-negotiable.", "Handle rate limits and retries from day one.", "Never put secrets in code."],
   "Build a small CLI that calls a model API, handles errors with retries and has 3 pytest tests."),

  ("basic", "Math, statistics and machine-learning essentials", "Know enough ML to choose methods, read metrics and debug models.", r"""
<table><tr><th>Area</th><th>Know</th></tr>
<tr><td>Statistics</td><td>Distributions, sampling, confidence intervals, hypothesis tests, A/B testing</td></tr><tr><td>Linear algebra</td><td>Vectors, matrices, dot product (embeddings), similarity</td></tr>
<tr><td>Calculus intuition</td><td>Gradients, loss minimisation (how models learn)</td></tr><tr><td>ML basics</td><td>Supervised/unsupervised, features, train/validation/test, overfitting, cross-validation, regularisation</td></tr>
<tr><td>Metrics</td><td>Accuracy, precision, recall, F1, ROC-AUC, MAE/RMSE, calibration</td></tr>
<tr><td>Classic models</td><td>Linear/logistic regression, trees, random forest, gradient boosting (XGBoost), k-means</td></tr>
<tr><td>Deep learning</td><td>Neural nets, backpropagation, CNNs, RNNs, transformers, attention; PyTorch basics</td></tr></table>
<p>Learn it here: """ + L("ml-01", "Descriptive statistics") + " · " + L("ml-04", "Hypothesis testing") + " · " + L("ml-15", "Cross-validation and tuning") + " · " + L("ml-19", "Gradient boosting") + " · " + L("genai-01", "How LLMs work (transformers)") + r"""</p>
<p>Tools: scikit-learn, pandas, NumPy, PyTorch, Jupyter, Kaggle for practice.</p>""",
   ["You don't need a PhD: need metrics, validation and intuition.", "Embeddings and similarity are linear algebra in use.", "scikit-learn first, PyTorch when needed."],
   "Train and evaluate a classifier on a Kaggle dataset with proper train/validation/test splits and 3 metrics."),

  ("intermediate", "LLM engineering: model APIs, prompts, structured output, cost and latency", "Build reliable features on top of model APIs.", ill_flow(["Choose model", "Write system prompt + context", "Call API (stream)", "Validate structured output", "Retry / fallback", "Log tokens, cost, latency"], "A production LLM call") + r"""
<ul><li><b>Providers:</b> Anthropic Claude, OpenAI, Google Gemini, plus open models (Llama, Mistral, Qwen, DeepSeek) via Hugging Face, Ollama, vLLM, Groq, Together.</li>
<li><b>Key parameters:</b> system prompt, temperature/sampling (where supported), max tokens, stop sequences, streaming, tool definitions, structured outputs/JSON schema.</li>
<li><b>Tokens & context:</b> price per input/output token, context window limits, prompt caching, batching for cost.</li>
<li><b>Reliability:</b> timeouts, retries with backoff, provider fallbacks, circuit breakers, idempotency.</li>
<li><b>Quality:</b> few-shot examples, chain-of-thought where useful, self-checks, guardrails.</li>
<li><b>Cost & latency:</b> route simple tasks to small models, cache, trim context, stream for perceived speed. Track cost per successful task.</li></ul>
<pre>cost per request = input_tokens × price_in + output_tokens × price_out
latency budget   = retrieval + model + tools + post-processing   (set a target for each)</pre>
<p>Learn it here: """ + L("genai-02", "Prompt engineering in depth") + " · " + L("genai-03", "Calling LLM APIs from Python") + " · " + '<a href="context-engineering.html">Prompt &amp; Context Engineering course</a> · <a href="ai-pricing.html">Pricing &amp; Monetising AI</a></p>',
   ["Treat the model as an unreliable remote service: validate, retry, fall back.", "Track tokens, cost and latency on every call.", "Structured outputs make LLMs usable in code."],
   "Build a function that returns validated JSON from an LLM, with retries, a fallback model and a cost log."),

  ("intermediate", "RAG, embeddings and vector databases", "Build search and question-answering over private data, and measure it.", ill_flow(["Ingest docs (PDF, web, DB)", "Clean & chunk", "Embed", "Store in vector DB + metadata", "Retrieve (hybrid, rerank)", "Generate with citations", "Evaluate"], "RAG pipeline") + r"""
<table><tr><th>Part</th><th>Options and decisions</th></tr>
<tr><td>Ingestion</td><td>Parsers for PDF/HTML/Docs, OCR for scans, incremental refresh, access control metadata</td></tr>
<tr><td>Chunking</td><td>By headings/sections, 300–800 tokens, overlap, keep tables intact</td></tr>
<tr><td>Embeddings</td><td>OpenAI, Cohere, Voyage, Gemini, open models (bge, e5); multilingual for Hindi</td></tr>
<tr><td>Vector stores</td><td>pgvector (Postgres), Pinecone, Qdrant, Weaviate, Milvus, Chroma, FAISS, Elasticsearch/OpenSearch</td></tr>
<tr><td>Retrieval</td><td>Hybrid (BM25 + vectors), metadata filters, query rewriting, rerankers (Cohere Rerank, cross-encoders), MMR</td></tr>
<tr><td>Advanced</td><td>GraphRAG, agentic RAG, multi-vector, parent-document retrieval, caching</td></tr>
<tr><td>Evaluation</td><td>Recall@k, MRR, faithfulness, answer relevance (see AI Evals)</td></tr></table>
<p>Learn it here: """ + L("genai-04", "Embeddings and vector search") + " · " + L("genai-05", "RAG: build, evaluate, improve") + ' · <a href="ai-evals.html">AI Evals</a> · <a href="ai-second-brain.html">AI Second Brain</a></p>',
   ["Retrieval quality limits answer quality.", "Hybrid search + reranking beat vectors alone.", "Measure retrieval and generation separately."],
   "Build a RAG Q&A over 20 PDFs with citations; report recall@3 and faithfulness on 30 questions."),

  ("intermediate", "Agents, tool use and MCP", "Build agents that call tools, with control and observability.", ill_flow(["Goal", "Plan", "Choose tool", "Execute (API / code / browser)", "Observe result", "Decide: continue / ask human / finish"], "Agent loop") + r"""
<ul><li><b>Tool/function calling:</b> describe tools with JSON schemas; the model returns structured calls; your code executes and returns results.</li>
<li><b>MCP (Model Context Protocol):</b> standard way to expose tools and data to AI assistants; build MCP servers for your product; use existing ones (GitHub, Slack, Playwright, databases).</li>
<li><b>Frameworks:</b> LangGraph, LangChain, LlamaIndex, OpenAI Agents SDK, Claude Agent SDK, CrewAI, AutoGen, Pydantic AI; or plain code (often the best start).</li>
<li><b>Patterns:</b> chaining, routing, parallel, orchestrator-workers, evaluator-optimizer (see Orchestration course).</li>
<li><b>Memory:</b> short-term (conversation), long-term (vector store/db), summaries, user profile.</li>
<li><b>Control:</b> step/cost limits, approvals for risky tools, sandboxing code execution, tracing every run.</li>
<li><b>Computer & browser use:</b> Playwright MCP, Browser Use (see Web Automation course).</li></ul>
<p>Learn it here: """ + L("genai-06", "Tool use and function calling") + " · " + L("genai-07", "AI agents and agentic AI") + " · " + L("genai-08", "MCP") + " · " + L("agents-05", "Claude Code tutorial") + ' · <a href="agent-orchestration.html">Agent Orchestration</a> · <a href="web-automation.html">Web Automation</a></p>',
   ["Agents = LLM + tools + loop + guardrails.", "Start with simple workflows; add autonomy when evals justify it.", "MCP standardises tool access."],
   "Build an agent with 3 tools (search, calculator, database lookup) with a step limit and full trace logging."),

  ("advanced", "Customising models: fine-tuning, distillation and open-source models", "Decide when to fine-tune, and how, and when not to.", ill_quad("Effort & cost", "Quality gain on your task", ["Prompting & examples: try first", "RAG: knowledge & freshness", "Fine-tune (LoRA): style, format, narrow tasks", "Train from scratch: almost never"], "Customisation ladder") + r"""
<table><tr><th>Method</th><th>When</th></tr><tr><td>Better prompts and examples</td><td>Always first</td></tr><tr><td>RAG</td><td>Knowledge changes or is private; need citations</td></tr>
<tr><td>Supervised fine-tuning (SFT)</td><td>Consistent style/format, domain behaviour, shorter prompts, cost reduction</td></tr><tr><td>LoRA / QLoRA</td><td>Parameter-efficient tuning of open models on one GPU</td></tr>
<tr><td>Preference tuning (DPO, RLHF concepts)</td><td>Align outputs with human preferences</td></tr><tr><td>Distillation</td><td>Teach a small, cheap model from a large one's outputs</td></tr></table>
<h3>Fine-tuning workflow</h3><ol><li>Collect 500–5,000 high-quality examples (inputs and ideal outputs); clean and split train/validation/test.</li><li>Baseline with prompting; define eval metrics first.</li><li>Fine-tune (provider fine-tuning APIs, or Hugging Face Transformers, PEFT, TRL, Unsloth, Axolotl).</li><li>Evaluate against the baseline on held-out data; check regressions and safety.</li><li>Deploy (vLLM, TGI, Ollama, or provider-hosted); monitor drift; retrain on new data.</li></ol>
<p>Learn it here: """ + L("genai-10", "Customising models: prompting vs RAG vs fine-tuning, LoRA") + ' · <a href="ml-products.html">ML Products for PMs</a></p>',
   ["Prompting → RAG → fine-tuning, in that order.", "Data quality beats data quantity.", "Always compare with a prompting baseline."],
   "Plan (data, metric, baseline, hardware, evaluation) a LoRA fine-tune for classifying support tickets."),

  ("advanced", "Evals, observability, guardrails and red-teaming", "Make quality measurable and keep it that way.", r"""
<ul><li><b>Evals:</b> golden dataset, code and LLM-judge graders, human review, regression suite in CI (see AI Evals course).</li>
<li><b>Observability:</b> trace every request (prompt, retrieved docs, tool calls, tokens, cost, latency); tools: Langfuse, LangSmith, Arize Phoenix, Braintrust, OpenTelemetry.</li>
<li><b>Guardrails:</b> input checks (PII, injection), output checks (schema, toxicity, policy), allow-lists for tools, rate limits; libraries such as Guardrails AI, NeMo Guardrails, Llama Guard, provider moderation APIs.</li>
<li><b>Red-teaming:</b> jailbreaks, prompt injection, data exfiltration, harmful content, bias tests; add each finding to the eval set.</li>
<li><b>Online quality:</b> sample live traffic, judge scores, user feedback, A/B tests.</li></ul>
<p>Learn it here: """ + L("genai-09", "Evaluating LLM applications and guardrails") + ' · <a href="ai-evals.html">AI Evals for PMs</a> · <a href="ai-governance.html">AI Governance</a></p>',
   ["No eval, no launch.", "Trace everything to debug fast.", "Guardrails are layers, not a single filter."],
   "Add tracing and a 50-case regression eval to your RAG app and run it in CI."),

  ("advanced", "Deployment and LLMOps: APIs, containers, cloud, CI/CD, scaling and cost", "Ship AI services that are reliable, fast and affordable.", ill_flow(["Code + tests", "Docker image", "CI: lint, test, evals", "Deploy (cloud / serverless)", "Gateway: auth, rate limit, cache", "Monitor & alert", "Roll back / canary"], "From commit to production") + r"""
<table><tr><th>Area</th><th>What to know</th></tr>
<tr><td>Serving</td><td>FastAPI/Flask/Node services, streaming (SSE/WebSockets), background queues (Celery, SQS, Pub/Sub), async I/O</td></tr>
<tr><td>Containers</td><td>Docker, docker-compose, Kubernetes basics</td></tr><tr><td>Cloud</td><td>AWS (Bedrock, Lambda, ECS, S3), Google Cloud (Vertex AI, Cloud Run), Azure (OpenAI Service, Container Apps); Cloudflare Workers/Pages</td></tr>
<tr><td>GPUs & model serving</td><td>vLLM, TGI, Triton, Ollama; quantisation (GGUF, AWQ); batching; autoscaling</td></tr>
<tr><td>Gateways</td><td>LiteLLM, OpenRouter, Cloudflare AI Gateway: routing, fallbacks, caching, budgets</td></tr>
<tr><td>Release safety</td><td>Feature flags, canary releases, A/B tests, prompt/model versioning, rollbacks</td></tr>
<tr><td>Reliability</td><td>Timeouts, retries, circuit breakers, idempotency, graceful degradation</td></tr>
<tr><td>Cost control</td><td>Budgets and alerts, model routing, caching, batching, trimming context, monitoring cost per successful task</td></tr></table>
<p>Learn it here: """ + L("genai-12", "Building and shipping a GenAI app") + " · " + L("tools-02", "n8n tutorial") + ' · <a href="agent-orchestration.html">Agent Orchestration &amp; Monitoring</a></p>',
   ["Containerise, test, evaluate, deploy, monitor.", "Use a gateway for routing, caching and budgets.", "Version prompts and models like code."],
   "Deploy your RAG API with Docker on a cloud service with a health check, logs and a cost alert."),

  ("advanced", "Data engineering for AI, security and governance", "Feed AI systems good data and keep them safe and compliant.", r"""
<h3>Data for AI</h3><ul><li>Pipelines (Airflow, Prefect, dbt) that clean, deduplicate and refresh documents and vector indexes.</li><li>Data quality checks, lineage, versioned datasets; labelling workflows (Label Studio, human review).</li><li>Synthetic data with review; privacy: mask PII before it reaches prompts, logs or training.</li></ul>
<h3>Security (OWASP Top 10 for LLM apps)</h3><table><tr><th>Risk</th><th>Control</th></tr><tr><td>Prompt injection (direct and from documents/web)</td><td>Treat content as data; separate instructions; restrict tool permissions; approvals</td></tr>
<tr><td>Sensitive data leakage</td><td>Access control in retrieval, redaction, no secrets in prompts, tenant isolation</td></tr><tr><td>Insecure output handling</td><td>Validate/escape model output; never run model-written code unsandboxed</td></tr>
<tr><td>Excessive agency</td><td>Least privilege tools, spend/step limits, human approval</td></tr><tr><td>Supply chain (models, packages)</td><td>Pin versions, scan dependencies, trusted model sources</td></tr><tr><td>Denial of wallet</td><td>Rate limits, quotas, budgets</td></tr></table>
<h3>Governance</h3><p>DPDP Act consent and minimisation, EU AI Act risk tiers, audit logs, system cards, incident response (see AI Governance course).</p>
<p>Learn it here: <a href="ai-governance.html">AI Governance &amp; Responsible AI</a> · """ + L("sql-02", "Data modelling") + ' · <a href="web-automation.html">Web Automation (secure webhooks)</a></p>',
   ["Good data pipelines keep RAG fresh and safe.", "Know the OWASP LLM risks and their controls.", "Least privilege for every agent tool."],
   "Write a threat model for an AI support agent that can issue refunds."),

  ("advanced", "System design for AI products and working with the team", "Design end-to-end AI systems and collaborate across roles.", ill_stack([("Client", "web/mobile/voice, streaming UI"), ("API & gateway", "auth, rate limits, routing, caching"), ("Orchestrator", "prompts, retrieval, tools, guardrails"), ("Models & tools", "LLMs, vector DB, APIs, code sandbox"), ("Data & observability", "logs, traces, evals, feedback, cost")], "Reference architecture for an AI assistant") + r"""
<h3>How to answer an AI system-design question</h3><ol><li>Clarify users, scale, languages, latency and quality targets, risks.</li><li>Sketch the architecture (above) and the data flow.</li><li>Pick approaches with trade-offs: prompting vs RAG vs fine-tune; one model vs routing; sync vs async.</li><li>Cover evals, safety, observability, cost and failure handling.</li><li>Discuss rollout: shadow, canary, A/B, human fallback.</li></ol>
<h3>Common designs to practise</h3><ul><li>Customer-support copilot (RAG + tools + handoff)</li><li>Document processing pipeline (OCR → extraction → validation → human review)</li><li>Voice agent for appointments (STT → LLM → TTS, barge-in, latency)</li><li>Code assistant (indexing, context selection, sandbox, tests)</li><li>Internal knowledge search with permissions</li><li>Recommendation or search ranking with LLM reranking</li></ul>
<h3>Working with PMs, designers and data teams</h3><ul><li>Turn PRDs into eval sets and acceptance criteria; push back with data on feasibility and cost.</li><li>Demo early with real outputs including failures; document assumptions and limits.</li><li>Be on-call for AI quality: incident reviews, postmortems, new tests.</li></ul>
<p>Learn it here: <a href="ai-product-strategy.html">AI Product Strategy</a> · <a href="ai-ux-design.html">Designing AI Experiences</a> · <a href="platform-api-pm.html">Platform &amp; API PM</a></p>""",
   ["Always state trade-offs and failure handling.", "Evals, safety and cost belong in every design.", "Great AI engineers translate between product and models."],
   "Design a document-processing AI system for insurance claims and present it in 10 minutes."),

  ("advanced", "Career: roadmap, portfolio projects, interviews and job descriptions", "Plan 12 months, build proof, and prepare for hiring loops.", r"""
<h3>12-month roadmap</h3><table><tr><th>Months</th><th>Focus</th><th>Proof</th></tr>
<tr><td>1–2</td><td>Python, Git, SQL, HTTP/APIs, testing</td><td>3 small tools on GitHub</td></tr><tr><td>3–4</td><td>ML basics, statistics, scikit-learn, one Kaggle project</td><td>Notebook with metrics and error analysis</td></tr>
<tr><td>5–6</td><td>LLM APIs, prompts, structured output, RAG</td><td>RAG app with citations and evals</td></tr><tr><td>7–8</td><td>Agents, tools, MCP, workflows</td><td>Agent with tracing and approvals</td></tr>
<tr><td>9–10</td><td>Evals, deployment, Docker, cloud, monitoring</td><td>Deployed app with CI and dashboards</td></tr><tr><td>11–12</td><td>Fine-tuning, system design, interviews, applications</td><td>Capstone + case studies + mock interviews</td></tr></table>
<h3>10 portfolio projects</h3><ol><li>Chat with your documents (RAG, citations)</li><li>Support copilot with ticket tools</li><li>Text-to-SQL analyst with guardrails</li><li>Resume/job matcher with embeddings</li><li>Voice appointment bot</li><li>Browser research agent with Playwright MCP</li><li>Document extraction pipeline (OCR → JSON → validation)</li><li>LoRA fine-tuned classifier vs prompting baseline</li><li>LLM eval harness with CI</li><li>Cost-aware model router with a dashboard</li></ol>
<h3>Interview loop</h3><ul><li><b>Coding:</b> Python, data structures, API handling; (see DSA lessons).</li><li><b>ML:</b> metrics, overfitting, validation, embeddings, transformers.</li><li><b>LLM:</b> RAG design, prompt/context, evals, hallucination, cost/latency, guardrails.</li><li><b>System design:</b> one AI architecture end to end.</li><li><b>Behavioural:</b> ownership, incidents, collaboration with product.</li></ul>
<h3>What job descriptions usually ask for</h3><p>Python; LLM APIs; RAG and vector databases; agents/tool use; evaluation and testing; cloud and containers; CI/CD; SQL and data pipelines; security and responsible AI; strong communication. (Read real postings and tick off what you can already show.)</p>
<p>Learn it here: """ + L("career-03", "Data Scientist, ML and GenAI interview preparation") + " · " + L("career-01", "Portfolio, GitHub and resume") + " · " + L("career-04", "Your 90-day plan") + " · " + L("python-26", "DSA I") + ' · <a href="questions.html#genai">Top GenAI questions</a> · <a href="lab.html">Practice Lab</a> · <a href="jobs.html">Job board</a></p>',
   ["Build proof, not just courses: 10 projects.", "Prepare coding, ML, LLM, system design and behavioural rounds.", "Match your portfolio to real job descriptions."],
   "Pick 3 projects, build them over the next 8 weeks, and publish each with a README, demo and eval results."),
 ],
 "templates_html": """<h3>A. AI project one-pager</h3><table><tr><th>Field</th><th>Fill in</th></tr><tr><td>Problem & user</td><td></td></tr><tr><td>Success metric & eval set</td><td></td></tr><tr><td>Approach (prompt / RAG / agent / fine-tune)</td><td></td></tr><tr><td>Data sources & access control</td><td></td></tr><tr><td>Architecture sketch</td><td></td></tr><tr><td>Risks & guardrails</td><td></td></tr><tr><td>Cost & latency budget</td><td></td></tr><tr><td>Deployment & monitoring</td><td></td></tr></table>
<h3>B. Production readiness checklist</h3><pre>[ ] Evals pass in CI   [ ] Tracing on   [ ] Secrets in env/secret manager   [ ] Rate limits & budgets
[ ] Prompt/model versions pinned   [ ] Fallback & timeouts   [ ] PII handling   [ ] Rollback plan   [ ] On-call owner</pre>
<h3>C. 12-month tracker</h3><pre>month | focus | project | proof link | done</pre>""",
 "cheat": [("Languages & libs", "Python, TypeScript; requests/httpx, pydantic, FastAPI, pytest, pandas, NumPy, scikit-learn, PyTorch"), ("Model APIs", "Anthropic Claude, OpenAI, Google Gemini; open models via Hugging Face, Ollama, vLLM, Groq, Together"),
           ("Frameworks", "LangGraph, LangChain, LlamaIndex, OpenAI Agents SDK, Claude Agent SDK, CrewAI, Pydantic AI"), ("Vector stores", "pgvector, Pinecone, Qdrant, Weaviate, Milvus, Chroma, FAISS, OpenSearch"),
           ("Evals & tracing", "promptfoo, Ragas, DeepEval, Inspect, Langfuse, LangSmith, Arize Phoenix, Braintrust"), ("Fine-tuning", "Hugging Face Transformers, PEFT, TRL, Unsloth, Axolotl; provider fine-tuning APIs"),
           ("Serving & gateways", "FastAPI, vLLM, TGI, Triton, Ollama, LiteLLM, OpenRouter, Cloudflare AI Gateway"), ("Infra", "Docker, Kubernetes, AWS/GCP/Azure, Cloudflare, GitHub Actions"),
           ("Data", "Postgres, DuckDB, Airflow, Prefect, dbt, Label Studio"), ("Safety", "Guardrails AI, NeMo Guardrails, Llama Guard, OWASP LLM Top 10"), ("Automation", "n8n, Zapier, Make, Playwright, Playwright MCP")],
 "qa": [("What does an AI engineer do?", "Builds, evaluates, deploys and operates AI-powered software: model APIs, RAG, agents and tools, evals, guardrails, cloud deployment and monitoring, with attention to cost, latency and safety."),
        ("AI engineer vs ML engineer?", "AI engineers mostly build products on existing models (prompts, RAG, agents, evals); ML engineers train and serve custom models and run ML pipelines. The roles overlap."),
        ("How would you design a RAG system?", "Ingest and chunk documents with metadata, embed, store in a vector DB, retrieve with hybrid search and reranking, generate with citations, enforce access control, evaluate retrieval and faithfulness, monitor and refresh."),
        ("When do you fine-tune?", "After prompting and RAG fall short: for consistent style or format, narrow tasks, or to lower cost with a smaller model; compare to a prompting baseline on held-out data."),
        ("How do you evaluate an LLM application?", "Golden dataset with slices, code and LLM-judge graders calibrated to humans, regression tests in CI, online metrics and sampled judging."),
        ("How do you reduce hallucinations?", "Ground answers in retrieved sources, require citations and 'not found', use structured outputs, add verification steps and evals, and escalate low-confidence cases."),
        ("How do you control cost and latency?", "Route to smaller models, cache, trim context, stream, batch, set budgets, and track cost per successful task."),
        ("What are the main security risks of LLM apps?", "Prompt injection, data leakage, insecure output handling, excessive agency, supply chain and denial of wallet; mitigate with least privilege, validation, sandboxing, approvals and rate limits."),
        ("Explain MCP.", "The Model Context Protocol standardises how AI assistants connect to tools and data; you can build MCP servers to expose your product and use existing ones."),
        ("Walk through deploying an AI service.", "FastAPI service in Docker, CI with tests and evals, deploy to cloud, gateway for auth/limits/routing, tracing and alerts, canary rollout and rollback."),
        ("How do you handle a quality regression in production?", "Check traces, compare against the eval set, identify cause (prompt, retrieval, model update, data drift), roll back, fix, add a regression test."),
        ("What projects would you show in a portfolio?", "A cited RAG app, an agent with tracing, an eval harness in CI, a deployed service with monitoring, and a fine-tune vs prompt comparison.")],
 "glossary": [("LLMOps", "Operating LLM apps in production: deployment, monitoring, evals, cost"), ("Embedding", "Vector capturing the meaning of text"), ("Reranker", "Model that reorders retrieved results by relevance"), ("LoRA", "Parameter-efficient fine-tuning method"),
              ("Quantisation", "Reducing model precision to run cheaper/faster"), ("Gateway", "Layer for routing, auth, caching and budgets across model providers"), ("Tracing", "Recording each step of a request for debugging")],
 "links": [("Hugging Face LLM course", "https://huggingface.co/learn/llm-course"), ("DeepLearning.AI short courses", "https://www.deeplearning.ai/short-courses/"), ("LLM Zoomcamp (DataTalks.Club)", "https://github.com/DataTalksClub/llm-zoomcamp"),
           ("MLOps Zoomcamp", "https://github.com/DataTalksClub/mlops-zoomcamp"), ("fast.ai Practical Deep Learning", "https://course.fast.ai/"), ("Andrej Karpathy: Neural Networks Zero to Hero", "https://karpathy.ai/zero-to-hero.html"),
           ("Anthropic: Building effective agents", "https://www.anthropic.com/research/building-effective-agents"), ("OpenAI Cookbook", "https://cookbook.openai.com/"), ("LangChain Academy", "https://academy.langchain.com/"),
           ("OWASP Top 10 for LLM apps", "https://genai.owasp.org/"), ("Chip Huyen: AI Engineering (book site)", "https://huyenchip.com/books/"), ("Full Stack Deep Learning", "https://fullstackdeeplearning.com/"), ("Eugene Yan: patterns for LLM systems", "https://eugeneyan.com/writing/llm-patterns/")],
}
