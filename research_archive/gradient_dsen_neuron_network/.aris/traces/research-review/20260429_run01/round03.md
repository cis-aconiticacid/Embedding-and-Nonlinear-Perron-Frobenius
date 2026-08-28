# Round 3 — Final Verdict

**Reviewer**: Codex MCP gpt-5.x xhigh, threadId 019dd9e1-c17d-7b93-885f-ccec18b048dd.
**Date**: 2026-04-29.

---

## My round-3 input

After Round 2's "Procrustes branch is dead" verdict, I ran the generic-baseline
comparison Codex requested (`refine-logs/control_baselines.py`):

Under matched threshold rule (`median + 3·MAD` on baseline window
`[500, 1800]`):

w=256:
| metric | mean ± std | gaps |
|---|---|---|
| frob_change_Z | 527 ± 105 | [600, 665, 380, 555, 435] |
| frob_change_W | 526 ± 104 | [600, 660, 380, 555, 435] |
| proc_resid_scaled_Z | 527 ± 105 | (= frob_change_Z) |
| simplex_hilbert_diam | **499 ± 77** | [575, 555, 380, 550, 435] |
| dH_change (|Δ d_H|) | 352 ± 274 | [600, 665, 10, 50, 435] |

w=512:
| metric | mean ± std |
|---|---|
| frob_change_Z | 280 ± 88 |
| frob_change_W | 280 ± 88 |
| proc_resid_scaled_Z | 255 ± 124 |
| simplex_hilbert_diam | **280 ± 88** (IDENTICAL) |

The "10× tighter than C4" claim was an artifact of:
- C4 used hardcoded threshold "simplex_diam > 1e-3" → ~46 step lead
- New metrics used "median + 3·MAD on baseline" → ~500 step lead
- Apply the same rule to simplex_diam → ~500 step lead too

Once thresholds are matched, all four geometric metrics give essentially
the same lead time in this regime.

## Reviewer response (final)

> *"Yes. I agree with the final deflation. Under matched-step and
> matched-threshold controls, the overnight story collapses to: these
> metrics are all tracking the same change point in this regime. That is
> a useful internal sanity check, but not a contribution."*

**Reviewer's recommendations**:

1. **Treat as null result.** Do not put in abstract, intro, or claimed
   contributions of the M2 paper. At most an appendix footnote: "we tested
   representation-level and Procrustes-style metrics; after fair controls,
   they did not outperform the existing simplex-based statistic on lead time;
   therefore they do not change the main story."

2. **Worth-saving forward question**: "Is there any regime where
   representation-level metrics decouple from weight-level / simplex
   metrics?" If no, drop the line entirely. If yes, the representation
   level becomes a reason to care.

3. **Second-best forward question**: do gradient-norm / parameter-update-norm /
   logit-change baselines also coincide? If so, the common onset is a
   generic update-size phenomenon, not a geometric one. Requires a fresh
   run with these saved (not in current track.json).

4. **Reviewer's max-defensible takeaway in ONE sentence**:
   > *"Under matched step-size and matched thresholding, the proposed
   > representation-level and Procrustes-based metrics provide no
   > incremental mechanistic or early-warning value over the existing
   > simplex-based statistic in this training regime."*

---

## Final disposition of the overnight session

**Status**: ❌ **NULL RESULT.** The hypothesis (Procrustes residual /
alignment_gain as saddle-to-saddle eigenspace-transition diagnostic) is
empirically refuted by two controls:

1. **Matched-step control** (Round 2): alignment_gain ≈ 0 happens whenever
   `frob_change_Z` is large, not specifically at escape. The "collapse"
   pattern is just a re-encoding of step-magnitude.

2. **Matched-threshold control** (Round 3): under the same robust threshold
   rule, simplex Hilbert diameter (the existing C4 detector) gives the
   same lead time as the new representation-level metrics.

**What was useful**:
- Eliminated a direction Elizabeth might otherwise have spent significant
  time on. The empirical answer is now in the record.
- Built reusable infrastructure (`proc_dynamics.py`, `run_proc.py`,
  `analyze_proc.py`, `control_matched_step.py`, `control_baselines.py`)
  that is ready for the worth-saving forward question (does representation
  decouple in any regime?). Easy to re-deploy.
- Clean, pre-declared protocol with Codex review applied — methodology was
  tight, the hypothesis just didn't pan out.
- Codex review process worked: Round 1 flagged the right concerns; Round 2
  killed the Procrustes branch; Round 3 killed the bare lead-time claim.

**What NOT to do going forward**:
- Do not include the alignment_gain / Procrustes / eigenspace-transition
  story in any paper or note to Tudisco. It is empirically false.
- Do not claim "representation-level Frobenius change is a tighter detector
  than C4." It is not, under fair comparison.
- Do not invest more time trying to rescue this direction without a clean
  hypothesis about WHEN representation-level decouples from weight-level
  metrics.

**What MIGHT be worth doing**:
- A targeted experiment: pick one regime where representation evolves
  differently from weights (e.g., width regime that lives near the lazy /
  feature-learning boundary; or a different optimizer / init regime).
  Re-run with `--save_repr` so we save Z/W per snapshot. Test whether
  representation lead time differs from weight lead time. If yes, there
  is a story. If no, drop the direction.
- Compute parameter-update-norm and gradient-norm baselines on a fresh run.
  Until these are tested, even the bare "representation Frobenius change
  has a 500-step lead" claim is not validated against the simplest possible
  baselines.

---

## Closing note for Elizabeth's records

The overnight pipeline ran cleanly and produced a definitive empirical
answer: representation-level pair-metrics (Procrustes residual, CKA,
alignment gain, subspace angle, Frobenius change) do NOT add incremental
value beyond the existing C4 simplex Hilbert diameter detector under fair
controls in this training regime. The honest move is to treat this as a
null result, document the methodology and controls (which are clean and
reusable), and continue extending the M2 framework along the original
Tudisco / sub-homogeneity / saddle-to-saddle axis.
