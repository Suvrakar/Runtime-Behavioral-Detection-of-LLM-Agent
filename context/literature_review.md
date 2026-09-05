# TRACE — Annotated Literature Review

**Paper:** Watch What It Does, Not What It Says — IEEE S&P 2027

This document is the working reference for all cited and considered papers.
Use it during writing to ensure Related Work is accurate and citations are placed correctly.

---

## How to Use This Document

- **During writing:** find the cluster for the topic you're writing about; use the "Relevance to TRACE" note to sharpen the claim you're making.
- **During citation placement:** use the BibTeX key column to drop the `\cite{}` directly.
- **During peer review:** update "Gap left" notes when reviewers point out missed work.

---

## Cluster 1: Indirect Prompt Injection — Attacks

### [greshake2023not] Greshake et al., 2023

**Full citation:** Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz. "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injections." *AISec@CCS*, 2023.

**Venue:** ACM Workshop on Artificial Intelligence and Security (AISec@CCS 2023)

**Summary:** The paper that named and formalized indirect prompt injection. The authors show that malicious text embedded in external content (web pages, documents, emails) can hijack an LLM agent by overriding its original task instructions. Demonstrates exploitation of real products including Bing Chat and GitHub Copilot.

**Relevance to TRACE:** This is the foundational paper establishing the attack class we defend against. Cite in Introduction (first mention of indirect injection) and Background §2.2.

**Gap left:** Does not propose a defense; focuses entirely on attack characterization. No evaluation of whether behavioral signals distinguish injected from benign runs.

---

### [perez2022ignore] Perez & Ribeiro, 2022

**Full citation:** Fábio Perez and Ian Ribeiro. "Ignore Previous Prompt: Attack Techniques for Language Models." *NeurIPS 2022 Workshop on Machine Learning Safety*, 2022. arXiv:2211.09527.

**Venue:** NeurIPS 2022 ML Safety Workshop

**Summary:** Introduced the term "prompt injection" and demonstrated basic direct injection (attacker controls the prompt) and indirect injection (attacker controls retrieved content). Established the attack taxonomy that subsequent work built upon.

**Relevance to TRACE:** Cite in Introduction as the original formalization of prompt injection as an attack class.

**Gap left:** Focuses on direct injection (attacker controls prompt) and simple indirect cases. No evasion analysis, no defense.

---

### [liu2023prompt] Liu et al., 2023

**Full citation:** Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, Yang Liu. "Prompt Injection Attack Against LLM-Integrated Applications." arXiv:2306.05499, 2023.

**Venue:** arXiv (pre-print; widely cited)

**Summary:** Systematic taxonomy of prompt injection attacks: goal hijacking, prompt leaking, jailbreaking, and combined attacks. Evaluates 7 real-world applications and shows high attack success rates. Introduces the notion of "naive" vs. "escape" injections.

**Relevance to TRACE:** Cite in Background §2.2 as the systematic taxonomy. Useful for justifying our attack cell design (overt attacks correspond to "naive" injections).

**Gap left:** No defense proposed. No analysis of behavioral signals that attacks leave. No evasion analysis.

---

### [zhan2024injectagent] Zhan et al., 2024

**Full citation:** Qiusi Zhan, Zhixiang Liang, Zifan Ying, Daniel Kang. "InjectAgent: Benchmarking Indirect Prompt Injections in Tool-Calling LLM Agents." *Findings of ACL 2024*. arXiv:2403.02691.

**Venue:** ACL 2024 Findings

**Summary:** A benchmark of 1,054 test cases across 17 tools for evaluating indirect prompt injection in tool-calling agents. Tests GPT-4 and Claude-2 and shows high vulnerability. Releases the InjectAgent dataset publicly.

**Relevance to TRACE:** Used as a source of injection keywords for our static scanner baseline. Cite in Experimental Setup when describing the static scanner deny-list.

**Gap left:** Evaluates model vulnerability, not defenses. No behavioral analysis of what the agent does when injected.

---

### [yi2023benchmarking] Yi et al., 2023

**Full citation:** Jingwei Yi, Yueqi Xie, Bin Zhu, Keegan Hines, Emre Kiciman, Guangzhong Sun, Xing Xie, Fangzhao Wu. "Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models." arXiv:2312.14197, 2023.

**Venue:** arXiv (pre-print)

**Summary:** Benchmarks attacks and defenses including keyword detection, paraphrase detection, and LLM-judge screens. Shows that position-aware injections (moving the payload to attention-privileged positions) evade text-level defenses. Proposes the LLM-judge screen as a defense and evaluates it.

**Relevance to TRACE:** Critical for two reasons: (1) introduces the evasive injection variant we use in our injection-evasive cell; (2) provides the LLM-judge defense we use as a baseline. Cite in Background §2.2 (evasive variants) and Experimental Setup §5.3 (baseline protocol).

**Gap left:** Shows LLM-judge helps against overt attacks but struggles with evasive ones. Does not propose behavioral detection as an alternative.

---

### [branch2022evaluating] Branch et al., 2022

**Full citation:** Hezekiah J. Branch et al. "Evaluating the Susceptibility of Pre-Trained Language Models via Handcrafted Adversarial Examples." arXiv:2209.02128, 2022.

**Venue:** arXiv

**Summary:** Early work on adversarial text examples for LLMs; covers instruction injection via handcrafted examples.

**Relevance to TRACE:** Background citation for early adversarial prompt work. Not a primary citation; use only if needed to establish historical context.

**Gap left:** Pre-agent era; no tool use or multi-step reasoning.

---

## Cluster 2: Agent Benchmarks

### [debenedetti2024agentdojo] Debenedetti et al., 2024

**Full citation:** Edoardo Debenedetti, Jie Zhang, Mislav Balunovic, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr. "AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents." *NeurIPS 2024*. arXiv:2406.13352.

**Venue:** NeurIPS 2024

**Summary:** A comprehensive benchmark with 97 tasks and 629 prompt injections across multiple agent personas (travel agent, bank assistant, etc.). Evaluates both attack success rates and defense effectiveness. Includes dynamic task environments that change between runs, making it harder for defenses to overfit.

**Relevance to TRACE:** Primary evaluation benchmark for injection attacks. Cite throughout: Introduction (our evaluation benchmark), Background §2.2 (injection benchmarks), Experimental Setup §5.2 (attack corpus source), and Results §6 (experiments A and B).

**Gap left:** Provides the benchmark but does not propose behavioral detection. Defense evaluation is limited to input-level defenses.

---

### [ruan2024identifying] Ruan et al., 2023

**Full citation:** Yangjun Ruan et al. "Identifying the Risks of LM Agents with an LM-Emulated Sandbox." arXiv:2309.15817, 2023.

**Venue:** arXiv / ICLR 2024

**Summary:** Proposes a sandbox environment (ToolEmu) where tool execution is emulated by an LLM rather than actually executed, enabling safe risk assessment of agent behaviors. Identifies risk categories including data exfiltration and destructive actions.

**Relevance to TRACE:** Validates our threat model's action categories (exfiltration, privilege escalation, destructive tool use). Cite in Threat Model §3 when justifying attacker goal categories.

**Gap left:** Focuses on risk assessment/simulation, not detection of attacks during actual execution.

---

## Cluster 3: Skill / Tool / MCP Poisoning

### [shi2024badagent] Shi et al., 2024

**Full citation:** Yifei Wang, Zongyu Lin, Yuansheng Xu, Weizhi Wang, Thanh Nguyen. "BadAgent: Inserting and Activating Backdoor Attacks in LLM Agents." arXiv:2406.03007, 2024.

**Note:** Verify author list before camera-ready — confirm on arXiv.

**Venue:** arXiv 2024

**Summary:** Demonstrates that an agent's tool set can be backdoored by poisoning the fine-tuning data or the tool definitions. A trigger phrase in the user's request activates a malicious action injected into the tool. Tested on ReAct-style agents.

**Relevance to TRACE:** Used as a source of poisoning attack instances and for the static scanner deny-list. Cite in Background §2.2 (tool poisoning), Experimental Setup §5.3 (baseline protocol).

**Gap left:** Proposes and demonstrates the attack; no defense. The trigger is visible in the skill definition (overt case). No analysis of whether behavioral signals differ from benign runs.

---

### [yang2024watch] Yang et al., 2024

**Full citation:** Xianjun Yang, Xiao Wang, Qi Zhang, Linda Petzold. "Watch Out for Your Agents! Investigating Backdoor Threats to LLM-Based Agents." arXiv:2402.11208, 2024.

**Venue:** arXiv 2024

**Summary:** Broader investigation of backdoor threats to LLM agents, covering both fine-tuning-based and tool-description-based poisoning. Shows that backdoors can be inserted without significantly affecting benign performance, making them hard to detect via functional testing.

**Relevance to TRACE:** Motivates the payload-less skill variant (our poisoning-evasive cell): the tool description is clean, but behavior is malicious. Cite in Background §2.2 and Related Work §8.

**Gap left:** No behavioral detection approach. Notes that functional testing fails — but does not explore runtime trace analysis.

---

### [cohen2024comes] Cohen et al., 2024

**Full citation:** Stav Cohen, Ron Bitton, Ben Nassi. "Here Comes the AI Worm: Unleashing Zero-click Worms that Target Generative AI Applications." arXiv:2403.02817, 2024.

**Venue:** arXiv 2024

**Summary:** Demonstrates that a poisoned generative AI agent can propagate malicious instructions to other agents in a multi-agent pipeline (an "AI worm"), exfiltrating data across multiple systems without user interaction.

**Relevance to TRACE:** Motivates the urgency of behavioral detection — if an agent is hijacked, it can contaminate downstream agents. Cite in Background §2.2 (tool poisoning) and Introduction (motivating urgency).

**Gap left:** Shows propagation is possible; no defense proposed. TRACE could detect propagation by observing unexpected cross-agent communication patterns.

---

## Cluster 4: Text-Level Defenses

### [hines2024spotlighting] Hines et al., 2024

**Full citation:** Keegan Hines, Gary Lopez, Matthew Hall, Federico Zarfati, Yonatan Zunger, Emre Kiciman. "Defending Against Indirect Prompt Injection Attacks with Spotlighting." arXiv:2403.14720, 2024.

**Venue:** arXiv 2024

**Summary:** Proposes "spotlighting" — marking retrieved content with a special delimiter token (e.g., `<RETRIEVED>...</RETRIEVED>`) to help the model distinguish data from instructions. Shows significant reduction in injection success rates without large accuracy loss on benign tasks.

**Relevance to TRACE:** Represents the state-of-the-art in text-level defense at time of writing. Our claim is not that spotlighting is ineffective, but that it can be bypassed by evasive injections and does nothing for skill poisoning (where the threat is in runtime behavior, not prompt text). Cite in Background §2.3 (text-level defenses) and Related Work §8.

**Gap left:** Only addresses injection (not poisoning). Requires modifying the agent's prompt templates; does not generalize to all frameworks. Does not address payload-less skill threats. Performance on evasive attacks not evaluated.

---

### [inan2023llama] Inan et al., 2023

**Full citation:** Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa. "Llama Guard: LLM-Based Input-Output Safeguard for Human-AI Conversations." arXiv:2312.06674, 2023.

**Venue:** arXiv 2023 (Meta AI technical report)

**Summary:** Presents Llama Guard, a fine-tuned LLM-based classifier for safety policy enforcement on inputs and outputs. Trained on human-annotated safety categories. Used widely as a "guard model" in production systems.

**Relevance to TRACE:** Used directly as our guard model baseline. Llama Guard classifies raw text of retrieved content. Cite in Experimental Setup §5.3 when describing the guard model baseline.

**Gap left:** Designed for policy violations in human-AI conversation, not for prompt injection in agent-tool pipelines. Not trained on injection-specific data. Does not observe tool call behavior.

---

### [wallace2019universal] Wallace et al., 2019

**Full citation:** Eric Wallace, Shi Feng, Nikhil Kandpal, Matt Gardner, Sameer Singh. "Universal Adversarial Triggers for Attacking and Analyzing NLP." *EMNLP-IJCNLP 2019*, pp. 2153–2162.

**Venue:** EMNLP 2019

**Summary:** Shows that short, universal sequences of tokens can be prepended to any input to consistently trigger specific undesirable model behaviors. Foundational work establishing that NLP models are vulnerable to adversarial text manipulation.

**Relevance to TRACE:** Background context for the adversarial text manipulation literature that prompt injection builds on. Not a primary citation for this paper; include only if needed to establish the research lineage.

**Gap left:** Pre-LLM-agent era; no tool calling or multi-step reasoning. Universal triggers are a different attack surface than injection.

---

### [armstrong2022red] Armstrong et al., 2022

**Full citation:** Sam Armstrong, Liane Lovitt, Amanda Askell, et al. (Anthropic). "Red-teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned." arXiv:2209.07858, 2022.

**Venue:** arXiv 2022

**Summary:** Describes Anthropic's red-teaming methodology for identifying harmful model behaviors through adversarial testing. Discusses scaling of red-teaming effort and types of failures found.

**Relevance to TRACE:** Background for red-teaming as a defense methodology. TRACE is complementary to red-teaming (red-teaming identifies failure modes before deployment; TRACE detects them at runtime).

**Gap left:** Focuses on pre-deployment evaluation, not runtime detection.

---

## Cluster 5: Agent Architecture Foundations

### [yao2023react] Yao et al., 2023

**Full citation:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023*. arXiv:2210.03629.

**Venue:** ICLR 2023

**Summary:** Introduces the ReAct framework, which interleaves chain-of-thought reasoning and action calls in a unified loop. The agent reasons about what to do, takes an action (calls a tool), observes the result, and repeats. Demonstrates strong performance on HotpotQA, FEVER, and ALFWorld.

**Relevance to TRACE:** The agent framework we instantiate. The "trajectory" concept in TRACE is directly grounded in ReAct's (thought, action, observation) tuples. Cite in Introduction (agent frameworks), Background §2.1 (agent architecture), and Experimental Setup §5.1.

**Gap left:** No security analysis. The paper does not discuss what happens when the retrieved observation contains malicious instructions.

---

### [schick2023toolformer] Schick et al., 2023

**Full citation:** Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom. "Toolformer: Language Models Can Teach Themselves to Use Tools." *NeurIPS 2023*.

**Venue:** NeurIPS 2023

**Summary:** Proposes Toolformer, which trains language models to call external APIs (calculator, search engine, calendar) by self-supervised learning on how and when to insert API calls into text. Demonstrates that models can learn tool use without explicit supervision.

**Relevance to TRACE:** Foundational paper for LLM tool use. Cite in Introduction and Background §2.1 to establish the tool-use paradigm. The TRACE telemetry model generalizes to any tool-calling paradigm, not just ReAct.

**Gap left:** Training-time approach; no runtime security analysis.

---

### [wang2024survey] Wang et al., 2024

**Full citation:** Lei Wang, Chen Ma, Xueyang Feng, et al. "A Survey on Large Language Model Based Autonomous Agents." *Frontiers of Computer Science* 18(6):186345, 2024. DOI: 10.1007/s11704-024-40231-1.

**Venue:** Frontiers of Computer Science (journal)

**Summary:** Comprehensive survey of LLM agent architectures, covering planning, memory, tool use, and multi-agent systems. Discusses the growing deployment of agents in production settings.

**Relevance to TRACE:** Cite in Introduction to establish the growth and importance of LLM agents; background for the "autonomy makes them a high-value attack surface" claim. Also cite in Background §2.1.

**Gap left:** Survey of capabilities, not of security. Security discussion is limited to a brief subsection.

---

### [wei2022chain] Wei et al., 2022

**Full citation:** Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*.

**Venue:** NeurIPS 2022

**Summary:** Demonstrates that prompting LLMs to produce intermediate reasoning steps ("chain of thought") dramatically improves performance on multi-step reasoning tasks. Foundational for the reasoning traces in ReAct.

**Relevance to TRACE:** Background context for why agents produce multi-step trajectories. Not a primary citation; cite only if needed to ground the concept of reasoning traces.

**Gap left:** Reasoning capability, not security.

---

### [wang2023voyager] Wang et al., 2023

**Full citation:** Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar. "Voyager: An Open-Ended Embodied Agent with Large Language Models." arXiv:2305.16291, 2023.

**Venue:** arXiv 2023

**Summary:** Presents Voyager, an LLM-powered Minecraft agent that writes and executes code as skills, storing them in a skill library. Shows that agents can learn and accumulate skills over time in an open-ended environment.

**Relevance to TRACE:** Example of skill-accumulating agents, motivating the skill poisoning attack surface. Cite in Background §2.2 when motivating why skill libraries are a target.

**Gap left:** No security analysis of the skill library.

---

### [shen2023hugginggpt] Shen et al., 2023

**Full citation:** Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, Yueting Zhuang. "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face." arXiv:2303.17580, 2023.

**Venue:** arXiv 2023

**Summary:** Uses ChatGPT as a controller to orchestrate specialized AI models (from Hugging Face) for complex multi-modal tasks. The controller selects, calls, and chains models as tools.

**Relevance to TRACE:** Background example of multi-model tool-calling agents. Cite in Background §2.1 as an example of heterogeneous tool ecosystems that expand the poisoning attack surface.

**Gap left:** No security analysis.

---

## Cluster 6: Behavioral Detection Analogs

### [forrest1996sense] Forrest et al., 1996

**Full citation:** Stephanie Forrest, Steven A. Hofmeyr, Anil Somayaji, Thomas A. Longstaff. "A Sense of Self for Unix Processes." *IEEE Symposium on Security and Privacy 1996*, pp. 120–128. DOI: 10.1109/SECPRI.1996.502675.

**Venue:** IEEE S&P 1996

**Summary:** Foundational paper for behavioral intrusion detection. Shows that the system calls a Unix process makes during normal execution form a stable, characteristic signature. Anomalous processes (those that have been compromised) produce system call sequences that deviate from this signature. Introduces the "sense of self" metaphor for process identity.

**Relevance to TRACE:** The direct intellectual ancestor of TRACE. The core insight — that behavioral sequences are a stable, anomaly-detectable signature of normal operation — applies to LLM agent tool calls just as it does to Unix system calls. Cite prominently in Related Work §8 (behavioral detection analogs) and possibly in Introduction when stating the intellectual lineage.

**Gap left:** Designed for OS-level processes, not AI agents. The threat model and action space are different. TRACE adapts the insight to a new domain with a new detector design.

---

### [kolbitsch2009effective] Kolbitsch et al., 2009

**Full citation:** Clemens Kolbitsch, Paolo Milani Comparetti, Christopher Kruegel, Engin Kirda, Xiaoyong Zhou, XiaoFeng Wang. "Effective and Efficient Malware Detection at End Hosts." *USENIX Security 2009*, pp. 351–366.

**Venue:** USENIX Security 2009

**Summary:** Malware detection by analyzing runtime API call sequences rather than static binary signatures. Extracts "behavior graphs" from API call traces and uses graph similarity to classify new samples. Shows high detection rates with low false positives.

**Relevance to TRACE:** Shows that the behavioral detection approach (analyze runtime call sequences) scales to malware classification with high accuracy and low FPR — exactly the regime we claim TRACE operates in. Cite in Related Work §8.

**Gap left:** Designed for Windows malware; static binary analysis as a baseline (signature detection). The analog to TRACE's static scanner baseline.

---

### [rieck2011automatic] Rieck et al., 2011

**Full citation:** Konrad Rieck, Philipp Trinius, Carsten Willems, Thorsten Holz. "Automatic Analysis of Malware Behavior Using Machine Learning." *Journal of Computer Security* 19(4):639–668, 2011. DOI: 10.3233/JCS-2010-0410.

**Venue:** Journal of Computer Security

**Summary:** Uses machine learning (SVM over behavior report features) to classify malware into families and detect novel variants. Demonstrates that ML classifiers over behavioral features outperform signature-based detection on novel malware.

**Relevance to TRACE:** Provides the ML-over-behavior-features template that TRACE applies to LLM agents. The feature engineering approach in TRACE (n-grams over tool calls, argument anomalies) is analogous to their behavior report feature extraction. Cite in Related Work §8.

**Gap left:** Binary executables, not LLM agents. No notion of "task intent" against which behavior is measured (TRACE's F4 feature).

---

### [sekar2001fast] Sekar et al., 2001

**Full citation:** R. Sekar, M. Bendre, D. Dhurjati, P. Bollineni. "A Fast Automaton-Based Method for Detecting Anomalous Program Behaviors." *IEEE S&P 2001*, pp. 144–155.

**Venue:** IEEE S&P 2001

**Summary:** Proposes a finite-state automaton model of normal system call sequences, enabling fast anomaly detection. Addresses the scalability limitation of Forrest et al.'s sliding-window approach.

**Relevance to TRACE:** Additional background for the behavioral detection lineage. Not a primary citation; use only if the paper needs to show depth of the behavioral detection tradition.

**Gap left:** OS-level; no LLM analog.

---

## Gap Analysis

### What Each Cluster Leaves Open (and How TRACE Fills It)

**Cluster 1 — Injection attacks:**
All papers characterize attacks and demonstrate vulnerability. None proposes behavioral detection. None measures overdefense (the cost of defense to legitimate users). TRACE fills the detection gap and provides the first overdefense curve.

**Cluster 2 — Benchmarks:**
AgentDojo and InjectAgent provide evaluation infrastructure. Neither proposes a defense. Neither evaluates evasive attacks against behavioral signals. TRACE fills the evasion-resistant defense gap using these benchmarks as evaluation corpora.

**Cluster 3 — Poisoning:**
All papers demonstrate attacks; none proposes a detection mechanism that operates at runtime on behavioral traces. The "payload-less skill" variant (yang2024watch) explicitly notes that static scanning and functional testing fail — but does not propose the behavioral alternative. TRACE directly addresses this gap.

**Cluster 4 — Text-level defenses:**
Spotlighting, guard models, and LLM-judge are the current state of the art. Each operates pre-execution on text. Each is shown (by yi2023benchmarking) to degrade on evasive attacks. TRACE is explicitly positioned as a complementary post-execution layer that catches what text inspection misses.

**Cluster 5 — Agent architecture:**
Establishes the tool-use paradigm that TRACE monitors. No security analysis in any of these papers. The ReAct trajectory format is the input format TRACE consumes.

**Cluster 6 — Behavioral detection analogs:**
The intellectual lineage is strong (Forrest 1996 → Kolbitsch 2009 → Rieck 2011). But these papers address static binary malware or OS processes. None addresses the LLM agent domain. The domain adaptation required for TRACE is non-trivial: (1) the notion of "task intent" (F4) has no analog in malware detection; (2) the attack surface includes multi-step reasoning traces rather than simple call sequences; (3) the attacker can influence the agent's reasoning (not just code execution). TRACE's contribution is the domain mapping, the feature design (especially F3 and F4), and the overdefense quantification methodology.

---

## Papers to Read Before Submission

Papers that may have appeared after the knowledge cutoff and must be checked:

- [ ] Any 2025–2026 papers on MCP server security (search "MCP server prompt injection 2025")
- [ ] Any 2025–2026 papers on LLM agent behavioral monitoring
- [ ] USENIX Security 2025 and IEEE S&P 2025 proceedings — check for behavioral agent defense papers
- [ ] NeurIPS 2024/2025 Agent Security workshop proceedings
- [ ] Check for papers directly citing Greshake 2023 that propose behavioral defenses (Google Scholar "cited by")

If a prior paper does behavioral agent defense: read it immediately and either (a) differentiate TRACE clearly or (b) re-scope the contribution.

---

## Citation Cross-Reference

| BibTeX key | Used in paper section(s) |
|---|---|
| greshake2023not | §1 Intro, §2.2 Background |
| perez2022ignore | §1 Intro |
| liu2023prompt | §2.2 Background |
| zhan2024injectagent | §2.2 Background, §5.3 Baselines |
| yi2023benchmarking | §2.2 Background (evasive), §5.3 Baselines |
| branch2022evaluating | (optional background) |
| debenedetti2024agentdojo | §1 Intro, §2.2 Background, §5.2 Corpus, §6 Results |
| ruan2024identifying | §3 Threat Model |
| shi2024badagent | §2.2 Background, §5.3 Baselines |
| yang2024watch | §2.2 Background, §8 Related Work |
| cohen2024comes | §2.2 Background, §1 Intro |
| hines2024spotlighting | §2.3 Text defenses, §8 Related Work |
| inan2023llama | §5.3 Baselines |
| wallace2019universal | (optional background) |
| armstrong2022red | (optional background) |
| yao2023react | §1 Intro, §2.1 Background, §5.1 Setup |
| schick2023toolformer | §2.1 Background |
| wang2024survey | §1 Intro, §2.1 Background |
| wei2022chain | (optional background) |
| wang2023voyager | §2.2 Background (skill libraries) |
| shen2023hugginggpt | §2.1 Background |
| forrest1996sense | §8 Related Work |
| kolbitsch2009effective | §8 Related Work |
| rieck2011automatic | §8 Related Work |
| sekar2001fast | (optional; related work depth) |
| ke2017lightgbm | §4.3 Classifier, §5.4 Implementation |
| pedregosa2011scikit | §5.4 Implementation |
| chen2016xgboost | (optional; mention as alternative) |
| guo2024survey | (optional; agent survey) |
| openai2023gpt4 | (optional; generator model background) |
