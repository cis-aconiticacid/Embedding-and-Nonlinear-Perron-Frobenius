# Research Pipeline Report — overnight session 2026-04-29

> **Final disposition (after 3-round Codex review on 2026-04-29 morning)**:
> ❌ **NULL RESULT.** Initial overnight findings were deflated by two
> independent controls. Documented as a null result for the project record.
> See `NARRATIVE_REPORT.md` and `.aris/traces/research-review/20260429_run01/`
> for full details.

**Direction**: combine `gradient_dsen_neuron_network/` (Hilbert/PF gradient-dynamics)
with reading notes `embedding_compatibility_adapters_notes.md` (Han Xiao
Procrustes alignment + spectral-contrastive picture).

**Hypothesis tested**: probe-representation Procrustes residual / alignment
gain as a saddle-to-saddle eigenspace-transition diagnostic.

**Status**: empirically refuted. Continue M2 along original sub-homogeneity /
saddle-to-saddle axis.

---

## Journey summary

| Stage | What happened |
|---|---|
| Survey | M2 prior work + Han Xiao notes; identified spectral-contrastive ⇄ saddle-to-saddle bridge |
| Idea discovery | Pre-declared primary endpoint (`proc_resid_scaled_Z` lead-gap), 6 hypotheses, 2 anti-claims, decision rules |
| Implementation | `proc_dynamics.py`, `run_proc.py`, `analyze_proc.py` (extends `run_b7`) |
| Codex pre-review | gpt-5.x xhigh: 2 CRITICAL + 6 MAJOR; fixed all CRITICAL + 5/6 MAJOR before deploying |
| Synthetic sanity | Verified scaled Procrustes ≈ 0 for B = c·A·R; rank-tolerance for low-rank inputs |
| Pilot (1 seed) | Confirmed primary endpoint fires; 200-step lead vs C4 = 50 |
| 5-seed sweep w=256 | All 5/5 showed alignment_gain collapse pattern; mean Δ +0.504 ± 0.04 |
| 3-seed sweep w=512 | 3/3 replicated; mean Δ +0.575 ± 0.027 |
| Initial writeup | Drafted positive finding |
| Codex review Round 1 | 2.5/10 (highlight) / 5.5/10 (subplot); flagged large-step confound + eigenspace overreach |
| **Round 2 — matched-step control** | **Plateau and pre-escape gain medians match within Δ ≈ 0.001 at matched frob magnitude. The "collapse" was a re-encoding of step-size.** |
| Codex review Round 2 | *"The Procrustes branch is dead."* Score 3/10. |
| **Round 3 — matched-threshold control** | **Under same `median + 3·MAD` rule, simplex Hilbert diameter (existing C4) gives ~500 step lead — same as frob_change_Z. The "10× tighter than C4" was a threshold artifact.** |
| Codex review Round 3 | *Full agreement with deflation. Treat as null result.* |
| Honest rewriting | NARRATIVE_REPORT, RESEARCH_PIPELINE_REPORT, READ_ME_FIRST, memory entry all updated to null-result framing |

---

## What survived (= nothing for the paper)

- **One useful sanity check**: under matched threshold rules, multiple
   geometric "update-magnitude" metrics give the same lead time (~500 steps
   in this regime). Useful internal record but NOT a contribution.
- **Reusable infrastructure** (`proc_dynamics.py` etc.) ready if a
   forward question with clean a-priori hypothesis emerges.
- **Methodology validation**: pre-declared protocol + Codex review +
   matched controls executed cleanly. The negative answer is empirically
   solid.

## What was REFUTED

| Claim | Why refuted |
|---|---|
| Procrustes orthogonal quotient adds detection power | Same first-crossing as raw Frobenius (5/5 seeds) |
| Procrustes orthogonal quotient adds diagnostic power (alignment_gain) | Matched-step control: gain ≈ 0 whenever frob is large, not specifically at escape |
| Eigenspace transition signature | No direct R_t measurement; alignment_gain pattern explainable by step-magnitude |
| 10× tighter lead than C4 | Threshold-rule artifact; under matched threshold, simplex_diam matches frob_change_Z lead |
| "Probe-representation richness beats scalar Hilbert" | All four metrics give same lead under fair threshold |
| Spectral-contrastive analog within saddle-to-saddle | Empirical premise unsupported |

---

## Codex's max-defensible takeaway (one sentence)

> *"Under matched step-size and matched thresholding, the proposed
> representation-level and Procrustes-based metrics provide no incremental
> mechanistic or early-warning value over the existing simplex-based
> statistic in this training regime."*

---

## Worth-saving forward direction (per Codex round 3)

The ONE worth-saving question:

> **"Is there any regime where representation-level metrics decouple from
> weight-level / simplex metrics?"**

If yes: representation-level analysis is justified, and there is a real
story. If no: drop the line entirely.

To test, would need (none of which are overnight):
- Save full Z, W per snapshot (`run_proc.py --save_repr` already supports).
- Pick a regime where lazy/feature-learning training is on the boundary
   (width sweep around critical-init scale, or different optimizer / init).
- Negative control: regime with no clean saddle escape (e.g., d=2 escapes
   immediately).
- Generic baselines: gradient norm and total parameter update norm
   (NOT in current track.json — needs fresh runs).
- Day-scale planning, not overnight.

---

## What NOT to do

- ❌ Do not include this in any note to Tudisco. The Procrustes /
   alignment_gain / eigenspace-transition framing is empirically false.
- ❌ Do not claim 10× lead over C4. That was a threshold artifact.
- ❌ Do not pursue more of this direction without a sharp a-priori
   hypothesis about WHEN representation metrics decouple from weight
   metrics.
- ❌ Do not skip Codex review before deployment for this user. The
   pre-deployment review caught 2 CRITICAL + 6 MAJOR; the post-deployment
   reviews killed the positive interpretations. Without them, this would
   have been miscommunicated.

---

## Files

```
/workspace/gradient_dsen_neuron_network/
├── idea-stage/IDEA_REPORT.md                       ← pre-declared protocol (preserved)
├── refine-logs/
│   ├── proc_dynamics.py                            ← reusable pair-metrics
│   ├── run_proc.py                                 ← multi-seed runner
│   ├── analyze_proc.py                             ← cross-seed analysis
│   ├── control_matched_step.py                     ← Round 2 control (CRITICAL #1)
│   ├── control_baselines.py                        ← Round 3 control
│   └── runs/Procrustes/
│       ├── P_d3_w256_s{0..4}/track.json
│       ├── P_d3_w512_s{0..2}/track.json
│       ├── figures_w{256,512}/                     ← per-seed + cross-seed plots
│       │   {…}, matched_step_control.png,
│       │   baselines_comparison.png
│       ├── AGGREGATE_w{256,512}.json
│       ├── MATCHED_STEP_w{256,512}.json
│       └── BASELINES_w{256,512}.json
├── .aris/traces/research-review/20260429_run01/
│   ├── round01_round02.md
│   └── round03.md
├── NARRATIVE_REPORT.md                             ← null-result narrative
└── RESEARCH_PIPELINE_REPORT.md                     ← THIS FILE
```

Plus `/workspace/READ_ME_FIRST.md` (entry-point) and memory update.

Total time: ~50 min overnight + ~30 min review-and-deflation = 1.5 hr wall;
~50 min GPU. M2 results untouched.
