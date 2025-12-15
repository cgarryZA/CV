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
tags: [Research, Electronics, SiC, JFET, CPU, LTspice, Compilers, Verification]
asset: assets/GARRY-CHRISTIAN-MEng-FYP.pdf
---

### Head

### Silicon Carbide JFET CPU — Master’s Dissertation  
*Extreme-environment computing; device-level logic to system-level verification*

Designed and validated a custom **4-bit microprocessor** in **LTspice** using **Silicon Carbide (SiC) JFET logic**, targeting **high-temperature and radiation-tolerant** computing. Delivered a **complete end-to-end toolchain**—from device-level gates to compiler, assembler, and simulation infrastructure—enabling instruction-level verification against a behavioural reference.

### Body

**What I built**
- Designed SiC **NAND/NOR/XOR** logic and transistor-optimised gates, balancing device count against timing and race-condition risk.
- Architected and simulated a **4004-compatible 4-bit CPU micro-architecture**, decomposed into ALU, control logic, registers, buses, and memory interfaces.
- Implemented a **full software toolchain**: C-like language and compiler (**C++**), assembler, and **Python** scripts to generate ROM contents and PWL stimulus waveforms.
- Integrated subsystem netlists programmatically to support repeatable, large-scale simulation runs.

**Verification & validation**
- Built a **cross-validation stack**: a corrected **JavaScript emulator** as a behavioural reference and a **MATLAB waveform-to-register interpreter** to decode LTspice analog traces step-by-step.
- Demonstrated **instruction-level parity in simulation** at 100 kHz, including execution of **unmodified Intel 4004 assembly routines**.
- Fabricated and measured **SiC JFET NAND and NOR gates**, comparing experimental waveforms against simulation to validate device models and frequency response.

**Findings & limitations**
- Achieved functional parity at the architectural level; identified **storage primitives** as the dominant contributor to transistor count relative to the original 4004.
- Experimental validation is currently limited to individual gates; system-level results are simulation-backed.
- Clear future work identified: multi-stage cascades, noise margins, temperature/radiation sweeps, and more transistor-efficient memory implementations.

**Impact**
Bridges **device physics**, **computer architecture**, and **verification infrastructure**, demonstrating end-to-end engineering from transistor models to validated instruction-level behaviour—directly applicable to safety-critical, high-reliability, and research-driven hardware systems.

**Final Grade**  
Awarded **84%**, among the highest marks in the cohort.

---

### Short CV Snippet (LaTeX)

```latex
\begin{twocolentry}
    {Durham, United Kingdom}
    \textbf{Silicon Carbide JFET CPU}
\end{twocolentry}

\begin{twocolentry}
    {Oct 2023 -- Apr 2024}
    \textbf{Master's Dissertation}
\end{twocolentry}

\vspace{0.10 cm}
\begin{onecolentry}
    \begin{highlights}
        \item Designed and simulated a 4-bit SiC JFET CPU in LTspice for extreme-environment computing.
        \item Built a complete toolchain (C++ compiler, assembler, Python automation) and verified instruction-level parity via emulator and waveform analysis.
    \end{highlights}
\end{onecolentry}
