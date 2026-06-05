# Christian Garry — Tailored CV
### Jane Street · Machine Learning Researcher (London)

christiangarry.southafrica@gmail.com · +44 79 3232 6827 · [christiangarry.com](https://christiangarry.com) · [linkedin.com/in/christian-tt-garry](https://www.linkedin.com/in/christian-tt-garry/)

**Machine Learning Researcher — stochastic control · deep learning · multi-agent RL**

---

## Profile

MSc Scientific Computing researcher (Distinction track, ~86%) working at the intersection of **deep learning, stochastic control, and quantitative finance**. My dissertation builds and debugs **deep neural solvers for a competitive market-making game**, validates them to **0.135%** against an exact benchmark, and uses **multi-agent reinforcement learning** to study how trading algorithms learn to price — finding a reproducible, statistically-significant *supra-cartel* effect. I move fluently between **model architecture, feature/transformation design, and stochastic-control theory**, and I hold the work to a high evidentiary bar: ablation batteries, multiple-comparison-corrected statistics, and a machine-checked error theory. Strong communicator — a 10-chapter dissertation plus three standalone papers.

---

## Research

**Deep BSDEs for Mean-Field Market Making — MSc Dissertation, Durham University** · *2026*
*Stochastic control × deep learning × multi-agent RL · [github.com/cgarryZA/MFG-BSDE-Equilibrium](https://github.com/cgarryZA/MFG-BSDE-Equilibrium)*

- Built **deep backward-SDE-with-jumps solvers** (PyTorch) for the Cont–Xiong dealer market-making game — pricing/quoting under inventory risk and mean-field competition — matching the exact tabular solution to **0.135% spread / 0.216% value error** and **scaling to ~5,000 agents** where grid methods are infeasible.
- **Tinkered architectures into working models:** identified, characterised (two as propositions) and fixed **three independent failure modes** that silently kill the mean-field signal in naïve networks — *generator bypass* (gradient path severed), *BatchNorm erasure* (zero-variance broadcast features), and *DeepSets collapse* (symmetric inputs cancelling at O(1/N)). Post-fix, the learned competition factor varies 4× and optimal quotes shift 2×; validated by a **26-experiment ablation battery**.
- **Trading-strategy learning dynamics:** trained **20 seeded decentralised-MADDPG** agents on the same game → mean spread **1.866** (95% CI [1.654, 2.072]), above both Nash (1.515) and cartel (1.593); **t=3.22, p=0.0022**, Cohen's d=0.72, surviving Bonferroni & Holm. The game has a unique competitive equilibrium with no supra-cartel fixed point — so the effect is a property of the **learning algorithm**, not the market (direct algorithmic-collusion / surveillance relevance).
- Developed an **a-posteriori error-certification theory** for deep-BSDE solvers — a computable residual estimator two-sidedly equivalent to the true error, with no spurious minima and a certified training-stop rule — and **machine-checked its core in Lean 4 / Mathlib** (~36k LOC, axiom-clean; 4-wave adversarial audit caught a real soundness bug).
- Built the **reproducible-research infrastructure**: a CI-guarded data→paper pipeline (build fails if any cited number drifts from its source), a GPU overnight job queue, and remote automated job submission.

**Silicon Carbide JFET CPU — MEng Dissertation, Durham University** · *2023–24 · 84%*
- Designed and simulated a 4-bit CPU in SiC JFET logic and built the **full verification toolchain** (C++ compiler, assembler, Python automation, emulator parity + waveform-to-state reconstruction) — instruction-level validation against a behavioural reference. Engineering rigour from device models to verified system behaviour.

---

## Education

**MSc Scientific Computing & Data Analysis (AI for Engineering) — Durham University** · *Sep 2025 – Sep 2026*
- Tracking **Distinction** (~86% across completed modules). Standout marks: **95%** Performance Modelling/Vectorisation/GPU, **94%** Machine Learning & Statistics, **~89%** in both Advanced Bayesian ML modules.
- Coverage directly relevant to ML research on large datasets: **Bayesian inference** (MCMC, variational methods, Gaussian processes), **deep learning** (CNNs, Transformers, diffusion, LoRA), **convex optimisation** (duality, KKT) applied to estimation & SVMs, **random forests/boosting**, and **GPU/HPC performance engineering** (roofline, AVX-512, CUDA, LIKWID).
- Python, C, R; reproducible, tested workflows.

**Mathematics modules (NetMath) — University of Illinois Urbana-Champaign** · *2026*
- Credit-bearing, exam-assessed proof-based mathematics taken alongside the MSc: **MATH 314** Introduction to Higher Mathematics (in progress, current average 100%) and **MATH 447** Real Analysis (upcoming) — sequences and convergence, metric spaces, compactness, and Riemann integration. Deepens the analytic foundations under the stochastic-control and ML theory.

**MEng Electronic Engineering — Durham University** · *2020–2024 · Upper Second-Class Honours (2:1)*

---

## Experience

**Graduate Communications Engineer — Siemens PLC** · *Sep 2024 – Present*
- Designed and built a **Retrieval-Augmented Generation platform from scratch in Python** (local LLMs via Ollama + Qdrant vector search) over large protocol specs and source trees — **cutting engineer time-to-answer by >90%**, with an emphasis on transparent, reproducible behaviour.
- Implemented **C/C++ communication components** (TCP/IP, serial) for digital-twin simulation, streaming data between simulated systems and PC tooling.

---

## Technical Skills

**ML / modelling:** deep learning (PyTorch, FBSNN/deep-BSDE, CNNs/Transformers), architecture & feature debugging, multi-agent RL (MADDPG), Bayesian inference (MCMC, Gaussian processes), random forests/boosting, hypothesis testing with multiple-comparison correction, bootstrap CIs.
**Stochastic / quant:** BSDEs/BSDEJs, McKean–Vlasov & mean-field games, HJB↔BSDE stochastic control, Monte-Carlo, market microstructure / optimal market making, inventory risk.
**Engineering:** Python, C++, C, R; GPU/CUDA, HPC (roofline, vectorisation, Slurm); Git/CI, reproducible-research pipelines; Lean 4 / Mathlib (formal verification).

---

<!--
TAILORING NOTES (not part of the CV — delete before sending)
Role: Jane Street ML Researcher — wants people who build models/strategies/systems that price & trade,
analyse large datasets, tinker with architectures/features/hyperparameters for robust inferences, and
communicate well.
LED WITH: the dissertation (deep ML for a market-making/pricing game = their exact domain) and
specifically the architecture-failure-mode work (matches "tinkering with model architectures... robust
inferences") + the multi-agent-RL trading-strategy study.
PULLED: solver accuracy/scaling, RL + statistical rigour, GPU/HPC (large datasets), Siemens RAG/C++.
SOFT-PEDALLED: Lean (kept to one rigour bullet), Professional Skills strand, the EV/hydrogen MEng
projects (omitted), market-microstructure jargon kept light since the *ML depth* is the headline.
HONEST SCOPE preserved: solver numbers are empirical validations vs an exact benchmark (not theorems);
"machine-checked/axiom-clean" = Lean maths only; Nash uniqueness is basin-level; the collusion result
is statistical (20 seeds, corrected). Don't over-claim these in interview — the rigour is the selling point.
-->
