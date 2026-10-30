---
title: Experiment plan and readout
---

# Experiment plan — [name]

| Item | Detail |
|---|---|
| Hypothesis | We believe [change] for [eligible users] will [move metric] because [reason]. |
| Primary metric | Definition: numerator / denominator / window |
| Secondary metrics | |
| Guardrails | e.g., complaint rate, payment errors, AOV, latency |
| Unit of randomisation | user / session / account / geography / time (switchback) |
| Eligibility | who is included / excluded |
| Variants | control: … · treatment: … |
| Baseline & MDE | baseline …% ; minimum detectable effect … points |
| Sample size per arm | (α = 0.05, power 80%) |
| Duration | full weeks; start/end dates |
| Stop rule | fixed horizon, or a sequential method designed for peeking |
| Analysis plan | test, CI, segments (pre-registered), SRM check |
| Decision rule | ship if …; iterate if …; stop if … |
| Owners | PM, analyst, engineer |

# Readout — [name]

**Decision requested:** …  **Recommendation:** …

| Metric | Control | Treatment | Difference (95% CI) | p-value |
|---|---|---|---|---|
| Primary | | | | |
| Guardrail 1 | | | | |

- **Sample ratio check:** planned vs observed split.
- **Segments (exploratory):** …
- **Caveats:** novelty, seasonality, data issues.
- **Learning:** what we now believe and why.
- **Next steps:** rollout plan, holdout, follow-up tests.
