# NARRATIVE REPORT — NULL RESULT (corrected after Codex review 2026-04-29)

> **Status**: This direction was tested overnight 2026-04-29 and FAILED two
> independent controls. The original positive findings reported here in
> earlier drafts were artifacts of (1) confounded step-magnitude
> interpretation and (2) mismatched threshold rules across metrics.
> Documented below as a null result to keep the record honest. **DO NOT
> include the rotation-quotient / eigenspace-transition story in the
> Tudisco-collaboration paper or any communication.** A previous version
> of this file (now archived in git history) overstated the findings; this
> version supersedes it.

---

## 早安 — 一句话总结

我用一晚上把 `embedding_compatibility_adapters_notes.md` 的 Procrustes 思路
搬到你 saddle-to-saddle MNIST 上,**发现没有 incremental value**。
Codex 三轮 review 把所有正面 claim 都 deflate 掉了。

可以走的诚实结论 (Codex 给的一句话):

> *"Under matched step-size and matched thresholding, the proposed
> representation-level and Procrustes-based metrics provide no incremental
> mechanistic or early-warning value over the existing simplex-based
> statistic in this training regime."*

**不要写进给 Tudisco 的 note 里**。最多在 paper appendix 里一行 "we tested
representation-level Procrustes metrics; they did not outperform simplex
diameter under fair controls; they are not load-bearing."

---

## What was tested

**Hypothesis** (pre-declared in `idea-stage/IDEA_REPORT.md`): within a
saddle-to-saddle training trajectory, between consecutive iterates, probe
representations evolve by orthogonal rotation during plateau and by
something more than rotation at escape (eigenspace transition). The
Procrustes residual and the derived `alignment_gain = 1 − proc/frob`
should therefore distinguish plateau from escape.

**Setup**:
- depth=3 FC-ReLU MNIST, init=1e-3, lr=1.0, full-batch CE.
- 5 seeds at width=256 + 3 seeds at width=512 = 8 seeds total.
- 5000 steps, constant Δ=5 cadence in [0, 3500].
- Pre-declared baseline window [500, 2200] + robust [500, 1800].
- Pre-declared primary endpoint: `proc_resid_scaled_Z` lead-gap.

**Code**: `refine-logs/proc_dynamics.py`, `refine-logs/run_proc.py`,
`refine-logs/analyze_proc.py`, `refine-logs/control_matched_step.py`,
`refine-logs/control_baselines.py`.

## Round 1 Codex review (gpt-5.x xhigh)

Score 2.5/10 (highlight) / 5.5/10 (subplot). **2 CRITICAL flagged**:
- Large-step confound: alignment_gain → 0 might just mean step is large.
- Eigenspace transition is overreach without measuring R_t directly.

Plus 6 MAJOR (subspace distance not measured, single regime, baseline
sensitivity, no held-out probe, etc.).

## Round 2 — matched-step control (Codex CRITICAL #1)

Bin all snapshots by `frob_change_Z` magnitude. Within each frob bin,
compare alignment_gain median for plateau-body snapshots vs 50-step
pre-escape snapshots.

w=256: across overlap bins, `|plateau_gain_median − escape_gain_median|`
≈ 0.001 (essentially same).

w=512: across overlap bins, `|Δ|` ≈ 0.003.

Per-seed Spearman correlation between `alignment_gain` and `frob_change_Z`
within plateau body: w=256 mean ρ = −0.12; w=512 mean ρ = −0.58.

**Conclusion**: alignment_gain ≈ 0 happens whenever `frob_change` is large —
NOT specifically at escape. The "collapse pattern" was a re-encoding of
step-magnitude. The eigenspace-transition framing is empirically refuted.

Reviewer round-2 verdict: *"The Procrustes branch is dead."* Score 3/10.

## Round 3 — matched-threshold control

The original "10× tighter than C4" claim used inconsistent threshold rules:
- C4: hardcoded "simplex_diam > 1e-3" → ~46 step lead.
- New metrics: `median + 3·MAD on baseline` → ~500 step lead.

Apply the SAME `median + 3·MAD` rule to both. Result:

w=256:
| metric | mean ± std lead-gap |
|---|---|
| frob_change_Z (probe rep) | 527 ± 105 |
| frob_change_W (last-layer wt) | 526 ± 104 |
| proc_resid_scaled_Z | 527 ± 105 |
| **simplex_hilbert_diam** | **499 ± 77** |

w=512:
| metric | mean ± std lead-gap |
|---|---|
| frob_change_Z | 280 ± 88 |
| frob_change_W | 280 ± 88 |
| simplex_hilbert_diam | **280 ± 88** (identical) |

Once threshold rules are matched, all four metrics are equivalent. The
"frob_change_Z is uniquely a strong leading indicator" framing is
unsupported.

Reviewer round-3 verdict: full agreement with the deflation. **Treat as
null result.**

## What was useful

1. **Definitively eliminated** the Procrustes / alignment_gain / eigenspace-
    transition direction. Future sessions don't need to revisit.
2. **Discovered that under matched threshold, all geometric "update-magnitude"
    metrics give the same lead time** (~500 steps in this regime). This is a
    useful internal sanity check on C4 (the previously claimed 46-step lead
    was a threshold-choice artifact).
3. **Reusable infrastructure**:
    - `proc_dynamics.py` — pair metrics module (Procrustes / CKA /
       subspace angle / Frobenius change / alignment gain). Tested
       synthetically (B = c·A·R gives proc_resid_scaled ≈ 0).
    - `run_proc.py` — multi-seed runner with snapshot-saving option.
    - `analyze_proc.py` — cross-seed analysis with both predeclared and
       robust baseline windows.
    - `control_matched_step.py` — matched-step confound check.
    - `control_baselines.py` — generic-baseline comparison.
4. **Methodological hygiene**: Codex review caught 2 CRITICAL + 6 MAJOR
    issues BEFORE deploying, and 2 more (matched-step, matched-threshold)
    AFTER initial results. This kept the empirical conclusions tight.

## What NOT to claim

- ❌ Procrustes orthogonal quotient adds diagnostic / detection value
   beyond raw Frobenius.
- ❌ alignment_gain collapse is a specifically-escape signature.
- ❌ Eigenspace transition / spectral-contrastive analog.
- ❌ "Probe-representation matrix beats scalar Hilbert diameter."
- ❌ "10× tighter lead than C4." (Was a threshold artifact.)

## What might still be worth pursuing

Per Codex round 3, one sharp forward question:

> *"Is there any regime where representation-level metrics decouple from
> weight-level / simplex metrics?"*

If yes, the representation level becomes worth caring about. If no, drop
the entire line. To test, would need:
- A regime where lazy / feature-learning training is closer to the
   boundary (e.g., width sweep around critical-init scale, or different
   activation).
- Save full Z and W per snapshot (`--save_repr`).
- Compare per-step `representation lead − weight lead` across regimes.
- Negative control: regime with no plateau / no clean escape.

Second-best forward question: do **gradient-norm** and **parameter-update-norm**
also coincide with the geometric metrics? Until tested, even the
"common-onset of geometric metrics" claim might just be a generic update-
size phenomenon, not a geometric one. This requires re-running with grad
norm + total param update norm logged (not in current track.json).

These are NOT done overnight; they need fresh runs and a tighter
experimental design. Would need ~1 day with focused planning, not an
overnight session.

## Files (status)

```
gradient_dsen_neuron_network/
├── idea-stage/IDEA_REPORT.md                  ← pre-declared protocol (kept as-is, not modified)
├── refine-logs/
│   ├── proc_dynamics.py                       ← reusable pair-metrics module
│   ├── run_proc.py                            ← multi-seed Procrustes runner
│   ├── analyze_proc.py                        ← cross-seed analysis
│   ├── control_matched_step.py                ← Round 2 matched-step control
│   ├── control_baselines.py                   ← Round 3 matched-threshold control
│   └── runs/Procrustes/
│       ├── P_d3_w256_s{0..4}/track.json       ← 5 seeds at w=256 raw data
│       ├── P_d3_w512_s{0..2}/track.json       ← 3 seeds at w=512 raw data
│       ├── figures_w256/                      ← per-width figures (DO NOT use
│       │     {alignment_gain,...}.png             figures from earlier draft —
│       │                                         labels reference refuted hyp.)
│       ├── figures_w512/                      ← same, w=512
│       ├── AGGREGATE_w{256,512}.json
│       ├── MATCHED_STEP_w{256,512}.json       ← Round 2 control
│       └── BASELINES_w{256,512}.json          ← Round 3 control
├── .aris/traces/research-review/20260429_run01/
│   ├── round01_round02.md                     ← Codex rounds 1-2
│   └── round03.md                             ← Codex round 3 + null-result disposition
├── NARRATIVE_REPORT.md                        ← THIS FILE (corrected)
├── RESEARCH_PIPELINE_REPORT.md                ← pipeline summary (corrected)
└── README_FIRST.md (at workspace root)
```

## Recommended action for Elizabeth

- Read `.aris/traces/research-review/20260429_run01/round03.md` for the
   verdict in Codex's words.
- Look at `runs/Procrustes/figures_w256/matched_step_control.png` (the
   Round 2 control plot) — visual confirmation that plateau and pre-escape
   points lie on the same gain-vs-frob curve.
- Look at `runs/Procrustes/figures_w256/baselines_comparison.png` (the
   Round 3 control plot) — visual confirmation that all four metrics give
   the same lead time under fair thresholding.
- Don't put this in the next note to Tudisco. Continue extending M2 along
   sub-homogeneity / saddle-to-saddle axis as planned.
- The Procrustes infrastructure is reusable if you ever want to pursue
   the "do representation metrics decouple from weight metrics in some
   regime?" question — but only with a clean a-priori hypothesis about
   what regime would show decoupling.
