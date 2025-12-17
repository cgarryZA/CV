# CV Snippet Manager

A **single-source CV system** where each experience, project, or role is written once as a Markdown entry and automatically rendered as:

- 📄 **A traditional CV PDF**
- 🌐 **A clean static HTML CV**
- 🧠 **A “Living CV” website**; this repo is designed to complement the Living CV project found below

This avoids duplicated CVs, stale PDFs, and hand-edited versions drifting out of sync.

---

Use the template branch to start your own CV

```bash
git clone -b template https://github.com/cgarryZA/CV.git my-cv
```
---
---

## Live Links

- **Website:** https://christiangarry.com  
- **Living CV (site repo):** https://github.com/cgarryZA/ChristianGarryLivingCV  

---

## Repository Structure

```
.
├── entries/                 # Individual CV entries (Markdown)
├── assets/                  # Images, logos, and shared media
├── header.json              # Name, headline, and contact links
├── build_cv.py              # Builds cv.tex → cv.pdf
├── build_html.py            # Builds standalone cv.html
├── .github/
│   └── workflows/
│       └── build-cv.yaml    # GitHub Actions CI pipeline
├── cv.pdf                   # Generated PDF output
├── cv.html                  # Generated HTML output
└── README.md

```

---

## Philosophy

Each **CV item is a first-class object**:

- Written once
- Machine-readable
- Human-readable
- Rendered consistently across PDF, HTML, and website

Markdown is the *source of truth*.

---

## Writing a CV Entry

All CV items live in `entries/` as Markdown files.

### Minimal example

```yaml
---
title: Graduate Communications Engineer
section: experience
period: Sep 2024 – Present
cv: true
cover: assets/siemens_logo.jpeg
---
```

```md
### Head

Graduate communications engineer focused on C++ networking systems and
Python-based engineering tooling in industrial environments.

### Body

Worked on TCP/IP and serial communication stacks, internal tooling,
and a retrieval-augmented documentation system using local LLMs.
```

---

## Front Matter (YAML)

| Field        | Purpose |
|--------------|--------|
| `title`      | Display title (used in blog cards) |
| `section`    | CV section (`education`, `experience`, `research`, etc.) |
| `period`     | Displayed date range |
| `date`       | Optional sortable fallback |
| `cv: true`   | **Required** to include in PDF/HTML CV |
| `cover`      | Optional image for Living CV cards |
| `id`         | Optional stable URL identifier |
| `publish`    | Optional list (e.g. `cv, blog`) |

If `cv: true` is **missing**, the entry will **not** appear in the PDF or HTML CV.

---

## Head vs Body

Each entry is split conceptually:

### Head
- Short, sharp summary
- Used as teaser text on the Living CV site
- Think “one-sentance abstract”

### Body
- Longer explanation
- Appears when expanded on the Living CV site
- Ignored by the PDF CV

---

## LaTeX CV Snippet

Each entry can optionally include a LaTeX block:

```latex
```latex
\begin{twocolentry}{Sep 2024 -- Present}
\textbf{Graduate Communications Engineer} \\
Siemens PLC
\end{twocolentry}

\begin{onecolentry}
\begin{highlights}
  \item Built C++ TCP/IP systems
  \item Developed Python engineering tools
\end{highlights}
\end{onecolentry}
```

This block is:

- Injected **directly** into the LaTeX CV
- Converted automatically to HTML for `cv.html`
- Ignored by the blog view

---

## Header Configuration (`header.json`)

Controls the CV header for **PDF and HTML**:

```json
{
  "name": "Christian Garry",
  "headline": "MSc Scientific Computing~\textbar{}~Probability · Statistics · Optimisation~\textbar{}~C++/Python",
  "contacts": [
    { "href": "mailto:...", "value": "email" },
    { "href": "tel:...", "value": "phone" },
    { "href": "https://...", "value": "website" },
    { "href": "https://...", "value": "linkedin" }
  ]
}
```

- LaTeX escapes are supported
- Automatically normalised for HTML
- Links are clickable but styled as plain text

---

## Build Scripts

### `build_cv.py`
- Reads `entries/*.md`
- Extracts LaTeX blocks
- Injects into LaTeX template
- Outputs `cv.pdf`
- Cleans auxiliary files automatically

### `build_html.py`
- Converts LaTeX blocks to semantic HTML
- Applies LaTeX-style typography
- Outputs standalone `cv.html`

---

## Living CV Website

The website:

- Fetches `cv.html` directly from this repo
- Injects it inline (no iframe)
- Provides:
  - Blog-style cards
  - Cover images
  - Teasers from entry heads
  - Deep links to full entries
  - PDF download button

---

## Assets

Images can be referenced as:

- `assets/logo.png` (repo-root)
- `./image.png` (entry-relative)
- Full external URLs

They are resolved automatically for both site and GitHub.

---

## Running Locally

```bash
python build_cv.py
python build_html.py
```

Outputs:
- `cv.pdf`
- `cv.html`

No database. No framework. No build system beyond Python.

---

## Design Goals

- **Single source of truth**
- **No duplicated CVs**
- **PDF-first but web-native**
- **Quant / research / engineering friendly**
- **Git-backed and reviewable**

---

## License

Personal CV system.  
Content © Christian Garry.
