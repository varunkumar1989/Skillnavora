# Module 2: Platform Architecture and Technical Foundations

**Level:** Beginner to intermediate · **Time:** about 3 hours

> **Source note.** xAI has not published the internal architecture of its production models in a form that could be checked for this course. Chapters 2.1 to 2.8 describe how modern LLM platforms work in general **[General]**. Where a Grok-specific figure is given, it is labelled.

---

## Chapter 2.1 How an LLM platform works inside

### Pillar 1: Core objective
Understand the main parts of an LLM system well enough to reason about speed, cost and failure.

### Pillar 2: Key concepts

**Topic 2.1.1 The transformer.** Almost all modern LLMs, including the Grok family, are built on the **transformer** design. It reads all input tokens together and uses **attention** to decide which earlier tokens matter for each new one.

> **Analogy.** Reading the sentence "The trophy did not fit in the suitcase because *it* was too big", you link "it" to "trophy". Attention is the model's way of making such links across thousands of tokens.

**Topic 2.1.2 Parameters and mixture-of-experts.** Parameters are the learned numbers inside the model. Some large models use **mixture-of-experts** (MoE): only part of the network runs for each token, which saves compute. xAI published Grok-1 (2024) as an MoE model **[General, public reporting]**; the design of current Grok 4.x models is not documented here **[Unverified]**.

**Topic 2.1.3 The serving stack.**
```
 Your app ─► API gateway (auth, rate limits, billing)
          ─► Router (picks model and server)
          ─► Inference servers (GPUs run the model)
          ─► Safety filters (inputs and outputs)
          ─► Usage meter (counts input, cached and output tokens)
          ─► Response (streamed or complete)
```

### Pillar 3: SOP: map the stack to your symptoms
| Symptom | Likely layer | First action |
|---|---|---|
| 401 error | Gateway (authentication) | Check the API key |
| 429 error | Gateway (rate limit) | Slow down, retry with backoff |
| Very slow first word | Inference servers (queue) | Try a smaller model; check status page |
| Refusal | Safety filters | Rephrase legitimately; check the policy |
| Bill higher than expected | Usage meter | Log tokens per request |

### Pillar 4: Pitfalls
- Assuming bigger always means better. Smaller models are faster and cheaper and often good enough.
- Treating the model as a database; it does not look up facts unless given tools.

---

## Chapter 2.2 Input and output processing and the context window

### Pillar 1: Core objective
Know what goes into a request, what comes out, and the limit that binds both.

### Pillar 2: Key concepts
- **Input** = system prompt + developer instructions + conversation history + your message + any documents or images + tool definitions.
- **Output** = the generated answer (plus any reasoning tokens the model produces, if the model reports them; see Module 3).
- **Context window** = the maximum number of tokens input and output can use together in one request. Reported figures include **500,000 tokens for Grok 4.7** and **1,000,000 tokens for Grok 4.3** **[Third-party, unverified]**.
- **Max output tokens** = a separate cap on the answer length, set by the model and by you (the `max_tokens` parameter).

> **Analogy.** The context window is a desk. Everything the model must consider (instructions, history, documents) has to fit on the desk at once. When the desk is full, something must come off.

### Pillar 3: SOP: check whether a job fits
1. Estimate tokens: words × 1.33 for English (Module 3). A 300-page book of about 90,000 words is about 120,000 tokens **[Estimate]**.
2. Add system prompt, history and expected output.
3. Compare with the model's context window on xAI's models page.
4. If it does not fit, or would be costly, split the document or use retrieval (Module 8).

### Pillar 4: Pitfalls
- A large window does not guarantee the model uses every part well; details in the middle of very long inputs can be missed. Test with questions about specific passages.
- Long prompts cost more, and some models charge a higher rate above a threshold (reported above 200K tokens for Grok 4.7) **[Third-party]**.

---

## Chapter 2.3 Conversation history and memory

### Pillar 1: Core objective
Understand that an API model is **stateless** and that "memory" is something the application builds.

### Pillar 2: Key concepts
- **Stateless:** each API request is independent. The model does not remember the previous request.
- **Conversation history:** to continue a chat, the app resends earlier messages with every new one. That is why long chats cost more (Module 3, example 3).
- **Product memory:** chat apps and agent products may store notes about you and add them to future prompts. How Grok Bot stores agent memory is not documented here **[Unverified]**.
- **Server-side conversation storage:** some APIs can keep a conversation on the server and let you refer to it by ID. Check xAI's documentation for whether and how it is offered **[Unverified]**.

### Pillar 3: SOP: manage history in your own app
1. Store messages as a list of `{role, content}` objects.
2. Before each request, count tokens in the list.
3. If over budget, drop the oldest turns or replace them with a short summary.
4. Always keep the system prompt.
5. **Test:** have a 20-turn conversation and confirm the bot still follows its rules.

### Pillar 4: Pitfalls
- Sending the entire history forever: cost grows with every turn.
- Summaries can lose details; keep key facts (names, order numbers) in a separate "facts" block.

---

## Chapter 2.4 System prompts, user prompts and developer instructions

### Pillar 1: Core objective
Use message **roles** to separate rules from requests.

### Pillar 2: Key concepts
| Role | Who writes it | Purpose | Example |
|---|---|---|---|
| `system` (or developer) | You, the builder | Persona, rules, format, limits | "You are a support assistant for Acme. Answer only from the policy. Reply in under 120 words." |
| `user` | The end user | The request | "Can I return shoes after 40 days?" |
| `assistant` | The model | Previous answers (resent as history) | "Returns are accepted within 30 days…" |
| `tool` | Your code | Results of a tool call | `{"order_status": "shipped"}` |

The system prompt is sent with **every** request, so its length is multiplied by the number of requests (Module 3, example 4).

### Pillar 3: SOP: write a system prompt
1. Role and audience. 2. What to do. 3. What never to do. 4. Output format and length. 5. What to say when unsure.
6. **Test:** try ten normal questions and five attempts to break the rules.

### Pillar 4: Pitfalls
- Putting secrets (API keys, internal prices) in a system prompt: users can sometimes extract it.
- Contradictory rules; the model will follow one at random.

---

## Chapter 2.5 Model selection

### Pillar 1: Core objective
Pick the cheapest model that meets the quality bar.

### Pillar 2: Key concepts
Reported xAI models and prices per 1M tokens **[Third-party, unverified]**:

| Model (as reported) | Input | Output | Cached input | Context | Note |
|---|---|---|---|---|---|
| Grok 4.7 | $2.00 | $6.00 | $0.50 | 500K | $4 / $12 above 200K input |
| Grok 4.3 | $1.25 | $2.50 | $0.20 | 1M | One source only |
| Grok Build 0.1 | $1.00 | $2.00 | not stated | not stated | Coding model |

One source states that all Grok text models share the same per-token rates, which contradicts the table. **Confirm on xAI's models page.**

### Pillar 3: SOP: choose a model with a test set
1. Collect 20 real inputs with good answers written by a person.
2. Run each candidate model on all 20.
3. Score correctness (pass or fail) and cost (from the `usage` field).
4. Choose the cheapest model that passes at least, say, 18 of 20.
5. Re-run the test whenever the model or prompt changes.

### Pillar 4: Pitfalls
- Choosing by a leaderboard rather than by your own tasks.
- Hard-coding a model ID that is later retired; keep it in configuration.

---

## Chapter 2.6 Streaming responses

### Pillar 1: Core objective
Understand streaming and when to use it.

### Pillar 2: Key concepts
With **streaming**, the server sends tokens as they are produced, usually as **server-sent events** (lines beginning `data:`). Without streaming, you wait for the full answer.
- **Time to first token (TTFT):** how soon the first word appears.
- **Tokens per second:** how fast the rest arrives.

Streaming does not change cost; it changes how fast the answer *feels*.

### Pillar 3: SOP
1. Use streaming for chat interfaces.
2. Use non-streaming for background jobs where you need the whole result (for example JSON).
3. Handle a stream that stops mid-way: show a "retry" button and log the error.

### Pillar 4: Pitfalls
- Parsing JSON before the stream has finished.
- Forgetting usage totals usually arrive at the end of the stream.

---

## Chapter 2.7 Multimodal capabilities

### Pillar 1: Core objective
Know which inputs and outputs beyond text a model may support, and how to check.

### Pillar 2: Key concepts
**Multimodal** models accept or produce images, audio or video. Grok models have supported image understanding since Grok-2 **[General, public reporting]**, and xAI has offered image generation **[General]**. Which current models accept images, audio or files, and how those inputs are counted in tokens, must be confirmed on xAI's models page **[Unverified]**.

### Pillar 3: SOP
1. Check the model card for supported input types.
2. Send one small test image; read the `usage` field to see how many tokens it cost.
3. Resize images to the smallest size that keeps the needed detail.

### Pillar 4: Pitfalls
- Sending full-resolution photos when a thumbnail would do: images can cost many tokens.
- Assuming OCR-quality reading of small text; test it.

---

## Chapter 2.8 Limitations, latency and response generation

### Pillar 1: Core objective
Predict where answers go wrong and why they are slow.

### Pillar 2: Key concepts
| Limitation | Effect | Mitigation |
|---|---|---|
| Hallucination | Wrong facts stated confidently | Ground in documents (RAG), require citations, human review |
| Knowledge cut-off | Outdated answers | Search tools, supplied documents |
| Non-determinism | Different answers to the same prompt | Lower temperature; tests that allow variation |
| Long-context recall | Missed details | Retrieval; put key facts near the question |
| Latency | Slow responses | Smaller model, shorter output, streaming, caching |

**Latency ≈ queue time + (input processing) + (output tokens ÷ generation speed).** Output length usually dominates, so shorter answers are faster.

**Topic 2.8.1 Reasoning models.** Some models "think" before answering, producing internal reasoning tokens. These add latency and may be billed as output. Whether and how Grok models report reasoning tokens must be checked in xAI's documentation **[Unverified]**.

---

## Chapter 2.9 The complete request-response lifecycle

### API request (developer view)
```
[1] Your code builds messages: system + history + user (+ tools)
[2] HTTPS POST to the API with the API key in a header
[3] Gateway checks key, rate limit and balance
[4] Tokenizer converts text to tokens; prompt cache checked
[5] Model processes input, then generates output token by token
[6] (Optional) Model requests a tool call → your code runs it → step [1] again
[7] Tokens streamed back; final usage block: input, cached, output tokens
[8] Your code shows the answer, logs usage and cost
```

### Agent run (Grok Bot style, conceptual) **[General; Grok Bot internals not documented]**
```
Trigger (schedule / event / you)
   └─► Agent plans steps ─► Acts in an app (read Gmail, post to Slack)
         └─► Observes result ─► Decides next step ─► ... ─► Reports / stops
Each step = one or more model requests = tokens used against your plan or bill
```

## Module 2 exercises

**Level 1.** Draw the API lifecycle from memory and label where cost is measured.

**Level 2.** For a chatbot with a 400-token system prompt, explain what happens to cost at turn 1, turn 10 and turn 30, and propose a history policy.

**Level 3.** Design a model-selection test for a customer-support use case: 20 test cases, scoring rule, cost metric, and the decision rule.

## Knowledge check
1. What does "stateless" mean for an API model?
2. Which roles exist in a chat request, and which one carries your rules?
3. Does streaming reduce cost?
4. Name two ways to reduce latency.
5. What is the reported price switch for Grok 4.7 above 200K input tokens, and how confident are we in it?

**Answers:** (1) The model keeps no memory between requests; the app resends history. (2) System (or developer), user, assistant, tool; the system role carries the rules. (3) No, it only improves perceived speed. (4) Shorter outputs, smaller model, caching, streaming. (5) Reported $4/$12 per 1M instead of $2/$6 **[Third-party]**; unverified, confirm on xAI's page.
