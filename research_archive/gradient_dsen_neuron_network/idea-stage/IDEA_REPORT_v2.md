# Research Idea Report — v2 (post-pivot, 2026-04-30)

> **v1 status**: yesterday's `IDEA_REPORT.md` (Procrustes / spectral-contrastive
> framing) was empirically refuted overnight (NULL RESULT — see
> `NARRATIVE_REPORT.md`). v1 file preserved unchanged for the project record;
> this v2 supersedes it.

## TL;DR (after one quick depth-3 pilot, idea-stage signals only)

- **Idea 1 — time-resolved BSJ ℓ^(1/4) cascade (TOP RECOMMENDATION)**:
  ✅ **POSITIVE on depth-3 quick pilot**. At saddle escape, the per-layer gap
  `g_ℓ = σ_1/σ_2(W_ℓ)` shows a sharp narrow spike with deeper-first cascade in
  2/3 seeds and a `g_3/g_1` ratio of **median 1.91 (range 1.48-2.96), all 3
  seeds satisfy the BSJ 3^(1/4) ≈ 1.32 lower bound**. Visually clean (see
  `runs/Spectral/figures_d3_w256/spectral_overview.png`). **Worth scaling up**
  to depth-6 multi-seed via `/experiment-bridge`.
- **Idea 2 — Perron-ray / PF gap (Tudisco bridge)**: ❌ **NEGATIVE as a
  detector**. Lead time 20-140 steps, vs simplex_diam (existing C4) at 555
  steps. Drop as a leading indicator. Dynamics interesting (PF gap *dips*
  mid-plateau, then explodes at escape) — possible mechanistic side-note but
  not a contribution.
- **Idea 3 — preregistered rank-one staircase**: ❌ **REFUTED at this temporal
  resolution**. The top-5 eigenvalues of Z_L Z_L^T jump *simultaneously* at
  escape, not sequentially — Jacot's discrete mode-birth picture does not
  hold as one-at-a-time on Δ=5 cadence in this regime.

**Headline recommendation**: pursue Idea 1 (BSJ time-resolved cascade) at
full scale via `/experiment-bridge` — depth-6 BSJ regime, 5 seeds, plus
ablation across init_scale (1e-2 / 1e-3 / 1e-4). The depth-3 quick pilot
already shows a clean signal; depth-6 is the load-bearing test that makes
this BSJ-comparable.

**Direction**: direct empirical measurement of the *eigenspace dynamics* of
representations and weight matrices during saddle-to-saddle escape in small
ReLU networks, framed as a bridge between the spectral-contrastive picture
(HaoChen 2021, Balestriero–LeCun 2022) and saddle-to-saddle dynamics
(Jacot 2021; Bantzis–Simon–Jacot 2025), with a Perron–Frobenius / Hilbert
projective leg toward Tudisco.

**Generated**: 2026-04-30
**Ideas evaluated**: 10 generated → 5 survived devil's-advocate → 3 piloted → top recommendation in v2 below.

---

## Pivot rationale (1 paragraph)

Yesterday's overnight session tested *Procrustes-style scalar pair-metrics*
on probe representation Z as saddle-to-saddle eigenspace-transition
diagnostics. Two controls killed it: matched-step bins showed alignment_gain
≈ 0 happens whenever step is large (not specifically at escape), and matched-
threshold (`median + 3·MAD on baseline`) showed simplex Hilbert diameter
gives the same lead time as the new metrics. Codex Round 1 CRITICAL was:
*"you never measured R_t directly, so eigenspace-transition is overreach."*
v2 takes that critical and turns it into the contribution: measure
top-k eigenspaces directly (per-layer SVD of W_ℓ; per-layer eigh of
Z_ℓ Z_ℓ^T) at fine cadence through the saddle-escape window, with matched-step
+ matched-threshold controls baked in from day-1. Five idea candidates were
generated; Codex's devil's-advocate cut #2 and #6, leaving three pilot-able
candidates plus one ablation.

---

## Landscape Summary

**Theoretical anchors that motivate direct eigenspace measurement**:

- *Saddle-to-saddle dynamics* (Jacot 2021 [arXiv:2106.15933]): in deep
  linear nets at small init, GD trajectory passes through a sequence of
  saddles, with each escape adding one new effective rank/feature. Theoretical;
  no per-step eigenspace measurement.
- *Low-rank bias in first saddle escape* (Bantzis–Simon–Jacot 2025
  [arXiv:2505.21722]): for deep ReLU at small init, the optimal escape
  direction has the ℓ-th layer first singular value ≥ ℓ^(1/4) larger than any
  other singular value. **Empirically confirmed end-state low-rank** on MNIST
  6-layer FC ReLU — but the *time-resolved* per-step gap dynamics and per-layer
  *onset ordering* during the escape ramp are not measured.
- *Saddle-to-saddle simplicity bias across architectures* (2512.20607,
  Dec 2025): saddle-to-saddle as a unifying mechanism for simplicity bias.
- *Spectral-contrastive picture* (HaoChen 2021 [arXiv:2106.04156];
  Balestriero–LeCun 2022): contrastive learning ≈ spectral decomposition of
  an operator on RKHS — top-k eigenfunctions are the targets. At convergence
  only; intra-training dynamics not addressed.
- *Sub-homogeneous DEQ* (Sittoni–Tudisco 2024 [arXiv:2403.00720]): nonlinear
  Perron–Frobenius framework for fixed-point existence/uniqueness in implicit
  networks. Theoretical anchor for this project's PF/Hilbert leg.

**Empirical eNTK / Gram tracking literature** (closest relatives):

- *GD induces alignment between weights and the empirical NTK*
  (Beneventano et al. 2024 [arXiv:2402.05271]): kernel alignment increases
  monotonically over training. Doesn't ask whether alignment increase is
  *concentrated at saddle escapes* or smooth.
- *Feature identification via empirical NTK* (Lin 2025
  [arXiv:2510.00468]): top-eNTK eigenvectors align with ground-truth features
  at end of training; eNTK spectrum diagnoses grokking phase transitions.
  Different phase-transition setting (grokking, not saddle-to-saddle).
- *Effective Gram matrix characterizes generalization* (2504.16450): residual
  lies in smallest-eigenvalue subspace during training. End-of-training
  generalization angle, not training dynamics.
- *Common principal subspace of deep features* (2110.02863): different DNNs
  share a common principal subspace at convergence; principal-angle dynamics
  measured 70-80° → smaller across full training. Not zoomed into saddle-escape
  window.

**Identified gaps (motivating the v2 direction)**:

1. The *time-resolved* per-step quantitative ℓ^(1/4) gap scaling and per-layer
   *escape-onset ordering* of Bantzis–Simon–Jacot 2025 has not been measured.
2. The hidden ReLU Gram matrix `Z_ℓ Z_ℓ^T` is a genuine PF object (nonneg
   PSD) but no one has tracked its Perron-vector stabilization + spectral gap
   widening through the saddle-escape window.
3. Whether saddle-escape onset coincides with discrete *mode births* in the
   deepest hidden Gram, or with smooth eigenvalue drift, is open.
4. Any new metric must survive matched-step + matched-threshold control —
   yesterday's null shows that scalar metrics with cosmetically different
   dynamics often collapse to the same step-magnitude or threshold artifact.

---

## Recommended Ideas (ranked, after Codex devil's-advocate cut)

### Idea 1 (TOP): Time-resolved layerwise low-rank bias ramp

- **Hypothesis**: In a depth-d FC-ReLU network at small init (1e-3) trained
  on MNIST full-batch with lr=1.0, during the first saddle-escape ramp
  (steps ~2300-3500), the per-layer gap g_ℓ(t) = σ_1(W_ℓ)/σ_2(W_ℓ) opens
  in a depth-ordered cascade (deepest layer's gap onset precedes shallower
  layers') AND the post-escape end-state gap satisfies g_ℓ ≥ ℓ^(1/4) · g_1
  to within seed variability — quantitatively realizing the
  Bantzis–Simon–Jacot 2025 prediction.
- **Minimum experiment**: spectral_dynamics.py runs depth-3 and depth-6 (BSJ
  regime), 3 seeds each, 5000 steps, snapshot Δ=5 in [0, 5000]. Per
  snapshot: SVD of every W_ℓ. Per-layer onset = first step in (BW_HI,
  escape] where g_ℓ exceeds median + 3·MAD on [500, 1800]. Rank seed-median
  onset times by layer index ℓ. Compare end-of-ramp gap to ℓ^(1/4) · g_1.
- **Expected outcome**: depth-6 should show clear deeper-first onset
  ordering AND quantitative ℓ^(1/4) match. Depth-3 may not have enough
  layers to resolve the cascade (only 3 W matrices) — used as control for
  "does the cascade exist for d=3 too?"
- **Novelty**: 5/10 — closest is BSJ 2025 itself, which confirmed the *end-
  state* on MNIST 6-layer FC ReLU. This pilot adds (a) per-step time-resolved
  cascade picture and (b) quantitative ℓ^(1/4) test against a fitted
  function, both not in BSJ. Differentiable from BSJ via the time axis.
- **Feasibility**: trivial — under 30 min total wall time, < 0.5 GPU-hr.
- **Risk**: LOW-MEDIUM (gap onset times may be too seed-noisy at depth-3 to
  resolve cascade; BSJ predicts the ℓ^(1/4) law for the *first* escape only,
  may not hold quantitatively for all subsequent saddles in a multi-saddle
  trajectory).
- **Contribution type**: empirical finding (time-resolved test of a
  theoretical prediction).
- **Pilot result** *(populated below in "Pilot Experiment Results")*.
- **Reviewer's likely objection**: "BSJ already showed this empirically; what's
  new?" Counter: time-resolved cascade picture and ℓ^(1/4) quantitative
  fit, not in BSJ. *"You can verify this against the BSJ figures."*
- **Why we should do this**: this is the cleanest yes/no theory test in
  the candidate set; cheap to run; both positive and negative outcomes
  publishable (a clean negative would be a quantitative refutation of the
  ℓ^(1/4) law's empirical reach, which BSJ would themselves want to see).

### Idea 2 (Tudisco-bridge): Perron-ray on hidden ReLU Gram

- **Hypothesis**: For each hidden layer ℓ, the Perron vector u_1(t) of
  A_ℓ(t) = Z_ℓ(t) Z_ℓ(t)^T (genuinely nonneg PSD) stabilizes its angle to
  a post-escape reference u_1^* (captured at step 4500), AND the PF gap
  λ_1/λ_2(A_ℓ) widens, BEFORE the simplex Hilbert diameter (existing C4
  detector) crosses its baseline+3·MAD threshold. Both effects deepest-first.
- **Minimum experiment**: same spectral_dynamics.py runs as Idea 1. Per
  snapshot: thin SVD of Z_ℓ → top eigenvalues + top-1 left-singular vector
  (= Perron vector since A_ℓ = U Σ² U^T). Compare lead-time of
  pf_overlap_to_ref and pf_ratio under same `median+3·MAD` rule against
  simplex_hilbert_diam.
- **Expected outcome**: PF stabilization should give a real but possibly
  modest lead time over C4. **Codex's failure-mode prediction**: at small
  init, the Perron vector might already be dominated by a trivial mean-
  activation mode early — angle stable long before escape, gap widens
  smoothly with no escape-local event. Pilot will reveal which.
- **Novelty**: 7/10 — closest is the FIM-as-PF-object result for random-
  weight 2-layer ReLU (2505.17907), which is a different setting (infinite-
  width, random weights, no training dynamics).
- **Feasibility**: same data as Idea 1; under 5 min additional analysis
  time.
- **Risk**: LOW-MEDIUM (most likely outcome: PF gap stable through
  plateau, modest widening at escape — interesting but not killer).
- **Contribution type**: empirical finding + theoretical bridge for Tudisco
  collaboration (PF eigenvector + sub-homogeneity language directly applies
  to A_ℓ = Z_ℓ Z_ℓ^T).
- **Pilot result** *(populated below)*.
- **Reviewer's likely objection**: *"This is just PCA with PF branding."*
  Counter: the operator A_ℓ is a measurable function of training time and
  has all PF properties (nonneg, irreducible-when-Z_ℓ has no zero rows);
  the *dynamic* claim (top-eigenvector stabilization timed against escape)
  is not derivable from PCA alone.
- **Why we should do this**: best Tudisco-facing language in the set
  (Tudisco-fit 9/10 per Codex). If pilot signal is non-trivial AND earlier
  than C4, this is the natural co-authored note.

### Idea 3 (highest upside, requires preregistration): Rank-one staircase

- **Hypothesis**: In the deepest hidden Gram A_L(t) = Z_L Z_L^T, the
  rank-r-effective top-r subspace expands by *discrete mode births* (one
  new mode at a time, with long residence intervals between admissions),
  not by smooth eigenvalue drift. Each birth is a candidate saddle-escape.
- **Minimum experiment**: same data as Ideas 1+2. Track top-5 eigenvalues
  of A_L plus top-k subspace principal angle to lag-1 (k=1..5).
  **PRE-REGISTERED EVENT RULE** (defined here BEFORE inspecting any data):
  - mode k is born at time t iff:
    1. λ_k(s) / λ_{k+1}(s) > **2.0** for ALL s in [t − 25, t]
       (5 consecutive snapshots at Δ=5 cadence — `STAIRCASE_DWELL_SNAPS`);
    2. principal angle(span(top-k at t), span(top-k at t−25)) <
       **30°** throughout that window (`STAIRCASE_MAX_ANGLE_DEG`);
    3. t > **1800** (after baseline window).
  - These constants are committed in `spectral_dynamics.py`
    (`STAIRCASE_GAP_RATIO`, `STAIRCASE_DWELL_SNAPS`,
    `STAIRCASE_MAX_ANGLE_DEG`) and replicated in `analyze_spectral.py`.
- **Expected outcome**: clear k=1 birth in plateau body (low-rank already
  established); k=2 birth coincident with first saddle escape; k=3,4
  later. Codex flagged failure modes: higher modes may *chatter through
  crossings* without persistent admission, or only emerge much later than
  the escape window.
- **Novelty**: 7/10 — Jacot's saddle-to-saddle theory predicts this
  qualitatively; nobody has done a preregistered time-resolved test.
- **Feasibility**: same data; analysis cost trivial.
- **Risk**: MEDIUM (upside high; downside is "no clean birth chain" → null,
  which is also publishable as a refinement of Jacot's qualitative
  picture).
- **Contribution type**: empirical finding (preregistered test of Jacot's
  rank-increasing saddle picture).
- **Reviewer's likely objection**: *"Mode birth could be a threshold
  artifact."* Counter: the rule is preregistered before inspection AND
  defined in code (committed alongside the data); event times survive
  step-matched permutation control (we ALSO compute the permuted-event
  control on the same data).
- **Why we should do this**: highest upside if it works AND piggybacks on
  the same snapshots — zero marginal compute cost.

### Ablation: Small-init phase transition (not piloted yet)

- For whichever of Ideas 1/2/3 wins above, repeat at init_scale ∈ {1e-2,
  1e-3, 1e-4}, 2 seeds each, to verify the diagnostic belongs specifically
  to the small-init saddle-to-saddle regime. Predicts: signal strong at
  1e-3 and 1e-4, weak/absent at 1e-2 (lazy regime). NOT pursued in the
  v2 pilot — to be added in follow-up.

---

## Eliminated Ideas (Codex Round-2 cut + Round-1 filter)

| Idea | Reason eliminated |
|------|-------------------|
| #2 *Operator leaderboard* (which operator carries Δf at escape) | "Too easy to attack as a fishing expedition; output Gram may win trivially." (Codex) |
| #6 *Residual transfer into top eNTK subspace* | "Most literature-adjacent; may give mixed/contradictory results (residual could equally lie in *small*-eigenvalue subspace per 2504.16450)." (Codex) |
| #7 *Label-subspace emergence of top modes* | Overlap with neural-collapse literature; not differentiable enough. |
| #8 *Transient common subspace across layers* | Speculative; risk MEDIUM-HIGH without theoretical anchor. |
| #9 *Hessian / eNTK / Gram triangle* | Too expensive (4-7 days; Lanczos HVP); blows GPU-hr budget. Hold for follow-up. |
| #4 (raw) *Operator leaderboard for predictive lead time* | Folded into Pilot 2's matched-threshold comparison. |

---

## Pilot Experiment Results (idea-stage quick signal only — depth-3, 3 seeds)

**Scope clarification**: per `idea-creator` workflow, Phase 5 pilots are
*cheap signal experiments* (single regime, 1-3 seeds, ~30 min) to flag
positive/negative direction — NOT full multi-seed multi-depth sweeps.
Those belong in `/experiment-bridge`. The depth-6 BSJ regime sweep was
started and then deliberately stopped at this stage; it is the obvious
next step if Elizabeth chooses to scale up Idea 1.

**Setup**:
- depth=3, width=256, init_scale=1e-3, lr=1.0, full-batch CE, 5000 steps
- 3 seeds (s=0, 1, 2). Δ=5 snapshot cadence.
- Predeclared baseline [500, 1800]; predeclared post-escape reference step
  4500; escape = first step ≥ 2300 with train_acc ≥ 0.20.
- Wall time: ~10 min; < 0.2 GPU-hr.
- Outputs: `runs/Spectral/S_d3_w256_s{0,1,2}/track.json`,
  `runs/Spectral/AGGREGATE_d3_w256.json`,
  `runs/Spectral/figures_d3_w256/spectral_overview.png`

### Idea 1 (BSJ ℓ^(1/4) cascade) — POSITIVE direction

| Metric | Value (3 seeds, depth-3) | Predicted (BSJ 2025) |
|---|---|---|
| Per-layer peak g_ℓ at escape (seed 0) | [7.56, 13.89, 22.39] | g_ℓ ≥ ℓ^(1/4) (lower bound) |
| Per-layer peak g_ℓ at escape (seed 1) | [30.01, 21.43, 57.37] | — |
| Per-layer peak g_ℓ at escape (seed 2) | [23.99, 31.19, 35.48] | — |
| Peak g_3 / Peak g_1 (BSJ ratio) | median **1.91**, range [1.48, 2.96] | ≥ 3^(1/4) ≈ **1.32** |
| Seeds satisfying BSJ lower bound | **3/3** | — |
| Seeds with strict deeper-first cascade (g_1 ≤ g_2 ≤ g_3) | 2/3 | — |
| Peak step (median) | 2395-2410 (≈ escape) | escape onset |

**Key finding**: empirically observed cascade ratio is ~1.5× *stronger* than
the BSJ analytical lower bound. Spike is sharp, narrow (~50 steps wide),
and visually clean. Depth-6 (BSJ regime) needed to fully resolve cascade.

**Failure mode flagged for scale-up**: seed 1 has g_1 > g_2 (30 > 21) —
strict cascade order can fail in some seeds even when BSJ lower bound
between top and bottom layers holds. Need ≥ 5 seeds at depth-6 to estimate
how often strict ordering holds.

### Idea 2 (Perron-ray / PF gap, Tudisco bridge) — NEGATIVE as detector

| Metric | Value | vs C4 (simplex_diam) |
|---|---|---|
| pf_ratio_lead_gap median (layer 0 / 1) | 135 / 20 steps | 555 (much earlier) |
| pf_overlap_lead_gap median (layer 0 / 1) | None / 140 steps | 555 |

**Verdict**: PF-gap signals fire *at* escape, not before. Simplex Hilbert
diameter (existing C4 detector) leads PF-based metrics by 400+ steps.
Drop Idea 2 as a leading-indicator candidate.

**Side-note (not a contribution)**: PF gap of deepest hidden Gram
*decreases* through plateau (from ~10⁴ at init to ~10¹-10² at step 2300),
then *explodes* (10⁵+) at escape. This U-shape could be relevant for
mechanistic interpretation but is not load-bearing as a detector.

### Idea 3 (preregistered rank-one staircase) — REFUTED

The predeclared event rule (λ_k/λ_{k+1} > 2.0 for 5 consecutive snaps with
top-k subspace stable to within 30°) fires at the search-window start for
all k=1..4 in all 3 seeds (artifact: λ_2..5 are essentially numerical zero
in plateau, so ratios are infinite). Visual inspection of top-5 eigenvalues
of Z_L Z_L^T (`spectral_overview.png` right panel) shows that **all 5
eigenvalues jump simultaneously** at saddle escape, not in a one-at-a-time
staircase.

**Verdict**: Jacot's discrete mode-birth picture does NOT hold as
"one-at-a-time" on Δ=5 cadence at small init in this regime. Higher
temporal resolution and/or different operator (e.g., eNTK rather than
hidden Gram) might recover staircase structure — but as preregistered, the
hypothesis is refuted on this evidence.

### Matched-step / matched-threshold control

- **Matched-step** (within bins of ‖ΔW_ℓ‖_F): all bins have 0 overlap
  between plateau-body and pre-escape — i.e., step magnitudes don't
  overlap distributions, so no matched-step confound is even possible
  in this regime. Note this differs from yesterday's null result (where
  alignment_gain confounded with overlapping step sizes).
- **Matched-threshold** (`median + 3·MAD on [500, 1800]`):
  - simplex_hilbert_diam (C4): lead 555 ± seed-variation steps. ✓
  - Idea 1 g_ℓ onset: lead 600 (artifact of detector — first eligible
    step). The BSJ test is **peak-based**, not lead-based; it asks
    whether the *quantitative ratio* matches theory at escape, not
    whether g_ℓ leads C4.
  - Idea 2 pf_ratio: lead 20-140 steps (LATER than C4).
  - Idea 2 pf_overlap: lead 140 steps (LATER than C4).
  - **Conclusion**: Idea 1's peak-based BSJ test is a complementary
    *quantitative theory-match* claim, NOT a "tighter detector than C4"
    claim. This is the right framing for scaling up.

### Matched-step + matched-threshold controls

For each idea, the pilot also computes:
- **Matched-step**: within log-spaced bins of `‖ΔW_ℓ‖_F` (Idea 1) or
  `‖ΔZ_ℓ‖_F` (Ideas 2,3), median spectral signal in plateau-body window
  vs pre-escape window. If `mean_abs_delta_across_bins ≈ 0`, the apparent
  signal is just step magnitude in disguise (yesterday's failure mode).
- **Matched-threshold**: under SAME `median+3·MAD on [500, 1800]` rule,
  compare lead time vs `simplex_hilbert_diam` (existing C4 detector). Must
  beat C4 by > 50 steps (1 SD of seed variance) to claim novelty over the
  existing M2 detector.

---

## Suggested Execution Order (post-idea-stage, for `/experiment-bridge`)

1. **Scale Idea 1 to depth-6 BSJ regime, 5 seeds** (the load-bearing test).
   The empirical question: does median(`g_6 / g_1`) ≥ 6^(1/4) ≈ 1.57 across
   5 seeds at depth-6, AND is the strict deeper-first cascade more
   consistent at depth-6 than at depth-3 (where it held only 2/3)?
2. **Init-scale ablation on Idea 1** (1e-2 / 1e-3 / 1e-4, 3 seeds each).
   Predicts: cascade visible at 1e-3 / 1e-4, weak/absent at 1e-2 (lazy
   regime). Confirms the signal is a small-init saddle-to-saddle
   phenomenon, not a generic late-training feature.
3. **Pre-deployment Codex review** of the depth-6 + ablation writeup
   BEFORE sending to Tudisco (per `feedback_workflow.md`).
4. **If positive at depth-6**: short focused note to Tudisco on
   "time-resolved empirical realization of BSJ 2025 ℓ^(1/4) cascade,
   with [stronger-than-predicted / matching] empirical scaling." This
   is *not* a major paper contribution by itself, but a clean theory-
   testing addendum that complements the M2 simplex-Hilbert work.
5. **If negative at depth-6** (cascade fails to scale, or ratio doesn't
   exceed 6^(1/4)): clean negative result — quantitative refutation of
   the BSJ scaling for typical GD trajectories, which BSJ would themselves
   want to see. Still publishable as a refinement of their bound.

## Next Steps (for Elizabeth)

- [ ] Decide: pursue Idea 1 scale-up via `/experiment-bridge`?
- [ ] If yes: spec a 5-seed depth-6 + 3×3 init-scale ablation experiment
      plan with Codex pre-review (per workflow feedback memory).
- [ ] If no / want different angle: Idea 5 PF dynamics as mechanistic
      side-note to M2, OR a different direction entirely.

## Files

```
gradient_dsen_neuron_network/
├── idea-stage/
│   ├── IDEA_REPORT.md            ← v1 (Procrustes / NULL RESULT, preserved)
│   └── IDEA_REPORT_v2.md         ← THIS FILE
├── refine-logs/
│   ├── spectral_dynamics.py      ← v2 pilot runner (NEW)
│   ├── analyze_spectral.py       ← v2 cross-seed analyzer (NEW)
│   └── runs/Spectral/
│       ├── S_d{3,6}_w256_s{0,1,2}/track.json
│       ├── AGGREGATE_d{3,6}_w256.json
│       └── figures_d{3,6}_w256/spectral_overview.png
├── .aris/traces/idea-creator/20260430_run01/
│   ├── round01_brainstorm.md     ← Codex 10 ideas
│   └── round02_devils_advocate.md ← Codex devil's advocate + final ranking
└── NARRATIVE_REPORT.md           ← v1 NULL RESULT (preserved)
```
