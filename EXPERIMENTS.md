# What We Are Experimenting

## The Core Idea

LLM agents (like ChatGPT with tools) can be **hijacked** by attackers.
Two main attack types:

1. **Prompt Injection** — attacker hides evil instructions inside a webpage or file the agent reads
2. **Skill Poisoning** — attacker publishes a fake plugin/tool that looks innocent but does harm

Existing defenses scan the *text* the agent reads. If the attack text looks clean, they miss it.

**Our idea:** Don't scan the text. Watch what the agent *does*.
A hijacked agent must exfiltrate data, contact unknown servers, or read secret files — regardless of how clean the trigger text looks.
Those actions show up in the execution log.

---

## The System — TRACE

TRACE sits between the agent and its tools.
Every tool call (read file, fetch URL, run shell) is logged.
TRACE looks at the pattern of those calls and scores the run as attack or benign.

```
Task → LLM Agent → [TRACE watches] → Tools → Result
                         ↓
                  Block or Allow
```

It uses a lightweight classifier (LightGBM) trained on 5 feature groups extracted from the log.

---

## The 5 Features

| # | Name | What it measures |
|---|------|-----------------|
| F1 | Sequence n-grams | Order of tool calls (e.g. read_file → POST is suspicious) |
| F2 | Argument anomalies | Base64 encoding, credential-shaped strings, unusual file paths |
| F3 | Network consistency | Did the agent contact a host the task never mentioned? |
| F4 | Intent–action gap | Are the agent's actions semantically related to its task? |
| F5 | Structural anomalies | Shell usage, repeated calls, privilege-sensitive tools |

---

## The 5 Experiments

### Experiment A — Does TRACE work at all?
Train TRACE on labeled trajectories. Measure AUC, detection rate, false positive rate.
Compare against three text-level baselines.

### Experiment B — Does it work on *evasive* attacks?
Evasive attacks use clean-looking text to fool scanners.
Text baselines should collapse. TRACE should hold.

### Experiment C — Security vs. Utility tradeoff
Sweep the detection threshold θ.
At each θ: how many attacks are caught vs. how many legitimate tasks are blocked?
Plot the frontier. Find the best operating point.

### Experiment D — Which features matter most?
Remove one feature group at a time. See how much AUC drops.
Expected: F1 (sequences) + F3 (network) do most of the work.

### Experiment E — Does it transfer across models?
Train on Gemini trajectories, test on Llama. Train on Llama, test on Gemini.
If AUC stays stable, the behavioral patterns are model-agnostic.

---

## The Data

| Set | Count | How |
|-----|-------|-----|
| Attack — injection overt | 30 | Agent reads a page with an obvious injection payload |
| Attack — injection evasive | 30 | Same but payload is disguised as maintenance instructions |
| Attack — poisoning overt | 30 | Agent loads a skill whose description warns it will exfiltrate |
| Attack — poisoning evasive | 30 | Same but description looks completely benign |
| Benign | 120 | Agent completes normal tasks (summarise, read config, write report) |

Two models run every task: **M1** (Gemini 1.5 Flash) and **M2** (Llama 3 8B via Groq).

---

## What Success Looks Like

| Hypothesis | What we need to see |
|------------|---------------------|
| H1 | TRACE AUC > 0.85, well above all text baselines |
| H2 | TRACE detection rate drops < 15% on evasive attacks; baselines drop > 40% |
| H3 | At 80% utility preserved, TRACE blocks > 80% of attacks |
| H4a | F1 + F3 alone explain most of the detection power |
| H4b | Transfer AUC drops < 0.05 between models |

---

## How to Run

```bash
# Add your OpenRouter key to .env
echo "OPENROUTER_API_KEY=sk-or-your-key" > .env

# Quick test (5 instances per cell, ~2 min)
python3 experiments/run_experiments.py --n 5

# Full run (30 per cell, ~3-4 hours)
python3 experiments/run_experiments.py --n 30

# If it crashes, just restart — checkpoints skip completed calls
python3 experiments/run_experiments.py --n 30

# Re-run analysis only (no API calls)
python3 experiments/run_experiments.py --skip-generation
```

Results land in `results/experiments.json`.
Every completed API call is saved in `data/checkpoints/` immediately —
a crash or shutdown loses nothing.
