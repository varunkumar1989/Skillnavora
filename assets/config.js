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
  linkedin: "https://www.linkedin.com/in/varun-pm01",
  instagram: "",
  youtube: "",
  twitter: "",                    // X (Twitter)
  facebook: "",
  telegram: "",
  // Community link, e.g. a WhatsApp community or LinkedIn group. "" hides "Community" in the menu.
  community: "",
  // Counselling call booking link (Calendly or Cal.com). Empty = the counselling form.
  booking: "",
  // Free key from web3forms.com so form submissions also reach your inbox by email.
  web3formsKey: "",
  // Small banner above the home page headline. "" hides it.
  announcement: "Inaugural cohort · Early-bird discount for the first learners",
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
  tag: "⚡ Early-bird pricing"
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
   fee:       e.g. "₹1,50,000". Empty shows "Fees on request".
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
    fee: "Starting from ₹1,50,000", feeNote: "Includes live classes, 25+ case studies, capstone, mock tests, 1:1 mentorship and the job assistance program.",
    earlyBird: "Inaugural early-bird discount for the first cohort. Talk to a counsellor for the early-bird price.",
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
      { title: "Capstone, mock tests and interview preparation", topics: ["Capstone: build and pitch your own AI product", "Weekly mock tests", "Product sense, metrics, strategy, RCA and behavioural rounds", "1:1 mock interviews with feedback"] },
      { title: "Job assistance program", topics: ["Resume and LinkedIn makeover", "Portfolio of 25+ case studies", "Referrals and job-search strategy", "Offer negotiation and salary discussions"] }
    ],
    projects: ["25+ real-world case studies across fintech, e-commerce, SaaS and consumer apps", "AI feature PRD with metrics and guardrails", "Your own product website, built with Claude Code and launched live", "Clickable Figma prototype tested with real users", "End-to-end capstone product"],
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
    id: "ai-swe",
    page: "program/ai-software-engineering.html",
    name: "AI-First Software Engineering",
    short: "Build AI-native apps, automate your workflow with coding agents and learn to design systems with LLMs at the core.",
    tagline: "Learn to build, test and ship like an AI-native engineer",
    badge: "Flagship",
    cohort: "", start: "", deadline: "", fee: "", feeNote: "", earlyBird: "", pay: "",
    duration: "16 weeks", format: "Live online classes with recordings", effort: "10–12 hours a week",
    highlights: ["Real-world projects", "Capstone project", "Mock interviews", "Job assistance"],
    outcomes: ["Ship faster with Claude Code and AI pair programming", "Build LLM apps with RAG, tools and agents",
               "Design scalable systems with AI components", "Test, evaluate and monitor AI features",
               "Deploy securely and control cost", "Ship a portfolio-grade AI product"],
    curriculum: [
      { title: "AI-native development workflow", topics: ["Coding agents and AI pair programming", "Claude Code: plan, edit, test", "Prompting for code"] },
      { title: "LLM fundamentals for engineers", topics: ["Tokens, context and sampling", "Model choice and cost", "Structured outputs"] },
      { title: "Building with LLM APIs", topics: ["Messages and streaming", "Tool use and function calling", "Error handling and retries"] },
      { title: "Retrieval-augmented generation", topics: ["Embeddings and vector search", "Chunking and ranking", "Citations and grounding"] },
      { title: "Agents and MCP", topics: ["Agent loops and planning", "MCP servers and tools", "Multi-agent patterns"] },
      { title: "Evaluation and testing", topics: ["Eval sets and LLM judges", "Regression tests for prompts", "Red-teaming"] },
      { title: "System design with AI", topics: ["Caching, queues and rate limits", "Latency and cost trade-offs", "Designing for failure"] },
      { title: "Shipping to production", topics: ["Deployment and CI/CD", "Observability and monitoring", "Security, privacy and abuse"] },
      { title: "Capstone, interviews and job assistance", topics: ["Build and demo an AI product", "DSA and system design mock interviews", "Resume, portfolio and referrals"] }
    ],
    projects: ["RAG assistant over your own documents", "Agent that uses tools through MCP", "Production-ready capstone app"],
    toolGroups: [
      { name: "Build", tools: ["Claude Code", "Cursor", "GitHub", "VS Code"] },
      { name: "AI", tools: ["Claude API", "Embeddings", "pgvector", "MCP"] },
      { name: "Ship", tools: ["Python", "TypeScript", "Postgres", "Docker", "GitHub Actions", "Cloudflare"] }
    ]
  },
  {
    id: "genai-launchpad",
    page: "program/genai-launchpad.html",
    name: "GenAI Launchpad",
    short: "A beginner-friendly program to use generative AI at work: prompting, AI assistants, no-code apps, automations, chatbots and voice agents.",
    tagline: "Go from AI-curious to AI-confident, with no coding needed",
    badge: "Beginner friendly",
    cohort: "", start: "", deadline: "", fee: "", feeNote: "", earlyBird: "", pay: "",
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
      { title: "Responsible AI", topics: ["Privacy and data safety", "Bias and accuracy", "Company AI policies"] },
      { title: "Capstone", topics: ["Solve a real problem with AI", "Demo day", "Certificate"] }
    ],
    projects: ["Personal AI assistant setup", "Website or no-code app for a real use case", "Automation or chatbot capstone"],
    toolGroups: [
      { name: "AI assistants", tools: ["Claude", "ChatGPT", "Gemini", "Perplexity"] },
      { name: "Build", tools: ["Lovable", "Claude", "Canva"] },
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
  note: ""
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
  { what: "Curriculum depth", sub: "What you'll actually learn", others: "PM basics, interview prep and a few AI tools", us: "Complete AI PM: product sense, strategy, analytics, growth, delivery tools (Jira, Confluence, Asana, Figma) and hands-on AI with Claude and Claude Code" },
  { what: "Hands-on projects", sub: "A portfolio you can show", others: "Often one capstone", us: "25+ real-world case studies, a capstone and your own live website and AI prototype" },
  { what: "Leadership access", sub: "Who guides your career", others: "Program mentors only", us: "Monthly 1:1 counselling with a CEO or Head of Product" },
  { what: "1:1 mentorship", sub: "Personal guidance and feedback", others: "Limited, or extra cost", us: "1:1 mentorship and mock interviews included" },
  { what: "AI PM training", sub: "Future-proof skills", others: "Mostly concepts", us: "Hands-on modules from prompt engineering to building agentic AI products" },
  { what: "Interview preparation", sub: "Getting the offer", others: "A few sessions", us: "Intensive: weekly mock tests, 1:1 mock interviews and a structured question bank" },
  { what: "Placement support", sub: "Getting your PM role", others: "A basic job board", us: "Job assistance program: resume, LinkedIn, portfolio, referrals and job-search support" },
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
  { c: "Fees", q: "What are the fees?", a: "AI-First Product Management starts from ₹1,50,000, with an inaugural early-bird discount for the first cohort. Talk to a counsellor for the current price and payment options." },
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
   also list them here. category: "product", "ai" or "engineering".
   { title: "Product Manager", company: "Company", location: "Bengaluru, India", category: "product",
     experience: "3-5 years", job_type: "Full time", posted_on: "2027-01-10",
     url: "https://www.linkedin.com/jobs/view/...", logo: "" } */
const JOBS = [
];

/* ---- Reviews. Add REAL reviews from your learners, with their permission.
   The Reviews page, menu item and home section appear once you add one.
   { name: "Priya S.", company: "Fintech startup", role: "Associate PM",
     quote: "...", photo: "assets/priya.jpg", linkedin: "https://...", video: "https://youtube.com/..." } */
const TESTIMONIALS = [
];
