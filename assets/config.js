/* =====================================================================
   SKILLNAVORA SETTINGS: edit this one file to update the whole site.
   On GitHub: open this file, click the pencil, edit, "Commit changes".
   The site updates in about a minute. Leave a value "" to hide it.
   ===================================================================== */

const SITE = {
  name: "SkillNavora",
  email: "varunebix@gmail.com",
  phone: "919211315006",          // with or without 91 in front
  whatsapp: "919211315006",
  address: "",                    // e.g. "Bengaluru, Karnataka, India" (shown in the footer)
  linkedin: "https://www.linkedin.com/in/varun-pm01",
  instagram: "",
  youtube: "",
  // Counselling call booking link (Calendly or Cal.com). Empty = WhatsApp.
  booking: "",
  // Free key from web3forms.com so contact-form messages reach your inbox.
  web3formsKey: "",
  // Optional banner at the top of the home page. "" hides it.
  announcement: "New cohorts open for AI-First Product Management",
  announcementLink: "program/ai-product-management.html"
};

/* ---- Student and admin logins (Supabase) ------------------------------
   See supabase/README.md. Paste the Project URL and the publishable
   ("anon public") key. NEVER paste the secret / service_role key.
   google: true shows "Continue with Google" (turn it on in Supabase first). */
const AUTH = {
  supabaseUrl: "",
  supabaseKey: "",
  google: false
};

/* ---- Programs ----------------------------------------------------------
   id:        don't change once students are enrolled (used by the LMS).
   cohort:    e.g. "Cohort 1". start: e.g. "15 Jan 2027".
   deadline:  enrolment closing date-time, e.g. "2027-01-10T23:59:00+05:30".
              Shows a live countdown like "Enrolment closes in 2d : 4h".
   fee:       e.g. "₹49,999". Empty shows "Fees on request".
   enroll:    payment or application link (Razorpay, Google Form...).
              Empty opens WhatsApp.
   Everything below is a starting draft: edit it to match your program. */
const COURSES = [
  {
    id: "ai-pm",
    page: "program/ai-product-management.html",
    name: "AI-First Product Management",
    short: "Learn the skills and AI tools to solve real product problems, build your portfolio and crack your next PM interview.",
    tagline: "The end-to-end program to become a confident, AI-first product manager",
    badge: "Flagship",
    cohort: "", start: "", deadline: "", fee: "", feeNote: "", enroll: "",
    duration: "16 weeks", format: "Live online classes with recordings", effort: "8–10 hours a week",
    for: ["Aspiring PMs switching from engineering, design, sales, operations or consulting",
          "Associate and junior PMs who want to grow faster",
          "Students and freshers aiming for APM roles"],
    outcomes: ["Run discovery and turn research into clear problem statements",
               "Prioritise, write PRDs and align stakeholders",
               "Define metrics, read funnels and run experiments",
               "Design and ship AI features: LLMs, RAG and agents",
               "Prototype with Claude, Figma, Lovable and n8n",
               "Build a portfolio of 3+ case studies and ace PM interviews"],
    curriculum: [
      { title: "Product thinking and the PM role", topics: ["What PMs do and how they decide", "Product life cycle and delivery approaches", "Outcomes over output"] },
      { title: "Product strategy", topics: ["Vision, positioning and moats", "Market sizing and competitor analysis", "OKRs and roadmaps"] },
      { title: "Discovery and user research", topics: ["Interviews and surveys", "Jobs-to-be-done and personas", "Journey maps and synthesis"] },
      { title: "Problem framing and prioritisation", topics: ["Root-cause analysis", "RICE, Kano and MoSCoW", "MVPs and experiments"] },
      { title: "UX and design collaboration", topics: ["Design reviews and usability tests", "Figma for PMs", "Accessibility basics"] },
      { title: "Communication and stakeholders", topics: ["Writing PRDs", "Stakeholder alignment and trade-offs", "Working with engineering"] },
      { title: "Analytics and metrics", topics: ["North-star and guardrail metrics", "Funnels, cohorts and retention", "A/B testing"] },
      { title: "Launch, growth and monetisation", topics: ["Go-to-market", "Growth loops", "Pricing and packaging"] },
      { title: "Tech and system design for PMs", topics: ["APIs, databases and the cloud", "Scalability trade-offs", "Explaining systems in interviews"] },
      { title: "AI foundations: LLMs and RAG", topics: ["How LLMs work", "Grounding with RAG", "Evaluation, cost and risk"] },
      { title: "Building with AI tools", topics: ["Claude and Claude Code", "Lovable and Figma Make prototypes", "n8n automations"] },
      { title: "Agentic AI and AI product design", topics: ["Agents and tool use", "Guardrails and human-in-the-loop", "Shipping AI features safely"] },
      { title: "Capstone and career", topics: ["Capstone product case study", "Resume and portfolio", "Mock PM interviews"] }
    ],
    projects: ["AI feature PRD with metrics", "Clickable prototype tested with users", "End-to-end capstone case study"],
    tools: ["Claude", "Claude Code", "Figma", "Lovable", "Notion", "n8n", "Mixpanel", "SQL"]
  },
  {
    id: "ai-swe",
    page: "program/ai-software-engineering.html",
    name: "AI-First Software Engineering",
    short: "Build AI-native apps, automate your workflow with coding agents and learn to design systems with LLMs at the core.",
    tagline: "Learn to build, test and ship like an AI-native engineer",
    badge: "Flagship",
    cohort: "", start: "", deadline: "", fee: "", feeNote: "", enroll: "",
    duration: "16 weeks", format: "Live online classes with recordings", effort: "10–12 hours a week",
    for: ["Software engineers with 0–8 years of experience", "Final-year CS students", "Data and QA engineers moving into AI engineering"],
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
      { title: "Capstone and career", topics: ["Build and demo an AI product", "Engineering portfolio", "Mock interviews"] }
    ],
    projects: ["RAG assistant over your own documents", "Agent that uses tools through MCP", "Production-ready capstone app"],
    tools: ["Claude Code", "Claude API", "Python", "TypeScript", "Postgres + pgvector", "GitHub Actions", "Docker"]
  },
  {
    id: "genai-launchpad",
    page: "program/genai-launchpad.html",
    name: "GenAI Launchpad",
    short: "A beginner-friendly program to use generative AI at work: prompting, AI assistants, no-code apps, automations, chatbots and voice agents.",
    tagline: "Go from AI-curious to AI-confident, with no coding needed",
    badge: "Beginner friendly",
    cohort: "", start: "", deadline: "", fee: "", feeNote: "", enroll: "",
    duration: "8 weeks", format: "Live online classes with recordings", effort: "5–6 hours a week",
    for: ["Working professionals in any role", "Founders and small-business owners", "Students who want practical AI skills"],
    outcomes: ["Write prompts that get reliable results", "Use Claude daily for writing, research and analysis",
               "Build a web app without code", "Automate repetitive work with n8n or Zapier",
               "Launch a WhatsApp or website chatbot", "Use AI responsibly and safely"],
    curriculum: [
      { title: "How generative AI works", topics: ["LLMs in plain language", "What AI is good and bad at", "Choosing the right tool"] },
      { title: "Prompting that works", topics: ["Clear instructions and examples", "Roles, formats and constraints", "Checking and improving answers"] },
      { title: "AI assistants for daily work", topics: ["Claude Projects", "Research and analysis", "Docs, emails and presentations"] },
      { title: "No-code apps", topics: ["Lovable from prompt to app", "Databases and login", "Publishing your app"] },
      { title: "Automation", topics: ["Zapier and Make basics", "n8n with AI steps", "Email and sheet workflows"] },
      { title: "Chatbots and voice agents", topics: ["WhatsApp and website bots", "Voice receptionists", "Handoff to humans"] },
      { title: "Responsible AI", topics: ["Privacy and data safety", "Bias and accuracy", "Company AI policies"] },
      { title: "Capstone", topics: ["Solve a real problem with AI", "Demo day", "Certificate"] }
    ],
    projects: ["Personal AI assistant setup", "No-code app for a real use case", "Automation or chatbot capstone"],
    tools: ["Claude", "Lovable", "Zapier", "Make", "n8n", "WhatsApp Business"]
  }
];

/* ---- Career support (shown on the home and program pages) ---------------- */
const SUPPORT = [
  { title: "Resume optimisation", text: "1:1 resume review that shows the right transferable skills." },
  { title: "Build your portfolio", text: "Hands-on assignments and expert help to create case studies and your own product." },
  { title: "Interview preparation", text: "Structured practice questions, expert guidance and mock interviews." },
  { title: "Job referrals", text: "Introductions through our network and community when you're job-ready." }
];

/* ---- FAQs (Programs page). category: Program, Schedule, Fees or Career ---- */
const FAQS = [
  { c: "Program", q: "How is the program delivered?", a: "Through live online classes with instructors, hands-on assignments and a capstone project. All classes are recorded and added to your LMS." },
  { c: "Program", q: "What if I can't attend a live session? Do I get recordings?", a: "Yes. Every live session is recorded and available in your LMS dashboard, so you can catch up any time." },
  { c: "Program", q: "Can I do this alongside a full-time job?", a: "Yes. Classes are scheduled for working professionals, and recordings let you learn at your own pace." },
  { c: "Program", q: "I'm a student or fresher. Can this program help me?", a: "Yes. The programs start from the fundamentals and help you build a portfolio that shows what you can do." },
  { c: "Program", q: "Can I ask instructors and mentors questions directly?", a: "Yes, during live classes and through the LMS, where you can request help and get feedback on your assignments." },
  { c: "Schedule", q: "What are the timings and schedule?", a: "Timings are shared before each cohort starts. Talk to a counsellor for the current schedule." },
  { c: "Fees", q: "What are the fees, and can I pay in instalments?", a: "Fees are listed on each program page when enrolment opens. Talk to a counsellor about payment options." },
  { c: "Career", q: "Do you help with jobs?", a: "We help you get job-ready with resume reviews, portfolio feedback, mock interviews and referrals through our network. No one can honestly guarantee a job." },
  { c: "Career", q: "Will I get a certificate?", a: "Yes, you get a certificate when you complete the program and capstone." },
  { c: "Career", q: "I have more questions. Where can I ask?", a: "Message us on WhatsApp or book a free counselling session, and we'll answer everything." }
];

/* ---- Testimonials (add real quotes, with permission). Hidden while empty.
   { name: "Priya S.", role: "Associate PM, fintech", quote: "...", photo: "" } */
const TESTIMONIALS = [
];
