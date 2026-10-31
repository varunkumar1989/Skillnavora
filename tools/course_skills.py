"""Course: AI Skills & Templates: package your recurring work (Agent Skills, Projects, Custom GPTs, Gems, templates)."""
COURSE = {
 "slug": "ai-skills", "pdf": "AI_Skills_and_Templates.pdf", "page": "ai-skills.html",
 "title": "AI Skills & Templates", "kicker": "SkillNavora · AI Product Management & GenAI Launchpad · Skill 2 of 7",
 "intro": "Turn your recurring work into reusable AI skills and templates: Claude Agent Skills, Projects, Custom GPTs and Gems, PRD and report templates, a PM skill library, testing skills with evals, and a case study → PRD → presentation skill.",
 "oneline": "A skill is a reusable method you teach an AI once (instructions, templates, examples, scripts) so it does a recurring task the same good way every time. A tool gives the AI access or actions; memory and evals are parts of the system around it.",
 "tutor_q": "How do I create a reusable AI skill for writing PRDs?",
 "extra_btn": '<a class="btn btn-line" href="prd-library.html">PRD templates</a>',
 "cheat_title": "Skills cheat sheet",
 "classes": [
  ("basic", "Skills, tools, memory and evals: the system", "Know the parts of an AI assistant and where a skill fits.", r"""
<table><tr><th>Part</th><th>What it is</th><th>Example</th></tr>
<tr><td><b>Skill</b></td><td>A reusable method: instructions, templates, examples, scripts</td><td>"Write a PRD our way"</td></tr>
<tr><td><b>Tool</b></td><td>Access or an action the AI can take</td><td>Search Drive, query SQL, create a Jira ticket, browse a site</td></tr>
<tr><td><b>Context / memory</b></td><td>What the AI knows about you and the task</td><td>Your role, project brief, past decisions</td></tr>
<tr><td><b>Evals</b></td><td>Checks that outputs meet your standard</td><td>Every PRD has metrics with targets</td></tr></table>
<h3>Why skills matter for PMs</h3>
<ul><li>Consistency: every PRD, update and teardown follows the same high standard.</li><li>Speed: 2 hours → 20 minutes for recurring documents.</li><li>Scale: a team shares one "house style" skill.</li><li>Quality improves over time: fix the skill once, every future output improves.</li></ul>
<h3>Good candidates</h3>
<p>Anything you do weekly or that has a template: PRDs, stakeholder updates, user-interview synthesis, competitor teardowns, release notes, sprint reports, case-study write-ups.</p>
""", ["Skill = method; tool = access/action; memory = context; evals = checks.", "Package anything recurring.", "Improve the skill, not each output."],
   "List 10 recurring tasks in your work or studies; mark the 3 best candidates for a skill and why."),

  ("basic", "Templates: the foundation of every skill", "Design templates that make outputs consistent and complete.", r"""
<h3>Template anatomy</h3>
<ul><li><b>Fixed sections</b> with one-line guidance each.</li><li><b>Required fields</b> (owner, date, metric targets).</li><li><b>Examples</b> of a good section.</li><li><b>Checklist</b> at the end (quality bar).</li></ul>
<h3>Starter templates for PMs</h3>
<table><tr><th>Template</th><th>Key sections</th></tr>
<tr><td>PRD</td><td>Problem, goals/non-goals, users, stories, requirements, metrics, launch, risks</td></tr>
<tr><td>Weekly update</td><td>TL;DR + status, metrics, progress, risks/asks, next week</td></tr>
<tr><td>Interview synthesis</td><td>Participants, themes with quotes, surprises, opportunities</td></tr>
<tr><td>Product teardown</td><td>Users, jobs, flows, strengths, weaknesses, metrics guess, ideas</td></tr>
<tr><td>Decision brief</td><td>Decision needed, options, recommendation, trade-offs, owner, date</td></tr></table>
<p>SkillNavora has ready PRD, BRD and FRD templates (PRD library, BRD &amp; FRD guide) to start from.</p>
""", ["Templates = sections + guidance + examples + checklist.", "Start from proven templates; adapt to your team.", "The checklist becomes your eval."],
   "Create a weekly-update template with a 6-point quality checklist."),

  ("intermediate", "Where to build skills: Projects, GPTs, Gems and Agent Skills", "Choose the right place to package a skill.", r"""
<table><tr><th>Option</th><th>What you package</th><th>Best for</th></tr>
<tr><td>Saved prompt / text expander</td><td>A prompt you paste</td><td>Quick personal reuse</td></tr>
<tr><td>Claude Projects / ChatGPT Projects</td><td>Instructions + knowledge files</td><td>Ongoing work on one product or topic</td></tr>
<tr><td>Custom GPTs (ChatGPT) / Gems (Gemini)</td><td>Instructions, files, sometimes actions; shareable</td><td>Team assistants for one job</td></tr>
<tr><td><b>Agent Skills</b> (Claude)</td><td>A folder with SKILL.md instructions plus optional templates, examples and scripts; loaded only when relevant</td><td>Reusable methods across chats, Claude Code and the API</td></tr>
<tr><td>Automation (n8n, Make, code)</td><td>Steps + AI calls + tools</td><td>Scheduled or triggered workflows</td></tr></table>
<h3>Anatomy of an Agent Skill</h3>
<pre>prd-writer/
  SKILL.md          # name, description, step-by-step instructions
  template.md       # the PRD template
  examples/good-prd.md
  checklist.md      # quality bar used to self-review
  scripts/metrics_table.py   (optional helper)

--- SKILL.md ---
---
name: prd-writer
description: Writes a PRD in our house format from a case study or brief. Use when asked for a PRD or product spec.
---
1. Read the brief and list facts, assumptions and gaps.
2. Ask up to 5 clarifying questions if key facts are missing.
3. Fill template.md section by section; cite the brief for every number.
4. Self-review against checklist.md and fix gaps.
5. Output the PRD, then a list of open questions.</pre>
<p>The <b>description</b> matters: it tells the AI when to use the skill.</p>
""", ["Projects for ongoing context; GPTs/Gems for shareable assistants.", "Agent Skills package instructions + files + scripts, loaded when relevant.", "Write a clear description so the skill triggers at the right time."],
   "Draft a SKILL.md for 'stakeholder weekly update' with a description, 5 steps and a checklist."),

  ("intermediate", "Writing great skill instructions", "Write instructions that produce consistent, high-quality results.", r"""
<h3>Principles</h3>
<ul><li>Write steps in order, each with a clear output.</li><li>Say what to do when information is missing (ask, or mark "Assumption:").</li><li>Include one excellent example and, ideally, one bad example with why it's bad.</li>
<li>Define the quality bar as a checklist the AI must apply before finishing.</li><li>Keep it short; move long reference material into separate files.</li></ul>
<h3>Self-review checklist (PRD)</h3>
<pre>[ ] Problem backed by evidence from the brief
[ ] Goals have metric, baseline and target
[ ] Non-goals listed
[ ] Every P0 story has acceptance criteria
[ ] Numbers match the source exactly; author and product names correct
[ ] Risks have owners</pre>
""", ["Ordered steps, missing-info rules, examples, checklist.", "Keep the core short; reference files for detail.", "The checklist doubles as your eval rubric."],
   "Improve your SKILL.md from Class 3 with a missing-info rule, a good example and a checklist."),

  ("intermediate", "A PM skill library", "Build a set of skills that covers your core PM work.", r"""
<table><tr><th>Skill</th><th>Produces</th></tr>
<tr><td>Problem framing</td><td>Problem statement with evidence and assumptions</td></tr><tr><td>PRD creation</td><td>Requirements, scope, flows, metrics, risks</td></tr>
<tr><td>Persona and JTBD</td><td>Evidence-based personas and jobs-to-be-done</td></tr><tr><td>Journey mapping</td><td>Steps, pain points, opportunities</td></tr>
<tr><td>Prioritisation</td><td>RICE table and reasoning</td></tr><tr><td>Roadmap</td><td>Now/Next/Later with outcomes</td></tr>
<tr><td>Metrics design</td><td>North Star, inputs, guardrails</td></tr><tr><td>Experiment plan</td><td>Hypothesis, variants, sample size, decision rules</td></tr>
<tr><td>Product teardown</td><td>Structured analysis of a product</td></tr><tr><td>Launch plan</td><td>Readiness, rollout, comms</td></tr>
<tr><td>Stakeholder update</td><td>Audience-specific status and asks</td></tr><tr><td>Decision log</td><td>Decision, rationale, owner, follow-ups</td></tr>
<tr><td>Weekly product report</td><td>Progress, metrics, blockers, next steps</td></tr></table>
<p>Try many of these instantly in the free <b>SkillNavora AI PM Toolkit</b>, then turn your favourites into your own skills.</p>
""", ["Cover the PM lifecycle with 8–13 skills.", "Start with the 3 you use most.", "Share team skills; keep personal ones private."],
   "Pick 3 skills from the library and write a one-paragraph spec (input, output, quality bar) for each."),

  ("advanced", "Connecting skills to sources and tools", "Ground skills in your documents and let them act through tools.", r"""
<ul><li><b>Sources</b>: attach briefs, research and data via Projects, a second brain, or MCP connectors (Drive, Notion).</li>
<li><b>Tools</b>: let a skill create the Jira tickets, update Notion or draft slides, with approval before sending anything.</li>
<li><b>Scripts</b>: deterministic helpers inside a skill (e.g. compute RICE scores or validate a metrics table) so maths is exact.</li></ul>
<h3>Example flow</h3>
<p class="flow">Case-study PDF (source) → PRD skill (instructions + template) → metrics script (exact numbers) → self-review checklist → slide-outline skill → human review → share</p>
""", ["Ground skills in real sources.", "Use scripts for exact calculations.", "Approval before external actions."],
   "Connect one skill to a source folder (Project or Drive) and test it on 3 different inputs."),

  ("advanced", "Testing skills with evals", "Prove a skill works and stays working.", r"""
<h3>Eval set for a skill</h3>
<ul><li>10–30 realistic inputs (different case studies, messy briefs, missing info).</li><li>Checks: deterministic (author name, product name, required sections present, numbers match source) and rubric-based (clarity, evidence, visual quality of slides).</li>
<li>Run after every change to the skill (regression).</li></ul>
<table><tr><th>Check</th><th>Type</th></tr><tr><td>Author and company names exactly as in the brief</td><td>Code / exact match</td></tr><tr><td>All 10 PRD sections present</td><td>Code</td></tr>
<tr><td>Every metric has baseline and target</td><td>Code / judge</td></tr><tr><td>No numbers that aren't in the source</td><td>Judge (faithfulness)</td></tr><tr><td>Slides readable: ≤ 6 bullets, one message per slide</td><td>Judge / human</td></tr></table>
<p>See the SkillNavora <b>AI Evals for Product Managers</b> guide for graders and calibration.</p>
""", ["Every skill needs an eval set.", "Mix exact checks and rubric checks.", "Re-run on every change."],
   "Write 10 eval cases and 5 checks for your PRD skill."),

  ("advanced", "Project: case study → PRD → presentation skill", "Build a portfolio-ready reusable skill end to end (e.g. for a VitaFit-style assignment).", r"""
<h3>Brief</h3>
<p>You often receive a case study (for example, a fitness app like "VitaFit" wanting to improve retention) and must produce a PRD and a presentation. Build a reusable skill that does this from any case study.</p>
<h3>Deliverables</h3>
<ol><li><b>Skill folder</b>: SKILL.md, PRD template, slide-outline template, one good example, checklist.</li>
<li><b>Sources</b>: the case-study document(s) connected via Project, Drive or upload.</li>
<li><b>Steps</b>: extract facts → frame the problem → personas/JTBD → solution options + RICE → PRD → 10-slide outline with speaker notes.</li>
<li><b>Evals</b>: factual accuracy vs the case study, correct author and company names, metrics with baselines and targets, required sections, slide visual-quality rubric.</li>
<li><b>Results</b>: run on 3 different case studies; report pass-rates; fix and re-run.</li></ol>
<h3>Present it</h3>
<p>5-minute demo: the skill, one output, eval results before and after improvements. This shows interviewers you can build AI workflows, not just use chatbots.</p>
""", ["Skills + sources + evals = reliable AI workflow.", "Test on several case studies, not one.", "Show before/after eval results in interviews."],
   "Build the case study → PRD → presentation skill and run it on 3 case studies."),
 ],
 "templates_html": """<h3>A. Skill spec</h3><pre>Name:
When to use (description):
Inputs:
Steps (with outputs):
Templates/examples/scripts included:
Missing-information rule:
Quality checklist:
Eval set location:</pre>
<h3>B. SKILL.md skeleton</h3><pre>---
name: your-skill-name
description: What it does and when to use it.
---
# Steps
1.
2.
# Quality checklist
- [ ]</pre>
<h3>C. Skill eval log</h3><pre>version | date | change | cases | pass-rate | notes</pre>""",
 "cheat": [("Agent Skills (Claude)", "Folders with SKILL.md + files/scripts; loaded when relevant"), ("Claude / ChatGPT Projects", "Instructions + knowledge files for ongoing work"), ("Custom GPTs", "Shareable ChatGPT assistants with instructions and files"),
           ("Gemini Gems", "Custom Gemini assistants with instructions"), ("Template", "Fixed sections + guidance + examples + checklist"), ("Self-review checklist", "Quality bar the AI applies before finishing"),
           ("Description field", "Tells the AI when to use the skill"), ("Helper script", "Deterministic code for exact calculations"), ("Skill eval", "Test inputs + checks run after every change")],
 "qa": [("What is an AI skill?", "A reusable method (instructions, templates, examples, scripts) that makes an AI perform a recurring task consistently."),
        ("Skill vs tool?", "A skill is how to do something; a tool gives access or performs an action, such as search, database query or ticket creation."),
        ("How would you build a PRD skill?", "Template + ordered steps + missing-info rule + good example + checklist, connected to source docs, tested with an eval set, iterated on failures."),
        ("Projects vs Custom GPTs vs Agent Skills?", "Projects hold context for ongoing work; GPTs/Gems are shareable assistants; Agent Skills are modular methods loaded when relevant across surfaces."),
        ("How do you test a skill?", "Run it on 10–30 realistic inputs with exact checks (names, sections, numbers) and rubric checks (clarity, evidence), after every change."),
        ("Which PM tasks would you package first?", "The most frequent and template-driven: PRDs, weekly updates, interview synthesis and teardowns."),
        ("How do you avoid wrong numbers in AI documents?", "Require citations to the source, use helper scripts for calculations, and run faithfulness checks."),
        ("What makes skill instructions good?", "Ordered steps with outputs, rules for missing info, examples, a checklist and short core text with reference files.")],
 "glossary": [("SKILL.md", "Main instruction file of an Agent Skill"), ("Regression", "A drop in quality after a change"), ("House style", "Team's standard format and tone"), ("JTBD", "Jobs-to-be-done")],
 "links": [("Agent Skills documentation", "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview"), ("Anthropic: Building effective agents", "https://www.anthropic.com/research/building-effective-agents"),
           ("OpenAI: Creating a GPT", "https://help.openai.com/en/articles/8554397-creating-a-gpt"), ("Google: Gems in Gemini", "https://support.google.com/gemini"), ("SkillNavora PRD library", "https://www.skillnavora.in/prd-library.html")],
}
