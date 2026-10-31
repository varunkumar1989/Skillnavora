/* =====================================================================
   SKILLNAVORA SETTINGS: edit this one file to update the whole site.
   On GitHub: open this file, click the pencil, edit, "Commit changes".
   The site updates in about a minute. Leave a value "" to hide it.
   The AI chat assistant also answers visitors' questions from this file,
   so keep it accurate.
   ===================================================================== */

const SITE = {
  name: "SkillNavora",
  email: "support@skillnavora.in",
  phone: "919211315006",          // with or without 91 in front
  whatsapp: "919211315006",
  address: "",                    // e.g. "Bengaluru, Karnataka, India" (shown in the footer)
  linkedin: "https://www.linkedin.com/in/skill-navora-1600b5447",
  founderLinkedin: "https://www.linkedin.com/in/varun-pm01",   // instructor section
  instagram: "https://www.instagram.com/skillnavora/",
  youtube: "https://www.youtube.com/@SkillNavora",
  twitter: "https://x.com/skillnavora",   // X (Twitter)
  facebook: "https://www.facebook.com/profile.php?id=61595706998987",
  telegram: "",
  // Community link, e.g. a WhatsApp community or LinkedIn group. "" hides "Community" in the menu.
  community: "",
  // Counselling call booking link (Calendly or Cal.com). Empty = the counselling form.
  booking: "",
  // Free key from web3forms.com so form submissions also reach your inbox by email.
  web3formsKey: "",
  // Small banner above the home page headline. "" hides it.
  announcement: "Inaugural cohort · Scholarships up to 100% for eligible candidates",
  announcementLink: "program/ai-product-management.html",
  // Show the "Not sure if this is for you?" pop-up after this many minutes on the site. 0 turns it off.
  popupMinutes: 5,
  // AI chat assistant (needs ANTHROPIC_API_KEY set in Cloudflare; see supabase/README.md). false hides it.
  chatbot: true
};

/* ---- Top announcement bar (all public pages). text "" hides it. ---- */
const TOPBAR = {
  text: "Learn AI-first Product Management. Inaugural cohort enrolling now",
  cta: "Apply now",
  link: "apply.html?program=ai-pm",
  tag: "Scholarships up to 100%"
};

/* ---- Student and admin logins (Supabase) ------------------------------
   See supabase/README.md. Paste the Project URL and the publishable
   ("anon public") key. NEVER paste the secret / service_role key.
   google: true shows "Continue with Google" (turn it on in Supabase first).
   phone:  true shows "Mobile number + OTP" (needs an SMS provider in Supabase).
   whatsapp: true shows "Continue with WhatsApp" (needs Twilio or Twilio Verify
             with a WhatsApp sender, set up as the SMS provider in Supabase). */
const AUTH = {
  supabaseUrl: "https://rnncabqtcxxivuyjwoja.supabase.co",
  supabaseKey: "sb_publishable_9sKPYxU3MHQfNT43n3d95A_bVLZi7BP",
  google: true,
  phone: false,
  whatsapp: false
};

/* ---- Programs ----------------------------------------------------------
   id:        don't change once students are enrolled (used by the LMS).
   cohort:    e.g. "Cohort 1". start: e.g. "15 Jan 2027".
   deadline:  enrolment closing date-time, e.g. "2027-01-10T23:59:00+05:30".
              Shows a live countdown like "Enrolment closes in 2d : 4h".
   fee:       e.g. "$2,000". Empty shows "Fees on request".
   feeINR:    the rupee price shown next to it, e.g. "₹1,74,000" (approximate; update if your price differs).
   earlyBird: early-bird offer text. Empty hides it.
   pay:       payment link (Razorpay, Instamojo...), shown after someone applies.
   Everything below is a starting draft: edit it to match your program. */
const COURSES = [
  {
    id: "ai-pm",
    page: "program/ai-product-management.html",
    name: "AI-First Product Management",
    short: "Learn the skills, tools and AI workflows to solve real product problems, build a portfolio with 25+ case studies and crack your next PM interview.",
    tagline: "The end-to-end program to become a confident, job-ready AI product manager",
    badge: "Flagship",
    cohort: "Inaugural cohort", start: "", deadline: "",
    fee: "$2,000", feeINR: "₹1,74,000", feeNote: "Includes live classes, 25+ case studies, capstone, mock tests, 1:1 mentorship and the job assistance program.",
    earlyBird: "",
    pay: "",
    duration: "16 weeks", format: "Live online classes with recordings", effort: "8–10 hours a week",
    highlights: ["25+ real-world case studies", "Capstone project", "Mock tests and interviews", "Monthly 1:1 with a CEO or Head of Product"],
    outcomes: ["Run discovery and turn research into clear problem statements",
               "Prioritise, write PRDs and user stories, and align stakeholders",
               "Plan sprints and ship with Jira, Confluence and Asana",
               "Define metrics, read funnels, write SQL and run A/B tests",
               "Design and ship AI features: LLMs, RAG, agents, evals and guardrails",
               "Build and launch your own website and AI prototype with Claude Code, Figma and Lovable",
               "Build a portfolio of 25+ case studies and a capstone",
               "Crack PM interviews with mock tests and 1:1 mock interviews"],
    curriculum: [
      { title: "Product thinking and the PM role", topics: ["What PMs do and how they decide", "Product life cycle and delivery approaches (Agile, Scrum, Kanban)", "Outcomes over output", "Types of PM roles: B2C, B2B SaaS, platform, growth, AI PM"] },
      { title: "Product strategy", topics: ["Vision, positioning and moats", "Market sizing (TAM, SAM, SOM) and competitor analysis", "Business models and pricing", "OKRs and outcome roadmaps"] },
      { title: "Discovery and user research", topics: ["User interviews and surveys", "Jobs-to-be-done, personas and journey maps", "Synthesis and insights", "Research tools: Google Forms, Typeform, Dovetail, Hotjar, Microsoft Clarity"] },
      { title: "Problem framing and prioritisation", topics: ["Root-cause analysis: five whys, fishbone", "RICE, Kano, MoSCoW and value vs effort", "MVPs and experiment design", "Opportunity solution trees"] },
      { title: "UX, wireframes and Figma", topics: ["UX principles and design reviews", "Wireframes and prototypes in Figma and FigJam", "Usability testing", "Working with designers; Balsamiq and Miro for quick sketches"] },
      { title: "PRDs, user stories and documentation", topics: ["Writing PRDs and one-pagers", "User stories and acceptance criteria", "Confluence and Notion for product docs", "Writing PRDs with AI and getting them critiqued"] },
      { title: "Agile delivery with Jira, Confluence and Asana", topics: ["Backlogs, epics, sprints and boards in Jira", "Sprint planning, stand-ups and retros", "Roadmaps and cross-team projects in Asana", "Release notes and stakeholder updates; Linear, Trello and ClickUp compared"] },
      { title: "Analytics, SQL and experimentation", topics: ["North-star, input and guardrail metrics", "Funnels, cohorts and retention in Mixpanel, Amplitude and GA4", "SQL for PMs and Excel / Google Sheets", "Dashboards in Looker Studio; A/B testing and statistics basics"] },
      { title: "Launch, growth and monetisation", topics: ["Go-to-market planning", "Growth loops, activation and retention", "Pricing and packaging", "Launch checklists and post-launch reviews"] },
      { title: "Tech and system design for PMs", topics: ["How the web works: front end, back end, APIs and databases", "Testing APIs with Postman", "Cloud, scalability and trade-offs", "Explaining systems in interviews"] },
      { title: "AI foundations for PMs", topics: ["How LLMs work: tokens, context, hallucinations", "Prompt engineering", "RAG, embeddings and vector search", "Evaluations, cost, latency, risk and responsible AI"] },
      { title: "Claude for product managers", topics: ["Claude Projects for research, synthesis and PRDs", "Artifacts: dashboards, mock-ups and documents", "Connectors: Gmail, Calendar, Drive, Slack and GitHub", "Skills and MCP: connecting Claude to your own tools"] },
      { title: "Claude Code: build and launch a website", topics: ["Setting up Claude Code and GitHub", "Building a landing page or product website from a prompt", "Deploying free on Cloudflare Pages or Netlify, with your own domain", "Adding forms, analytics and an AI chatbot; iterating safely with Git"] },
      { title: "AI prototyping and automation tools", topics: ["Lovable, Bolt, v0 and Replit for app prototypes", "Figma Make and AI design tools", "n8n, Zapier and Make automations", "ChatGPT, Gemini, Perplexity and NotebookLM for research"] },
      { title: "Agentic AI and AI product design", topics: ["Agents, tool use and MCP", "Human-in-the-loop and guardrails", "AI metrics and evaluation", "Writing an AI PRD"] },
      { title: "AI evals: measuring AI quality (basic to advanced)", topics: ["What evals are and why PMs own them; success criteria and rubrics", "Golden datasets, code graders, human review and LLM-as-judge", "Error analysis, RAG and agent evals, safety and red-teaming", "A/B tests, monitoring, regression gates and the eval section of an AI PRD"] },
      { title: "Browser automation and AI agents", topics: ["Scripts, RPA and AI browser agents: when to use which", "Playwright basics and Chrome Recorder for PMs", "Computer-use agents, deep research agents and competitor research", "Safety, approvals, prompt injection and evaluating browser agents"] },
      { title: "Your AI second brain and context engineering", topics: ["PARA and CODE: capture, organise, distil, express", "NotebookLM, Claude Projects, Notion AI and Obsidian", "Context engineering and managing AI memory", "Insight repository, decision log and MCP-connected knowledge"] },
      { title: "Capstone, mock tests and interview preparation", topics: ["Capstone: build and pitch your own AI product", "Weekly mock tests", "Product sense, metrics, strategy, RCA and behavioural rounds", "1:1 mock interviews with feedback"] },
      { title: "Job assistance program", topics: ["Resume and LinkedIn makeover", "Portfolio of 25+ case studies", "Referrals and job-search strategy", "Offer negotiation and salary discussions"] }
    ],
    projects: ["25+ real-world case studies across fintech, e-commerce, SaaS and consumer apps", "AI feature PRD with metrics and guardrails", "Eval plan and golden dataset for an AI feature", "Your own product website, built with Claude Code and launched live", "Clickable Figma prototype tested with real users", "End-to-end capstone product"],
    toolGroups: [
      { name: "Product and delivery", tools: ["Jira", "Confluence", "Asana", "Notion", "Linear", "Trello", "ClickUp", "Productboard", "Aha!"] },
      { name: "Design and collaboration", tools: ["Figma", "FigJam", "Miro", "Balsamiq", "Whimsical", "Slack", "Loom"] },
      { name: "Analytics and data", tools: ["Mixpanel", "Amplitude", "Google Analytics 4", "SQL", "Excel / Google Sheets", "Looker Studio", "Hotjar", "Microsoft Clarity"] },
      { name: "Research and testing", tools: ["Typeform", "Google Forms", "Maze", "Dovetail", "Postman"] },
      { name: "AI assistants", tools: ["Claude", "ChatGPT", "Gemini", "Perplexity", "NotebookLM", "Microsoft Copilot"] },
      { name: "Build with AI", tools: ["Claude Code", "Cursor", "GitHub", "Lovable", "Bolt", "v0", "Replit", "Figma Make"] },
      { name: "Automation", tools: ["n8n", "Zapier", "Make"] }
    ]
  },
  {
    id: "ai-de",
    page: "program/ai-data-engineering.html",
    name: "AI-First Data Engineer",
    short: "Learn SQL, Python, data modelling, pipelines, Spark, Airflow and the cloud, then build the data and AI pipelines that power modern products.",
    tagline: "Build reliable data pipelines and the data foundation for AI",
    badge: "Flagship",
    cohort: "", start: "", deadline: "", fee: "$1,500", feeINR: "₹1,30,000", feeNote: "Includes live classes, real-world projects, capstone, mock interviews and job assistance.", earlyBird: "", pay: "",
    duration: "16 weeks", format: "Live online classes with recordings", effort: "10–12 hours a week",
    highlights: ["Real-world projects", "Capstone project", "Mock interviews", "Job assistance"],
    outcomes: ["Write advanced SQL and production-quality Python for data", "Design data models and warehouses (star schema, lakehouse)",
               "Build batch and streaming pipelines with Spark, Airflow, dbt and Kafka", "Run data on the cloud with Snowflake, BigQuery or Databricks",
               "Build AI data pipelines: embeddings, vector databases and RAG", "Ship a portfolio-grade end-to-end data platform"],
    curriculum: [
      { title: "SQL for data engineers", topics: ["Joins, window functions and CTEs", "Query performance and indexes", "SQL interview patterns"] },
      { title: "Python for data engineering", topics: ["Python for files, APIs and automation", "pandas and Polars", "Testing and packaging code"] },
      { title: "Data modelling and warehousing", topics: ["OLTP vs OLAP", "Star and snowflake schemas", "Slowly changing dimensions"] },
      { title: "ETL and ELT pipelines", topics: ["Batch ingestion from APIs and databases", "Transformations with dbt", "Incremental loads and idempotency"] },
      { title: "Orchestration with Airflow", topics: ["DAGs, scheduling and retries", "Backfills and dependencies", "Monitoring and alerting"] },
      { title: "Big data with Spark", topics: ["Spark and PySpark basics", "Partitioning and performance", "Lakehouse with Delta Lake"] },
      { title: "Streaming data", topics: ["Kafka fundamentals", "Real-time pipelines", "Exactly-once and late data"] },
      { title: "Cloud data platforms", topics: ["AWS, GCP and Azure data services", "Snowflake, BigQuery and Databricks", "Cost, security and access control"] },
      { title: "Data quality and governance", topics: ["Data tests and contracts", "Lineage and observability", "Privacy and compliance"] },
      { title: "AI for data engineers", topics: ["Embeddings and vector databases", "RAG and LLM data pipelines", "AI-assisted coding with Claude Code"] },
      { title: "Capstone, interviews and job assistance", topics: ["End-to-end data platform capstone", "SQL, Python and system design mock interviews", "Resume, portfolio and referrals"] }
    ],
    audience: [
      { title: "Students and freshers", text: "Learn SQL, Python and pipelines with real projects, and aim for data engineer and analytics engineer roles." },
      { title: "Working professionals", text: "Learn on weekends alongside your job, with live classes, recordings and flexible schedules." },
      { title: "Career switchers", text: "Move into data engineering from software, testing, support, analytics or any technical role." },
      { title: "Salary hike and promotion", text: "Grow into senior data engineer and data platform roles with stronger skills, a portfolio and interview preparation." }
    ],
    projects: ["Batch ELT pipeline with Airflow and dbt into a cloud warehouse", "Real-time streaming pipeline with Kafka and Spark", "RAG data pipeline with embeddings and a vector database"],
    toolGroups: [
      { name: "Code and query", tools: ["SQL", "Python", "pandas", "Jupyter", "Git"] },
      { name: "Pipelines", tools: ["Apache Airflow", "dbt", "Apache Spark", "Apache Kafka", "Docker"] },
      { name: "Cloud and warehouse", tools: ["Snowflake", "BigQuery", "Databricks", "AWS", "PostgreSQL"] },
      { name: "AI", tools: ["Claude", "Claude Code", "ChatGPT", "GitHub Copilot", "Pinecone", "Replit"] }
    ]
  },
  {
    id: "genai-launchpad",
    page: "program/genai-launchpad.html",
    name: "GenAI Launchpad",
    short: "A beginner-friendly program to use generative AI at work: prompting, AI assistants, no-code apps, automations, chatbots and voice agents.",
    tagline: "Go from AI-curious to AI-confident, with no coding needed",
    badge: "Beginner friendly",
    cohort: "", start: "", deadline: "", fee: "$1,000", feeINR: "₹87,000", feeNote: "Includes live classes, hands-on projects, a capstone and demo day.", earlyBird: "", pay: "",
    duration: "8 weeks", format: "Live online classes with recordings", effort: "5–6 hours a week",
    highlights: ["Hands-on projects", "No coding needed", "Capstone and demo day", "Certificate"],
    outcomes: ["Write prompts that get reliable results", "Use Claude daily for writing, research and analysis",
               "Build a website or web app without code", "Automate repetitive work with n8n or Zapier",
               "Launch a WhatsApp or website chatbot", "Use AI responsibly and safely"],
    curriculum: [
      { title: "How generative AI works", topics: ["LLMs in plain language", "What AI is good and bad at", "Choosing the right tool"] },
      { title: "Prompting that works", topics: ["Clear instructions and examples", "Roles, formats and constraints", "Checking and improving answers"] },
      { title: "AI assistants for daily work", topics: ["Claude Projects", "Research and analysis", "Docs, emails and presentations"] },
      { title: "Websites and no-code apps", topics: ["Lovable from prompt to app", "Building a website with Claude", "Publishing with your own domain"] },
      { title: "Automation", topics: ["Zapier and Make basics", "n8n with AI steps", "Email and sheet workflows"] },
      { title: "Chatbots and voice agents", topics: ["WhatsApp and website bots", "Voice receptionists", "Handoff to humans"] },
      { title: "AI agents, MCP and deep research", topics: ["What AI agents are and how they use tools", "MCP: connecting AI to your apps", "Deep research agents and checking sources"] },
      { title: "Browser automation and AI agents", topics: ["No-code record-and-replay and AI browser agents", "Writing safe agent tasks with stop points", "Real workflows: research, forms, price tracking"] },
      { title: "Your AI second brain", topics: ["PARA and CODE with Notion, Obsidian or NotebookLM", "Context engineering and AI memory", "Automating notes from meetings, email and reading"] },
      { title: "AI evals: checking AI quality", topics: ["What evals are and simple rubrics", "Test sets and AI-as-judge", "Safety checks and monitoring"] },
      { title: "Responsible AI", topics: ["Privacy and data safety", "Bias and accuracy", "Company AI policies"] },
      { title: "Capstone", topics: ["Solve a real problem with AI", "Demo day", "Certificate"] }
    ],
    audience: [
      { title: "Students and freshers", text: "Learn the AI tools employers expect and build projects you can show, with no coding needed." },
      { title: "Working professionals", text: "Save hours every week with AI assistants and automations, on weekends alongside your job." },
      { title: "Business owners", text: "Build chatbots, voice agents and automations that help your business serve customers." },
      { title: "Career switchers", text: "Add practical AI skills that make you stand out in any role or industry." }
    ],
    projects: ["Personal AI assistant setup", "Website or no-code app for a real use case", "Automation or chatbot capstone"],
    toolGroups: [
      { name: "AI assistants", tools: ["Claude", "ChatGPT", "Gemini", "Perplexity"] },
      { name: "Build", tools: ["Lovable", "Replit", "Claude", "Canva"] },
      { name: "Automate", tools: ["Zapier", "Make", "n8n", "WhatsApp Business"] }
    ]
  }
];

/* ---- Stats band under the "What makes us different" section.
   show: false keeps it hidden. Only switch it on with numbers you can prove:
   India's consumer protection rules (CCPA) penalise misleading placement claims.
   note: short source line shown under the numbers, e.g. "Placements of learners mentored by Varun Kumar since 2019". */
const STATS = {
  show: false,
  items: [
    { n: "100+", t: "Students placed" },
    { n: "50 LPA", t: "Highest package" },
    { n: "50+", t: "Industry experts" },
    { n: "500+", t: "Hiring companies" }
  ],
  note: "One scholarship or discount per learner. Scholarships are decided after a short test and a counselling call."
};

/* ---- Who is this for (home and program pages) ---- */
const AUDIENCE = [
  { title: "Students and freshers", text: "Build real PM skills and a portfolio before your first job, and aim for APM and analyst roles." },
  { title: "Working professionals", text: "Learn on weekends alongside your job, with live classes, recordings and flexible schedules." },
  { title: "Career switchers", text: "Move into product from engineering, design, sales, operations, consulting or any other role." },
  { title: "Salary hike and promotion", text: "Grow into senior PM and AI PM roles with stronger skills, a portfolio and interview preparation." }
];

/* ---- What makes SkillNavora different (the moat) ---- */
const MOAT = [
  { title: "Monthly 1:1 with a CEO or Head of Product", text: "Every month, a 1:1 counselling session with a CEO or Head of Product to review your progress, portfolio and career plan." },
  { title: "25+ real-world case studies", text: "Work on real problems from fintech, e-commerce, SaaS and consumer apps, so you graduate with a portfolio, not just a certificate." },
  { title: "Build and launch your own product", text: "Use Claude, Claude Code, Figma and Lovable to build and launch a real website and AI prototype that recruiters can try." },
  { title: "Job-ready, not just course-complete", text: "Capstone, weekly mock tests, 1:1 mock interviews and a job assistance program until you're ready to apply." }
];

/* ---- Why join: comparison table ---- */
const COMPARE = [
  { what: "Curriculum depth", sub: "What you'll actually learn", others: "Basics, interview prep and a few AI tools", us: "Job-ready depth in every track: AI product management, data engineering (SQL, Airflow, Spark, cloud) and generative AI, all hands-on with Claude and Claude Code" },
  { what: "Hands-on projects", sub: "A portfolio you can show", others: "Often one capstone", us: "Real-world case studies and projects in every module, plus a capstone you can demo: a live product, a data platform or an AI automation" },
  { what: "Leadership access", sub: "Who guides your career", others: "Program mentors only", us: "Monthly 1:1 counselling with an industry leader to review your progress, portfolio and career plan" },
  { what: "1:1 mentorship", sub: "Personal guidance and feedback", others: "Limited, or extra cost", us: "1:1 mentorship, assignment feedback and mock interviews included" },
  { what: "AI skills", sub: "Future-proof for every role", others: "Mostly concepts", us: "Hands-on AI in every program: prompting, AI assistants, RAG, agents, AI data pipelines and automation" },
  { what: "Interview preparation", sub: "Getting the offer", others: "A few sessions", us: "Role-specific mock tests, 1:1 mock interviews and question banks for PM, data engineering and AI roles" },
  { what: "Placement support", sub: "Getting your next role", others: "A basic job board", us: "1 year of placement support: resume, LinkedIn, portfolio, referrals and job-search help" },
  { what: "Schedule flexibility", sub: "For working professionals", others: "Fixed schedule", us: "Weekend live classes, recordings in the LMS and help to catch up" }
];

/* ---- Job assistance program and interview preparation ---- */
const JOB_ASSIST = {
  program: ["Resume and LinkedIn makeover with 1:1 reviews", "Portfolio of 25+ case studies, capstone and your live product", "Referrals through our network when you're job-ready", "Job-search strategy: target roles, companies and outreach", "Offer evaluation and salary negotiation guidance"],
  interview: ["Weekly mock tests on product sense, metrics and strategy", "1:1 mock interviews with detailed feedback", "Question bank: product design, RCA, guesstimates, metrics, behavioural", "AI PM and system design rounds for PMs", "Practice with AI between sessions"]
};

/* ---- Mentors. The section appears once you add at least one REAL mentor.
   { name: "Name", role: "Head of Product", company: "Company", photo: "assets/mentor-name.jpg",
     linkedin: "https://www.linkedin.com/in/...", note: "IIM Bangalore alumnus" } */
const MENTORS = [
];

/* ---- Career support cards ---- */
const SUPPORT = [
  { title: "Resume optimisation", text: "1:1 resume and LinkedIn reviews that show the right transferable skills." },
  { title: "Build your portfolio", text: "25+ real-world case studies, a capstone and your own live product." },
  { title: "Intensive interview prep", text: "Weekly mock tests, a question bank and 1:1 mock interviews." },
  { title: "Job assistance program", text: "Referrals, job-search strategy and offer guidance when you're job-ready." }
];

/* ---- FAQs. category: Program, Schedule, Fees or Career ---- */
const FAQS = [
  { c: "Program", q: "How is the program delivered?", a: "Through live online classes with instructors, 25+ hands-on case studies, assignments and a capstone. All classes are recorded and added to your LMS." },
  { c: "Program", q: "What if I can't attend a live session? Do I get recordings?", a: "Yes. Every live session is recorded and available in your LMS, so you can catch up any time." },
  { c: "Program", q: "Can I do this alongside a full-time job?", a: "Yes. Classes are scheduled for working professionals, and recordings let you learn at your own pace." },
  { c: "Program", q: "I'm a student or fresher. Can this program help me?", a: "Yes. The program starts from the fundamentals and helps you build a portfolio that shows what you can do." },
  { c: "Program", q: "Which tools will I learn?", a: "Delivery tools like Jira, Confluence, Asana and Notion; design tools like Figma and Miro; analytics like Mixpanel, Amplitude, GA4 and SQL; and AI tools including Claude, Claude Code, ChatGPT, Gemini, Lovable and n8n." },
  { c: "Program", q: "Can I ask instructors and mentors questions directly?", a: "Yes, during live classes, in 1:1 mentorship, and through the LMS. You also get a monthly 1:1 session with a CEO or Head of Product." },
  { c: "Schedule", q: "What are the timings and schedule?", a: "Live classes run on weekends. Exact timings are shared before each cohort starts; talk to a counsellor for the current schedule." },
  { c: "Fees", q: "What are the fees?", a: "AI-First Product Management is $2,000, AI-First Data Engineer is $1,500 and GenAI Launchpad is $1,000. Eligible candidates can get a scholarship of up to 100%. Talk to a counsellor for payment options." },
  { c: "Career", q: "Do you help with jobs?", a: "Yes, through the job assistance program: resume and LinkedIn reviews, portfolio, intensive interview preparation and referrals through our network. No one can honestly guarantee a job, but we work with you until you're job-ready." },
  { c: "Career", q: "Will I get a certificate?", a: "Yes, you get a certificate when you complete the program and capstone." },
  { c: "Career", q: "I have more questions. Where can I ask?", a: "Ask our AI assistant, message us on WhatsApp, or book a free counselling session." }
];

/* ---- Public events (Events page). Past ones move to "Past events".
   { title: "Build agentic workflows with n8n", date: "2027-01-18", time: "5:00 PM – 6:30 PM",
     text: "Live build-along for beginners.", register: "https://forms.gle/..." } */
const EVENTS = [
];

/* ---- Job board extras. Jobs are easiest to manage in Admin → Job board; you can
   also list them here. category: "product", "ai" or "data" (data engineering).
   { title: "Product Manager", company: "Company", location: "Bengaluru, India", category: "product",
     experience: "3-5 years", job_type: "Full time", posted_on: "2027-01-10",
     url: "https://www.linkedin.com/jobs/view/...", logo: "" } */
/* ---- Official websites for the tools listed on program pages ----------- */
const TOOL_LINKS = {
  "Apache Airflow": "https://airflow.apache.org", "dbt": "https://www.getdbt.com", "Apache Spark": "https://spark.apache.org", "Apache Kafka": "https://kafka.apache.org",
  "Docker": "https://www.docker.com", "Snowflake": "https://www.snowflake.com", "BigQuery": "https://cloud.google.com/bigquery", "Databricks": "https://www.databricks.com",
  "AWS": "https://aws.amazon.com", "PostgreSQL": "https://www.postgresql.org", "Pinecone": "https://www.pinecone.io", "Git": "https://git-scm.com",
  "Jira": "https://www.atlassian.com/software/jira", "Confluence": "https://www.atlassian.com/software/confluence", "Asana": "https://asana.com",
  "Notion": "https://www.notion.com", "Linear": "https://linear.app", "Trello": "https://trello.com", "ClickUp": "https://clickup.com",
  "Productboard": "https://www.productboard.com", "Aha!": "https://www.aha.io",
  "Figma": "https://www.figma.com", "FigJam": "https://www.figma.com/figjam/", "Miro": "https://miro.com", "Balsamiq": "https://balsamiq.com",
  "Whimsical": "https://whimsical.com", "Slack": "https://slack.com", "Loom": "https://www.loom.com",
  "Mixpanel": "https://mixpanel.com", "Amplitude": "https://amplitude.com", "Google Analytics 4": "https://marketingplatform.google.com/about/analytics/",
  "SQL": "https://www.w3schools.com/sql/", "Excel / Google Sheets": "https://workspace.google.com/products/sheets/", "Looker Studio": "https://lookerstudio.google.com",
  "Hotjar": "https://www.hotjar.com", "Microsoft Clarity": "https://clarity.microsoft.com",
  "Typeform": "https://www.typeform.com", "Google Forms": "https://www.google.com/forms/about/", "Maze": "https://maze.co", "Dovetail": "https://dovetail.com",
  "Postman": "https://www.postman.com",
  "Claude": "https://claude.ai", "ChatGPT": "https://chatgpt.com", "Gemini": "https://gemini.google.com", "Perplexity": "https://www.perplexity.ai",
  "NotebookLM": "https://notebooklm.google", "Microsoft Copilot": "https://copilot.microsoft.com",
  "Claude Code": "https://www.anthropic.com/claude-code", "Cursor": "https://cursor.com", "GitHub": "https://github.com", "Lovable": "https://lovable.dev",
  "Bolt": "https://bolt.new", "v0": "https://v0.dev", "Replit": "https://replit.com", "Figma Make": "https://www.figma.com/make/",
  "n8n": "https://n8n.io", "Zapier": "https://zapier.com", "Make": "https://www.make.com",
  "Python": "https://www.python.org", "pandas": "https://pandas.pydata.org", "NumPy": "https://numpy.org", "Jupyter": "https://jupyter.org",
  "scikit-learn": "https://scikit-learn.org", "XGBoost": "https://xgboost.ai", "Statsmodels": "https://www.statsmodels.org",
  "Power BI": "https://www.microsoft.com/power-platform/products/power-bi", "Tableau": "https://www.tableau.com", "Matplotlib": "https://matplotlib.org",
  "Seaborn": "https://seaborn.pydata.org", "Excel": "https://www.microsoft.com/microsoft-365/excel", "GitHub Copilot": "https://github.com/features/copilot",
  "Canva": "https://www.canva.com", "WhatsApp Business": "https://business.whatsapp.com"
};

/* ---- Scholarships and payment options ------------------------------------
   earlyBirdEnds: a real end date (India time) shows a countdown; leave "" to hide it.
   items: the scholarships and options you offer. */
const OFFERS = {
  earlyBirdEnds: "",
  earlyBirdText: "",
  items: [
    { pct: "Up to 100%", title: "Merit scholarship", text: "For eligible candidates who do well in the SkillNavora scholarship test and interview. Limited seats every cohort." },
    { pct: "Students", title: "Students and freshers", text: "Special pricing for college students and recent graduates, with a valid student or graduation ID." },
    { pct: "EMI", title: "Flexible payment plans", text: "Pay the fee in easy monthly instalments, with plans for every cohort." }
  ],
  note: "One scholarship or discount per learner. Scholarships are decided after a short test and a counselling call."
};

/* ---- Refer & earn ------------------------------------------------------
   learnerReward / hireReward: the reward you pay, e.g. "₹10,000". Leave "" to
   show "a cash reward" until you decide the amounts. */
const REFERRAL = {
  learnerReward: "",
  hireReward: "",
  terms: "Rewards are paid by bank transfer or UPI after the referred learner completes 30 days of the program, or the referred candidate completes 90 days in the new job. One reward per person referred. SkillNavora may update these terms."
};

/* ---- Careers page: open roles at SkillNavora ------------------------------
   Leave empty to show "send a general application". Example:
   { title: "Teaching assistant (AI PM)", team: "Teaching", type: "Part time", location: "Remote", text: "Help learners with assignments and doubts." } */
const CAREERS = [
];

const JOBS = [
];

/* ---- Reviews. Add REAL reviews from your learners, with their permission
   (the Reviews page form collects them into Admin -> Applications).
   Wrap phrases in ==double equals== to highlight them. Example:
   { name: "Priya S.", photo: "assets/priya.jpg", linkedin: "https://...",
     quote: "The program ==helped me build a real product portfolio==. The mock interviews...",
     from: { role: "Business Analyst", company: "Infosys" },
     to:   { role: "Associate Product Manager", company: "Razorpay" } } */
const TESTIMONIALS = [
];
