"""Course: Prompt & Context Engineering (with structured outputs, task decomposition, documents/OCR, attribution, knowledge graphs)."""
COURSE = {
 "slug": "context-engineering", "pdf": "Prompt_and_Context_Engineering.pdf", "page": "context-engineering.html",
 "title": "Prompt & Context Engineering", "kicker": "SkillNavora · AI Product Management & GenAI Launchpad · Skill 1 of 7",
 "intro": "Make every AI request precise and evidence-based: clear instructions, the right context, structured outputs, task decomposition, long-context compression, reading documents and scans, citing sources and organising knowledge.",
 "oneline": "Prompt engineering is how you ask; context engineering is what the AI gets to see when it answers: your instructions, examples, documents, data, memory and tools. Getting both right is the first and most useful AI skill.",
 "tutor_q": "Teach me context engineering with a product manager example",
 "extra_btn": '<a class="btn btn-line" href="pm-toolkit.html">Practise in the AI PM Toolkit</a>',
 "cheat_title": "Patterns cheat sheet",
 "classes": [
  ("basic", "From prompts to context", "See why the information you give the AI matters more than clever wording.", r"""
<h3>Prompt vs context</h3>
<table><tr><th>Prompt engineering</th><th>Context engineering</th></tr>
<tr><td>The words of your request: task, role, format, tone, examples</td><td>Everything the model sees: system instructions, documents, data, chat history, memory, tool results</td></tr>
<tr><td>"Write a PRD for a bill-split app"</td><td>…plus your user-interview summary, metrics, constraints, PRD template and two example PRDs</td></tr></table>
<h3>The six building blocks of a strong request</h3>
<ol><li><b>Goal</b>: what you need and why ("so my VP can decide by Friday").</li><li><b>Audience</b>: who will read it.</li><li><b>Context</b>: facts, documents and data the AI must use.</li>
<li><b>Constraints</b>: length, scope, what to avoid, rules.</li><li><b>Format</b>: sections, table, JSON, slide outline.</li><li><b>Quality bar</b>: "cite the source for every number; say 'unknown' if not in the documents".</li></ol>
<h3>Before and after</h3>
<pre>Weak:   Summarise this survey.
Strong: You are helping a PM at a food-delivery startup in Pune.
        Goal: find the top 3 reasons users cancel orders, for a roadmap review.
        Use ONLY the attached survey (412 responses). Quote 2 responses per reason.
        Output: a table (reason, % of mentions, quotes), then 3 recommendations.
        If something isn't in the data, write "not in data".</pre>
<div class="box">Evidence-based requests ("use only these sources, cite each claim, flag gaps") are the single best defence against hallucinations.</div>
""", ["Context (documents, data, examples) usually matters more than wording.", "Goal, audience, context, constraints, format, quality bar.", "Ask for citations and 'not in data' when unsure."],
   "Rewrite three of your recent AI requests using the six building blocks, and compare the answers."),

  ("basic", "Prompt patterns that work", "Use proven patterns: examples, step-by-step, roles, critique and iteration.", r"""
<table><tr><th>Pattern</th><th>When</th><th>Example</th></tr>
<tr><td>Few-shot examples</td><td>You want a specific style or format</td><td>Give 2 good user stories, then ask for 10 more like them</td></tr>
<tr><td>Step-by-step</td><td>Reasoning, maths, analysis</td><td>"First list assumptions, then calculate, then give the answer"</td></tr>
<tr><td>Role and audience</td><td>Tone and depth</td><td>"Explain to a non-technical CFO in 120 words"</td></tr>
<tr><td>Delimiters</td><td>Separate instructions from data</td><td>Put documents inside &lt;doc&gt;…&lt;/doc&gt; tags</td></tr>
<tr><td>Critique and revise</td><td>Higher quality drafts</td><td>"Review your draft against this checklist, then improve it"</td></tr>
<tr><td>Ask me questions first</td><td>Ambiguous tasks</td><td>"Before writing, ask me up to 5 questions"</td></tr>
<tr><td>Negative constraints</td><td>Avoid common mistakes</td><td>"No jargon; don't invent metrics"</td></tr></table>
<h3>Iterate like a PM</h3>
<p>Treat prompts like product: version them, test them on 5–10 examples, keep what works. Save good prompts as templates (Class 3 of the AI Skills &amp; Templates course).</p>
""", ["Show examples of what good looks like.", "Separate instructions from data with clear delimiters.", "Version and test prompts like product features."],
   "Create a few-shot prompt that turns raw customer complaints into well-formed user stories; test it on 10 complaints."),

  ("intermediate", "Structured outputs: JSON, tables and fixed sections", "Get predictable output other tools and people can use directly.", r"""
<h3>Why structure</h3>
<p>Structured output can be pasted into Sheets, parsed by code, compared across runs and graded automatically (evals).</p>
<h3>Ways to get it</h3>
<ul><li><b>Describe the schema</b> in the prompt with an example.</li><li><b>Structured-output / JSON modes</b> in model APIs that enforce a schema.</li><li><b>Fixed document sections</b> for PRDs and reports: "Use exactly these headings".</li></ul>
<pre>Return ONLY JSON matching:
{ "theme": string, "mentions": integer, "severity": "low" | "medium" | "high",
  "quotes": [string, string], "source_rows": [integer] }
One object per theme, in an array, sorted by mentions.</pre>
<h3>Checks</h3>
<ul><li>Validate the JSON (does it parse? required fields present?).</li><li>Spot-check values against the source.</li><li>Keep field names stable across versions so dashboards don't break.</li></ul>
""", ["Structure makes outputs reusable and testable.", "Give a schema plus an example.", "Validate and spot-check structured output."],
   "Turn 30 app-store reviews into JSON themes using a schema, then load the JSON into a Google Sheet."),

  ("intermediate", "Task decomposition and chaining", "Break big jobs into steps the AI can do reliably.", r"""
<h3>Decompose</h3>
<p>One giant prompt ("research the market, write a PRD and make slides") gives shallow results. Break it into steps, each with a clear input and output:</p>
<p class="flow">1 Extract facts from sources → 2 Synthesise insights → 3 Frame the problem → 4 Draft PRD sections → 5 Check against rubric → 6 Make slide outline</p>
<h3>Rules for good steps</h3>
<ul><li>Each step has one job and a checkable output.</li><li>Pass only what the next step needs (keeps context small and focused).</li><li>Add a review step (human or AI checklist) before anything goes to stakeholders.</li></ul>
<h3>Where to run chains</h3>
<p>Manually in chat, in Claude or ChatGPT Projects, with Skills (packaged steps), or automated in n8n, Make or code (see Agent Orchestration &amp; Monitoring).</p>
""", ["Big tasks → small steps with checkable outputs.", "Pass only needed context between steps.", "Insert review steps before sharing."],
   "Decompose 'prepare a competitor teardown deck' into 6 steps with inputs and outputs for each."),

  ("intermediate", "Long context: compression, summaries and memory", "Keep long projects accurate when chats and documents get large.", r"""
<h3>Problems with long context</h3>
<ul><li>Important details get lost in very long chats ("context drift").</li><li>Cost and latency grow with every token sent.</li><li>Old, wrong information keeps influencing answers.</li></ul>
<h3>Techniques</h3>
<table><tr><th>Technique</th><th>How</th></tr>
<tr><td>Running summary</td><td>Every 20–30 messages, ask for a summary of decisions, facts and open questions; start a fresh chat with it</td></tr>
<tr><td>Project brief</td><td>A 1-page brief (goal, users, constraints, decisions) pinned in a Project</td></tr>
<tr><td>Retrieve, don't paste</td><td>Keep documents in a Project/second brain and let retrieval pick relevant parts</td></tr>
<tr><td>Compression with care</td><td>Ask the summary to keep numbers, names, dates and decisions exactly</td></tr>
<tr><td>Memory hygiene</td><td>Review stored memories; remove outdated facts</td></tr></table>
<pre>Summarise this conversation for a fresh chat. Keep exactly: decisions, numbers,
names, dates, open questions, and the current task. Max 250 words.</pre>
""", ["Long chats drift; summarise and restart.", "Pin a project brief; retrieve documents instead of pasting.", "Compression must keep numbers, names and decisions exact."],
   "Take a long chat from your work and write a 250-word handover summary; start a new chat with it and check nothing important was lost."),

  ("intermediate", "Documents, PDFs, scans and OCR", "Get reliable information out of PDFs, slides, spreadsheets and images.", r"""
<h3>Document ingestion</h3>
<ul><li>Modern assistants read PDFs, Word, slides and images directly; very long files may be chunked.</li><li>Tables in PDFs are error-prone: ask for the table as CSV and check totals.</li>
<li><b>OCR</b> (optical character recognition) reads text from scans and photos: invoices, handwritten notes, whiteboards. Vision models can also describe charts.</li></ul>
<h3>Extraction prompt</h3>
<pre>From the attached invoice images, extract: vendor, GSTIN, invoice no., date (DD-MM-YYYY),
items (name, qty, rate, amount), tax, total. Return CSV. If a field is unreadable,
write UNREADABLE (don't guess). Then check: do item amounts add up to the total?</pre>
<h3>Accuracy habits</h3>
<ul><li>Add arithmetic and cross-checks (totals, dates in range).</li><li>Spot-check 10% by hand; track error rate (that's an eval).</li><li>Mask personal data (Aadhaar, PAN, phone) before sharing documents with AI tools.</li></ul>
""", ["AI reads PDFs, slides and images; tables need checking.", "Ask for 'UNREADABLE' instead of guesses.", "Cross-check totals and spot-check samples."],
   "Extract data from 5 receipts or invoices (photos) into CSV and measure how many fields were correct."),

  ("advanced", "Source attribution, fact-checking and knowledge graphs", "Make AI outputs traceable to evidence and organise knowledge by relationships.", r"""
<h3>Attribution</h3>
<ul><li>Ask for citations per claim: document name + page/section, or a quote.</li><li>Use tools with built-in citations (NotebookLM, Claude citations, Perplexity) for research.</li>
<li>Verify: open the cited place and check it actually supports the claim (see the AI Evals course on faithfulness).</li></ul>
<h3>Fact-check prompt</h3>
<pre>For each claim in the draft below, label SUPPORTED / NOT FOUND / CONTRADICTED using
only the sources provided, and quote the supporting sentence.</pre>
<h3>Knowledge graphs in plain words</h3>
<p>A knowledge graph stores <b>things</b> (people, products, features, customers) and <b>relationships</b> between them ("Feature X requested by Customer Y", "Metric A depends on Metric B"). It helps answer connected questions: "Which enterprise customers asked for features that depend on the payments API?"</p>
<ul><li>Start simple: a table of entities and a table of relationships in Notion or Sheets.</li><li>AI can extract entities and relationships from notes and tickets.</li><li>Graph tools (e.g. Neo4j) and "GraphRAG" approaches combine graphs with retrieval for complex questions.</li></ul>
""", ["Every important claim should point to evidence.", "Use SUPPORTED / NOT FOUND / CONTRADICTED checks.", "Knowledge graphs capture relationships that plain search misses."],
   "Build a mini knowledge graph (entities + relationships table) from 10 customer tickets and ask AI 3 connected questions."),

  ("advanced", "Context engineering for products and agents", "Design what your AI feature or agent sees, and test it.", r"""
<h3>Context design for an AI feature</h3>
<table><tr><th>Layer</th><th>Decide</th></tr><tr><td>System instructions</td><td>Role, rules, refusals, tone, format</td></tr><tr><td>User and session</td><td>Profile, language, permissions, history summary</td></tr>
<tr><td>Knowledge</td><td>Which sources are retrieved, how fresh, how many chunks</td></tr><tr><td>Tools</td><td>Which tools are available and their descriptions</td></tr><tr><td>Examples</td><td>Few-shot examples of ideal answers</td></tr></table>
<h3>Common context failures</h3>
<ul><li>Too much irrelevant context (the model gets distracted).</li><li>Missing a key fact (answers become generic or wrong).</li><li>Conflicting instructions between system prompt and documents.</li><li>Untrusted content (web pages, emails) treated as instructions: prompt injection.</li></ul>
<h3>Test it</h3>
<p>Use an eval set (AI Evals course): vary the context (fewer chunks, more examples, shorter instructions) and measure quality, cost and latency. Pick the smallest context that meets the quality bar.</p>
<h3>Final project</h3>
<p>Write the context design for an AI feature (e.g. a Hinglish support bot): system prompt, retrieval plan, tools, 3 few-shot examples, a structured output schema, and a 20-case eval comparing two context versions.</p>
""", ["Design every layer the model sees.", "Less but relevant context beats more context.", "Measure context changes with evals."],
   "Complete the final project for an AI feature of your choice."),
 ],
 "templates_html": """<h3>A. Evidence-based request</h3><pre>Goal (and why):
Audience:
Use only these sources:
Constraints (length, scope, avoid):
Output format (sections / table / JSON schema):
Quality bar (cite each claim; write "not in data" if missing):</pre>
<h3>B. Handover summary</h3><pre>Decisions: · Facts and numbers (exact): · Names and dates: · Open questions: · Current task:</pre>
<h3>C. Context design sheet</h3><table><tr><th>Layer</th><th>Content</th><th>Size</th><th>Owner</th></tr><tr><td>System instructions</td><td></td><td></td><td></td></tr><tr><td>User/session</td><td></td><td></td><td></td></tr><tr><td>Knowledge (retrieval)</td><td></td><td></td><td></td></tr><tr><td>Tools</td><td></td><td></td><td></td></tr><tr><td>Examples</td><td></td><td></td><td></td></tr></table>""",
 "cheat": [("Few-shot", "Give examples of ideal outputs"), ("Delimiters", "Wrap data in tags or quotes to separate it from instructions"), ("Chain-of-thought / step-by-step", "Ask for reasoning steps before the answer"),
           ("Structured output", "JSON/table/sections with a schema"), ("Task decomposition", "Split work into checkable steps"), ("Prompt chaining", "Output of one step feeds the next"),
           ("Context compression", "Summaries that keep decisions, numbers and names"), ("RAG", "Retrieve relevant passages before answering"), ("OCR", "Read text from scans and images"),
           ("Attribution", "Link each claim to a source"), ("Knowledge graph", "Entities + relationships for connected questions"), ("Prompt injection", "Untrusted content trying to act as instructions")],
 "qa": [("Prompt vs context engineering?", "Prompting is the wording of the request; context engineering is designing all information the model sees: instructions, documents, data, memory, tools and examples."),
        ("How do you reduce hallucinations?", "Provide sources, restrict answers to them, ask for citations and 'not in data', use retrieval, and verify with fact-check evals."),
        ("Why use structured output?", "It makes outputs predictable, machine-readable, comparable and easy to grade; useful for dashboards, automation and evals."),
        ("What is task decomposition?", "Breaking a complex task into smaller steps with clear inputs and outputs, often chained, with review steps."),
        ("How do you handle very long chats?", "Summarise decisions and facts, start fresh with the summary, pin a project brief and retrieve documents instead of pasting everything."),
        ("How do you extract data reliably from PDFs or scans?", "Ask for a fixed schema, 'UNREADABLE' instead of guessing, arithmetic cross-checks, and measure accuracy on a sample."),
        ("What is a knowledge graph?", "A store of entities and their relationships that answers connected questions plain keyword or vector search may miss."),
        ("How do you decide how much context to give?", "Test variants against an eval set and choose the smallest context that meets quality, cost and latency bars."),
        ("What is prompt injection?", "Instructions hidden in untrusted content (web pages, emails, documents) that try to override yours; treat such content as data and limit tool permissions."),
        ("Give an evidence-based prompt for a PM task.", "Goal, audience, 'use only the attached survey', quote two responses per theme, table output, and 'not in data' for gaps.")],
 "glossary": [("Context window", "All text the model can see at once"), ("System prompt", "Standing instructions for the AI's role and rules"), ("Schema", "Definition of fields and types for structured output"),
              ("Chunk", "A piece of a document used for retrieval"), ("Citation", "Pointer from a claim to its source"), ("GraphRAG", "Retrieval that uses a knowledge graph")],
 "links": [("Anthropic: prompt engineering overview", "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"), ("Anthropic: effective context engineering for AI agents", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
           ("OpenAI: structured outputs", "https://platform.openai.com/docs/guides/structured-outputs"), ("Google: prompting guide (Gemini)", "https://ai.google.dev/gemini-api/docs/prompting-strategies"), ("Prompting Guide", "https://www.promptingguide.ai/"),
           ("Neo4j: what is a knowledge graph", "https://neo4j.com/blog/what-is-knowledge-graph/")],
}
