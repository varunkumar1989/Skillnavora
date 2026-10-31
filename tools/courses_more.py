"""Eight more AI-PM courses (gap fill): strategy, AI UX, pricing, ML products, governance, platforms/APIs, product ops, multimodal."""
from coursekit import ill_flow, ill_cycle, ill_quad, ill_stack

def C(slug, pdf, page, title, intro, oneline, tutor_q, classes, cheat, qa, glossary, links, templates):
    return {"slug": slug, "pdf": pdf, "page": page, "title": title, "kicker": "SkillNavora · AI Product Management & GenAI Launchpad",
            "intro": intro, "oneline": oneline, "tutor_q": tutor_q, "extra_btn": '<a class="btn btn-line" href="ai-academy.html">All AI Skills Academy courses</a>',
            "cheat_title": "Cheat sheet", "classes": classes, "cheat": cheat, "qa": qa, "glossary": glossary, "links": links, "templates_html": templates}

TPL_CANVAS = lambda rows: '<table><tr><th>Field</th><th>Fill in</th></tr>' + "".join(f"<tr><td>{r}</td><td></td></tr>" for r in rows) + "</table>"

STRATEGY = C("ai-strategy", "AI_Product_Strategy.pdf", "ai-product-strategy.html", "AI Product Strategy",
 "Decide where AI creates real value: AI-first vs AI-added products, moats and data flywheels, build vs buy vs partner, model choice, opportunity assessment and AI roadmaps.",
 "AI product strategy is deciding which problems AI should solve for your users and business, how you'll win (data, distribution, workflow, trust), and what to build, buy or partner for, before writing a single PRD.",
 "How should a PM decide where to use AI in a product?",
 [("basic", "Where AI creates value", "Separate real AI opportunities from hype.", ill_quad("Feasibility with today's AI", "User & business value", ["Quick wins: ship now", "Big bets: invest + research", "Avoid: low value, hard", "Nice-to-have: low priority"], "AI opportunity matrix") + r"""
<h3>AI-first vs AI-added</h3><table><tr><th>AI-added</th><th>AI-first</th></tr><tr><td>AI improves an existing workflow (summaries in a CRM, smart replies)</td><td>The product only exists because of AI (AI tutor, coding agent, voice receptionist)</td></tr><tr><td>Lower risk, faster</td><td>Bigger upside, more uncertainty</td></tr></table>
<h3>Good AI opportunities usually have</h3><ul><li>A frequent, painful job with lots of language, images, or decisions.</li><li>Tolerance for some errors, or a cheap human check.</li><li>Data or context you can access (documents, tickets, history).</li><li>A clear metric that improves (time saved, conversion, resolution).</li></ul>""",
   ["Start from the user job, not the model.", "Plot value vs feasibility.", "Error tolerance decides how much autonomy AI gets."], "List 10 AI ideas for a product you know and place them on the opportunity matrix."),
  ("basic", "Moats and data flywheels", "Understand what makes an AI product hard to copy.", ill_cycle(["More users", "More usage data & feedback", "Better model / prompts / retrieval", "Better product"], "The data flywheel") + r"""
<h3>Where advantage comes from (when everyone can call the same models)</h3><ul><li><b>Proprietary data and context</b>: your customers' history, domain documents, labelled outcomes.</li><li><b>Workflow ownership</b>: being where the work happens (the system of record).</li><li><b>Distribution</b>: existing users, brand, partnerships.</li><li><b>Trust and quality</b>: evals, safety, reliability in a domain (health, finance, legal).</li><li><b>Speed of learning</b>: feedback loops that improve weekly.</li></ul>
<div class="box">Thin "wrapper" products that only add a UI on a public model are easy to copy; add data, workflow, and trust.</div>""",
   ["Models are commodities; data, workflow and trust are moats.", "Design feedback loops from day one.", "Measure the flywheel: does quality improve with usage?"], "Draw the data flywheel for an AI feature you'd build and name the metric for each step."),
  ("intermediate", "Build vs buy vs partner, and choosing models", "Make sourcing and model decisions with clear trade-offs.", r"""
<table><tr><th>Option</th><th>When</th><th>Risks</th></tr><tr><td>Buy (SaaS AI tool)</td><td>Non-core need, fast time to value</td><td>Vendor lock-in, data sharing, less differentiation</td></tr>
<tr><td>Build on model APIs</td><td>Core experience, need control over prompts, data, UX</td><td>Team skills, evals, cost management</td></tr><tr><td>Partner</td><td>Specialised data or distribution you lack</td><td>Dependency, revenue share</td></tr>
<tr><td>Fine-tune / self-host open models</td><td>Strict data residency, high volume, specialised tasks</td><td>Infrastructure, maintenance, quality gap</td></tr></table>
<h3>Model choice criteria</h3><ul><li>Quality on <b>your</b> eval set (not public leaderboards alone).</li><li>Cost per successful task; latency; context length.</li><li>Data policies, residency (India data needs), enterprise terms.</li><li>Multilingual quality (Hindi and regional languages), safety behaviour.</li><li>Keep a provider-agnostic layer so you can switch.</li></ul>""",
   ["Buy non-core, build core, partner for missing assets.", "Choose models with your own evals and cost per task.", "Avoid lock-in with an abstraction layer."], "Write a build-vs-buy memo for an AI support assistant at a 200-person company."),
  ("intermediate", "Assessing and prioritising AI opportunities", "Score AI ideas on value, feasibility and risk.", ill_flow(["Problem & user", "Value (metric)", "Feasibility (data, quality)", "Risk (harm, compliance)", "Cost & effort", "Decision"], "AI opportunity assessment") + r"""
<table><tr><th>Question</th><th>Evidence</th></tr><tr><td>How often and how painful is the job?</td><td>Usage data, interviews</td></tr><tr><td>Can AI do it well enough today?</td><td>Prototype + 30-case eval</td></tr><tr><td>What happens when it's wrong?</td><td>Failure modes, human check cost</td></tr><tr><td>Cost per task vs value per task</td><td>Token estimates, pricing</td></tr><tr><td>Data access and permissions</td><td>Legal and security review</td></tr></table>
<p>Run a <b>2-week feasibility spike</b>: prototype, small eval, cost estimate, user reaction, before committing roadmap space.</p>""",
   ["Prototype + eval before roadmap commitment.", "Compare cost per task with value per task.", "Price in the cost of errors."], "Assess 3 AI ideas with the table above and recommend one."),
  ("advanced", "AI roadmaps and portfolio of bets", "Plan AI work under uncertainty.", ill_stack([("Horizon 1: improve core", "AI-added features, quick wins, 0–6 months"), ("Horizon 2: new experiences", "Copilots, agents in key workflows, 6–18 months"), ("Horizon 3: new business", "AI-first products, new markets, 18+ months")], "Three horizons for AI investment") + r"""
<ul><li>Use outcome-based roadmaps with confidence levels; AI capability changes fast.</li><li>Budget for evals, data work and safety, not only features.</li><li>Revisit quarterly: new models can make "hard" ideas easy (and cheaper).</li><li>Kill criteria: what eval or adoption level stops a bet.</li></ul>""",
   ["Balance quick wins with bigger bets.", "Include evals, data and safety work in the plan.", "Set kill criteria for each bet."], "Create a 3-horizon AI roadmap for an Indian fintech app."),
  ("advanced", "Case studies and final project", "Apply the strategy tools end to end.", r"""
<h3>Mini cases</h3><ul><li><b>Customer support (B2B SaaS)</b>: AI-added copilot first (draft replies), then AI-first self-service; moat = resolved-ticket data + workflow integration.</li><li><b>Edtech tutor</b>: AI-first; moat = curriculum-aligned content, learner progress data, trust with parents.</li><li><b>Fintech</b>: AI for fraud and support; regulatory trust as moat; heavy human-in-the-loop.</li></ul>
<h3>Final project</h3><p>Write a 2-page AI strategy for a product: opportunity matrix, flywheel, build/buy/partner decision, model-choice criteria, 3-horizon roadmap with kill criteria, and the evals that prove progress.</p>""",
   ["Strategy = where to play + how to win + what to build.", "Tie every bet to evals and metrics.", "Revisit as models change."], "Complete the 2-page AI strategy and present it in 7 minutes.")],
 [("AI-added", "AI improves an existing workflow"), ("AI-first", "Product only possible because of AI"), ("Data flywheel", "Usage → data → better product → more usage"), ("Moat", "Durable advantage competitors can't copy quickly"), ("Feasibility spike", "Short prototype + eval to test viability"), ("Kill criteria", "Pre-agreed signal to stop a bet")],
 [("How do you decide where to use AI?", "Start with frequent, painful jobs; check value, feasibility (prototype + eval), risk of errors and cost per task; plot on a value-feasibility matrix."),
  ("What is a moat for an AI product?", "Proprietary data and context, workflow ownership, distribution, trust/quality in a domain, and fast learning loops; not the model itself."),
  ("Build vs buy for AI?", "Buy non-core needs, build the core experience on model APIs, partner for missing data or distribution; consider lock-in, data policies and cost."),
  ("How do you choose a model?", "Your own evals, cost per successful task, latency, context, data policies and residency, multilingual quality, with an abstraction layer to switch."),
  ("What is a data flywheel?", "A loop where usage creates data and feedback that improves quality, attracting more usage."),
  ("How do you roadmap AI under uncertainty?", "Outcome roadmaps with confidence levels, three horizons, quarterly review, and kill criteria tied to evals and adoption.")],
 [("Wrapper", "Thin product on top of a public model"), ("System of record", "Where the main business data lives")],
 [("a16z: AI articles", "https://a16z.com/ai/"), ("Sequoia: AI perspectives", "https://www.sequoiacap.com/our-companies/"), ("Lenny's Newsletter: AI product", "https://www.lennysnewsletter.com/"), ("Reforge: AI strategy", "https://www.reforge.com/")],
 "<h3>AI strategy canvas</h3>" + TPL_CANVAS(["Target users & jobs", "AI opportunities (value × feasibility)", "Moat & flywheel", "Build / buy / partner", "Model criteria", "Horizon 1 / 2 / 3 bets", "Evals & metrics", "Kill criteria"]))

AIUX = C("ai-ux", "Designing_AI_Experiences.pdf", "ai-ux-design.html", "Designing AI Experiences (AI UX)",
 "Design AI features people trust and use: interaction patterns (copilot, chat, agent, inline), setting expectations, explainability and citations, feedback and control, failure and handoff design, and testing AI UX.",
 "AI UX is designing products where outputs are probabilistic: helping users understand what AI can do, trust it the right amount, correct it easily, and recover when it's wrong.",
 "What are good UX patterns for AI features?",
 [("basic", "Principles of AI UX", "Design for uncertainty and the right level of trust.", ill_flow(["Set expectations", "Show what AI did", "Let users verify", "Easy to correct", "Learn from feedback"], "AI UX loop") + r"""
<ul><li><b>Set expectations</b>: say what the AI can and can't do; show examples.</li><li><b>Calibrated trust</b>: not too much (blind acceptance), not too little (ignored).</li><li><b>User in control</b>: undo, edit, regenerate, opt out.</li><li><b>Transparency</b>: label AI content; show sources.</li><li><b>Graceful failure</b>: say "I'm not sure" and offer a human or manual path.</li></ul>""",
   ["Design for being wrong sometimes.", "Aim for calibrated trust.", "Always provide control and recovery."], "Audit an AI feature you use against the five principles."),
  ("basic", "Interaction patterns", "Pick the right pattern for the job.", r"""
<table><tr><th>Pattern</th><th>Example</th><th>Best for</th></tr><tr><td>Inline suggestion / autocomplete</td><td>Gmail Smart Compose, code completion</td><td>Small, frequent help</td></tr><tr><td>Copilot side panel</td><td>Docs or CRM assistant</td><td>Help while staying in the workflow</td></tr>
<tr><td>Chat</td><td>Support bot, tutor</td><td>Open questions, exploration</td></tr><tr><td>Generate-then-edit</td><td>Draft email, PRD, image</td><td>Creation with human polish</td></tr><tr><td>Agent with approvals</td><td>Booking, research agent</td><td>Multi-step tasks</td></tr><tr><td>Invisible AI</td><td>Ranking, fraud scores, smart defaults</td><td>Decisions users don't need to see</td></tr></table>
<p>Chat is not always the answer; often a button ("Summarise", "Fix grammar") inside the workflow converts better.</p>""",
   ["Match pattern to task size and risk.", "Prefer in-workflow buttons over generic chat.", "Agents need approvals and progress views."], "Redesign one chat feature as an inline pattern and compare."),
  ("intermediate", "Trust, explainability and citations", "Help users judge AI output quickly.", r"""
<ul><li>Cite sources with clickable references; highlight the supporting text.</li><li>Show confidence carefully (e.g. "Needs review" labels) rather than fake precision.</li><li>Explain decisions in plain words ("Flagged because the amount is 5× your usual").</li><li>Show what data was used and allow users to exclude data.</li><li>Label AI-generated content, especially images and voice.</li></ul>""",
   ["Citations and highlights speed verification.", "Explain decisions in user language.", "Label AI content clearly."], "Design the citation UI for an AI answer from 3 policy documents."),
  ("intermediate", "Feedback, control and personalisation", "Turn user actions into learning signals.", ill_cycle(["AI suggests", "User edits / accepts / rejects", "Signals logged", "Prompts, data or model improved"], "Feedback loop") + r"""
<ul><li>Explicit: thumbs, ratings, "report a problem" with reasons.</li><li>Implicit: accept, edit distance, regenerate, copy, abandon.</li><li>Controls: tone, length, language, sources to use, memory on/off.</li><li>Close the loop: show users that feedback changes results.</li></ul>""",
   ["Implicit signals are richer than thumbs.", "Give users meaningful controls.", "Feed signals into evals and improvements."], "List 6 feedback signals for an AI resume writer and how you'd use each."),
  ("advanced", "Failure, safety and handoff design", "Design what happens when AI can't or shouldn't answer.", r"""
<table><tr><th>Situation</th><th>Design</th></tr><tr><td>Low confidence / no source</td><td>"I couldn't find this in your documents" + search or human</td></tr><tr><td>Sensitive request</td><td>Safe response + helpline/expert; no judgement</td></tr>
<tr><td>Agent about to act</td><td>Preview + confirm; clear undo window</td></tr><tr><td>Slow response</td><td>Streaming, progress steps, cancel button</td></tr><tr><td>Outage</td><td>Manual fallback path; status message</td></tr></table>""",
   ["Every AI feature needs a fallback path.", "Preview and confirm before actions.", "Stream and show progress for long tasks."], "Write failure states for an AI booking agent."),
  ("advanced", "Testing AI UX and final project", "Validate AI experiences with users and evals.", r"""
<ul><li>Wizard-of-Oz tests before building (a human plays the AI).</li><li>Prototype with real model outputs, including bad ones; watch how users react to errors.</li><li>Measure: task success, time saved, trust calibration (do users catch wrong answers?), retention.</li><li>Accessibility and Indian language support.</li></ul>
<h3>Final project</h3><p>Design an AI feature end to end: pattern choice, key screens (Figma), expectation-setting copy, citation UI, feedback signals, failure states, and a 5-user test plan.</p>""",
   ["Test with imperfect outputs.", "Measure trust calibration, not only satisfaction.", "Design and evals go together."], "Complete the AI UX final project.")],
 [("Calibrated trust", "Users trust AI as much as it deserves"), ("Generate-then-edit", "AI drafts, user polishes"), ("Wizard of Oz", "Human simulates AI in tests"), ("Implicit feedback", "Signals from behaviour (edits, accepts)")],
 [("Key principles of AI UX?", "Set expectations, design for uncertainty, transparency with sources, user control and recovery, graceful failure with handoff."),
  ("When not to use chat?", "When a task is small and in a workflow; an inline button or suggestion is faster and clearer."),
  ("How do you build trust?", "Citations, plain explanations, labels for AI content, consistent quality, and easy correction."),
  ("What feedback signals matter?", "Accept/edit/regenerate/abandon rates and edit distance, plus explicit ratings with reasons."),
  ("How do you test AI UX?", "Wizard-of-Oz, prototypes with real and bad outputs, task success and trust calibration metrics."),
  ("Design for an AI agent action?", "Preview, confirmation, progress, undo window, and clear logs.")],
 [("Handoff", "Passing a task to a human"), ("Streaming", "Showing output as it's generated")],
 [("Google PAIR Guidebook", "https://pair.withgoogle.com/guidebook/"), ("Microsoft HAX Toolkit (Human-AI guidelines)", "https://www.microsoft.com/en-us/haxtoolkit/"), ("Nielsen Norman Group: AI articles", "https://www.nngroup.com/topic/ai/"), ("Shape of AI (UX patterns)", "https://www.shapeof.ai/")],
 "<h3>AI UX checklist</h3>" + TPL_CANVAS(["Pattern chosen & why", "Expectation-setting copy", "Citation / explanation UI", "Controls (tone, length, sources)", "Feedback signals", "Failure & handoff states", "Accessibility & languages", "Test plan"]))

PRICING = C("ai-pricing", "Pricing_and_Monetising_AI.pdf", "ai-pricing.html", "Pricing & Monetising AI Products",
 "Make AI products profitable: AI cost structure and unit economics, pricing models (seat, usage, credits, outcome, hybrid), packaging AI features, margin control and go-to-market.",
 "AI features have real running costs on every use, so pricing must cover cost per task while matching the value customers get; that's why AI pricing is shifting from per-seat to usage and outcome models.",
 "How should I price an AI feature?",
 [("basic", "AI cost structure and unit economics", "Know what each AI task costs.", ill_stack([("Model tokens", "input + output tokens × price"), ("Retrieval & tools", "search, vector DB, API calls"), ("Infrastructure", "hosting, logging, monitoring"), ("Human review", "QA, escalations"), ("Support & evals", "testing, safety, improvements")], "Cost per AI task") + r"""
<pre>cost per task = (input tokens × input price + output tokens × output price) × calls per task
               + tools/retrieval + human review share
gross margin  = (price per task − cost per task) ÷ price per task</pre>
<p>Measure cost per <b>successful</b> task; retries and failures count.</p>""",
   ["Every AI use has a variable cost.", "Track cost per successful task.", "Include human review and evals in cost."], "Estimate the cost per conversation for an AI support bot with your own assumptions."),
  ("basic", "Pricing models", "Compare seat, usage, credits, outcome and hybrid pricing.", r"""
<table><tr><th>Model</th><th>Example</th><th>Pros</th><th>Cons</th></tr><tr><td>Per seat</td><td>₹X per user/month incl. AI</td><td>Simple, predictable</td><td>Heavy users erode margin</td></tr>
<tr><td>Usage</td><td>Per 1,000 messages / minutes</td><td>Aligns with cost</td><td>Unpredictable bills</td></tr><tr><td>Credits</td><td>Monthly credit pack, top-ups</td><td>Flexible, controls cost</td><td>Harder to understand</td></tr>
<tr><td>Outcome</td><td>Per resolved ticket / booked meeting</td><td>Aligns with value</td><td>Needs clear measurement</td></tr><tr><td>Hybrid</td><td>Seat + included usage + overage</td><td>Balanced</td><td>More complex</td></tr></table>""",
   ["Match price metric to value and cost.", "Hybrid models are common.", "Outcome pricing needs trusted measurement."], "Pick a pricing model for 3 AI products and justify it."),
  ("intermediate", "Packaging AI features", "Decide free, paid and add-on AI.", r"""
<ul><li><b>Free tier AI</b> to drive adoption (limited usage).</li><li><b>AI in premium plans</b> to upsell.</li><li><b>AI add-on</b> priced separately for heavy-value use.</li><li>Fair-use limits and clear meters; show usage in-product.</li><li>India context: price sensitivity, UPI autopay, annual discounts, team plans for SMEs.</li></ul>""",
   ["Free AI drives adoption; limits protect margin.", "Show usage clearly.", "Localise price points and payment methods."], "Design Free / Pro / Business packaging for an AI writing tool for Indian SMEs."),
  ("intermediate", "Protecting margins", "Reduce AI cost without hurting quality.", ill_flow(["Route easy tasks to small models", "Cache repeated answers", "Trim context", "Cap steps & retries", "Batch offline work", "Monitor cost per task"], "Margin levers") + r"""<p>Always check quality with evals after a cost change.</p>""",
   ["Routing and caching are the biggest levers.", "Cap runaway usage.", "Verify quality after every cost cut."], "Pick 3 margin levers for an AI tutor and estimate savings."),
  ("advanced", "Go-to-market for AI products", "Launch and sell AI with proof.", r"""
<ul><li>Lead with measurable outcomes (hours saved, tickets resolved) and case studies.</li><li>Free trials with guided use cases; time-to-value under 10 minutes.</li><li>Address trust: security, data use, accuracy, human control.</li><li>Sales enablement: ROI calculator, demo scripts, objection handling (hallucinations, privacy).</li></ul>""",
   ["Sell outcomes with proof.", "Fast time-to-value in trials.", "Answer trust objections upfront."], "Write an ROI calculator outline for an AI support copilot."),
  ("advanced", "Final project", "Price and package a real AI product.", r"""<p>Choose an AI product; build a unit-economics sheet (cost per task, margin), choose a pricing model and packaging, set fair-use limits, write the pricing page copy, and an experiment plan to test willingness to pay.</p>""",
   ["Numbers first, then packaging.", "Test willingness to pay.", "Revisit as model prices fall."], "Complete the pricing project.")],
 [("Unit economics", "Revenue and cost per unit (task, user)"), ("Gross margin", "(Price − cost) ÷ price"), ("Credits", "Prepaid units consumed by AI use"), ("Outcome pricing", "Charging per result achieved"), ("Fair use", "Limits that prevent abuse")],
 [("Why is AI pricing different?", "Each use has variable model cost, so heavy usage can destroy margins on flat seat pricing."),
  ("Which pricing model would you choose?", "The one whose metric matches customer value and cost: often hybrid seat + included usage + overage, or outcome pricing when results are measurable."),
  ("How do you calculate cost per task?", "Tokens × prices × calls + tools and retrieval + human review share, divided over successful tasks."),
  ("How do you protect margins?", "Routing, caching, context trimming, step caps, batching, monitoring cost per task, verified with evals."),
  ("How do you sell AI?", "Outcome proof, fast time-to-value, trust answers, ROI tools.")],
 [("Overage", "Charge beyond included usage"), ("ROI", "Return on investment")],
 [("OpenAI pricing", "https://openai.com/api/pricing/"), ("Anthropic pricing", "https://www.anthropic.com/pricing"), ("Google AI pricing", "https://ai.google.dev/pricing"), ("OpenView: usage-based pricing", "https://openviewpartners.com/usage-based-pricing/")],
 "<h3>Unit-economics sheet</h3>" + TPL_CANVAS(["Tasks per user per month", "Tokens per task (in / out)", "Model price", "Tools & retrieval cost", "Human review cost", "Cost per successful task", "Price per user / per task", "Gross margin"]))

MLPM = C("ml-products", "ML_Products_for_PMs.pdf", "ml-products.html", "Machine Learning Products for PMs",
 "Manage traditional ML products: problem types, data and labelling, metrics, working with data scientists, recommendation and personalisation, the model lifecycle and MLOps monitoring.",
 "Before LLMs, most AI in products was machine learning that predicts, classifies, ranks or recommends (fraud scores, feeds, ETAs). PMs still own these products: the problem, the data, the metric trade-offs and the lifecycle.",
 "How does a product manager work on a machine learning product?",
 [("basic", "ML problem types", "Recognise which ML problem you're solving.", r"""
<table><tr><th>Type</th><th>Question</th><th>Example</th></tr><tr><td>Classification</td><td>Which category?</td><td>Fraud / not fraud, spam</td></tr><tr><td>Regression</td><td>How much?</td><td>Delivery time, price</td></tr><tr><td>Ranking / recommendation</td><td>What order?</td><td>Feed, search results, products</td></tr>
<tr><td>Clustering</td><td>What groups exist?</td><td>Customer segments</td></tr><tr><td>Forecasting</td><td>What next?</td><td>Demand, inventory</td></tr><tr><td>Anomaly detection</td><td>What's unusual?</td><td>Payment spikes, outages</td></tr></table>""",
   ["Name the problem type first.", "Each type has different metrics.", "Many products combine types."], "Name the ML problem type for 8 features in apps you use."),
  ("basic", "Data and labelling", "Get the data an ML product needs.", ill_flow(["Define label", "Collect data", "Label / annotate", "Check quality & bias", "Split train / test", "Refresh"], "Data pipeline for ML") + r"""
<ul><li>Labels from outcomes (did the user default?), humans (annotators), or rules.</li><li>Watch leakage (using future information), class imbalance (rare fraud), and bias.</li><li>Labelling tools and vendors; clear guidelines and agreement checks.</li></ul>""",
   ["Data quality decides model quality.", "Write labelling guidelines.", "Check leakage, imbalance and bias."], "Write labelling guidelines for classifying support tickets into 6 categories."),
  ("intermediate", "Metrics and trade-offs", "Choose model metrics that match business costs.", ill_quad("Predicted positive", "Actually positive", ["False negative (missed)", "True positive", "True negative", "False positive (false alarm)"], "Confusion matrix (simplified)") + r"""
<ul><li>Precision = of flagged, how many were right; recall = of all positives, how many we caught.</li><li>Choose thresholds by business cost: missing fraud vs annoying good customers.</li><li>Link model metrics to product metrics (approval rate, losses, CSAT) with A/B tests.</li></ul>""",
   ["Precision vs recall is a business decision.", "Set thresholds by cost of errors.", "Validate with online experiments."], "For a loan-default model, decide which error is worse and how you'd set the threshold."),
  ("intermediate", "Recommendations and personalisation", "Understand how recommenders work and are measured.", r"""
<ul><li>Approaches: popularity, collaborative filtering (people like you), content-based (similar items), and hybrid/deep models.</li><li>Cold start for new users/items: onboarding questions, popular items, content features.</li><li>Metrics: CTR, conversion, watch time, diversity, novelty, long-term retention.</li><li>Guardrails: filter bubbles, fairness to sellers/creators, safety.</li></ul>""",
   ["Hybrid recommenders are common.", "Plan for cold start.", "Balance engagement with diversity and long-term value."], "Design recommendations for a regional-language news app."),
  ("advanced", "Model lifecycle and MLOps", "Keep models working after launch.", ill_cycle(["Train", "Evaluate", "Deploy (shadow / A/B)", "Monitor drift", "Retrain"], "ML lifecycle") + r"""
<ul><li>Shadow mode and gradual rollout before full launch.</li><li>Monitor data drift, prediction drift and business metrics; alert on drops.</li><li>Model registry and versioning; rollback plans.</li><li>Model cards documenting purpose, data, limits.</li></ul>""",
   ["Launch is the start of the lifecycle.", "Monitor drift and business impact.", "Always have a rollback."], "Write a monitoring plan for a delivery-ETA model."),
  ("advanced", "Working with data scientists and final project", "Collaborate well and ship an ML feature.", r"""
<ul><li>PM brings: problem, users, business costs of errors, constraints, success metric.</li><li>DS brings: feasibility, data needs, model choice, offline metrics.</li><li>Agree early: baseline (simple rules), target metric, timeline for experiments.</li></ul>
<h3>Final project</h3><p>Write an ML PRD for a fraud or recommendation feature: problem type, labels and data, metrics and threshold logic, A/B plan, monitoring, model card.</p>""",
   ["Start from a simple baseline.", "Agree metrics and costs of errors early.", "Document with a model card."], "Complete the ML PRD.")],
 [("Precision", "TP ÷ (TP + FP)"), ("Recall", "TP ÷ (TP + FN)"), ("Threshold", "Score cut-off for a decision"), ("Drift", "Data or behaviour changing over time"), ("Shadow mode", "Model runs without affecting users"), ("Cold start", "No history for new users/items")],
 [("How is ML PM different from regular PM?", "Probabilistic outputs, data dependency, metric trade-offs, experimentation and ongoing monitoring/retraining."),
  ("Precision vs recall trade-off?", "Choose based on the cost of false positives vs false negatives; set thresholds accordingly and validate online."),
  ("How do you handle cold start?", "Onboarding preferences, popular/trending items, content-based features, and exploration."),
  ("What is drift?", "Change in input data or relationships over time that degrades model quality; detect via monitoring and retrain."),
  ("What goes in an ML PRD?", "Problem type, labels/data, metrics and thresholds, baseline, experiment plan, monitoring, rollback, model card.")],
 [("Label", "The correct answer used for training"), ("Leakage", "Training on information unavailable at prediction time")],
 [("Google: Rules of ML", "https://developers.google.com/machine-learning/guides/rules-of-ml"), ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"), ("Model cards paper (Google)", "https://modelcards.withgoogle.com/about"), ("SkillNavora Statistics & ML track", "https://www.skillnavora.in/data-science/index.html")],
 "<h3>ML PRD extras</h3>" + TPL_CANVAS(["Problem type", "Label definition & source", "Baseline", "Offline metric & target", "Threshold logic (cost of errors)", "Online A/B metric", "Monitoring & drift alerts", "Rollback plan", "Model card link"]))

GOV = C("ai-governance", "AI_Governance_and_Responsible_AI.pdf", "ai-governance.html", "AI Governance & Responsible AI",
 "Ship AI responsibly: principles and risks, regulations (EU AI Act, India's DPDP Act and AI guidelines, sector rules), AI risk and impact assessments, policies and documentation, and operating governance.",
 "AI governance is the set of policies, reviews and controls that make sure AI is safe, fair, legal and accountable, so teams can ship faster with fewer surprises.",
 "What does responsible AI governance mean for product managers?",
 [("basic", "Principles and risks", "Know the main responsible-AI principles and risks.", ill_stack([("Accountability", "clear owners and decisions"), ("Safety & security", "no harm, robust to attacks"), ("Fairness", "no unjust bias"), ("Privacy", "lawful, minimal data use"), ("Transparency", "people know AI is used and why")], "Responsible AI principles") + r"""
<p>Typical risks: harmful or wrong outputs, bias, privacy leaks, IP/copyright, security (prompt injection), over-reliance, and job or social impact.</p>""",
   ["Principles must turn into checks.", "List risks per feature.", "Name an accountable owner."], "List the top 5 risks of an AI hiring-screening feature."),
  ("basic", "Regulations to know", "Understand the main laws and frameworks at a PM level.", r"""
<table><tr><th>Framework</th><th>What PMs should know</th></tr>
<tr><td>EU AI Act</td><td>Risk tiers: prohibited, high-risk (e.g. hiring, credit), limited-risk (transparency duties like disclosing chatbots), minimal; obligations phase in over several years</td></tr>
<tr><td>India: DPDP Act 2023</td><td>Consent, purpose limitation, data minimisation, rights of data principals; applies to personal data used in AI</td></tr>
<tr><td>India: government AI guidance</td><td>Advisories and governance guidelines on responsible AI, deepfakes and labelling; check current versions</td></tr>
<tr><td>Sector rules</td><td>RBI (lending, fraud), SEBI (investment advice), IRDAI (insurance), health regulators</td></tr>
<tr><td>Standards</td><td>NIST AI Risk Management Framework; ISO/IEC 42001 AI management systems</td></tr></table>
<p>This is a learning summary, not legal advice; involve legal counsel for real decisions.</p>""",
   ["Know your feature's risk tier.", "Personal data → DPDP duties.", "Check sector regulators and current guidance."], "Classify 5 AI features by EU AI Act risk tier and explain."),
  ("intermediate", "AI risk and impact assessment", "Assess a feature before launch.", ill_flow(["Describe use & users", "Identify risks", "Rate likelihood × impact", "Mitigations & evals", "Residual risk sign-off", "Monitor"], "AI risk assessment") + r"""<p>Use evals and red-teaming results as evidence for each mitigation.</p>""",
   ["Assess before launch, not after incidents.", "Evidence = evals and red-team results.", "Sign off residual risk explicitly."], "Complete a risk assessment for an AI loan-eligibility assistant."),
  ("intermediate", "Policies and documentation", "Write the documents governance needs.", r"""
<ul><li>Company AI use policy (what tools, what data, approvals).</li><li>Model/system cards: purpose, data, evaluation, limits, contacts.</li><li>Data protection impact assessment for personal data.</li><li>User-facing disclosures: "You're chatting with AI", AI-generated labels.</li><li>Decision logs for high-impact choices.</li></ul>""",
   ["Document purpose, data, evals and limits.", "Disclose AI to users.", "Keep decision logs."], "Draft a 1-page AI use policy for a 50-person startup."),
  ("advanced", "Operating governance", "Run governance without slowing teams down.", r"""
<ul><li>Tiered review: light checklist for low-risk features, committee review for high-risk.</li><li>Incident response: report, triage, rollback, communicate, learn.</li><li>Audits: periodic eval and bias re-checks, access reviews.</li><li>Vendor management: data terms, security, model changes.</li></ul>""",
   ["Tier the process by risk.", "Have an incident playbook.", "Re-check periodically."], "Design a tiered AI review process for your company."),
  ("advanced", "Final project", "Govern a real AI feature.", r"""<p>For an AI feature, produce: risk tier, risk assessment table, mitigations with eval evidence, system card, user disclosure copy, DPDP checklist, incident playbook.</p>""",
   ["Governance is a product practice.", "Evidence over promises.", "Make it lightweight for low risk."], "Complete the governance pack.")],
 [("EU AI Act", "EU law with risk-based AI obligations"), ("DPDP Act", "India's Digital Personal Data Protection Act, 2023"), ("NIST AI RMF", "US framework for AI risk management"), ("ISO/IEC 42001", "AI management system standard"), ("System card", "Document describing an AI system's purpose and limits")],
 [("What is responsible AI?", "Building AI that is accountable, safe, fair, private and transparent, backed by processes and evidence."),
  ("How does the EU AI Act affect products?", "Obligations depend on risk tier; high-risk uses like hiring or credit need risk management, data governance, documentation and human oversight."),
  ("What does DPDP mean for AI features?", "Lawful consent/purpose, minimal data, user rights, security, and care with personal data in prompts and logs."),
  ("How do you run a risk assessment?", "Describe use, identify risks, rate them, add mitigations with eval evidence, sign off residual risk, monitor."),
  ("How do you keep governance fast?", "Tiered reviews, templates, automation of checks, clear owners.")],
 [("Residual risk", "Risk left after mitigations"), ("Red-teaming", "Trying to make the AI fail")],
 [("EU AI Act overview", "https://artificialintelligenceact.eu/"), ("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"), ("ISO/IEC 42001", "https://www.iso.org/standard/81230.html"), ("India DPDP Act (MeitY)", "https://www.meity.gov.in/data-protection-framework"), ("OECD AI principles", "https://oecd.ai/en/ai-principles")],
 "<h3>AI risk register</h3><pre>risk | feature | likelihood (1-5) | impact (1-5) | mitigation | eval evidence | owner | status</pre>")

PLATFORM = C("platform-pm", "Platform_and_API_Product_Management.pdf", "platform-api-pm.html", "Platform & API Product Management",
 "Manage platforms and APIs as products: developer experience, API design decisions, versioning and limits, ecosystems and partners, platform metrics, and AI/MCP platforms.",
 "A platform PM builds products that other teams, developers or partners build on: APIs, SDKs, internal platforms and ecosystems. The users are developers, and the product is how easily they succeed.",
 "What does a platform or API product manager do?",
 [("basic", "Platforms and APIs as products", "Understand platform types and users.", ill_stack([("External developers & partners", "public APIs, marketplaces"), ("Internal product teams", "shared services, design system"), ("Core platform", "data, identity, payments, AI services")], "Platform layers") + r"""
<p>Examples: UPI/payment APIs (Razorpay, Stripe), maps APIs, WhatsApp Business API, internal identity or AI platforms, MCP servers that expose your product to AI assistants.</p>""",
   ["Developers are the users.", "Internal platforms are products too.", "AI assistants are a new channel (MCP)."], "Map the platform users and their jobs for a payments company."),
  ("basic", "Developer experience (DX)", "Make developers successful fast.", ill_flow(["Discover", "Sign up & get key", "First API call", "Build integration", "Go live", "Scale & support"], "Developer journey") + r"""
<ul><li>Time to first successful call (aim for minutes).</li><li>Clear docs, quickstarts, SDKs, sandbox keys, Postman collections.</li><li>Helpful errors, status page, changelog, community support.</li></ul>""",
   ["Measure time to first call.", "Docs and sandbox are the onboarding.", "Errors should explain the fix."], "Audit a public API's onboarding and list 5 improvements."),
  ("intermediate", "API design decisions for PMs", "Decide what matters in API contracts.", r"""
<ul><li>Resources and endpoints that match developer jobs; consistent naming.</li><li>Authentication (API keys, OAuth), permissions and scopes.</li><li>Versioning and deprecation policy (e.g. 12 months notice).</li><li>Rate limits and quotas; idempotency keys for payments.</li><li>Webhooks for events; pagination; error formats.</li></ul>""",
   ["Contracts are promises: version carefully.", "Rate limits protect reliability.", "Webhooks make integrations real-time."], "Write the API requirements for a 'refund' endpoint."),
  ("intermediate", "Ecosystems and partners", "Grow a platform through others.", ill_cycle(["More developers & apps", "More value for users", "More users", "More reasons to build"], "Platform network effect") + r"""<ul><li>Partner tiers, certification, marketplace listing, revenue share.</li><li>Governance: app review, security, data access rules.</li></ul>""",
   ["Platforms grow through network effects.", "Partners need clear rules and incentives.", "Review apps for security."], "Design a partner program for a SaaS marketplace."),
  ("advanced", "Platform metrics", "Measure platform health.", r"""
<table><tr><th>Metric</th><th>Why</th></tr><tr><td>Active developers / apps</td><td>Adoption</td></tr><tr><td>Time to first call / to production</td><td>DX quality</td></tr><tr><td>API calls, success rate, latency</td><td>Usage and reliability</td></tr><tr><td>Revenue via platform</td><td>Business value</td></tr><tr><td>Support tickets per integration</td><td>Friction</td></tr></table>""",
   ["Mix adoption, DX, reliability and revenue.", "Track success rate and latency.", "Use tickets to find friction."], "Build a platform dashboard spec."),
  ("advanced", "AI platforms and final project", "Apply platform thinking to AI.", r"""
<ul><li>Internal AI platforms: shared model access, evals, guardrails, prompt/skill libraries, cost tracking.</li><li>Exposing your product via MCP so AI assistants can use it.</li></ul>
<h3>Final project</h3><p>Write a platform PRD for a public API or internal AI platform: users, developer journey, API requirements, limits and versioning, partner rules, metrics.</p>""",
   ["AI platforms centralise models, evals and guardrails.", "MCP is a new distribution channel.", "Treat developers like customers."], "Complete the platform PRD.")],
 [("DX", "Developer experience"), ("SDK", "Software development kit"), ("Webhook", "Event notification sent to your URL"), ("Rate limit", "Max requests per time"), ("Deprecation", "Planned retirement of an API version")],
 [("What does a platform PM do?", "Builds products other teams or developers build on, optimising developer success, reliability and ecosystem growth."),
  ("Key DX metric?", "Time to first successful API call, plus time to production."),
  ("How do you version an API?", "Explicit versions, backward compatibility, deprecation notices, migration guides and changelogs."),
  ("Platform metrics?", "Active developers/apps, success rate, latency, calls, revenue, support friction."),
  ("What is an AI platform team?", "Provides shared model access, evals, guardrails, prompt/skill libraries and cost controls to product teams.")],
 [("Idempotency key", "Prevents duplicate actions on retries"), ("OAuth", "Standard for delegated access")],
 [("Stripe API docs (example of great DX)", "https://docs.stripe.com/api"), ("Razorpay docs", "https://razorpay.com/docs/"), ("Postman learning center", "https://learning.postman.com/"), ("Model Context Protocol", "https://modelcontextprotocol.io/")],
 "<h3>Platform PRD extras</h3>" + TPL_CANVAS(["Developer personas", "Jobs & use cases", "Time-to-first-call target", "Endpoints / events", "Auth & scopes", "Limits & versioning", "Partner rules", "Metrics"]))

OPS = C("product-ops", "Product_Operations.pdf", "product-ops.html", "Product Operations",
 "Help product teams scale: what product ops does, processes and rituals, tools and data, customer-insight pipelines, launch management, and AI in product ops.",
 "Product operations is the function that makes product teams run smoothly at scale: shared processes, tools, data and insight pipelines, so PMs spend time on decisions instead of admin.",
 "What does product operations do?",
 [("basic", "What product ops is", "Know the scope and value of product ops.", ill_stack([("Data & insights", "metrics, dashboards, customer feedback"), ("Process & rituals", "planning, reviews, launches"), ("Tools & systems", "Jira, Productboard, Notion, analytics"), ("Enablement", "templates, training, communication")], "Product ops pillars") + r"""<p>Common in companies with 10+ PMs; in smaller teams PMs do it themselves.</p>""",
   ["Product ops removes friction.", "Four pillars: data, process, tools, enablement.", "Scale matters."], "List 10 recurring admin tasks PMs on your team do."),
  ("basic", "Processes and rituals", "Design lightweight rhythms.", ill_cycle(["Quarterly planning", "Roadmap reviews", "Sprint / release cadence", "Launch reviews", "Retrospectives"], "Product operating rhythm") + r"""<p>Each ritual needs an owner, inputs, outputs and a template; cut rituals that don't change decisions.</p>""",
   ["Rituals must change decisions.", "Templates make them fast.", "Owners keep them alive."], "Design the agenda and template for a monthly product review."),
  ("intermediate", "Tools and data", "Run the product tool stack and metrics.", r"""
<ul><li>Single source of truth for roadmap and feedback (Productboard, Jira Product Discovery, Notion).</li><li>Metrics definitions and dashboards (a metrics dictionary).</li><li>Clean taxonomy: product areas, customer segments, tags.</li><li>Tool consolidation and access hygiene.</li></ul>""",
   ["One source of truth per object.", "A metrics dictionary prevents arguments.", "Taxonomy makes insights searchable."], "Draft a metrics dictionary with 8 metrics."),
  ("intermediate", "Customer-insight pipelines", "Turn feedback into prioritised insights.", ill_flow(["Collect (support, sales, reviews, interviews)", "Tag & deduplicate (AI-assisted)", "Link to opportunities", "Quantify (customers, revenue)", "Share in reviews", "Close the loop with customers"], "Insight pipeline") + "",
   ["AI can tag and cluster feedback at scale.", "Link insights to opportunities and revenue.", "Close the loop with customers."], "Build a feedback-tagging taxonomy and test it on 30 items with AI."),
  ("advanced", "Launch management and governance", "Make launches predictable.", r"""
<ul><li>Launch tiers (big, medium, small) with checklists.</li><li>Go/no-go reviews with evals, support readiness, docs, legal.</li><li>Release notes and internal enablement; post-launch reviews.</li></ul>""",
   ["Tier launches by impact.", "Checklists and go/no-go.", "Post-launch review every time."], "Create a tiered launch checklist."),
  ("advanced", "AI in product ops and final project", "Automate product ops with AI.", r"""
<ul><li>AI skills for weekly reports, release notes, insight synthesis, meeting notes.</li><li>Agents that keep Jira and docs in sync (with approvals).</li><li>Dashboards with AI summaries.</li></ul>
<h3>Final project</h3><p>Design a product-ops toolkit for a 10-PM team: operating rhythm, templates, metrics dictionary, insight pipeline, launch tiers, and 3 AI automations.</p>""",
   ["Automate reporting and synthesis.", "Keep humans on decisions.", "Measure time saved for PMs."], "Complete the product-ops toolkit.")],
 [("Operating rhythm", "Recurring planning and review cadence"), ("Metrics dictionary", "Agreed definitions of metrics"), ("Launch tier", "Size category deciding launch process")],
 [("What is product ops?", "A function that scales product teams through data, process, tools and enablement."),
  ("When do you need it?", "When PM count grows and inconsistency, admin load and scattered data slow decisions."),
  ("How do you build an insight pipeline?", "Collect from all channels, tag and dedupe (AI-assisted), link to opportunities, quantify, share, close the loop."),
  ("How does AI change product ops?", "Automates synthesis, reports, release notes and tool hygiene; humans keep decisions.")],
 [("Taxonomy", "Agreed categories and tags")],
 [("Productboard: product ops", "https://www.productboard.com/blog/"), ("Atlassian: Jira Product Discovery", "https://www.atlassian.com/software/jira/product-discovery"), ("Mind the Product: product ops", "https://www.mindtheproduct.com/")],
 "<h3>Operating rhythm sheet</h3><pre>ritual | cadence | owner | inputs | outputs | template | decisions it informs</pre>")

MEDIA = C("multimodal", "Multimodal_and_AI_Media.pdf", "multimodal-ai.html", "Multimodal AI & AI Media",
 "Use AI that sees, hears and creates: vision understanding, image generation, video and voice, multimodal product use cases, and rights, safety, deepfakes and content labelling.",
 "Multimodal AI understands and generates more than text: images, audio and video. It powers features like reading invoices from photos, voice assistants, product images and video explainers, along with new risks like deepfakes.",
 "What can product managers build with multimodal AI?",
 [("basic", "Multimodal basics", "Know what modern models can see, hear and create.", ill_stack([("Text", "chat, writing, analysis"), ("Images", "understand photos, charts; generate visuals"), ("Audio", "speech-to-text, text-to-speech, voice agents"), ("Video", "summarise, search, generate clips")], "Modalities") + "",
   ["Models now take and produce many modalities.", "Choose the modality users already use.", "Voice matters in India (literacy, languages)."], "List 5 features where a photo or voice input beats typing."),
  ("basic", "Vision understanding use cases", "Use AI to read and interpret images.", r"""
<ul><li>OCR of invoices, IDs (with consent), forms; handwritten notes.</li><li>Chart and screenshot understanding; UI review.</li><li>Quality inspection (manufacturing), crop disease, damage assessment (insurance).</li><li>Accessibility: describing images for visually impaired users.</li></ul>""",
   ["Vision unlocks offline-to-digital workflows.", "Mask personal data.", "Measure accuracy on your own images."], "Design an AI feature that reads shop receipts for expense tracking."),
  ("intermediate", "Image generation in products", "Use generative images responsibly.", ill_flow(["Brief & brand rules", "Generate variants", "Human review", "Edit & upscale", "Label & publish"], "Image generation workflow") + r"""<p>Tools: Midjourney, Adobe Firefly, Ideogram, Leonardo, DALL·E, Imagen, Canva AI. Use cases: ads, product mock-ups, thumbnails, illustrations.</p>""",
   ["Keep brand rules in the brief.", "Human review before publishing.", "Prefer tools with clear commercial-use terms."], "Create a brand-safe image brief template."),
  ("intermediate", "Voice and video", "Build with speech and video AI.", r"""
<ul><li>Speech-to-text and text-to-speech in many Indian languages; voice agents (see Voice Agents lesson).</li><li>Video: AI summaries and search of recordings; avatar and generative video tools (Runway, Veo, Sora, HeyGen, Synthesia) for explainers.</li><li>Latency, accents, background noise and cost are key constraints.</li></ul>""",
   ["Test with real accents and noise.", "Video AI is great for explainers and summaries.", "Watch latency and cost."], "Plan a Hindi voice FAQ assistant for a clinic."),
  ("advanced", "Rights, safety, deepfakes and labelling", "Manage the risks of AI media.", r"""
<ul><li>Copyright and licences: check tool terms for commercial use; avoid copying artists or brands.</li><li>Consent for faces and voices; never clone voices without permission.</li><li>Label AI-generated media; content credentials (C2PA) and watermarking.</li><li>Moderation of user-generated AI media; follow Indian advisories on deepfakes.</li></ul>""",
   ["Consent for likeness and voice.", "Label AI media.", "Check commercial-use rights."], "Write an AI media policy for a marketing team."),
  ("advanced", "Final project", "Ship a multimodal feature.", r"""<p>Design a multimodal feature (photo receipts, voice ordering, or video course summaries): user flow, model/tool choice, accuracy eval on 30 samples, privacy and consent, labelling, cost estimate.</p>""",
   ["Evaluate on real samples.", "Design for consent and privacy.", "Estimate cost per use."], "Complete the multimodal project.")],
 [("OCR", "Reading text from images"), ("TTS / STT", "Text-to-speech / speech-to-text"), ("C2PA", "Content credentials standard for media provenance"), ("Deepfake", "Realistic fake media of real people")],
 [("What is multimodal AI?", "Models that understand and/or generate several types of data: text, images, audio and video."),
  ("A good vision use case?", "Reading receipts or forms from photos to remove manual entry, with accuracy checks and privacy."),
  ("Risks of AI media?", "Copyright, consent for likeness and voice, deepfakes, misinformation; mitigate with consent, labelling, C2PA and moderation."),
  ("Why voice in India?", "Many users prefer speaking, many languages and literacy levels; voice widens access.")],
 [("Watermark", "Hidden or visible mark identifying AI content")],
 [("C2PA content credentials", "https://c2pa.org/"), ("Google AI Studio (Gemini multimodal)", "https://aistudio.google.com/"), ("Adobe Firefly", "https://www.adobe.com/products/firefly.html"), ("ElevenLabs docs", "https://elevenlabs.io/docs"), ("Runway Academy", "https://academy.runwayml.com/")],
 "<h3>AI media brief</h3>" + TPL_CANVAS(["Purpose & audience", "Brand rules", "Tool & licence", "Consent needed?", "Review steps", "Labelling", "Accessibility (alt text, captions)"]))

ALL = [STRATEGY, AIUX, PRICING, MLPM, GOV, PLATFORM, OPS, MEDIA]
