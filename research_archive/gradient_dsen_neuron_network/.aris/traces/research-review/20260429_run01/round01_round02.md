# Research Review Trace — 2026-04-29 run01
**Reviewer**: Codex MCP (gpt-5.x), `model_reasoning_effort=xhigh`, sandbox=read-only.
**Thread ID**: `019dd9e1-c17d-7b93-885f-ccec18b048dd`
**Subject**: Procrustes-residual / alignment_gain / probe-representation Frobenius
detector for saddle-to-saddle escape, Elizabeth Wen's Hilbert/PF project.

---

## Round 1 — initial review

**My prompt summary**: full context (M2 prior work + the new finding) + 8/8
seed alignment_gain collapse + acknowledged weaknesses + 5 explicit questions.

**Reviewer verdict (round 1)**:
- *"This is a real observation, but not yet a publishable claim."*
- Strongest fact: orthogonal-alignment quotient collapses near escape.
- Weakest part: "eigenspace transition" is overreach.
- Score as paper highlight: **2.5/10**. As subplot: **5.5/10**.
- **2 CRITICAL flagged**:
  - **Large-step confound**: alignment_gain → 0 might just mean "step is large".
    Match raw step magnitude in plateau vs pre-escape, see if gain still
    differs.
  - **No direct R_t measurement**: I claimed R → I without computing it.
- **MAJOR list**: held-out probe; subspace/projector distance; W_out
  control; one additional regime; negative control; baseline-window
  sensitivity is a red flag.
- **Closest literature**: Kornblith CKA 2019, Williams shape metrics 2021,
  Harvey 2024, Lange 2023, Pashakhanloo–Koulakov 2023, Altintas 2025.

---

## Round 2 — matched-step control + reply

**What I did between rounds**: ran the matched-step control on existing
data (`refine-logs/control_matched_step.py`):

w=256 (5 seeds): in frob-overlap bins, plateau and pre-escape gain medians
  match within Δ ≈ 0.001. Within-plateau Spearman(gain, frob) per seed:
  {-0.034, +0.257, -0.320, -0.134, -0.368}, mean -0.12.

w=512 (3 seeds): in frob-overlap bins, plateau gain medians match pre-escape
  within Δ ≈ 0.003. Spearman: {-0.540, -0.511, -0.686}, mean -0.58.

**alignment_gain ≈ 0 happens whenever frob_change is large** — not
specifically at escape. The "collapse" I claimed = the "frob spike" Codex
already had. Spectral-contrastive eigenspace-transition story REFUTED.

**Reviewer verdict (round 2)**:
- *"The Procrustes branch is dead."*
- Surviving claim: `frob_change_Z` is an earlier-warning statistic than C4
  simplex. Plausibly novel in this exact form, but close to generic
  function/representation update monitoring.
- This is a **minor empirical subplot**, not a pillar. One figure +
  paragraph, not a section with theoretical ambitions.
- Mock NeurIPS review:
  - Score: **3/10 reject**, confidence 4/5.
  - "Useful empirical diagnostic, but does not yet support a top-conference
    paper as the main contribution."
  - "Does not establish that `frob_change_Z` is better than simpler
    generic alternatives such as parameter-update norm, gradient norm,
    or probe logit change."
- **Best single experiment to make it interesting**:
  - Prospective online evaluation with fixed threshold.
  - One additional escape regime + one no-escape negative control.
  - Compare against generic baselines: parameter update norm, gradient norm,
    probe logit change.
  - "If `frob_change_Z` does NOT beat these generic baselines, the claim
    is empty. If it DOES, there's something specific to representation
    geometry."
- **Recommended framing**: "Probe-representation motion anticipates escape
  earlier than simplex Hilbert diameter." Avoid: "saddle detector", "phase
  transition", "10× tighter".

---

## Decision-record

**Status of each pre-declared hypothesis**:
- H1 (within-saddle near-rotation): partially supported as plateau-body
  alignment_gain ≈ 0.5, BUT this turned out to be a function of step
  magnitude — refuted as a *specific* claim about rotational dynamics.
- H2 (saddle-escape spike): confirmed for `frob_change_Z`. Not specific to
  Procrustes — equivalent magnitude-spike on raw Frobenius.
- H3 (positive lead time): confirmed — but unclear whether against
  generic baselines.
- H4 (CKA mirror): partial; high variance.
- H5 (W-side mirror): confirmed — `frob_change_W` ≈ `frob_change_Z` in
  lead time. This is a *deflation* — weight change tracks representation
  change.
- H6 (beats Hilbert): confirmed vs C4 simplex — but requires baseline
  against gradient norm / parameter norm.
- A1 (Procrustes is reparametrization): confirmed — for spike detection.
- A2 (orthogonal quotient adds nothing): also confirmed — matched-step
  control killed alignment_gain as a separate diagnostic.

**What I am willing to write up as a result**:
- One figure, one paragraph: "Frobenius change of the penultimate-layer
  probe representation crosses a robust threshold ~500 steps before
  acc-escape (5/5 seeds at w=256), generalizing F5's "fuller geometry"
  thesis from a 256-d L1-norm scalar feature vector to the 500×256
  probe representation matrix."

**What I am NOT willing to claim** (per round 2):
- Procrustes orthogonal quotient adds anything.
- Eigenspace transition / spectral contrastive analog.
- Rotation framing breaks at escape.
- That `frob_change_Z` is a domain-specific saddle detector (could be
  generic "any update-magnitude metric works").

**Outstanding gaps before this is publishable as a sub-plot**:
1. Compare to generic baselines: gradient norm, parameter update norm,
   probe logit change. Without this, "10× tighter than C4" is meaningless.
2. Test on a no-escape regime as negative control.
3. Test on at least one additional escape regime (depth=4 init=0.05;
   or different lr).
4. Held-out test-set probe.
5. Rewrite to drop all mechanistic claims.

---

## Round 3 (planned)

After computing parameter-update-norm and feat_vec change baselines on
existing data: ask reviewer for the exact 3-sentence defensible version
of the claim, and whether a no-escape negative control on existing
M2 depth=2 runs would suffice.
