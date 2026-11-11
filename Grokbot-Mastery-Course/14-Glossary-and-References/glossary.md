# Glossary of Technical Terms

| Term | Meaning |
|---|---|
| Agent | AI software that takes steps towards a goal, choosing actions and tools in a loop |
| API | Application Programming Interface: a defined way for programs to request services from each other |
| API key | Secret string that identifies your account to an API; whoever holds it can spend your money |
| Attention | The transformer mechanism that relates each token to the others |
| Authentication | Proving who you are |
| Authorisation | Deciding what you are allowed to do |
| Backoff (exponential) | Waiting 1 s, 2 s, 4 s… between retries |
| BPE (byte-pair encoding) | A tokenizer method that merges frequent character pairs into tokens |
| BM25 | A keyword-ranking formula used for search |
| Cached input | Repeated prompt content billed at a lower rate when the provider supports caching |
| Chunk | A passage of a document stored for retrieval |
| Context window | Maximum input + output tokens in one request |
| cURL | Command-line tool for making HTTP requests |
| Embedding | A list of numbers representing the meaning of a text |
| Endpoint | A specific API web address for one kind of request |
| Environment variable | A named setting outside your code, used for secrets and configuration |
| Few-shot prompting | Giving a few examples in the prompt |
| Fine-tuning | Further training a model on your own examples |
| finish_reason | Why generation stopped (`stop`, `length`, tool call) |
| Function / tool calling | The model requests that your code run a named function with arguments |
| Generative AI | AI that creates new content |
| Grok | xAI's family of language models and its chat product |
| Grok Bot | xAI's agent app for always-on agents (reported launch 11 August 2026) |
| Groq | A different company selling fast inference for other models |
| Grounding | Making the model answer from supplied sources |
| Hallucination | Fluent, confident, false output |
| HTTP | The protocol used to send web requests and responses |
| Human-in-the-loop | A person reviews or approves before an action |
| Idempotent | Safe to repeat without duplicating the effect |
| Inference | Running a trained model to produce output |
| JSON | A text format for structured data |
| Latency | Delay before and during a response |
| LLM | Large language model, trained to predict text |
| max_tokens | Your cap on the length of the model's answer |
| Mixture-of-experts (MoE) | A model design where only part of the network runs per token |
| Model ID | The exact name used to select a model in the API |
| Multimodal | Handling more than text: images, audio, video |
| Orchestration | Running, connecting and recovering multi-step workflows |
| Parameters | The learned numbers inside a model |
| Prompt | The input you send to a model |
| Prompt caching | Reusing processing of a repeated prompt prefix at lower cost |
| Prompt injection | Text that tries to override the model's instructions |
| RAG | Retrieval-augmented generation: retrieve relevant documents, then answer from them |
| Rate limit | Maximum requests or tokens allowed per time period |
| Reasoning tokens | Internal tokens some models generate before answering; often billed |
| Server-sent events (SSE) | A streaming format: `data:` lines sent as the answer is produced |
| Stateless | Keeping no memory between requests |
| Streaming | Sending output tokens as they are produced |
| System prompt | Builder's instructions sent with every request |
| Temperature | A setting for randomness of output |
| Token | A unit of text the model reads, writes and bills |
| Tokenizer | The component that splits text into tokens |
| Transformer | The neural network design behind modern LLMs |
| Vector database | A database that finds the nearest embeddings quickly |
| Webhook | A URL that another system calls when an event happens |
| Workflow | Fixed sequence of steps defined in advance |
| Brand bible | A short, verified reference for a brand: story, approved phrases, prices, products and claims. Every bot checks its output against it. |
| Chief of staff bot | A manager bot that takes an outcome, hires specialist bots, coordinates them and checks their work. |
| Group chat (bots) | A shared chat where a chief and its specialist bots receive requests and report progress. |
| Plugin (Grok Bot) | A connected app, such as Gmail or Notion, that a bot can read from or act in. Grok Bot calls connections plugins. |
| Routine | A job a bot runs on its own, on a schedule or when an event happens. It can be paused and resumed. |
| Skill (Grok Bot) | A repeatable process with its trigger, inputs, steps, checks, hand-back and approval points. |
| Bot template | A copy of a bot's memory, skills and instructions, published with a shareable link. |
| Verified vs unverified fact | Verified: taken from the brand's official source. Unverified: derived or assumed, and must be confirmed with the client. |
| Escalation | Handing a conversation from an AI agent to a human when it cannot or should not answer. |
| Data fiduciary | The party responsible for keeping personal data safe and lawful, even when a vendor's tools handle it. |
