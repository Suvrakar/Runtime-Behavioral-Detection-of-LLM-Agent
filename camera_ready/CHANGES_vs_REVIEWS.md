# Camera-ready changes vs. reviewer comments
**Paper 2668 — Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories (IEEE ICCIT 2026)**
Files: `paper.tex`, `strings.bib`, `paper.pdf` (6 pages). New numbers: `experiments/run_camera_ready.py` -> `results/camera_ready.json`.

## Reviewer 1

| # | Request | What changed | Where |
|---|---------|--------------|-------|
| 1 | Add AUC confidence intervals | Percentile-bootstrap 95% CIs (2,000 resamples of the 228-trajectory test split): TRACE 0.986 [0.967-0.998], RF 0.981 [0.959-0.996], LR-all 0.965 [0.941-0.986], LR-F1 0.907 [0.868-0.940]. Text now states TRACE vs RF is not statistically distinguishable. | Table II, Sec. VI-A |
| 2 | Report step-level false-positive rate at theta=0.08 | Scoring every prefix of the 118 benign test trajectories flags 95 (**80.5%**, Wilson CI 72.4-86.6%); 69.5% at theta=0.5; run-level FPR at theta=0.08 is 6.8%. Step-level mode is now described as a recall-oriented trigger, not a deployable blocker; abstract, Sec. VI-B, Discussion and Conclusion updated accordingly. | Abstract, Sec. VI-B, VII, VIII |
| 3 | State plainly that tools are simulated and template bank is small | New "Limitations" paragraph: all tools are simulated stubs (five tools), 15 attack / 25 benign templates, LLM-simulated trajectories may let the detector learn simulation artifacts; live-trace validation needed. | Sec. VII |
| 4 | Explain how cross-model calibration would work | Practical procedure: collect benign logs from the target deployment, then refit on them plus the released attack corpus, or re-select theta as the score quantile meeting the FPR budget (corrects score shift, not feature shift). | Sec. VII |
| 5 | Rename "Exp M3" | Renamed "Exp LOTO" (leave-one-template-out) everywhere; baseline LR-F1 likewise no longer called "M2". | Sec. II, V, VI, VII |
| 6 | Include the artifact link | `https://github.com/Suvrakar/Runtime-Behavioral-Detection-of-LLM-Agent`. | Sec. V-C |

## Reviewer 2

| # | Question | Answer added to the paper (honest scope) | Where |
|---|----------|------------------------------------------|-------|
| 1 | Which feature engineering/primitives let the classifier generalize across heterogeneous generator models? | F3 (off-allow-list network calls) and F2 counts are defined by task and tool semantics, not model phrasing, so are the most plausible model-agnostic signals; F1 n-grams encode model tool-use habits and are the likely source of cross-family degradation (AUC 0.61-1.00). Stated as untested; no generator-invariance claim. | Sec. VII |
| 2 | Architectural enhancements against adversaries who mimic benign pathways? | Existing evidence: F1+F2+F3 suppression drops DR to 54.5% (Exp G2). Proposed, not evaluated: gateway enforcement of the host allow-list, taint tracking from untrusted observations to network-write tools, adversarial training on suppression-augmented attacks, sequence models over event streams. | Sec. VII |
| 3 | Scalability of 0.67 ms/query for concurrent multi-agent, long-horizon settings? | Measured: 0.64 ms single query, 0.002 ms/trajectory batched (~5x10^5/s one core), feature extraction 1.2 ms for a 10-step trajectory. Scoring is stateless per trajectory (horizontal scaling); naive per-prefix re-extraction is quadratic unless counters are incremental. Concurrent multi-agent load and >10-step trajectories were **not** measured, and the paper says so. | Sec. VII |

## Other corrections made while revising (not requested)
- Hyperparameters were described as "grid-searched"; `trace/classifier.py` uses fixed values. Text now says they were fixed defaults, not tuned.
- Fig. 3 plotted the static scanner at 25% detection; corrected to 23.6% (matches table and text).
- "Three LLM families" corrected to four.
- Sec. VII "Adaptive attackers" text merged with mimicry discussion; sections trimmed (setup, Exp A/C/D/E/F text, conclusion) to stay at 6 pages.

## Formatting for IEEE Xplore
- IEEEtran conference class, 6 pages, no page numbers, all fonts embedded.
- Double-blind placeholder removed; author block and IEEE keywords added.
- **TODO before upload:** replace nothing in emails (real emails added); add postal addresses if required, then complete CMT upload, registration and the IEEE e-Copyright form.
