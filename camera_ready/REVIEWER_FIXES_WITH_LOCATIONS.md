# Reviewer comments → fixes, with page and line numbers

**Paper 2668 — Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories (IEEE ICCIT 2026, Accepted [Oral])**
Checked against the certified file `camera_ready/certified/2668.pdf` (6 pages, IEEE PDF eXpress certified).

**How to read the locations.** The IEEE format has no printed line numbers. "p4 · left · lines 72–73" means page 4, left column, counting printed lines from the top of that column (table and figure text rows count). Treat line numbers as accurate to about ±2. Section names are given so each item is easy to find.

---

## Reviewer 1

The review praises the idea, the evaluation and the honesty about weak spots. It then lists six requests for the camera-ready version.

| # | Reviewer request (verbatim) | Status | What was changed | Location in certified PDF |
|---|---|---|---|---|
| R1.1 | "Add AUC confidence intervals." | Done | Percentile-bootstrap 95% CIs (2,000 resamples of the 228-trajectory test split). Trace AUC 0.986 [0.967–0.998]; CIs also given for RF 0.981 [0.959–0.996], LR-all 0.965 [0.941–0.986] and LR-F1 0.907 [0.868–0.940]. The text states Trace and RF are not statistically distinguishable. | **Table II**, p4 · left · lines 1–12 (caption states the bootstrap), row at line 29; **Sec. VI-A text**, p4 · left · lines 72–73 ("AUC 0.986 (95 % CI 0.967–0.998)"); abstract mention p1 · left · line 25 |
| R1.2 | "Report the false-positive rate for step-level mode at θ = 0.08." | Done | Every prefix of the 118 benign test trajectories was scored: 95 of 118 (**80.5%**, Wilson CI 72.4–86.6%) flagged at θ=0.08; 69.5% at θ=0.5; run-level FPR 6.8%. Step-level mode is reframed as a recall-oriented trigger, not a deployable blocker. | **Sec. VI-B**, p4 · right · lines 58–68 (the 80.5 / 69.5 / 6.8 figures at lines 62–65); **Abstract**, p1 · left · lines 28–32; **Discussion VII-c**, p5 · right · lines 34–38; **Conclusion**, p5 · right (step-level sentence from line 50) |
| R1.3 | "State plainly that the tools are simulated and the template bank is small." | Done | New Limitations paragraph: all tools are simulated stubs (five tools), the template bank is small (15 attack, 25 benign), trajectories are LLM-simulated so the detector may partly learn simulation artifacts, and validation on live agent traces is needed. | **Limitations (VII-d)**, p5 · right · lines 39–44; **Setup**, p3 · right · lines 40–42 ("All tools are simulated stubs, no real network I/O") |
| R1.4 | "Explain how cross-model calibration would work in practice." | Done | Practical procedure: collect benign trajectories from the target deployment, then refit on them plus the released attack corpus. If refitting is impossible, re-select θ as the score quantile meeting the FPR budget. The paper states this corrects score shift but not feature shift. | **Sec. VII-b "Feature generalization and calibration"**, p5 · right · lines 14–26 (procedure at lines 21–26) |
| R1.5 | "Rename 'Exp M3' so it isn't confused with model M3." | Done | Renamed to **Exp LOTO** (leave-one-template-out) everywhere. The baseline LR-F1 is likewise no longer called "M2". A text search of the PDF finds no "Exp M3". | **Sec. V-B**, p4 · left · lines 50–53 ("Exp LOTO, 15-fold … macro AUC 0.983, DR 92.3 %, FPR 5.5 %"); **Related Work**, p2 · left · lines 59–60 ("leave-one-template-out (LOTO) evaluation"); abstract p1 · left · line 25 (template-disjoint CV: 0.983) |
| R1.6 | "Include the artifact link." | Done | `https://github.com/Suvrakar/Runtime-Behavioral-Detection-of-LLM-Agent` (the repo is public). | **Sec. V-C**, p4 · left · lines 61–63; abstract p1 · left · lines 33–34 ("released as an open artifact") |

---

## Reviewer 2

This review asks three questions. Each is answered in Section VII (Discussion) with the evidence available, and the paper marks what was not tested.

| # | Reviewer question (verbatim) | Status | Answer added to the paper | Location in certified PDF |
|---|---|---|---|---|
| R2.1 | "What feature engineering strategies and behavioral primitives enable the gradient-boosted classifier to generalize effectively for highly heterogeneous generator models?" | Answered, and stated as untested | F3 (network destination consistency) and F2 (argument anomalies) are defined by task and tool semantics, not model phrasing, so they are the most plausible model-agnostic signals. F1 (tool-name n-grams) encodes each model's tool-use habits and is the likeliest source of the cross-family degradation in Table IV (AUC 0.61–1.00). The paper explicitly does not claim the feature set is generator-invariant. | **Sec. VII-b**, p5 · right · lines 14–20 |
| R2.2 | "What architectural enhancements are needed to counter sophisticated adversaries who intentionally mimic benign execution pathways?" | Answered, with a measured result and untested proposals | Measured: full F1+F2+F3 suppression drops DR to **54.5%** (AUC 0.927), still 2.3× the keyword scanner. Proposed but not evaluated: (i) enforce the host allow-list at a gateway, (ii) taint tracking from untrusted observations to network-write tools, (iii) adversarial training on suppression-augmented attacks, (iv) sequence models over event streams. | **Sec. VII-a "Adaptive attackers and mimicry"**, p5 · right · lines 5–13; measured result in **Exp G2**, p5 · left · lines 61–64 and p5 · right · lines 1–3; abstract p1 · left · lines 32–33 |
| R2.3 | "How scalable is the 0.67 ms/query step-level inference latency when scaling to concurrent multi-agent environments with complex, long-horizon dependency chains?" | Answered, and states what was not measured | Measured: 0.64–0.67 ms per single query, 0.002 ms per trajectory batched, 1.2 ms feature extraction for a 10-step trajectory. Scoring is stateless per trajectory, so concurrent agents scale horizontally. Per-prefix re-extraction is quadratic in length unless counters are incremental. **Not measured:** concurrent multi-agent load and long-horizon trajectories, and the paper says so. | **Sec. VII-c "Scalability and timing"**, p5 · right · lines 27–38 (batched/1.2 ms at lines 28–29, "not measured" at lines 33–34) |

---

## Extra corrections made while revising (not requested by reviewers)

| Fix | Detail | Location |
|---|---|---|
| Hyperparameters | The text said "grid-searched", but the code uses fixed values. The text now says fixed defaults, not tuned. | Sec. V (implementation) |
| Fig. 3 | The static scanner was plotted at 25% detection. Corrected to 23.6%, matching the table and text. | **Fig. 3**, p4 · right · lines 17–19; 23.6% also at p4 · left · lines 10 and 71 |
| Generator families | "Three LLM families" corrected to four. | Sec. V (setup) |
| Adaptive text | The "Adaptive attackers" and mimicry text was merged, and sections were trimmed to hold the 6-page limit. | Sec. VII-a |
| Camera-ready format | Real author block and emails, IEEE Index Terms, ICCIT header (top of p1), IEEE copyright footer `979-8-3195-0171-4/26/$31.00 ©2026 IEEE` (p1 · left · line 52), 6 pages, fonts embedded. | Page 1 |

## Honest limits (as stated in the paper)

- The 80.5% step-level false-positive rate is real. Step-level mode is not a deployable blocker until a prefix-trained classifier exists.
- Cross-model transfer was not confirmed (H2 not confirmed).
- The tools are simulated, so results are in-benchmark estimates.
- The mimicry defenses in R2.2 are proposals, not evaluated results.
- Concurrent multi-agent and long-horizon latency were not measured (R2.3).

## Known gap outside the reviewers' requests

- The abstract says "the corpus and trained weights are released as an open artifact" (p1 · left · lines 33–34). The repo contains the corpus and code, but no saved model-weights file. Either add the weights file to the repo or change that sentence. Editing the PDF now would mean redoing PDF eXpress.
