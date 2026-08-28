# Round 1 — Codex Brainstorm (10 ideas)

**Reviewer**: Codex MCP gpt-5.x xhigh, threadId `019ddc5a-347d-7ec1-9df5-dba04f849929`.
**Date**: 2026-04-30.
**Trigger**: pivot from yesterday's null-result Procrustes direction to direct-eigenspace-measurement framing of the spectral-decomposition / saddle-to-saddle bridge.

---

## Direction sent to Codex

Direct empirical measurement of eigenspace dynamics of representations and empirical NTK during saddle-to-saddle escape in small ReLU networks. Pivot: yesterday's Procrustes scalar metric direction was killed by matched-step + matched-threshold controls; the Codex Round 1 CRITICAL "you never measured R_t directly, so eigenspace claim is overreach" becomes the new contribution: measure top-k eigenspaces directly, not via derived scalar metrics.

Setting: depth-3 FC-ReLU MNIST, init=1e-3, lr=1.0, full-batch CE, 5000 steps, plateau ~1500-2300, escape ~2500, ramp ~2500-3500. 5-8 seeds, constant Δ=5 cadence. M2 milestone done. Reusable infra: `proc_dynamics.py`, `run_proc.py`, `analyze_proc.py`, `control_matched_step.py`, `control_baselines.py`. 8 GPU-hours total budget. Constraints: must survive matched-step + matched-threshold controls by design; must connect to Tudisco's PF / sub-homogeneity language.

Banlist: Procrustes residual / scaled Procrustes / CKA / alignment_gain / any new scalar pair-metric on consecutive Z without matched controls.

## Codex's 10 ideas

| # | Title | Risk | Effort | Codex pick? |
|---|---|---|---|---|
| 1 | Layerwise low-rank-bias law (Bantzis-Simon-Jacot ℓ^(1/4) test) | LOW-MED | 1-2 days | top-3 |
| 2 | Which operator carries the escape (G_ℓ, C_ℓ, eNTK, output Gram) | MED | 2-3 days | top-3 |
| 3 | Rank-one staircase (Jacot discrete mode-births) | LOW-MED | 1-2 days | — |
| 4 | Operator leaderboard for predictive lead time | LOW | 1-2 days | — |
| 5 | Perron-ray stabilization of hidden ReLU Gram (Tudisco bridge) | LOW-MED | 1 day | **top-1** |
| 6 | Residual transfer into top eNTK eigenspace at escape | MED | 2-3 days | top-3 |
| 7 | Label-subspace emergence of top modes | MED | 1-2 days | — |
| 8 | Transient common subspace across layers | MED-HIGH | 1-2 days | — |
| 9 | Hessian / eNTK / Gram triangle (escape-direction mapping) | HIGH | 4-7 days | — |
| 10 | Small-init phase-transition control (1e-2 / 1e-3 / 1e-4) | MED | 1-2 days | ablation |

Codex's recommended first 8 GPU-hours: **5 → 1 → 2/6**. "One PF-facing claim, one sharp theory test, one operator-comparison result; all three publishable if they fail."

## Full text of each idea

(See raw Codex response — preserved verbatim in conversation log.)

## Targeted novelty searches that followed

| Idea | Closest prior | Novelty hit | Refinement |
|---|---|---|---|
| #1 (raw) | Bantzis-Simon-Jacot 2025 already showed *end-state* single dominant singular value, deeper-first, on MNIST 6-layer FC ReLU. | HIGH novelty hit on the qualitative claim. | Refine to **time-resolved per-step ℓ^(1/4) scaling + per-layer escape ONSET ordering** (when does each layer's gap open? synchronous or layered?) — that's still novel. |
| #5 | 2505.17907 (FIM as PF object in random-weight 2-layer ReLU); silent alignment papers. | LOW-MED (closest is infinite-width random-weight, not finite-width saddle-to-saddle). | Hidden ReLU Gram `Z_ℓ Z_ℓ^T` is a genuine PF object (nonneg). PF gap + Perron vector overlap to post-escape reference, deepest-first. |
| #2 | 2510.00468 (eNTK at end-of-training); 2402.05271 (weight-eNTK alignment). | None do per-step *operator leaderboard* during saddle escape. | Novel. |
| #6 | 2402.05271 (alignment increases monotonically); silent alignment. | None localize residual transfer to escape window. | Novel. |
| #3 | Jacot 2021 theoretical; nobody has time-resolved mode-birth test. | Novel. | OK. |

## Filtering decision

**Carried to Phase 4 (devil's-advocate)**: #5 (Tudisco bridge, lowest risk), #1-refined (sharp BSJ test), #2 (operator leaderboard), #6 (residual transfer), #3 (rank-one staircase).

**Dropped or held**: #4 (overlaps with #2, fold in), #7 (overlap with neural collapse lit), #8 (speculative), #9 (4-7 days, blows budget; defer), #10 (use as ablation, not standalone).
