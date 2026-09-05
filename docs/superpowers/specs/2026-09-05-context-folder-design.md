# Context Folder Design: LLM Agent Hijacking Paper

**Date:** 2026-09-05
**Target venue:** IEEE S&P (Oakland)
**Project:** Watch What It Does, Not What It Says — Behavioral Detection of Agent Hijacking from Execution Trajectories

---

## Scope

Create the `context/` folder as the working home for the paper draft, bibliography, experiment specifications, and literature review. Four files total. Everything needed to go from spec to submission without hunting for references or experiment details.

---

## File Structure

```
llm-hijacking-paper/
└── context/
    ├── paper.tex              # Full IEEE S&P draft, IEEEtran class, ~13 pages
    ├── paper.bib              # BibTeX entries for all cited papers (~50 entries)
    ├── experiments_spec.md    # Per-experiment protocol (Experiments A–E + overhead)
    └── literature_review.md   # Annotated bibliography + gap analysis by cluster
```

---

## paper.tex

- Class: `\documentclass[conference]{IEEEtran}`
- Packages: amsmath, amssymb, graphicx, tikz, pgfplots, algorithm, algorithmic, booktabs, hyperref, xcolor, cleveref
- State: **Full draft**. Every prose section written. Results section has `\todo{}` placeholder values but full table structure and expected-direction commentary.
- Double-blind ready: no author names, no self-identifying acknowledgments.

### Sections

| # | Title | State |
|---|---|---|
| — | Abstract | Fully written, 200 words |
| 1 | Introduction | Fully written |
| 2 | Background | Fully written |
| 3 | Threat Model | Fully written |
| 4 | TRACE: Trajectory-based Runtime Agent Compromise Examiner | Fully written + TikZ figures |
| 5 | Experimental Setup | Fully written |
| 6 | Results | Tables with `\todo{}` + expected direction prose |
| 7 | Discussion | Fully written |
| 8 | Related Work | Fully written |
| 9 | Conclusion | Fully written |
| — | References | Auto via BibTeX |

### TikZ Figures

- **Fig 1** — TRACE system architecture (agent → telemetry → feature extraction → classifier → decision gate)
- **Fig 2** — Attack taxonomy 2×2 grid (injection vs. poisoning × overt vs. evasive)
- **Fig 3** — Detection pipeline flowchart (runtime flow of a single agent step through TRACE)
- **Fig 4** — Placeholder security-utility frontier (ROC-style curve, `\todo{}` data)

### Algorithms

- **Algorithm 1** — TRACE feature extraction pseudocode
- **Algorithm 2** — Threshold sweep for security-utility frontier

---

## paper.bib

~50 BibTeX entries organized in clusters:
1. Prompt injection attacks (Greshake, Perez & Ribeiro, Liu et al., Zhan et al.)
2. Skill/tool/MCP poisoning (Shi et al. BadAgent, MCP security literature)
3. Agent benchmarks (AgentDojo/Debenedetti, InjectAgent)
4. Text-level defenses (spotlighting, guard models, LLM-judge)
5. Agent architecture (ReAct, Toolformer, agent surveys)
6. Behavioral detection analogs (Forrest et al. system-call, malware behavior analysis)
7. LLM security surveys

---

## experiments_spec.md

One section per experiment plus an overhead measurement section. Each section contains:

- **Hypothesis:** which research hypothesis this tests
- **Setup:** exact corpora (attack class × variant × N per cell), train/test splits, repetitions
- **Telemetry schema:** JSON format for a single trajectory log entry
- **Measurement protocol:** how to compute each metric, confidence intervals, statistical test
- **Confirmation criteria:** specific numerical criterion that "confirms" the hypothesis
- **Refutation criteria:** what result would falsify it
- **Known failure modes:** rate limits, trajectory variance, class imbalance — and mitigations

Experiments: A (separability), B (evasion stress), C (overdefense frontier), D (signal attribution), E (cross-model transfer), + deployment overhead.

---

## literature_review.md

Annotated bibliography structured by five clusters plus a gap analysis section.

### Clusters

1. **Indirect prompt injection** (6 papers) — attacks, benchmarks, characterization
2. **Skill/tool/MCP poisoning** (5 papers) — attack mechanisms, stealthy variants
3. **Text-level defenses** (5 papers) — static scanners, guard models, spotlighting, LLM-judge
4. **Behavioral detection analogs** (4 papers) — system-call anomaly detection, malware behavioral analysis, API sequence analysis
5. **Agent architecture foundations** (5 papers) — ReAct, Toolformer, plan-and-execute, agent surveys

### Per-entry format

```
### [SHORT_KEY] Author et al., Year
**Full citation:** ...
**Venue:** ...
**Summary:** 2 sentences.
**Relevance to TRACE:** 1-2 sentences.
**Gap left:** 1 sentence — what this paper does NOT address that TRACE does.
```

### Gap analysis section

After all clusters: a prose section mapping each cluster's collective gap to a specific TRACE contribution or research question.

---

## Constraints

- No external figures (PDF/PNG) — all figures via TikZ inline in paper.tex
- All citations real, verified papers (no hallucinated DOIs or titles)
- Results tables use `\todo{}` with expected direction noted in comments
- Double-blind compliant (no author info)
- Compiles clean with `pdflatex paper.tex` after `bibtex paper`
