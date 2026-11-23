# TRACE: Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories

Code and corpus for the paper **"Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories"**, accepted as an **oral presentation** at **IEEE ICCIT 2026**, the 29th International Conference on Computer and Information Technology (18–20 December 2026, Cox's Bazar, Bangladesh). Paper ID 2668.

## Publication

| | |
|---|---|
| **Title** | Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories |
| **Venue** | 2026 29th International Conference on Computer and Information Technology (ICCIT), IEEE |
| **Date and place** | 18–20 December 2026, Cox's Bazar, Bangladesh |
| **Paper ID** | 2668 (Accepted, Oral) |
| **Length** | 6 pages, IEEE two-column conference format |
| **Copyright line** | 979-8-3195-0171-4/26/$31.00 ©2026 IEEE |

### Authors

- **Debashis Kar Suvra**, Institute of Appropriate Technology, Bangladesh University of Engineering and Technology (BUET), Dhaka
- **Jannatul Ferdous Modina**, Bangladesh University of Business and Technology (BUBT), Dhaka
- **Azrin Nahar Anika**, Bangladesh University of Business and Technology (BUBT), Dhaka
- **MD Bakhtiar Abid**, BRAC University, Dhaka

### Citation

```bibtex
@inproceedings{suvra2026trace,
  title     = {Runtime Behavioral Detection of {LLM} Agent Hijacking from Execution Trajectories},
  author    = {Suvra, Debashis Kar and Modina, Jannatul Ferdous and Anika, Azrin Nahar and Abid, MD Bakhtiar},
  booktitle = {2026 29th International Conference on Computer and Information Technology (ICCIT)},
  year      = {2026},
  address   = {Cox's Bazar, Bangladesh},
  publisher = {IEEE}
}
```

(Pages and DOI will be added when IEEE Xplore publishes the proceedings.)

## Summary

LLM agents are vulnerable to indirect prompt injection and skill poisoning. Text-level defenses inspect the trigger text, so they fail against evasive variants whose triggering text is engineered to look clean. The key insight is that **the trigger can be hidden, but the behavioral consequence often cannot**: a hijacked agent must still make unauthorized tool calls, contact attacker-controlled hosts or exfiltrate data.

**TRACE (Trajectory-based Runtime Agent Compromise Examiner)** is a lightweight behavioral detector. It classifies an agent's execution trajectory (tool-call sequences, arguments and network destinations) with a gradient-boosted classifier. It needs only structured agent logs, not model weights or prompts, and runs on a CPU.

### Method

- **Classifier:** LightGBM (200 estimators, 31 leaves, learning rate 0.05, minimum child samples 5, balanced class weights, seed 42). These are fixed defaults, not grid-searched.
- **30 features in five groups:**
  - F1: sequence n-grams (15 dims)
  - F2: argument anomalies (5 dims)
  - F3: network-destination consistency (2 dims)
  - F4: TF-IDF intent–action similarity (1 dim)
  - F5: structural features (7 dims)

### Corpus

- 1,133 trajectories: 539 attack and 594 benign.
- Five generator models: Gemini 2.5 Flash Lite, Llama 3.1 8B, Mistral Nemo, Qwen 2.5 7B and Llama 3.2 3B.
- Four attack cells: overt and evasive injection, and overt and evasive poisoning.
- Split 60/20/20 (train/validation/test), stratified. The test set has 110 attack and 118 benign trajectories.
- Tools are **simulated stubs** (no real network or filesystem I/O).

### Key results

| Result | Value |
|---|---|
| AUC | **0.986** (95% CI 0.967–0.998) |
| Detection rate at FPR 2.5% | **93.6%** |
| Detection rate per attack cell | 90.0–96.2% |
| Keyword scanner detection rate | 23.6% (behavioral rules: 44.5%) |
| Leave-one-template-out (LOTO) | AUC 0.983, DR 92.3%, FPR 5.5% |
| Cross-model transfer AUC | 0.61–1.00 (hypothesis H2 not confirmed) |
| Adaptive F1+F2+F3 suppression | DR falls to 54.5% |
| Step-level mode (θ = 0.08) | 99.1% of attacks flagged before completion, but **80.5%** of benign runs flagged on some prefix (run-level FPR 6.8%) |
| Latency | 0.64–0.67 ms per query; 0.002 ms per trajectory batched; 1.2 ms feature extraction for 10 steps |

### Limitations

- All tools are simulated stubs, and the template bank is small (15 attack and 25 benign templates).
- The 80.5% step-level false-positive rate means step-level mode is a recall-oriented trigger, not a deployable blocker.
- Results are in-benchmark estimates and need validation on live agent traces.
- Cross-model transfer was not confirmed, and the detector may partly learn simulation artifacts.

## Repository layout

```
agent/          ReAct-style agent loop, tool stubs and telemetry used to generate trajectories
baselines/      Static keyword scanner baseline (15-keyword deny-list)
trace/          TRACE feature extraction (features.py), classifier (classifier.py), threshold sweep (sweep.py)
experiments/    Experiment scripts (run_experiments.py, run_baselines.py, run_camera_ready.py, ...)
data/           Corpus: 1,133 trajectory JSON files in data/checkpoints/
results/        Saved result files (experiments.json, camera_ready.json, smoke_test.json)
context/        Paper source (LaTeX)
camera_ready/   Camera-ready LaTeX source, certified PDF and reviewer-change notes
presentation/   Conference slides and speech
EXPERIMENTS.md  Experiment notes
```

## Getting started

```bash
pip install -r requirements.txt

# Reproduce the camera-ready numbers (AUC bootstrap CIs, step-level FPR, latency).
# Uses the stored corpus in data/checkpoints and makes no LLM API calls.
python experiments/run_camera_ready.py
```

The corpus was generated by running LLM agents through the simulated tools. Regenerating it (`experiments/run_experiments.py`) needs LLM API access and keys in a `.env` file. Evaluating on the released corpus does not.

> **Note:** the repository contains the corpus and code. A saved trained-model file is not included, so train the classifier from the data with `trace/classifier.py`.

## Scope and responsible use

This is defensive research on detecting hijacked agents. The attack trajectories are synthetic, produced against simulated tools. The detector is evaluated under a non-adaptive threat model. Under full feature suppression its detection rate falls to 54.5%, so it should complement pre-execution defenses, not replace them.

## Contact

Debashis Kar Suvra, 0421292001@iat.buet.ac.bd
