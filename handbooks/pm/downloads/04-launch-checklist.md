---
title: Launch checklist
---

# Launch checklist — [feature] (Tier 1 / 2 / 3)

## Product & quality
- [ ] Acceptance criteria met; QA and UAT signed off
- [ ] Accessibility check (keyboard, screen reader, contrast)
- [ ] Performance/load test against p95 targets
- [ ] Feature flag, kill switch, rollback plan and owner

## Data & measurement
- [ ] Success metrics and guardrails defined with baselines
- [ ] Events validated in staging; dashboard live; alerts configured
- [ ] Experiment/holdout plan (if applicable)

## Risk & compliance
- [ ] Security review · [ ] Privacy/consent review · [ ] Legal review of claims/terms · [ ] Fraud/abuse review

## Go-to-market
- [ ] Positioning and messaging · [ ] Pricing/plan changes · [ ] Channels and calendar · [ ] Sales enablement / FAQ

## Support & operations
- [ ] Help articles · [ ] Support macros and training · [ ] Escalation path · [ ] Ops capacity

## Rollout
| Stage | Exposure | Gate criteria | Date | Owner |
|---|---|---|---|---|
| Internal | 1% | no critical errors | | |
| Canary | 5% | error rate < …; latency < … | | |
| Experiment | 50/50 | primary + guardrails | | |
| Full | 100% (+ holdout) | readout approved | | |

## After launch
- [ ] Daily monitoring during ramp · [ ] Feedback collection · [ ] Retrospective scheduled (2–4 weeks)
