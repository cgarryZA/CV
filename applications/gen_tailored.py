#!/usr/bin/env python3
"""
gen_tailored.py — generate the Jane Street tailored CVs as LEAN one-page PDFs
that match the canonical cv.pdf layout exactly (twocolentry right-aligned
location/dates, terse highlights), reusing build_cv.py's PREAMBLE_LATEX.

Hand-authored lean blocks (reordered + role-tuned) — NOT the verbose website md.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CV_ROOT = HERE.parent
sys.path.insert(0, str(CV_ROOT))
from build_cv import PREAMBLE_LATEX  # noqa: E402

GENERIC_TAGLINE = r"MSc Scientific Computing~\textbar{}~Probability · Statistics · Optimisation~\textbar{}~C++/Python"

# ----------------------------------------------------------------------------
# Shared lean blocks
# ----------------------------------------------------------------------------
SIC = r"""
\begin{twocolentry}
  {Durham, United Kingdom}
  \textbf{Silicon Carbide JFET CPU}
\end{twocolentry}
\begin{twocolentry}
  {Oct 2023~--~Apr 2024}
  \textbf{MEng Dissertation (84\%)}
\end{twocolentry}
\vspace{0.10 cm}
\begin{onecolentry}
  \begin{highlights}
    \item Designed and simulated a 4-bit CPU in SiC JFET logic (LTspice) for extreme-temperature/radiation computing.
    \item Built the full verification toolchain --- C++ compiler, assembler, Python automation, emulator-parity + waveform-to-state checks.
  \end{highlights}
\end{onecolentry}
"""

MSC_HEADER = r"""
\begin{twocolentry}
  {Durham, United Kingdom}
  \textbf{MSc Scientific Computing \& Data Analysis (AI for Engineering)}
\end{twocolentry}
\begin{twocolentry}
  {Sep 2025~--~Exp. Sep 2026}
  \textbf{Durham University}
\end{twocolentry}
\vspace{0.10 cm}
"""

UIUC = r"""
\begin{twocolentry}
  {Apr 2026~--~Dec 2026}
  \textbf{University of Illinois Urbana-Champaign} --- Mathematics Modules (NetMath, online)
\end{twocolentry}
\vspace{0.10 cm}
\begin{onecolentry}
  \begin{highlights}
    \item \textbf{MATH 314} Higher Mathematics \textit{(in progress, 100\%)} \& \textbf{MATH 447} Real Analysis \textit{(upcoming)} --- proof techniques, metric spaces, compactness, Riemann integration.
  \end{highlights}
\end{onecolentry}
"""

MENG = r"""
\begin{twocolentry}
  {Durham, United Kingdom}
  \textbf{MEng Electronic Engineering}
\end{twocolentry}
\begin{twocolentry}
  {Sep 2020~--~Jun 2024}
  \textbf{Durham University}
\end{twocolentry}
\vspace{0.10 cm}
\begin{onecolentry}
  \begin{highlights}
    \item Upper Second-Class Honours (2:1). Dissertation: \textit{Silicon Carbide JFET CPU} (see Research).
  \end{highlights}
\end{onecolentry}
"""

SIEMENS = r"""
\begin{twocolentry}
  {Hebburn, United Kingdom}
  \textbf{Graduate Communications Engineer}
\end{twocolentry}
\begin{twocolentry}
  {Sep 2024~--~Present}
  \textbf{Siemens PLC}
\end{twocolentry}
\vspace{0.10 cm}
\begin{onecolentry}
  \begin{highlights}
    \item Built a Python RAG platform from scratch (local LLMs, vector search) over large technical corpora --- cut engineer time-to-answer by >90\%.
    \item Implemented C/C++ communication components (TCP/IP, serial) for digital-twin simulation.
  \end{highlights}
\end{onecolentry}
"""


def section(title, *blocks):
    return f"\n\\section*{{{title}}}\n" + "\n\\vspace{0.16 cm}\n".join(blocks)


def profile(text):
    return ("\n\\begin{onecolentry}\n" + text.strip() + "\n\\end{onecolentry}\n")


# ----------------------------------------------------------------------------
# ML RESEARCHER
# ----------------------------------------------------------------------------
ML_TAGLINE = r"Machine Learning Researcher~\textbar{}~Stochastic Control · Deep Learning · Multi-Agent RL"

ML_DISS = r"""
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
    \item Built deep backward-SDE-with-jumps solvers (PyTorch) for a competitive mean-field market-making game (Cont--Xiong); matched the exact solution to 0.135\% spread error and scaled to \textasciitilde5{,}000 agents.
    \item \textbf{Tinkered architectures into working models:} diagnosed and fixed three failure modes that silently kill the mean-field signal (generator bypass, BatchNorm erasure, DeepSets collapse); validated over a 26-experiment ablation battery, with the error theory machine-checked in Lean 4 / Mathlib (\textasciitilde36k LOC).
    \item 20-seed multi-agent-RL (MADDPG) study: learned spreads reach \textbf{supra-cartel} (t=3.22, p=0.0022) --- collusion is a property of the learning dynamics, not the market equilibrium.
  \end{highlights}
\end{onecolentry}
"""

ML_MSC = MSC_HEADER + r"""
\begin{onecolentry}
  \begin{highlights}
    \item Tracking Distinction --- average \textasciitilde86\% (95\% performance/GPU, 94\% machine learning \& statistics, \textasciitilde89\% advanced Bayesian ML).
    \item \textbf{Focus:} Bayesian inference (MCMC, Gaussian processes), deep learning (CNNs, Transformers, diffusion), convex optimisation (duality, KKT), GPU/HPC. Python, C, R.
  \end{highlights}
\end{onecolentry}
"""

ML_SKILLS = r"""
\begin{onecolentry}
  \begin{highlights}
    Deep learning (PyTorch, deep-BSDE/FBSNN, CNNs/Transformers) \textbullet{} architecture \& feature debugging \textbullet{} multi-agent RL (MADDPG) \textbullet{} Bayesian inference (MCMC, Gaussian processes) \textbullet{} stochastic control (HJB$\leftrightarrow$BSDE, mean-field games) \textbullet{} hypothesis testing with multiple-comparison correction \textbullet{} GPU/CUDA \& HPC \textbullet{} Python, C++, C, R \textbullet{} Lean 4 / Mathlib
  \end{highlights}
\end{onecolentry}
"""

ML_BODY = (
    section("Research", ML_DISS, SIC)
    + section("Education", ML_MSC, UIUC, MENG)
    + section("Experience", SIEMENS)
    + section("Technical Skills", ML_SKILLS)
)

# ----------------------------------------------------------------------------
# QUANT RESEARCHER
# ----------------------------------------------------------------------------
QUANT_TAGLINE = r"Quantitative Researcher~\textbar{}~Stochastic Control · Pricing Models · Probability \& Statistics"

QUANT_DISS = r"""
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
    \item Built \textbf{models for pricing and quoting} in a competitive market-making game (Cont--Xiong) under inventory risk and mean-field competition; validated to 0.135\% spread error vs an exact benchmark and scaled to \textasciitilde5{,}000 agents.
    \item 20-seed multi-agent-RL (MADDPG) \textbf{trading-strategy} study: learned spreads exceed the cartel level (t=3.22, p=0.0022) --- an algorithmic-collusion finding with market-surveillance relevance (FCA/PRA/SR 11-7).
    \item Engineered the population/competition features naive networks suppress (three fixed failure modes, 26-experiment validation); error theory machine-checked in Lean 4 / Mathlib (\textasciitilde36k LOC).
  \end{highlights}
\end{onecolentry}
"""

QUANT_MSC = MSC_HEADER + r"""
\begin{onecolentry}
  \begin{highlights}
    \item Tracking Distinction --- average \textasciitilde86\% (95\% performance/GPU, 94\% machine learning \& statistics, \textasciitilde89\% advanced Bayesian ML).
    \item \textbf{Relevant:} Bayesian statistics (MCMC, Gaussian processes), \textbf{time-series \& regression} (incl. a high-dimensional survival regression), convex optimisation (duality, KKT), GPU/HPC. Python, C, R.
  \end{highlights}
\end{onecolentry}
"""

QUANT_SKILLS = r"""
\begin{onecolentry}
  \begin{highlights}
    Stochastic control (BSDEs/BSDEJs, McKean--Vlasov \& mean-field games, HJB$\leftrightarrow$BSDE) \textbullet{} probability \& statistics \textbullet{} time-series \& regression \textbullet{} Monte-Carlo \& finite-difference numerics \textbullet{} optimisation \textbullet{} market microstructure / optimal market making \textbullet{} multi-agent RL (MADDPG) \textbullet{} Python (strong), C++, C, R \textbullet{} GPU/HPC \textbullet{} Lean 4
  \end{highlights}
\end{onecolentry}
"""

QUANT_BODY = (
    section("Research", QUANT_DISS, SIC)
    + section("Education", QUANT_MSC, UIUC, MENG)
    + section("Experience", SIEMENS)
    + section("Technical Skills", QUANT_SKILLS)
)

ROLES = {
    "jane-street-ml-researcher": (ML_TAGLINE, ML_BODY),
    "jane-street-quant-researcher": (QUANT_TAGLINE, QUANT_BODY),
}


def build(name):
    tagline, body = ROLES[name]
    preamble = PREAMBLE_LATEX.replace(GENERIC_TAGLINE, tagline)
    tex = preamble + "\n" + body + "\n\\end{document}\n"
    tex_path = HERE / f"{name}.tex"
    tex_path.write_text(tex, encoding="utf-8")
    latexmk = shutil.which("latexmk")
    cmd = [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    r = subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    pdf = HERE / f"{name}.pdf"
    if pdf.exists():
        for ext in (".aux", ".log", ".fls", ".fdb_latexmk", ".out", ".synctex.gz"):
            p = HERE / f"{name}{ext}"
            if p.exists():
                p.unlink()
        print(f"[OK] {pdf.name}")
    else:
        print(f"[FAIL] {name}\n" + (r.stdout or "")[-2500:])
        sys.exit(1)


if __name__ == "__main__":
    targets = sys.argv[1:] or list(ROLES)
    for t in targets:
        build(t)
