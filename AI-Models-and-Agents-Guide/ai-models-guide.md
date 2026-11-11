# AI Models and Platforms: The Complete Guide

**Who this is for:** anyone who uses AI tools at work or at home and wants to know what each model and platform does, which one to choose, and how the features fit together.
**What it covers:** the core concepts (LLM, tokens, context window, reasoning, multimodal inputs), the Grok family including Grok Bot, image generation and coding, ChatGPT, Claude, Gemini, Lovable and app builders, and how to choose.
**How to use it:** read Chapter 1 once. Then go to the platform you use. Every platform chapter follows the same structure, so you can compare them quickly.

---

## Read this first: what is verified and what is not

| Label | Meaning |
|---|---|
| **[Fact]** | A standard definition that does not change between products |
| **[Check]** | A product name, feature, limit or price that changes often. Confirm it on the official page before you rely on it, and note the date you checked |
| **[Opinion]** | A recommendation, not a measured result |

Product lineups change every few months. Model names, plan names and limits in this guide are the names known when it was written. Treat every product-specific detail as **[Check]**. This guide does not compare benchmark scores, because they change constantly and are often measured under conditions that do not match everyday use.

**Official pages to check (start here):**
- xAI and Grok: https://x.ai and https://grok.com
- OpenAI and ChatGPT: https://openai.com and https://chatgpt.com
- Anthropic and Claude: https://www.anthropic.com and https://claude.ai
- Google and Gemini: https://gemini.google.com
- Lovable: https://lovable.dev

---

## Chapter 1: How large language models work

### 1.1 What a large language model is **[Fact]**
A **large language model (LLM)** is a program trained on very large amounts of text to predict the next piece of text. When you ask a question, it generates an answer one piece at a time, each time choosing a likely continuation. "Large" refers to the number of internal numbers it learned, called **parameters**, which can run into the billions.

> **Analogy.** A phone keyboard suggests the next word. An LLM does the same job at a far larger scale, which is why its answers can read like reasoning.

### 1.2 Training and inference **[Fact]**
- **Training** is the one-off, expensive process that sets the parameters from data.
- **Inference** is every time you use the model. You pay for inference, usually per token.

### 1.3 Tokens **[Fact]**
A **token** is a piece of text the model reads or writes: a whole word, part of a word, a number fragment or punctuation. The same sentence can be a different number of tokens in different models, because each has its own tokenizer. As a rough English rule, one token is about three-quarters of a word **[Estimate]**.

Tokens matter for three reasons:
1. **Cost.** API prices are quoted per million tokens, separately for input and output.
2. **Limits.** Every model has a maximum amount it can handle at once.
3. **Speed.** More output tokens take longer to generate.

### 1.4 Context window and context **[Fact]**
The **context** is everything the model can see when it answers: your message, the earlier conversation, any uploaded documents, and any hidden instructions the product adds. The **context window** is the maximum amount of context a model can hold in one request, measured in tokens. A larger window lets you include more material, but a model does not always use every part of a very long input equally well.

What fills the context window in a typical chat:
- The product's own instructions (hidden from you)
- Your custom instructions, project files or saved memory, if the product uses them
- The conversation so far
- The message you are writing now
- Any tool results, search results or uploaded files

When a conversation grows too long, products drop or summarise older parts. That is why a model can "forget" a detail from the start of a long chat.

### 1.5 Parameters, weights and model size **[Fact]**
Parameters are the learned values inside the model. Bigger models often know more and reason better, but they are slower and more expensive. Smaller models are fast and cheap and are often good enough for simple tasks. Choosing a model is a trade-off between quality, speed and cost.

### 1.6 Reasoning models **[Fact]**
Some models spend extra output on working through a problem before they give the final answer. These are often called reasoning models. They are better at maths, multi-step logic and code, and slower and more costly per answer. Use them for hard problems, not for simple drafting. Whether a product shows the reasoning, and how it bills it, is **[Check]**.

### 1.7 Multimodal models **[Fact]**
A **multimodal** model accepts more than text: images, documents, sometimes audio and video, and sometimes produces images. Which inputs and outputs a given model supports is **[Check]**, because it varies by model and plan.

### 1.8 Hallucination **[Fact]**
A model can produce a confident answer that is false, such as a made-up citation or statistic. Check any fact that matters, and ask for sources you can open. Chapter 1.4 explains why: the model generates likely text, and it does not check it against a database unless a tool does that for it.

### 1.9 Knowledge cut-off and tools **[Fact]**
A model knows only what was in its training data up to a cut-off date. For newer information it needs a tool: web search, a document, or a connector to a live system. When a product says it "searched the web", it is using a tool, and the sources it cites are the ones to check.

### 1.10 Choosing a model: a quick method **[Opinion]**
1. Write the task in one sentence and the output you need.
2. Pick the cheapest model that handles that task. Test it on three real examples.
3. Move to a stronger model only if the cheap one fails on quality.
4. For code or long documents, check the context window and the output limit first.
5. For private data, read the platform's data-use and retention terms, not just the marketing page.

---

## Chapter 2: The Grok family (xAI)

### 2.1 What Grok is **[Check]**
**Grok** is xAI's family of AI models and the chat products built on them. The consumer chat is available on the Grok website and apps, and xAI also offers models through an API for developers. The API is billed per token. Plans for the chat products are subscriptions. Keep the two separate: a subscription does not give you API credits unless the provider says so.

### 2.2 Model generations and how to pick **[Check]**
Model names have moved quickly through 2026. Third-party price listings mention Grok 4.3, Grok 4.6 and Grok 4.7, and a separate coding model called Grok Build 0.1. Read the current model list on xAI's own documentation before you choose. For each model, check:
- context window (how much it can hold at once)
- whether it accepts images or files
- whether it has a reasoning mode
- price per million input and output tokens
- rate limits and the plan that includes it

### 2.3 Context windows in the Grok family **[Check]**
Some third-party sources list a context window of about 500,000 tokens for one Grok 4.x model and about 1,000,000 tokens for another. Confirm the figure for the exact model you use. Long context is useful for large codebases and document sets, but test whether the answers stay accurate near the end of a very long input.

### 2.4 Grok in the chat app **[Check]**
- Ask questions, draft text, summarise documents and analyse images.
- Use it for current events that need live search, and check the sources it links.
- Use the model picker if your plan offers several models, and choose the fast one for simple tasks.

### 2.5 Grok Bot: agents that work for you **[Check]**
**Grok Bot** is xAI's agent product. A Grok Bot agent is a named assistant that can work in your apps and on a schedule. Reported features include connections to email and team chat (Gmail and Slack have been named), learning a task by watching you do it, and running on a schedule. Plan availability and usage limits change, and reviewers have reported that usage allowances can run out quickly. Confirm which plan includes Grok Bot and what the usage limit is before you rely on it.

Chapter 2 of the AI Agents guide explains how any agent works, which applies to Grok Bot as well.

### 2.6 Grok image generation **[Check]**
Grok can generate images inside the chat product. Check the current image feature name, which plans include it, how many images you get, and the rules on what you may create and publish. Do not generate images of real people in ways that could mislead or harm them, and do not use generated images in advertising without checking the licence and disclosure rules that apply to you.

### 2.7 Grok for coding **[Check]**
xAI offers coding-focused models and coding tools. Use them the way you would use any coding assistant:
- give the model the file, the error message and the expected behaviour
- ask for a small change, then run the tests
- review every change before you commit it
- never paste secret keys into a prompt

Whether a coding tool can run commands on your machine, and how it is sandboxed, is **[Check]** for the exact product.

### 2.8 Grok pitfalls **[Opinion]**
- Assuming a subscription includes API usage.
- Relying on a model's live-search answer without opening its sources.
- Using a coding model's output without tests.
- Confusing Grok (xAI) with Groq, a different company.

---

## Chapter 3: ChatGPT (OpenAI)

### 3.1 What ChatGPT is **[Fact]**
ChatGPT is OpenAI's chat product, built on OpenAI's GPT models. OpenAI also offers the models through an API. As with Grok, the chat plans and the API are billed separately **[Check]**.

### 3.2 Models in ChatGPT **[Check]**
OpenAI releases models in families and sizes, and the set available in ChatGPT depends on your plan. Check the model picker in your account and OpenAI's current model documentation. Look at context window, image input, reasoning options and rate limits for each model.

### 3.3 Core features **[Check]**
Feature names and plan limits change. These are the categories to check in your own account:
- **Chat and writing:** drafting, rewriting, summarising and translating.
- **File and image input:** upload documents and images for analysis.
- **Search:** answers with web sources. Open the sources.
- **Deep research:** longer multi-step research that produces a report with citations. Check how long it takes and what it costs in your plan.
- **Image generation:** create and edit images in the chat. Check the rules and the licence terms.
- **Voice:** spoken conversation on mobile and desktop.
- **Projects:** group chats with shared files and instructions.
- **Custom GPTs:** saved assistants with their own instructions and files. Check who can see and share them.
- **Memory:** the product can remember facts about you across chats. You can view and delete them.
- **Canvas or document editing:** edit long text or code side by side with the chat.
- **Agent features:** tasks where ChatGPT uses a browser or connected apps. These need care; see the AI Agents guide, Chapter 8.

### 3.4 Custom GPTs and projects: when to use which **[Opinion]**
Use a **Project** when you work on one ongoing piece of work with shared files. Use a **custom GPT** when you want the same instructions and knowledge available to many people, and when you have checked who can access it. Before sharing any custom GPT, remove private data from its files.

### 3.5 The API **[Check]**
The API gives developers the same models for their own products. It is billed per token. Use the API for products, automations and integrations. Use the chat product for personal work.

### 3.6 ChatGPT pitfalls **[Opinion]**
- Trusting a search answer without opening its sources.
- Uploading confidential documents without checking the data controls on your plan.
- Sharing a custom GPT that contains private information in its files.
- Expecting memory to be perfect. Check what it has stored.

---

## Chapter 4: Claude (Anthropic)

### 4.1 What Claude is **[Fact]**
Claude is Anthropic's AI assistant, built on the Claude family of models. It is available through the Claude website and apps, through Claude Code for developers, and through the API. The API is billed per token; the chat plans are subscriptions **[Check]**.

### 4.2 Models **[Check]**
Anthropic publishes a family of models in several sizes, aimed at different trade-offs of speed, cost and capability. The current names and prices are on Anthropic's model pages. Choose the smallest model that does the task well, and move up only when the smaller one fails your tests.

### 4.3 Core features in the Claude app **[Check]**
Feature names and plan limits change. These are the categories to check:
- **Chat and writing:** drafting, editing and analysis.
- **File and image input:** upload documents, spreadsheets and images.
- **Projects:** a workspace with its own instructions and uploaded files, for ongoing work.
- **Artifacts:** a panel where Claude produces a document, a web page, a diagram or a small app, which you can view, edit and download.
- **Styles and preferences:** instructions that shape how Claude writes for you.
- **Memory:** Claude can use context from earlier chats where the feature is enabled. Check what is stored and how to delete it.
- **Skills:** saved, reusable instructions and resources that Claude uses for a type of task.
- **Connectors:** links to external services (for example, a hosting provider or a data tool) through the Model Context Protocol (MCP). Chapter 8 explains MCP.
- **Web search:** answers with sources. Open the sources.

### 4.4 Claude Code **[Check]**
Claude Code is a coding tool that works inside a project folder on your computer. It can read files, propose changes, run commands and tests, with your approval for each step. Use it for real projects. Read the permission prompts, keep secrets out of the project, and review every change before you commit.

### 4.5 The API and prompt caching **[Check]**
The API bills input and output tokens separately. Some providers offer **prompt caching**, which lowers the cost of repeated input such as a long system prompt or a reference document. Check whether caching is available for your model and how long a cache lasts.

### 4.6 Claude pitfalls **[Opinion]**
- Pasting private client data into a chat without checking the data terms of your plan.
- Forgetting that a Project's files and instructions apply to every chat in it.
- Trusting a generated artifact without opening and testing it.
- Connecting a tool with more permission than the task needs.

---

## Chapter 5: Gemini (Google)

### 5.1 What Gemini is **[Fact]**
Gemini is Google's family of AI models and its assistant. It is built into Google products such as Search, Gmail, Docs and Workspace, and is also offered as an app and through the Gemini API **[Check]**.

### 5.2 Features to check **[Check]**
- Chat, writing and summarising.
- Working with Google Docs, Gmail and Drive content, where your organisation allows it.
- Image and document input.
- Deep research style reports with sources.
- Video and audio understanding in some models **[Check]**.
- The API, billed per token, with a free tier for testing **[Check the current limits]**.

### 5.3 When Gemini fits well **[Opinion]**
Gemini is a natural choice when your work already lives in Google Workspace, because the integration removes copy-and-paste. Check your organisation's admin settings for which apps the assistant can read.

---

## Chapter 6: Lovable and app builders

### 6.1 What Lovable is **[Check]**
Lovable is an AI tool that builds working web apps from a description. You describe the app in plain language; it writes the code, shows a live preview, and can connect a database and login. It is one of several AI app builders. Others include Replit and Bolt. Check each product's current features and pricing.

### 6.2 How app builders work **[Fact]**
An app builder combines three things: a model that writes code from your instructions, a sandbox that runs the app so you can see it, and integrations for hosting, a database and sign-in. Each change is a new prompt that edits the code.

### 6.3 Using an app builder well **[Opinion]**
1. Start with the smallest working version: one screen, one action.
2. Be specific: name the data, the user and the result you expect.
3. Check the database security rules before you put real user data in. Row-level security must restrict each user to their own rows.
4. Test sign-up, log-in, the main action and an invalid input.
5. Export or sync the code to a repository before you rely on the app.
6. Keep the secret keys in the platform's secret store, not in a prompt.

The full Lovable tutorial with 14 classes is on the site: Lovable: Complete Tutorial (lovable-tutorial.html).

### 6.4 Security checks for app builders **[Fact]**
- Never publish an app that lets anyone read or change other users' data.
- Assume that any value in front-end code is visible to users.
- Run the platform's security scan, and read its findings.

---

## Chapter 7: Other models and platforms

| Platform type | Examples **[Check]** | Use it for |
|---|---|---|
| Open-weight models you can run yourself | Llama, Mistral, Qwen and others | Private data, offline use, cost control; needs technical setup |
| Search-first assistants | Perplexity and similar | Research with cited sources |
| Coding assistants in an editor | GitHub Copilot, Cursor and similar | Writing and editing code in your project |
| Automation platforms | n8n, Make, Zapier | Connecting apps on triggers, with AI steps |
| Image and video generators | Various, check licence and rights | Creative assets; check commercial-use terms |

Open-weight models have their own licence terms; read them before commercial use **[Check]**.

---

## Chapter 8: Connecting models to tools: MCP and APIs

### 8.1 What an API is **[Fact]**
An **API** (application programming interface) lets one program ask another for a service. A model API receives your messages and returns the model's reply.

### 8.2 What MCP is **[Fact]**
The **Model Context Protocol (MCP)** is an open standard for connecting AI assistants to tools and data sources in a consistent way. An **MCP server** exposes tools (actions) and resources (readable data). An assistant that supports MCP can discover those tools and use them when a task needs them. Check the current MCP documentation at https://modelcontextprotocol.io.

### 8.3 Why it matters **[Opinion]**
Without a standard, every assistant needs its own connector for every service. With MCP, one server can serve many assistants. The trade-off is that a connector gives the assistant real power, so each tool needs permission limits and logging.

---

## Chapter 9: Choosing and comparing platforms

| Question | Look at |
|---|---|
| Which tasks? | Writing, research, code, images, data, automation |
| Which data? | Public, internal or confidential; check the data-use terms |
| Which budget? | Subscription for personal use; API for products; check limits |
| Which integrations? | Your email, documents, code host, database, team chat |
| Which quality? | Your own three-example test, not a leaderboard |
| Which control? | Admin settings, memory controls, sharing controls |

**A simple decision guide [Opinion]:**
- Personal writing and research: pick the one you find easiest, then test it on your real work.
- Team knowledge in documents: use a platform with project or workspace features and admin controls.
- A product for customers: use an API, with cost controls, tests and monitoring.
- Building a small web app without deep coding: an app builder, then review the security rules.
- Automating a workflow across apps: an automation platform with an AI step, or an agent (see the AI Agents guide).

---

## Chapter 10: Glossary

| Term | Definition |
|---|---|
| LLM | Large language model: a model trained to predict and generate text |
| Parameter | A learned value inside a model |
| Token | A unit of text the model reads and writes; the basis of price and limits |
| Context | Everything the model can see when it answers |
| Context window | The maximum context a model can hold in one request |
| Inference | Running a trained model to produce an answer |
| Reasoning model | A model that works through a problem before answering |
| Multimodal | Accepting or producing more than text |
| Hallucination | A confident answer that is false |
| Knowledge cut-off | The date after which a model has no training data |
| Tool | An action a model can request, such as search or running code |
| API | Application programming interface, a way for programs to call a service |
| MCP | Model Context Protocol, a standard for connecting assistants to tools |
| Prompt caching | Reusing processed repeated input at lower cost |
| Project (Claude, ChatGPT) | A workspace with shared files and instructions |
| Custom GPT | A saved ChatGPT assistant with its own instructions and files |
| Artifact (Claude) | A document, page or app that Claude produces in a side panel |
| Skill (Claude) | Saved reusable instructions for a type of task |
| Connector | A permission link to an external service |
| Agent | An AI system that takes steps towards a goal using tools (see the AI Agents guide) |

---

## Learning tools and links

- xAI (Grok, API): https://x.ai
- Grok: https://grok.com
- OpenAI (ChatGPT, API): https://openai.com
- ChatGPT: https://chatgpt.com
- Anthropic (Claude, API): https://www.anthropic.com
- Claude: https://claude.ai
- Claude documentation: https://docs.claude.com
- Google Gemini: https://gemini.google.com
- Lovable: https://lovable.dev
- Replit: https://replit.com
- Model Context Protocol: https://modelcontextprotocol.io
- n8n: https://n8n.io

---

## Related pages on this site

- Context engineering course: context-engineering.html
- AI evals course: ai-evals.html
- Agent orchestration and multi-agent systems: agent-orchestration.html
- Browser automation and AI agents: browser-automation.html
- Lovable tutorial: lovable-tutorial.html
- Grok Bot Mastery Course: grokbot-course.html

---

## Sources and disclosure

- Product names, features, limits and prices are the names known when this guide was written and must be checked on the official pages listed above.
- No benchmark scores are reported.
- Sponsored or affiliate material is not included.
