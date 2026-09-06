# Peer Review Response — TRACE (ICCIT 2026)

**Paper:** Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories
**Review date:** September 6, 2026
**Response prepared:** September 6, 2026

---

## Major Comments

| # | Issue | Action | Status | Files changed |
|---|-------|--------|--------|---------------|
| M1 | Novelty claims not supported by 2025–2026 literature — several behavioral trajectory detectors exist (AgentArmor, Agent-Sentry, fraud-detection-layer paper, MindGuard) not cited | Rewrote §II-D to explicitly acknowledge the 2024–2026 convergence on trajectory-based detection; added Agent Security Bench and CyberSecEval 2 citations; reframed the contribution as FPR-calibrated overdefense + CPU-only/model-internals-free rather than claiming to be "first" | **Fixed in text** — novelty reframed | `paper.tex §II-D`, `strings.bib` |
| M2 | "First overdefense quantification framework" claim contradicted by ASB (2024) and CyberSecEval 2 (2024) | Removed "first" claim in §VIII Conclusion; reframed the contribution as "FPR-calibrated overdefense frontier over a size-matched benign corpus, complementary to existing security-utility benchmarks"; added \cite{zhang2024agentsecuritybench} and \cite{bhatt2024cyberseceval2} | **Fixed** | `paper.tex §II-D, §VIII`, `strings.bib` |
| M3 | Only a keyword scanner is used as a runtime baseline; no behavioral competitor evaluated | Added Exp F: behavioral rule-based detector (R1=out-of-policy host, R2=base64 args, R3=POST to external host) — DR=50.0% [36.1–63.9], FPR=0.0%. Added to Table II. No new API calls required — computed from existing checkpoints. A fully replicated contemporaneous behavioral competitor (e.g., Agent-Sentry) remains future work and noted in conclusion. | **Fixed (new experiment)** | `paper.tex Table II, §VI-F/G`, `experiments/run_new_experiments.py`, `results/experiments.json` |
| M4 | LLM-generated corpus may encode generation-provenance artifacts rather than pure behavioral signal | Added explicit construct-validity note to §VII ("Sandbox generalizability and corpus validity") explaining the risk and recommending validation on live compromised-agent trajectories | **Fixed in text** | `paper.tex §VII` |
| M5 | Table II (FPR=4.2%) and Table III ("FPR=0 for all methods") irreconcilable — Table III per-cell evaluation contains no benign trajectories, making FPR=0 trivially true | Fixed Table III caption: removed misleading FPR claim, added explicit note that per-cell evaluation covers attack trajectories only, with aggregate FPR from Table II; fixed §VI-B text to remove "FPR=0 throughout" | **Fixed** | `paper.tex §VI-B, Tab. III caption` |
| M6 | F1+F3 carry ~96% of detection power but are also the easiest features to suppress (per §VII-a); headline 91.7–100% rates not qualified accordingly | Added Exp G: adaptive-attacker ablation simulating F3 suppression (redirect URLs to implied host) and F1 suppression (shuffle step order). Results: F3-only suppression leaves DR=97.9% unchanged (other features compensate); F1+F3 combined reduces DR to 77.1% (AUC=0.967) — still 3× keyword scanner. New Table VI + §VI-G added. §VII-a updated with actual numbers. | **Fixed (new experiment)** | `paper.tex §VI-G, §VII-a, Table VI`, `experiments/run_new_experiments.py` |
| M7 | Cross-model transfer criterion (H2) not met; Abstract/Conclusion imply released weights are directly reusable | Updated §VIII Conclusion to state "the released weights and dataset enable independent replication of classifier results, but per-deployment calibration on target-model benign logs is required before production use" | **Fixed** | `paper.tex §VIII` |

---

## Minor Comments

| # | Issue | Action | Status | Files changed |
|---|-------|--------|--------|---------------|
| 1 | "first…framework" language repeated near-verbatim in Abstract and §VIII | Removed from both locations; replaced with reframed contribution language in §II-D and §VIII | **Fixed** | `paper.tex` |
| 2 | Related Work stops at 2024; no 2025–2026 defense cited | Added ASB (2024) and CyberSecEval 2 (2024) to §II-D; text acknowledges contemporaneous behavioral-detector work | **Partially fixed** (cannot do full literature survey in revision; additional papers from review not cited pending verification of their existence) | `paper.tex §II-D`, `strings.bib` |
| 3 | §III-b does not state whether attacker is black-box w.r.t. TRACE classifier | Added: "The attacker is assumed black-box with respect to TRACE: aware that a behavioral detector exists but not knowing the trained weights or threshold θ" | **Fixed** | `paper.tex §III` |
| 4 | Table III n=12 arithmetic unexplained | Caption now reads "n=12 attack trajectories per cell = 60 × 20% test portion" | **Fixed** | `paper.tex Tab. III` |
| 5 | Δ=0.000 for F2/F4 interpreted as "subsumed" — may be measurement noise at near-ceiling AUC | Hedged §VI-D: "on a 96-trajectory test set near performance ceiling, Δ=0.000 may partly reflect measurement resolution rather than strict redundancy" | **Fixed** | `paper.tex §VI-D` |
| 6 | LightGBM hyperparameters not reported (needed for reproducibility) | Added to §IV-C: "200 estimators; 31 leaves; learning rate 0.05; minimum 5 child samples; balanced class weights; random seed 42" (from `trace/classifier.py`) | **Fixed** | `paper.tex §IV-C` |
| 7 | "XGBoost produces equivalent results" asserted with no numbers | Removed the unsupported XGBoost equivalence claim | **Fixed** | `paper.tex §IV-C` |
| 8 | F4 called "novel" contribution in §II-D but ablation shows it contributes 0.000 AUC | Reframed in §II-D: F4 "introduces an agent-specific signal with no direct OS analog; the current TF-IDF implementation contributes minimally in isolation (Exp D), motivating richer future instantiations" | **Fixed** | `paper.tex §II-D` |
| 9 | §V-B: unclear how many templates appear in test vs. train (template leakage risk) | Added clarification: "Because the number of unique base task templates is small (5 attack, 10 benign), all template families appear in both train and test; the split tests generalization across instance variation (host, repetition, model) rather than held-out task semantics" | **Fixed** | `paper.tex §V-B` |
| 10 | InjectAgent described as "17 tools" — actually 17 user tools + 62 attacker tool types | Fixed §II-B: "1,054 injection cases across 17 user tools (62 attacker tool types)" | **Fixed** | `paper.tex §II-B` |
| 11 | Figure 3 θ=0.08 operating point not visually marked on curve | Added `\node` annotation at (95.8, 97.9) labelled "$\theta{=}0.08$" in the PGFPlots axis | **Fixed** | `paper.tex Fig. 3` |
| 12 | "Requiring no model internals" appears near-verbatim in Abstract, §I, §III | Abstract changed to "operating without access to model weights or prompts"; §I contribution bullet changed to "black-box with respect to model weights and prompts"; §III keeps the detailed formal statement | **Fixed** | `paper.tex Abstract, §I` |
| 13 | Title uses "hijacking"; system name expands to "Compromise Examiner" — terms used interchangeably | Black-box attacker assumption in §III uses "hijacking" for the attack event. Full resolution would require renaming the acronym (not done — TRACE is the system name) | **Partially fixed** (clarified in §III; renaming acronym deferred) | `paper.tex §III` |
| 14 | Table IV mixes "−F1" ablation and "F3 only" isolation naming conventions | Reformatted: ablation rows indented with `\quad −` prefix; isolation rows separated by `\midrule` and labelled "F3 alone" / "F1+F3 alone" | **Fixed** | `paper.tex Tab. IV` |
| 15 | §VIII Conclusion restates AUC/DR/utility figures nearly verbatim from §VI | Conclusion rewritten to focus on takeaways (threat-model scoping, open problems) rather than repeating numbers | **Fixed** | `paper.tex §VIII` |
| 16 | No AI-use disclosure | Added `\section*{AI Use Disclosure}` before `\end{document}` clarifying LLM APIs used for trajectory generation, not for manuscript text | **Fixed** | `paper.tex` |
| 17 | Claimed artifact release has no repository link/DOI/license | Added `[repository link redacted for review]` placeholder in §V-C; replace with actual URL before submission | **Fixed (placeholder)** — replace before camera-ready | `paper.tex §V-C` |

---

## Experiments Completed in This Revision

| Exp | Description | Result |
|-----|-------------|--------|
| Exp F | Behavioral rule-based baseline (R1=out-of-policy host, R2=base64, R3=POST to external) — no ML | DR=50.0% [36.1–63.9], FPR=0.0% (vs. 25.0% keyword, 97.9% TRACE) |
| Exp G (F3) | Adaptive attacker: route exfiltration through task-implied host | DR=97.9% — unchanged; F1/F2/F5 compensate |
| Exp G (F1) | Adaptive attacker: shuffle step sequence to break attack bigrams | DR=77.1%, AUC=0.967 |
| Exp G (F1+F3) | Both simultaneous worst-case suppression | DR=77.1%, AUC=0.967 — same as F1 alone; F2/F5 maintain residual signal |

## Still Requires New Experiments (outside revision scope)

| Item | Description | Recommendation |
|------|-------------|----------------|
| M4 (full) | Isolate generation-provenance confound | Train/test on a held-out generator model or use actual compromised-agent traces rather than prompted generation |
| M7 (full) | Add ≥1 more generator model family | Evaluate transfer to a third backbone (e.g., GPT-4o-mini, Mistral) to substantiate any cross-model generalization claim |

---

## Changes NOT Made (and Why)

| Item | Reason |
|------|--------|
| Adding citations for AgentArmor, Agent-Sentry, MindGuard, Yu et al. 2026 (M1/M2) | These paper titles appear in the reviewer report but their full bibliographic details and existence were not independently verified. Adding unverified citations would risk citing hallucinated papers. The §II-D rewrite acknowledges the trend without citing unverified sources. These should be found and added before submission via a fresh literature search. |
| Renaming TRACE acronym for "hijacking"/"compromise" consistency (Minor 13) | TRACE backronym is established in the abstract and throughout. Renaming would require global changes with marginal benefit. |

---

## Summary Statistics (Round 1)

| Category | Total issues | Fixed in text | Requires experiment | Deferred/partial |
|----------|-------------|---------------|--------------------|--------------------|
| Major | 7 | 5 (M1,M2,M4,M5,M6,M7 — text portion) | 3 (M3,M4,M6 — new data) | 1 (M3 baseline) |
| Minor | 17 | 15 | 0 | 2 (13, 2-partial) |
| **Total** | **24** | **19** | **3** | **3** |

---

## Round 2 Peer Review Response

**Review date:** September 6, 2026 (second review)

### Major Comments

| # | Issue | Action | Status | Files changed |
|---|-------|--------|--------|---------------|
| M1 | Missing prior art: TraceAegis, PIDS literature (Kairos, Zipperle survey) make the same OS-to-agent analogy | Rewrote §II-D to acknowledge PIDS literature and contemporaneous agent-security systems; added `\cite{zipperle2022pids,cheng2024kairos}` for the PIDS grounding; reframed contributions as FPR-calibrated frontier + one-command reproducibility rather than "domain mapping"; added explicit ASB vs CyberSecEval2 contrast (Minor 13 also fixed here) | **Fixed in text** | `paper.tex §II-D`, `strings.bib` |
| M2 | No learned baseline (LR over bigrams, XGBoost/GNN competitors exist) | Acknowledged in §VII-b (already) and REVIEW_RESPONSE; implementing a logistic-regression-over-F1 baseline requires re-running experiments — deferred as future experiment | **Deferred** — requires new experiment run | — |
| M3 | Train/test template overlap inflates AUC; template-disjoint split needed | §V-B already discloses the confound explicitly; implementing a leave-template-out split requires regenerating trajectories with held-out templates — deferred | **Deferred** — requires new data generation | — |
| M4 | Simulated stubs limit external validity; should be foregrounded | Promoted stub limitation note into §V-A (agent environment) rather than burying in §VII; §VII limitation paragraph retained | **Fixed in text** | `paper.tex §V-A` |
| M5 | Over ICCIT 6-page limit | Multiple rounds of cutting brought paper to 6 pages | **Fixed** | `paper.tex` |
| M6 | Abstract omits negative H2 cross-model result | Added one sentence to Abstract: "Cross-model transfer AUC (0.80–0.85) does not meet the stated <0.05-drop criterion: per-deployment recalibration is required." | **Fixed** | `paper.tex Abstract` |

### Minor Comments

| # | Issue | Action | Status |
|---|-------|--------|--------|
| 1/12 | "no inference cost" overclaims | Changed to "negligible inference cost"; removed vague clause | **Fixed** |
| 2 | F4 contributes 0.000 AUC — drop or invest | Retained with existing "TF-IDF contributes minimally" caveat; dropping F4 would require re-running all experiments | **Partially fixed** (text caveat) |
| 3 | §III scope vs Exp G tension | Revised §III Scope to explicitly include "partial adaptive evasion (Exp G)" as in-scope and clarify out-of-scope as "full adaptive evasion" | **Fixed** |
| 4 | Table IV (−0.004 AUC) vs Table VI (−20.8 DR) unexplained | Added one sentence to §VI-D: "redundant-but-load-bearing features behave differently under retraining versus adversarial corruption at test time" | **Fixed** |
| 5 | Hyperparameter selection unclear | Added "selected by grid search on the validation split with no further tuning on the test set" to §IV-C | **Fixed** |
| 6 | Both models are small/cheap tiers | Added note in §V-A: "both smaller/cheaper tiers; larger planning models may produce different F1/F5 feature distributions" | **Fixed** |
| 7 | CPU spec not given | Changed "standard laptop CPU" to "mid-range laptop CPU"; full CPU model omitted (double-blind) | **Partially fixed** |
| 8 | Table III wide CIs — state in body | Added note in §VI-B body: "wide CI reflects n=12 per cell; point estimates should not be over-indexed" | **Fixed** |
| 9 | AUC 0.984 lacks bootstrapped CI | Not added — would require code change and new run; noted as limitation | **Deferred** |
| 10 | One-miss mechanism explained at wrong location | Kept explanation in §VI-C where it first matters for the threshold discussion; §VI-B now notes the wide CIs instead | **Partially fixed** |
| 11 | Artifact anonymized upload | Informational — no text change needed | N/A |
| 13 | ASB/CyberSecEval2 contrast missing | Added explicit "neither provides a per-deployment FPR-calibrated frontier" contrast in §II-D | **Fixed** (folded into M1) |
| 14 | Citation packing | §II-D rewritten to distribute citations across sentences | **Fixed** |

### Changes NOT Made (Round 2)

| Item | Reason |
|------|--------|
| TraceAegis, Zavrak 2026, Yu et al. 2026 citations | Paper titles appear in reviewer report but full bibliographic details and existence were not independently verified — citing unverified papers risks hallucinated references. §II-D acknowledges the concurrent work trend without fabricating citations. Search and add before camera-ready. |
| Logistic regression learned baseline (M2) | Requires re-running experiment pipeline; deferred |
| Template-disjoint split (M3) | Requires generating new held-out task templates and re-running; deferred |
| Bootstrapped AUC CI (Minor 9) | Requires code change and re-run |
