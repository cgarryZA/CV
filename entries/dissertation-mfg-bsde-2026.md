---
cv: true
id: dissertation-mfg-bsde-2026
title: Deep BSDEs for Mean-Field Market Making (MSc Dissertation)
date: 2025-10-01
type: research
section: Research
institution: Durham University
location: Durham, United Kingdom
period: Oct 2025 – Sept 2026
links.github: https://github.com/cgarryZA/MFG-BSDE-Equilibrium
cover: assets\durham_university_logo.jpeg
crosslinks:
  - id: msc-sci-comp-2025
    label: MSc Scientific Computing & Data Analysis (AI for Engineering)
tags: [Research, Quantitative Finance, BSDE, Mean-Field Games, Deep Learning, Reinforcement Learning, Stochastic Control, Lean, Formal Verification, Market Making]
---

### Head

### Deep BSDEs for Mean-Field Market Making — MSc Dissertation
*Stochastic control × deep learning × multi-agent RL × formal verification | Durham University, report Sep 2026*
*Supervised by Dr Chunrong Feng (Mathematics).*

Built and validated **deep backward-SDE-with-jumps solvers** for a competitive **mean-field market-making game** (the Cont–Xiong 2024 dealer model), validated to **0.135% spread error** against an exact benchmark and scaled to **~5,000 agents**. Alongside it: an **a-posteriori certification theory** (a computable error estimator with provable two-sided guarantees, machine-checked in **Lean 4 / Mathlib**, ~36k LOC), and a **20-seed multi-agent-RL study** showing that learning algorithms drift to spreads **above the cartel level** — i.e. "tacit collusion" is a property of the *learning dynamics*, not the market equilibrium. A finding with direct algorithmic-collusion / market-surveillance implications.

### Body

**The problem**
A market maker quotes bid/ask and earns the spread while bearing **inventory risk** and facing **competition**. Cont & Xiong (2024) model this as a stochastic game: each dealer controls fill *intensities* (a pure-jump control problem), inventory mean-reverts under a quadratic penalty, and competition couples dealers through the *distribution* of quotes — a **mean-field game**. The same game can end at the competitive **Nash** equilibrium, a wider **cartel/Pareto** outcome, or — under learning — **tacit collusion**. Solving, validating and quantifying these at arbitrary numbers of agents is the motivating question. It matters because (i) deep BSDEs are the practical route to high-dimensional stochastic control where PDE/grid methods hit the curse of dimensionality, and (ii) algorithmic collusion is a live regulatory concern (FCA, PRA, the Fed's SR 11-7).

**What I built**

- **A four-rung BSDEJ "ladder" for the dealer game** — finite-N HJB Nash system → its exact finite-N backward-SDE-with-jumps reformulation → the McKean–Vlasov N→∞ mean-field limit → a common-noise extension, each with verification and HJB↔BSDEJ equivalence theorems. *(The machinery is standard Carmona–Delarue; the unified pure-jump dealer-game application is the new part.)*

- **A validated neural Bellman solver** — value iteration on the Bellman residual with a fictitious-play outer loop, matching the exact tabular solution to **0.135% spread / 0.216% value-function error at N=2** (0.0001% in a boundary-patched direct-value formulation) and **scaling to N≈5,000** where the tabular method is infeasible (mean-field rate O(1/√N) confirmed).

- **Architectural diagnostics for mean-field deep-BSDE networks** *(load-bearing)* — identified, characterised (two as propositions) and fixed **three independent failure modes** that silently suppress the mean-field signal: **generator bypass** (law embedding never reaches the generator), **BatchNorm erasure** (broadcast population features have zero batch variance), and **DeepSets collapse** (mean-pooling cancels symmetric inputs at O(1/N)). After fixing all three, the learned competition factor varies 4× and optimal quotes shift 2×; the effect vanishes if any one mode remains — a transferable lesson for conditional/mean-field deep nets, validated by a 26-experiment battery.

- **Separating equilibrium discovery from learning-algorithm collusion** *(load-bearing)* — the deep-BSDE Nash solver finds the **unique symmetric Nash** from every seed in the tested basin (triangulated by three orthogonal experiments; local contraction ρ≈0.11). Training **20 seeded decentralised-MADDPG runs** on the *same* game yields a mean spread of **1.866** (95% CI [1.654, 2.072]) — above both the Nash anchor (1.515) and the **cartel level (1.593)**, with **13/20 seeds supra-cartel** (t₁₉=3.22, **p=0.0022**, d=0.72, surviving Bonferroni & Holm). Since the game has a unique competitive equilibrium and no supra-cartel fixed point, the collusion is a property of the *learning algorithm*, not the market.

**Companion theory — a-posteriori certification of deep-BSDE solvers**
A standalone strand (three short papers + Lean) extending the Reisinger–Stockinger–Zhang Brownian a-posteriori theory to **jumps**: a **computable residual estimator** two-sidedly equivalent to the true error (`c·Eπ ≤ Dπ ≤ C·Eπ`) — so a solver's error is bounded *without knowing the exact solution* — with **no spurious zero**, **architecture-agnostic consistency**, **dimension-free constants**, and a **certified training-stop rule**. A **certification taxonomy** proves the natural "value-BSDE" market-making formulation is structurally outside the certifiable class while an **adjoint** reformulation restores it.

**Formal verification (Lean 4 / Mathlib)**
A **~36,400-line, ~45-headline-theorem** formalisation with an axiom-clean core: discrete BSDEJ existence, the mean-field equilibrium closure on a genuine law-valued type, the a-posteriori two-term error bound, and the market-making no-go/repair theorems — under a disciplined PROVEN / conditional / cited-axiom taxonomy and a **4-wave adversarial self-audit** that caught (and fixed) a genuine soundness bug.

**Research infrastructure I built**
An **anti-staleness results pipeline** (committed result JSONs → LaTeX macros/tables via one generator, with a **CI guard** that fails the build if any paper number drifts from its data source); a **GPU overnight job queue/runner** with auto-retry; and **remote job submission** (push a spec → self-hosted GitHub Actions runner appends it under a lock). Per-result provenance SHAs, seed control, a commit-history logbook.

**Skills demonstrated**
Stochastic analysis (BSDEs/BSDEJs, McKean–Vlasov, propagation of chaos, mean-field games) · stochastic control (HJB↔BSDE, intensity control, fixed-point equilibria) · deep learning (deep-BSDE/FBSNN in PyTorch, conditional/mean-field architecture debugging) · multi-agent RL (MADDPG, Nash vs Pareto vs collusion) · quantitative finance (market microstructure, optimal market making, inventory risk; FCA/PRA/SR 11-7 framing) · formal methods (Lean 4 / Mathlib, adversarial proof auditing) · numerical methods & statistics (Monte-Carlo, multiple-comparison correction, bootstrap CIs) · research software engineering (CI-guarded data→paper pipeline, GPU orchestration, reproducible provenance).

---

### Short CV Snippet (LaTeX)

```latex
\begin{twocolentry}
    {Durham, United Kingdom}
    \textbf{Deep BSDEs for Mean-Field Market Making}
\end{twocolentry}

\begin{twocolentry}
    {2026~--~MSc Dissertation}
    \textbf{Durham University}
\end{twocolentry}

\vspace{0.10 cm}
\begin{onecolentry}
    \begin{highlights}
        \item Built deep backward-SDE-with-jumps solvers for a competitive mean-field market-making game (Cont--Xiong), validated to 0.135\% spread error vs an exact benchmark and scaled to \textasciitilde5{,}000 agents.
        \item Showed via a 20-seed multi-agent-RL study (MADDPG) that learning algorithms reach \textbf{supra-cartel} spreads (t=3.22, p=0.0022) --- tacit collusion is a property of the learning dynamics, not the market equilibrium.
        \item Developed an a-posteriori error-certification theory for deep-BSDE solvers and machine-checked its core in Lean 4 / Mathlib (\textasciitilde36k LOC, axiom-clean).
    \end{highlights}
\end{onecolentry}
```
