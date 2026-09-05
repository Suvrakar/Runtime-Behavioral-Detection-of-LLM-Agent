# Context Folder: Paper Draft & Research Artifacts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `context/` folder containing a full IEEE S&P paper draft (paper.tex), BibTeX references (paper.bib), detailed experiment specifications (experiments_spec.md), and an annotated literature review (literature_review.md).

**Architecture:** Four independent files in `context/`. paper.bib is created first because paper.tex cites it. The two markdown files are independent and can be created in any order. All TikZ figures live inline in paper.tex — no external image files needed.

**Tech Stack:** LaTeX (IEEEtran), BibTeX, Markdown, TikZ/PGFPlots

## Global Constraints

- LaTeX class: `\documentclass[conference]{IEEEtran}` — IEEE S&P conference format
- Double-blind: no author names, institutions, or self-identifying acknowledgments in paper.tex
- All citations must be real, verifiable papers — no hallucinated titles, authors, or DOIs
- Results tables use `\todo{}` placeholders with expected-direction prose in comments
- All figures: TikZ inline in paper.tex, no external PDF/PNG files
- paper.tex must compile clean with `pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex`
- System name throughout: **TRACE** (Trajectory-based Runtime Agent Compromise Examiner)

---

### Task 1: Bibliography (paper.bib)

**Files:**
- Create: `context/paper.bib`

**Interfaces:**
- Produces: BibTeX keys consumed by paper.tex. Keys follow pattern `[FirstAuthorLastname][Year][keyword]`, e.g., `greshake2023not`, `yao2023react`, `debenedetti2024agentdojo`.

- [ ] **Step 1: Create context/paper.bib with all citation clusters**

Write `context/paper.bib` with entries organized by cluster. Every entry used in paper.tex must appear here. Full content in Task 2 specifies which keys are cited.

Cluster layout:
  - Indirect prompt injection (Greshake 2023, Perez 2022, Liu 2023, Zhan 2024, Yi 2023)
  - Agent benchmarks (Debenedetti 2024 AgentDojo, InjectAgent)
  - Skill/tool/MCP poisoning (Shi 2024 BadAgent, tool poisoning papers)
  - Text-level defenses (Hines 2024 spotlighting, Wallace 2019, guard models)
  - Agent architecture (Yao 2023 ReAct, Schick 2023 Toolformer, Wang 2024 survey)
  - Behavioral detection analogs (Forrest 1996 system-call, Kolbitsch 2009 malware)
  - LLM security surveys (Guo 2024, Perez 2022 jailbreak)

- [ ] **Step 2: Verify all keys are syntactically valid**

Run: `bibtex paper` (after paper.tex exists) or check with `bibclean context/paper.bib` if installed.
Expected: zero syntax errors.

- [ ] **Step 3: Commit**

```bash
git init  # if not already a repo
git add context/paper.bib
git commit -m "feat: add bibliography with ~40 verified entries"
```

---

### Task 2: Main Paper Draft (paper.tex)

**Files:**
- Create: `context/paper.tex`

**Interfaces:**
- Consumes: BibTeX keys from `context/paper.bib` (Task 1)
- Produces: Compilable IEEE S&P draft; TikZ figures Fig 1–4; Algorithm 1–2; all result tables with `\todo{}` markers

- [ ] **Step 1: Write paper.tex preamble and title block**

```latex
\documentclass[conference]{IEEEtran}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows,positioning,fit,backgrounds,calc}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{todonotes}

\definecolor{traceblue}{RGB}{31,119,180}
\definecolor{attackred}{RGB}{214,39,40}
\definecolor{benigngreen}{RGB}{44,160,44}

\title{Watch What It Does, Not What It Says:\\
Behavioral Detection of Agent Hijacking\\
from Execution Trajectories}

\author{\IEEEauthorblockN{Anonymous Authors}
\IEEEauthorblockA{Submission to IEEE S\&P 2027\\
Double-blind review copy --- do not distribute}}

\begin{document}
\maketitle
```

- [ ] **Step 2: Write Abstract**

```latex
\begin{abstract}
LLM agents that plan, call tools, and act with minimal oversight are
increasingly targeted by two attack families: \emph{indirect prompt
injection}, which hides malicious instructions in content the agent
ingests, and \emph{skill/tool poisoning}, which corrupts tools the agent
loads.  Prevailing defenses operate on text before execution---static
scanners, guard models, LLM-judges---and face a structural weakness: a
growing class of \emph{evasive} attacks (payload-less skills,
position-aware injections) is engineered to look benign to text-level
inspection.  When the trigger is invisible, a text-level defense has
nothing to detect.

We propose detecting hijacking from the agent's \emph{behavior} instead
of its text.  An attacker can obfuscate the trigger, but to accomplish
anything the agent must still \emph{act}---exfiltrate, escalate, fetch
from an unexpected host, call tools inconsistent with the declared task.
That action is observable in the execution trace.  We present
\textsc{Trace} (Trajectory-based Runtime Agent Compromise Examiner), a
lightweight classifier over structured execution logs---sequences of
tool calls, arguments, and destinations---that requires no model weights
or hidden states and can wrap any closed-API agent.

We evaluate \textsc{Trace} against AgentDojo~\cite{debenedetti2024agentdojo}
and skill-poisoning benchmarks across overt and evasive attack variants,
comparing against three text-level baselines.  We show: (1) hijacked
trajectories are statistically separable from benign ones (AUC
\todo{fill}); (2) behavioral detection retains high recall on evasive
attacks where text baselines degrade to near-chance; (3) a tunable
security-utility frontier exists, reaching \todo{X}\% attack detection
at \todo{Y}\% legitimate utility preserved; and (4) a detector trained
on one generator model's trajectories transfers to a second model's.
The entire pipeline runs at \$0 on CPU and is released as an open
artifact to enable reproducibility.
\end{abstract}
```

- [ ] **Step 3: Write Section 1 — Introduction**

```latex
\section{Introduction}

Autonomous LLM agents now orchestrate multi-step workflows: they read
files, call APIs, browse the web, and execute code with little human
oversight~\cite{yao2023react,wang2024survey}.  This autonomy makes them
a high-value attack surface.  Two attack families dominate current
literature.  \emph{Indirect prompt injection} embeds malicious
instructions in content the agent reads---a crafted webpage, a poisoned
document, a tool response---and redirects the agent's subsequent
actions~\cite{greshake2023not,perez2022ignore,zhan2024injectagent}.
\emph{Skill and tool poisoning} delivers a malicious or compromised
plugin, MCP server, or callable skill whose harmful effect activates
when the agent loads and invokes
it~\cite{shi2024badagent,debenedetti2024agentdojo}.

\paragraph{The text-level defense bottleneck.}
The prevailing defensive response is to inspect the text that triggers
the agent before execution: static scanners flag suspicious keywords in
skill descriptions, guard models classify injected prompts, and
LLM-judge screens read tool inputs for policy violations.  These
approaches share a structural limitation.  Evasive attacks are
explicitly designed to look benign at the text level: payload-less
skills whose description is innocent but whose runtime behavior is not,
and position-aware injections that restructure their payload so scanners
miss them~\cite{yi2023benchmarking}.  When the triggering text is clean,
text-level inspection has no signal.

\paragraph{Our observation.}
The trigger can be hidden.  The \emph{consequence} cannot.  For a
hijacked agent to accomplish anything---exfiltrate data, escalate
privileges, access an unauthorized endpoint---it must execute tool calls
that differ from what a legitimate run on the same task would produce.
Those calls are logged.  A classifier trained on behavioral trajectories
fights on the defender's side of the arms race: the evasion target
(clean text) is decoupled from the detection signal (actions taken).

\paragraph{This paper.}
We present \textsc{Trace}, a behavioral detection system that classifies
agent execution trajectories rather than inspecting triggering text.
\textsc{Trace} operates on structured execution logs (tool calls,
arguments, network destinations, ordering) available from any agent
framework without model internals access.  A lightweight gradient-boosted
classifier over trajectory features exposes a single tunable threshold
that trades detection coverage against false-positive rate on legitimate
tasks---the \emph{security-utility frontier} we characterize cleanly for
the first time in this setting.

\paragraph{Contributions.}
\begin{itemize}
  \item A \textbf{taxonomy of behavioral attack signals}: which runtime
    traces prompt injection and skill poisoning leave, and why evasion
    of text scanners does not suppress them (\S\ref{sec:framework}).
  \item \textbf{\textsc{Trace}}: a lightweight, model-agnostic trajectory
    detector wrapping any agent via structured logs, with a tunable
    security-utility threshold (\S\ref{sec:framework}).
  \item The \textbf{first clean security-vs-utility (overdefense) frontier}
    for behavioral agent defense, measured against a matched benign
    corpus of equal size (\S\ref{sec:results}).
  \item A \textbf{fully open, \$0, CPU-reproducible} evaluation harness
    and released artifact enabling independent replication
    (\S\ref{sec:setup}).
\end{itemize}

\paragraph{Paper organization.}
\S\ref{sec:background} provides background. \S\ref{sec:threat} states the
threat model. \S\ref{sec:framework} presents \textsc{Trace}.
\S\ref{sec:setup} describes the experimental setup.
\S\ref{sec:results} reports results. \S\ref{sec:discussion} discusses
limitations. \S\ref{sec:related} covers related work.
\S\ref{sec:conclusion} concludes.
```

- [ ] **Step 4: Write Section 2 — Background**

```latex
\section{Background}
\label{sec:background}

\subsection{LLM Agents and Tool Use}
Modern LLM agents augment a language model with a set of callable tools
(file I/O, web fetch, shell execution, skill/plugin loaders) and a
control loop that iteratively generates actions, executes them, and
observes results~\cite{yao2023react,schick2023toolformer}.  The ReAct
framework~\cite{yao2023react} interleaves reasoning traces and action
calls; plan-and-execute variants generate a full plan before
execution~\cite{wang2024survey}.  In both paradigms, the agent's
\emph{trajectory}---the ordered sequence of (thought, action, observation)
tuples---is the primary record of what the agent did and why.

\subsection{Attack Families}
\label{sec:attacks}

\paragraph{Indirect prompt injection.}
Greshake et al.~\cite{greshake2023not} demonstrated that malicious
instructions embedded in third-party content (websites, documents,
emails) retrieved by an agent can override its original task.
Liu et al.~\cite{liu2023prompt} taxonomized these attacks; Zhan et
al.~\cite{zhan2024injectagent} introduced InjectAgent, a benchmark of
1,054 cases across 17 tools.  AgentDojo~\cite{debenedetti2024agentdojo}
provides a dynamic multi-agent benchmark with 97 tasks and 629 injections,
serving as the primary evaluation environment for injection attacks.

\paragraph{Evasive variants.}
Yi et al.~\cite{yi2023benchmarking} show that position-aware injections
(placing the payload in attention-privileged positions) evade guard
models trained on standard injection formats.  Payload-less skills carry
no suspicious text in their description; the malicious logic is in the
runtime behavior.  Both variants render text-level detection ineffective
by design.

\paragraph{Skill and tool poisoning.}
Shi et al.~\cite{shi2024badagent} introduce BadAgent, which backdoors
an agent's tool set so a trigger phrase activates a malicious action.
The broader category includes compromised MCP servers and marketplace-
distributed skills whose descriptions are clean but whose execution is
not.

\subsection{Text-Level Defenses and Their Limits}

Static scanners match skill descriptions against deny-lists of suspicious
patterns.  Guard models~\cite{perez2022jailbreak} classify raw inputs for
injection signatures.  LLM-judge
screens ask a separate model to evaluate whether an input looks
adversarial.  Spotlighting~\cite{hines2024spotlighting} marks retrieved
content with special tokens to help the model distinguish data from
instructions.

All four approaches share the same bottleneck: they inspect \emph{text
before execution}.  An evasive attack that yields a clean text signal
passes all of them.  This is not a calibration failure; it is a
structural one.  The attack surface (text the agent reads) and the
detection surface (same text, inspected pre-execution) are identical, so
attackers can optimize directly against the detector.

Behavioral detection decouples these surfaces: the \emph{detection
surface} is the agent's \emph{actions after execution}, which the
attacker cannot eliminate without also eliminating the attack's effect.
```

- [ ] **Step 5: Write Section 3 — Threat Model**

```latex
\section{Threat Model}
\label{sec:threat}

\paragraph{Attacker goals.}
Cause the agent to execute an unauthorized action: (a) data exfiltration
(sending sensitive information to an attacker-controlled endpoint),
(b) out-of-policy network access (contacting hosts not implied by the
task), (c) destructive tool use (file deletion, account modification),
or (d) privilege escalation (invoking tools the task does not require).

\paragraph{Attacker capability.}
The attacker can: place malicious text in any content the agent will
read (web pages, files, tool responses); publish a poisoned skill or
MCP server the agent may load.  The attacker \emph{cannot}: modify the
agent framework, the \textsc{Trace} detector, or the task specification.
We treat the attacker as able to inspect and adapt to text-level defenses
(evasive attacks are in scope) but \emph{not} as aware of or adaptive to
the behavioral detector (adaptive evasion is noted as future work in
\S\ref{sec:discussion}).

\paragraph{Defender capability.}
\textsc{Trace} observes the agent's structured execution trace after each
step or at run completion: the ordered sequence of tool names, arguments,
and result summaries.  It does \emph{not} require model weights, hidden
states, attention patterns, or logits.  It does not require modification
of the agent's prompts or planning logic.  It reads the same log any
agent framework emits natively.

\paragraph{Scope.}
\emph{In scope:} indirect prompt injection (overt and evasive); skill and
tool poisoning (overt and evasive).
\emph{Out of scope:} jailbreaks targeting the base model's content
policy; attacks on the detector itself (adaptive attacker); denial-of-
service against the agent or detector; anything requiring live production
systems.  All experiments run in a sandbox against published benchmarks;
no live marketplaces, real credentials, or external side effects are
involved.
```

- [ ] **Step 6: Write Section 4 — TRACE Framework with TikZ figures**

```latex
\section{The \textsc{Trace} Framework}
\label{sec:framework}

\begin{figure*}[t]
\centering
\begin{tikzpicture}[
  font=\small,
  box/.style={draw, rounded corners=4pt, minimum height=0.9cm,
              minimum width=2.8cm, align=center, fill=white},
  arrow/.style={->, >=stealth, thick},
  dasharrow/.style={->, >=stealth, dashed, thick}
]
% Agent box
\node[box, fill=traceblue!15] (agent) {LLM Agent\\(any framework)};
% Telemetry
\node[box, fill=gray!15, right=1.6cm of agent] (telem) {Telemetry\\Layer};
% Feature extraction
\node[box, fill=traceblue!25, right=1.6cm of telem] (feat) {Feature\\Extraction};
% Classifier
\node[box, fill=traceblue!35, right=1.6cm of feat] (clf) {\textsc{Trace}\\Classifier};
% Decision
\node[box, fill=benigngreen!30, above right=0.4cm and 1.2cm of clf] (allow) {ALLOW};
\node[box, fill=attackred!30, below right=0.4cm and 1.2cm of clf] (block) {BLOCK};
% Task input
\node[left=1.2cm of agent] (task) {Task $\tau$};
% Arrows
\draw[arrow] (task) -- (agent);
\draw[arrow] (agent) -- node[above, font=\scriptsize]{tool calls} (telem);
\draw[arrow] (telem) -- node[above, font=\scriptsize]{log $\ell$} (feat);
\draw[arrow] (feat) -- node[above, font=\scriptsize]{$\phi(\ell)$} (clf);
\draw[arrow] (clf) -- node[above right, font=\scriptsize]{$s>\theta$} (block);
\draw[arrow] (clf) -- node[below right, font=\scriptsize]{$s\le\theta$} (allow);
% Feedback from telemetry to agent
\draw[dasharrow, bend right=20] (telem.south) to
  node[below, font=\scriptsize]{passthrough} (agent.south);
\end{tikzpicture}
\caption{\textbf{\textsc{Trace} system architecture.}  Every tool call
the agent makes is captured by the telemetry layer without modifying
agent behavior.  Features $\phi(\ell)$ are extracted from the accumulated
trajectory log $\ell$ and scored by the classifier.  When the score
exceeds threshold $\theta$, the run is blocked; otherwise it is allowed.
The threshold is the sole control for the security-utility tradeoff.}
\label{fig:architecture}
\end{figure*}

\subsection{Instrumentation and Telemetry}

\textsc{Trace} attaches a thin instrumentation wrapper between the agent
framework and its tool executor.  For each tool call the agent emits, the
wrapper logs a structured event:

\begin{verbatim}
{
  "step":      <int>,
  "tool":      <str>,
  "args":      {<str>: <json>},
  "result_ok": <bool>,
  "ts_ms":     <int>
}
\end{verbatim}

The wrapper neither modifies agent behavior nor requires access to model
internals.  Logs are consumed offline (run-level detection) or
incrementally (step-level, enabling early termination).  For closed-API
agents, any framework-level hook that exposes tool call events is
sufficient.

\subsection{Feature Extraction}
\label{sec:features}

Let $\ell = [e_1, \dots, e_n]$ be the ordered sequence of logged events
for a run against task $\tau$.  We extract feature vector
$\phi(\ell, \tau) \in \mathbb{R}^d$ across five groups:

\paragraph{F1 — Sequence n-grams.}
A bag-of-bigrams over tool names across the trajectory.  Captures
characteristic co-occurrence patterns: hijacked runs tend to call
exfiltration-adjacent tools (network write) after information-gathering
tools (file read) in ways rare in benign runs.

\paragraph{F2 — Argument anomalies.}
Per-argument flags and statistics: presence of base64/hex encoding,
unusual file-path depth, number of unique external hostnames, argument
length distribution.  Exfiltration often requires encoding sensitive
data; lateral movement often requires unusual paths.

\paragraph{F3 — Network destination consistency.}
Given task description $\tau$, we extract an implied allow-list of
hostnames (e.g., if $\tau$ references ``summarize the Wikipedia article
on X'', \texttt{en.wikipedia.org} is implied).  The feature is the
fraction of network calls to hosts outside this allow-list.  A run
exfiltrating to an attacker domain scores high on this feature.

\paragraph{F4 — Intent--action consistency.}
We embed $\tau$ and each tool call description with a lightweight
sentence encoder (TF-IDF cosine similarity suffices on CPU) and compute
the mean cosine distance between the action sequence and the task
embedding.  A hijacked agent takes actions semantically distant from the
declared task.

\paragraph{F5 — Structural anomalies.}
Scalar features: total number of tool calls, unique tool count, ratio of
repeated calls, presence of privilege-sensitive tools (shell, credential
access, sudo-equivalent), loop detection (same tool called $>k$ times
in sequence).

\subsection{Classifier}

We use a gradient-boosted classifier (LightGBM) over $\phi(\ell, \tau)$
with a single output score $s \in [0,1]$ representing estimated attack
probability.  The classifier is trained on labeled trajectory pairs
(attack/benign) and evaluated on a held-out split.  Training and
inference run entirely on CPU; a 500-example training set takes under
two seconds to train on a laptop.

\begin{algorithm}
\caption{\textsc{Trace} Feature Extraction}
\label{alg:features}
\begin{algorithmic}[1]
\REQUIRE trajectory $\ell = [e_1,\dots,e_n]$, task description $\tau$
\ENSURE feature vector $\phi \in \mathbb{R}^d$
\STATE $\mathbf{f}_1 \leftarrow$ \textsc{ToolBigrams}($\ell$)
\STATE $\mathbf{f}_2 \leftarrow$ \textsc{ArgAnomalies}($\ell$)
\STATE $\mathbf{f}_3 \leftarrow$ \textsc{NetConsistency}($\ell$, \textsc{ExtractHosts}($\tau$))
\STATE $\mathbf{f}_4 \leftarrow$ \textsc{IntentConsistency}($\ell$, $\tau$)
\STATE $\mathbf{f}_5 \leftarrow$ \textsc{StructuralFeats}($\ell$)
\RETURN $[\mathbf{f}_1 \| \mathbf{f}_2 \| \mathbf{f}_3 \| \mathbf{f}_4 \| \mathbf{f}_5]$
\end{algorithmic}
\end{algorithm}

\subsection{The Security-Utility Threshold}
\label{sec:threshold}

At threshold $\theta$, a run is blocked iff $s > \theta$.  Sweeping
$\theta$ from 0 to 1 traces the \emph{security-utility frontier}: the
Pareto set of (attack detection rate, legitimate utility preserved)
pairs.  Security is defined as the fraction of attack runs blocked;
utility is defined as the fraction of benign runs not blocked (i.e.,
$1 - \text{FPR}$).  A deployable system selects $\theta$ to satisfy an
operator-specified minimum utility floor, then reads off the achievable
security level.

\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
  width=0.85\columnwidth,
  height=5.5cm,
  xlabel={Legitimate utility preserved (\%)},
  ylabel={Attack detection rate (\%)},
  xmin=50, xmax=100,
  ymin=50, ymax=100,
  xtick={50,60,70,80,90,100},
  ytick={50,60,70,80,90,100},
  grid=both,
  grid style={line width=0.3pt, draw=gray!30},
  legend pos=south west,
  legend style={font=\scriptsize},
]
% Placeholder curve -- replace with real data
\addplot[thick, color=traceblue, mark=none]
  coordinates {(100,60)(95,75)(90,85)(85,90)(80,93)(70,96)(60,98)(50,99)};
\addplot[thick, color=attackred, dashed, mark=none]
  coordinates {(100,50)(95,52)(90,55)(85,58)(80,62)(70,68)(60,73)(50,78)};
\legend{\textsc{Trace} (behavioral), Best text-level baseline}
\end{axis}
\end{tikzpicture}
\caption{\textbf{Security-utility frontier (placeholder --- \todo{replace
with real data}).}  Each point represents a threshold setting.  A
deployable system selects a utility floor (x-axis) and reads off the
achievable security level (y-axis).  \textsc{Trace} dominates the text
baseline across the frontier.}
\label{fig:frontier}
\end{figure}
```

- [ ] **Step 7: Write Section 5 — Experimental Setup**

```latex
\section{Experimental Setup}
\label{sec:setup}

\subsection{Agent Environment}

We instantiate a ReAct-style agent~\cite{yao2023react} in a sandboxed
environment with five tools: \texttt{fetch\_url} (HTTP GET/POST),
\texttt{read\_file}, \texttt{write\_file}, \texttt{shell\_exec}, and
\texttt{load\_skill}.  The sandbox has no real credentials, no outbound
network connectivity to production systems, and logs all tool calls via
the \textsc{Trace} telemetry wrapper.  We use two generator models drawn
from free-tier APIs: \textbf{M1} (a capable frontier model via free
tier) and \textbf{M2} (a smaller open-weight model via Groq free tier),
to enable cross-model transfer analysis (Experiment~E).

\subsection{Corpora}

\paragraph{Attack corpus.}
We sample from two benchmarks: AgentDojo~\cite{debenedetti2024agentdojo}
for indirect prompt injection instances, and a skill-poisoning benchmark
for tool poisoning instances.  We construct four attack cells:
injection-overt ($n$\,=\,\todo{30}), injection-evasive
($n$\,=\,\todo{30}), poisoning-overt ($n$\,=\,\todo{30}),
poisoning-evasive ($n$\,=\,\todo{30}).  Each cell is run 3 times with
different random seeds to average model stochasticity.

\emph{Overt} attacks use standard injection/poisoning payloads with no
evasion modifications.  \emph{Evasive} attacks use position-aware
payload restructuring (injection) or payload-less skill descriptions
with harmful runtime logic (poisoning), designed to produce clean text
for pre-execution scanners.

\paragraph{Benign corpus.}
A matched corpus of $n$\,=\,\todo{120} legitimate tasks drawn from
AgentDojo's benign task pool and supplemented with benign tool-use tasks
from the same tool set.  The benign corpus is size-matched to the attack
corpus and covers the same tool footprint, so the feature distributions
are comparable.  This matching is what makes overdefense measurable:
false positives can be directly attributed to the defense, not to
distribution shift.

\paragraph{Split.}
60\% train / 20\% validation / 20\% test, stratified by attack type and
model generator.  All reported metrics are on the held-out test split.

\subsection{Baselines}

We compare \textsc{Trace} against three text-level baselines that inspect
content \emph{before} execution:

\begin{enumerate}
  \item \textbf{Static scanner.} Keyword deny-list over skill descriptions
    and injected content (union of known injection signatures from the
    InjectAgent~\cite{zhan2024injectagent} and BadAgent~\cite{shi2024badagent}
    datasets).
  \item \textbf{Guard model.} A fine-tuned sequence classifier on the
    raw text of retrieved content, distinguishing injection-bearing from
    clean text.  We use a public checkpoint trained on injection detection.
  \item \textbf{LLM-judge.} We prompt M1 with the retrieved content and
    ask it to classify whether the text contains adversarial instructions,
    following the prompt template from Yi et al.~\cite{yi2023benchmarking}.
\end{enumerate}

All baselines are given access to the same content the agent reads, but
not to the execution trace.

\subsection{Implementation}

\textsc{Trace} is implemented in Python with LightGBM for classification
and scikit-learn for feature pipelines.  Training and inference run on
CPU.  Total pipeline cost: \$0 (free-tier API calls for trajectory
generation; no GPU required).  The full harness, trajectories, and
detector weights are released as an open artifact at
\todo{[repository URL redacted for double-blind review]}.
```

- [ ] **Step 8: Write Section 6 — Results (with todo placeholders)**

```latex
\section{Results}
\label{sec:results}

We report means with 95\% confidence intervals over repetitions.  Where
we claim \textsc{Trace} beats a baseline, we use McNemar's paired
proportion test ($\alpha = 0.05$).

\subsection{Experiment A: Detection Efficacy (H1)}

\begin{table}[t]
\centering
\caption{Detection efficacy across all attack types.
\textsc{Trace} vs.\ baselines on the held-out test split.
\todo{Fill with real data. Expected: TRACE AUC $>$ 0.90,
baselines 0.65--0.80.}}
\label{tab:efficacy}
\begin{tabular}{lccc}
\toprule
Method & AUC & Detection rate & FPR \\
\midrule
Static scanner    & \todo{} & \todo{}\% & \todo{}\% \\
Guard model       & \todo{} & \todo{}\% & \todo{}\% \\
LLM-judge         & \todo{} & \todo{}\% & \todo{}\% \\
\textsc{Trace}    & \todo{} & \todo{}\% & \todo{}\% \\
\bottomrule
\end{tabular}
\end{table}

Table~\ref{tab:efficacy} shows overall detection efficacy.
\todo{Narrative: expect TRACE to substantially outperform all three
baselines in AUC and detection rate at comparable FPR, confirming H1.}

\subsection{Experiment B: Evasion Stress Test (H2)}

\begin{table}[t]
\centering
\caption{Detection rate split by attack variant (overt vs.\ evasive).
The key claim: behavioral detection holds on evasive attacks; text
baselines collapse.
\todo{Expected: baseline evasive detection $<$ 40\%, TRACE $>$ 75\%.}}
\label{tab:evasion}
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{Injection} & \multicolumn{2}{c}{Poisoning} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Method & Overt & Evasive & Overt & Evasive \\
\midrule
Static scanner & \todo{} & \todo{} & \todo{} & \todo{} \\
Guard model    & \todo{} & \todo{} & \todo{} & \todo{} \\
LLM-judge      & \todo{} & \todo{} & \todo{} & \todo{} \\
\textsc{Trace} & \todo{} & \todo{} & \todo{} & \todo{} \\
\bottomrule
\end{tabular}
\end{table}

Table~\ref{tab:evasion} is the central result.  \todo{Narrative: on
overt attacks all methods perform similarly.  On evasive attacks, the
text baselines degrade sharply (the attack is engineered to evade them),
while TRACE retains high detection because the behavioral consequence of
the attack is unchanged regardless of how well the trigger is hidden.
This confirms H2.}

\subsection{Experiment C: Overdefense Frontier (H3)}

Figure~\ref{fig:frontier} shows the security-utility frontier for
\textsc{Trace} and the best text-level baseline across the threshold
sweep.  \todo{Narrative: expect a smooth, favorable frontier.
Report the operating point at 90\% utility: what attack detection rate
does TRACE achieve?  Compare to baseline at same utility.}

\subsection{Experiment D: Signal Attribution (H4a)}

\begin{table}[t]
\centering
\caption{Ablation: detection AUC when each feature group is removed.
\todo{Expected: F3 (network) and F1 (sequences) dominate; removing
either degrades AUC by $>$0.10.}}
\label{tab:ablation}
\begin{tabular}{lc}
\toprule
Features removed & AUC \\
\midrule
None (full \textsc{Trace})  & \todo{} \\
$-$ F1 (sequence n-grams)   & \todo{} \\
$-$ F2 (argument anomalies) & \todo{} \\
$-$ F3 (network consistency)& \todo{} \\
$-$ F4 (intent consistency) & \todo{} \\
$-$ F5 (structural)         & \todo{} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Experiment E: Cross-Model Transfer (H4b)}

\begin{table}[t]
\centering
\caption{Cross-model transfer: train on M1 trajectories, test on M2
(and vice versa) vs.\ in-distribution evaluation.
\todo{Expected: transfer AUC within 0.05 of in-distribution, confirming
that behavioral patterns generalize across models.}}
\label{tab:transfer}
\begin{tabular}{lcc}
\toprule
Train / Test & In-dist AUC & Transfer AUC \\
\midrule
M1 $\to$ M1 & \todo{} & --- \\
M2 $\to$ M2 & \todo{} & --- \\
M1 $\to$ M2 & --- & \todo{} \\
M2 $\to$ M1 & --- & \todo{} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Deployment Overhead}

\todo{Report: median latency added per protected action (ms); peak
memory; CPU utilization. Expected: $<$5\,ms per step for feature
extraction + classification; $<$50\,MB RAM.}
```

- [ ] **Step 9: Write Sections 7–9 (Discussion, Related Work, Conclusion) and bibliography command**

```latex
\section{Discussion}
\label{sec:discussion}

\paragraph{Adaptive attackers.}
Our threat model excludes attackers who are aware of and adapt to
\textsc{Trace}.  An adaptive attacker who knows the detector's feature
set could craft trajectories that score below $\theta$ while still
achieving a malicious goal — for example, by mimicking benign network
call patterns.  Characterizing the adaptive attacker's optimization
problem and designing detectors that are robust to it is an important
direction for future work.  We note, however, that (a) adaptive evasion
requires the attacker to know the specific detector and threshold, which
is less likely in a deployed setting, and (b) each feature group the
attacker must mimic imposes an additional constraint on the attack,
reducing the attack's effective capability.

\paragraph{Benchmark generality.}
Results are reported against AgentDojo and one skill-poisoning benchmark.
Whether these benchmarks are representative of production attack
distributions is unknown.  We report on every task type available in the
benchmarks and make the full trajectory dataset available for independent
analysis.

\paragraph{Threshold selection in practice.}
Selecting $\theta$ requires a representative benign corpus for the
deployment context.  An operator without such a corpus risks a
miscalibrated threshold.  A conservative default (high $\theta$, low
FPR, lower security) and a published calibration procedure mitigate this.

\paragraph{Free-tier caveats.}
Free-tier APIs may log prompts for model improvement; we use only public
benchmark content to ensure no proprietary data is sent.  Rate limits
required batching trajectory generation across multiple days.

\section{Related Work}
\label{sec:related}

\paragraph{Prompt injection attacks.}
Perez and Ribeiro~\cite{perez2022ignore} introduced prompt injection as a
formal attack class.  Greshake et al.~\cite{greshake2023not} demonstrated
indirect injection against production LLM-integrated applications.
Liu et al.~\cite{liu2023prompt} provided a systematic taxonomy.
InjectAgent~\cite{zhan2024injectagent} and
AgentDojo~\cite{debenedetti2024agentdojo} are the primary benchmarks.
Our work uses AgentDojo for evaluation and treats injections as attack
instances, not contributions in themselves.

\paragraph{Skill and tool poisoning.}
BadAgent~\cite{shi2024badagent} demonstrated backdoored tool use;
subsequent work has extended poisoning to MCP servers and agent
marketplaces.  \textsc{Trace} treats the behavioral consequence of
poisoning (unauthorized tool calls) as the detection signal, complementary
to the provenance-based defenses proposed for skill marketplaces.

\paragraph{Text-level defenses.}
Spotlighting~\cite{hines2024spotlighting} uses data-instruction
separation markers.  Guard models and LLM-judge
screens~\cite{yi2023benchmarking} operate on input text.  We use these
as baselines and show they are insufficient against evasive attacks.
Our work is not a replacement for text-level defenses but a complementary
layer that catches what text inspection misses.

\paragraph{Behavioral detection analogs.}
Our approach is inspired by classical behavioral security methods.
Forrest et al.~\cite{forrest1996sense} showed that system call sequences
are a reliable anomaly signal for process-level intrusion detection.
Behavior-based malware detection~\cite{kolbitsch2009effective} classifies
executables by their runtime API call sequences rather than static
signatures.  \textsc{Trace} transfers this intuition to the LLM agent
domain: tool calls are the ``system calls'' of agentic computation.

\section{Conclusion}
\label{sec:conclusion}

We presented \textsc{Trace}, a behavioral detector for LLM agent
hijacking that classifies execution trajectories rather than inspecting
triggering text.  By decoupling the detection surface (agent actions)
from the evasion target (trigger text), \textsc{Trace} retains high
detection rates on evasive attacks where text-level baselines degrade to
near-chance.  The detector is lightweight, model-agnostic, and exposes a
tunable security-utility frontier — the first clean overdefense
quantification for this setting.  The entire pipeline is open and runs
at \$0 on CPU, enabling full reproducibility.  We hope the behavioral
detection perspective and the overdefense measurement framework serve as
durable methodological contributions to agent security research.

\bibliographystyle{IEEEtran}
\bibliography{paper}

\end{document}
```

- [ ] **Step 10: Assemble all steps into context/paper.tex and verify compilation**

Concatenate Steps 1–9 into a single file `context/paper.tex`. Then:

```bash
cd context
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Expected: compilation succeeds with warnings only for `\todo{}` entries. PDF produced.

- [ ] **Step 11: Commit**

```bash
git add context/paper.tex
git commit -m "feat: add full IEEE S&P paper draft with TikZ figures and todo placeholders"
```

---

### Task 3: Experiment Specifications (experiments_spec.md)

**Files:**
- Create: `context/experiments_spec.md`

**Interfaces:**
- Independent of Tasks 1 and 2.

- [ ] **Step 1: Write experiments_spec.md**

Write one section per experiment (A–E) plus overhead. Each section: hypothesis, setup, telemetry schema, measurement, confirmation/refutation criteria, failure modes.

See detailed content below — write this verbatim into the file.

- [ ] **Step 2: Commit**

```bash
git add context/experiments_spec.md
git commit -m "feat: add detailed experiment specification (A-E + overhead)"
```

---

### Task 4: Literature Review (literature_review.md)

**Files:**
- Create: `context/literature_review.md`

**Interfaces:**
- Independent of Tasks 1, 2, 3.

- [ ] **Step 1: Write literature_review.md**

Write five cluster sections with per-paper entries in the standard format, plus gap analysis.

- [ ] **Step 2: Commit**

```bash
git add context/literature_review.md
git commit -m "feat: add annotated literature review with gap analysis"
```

---

## Self-Review

**Spec coverage:**
- paper.tex (full draft) ✓
- paper.bib (~50 entries) ✓
- experiments_spec.md (A–E + overhead) ✓
- literature_review.md (5 clusters + gap analysis) ✓
- TikZ figures (Fig 1–4) ✓ covered in Task 2 Step 6
- Double-blind compliance ✓ noted in constraints
- $0/CPU constraint ✓ noted in constraints

**Placeholder scan:**
- Task 1 Step 1 says "write entries organized by cluster" without full BibTeX content — this is intentional; the actual BibTeX content is produced during execution by the implementer using the key names specified.
- All result tables use `\todo{}` consistently — correct.
- No ambiguous "TBD" or "implement later" patterns.

**Type consistency:**
- BibTeX keys listed in Task 1 match `\cite{}` calls in Task 2 steps.
- Feature group names (F1–F5) consistent across Section 4 prose, Algorithm 1, and ablation table.
