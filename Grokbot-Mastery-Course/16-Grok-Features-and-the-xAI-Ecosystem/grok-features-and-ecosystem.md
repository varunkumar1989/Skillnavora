# Grok Features and the xAI Ecosystem

**Level:** Beginner to intermediate · **Time:** about 2 hours · **Sources:** the walkthrough transcript supplied for this course, plus the third-party coverage noted in Module 4. Every product detail carries a status tag. Plans, prices, model names and feature availability change often.

**Status tags:** **[Transcript]** = stated in the transcript, not checked · **[Third-party]** = from a non-xAI source · **[Check]** = confirm on the official page before you rely on it · **[General]** = stable concept.

---

## Chapter 16.0 The map: what xAI offers

The transcript describes xAI as the company behind an ecosystem of products **[Transcript]**. Since February 2026, xAI has been owned by SpaceX, and in May 2026 it was reported to be folded into SpaceX as its AI division; Grok continues as a product **[Third-party, check]**:

| Product | What it is (plain words) | Closest equivalent named in the transcript | Chapter |
|---|---|---|---|
| **Grok models** (chat) | Large language models you talk or reason with | ChatGPT, Gemini, Claude chat | 16.1 |
| **Grok Imagine** | Image creation | GPT Images, Nano Banana | 16.2 |
| **Grok Build** | Building websites and code from a prompt | Claude Artifacts, GPT Sites | 16.3 |
| **Grok Bot** | Always-on agents that work for you | ChatGPT Dots, Gemini Gems | 16.4 |
| **Grok Voice** | Speaking with Grok | Voice modes in other assistants | 16.5 |
| **xAI API** | Access to Grok for developers and products | OpenAI or Anthropic APIs | 16.6 |
| **X search** | Searching X (formerly Twitter) posts from inside Grok | Web search tools | 16.7 |

**Plain-English summary:** the models are the brain; Imagine, Build and Voice are tools that use it; Grok Bot is the agent that runs jobs on a schedule; the API lets your own software use the same brain.

---

## Chapter 16.1 Grok models and chat

**What it is [Transcript]:** Grok is a family of large language models. The transcript names **Grok 4.7** as the most important general model available to everyone at the time of recording (October 2026), with cheaper and faster models also available.

**Key facts from the transcript [Transcript, Check]:**
- The **context window** is **500,000 tokens**, which the transcript converts to about 375,000 words (see 16.8).
- Grok 4.7 offers **four reasoning levels**. In a bot you must choose the level **[Transcript, Check]**.
- Compared with other models named in the transcript, a bigger window is not automatically a better answer.

**How it works:** you type, Grok reads the whole conversation (within the context window), and replies. Each reply uses tokens for input and output, and costs are based on those tokens **[General]**.

**How to use it well:**
1. Put the goal, the audience, the facts you want used, and the format you want in one message (see Module 5).
2. Pick a reasoning level. Use a higher level for multi-step analysis and a lower one for quick rewrites **[Check]**.
3. Start a new chat when the topic changes, so old context does not crowd the new question.
4. Treat the answer as a first draft. The transcript's rule: AI output is the baseline, not the finish line **[Transcript]**.

**Example:** "You are reviewing a pricing page for a D2C sweets brand. Using only the price list I paste below, list any price that does not match the offer text. Output a table: item, price in list, price in offer, match yes/no." Paste the price list. Check every row yourself before using it.

---

## Chapter 16.2 Grok Imagine (images)

**What it is [Transcript]:** Grok Imagine creates images. The transcript compares it with GPT Images and Nano Banana in other ecosystems.

**How it works [General]:** you describe a picture in words, and a text-to-image model generates it. You can usually refine by asking for changes ("make the box blue, keep the lettering").

**How to use it for a brand:**
1. Give the brand's visual rules first: colours, fonts, product shapes. Paste them as text.
2. Write one prompt per asset: subject, setting, lighting, format (square for Instagram, 16:9 for a banner), and what must not appear.
3. Check every output for wrong text, extra fingers, invented logos and product shapes that do not match the real product.
4. Never publish an image that shows a real product with a shape or claim the product does not have.

**Example:** "Square 1080×1080 image. A box of assorted Indian sweets on a brass tray, warm Diwali lamps behind, soft light. The box is cream with a green ribbon. No text, no logo, no people." The transcript's creative bot used this kind of brief with an image tool to make brand images **[Transcript]**.

**Check [Check]:** which image tool your plan includes, usage limits, and the licence for commercial use.

---

## Chapter 16.3 Grok Build (websites and code)

**What it is [Transcript]:** Grok Build is for building websites and code. The transcript compares it with Claude Artifacts and GPT Sites **[Transcript]**.

**How it works [General]:** you describe the app or page, the tool generates code and a preview, and you iterate by describing changes. Some builders also host the result.

**How to use it:**
1. Describe the page: sections in order, the call to action, the products or services, and the contact method.
2. Give it real facts and mark them clearly: prices and certifications should come from the client, not from memory.
3. Test forms, links and mobile layout before you publish.
4. Keep any keys, passwords or webhook URLs out of the prompt. Paste them into the builder's secure settings yourself (see Chapter 15.6).

**Example:** "Build a one-page site for a sweets brand: hero with the tagline 'Guilt-free traditional sweets' (client-approved), a product grid with the 6 products and prices in the attached list, a corporate gifting section, an inquiry form that sends details to our webhook, and a footer with the address and phone."

**Check [Check]:** whether the current plan includes Build, hosting limits, and who owns the code.

---

## Chapter 16.4 Grok Bot (agents)

**What it is [Transcript]:** Grok Bot is the agentic platform. You create bots that run jobs for you; bots can use connected apps, run on schedules, and coordinate with other bots. The full method is in Chapter 15 and Modules 7–8.

**Key facts from the transcript [Transcript, Check]:**
- Grok Bot is included in the **SuperGrok plan and above** (the transcript calls it the Premium plan); the minimum is **$30 a month**.
- A bot has details, library and a virtual computer. Under details you find **routines**.
- Bots can have their own email address, created once.

**How to use it:** follow Chapter 15.2 (one bot, one job), 15.3 (plugins, skills, routines) and 15.4 (memory, shared files).

**Check [Check]:** current plans, the feature list in each plan, and whether team plans are available in your country.

---

## Chapter 16.5 Grok Voice and live voice chat

**What it is [Transcript]:** Grok Voice is the voice mode of Grok. In Grok Bot, a **live voice chat** button lets you speak to a bot; the transcript shows the bot answering by voice and ending the call itself **[Transcript]**.

**How it works [General]:** your speech is turned into text, the model replies, and the reply is turned back into speech. Voice is faster for planning, but harder to check later, so write down the decisions.

**How to use it:**
1. Use voice for briefing and quick decisions.
2. After each call, ask the bot to write a summary and a list of actions, and save it to the shared folder.
3. Confirm any decision that involves money, a client or a published message in writing.

**Example:** speak: "Chief, add a check that every price on the website matches the price list before any ad goes out." Then ask in text: "Summarise that instruction as a rule and add it to your memory."

**Check [Check]:** which voice features are in your plan, and whether recordings are stored.

---

## Chapter 16.6 The xAI API (for developers)

**What it is [Transcript]:** the xAI API lets developers and solution builders use Grok inside their own software or voice agents **[Transcript]**.

**How it works [General]:** your code sends a request (a message, optional tools, settings such as reasoning level) to an endpoint, and gets a reply in JSON. You pay for tokens, and some server-side tools are charged per call.

**Third-party reference [Third-party]:** one non-xAI source reports **$5 per 1,000 calls** for server-side tools such as Web Search and X Search, on top of tokens. Verify on xAI's pricing page before quoting it.

**Minimal example (pseudo-code, check the current SDK and endpoint names):**
```
response = client.chat(model="<model name from xAI's model page>",
                       reasoning="medium",
                       messages=[{"role": "user", "content": "Summarise these 3 reviews in 50 words."}])
print(response.text)
```

**Safety rules for API keys:** never put a key in code you share, in a chat, or in a screenshot. Store it as an environment variable or a secret. Rotate it if it leaks. Module 10 covers this in depth.

**Check [Check]:** the current endpoint, SDK, model names and pricing; the transcript's model names are not verified here.

---

## Chapter 16.7 X search and live posts

**What it is [Transcript]:** Grok can search X (formerly Twitter) posts. The transcript says bots can search X and summarise competitors' posts, included in the plan **[Transcript, Check]**.

**How it works [General]:** the model calls a search tool, reads the returned posts, and summarises them with their links. Results are only as good as the search and the posts found.

**How to use it:**
1. Ask a specific question with a time window: "Posts from the last 30 days by these three brands about pricing or offers."
2. Ask for the post links and the date of each post.
3. Check each claim by opening the post. Posts can be deleted, edited, or taken out of context.
4. Never copy a rumour or a competitor's private information into client work.

**Example:** "Search X for posts by @brandA in the last 30 days about Diwali offers. List each post: date, offer, link. Mark any you could not verify."

---

## Chapter 16.8 Context windows, tokens and compaction, with examples

**Definition:** a **context window** is the maximum number of tokens a model can consider in one request. It holds your instructions, your files, the chat history, memory and the answer. **Token:** a piece of text the model reads and writes, roughly three-quarters of an English word **[General]**.

**Example:** a 500,000-token window is about 375,000 English words (transcript's conversion, rule of thumb). A 40-page PDF is roughly 15,000–20,000 words, so a few PDFs fit easily. The window still gets used up by system instructions, memory and the whole chat, so long projects fill it faster than you expect.

**When the window fills, the transcript names four techniques [Transcript]:**
- **Truncation:** remove the oldest messages from the active context. Example: the first brief disappears, so the bot forgets a rule you gave on day one.
- **Summarisation:** replace old discussion with a shorter summary. Example: 40 messages become a 10-line note of decisions.
- **Retrieval:** fetch only the relevant earlier parts. Example: the bot searches the shared folder for "invoice terms" instead of rereading everything.
- **Context compaction:** a general name for the above. Example: a new working session starts with a summary of key facts.

**The transcript's warning:** every one of these is a summary, so it can be wrong or incomplete. Keep important rules in memory or in a written document, and check outputs **[Transcript]**.

**The transcript's point about bigger windows:** a model that reads 1 million tokens is not automatically more intelligent. Intelligence depends on how well it uses what it reads **[Transcript]**.

---

## Chapter 16.9 Plans and pricing (what the transcript says)

| Item | What the transcript says | Status |
|---|---|---|
| Plans | Free, Plus, Premium, Super | [Transcript, Check] |
| Grok Bot access | Premium and above; minimum $30 a month | [Transcript, Check] |
| Token prices and per-call tool fees | See Module 4 | [Third-party] |

**Check [Check]:** all prices and plan contents on xAI's own pricing page before you advise a client.

---

## Chapter 16.10 Checklist: before you rely on any Grok feature

- [ ] I have checked the plan that includes the feature.
- [ ] I have checked the official page for model names, limits and prices.
- [ ] Output is reviewed by a person before it is published or sent.
- [ ] No key, password or private data is pasted into a prompt.
- [ ] Facts about a brand come from that brand, and are marked verified or unverified.
