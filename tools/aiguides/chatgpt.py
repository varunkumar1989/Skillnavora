"""ChatGPT complete guide (checked against OpenAI help-centre articles and announcements, November 2026).
OpenAI renames menus often; lessons give the concept first and the current menu name second."""
from md import P, UL, CODE, TABLE, NOTE, STEPS, MENU, K

CHECKED = "November 2026"
HELP = "https://help.openai.com/en/articles"

G1 = {
    "slug": "apps-plans-tools",
    "title": "ChatGPT in November 2026: apps, plans, models and built-in tools",
    "lead": "Where ChatGPT runs (web, desktop with Codex, phone, browser), what each plan includes, how to choose a model, and the built-in tools: search, deep research, canvas, images, voice and agent.",
    "minutes": 15,
    "plain": "ChatGPT is one assistant with a toolbox. You type a request, and it decides (or you choose) whether to just answer, search the web, write in a canvas, make an image, or act as an agent in a browser.",
    "ideas": [
        ("ChatGPT", "OpenAI's assistant, on the web (chatgpt.com), desktop, mobile and inside other apps."),
        ("Model picker", "The menu where you choose the model or mode (fast or thinking). Names change often, so read the short descriptions in the menu."),
        ("Search", "Looks up current information and cites sources."),
        ("Deep research", "A longer, multi-step investigation that returns a cited report."),
        ("Canvas", "A side-by-side editor for writing and code you can edit with ChatGPT."),
        ("Agent", "ChatGPT working on its own computer and browser to complete multi-step tasks, asking before important actions."),
    ],
    "flow": ["Pick a plan", "Open web, desktop or phone", "Choose model / mode", "Use a tool if needed", "Review sources and output"],
    "body": [
        ("Where ChatGPT runs", TABLE(["App", "Best for"], [
            ["chatgpt.com (web)", "Everyday chat, files, search, canvas, images, projects"],
            ["Desktop app (macOS, Windows)", "Chat plus <b>Codex</b> for coding (OpenAI merged the Codex app into the desktop app in July 2026), working with apps on your computer"],
            ["Mobile app", "Voice conversations, camera and photos, quick questions"],
            ["ChatGPT Atlas", "OpenAI's web browser with ChatGPT built in, including agent mode on web pages"],
            ["Codex", "Coding agent in the cloud, the terminal (Codex CLI), IDEs and the desktop app"],
        ])),
        ("Plans in plain words", P("OpenAI offers <b>Free</b>, <b>Go</b>, <b>Plus</b> and <b>Pro</b> for individuals, and <b>Business</b>, <b>Enterprise</b> and <b>Edu</b> for organisations. Higher plans give more usage, access to the most capable models, longer deep research and more agent runs. Prices and limits change; check <a href=\"https://chatgpt.com/pricing\" target=\"_blank\" rel=\"noopener\">chatgpt.com/pricing</a> for your country.") + NOTE("Business, Enterprise and Edu workspaces have admin controls: admins decide which plugins, apps and memory features members can use, and business data is not used for training by default.", "info")),
        ("Choosing a model or mode", UL([
            "Open the model picker at the top of the chat. You will usually see a fast option for everyday work and a thinking option that reasons longer for hard problems.",
            "Use the thinking mode for maths, multi-step analysis, careful code and planning; use the fast mode for drafts and quick answers.",
            "Model names change often (OpenAI released several new models in 2026), so read the one-line description in the picker rather than memorising names.",
        ])),
        ("Built-in tools", TABLE(["Tool", "Use it for", "Example prompt"], [
            ["Search", "Anything recent; cites sources", "\"What are the newest UPI rules for merchants? Cite official sources.\""],
            ["Deep research", "A report from many sources", "\"Research the AI PM job market in Bengaluru: top companies, skills asked, salary ranges, with sources.\""],
            ["Canvas", "Editing a long document or code together", "\"Open a canvas and draft my product case study; I will edit section by section.\""],
            ["Images", "Creating and editing images", "\"Make a clean infographic of the 5 steps of a Git workflow.\""],
            ["Data analysis", "Working with spreadsheets and CSVs using code", "\"Analyse this sales CSV and chart revenue by month.\""],
            ["Voice", "Talking hands-free, practising interviews", "\"Ask me five PM interview questions and give feedback after each.\""],
            ["Agent", "Multi-step tasks on websites", "\"Find three co-working spaces near Koramangala under Rs 8,000 a month and compare them in a table.\""],
        ])),
        ("Your first 15 minutes", STEPS([
            "Sign in at chatgpt.com and open your profile menu, then <b>Settings</b>.",
            f"Under {MENU('Settings', 'Personalization')}, add custom instructions (Lesson 2) and check that memory is set the way you want (Lesson 3).",
            "Ask: \"I am a data analyst. Give me a 4-week plan to learn GitHub, with one practice task per week.\"",
            "Turn on search and ask a question about something that changed this month; open two of the sources.",
            "Browse <b>Plugins</b> in the sidebar to see what you can connect (Lesson 4).",
        ])),
    ],
    "mistakes": [
        ("Treating an answer about recent events as current without search", "Turn on search and ask for sources and dates."),
        ("Using the thinking mode for every tiny task", "Use the fast mode for drafts; save thinking for hard problems."),
        ("Letting an agent buy or send things without checking", "Agents ask before important actions; read each step before you confirm."),
    ],
    "practice": [
        "Ask the same planning question in the fast and thinking modes and compare quality and time.",
        "Run one deep research report on your target role and verify three sources.",
        "Use canvas to rewrite your LinkedIn About section, editing one paragraph at a time.",
    ],
    "quiz": [
        ("Which app gained Codex in July 2026?", "The ChatGPT desktop app (OpenAI merged the Codex app into it)."),
        ("When should you use deep research instead of normal search?", "When you need a report that combines many sources and steps, not a quick fact."),
        ("Why read the model picker descriptions instead of memorising model names?", "Because OpenAI changes model names often; the descriptions tell you which is fast and which reasons longer."),
    ],
    "links": [
        ("ChatGPT release notes", f"{HELP}/6825453-chatgpt-release-notes"),
        ("ChatGPT pricing", "https://chatgpt.com/pricing"),
        ("OpenAI Academy", "https://academy.openai.com"),
    ],
}

G2 = {
    "slug": "custom-instructions-projects",
    "title": "Custom instructions, personality and Projects",
    "lead": "Tell ChatGPT who you are once, choose its tone, and organise work in Projects with their own files, instructions and project-only memory.",
    "minutes": 15,
    "plain": "Custom instructions are your standing brief. A Project is a dedicated room for one goal: its own files on the shelf, its own rules on the wall, and, if you want, its own memory that never leaves the room.",
    "ideas": [
        ("Custom instructions", "Account-wide text that tells ChatGPT about you and how to respond, applied to new chats."),
        ("Personality", "A preset tone (for example more concise or more friendly) you can choose in personalization settings."),
        ("Project", "A container for related chats, files and instructions."),
        ("Project instructions", "Rules that apply only inside one project and take priority over your global custom instructions."),
        ("Project-only memory", "A project setting that uses context only from chats inside that project, not your global memories."),
        ("Temporary chat", "A chat that does not use or create memories and is not kept in history."),
    ],
    "flow": ["Custom instructions (you)", "Project (the goal)", "Project files + instructions", "Chats inside the project"],
    "body": [
        ("Set custom instructions", STEPS([
            f"Open your profile menu, then {MENU('Settings', 'Personalization')}.",
            "Fill in what ChatGPT should know about you (role, goals, context) and how you want it to respond (length, tone, format).",
            "Optionally pick a <b>personality</b> preset for tone.",
            "Save. New chats use the instructions; existing chats keep their earlier context.",
        ]) + CODE("""About me: Business analyst in Pune moving into product management. I use Excel, SQL and Jira.
How to respond: Plain English, bullet points first, one Indian example, under 250 words unless I ask
for more. Show calculations. If you are not sure, say so and suggest how to check.""", "Example custom instructions")),
        ("Create a Project", STEPS([
            "Select <b>Projects</b> (or <b>New project</b>) in the sidebar and name it, for example \"Data PM job hunt\".",
            "Choose the memory mode when you create it: <b>default</b> (can use your saved memories) or <b>project-only</b> (uses only chats inside this project). You can change it later in project settings where your plan allows.",
            "Add files: resume, target job descriptions, notes. Every chat in the project can use them.",
            "Write project instructions: \"You are my interview coach. Ask one question at a time and score my answer out of 5.\"",
            "Start chats inside the project. Move existing chats in by dragging them or using the chat's menu.",
        ]) + NOTE("Shared projects switch to project-only memory automatically, so nobody's personal memory is exposed to collaborators. On Business, Enterprise and Edu, check with your admin which project features are on.", "info")),
        ("Which setting wins?", TABLE(["Setting", "Applies to", "Notes"], [
            ["Custom instructions", "All your chats", "Inside projects, project instructions take priority; on some Enterprise and Edu workspaces only project instructions apply in projects"],
            ["Project instructions", "Chats in that project", "Best place for task rules and roles"],
            ["Saved memory", "Chats that use memory", "Not used by project-only projects or temporary chats"],
            ["Temporary chat", "One chat", "No memory used or created, not kept in history"],
        ])),
    ],
    "mistakes": [
        ("Writing personal facts in project instructions you will share", "Keep personal context in custom instructions; share only task rules in the project."),
        ("Using one project for unrelated goals", "Create one project per goal so files and memory stay relevant."),
        ("Expecting old chats to pick up new instructions", "Start a new chat after you change instructions."),
    ],
    "practice": [
        "Write custom instructions in under 100 words and test them with two questions.",
        "Create a project with project-only memory, add two files and run an interview-practice chat.",
        "Compare an answer in a normal chat and in a temporary chat for the same question.",
    ],
    "quiz": [
        ("Where are custom instructions?", "Settings, then Personalization."),
        ("What does project-only memory do?", "The project uses context only from its own chats, not your global saved memories or other projects."),
        ("What happens to memory when you share a project?", "It switches to project-only memory automatically."),
    ],
    "links": [
        ("Projects in ChatGPT", f"{HELP}/10169521-projects-in-chatgpt"),
        ("Custom instructions", f"{HELP}/8096356-custom-instructions-for-chatgpt"),
        ("OpenAI Academy: Projects", "https://academy.openai.com/public/resources/projects"),
    ],
}

G3 = {
    "slug": "memory",
    "title": "ChatGPT memory: saved memories, chat history and how to control both",
    "lead": "The two memory settings (reference saved memories and reference chat history), how to view and delete what ChatGPT remembers, temporary chats, and privacy habits.",
    "minutes": 15,
    "plain": "ChatGPT has two kinds of memory. Saved memories are sticky notes you (or ChatGPT) deliberately pin up. Chat history is ChatGPT glancing back through your old conversations for useful context. You can turn each one off separately.",
    "ideas": [
        ("Reference saved memories", "Uses details ChatGPT has explicitly saved, often because you asked (\"remember that…\"). Kept until you delete them."),
        ("Reference chat history", "Lets ChatGPT use information from past chats. Less fixed: what it draws on can change over time."),
        ("Manage memories", "The list of saved memories in settings, where you can delete one or all."),
        ("Temporary chat", "Does not use existing memories or create new ones."),
        ("Project-only memory", "A project setting that keeps a project's context separate from your global memory."),
    ],
    "flow": ["You chat", "ChatGPT saves or recalls", "Settings > Personalization > Memory", "Delete or turn off", "Temporary chat for private topics"],
    "body": [
        ("Turn memory on or off", STEPS([
            f"Open {MENU('Settings', 'Personalization')} and find <b>Memory</b>.",
            "Switch <b>Reference saved memories</b> on or off.",
            "Switch <b>Reference chat history</b> on or off. Turning it off schedules what was remembered from past chats for deletion within 30 days; the chats themselves stay unless you delete them.",
            "Select <b>Manage memories</b> to see, delete one, or delete all saved memories.",
        ]) + NOTE("Deleting a chat does not delete a saved memory that came from it. To remove something completely, delete the saved memory in settings and the chat where you shared it.", "warn")),
        ("Use memory on purpose", UL([
            "Tell it: <i>\"Remember that I am preparing for data PM roles and I prefer examples from Indian fintech.\"</i>",
            "Ask: <i>\"What do you remember about me?\"</i> and correct anything wrong: <i>\"Forget my old company name.\"</i>",
            "Keep memory for stable facts (role, goals, preferences), not one-time details.",
        ])),
        ("Private conversations", UL([
            "Use a <b>temporary chat</b> for anything you do not want remembered or kept in history.",
            "Use a project with <b>project-only memory</b> for a client or confidential work.",
            "Never share passwords, card numbers, Aadhaar or PAN numbers, or customer data in any chat.",
            f"Check {MENU('Settings', 'Data controls')} for whether your chats help improve OpenAI's models, and turn that off if you prefer.",
        ])),
        ("ChatGPT memory compared with Claude memory", TABLE(["", "ChatGPT", "Claude"], [
            ["What is stored", "Saved memories plus reference to chat history", "Individual topics saved during chats; chat search on paid plans"],
            ["Where to manage", "Settings, Personalization, Memory, Manage memories", "Settings, Your Claude, Your memory, Manage"],
            ["Private chat", "Temporary chat", "Incognito chat (ghost icon)"],
            ["Per-project separation", "Project-only memory", "Project memory; turn off Use account memory"],
        ]) + P("Memory does not move between the two. If you switch, ask the old assistant to list what it remembers and paste the useful parts into the new one's instructions or memory.")),
    ],
    "mistakes": [
        ("Assuming deleting a chat removes the memory", "Delete the saved memory in Manage memories as well."),
        ("Never reviewing memories", "Open Manage memories monthly and remove outdated facts."),
        ("Discussing sensitive personal topics with memory on", "Use a temporary chat."),
    ],
    "practice": [
        "Open Manage memories and delete one outdated memory.",
        "Ask ChatGPT what it remembers about you, then correct one fact.",
        "Start a temporary chat, share a test fact, and check that it is not remembered later.",
    ],
    "quiz": [
        ("Name the two memory settings.", "Reference saved memories and reference chat history."),
        ("Does a temporary chat use your memories?", "No. It does not use existing memories or create new ones."),
        ("What happens when you turn off reference chat history?", "What was remembered from past chats is scheduled for deletion within 30 days; your chats remain unless you delete them."),
    ],
    "links": [
        ("Memory FAQ (OpenAI)", f"{HELP}/8590148-memory-faq"),
        ("What is memory and how do I turn it on or off", f"{HELP}/8983136-what-is-memory-and-how-do-i-turn-it-on-or-off"),
        ("Memory and new controls (announcement)", "https://openai.com/blog/memory-and-new-controls-for-ChatGPT"),
    ],
}

G4 = {
    "slug": "plugins-apps-connectors",
    "title": "Connect ChatGPT to other tools: plugins, apps and custom MCP servers",
    "lead": "The 2023 plugins, connectors, apps and the new Plugin directory explained in order; how to install a plugin and connect its app; using it in a chat; adding a custom MCP server; and staying safe.",
    "minutes": 20,
    "plain": "Since July 2026 a ChatGPT plugin is a box. Inside the box there can be apps (live connections to services like Google Drive or Notion, where you sign in) and skills (written know-how that needs no account). You install the box once, then connect the apps inside it.",
    "ideas": [
        ("Plugin (2026)", "A package in the Plugin directory that can contain apps, skills and app templates. Not the same as the 2023 plugins, which were discontinued."),
        ("App", "An integration with an outside service inside ChatGPT. Many need you to sign in (OAuth). Formerly called connectors."),
        ("Skill", "Written instructions and resources ChatGPT follows for a task; some plugins contain only skills."),
        ("MCP server", "A service that speaks the Model Context Protocol. You can add a custom one to connect your own tools."),
        ("Developer mode", "Settings for building and testing your own apps; custom MCP servers can now be added from Plugins directly."),
        ("Apps SDK", "OpenAI's kit for developers to build apps that show interactive content in ChatGPT."),
    ],
    "flow": ["Settings > Plugins", "Pick a plugin", "Install plugin", "Connect its app (sign in)", "Use it in a chat", "Review actions"],
    "body": [
        ("How the names changed", TABLE(["When", "What happened"], [
            ["2023", "The first ChatGPT <b>plugins</b> launched. OpenAI later discontinued them in favour of GPTs."],
            ["Nov 2023", "<b>GPTs</b>: custom versions of ChatGPT with instructions, knowledge files and actions."],
            ["2025", "<b>Connectors</b> let ChatGPT search and act in apps such as Google Drive, Gmail, GitHub and SharePoint, and developers could add MCP servers."],
            ["Dec 2025", "Connectors were renamed <b>apps</b>, with an app directory and the Apps SDK."],
            ["9 Jul 2026", "The app directory moved into the <b>Plugin directory</b>. Plugins became the main way to find workflow capabilities across ChatGPT and Codex. Existing app connections were not affected."],
            ["11 Dec 2026", "Scheduled retirement of <b>custom GPTs</b>; OpenAI's replacement is plugins (Lesson 5)."],
        ])),
        ("Install a plugin and connect its app", STEPS([
            f"Open {MENU('Settings', 'Plugins')} (or <b>Plugins</b> in the sidebar).",
            "Search or browse, then select the app you need or the plugin that includes it.",
            "Select <b>Install plugin</b> if shown.",
            "If prompted, select <b>Connect</b> and sign in to the service, then review and approve the access it asks for. Some apps need no separate sign-in.",
            "Plugins that contain only skills work straight away; others will not work until their required app is connected and authenticated.",
        ]) + NOTE("Whether you can install or use a plugin depends on your plan, workspace settings, role, region, device and the apps inside it. On Business and Enterprise, admins manage plugin installation in workspace settings and can disable apps.", "info")),
        ("Use a plugin in a chat", UL([
            "Ask normally and ChatGPT can choose a connected app when it helps: <i>\"Find the latest pricing deck in my Google Drive and summarise the changes.\"</i>",
            "Or pick it yourself from the tools (<b>+</b>) menu in the message box, or mention it by name in your prompt.",
            "Some apps show interactive content inside the chat (maps, product lists, forms).",
            "Before an app sends, deletes, books or buys something, check the action ChatGPT proposes and confirm only what you intended.",
        ])),
        ("Connect your own tool with a custom MCP server", STEPS([
            f"In {MENU('Settings', 'Plugins')}, choose to add a custom MCP server (you no longer need to turn on Developer mode first).",
            "Enter the server's URL and its sign-in details as the provider documents them.",
            "Read and acknowledge the risk warning shown for each server.",
            "Test it in a new chat with a read-only request before you allow any actions.",
        ]) + P("On workspace plans, custom apps may need admin approval. Only add servers you or your company run, or ones from providers you trust.")),
        ("Safety checklist", UL([
            "Connect with the least access you need; start with read-only use.",
            "Watch for instructions hidden in emails, documents or web pages (prompt injection). Review every action before confirming.",
            "Remove plugins and disconnect apps you no longer use.",
            "Keep customer and personal data out of apps your company has not approved.",
        ])),
    ],
    "mistakes": [
        ("Following an old guide that says \"enable plugins in Beta features\"", "Those 2023 plugins are gone; use Settings, Plugins."),
        ("Installing a plugin and expecting it to work without signing in", "Connect the app inside the plugin first."),
        ("Adding an unknown MCP server", "Only use servers you or trusted providers run, and read the warning."),
    ],
    "practice": [
        "Install one plugin that includes Google Drive or OneDrive and ask for a summary of a recent document.",
        "Find one plugin that contains only skills and try it.",
        "List the apps you have connected and disconnect any you do not use.",
    ],
    "quiz": [
        ("What can a 2026 plugin contain?", "Apps, skills and app templates."),
        ("What were apps called before December 2025?", "Connectors."),
        ("Do you still need Developer mode to add a custom MCP server?", "No; you can add one from Plugins directly, after acknowledging a risk warning."),
        ("Did existing app connections break when the Plugin directory launched?", "No. OpenAI says existing app connections were unaffected."),
    ],
    "links": [
        ("Apps in ChatGPT (OpenAI help)", f"{HELP}/11487775-apps-in-chatgpt"),
        ("Apps in ChatGPT and the Apps SDK", f"{HELP}/12503483-apps-in-chatgpt-and-the-apps-sdk"),
        ("Apps SDK for developers", "https://developers.openai.com"),
        ("Model Context Protocol", "https://modelcontextprotocol.io"),
    ],
}

G5 = {
    "slug": "gpts-skills",
    "title": "Custom GPTs, their retirement, and skills: what to build in 2026",
    "lead": "What custom GPTs are, the December 2026 retirement and how to migrate, skills in ChatGPT and Codex (the same SKILL.md format Claude uses), and how to choose between a project, a skill and a plugin.",
    "minutes": 18,
    "plain": "A custom GPT was a ChatGPT with its own job description and reference files. OpenAI is replacing GPTs with plugins and skills, which are more portable: a skill written as a SKILL.md file can work in ChatGPT, Codex, Claude and other tools that follow the same open format.",
    "ideas": [
        ("Custom GPT", "A configured ChatGPT with instructions, knowledge files, capabilities and optional actions (API calls)."),
        ("GPT retirement", "OpenAI's help centre lists 11 December 2026 as the scheduled date custom GPTs stop running, on all plans."),
        ("Migration", "Moving a GPT to a plugin. Custom actions do not transfer; rebuild them with a supported app or a custom MCP server."),
        ("Skill", "A folder with SKILL.md (name, description, instructions) and optional references and scripts."),
        ("Agent Skills standard", "The open SKILL.md format (agentskills.io) shared by Codex, Claude and many other tools."),
    ],
    "flow": ["List your GPTs", "Export instructions + files", "Rebuild as plugin / skill / project", "Rebuild actions as app or MCP", "Test, then share"],
    "body": [
        ("The GPT retirement timeline", TABLE(["Date", "What OpenAI's help centre says"], [
            ["26 Oct 2026", "New GPT creation ended for affected Enterprise workspaces (FedRAMP workspaces excluded)."],
            ["Until retirement", "Existing GPTs that are not migrated stay usable and editable. After you migrate one, the original becomes read-only."],
            ["11 Dec 2026", "Scheduled retirement: custom GPTs stop running. Migrated GPT links are planned to redirect to the replacement for people who have access."],
        ]) + NOTE("Dates can move. Check OpenAI's \"Custom GPT retirement and migration FAQ\" before you plan around them, and migrate the GPTs you depend on now rather than in December.", "warn")),
        ("Migrate a GPT step by step", STEPS([
            "Open each GPT you own in the editor and copy its <b>instructions</b>, conversation starters and the list of <b>knowledge files</b>. Download the files if you do not have copies.",
            "Decide the replacement: a <b>Project</b> (personal use with files), a <b>skill</b> (a repeatable procedure), or a <b>plugin</b> (share skills plus apps with others).",
            "Use OpenAI's migration workflow where it is offered for your GPT.",
            "Rebuild any <b>custom actions</b> (API calls). They do not transfer: use a supported app or a custom MCP server instead.",
            "Test the replacement with the same five questions you used to test the GPT, then share the new link with users.",
        ])),
        ("Skills in ChatGPT and Codex", P("Skills work inside ChatGPT and Codex. Find them under <b>Plugins</b> in the sidebar on the <b>Skills</b> tab. A skill uses the same open format as Claude skills:") + CODE("""---
name: release-notes
description: Turn merged pull requests into customer-friendly release notes. Use when the user asks for release notes, a changelog or "what's new".
---

# Release notes
1. Group changes into New, Improved and Fixed.
2. One line each, in plain words, starting with a verb.
3. Skip internal refactors and dependency bumps.
4. End with "Thanks to" and the contributors' names.""", "release-notes/SKILL.md") + UL([
            f"In Codex, repository skills go in {K('.agents/skills/<name>/SKILL.md')} and personal skills in {K('~/.agents/skills/')} (older guides mention {K('~/.codex/skills')}, now legacy).",
            "Codex loads only each skill's name and description at start, and reads the body when it decides to use the skill, the same idea as Claude.",
            "OpenAI publishes a <b>skill-creator</b> skill (github.com/openai/skills) that drafts the folder and SKILL.md for you.",
            "Because the format is shared, the skill from the Claude guide (Lesson 5) can be reused here with little or no change.",
        ])),
        ("Project, skill, plugin or app?", TABLE(["Need", "Choose"], [
            ["Personal workspace with files and rules for one goal", "<b>Project</b>"],
            ["A procedure done the same way every time (format, checklist, steps)", "<b>Skill</b>"],
            ["Live data or actions in another service", "<b>App</b> (or a custom MCP server)"],
            ["Share skills and apps with a team as one install", "<b>Plugin</b>"],
            ["An old custom GPT", "Migrate to one of the above before 11 Dec 2026"],
        ])),
    ],
    "mistakes": [
        ("Waiting until December to migrate important GPTs", "Copy instructions and files now and test the replacement early."),
        ("Expecting GPT actions to move automatically", "Rebuild them as an app connection or custom MCP server."),
        ("Writing a skill description that does not match how people ask", "Include the phrases users actually type."),
    ],
    "practice": [
        "List every GPT you use, and choose its replacement (project, skill, app or plugin).",
        "Write a SKILL.md for one weekly task and test it in ChatGPT or Codex.",
        "Reuse the same skill in Claude and compare results.",
    ],
    "quiz": [
        ("When are custom GPTs scheduled to stop running?", "11 December 2026, according to OpenAI's help centre (check the FAQ for changes)."),
        ("Do GPT custom actions transfer when you migrate?", "No. Rebuild them with a supported app or a custom MCP server."),
        ("Where do repository skills live for Codex?", ".agents/skills/<name>/SKILL.md"),
        ("Why can the same SKILL.md work in Claude and Codex?", "Both follow the open Agent Skills format (agentskills.io)."),
    ],
    "links": [
        ("Custom GPT retirement and migration FAQ", f"{HELP}/20001519-custom-gpt-retirement-and-migration-faq"),
        ("GPTs in ChatGPT", f"{HELP}/8554407-gpts-in-chatgpt"),
        ("Agent Skills specification", "https://agentskills.io/specification"),
        ("OpenAI skills repository", "https://github.com/openai/skills"),
    ],
}

G6 = {
    "slug": "agent-codex-automation",
    "title": "ChatGPT agent, deep research, Codex and scheduled tasks",
    "lead": "Hand ChatGPT multi-step work: agent mode on websites, deep research reports, Codex for code with AGENTS.md, scheduled tasks, and the safety habits that keep you in control.",
    "minutes": 18,
    "plain": "Agent mode is like giving an intern a laptop and a clear task. It opens websites, clicks, reads and fills forms, and checks with you before anything important. Codex is the same idea for software: it works in a copy of your code and proposes changes you review.",
    "ideas": [
        ("Agent mode", "ChatGPT uses its own browser and tools to complete a multi-step task, and asks before consequential actions."),
        ("Deep research", "Multi-step research that reads many sources and writes a cited report."),
        ("Codex", "OpenAI's coding agent in the cloud, the CLI, IDEs and the desktop app."),
        ("AGENTS.md", "A file in a repository that tells coding agents how to build, test and follow your conventions."),
        ("Scheduled tasks", "Ask ChatGPT to run something later or on a schedule, such as a daily summary."),
    ],
    "flow": ["Clear goal + limits", "Agent plans steps", "Works in browser / code", "Asks before key actions", "You review result"],
    "body": [
        ("Give agent mode a good task", CODE("""Goal: Compare 3 online SQL courses for a beginner data analyst in India.
Check: price in INR, hours, certificate, last updated date, reviews.
Output: a table plus a 3-line recommendation.
Limits: do not sign up, pay or enter any personal details. Stop and ask if a site needs login.""", "Agent prompt with limits") + UL([
            "Be specific about what done looks like and what it must not do.",
            "Watch the live steps; you can take over the browser or stop at any time.",
            "Confirm purchases, sends and form submissions yourself.",
        ])),
        ("Deep research that you can trust", UL([
            "Ask a focused question with a scope: market, country, time period, and the decision you need to make.",
            "Ask for a sources table with dates, and open the key ones.",
            "Follow up: <i>\"Which claims rely on a single source?\"</i>",
        ])),
        ("Codex for code", STEPS([
            "Open Codex in the desktop app, the web, your IDE or the CLI and connect your GitHub repository.",
            "Add an <b>AGENTS.md</b> at the repository root with build, test and style rules (Codex reads it; Claude Code can too).",
            "Give one clear task, such as \"Add input validation to the signup form and a test for it.\"",
            "Review the diff, run the tests yourself, and open a pull request only when you are satisfied.",
        ]) + CODE("""# AGENTS.md
## Setup
npm install
## Test before every change
npm test
## Style
- TypeScript strict mode. No new dependencies without asking.
- Small pull requests: one change per PR, with a clear title.""", "Example AGENTS.md")),
        ("Scheduled tasks", P("Ask: <i>\"Every weekday at 8 am, give me three AI product news items with links\"</i> or <i>\"Remind me on Friday to send my weekly report.\"</i> Manage or pause them from the schedule or tasks area in the app. Keep scheduled tasks small and check the first few results.")),
        ("Claude and ChatGPT side by side", TABLE(["Need", "Claude", "ChatGPT"], [
            ["Standing instructions", "Instructions for Claude", "Custom instructions"],
            ["Workspace for a goal", "Projects", "Projects"],
            ["Memory", "Topics; chat search (paid)", "Saved memories; reference chat history"],
            ["Repeatable procedures", "Skills (SKILL.md)", "Skills (same SKILL.md format)"],
            ["Connect other apps", "Connectors (MCP)", "Apps inside plugins (MCP)"],
            ["Install a bundle", "Plugins", "Plugins"],
            ["Do multi-step work", "Cowork (+ Claude in Chrome)", "Agent mode (+ Atlas)"],
            ["Coding agent", "Claude Code (CLAUDE.md)", "Codex (AGENTS.md)"],
        ]) + P("Many teams use both. Write skills in the shared SKILL.md format and keep project rules in AGENTS.md (imported from CLAUDE.md) so the same knowledge works in either tool.")),
    ],
    "mistakes": [
        ("Vague agent tasks such as \"plan my trip\"", "Give budget, dates, sources, output format and what not to do."),
        ("Merging Codex changes without running tests", "Run tests and read the diff; keep pull requests small."),
        ("No AGENTS.md in the repository", "Add one with setup, test and style rules so every agent follows them."),
    ],
    "practice": [
        "Run an agent task with clear limits and note every point where it asked for confirmation.",
        "Write an AGENTS.md for a small project and ask Codex (or Claude Code) for one change.",
        "Create one scheduled task and review its first three runs.",
    ],
    "quiz": [
        ("What should every agent prompt include besides the goal?", "What done looks like (output format) and the limits: what it must not do."),
        ("Which file tells Codex how to build and test your project?", "AGENTS.md at the repository root."),
        ("What is the Claude equivalent of ChatGPT agent mode?", "Cowork, paired with Claude in Chrome for websites."),
    ],
    "links": [
        ("ChatGPT agent", f"{HELP}/11752874-chatgpt-agent"),
        ("Deep research in ChatGPT", f"{HELP}/10500283-deep-research-faq"),
        ("Codex documentation", "https://developers.openai.com"),
        ("AGENTS.md", "https://agents.md"),
    ],
}

GUIDE = {
    "id": "chatgpt",
    "title": "ChatGPT Complete Guide",
    "subtitle": "Instructions, Projects, memory, plugins and apps, skills, GPT migration, agent and Codex",
    "checked": CHECKED,
    "hue": 160,
    "pdf": "handbook/ChatGPT-Complete-Guide-Nov-2026.pdf",
    "intro": "How to use ChatGPT well in November 2026: personalisation, Projects, both kinds of memory, the new Plugin directory, connecting your own tools, skills, migrating custom GPTs before their 11 December 2026 retirement, agent mode and Codex. OpenAI renames menus often, so each step names the idea first and the current menu second.",
    "lessons": [G1, G2, G3, G4, G5, G6],
    "sources": [("OpenAI Help Center", "https://help.openai.com"), ("OpenAI Academy", "https://academy.openai.com"), ("OpenAI developer docs", "https://developers.openai.com")],
}
