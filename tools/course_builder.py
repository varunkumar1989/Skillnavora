"""Course: AI Builder Tools for PMs and GenAI learners: Claude, Claude Code, ChatGPT & Codex, Gemini, Lovable and more.
What each tool can do, step-by-step how-tos, and end-to-end builds (website, pages, connecting tools and other websites)."""
from coursekit import ill_flow, ill_stack, ill_quad

COURSE = {
 "slug": "builder-tools", "pdf": "AI_Builder_Tools.pdf", "page": "ai-builder-tools.html",
 "title": "AI Builder Tools: Claude, ChatGPT, Codex, Gemini, Lovable", "kicker": "SkillNavora · AI Product Management & GenAI Launchpad",
 "intro": "What you can do with Claude, Claude Code, ChatGPT and Codex, Gemini, Lovable and other top AI tools, and exactly how: create a website, add pages, connect tools, connect other websites and APIs, publish on your own domain, and run PM workflows end to end.",
 "oneline": "AI builder tools let PMs and non-coders research, write, prototype, build websites and apps, and connect tools together. This course shows what each tool is best at and walks you through real builds step by step.",
 "tutor_q": "How can a product manager build a website with Claude Code or Lovable step by step?",
 "extra_btn": '<a class="btn btn-line" href="tools.html">Tool tutorials &amp; official guides</a>',
 "cheat_title": "Which tool for what",
 "classes": [
  ("basic", "Choosing the right AI tool", "Know the four kinds of AI tools and when to use each.", ill_stack([
      ("AI assistants", "Claude, ChatGPT, Gemini: research, writing, analysis, documents"),
      ("App & website builders", "Lovable, Bolt, v0, Replit: idea to working app in the browser"),
      ("Coding agents", "Claude Code, OpenAI Codex, Cursor, GitHub Copilot: build and change real code"),
      ("Automation & connectors", "Zapier, Make, n8n, MCP: connect tools and websites")], "The AI builder stack") + r"""
<table><tr><th>I want to…</th><th>Start with</th></tr>
<tr><td>Research a market, write a PRD, analyse a spreadsheet</td><td>Claude, ChatGPT or Gemini</td></tr>
<tr><td>Make a clickable prototype or small app fast, no code</td><td>Lovable (or Bolt, v0, Replit)</td></tr>
<tr><td>Build or edit a real website/codebase, deploy it, keep it in GitHub</td><td>Claude Code or OpenAI Codex (or Cursor)</td></tr>
<tr><td>Connect a form to a sheet, email, Slack or CRM</td><td>Zapier, Make or n8n</td></tr>
<tr><td>Let your AI assistant read/write your tools (Drive, Notion, GitHub)</td><td>Connectors and MCP</td></tr>
<tr><td>Ask questions across your own documents</td><td>NotebookLM, Claude/ChatGPT Projects</td></tr></table>
<p class="small">Product menus and plan limits change often; the steps here describe what to look for, and each class links to the official guide.</p>""",
   ["Assistants think and write; builders make apps; coding agents change real code; automation connects tools.", "Pick by the job, not the brand.", "Combine tools in one workflow."],
   "List 5 tasks from your work and choose the tool type for each."),

  ("basic", "Claude for PMs: what you can do and how", "Use Claude's Projects, Artifacts, research, connectors and Skills in daily PM work.", r"""
<table><tr><th>What you can do</th><th>How</th></tr>
<tr><td>Keep a product workspace</td><td>Create a <b>Project</b> → add instructions ("I'm the PM for…; answer concisely") → upload PRDs, research, metrics</td></tr>
<tr><td>Write PRDs, updates, emails</td><td>In the Project, ask with goal, audience and format; attach the brief; ask it to self-check against your template</td></tr>
<tr><td>Make interactive pages, dashboards, mock-ups</td><td>Ask for an <b>Artifact</b>: "Build an interactive pricing calculator as an artifact"; iterate by chatting; share the link</td></tr>
<tr><td>Research with sources</td><td>Turn on web search / research; ask for a cited table; verify key sources</td></tr>
<tr><td>Work with your tools</td><td>Enable <b>connectors</b> (Google Drive, Gmail, Calendar, GitHub, Notion, Slack…) in settings; then ask "Summarise this week's customer emails"</td></tr>
<tr><td>Analyse data</td><td>Upload a CSV/Excel; ask for charts and insights; ask it to show the calculations</td></tr>
<tr><td>Reuse your methods</td><td>Create <b>Skills</b> for PRDs, updates, teardowns (see AI Skills &amp; Templates course)</td></tr></table>
<h3>Starter prompt</h3><pre>You are my product co-pilot for [product]. Users: [who]. Goal this quarter: [metric].
Using the attached interview notes, list the top 5 problems with quotes and frequency,
then draft a 1-page PRD for the biggest one using my PRD template. Mark assumptions.</pre>
<p>More: PM handbook <a href="handbooks/pm/m14.html">Module 14: Claude for daily PM work</a>.</p>""",
   ["Projects hold context; Artifacts make interactive outputs.", "Connectors bring your real data in.", "Skills make your best methods repeatable."],
   "Create a Claude Project for a product you know, add 3 documents, and produce a 1-page PRD and an interactive artifact."),

  ("basic", "ChatGPT for PMs: Projects, GPTs, Canvas, research and agent", "Use ChatGPT's main features for research, documents, data and automation.", r"""
<table><tr><th>What you can do</th><th>How</th></tr>
<tr><td>Organise work</td><td><b>Projects</b>: group chats and files per product, with project instructions</td></tr>
<tr><td>Edit long documents and code side by side</td><td><b>Canvas</b>: ask "open this in canvas", then edit sections, change tone and length</td></tr>
<tr><td>Deep research reports</td><td><b>Deep research</b>: give a clear question and scope; get a cited report; verify sources</td></tr>
<tr><td>Analyse spreadsheets</td><td>Upload files; ask for cleaning, pivots, charts; download results</td></tr>
<tr><td>Build team assistants</td><td><b>Custom GPTs</b>: Explore GPTs → Create → instructions, files, conversation starters → share with your team</td></tr>
<tr><td>Let AI do web tasks</td><td><b>Agent mode</b>: describe the task with allowed sites and stop points (see Browser Automation course)</td></tr>
<tr><td>Voice and images</td><td>Voice conversations for practice; image generation for mock-ups and visuals</td></tr></table>
<h3>Custom GPT recipe: "PRD Reviewer"</h3><ol><li>Create a GPT → Instructions: "Review PRDs against this checklist; score each section; suggest fixes."</li><li>Upload your PRD template and a great example.</li><li>Add conversation starters: "Review my PRD", "What's missing?".</li><li>Test on 3 PRDs, refine, then share with your team.</li></ol>""",
   ["Projects + Canvas for documents; deep research for reports.", "Custom GPTs package team methods.", "Agent mode for web tasks with approvals."],
   "Build a 'PRD Reviewer' custom GPT and test it on two PRDs."),

  ("basic", "Gemini for PMs: Gemini app, Gems, Deep Research, NotebookLM, Workspace, AI Studio", "Use Google's AI tools, especially if your team lives in Google Workspace.", r"""
<table><tr><th>What you can do</th><th>How</th></tr>
<tr><td>Chat, write, analyse</td><td><b>Gemini app</b> (gemini.google.com): upload files, ask for analysis and drafts</td></tr>
<tr><td>Reusable assistants</td><td><b>Gems</b>: create a Gem with instructions (e.g. "Interview synthesiser") and reuse it</td></tr>
<tr><td>Research reports</td><td><b>Deep Research</b>: research plan → cited report → export to Google Docs</td></tr>
<tr><td>AI inside Gmail, Docs, Sheets, Slides, Meet</td><td><b>Gemini in Workspace</b>: side panel to summarise threads, draft docs, build formulas, make slides, meeting notes</td></tr>
<tr><td>Ask across your sources</td><td><b>NotebookLM</b>: add PDFs, Docs, links, videos → ask with citations → audio/video overviews</td></tr>
<tr><td>Prototype with the API</td><td><b>Google AI Studio</b> (aistudio.google.com): test prompts, get an API key, build small apps (SkillNavora's AI uses Gemini this way)</td></tr></table>
<h3>Workflow: user interviews → insights deck</h3><ol><li>Upload interview transcripts to NotebookLM; ask "Top 5 pain points with quotes and counts".</li><li>Paste results into a Gemini chat; ask for a 6-slide outline.</li><li>In Google Slides, use Gemini to draft slides from the outline; edit and add data.</li></ol>""",
   ["Gemini shines inside Google Workspace.", "Gems and NotebookLM make repeatable, source-grounded work.", "AI Studio gives you API keys and prototypes."],
   "Create a Gem for interview synthesis and a NotebookLM notebook with 3 sources; produce an insights summary."),

  ("intermediate", "Lovable: from idea to a working app (no code)", "Build and publish an app with Lovable, including a database, login and your own domain.", ill_flow(["Describe the app", "Generate first version", "Refine screens by chat", "Add backend (Supabase): data & login", "Sync to GitHub", "Publish + custom domain"], "Lovable build flow") + r"""
<h3>Step by step</h3><ol><li>Sign in at lovable.dev → <b>new project</b> → describe the app: users, pages, key actions, style ("A booking app for a Pune yoga studio: home, classes, book a slot, my bookings; calm green style").</li>
<li>Review the first version; ask for changes one at a time ("Add a pricing page with 3 plans", "Make the header sticky").</li>
<li>Connect <b>Supabase</b> for a database and user login; ask Lovable to create the tables (classes, bookings) and sign-up.</li>
<li>Connect <b>GitHub</b> to keep the code (you or a developer can continue in Claude Code or Codex).</li>
<li><b>Publish</b>, then connect a <b>custom domain</b> in project settings and add the DNS records it shows at your domain provider.</li></ol>
<h3>Tips</h3><ul><li>Write a mini-PRD first (pages, data, roles); paste it as the first prompt.</li><li>Use screenshots or Figma links as references.</li><li>Never put secret keys in the front end; use the backend's secure settings.</li></ul>
<p>More: PM handbook <a href="handbooks/pm/m16.html">Module 16: Lovable basic to advanced</a>.</p>""",
   ["Start with a mini-PRD prompt.", "Supabase adds data and login.", "GitHub sync lets you grow beyond the builder."],
   "Build a 3-page app in Lovable with a form that saves data, then publish it."),

  ("intermediate", "Claude Code and OpenAI Codex: coding agents for PMs", "Use coding agents to build and change real websites and apps, safely.", r"""
<table><tr><th></th><th>Claude Code</th><th>OpenAI Codex</th></tr>
<tr><td>What it is</td><td>Anthropic's coding agent: in the terminal, IDEs, desktop and web</td><td>OpenAI's coding agent: CLI, IDE extension and cloud tasks</td></tr>
<tr><td>Good at</td><td>Building features from plain English, editing many files, running tests, git, deploying</td><td>Same jobs; runs tasks in parallel in the cloud and proposes changes</td></tr>
<tr><td>Project memory</td><td><code>CLAUDE.md</code> file with project rules</td><td><code>AGENTS.md</code> file with project rules</td></tr></table>
<h3>Build your first website with a coding agent</h3><pre>1. Install the agent (see official docs) and create an empty folder.
2. Prompt: "Create a fast, mobile-friendly website for [business] with pages:
   Home, About, Services, Pricing, Contact (form). Plain HTML/CSS/JS.
   Use these brand colours … Add SEO titles and a sitemap."
3. Ask: "Run it locally and tell me how to preview it." Open it in the browser.
4. Iterate: "Add a testimonials section", "Make the contact form send to Formspree".
5. "Initialise git and push to a new GitHub repo."
6. Deploy free: connect the repo to Cloudflare Pages or Netlify; every push goes live.</pre>
<h3>Safety habits</h3><ul><li>Work on a branch; review the summary of changes before merging.</li><li>Keep secrets in the host's environment settings, never in code.</li><li>Write project rules (CLAUDE.md / AGENTS.md): how to build, test and deploy.</li></ul>
<p>More: <a href="handbooks/pm/m15.html">PM handbook Module 15: Claude Code</a> and the <a href="data-science/index.html">Claude Code complete tutorial</a> in the Data Science handbook (AI Agents track).</p>""",
   ["Coding agents turn plain English into real code changes.", "Project rules files keep them consistent.", "GitHub + Cloudflare/Netlify = free automatic deploys."],
   "Use Claude Code or Codex to build a 5-page website, push it to GitHub and deploy it."),

  ("intermediate", "Tutorial: create a website, add pages and publish on your domain", "Follow one complete path from idea to a live site you own.", ill_flow(["Plan pages & content", "Generate site", "Add pages & navigation", "Forms & WhatsApp", "Analytics & SEO", "GitHub", "Deploy (Cloudflare/Netlify)", "Custom domain + HTTPS"], "Website build path") + r"""
<ol><li><b>Plan</b>: audience, goal (leads? bookings?), pages, one call to action; collect logo, colours, photos, text.</li>
<li><b>Generate</b>: Lovable (no code) or Claude Code/Codex (code you own). Paste your plan as the first prompt.</li>
<li><b>Add pages</b>: "Add a Blog page with 3 sample posts and link it in the menu"; check mobile view.</li>
<li><b>Forms</b>: contact form to email/Sheet (Formspree, Google Forms embed, or your backend); WhatsApp chat button with your number link.</li>
<li><b>Analytics &amp; SEO</b>: Google Analytics 4 or Microsoft Clarity; page titles, descriptions, sitemap; submit to Google Search Console.</li>
<li><b>GitHub</b>: keep the code in a repository.</li><li><b>Deploy</b>: connect the repo to Cloudflare Pages or Netlify (free tiers).</li>
<li><b>Domain</b>: buy a domain (GoDaddy, Hostinger, Cloudflare Registrar); add it in your host's "custom domains"; copy the DNS records; HTTPS turns on automatically.</li></ol>
<p>This is exactly how skillnavora.in is built: code in GitHub, Claude Code for changes, deployed on Cloudflare Pages.</p>""",
   ["Plan before you prompt.", "Own your code in GitHub.", "Free hosting + your domain + HTTPS in under an hour."],
   "Publish a 4-page website on your own domain with a working contact form and analytics."),

  ("intermediate", "Connect your tools: Zapier, Make, n8n, webhooks and MCP", "Make your website and tools talk to each other.", ill_flow(["Trigger: form submitted", "Add row to Google Sheet", "AI step: summarise / classify", "Notify Slack / WhatsApp / email", "Create CRM lead"], "Example automation") + r"""
<table><tr><th>Tool</th><th>Best for</th></tr><tr><td>Zapier</td><td>Easiest; thousands of app connections</td></tr><tr><td>Make</td><td>Visual, flexible scenarios, good value</td></tr><tr><td>n8n</td><td>Powerful, self-hostable, strong AI nodes</td></tr><tr><td>Webhooks</td><td>Any app that can send or receive an HTTP request</td></tr><tr><td>MCP / connectors</td><td>Let Claude or ChatGPT read and act in your tools from chat</td></tr></table>
<h3>Recipe: website lead → Sheet → AI summary → Slack</h3><ol><li>In Zapier/Make/n8n, choose a trigger: "New form submission" (Typeform, Google Forms, Webflow) or a <b>webhook</b> your site posts to.</li><li>Action: add a row to Google Sheets.</li><li>AI step: "Classify this lead as Hot/Warm/Cold and write a 2-line summary."</li><li>Action: post to Slack; if Hot, also email sales.</li><li>Test with 3 sample leads; turn it on; check the run history weekly.</li></ol>
<p>More: <a href="handbooks/pm/m20.html">PM handbook Module 20: Zapier, Make and n8n</a> and the n8n complete tutorial in the Data Science handbook.</p>""",
   ["Trigger → actions → AI step → notify.", "Webhooks connect anything that speaks HTTP.", "MCP lets AI assistants use your tools."],
   "Build the lead automation above with a test form."),

  ("advanced", "Connect other websites and services", "Embed, integrate and call other websites safely.", r"""
<table><tr><th>Goal</th><th>How</th></tr>
<tr><td>Show a video, map, calendar or form</td><td><b>Embed</b>: YouTube, Google Maps, Calendly, Google Forms give an embed code (iframe) to paste into a page</td></tr>
<tr><td>Take payments</td><td>Payment links or checkout from Razorpay, Stripe or Cashfree; webhooks confirm payment to your system</td></tr>
<tr><td>Login with Google / email</td><td>Auth from Supabase, Firebase or Clerk</td></tr>
<tr><td>Show data from another service</td><td>Call its <b>API</b> from your backend or an automation; cache results</td></tr>
<tr><td>Send emails/WhatsApp</td><td>Email APIs (Resend, SendGrid) or WhatsApp Business API providers</td></tr>
<tr><td>Let AI use your site's data</td><td>Expose an API or MCP server with read-only access first</td></tr></table>
<h3>Rules for connecting safely</h3><ul><li>API keys and secrets only in server/host settings, never in the browser.</li><li>Use test mode for payments first; verify webhooks.</li><li>Respect terms of use and privacy (DPDP); ask consent before collecting personal data.</li><li>Prefer official APIs over scraping.</li></ul>""",
   ["Embeds for content; APIs for data; webhooks for events.", "Secrets stay on the server.", "Test mode before real money."],
   "Add a Calendly embed and a Razorpay test payment link to your site."),

  ("advanced", "PM workflows end to end and capstone", "Combine tools into a real product workflow.", ill_flow(["Research (Gemini/ChatGPT deep research)", "Synthesis (NotebookLM / Claude Project)", "PRD (Claude Skill / PRD Writer)", "Prototype (Lovable)", "Build & deploy (Claude Code / Codex)", "Connect (Zapier / n8n)", "Measure (analytics + evals)"], "AI-powered product workflow") + r"""
<h3>Capstone</h3><p>Pick a real problem (for example a booking app for a local business). Deliver:</p><ol><li>Research summary with sources.</li><li>PRD (with metrics and evals).</li><li>Lovable prototype tested with 3 users.</li><li>A live website or app on your own domain built with Claude Code or Codex.</li><li>One automation (lead → Sheet → Slack).</li><li>A 5-minute demo: what each AI tool did, time saved, what you'd improve.</li></ol>
<h3>Cost and safety checklist</h3><ul><li>Free tiers first; set spending limits on paid plans and API keys.</li><li>Don't paste confidential company data into personal accounts.</li><li>Review AI output before publishing; keep humans approving sends and payments.</li></ul>""",
   ["Each tool has a role in the workflow.", "Ship something real and measurable.", "Control cost and data from day one."],
   "Complete the capstone and record a 5-minute demo."),
 ],
 "templates_html": """<h3>A. Website plan (paste as your first prompt)</h3><pre>Business / product:
Audience:
Goal & main call to action:
Pages (with 1-line purpose each):
Brand (colours, fonts, tone), logo link:
Forms & integrations (email, Sheet, WhatsApp, payments, booking):
Must-have: mobile-friendly, fast, SEO titles, analytics</pre>
<h3>B. Tool chooser</h3><table><tr><th>Task</th><th>Tool</th><th>Why</th></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr></table>
<h3>C. Launch checklist</h3><pre>[ ] All pages load on mobile   [ ] Forms tested   [ ] Analytics on   [ ] Titles & sitemap
[ ] Custom domain + HTTPS     [ ] Secrets not in code   [ ] Privacy policy   [ ] Backup in GitHub</pre>""",
 "cheat": [("Claude", "Projects, Artifacts, research, connectors, Skills, data analysis"), ("Claude Code", "Coding agent: build/edit sites and apps, git, deploy"), ("ChatGPT", "Projects, Canvas, deep research, custom GPTs, agent mode, data analysis"),
           ("OpenAI Codex", "Coding agent: CLI, IDE and cloud tasks"), ("Gemini", "Gemini app, Gems, Deep Research, Workspace side panel"), ("NotebookLM", "Answers from your sources with citations; audio overviews"),
           ("Google AI Studio", "Prompt testing, API keys, quick AI apps"), ("Lovable", "No-code apps: Supabase data/login, GitHub sync, publish + domain"), ("Bolt / v0 / Replit", "Other app builders in the browser"),
           ("Cursor / GitHub Copilot", "AI inside code editors"), ("Zapier / Make / n8n", "Automations between apps"), ("Cloudflare Pages / Netlify", "Free hosting from GitHub with custom domains")],
 "qa": [("Which AI tool would you use to prototype an app quickly?", "A no-code builder like Lovable (or Bolt/v0/Replit) for a clickable, working prototype; then move to a coding agent for production."),
        ("Claude Code vs Lovable?", "Lovable is a no-code app builder in the browser; Claude Code is a coding agent that edits real code in your repo, runs commands and deploys, giving full ownership and flexibility."),
        ("How would you build a website as a PM?", "Plan pages and CTA, generate with Lovable or a coding agent, add pages and forms, analytics and SEO, push to GitHub, deploy on Cloudflare Pages/Netlify, connect a custom domain."),
        ("How do you connect a website form to your tools?", "Use an automation (Zapier/Make/n8n) or a webhook: form → Sheet → AI summary → Slack/CRM."),
        ("What are Custom GPTs and Gems?", "Reusable assistants with your instructions and files in ChatGPT (GPTs) and Gemini (Gems)."),
        ("How do you keep API keys safe?", "Store them only in server or hosting secret settings, never in front-end code or prompts; use limits and rotate keys."),
        ("When use NotebookLM?", "When answers must come from your own sources with citations: research, study, interview synthesis."),
        ("How do PMs use coding agents responsibly?", "Branches and reviews, project rules files, tests, no secrets in code, and human approval before merging and deploying.")],
 "glossary": [("Artifact", "Interactive output (page, app, chart) created in Claude"), ("Canvas", "ChatGPT's side-by-side editor"), ("Gem", "Custom Gemini assistant"), ("Custom GPT", "Custom ChatGPT assistant"),
              ("CLAUDE.md / AGENTS.md", "Project rules files for coding agents"), ("DNS", "Settings that point your domain to your host"), ("Webhook", "Automatic HTTP message when an event happens"), ("Embed", "Code that shows another site's content in your page")],
 "links": [("Claude help center", "https://support.anthropic.com/"), ("Claude Code docs", "https://docs.claude.com/en/docs/claude-code/overview"), ("ChatGPT help", "https://help.openai.com/"),
           ("OpenAI Codex docs", "https://developers.openai.com/codex"), ("Gemini help", "https://support.google.com/gemini"), ("Google AI Studio", "https://aistudio.google.com/"), ("NotebookLM help", "https://support.google.com/notebooklm"),
           ("Lovable docs", "https://docs.lovable.dev/"), ("Replit docs", "https://docs.replit.com/"), ("v0 docs", "https://vercel.com/docs/v0"), ("Cursor docs", "https://docs.cursor.com/"),
           ("Cloudflare Pages docs", "https://developers.cloudflare.com/pages/"), ("Netlify docs", "https://docs.netlify.com/"), ("Zapier Learn", "https://learn.zapier.com/"), ("n8n docs", "https://docs.n8n.io/"),
           ("Razorpay docs", "https://razorpay.com/docs/"), ("Calendly embed help", "https://help.calendly.com/"), ("Google Search Console", "https://search.google.com/search-console")],
}
