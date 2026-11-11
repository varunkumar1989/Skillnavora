# Walkthrough: Build a D2C Agent Team with Grok Bot

**Level:** Intermediate · **Time:** about 3 hours (plus the homework) · **Source:** the transcript of the walkthrough video "Master xAI's Grok 4.7 by Elon Musk in 1 Hour" (The Cutting Edge School), as supplied. This chapter restates the transcript's workflow, adds the checks it skips, and tags every claim.

**Status tags:** **[Transcript]** = claim made in the transcript, not checked by us · **[Third-party]** = product behaviour from the provider, which changes · **[General]** = stable concept · **[Check]** = verify on the provider's page before relying on it.

---

## Chapter 15.0 What the transcript covers, in order

| Part | What it teaches | Where it is in this course |
|---|---|---|
| 1. The Grok ecosystem | xAI, Grok models, Grok Imagine, Grok Build, Grok Bot, Grok Voice, the API | Module 2 |
| 2. Context windows | Tokens, why a 500,000-token window matters, compaction | Module 3 |
| 3. Chat vs bot | Do-it-yourself chat vs done-for-you agents | Chapter 15.1 |
| 4. Building a team | Chief of staff, specialist bots, one bot one job | Chapter 15.2 |
| 5. Tools, skills, routines | Connected apps, skills, routines, templates | Chapter 15.3 |
| 6. Memory and workspace | Shared files, group chat, memory, the brand bible | Chapter 15.4 |
| 7. Customer support | WhatsApp support agent, knowledge base, escalation | Chapter 15.5 |
| 8. Inbound automation | Website form → webhook → personalised brochure and invoice | Chapter 15.6 |
| 9. Outbound and influencers | Prospect lists, decks, personalised drafts | Chapter 15.7 |
| 10. Packaging for clients | Publishing a bot as a template, selling outputs or agents | Chapter 15.8 |
| 11. Homework and judgement | What to check before anything goes out | Chapter 15.9 |

**The rule that runs through the whole transcript:** the bots do the work; a person checks it and presses send. Every chapter below repeats that rule.

---

## Chapter 15.1 Chat versus a bot

| | Chatbot | Grok Bot (agent) |
|---|---|---|
| How you work | You ask, read, copy, paste into other tools | You describe a job and its outcome; the bot plans the steps |
| What it returns | Text to copy | Files, drafts, links and updates in your connected tools |
| When it runs | While the chat is open | On a schedule (routines) or when an event happens |
| Memory | The chat history | Its own memory, instructions and a shared workspace |
| Analogy in the transcript | Phoning a smart person | Hiring an intern with a manager |

**[Transcript]** "These are always-on AI agents that work on a done-for-you model."

**Check:** a bot works only inside the plan, tools and permissions you give it. Start with read-only access to every tool.

---

## Chapter 15.2 Build the team: chief of staff, then specialists

**The method in the transcript:**
1. Create a **chief of staff** bot. Its job: take the outcome you want, hire the right specialist bots, coordinate them, and check their outputs.
2. Ask the chief to create a **group chat** for the project so you can give work in one place.
3. Let the chief hire specialists: research, designer, creative (images and ads), website builder, customer support, outreach and proposals.

**One bot, one job.** A single bot that holds ads, complaints and invoices gets slow, messy and hard to hand over. Separate bots keep their context small and easy to fix.

**The "and" rule (from the transcript):** if a job description contains "and", it is probably two jobs. "Create images **and** research competitors" becomes two bots.

**Writing a good job description.** Use this template for every bot:
- **Goal:** the outcome in one sentence.
- **Inputs:** what it can read (named tools, folders, files).
- **Schedule:** when it runs (for example "every evening at 17:00").
- **Output:** the file or draft it produces and where it goes.
- **Approval:** what it must ask you before doing.

**Worked example from the transcript (the Healthy Mithai D2C brand and its Diwali offer):**
- Research bot: "Find out everything about the brand's competitors, and run a search every evening to tell me if any competitor made a move."
- The research bot returned a competitor report and a markdown file **[Transcript]**.

**Check:** bots can be wrong about who they are. The transcript's chief first added an old, unrelated bot to the group. Review the member list of every group chat.

---

## Chapter 15.3 Tools, plugins, skills and routines

### Connected apps (plugins)
- In the app's **Connect apps** page you connect tools such as Gmail, Slack, Notion, Google Drive, Shopify, Canva, Google Slides, Lovable and ElevenLabs **[Third-party]**. The transcript calls these connections *plugins*.
- Each plugin has three parts: **accounts** (what is connected), **tools** (actions the bot can take, such as creating or deleting an agent) and **skills** (built-in playbooks).
- **Principle:** a bot is only as capable as the tools it can use. Connect only what the bot needs.
- The transcript says Supabase can be connected **[Transcript]**. Confirm the current list on the Connect apps page.

### Built-in X search
- The transcript says X search is included in the plan, so a bot can search posts and summarise competitors' campaigns **[Transcript, Check]**. Whether it is included, and its limits, depend on your plan; check the current plan page.

### Skills
- A **skill** is a repeatable process: when to use it, its inputs, its steps, how to check the work, what to hand back, and what needs approval **[Transcript]**. Write a skill once and reuse it for the next client.
- To make a standing rule, ask the chief to create a skill, then open it and read every step. Example from the transcript: "When I create a new website and an ElevenLabs agent exists, link the agent to the website."
- **Publishing a skill to a team** lets everyone in the team's workspace use it **[Transcript, Check]**.

### Routines
- A **routine** is a job a bot runs on its own: on a schedule, or when an event happens. You can pause a routine with its toggle and resume it later; it keeps the same timing **[Transcript]**.
- Routines are how bots keep working when you are away.

---

## Chapter 15.4 Shared workspace, group chat, memory and the brand bible

### Virtual computer and shared files
- Each bot can use a virtual computer with a browser, a terminal and file storage **[Transcript]**.
- Files saved in a project folder are visible to every bot in that project, so bots share context without you repeating it.
- **Check:** every file in the shared folder is visible to every bot. Keep client data in the client's own folder.

### Group chat
- The group chat is where the chief takes requests and reports progress. You can type or use voice chat **[Transcript]**.
- Voice and text give you the same work; to talk to one specialist, open its own tab.

### Memory and feedback
- When you correct a bot ("don't put links in drafts", "use only verified prices"), it stores the correction and follows it next time **[Transcript, Check]**.
- Ask the bot to add the rule to its memory, then test that it follows it on the next task.

### The brand bible
- The transcript's chief built a brand bible of about 14–25 pages: brand story, founders, verified phrases and taglines, tone, product catalogue with prices and date, diet tags, ingredients, collections, offers, claims, and visual do's and don'ts **[Transcript]**.
- **Verified** facts come from the brand's official website and can be used as they are. **Unverified** facts are derived or assumed and must be confirmed with the client before use.
- Add a one-page executive summary at the front, so a reader can get the gist quickly **[Transcript suggestion]**.
- Mark the bible as the single source of truth and tell every bot to check its outputs against it.

**Check:** a brand bible is only as good as its sources. Confirm prices, delivery times and certifications with the client before publishing anything.

---

**Media tools (named in the transcript):** images and short videos are created with **Higgsfield** (the transcript spells it "Higgs Field") **[Transcript, Check]**. The transcript states that all media assets must come from this tool, and that websites are built on Lovable and support runs on ElevenLabs.

## Chapter 15.5 Customer support on WhatsApp (ElevenLabs)

**What the transcript builds:** a conversational agent on ElevenLabs, connected to a WhatsApp Business number, that answers simple questions in real time and escalates the rest to a person **[Transcript]**.

**Build steps:**
1. Create the agent on ElevenLabs. Write its role, tone and the escalation rules (what it must never answer, such as medical advice).
2. Add a **knowledge base**: FAQs, product list, prices, delivery policy, ingredients, and the brand's approved health statements. Index it.
3. Connect your own WhatsApp number through the WhatsApp Business setup. The transcript does this manually **[Transcript]**; some steps cannot be done by a bot.
4. Test with real questions before going live.
5. Add custom guardrails in the agent's guardrails tab if you need them.

**The health-claim example from the transcript:** asked "can a diabetic person eat this?", the agent answered from the brand's stated facts and advised checking with a doctor **[Transcript]**. Keep health answers strictly to approved wording.

**Security and responsibility (from the transcript):** if a client's data leaks, you become responsible as the data fiduciary. Check every output before it goes to a customer, and handle personal data under the rules that apply to you (in India, the Digital Personal Data Protection Act, 2023) **[General]**.

**Check:** test escalation. Ask at least ten questions the agent must hand to a human (refunds, complaints, allergies, bulk orders) and confirm each one escalates.

---

## Chapter 15.6 Inbound automation: website form to webhook to brochure

**The chain:**
1. A visitor fills an inquiry form on the website (built in Lovable in the transcript).
2. The form's submit action sends a **webhook** (an HTTP request) to a URL.
3. A Grok Bot routine receives the details, drafts a personalised brochure and, if requirements are given, an invoice, and saves them as drafts in Gmail **[Transcript]**.
4. A person reviews the draft and presses send.

**The credentials step (important):** the transcript says the bot cannot copy the webhook URL or key from its own chat or computer, so you must copy them yourself and paste them into the website builder **[Transcript]**. Treat this as a security rule, not a quirk:
- Never paste webhook keys, passwords or tokens into a chat with a bot.
- Store them only in the builder's secure settings.
- Rotate the key if it was shared by mistake.

**Invoice check:** the transcript computes "25 boxes × ₹700" and adds an early-bird discount **[Transcript]**. Check the arithmetic, the tax and any discount rule yourself before sending.

**Check:** submit a test form, confirm the routine fires, check the draft, and confirm nothing is sent automatically.

---

## Chapter 15.7 Outbound and influencers

**Prospect lists (Apollo):** the outreach bot found 20+ prospects with company, segment, decision-maker title, email, email status, LinkedIn, phone, fit note and a personalisation hook **[Transcript]**.
- **Only use verified emails.** Skip unverified ones. The transcript's bot found emails for 18 of 53 companies and drafted 35 emails, rather than guessing the rest **[Transcript]**. Keep that rule.
- Check each person's role and company before writing to them.

**Influencer ranking:** rank influencers by audience fit, engagement and whether they have posted for similar brands. Give each a contact, a short rationale and an outreach deck **[Transcript]**.

**Drafts, not sends:** the bots write Gmail drafts with attachments. You read, edit and send **[Transcript]**.

**Personalisation that works (from the transcript):** name one recent launch or campaign for each recipient, and remove long links from the body. The transcript's first drafts included long links and the rewrite removed them **[Transcript]**.

**Bot email addresses:** the transcript shows a bot with its own email address, in the form ces@mail.grokbot.com, used to subscribe to newsletters and receive replies **[Transcript, Check]**. The transcript says the address is claimed once and cannot be deleted or renamed, so check the spelling (the speaker corrected "gogbots" to "grokbot") before you confirm.

**Competitor monitoring:** have the research bot subscribe to competitors' newsletters, review their latest X posts, and report campaigns and what to learn from them **[Transcript]**. Confirm each subscription in your own inbox.

---

## Chapter 15.8 Packaging: sell outputs, sell agents, or both

**Two ways to sell (from the transcript):**
1. **Sell outputs** plus your judgement: brand bible, creatives, decks, outreach drafts, website, support agent set-up.
2. **Sell agents as a service**: a roster of bots the client keeps and reuses for future campaigns. Charge for setup and for the roster.

**How to publish a bot as a template (from the transcript):** open the bot, choose **create a copy**, ask it to create a public template. The template holds the bot's memories, skills and instructions. Publish it to get a shareable link **[Transcript, Check]**.

**Before you share a template:** remove client names, keys, emails, private files and any memory that holds client data. A template is a deliverable, so review it like one.

**Team plan:** a team can share skills and bots within the team's workspace **[Transcript, Check]**.

---

## Chapter 15.9 Judgement and homework

**What the transcript says the human must do:**
- Approve every message that goes to a real person.
- Check every output against the brand bible and the real source.
- Decide whether a result is good enough to show a client.

**Homework from the transcript:** pick a young brand you like and try these use cases for them. **Do not email anyone.** First improve the bots, check the outputs yourself, and ask: would a first-time buyer purchase this, does the output appeal to me, and would I actually use it? Only then show the work to the brand.

**Judgement checklist before anything goes out**
- [ ] Every fact traces to a verified source, or is marked unverified and cleared with the client.
- [ ] Prices, dates and offers match the brand's current site.
- [ ] No health or medical claim beyond the brand's approved wording.
- [ ] No personal data in the output that the recipient does not need.
- [ ] No link, key or token pasted into a message.
- [ ] A person has read, edited and approved the draft.

---


## Chapter 15.11 Key terms from the transcript, with definitions and examples

Every term the transcript uses for a key idea, with a short definition and an example. Tags show where the claim comes from.

| Term | Definition | Example |
|---|---|---|
| **Evals (evaluations)** | A repeatable test that measures how well an AI does a job, using fixed cases and clear scoring. The transcript calls them 'tests that people run to test the intelligence' [Transcript]. | Keep 50 real customer questions with the right answers. Each time you change a prompt, run all 50 and count how many are right. |
| **Context** | Everything the model can see for one request: instructions, files, chat, memory and tool results, all counted in tokens [Transcript]. | A support bot's context holds its rules, the refund policy, this customer's order and the last three messages. |
| **Context window** | The maximum tokens a model can use at once [Transcript]. | A 500,000-token window holds about 375,000 words [Transcript]. See Chapter 16.8. |
| **Token** | A piece of text a model reads or writes, about three-quarters of an English word [Transcript]. | 'Elon Musk founded xAI in 2023' is split into several tokens before the model reads it. |
| **Context capacity, retrieval accuracy, reasoning quality** | The transcript's three ways to judge a model: how much it can hold, how reliably it finds the right information, and how well it uses that information [Transcript]. | Two models with the same window can differ: one finds the right clause in a 300-page contract, the other misses it. |
| **Compaction, truncation, summarisation, retrieval** | Four ways to keep a long session working when the window fills. Each is a summary of what was there [Transcript]. | After 200 messages, the bot replaces the old chat with a 10-line summary of decisions. |
| **System instructions / custom instructions** | Standing rules sent with every request, written by the builder or by you in a project [Transcript]. | 'Always answer in simple English, never promise a delivery date.' |
| **Memory** | Facts or preferences a bot or assistant keeps between sessions and reuses [Transcript]. | After you correct a bot twice ('no links in drafts'), it keeps that rule for future drafts. |
| **Uploaded documents** | Files added to the context; they count towards the window [Transcript]. | A 20-page brand bible uploaded to a chat uses a large share of the window. |
| **LLM (large language model)** | The model that reads text and predicts the next token; the 'intelligence' part of a product [Transcript]. | Grok 4.7 is a model; Grok Bot is the product that uses it. |
| **Reasoning level** | A setting that controls how much a model thinks before it answers [Transcript]. | Use a higher level for a multi-step margin calculation; a lower one for rewriting a caption. |
| **Chatbot** | A tool you ask and it answers in the conversation; you copy the output elsewhere [Transcript]. | You paste a question, get a draft, and copy it into your email yourself. |
| **Agent / persistent agent** | A bot that takes an outcome, plans steps, uses tools and keeps running on schedules or events [Transcript]. | A competitor-watch bot searches every evening and writes a report. |
| **Done-for-you vs do-it-yourself** | Chat is do-it-yourself: you direct every step. An agent is done-for-you: you set the outcome and check the result [Transcript]. | You ask a chatbot for a report, then compile it. You ask an agent for the report and it compiles it and files it. |
| **Routine** | A job a bot runs on its own, on a schedule or when an event happens; it can be paused [Transcript]. | Every morning at 9, the research bot checks competitors' posts and writes a summary. |
| **Skill** | A repeatable process a bot follows, with its trigger, inputs, steps, checks, hand-back and approval points [Transcript]. | A 'website with ElevenLabs agent' skill that always adds the support agent to new sites. |
| **Plugin (connected app)** | An app a bot can read or act in, such as Gmail, Notion or Google Drive [Transcript]. | After connecting Gmail, the bot can write drafts there; it cannot send unless you allow it. |
| **Template (bot template)** | A saved copy of a bot's memory, skills and instructions that others can use [Transcript]. | A 'Diwali campaign' template that you share with a client so they can reuse the setup. |
| **Marketplace** | A place to browse and import community or official bot templates [Transcript]. | Importing a 'personal assistant' template, then changing its memories for your own use. |
| **Group chat** | A shared chat where a chief bot and specialist bots take requests and report [Transcript]. | You post 'please prepare the Diwali brochure' once; the chief assigns it to the creative bot. |
| **Live voice chat** | Speaking with a bot in real time instead of typing [Transcript]. | You talk through a brief; the bot replies by voice and ends the call when finished. |
| **Virtual computer** | A cloud computer each bot can use, with a browser, terminal and file storage [Transcript]. | The research bot opens a competitor's website in the browser and saves a screenshot to the shared folder. |
| **Shared workspace / shared folder** | Files every bot in a project can see, so context is shared [Transcript]. | The brand bible saved once is used by the website, creative and support bots. |
| **Brand bible** | A short, verified reference for a brand: story, approved phrases, prices, products, claims and visual rules [Transcript]. | A 14-page document listing the approved tagline and the current price for each product. |
| **Verified vs unverified fact** | Verified facts come from the brand's own source. Unverified facts are derived or assumed and need the client's confirmation [Transcript]. | 'Free delivery above ₹499' copied from the site is verified; 'best in Pune' from a guess is unverified. |
| **Webhook** | An automatic message one system sends to a web address when something happens [Transcript]. | A website form sends each submission to a routine, which drafts a brochure. |
| **Credentials (webhook URL and key)** | The address and secret key that let one system send data to another. They must be pasted by a person, never shared in chat [Transcript]. | You copy the webhook key into Lovable's settings yourself; you never paste it into a bot chat. |
| **Guardrail** | A limit that stops an AI from doing something it should not: a rule, a filter or a check [Transcript]. | The support agent is told never to give medical advice and to refer health questions to a doctor. |
| **Escalation** | Passing a conversation to a person when the AI should not or cannot answer [Transcript]. | A bulk-order request is passed to the sales team with the customer's details. |
| **Knowledge base** | The documents an agent searches to answer questions [Transcript]. | A list of FAQs, prices and delivery rules, indexed for the support agent. |
| **Data fiduciary** | The party responsible for personal data entrusted to it, even when vendors' tools process it [Transcript]. | If a client's customer data leaks through your agent, you are accountable to the client. |
| **Human in the loop** | A person checks and approves the important steps before they happen [Transcript]. | The bot drafts emails; you read each one and press send. |
| **SHAPE framework** | The transcript's five-part framework: SOP-driven work, human in the loop, arbitrage, product is no longer the moat, and be employable [Transcript]. | A checklist for a new AI service: write the process first, keep a person approving, find the price gap you can fill, compete on service, and build skills. |
| **Arbitrage** | Profiting from a gap between what something costs and what people will pay [General; the transcript uses it inside SHAPE]. | Doing a repeatable service for clients who lack the time, using tools that cost less than your fee. |
| **First draft vs last draft** | The transcript's rule: AI output is a first draft; the human makes the last draft [Transcript]. | The AI writes a proposal; you check the numbers, rewrite the opening and approve it. |
| **Team plan** | A plan that lets a team share bots, skills and assign work to each other [Transcript, Check]. | Three team members share the same brand-bible skill. |
| **Force multiplier** | A tool that lets one person do much more work, while judgement stays with the person [Transcript]. | One person manages six specialist bots and reviews their output each day. |
| **Apollo (prospect data)** | A sales database that finds contacts and email status [Transcript; a third-party tool]. | A list of 20 decision-makers, each with a verified email before you write to them. |
| **Personalisation hook** | One specific, true detail about the recipient used to open a message [Transcript]. | 'Congratulations on your October launch' instead of 'Hello'. |
| **Gmail draft** | An email saved, not sent, for a person to review [Transcript]. | The bot writes 35 drafts with attachments; you send only the ones you approve. |
| **Whisper Flow (dictation)** | A voice-to-text tool the transcript uses to speak a long job description instead of typing it [Transcript; a third-party tool]. | You dictate a bot's job description in one minute, then check the text before saving it. |
| **Higgsfield (media tool)** | A tool for creating images and video, named in the transcript [Transcript, Check]. | Product images for the brand's website. |
| **ElevenLabs** | A platform for voice and conversational agents, named in the transcript [Transcript, Check]. | A WhatsApp support agent that answers FAQs and escalates the rest. |
| **Lovable** | A tool that builds websites and apps from prompts, named in the transcript [Transcript, Check]. | A brand website built from a prompt and then published on the client's domain. |

---

## Chapter 15.10 What the transcript claims that we have not verified

| Claim in the transcript | Our status |
|---|---|
| Grok Bot is included only from the Premium plan, minimum $30 a month | **[Transcript, Check]** plans and prices change; see Module 4 |
| The 500,000-token context window, and the comparison with other models' window sizes | **[Transcript]** model names and limits change; see Module 3 and the official model page |
| Four reasoning levels for Grok 4.7 | **[Transcript, Check]** confirm in the app |
| X search is built in at no extra cost | **[Transcript, Check]** confirm the plan terms |
| Bots can earn money or win clients for you | **[Transcript]** no result is promised; see the honest caveat in Module 10 |
| A bot can negotiate with 40 suppliers on WhatsApp | **[Transcript]** an anecdote; not verified |
| Scholarship and subscribe calls to action | Not part of this course |

**The transcript's own warning, which we repeat:** the tools will change; the way of working (clear job, checked output, human approval) does not.
