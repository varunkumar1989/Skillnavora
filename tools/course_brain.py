"""Course: Your AI Second Brain (basic to advanced), including context engineering and AI memory."""
COURSE = {
 "slug": "second-brain", "pdf": "AI_Second_Brain.pdf", "page": "ai-second-brain.html",
 "title": "Your AI Second Brain", "kicker": "SkillNavora · AI Product Management & GenAI Launchpad",
 "intro": "Capture everything you learn, organise it simply and ask AI questions across it: PARA and CODE methods, Notion, Obsidian and NotebookLM, context engineering and AI memory, meeting and reading pipelines, and building your own with MCP and automation.",
 "oneline": "A second brain is a personal knowledge system outside your head: notes, documents, meetings and ideas stored in one trusted place. With AI, it becomes something you can talk to: ask questions across everything you've saved and get answers with sources.",
 "tutor_q": "How do I build an AI second brain as a student or product manager?",
 "extra_btn": '<a class="btn btn-line" href="resources.html#learn-genai">Tools to start with</a>',
 "cheat_title": "Tools cheat sheet",
 "classes": [
  ("basic", "What a second brain is, and why AI changes it", "Understand the idea, the PARA and CODE methods, and what AI adds.", r"""
<h3>The problem</h3>
<p>We read, watch and hear more than we can remember: lectures, articles, meetings, WhatsApp forwards, PDFs. Most of it is lost, so we redo work and forget good ideas. A <b>second brain</b> is a trusted system outside your head where useful information is captured and can be found again.</p>
<h3>Two simple methods (Tiago Forte, <i>Building a Second Brain</i>)</h3>
<table><tr><th>CODE: the workflow</th><th>PARA: the folders</th></tr>
<tr><td><b>C</b>apture what resonates<br><b>O</b>rganise by where you'll use it<br><b>D</b>istil the key points<br><b>E</b>xpress: use it to create something</td><td><b>P</b>rojects: active, with a deadline (e.g. "Capstone PRD")<br><b>A</b>reas: ongoing responsibilities ("Career", "Health")<br><b>R</b>esources: topics of interest ("SQL", "AI evals")<br><b>A</b>rchive: finished or inactive</td></tr></table>
<h3>What AI adds</h3>
<ul><li><b>Ask, don't search</b>: "What did the client say about pricing in last month's calls?"</li>
<li><b>Auto-summaries</b> of long PDFs, videos and meetings.</li><li><b>Connections</b> between notes you forgot were related.</li>
<li><b>Drafting</b>: turn your notes into a PRD, blog post or interview answer in your own voice.</li></ul>
<div class="box">Rule: the second brain is for <b>using</b> knowledge, not hoarding it. If a note will never help a project, don't save it.</div>
""", ["Capture → Organise → Distil → Express.", "Organise by where you'll use information (PARA), not by topic perfection.", "AI turns notes into something you can question and reuse."],
   "List your current 'information mess': where your notes, files and bookmarks live today. Sketch PARA folders for your own life (2 projects, 3 areas, 5 resources)."),

  ("basic", "Capture: getting things into the system", "Set up fast, low-friction capture from phone, browser, reading and voice.", r"""
<h3>Capture tools</h3>
<table><tr><th>Source</th><th>Tool examples</th></tr>
<tr><td>Quick notes on phone</td><td>Notion, Obsidian mobile, Google Keep, Apple Notes</td></tr>
<tr><td>Web pages and articles</td><td>Notion Web Clipper, Obsidian Web Clipper, Readwise Reader, Pocket-style read-later apps</td></tr>
<tr><td>Highlights from books and PDFs</td><td>Readwise, Kindle highlights export</td></tr>
<tr><td>Voice thoughts</td><td>Voice notes → AI transcription (WhatsApp to self + AI, Otter, phone dictation)</td></tr>
<tr><td>Meetings and classes</td><td>Otter, Fireflies, Granola, built-in meeting summaries in Zoom, Teams and Meet</td></tr>
<tr><td>Screenshots</td><td>Save with a one-line note on why it matters</td></tr></table>
<h3>Capture rules</h3>
<ul><li>One <b>inbox</b>: everything lands in one place first.</li><li>Add one line: <i>why</i> you saved it and where you might use it.</li>
<li>Capture in 10 seconds or less, or you'll stop doing it.</li><li>Don't capture what you can easily find again (most of Google).</li></ul>
<h3>Choosing your main app</h3>
<table><tr><th>App</th><th>Best for</th></tr><tr><td>Notion</td><td>Databases, templates, sharing with teams; Notion AI built in</td></tr><tr><td>Obsidian</td><td>Private, local Markdown files, linked notes, many AI plugins</td></tr>
<tr><td>Google Drive + NotebookLM</td><td>PDFs and docs you already have; ask questions with citations</td></tr><tr><td>Claude / ChatGPT Projects</td><td>Topic workspaces with files and instructions for an AI assistant</td></tr></table>
""", ["One inbox, captured in under 10 seconds.", "Always note why you saved something.", "Pick one main app; don't spread across five."],
   "Install a web clipper and a voice-capture method. Capture 10 useful things this week with a one-line 'why' each."),

  ("basic", "Organise and distil", "Turn a pile of captures into findable, useful notes.", r"""
<h3>Weekly organising (20 minutes)</h3>
<ol><li>Empty the inbox: move each item into a PARA folder or delete it.</li><li>Rename notes with clear titles ("SQL window functions – examples").</li>
<li>Link related notes (Obsidian [[links]] or Notion relations).</li><li>Archive finished projects.</li></ol>
<h3>Progressive summarisation</h3>
<p>Layer 1: the saved text. Layer 2: <b>bold</b> the key passages. Layer 3: <mark>highlight</mark> the best of the bold. Layer 4: a 3-line summary in your own words at the top. AI can do a first draft of layers 2–4: "Summarise this in 3 bullets for a PM preparing for interviews."</p>
<h3>Note templates</h3>
<pre>Title:
Source / link:          Date:
Why I saved it:
Key points (3):
How I'll use it (project/area):
Related notes:</pre>
<h3>Tags vs folders vs links</h3>
<ul><li><b>Folders (PARA)</b> answer "where do I use this?"</li><li><b>Links</b> connect ideas across folders.</li><li><b>Tags</b>: keep to a few (e.g. #idea, #quote, #interview).</li></ul>
""", ["Weekly 20-minute review keeps the system alive.", "Summarise in your own words at the top of each note.", "Folders for use, links for ideas, few tags."],
   "Take 5 saved articles and apply progressive summarisation (ask AI for a draft, then edit it into your own words)."),

  ("intermediate", "Ask AI across your notes", "Use NotebookLM, Claude and ChatGPT Projects, Notion AI and Obsidian plugins to question your knowledge.", r"""
<h3>Tools that answer from your own files</h3>
<table><tr><th>Tool</th><th>How it works</th><th>Great for</th></tr>
<tr><td>NotebookLM</td><td>Upload PDFs, docs, links, videos; answers with citations; audio overviews</td><td>Exam prep, research, course notes</td></tr>
<tr><td>Claude Projects</td><td>Project knowledge files + custom instructions</td><td>PRDs, writing in your style, ongoing work</td></tr>
<tr><td>ChatGPT Projects</td><td>Files, instructions and chats grouped by project</td><td>Study plans, job search</td></tr>
<tr><td>Notion AI</td><td>Q&amp;A across your Notion workspace</td><td>Team wikis, meeting notes</td></tr>
<tr><td>Obsidian + AI plugins</td><td>Plugins (e.g. Smart Connections, Copilot for Obsidian) chat with your vault</td><td>Private personal notes</td></tr></table>
<h3>How it works: RAG in plain words</h3>
<p>Your notes are split into chunks, turned into "meaning fingerprints" (embeddings) and stored. When you ask a question, the most relevant chunks are found and given to the AI with your question, so it answers from <b>your</b> material and can cite it.</p>
<h3>Good questions to ask your second brain</h3>
<ul><li>"What are the 5 recurring complaints in my user-interview notes? Quote each."</li><li>"Make a revision quiz from my SQL notes, hardest first."</li>
<li>"What did I learn about pricing across all projects this year?"</li><li>"Draft a STAR answer about stakeholder conflict using my project notes."</li></ul>
<h3>Quality checks</h3>
<ul><li>Ask for citations and open them.</li><li>If the answer isn't in your notes, the AI should say so.</li><li>Keep sources clean and current; old notes give old answers.</li></ul>
""", ["NotebookLM and Projects answer from your files with citations.", "RAG = find relevant chunks + answer from them.", "Ask for quotes and sources; verify."],
   "Create a NotebookLM notebook (or Claude Project) with 5 of your study documents and ask 5 questions, including one whose answer isn't in the files."),

  ("intermediate", "Context engineering and AI memory", "Give AI the right context about you and your work, and manage what it remembers.", r"""
<h3>Why context matters</h3>
<p>An AI only knows what's in its <b>context window</b> (the text it can see right now) plus any <b>memory</b> features. Better context beats better prompts: the same question gives much better answers when the AI knows your role, goals, style and project.</p>
<h3>Layers of context</h3>
<table><tr><th>Layer</th><th>Where it lives</th><th>Example</th></tr>
<tr><td>Personal profile</td><td>Custom instructions / memory / a "about me" file</td><td>"I'm a 2nd-year PM aspirant in Pune; explain with Indian app examples; be concise"</td></tr>
<tr><td>Project brief</td><td>Project instructions + key files</td><td>Capstone PRD brief, user research summary, metrics</td></tr>
<tr><td>Task context</td><td>The prompt itself</td><td>"Rewrite section 3 for a VP audience in 150 words"</td></tr>
<tr><td>Retrieved knowledge</td><td>Second brain search (RAG)</td><td>Relevant interview quotes</td></tr></table>
<h3>Personal context file (template)</h3>
<pre>About me: role, experience, location, goals this quarter
How I like answers: length, format, tone, language
Current projects: name – goal – deadline – key files
Things to avoid: jargon, US-only examples, …
Glossary: company or course terms</pre>
<h3>Memory hygiene</h3>
<ul><li>Review and delete stored memories regularly (ChatGPT and Claude let you view and manage them).</li><li>Don't store passwords, bank details, Aadhaar or health data in AI memory.</li>
<li>Use separate projects for separate contexts (job search vs college vs work).</li><li>Long chats drift: start a fresh chat with a short summary when quality drops.</li></ul>
""", ["Context beats clever prompts.", "Keep a reusable personal context file and project briefs.", "Manage memory: review, delete, separate, never store secrets."],
   "Write your personal context file (1 page) and a project brief for one current project. Compare answers with and without them on the same question."),

  ("intermediate", "Pipelines: meetings, email, reading and learning", "Automatically feed your second brain from meetings, email and courses.", r"""
<h3>Pipelines that run themselves</h3>
<table><tr><th>Pipeline</th><th>How</th></tr>
<tr><td>Meetings → notes</td><td>Otter / Fireflies / Granola summary → automation saves to Notion "Meetings" with date, people, decisions, action items</td></tr>
<tr><td>Starred emails → tasks</td><td>Zapier / Make / n8n: Gmail star → Notion task with link</td></tr>
<tr><td>Highlights → notes</td><td>Readwise syncs book and article highlights to Notion or Obsidian</td></tr>
<tr><td>YouTube / courses → notes</td><td>Transcript → AI summary + 5 key takeaways + 3 quiz questions</td></tr>
<tr><td>Weekly digest</td><td>Every Friday: AI summarises the week's notes and open action items</td></tr></table>
<h3>A meeting-notes prompt</h3>
<pre>From this transcript, write:
1. Summary (5 bullets)  2. Decisions  3. Action items (owner, due date)
4. Open questions  5. Quotes worth keeping (with speaker)
Keep names exact; don't invent facts.</pre>
<h3>Weekly review checklist</h3>
<ul><li>Inbox to zero · update project statuses · review action items · archive finished work · pick 1 note to turn into something (post, PRD section, answer).</li></ul>
<p>Ask permission before recording meetings, and follow your company's policies on meeting data.</p>
""", ["Automate capture from meetings, email and reading.", "Structure summaries: decisions, actions, questions.", "Weekly review keeps it useful."],
   "Build one automation: starred Gmail → Notion task, or meeting summary → Notion page, using Zapier, Make or n8n."),

  ("advanced", "Second brains for PMs, students and teams", "Apply the system to product work, exam prep and team knowledge.", r"""
<h3>For product managers</h3>
<ul><li><b>Insight repository</b>: every user-interview quote tagged by theme and segment; AI finds patterns across 50 interviews.</li>
<li><b>Decision log</b>: date, decision, options, why, owner; ask "why did we choose X?" months later.</li><li><b>Metrics notebook</b>: definitions, dashboards, past experiments and results.</li>
<li><b>Interview bank</b>: STAR stories from your projects; AI drafts answers in your words.</li></ul>
<h3>For students and job seekers</h3>
<ul><li>One notebook per subject; AI makes quizzes, flashcards and summaries before exams.</li><li>Project portfolio notes ready for resumes and interviews.</li><li>Job-search tracker with company research and tailored resume points.</li></ul>
<h3>For teams</h3>
<ul><li>Shared wiki (Notion / Confluence) with AI search; owners for each page; review dates.</li><li>Onboarding: a new joiner can ask "how do we deploy?" and get the official answer with a link.</li>
<li>Permissions: AI should only see what each person is allowed to see.</li></ul>
<h3>Privacy and data protection</h3>
<p>Keep personal data of others (customers, classmates) out of personal tools unless allowed; follow the DPDP Act and company policy; prefer enterprise AI plans for work data; know where your files are stored.</p>
""", ["PMs: insight repository + decision log + interview bank.", "Students: notebooks per subject with AI quizzes.", "Teams: owned pages, permissions, privacy."],
   "Set up an insight repository with 10 real or sample interview quotes, tag them, and ask AI for the top 3 themes with supporting quotes."),

  ("advanced", "Build your own: MCP, automation and evaluation", "Connect AI assistants to your notes with MCP and automation, and make sure answers stay accurate.", r"""
<h3>MCP: connecting AI to your second brain</h3>
<p>The <b>Model Context Protocol (MCP)</b> lets assistants like Claude read and write in your tools: Notion, Google Drive, GitHub, Slack, or a folder of Obsidian notes. Example requests: "Find my notes on pricing and draft a 1-page summary in my Projects folder", or "Add today's meeting actions to my Notion task list".</p>
<h3>DIY architecture (for builders)</h3>
<p class="flow">Notes (Markdown / Notion / Drive) → chunk + embed → vector store → retrieve top matches → AI answers with citations → optional: write back new notes</p>
<p>No-code route: n8n or Make with an AI step and a vector-store node. Code route: Python with an embeddings model and a vector database (e.g. pgvector, Chroma).</p>
<h3>Evaluate your second brain</h3>
<ul><li>Write 20 questions you know the answers to; check if the AI finds the right note (retrieval) and answers faithfully (no invented facts).</li>
<li>Track: answer correct, source correct, "I don't know" when it should.</li><li>Fix by improving titles, summaries and chunking; remove outdated notes.</li></ul>
<h3>Final project</h3>
<p>Build your AI second brain for one area of your life (study, job search or a product): PARA structure, capture from 3 sources, one automation, a personal context file, an AI Q&amp;A setup (NotebookLM, Projects or MCP), and a 20-question accuracy check. Show it in a 5-minute demo.</p>
""", ["MCP connects assistants to your tools safely.", "DIY: chunk, embed, retrieve, answer with citations.", "Test with known questions; fix sources, not just prompts."],
   "Complete the final project and demo it to a friend or mentor."),
 ],
 "templates_html": """<h3>A. PARA starter</h3><pre>1 Projects/   Capstone PRD · Job search Q4 · SQL certification
2 Areas/      Career · Health · Finances · Learning
3 Resources/  AI evals · SQL · Product case studies · Interview stories
4 Archive/    Finished projects and old material</pre>
<h3>B. Personal context file</h3><pre>About me:
Goals this quarter:
How I like answers (length, format, tone, language):
Current projects (goal, deadline, key files):
Avoid:
Glossary:</pre>
<h3>C. Weekly review (20 minutes)</h3><table><tr><th>Step</th><th>Done</th></tr><tr><td>Inbox to zero</td><td></td></tr><tr><td>Update project statuses</td><td></td></tr><tr><td>Review action items</td><td></td></tr><tr><td>Archive finished work</td><td></td></tr><tr><td>Turn one note into output</td><td></td></tr><tr><td>Review AI memory and delete what's stale</td><td></td></tr></table>
<h3>D. Decision log</h3><pre>date | decision | options considered | why | owner | revisit date</pre>""",
 "cheat": [("Notion + Notion AI", "Databases, templates, team wiki; AI Q&A across the workspace"), ("Obsidian", "Local Markdown notes with links; AI plugins such as Smart Connections and Copilot for Obsidian"), ("NotebookLM", "Ask questions across uploaded sources with citations; audio overviews"),
           ("Claude Projects / ChatGPT Projects", "Workspaces with files, instructions and chats"), ("Readwise / Reader", "Highlights and read-later, synced to notes"), ("Otter / Fireflies / Granola", "Meeting transcription and AI notes"),
           ("Zapier / Make / n8n", "Automate capture pipelines"), ("MCP", "Standard way to connect AI assistants to your tools and data"), ("Embeddings + vector DB", "How AI finds relevant notes by meaning"),
           ("PARA", "Projects, Areas, Resources, Archive"), ("CODE", "Capture, Organise, Distil, Express"), ("Progressive summarisation", "Bold → highlight → summary layers on each note")],
 "qa": [("What is a second brain?", "A trusted external system for capturing, organising and reusing knowledge, so you don't rely on memory. With AI, you can ask questions across it and get cited answers."),
        ("Explain PARA and CODE.", "PARA organises by actionability: Projects, Areas, Resources, Archive. CODE is the workflow: Capture, Organise, Distil, Express."),
        ("How does AI answer from your notes?", "Retrieval-augmented generation: notes are chunked and embedded; the most relevant chunks are retrieved for a question and given to the model, which answers with citations."),
        ("What is context engineering?", "Designing what information the AI sees: personal profile, project brief, task instructions and retrieved knowledge. Good context usually improves answers more than prompt tricks."),
        ("How do you manage AI memory safely?", "Review and delete memories, keep projects separate, never store secrets or sensitive personal data, and prefer enterprise plans for work data."),
        ("How would a PM use a second brain?", "An insight repository of user quotes, a decision log, metrics and experiment notes, and an interview story bank, with AI finding patterns and drafting documents."),
        ("NotebookLM vs Claude Projects?", "NotebookLM is source-grounded Q&A over uploaded material with citations and audio overviews; Projects combine files with custom instructions for ongoing work and drafting."),
        ("What is MCP?", "The Model Context Protocol: a standard way for AI assistants to connect to tools and data (Notion, Drive, GitHub) to read and act with permission."),
        ("How do you know your AI second brain is accurate?", "Test with questions whose answers you know; check retrieval (right note), faithfulness (no invented facts) and correct 'I don't know' responses."),
        ("Biggest mistake people make?", "Hoarding without using: saving everything, never distilling or expressing. Fix it with a one-line 'why' on capture and a weekly review."),
        ("How do you automate capture?", "Meeting tools + automations into Notion, starred email to tasks, highlight syncing, and transcript summaries with structured prompts."),
        ("What data should never go into it?", "Passwords, bank and card details, Aadhaar, health records, and others' personal data without permission, per the DPDP Act and company policy.")],
 "glossary": [("Second brain", "External system for knowledge you want to reuse"), ("Context window", "The text an AI model can see at once"), ("Memory", "AI features that remember facts about you across chats"),
              ("Embedding", "Numeric 'meaning fingerprint' of text used for search"), ("Vector database", "Store for embeddings that finds similar meaning"), ("RAG", "Retrieval-augmented generation: answer from retrieved sources"),
              ("Inbox", "Single landing place for new captures"), ("Decision log", "Record of decisions with reasons"), ("MCP", "Model Context Protocol")],
 "links": [("Building a Second Brain (Tiago Forte)", "https://www.buildingasecondbrain.com/"), ("The PARA method", "https://fortelabs.com/blog/para/"), ("NotebookLM help", "https://support.google.com/notebooklm"),
           ("Claude Projects", "https://support.anthropic.com/"), ("Notion AI help", "https://www.notion.com/help/guides"), ("Obsidian help", "https://help.obsidian.md/"),
           ("Model Context Protocol", "https://modelcontextprotocol.io/"), ("Readwise", "https://readwise.io/"), ("n8n docs", "https://docs.n8n.io/")],
}
