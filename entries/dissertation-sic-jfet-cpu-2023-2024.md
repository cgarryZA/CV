---
id: dissertation-sic-jfet-cpu-2023-2024
title: Silicon Carbide JFET CPU (Master’s Dissertation)
date: 2023-10-01
type: research
section: Research
institution: Durham University
location: Durham, United Kingdom
period: Oct 2023 – Apr 2024
links.linkedin:
links.github:
links.education: ./meng-electronic-2024.md
cover: assets\durham_university_logo.jpeg
cv: true
tags: [Research, Electronics, SiC, JFET, CPU, LTspice, Compilers]

asset: assets/GARRY-CHRISTIAN-MEng-FYP.pdf

---
### Head

### Silicon Carbide JFET CPU — Master’s Dissertation  
*Extreme‑environment computing; device‑level logic to system‑level toolchain*

Built a custom **4‑bit CPU** in **LTspice** using **SiC JFET logic** targeting **high‑temperature and radiation** environments. Delivered an **end‑to‑end toolchain**: C‑like language & compiler (**C++**), assembler, and **Python** scripts to generate PWL stimuli for simulation.

### Body

**What I did**  
- Designed **NAND/NOR/XOR** JFET logic and **custom transistor‑optimised gates** (e.g., **carry‑lookahead adder** blocks).  
- Architected and simulated a **minimal 4‑bit ISA** and micro‑architecture suitable for SiC characteristics.  
- Implemented a **C‑like compiler** → assembler → PWL generator for **repeatable simulation runs** and program testing.  
- Benchmarked timing, switching energy, and noise margins under temperature/radiation assumptions.

**Impact**  
Bridges **device physics** and **computer architecture**, showcasing **numerical modelling**, **compiler construction**, and **hardware‑aware software**—useful for HL/LL stack reasoning in safety‑critical or latency‑sensitive systems.

**Final Grade**
I recieved 84% for my final report which was one of the highest in the cohort.

---

### Short CV Snippet (LaTeX)

```latex
\begin{twocolentry}
    {Durham, United Kingdom}
    \textbf{Silicon Carbide JFET CPU}
\end{twocolentry}

\begin{twocolentry}
    {Oct 2023 – Apr 2024}
    \textbf{Master's Dissertation}
\end{twocolentry}

\vspace{0.10 cm}
\begin{onecolentry}
    \begin{highlights}
        \item Built custom 4-bit CPU in LTspice from SiC JFETs for extreme temperature and radiation environments.
        \item Developed complete toolchain: C-like compiler (C++), assembler, and Python automation scripts.
    \end{highlights}
\end{onecolentry}


```
