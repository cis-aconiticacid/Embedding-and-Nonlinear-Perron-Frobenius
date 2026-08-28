# Experiment Plan — Idea 1 (BSJ ℓ^(1/4) time-resolved test)

**Status**: REVISED 2026-04-30 after Codex pre-deployment review caught 4
CRITICAL issues. Awaiting smoke-test confirmation that depth-6 init=1e-3
escapes before deploying full sweep.
**Date**: 2026-04-30

---

## Claim under test (CORRECTED post-Codex review)

**Primary claim (BSJ-faithful per-layer test)**: In a depth-L bias-free
FC-ReLU network at small initialization (init_scale=1e-3) trained on MNIST
full-batch with lr=1.0 (saddle-to-saddle regime), at the moment of first
saddle escape, **each layer ℓ ∈ {1, ..., L}** satisfies

    peak_g_ℓ  =  max_{t ∈ [escape−100, escape+50]} σ_1(W_ℓ(t)) / σ_2(W_ℓ(t))
              ≥  ℓ^(1/4)

— directly testing the Bantzis–Simon–Jacot 2025 (arXiv:2505.21722) per-layer
lower bound. Note this is a **per-layer test**, NOT a cross-layer ratio
(the original draft had `g_L/g_1 ≥ L^(1/4)`, which Codex flagged as a
misreading of BSJ).

**Architecture (CRITICAL #2 fix)**: BSJ's formal setup assumes degree-L
homogeneity, which requires bias-free Linear layers. Primary runs use
`Linear(bias=False)`. We will also report a parallel run with biases
included (matching the rest of the M2 codebase) for comparison; the BSJ
claim only applies to the bias-free path.

**Secondary claims (descriptive)**:
- C-S1: empirical cascade ratio `peak_g_L / peak_g_1` is reported
  per-seed; not a primary endpoint, no hypothesis attached.
- C-S2: BSJ-per-layer pass count shows ordinal pattern across init scales:
  `lazy(1e-2) < main(1e-3) ≤ deep(1e-4)`. NOT a numeric threshold rule.
- C-S3: per-layer peak step lies within ±50 steps of escape; not at
  generic large-step events during plateau.
- C-S4 (descriptive): Spearman rank correlation between layer index and
  `peak_g_ℓ` is positive in a majority of seeds (depth-monotone trend).

**Anti-claims** (we are NOT claiming):
- A1: peak g_ℓ is a *tighter detector* than simplex_hilbert_diam. (Pilot
  showed it is NOT — peak g_ℓ fires AT escape, not before.)
- A2: g_ℓ at peak quantitatively MATCHES L^(1/4) (we only claim it
  *exceeds* the bound; equality is not predicted).
- A3: spectral structure is the cause of escape. (We measure correlation
  with theoretical bound, not causation.)

## Predeclared analysis (CORRECTED)

**Primary window**: `[escape − 100, escape + 50]` (escape-relative;
narrower than the original `[1800, escape + 50]` per Codex MAJOR fix).
A wider robustness window `[1800, escape + 50]` is also reported.

**Escape definition**: first step `t ≥ 2300` with `train_acc ≥ 0.20`,
where `train_acc` is computed on `X_train[:4000]` (a fixed subset; this
matches the M2 codebase convention but is NOT full-train accuracy —
Codex MAJOR clarification).

**Primary endpoint (BSJ-faithful per-layer)**: for each seed, count
`bsj_per_layer_n_pass` = #{ℓ : peak_g_ℓ ≥ ℓ^(1/4)} over ℓ = 1..L.

**Acceptance rule** (Codex CRITICAL #3 fix — separate, NOT AND-fused):
- Rule A — "BSJ-faithful holds empirically": ≥ 4/5 main-config seeds have
  `bsj_per_layer_n_pass ≥ 5` (out of 6 layers at depth=6). Layer 1 is
  trivial, so this is "5 of 6 nontrivial layers pass."
- Rule B (descriptive) — "empirical cascade ratio is large": report
  per-seed `peak_g_L / peak_g_1` median + IQR; NOT a binary
  acceptance rule.
- Rule C (ablation, ordinal — Codex MAJOR fix): predicted ordering is
  `bsj_per_layer_n_pass_median(lazy) < main ≤ deep`. Reported as binary
  "ordinal prediction holds" iff this ordering is satisfied. NOT a
  numeric threshold like `[0.9, 1.1]`.

## Configurations

⚠️ **Smoke test gate**: depth-6 init=1e-3 may not escape in 5000 steps
under this code path (Codex CRITICAL #4 — earlier
`EXPERIMENT_TRACKER.md` flagged it as infeasible). Single-seed smoke
test runs FIRST; full sweep only deploys if smoke shows clean escape.

If smoke confirms escape:

| ID | depth | width | init_scale | bias_free | seeds | purpose |
|---|---|---|---|---|---|---|
| MAIN_d6 | 6 | 256 | 1e-3 | True | s∈{0..4} | primary BSJ-faithful test |
| ABL_d6_lazy | 6 | 256 | 1e-2 | True | s∈{0..2} | ordinal: BSJ should weaken |
| ABL_d6_deep | 6 | 256 | 1e-4 | True | s∈{0..2} | ordinal: BSJ should hold ≥ main |
| CROSS_d3 | 3 | 256 | 1e-3 | False | s∈{0..2} | already collected, biased path |

EXT_d3 dropped from default (Codex MAJOR — run-matrix consistency).
Total Phase 1 deploy: 5 (MAIN_d6) + 3 (ABL_lazy) + 3 (ABL_deep) = 11
new training runs, all bias_free=True. CROSS_d3 stays as-is for
descriptive cross-depth comparison.

## Compute budget

- depth-3 width-256 5000-step run: ~3.5 min wall (CPU-bound on snap eigh)
- depth-6 width-256 5000-step run: ~7 min wall
- Sequential total Phase 1+2: 5×7 + 3×7 + 3×7 + 2×3.5 = 84 min ≈ 1.4 hr
- Within 8 GPU-hr budget by a factor of 6.

## Controls

**Matched-step control (CORRECTED per Codex MAJOR)**: at each
*contemporaneous* step `t` in the pre-escape window, compute Spearman
rank correlation across layers between (layer_index, g_ℓ(t)) and between
(layer_index, ‖ΔW_ℓ(t)‖_F). If the depth-monotone ordering of g_ℓ is
just "deeper-larger-step," then both rank correlations should be ≈ 1
together. If they decouple — e.g., g_ℓ shows depth-monotone correlation
but ‖ΔW_ℓ‖_F does not, or vice versa — the spectral structure is
genuinely independent of step magnitude.

**Matched-threshold**: not applicable to a peak-based theory-match test.
Idea 1 is NOT a lead-time race; simplex_hilbert_diam remains the best
detector. Reported in writeup as a side-bar.

## Implementation

- New driver: `refine-logs/run_idea1_full.py`
- Reuse: `refine-logs/spectral_dynamics.py` (`run_pass`)
- New analyzer: `refine-logs/analyze_idea1.py` (cross-config aggregation)
- Output dir: `refine-logs/runs/Idea1/<config_id>/<seed>/track.json`
- Aggregate: `refine-logs/runs/Idea1/AGGREGATE_idea1.json`
- Figures: `refine-logs/runs/Idea1/figures/{cascade_d6.png,
  bsj_ratio_vs_depth.png, init_ablation.png, matched_step_control.png}`

## Pre-deployment Codex review checklist

1. Is the bsj_ratio definition precise enough to avoid post-hoc tuning?
   (Window [1800, escape+50] is predeclared; peak operator is max-over-window.)
2. Does the matched-step depth-ordering control actually distinguish
   spectral structure from step-size? Specifically: can a hand-constructed
   counter-example (e.g. layer-uniform W update with depth-uniform g_ℓ
   spike) defeat it?
3. Should the ablation use `init_scale ∈ {1e-2, 1e-3, 1e-4}` or
   {1e-1, 1e-3, 1e-5} (wider span)? What does BSJ predict?
4. Are 5 seeds sufficient for cross-seed conclusions, or should main-config
   be 8 seeds?
5. What predeclared rule should govern "cascade FAILED in seed s"?
   (Currently: bsj_ratio < L^(1/4), but is that the right cut?)
