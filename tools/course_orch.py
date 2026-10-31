"""Course: Agent Orchestration & Monitoring (workflows, routing, parallel, state, HITL, recovery, multi-agent, cost, monitoring)."""
COURSE = {
 "slug": "orchestration", "pdf": "Agent_Orchestration_and_Monitoring.pdf", "page": "agent-orchestration.html",
 "title": "Agent Orchestration & Monitoring", "kicker": "SkillNavora · AI Product Management & GenAI Launchpad · Skill 7 of 7",
 "intro": "Run longer AI workflows reliably: workflow patterns, routing and model selection, parallel work, state and checkpoints, human-in-the-loop approvals, error recovery, multi-agent systems, scheduling and triggers, cost control, and production monitoring.",
 "oneline": "Orchestration is how AI steps, tools and people are connected into a workflow that runs reliably; monitoring is how you know it keeps working. Start with a simple workflow and add agents only where they are needed.",
 "tutor_q": "Explain AI agent orchestration patterns like routing and orchestrator-workers with examples",
 "extra_btn": '<a class="btn btn-line" href="browser-automation.html">Browser automation course</a>',
 "cheat_title": "Patterns cheat sheet",
 "classes": [
  ("basic", "Workflows vs agents: start simple", "Know when a fixed workflow is enough and when an agent is worth it.", r"""
<table><tr><th></th><th>Workflow</th><th>Agent</th></tr><tr><td>Steps</td><td>Defined in advance by you</td><td>Chosen by the model as it goes</td></tr>
<tr><td>Predictability</td><td>High</td><td>Lower; needs guardrails</td></tr><tr><td>Cost / speed</td><td>Lower / faster</td><td>Higher / slower</td></tr><tr><td>Best for</td><td>Known, repeatable processes</td><td>Open-ended tasks with unknown steps</td></tr></table>
<div class="box">Rule: start with one model and a few tools in a clear workflow. Add agent autonomy or multiple agents only when simpler options fail your evals.</div>
<h3>Building blocks</h3><p>An LLM call + retrieval + tools + memory, connected by an orchestrator (code, n8n, Make, Zapier or an agent framework).</p>
""", ["Workflows are predictable; agents are flexible.", "Start simple; add autonomy only when needed.", "Measure with evals before adding complexity."],
   "For 3 processes in your work, decide workflow or agent and justify it."),

  ("basic", "Core patterns: chaining, routing and parallelisation", "Use the three most common orchestration patterns.", r"""
<table><tr><th>Pattern</th><th>How it works</th><th>Example</th></tr>
<tr><td>Prompt chaining</td><td>Step 1 output → step 2 input, with checks between</td><td>Extract facts → draft PRD → review</td></tr>
<tr><td>Routing</td><td>Classify the request, send it to the right workflow or model</td><td>Support: refund → refund flow; bug → engineering; simple FAQ → cheap model</td></tr>
<tr><td>Parallelisation</td><td>Run independent parts at once, then combine; or run several attempts and vote</td><td>Analyse 5 competitors in parallel; 3 judges vote on a risky answer</td></tr></table>
<h3>Model selection inside routing</h3><p>Use small, fast models for classification and simple answers; larger models for reasoning, writing and agents. Measure quality and cost per successful task, not per call.</p>
""", ["Chain for sequences, route for variety, parallelise for speed.", "Routing also picks the right model for cost.", "Check outputs between steps."],
   "Design a router for a customer-support bot with 5 intents, the workflow and model size for each."),

  ("intermediate", "Orchestrator-workers and evaluator-optimizer", "Use the two most powerful agentic patterns safely.", r"""
<h3>Orchestrator-workers</h3><p>A lead model plans the work, sends sub-tasks to workers (other model calls or agents), then combines results. Good for research and analysis where sub-tasks aren't known in advance.</p>
<h3>Evaluator-optimizer</h3><p>One model drafts, another evaluates against a rubric and gives feedback, loop until the bar is met or a step limit is reached. Good for writing, code and PRDs with clear quality criteria.</p>
<pre>loop max 3 times:
  draft = writer(brief, feedback)
  review = evaluator(draft, rubric)      # returns pass + issues
  if review.pass: break
  feedback = review.issues
return draft, review</pre>
<p>Always set limits (steps, time, cost) so loops end.</p>
""", ["Orchestrator plans; workers execute; orchestrator combines.", "Evaluator-optimizer loops on a rubric with a step cap.", "Limits on steps, time and cost are mandatory."],
   "Sketch an orchestrator-workers design for 'market research report on EV two-wheelers in India'."),

  ("intermediate", "State, checkpoints and long-running work", "Make workflows resumable and traceable.", r"""
<ul><li><b>State</b>: a record of what's done, what's pending, inputs, outputs and decisions (a table, JSON file or database row per run).</li>
<li><b>Checkpoints</b>: save after each major step so a failure resumes from there instead of starting over.</li>
<li><b>Idempotency</b>: re-running a step doesn't duplicate actions (e.g. doesn't create two Jira tickets).</li>
<li><b>Caching</b>: reuse valid results (search results, document summaries) to save time and money.</li></ul>
<pre>run_id | step | status (pending/running/done/failed) | input_ref | output_ref | started | finished | cost</pre>
""", ["Track state per run.", "Checkpoint after major steps.", "Make actions idempotent; cache reusable results."],
   "Design a state table for a weekly competitor-report workflow with 5 steps."),

  ("intermediate", "Human-in-the-loop, approvals and error recovery", "Put people at the right points and recover from failures safely.", r"""
<h3>Where humans add value</h3><ul><li>Before consequential actions: sending, publishing, paying, deleting.</li><li>When confidence is low or rules conflict.</li><li>Reviewing samples for quality.</li></ul>
<h3>Error recovery</h3><table><tr><th>Failure</th><th>Response</th></tr><tr><td>Timeout / rate limit</td><td>Retry with backoff; switch provider</td></tr><tr><td>Bad output (fails checks)</td><td>Retry with feedback; then escalate to human</td></tr>
<tr><td>Tool error</td><td>Log, retry once, fall back to manual path</td></tr><tr><td>Unexpected state</td><td>Stop, alert owner, keep checkpoint</td></tr></table>
""", ["Approvals before consequential actions.", "Retry with limits; fall back; escalate.", "Never fail silently: alert an owner."],
   "Write the approval points and error-recovery rules for an AI that drafts and sends customer emails."),

  ("advanced", "Multi-agent systems", "Know when splitting work across agents helps, and how to coordinate them.", r"""
<p>Multiple specialised agents (researcher, analyst, writer, reviewer) can help when work is large, parallel and needs different tools or context. They also add cost, latency and coordination problems.</p>
<ul><li>Give each agent a clear role, tools and output format.</li><li>Share state through a common store, not long chat histories.</li><li>Use a lead agent or a fixed workflow to coordinate and to decide when work is done.</li><li>Evaluate the final result and each agent's contribution.</li></ul>
<div class="box">Many tasks work best with one capable agent and good tools; prove the multi-agent version is better on your evals before adopting it.</div>
""", ["Multi-agent helps for large parallel work.", "Clear roles, shared state, a coordinator.", "Prove the benefit with evals."],
   "Design a 3-agent system for producing a weekly market newsletter and compare it with a single-agent design."),

  ("advanced", "Triggers, scheduling and cost control", "Run workflows automatically and within budget.", r"""
<h3>Triggers</h3><ul><li><b>Scheduled</b>: every morning, every Friday (cron, n8n schedule).</li><li><b>Event-driven</b>: new form submission, new support ticket, file uploaded, price change detected.</li><li><b>On demand</b>: a button, Slack command or chat request.</li></ul>
<h3>Cost management</h3><ul><li>Budget per run and per month; alert at 80%.</li><li>Route easy work to smaller models; cache; trim context.</li><li>Cap steps, retries and tool calls.</li><li>Track cost per successful task as a key metric.</li></ul>
""", ["Choose scheduled, event-driven or on-demand triggers.", "Set budgets and alerts.", "Measure cost per successful task."],
   "Define triggers and a monthly budget with alerts for 2 workflows you'd automate."),

  ("advanced", "Monitoring, observability and the final project", "Know when a workflow breaks or degrades, and fix it fast.", r"""
<h3>What to monitor</h3><table><tr><th>Signal</th><th>Example alert</th></tr><tr><td>Success rate</td><td>Runs succeeding fell below 95%</td></tr><tr><td>Quality</td><td>Sampled judge score dropped 5 points</td></tr>
<tr><td>Latency</td><td>p95 above 30 s</td></tr><tr><td>Cost</td><td>Daily spend above budget</td></tr><tr><td>Safety</td><td>Any unapproved action or injection flag</td></tr><tr><td>Drift</td><td>New topics or languages in inputs</td></tr></table>
<h3>Tools</h3><p>Traces and dashboards in Langfuse, LangSmith, Arize Phoenix or Braintrust; n8n execution logs; simple Google Sheet logs and Slack alerts for no-code workflows.</p>
<h3>Final project</h3><p>Build one end-to-end workflow (e.g. "new customer feedback → classify → summarise weekly → Notion report → Slack"), with routing, a checkpointed state table, one approval step, retries, a budget, a monitoring sheet and a 10-case eval. Demo it in 5 minutes.</p>
""", ["Monitor success, quality, latency, cost, safety, drift.", "Trace every run for debugging.", "Ship with alerts and an owner."],
   "Complete the final project."),
 ],
 "templates_html": """<h3>A. Workflow design sheet</h3><table><tr><th>Field</th><th>Fill in</th></tr><tr><td>Goal and trigger</td><td></td></tr><tr><td>Steps (pattern: chain / route / parallel / orchestrator)</td><td></td></tr><tr><td>Models per step</td><td></td></tr><tr><td>Tools</td><td></td></tr><tr><td>State and checkpoints</td><td></td></tr><tr><td>Approvals</td><td></td></tr><tr><td>Error recovery</td><td></td></tr><tr><td>Budget and limits</td><td></td></tr><tr><td>Monitoring and owner</td><td></td></tr><tr><td>Eval set</td><td></td></tr></table>
<h3>B. Run log</h3><pre>run_id | trigger | steps done | status | cost | latency | quality score | approvals | errors</pre>""",
 "cheat": [("Prompt chaining", "Sequential steps with checks"), ("Routing", "Classify then send to the right path or model"), ("Parallelisation", "Independent parts at once; or voting"),
           ("Orchestrator-workers", "Lead plans and delegates; combines results"), ("Evaluator-optimizer", "Draft → evaluate → improve loop with a cap"), ("Checkpoint", "Saved progress to resume after failure"),
           ("Idempotency", "Re-running doesn't duplicate actions"), ("Human-in-the-loop", "Approval or review by a person"), ("Observability", "Traces, logs and metrics to see what happened")],
 "qa": [("Workflow or agent?", "Workflow when steps are known and repeatable; agent when steps can't be predicted. Start simple and prove the agent is better with evals."),
        ("Explain routing.", "Classify each request and send it to the appropriate workflow or model, e.g. cheap model for FAQs, strong model for complex cases."),
        ("What is orchestrator-workers?", "A lead model breaks a task into sub-tasks, delegates to workers and synthesises their results."),
        ("How do you make long workflows reliable?", "State tracking, checkpoints, idempotent actions, retries with limits, approvals, alerts and monitoring."),
        ("When do you need multiple agents?", "Large parallel work needing different tools or context, and only when evals show it beats a single agent."),
        ("How do you control AI workflow cost?", "Budgets and alerts, routing to smaller models, caching, trimmed context, step and retry caps, and tracking cost per successful task."),
        ("What would you monitor in production?", "Success rate, sampled quality scores, latency, cost, safety events and input drift, with owners and alerts."),
        ("Where do humans fit?", "Before consequential actions, on low confidence or conflicts, and in sampled quality review.")],
 "glossary": [("Orchestrator", "Component that runs and connects steps"), ("Trigger", "Event or schedule that starts a workflow"), ("Backoff", "Waiting longer between retries"), ("Trace", "Record of every step in a run"), ("Drift", "Inputs or quality changing over time")],
 "links": [("Anthropic: Building effective agents", "https://www.anthropic.com/research/building-effective-agents"), ("Anthropic: Demystifying evals for AI agents", "https://www.anthropic.com/research/demystifying-evals-for-ai-agents"),
           ("n8n docs", "https://docs.n8n.io/"), ("LangGraph docs", "https://langchain-ai.github.io/langgraph/"), ("Langfuse docs", "https://langfuse.com/docs"), ("OpenAI Agents SDK", "https://openai.github.io/openai-agents-python/")],
}
