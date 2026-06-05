---
cv: true
id: msc-sci-comp-2025
title: MSc Scientific Computing & Data Analysis (AI for Engineering)
date: 2025-09-01
type: education
section: Education
institution: Durham University
location: Durham, United Kingdom
period: Sep 2025 – Present
links.linkedin:
links.github:
links.education: https://www.durham.ac.uk/study/courses/scientific-computing-and-data-analysis-artificial-intelligence-for-engineering-g5t809/
cover: assets\durham_university_logo.jpeg
crosslinks:
  - id: dissertation-mfg-bsde-2026
    label: Dissertation — Deep BSDEs for Mean-Field Market Making
tags: [MSc, Durham, Scientific Computing, AI, Machine Learning, Bayesian, HPC, GPU, Deep Learning, Optimisation, Education]
---

### Head

### MSc Scientific Computing & Data Analysis (AI for Engineering) — Durham University
*Sep 2025 – Present (expected Sep 2026) | Studied concurrently with full-time Siemens role*

A specialisation MSc (G5T809) spanning **machine learning and Bayesian statistics, convex optimisation, numerical methods, and high-performance / GPU computing**, applied to engineering problems. Tracking at **Distinction** standard — current weighted average **~86%** across completed modules, including **95%** in GPU/performance engineering and **94%** in machine learning & statistics. The **60-credit dissertation** develops deep BSDE solvers for mean-field market making (see the dedicated entry).

### Body

**Dissertation (60 credits, in progress)**
- **Deep BSDEs for Mean-Field Market Making** — supervised by Dr Chunrong Feng (Mathematics). Deep backward-SDE-with-jumps solvers for the Cont–Xiong dealer game (validated to 0.135% spread error, scaled to ~5,000 agents), an a-posteriori certification theory machine-checked in Lean 4, and a multi-agent-RL study of tacit collusion. *Fully written up in its own [dissertation entry](entry.html?id=dissertation-mfg-bsde-2026).*

**Completed modules — marks**
- Performance Modelling, Vectorisation & GPU Programming — **95%**
- Introduction to Machine Learning & Statistics — **94%** (Data Analysis 98 / ML 90)
- Advanced Statistics & ML: Regression & Classification — **89.5%**
- Advanced Statistical & ML: Foundations & Unsupervised Learning — **89%**
- Professional Skills — **76%**
- Introduction to Scientific & High-Performance Computing — **72%**
- *In progress:* Optimisation & Control for AI (exam), Deep Learning for Engineering (portfolio), MISCADA dissertation.

**What each module covered (AI for Engineering stream, 180 credits)**

- **Performance Modelling, Vectorisation & GPU Programming (95%)** — performance engineering on a *measure → model → optimise* basis: the **roofline model**, SSE/AVX/AVX-512/FMA vectorisation, cache blocking & tiling, GEMM micro-kernels, **LIKWID** profiling with hardware counters, **CUDA / OpenMP / SYCL** GPU programming, and Nsight. Coursework: optimising a real C++ kernel on Durham's Hamilton-8 cluster (Slurm).

- **Introduction to Machine Learning & Statistics (94%)** — statistical data analysis (error propagation, χ² fitting, least squares, Gaussian/Poisson, Chauvenet's criterion, curvature/error matrices) and supervised ML (perceptron, logistic regression, SVMs, neural networks, PCA, k-NN, ROC, bias–variance) in Python (NumPy/pandas/SciPy/scikit-learn). Assessed by an exam; included a task critically evaluating **AI-generated fitting code for overfitting and hallucination**.

- **Advanced Statistics & ML: Regression & Classification (89.5%)** — **Gaussian processes** (hand-coded squared-exponential kernel, `DiceKriging`), Bayesian linear regression with JAGS/MCMC, regularisation (LASSO/PCR), kernel/spline/GAM smoothing; classification through LDA/QDA, CART, **random forests, boosting**, and **deep neural nets** (Keras MLP→CNN on MNIST). Summative: a high-dimensional **gene-expression survival regression** (p≈7,400) in R.

- **Advanced Statistical & ML: Foundations & Unsupervised Learning (89%)** — first-principles **Bayesian inference** (conjugate priors, decision theory, **Monte-Carlo & MCMC**, variational methods, simulated annealing, hierarchical/empirical Bayes, graphical models) and **unsupervised learning** (GMMs via EM, KDE, k-means/medoids, mean-shift, PCA, autoencoders). R + Jupyter with full derivations.

- **Optimisation & Control for AI (exam pending)** — a Boyd-style **convex-optimisation** course: convex sets & functions, LP/QP/SOCP/SDP, **Lagrangian duality, KKT conditions and Slater's condition**, applied to **ridge/LASSO/total-variation fitting, maximum-likelihood estimation and max-margin SVMs**, plus an Optimal-Power-Flow application (SDP/SOCP relaxations). Tooling in MATLAB/CVX.

- **Deep Learning for Engineering (portfolio in progress)** — Keras 3 / TensorFlow: CNNs, **Grad-CAM**, U-Net & SAM **image segmentation**, object detection, transfer learning (MobileNetV2/ResNet50); then the **Transformer/attention**, **LoRA** fine-tuning, and **VAE/diffusion** generation. Portfolio: **U-Net concrete-crack segmentation** (IoU + Grad-CAM) and either **RoBERTa/Gemma fine-tuning** on maintenance logs or a **conditional 1-D diffusion model for synthetic vibration signals**.

- **Introduction to Scientific & High-Performance Computing (72%)** — numerical simulation of physical systems (SHM, chaos, random walks/diffusion, percolation, the Ising model) in Python, and parallel HPC in **C** on the Hamilton cluster — Amdahl/Gustafson scaling, **OpenMP** and **MPI** (point-to-point, collectives, hybrid). Coursework on reaction–diffusion systems.

- **Professional Skills (76%)** — collaborative software practice: Git/PR workflow, Make/CMake, **TDD** (googletest/pytest), **GitHub Actions CI**; project management (Scrum, WBS, critical-path Gantt); data ethics (ACM Code, EU AI Act, algorithmic fairness); and structured innovation (Design Thinking, Lean Startup).

**Technical focus carried through the programme**
- Bayesian inference & probabilistic modelling (MCMC, variational methods, Gaussian processes)
- Convex optimisation (duality, KKT) and its application to estimation & ML
- Deep learning for engineering, including physics/simulation-informed models
- Stochastic methods — BSDEs and Monte-Carlo for quantitative/derivative pricing
- HPC performance engineering: vectorisation and GPU acceleration of data-intensive code
- Reproducible, tested workflows (Python, C, R, Git/CI)

---

### Short CV Snippet (LaTeX)

```latex
\begin{twocolentry}
  {Durham, United Kingdom}
  \textbf{MSc Scientific Computing \& Data Analysis (AI for Engineering)}
\end{twocolentry}

\begin{twocolentry}
  {Sep 2025~--~Exp. Sep 2026}
  \textbf{Durham University}
\end{twocolentry}

\vspace{0.10 cm}
\begin{onecolentry}
  \begin{highlights}
    \item Tracking Distinction --- average \textasciitilde86\% (95\% performance/GPU, 94\% machine learning \& statistics).
    \item \textbf{Dissertation:} Deep BSDEs for mean-field market making (Cont--Xiong), with Lean-verified error certification.
    \item \textbf{Focus:} Bayesian inference, convex optimisation, deep learning, HPC/GPU. Python, C, R.
  \end{highlights}
\end{onecolentry}
```
