# TRACE — Experiment Specifications

**System:** TRACE (Trajectory-based Runtime Agent Compromise Examiner)
**Paper:** Watch What It Does, Not What It Says — IEEE S&P 2027 submission

This document is the authoritative protocol for all experiments.
Run experiments in order A → B → C → D → E → Overhead.
Experiments B through C reuse corpora and scores from A; D and E reuse the trained classifier.

---

## Shared Setup (All Experiments)

### Corpus Construction

Build **two corpora** before running any experiment. All experiments draw from these.

#### Attack Corpus

| Cell | N instances | Source | Evasion |
|---|---|---|---|
| injection-overt | 30 | AgentDojo | None — standard payload |
| injection-evasive | 30 | AgentDojo | Position-aware restructuring |
| poisoning-overt | 30 | Skill-poisoning benchmark | None — suspicious description |
| poisoning-evasive | 30 | Skill-poisoning benchmark | Payload-less description |
| **Total** | **120** | | |

Run each instance **3 times** with different random seeds (accounts for model stochasticity).
Total attack trajectories: **360**.

#### Benign Corpus

| Source | N instances | Tool footprint |
|---|---|---|
| AgentDojo benign pool | ~80 | fetch_url, read_file, write_file |
| Curated tool-use tasks | ~40 | shell_exec, load_skill |
| **Total** | **120** | All 5 tools represented |

Run each benign instance **3 times**.
Total benign trajectories: **360**.

**Why size-match?** False-positive rate on the benign corpus directly measures overdefense. If corpora are different sizes, any class imbalance becomes a confound.

#### Stratified Train / Val / Test Split

Split: **60 / 20 / 20** of *instances* (not trajectories), stratified by:
- Attack type (injection vs. poisoning)
- Evasion level (overt vs. evasive)
- Generator model (M1 vs. M2)

All 3 repetitions of an instance go into the same split (never split repetitions of the same instance across folds — that's data leakage).

After split: label trajectories as `attack=1` or `attack=0`.

#### Generator Models

- **M1:** Frontier model via free tier (e.g., Gemini 1.5 Flash via Google AI Studio free tier, or similar)
- **M2:** Smaller open-weight model via Groq free tier (e.g., Llama 3.1 8B or Mixtral 8x7B)

Document the exact model versions used in the paper.

---

### Telemetry Schema

Every trajectory is logged as a JSON file with this schema:

```json
{
  "run_id": "string — unique per (instance_id, seed, model)",
  "instance_id": "string — task identifier from source benchmark",
  "seed": 0,
  "model": "m1|m2",
  "label": "attack|benign",
  "attack_type": "injection_overt|injection_evasive|poisoning_overt|poisoning_evasive|null",
  "task_description": "string — the original task given to the agent",
  "split": "train|val|test",
  "steps": [
    {
      "step_id": 0,
      "tool": "string — tool name",
      "args": {},
      "result_ok": true,
      "result_summary": "string — first 200 chars of tool output",
      "ts_ms": 1234567890
    }
  ],
  "final_action": "task_complete|exfiltrate|privilege_escalate|destructive|out_of_policy_network|other",
  "attack_succeeded": true,
  "total_steps": 0,
  "wall_clock_ms": 0
}
```

Store trajectories under `data/trajectories/{label}/{run_id}.json`.

---

### Baseline Protocols

Run all three baselines on the **same test-split trajectories** used for TRACE.

**Static scanner:** For each trajectory, check if the retrieved content at any step matches the deny-list. Report detection = 1 if any step triggers. Deny-list source: union of InjectAgent and BadAgent keyword sets.

**Guard model:** Run Llama Guard on the raw text of retrieved content at each step. Detection = 1 if any step scores above guard model's default threshold. Use the public `meta-llama/Llama-Guard-3-8B` checkpoint.

**LLM-judge:** For each step's retrieved content, send the classification prompt from Yi et al. (2023) Appendix to M1. Detection = 1 if the model responds "adversarial" or equivalent. Cap at 1 LLM call per step to bound cost.

---

## Experiment A — Separability / Detection Efficacy

**Tests:** H1 — Hijacked trajectories are statistically separable from benign trajectories.

### Setup

1. Extract feature vector `φ(ℓ, τ)` for every trajectory in the **train split**.
2. Train LightGBM classifier on train split (binary label: attack=1, benign=0).
3. Tune hyperparameters on val split (num_leaves, learning_rate, min_child_samples).
4. Lock the model. Run on **test split only** for all reported metrics.

### Measurement Protocol

For each threshold θ ∈ {0.3, 0.4, 0.5, 0.6, 0.7} and the optimal threshold from val-set Youden J:

- **Detection rate (DR):** fraction of attack trajectories where `score > θ`
- **False-positive rate (FPR):** fraction of benign trajectories where `score > θ`
- **AUC-ROC:** area under the receiver operating characteristic curve (threshold-free)
- **AUC-PR:** area under the precision-recall curve (better for imbalanced cases)

Report: mean ± 95% CI over the 3 repetitions of each test instance.

### Statistical Test

For the claim "TRACE detects better than baseline X":
Use **McNemar's paired proportion test** on the matched per-instance detection outcomes (TRACE correct vs. baseline correct on the same instance).
Significance threshold: α = 0.05, two-tailed.

### Confirmation Criteria (H1 confirmed)

- TRACE AUC-ROC > 0.85 on test split
- TRACE detection rate > 75% at FPR < 20%
- Difference from each baseline is statistically significant (McNemar's p < 0.05)

### Refutation Criteria (H1 refuted)

- TRACE AUC-ROC < 0.65 (near-random)
- OR TRACE is not significantly better than at least 2 of 3 baselines

### Known Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Class imbalance in attack cells | Stratified split; report AUC-PR not just AUC-ROC |
| Model stochasticity inflating variance | 3 repetitions per instance; report per-instance mean before pooling |
| Overfitting to train split | Val split tuning; locked model for test; report both val and test AUC |
| Feature leakage (ground truth label bleeds into features) | Double-check that `final_action` and `attack_succeeded` fields are NOT used as features |

---

## Experiment B — Evasion Stress Test

**Tests:** H2 — Behavioral detection retains high recall on evasive attacks where text-level defenses fail.

**This is the central result of the paper.**

### Setup

Reuse the same trained TRACE classifier from Experiment A.
Reuse the baseline results from Experiment A.
Slice the test split into four cells: {injection, poisoning} × {overt, evasive}.

### Measurement Protocol

For each method (TRACE + 3 baselines) and each cell:

- **Detection rate (DR):** fraction of trajectories in that cell detected (at optimal threshold from val split)
- **Drop from overt to evasive:** DR(overt) − DR(evasive) for each method

The key figure: a 4-column table (method × {injection-overt, injection-evasive, poisoning-overt, poisoning-evasive}).

Secondary figure: bar chart of DR by cell and method (makes the evasion collapse visually clear).

### Confirmation Criteria (H2 confirmed)

- All three text baselines show DR(evasive) < DR(overt) − 25 pp (i.e., detection collapses on evasive attacks)
- TRACE shows DR(evasive) < DR(overt) − 15 pp (some degradation is acceptable; the behavioral consequence is preserved but may be noisier)
- TRACE evasive DR > best baseline evasive DR by > 20 pp (statistically significant)

### Refutation Criteria (H2 refuted)

- TRACE evasive DR does not significantly exceed baselines' evasive DR
- OR text baselines do not degrade on evasive attacks (the attack's evasion claims are incorrect)

### Known Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Evasive cells are too small for significance | Report exact N per cell; add power analysis note if N < 20 |
| Evasive attacks actually partially visible in text | Manual inspection of 5 random evasive instances to verify trigger is invisible |
| TRACE degrades on evasive because features change | Ablation (Exp D) reveals which features are sensitive to evasion |

---

## Experiment C — Overdefense Frontier

**Tests:** H3 — Detection strength and preserved utility trade off along a smooth, tunable frontier.

### Setup

Reuse scored test-split trajectories from Experiment A (TRACE scores and baseline scores).
Run Algorithm 2 (threshold sweep) for TRACE and each baseline.
δ = 0.01 (101 threshold values from 0 to 1).

### Measurement Protocol

At each threshold θ:
- **Security S(θ):** DR on attack test split at that threshold
- **Utility U(θ):** 1 − FPR on benign test split at that threshold (fraction of benign runs not blocked)
- Record (U(θ), S(θ)) as a frontier point

Plot:
- X-axis: U(θ) = utility preserved (%)
- Y-axis: S(θ) = attack detection (%)
- One curve per method (TRACE + best baseline)

Report operating points explicitly:

| Utility floor | TRACE detection | Best baseline detection |
|---|---|---|
| 95% | ? | ? |
| 90% | ? | ? |
| 80% | ? | ? |
| 70% | ? | ? |

### Confirmation Criteria (H3 confirmed)

- TRACE curve is smooth (no discontinuous jumps > 10 pp between adjacent θ)
- At 90% utility retained, TRACE blocks > 70% of attacks
- TRACE dominates all baselines at every utility level ≥ 70%
- A viable operating point exists (e.g., 90% utility + 70% security)

### Refutation Criteria (H3 refuted)

- No threshold achieves > 60% security at > 80% utility (no viable operating point)
- OR frontier is non-monotone / degenerate

### Interpretation Notes

Report the area under the frontier curve (AUFC) as a single-number summary of overall tradeoff quality. Higher AUFC = better defense at all operating points simultaneously.

---

## Experiment D — Signal Attribution

**Tests:** H4a — A small, interpretable subset of behavioral signals accounts for most detection power.

### Setup

Retrain TRACE classifier on train split with each feature group removed, one at a time.
Evaluate each ablated classifier on val split (use val to avoid test-set p-hacking).
Also evaluate: F3 only; F1+F3 only; F1+F2+F3 only.

### Measurement Protocol

For each configuration:
- AUC-ROC on val split
- Detection rate at threshold calibrated on val split
- Report: AUC drop = Full_AUC − Ablated_AUC

Table format:

| Configuration | AUC | AUC drop |
|---|---|---|
| Full TRACE | X.XX | — |
| − F1 (sequence n-grams) | X.XX | ΔX |
| − F2 (argument anomalies) | X.XX | ΔX |
| − F3 (network destination) | X.XX | ΔX |
| − F4 (intent−action) | X.XX | ΔX |
| − F5 (structural) | X.XX | ΔX |
| F3 only | X.XX | — |
| F1 + F3 only | X.XX | — |

Feature importance: also report LightGBM's built-in feature importance (gain) to rank individual features within each group.

### Confirmation Criteria (H4a confirmed)

- Removing F3 or F1 causes AUC drop > 0.10 (these are the dominant signals)
- F1 + F3 alone achieves > 90% of full TRACE AUC

### Refutation Criteria (H4a refuted)

- No single feature group removal causes AUC drop > 0.05 (features contribute uniformly)
- OR F1 + F3 alone achieves < 80% of full AUC (no small interpretable subset dominates)

---

## Experiment E — Cross-Model Transfer

**Tests:** H4b — A detector trained on one model's trajectories generalizes to another's.

### Setup

Train four classifiers:
- **M1→M1:** train on M1 train split, evaluate on M1 test split
- **M2→M2:** train on M2 train split, evaluate on M2 test split
- **M1→M2:** train on M1 train split, evaluate on M2 test split
- **M2→M1:** train on M2 train split, evaluate on M1 test split

Use the same hyperparameters found in Experiment A (do not re-tune per split to avoid leakage).

### Measurement Protocol

For each of the four classifiers:
- AUC-ROC on the respective test split
- Detection rate at threshold calibrated on the training model's val split
- **Transfer gap:** in-distribution AUC − cross-model AUC

### Confirmation Criteria (H4b confirmed)

- Transfer gap < 0.05 for both cross-model directions
- Cross-model detection rate > 65% at FPR < 30% (still substantially above chance)

### Refutation Criteria (H4b refuted)

- Transfer gap > 0.15 for either direction
- Cross-model detection rate drops to near-chance (< 55%)

### Implications if Refuted

If H4b is refuted: behavioral patterns are model-specific, meaning operators need to calibrate on trajectories from their specific deployed model. This is still practically feasible — report the calibration cost — but the generality claim must be scoped.

---

## Deployment Overhead Measurement

Not a hypothesis test. A required deployability metric.

### Protocol

Measure for 100 trajectories from the test split (mix of attack and benign):

1. **Baseline latency:** Record wall-clock time for the agent to complete a run with telemetry collection only (no feature extraction, no classifier).
2. **TRACE latency:** Record wall-clock time with full TRACE (telemetry + features + classification).
3. **Overhead per step:** (TRACE_time − baseline_time) / num_steps

Also record:
- **Peak RSS memory** (MB) during TRACE feature extraction
- **CPU utilization** (%) averaged over 100 runs (use `psutil`)

### Targets

| Metric | Target |
|---|---|
| Overhead per step | < 5 ms |
| Peak RSS overhead | < 50 MB above baseline |
| CPU utilization | < 5% incremental |

If targets are missed: profile and report the bottleneck. Expected bottleneck: F4 (TF-IDF embedding computation). Mitigation: cache task embeddings; use faster embedding.

---

## Reporting Checklist (Before Submitting)

- [ ] All `\todo{}` markers in paper.tex replaced with real numbers
- [ ] Confidence intervals reported for all point estimates (AUC, DR, FPR)
- [ ] McNemar's test p-values reported for all "TRACE beats baseline X" claims
- [ ] N per cell reported in Table 1 (final counts, not targets)
- [ ] Model versions (M1, M2) documented with exact model IDs and API snapshot dates
- [ ] Benign corpus composition documented (benchmark source breakdown)
- [ ] Figure 3 (frontier) updated with real data curves
- [ ] All ablation rows in Table 4 filled
- [ ] All transfer rows in Table 5 filled
- [ ] Overhead measurements reported in §6.6
- [ ] Artifact repository URL added (un-redact for camera-ready)
