# 早安 Elizabeth — 重要更新

## ⚠️ 昨晚我跑的实验 + 今早的 Codex review = NULL RESULT

我用一晚上把 `embedding_compatibility_adapters_notes.md` 的 Procrustes 思路
搬到你 saddle-to-saddle 实验上,初看 5/5 + 3/3 seed 都有 alignment_gain
collapse,以为是个干净的 finding。

但今早跑了 `/research-review` (Codex MCP, gpt-5.x xhigh, 三轮),把所有 claim
都 deflate 掉了:

1. **Round 1**: 标记 2 CRITICAL — large-step confound + 没直接测 R_t 不能
   声称 "rotation collapses to identity"。Score 2.5/10 (highlight) /
   5.5/10 (subplot).

2. **Round 2 — matched-step control**: 我跑了控制,把 plateau body 和
   pre-escape window 按 `frob_change_Z` magnitude 配对比较。结果:**配对
   bin 内 alignment_gain median 几乎相同 (Δ ≤ 0.004)**。说明 alignment_gain
   ≈ 0 是 "step magnitude 大" 的一般 effect,不是 "saddle escape" 的特定
   effect。eigenspace transition 故事被实证否定。Codex round 2: *"The
   Procrustes branch is dead."* Score 3/10.

3. **Round 3 — matched-threshold control**: "比 C4 提前 10 倍" 是用了
   不同 threshold rule 的 artifact (C4 用硬编码 1e-3, 新指标用
   `median + 3·MAD`)。**用同一 rule, simplex_diam 也给 ~500 步 lead**:
   - frob_change_Z: 527 ± 105
   - frob_change_W: 526 ± 104
   - simplex_hilbert_diam: **499 ± 77**
   - 所有 metric 等价。

**Codex 给的 max-defensible takeaway (一句话)**:
> *"Under matched step-size and matched thresholding, the proposed
> representation-level and Procrustes-based metrics provide no incremental
> mechanistic or early-warning value over the existing simplex-based
> statistic in this training regime."*

## 不要做什么

- ❌ 不要把这个写进给 Tudisco 的 note 里
- ❌ 不要 claim "Procrustes 加什么 detection / diagnostic value"
- ❌ 不要 claim "eigenspace transition signature"
- ❌ 不要 claim "比 C4 早 10 倍" (这是 threshold rule mismatch 的 artifact)
- ❌ 不要 claim "probe representation 比 simplex scalar 强"

## 可以做什么

- ✅ 这个 null result 节省你后续的探索时间 — Procrustes 这条线不用再走
- ✅ 全套 infrastructure 是 reusable 的 (proc_dynamics.py, run_proc.py,
   analyze_proc.py, control_matched_step.py, control_baselines.py),
   如果将来要测 "在什么 regime 下 representation metric 和 weight metric
   decouple", 已经准备好
- ✅ Codex 给了一个值得追的 forward question: "Is there any regime where
   representation-level metrics decouple from weight-level/simplex metrics?"
   如果有, representation 才值得 care; 如果没有, 这条线就可以 drop
- ✅ 继续走原来 M2 的 C1-C4 + sub-homogeneity 主线

## 入口文件

| 文件 | 作用 |
|---|---|
| `gradient_dsen_neuron_network/NARRATIVE_REPORT.md` | 详细 null-result 报告 |
| `.aris/traces/research-review/20260429_run01/round03.md` | Codex 三轮 review 完整记录 |
| `.aris/traces/research-review/20260429_run01/round01_round02.md` | round 1+2 详细 |
| `runs/Procrustes/figures_w256/matched_step_control.png` | Round 2 control 图 (plateau 和 escape 点重叠) |
| `runs/Procrustes/figures_w256/baselines_comparison.png` | Round 3 control 图 (所有 metric 等价) |
| `runs/Procrustes/MATCHED_STEP_w*.json` | 数值结果 |
| `runs/Procrustes/BASELINES_w*.json` | 数值结果 |

## 工作流复盘 (你 feedback 里说的 Codex review 流程)

按你 `feedback_workflow.md` 的偏好,我**先**让 Codex review code+plan
(deploy 前抓了 2 CRITICAL + 6 MAJOR,全部修了),然后**才** deploy。
deploy 后又跑了两轮 review (matched-step + matched-threshold)。Codex
review 工作流这次发挥了核心作用 — 没有它,我可能会把这个 null result
当成 positive finding 写进 note 里。

## Memory 我已经更新

`/root/.claude/projects/-workspace/memory/project_hilbert_pf_procrustes_addendum.md`
已经写为 null-result 的版本,后续 session 不会再误以为这是 positive
finding。

**没动的**:M2 老代码 (B1-B6) 完好;给 Tudisco 的 .eml/.pdf 没碰;
原 IDEA_REPORT (pre-declared protocol) 保留作为 record 不修改。
