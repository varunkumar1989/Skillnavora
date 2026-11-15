# AI Master Course starter project

The runnable code for the SkillNavora AI Master Course (https://www.skillnavora.in/ai-master-course.html).
Everything runs **for free, offline**, out of the box. Add an Anthropic API key and the same code calls Claude for real.

## 1. Set up (5 minutes)

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q                            # 13 tests, all offline
```

## 2. Run the lessons

| Lesson | Command | What you see |
|---|---|---|
| Week 1: first model call | `python examples/w1_first_call.py` | answer, tokens, latency, cost |
| Week 3: agent with tools | `python examples/w3_agent_tools.py` | the tool calls and the final answer |
| Chunking | `python examples/l1_chunking.py` | four chunking strategies compared by recall@3 |
| Hallucinations and guardrails | `python examples/l2_guardrails.py` | injection check, PII removal, grounding, refusals |
| Latency and cost | `python examples/l3_latency_cost.py` | time per step, cost per request and per correct answer, caching |
| LLMOps and monitoring | `python examples/l4_llmops.py` | JSON logs, prompt versions, a release gate |
| PDF chatbot | `python examples/l6_pdf_chatbot.py` | answers with page citations, refusals, blocked requests |
| Evaluation | `python evals/run_evals.py` | scorecard on 16 golden questions; exit code 1 if the gate fails |
| Course basics | `python examples/course/01_calculator.py` … `06_eval_harness.py` | the six handbook examples |

## 3. Run the chatbot as an app

```bash
streamlit run app/streamlit_app.py          # chat UI, upload your own PDF
uvicorn api.main:app --reload               # REST API, open http://127.0.0.1:8000/docs
```

With Docker:

```bash
docker build -t pdf-chatbot .
docker run -p 8000:8000 --env-file .env pdf-chatbot
```

## 4. Switch to the real API

1. Create a key at https://platform.claude.com (keep it secret; never commit it).
2. `cp .env.example .env` and put the key after `ANTHROPIC_API_KEY=`.
3. Run any lesson again. The header line changes from "offline" to "Claude (claude-opus-5-5)".

Settings in `.env`:

| Variable | Default | Meaning |
|---|---|---|
| `ANTHROPIC_API_KEY` | empty | empty means offline mode |
| `CLAUDE_MODEL` | `claude-opus-5-5` | any current Claude model id |
| `CLAUDE_EFFORT` | `medium` | `low`, `medium`, `high`, `xhigh` or `max`: more effort is slower and dearer |
| `MIN_RETRIEVAL_SCORE` | `0.12` | below this, the chatbot says "I don't know" without calling the model |

Costs: each answer prints its token count and an estimated cost. Prices in `starter/config.py` are set for Claude Opus 5.5 ($4 input / $20 output per million tokens); change `PRICE_INPUT_PER_M` and `PRICE_OUTPUT_PER_M` if you use another model, and check the current price list before you plan a budget.

## 5. What is inside

```
starter/      the library: config, llm (offline or Claude), chunking, embeddings, store,
              pdf_loader, guardrails, costs, ops (logs, prompt versions, release gate), rag
examples/     one script per lesson (see the table above)
app/          Streamlit chat app
api/          FastAPI service: /health, /ask, /upload
evals/        golden questions, the eval runner and the baseline scores
tests/        pytest suite (offline; the real-API path is tested with a fake client)
data/         sample_policy.pdf, a fictional two-page HR policy
```

## 6. Honest limits

- Offline mode quotes the best-matching sentence. It is not a language model: it cannot combine facts or reason.
- The offline embedding counts shared words. Swap `starter/embeddings.py` for a real embedding model for production.
- The guardrail patterns catch common attacks only. Treat them as one layer, not as security.

Licence: free to use for learning and in your own portfolio projects.
