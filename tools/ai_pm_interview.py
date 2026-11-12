"""AI PM interview guide: questions and model answers tied to the Part 2/3 job research.

Each question cites the job record IDs (research/part2_job_descriptions.csv) whose stated requirements it maps to.
Only J13 was opened in full; the rest are search summaries. Answers are general practice, not quoted from employers.
"""
import html
E = html.escape

# (section, intro, [(question, answer_html, evidence_ids)])
GUIDE = [
 ("1. Product sense and strategy", "Maps to: roadmap and strategy, customer research, vision to launch (J01, J05, J13, J15, J16).", [
  ("How would you decide whether a new AI feature belongs on the roadmap?",
   "<p>Start with the customer problem, not the model. Frame it as: who has the problem, how often, what do they do today, and what is it worth to fix. Then test AI fit with three checks: (1) is the task tolerant of occasional errors, (2) do we have or can we get the data, (3) is a non-AI solution clearly worse?</p><p>Size the opportunity, estimate cost per request and latency, name the main risk (quality, safety, cost), and propose the smallest experiment that would prove value. Close with the decision criteria: what result makes us build, pause or drop it.</p>", "J01 J13 J15"),
  ("Describe how you would take a product from vision to launch in a fast-moving, competitive space.",
   "<p>Vision (one sentence on the user outcome) → discovery (5-10 customer conversations, usage data) → bets (prioritised problems, each with a success metric) → prototype quickly with the real model on real examples → private beta with a tight feedback loop → staged rollout with guardrail metrics → post-launch review.</p><p>Say how you handle competition: you do not copy feature lists; you pick where you have an advantage (data, distribution, workflow depth) and ship the narrow thing that advantage supports first.</p>", "J13 J05"),
  ("How do you prioritise when everything is urgent?",
   "<p>Use one explicit framework (for example impact x confidence / effort, or RICE) and state the assumptions behind each number so stakeholders argue about inputs rather than rankings. Protect a share of capacity for reliability and technical debt. Tell stakeholders what is not being done and why.</p>", "J15"),
  ("Pick an AI product you use. What would you change and why?",
   "<p>Structure: user and job to be done → where it fails today (cite a concrete example) → proposed change → how you would measure it → what could go wrong. Keep to one change. Interviewers are looking for a clear opinion backed by a metric, not a list of ideas.</p>", "J07 J44"),
 ]),
 ("2. AI and ML fundamentals for PMs", "Maps to: ML / AI model lifecycle, AI tool proficiency, shipping 0-to-1 AI products (J01, J13, J43, J44).", [
  ("Explain the difference between prompting, RAG and fine-tuning, and when you would pick each.",
   "<p><b>Prompting</b>: change instructions and examples; cheapest, fastest, start here. <b>RAG</b>: retrieve relevant documents at request time and give them to the model; use when answers must be grounded in fresh or private knowledge and you need citations. <b>Fine-tuning</b>: train on examples to change style, format or narrow-task behaviour; use when prompting plateaus and you have good labelled data.</p><p>They combine: a common path is prompt first, add RAG for knowledge, fine-tune only if quality or cost still falls short.</p>", "J13 J43"),
  ("What is the ML model lifecycle and where does the PM add value?",
   "<p>Problem framing → data collection and labelling → training or model selection → evaluation → deployment → monitoring and retraining. The PM owns framing (is this the right problem, what is success), the evaluation definition (what 'good' means to users), the launch plan, and the monitoring metrics. The PM does not pick the architecture but should understand the trade-offs enough to challenge cost, latency and quality claims.</p>", "J13 J43"),
  ("Why do LLMs hallucinate, and what can a product do about it?",
   "<p>The model produces plausible next tokens; it has no built-in notion of truth. Product mitigations: ground answers in retrieved sources and show citations, constrain output formats, let the model say 'I don't know', add verification steps for high-stakes claims, keep a human in the loop where errors are costly, and measure hallucination rate on a fixed test set.</p>", "J13 J44"),
  ("How do you think about cost, latency and quality trade-offs?",
   "<p>They form a triangle. Quantify each: cost per successful task, p50/p95 latency, quality score from your eval set. Options: a smaller model for easy requests with a larger one as fallback, caching, shorter prompts, streaming to improve perceived latency. Decide with the user's tolerance in mind: a chat reply can take 3 seconds, an autocomplete cannot.</p>", "J07 J13"),
 ]),
 ("3. Agents and agentic products", "Maps to: agent frameworks (LangChain, LangGraph, AutoGen, CrewAI, n8n) named in J39, J42, J45; API agents (J08).", [
  ("What is an AI agent and how is it different from a chatbot?",
   "<p>A chatbot answers. An agent pursues a goal: it plans, calls tools (APIs, search, code), observes results and loops until done or blocked. The product implications are autonomy (what may it do without asking), reliability over many steps, permissions, and cost per task.</p>", "J39 J42 J45"),
  ("How would you decide how much autonomy to give an agent?",
   "<p>Rate each action by reversibility and blast radius. Read-only and reversible actions can run automatically; irreversible or external actions (sending email, spending money, deleting data) need confirmation or an approval policy. Start with human-in-the-loop, measure the approval rate, and loosen autonomy only where approvals are almost always accepted.</p>", "J39 J42"),
  ("What failure modes are specific to agents?",
   "<p>Compounding errors across steps, infinite loops, wrong tool choice, prompt injection through tool outputs, runaway cost, and silent partial completion. Mitigate with step and budget limits, tool permissions, structured logs of every step, task-level success metrics, and replayable traces for debugging.</p>", "J42 J45"),
  ("You are the PM for an API that lets developers build agents. What do you prioritise?",
   "<p>Developer time-to-first-success, reliability and clear error messages, stable versioned contracts, observability (traces), cost transparency, and good docs and examples. Metrics: time to first successful call, week-4 retention of API keys, error rate, support tickets per active developer.</p>", "J08 J28 J30"),
 ]),
 ("4. Evaluation, experimentation and metrics", "Maps to: SQL (6 records), experimentation (5), analytics dashboards (3), statistics (2) in the skill matrix.", [
  ("How do you evaluate the quality of an LLM-powered feature before launch?",
   "<p>Build a golden set of real, representative inputs with expected outcomes or rubrics, including hard and adversarial cases. Score with a mix of automated checks, an LLM judge (validated against human labels) and human review of samples. Track the score for every prompt or model change so regressions are caught before users see them. Define a launch bar in advance.</p>", "J02 J13"),
  ("Design an A/B test for a new AI-generated recommendation. What do you watch?",
   "<p>State the hypothesis and a single primary metric (for example conversion or task completion), plus guardrails (latency, error rate, complaints, cost). Randomise at the user level, compute sample size from the minimum effect worth detecting, run for full weekly cycles, and do not peek and stop early. Check for novelty effects and segment differences before shipping.</p>", "J15 J31 J32 J33"),
  ("Which metrics would you use for an AI assistant?",
   "<p>Outcome: task success rate, time saved. Engagement: weekly active users, retention. Quality: thumbs-up rate, edit distance of accepted outputs, escalation rate. Safety: policy-violation rate. Efficiency: cost per task, p95 latency. Pick one north-star and treat the rest as guardrails.</p>", "J14 J15 J35"),
  ("Write the query you would use to find week-1 retention. (SQL screen)",
   "<p>Describe the logic: take each user's first-activity date, join to activity in days 7-13 after it, and divide users who returned by users in the cohort, grouped by cohort week. Mention edge cases: users with no events, time zones, and the definition of 'active'. Interviewers check that you can structure the query and reason about the metric, not just recall syntax.</p>", "J14 J25 J26 J31"),
  ("A key metric dropped 8% last week. What do you do?",
   "<p>First check data integrity (logging, pipeline). Then segment: platform, geography, cohort, acquisition channel, feature. Check release and incident timelines and external factors (seasonality, competitor, outage). Form hypotheses, test the most likely, and report what you know, what you do not, and the next step.</p>", "J14 J15"),
 ]),
 ("5. Execution, stakeholders and requirements", "Maps to: requirements and user stories, cross-functional work, Agile, Jira (J05, J15, J24, J25, J36, J37).", [
  ("Write a short PRD outline for an AI feature.",
   "<p>Problem and users; goals and non-goals; success metrics and guardrails; user stories with acceptance criteria; AI-specific sections (data sources, quality bar and eval plan, failure handling, human oversight, cost and latency budget); rollout and rollback plan; open questions. Keep it to a few pages and link the eval set.</p>", "J05 J24 J25"),
  ("How do you work with engineers and researchers who disagree with your priorities?",
   "<p>Bring data and the customer problem, ask what they see that you do not, and make the trade-off explicit. Agree on a time-boxed experiment when evidence is missing. Decide, document the decision and the reason, and revisit it on a fixed date.</p>", "J01 J07 J13"),
  ("How do you handle ambiguity?",
   "<p>Turn it into a small number of testable assumptions, rank them by risk, and run the cheapest test for the riskiest one. Communicate what is known and unknown so the team can move without false certainty.</p>", "J07"),
  ("How do you run a release for an AI feature?",
   "<p>Staged rollout behind a feature flag (for example 5%, 25%, 100%), guardrail metrics watched at each stage, a go/no-go check against the launch bar, and a rollback trigger written before launch. See the release management section above.</p>", "J36 J37"),
 ]),
 ("6. Responsible AI, risk and domain", "Maps to: regulatory knowledge, payments/banking domain, safety-focused roles (J12, J17, J18, J20, J21).", [
  ("What responsible-AI risks would you check before launching an AI feature?",
   "<p>Harmful or biased outputs, privacy and data use, security (prompt injection, data leakage), copyright and provenance, over-reliance by users, and misuse by bad actors. For each: an owner, a test, a mitigation and a monitoring signal. Document them and review before each major change.</p>", "J12 J17"),
  ("You build an AI feature in a regulated domain such as banking or payments. How does your approach change?",
   "<p>Involve compliance and risk at discovery, not at launch. Require explainability and audit trails for decisions, stricter data handling, a human-review path for adverse outcomes, and slower, more conservative rollouts. Name the specific regulation relevant to the market and confirm requirements with the compliance team rather than assuming.</p>", "J17 J18 J19 J20 J21"),
  ("How would you reduce abuse on an AI product at scale?",
   "<p>Define abuse categories, build detection signals (rate, content, account age), tier responses (warn, throttle, block), keep an appeals path, and measure precision and recall of the detection plus the cost of false positives to legitimate users.</p>", "J12"),
 ]),
 ("7. Behavioural questions", "Prepare stories using the STAR format (situation, task, action, result), each with a number.", [
  ("Tell me about a product you shipped and what you would do differently.",
   "<p>Choose a real launch. State the goal metric, your role, one decision you got wrong, what the data showed, and the change you made. Own the mistake; interviewers discount stories where nothing went wrong.</p>", "J01 J07"),
  ("Tell me about a time you influenced without authority.",
   "<p>Show how you found the other party's incentives, used evidence, and reached an outcome both sides could live with. Include the result.</p>", "J01"),
  ("Why AI product management, and why this company?",
   "<p>Link one specific problem you care about to something concrete about the company's product. Avoid generic enthusiasm about AI; show that you use the product and have a view.</p>", "J07 J13"),
 ]),
]

def section():
    n = sum(len(q) for _, _, q in GUIDE)
    css = """<style>.iq{border:1px solid var(--line);border-radius:10px;margin:8px 0;background:var(--surface)}.iq summary{cursor:pointer;padding:11px 14px;font-weight:600}.iq .a{padding:0 14px 12px}.iq .ev{font-size:12px;color:var(--muted,#667);margin-top:6px}</style>"""
    out = [css, '<h2 class="sec-h ap-sec" id="interview-guide">Interview guide: questions and model answers</h2>',
           f'<div class="ap-note"><b>Basis.</b> {n} questions built from the skills named in the job records above. Only one posting (J13, Databricks) was opened in full; the others are search summaries, so the evidence tags are indicative, not a claim about what any interviewer will ask. Answers are general practice and model frameworks, not employer-provided. Use your own examples and numbers.</div>']
    for title, intro, qs in GUIDE:
        out.append(f'<h3 style="margin-top:22px">{E(title)}</h3><p class="sub">{E(intro)}</p>')
        for q, a, ev in qs:
            out.append(f'<details class="iq"><summary>{E(q)}</summary><div class="a">{a}<div class="ev">Job records: {E(ev)}</div></div></details>')
    return "\n".join(out)
