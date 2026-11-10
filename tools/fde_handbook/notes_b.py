
NOTES_B = {
"6.1": [
 "An AI agent uses a model to decide its own next steps toward a goal, calling tools and reacting to results. A chatbot replies to messages; an agent takes actions (search, update a CRM, send an email). Agent architecture = model + instructions + tools + memory/state + a control loop + guardrails.",
 "Reasoning interprets the goal and the current situation. Planning breaks the goal into steps. Tools and actions change or read the outside world. Memory keeps short-term state (this task) and long-term facts (user preferences). State is the structured record of progress that the loop updates each step.",
 "Autonomous agents act without approval inside set limits; supervised agents pause for human approval at key points. Limitations: they can loop, misuse tools, follow injected instructions, run up costs or compound small errors, so production agents need step limits, budgets, logging and approvals.",
],
"6.2": [
 "LangChain: components for models, prompts, tools, retrievers and agents, with many integrations. LangGraph: builds agents and workflows as graphs of nodes and edges with explicit state, checkpoints and human-in-the-loop pauses. CrewAI: defines agents with roles, goals and tasks that collaborate as a crew. LlamaIndex: data framework for ingestion, indexing and RAG, plus agents.",
 "OpenAI Agents SDK: lightweight Python/TypeScript library for agents, tools, hand-offs between agents, guardrails and tracing on OpenAI models. Google Agent Development Kit (ADK): framework for building, evaluating and deploying agents, integrated with Gemini and Vertex AI. Claude Agent SDK provides the agent loop used by Claude Code.",
 "Compare frameworks on control (can you see and change every step?), state and persistence, tracing, provider support, community and maturity. Pick plain code for simple flows, LangGraph for complex stateful flows, CrewAI for quick role-based prototypes, LlamaIndex for data-heavy RAG.",
],
"6.3": [
 "Function calling: you describe functions to the model; it returns the function name and JSON arguments instead of text when a function is needed. Tool schemas use JSON Schema (name, description, parameters with types and required fields). API-based tools wrap external APIs (weather, CRM, payments) as callable functions.",
 "Tool permissions: decide which tools each agent may use and whether they read or write. Execution happens in your code, never inside the model. Validate arguments (types, ranges, allowed values) before execution. Error handling returns clear messages so the model can correct itself, with a maximum number of retries.",
],
"6.4": [
 "MCP (Model Context Protocol) standardises how AI applications connect to tools and data. An MCP host (Claude Desktop, Claude Code, an IDE) runs MCP clients; each client connects to one MCP server; the server exposes capabilities over JSON-RPC 2.0, via STDIO (local) or Streamable HTTP (remote).",
 "Servers expose three primitives: resources (readable data such as files or records), prompts (reusable templates) and tools (actions the model can call). Remote servers use OAuth-based authorisation; apply least privilege, validate inputs, ask for user consent on sensitive tools, and only install servers you trust.",
],
"6.5": [
 "Single-agent: one model with several tools; simpler and easier to debug. Multi-agent: several specialised agents (researcher, writer, reviewer). Delegation passes a sub-task to another agent; communication happens through messages or shared state.",
 "A supervisor (orchestrator) agent plans and routes work to worker agents and combines results. Orchestration defines the order and conditions. Workflow execution may run steps in parallel. State management keeps one shared record of progress. Failure recovery retries a step, switches to a fallback or escalates to a human.",
],
"6.6": [
 "Human approval: the agent pauses before an action until a person approves. Escalation: hand the case to a human when confidence is low or rules require it. Manual review: a person checks a sample or all outputs. Sensitive action approval applies to payments, deletions, external emails and legal or medical content.",
 "Audit trails log who did what, when and why (prompts, tool calls, approvals). Agent permissions limit tools and data per agent. Safe execution uses sandboxes, dry-run modes and spending limits. Production controls include kill switches, rate limits, monitoring and alerting.",
],
"6.7": [
 "n8n: open-source, self-hostable workflow automation with code nodes and AI agent nodes. Zapier: easiest no-code automation with thousands of app connectors. Make: visual scenarios with powerful data mapping. Webhooks start workflows from external events. API integrations connect any service that has an API.",
 "CRM automation: create and update leads, deals and tasks (HubSpot, Salesforce, Zoho). Email automation: send, classify and reply to emails. WhatsApp Business integrations: use the official WhatsApp Business Platform (Cloud API) through Meta or a provider to send templates and reply to customers within policy rules.",
 "Document processing workflows extract data from uploads. Scheduled workflows run on a timer (daily reports). Error handling uses error branches, retries and alerts. Monitoring tracks failed runs. Versioning keeps workflow exports in Git so changes can be reviewed and rolled back.",
],
"7.1": [
 "HTML defines structure (headings, forms, buttons). CSS defines layout and style (flexbox, grid, colours). JavaScript/TypeScript adds behaviour. React builds the UI from components: functions that take props and return markup (JSX).",
 "State (useState) holds data that changes; when state changes React re-renders. State management for larger apps uses context, Zustand or Redux. Forms collect and validate input. Responsive design adapts layout to screen size with CSS media queries or Tailwind. API integration calls the backend with fetch, showing loading, success and error states.",
],
"7.2": [
 "The backend receives requests, applies business logic, talks to databases and services, and returns responses. Python is a strong backend choice for AI because of its libraries. FastAPI is a modern Python framework: fast, typed, async, with automatic interactive docs at /docs.",
 "A route (endpoint) is a URL + method handled by a function (@app.get('/leads/{id}')). Request handling reads path, query and body parameters; response handling returns JSON and status codes. Middleware runs on every request (CORS, logging, auth). Validation uses Pydantic models that reject bad input with clear 422 errors.",
 "Error handling raises HTTPException(status_code=404, detail='Lead not found') and logs unexpected errors. Background tasks run work after responding (sending an email). Async programming (async def, await) lets one server handle many requests while waiting for databases or AI APIs.",
],
"7.3": [
 "Client-server architecture: the client (browser, mobile app) sends requests; the server processes them and responds. REST APIs define the contract between them with resources, methods and status codes.",
 "Authentication answers 'who are you?' (passwords, magic links, Google login, tokens). Authorisation answers 'what may you do?' (roles, permissions, row-level security). Session management keeps users logged in with secure cookies or short-lived tokens (JWT) plus refresh tokens. Database connectivity uses connection pools and an ORM (SQLAlchemy) or a query builder.",
 "File uploads: check type and size, store in object storage (S3, Supabase Storage), save only the reference in the database. Third-party integrations: payments, email, CRM, AI APIs, each wrapped in a small service module. Application logging: structured logs (JSON) with request IDs, without passwords or personal data.",
],
"7.4": [
 "SaaS (software as a service) is software delivered over the internet on a subscription. Multi-tenant architecture serves many customers (tenants) from one deployment, keeping each tenant's data isolated, usually with a tenant_id column and row-level security, or a separate schema or database per tenant.",
 "User management: sign-up, invite, profile, password reset. Organisation management: workspaces with members. Role-based access control (RBAC): roles such as owner, admin, member, viewer map to permissions checked on every request.",
 "Subscriptions and payments use a provider such as Stripe or Razorpay: plans, checkout, invoices and webhooks that update the account's plan. Usage tracking counts metered units (AI calls, documents). API limits enforce plan quotas. Billing combines subscription fees and usage.",
 "Admin dashboards let your team manage accounts, plans and support. Customer onboarding guides new users to first value (checklists, sample data). Product analytics track sign-ups, activation, feature usage and retention.",
],
"7.5": [
 "Modular architecture splits the app into modules with clear responsibilities (auth, billing, documents, AI). Reusable components (UI and backend functions) are written once and used in many places. Service separation keeps different concerns in different modules or services.",
 "The API layer handles HTTP; the service layer holds business logic; the database layer handles queries. Configuration (URLs, limits, feature flags) lives in config files or environment variables. Environment variables hold settings and secrets that differ between development and production; never commit them to Git (.env in .gitignore).",
 "Scalability: the app handles more users by adding instances (stateless servers), caching and queues. Maintainability: clean modules, tests and documentation let new developers change code safely.",
],
"8.1": [
 "Cloud computing delivers computing resources on demand over the internet with pay-as-you-go pricing, instead of owning hardware. Benefits: speed, elasticity, global reach and managed services. Trade-offs: cost control, vendor lock-in and shared responsibility for security.",
 "IaaS: you rent virtual machines, storage and networks (EC2, Azure VMs, Compute Engine). PaaS: you deploy code and the platform runs it (App Service, Cloud Run, Elastic Beanstalk). SaaS: complete applications you use (Gmail, Salesforce).",
 "Public cloud: shared provider infrastructure. Private cloud: dedicated to one organisation. Hybrid cloud: on-premises plus public cloud. Regions are geographic areas (Mumbai, Frankfurt); availability zones are isolated data centres within a region for resilience; choose regions for latency and data residency rules.",
 "Compute runs code (VMs, containers, serverless). Storage keeps files (object storage such as S3), disks (block) and shared folders (file). Networking connects resources (virtual networks, subnets, load balancers, DNS). Databases are offered as managed services so the provider handles backups and patching.",
],
"8.2": [
 "AWS: the largest catalogue of services, widely used by startups and enterprises. Microsoft Azure: strong with enterprises using Microsoft 365, Active Directory and Azure OpenAI. Google Cloud Platform: strong in data, analytics, Kubernetes (GKE) and Vertex AI with Gemini.",
 "Account setup: enable MFA on the root account, create admin users, set budget alerts. IAM: users, groups, roles and policies grant least-privilege permissions. Compute: EC2/VMs/Compute Engine, serverless (Lambda, Azure Functions, Cloud Functions), containers (ECS/EKS, AKS, GKE, Cloud Run). Storage: S3, Blob Storage, Cloud Storage. Managed databases: RDS, Azure Database for PostgreSQL, Cloud SQL. AI services: Bedrock, Azure OpenAI/AI Foundry, Vertex AI.",
 "Networking: VPC/VNet, subnets, security groups, private endpoints. Monitoring: CloudWatch, Azure Monitor, Cloud Monitoring. Security: KMS, secrets managers, security centres. Cost management: budgets, cost explorer, tagging, right-sizing and shutting down idle resources. Deployment: console for learning, Infrastructure as Code and CI/CD for real work.",
],
"8.3": [
 "A container is a lightweight, isolated package of an app and its dependencies that runs consistently anywhere. It solves 'it works on my machine'.",
 "A virtual machine virtualises hardware and runs a full guest operating system (heavy, minutes to boot). Containers share the host OS kernel and isolate processes (light, seconds to start). Docker images are read-only templates built in layers from a Dockerfile (FROM, WORKDIR, COPY, RUN, EXPOSE, CMD); containers are running instances of images.",
 "Docker Compose defines multi-container apps in docker-compose.yml (services, ports, volumes, environment) and starts them with docker compose up. Container networking lets services reach each other by name (api can call db:5432). Registries (Docker Hub, Amazon ECR, Azure Container Registry, Google Artifact Registry) store and version images with tags.",
],
"8.4": [
 "Kubernetes (K8s) orchestrates containers across machines. A cluster has a control plane (API server, scheduler, controllers, etcd) and worker nodes. Pods are the smallest unit (one or more containers sharing network and storage). Deployments declare the desired number of Pod replicas and roll out updates. Services give Pods a stable network name and load-balance between them.",
 "ConfigMaps hold non-secret configuration; Secrets hold sensitive values (base64-encoded, so also encrypt at rest and restrict access). Scaling: manually (kubectl scale) or automatically with the Horizontal Pod Autoscaler. Monitoring: metrics-server, Prometheus, Grafana and logs. Orchestration means Kubernetes keeps reality matching your declared YAML: restarting failed Pods and rescheduling them on healthy nodes.",
],
"8.5": [
 "Continuous integration: every push is built and tested automatically, catching problems early. Continuous delivery: every passing build is ready to deploy with one approval. Continuous deployment: every passing build goes to production automatically.",
 "GitHub Actions runs workflows defined in .github/workflows/*.yml: triggers (on: push, pull_request), jobs, runners (ubuntu-latest), steps (uses: actions/checkout, run: pytest). Build pipelines compile and package; testing pipelines run unit, integration and evaluation tests; deployment pipelines push images and update the environment, using stored secrets.",
 "Automated testing gates the pipeline: no deploy if tests fail. Rollbacks restore the previous version quickly (redeploy the previous image tag or use Kubernetes rollout undo). Release management uses version tags, release notes, staged rollouts (staging → production) and feature flags.",
],
"8.6": [
 "Serverless: functions run on events and scale to zero (Lambda, Cloud Functions). Microservices: small independently deployable services owning their data. Event-driven architecture: services publish and subscribe to events through queues or streams (SQS, Pub/Sub, Kafka). API gateways: one front door with auth, rate limits and routing. Load balancing: spreads traffic across healthy instances.",
 "Infrastructure as Code: Terraform describes cloud resources in HCL; the workflow is write → terraform plan (preview) → terraform apply; state tracks what exists. Helm packages Kubernetes YAML into charts with values per environment. Cloud networking: VPCs, private subnets, NAT, peering, private endpoints. Identity management: SSO, IAM roles, workload identity. Secrets management: Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager.",
],
"8.7": [
 "Model serving for AI apps: either call a hosted API or host models yourself (vLLM, TGI, SageMaker, Vertex endpoints). AI inference endpoints need timeouts, retries and fallbacks. Environment management keeps dev, staging and production separate, each with its own keys, models and data.",
 "Monitoring: request rates, errors, latency (p50/p95), token usage. Logging: prompts, outputs, tool calls and versions, with personal data masked. Tracing: follow one request through every step (OpenTelemetry, LangSmith, Langfuse). Latency monitoring finds slow steps; cost monitoring tracks spend per feature, customer and model.",
 "Model versioning pins exact model versions and records prompt versions. Scaling: autoscale app servers, use queues for heavy jobs, cache repeated answers, and respect provider rate limits. Reliability: fallback models, graceful degradation and health checks. Disaster recovery: backups, multi-zone deployment, a tested restore runbook and stated recovery time.",
],
"8.8": [
 "Authentication verifies identity (SSO, MFA). Authorisation grants permissions (RBAC, IAM policies). Encryption protects data in transit (TLS/HTTPS) and at rest (KMS-managed keys). Network security uses private networks, firewalls/security groups and WAFs. Data isolation keeps tenants and environments separate.",
 "Secrets management stores keys in a vault and rotates them. Least privilege gives each identity only what it needs. Vulnerability management scans code, dependencies and images (Dependabot, Trivy) and patches promptly. Security monitoring collects audit logs and alerts on unusual activity. Compliance maps controls to standards such as ISO 27001, SOC 2, GDPR and India's DPDP Act.",
],
"9.1": [
 "Customer discovery learns about the customer's world before proposing a solution. User research uses interviews, observation and data. Customer interviews ask about real past experiences ('tell me about the last time…'). Pain points are the frictions, delays, costs and risks users experience.",
 "A problem statement says who has the problem, what it is, its impact and how it is measured. Jobs to Be Done frames what the user is trying to accomplish. Personas summarise user types. Customer journeys map each stage of their experience. Process mapping documents current steps (as-is) and proposed steps (to-be). Root cause analysis (5 Whys, fishbone) finds why the problem happens.",
],
"9.2": [
 "AI use-case discovery lists tasks that involve reading, writing, classifying, extracting, summarising, answering or deciding at volume. Automation discovery finds repetitive rule-based steps. Feasibility checks technical possibility; data availability checks the data exists and can be accessed legally; model suitability checks a model can do the task to the needed accuracy.",
 "Build vs buy: buy an existing tool when it fits; build when the workflow, data or integration is unique or core. AI vs traditional software: use plain rules when they are reliable and explainable; use AI for language and judgement. Risk assessment covers wrong outputs, privacy, bias and regulation. Prioritisation ranks by value, effort and risk (RICE or impact/effort matrix).",
],
"9.3": [
 "Product vision: the long-term change the product makes. Strategy: where and how it will win. Roadmap: the planned sequence of outcomes and features. Product lifecycle: introduction, growth, maturity, decline.",
 "PRD (product requirements document): problem, users, goals, requirements, metrics, scope. BRD (business requirements document): business need, objectives, stakeholders, benefits. Technical specification: how engineers will build it. User stories ('As a…, I want…, so that…') with acceptance criteria (Given/When/Then).",
 "Agile, Scrum and Kanban organise delivery. Backlog management keeps a prioritised, refined list of work. MVP (minimum viable product) tests the core value with the least effort. Prototyping uses clickable designs or quick builds. Product discovery validates value, usability, feasibility and viability before full build.",
],
"9.4": [
 "The AI product lifecycle adds data collection, model selection, evaluation and monitoring to the normal lifecycle. AI product architecture shows the model, prompts, retrieval, tools, guardrails and feedback loop. Model selection balances quality, cost, latency and data rules.",
 "AI requirements specify quality targets, allowed error rates, latency and cost budgets. Prompt and context requirements specify instructions, knowledge sources and tone. Model evaluation uses a test set and rubric. AI quality metrics include accuracy, groundedness, task success and user acceptance rate.",
 "Human oversight defines when people review or approve. AI UX shows sources, confidence and editability, and sets expectations about errors. Responsible AI covers fairness, transparency, privacy and safety. AI product iteration improves prompts, data and models using evaluation results and user feedback.",
],
"9.5": [
 "Onboarding guides users to their first success. Activation is the moment users first get value. Adoption metrics: active users, feature usage, frequency. Retention: users still active after 30/90 days. Engagement: depth of use. Feature adoption: share of users using a specific feature.",
 "Customer success teams help accounts achieve outcomes. Feedback loops capture ratings, comments and corrections. Product analytics measure behaviour. Change management helps people accept new ways of working. Training and enablement give users and champions the skills and materials they need.",
],
"9.6": [
 "A business case justifies an investment with benefits, costs, risks and alternatives. Cost-benefit analysis compares them in money. ROI = (benefit − cost) ÷ cost. TCO (total cost of ownership) includes build, licences, model usage, cloud, support, training and maintenance over several years.",
 "Productivity improvement: more output per person-hour. Process efficiency: shorter cycle time and fewer errors. Cost savings: lower spending. Revenue opportunities: more conversions or new offerings. Automation payback period: months until savings repay the investment. KPIs measure progress (response time, accuracy, cost per case). Label estimates as estimates and state assumptions.",
],
"9.7": [
 "Jira: issue and sprint tracking. Figma: interface design and prototypes. FigJam: collaborative whiteboard for workshops and flows. Postman: API testing. Power BI: dashboards and business reports. Mixpanel: product event analytics and funnels. Google Analytics: website traffic and conversions. Confluence: team documentation. Miro: visual collaboration boards for mapping and planning.",
],
"10.1": [
 "Application architecture: the systems and how they interact. Data architecture: where data lives, its models and flows. Integration architecture: how systems connect (APIs, events, files). Infrastructure architecture: compute, network and storage. AI architecture: models, gateways, retrieval, agents, evaluation and governance.",
 "Architecture principles are agreed rules that guide decisions (security by design, API-first, reuse before build). Architecture documentation includes context, container and component diagrams (the C4 model), data flows and non-functional requirements. Architecture decision records (ADRs) capture each significant decision with context, options, choice and consequences.",
],
"10.2": [
 "ERP (SAP, Oracle, Dynamics) runs finance, supply chain and operations. CRM (Salesforce, HubSpot, Zoho) manages customers and sales. HRMS (Workday, SAP SuccessFactors) manages employees. Payment systems (Stripe, Razorpay) process payments. Document management systems (SharePoint, Google Drive) store files. Each has APIs, permissions and data rules.",
 "Legacy systems are old but critical, often with limited APIs: integrate through database views, file exports, SOAP services or RPA. REST APIs suit request-response. Webhooks push events in real time. Message queues (RabbitMQ, SQS, Kafka) decouple systems and absorb load. Event-driven integration reacts to business events (order placed, invoice received).",
 "API gateways secure and route API traffic. Middleware transforms and routes messages between systems (MuleSoft, Boomi, Azure Logic Apps). An enterprise service bus (ESB) is a central integration backbone in older architectures; modern designs prefer lighter API and event-based integration.",
],
"10.3": [
 "A centralised AI platform gives all teams one governed set of models and tools; distributed means each team runs its own. Multi-provider LLM architectures use several providers for quality, cost and resilience. A model abstraction layer gives one internal interface so applications are not tied to one provider.",
 "Enterprise RAG adds permissions, freshness, citations and scale to RAG. Agent orchestration coordinates agents, tools, approvals and state across business processes. AI gateways (LiteLLM, cloud API management, Kong) centralise keys, routing, rate limits, logging and cost control. Model routing sends each request to the right model by task, cost or availability.",
 "Data access controls ensure the AI only uses data the requesting user may see. Multi-tenant enterprise AI separates business units or customers. AI observability tracks quality, latency, cost, usage, errors and safety events across all AI applications.",
],
"10.4": [
 "Data privacy protects personal data according to law (GDPR, India's DPDP Act). Data classification labels sensitivity. Data retention sets how long data, prompts and outputs are kept. Responsible AI ensures fairness, transparency and accountability. AI governance assigns ownership, policies and approval processes.",
 "Model risk management assesses and monitors risks of each model use. Explainability shows how a result was reached (sources, factors). Bias checks outcomes across groups. Hallucination risk is reduced with grounding and review. Auditability means logs and versions let you reconstruct any decision.",
 "Access control enforces who can use which AI capability and data. Regulatory awareness tracks the laws and sector rules that apply (EU AI Act, RBI or SEBI guidelines in Indian finance, HIPAA in US health). Enterprise security reviews assess the solution's architecture, data flows, vendors and controls before approval.",
],
"10.5": [
 "Availability: share of time the service works (99.9% ≈ 43 minutes downtime a month). Reliability engineering designs for failure. Scalability handles growth. Fault tolerance keeps working when parts fail. Resilience recovers quickly from failures.",
 "Disaster recovery restores service after a major failure, with targets for recovery time (RTO) and data loss (RPO). Backups must be tested by restoring them. Incident management detects, triages, resolves and communicates. Troubleshooting narrows down causes using logs, metrics and traces. Root cause analysis finds and fixes the underlying cause.",
 "A service-level indicator (SLI) is a measured value (successful requests %). A service-level objective (SLO) is the internal target (99.9%). A service-level agreement (SLA) is the contractual commitment to the customer, usually looser than the SLO, with penalties if missed.",
],
"11.1": [
 "Client discovery meetings learn the client's goals, current process, pain points, systems and constraints. Business requirements describe what outcome is needed; technical requirements describe systems, data, security, performance and integration needs.",
 "Stakeholder interviews collect each group's view (leaders, users, IT, security, finance). Business process observation watches the real work, which often differs from the documented process. Problem validation confirms the problem is real, frequent and costly. Technical feasibility checks access to data and systems, model capability and constraints early.",
],
"11.2": [
 "CTOs care about architecture fit and maintainability; CIOs about systems and portfolio; CFOs about cost and ROI; CISOs about security, privacy and risk; business teams about daily workflow and results. Tailor each conversation to what that person is accountable for.",
 "Manage expectations by stating what AI can and cannot do, accuracy targets and timelines in writing. Resolve disagreements by returning to shared goals and evidence. Communicate technical constraints (rate limits, data access, accuracy limits) early, with options and trade-offs rather than only problems.",
],
"11.3": [
 "Technical presentations explain a solution's design and reasoning. Architecture walkthroughs take reviewers through diagrams, data flows and decisions. Product demonstrations show the solution working on realistic scenarios.",
 "Proof-of-concept presentations report what was tested, results on the client's data and next steps. Technical workshops teach or co-design with client teams. Code-with sessions pair FDEs with client engineers to build together and transfer skills.",
 "Technical documentation: architecture, setup, APIs, runbooks. Executive summaries: one page with problem, result, cost, risk and decision. Business impact presentations connect results to the client's KPIs and money.",
],
"11.4": [
 "Project planning sets milestones, owners and dates. Scope management controls what is in and out, with a change process. Risk management lists risks, likelihood, impact, owner and mitigation.",
 "Testing covers unit, integration, performance and AI evaluation. User acceptance testing (UAT): the client verifies the solution meets agreed criteria. Production readiness: monitoring, security, backups, support and runbooks are in place. Release management schedules and controls go-live. Deployment documentation records how to deploy and roll back.",
 "Knowledge transfer hands over understanding to the client's team. Client training teaches users and admins. Change management helps people adopt the new process.",
],
"11.5": [
 "Production troubleshooting finds why something fails in the live system using logs, metrics and traces. Incident management: detect, classify severity, assign, communicate, resolve. Root cause analysis finds the underlying cause and prevents recurrence.",
 "Monitoring watches health, quality and cost dashboards. Escalation brings in the right expert or vendor when needed. Bug resolution reproduces, fixes, tests and releases. Performance optimisation improves speed and cost (caching, smaller models, better queries).",
 "Post-deployment reviews compare results with goals after launch. Continuous improvement uses feedback, failures and new requirements to plan the next iteration.",
],
"12.1": [
 "Prompt injection: user input that tries to override system instructions ('ignore previous instructions'). Indirect prompt injection: malicious instructions hidden in content the model reads (web pages, emails, documents, tool results). Defences: separate instructions from data, restrict tools, validate outputs, require approval for sensitive actions, and test with attack examples.",
 "Data leakage: exposing secrets, personal data or other users' data through outputs or logs. Insecure output handling: using model output directly in HTML, SQL or shell without escaping or validation. Excessive agency: giving agents more tools, permissions or autonomy than needed. Model denial of service: inputs that consume huge tokens or compute; defend with limits and quotas.",
 "Supply-chain risks: compromised models, libraries, plugins or MCP servers; use trusted sources and pin versions. Retrieval poisoning: attackers plant content in sources the RAG system retrieves. Secrets exposure: keys in prompts, code or logs; keep them in a secrets manager and out of model context.",
],
"12.2": [
 "Secure API integration: HTTPS, signed webhooks, scoped tokens, input validation. Identity and access management: SSO and the user's own permissions applied to data the AI retrieves. Role-based permissions limit features and tools per role.",
 "Personally identifiable information (PII): names, phone numbers, IDs, addresses; detect and mask it where not needed. Encryption in transit and at rest. Data minimisation: send the model only what the task requires. Human approval for consequential actions. AI audit logs record prompts, tools, outputs, users and approvals for review.",
],
"12.3": [
 "Model governance registers models and uses, owners, approvals and versions. AI risk management (NIST AI RMF: govern, map, measure, manage) identifies and treats risks. Responsible AI principles: fairness, reliability, privacy, inclusiveness, transparency and accountability.",
 "Red teaming attacks the system deliberately (injection, jailbreaks, data extraction, harmful content) to find weaknesses. Security testing adds automated scans and penetration tests. Incident response plans how to detect, contain and fix AI-specific incidents, and how to inform affected people.",
 "Threat modelling (for example STRIDE) lists assets, entry points, threats and controls for the AI system. A secure AI deployment checklist covers: data classification, access controls, secrets, input/output validation, tool permissions, logging, evaluation results, red-team results and rollback plan.",
],
"13.1": [
 "An AI automation agency designs, builds and maintains AI and automation solutions for clients. Agency: you deliver custom work. Consulting: you advise and plan. SaaS: you sell one product to many customers. Many start as an agency, then turn repeated solutions into SaaS.",
 "Service business models: project fees, monthly retainers, productised services (fixed scope and price). Niche selection: choose an industry and problem you understand. Target customer: the specific business type and decision-maker. Value proposition: the measurable outcome you deliver.",
 "Service packaging: clear packages (Starter, Growth, Enterprise) with scope and deliverables. Pricing: value-based, fixed-fee or retainer. Client acquisition: referrals, LinkedIn, content, partnerships, cold outreach. Sales funnels: lead → call → audit → proposal → close. Proposals and contracts define scope, timeline, price, acceptance and IP. Retainers fund ongoing support and improvements.",
],
"13.2": [
 "AI customer support: chat and email assistants answer from a knowledge base and escalate. AI lead generation: find, enrich and qualify prospects. Sales automation: follow-ups, CRM updates, meeting booking. Marketing automation: content drafts, campaigns, segmentation.",
 "Document processing: extract data from invoices, forms and contracts. Reporting automation: scheduled reports and summaries from data. AI employee assistants: answer internal policy and process questions. Knowledge management: organise and search company knowledge.",
 "Workflow automation: connect apps to remove manual steps. Voice agents: answer and make phone calls with speech-to-text and text-to-speech. Email automation: classify, route and draft replies. CRM automation: keep records accurate and up to date automatically.",
],
"13.3": [
 "Real estate: capture leads from portals, website and WhatsApp; qualify by budget, location and timeline; recommend matching properties; send follow-ups; schedule site visits; update the CRM; process documents (KYC, agreements); report on pipeline and conversions.",
 "Education: answer student and parent questions 24/7; support admissions (eligibility, documents, deadlines); course assistants explain concepts from course material; monitor progress and alert teachers; send fee reminders; support counselling with information while a human counsellor makes decisions.",
 "Financial services: extract data from statements, payslips and forms; check applications for completeness; validate against rules; answer customer queries; support compliance with checklists and audit trails; detect exceptions and inconsistencies for human review. Credit, lending and compliance decisions stay with authorised humans.",
],
"13.4": [
 "Discovery understands the client's goals. An automation audit finds the best opportunities and estimates impact. Workflow mapping documents the as-is and to-be process. A proposal sets scope, price and timeline. A proof of concept proves feasibility on real data. An MVP delivers the first usable version.",
 "Implementation builds the full solution. Testing verifies accuracy and edge cases. Deployment puts it live. Training teaches users. Support fixes issues and improves the solution. Renewal extends the contract. Case studies document results (with permission) to win new clients.",
],
"13.5": [
 "Startup costs: laptop, registrations, website, legal templates. Technology costs: AI API usage, automation platform plans, hosting, domains. Software and infrastructure costs: CRM, email, design and project tools, cloud. All figures should be treated as hypothetical until checked against current prices.",
 "Project pricing: fixed fee per build based on value and effort. Retainers: monthly fee for support and improvements. Gross margin: revenue minus direct costs (APIs, contractors) divided by revenue. Customer acquisition cost (CAC): sales and marketing spend ÷ new clients. Lifetime value (LTV): average monthly profit per client × months retained.",
 "Break-even: the point where revenue covers all costs. Forecasting: project monthly revenue, costs and cash for 12 months using conservative, expected and optimistic cases. Every financial example in this programme is hypothetical, with assumptions shown, and is not financial advice.",
],
"14.1": [
 "SaaS business models: subscriptions (monthly or annual), freemium, usage-based, or hybrid. B2B SaaS sells to businesses. Vertical SaaS serves one industry (real estate CRM); horizontal SaaS serves one function across industries (helpdesk).",
 "Product-market fit: strong retention and demand from a defined segment. Market research sizes the opportunity (TAM, SAM, SOM). Competitor research compares features, pricing and positioning. Customer segmentation groups buyers by size, industry and need. Pricing strategy sets tiers, value metrics and discounts.",
],
"14.2": [
 "Discovery and validation confirm the problem and willingness to pay. MVP definition chooses the smallest feature set that delivers the core value. Product architecture plans components and data. UX/UI design creates flows and screens.",
 "Frontend (React), backend (FastAPI or Node), database (PostgreSQL), APIs, authentication, multi-tenancy (tenant isolation), security (encryption, RBAC, audits), billing (Stripe or Razorpay), analytics (product events) and deployment (cloud, CI/CD, monitoring) together make a production SaaS.",
],
"14.3": [
 "Customer onboarding gets new accounts to value fast. Customer success monitors health and expands accounts. Support systems: help centre, chat, tickets. Churn is the share of customers who cancel; retention keeps them. Usage analytics show how features are used.",
 "Subscription management handles plans, upgrades, downgrades and renewals. The product roadmap plans improvements. Feature prioritisation weighs customer value, revenue impact and effort. Product growth uses activation, expansion revenue and referrals.",
],
"14.4": [
 "The ideal customer profile (ICP) describes the best-fit company. Positioning states the category, target and difference. The value proposition states the outcome and proof. Landing pages convert visitors with a clear headline, proof and a call to action.",
 "Content marketing and SEO attract buyers searching for solutions. Email marketing nurtures leads. LinkedIn outreach reaches decision-makers. Partnerships with consultants or platforms add channels. Product demos show value. A sales pipeline tracks deals by stage. Customer feedback guides positioning and product.",
],
"14.5": [
 "Product scalability: features that serve larger customers. Technical scalability: architecture that handles more users and data. Cloud cost optimisation: right-sizing, reserved capacity, caching and cheaper models. Support scalability: self-service help and automation.",
 "Team development: hire for engineering, customer success and sales as revenue grows. International expansion: localisation, data residency, payments and tax. Enterprise sales: security reviews, SSO, SLAs and procurement. Channel partnerships: resellers and integrators sell and implement for you.",
],
}
