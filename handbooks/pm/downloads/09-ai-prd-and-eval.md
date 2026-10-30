---
title: AI PRD additions and evaluation plan
---

# AI PRD additions (add to the standard PRD)

| Section | Content |
|---|---|
| Intended use | Who, what tasks, which channels |
| Prohibited use | e.g., financial/medical/legal advice; actions without approval |
| Non-AI baseline | What simpler solution we compared against |
| Data & sources | Approved sources, owners, freshness, permissions, retention |
| Model & architecture | Prompting / RAG / fine-tuning / tools; model choice rationale |
| Autonomy level | L0–L4 per capability; approval checkpoints |
| Guardrails | Input/output filters, refusals, escalation, kill switch |
| Evaluation | Test set composition, rubric, severity levels, launch gates |
| Quality targets | e.g., ≥ 90% correct with citation; 100% correct routing for high-risk intents |
| Safety & privacy | Injection tests, PII handling, vendor terms, logging |
| Latency & cost | p95 target; cost per request budget |
| Human-in-the-loop | Who reviews what, SLAs, feedback loop |
| Monitoring | Sampling, drift, incident process, re-eval on every change |
| Fallback & rollback | What users see when AI fails; how to disable |

# Evaluation plan

| Category | # cases | Expected behaviour | Scoring | Gate |
|---|---|---|---|---|
| Answerable (single source) | | answer + citation | correct/incorrect | ≥ 90% |
| Answerable (multi-source) | | answer + citations | rubric 1–5 | ≥ 4.0 avg |
| Not covered | | say so + route | pass/fail | 100% |
| High-risk intents | | route to human | pass/fail | 100% |
| Adversarial / injection | | refuse, no leak | pass/fail | 100% |
| Unauthorised data | | deny | pass/fail | 100% |

Re-run on every model, prompt, source or tool change. Review all failures by severity.
