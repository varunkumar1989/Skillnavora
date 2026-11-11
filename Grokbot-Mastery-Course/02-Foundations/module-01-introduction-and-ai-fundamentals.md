# Module 1: Introduction to Grokbot and AI Fundamentals

**Level:** Beginner · **Time:** about 3 hours · **You need:** nothing but curiosity

---

## Chapter 1.1 What Grokbot is and what problem it solves

### Pillar 1: Core objective
- **Understand** what Grok Bot does, who makes it, and how it relates to the Grok models and the Grok API.
- **Implement** a one-paragraph description of a task you would hand to an agent.
- **Skill developed:** spotting tasks that suit an always-on agent and tasks that do not.

### Pillar 2: Key concepts and mental models

**Topic 1.1.1 What Grok Bot is.** Grok Bot is an agent app from xAI. An **agent** is AI software that does not just answer a question but takes steps towards a goal: it opens apps, reads email, drafts replies, checks a website, and reports back. Reported features: named agents, connections to Gmail and Slack, learning a task by watching you, and schedules **[Third-party]**.

> **Analogy.** A chatbot is a knowledgeable friend you phone with a question. An agent is an assistant who sits at a desk with their own computer, does the job while you are away, and leaves you a note.

**Topic 1.1.2 The problem it solves.** Knowledge workers spend hours on repetitive digital chores: triaging inboxes, copying data between tools, checking sites for changes, writing routine updates. Chat assistants help one prompt at a time; an always-on agent can run those chores on a schedule.

| Task | Good fit for an agent? | Why |
|---|---|---|
| Every morning, summarise new support emails into a Slack post | Yes | Repetitive, low risk, clear output |
| Watch a competitor's pricing page and alert on changes | Yes | Scheduled, simple check |
| Approve a refund of ₹50,000 | No, not without a human | Money moves; needs approval |
| Write the company's annual strategy | No | Needs judgement and accountability |

**Topic 1.1.3 History and evolution.** **[General, public reporting; verify dates]**
- 2023: xAI founded; the first Grok chat assistant released to X (Twitter) subscribers in late 2023.
- 2024: Grok-1 model weights published openly; Grok-2 released with image understanding.
- 2025: Grok 3 and Grok 4 released; standalone Grok apps and the grok.com website.
- 2026: Grok 4.x updates reported (4.3, 4.6, 4.7 appear in third-party price listings), and Grok Bot announced on 11 August 2026 **[Third-party]**.

### Pillar 3: Step-by-step SOP: decide whether a task suits Grok Bot
1. Write the task as a sentence: trigger, action, output. *"Every weekday at 9 a.m., read new emails labelled 'Leads' and post a summary in #sales."*
2. Score risk: does it send money, delete data, or speak for the company to customers? If yes, add a human approval step.
3. Score frequency: daily or weekly tasks benefit most.
4. Check access: the agent needs a login or connection to every tool involved.
5. Define "done": what output proves the task worked (a Slack post, a sheet row).
6. **Expected output:** a one-line agent brief plus a risk note.
7. **Test:** run the task once by hand and time it; compare with the agent run.

### Pillar 4: Pitfalls and guardrails
- Giving an agent broad access "just in case". Give the minimum access each task needs.
- Assuming plan usage is unlimited. Reviewers report usage limits that are hard to understand **[Third-party]**.
- Letting an agent send external messages unsupervised in the first weeks.
- Confusing Grok (xAI) with Groq (a different company).

---

## Chapter 1.2 How Grok differs from ChatGPT, Claude and Gemini

### Pillar 1: Core objective
Understand the main AI assistants as **products built on models**, and compare them on the dimensions that matter for a buyer, without relying on marketing claims.

### Pillar 2: Key concepts

| Dimension | What to compare | How to check it yourself |
|---|---|---|
| Company and model family | xAI Grok · OpenAI GPT · Anthropic Claude · Google Gemini | Official model pages |
| Live data | Grok is integrated with X (real-time posts); others use web search tools | Ask each about today's news and check sources |
| Context window | How much text fits in one request | Model documentation |
| Agents and automation | Grok Bot; ChatGPT agents; Claude Code and Cowork; Gemini in Workspace | Product pages and trials |
| API pricing | Per million input and output tokens | Official pricing pages |
| Data and privacy | Training on your data, retention, enterprise terms | Terms and privacy policy |

**Topic 1.2.1 Products versus models.** "ChatGPT" is a product; GPT models power it. "Claude" is both the assistant product and the model family. "Grok" is the model family and the chat product; "Grok Bot" is the agent product. Comparing "Grok vs Claude" without saying *which product and which model* produces confused answers.

**Topic 1.2.2 Benchmark caution.** Leaderboards change monthly and test narrow skills. Your own task with your own data is the only benchmark that matters.

### Pillar 3: SOP: run your own comparison
1. Pick three real tasks from your work (a summary, a data question, a draft email).
2. Write one identical prompt per task.
3. Run each prompt on each assistant you can access.
4. Score each answer 1–5 on accuracy, usefulness and tone, and note the time taken.
5. Record any factual error.
6. **Expected output:** a 3×4 scoring table and a one-paragraph conclusion.

### Pillar 4: Pitfalls
- Comparing a free tier of one product with a paid tier of another.
- Trusting a single impressive answer; run each prompt at least twice.
- Ignoring data terms: business data may need an enterprise plan.

---

## Chapter 1.3 Generative AI and large language models

### Pillar 1: Core objective
Explain, in plain language, what generative AI and a large language model (LLM) are, and why they sometimes make things up.

### Pillar 2: Key concepts

**Topic 1.3.1 Generative AI** creates new content (text, images, audio, code) by learning patterns from very large amounts of examples.

**Topic 1.3.2 A large language model** is a generative AI model trained to predict the next piece of text. "Large" refers to billions of internal settings (**parameters**) and the huge training data.

> **Analogy.** Phone keyboards suggest the next word. An LLM is that idea scaled up enormously: trained on a vast library, it can continue a sentence so well that the result reads like reasoning, writing or code.

**Topic 1.3.3 Training versus inference.** **Training** is the expensive one-off process in which the model learns from data. **Inference** is each later use: you send a prompt, the trained model generates an answer. You pay for inference.

**Topic 1.3.4 Why models hallucinate.** The model produces the most plausible continuation, not a checked fact. If it has no reliable knowledge, it can still produce fluent, confident, wrong text. This is called a **hallucination**.

**Topic 1.3.5 Knowledge cut-off.** A model knows only what was in its training data, up to a date. For newer facts it needs tools such as web search or X search, or documents you provide.

### Pillar 3: SOP: test a model's limits
1. Ask about an event from last week without enabling search. Note whether it admits not knowing.
2. Enable search (if available) and ask again; check that it cites sources.
3. Ask for a statistic and request the source; open the source to confirm.
4. **Expected output:** a note listing which answers were verified, which were not.

### Pillar 4: Pitfalls
- Treating fluent text as true. Verify numbers, names, quotes and legal or medical claims.
- Assuming the model "remembers" you between chats; memory features are product-specific.

---

## Chapter 1.4 What happens when you submit a prompt

### Pillar 1: Core objective
Follow a prompt from your keyboard to the answer on screen, and know where cost and delay come from.

### Pillar 2: Key concepts: the lifecycle
```
You type ─► App adds system prompt + history ─► Text split into tokens
   ─► Model reads all tokens (input) ─► Generates one token at a time (output)
   ─► Tokens turned back into text ─► Streamed to your screen ─► Usage counted and billed
```
- **Prompt:** the text you send.
- **System prompt:** hidden instructions the app adds (tone, rules).
- **Tokens:** pieces of text the model reads and writes (Module 3).
- **Generation:** the model produces one token at a time, each time choosing a likely next token.
- **Streaming:** sending each token to your screen as soon as it is produced.

**Topic 1.4.1 Inference** is the computation that turns your input tokens into output tokens, run on specialised chips (GPUs) in a data centre.

### Pillar 3: SOP: observe the lifecycle
1. Ask a long question and watch the answer stream word by word.
2. Ask the same question asking for "one sentence only"; notice it finishes faster.
3. **Expected output:** the observation that longer answers take longer and (on the API) cost more.

### Pillar 4: Pitfalls
- Thinking the model searches a database for your answer. By default it generates from learned patterns.
- Forgetting that the app's hidden system prompt and history also count as input.

---

## Chapter 1.5 Models, applications and APIs

### Pillar 1: Core objective
Distinguish a **model**, an **application** and an **API**, and know which one you pay for in each case.

### Pillar 2: Key concepts

| Layer | Example | You pay by |
|---|---|---|
| Model | Grok 4.x | (Not sold directly; reached through an app or API) |
| Application | Grok chat app, Grok Bot | Subscription or plan |
| API | xAI Grok API | Tokens used (pay-as-you-go) |

An **API** (Application Programming Interface) is a door that lets one program ask another for something. With the xAI API, your program sends text and receives the model's answer.

> **Analogy.** The model is a kitchen. The app is a restaurant with a set menu and a monthly membership. The API is the kitchen's delivery hatch: you order exactly what you want and pay per dish.

### Pillar 3: SOP: choose the right layer
1. Do you just need answers or agents for yourself or your team? Use the app (Grok or Grok Bot).
2. Do you need AI inside your own website, product or data pipeline? Use the API.
3. Do you need both? Many businesses prototype in the app, then build on the API.

### Pillar 4: Pitfalls
- **A subscription does not include API credits** unless the provider explicitly says so. They are separate products with separate bills (Module 4).

---

## Chapter 1.6 Common terminology

| Term | Plain meaning | Example |
|---|---|---|
| Model | The trained AI that generates text | Grok 4.x |
| Prompt | What you send to the model | "Summarise this email" |
| Token | A chunk of text the model counts | "running" may be 1–2 tokens |
| Context window | The most tokens one request can hold | Reported 500K for one Grok model **[Third-party]** |
| Inference | Running the model to get an answer | Each message you send |
| Agent | AI that takes steps and uses tools | A Grok Bot agent posting to Slack |
| Tool / function calling | The model asks your code to run an action | "get_weather(city)" |
| RAG | Retrieval-augmented generation: look up documents first, then answer | Company handbook Q&A |
| Hallucination | Confident but wrong output | A made-up statistic |
| Latency | Time until an answer appears | 2 seconds to first token |

---

## Module 1 exercises

**Level 1 (beginner).** List five tasks from your week. Mark each "agent", "chat" or "neither", with one reason each.

**Level 2 (intermediate).** Run the comparison SOP from Chapter 1.2 on three tasks and two assistants. Present the scoring table.

**Level 3 (advanced).** Write a one-page brief for an always-on agent in your business: trigger, steps, tools, access needed, approval points, success measure and the risks.

## Knowledge check

1. What is the difference between Grok, Grok Bot and the Grok API?
2. Why is "Grok vs Claude" an unclear question?
3. What is inference, and why do you pay for it?
4. Give one reason a model hallucinates.
5. Does a chat subscription include API usage? How would you check?
6. Which company is Groq, and why does it matter?

**Answers:** (1) Grok is the model family and chat app; Grok Bot is the agent app; the API is developer access billed per token. (2) It does not say which product and which model. (3) Running the trained model on your prompt; it uses computing power each time. (4) It generates the most plausible text, not checked facts. (5) Not unless the provider says so; check the official pricing and plan pages. (6) A different company selling fast inference for other models; confusing them leads to wrong docs and keys.
