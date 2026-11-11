# Module 8: Advanced AI Applications and Agent Workflows

**Level:** Advanced · **Time:** about 4 hours · **Code:** `code/agent_tools.py`, `code/rag_assistant.py`

---

## Chapter 8.0 What is native and what needs extra tools

| Capability | Native in xAI / Grok Bot? | Status of that claim | If not native, use |
|---|---|---|---|
| Always-on agents with schedules | Yes, Grok Bot | **[Third-party]** | n8n, Make, Zapier, cron jobs |
| Connections to Gmail and Slack | Yes, Grok Bot | **[Third-party]** | Each app's API, n8n, Zapier |
| Learning a task by watching you | Yes, Grok Bot | **[Third-party]** | Recorded workflows, written SOPs |
| Function (tool) calling in the API | Yes | **[General; re-check docs]** | – |
| Server-side Web Search and X Search | Yes, billed per call | **[Third-party]** $5 per 1,000 calls | Your own search API |
| Structured (JSON) output | Likely | **[Unverified]** | JSON prompting plus validation |
| Embeddings endpoint | Not confirmed | **[Unverified]** | A separate embeddings provider |
| Vector database | No | – | pgvector, Qdrant, Pinecone, Chroma |
| Workflow orchestration and retries | Grok Bot handles its own agents; for custom systems, no | **[Unverified]** | Your code, n8n, LangGraph, Temporal |
| Human approval steps | Not documented here | **[Unverified]** | Build approval into your code (see `agent_tools.py`) |
| Evaluation and monitoring | No | – | Test sets, Langfuse, your logs (`usage_monitor.py`) |

---

## Chapter 8.1 AI agents and agentic workflows

### Pillar 1: Core objective
Know when to use a fixed workflow and when an agent is worth the extra cost and risk.

### Pillar 2: Key concepts
- **Workflow:** steps fixed in advance by you. Predictable, cheap.
- **Agent:** the model chooses the next step and the tools, in a loop, until done.
- **Agent loop:** think → act (tool) → observe result → repeat → answer.

| | Workflow | Agent |
|---|---|---|
| Steps | Known | Decided at run time |
| Cost | Lower | Higher (many model calls) |
| Reliability | Higher | Needs guardrails |
| Example | Every new lead → classify → add to CRM | "Research this company and draft a tailored pitch" |

**Rule:** start with a workflow. Add agent autonomy only where steps cannot be predicted, and prove it is better on a test set.

---

## Chapter 8.2 Tool calling and function calling

### Pillar 2: Key concepts
You describe each tool (name, description, JSON parameters). The model may reply with a **tool call** instead of text. **Your code** runs the tool and sends the result back. The model never runs code itself.

### Pillar 3: SOP (with `code/agent_tools.py`)
1. Define tools in `TOOLS` (the example has `get_order_status` and `issue_refund`).
2. Mark risky tools in `RISKY`; they need `approve()` to return True.
3. `run_agent()` loops: call model → run requested tools → add results → repeat, at most `max_steps` times.
4. **Test offline:** `python3 test_offline.py` runs a scripted model through four cases: lookup, refund blocked, refund approved, step limit reached.
5. **Expected trace:** `[{step 0, tool get_order_status, result shipped}, {step 1, final: "Your order has shipped."}]`.

### Pillar 4: Pitfalls
- Trusting tool arguments: validate them (does this customer own this order?).
- No step limit: a confused agent can loop and spend money.
- Tools with broad powers ("run any SQL"). Give narrow tools.

---

## Chapter 8.3 Retrieval-augmented generation (RAG)

### Pillar 2: Key concepts
**RAG** = find the relevant passages in your documents, put them in the prompt, and ask the model to answer only from them, with citations.

```
Documents ─► chunk ─► index (keywords or embeddings)
Question ─► search index ─► top 3–5 chunks ─► prompt: "answer only from these, cite ids"
         ─► answer with [source#chunk] citations ─► (optional) human check
```

- **Chunking:** split documents into passages (100–500 words) with some overlap so ideas are not cut in half.
- **Retrieval:** keyword search (BM25) or semantic search with embeddings, or both (hybrid).
- **Grounding:** instruct the model to say "not found" when the context lacks the answer.

### Pillar 3: SOP (with `code/rag_assistant.py`)
1. `chunk(text, source)` splits each document.
2. `Index(chunks)` builds a BM25 keyword index; `search(question)` returns the best chunks.
3. `answer(index, question)` builds the grounded prompt and calls the model; if nothing matches, it says so **without** calling the model (saves tokens and avoids invented answers).
4. Tests check chunk overlap, correct source retrieval and the honest "not found".

### Pillar 4: Pitfalls
- Chunks too large (cost, noise) or too small (missing context).
- Stale documents: re-index when policies change.
- Not checking citations: sample answers weekly and open the cited chunks.

---

## Chapter 8.4 Embeddings and vector databases

- An **embedding** turns text into a list of numbers so that texts with similar meaning have similar numbers. "Refund policy" and "money back rules" end up close together even with no shared words.
- A **vector database** stores embeddings and finds the nearest ones quickly.
- Use embeddings when users phrase questions differently from your documents; keep keyword search for exact terms (product codes, names). **Hybrid search** combines both.
- Whether xAI provides an embeddings model could not be verified; many teams use a separate embeddings provider and the Grok model only for the final answer.

---

## Chapter 8.5 Document processing and knowledge bases

| Step | Tooling | Check |
|---|---|---|
| Extract text from PDF, Word, web | PDF text extractors, OCR for scans | Spot-check tables and numbers |
| Clean | Remove headers, footers, page numbers | Compare word counts |
| Chunk and index | `rag_assistant.py`, or a vector database | Retrieval test with 20 questions |
| Metadata | Source, date, owner, access level | Filter by user permissions |
| Refresh | Scheduled re-index | Changed documents logged |

---

## Chapter 8.6 Multi-step workflows, memory and orchestration

- **Prompt chaining:** extract → analyse → draft → check, with validation between steps.
- **Routing:** classify the request, send it to the right workflow or model (`route()` in `usage_monitor.py`).
- **Agent memory:** short-term (the conversation), long-term (facts saved to a database and retrieved later). Save only what is needed, with the user's permission.
- **Orchestration:** something must run steps, retry failures, store state and resume. For Grok Bot agents the product does this **[Third-party]**; for custom systems use code, n8n or a workflow engine.

### Cost example **[Estimate, third-party prices]**
A research agent running 8 model steps of 3,000 input and 300 output tokens on Grok 4.7, plus 3 web searches, costs about **$0.077 per run**, or **$92.88 a month** at 40 runs a day.

---

## Chapter 8.7 Human-in-the-loop approvals

Put a person in the loop:
- Before actions that move money, delete data, or send messages to customers or the public.
- When the model's confidence is low or sources conflict.
- For a random sample of outputs every week (quality review).

`agent_tools.py` blocks `issue_refund` unless `approve()` returns True; the agent is told to say a person will review it.

---

## Chapter 8.8 Evaluation, reliability, security and permissions

| Area | Practice |
|---|---|
| Evaluation | Test set of real tasks; pass/fail plus cost per successful task |
| Reliability | Step limits, retries with backoff, idempotent actions (safe to repeat) |
| Permissions | Least privilege: read-only by default; separate accounts per agent |
| Secrets | Agents never see raw keys; tools hold them |
| Audit | Log every tool call with inputs, outputs and who approved |
| Prompt injection | Treat content from emails, web pages and documents as data, not instructions (Module 10) |

## Module 8 exercises

**Level 1.** Classify five of your processes as workflow or agent, with reasons.

**Level 2.** Add a `cancel_order` tool to `agent_tools.py`, marked risky, and write two tests (approved, not approved).

**Level 3.** Build a RAG assistant over 10 of your own documents, measure retrieval accuracy on 20 questions, and estimate monthly cost for 200 questions a day.

## Knowledge check
1. Who runs a tool: the model or your code?
2. Why should `answer()` skip the model call when nothing is retrieved?
3. When are embeddings better than keywords?
4. Name two actions that need human approval.
5. Which capabilities in this module could not be verified as native to xAI?

**Answers:** (1) Your code. (2) It saves tokens and prevents invented answers. (3) When users use different words from the documents. (4) Moving money; sending external messages (also deleting data). (5) Structured output, embeddings, human approval, and orchestration for custom systems.
