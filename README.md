# CV Build System (No external dependencies)

**Your snippets live in:** `/mnt/data/CV`

Each snippet is a Markdown file with YAML front matter and a fenced LaTeX block named `Short CV Snippet (LaTeX)`, e.g.:

---
id: example
title: Example Entry
date: 2025-11-03
type: education
---

Longer Markdown description (for your website).

---

### Short CV Snippet (LaTeX)

```latex
\begin{twocolentry}
  {Durham, United Kingdom}
  \textbf{MSc Scientific Computing \& Data Analysis (AI for Engineering)}
  \textit{}
\end{twocolentry}
```
(End block.)

## Types supported
["education", "experience", "research", "skills", "leadership"]

## Build
```bash
python build_cv.py
pdflatex build/cv.tex   # or xelatex
```

## Output
- LaTeX: `/mnt/data/build/cv.tex`

## Notes
- Items are grouped by `type` and sorted by `date` (desc).
- If a snippet has no fenced ```latex block, a comment placeholder is inserted.
- Adjust section titles/order in `build_cv.py` (SECTION_ORDER).
