# Module 5: Prompt Engineering and Advanced Instructions

**Level:** Beginner to advanced · **Time:** about 3 hours

> Techniques here are **[General]**: they work across Grok, GPT, Claude and Gemini. Test every prompt on the exact Grok model you will use, because models respond differently.

---

## Chapter 5.1 What prompt engineering is

### Pillar 1: Core objective
Write prompts that give correct, consistent, cheap answers on the first try.

### Pillar 2: Key concepts
**Prompt engineering** is designing the instructions and context you give a model so that it produces the output you need. It is closer to writing a clear brief for a new colleague than to programming.

> **Analogy.** Asking a new intern "do the report" gets a guess. Asking "summarise last week's 12 support tickets into 3 themes, one line each, for the Monday stand-up" gets the job done.

### Pillar 4: Pitfalls
- Vague verbs ("improve", "handle") with no success criteria.
- Long prompts written to sound clever; length costs tokens on every request.

---

## Chapter 5.2 The structure of a strong prompt

### Pillar 2: Key concepts: the six parts

| Part | Question it answers | Example |
|---|---|---|
| Role | Who should the model act as? | "You are a support agent for an online shoe shop." |
| Context | What background does it need? | "Our return window is 30 days; refunds take 5–7 days." |
| Task | What exactly should it do? | "Answer the customer's question." |
| Constraints | What must it avoid? | "Do not promise exceptions. If unsure, offer a human." |
| Format | What should the output look like? | "Max 80 words. Plain text. End with a next step." |
| Examples | What does good look like? | One sample question and answer |

### Pillar 3: Before and after

**Before (weak)**
```
Write something about our new product for social media.
```
**After (strong)**
```
Role: You are a social media copywriter for a fitness app aimed at busy Indian professionals.
Context: We launched "10-minute desk workouts" today. Free for 14 days.
Task: Write 3 LinkedIn post options.
Constraints: No medical claims. No hashtags beyond 3. No emojis in the first line.
Format: Each option under 60 words, numbered 1–3.
```
The second prompt is longer, but it removes rounds of corrections, which cost more tokens overall.

---

## Chapter 5.3 Role-based, zero-shot and few-shot prompting

### Pillar 2: Key concepts
- **Role prompting:** assign a persona to set expertise and tone.
- **Zero-shot:** no examples, only instructions. Good for simple, common tasks.
- **Few-shot:** a few input-output examples to show the pattern. Good for classification, tone matching and unusual formats.

### Pillar 3: Few-shot example: classify support tickets
```
Classify each ticket as BILLING, DELIVERY, PRODUCT or OTHER. Reply with the label only.

Ticket: "I was charged twice for order 4471." → BILLING
Ticket: "My parcel says delivered but I don't have it." → DELIVERY
Ticket: "The left shoe is a size bigger than the right." → PRODUCT

Ticket: "Can I change the address on my order?" →
```
Expected output: `DELIVERY`.

### Pillar 4: Pitfalls
- Examples that are all one label: the model learns to always answer that label. Balance them.
- Too many examples: each one costs input tokens on every request. Three to five usually suffice.

---

## Chapter 5.4 Reasoning prompts and safe practice

### Pillar 2: Key concepts
**Chain-of-thought** means asking the model to work through steps before answering. It helps with maths, logic and multi-step decisions. Reasoning models already do this internally; for them, a direct, clear task is often enough.

Safe practice:
- Ask for the **answer plus a short justification**, not pages of reasoning, to save output tokens.
- For decisions, ask the model to list assumptions so a human can check them.
- Do not treat the model's stated reasoning as proof; verify the result itself.

### Pillar 3: Example
```
A customer bought 3 items at ₹1,200, ₹850 and ₹450 with a 10% discount on orders over ₹2,000.
Calculate the total. Show the calculation in at most 3 lines, then the final amount on its own line.
```
Expected: subtotal ₹2,500; discount ₹250; **total ₹2,250**.

---

## Chapter 5.5 Structured output and JSON

### Pillar 1: Core objective
Get output that a program can read without errors.

### Pillar 2: Key concepts
**JSON** (JavaScript Object Notation) is a text format for data: `{"name": "Asha", "score": 82}`. Many APIs, including OpenAI-compatible ones, can be asked to return JSON, and some support a **schema** that the output must match. Check xAI's documentation for its structured-output options **[Unverified]**.

### Pillar 3: Prompt for JSON
```
Extract these fields from the email below and reply with JSON only, no other text:
{"customer_name": string, "order_id": string or null, "issue": one of ["refund","delay","damage","other"], "urgent": true or false}

Email: """Hi, it's Ravi. Order 88213 arrived with a cracked screen. I need this fixed before Friday!"""
```
Expected:
```json
{"customer_name": "Ravi", "order_id": "88213", "issue": "damage", "urgent": true}
```
**Validate in code:** parse the JSON; if parsing fails or a field is missing, retry once with the error message, then send to a human.

### Pillar 4: Pitfalls
- Trusting JSON without parsing it.
- Asking for prose and JSON in the same reply.

---

## Chapter 5.6 Templates and reusable system instructions

### Pillar 3: A reusable system prompt template
```
You are {assistant_name}, a {role} for {company}.
Audience: {audience}.
Do: {main_tasks}.
Never: {forbidden_actions}.
If information is missing or you are unsure, say so and {fallback_action}.
Format: {format_rules}. Maximum {max_words} words.
Language: reply in the user's language.
```
Fill the braces in code, store the template in version control, and give each version a number so you can link quality changes to prompt changes.

### Pillar 4: Pitfalls
- Editing the live prompt without testing. Keep a test set of 20 questions and re-run it after every change.

---

## Chapter 5.7 Prompt debugging

### Pillar 3: SOP: when output is wrong
1. **Reproduce:** run the same input three times. Is the error consistent?
2. **Locate:** is it missing information (add context), misunderstanding (clarify task), wrong format (add an example) or ignoring a rule (move the rule up, make it specific)?
3. **Change one thing** at a time.
4. **Re-test** on the full test set, not only the failing case.
5. **Record** the change and the result.

| Symptom | Likely fix |
|---|---|
| Answer too long | "Maximum 80 words" plus `max_tokens` |
| Invents facts | "Answer only from the context below; if not found, say 'I don't know'" |
| Ignores format | Add one example of the exact format |
| Inconsistent labels | Few-shot examples and a closed list of labels |
| Wrong language | "Reply in the language of the user's message" |

---

## Chapter 5.8 Context optimisation and token saving

| Change | Before | After | Saving |
|---|---|---|---|
| Remove pleasantries and repetition in the system prompt | 900 tokens | 300 tokens | 600 tokens per request |
| Send relevant chunks instead of whole policy | 20,000 tokens | 2,000 tokens | 18,000 tokens per request |
| Ask for bullet answers | 600-token answers | 150-token answers | 450 output tokens |
| Batch 20 classifications in one request | 20 requests | 1 request | System prompt sent once, not 20 times |

Use Module 3's calculator to convert these savings into money.

## Module 5 exercises

**Level 1.** Rewrite three vague prompts from your work using the six-part structure.

**Level 2.** Build a few-shot classifier for five categories in your business. Test it on 20 real examples and report accuracy.

**Level 3.** Create a versioned system prompt and a 20-question test set. Make three improvements, measure accuracy and average tokens after each, and report the best version.

## Knowledge check
1. Name the six parts of a strong prompt.
2. When is few-shot better than zero-shot?
3. Why should you validate JSON in code?
4. What is the first step when a prompt gives a wrong answer?
5. How does batching save tokens?

**Answers:** (1) Role, context, task, constraints, format, examples. (2) For classification, unusual formats or matching a tone. (3) The model can return invalid or incomplete JSON. (4) Reproduce it several times. (5) The system prompt and instructions are sent once for many items.
