# Round 2 — Devil's-Advocate Review

**Reviewer**: Codex MCP gpt-5.x xhigh, threadId `019ddc5a-347d-7ec1-9df5-dba04f849929`.
**Date**: 2026-04-30.

---

## Final ranking from Codex

1. **#1-refined** (time-resolved per-step ℓ^(1/4) gap + per-layer onset ordering).
   Works 8/10, negative 7/10. Tudisco-fit 6/10. *"This is the strongest sharp theory test. I would stake my name on piloting it first."*

2. **#5** (Perron-ray on hidden ReLU Gram).
   Works 6/10, negative 4/10. Tudisco-fit 9/10. *"Good co-authored note material, weak as a standalone flagship claim unless the signal is visibly nontrivial and earlier than C4."*

3. **#3** (Rank-one staircase / discrete mode births).
   Works 8/10, negative 6/10. Tudisco-fit 7/10. *"Highest upside after #1, but only if you define births before looking. Otherwise it will not survive review."*

4. **#2** Operator leaderboard — CUT. *"Too easy to attack as fishing expedition."*

5. **#6** Residual transfer — CUT. *"Too literature-adjacent; may give mixed/contradictory results."*

## Per-idea decisive tests Codex demanded

| Idea | Decisive matched-step / matched-threshold test |
|---|---|
| #1 | Within matched ‖ΔW_ℓ‖_F bins, does deeper-first onset ordering persist? Does estimated onset order survive seed aggregation? |
| #5 | Step-binned comparison of PF-angle and λ_1/λ_2 between escape-window snapshots and non-escape snapshots with the same ‖ΔZ‖_F. PF-stabilization must NOT be explained by Davis-Kahan with larger ‖ΔZ‖_F. |
| #3 | Step-matched permutation of event times. Event times must be earlier than C4 under same `median+3·MAD` rule. Births must be defined by **preregistered persistent-crossing rule with dwell time** before inspection. |

## What Codex would actually pilot in 8 GPU-hours

1. **#1-refined first** — cleanest yes/no theory test, cheapest to run.
2. **#5 second** — same snapshots/infrastructure as #1; PF bridge.
3. **#3 third** — piggybacks on same spectral traces; ONLY with hard preregistered event definition.

If one of #1/#5/#3 wins → use **#10 (small-init phase transition: 1e-2 / 1e-3 / 1e-4)** as the regime ablation on the winner only.

## What Codex flagged for "would I stake my name?"

> *"On #1-refined and #5, yes. On #3, yes only with the event rule fixed before inspection. On #2 or #6 as the lead claim, no."*
