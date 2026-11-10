import html as H
def E(t): return H.escape(str(t), quote=False)
MODULES=[
("1","Programming and Software Engineering Foundations",[
 ("1.1","Introduction to Programming",["What is programming and what is software","How computers execute instructions","Programming languages; compiled vs interpreted","Frontend vs backend","Development environments and IDEs","How applications are created and how software communicates"]),
 ("1.2","Python Fundamentals",["Installation and environment setup","Variables, data types, strings and numbers","Lists, tuples, sets and dictionaries","Operators, conditions and loops","Functions, parameters and return values","Modules and packages; file handling; exception handling","Object-oriented programming: classes, objects, inheritance","JSON, CSV and Excel; virtual environments; pip; reusable code"]),
 ("1.3","JavaScript and TypeScript",["JavaScript fundamentals, variables, functions, arrays and objects","ES6 concepts; Promises; async and await; JSON","TypeScript types, interfaces and type safety","JavaScript vs TypeScript; practical API integration"]),
 ("1.4","Data Structures and Algorithms",["Arrays, linked lists, stacks, queues, hash tables, trees and graphs","Searching, sorting and recursion","Big O notation, time and space complexity, problem decomposition"]),
 ("1.5","Git and GitHub",["Repositories, cloning, committing, branching and merging","Pull requests, conflict resolution, README files","Issues, projects and portfolio development"]),
 ("1.6","Software Engineering",["Software Development Life Cycle; Agile; Scrum and Kanban","Requirements analysis, software design, modular programming, clean code","Code reviews, testing fundamentals, debugging, logging, documentation","Design patterns, SOLID principles, refactoring, maintenance"]),
 ("1.7","Development Tools",["VS Code, Cursor, GitHub, GitHub Copilot, Claude Code","Terminal and command line; package managers; debugging tools","Using AI coding assistants responsibly without accepting code blindly"])]),
("2","Data Engineering, Databases and Data Integration",[
 ("2.1","Data Fundamentals",["Types of data: structured, semi-structured, unstructured","Formats: JSON, XML, CSV, Excel","Data validation, quality and integrity"]),
 ("2.2","SQL and PostgreSQL",["Databases, tables, rows, columns, primary and foreign keys","SELECT, WHERE, GROUP BY, ORDER BY, JOIN, subqueries, CTEs, window functions","Aggregate functions, indexing, optimisation, transactions, normalisation","PostgreSQL installation and setup"]),
 ("2.3","Database Technologies",["PostgreSQL, Supabase, MySQL, MongoDB, Redis, SQLite","Vector stores: Pinecone, Qdrant, pgvector","Relational vs NoSQL vs vector databases"]),
 ("2.4","APIs and Data Integration",["What an API is; REST; GraphQL fundamentals; HTTP methods","Requests, responses, headers, authentication, API keys, OAuth, webhooks","Rate limits, pagination, API documentation, Postman, API testing","Third-party integration, error handling, API security"]),
 ("2.5","Data Engineering",["Data pipelines, ETL vs ELT, ingestion, transformation, cleaning, validation","Batch and stream processing; orchestration","Data warehouses, data lakes, lakehouses, data governance"])]),
("3","Artificial Intelligence and Machine Learning",[
 ("3.1","AI Fundamentals",["AI vs ML vs deep learning; generative vs traditional AI","Neural networks; training vs inference; parameters","Features, labels, datasets, model limitations"]),
 ("3.2","Machine Learning",["Supervised, unsupervised and reinforcement learning","Classification, regression, clustering","Decision trees, random forests, gradient boosting, neural networks","Feature engineering, preprocessing, training, validation, testing"]),
 ("3.3","Model Evaluation",["Accuracy, precision, recall, F1, confusion matrix, ROC-AUC","MAE, MSE; overfitting, underfitting, cross-validation, bias and variance, model drift"]),
 ("3.4","AI Model Deployment",["Model serving; inference APIs; batch and real-time inference","Model monitoring, versioning and retraining; production evaluation"])]),
("4","Generative AI and Large Language Models",[
 ("4.1","Generative AI Fundamentals",["Generative models; foundation models; LLMs; transformers and attention","Tokens, tokenisation, context windows, parameters, temperature","Hallucinations; multimodal AI (text, image, audio, video)"]),
 ("4.2","Major AI Model Providers",["OpenAI API, Anthropic Claude API, Google Gemini API","Open-source models, Hugging Face, Ollama","Model selection, pricing and usage considerations, limitations, multi-model architecture"]),
 ("4.3","Prompt Engineering",["Zero-shot and few-shot prompting","Chain-of-thought concepts and safe reasoning guidance","Role-based prompting; structured and JSON output; prompt templates","System and user instructions; prompt evaluation, optimisation and versioning"]),
 ("4.4","Context Engineering",["Context windows and context management; context retrieval","Memory, conversation history, context compression, relevance","Long-context strategies; context engineering for agents"]),
 ("4.5","Embeddings and Tokenisation",["What embeddings are and how they work; semantic representation","Similarity search; cosine similarity","Token counting, token costs, embedding model selection"]),
 ("4.6","Fine-Tuning Fundamentals",["What fine-tuning is; fine-tuning vs RAG","Supervised fine-tuning; dataset preparation; evaluation; cost and limits"]),
 ("4.7","LLM Evaluation",["Accuracy, relevance, faithfulness, groundedness, hallucination evaluation","Response quality, latency, cost per request","Human vs automated evaluation; LLM-as-a-judge limitations"]),
 ("4.8","AI Application Development with Lovable",["What Lovable is; prompting Lovable; building frontends","Connecting Supabase; database, authentication, API integration","Testing, debugging, GitHub synchronisation, deployment, limitations of AI-generated development"])]),
("5","RAG and Enterprise Knowledge Systems",[
 ("5.1","RAG Fundamentals",["What retrieval-augmented generation is and why it is needed","RAG vs fine-tuning; architecture; retrieval and generation; grounding"]),
 ("5.2","Document Processing",["PDF, Word, Excel and HTML processing; web page extraction","OCR, document parsing, metadata extraction, document classification"]),
 ("5.3","Chunking and Embeddings",["Fixed-size, semantic and overlapping chunking; chunk size optimisation","Embedding generation, metadata filtering, embedding storage"]),
 ("5.4","Vector Databases",["Pinecone, Qdrant, pgvector, Supabase Vector","Vector indexing, semantic search, hybrid search, metadata filtering, ranking"]),
 ("5.5","Advanced RAG",["Hybrid retrieval, query rewriting, reranking, multi-query retrieval","Contextual retrieval, agentic RAG, knowledge graphs, multimodal RAG"]),
 ("5.6","RAG Evaluation",["Retrieval accuracy, context relevance, faithfulness, answer relevance","Recall and precision; retrieval latency; cost optimisation; RAGAS fundamentals; test datasets"])]),
("6","AI Agents and Intelligent Automation",[
 ("6.1","AI Agent Fundamentals",["What an agent is; chatbot vs agent; agent architecture","Reasoning, planning, tools and actions, memory, state","Autonomous vs supervised agents; limitations"]),
 ("6.2","Agent Development Frameworks",["LangChain, LangGraph, CrewAI, LlamaIndex","OpenAI Agents SDK, Google Agent Development Kit","Framework comparison and selection"]),
 ("6.3","Tool Calling",["Function calling; tool schemas; API-based tools","Tool permissions, execution, validation and error handling"]),
 ("6.4","MCP: Model Context Protocol",["MCP architecture; MCP servers and clients","Resources, prompts and tools; authentication and security"]),
 ("6.5","Multi-Agent Systems",["Single vs multi-agent architecture; delegation and communication","Supervisor agents, orchestration, workflow execution, state, failure recovery"]),
 ("6.6","Human-in-the-Loop",["Human approval, escalation, manual review, sensitive action approval","Audit trails, agent permissions, safe execution, production controls"]),
 ("6.7","AI Automation",["n8n, Zapier, Make; webhooks; API integrations","CRM and email automation; WhatsApp Business integrations","Document processing; scheduled workflows; error handling; monitoring; versioning"])]),
("7","Full-Stack Application Development",[
 ("7.1","Frontend Development",["HTML, CSS, JavaScript, TypeScript, React","Components, state management, forms, responsive design, API integration"]),
 ("7.2","Backend Development",["Backend fundamentals; Python application development; FastAPI","Routes, endpoints, request and response handling, middleware, validation","Error handling, background tasks, async programming"]),
 ("7.3","Full-Stack Architecture",["Client-server architecture; REST APIs","Authentication, authorisation, session management, database connectivity","File uploads, third-party integrations, application logging"]),
 ("7.4","SaaS Development",["What SaaS is; multi-tenant architecture","User and organisation management; role-based access control","Subscriptions, payments, usage tracking, API limits, billing","Admin dashboards, customer onboarding, product analytics"]),
 ("7.5","Modular Application Development",["Modular architecture; reusable components; service separation","API and database layers; configuration; environment variables","Scalability and maintainability"])]),
("8","Cloud Computing, DevOps and Production Deployment",[
 ("8.1","Cloud Fundamentals",["What cloud computing is","IaaS, PaaS and SaaS","Public, private and hybrid cloud; regions and availability zones","Compute, storage, networking, databases"]),
 ("8.2","Cloud Platforms",["AWS, Microsoft Azure and Google Cloud Platform foundations","Accounts, IAM, compute, storage, managed databases, AI services","Networking, monitoring, security, cost management, deployment"]),
 ("8.3","Containerisation",["What containers are; virtual machines vs containers","Docker images, containers, Dockerfiles, Docker Compose","Container networking and registries"]),
 ("8.4","Kubernetes",["Clusters, nodes, pods, deployments, services","ConfigMaps, secrets, scaling, monitoring, orchestration"]),
 ("8.5","CI/CD",["Continuous integration, delivery and deployment","GitHub Actions; build, testing and deployment pipelines","Automated testing, rollbacks, release management"]),
 ("8.6","Advanced Cloud Architecture",["Serverless, microservices, event-driven architecture, API gateways, load balancing","Infrastructure as Code: Terraform, Helm; cloud networking; identity and secrets management"]),
 ("8.7","Production AI Deployment",["Model serving; AI inference endpoints; environment management","Monitoring, logging, tracing, latency and cost monitoring","Model versioning, scaling, reliability, disaster recovery"]),
 ("8.8","Cloud Security",["Authentication, authorisation, encryption, network security, data isolation","Secrets management, least privilege, vulnerability management, security monitoring, compliance"])]),
("9","AI Product Management, Business Thinking and Adoption",[
 ("9.1","Business Problem Discovery",["Customer discovery, user research, customer interviews, pain points","Problem statements, Jobs to Be Done, personas, customer journeys, process mapping, root cause analysis"]),
 ("9.2","AI Opportunity Identification",["AI use-case and automation discovery; feasibility; data availability; model suitability","Build vs buy; AI vs traditional software; risk assessment; prioritisation"]),
 ("9.3","Product Management",["Product vision, strategy, roadmap and lifecycle","PRD, BRD, technical specifications, user stories, acceptance criteria","Agile, Scrum, Kanban, backlog management, MVP, prototyping, product discovery"]),
 ("9.4","AI Product Management",["AI product lifecycle and architecture; model selection","AI requirements; prompt and context requirements; model evaluation; AI quality metrics","Human oversight, AI UX, responsible AI, AI product iteration"]),
 ("9.5","Product Adoption",["Onboarding, activation, adoption metrics, retention, engagement, feature adoption","Customer success, feedback loops, product analytics, change management, training, enablement"]),
 ("9.6","Business Impact and ROI",["Business cases; cost-benefit analysis; ROI; TCO","Productivity, process efficiency, cost savings, revenue opportunities, automation payback, KPIs"]),
 ("9.7","Product and Analytics Tools",["Jira, Figma, FigJam, Postman, Power BI, Mixpanel, Google Analytics, Confluence, Miro"])]),
("10","Enterprise Solutions Architecture and System Integration",[
 ("10.1","Enterprise Architecture",["Application, data, integration, infrastructure and AI architecture","Architecture principles, documentation, architecture decision records"]),
 ("10.2","Enterprise Integration",["ERP, CRM, HRMS, payment and document management integration","Legacy systems; REST APIs; webhooks; message queues; event-driven integration","API gateways, middleware, enterprise service buses"]),
 ("10.3","Enterprise AI Architecture",["Centralised and distributed AI platforms; multi-provider LLM architectures","Model abstraction layers; enterprise RAG; agent orchestration","AI gateways, model routing, data access controls, multi-tenant enterprise AI, AI observability"]),
 ("10.4","Security and Governance",["Data privacy, classification, retention; responsible AI; AI governance","Model risk management, explainability, bias, hallucination risk, auditability","Access control, regulatory awareness, enterprise security reviews"]),
 ("10.5","Enterprise Reliability",["Availability, reliability engineering, scalability, fault tolerance, resilience","Disaster recovery, backup, incident management, troubleshooting, root cause analysis","Service-level objectives and agreements"])]),
("11","Customer-Facing Engineering, Consulting and Communication",[
 ("11.1","Customer Discovery",["Client discovery meetings; business and technical requirement gathering","Stakeholder interviews; business process observation; problem validation; technical feasibility"]),
 ("11.2","Stakeholder Management",["Working with CTOs, CIOs, CFOs, CISOs and business teams","Managing expectations, resolving disagreements, communicating technical constraints"]),
 ("11.3","Technical Communication",["Technical presentations, architecture walkthroughs, product demonstrations","Proof-of-concept presentations, technical workshops, code-with sessions","Technical documentation, executive summaries, business impact presentations"]),
 ("11.4","Delivery and Deployment Management",["Project planning, scope management, risk management","Testing, UAT, production readiness, release management, deployment documentation","Knowledge transfer, client training, change management"]),
 ("11.5","Production Support",["Production troubleshooting, incident management, root cause analysis","Monitoring, escalation, bug resolution, performance optimisation","Post-deployment reviews and continuous improvement"])]),
("12","AI Security, Safety, Governance and Responsible AI",[
 ("12.1","AI Security Fundamentals and OWASP Top 10 for LLM Applications",["Prompt injection and indirect prompt injection","Data leakage, insecure output handling, excessive agency, model denial of service","Supply-chain risks, retrieval poisoning, secrets exposure"]),
 ("12.2","Secure Integration",["Secure API integration; identity and access management; role-based permissions","Personally identifiable information; encryption; data minimisation; human approval; AI audit logs"]),
 ("12.3","AI Governance and Responsible AI",["Model governance; AI risk management; responsible AI","Red teaming; security testing; incident response","Threat-modelling exercises and secure AI deployment checklists"])]),
("13","AI Automation Consulting and Agency Development",[
 ("13.1","Agency Fundamentals",["What an AI automation agency is; agency vs consulting vs SaaS","Service business models; niche and target customer selection; value proposition","Service packaging, pricing, client acquisition, sales funnels, proposals, contracts, retainers"]),
 ("13.2","Automation Service Categories",["AI customer support, lead generation, sales and marketing automation","Document processing, reporting, employee assistants, knowledge management","Workflow automation, voice agents, email automation, CRM automation"]),
 ("13.3","Industry Specialisation",["Real estate: lead capture, qualification, recommendations, follow-ups, visit scheduling, CRM, documents, reporting","Education: student support, admissions, course assistants, progress monitoring, fee reminders, counselling","Financial services: document extraction, application processing, validation, support, compliance support, exception detection"]),
 ("13.4","Commercial Delivery",["Discovery, automation audit, workflow mapping, proposal, proof of concept, MVP","Implementation, testing, deployment, training, support, renewal, case studies"]),
 ("13.5","Agency Financial Planning",["Startup and technology costs; software and infrastructure costs","Project pricing, retainers, gross margins, customer acquisition cost, lifetime value, break-even, forecasting","All financial examples labelled as hypothetical, with assumptions shown"])]),
("14","Building a B2B AI SaaS Business",[
 ("14.1","SaaS Fundamentals",["SaaS business models; B2B, vertical and horizontal SaaS","Product-market fit; market and competitor research; segmentation; pricing"]),
 ("14.2","SaaS Product Development",["Discovery, validation, MVP definition, product architecture, UX/UI","Frontend, backend, database, APIs, authentication, multi-tenancy, security, billing, analytics, deployment"]),
 ("14.3","SaaS Business Operations",["Onboarding, customer success, support systems, churn, retention, usage analytics","Subscription management, roadmap, feature prioritisation, product growth"]),
 ("14.4","SaaS Go-to-Market",["Ideal customer profile, positioning, value proposition, landing pages","Content marketing, SEO, email, LinkedIn outreach, partnerships, demos, sales pipeline, feedback"]),
 ("14.5","Scaling",["Product and technical scalability; cloud cost optimisation; support scalability","Team development, international expansion, enterprise sales, channel partnerships"])]),
]
VOLUMES=[("1","Introduction to FDE and Career Foundations"),("2","Programming and Software Engineering"),("3","Data Engineering, SQL and Databases"),("4","AI and Machine Learning"),("5","Generative AI and LLMs"),("6","RAG and Knowledge Systems"),("7","AI Agents and Automation"),("8","Full-Stack Development"),("9","Cloud, DevOps and Deployment"),("10","AI Product Management and Business Thinking"),("11","Enterprise Architecture and Integration"),("12","Security, Governance and Responsible AI"),("13","AI Automation Consulting and Agency Building"),("14","B2B AI SaaS Development"),("15","Four End-to-End Industry Projects"),("16","Career Preparation and Interview Handbook"),("17","Tools, Glossary and Learning Resources")]
EXTRA_PDFS=["Master curriculum","Master learning roadmap","Practical project workbook","Coding exercise workbook","Interview preparation","Agency launch playbook","SaaS startup playbook","Technical glossary","Master tool comparison"]
PROJECTS=[("Project 1","AI customer support agent","Knowledge retrieval, CRM context, escalation to humans, interaction records, support analytics"),
("Project 2","Real estate AI automation platform","Website lead capture, qualification, property recommendations, follow-ups, visit scheduling, CRM updates, sales reports, agent dashboard"),
("Project 3","AI educational assistant","Student Q&A from course material, concept explanations, progress tracking, personalised recommendations, teacher dashboards, learning analytics"),
("Project 4","Financial documentation automation","Document extraction, missing-information checks, inconsistency flags, rule validation, review summaries, human review routing, audit records. Consequential decisions always need authorised human review.")]
TOOLS=[("Programming","Python, JavaScript, TypeScript"),("AI models","OpenAI, Claude, Gemini"),("AI coding","VS Code, Cursor, GitHub Copilot, Claude Code"),("Application builders","Lovable"),("AI frameworks","LangChain, LangGraph, CrewAI, LlamaIndex"),("AI agent platforms","OpenAI Agents SDK, Google ADK"),("Databases","PostgreSQL, Supabase, MySQL, MongoDB"),("Vector databases","Pinecone, Qdrant, pgvector"),("APIs","Postman, FastAPI"),("Version control","Git, GitHub"),("Cloud","AWS, Azure, GCP"),("Deployment","Docker, Kubernetes"),("Infrastructure","Terraform, Helm"),("CI/CD","GitHub Actions"),("Automation","n8n, Zapier, Make"),("Product management","Jira, Confluence"),("Design","Figma, FigJam, Miro"),("Analytics","SQL, Power BI, Mixpanel"),("Monitoring","OpenTelemetry and cloud monitoring tools")]
STAGES=[("Stage 1","Programming foundations","Computer and software basics, Python, SQL, Git, APIs, JavaScript basics, terminal, debugging","Understand programming; build simple applications"),
("Stage 2","Applied AI","OpenAI, Claude and Gemini APIs, prompt and context engineering, embeddings, tokenisation, basic RAG","Build practical LLM-powered applications"),
("Stage 3","Agent development","LangChain, LangGraph, CrewAI, tool calling, MCP, agent memory, multi-agent workflows, human-in-the-loop","Build tool-using agents and automated workflows"),
("Stage 4","Application development","FastAPI, React, frontend and backend, database integration, authentication, authorisation, SaaS fundamentals","Build complete AI-powered applications"),
("Stage 5","Production deployment","Cloud (AWS, Azure, GCP), Docker, Kubernetes, CI/CD, monitoring, security, AI evaluation, production troubleshooting","Deploy secure, scalable applications"),
("Stage 6","Enterprise projects","Real estate, education and financial services solutions, built and deployed","Demonstrate end-to-end project ownership"),
("Stage 7","Professional and entrepreneurial readiness","FDE interviews, architecture presentations, customer discovery, client demos, agency packaging, SaaS MVP, sales","Prepare for employment and independent business")]
JOBS=[("OpenAI","Forward Deployed Engineer","https://openai.com/careers/search/"),("OpenAI","Forward Deployed Engineering roles (search)","https://openai.com/careers/search/?q=forward"),("Palantir","Forward Deployed AI Engineer","https://jobs.lever.co/palantir/ff1029bd-bb6d-4d78-a03e-5f9744d0b798"),("Accenture India","Forward Deployed Engineer","https://www.accenture.com/in-en/careers/jobdetails?id=R00344052_en"),("Accenture India","Forward Deployed AI Engineer","https://www.accenture.com/in-en/careers/jobdetails?id=ATCI-5613009-S2028500_en")]
OFFICIAL=[("OpenAI API docs","https://platform.openai.com/docs"),("Anthropic Claude docs","https://docs.claude.com/"),("Google AI for Developers","https://ai.google.dev/"),("Python docs","https://docs.python.org/3/"),("PostgreSQL docs","https://www.postgresql.org/docs/"),("Supabase docs","https://supabase.com/docs"),("Pinecone docs","https://docs.pinecone.io/"),("Qdrant docs","https://qdrant.tech/documentation/"),("LangChain Python docs","https://python.langchain.com/docs/"),("LangGraph docs","https://langchain-ai.github.io/langgraph/"),("CrewAI docs","https://docs.crewai.com/"),("Model Context Protocol","https://modelcontextprotocol.io/"),("OWASP Top 10 for LLM Applications","https://genai.owasp.org/llm-top-10/"),("AWS documentation","https://docs.aws.amazon.com/"),("Microsoft Azure documentation","https://learn.microsoft.com/azure/"),("Google Cloud documentation","https://cloud.google.com/docs"),("Docker docs","https://docs.docker.com/"),("Kubernetes docs","https://kubernetes.io/docs/"),("Terraform docs","https://developer.hashicorp.com/terraform/docs"),("GitHub docs","https://docs.github.com/"),("n8n docs","https://docs.n8n.io/"),("Lovable docs","https://docs.lovable.dev/"),("FastAPI docs","https://fastapi.tiangolo.com/"),("React docs","https://react.dev/")]
ADDITIONS=["Module 0 (new): learning setup, accounts, safe use of AI tools, and what not to paste into AI tools","Data privacy and consent basics for non-coders building with customer data","Evaluating agents: test sets, tool-call tracing and regression checks before release","AI cost control: token budgets, caching and model routing decisions with worked numbers","Portfolio and public demo: GitHub README standards, live demo hosting, case-study writing","Customer communication kit: discovery questions, status updates and handover checklists","Agency legal and contract basics (general information only; not legal advice)"]
def sec_html():
    out=[]
    for num,title,subs in MODULES:
        body="".join(f'<details class="sub"><summary><b>{E(sn)}</b> {E(st)}</summary><ul>'+"".join(f"<li>{E(t)}</li>" for t in topics)+"</ul></details>" for sn,st,topics in subs)
        out.append(f'<details class="mod" open><summary><span class="mn">Module {num}</span> {E(title)} <span class="cnt">{len(subs)} sections</span></summary>{body}</details>')
    return "".join(out)
def build():
    vol="".join(f'<li><span class="vn">Volume {n}</span> {E(t)}</li>' for n,t in VOLUMES)
    extra="".join(f"<li>{E(x)}</li>" for x in EXTRA_PDFS)
    proj="".join(f'<div class="card"><div class="k">{E(a)}</div><h3>{E(b)}</h3><p>{E(c)}</p><p class="s">Beginner, intermediate and advanced versions are included.</p></div>' for a,b,c in PROJECTS)
    stages="".join(f'<div class="card"><div class="k">{E(a)}</div><h3>{E(b)}</h3><p><b>Topics:</b> {E(c)}</p><p><b>Outcome:</b> {E(d)}</p></div>' for a,b,c,d in STAGES)
    tools="".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a,b in TOOLS)
    jobs="".join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td><a href="{u}" target="_blank" rel="noopener">{E(u)}</a></td><td>Not checked live from this environment; confirm the role is open</td></tr>' for a,b,u in JOBS)
    off="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(n)}</a> <span class="s">(official starting page; not checked live from this environment)</span></li>' for n,u in OFFICIAL)
    add="".join(f"<li>{E(x)}</li>" for x in ADDITIONS)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="claude:viewport-fit-sides" content="cover"><title>FDE Master Curriculum · SkillNavora</title><style>
:root{{--bg:#f5f3ff;--fg:#1d1b2e;--muted:#5b5876;--card:#fff;--line:#e3dff5;--accent:#6a3fd1;--accent2:#0b7a75;--accent-fg:#fff}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#15131f;--fg:#f0eefe;--muted:#b8b3d9;--card:#201d31;--line:#3a3556;--accent:#b9a2ff;--accent2:#38d9a9;--accent-fg:#1a1030;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#15131f;--fg:#f0eefe;--muted:#b8b3d9;--card:#201d31;--line:#3a3556;--accent:#b9a2ff;--accent2:#38d9a9;--accent-fg:#1a1030;color-scheme:dark}}
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 40px}}
.hero{{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px))) 18px;padding:28px 18px 24px;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}}
.hero small{{font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:11px;opacity:.9}}
.hero h1{{font:800 26px/1.2 "Space Grotesk",system-ui,sans-serif;margin:6px 0 8px;text-wrap:balance}}
.hero p{{margin:0;max-width:62ch;opacity:.95}}
main{{max-width:960px;margin:0 auto;display:grid;gap:16px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;min-width:0}}
h2{{font:700 19px/1.3 "Space Grotesk",system-ui,sans-serif;margin:0 0 10px}}
h3{{font:700 16px/1.3 "Space Grotesk",system-ui,sans-serif;margin:4px 0 6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:12px}}
.card{{border:2px solid var(--line);border-radius:14px;padding:12px;background:var(--bg);min-width:0;overflow-wrap:anywhere}}
.k{{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--accent);font-weight:700}}
.s{{color:var(--muted);font-size:13px}}
details.mod{{border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin-bottom:10px;background:var(--bg)}}
details.mod>summary{{font:700 15.5px "Space Grotesk",system-ui,sans-serif;cursor:pointer;overflow-wrap:anywhere}}
.mn{{display:inline-block;background:var(--accent);color:var(--accent-fg);border-radius:99px;padding:2px 10px;font-size:12px;margin-right:6px}}
.cnt{{color:var(--muted);font-size:12.5px;font-weight:600;margin-left:6px}}
details.sub{{margin:8px 0 0 6px;border-left:3px solid var(--accent2);padding:4px 0 4px 12px}}
details.sub>summary{{cursor:pointer;overflow-wrap:anywhere}}
details.sub ul{{margin:6px 0 4px 18px;padding:0}}
ol,ul{{padding-left:20px}}
table{{width:100%;border-collapse:collapse;font-size:14px;display:block;overflow-x:auto}}
th,td{{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}
th{{background:var(--bg)}}
a{{color:var(--accent);overflow-wrap:anywhere}}
.vn{{font-weight:700;color:var(--accent2);margin-right:4px}}
.pill{{display:inline-block;border:2px solid var(--line);border-radius:99px;padding:5px 12px;margin:4px 6px 4px 0;font-weight:600;font-size:13px}}
@media (prefers-reduced-motion: reduce){{*{{transition:none!important}}}}
</style></head><body>
<header class="hero"><small>SkillNavora · Forward Deployed Engineering</small><h1>The Complete AI Forward Deployed Engineer, Enterprise AI Architect and AI Automation Business Handbook</h1><p>From Non-Coder to Enterprise AI Builder: Learn, Build, Deploy, Get Hired and Launch Your AI Business.</p></header>
<main>
<section><h2>Who this programme is for</h2><p>Absolute beginners, non-coders, working professionals, fresh graduates, software developers, business analysts, product managers, consultants and entrepreneurs. It starts from zero and ends at professional, production-ready practice.</p>
<div class="grid">
<div class="card"><div class="k">Track A</div><h3>AI Forward Deployed Engineer</h3><p>Customer problems to production: Python apps, LLM integrations, RAG, agents, APIs, cloud deployment, debugging and monitoring.</p></div>
<div class="card"><div class="k">Track B</div><h3>AI Solutions Architect</h3><p>Enterprise architecture, multi-provider AI design, integration layers, security, governance, cost estimates and architecture documents.</p></div>
<div class="card"><div class="k">Track C</div><h3>AI Product Manager</h3><p>Opportunity discovery, feasibility, roadmaps, PRDs, MVPs, AI metrics, launches, adoption and ROI.</p></div>
<div class="card"><div class="k">Track D</div><h3>AI Automation Consultant</h3><p>Process audits, no-code and AI workflows, CRM and ERP integration, support and document automation, selling and supporting solutions.</p></div>
</div></section>
<section><h2>What the FDE role is</h2><p>A Forward Deployed Engineer works where software engineering, AI engineering, solutions architecture, product consulting and business process change meet. They work with the customer, build the solution, deploy it to production, and own the outcome.</p>
<div style="overflow-x:auto"><table><tr><th>Dimension</th><th>Product Manager</th><th>AI Engineer</th><th>Forward Deployed Engineer</th></tr>
<tr><td>Understanding business problems</td><td>High</td><td>Medium</td><td>High</td></tr>
<tr><td>Product strategy</td><td>High</td><td>Medium</td><td>Medium–High</td></tr>
<tr><td>Coding</td><td>Usually limited</td><td>High</td><td>High</td></tr>
<tr><td>AI development</td><td>Conceptual / technical</td><td>High</td><td>High</td></tr>
<tr><td>Customer interaction</td><td>High</td><td>Variable</td><td>Very high</td></tr>
<tr><td>Deployment</td><td>Coordinates</td><td>Builds and deploys</td><td>Owns customer deployment</td></tr>
<tr><td>Business outcomes</td><td>Product outcomes</td><td>Technical outcomes</td><td>Deployment and business outcomes</td></tr>
<tr><td>Architecture</td><td>Product level</td><td>Technical</td><td>Enterprise and application</td></tr>
<tr><td>Integration</td><td>Coordinates</td><td>Implements</td><td>Designs and implements</td></tr>
<tr><td>Troubleshooting</td><td>Product issues</td><td>Technical issues</td><td>Customer and production issues</td></tr></table></div></section>
<section><h2>Learning roadmap: seven stages</h2><div class="grid">{stages}</div></section>
<section><h2>Complete curriculum: 14 modules, every topic</h2><p class="s">Each topic is taught with: a simple definition, why it matters, how it works, a real-world example, business use, tools, a step-by-step tutorial, a hands-on exercise, common mistakes, interview questions, a knowledge check, a mini-project and further resources. Expand a module to see its sections.</p>{sec_html()}</section>
<section><h2>Volume plan (17 PDF volumes)</h2><ol style="list-style:none;padding:0">{vol}</ol>
<h3>Additional PDFs</h3><ul>{extra}</ul></section>
<section><h2>Four end-to-end industry projects</h2><div class="grid">{proj}</div></section>
<section><h2>Final capstone</h2><p>Choose a business problem and complete: customer discovery, problem definition, business and product requirements, technical specifications, architecture, database design, APIs, model selection, RAG, agents, frontend, backend, enterprise integration, authentication and authorisation, security, testing, evaluation, cloud deployment, monitoring, documentation, a client presentation, an ROI framework and a final demonstration.</p></section>
<section><h2>Tool directory</h2><div style="overflow-x:auto"><table><tr><th>Category</th><th>Tools</th></tr>{tools}</table></div><p class="s">Tools that serve similar purposes are compared, and learners do not need to use all of them. Three stacks are given: beginner, intermediate and advanced.</p></section>
<section><h2>Career preparation: job links</h2><p>Analyse current job descriptions for skills, programming, AI, cloud, architecture, integration, deployment, communication, experience and education requirements, then compare them with the curriculum. Compensation depends on skill depth, experience, location, employer and demonstrated production capability. No salary or placement is promised.</p>
<div style="overflow-x:auto"><table><tr><th>Organisation</th><th>Role</th><th>Link</th><th>Status</th></tr>{jobs}</table></div>
<p>Interview preparation will cover: resume templates for FDE, AI Engineer, AI Solutions Architect, AI Product Manager and AI Automation Consultant; LinkedIn positioning; technical portfolio and GitHub requirements; system design, Python, SQL, RAG and LLM, agent, cloud and DevOps questions; customer-facing scenarios; and STAR answer frameworks.</p></section>
<section><h2>Business path</h2><p>The same skills support two paths: employment (FDE, AI Engineer, Solutions Architect, Product Manager or Solutions Consultant) and entrepreneurship (an AI automation agency, then a B2B AI SaaS). The business roadmap covers market research, industry selection, competitor analysis, customer interviews, problem validation, service selection, prototypes, pricing and proposals, client acquisition, implementation, retainers, SaaS opportunity identification, MVP development, product-market fit and scaling. Examples are given for India and international markets.</p></section>
<section><h2>Official learning resources</h2><p class="s">These are official starting pages. They could not be opened from the environment where this curriculum was drafted, so please confirm each link before relying on it.</p><ul>{off}</ul></section>
<section><h2>Suggested additions (for your approval)</h2><p>These are not in the original prompt. They are proposed to make the programme complete.</p><ul>{add}</ul></section>
<section><h2>Next step</h2><p>Approve this curriculum, or tell me what to change. After approval, Volume 1 is written first, and each later volume is checked against this table of contents before it is produced.</p></section>
</main></body></html>'''
open("fde_curriculum.html","w",encoding="utf-8").write(build()); print("ok", len(build()))
