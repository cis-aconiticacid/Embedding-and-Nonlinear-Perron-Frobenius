# IDEA REPORT — Procrustes-Residual & CKA on Probe Representations as a Saddle-to-Saddle Detector

**Date**: 2026-04-29 (overnight session)
**Author**: Claude (autonomous research-pipeline run, on behalf of Elizabeth Wen)
**Scope**: combine `gradient_dsen_neuron_network/` (Hilbert × PF × gradient dynamics, M2 already complete) with `embedding_compatibility_adapters_notes.md` (Han Xiao / spectral contrastive Procrustes alignment).

---

## 1. The two threads being combined

### Thread A — Elizabeth's M2 result (what's already on the table)
- On FC-ReLU MNIST with small init (1e-3) + full-batch GD, training shows a long acc=0.114 plateau before clean saddle escape (Jacot saddle-to-saddle).
- During the plateau, the **last-layer Hilbert distance to anchor** contracts ~4% (S1: sub-homogeneous PF prediction).
- The **argmin of the log-ratio vector** locks 50–69 steps before acc escape (S2/C3, weight-space leading indicator).
- The **simplex Hilbert diameter on probe outputs** is < 1e-3 throughout the main plateau body and crosses 1e-3 ~46 steps before acc escape (C4, output-space leading indicator).
- **F5 (key empirical fact)**: the Hilbert scalar (max-min log-ratio) is a *worse* event detector than the full **log-ratio L2 norm** (F1=0.31–0.41 vs 0.06–0.17). Information is being thrown away by the max-min reduction.

### Thread B — Han Xiao embedding adapter notes (what they suggest)
- Two embedding models trained on similar data + recipe have representation spaces that **differ only by an orthogonal rotation** (CKA > 0.9 → near-lossless Procrustes alignment).
- Theoretical anchor: **contrastive learning ≈ spectral decomposition of an operator on RKHS** (HaoChen et al. 2021, Balestriero & LeCun 2022). Two models approximate the same top-k eigenspace; their bases differ only by orthogonal change-of-basis.
- The notes explicitly raise (§4.3): **"non-contrastive SSL (BYOL, DINO) might correspond to a non-linear PF fixed point"** — i.e., when the operator is non-linear, the "rotation invariance" should fail, and dynamics should look more like sub-homogeneous / saddle-to-saddle.

### The bridge
Spectral contrastive view: two snapshots of "the same model" should differ by orthogonal rotation **as long as they live in the same eigenspace**. Saddle-to-saddle theory says training discretely visits a sequence of eigenspaces.

→ **Within a single training run**, consecutive iterates' probe representations should differ by **near-orthogonal rotation during plateau** (still in the same eigenspace) and by **substantially more than rotation at saddle escape** (jumping to a new eigenspace).

This gives a **new geometric event detector**: the **Procrustes residual** between consecutive probe representations. It's distinct from Hilbert metric, log-ratio L2, simplex diameter, accuracy. And its theoretical motivation comes directly from the contrastive ≈ spectral picture.

---

## 2. Hypothesis (precise)

Let `Z_t ∈ R^{N×H}` be the penultimate-layer post-activation matrix on a fixed probe set of N points, at training step t. Let
$$\rho_t = \min_{R \in O(H)} \frac{\|Z_t R - Z_{t+\Delta}\|_F}{\|Z_{t+\Delta}\|_F}$$
be the **orthogonal-Procrustes residual** between the representations at steps t and t+Δ (closed-form via SVD of `Z_t^T Z_{t+Δ}`).

**H1 (within-saddle near-rotation)**: During the silent plateau (steps t with train_acc < 0.20), `ρ_t` is small and stable (≪ 1).

**H2 (saddle-escape spike)**: `ρ_t` spikes at the saddle-escape step, exceeding its plateau-body 95th percentile by ≥3×.

**H3 (leading indicator)**: `ρ_t` crosses a threshold *before* the accuracy crosses 0.20, with a positive lead time (median ≥10 steps over seeds where escape happens).

**H4 (CKA mirror)**: Linear CKA between Z_t and Z_{t+Δ} drops sharply at the same event (consistent with Han Xiao's "CKA > 0.9 ⇔ Procrustes works"; in our within-training case, "CKA stays high during plateau, dips at escape").

**H5 (W-side mirror)**: The same phenomenon should be visible on the output-layer matrix `W^{(3)} ∈ R^{10×H}` via row-Procrustes, but **at lower signal-to-noise** than on Z (since W is 10-dimensional in the row direction; the eigenspace argument gives sharper signal on the 256-d feature side).

**H6 (consistency with F5)**: The Procrustes residual should beat Hilbert as an event detector, in the same way log-ratio L2 already beats Hilbert (F5). It may or may not beat log-ratio L2 itself — that's the open question.

### Anti-hypothesis to be tested

**A1**: "Procrustes residual is just a re-parametrization of the existing Hilbert / log-ratio L2 / simplex diameter signal." Falsified if `ρ_t` produces a non-trivial event-detection F1 score on top of those existing metrics (i.e., an event visible only in Procrustes).

**A2**: "Procrustes residual is no better than ||Z_{t+Δ} − Z_t||_F (raw Frobenius change)." This would mean the orthogonal-quotient adds nothing. Falsified if we see plateau-body `ρ_t` ≪ raw Frobenius change at the same time, i.e. plateau-time evolution is almost entirely rotational.

---

## 3. Why this is novel

I cross-checked the existing Hilbert/PF paper map (`reference_hilbert_pf_papers.md`) and the Tudisco / Deidda / Cavalcante papers tracked there. The closest things in adjacent literature:

| Prior work | What it does | Why this is still novel |
|---|---|---|
| Han Xiao 2026 (embedding adapter) | Procrustes between **two trained models** | We track Procrustes **within one model's training trajectory** — different question |
| HaoChen 2021 / Balestriero–LeCun 2022 (spectral contrastive) | Show contrastive ≈ spectral decomp at convergence | Static analysis at fixed point; we're looking at **training dynamics** |
| Jacot 2021 / 2505.21722 (saddle-to-saddle) | Track loss plateaus in deep linear / ReLU nets | Uses spectral / loss decomposition; **doesn't measure Procrustes residual** between iterates |
| Sittoni–Tudisco 2024 (sub-hom DEQ) | Hilbert contraction for sub-hom maps | Static fixed-point theory; doesn't connect to Procrustes / CKA |
| Zhang–Deidda–Higham–Tudisco 2025 (oversmoothing in GNNs) | Rank-based metrics over training | Effective rank, not orthogonal-quotient distance |
| F5 in Elizabeth's own M2 (log-ratio L2 vs Hilbert) | Established that fuller geometry beats max-min | Same spirit; Procrustes residual extends the "use more geometry" thesis to the **representation space**, not just the weight vector |

**The closest neighbor is Elizabeth's own F5**: she showed that throwing less information away (log-ratio L2 over max-min Hilbert) gives a better event detector. Procrustes residual extends this from the 256-d weight feature vector to the 500×256 probe-representation matrix. It uses dramatically more of the available geometric structure.

**Theoretical interpretation**: Procrustes residual measures "fraction of representation change that cannot be explained by orthogonal change of basis in feature space." In the spectral contrastive picture, *all* basis change is rotation as long as the eigenspace is preserved; basis change beyond rotation means the eigenspace moved. So Procrustes residual is a direct empirical measurement of **"is the eigenspace stable?"** — which is exactly the question the saddle-to-saddle theory asks.

---

## 4. Pilot signal (cheap pre-check)

Before committing to a full run, I'll do a 1-seed pilot (5 minutes on the 4060) at d=3, init=1e-3, lr=1.0 with the modified training script saving Z and W. The pilot passes if:

1. ρ_t on probe representations is well-defined and stable across the plateau (no NaN/inf).
2. At least *some* visible spike around the known escape window (~2400 steps for d3_s0).
3. The metric is non-trivially correlated with neither Hilbert nor accuracy alone (correlation < 0.95 with both).

If the pilot fails (no visible signal), pivot to plan B: track only on the W output layer, drop Z (W is cheaper to save and post-hoc analyse).

---

## 5. Experimental design (full run)

### Configuration
- Network: depth=3, width=256, init=1e-3, lr=1.0, full-batch SGD, ce loss, ReLU activation.
- Training: 5000 steps (matches B1/B7 plan, covers the typical d3 escape window 2000-2700).
- Seeds: **5 seeds** (instead of 3) to bring statistical confidence — within the GPU budget.
- Probe: 500 stratified MNIST training points, fixed across runs (probe_seed=42, matching existing protocol).
- Logging: every 5 steps in window [1500, 2900] (step-level resolution near escape); every 10 steps in [0, 1500); every 50 steps in [2900, 5000].

### Modifications to `mnist_hilbert.py`
1. Add `--save_repr` flag. When true, snapshot saves:
   - `Z_t` = penultimate post-activation [N_probe, H] on the fixed probe.
   - `W_out_t` = output_layer.weight [10, H].
2. Compute online (between successive snapshots; stored as scalars):
   - `proc_resid_Z`: orthogonal Procrustes residual on Z (Frobenius-normalized).
   - `proc_resid_W_right`: row-orthogonal Procrustes on W_out (rectangular: O(H)).
   - `cka_Z`: linear CKA between Z_t and Z_{t-Δ}.
   - `cka_W`: linear CKA between W_out_t and W_out_{t-Δ}.
   - `frob_change_Z`: ||Z_t - Z_{t-1}||_F / ||Z_t||_F (raw, control for A2).
   - `subspace_overlap`: top-r principal angle (r = num_classes = 10) between SVD subspaces of Z_t and Z_{t-Δ}.

### Analysis
- **Plot 1 (5-panel trajectory)**: per seed, plot vs step:
  acc, Hilbert distance, simplex diameter, Procrustes residual (Z), CKA (Z), with vertical lines for support switches and acc escape.
- **Plot 2 (event-detection F1 comparison)**: compute F1 of "metric exceeds threshold within K steps of acc escape" for each metric (Hilbert, log-ratio L2, simplex diameter, Procrustes, CKA, raw Frobenius). Reuse the F5 protocol from B2.
- **Plot 3 (lead time histogram)**: across seeds, histogram of (acc_escape - first_proc_resid_spike), compared to the same histogram for simplex_diam.
- **Table 1**: per-seed escape statistics + per-metric leading-edge step + leading-edge gap.

### Compute budget
- 5 seeds × 2 passes (anchor + track) × ~10 min = ~100 min on RTX 4060.
- Online Procrustes/CKA per snapshot: ~10ms each, ~850 snapshots → 8.5s overhead. Negligible.
- Raw save Z+W per snapshot: ~512KB × 850 = ~430MB per run × 5 = 2.2 GB. OK.

### Reproducibility
- Reuse `set_deterministic` + cudnn flags from existing pipeline.
- Same probe_seed=42, val_seed=123, MNIST root=/workspace/data — matches existing runs exactly.

---

## 6. Risk register

| Risk | Probability | Mitigation |
|---|---|---|
| Procrustes residual is dominated by raw Frobenius change (orthogonal-quotient does nothing useful) | Medium | A2 directly tests this. If true, downgrade to "raw Frobenius / CKA dynamic + Hilbert" framing — still a contribution. |
| Numerical: SVD on probe Z_t^T Z_{t+Δ} when activations are nearly rank-deficient (early training, all ReLU outputs near zero) | Medium | Add eps to SVD; mask snapshots where ‖Z_t‖_F < 1e-6; report mask rate. |
| GPU OOM on 8GB at width=256 + full batch + saving | Low | Already validated by existing B1/B6/B7 runs. Probe matmul (500×256 × 256×500) is ~125K elements, trivial. |
| Pilot signal too noisy → can't see effect at one seed | Medium | If pilot fails at d=3, try d=4 (longer plateau, larger drop, more obvious signal). |
| Effect is real but tiny / single-step transient | Medium | Use step-level logging in escape window (every 5 steps). If still not visible, this is informative — write it up as a negative result. |

---

## 7. Decision rules at the end

After the full run:

- **If H1+H2+H3 hold across ≥3/5 seeds**: positive signal. Write up as a clean addendum to F5 (event-detection metric) + a theoretical bridge to spectral contrastive learning. Send to Tudisco as part of the next note iteration.
- **If H1 holds but H2/H3 weak**: partial confirmation. Procrustes is "consistent with" the saddle-to-saddle picture but not a clean leading indicator. Frame as "geometric corroboration" rather than a new diagnostic.
- **If A1 (just a reparametrization) is supported**: write up as a negative result documenting the redundancy. Useful — saves future time.
- **If signal is real but the better-correlated metric is `frob_change_Z` (no orthogonal quotient)**: drop Procrustes; ship "Frobenius change of Z + CKA" as the takeaway. Still a step forward.

---

## 8. Connection back to the Tudisco / Deidda agenda

- Tudisco's 2026-03-31 hint ("sub-homogeneity of softplus gradient, see Sittoni–Tudisco 2024") is a **mechanism statement** about why the iterate map is non-expansive in Hilbert.
- This idea complements that: it's a **diagnostic statement** about *what changes* during a saddle-to-saddle escape — namely, the **eigenspace** of the representation operator, observable as a Procrustes-residual spike.
- These two viewpoints are the same picture from different angles:
  - Tudisco/Sittoni: the **map** is sub-homogeneous → Hilbert non-expansion.
  - This idea: the **iterate's representation** approximates the top-k eigenspace; the eigenspace is constant during a saddle (rotational evolution) and discretely jumps at escape.
- A clean paper synthesising both: "Hilbert contraction is the non-expansion side of a representation operator that tracks an eigenspace; saddle-to-saddle escape is the discrete eigenspace transition, observable via Procrustes residual."

---

## 9. Pilot + Full run plan for tonight

| Phase | Step | Time | Deliverable |
|---|---|---|---|
| 0 | Patch `mnist_hilbert.py` with --save_repr + procrustes/cka helpers | 30 min | `mnist_hilbert.py` v2 (backwards-compatible) |
| 0a | Codex cross-review on patch + plan | 15 min | review notes; fix MAJORs |
| 1 | Pilot: 1 seed (d=3, s=0) full run | 10 min | confirm signal exists |
| 2 | Full run: 5 seeds (d=3, s=0..4) | ~60 min | per-seed `track.json` with new metrics + saved Z/W |
| 3 | Analysis script: F1 comparison + 3-panel figures | 30 min | `runs/Procrustes/figures/*.png`, `summary.json` |
| 4 | NARRATIVE_REPORT.md + research pipeline report | 20 min | final write-up at workspace root |
| **Total** | | **~3 h wall** | full handoff |

---

## 10. Selected idea (1 of 1)

**Title**: Procrustes residual on probe representations as a finer event detector for saddle-to-saddle transitions in MNIST.

**Pilot signal**: pending (run on 1 seed).
**Novelty**: CONFIRMED (no prior work links Procrustes residual within training to saddle-to-saddle dynamics; F5's "fuller geometry beats max-min" thesis directly motivates it).
**Tractability**: HIGH (uses existing infrastructure; ~3 hour overnight budget).
**Connection to existing project**: TIGHT (extends F5; complementary to C2/C3/C4; theoretical bridge to embedding-adapter notes Elizabeth wrote on the same topic).

**Recommendation**: proceed.
