# Christian Garry — Tailored CV
### Jane Street · Quantitative Researcher (London)

christiangarry.southafrica@gmail.com · +44 79 3232 6827 · [christiangarry.com](https://christiangarry.com) · [linkedin.com/in/christian-tt-garry](https://www.linkedin.com/in/christian-tt-garry/)

**Quantitative Researcher — stochastic control · pricing models · machine learning**

---

## Profile

Quantitative-finance researcher (MSc Scientific Computing, Distinction track ~86%) who builds and validates **models, strategies, and systems for pricing and trading**. My dissertation develops **deep solvers for a competitive market-making game** — pricing and quoting under inventory risk and mean-field competition — validated to **0.135%** against an exact benchmark, and studies how **trading-strategy learning** behaves via multi-agent reinforcement learning, with a reproducible, statistically-significant finding on equilibrium vs. learned spreads. A strong Python programmer with deep grounding in **stochastic control, probability/statistics, optimisation, and time-series**, a genuine research track record (a 10-chapter dissertation + three standalone papers), and a precise, honest communication style.

---

## Research

**Deep BSDEs for Mean-Field Market Making — MSc Dissertation, Durham University** · *2026*
*Quantitative finance × stochastic control × machine learning · [github.com/cgarryZA/MFG-BSDE-Equilibrium](https://github.com/cgarryZA/MFG-BSDE-Equilibrium)*

- Built **models for pricing and quoting** in the Cont–Xiong dealer market-making game — intensity-controlled fills, inventory risk, mean-field competition — using deep backward-SDE-with-jumps solvers; **validated to 0.135% spread / 0.216% value error** against an exact benchmark and **scaled to ~5,000 agents** (mean-field rate O(1/√N) confirmed) where grid/PDE methods are infeasible.
- **Studied trading-strategy learning dynamics:** trained **20 seeded multi-agent RL (decentralised MADDPG)** agents on the same game → population mean spread **1.866** (95% CI [1.654, 2.072]), above both the competitive Nash anchor (1.515) and the cartel level (1.593); **t=3.22, p=0.0022**, Cohen's d=0.72, surviving Bonferroni & Holm correction. Established that the game has a *unique* competitive equilibrium with no supra-cartel fixed point — so the effect is a property of the **learning algorithm**, not the market (direct algorithmic-collusion / surveillance relevance: FCA, PRA, SR 11-7).
- **Feature/architecture engineering for financial-dataset models:** identified and fixed three failure modes (generator bypass, BatchNorm erasure, DeepSets collapse) that silently destroy the population/competition signal in mean-field networks; validated across a **26-experiment** battery (post-fix, learned competition factor varies 4× and optimal quotes shift 2×).
- Developed an **a-posteriori error-certification theory** (a computable estimator with two-sided guarantees and a certified stopping rule) and machine-checked its core in **Lean 4 / Mathlib** (~36k LOC, axiom-clean) — rigour that carries straight into trusting a model's numbers.
- Built **reproducible-research infrastructure**: a CI-guarded data→results pipeline (build fails if any cited number drifts), a GPU job queue, and remote automated job submission.

**Silicon Carbide JFET CPU — MEng Dissertation, Durham University** · *2023–24 · 84%*
- Built a custom 4-bit CPU and its **full verification toolchain** (compiler, assembler, automation, emulator-parity + waveform-to-state checks) — instruction-level validation against a behavioural reference. Demonstrates end-to-end engineering rigour and modelling-to-validation discipline.

---

## Education

**MSc Scientific Computing & Data Analysis (AI for Engineering) — Durham University** · *Sep 2025 – Sep 2026*
- Tracking **Distinction** (~86%). Directly relevant coursework: **Bayesian inference & statistics** (MCMC, Gaussian processes — incl. a high-dimensional gene-expression *survival regression* and **time-series / regression** modelling), **convex optimisation** (duality, KKT) applied to estimation & SVMs, **random forests/boosting & deep learning**, and **GPU/HPC performance engineering** (for large financial datasets).
- Standout marks: **95%** Performance/GPU, **94%** Machine Learning & Statistics, **~89%** in both Advanced Bayesian ML modules. Python, C, R.

**Mathematics modules (NetMath) — University of Illinois Urbana-Champaign** · *2026*
- Credit-bearing, exam-assessed proof-based mathematics taken alongside the MSc: **MATH 314** Introduction to Higher Mathematics (in progress, current average 100%) and **MATH 447** Real Analysis (upcoming) — sequences and convergence, metric spaces, compactness, and Riemann integration. Strengthens the rigorous-analysis foundations under stochastic calculus and probability.

**MEng Electronic Engineering — Durham University** · *2020–2024 · Upper Second-Class Honours (2:1)*

---

## Experience

**Graduate Communications Engineer — Siemens PLC** · *Sep 2024 – Present*
- Designed and built a **Retrieval-Augmented Generation platform from scratch in Python** (local LLMs + Qdrant vector search) over large technical corpora — **cutting engineer time-to-answer by >90%**, with transparent, reproducible behaviour.
- Implemented **C/C++ data-exchange / networking components** (TCP/IP, serial) for digital-twin simulation environments.

---

## Technical Skills

**Quantitative / stochastic:** BSDEs/BSDEJs, McKean–Vlasov & mean-field games, HJB↔BSDE stochastic control, Monte-Carlo & finite-difference numerics, market microstructure / optimal market making, inventory risk, fixed-point/equilibrium computation.
**Statistics / ML:** Bayesian inference (MCMC, Gaussian processes), time-series & regression modelling, feature engineering, random forests/boosting, deep learning (PyTorch), multi-agent RL (MADDPG), hypothesis testing with multiple-comparison correction, bootstrap CIs.
**Engineering:** Python (strong), C++, C, R; GPU/CUDA & HPC (roofline, vectorisation, Slurm); Git/CI, reproducible-research pipelines; Lean 4 / Mathlib.

---

<!--
TAILORING NOTES (delete before sending)
Role: Jane Street Quantitative Researcher — "build models, strategies, and systems for pricing and
trading"; time-series analysis, feature engineering, models for financial datasets, hyperparameter
tuning, debugging distributed training; required strong Python + math + precise communicator;
PREFERRED data-science/ML experience + PhD or research background.
RE-ANGLE vs the ML-Researcher version:
  - Lead on PRICING/TRADING MODELS + the quant-finance domain (market making, inventory risk), not on
    ML-architecture internals.
  - Foreground TIME-SERIES / REGRESSION / FEATURE-ENGINEERING (MSc survival-regression + GP/Bayesian
    modelling) to hit "time series analysis and feature engineering / models for financial datasets."
  - Foreground RESEARCH BACKGROUND (dissertation + 3 papers) to satisfy the "PhD or research background"
    preference, since you have the research depth without a PhD.
  - Multi-agent RL framed as "trading-strategy learning dynamics."
  - Architecture-failure-mode work kept but reframed as feature/signal engineering; Lean kept to a
    one-line rigour point.
HONEST SCOPE preserved (empirical validations not theorems; Lean = maths only; Nash uniqueness
basin-level; collusion result statistical). The rigour is the selling point — don't over-claim.
-->
