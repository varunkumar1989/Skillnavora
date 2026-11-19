"""Claude complete guide (checked against claude.com/docs and support.claude.com in November 2026)."""
from md import P, UL, OL, CODE, TABLE, NOTE, STEPS, MENU, K

CHECKED = "November 2026"
DOCS = "https://claude.com/docs"

L1 = {
    "slug": "apps-plans-models",
    "title": "Claude in November 2026: apps, plans and models",
    "lead": "Where Claude runs (web, desktop, phone, terminal, browser, Office, Slack), what the plans include, how to pick a model, and when to use Chat, Cowork or Claude Code.",
    "minutes": 15,
    "plain": "Think of Claude as one assistant with several desks. Chat is the front desk where you talk. Cowork is a back office where Claude works on files and websites while you do something else. Claude Code is the workshop where it writes and runs software. Your account, memory, skills and connectors follow you to every desk.",
    "ideas": [
        ("Claude", "Anthropic's AI assistant. One account works on the web, desktop, phone and in the terminal."),
        ("Chat", "The conversation view at claude.ai, in the desktop app and on mobile."),
        ("Cowork", "An agentic workspace in the desktop app: you describe an outcome and Claude does multi-step work on files, folders and websites."),
        ("Claude Code", "Claude for software work: it reads a codebase, edits files and runs commands, in the terminal, an IDE, the desktop app or the web."),
        ("Model", "The engine behind the answers. Bigger models reason more deeply; smaller ones are faster."),
        ("Customize", "The page that holds your connectors, skills and plugins, in claude.ai and the desktop app."),
    ],
    "flow": ["Sign in once", "Pick an app (Chat, Cowork, Code)", "Pick a model", "Add context (files, projects, connectors)", "Review and reuse"],
    "body": [
        ("Where Claude runs", TABLE(["App", "Best for", "How to get it"], [
            ["claude.ai (web)", "Everyday chat, research, writing, analysis, artifacts", "Sign in at claude.ai"],
            ["Claude desktop app", "Chat plus <b>Cowork</b> and <b>Code</b>, local files, desktop extensions", "Download from claude.com/download (macOS, Windows)"],
            ["Claude mobile app", "Chat on the go, voice, photos of documents, remote connectors", "App Store or Google Play"],
            ["Claude Code", "Building and fixing software: reads your repository, edits, runs tests", "Terminal, VS Code or JetBrains, the desktop app, or claude.ai/code"],
            ["Claude in Chrome", "Lets Claude act on websites (forms, research, repetitive clicks)", "Chrome extension, paired with Cowork"],
            ["Claude for M365", "Claude inside Excel, PowerPoint, Word and Outlook", "Office add-ins (work accounts)"],
            ["Claude Tag (Slack)", "Ask Claude in Slack channels and DMs with your team's tools", "Installed by a Slack and Claude admin"],
        ]) + P("Everything you add under <b>Customize</b> (connectors, skills, plugins) is saved to your account, so it appears on the web, desktop and phone. Claude Code picks it up when you sign in with the same account.")),
        ("Plans in plain words", P("Anthropic offers <b>Free</b>, <b>Pro</b>, <b>Max</b> and <b>Ultra</b> plans for individuals, and <b>Team</b> and <b>Enterprise</b> for organisations. Prices change and are shown in your currency at checkout, so check <a href=\"https://claude.com/pricing\" target=\"_blank\" rel=\"noopener\">claude.com/pricing</a> before you buy.") + TABLE(["Feature", "Free", "Paid personal (Pro, Max, Ultra)", "Team / Enterprise"], [
            ["Chat, file upload, web search", "Yes (lower limits)", "Yes, higher limits", "Yes"],
            ["Memory", "Yes, on by default", "Yes, on by default", "Owner decides for the organisation"],
            ["Search past chats", "No", "Yes", "Yes"],
            ["Projects", "Up to 5", "Yes", "Yes, shareable with teammates"],
            ["Skills you upload", "Check your plan page", "Yes", "Yes, can be shared or published to the org"],
            ["Plugins from the directory", "No", "Yes", "If the Owner keeps the directory on"],
            ["Cowork and Claude Code", "Check your plan page", "Yes", "Yes, with admin controls"],
        ]) + NOTE("Limits are measured in usage, not just messages. Long files, long chats and the biggest model use your allowance faster. Start a new chat when the topic changes.", "tip")),
        ("Choosing a model", P("Open the model menu under the message box. In November 2026 the current family is <b>Claude 5</b>: <b>Fable 5.2</b>, <b>Opus 5.5</b>, <b>Sonnet 5.5</b> and <b>Haiku 5.5</b>. Which ones you see depends on your plan.") + UL([
            "Use the most capable model your plan offers for hard reasoning: strategy memos, long analysis, tricky code.",
            "Use a balanced model for most daily work: emails, summaries, PRDs, data questions.",
            "Use the fastest, smallest model for quick, simple, repeated tasks.",
            "If an answer feels shallow, retry with a larger model or turn on extended thinking (where your plan shows it) before you rewrite the whole prompt.",
        ])),
        ("Chat, Cowork or Claude Code?", TABLE(["You want to…", "Use", "Why"], [
            ["Ask, draft, summarise, brainstorm", "Chat", "Fast back-and-forth, you stay in control of each step"],
            ["Turn a folder of files into a report, clean 40 spreadsheets, research and fill a web form", "Cowork", "Claude plans the steps, uses sub-agents, works on local files and websites, and comes back with finished work"],
            ["Build a website, fix a bug, write tests, review a pull request", "Claude Code", "Built for code: reads the repository, runs commands, uses Git"],
        ]) + P("The same skills, connectors and plugins work in all three, so a skill you write for chat also helps Cowork and Claude Code.")),
        ("Your first 15 minutes", STEPS([
            "Sign in at claude.ai (or install the desktop app) and open <b>Settings</b> from your initials in the lower left.",
            f"Under {MENU('Settings', 'Your Claude', 'Instructions')}, write three lines about you: role, what you are learning, how you like answers (for example \"short, with examples, Indian context\").",
            "Start a chat: \"I am a business analyst moving into product management. Make me a 4-week learning plan with one practice task per week.\"",
            "Ask a follow-up that improves it: \"Make week 2 about metrics and add one free resource per week.\"",
            f"Open {MENU('Customize', 'Connectors')} and look at what you could connect later (Google Drive, Gmail, Calendar, GitHub, Notion and more). You will connect one in Lesson 6.",
        ])),
    ],
    "mistakes": [
        ("Using one very long chat for everything", "Start a new chat per topic, or use a Project. Long chats are slower, cost more usage and mix topics."),
        ("Assuming Claude knows today's news", "Turn on web search or Research for anything recent, and ask for sources."),
        ("Pasting passwords or customer data", "Never paste secrets. Use connectors with your own sign-in, and follow your company's data rules."),
        ("Picking the biggest model for every small task", "Use a faster model for simple work; keep the largest for hard problems."),
    ],
    "practice": [
        "Write your Instructions for Claude in under 80 words and test them with two different questions.",
        "Ask the same question to two models from the menu and note differences in depth and speed.",
        "List three tasks from your week and decide whether each belongs in Chat, Cowork or Claude Code.",
    ],
    "quiz": [
        ("Where do you add connectors, skills and plugins?", "On the <b>Customize</b> page in claude.ai or the desktop app. They are saved to your account and appear on web, desktop and mobile."),
        ("Which app would you use to turn a folder of 30 PDFs into one formatted report while you do other work?", "Cowork, the agentic workspace in the desktop app. It plans the steps and works on local files."),
        ("Is memory available on the Free plan?", "Yes. Since 2026 memory is on by default for Free, Pro, Max and Ultra. On Team and Enterprise the Owner controls it."),
        ("Name the four models in the Claude 5 family listed in November 2026.", "Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5."),
    ],
    "links": [
        ("Claude docs home", f"{DOCS}/index"),
        ("Connectors, skills and plugins", f"{DOCS}/extend/overview"),
        ("Cowork overview", f"{DOCS}/cowork/overview"),
        ("Claude Code docs", "https://code.claude.com/docs/en/overview"),
        ("Claude pricing", "https://claude.com/pricing"),
    ],
}

L2 = {
    "slug": "everyday-chat",
    "title": "Everyday Claude: prompts, files, web search, research and artifacts",
    "lead": "A simple prompt formula, how to work with files and images, when to switch on web search or Research, and how artifacts turn answers into documents, apps and diagrams you can share.",
    "minutes": 20,
    "plain": "Briefing Claude is like briefing a smart new teammate who has never seen your company. The clearer the brief (who it is for, what good looks like, what to avoid), the less you need to correct afterwards.",
    "ideas": [
        ("Prompt", "Your instruction. Good prompts say the goal, the audience, the format and the limits."),
        ("Context", "Everything Claude can see in the conversation: your messages, files, project knowledge and connector results."),
        ("Web search", "Lets Claude look things up and cite pages. Use it for anything that changes over time."),
        ("Research", "A longer, multi-search investigation that returns a cited report. Takes minutes, not seconds."),
        ("Artifact", "A document, web page, chart, diagram or small app Claude makes in a side panel, which you can edit, reuse and share."),
        ("File creation", "Claude can produce real files such as Word documents, spreadsheets with formulas and slide decks."),
    ],
    "flow": ["Goal + audience", "Context (paste or attach)", "Format and limits", "Draft", "Critique and refine"],
    "body": [
        ("The 5-part prompt formula", P("Use <b>Goal, Audience, Context, Format, Limits</b>. You do not need all five every time, but the more that matters, the more you include.") + CODE("""Goal: Write a one-page PRD for a "save for later" button in our food app.
Audience: engineers and the design lead; they know the app well.
Context: 18% of users abandon carts at night; we want them to come back next day.
Format: headings Problem, Users, Solution, Success metrics, Risks. Max 350 words.
Limits: no jargon, no made-up numbers; mark assumptions as ASSUMPTION.""", "Example prompt") + P("Then improve it in conversation: <i>\"Make the metrics measurable and add a guardrail metric.\"</i> Asking for a critique is powerful too: <i>\"Act as a sceptical engineering manager and list the five weakest points of this PRD.\"</i>")),
        ("Working with files and images", UL([
            "Attach PDFs, Word files, spreadsheets, CSVs, images and screenshots with <b>+</b> in the message box, or drag them in.",
            "Ask for structure first: <i>\"List the sections of this report and the three numbers that matter most.\"</i> Then go deeper.",
            "For spreadsheets, ask Claude to analyse and chart the data; it can write and run code to do the maths instead of guessing.",
            "Photograph a whiteboard or handwritten notes on your phone and ask Claude to turn them into a clean summary with action items.",
            "Ask for a downloadable file when you need one: <i>\"Create an Excel file with this table and a SUM row.\"</i>",
        ]) + NOTE("Check numbers that matter. Ask: \"Show the calculation\" or \"Quote the exact sentence from the file that supports this.\"", "warn")),
        ("Web search and Research", TABLE(["Use", "When", "Example"], [
            ["No search", "General knowledge, writing, reasoning about your own files", "\"Rewrite this email to be friendlier.\""],
            ["Web search", "Facts that change: prices, laws, versions, news, job trends", "\"What changed in GitHub Copilot this month? Cite sources.\""],
            ["Research", "A multi-angle question worth a report", "\"Compare five no-code agent builders for a 10-person team in India: pricing, data residency, Hindi support.\""],
        ]) + P("Always ask for sources and open two or three of them yourself. If two sources disagree, ask Claude to show both and say which is newer.")),
        ("Artifacts: answers you can use", P("When you ask for something self-contained, such as a one-page plan, a landing page, a quiz, a flowchart or a calculator, Claude can build it as an <b>artifact</b> in a side panel. You can ask for changes (\"make the button green, add a reset\"), copy it, download it or share a link.") + UL([
            "Good artifact requests: interactive quiz for your team, a pricing calculator, a project timeline, a Mermaid flowchart of a process, a dashboard mock-up.",
            "Keep data private: anyone with a shared link can see what is in the artifact.",
            "Reuse: ask Claude to \"turn this into a template I can fill in each week\".",
        ])),
        ("Prompts you can copy", TABLE(["Role", "Prompt"], [
            ["Product manager", "\"Here are 40 app reviews. Group them into themes, count each theme, and give one quote per theme. Then suggest the top 3 problems to solve.\""],
            ["Data analyst", "\"This CSV has orders by city. Find the 3 cities with the biggest month-on-month drop and suggest 2 reasons to check for each.\""],
            ["Job seeker", "\"Compare my resume with this job description. List missing keywords and rewrite 3 bullets with numbers, without inventing facts.\""],
            ["Student", "\"Explain Git branches using a cricket team analogy, then give me 5 quiz questions with answers hidden.\""],
        ])),
    ],
    "mistakes": [
        ("Vague asks like \"make it better\"", "Say better for whom and how: shorter, more data, friendlier tone, for executives."),
        ("Trusting a statistic without a source", "Ask for the source, or use web search; mark unverifiable numbers as assumptions."),
        ("Uploading a 300-page file and asking one broad question", "Ask for an outline first, then work section by section."),
        ("Sharing an artifact link that contains private data", "Remove personal or company data before sharing."),
    ],
    "practice": [
        "Rewrite one of your real work requests using the 5-part formula and compare the result with your old prompt.",
        "Upload a spreadsheet and ask for one chart and three insights; verify one insight by hand.",
        "Run one Research question about your target job market and check three of its sources.",
        "Ask for an interactive quiz artifact on a topic you are learning and share it with a friend.",
    ],
    "quiz": [
        ("What are the five parts of the prompt formula in this lesson?", "Goal, Audience, Context, Format and Limits."),
        ("When should you switch on web search?", "For facts that change over time, such as prices, laws, software versions, news and job trends, and whenever you need sources."),
        ("What is an artifact?", "A self-contained output such as a document, web page, chart, diagram or small app that Claude builds in a side panel and you can edit, download or share."),
        ("How do you check a number Claude gives from a file?", "Ask it to show the calculation or quote the exact sentence from the file, and check key numbers yourself."),
    ],
    "links": [
        ("Prompt engineering overview (Anthropic)", "https://claude.com/docs/index"),
        ("Claude help centre", "https://support.claude.com"),
        ("SkillNavora: AI Builder Tools course", "ai-builder-tools.html"),
    ],
}

L3 = {
    "slug": "instructions-projects",
    "title": "Instructions, styles and Projects: teach Claude your context once",
    "lead": "Account-wide Instructions for Claude, writing styles, and Projects with their own files, instructions and memory, plus a simple rule for what goes where.",
    "minutes": 15,
    "plain": "Instructions are your standing note to Claude (\"I prefer short answers\"). A Project is a labelled folder for one piece of work, with its own reference files and rules. You set them up once and stop repeating yourself.",
    "ideas": [
        ("Instructions for Claude", "Account-wide guidance that applies to every conversation: your role, preferences and tone."),
        ("Project", "A workspace for one goal, with its own chats, files (project knowledge), instructions and memory."),
        ("Project instructions", "Rules that apply only to chats inside that project, such as \"answer as our support team\"."),
        ("Project knowledge", "Files you add to a project so every chat in it can use them."),
        ("Style", "A way of writing (for example concise or explanatory) you can choose for a response."),
    ],
    "flow": ["Instructions (who you are)", "Project (what this work is)", "Project files (reference)", "Chat (the task)"],
    "body": [
        ("Set your Instructions for Claude", STEPS([
            "Click your initials in the lower left and open <b>Settings</b>.",
            f"Go to {MENU('Your Claude', 'Instructions')} (in the older layout: {MENU('Account', 'Instructions for Claude')}).",
            "Write who you are, what you work on, the terms you use and how you like answers. Keep it short and specific.",
            "Save and test with a normal question. If Claude ignores something, make that line more concrete.",
        ]) + CODE("""I am a product analyst at a fintech in Bengaluru, learning AI product management.
Answer in plain English, short paragraphs, with one example from Indian apps.
Use INR and Indian number format (1,00,000). Say "I don't know" rather than guessing.
When I ask for a document, use headings and a summary at the top.""", "Example Instructions for Claude") + NOTE("Cowork's old \"Global instructions\" are now part of Instructions for Claude, so one place covers both.", "info")),
        ("Styles", P("Styles change <i>how</i> Claude writes without changing <i>what</i> it knows. Where your app shows a style option in the message box menu, you can pick a preset (such as concise, explanatory or formal) or create a custom style from writing samples you upload. Use a style for tone; use instructions for facts and rules about you.")),
        ("Create a Project", STEPS([
            "Select <b>Projects</b> in the sidebar, then <b>New project</b>. Give it a clear name, such as \"AI PM interview prep\".",
            "Add <b>project knowledge</b>: upload the job description, your resume, notes and a list of target companies.",
            "Write <b>project instructions</b>: \"You are my interview coach. Ask one question at a time, wait for my answer, then score it 1 to 5 with one improvement.\"",
            "Start chats inside the project. Each one sees the files and instructions, and the project builds its own memory.",
            "On Team and Enterprise plans you can share a project with teammates so everyone uses the same files and rules.",
        ]) + NOTE("Free accounts can create up to five projects, which is enough for one per goal.", "info")),
        ("Project memory and isolation", P("Each project has its own memory. Inside a project, Claude uses that project's memory plus your account memory from chats outside projects, but never another project's memory. For confidential work, open the project page and under <b>Memory</b> turn off <b>Use account memory</b>, so nothing from your personal chats leaks in.")),
        ("What goes where", TABLE(["Put it in…", "When", "Example"], [
            ["Instructions for Claude", "True for almost every chat", "Your role, language, tone, units"],
            ["A Project", "One ongoing goal with reference files", "Interview prep, a client account, a course you are taking"],
            ["Memory", "Things Claude learns as you talk, which you can review", "\"I am preparing for Razorpay APM interviews\""],
            ["A Skill (Lesson 5)", "A repeatable task done the same way every time", "Your weekly report format, a review checklist"],
            ["A Connector (Lesson 6)", "Live data from another app", "Your Google Drive, Calendar, GitHub, Notion"],
        ])),
    ],
    "mistakes": [
        ("Writing a two-page instruction block", "Keep instructions short; move task procedures into a skill and reference files into a project."),
        ("Mixing unrelated work in one project", "One project per goal. Create another project for a different client or course."),
        ("Putting confidential client files in a project that also uses account memory", "Turn off Use account memory for that project, or use a separate account if your company requires it."),
    ],
    "practice": [
        "Create a Project for one real goal, upload two reference files and write five lines of project instructions.",
        "Ask the same question inside and outside the project and compare the answers.",
        "Move one long paragraph from your Instructions into either a project or a skill, and explain why.",
    ],
    "quiz": [
        ("What is the menu path to Instructions for Claude in the new layout?", "Settings, then Your Claude, then Instructions."),
        ("Does a project see another project's memory?", "No. It uses its own memory plus account memory from non-project chats, unless you turn off Use account memory."),
        ("Where should a repeatable report format go: Instructions, a Project or a Skill?", "A Skill, because it is a task done the same way every time and loads only when needed."),
    ],
    "links": [
        ("Understanding Claude's personalization features", "https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features"),
        ("Chat search and memory", "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context"),
    ],
}

L4 = {
    "slug": "memory",
    "title": "Claude memory and chat search: what Claude remembers and how to control it",
    "lead": "How memory works in November 2026 (topics, not summaries), how to view, edit, pause and reset it, project memory, incognito chats, memory in Cowork, and admin controls for teams.",
    "minutes": 18,
    "plain": "Memory is Claude's notebook about you. As you chat, Claude writes short notes by topic (your role, your project, your preferences). You can open the notebook, edit or delete any page, pause it, or start fresh.",
    "ideas": [
        ("Memory", "Notes Claude saves as individual topics during chats, and uses in later chats."),
        ("Topic", "One saved memory entry, such as \"Career goal\" or \"Preferred report format\". You can read, edit or delete each one."),
        ("Chat search", "Claude can search your past chats (outside and inside projects) when you refer to earlier work. Paid plans."),
        ("Incognito chat", "A chat that is not saved to history, memory or search. Ghost icon in the upper right."),
        ("Pause memory", "Keeps what is saved but stops using it or adding to it."),
        ("Reset memory", "Permanently deletes all memory, including project memory."),
    ],
    "flow": ["You chat", "Claude saves a topic", "You review in Settings", "Edit, delete or pause", "Next chat uses it"],
    "body": [
        ("Who has memory", TABLE(["Plan", "Memory", "Chat search"], [
            ["Free", "On by default", "Not included"],
            ["Pro, Max, Ultra", "On by default", "Included"],
            ["Team, Enterprise", "The Owner decides. New organisations created from 31 October 2026 start with it on; older ones start off until each member turns it on", "Included"],
        ]) + P("Some organisations (HIPAA-enabled, government platforms, Claude for Teachers) do not start with memory on.")),
        ("How memory is stored", UL([
            "Claude saves memory as <b>individual topics</b> during your chats, not as a summary written after the chat ends.",
            "You can ask directly: <i>\"Remember that I am preparing for APM interviews at fintech companies.\"</i>",
            "Sensitive topics (such as health, politics or religion) are <b>not saved by default</b>. You can opt in with <b>Include sensitive topics in memory</b>.",
            "Some things are <b>never saved</b>: government ID numbers, criminal history, financial account numbers and immigration status.",
        ])),
        ("View, edit and delete memory", STEPS([
            f"Open {MENU('Settings', 'Your Claude')} (older layout: {MENU('Settings', 'Memory')}).",
            "Next to <b>Your memory</b>, select <b>Manage</b>. Your saved items are listed under <b>Topics</b>.",
            "Select a topic to read it, use the edit icon to correct it, or select <b>Delete</b>.",
            "Use the toggle menu for <b>Pause memory</b> (keep but do not use or add) or <b>Reset memory</b> (delete everything, including project memory).",
        ]) + P("You can also manage memory in conversation: <i>\"Forget my old job title\"</i>, <i>\"Update my target role to Data PM\"</i>, <i>\"What do you remember about my job search?\"</i>")),
        ("Chat search", P(f"On paid plans Claude can search your earlier chats when you say things like <i>\"continue the PRD we wrote last week\"</i>. Searches show up as tool calls so you can see what it looked at. To turn it off, open {MENU('Settings', 'Your Claude')} and switch off <b>Search and reference chats</b> (this also controls Claude Duet). Incognito chats are never searched.")),
        ("Control memory for one chat", UL([
            "<b>Incognito</b>: select the ghost icon in the upper right before you start. Nothing is saved to history, memory or search.",
            "<b>Memory off for one chat</b>: in a new chat open the <b>+</b> menu and turn off <b>Memory</b> before your first message. The chat stays in history and search. You cannot change this after the chat starts.",
            "<b>Projects</b>: each project has its own memory. Turn off <b>Use account memory</b> on the project page to isolate it completely.",
        ])),
        ("Memory in Cowork", P("Memory is shared between Chat and Cowork when Cowork runs in the cloud. Local Cowork sessions on your computer do not use memory. The memory setting is fixed when a task starts.")),
        ("Import, export and retention", UL([
            "You can import memories from other AI assistants, or export Claude's memory for backup (an experimental feature). Memory is also included in your data export.",
            "Deleting a conversation does <b>not</b> delete memory entries created from it. Delete those entries in Manage.",
            "Project memory is deleted when you delete the project.",
        ])),
        ("For Team and Enterprise owners", UL([
            f"Owners set the organisation-wide switch in {MENU('Organization settings', 'Capabilities')}. When it is off, Claude stops using and saving memory for everyone and members cannot turn it back on. Existing entries are kept.",
            "Owners cannot view or edit members' memories, and cannot turn memory on for one person.",
            "Each member must opt in to sensitive topics personally. Audit logs of owner memory changes are on Enterprise plans.",
            "A few older organisations still use legacy memory (a summary refreshed every 24 hours). It does not apply to Cowork.",
        ])),
    ],
    "mistakes": [
        ("Thinking that deleting a chat deletes what Claude remembered", "Open Manage under Your memory and delete the topic too."),
        ("Letting wrong or old facts stay in memory", "Review topics monthly and edit anything outdated, such as an old job title."),
        ("Discussing a confidential client in normal chats", "Use a project with account memory off, or an incognito chat."),
        ("Expecting Claude memory to follow you into ChatGPT or other tools", "Memory lives in your Claude account only. Use export or import if you switch."),
    ],
    "practice": [
        "Open Manage under Your memory and read every topic. Correct one and delete one you no longer want.",
        "Tell Claude one fact to remember, then start a new chat and check that it uses it.",
        "Start an incognito chat, share a test fact, then confirm in Manage that nothing new was saved.",
        "Create a project, turn off Use account memory, and confirm it does not know your personal preferences.",
    ],
    "quiz": [
        ("Does Claude save memory as a summary after each chat?", "No. In the current system it saves individual topics during chats. Only some older Team or Enterprise organisations use the 24-hour summary (legacy memory)."),
        ("What is the difference between Pause memory and Reset memory?", "Pause keeps existing memory but stops using and adding to it. Reset permanently deletes all memory, including project memory."),
        ("Which information is never saved to memory?", "Government ID numbers, criminal history, financial account numbers and immigration status."),
        ("Does local Cowork use memory?", "No. Memory is shared between Chat and Cowork only when Cowork runs in the cloud."),
        ("Can a Team Owner read a member's memory?", "No. Owners control the organisation switch but cannot view or edit individual memories."),
    ],
    "links": [
        ("Use Claude's chat search and memory (official)", "https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context"),
        ("Bringing memory to Claude (announcement)", "https://claude.com/blog/memory"),
    ],
}

L5_SKILL = """---
name: weekly-status-report
description: Write the weekly status report for a product or data team in the SkillNavora format. Use when the user asks for a weekly update, status report, weekly summary or progress report for a team or project.
---

# Weekly status report

Write the report in this order. Keep it under 300 words.

1. **Headline** - one sentence: on track, at risk, or off track, and why.
2. **Done this week** - 3 to 5 bullets, each with a measurable result.
3. **Next week** - 3 bullets with an owner name in brackets.
4. **Risks and asks** - each risk with impact (High, Medium, Low) and what help is needed.
5. **Metric snapshot** - fill the table in `assets/metrics-table.md`.

Rules:
- Use numbers from the user's notes only. If a number is missing, write "TBC", never guess.
- Plain English, no jargon. Indian number format for money (Rs 1,20,000).
- For tone, follow `references/tone.md`.
"""

L5 = {
    "slug": "skills",
    "title": "Claude Skills: teach Claude a task once and reuse it everywhere",
    "lead": "What a skill is, the SKILL.md format, a complete worked example you can copy, how to zip, upload and turn it on, how to test it with skill-creator, and how skills work in Cowork, Claude Code and the API.",
    "minutes": 25,
    "plain": "A skill is a recipe card. It says when to use it (the description) and the exact steps (the instructions), and can come with templates and small scripts. Claude keeps the card in a drawer and only takes it out when your request matches.",
    "ideas": [
        ("Skill", "A folder with a SKILL.md file of instructions, plus optional reference files, templates and scripts."),
        ("SKILL.md", "The one required file. YAML frontmatter (name, description) followed by plain Markdown instructions."),
        ("name", "Lowercase letters, numbers and hyphens, up to 64 characters. Must match the folder name."),
        ("description", "What the skill does and when to use it, up to 1,024 characters. Claude reads only this to decide whether to load the skill."),
        ("references/, assets/, scripts/", "Optional folders: background Claude reads when needed, templates it fills in, and code it runs."),
        ("Agent Skills specification", "The open format skills follow (agentskills.io), so the same skill can work in other tools that support it."),
    ],
    "flow": ["Write one-sentence job", "SKILL.md (name + description)", "Add steps, templates, scripts", "Zip the folder", "Customize > Skills: upload, turn on", "Test and refine"],
    "body": [
        ("When a skill is the right tool", TABLE(["Situation", "Use"], [
            ["You keep correcting Claude with the same instructions for a task", "<b>Skill</b>"],
            ["A report format, review checklist, multi-step procedure, or a task that needs a template or script", "<b>Skill</b>"],
            ["A one-off task", "Just describe it in the chat"],
            ["Live data from another service", "A <b>connector</b> (a skill can explain how to use one)"],
            ["Instructions for every conversation", "<b>Instructions for Claude</b> or project instructions"],
        ]) + P("Start by writing the task in one sentence plus what a good result looks like. That sentence becomes the description; the rest becomes the instructions.")),
        ("Folder structure", CODE("""weekly-status-report/
├── SKILL.md              # required: frontmatter and instructions
├── references/           # optional: background Claude reads when a step needs it
│   └── tone.md
├── assets/               # optional: templates and files Claude fills in
│   └── metrics-table.md
└── scripts/              # optional: code Claude runs
    └── check_numbers.py""", "A skill is a folder named after the skill")),
        ("A complete SKILL.md you can copy", CODE(L5_SKILL, "weekly-status-report/SKILL.md", "markdown") + UL([
            "The <b>description</b> includes the words people actually type (\"weekly update\", \"status report\"), so Claude recognises the request.",
            "Long material lives in <code>references/</code> and <code>assets/</code> and is mentioned at the step where it is needed, so the skill loads quickly.",
            "Keep SKILL.md under 500 lines. Never put API keys or passwords in a skill: everyone you share it with receives its files.",
        ])),
        ("Scripts inside a skill", P("Add a script when a step is more reliable as code (checking numbers, converting files, validating a format). Refer to it as <code>python3 ${CLAUDE_SKILL_DIR}/scripts/check_numbers.py</code>. Claude Code and Cowork replace <code>${CLAUDE_SKILL_DIR}</code> with the skill's folder; in chat on claude.ai the whole folder is copied into the code sandbox, so also keep the path readable relative to SKILL.md (<code>scripts/check_numbers.py</code>). In Claude Code, running a script is a shell command and asks your permission.")),
        ("Package it as a ZIP", P("The ZIP must contain the skill <i>folder</i> at the top level. A SKILL.md sitting at the root of the ZIP is not recognised.") + CODE("""cd ~/skills                      # the folder that CONTAINS weekly-status-report/
zip -r weekly-status-report.zip weekly-status-report/
unzip -l weekly-status-report.zip   # every line should start with weekly-status-report/""", "On macOS or Linux") + P("On Windows, right-click the <b>weekly-status-report</b> folder itself and choose <b>Compress to ZIP file</b> (not the files inside it).")),
        ("Upload, turn on and test", STEPS([
            f"Open {MENU('Customize', 'Skills')} in claude.ai or the desktop app.",
            "Upload the ZIP (or use the quick-create option and describe the skill in plain words so Claude drafts it with you).",
            "Turn the skill <b>on</b>.",
            "Send prompts that should trigger it, such as \"Here are my notes, write this week's status report\", and check Claude's thinking to confirm it loaded the skill.",
            "If it does not trigger, improve the description with the words you actually used.",
            "To run a skill yourself, type <b>/</b> in the message box and pick it from the list.",
        ]) + NOTE("Turn on <b>skill-creator</b> (listed as from Anthropic under Customize, Skills) and ask Claude to evaluate your skill. In Cowork and Claude Code it also runs the same prompts without the skill and shows pass rates, so you know the skill really helps.", "tip")),
        ("Skills Anthropic provides", P("Anthropic's skills repository (github.com/anthropics/skills) has working examples you can read and copy: <b>brand-guidelines</b> (instructions only), <b>internal-comms</b> (instructions plus examples), <b>pdf</b> (reference files and scripts) and <b>skill-creator</b>. Built-in document skills let Claude create Word, Excel, PowerPoint and PDF files. Copy the structure, not the contents.")),
        ("Skills across Claude", TABLE(["Where", "How skills get there"], [
            ["Chat (web, desktop, mobile)", "Upload or create in Customize, Skills; saved to your account"],
            ["Cowork", "Loads skills enabled on your claude.ai account at the start of each task"],
            ["Claude Code", f"Personal: {K('~/.claude/skills/<name>/SKILL.md')}; project: {K('.claude/skills/<name>/SKILL.md')} (commit it to share with the team); run with {K('/<name>')}; manage with {K('/skills')}"],
            ["Claude API", f"Create with the {K('/v1/skills')} endpoint and reference by skill ID. API skills do not sync with your claude.ai skills"],
            ["Team and Enterprise", "Open a skill in Customize, Skills and use <b>Share</b> or <b>Publish to org</b>"],
        ])),
        ("Five ideas for your first skills", UL([
            "<b>interview-answer-coach</b>: scores an answer with the STAR method and suggests one improvement.",
            "<b>sql-review</b>: checks a query for missing joins, NULL handling and performance, in your team's style.",
            "<b>linkedin-post</b>: turns a project into a post in your voice with a hook, three points and a question.",
            "<b>meeting-minutes</b>: decisions, owners and dates in a fixed table from any transcript.",
            "<b>invoice-checker</b>: compares an invoice with a purchase order and lists mismatches.",
        ])),
    ],
    "mistakes": [
        ("Zipping the files instead of the folder", "Zip the skill folder from its parent folder so every entry starts with the skill name."),
        ("A vague description like \"helps with reports\"", "Say exactly when to use it and include the words a request would contain."),
        ("Folder name different from the name field", "They must match, using lowercase letters, numbers and hyphens."),
        ("One giant skill for many workflows", "Make several focused skills; Claude can use more than one in a conversation."),
        ("Putting an API key inside a script", "Use a connector so each person signs in with their own account."),
    ],
    "practice": [
        "Build the weekly-status-report skill above, zip it, upload it and test it with your real notes.",
        "Write a second skill for a task you repeat weekly, then evaluate it with skill-creator.",
        "If you use Claude Code, copy one skill into ~/.claude/skills and run it with /its-name.",
    ],
    "quiz": [
        ("Which two frontmatter fields are required in SKILL.md?", "name and description."),
        ("What does Claude read to decide whether to load a skill?", "Only the description. The body is read after the skill loads."),
        ("Why do uploads fail when you zip the files inside the skill folder?", "Claude looks for <skill-name>/SKILL.md inside the ZIP. A SKILL.md at the root of the ZIP is not recognised."),
        ("Where do personal skills live for Claude Code?", "~/.claude/skills/<name>/SKILL.md (project skills go in .claude/skills/ in the repository)."),
        ("Do skills created with the API appear in claude.ai automatically?", "No. API skills are managed separately and do not sync across surfaces."),
    ],
    "links": [
        ("Create custom skills (official)", "https://claude.com/docs/skills/how-to"),
        ("Skills overview", "https://claude.com/docs/skills/overview"),
        ("Agent Skills specification", "https://agentskills.io/specification"),
        ("Anthropic skills repository", "https://github.com/anthropics/skills"),
        ("Skills in Claude Code", "https://code.claude.com/docs/en/skills"),
    ],
}

L6 = {
    "slug": "connectors-mcp",
    "title": "Connectors and MCP: connect Claude to Drive, Gmail, GitHub, Notion and more",
    "lead": "Add a connector from the directory, switch it on per chat, approve tool calls, set tool permissions, connect a custom MCP server by URL, install local desktop extensions, and stay safe.",
    "minutes": 18,
    "plain": "A connector is a key you hand Claude for one app, cut to fit only the doors you choose. With it Claude can read your calendar or open issues, and you decide each time whether it may act.",
    "ideas": [
        ("Connector", "A link from Claude to an outside app or service, so Claude can find information there and take actions for you."),
        ("MCP", "Model Context Protocol, the open standard connectors use. The service runs an MCP server; Claude connects to it."),
        ("Remote connector", "Runs on the internet; you sign in to the service. Works on web, desktop and mobile."),
        ("Local connector (desktop extension)", "Runs on your computer in the desktop app, packaged as an MCP Bundle (.mcpb)."),
        ("Tool permissions", "Per tool: Always allow, Needs approval, or Blocked."),
        ("Verified / Community", "Labels in the directory that tell you who reviewed a connector."),
    ],
    "flow": ["Customize > Connectors", "Discover and connect", "Sign in and approve access", "Turn on in a chat (+ > Connectors)", "Allow once / Always allow"],
    "body": [
        ("Add a connector from the directory", STEPS([
            f"Go to {MENU('Customize', 'Connectors')} (desktop app: <b>Customize</b> in the sidebar, then <b>Connectors</b>).",
            "Select <b>Discover</b>, search for a service (for example Google Drive, Gmail, Google Calendar, GitHub, Notion, Slack, Microsoft 365), and open its page. Check its <b>Verified</b> or <b>Community</b> label.",
            "Select <b>Connect to Claude</b>. Some connectors first ask for a server URL or region.",
            "Sign in to the service, review the access Claude asks for, and approve it.",
            "Back on the Connectors page it shows under <b>Your connectors</b> with the status <b>Connected</b>.",
        ]) + NOTE("On Team and Enterprise plans an Owner adds a connector for the organisation first. Members then see <b>Connect to Claude</b>; otherwise they see <b>Request</b>.", "info")),
        ("Use it in a conversation", STEPS([
            "In a chat, select <b>+</b> in the message box, then <b>Connectors</b>, and make sure the toggle for your connector is on.",
            "Ask for something the service holds: \"What is on my calendar tomorrow afternoon?\" or \"Summarise the open GitHub issues assigned to me.\"",
            "When Claude asks to use a tool, choose <b>Allow once</b> or <b>Always allow</b>.",
            "Turn the toggle off in the same menu to stop Claude using it in this chat. It stays connected for other chats.",
        ])),
        ("Manage permissions and disconnect", UL([
            f"Open {MENU('Customize', 'Connectors')} and select the connector under <b>Your connectors</b>.",
            "Under <b>Tool permissions</b> choose <b>Always allow</b>, <b>Needs approval</b> or <b>Blocked</b> for each tool group or single tool. A good default: read tools Always allow, write tools (send, delete, create) Needs approval.",
            "<b>Disconnect</b> signs Claude out of the service. <b>Remove</b> (three-dot menu) takes it off your account.",
            "If access expires, the row shows <b>Reconnect</b>.",
        ])),
        ("Where connectors work", TABLE(["App", "Supports"], [
            ["claude.ai web", "Remote connectors, including MCP Apps that show interactive content in the chat"],
            ["Desktop app", "Remote connectors plus local desktop extensions (.mcpb)"],
            ["Mobile app", "Remote connectors"],
            ["Claude Code", "Connectors you added in claude.ai, in the terminal and in cloud sessions, when signed in with the same account"],
            ["Cowork", "Connectors and plugins"],
        ])),
        ("Custom connectors and desktop extensions", P("If a service is not in the directory but gives you an MCP server URL, add it by URL from the Connectors page (\"Add a connector that isn't in the directory\"). To run a tool on your own computer, install a desktop extension (.mcpb file) in the desktop app. Only add servers from people you trust: a connector can read and act with the account you connect.")),
        ("Safety checklist", UL([
            "Connect with the least access you need, and prefer read-only first.",
            "Keep write actions on Needs approval until you trust the workflow.",
            "Watch for instructions hidden in documents or web pages (prompt injection). Claude should treat them as data, but you should still review actions before approving.",
            "Disconnect connectors you no longer use.",
        ]) + P("For a deeper, no-code explanation of MCP and three ways to use it, see the SkillNavora lesson <a href=\"data-science/lessons/agents-02-mcp-model-context-protocol-without-code-connect-claude-to-yo.html\">MCP without code</a>.")),
    ],
    "mistakes": [
        ("Setting every tool to Always allow on day one", "Allow read tools; keep send, delete and create on Needs approval."),
        ("Forgetting the toggle is per conversation", "Check + > Connectors in each chat."),
        ("Adding an unknown MCP server from a random website", "Use Verified connectors or servers from sources you trust."),
    ],
    "practice": [
        "Connect Google Calendar (or Outlook) and ask for a summary of next week with free slots for focused study.",
        "Connect Google Drive and ask Claude to find and summarise your three latest documents on one topic.",
        "Open the connector's Tool permissions and set every write action to Needs approval.",
    ],
    "quiz": [
        ("What do Allow once and Always allow do?", "Allow once approves this tool call only; Always allow skips the prompt for that tool from now on (changeable in Tool permissions)."),
        ("Which connector type works on mobile?", "Remote connectors. Local desktop extensions run only in the desktop app."),
        ("What file type is a local desktop extension?", "An MCP Bundle, a .mcpb file."),
        ("What is the difference between Disconnect and Remove?", "Disconnect signs Claude out but keeps the connector in your list; Remove takes it off your account."),
    ],
    "links": [
        ("Get started with connectors (official)", "https://claude.com/docs/connectors/getting-started"),
        ("Connectors directory", "https://claude.com/docs/connectors/directory"),
        ("Add a connector that isn't in the directory", "https://claude.com/docs/connectors/custom/add-unlisted"),
        ("Model Context Protocol", "https://modelcontextprotocol.io"),
    ],
}

L7 = {
    "slug": "plugins-cowork",
    "title": "Plugins and Cowork: install a whole toolkit and let Claude finish real work",
    "lead": "What a plugin contains (skills, connectors, commands, agents), how to find, add, use and remove one, build your own, and how Cowork, Claude in Chrome and Dispatch run multi-step tasks for you.",
    "minutes": 20,
    "plain": "If a skill is a recipe card and a connector is a key, a plugin is the full kitchen kit for one job: recipes, keys and helpers in one box you install once. Cowork is the kitchen where Claude can actually cook while you are away.",
    "ideas": [
        ("Plugin", "An installable package of skills, MCP connectors, commands and agents, added in one step and shareable."),
        ("Command", "A named action you run with /plugin-name:command (in chat it loads as a skill)."),
        ("Agent", "A specialist Claude delegates part of a task to. Runs in Cowork and Claude Code."),
        ("Marketplace", "A Git repository that lists plugins, which you can add to see its plugins."),
        ("Cowork", "The agentic workspace in the desktop app: works on local files, coordinates sub-agents and produces finished documents."),
        ("Dispatch", "Runs Cowork tasks in the background, including tasks you send from your phone."),
    ],
    "flow": ["Customize > Plugins", "Discover / Add marketplace / Upload", "Connect bundled connectors", "Use with / in chat, Cowork, Code", "Disable or remove if not useful"],
    "body": [
        ("What a plugin can contain", TABLE(["Component", "What it adds", "Where it works"], [
            ["Skills", "Instructions Claude follows when a task matches", "Chat, Cowork, Claude Code"],
            ["Commands", "Named actions: type /plugin-name:command", "Chat (as a skill), Cowork, Claude Code"],
            ["MCP connectors", "Access to an outside tool or data", "Chat, Cowork, Claude Code"],
            ["Agents", "Specialists for part of a task", "Cowork, Claude Code"],
        ]) + P("In Cowork and Claude Code some parts can run on your computer (agents, hooks, connectors marked <b>Runs in each session</b>). Anthropic reviews plugins in its directory; plugins you add from a marketplace URL or upload yourself are not reviewed, so add those only from sources you trust.")),
        ("Find and add a plugin", STEPS([
            f"Open {MENU('Customize', 'Plugins')}.",
            "<b>Discover</b>: browse plugins from Anthropic, the directory (Pro, Max, Ultra, Team, Enterprise) and your organisation. Open one to see what it contains, then select <b>Add</b>.",
            f"Or {MENU('Add', 'Add marketplace')}: enter a repository URL such as <code>https://github.com/your-org/your-plugins</code> or <code>owner/repo</code>.",
            f"Or {MENU('Add', 'Upload plugin')}: upload a .zip or .plugin file that holds one <code>.claude-plugin/plugin.json</code>.",
            "Open the plugin's <b>Connectors</b> tab. Each bundled connector shows <b>Connected</b>, <b>Not connected</b> (sign in here) or <b>Not added</b> (add, then connect).",
        ])),
        ("Use, update and remove", UL([
            "In chat, describe the task and Claude loads the matching skill, or type <b>/</b> and pick it (type the plugin name or <code>plugin-name:skill-name</code> to filter).",
            "In Cowork, type <code>/plugin-name:command</code> or describe the task. In Claude Code, type <code>/plugin-name:skill-name</code>; synced plugins load on the next session or after <code>/reload-plugins</code>.",
            "Turn a plugin off with its <b>Disable plugin</b> toggle, or open its menu and select <b>Remove</b>.",
            "Plugins from a marketplace or the directory update automatically from their source; use <b>Check for updates</b> for a marketplace you added.",
            "On Team and Enterprise, plugins can be <b>Installed by default</b> (you can turn it off) or <b>Required</b> (always on).",
        ])),
        ("Build your own plugin", P(f"From {MENU('Customize', 'Plugins', 'Add')} choose <b>Create with Claude</b> (Claude builds it with you in a conversation) or <b>Create a plugin</b> (an editor). As files, a plugin is a folder with a manifest:") + CODE("""my-team-toolkit/
├── .claude-plugin/
│   └── plugin.json        # name, description, version, author
├── skills/
│   └── weekly-status-report/
│       └── SKILL.md
├── commands/
│   └── standup.md         # becomes /my-team-toolkit:standup
├── agents/
│   └── reviewer.md        # a specialist for Cowork and Claude Code
└── .mcp.json              # connectors the plugin bundles""", "Typical plugin layout") + P("Check it with <code>claude plugin validate ./my-team-toolkit</code> in a terminal, share it with specific people or publish it to your organisation, and submit it to Anthropic's directory once it is polished.")),
        ("Cowork: delegate a whole task", UL([
            "Cowork runs in the Claude desktop app using the same agentic engine as Claude Code, without a terminal.",
            "It reads and writes <b>local files</b> in folders you choose, so you do not need to upload or download.",
            "Paired with <b>Claude in Chrome</b> it can work on websites: research, fill forms, collect data.",
            "It splits big work into <b>sub-agents</b> that run in parallel, and produces finished outputs such as Excel files with working formulas, PowerPoint decks and formatted documents.",
            "Use <b>Dispatch</b> to run tasks in the background, including ones you send from your phone, and Cowork <b>projects</b> to keep related tasks and files together.",
            "Cowork loads the connectors, skills and plugins enabled in <b>Customize</b> at the start of each task. It does not read Claude Code's local ~/.claude folder.",
        ]) + CODE("""In the folder "Q3 vendor quotes", read every PDF quote.
Make an Excel file comparing vendor, item, unit price, delivery days and payment terms,
with a column for total cost at 500 units and conditional formatting for the cheapest.
Then write a one-page recommendation in Word. Ask me before emailing anyone.""", "Example Cowork task") + NOTE("Cowork asks before actions that matter. Read its plan, keep sensitive folders out of its reach, and approve sending, deleting or purchasing one step at a time.", "warn")),
    ],
    "mistakes": [
        ("Adding a plugin from an unknown marketplace", "Prefer the reviewed directory or your organisation's plugins; read what a plugin contains first."),
        ("Expecting a plugin to sign you in to its apps", "Open its Connectors tab and connect each one."),
        ("Giving Cowork your whole home folder", "Share only the folder the task needs."),
    ],
    "practice": [
        "Add one plugin from Discover, open each tab (Skills, Commands, Connectors) and run one of its skills.",
        "Bundle the skill from Lesson 5 into a small plugin with Create with Claude.",
        "Give Cowork a real task on a copy of a folder, such as renaming and sorting 50 files, and review its plan before approving.",
    ],
    "quiz": [
        ("Which plugin component runs only in Cowork and Claude Code, not in chat?", "Agents."),
        ("What three ways can you add a plugin from Customize, Plugins?", "Discover, Add marketplace, and Upload plugin."),
        ("A bundled connector shows Not added. What do you do?", "Add it from the plugin's Connectors tab (or ask an Owner on Team/Enterprise), then connect it with your account."),
        ("What lets you send a Cowork task from your phone and have it run in the background?", "Dispatch."),
    ],
    "links": [
        ("Plugins (official)", "https://claude.com/docs/plugins/overview"),
        ("Build your first plugin", "https://claude.com/docs/plugins/quickstart"),
        ("Cowork overview", "https://claude.com/docs/cowork/overview"),
        ("Run tasks in the background with Dispatch", "https://claude.com/docs/cowork/guide/dispatch"),
    ],
}

L8 = {
    "slug": "claude-code-memory-skills",
    "title": "Claude Code for builders: CLAUDE.md memory, rules, skills, plugins and hooks",
    "lead": "How Claude Code remembers your project (CLAUDE.md, AGENTS.md, rules and auto memory), where files go, how to write good instructions, and how skills, plugins and hooks extend it.",
    "minutes": 22,
    "plain": "Every Claude Code session starts with a fresh mind. CLAUDE.md is the project handbook you leave on its desk each morning; auto memory is the notebook where Claude writes what it learned from your corrections.",
    "ideas": [
        ("CLAUDE.md", "Instructions you write for a project or for yourself; loaded at the start of every session."),
        ("AGENTS.md", "A shared instruction file many coding agents read. Claude Code reads it when there is no CLAUDE.md, or alongside it if configured."),
        (".claude/rules/", "Extra rule files, optionally scoped to file patterns with a paths field."),
        ("Auto memory", "Notes Claude writes itself from your corrections and preferences, per repository."),
        ("Skills and plugins", "Reusable procedures (/name) and installable packages, shared with your claude.ai account."),
        ("Hooks", "Commands that run on events (for example before a tool runs) and can block actions; enforced, unlike CLAUDE.md."),
    ],
    "flow": ["Managed CLAUDE.md (org)", "~/.claude/CLAUDE.md (you)", "./CLAUDE.md (team, in Git)", "CLAUDE.local.md (you, this repo)", "Auto memory + rules"],
    "body": [
        ("Where instructions live", TABLE(["Scope", "Location", "Shared with"], [
            ["Managed policy", "macOS <code>/Library/Application Support/ClaudeCode/CLAUDE.md</code>, Linux/WSL <code>/etc/claude-code/CLAUDE.md</code>, Windows <code>C:\\Program Files\\ClaudeCode\\CLAUDE.md</code>", "Everyone on the machine (set by IT)"],
            ["User", "<code>~/.claude/CLAUDE.md</code>", "Only you, all projects"],
            ["Project", "<code>./CLAUDE.md</code> or <code>./.claude/CLAUDE.md</code>", "The team, through Git"],
            ["Local", "<code>./CLAUDE.local.md</code> (add to .gitignore)", "Only you, this project"],
        ]) + P("Run <code>/init</code> in a repository to have Claude draft a CLAUDE.md from the code, and <code>/memory</code> to open and edit memory files.")),
        ("Write a CLAUDE.md that works", CODE("""# SkillNavora website

## Build and test
- Regenerate pages with `python3 tools/gen_site.py`; never hand-edit generated HTML.
- Before publishing: no broken internal links, no file over 25 MB, headless check of changed pages.

## Conventions
- Plain English, Indian number format, no model names in commit messages.
- Secrets live in Cloudflare settings, never in the repository.

## Where things are
- Lessons: tools/aiguides/*.py   Pages: generated into the repo root
@docs/architecture.md""", "Example project CLAUDE.md") + UL([
            "Target under 200 lines per file. Use headings and bullets; avoid contradictions.",
            "Write instructions you can verify (\"run X before committing\"), not wishes (\"write good code\").",
            "Import other files with <code>@path/to/file</code>; they load with the CLAUDE.md that references them.",
            "CLAUDE.md is guidance, not enforcement. To <i>block</i> an action, use a PreToolUse hook or permission rules.",
        ])),
        ("Rules for parts of the codebase", P("Put rules that only matter for some files in <code>.claude/rules/</code>, with a <code>paths</code> list in the frontmatter:") + CODE("""---
paths:
  - "src/api/**/*.ts"
---
# API rules
- Every endpoint validates input and returns typed errors.
- Add a test in tests/api for each new route.""", ".claude/rules/api.md")),
        ("AGENTS.md and other tools", P("If your repository already has an AGENTS.md (used by several coding agents), Claude Code reads it when there is no CLAUDE.md in your working folder or above. To keep one source for every tool, put <code>@AGENTS.md</code> inside CLAUDE.md so both are used.")),
        ("Auto memory", TABLE(["", "CLAUDE.md", "Auto memory"], [
            ["Who writes it", "You", "Claude"],
            ["Contains", "Instructions and rules", "Learnings and patterns from your corrections"],
            ["Scope", "Project, user or organisation", "Per repository, shared across worktrees"],
            ["Loaded", "Every session", "Every session (first 200 lines or 25 KB)"],
        ]) + P("Review auto memory now and then with <code>/memory</code>, and delete notes that are wrong or outdated.")),
        ("Skills, plugins and hooks in Claude Code", UL([
            f"Skills: {K('~/.claude/skills/<name>/SKILL.md')} for you, {K('.claude/skills/<name>/SKILL.md')} for the project. Run with {K('/<name>')}; manage with {K('/skills')}.",
            "Plugins: install from marketplaces with the <code>/plugin</code> command, or use plugins synced from your claude.ai account (run <code>/reload-plugins</code> after adding one on the web).",
            "Connectors you added on claude.ai are available in Claude Code when you sign in with the same account.",
            "Hooks: shell commands that run on events such as before a tool call; use them to block risky commands or run formatters automatically.",
            "Subagents: specialists defined as files in <code>.claude/agents/</code> that Claude delegates to.",
        ]) + P("The full Claude Code walkthrough (install, plan mode, permissions, MCP, hooks, subagents, automation) is in the SkillNavora lesson <a href=\"data-science/lessons/agents-05-claude-code-complete-tutorial-from-first-prompt-to-agents-mc.html\">Claude Code complete tutorial</a>.")),
    ],
    "mistakes": [
        ("A 600-line CLAUDE.md that nobody reads", "Keep it under 200 lines; move details into imported files or path-scoped rules."),
        ("Relying on CLAUDE.md to stop dangerous commands", "Use permission rules or a PreToolUse hook to enforce."),
        ("Committing CLAUDE.local.md with personal URLs", "Add CLAUDE.local.md to .gitignore."),
        ("Different instructions in CLAUDE.md and AGENTS.md", "Import AGENTS.md from CLAUDE.md so there is one source."),
    ],
    "practice": [
        "Run /init in a small repository and cut the draft CLAUDE.md to the 20 lines that matter.",
        "Add one path-scoped rule in .claude/rules/ and check that Claude follows it when editing those files.",
        "Copy your Lesson 5 skill into .claude/skills/ and run it with /its-name.",
    ],
    "quiz": [
        ("Which file holds your personal instructions for all projects?", "~/.claude/CLAUDE.md"),
        ("How do you include another file in CLAUDE.md?", "With an @path/to/file import."),
        ("Is CLAUDE.md enforced?", "No, it is context. Use permission rules or hooks to enforce behaviour."),
        ("How much of auto memory loads each session?", "The first 200 lines or 25 KB."),
    ],
    "links": [
        ("How Claude remembers your project (official)", "https://code.claude.com/docs/en/memory"),
        ("Skills in Claude Code", "https://code.claude.com/docs/en/skills"),
        ("Install plugins in Claude Code", "https://code.claude.com/docs/en/plugins/install"),
        ("Hooks guide", "https://code.claude.com/docs/en/hooks-guide"),
    ],
}

GUIDE = {
    "id": "claude",
    "title": "Claude Complete Guide",
    "subtitle": "Chat, Projects, memory, skills, connectors, plugins, Cowork and Claude Code",
    "checked": CHECKED,
    "hue": 265,
    "pdf": "handbook/Claude-Complete-Guide-Nov-2026.pdf",
    "intro": "Everything a working professional needs to use Claude well in November 2026, from your first chat to skills, plugins and Claude Code. Every menu path and limit was checked against Anthropic's official documentation this month.",
    "lessons": [L1, L2, L3, L4, L5, L6, L7, L8],
    "sources": [("Claude docs", "https://claude.com/docs"), ("Claude help centre", "https://support.claude.com"), ("Claude Code docs", "https://code.claude.com/docs")],
}
