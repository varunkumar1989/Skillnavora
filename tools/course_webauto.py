"""Course: Web Automation: Webhooks, Triggers, Browser Automation & Playwright MCP (plus every major web-automation platform)."""
from coursekit import ill_flow, ill_stack, ill_quad, ill_cycle

COURSE = {
 "slug": "web-automation", "pdf": "Web_Automation_Webhooks_Triggers_Playwright_MCP.pdf", "page": "web-automation.html",
 "title": "Web Automation: Webhooks, Triggers & Playwright MCP", "kicker": "SkillNavora · AI Product Management & GenAI Launchpad · AI tools",
 "intro": "The modern web-automation stack in one course: webhooks, triggers (schedules, events, polling), browser automation with Playwright, the Playwright MCP that lets Claude and other AI assistants drive a real browser, and every major alternative: Selenium, Puppeteer, Cypress, Chrome DevTools MCP, Browser Use, Stagehand, Skyvern, Browserbase, Apify, n8n, Zapier, Make, Pipedream, RPA and AI browsers.",
 "oneline": "Webhooks tell your system the moment something happens; triggers decide when automations run; browser automation does the clicking when there's no API; and the Playwright MCP lets an AI assistant like Claude use a real browser for you. Together they're the most-used web automation stack in 2026.",
 "tutor_q": "Explain webhooks, triggers and the Playwright MCP with a simple example",
 "extra_btn": '<a class="btn btn-line" href="ai-builder-tools.html">AI Builder Tools course</a>',
 "cheat_title": "Platform cheat sheet",
 "classes": [
  ("basic", "The web-automation stack: APIs, webhooks, triggers, browsers", "See how the pieces fit, and pick the right one for each job.", ill_stack([
      ("Triggers", "when to run: schedule, event, webhook, polling, manual"),
      ("Webhooks & APIs", "systems talking directly: fastest and most reliable"),
      ("Workflow tools", "n8n, Zapier, Make, Pipedream connect the steps"),
      ("Browser automation", "Playwright, Selenium, Puppeteer: no API needed"),
      ("AI agents & MCP", "Playwright MCP, Browser Use: AI drives the browser")], "The web automation stack") + r"""
<table><tr><th>Situation</th><th>Use</th></tr>
<tr><td>Another app should tell you instantly when something happens (payment, form, new order)</td><td><b>Webhook</b></td></tr>
<tr><td>You need data or actions from a service that has an API</td><td><b>API call</b></td></tr>
<tr><td>Something should run every hour / day / Monday</td><td><b>Scheduled trigger</b> (cron)</td></tr>
<tr><td>A website has no API and you must click through it</td><td><b>Browser automation</b> (Playwright)</td></tr>
<tr><td>You want an AI assistant to research or test websites for you</td><td><b>Playwright MCP</b> or an AI browser agent</td></tr></table>
<div class="box"><b>Golden rule:</b> webhook or API first; browser automation only when there's no API; AI agents for messy, changing tasks; humans approve anything irreversible.</div>""",
   ["Triggers decide when; webhooks and APIs connect systems; browsers click when nothing else works.", "Prefer APIs and webhooks for reliability.", "AI agents sit on top for flexible tasks."],
   "Map 5 tasks from your work to webhook, API, schedule, browser automation or AI agent."),

  ("basic", "Webhooks explained (with real examples)", "Understand webhooks and receive your first one.", ill_flow(["Event happens (payment captured)", "Provider sends HTTP POST with JSON", "Your endpoint verifies signature", "Your system updates (order paid)", "Reply 200 OK fast"], "How a webhook works") + r"""
<p>A <b>webhook</b> is an automatic message one app sends to a URL you give it when an event happens. Instead of asking "any new payments?" every minute (polling), the provider <i>pushes</i> the news to you instantly.</p>
<h3>Common webhooks</h3><table><tr><th>Provider</th><th>Example events</th></tr>
<tr><td>Razorpay / Stripe</td><td>payment.captured, refund.processed, subscription.charged</td></tr><tr><td>GitHub</td><td>push, pull_request, issues</td></tr><tr><td>Typeform / Google Forms (via tools)</td><td>new response</td></tr>
<tr><td>Shopify / WooCommerce</td><td>orders/create, orders/paid</td></tr><tr><td>Slack / WhatsApp Business</td><td>message received</td></tr><tr><td>Calendly</td><td>invitee.created</td></tr></table>
<h3>Example payload</h3><pre>POST https://yourapp.com/webhooks/razorpay
{ "event": "payment.captured",
  "payload": { "payment": { "entity": { "id": "pay_29QQoUBi66xm2f", "amount": 49900,
     "currency": "INR", "email": "riya@example.com", "status": "captured" } } } }</pre>
<h3>Try it in 5 minutes (no code)</h3><ol><li>Open a free webhook tester (e.g. webhook.site) and copy your unique URL.</li><li>Paste it as the webhook URL in a test tool (a form tool, GitHub repo settings → Webhooks, or Razorpay test mode).</li><li>Trigger the event (submit the form, push a commit) and watch the request arrive with its headers and JSON.</li></ol>""",
   ["Webhooks push events to you in real time.", "The body is usually JSON describing the event.", "Test with a webhook inspector before writing code."],
   "Receive a real webhook from GitHub or a form tool in a webhook tester and identify the event name and key fields."),

  ("intermediate", "Building reliable webhook receivers", "Verify, process and retry webhooks safely in production.", r"""
<h3>Six rules for production webhooks</h3><ol><li><b>Verify the signature</b> (HMAC) so only the real provider can call you.</li><li><b>Respond fast</b> (200 OK within a few seconds); do heavy work in a queue.</li>
<li><b>Be idempotent</b>: providers retry, so the same event may arrive twice; store event IDs and skip duplicates.</li><li><b>Handle retries and order</b>: events can arrive late or out of order; check current state.</li>
<li><b>Log everything</b>: raw payload, headers, result; keep a replay option.</li><li><b>Secrets in environment settings</b>, never in code.</li></ol>
<h3>Signature check (Node.js / Cloudflare-style function)</h3><pre>import crypto from "node:crypto";
export async function onRequestPost({ request, env }) {
  const body = await request.text();                       // raw body, before JSON parsing
  const sig = request.headers.get("x-razorpay-signature") || "";
  const expected = crypto.createHmac("sha256", env.RAZORPAY_WEBHOOK_SECRET).update(body).digest("hex");
  if (sig.length !== expected.length ||
      !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected)))
    return new Response("invalid signature", { status: 401 });
  const event = JSON.parse(body);
  // idempotency: skip if this event id was already processed (check your DB/KV)
  // enqueue the work, then reply quickly
  return new Response("ok");
}</pre>
<p class="small">Each provider documents its own header name and signing method; follow its official guide.</p>
<h3>Local testing</h3><p>Expose your laptop with a tunnel (ngrok, Cloudflare Tunnel) or use the provider's CLI to forward test events; replay saved payloads in tests.</p>""",
   ["Verify signatures, respond fast, be idempotent.", "Expect retries and out-of-order events.", "Log and replay for debugging."],
   "Write the requirements (or code) for a webhook receiver that marks orders paid, including signature, idempotency and logging."),

  ("basic", "Triggers: schedules, events, polling and manual", "Choose how and when automations start.", ill_quad("Speed of reaction", "Cost & complexity", ["Polling: simple, delayed", "Webhook / event: instant", "Schedule (cron): predictable batches", "Manual / button: human-started"], "Trigger types") + r"""
<table><tr><th>Trigger</th><th>Example</th><th>Where</th></tr>
<tr><td>Schedule (cron)</td><td>Every day 9:00 IST: download sales report</td><td>n8n Schedule, Zapier Schedule, Make scheduling, GitHub Actions cron, Cloudflare Cron Triggers</td></tr>
<tr><td>Webhook / event</td><td>New payment → send receipt on WhatsApp</td><td>Any webhook trigger node</td></tr>
<tr><td>Polling</td><td>Every 15 min check a Google Sheet for new rows</td><td>Most "new row/new email" app triggers</td></tr>
<tr><td>App event</td><td>New Gmail with label "lead"</td><td>Zapier/Make/n8n app triggers</td></tr>
<tr><td>File / folder</td><td>New CSV in Drive → import</td><td>Drive/Dropbox triggers</td></tr>
<tr><td>Manual / chat</td><td>Button in Slack or a form; "run now"</td><td>Slack commands, forms, chat triggers</td></tr></table>
<h3>Cron in one minute</h3><pre>minute hour day-of-month month day-of-week
0 9 * * 1-5        → 09:00 every weekday
*/15 * * * *       → every 15 minutes
30 18 1 * *        → 18:30 on the 1st of every month
Note: many servers use UTC; 09:00 IST = 03:30 UTC.</pre>""",
   ["Webhooks for instant, schedules for batches, polling when nothing else exists.", "Watch time zones in cron (IST vs UTC).", "Add manual triggers for testing."],
   "Write cron expressions for 3 schedules you need, in IST and UTC."),

  ("intermediate", "Playwright for browser automation", "Automate any website reliably with Playwright.", r"""
<p><b>Playwright</b> (by Microsoft) controls Chromium, Firefox and WebKit from Python, JavaScript/TypeScript, Java or .NET. It auto-waits for elements, records your clicks as code and replays failures step by step.</p>
<h3>Setup and record</h3><pre>pip install playwright && playwright install chromium
playwright codegen https://demo.playwright.dev/todomvc/     # click around; code is written for you</pre>
<h3>Script: log in, export a report (pattern)</h3><pre>from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(storage_state="auth.json")   # reuse a saved, authorised login
    page = ctx.new_page()
    page.goto("https://portal.example.com/reports")
    page.get_by_label("From").fill("2026-10-01")
    page.get_by_role("button", name="Export CSV").click()
    with page.expect_download() as d:
        page.get_by_role("link", name="Download").click()
    d.value.save_as("report.csv")
    browser.close()</pre>
<h3>Make it robust</h3><ul><li>Locate by role, label, text or test id, not fragile CSS paths.</li><li>Use <code>storage_state</code> for logins (store securely; never commit it).</li><li>Turn on tracing; open failures in the trace viewer.</li><li>Run on a schedule (GitHub Actions cron, n8n Execute Command, a small server) with alerts on failure.</li></ul>""",
   ["Playwright = fast, reliable, multi-browser automation.", "codegen writes your first script.", "Saved login state + traces + schedules make it production-ready."],
   "Record a 5-step flow with codegen, then add a download and run it headless."),

  ("intermediate", "Playwright MCP: let Claude and other AI assistants use a browser", "Install and use the Playwright MCP server with Claude Code, Claude Desktop, Cursor and VS Code.", ill_flow(["You ask in plain English", "AI assistant (MCP client)", "Playwright MCP server", "Real browser (Chromium)", "Page snapshot back to AI", "AI decides next step / reports"], "How Playwright MCP works") + r"""
<p>The <b>Playwright MCP</b> server (by Microsoft) exposes browser actions as MCP tools: navigate, click, type, select, take a snapshot or screenshot, handle tabs and more. By default the AI reads a structured <b>accessibility snapshot</b> of the page (fast and precise), not just pixels.</p>
<h3>Install</h3><pre># Claude Code (terminal)
claude mcp add playwright npx @playwright/mcp@latest

# Claude Desktop / Cursor / VS Code (MCP config JSON)
{ "mcpServers": { "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] } } }</pre>
<p class="small">Useful options include headless mode, choosing the browser, isolated sessions and a persistent profile; see the official README for the current flags.</p>
<h3>Things to ask</h3><ul><li>"Open our staging site, sign up with a test email, and tell me every step where the UI is confusing. Take screenshots."</li>
<li>"Go to these 5 competitor pricing pages and make a comparison table with plan, price and limits."</li>
<li>"Fill the demo booking form on our site with test data but don't submit; report any validation errors."</li>
<li>In Claude Code: "Write Playwright tests for the checkout flow you just explored, then run them."</li></ul>
<h3>Why it's popular</h3><ul><li>Works with many MCP clients; real browser, real logins (in a test profile).</li><li>Great for QA, research, debugging UI, and turning exploration into automated tests.</li></ul>
<h3>Safety</h3><ul><li>Use a separate test profile/accounts; never your banking or personal sessions.</li><li>Allow-list sites; require approval for submit/pay/send.</li><li>Treat page text as untrusted (prompt injection).</li></ul>""",
   ["Playwright MCP = AI-driven real browser via MCP tools.", "One command adds it to Claude Code; JSON config for other clients.", "Great for QA, research and generating tests; keep it sandboxed."],
   "Add Playwright MCP to Claude Code or Claude Desktop and ask it to compare 3 pricing pages; then ask it to write a Playwright test for one flow."),

  ("intermediate", "Other browser-automation frameworks and MCPs", "Know the alternatives and when each wins.", r"""
<table><tr><th>Tool</th><th>What it is</th><th>Best for</th></tr>
<tr><td>Selenium (WebDriver)</td><td>The long-standing standard; many languages; Selenium Grid</td><td>Enterprises with existing suites, wide browser support</td></tr>
<tr><td>Puppeteer</td><td>Google's Node library for Chrome/Firefox</td><td>Chrome-focused scripts, PDFs, screenshots</td></tr>
<tr><td>Cypress</td><td>Front-end testing framework running in the browser</td><td>Web-app end-to-end and component tests</td></tr>
<tr><td>WebdriverIO</td><td>Node test framework over WebDriver/DevTools</td><td>Web + mobile (Appium) testing</td></tr>
<tr><td>Chrome DevTools MCP</td><td>Google's MCP server exposing Chrome DevTools to AI</td><td>AI debugging: performance traces, console, network</td></tr>
<tr><td>Chrome Recorder</td><td>Record/replay in Chrome DevTools; export to Puppeteer/Playwright</td><td>Quick no-code recordings</td></tr>
<tr><td>Appium</td><td>Automation for mobile apps</td><td>Android/iOS app testing</td></tr></table>
<p><b>Choosing:</b> new projects usually pick Playwright (speed, auto-wait, multi-browser, MCP); keep Selenium where it already runs; Cypress if your front-end team prefers it; DevTools MCP when debugging performance with AI.</p>""",
   ["Playwright is the default for new work.", "Selenium remains common in enterprises.", "Pick by team skills and browsers needed."],
   "Compare Playwright, Selenium and Cypress for a QA plan of your product's sign-up flow."),

  ("advanced", "AI browser agents and cloud browsers", "Use AI-native automation tools and hosted browsers at scale.", r"""
<table><tr><th>Tool</th><th>What it does</th></tr>
<tr><td>Browser Use (open source)</td><td>Python library: give an LLM a goal; it plans and drives a browser</td></tr>
<tr><td>Stagehand (by Browserbase)</td><td>Playwright plus AI actions (act, extract, observe) in plain English inside code</td></tr>
<tr><td>Skyvern</td><td>AI agent for form-heavy workflows using vision + DOM</td></tr>
<tr><td>Browserbase, Browserless, Steel</td><td>Cloud browser infrastructure: run many headless browsers, sessions, proxies, recordings</td></tr>
<tr><td>Claude in Chrome / computer use</td><td>Claude operating your browser or a computer with permission</td></tr>
<tr><td>ChatGPT agent mode</td><td>OpenAI's agent completing web tasks in a virtual browser</td></tr>
<tr><td>Perplexity Comet and other AI browsers</td><td>Browsers with built-in assistants that act on pages</td></tr></table>
<h3>Pattern: AI where needed, code where possible</h3><p class="flow">Playwright script for stable steps → AI action (Stagehand/Browser Use) for the messy page → validation → human approval → save results</p>
<p>Measure success rate, cost per task and safety (see Evals and Browser Automation courses).</p>""",
   ["AI agents handle changing pages; code handles stable steps.", "Cloud browsers scale and isolate sessions.", "Always measure reliability and cost."],
   "Design a hybrid workflow (script + AI step) for collecting prices from 10 sites."),

  ("advanced", "Workflow platforms: n8n, Zapier, Make, Pipedream, RPA and scrapers", "Run webhooks, triggers and browser steps as complete workflows.", r"""
<table><tr><th>Platform</th><th>Strengths</th></tr>
<tr><td>n8n</td><td>Webhook and schedule triggers, AI agent nodes, code nodes, self-hostable; can call Playwright scripts or browser services</td></tr>
<tr><td>Zapier</td><td>Easiest; "Webhooks by Zapier" catch and send hooks; huge app library</td></tr>
<tr><td>Make</td><td>Visual scenarios, custom webhooks, good value</td></tr>
<tr><td>Pipedream</td><td>Developer-friendly: webhook triggers + code steps (Node/Python)</td></tr>
<tr><td>IFTTT</td><td>Simple personal automations</td></tr>
<tr><td>Apify</td><td>Ready "Actors" for scraping and browser automation, schedules, datasets, API</td></tr>
<tr><td>Bardeen, Axiom</td><td>Browser-extension automation for repetitive web tasks</td></tr>
<tr><td>UiPath, Power Automate, Automation Anywhere</td><td>Enterprise RPA for desktop + web with governance</td></tr></table>
<h3>Example: payment webhook → n8n → browser step → WhatsApp</h3><ol><li>Webhook node receives Razorpay <code>payment.captured</code> (verify signature).</li><li>Look up the order in Google Sheets/DB.</li><li>If the partner portal has no API, call a Playwright script (or Apify actor) to register the booking.</li><li>Send a WhatsApp/email confirmation; log the run; alert on failure.</li></ol>""",
   ["n8n/Zapier/Make/Pipedream orchestrate triggers and actions.", "Apify and RPA tools cover scraping and enterprise desktop work.", "Combine webhook + workflow + browser step + notification."],
   "Build the payment-to-confirmation workflow in n8n or Make with a test webhook."),

  ("advanced", "Production: security, legality, monitoring, evals and capstone", "Run web automations safely and prove they work.", ill_cycle(["Design with approvals", "Run in sandbox", "Monitor & alert", "Evaluate & improve"], "Production loop") + r"""
<h3>Checklist</h3><ul><li>Secrets in environment settings; rotate keys; least-privilege accounts.</li><li>Respect site terms and robots.txt, rate-limit, never bypass CAPTCHAs; prefer APIs; follow the DPDP Act for personal data.</li>
<li>Approvals before submit/pay/send/delete; allow-listed sites for AI agents.</li><li>Monitoring: success rate, duration, cost, failures with screenshots/traces; alerts to Slack/email.</li><li>Evals: 20–50 test tasks with known end states; run after changes (see AI Evals course).</li></ul>
<h3>Capstone</h3><p>Build a "competitor & order watch": (1) a webhook receiver for test payments with signature check and idempotency, (2) a daily cron workflow in n8n, (3) a Playwright script that collects 3 competitor prices, (4) a Playwright MCP session in Claude that explores your own site and writes one automated test, (5) alerts and a run log, (6) a 1-page PRD with an approval matrix. Demo in 5 minutes.</p>""",
   ["Secure, legal, approved, monitored, evaluated.", "Every failure leaves a trace and an alert.", "Ship a capstone you can demo in interviews."],
   "Complete the capstone and present it."),
 ],
 "templates_html": """<h3>A. Webhook spec</h3><table><tr><th>Field</th><th>Fill in</th></tr><tr><td>Provider & events</td><td></td></tr><tr><td>Endpoint URL</td><td></td></tr><tr><td>Signature method & secret name</td><td></td></tr><tr><td>Idempotency key</td><td></td></tr><tr><td>Processing (queue?)</td><td></td></tr><tr><td>Retries & dead-letter</td><td></td></tr><tr><td>Logging & alerts</td><td></td></tr></table>
<h3>B. Trigger plan</h3><pre>workflow | trigger type | schedule/event | time zone | owner | failure alert</pre>
<h3>C. Playwright MCP session brief</h3><pre>Goal:
Sites allowed:
Test account / profile:
Do NOT: submit / pay / send / delete
Output: table / findings / screenshots / generated test file</pre>""",
 "cheat": [("Webhook", "Event pushed to your URL in real time"), ("Trigger", "What starts an automation: schedule, event, polling, manual"), ("Cron", "Schedule syntax: minute hour day month weekday"),
           ("Playwright", "Modern browser automation & testing (Microsoft)"), ("Playwright MCP", "MCP server so AI assistants drive a real browser"), ("Chrome DevTools MCP", "AI access to Chrome DevTools for debugging"),
           ("Selenium", "Long-standing WebDriver standard"), ("Puppeteer", "Chrome automation for Node"), ("Cypress", "Front-end end-to-end testing"),
           ("Browser Use / Stagehand / Skyvern", "AI-native browser automation"), ("Browserbase / Browserless / Steel", "Cloud browsers at scale"), ("Apify", "Scraping & automation Actors"),
           ("n8n / Zapier / Make / Pipedream", "Workflow platforms with webhook & schedule triggers"), ("UiPath / Power Automate", "Enterprise RPA")],
 "qa": [("What is a webhook?", "An HTTP request an app sends to your URL when an event happens, so you get updates instantly instead of polling."),
        ("How do you secure a webhook endpoint?", "Verify the provider's HMAC signature on the raw body, use HTTPS, keep the secret in environment settings, respond fast, and process idempotently."),
        ("Webhook vs polling?", "Webhooks push instantly and save calls; polling checks repeatedly and adds delay but works when no webhooks exist."),
        ("What is idempotency and why does it matter?", "Processing the same event twice has no extra effect; needed because providers retry and may send duplicates."),
        ("What is the Playwright MCP?", "An MCP server by Microsoft that exposes browser actions (navigate, click, type, snapshot) so AI assistants like Claude can use a real browser."),
        ("Playwright vs Selenium?", "Playwright: newer, faster, auto-waiting, multi-browser, great tooling and MCP. Selenium: mature standard with broad language and grid support, common in existing enterprise suites."),
        ("When would you use an AI browser agent instead of a script?", "When pages change often or tasks vary; keep scripts for stable steps and add AI for the messy parts, with evals and approvals."),
        ("How do you schedule an automation for 9 am IST on weekdays?", "Cron '0 9 * * 1-5' in IST, or '30 3 * * 1-5' if the server runs in UTC."),
        ("What risks come with browser automation?", "Breaking on UI changes, terms-of-service and legal issues, credential leaks, prompt injection for AI agents, and irreversible actions; mitigate with APIs, sandboxes, approvals and monitoring."),
        ("Give a PM use case for Playwright MCP.", "Ask Claude to walk the onboarding flow on staging, list UX issues with screenshots, then generate Playwright tests for the happy path.")],
 "glossary": [("HMAC", "Signature proving a message came from the sender"), ("Payload", "The data sent in a request"), ("Endpoint", "URL that receives requests"), ("Idempotency", "Same request twice = same result"),
              ("Headless", "Browser without a visible window"), ("Accessibility snapshot", "Structured view of a page's elements used by Playwright MCP"), ("Tunnel", "Exposes a local server to the internet for testing")],
 "links": [("Playwright docs", "https://playwright.dev/docs/intro"), ("Playwright MCP (GitHub)", "https://github.com/microsoft/playwright-mcp"), ("Chrome DevTools MCP (GitHub)", "https://github.com/ChromeDevTools/chrome-devtools-mcp"),
           ("Selenium docs", "https://www.selenium.dev/documentation/"), ("Puppeteer docs", "https://pptr.dev/"), ("Cypress docs", "https://docs.cypress.io/"), ("Browser Use", "https://github.com/browser-use/browser-use"),
           ("Stagehand", "https://www.stagehand.dev/"), ("Skyvern", "https://www.skyvern.com/"), ("Browserbase", "https://www.browserbase.com/"), ("Apify docs", "https://docs.apify.com/"),
           ("n8n webhook node", "https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/"), ("Zapier webhooks", "https://zapier.com/apps/webhook/integrations"), ("Pipedream docs", "https://pipedream.com/docs"),
           ("Razorpay webhooks", "https://razorpay.com/docs/webhooks/"), ("GitHub webhooks", "https://docs.github.com/en/webhooks"), ("Crontab guru (cron helper)", "https://crontab.guru/"), ("Model Context Protocol", "https://modelcontextprotocol.io/")],
}
