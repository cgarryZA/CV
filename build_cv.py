#!/usr/bin/env python3
import re
from datetime import datetime
from pathlib import Path

# --- Paths ---
ROOT = Path(__file__).resolve().parent
ENTRIES_DIR = ROOT / "entries"          # your snippet .md files live here
OUTPUT_TEX  = ROOT / "cv.tex"           # final stitched LaTeX at repo root

# --- Sections & order ---
SECTION_ORDER = [
    ("education",  "Education"),
    ("skills",     "Key Skills"),
    ("experience", "Experience"),
    ("research",   "Projects \\& Research"),
    ("leadership", "Leadership, Activities \\& Interests"),
]

# === Insert \vspace between items only for these sections ===
ENTRY_SPACED_SECTIONS = {"education", "experience", "research"}
ENTRY_SPACER = r"\vspace{0.10 cm}"

# --- Parsers ---
FRONT_MATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.S | re.M)
LATEX_BLOCK_RE  = re.compile(r"```latex\s*(.*?)\s*```", re.S | re.I)

# Month map for 'period' like "Sep 2025 – Present"
_MONTHS = {
    "jan": 1,  "january": 1,
    "feb": 2,  "february": 2,
    "mar": 3,  "march": 3,
    "apr": 4,  "april": 4,
    "may": 5,
    "jun": 6,  "june": 6,
    "jul": 7,  "july": 7,
    "aug": 8,  "august": 8,
    "sep": 9,  "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

def _parse_front_matter(text: str):
    m = FRONT_MATTER_RE.match(text)
    meta, body = {}, text
    if m:
        fm = m.group(1)
        body = text[m.end():]
        for raw in fm.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    return meta, body

def _extract_latex(body: str) -> str:
    m = LATEX_BLOCK_RE.search(body)
    return (m.group(1).strip() if m else "").strip()

def _parse_iso_like(s: str):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m", "%Y/%m", "%Y"):
        try:
            return datetime.strptime(s[:len(fmt)], fmt)
        except Exception:
            pass
    return None

def _parse_period(meta: dict):
    period = (meta.get("period") or "").strip()
    if not period:
        return None
    period = period.replace("—", "-").replace("–", "-")
    left = period.split("-", 1)[0].strip()
    tokens = left.replace(",", " ").split()
    if not tokens:
        return None
    if len(tokens) == 1 and tokens[0].isdigit():
        try:
            return datetime(int(tokens[0]), 1, 1)
        except Exception:
            return None
    if len(tokens) >= 2:
        month_token = tokens[0].lower()
        year_token = None
        for t in tokens[1:]:
            if t.isdigit() and len(t) == 4:
                year_token = t
                break
        if month_token in _MONTHS and year_token:
            try:
                return datetime(int(year_token), _MONTHS[month_token], 1)
            except Exception:
                return None
        if tokens[0].isdigit() and len(tokens[0]) == 4:
            try:
                return datetime(int(tokens[0]), 1, 1)
            except Exception:
                return None
    return None

def _parse_date(meta: dict):
    d = (meta.get("date") or "").strip()
    dt = _parse_iso_like(d) if d else None
    if dt:
        return dt
    dt = _parse_period(meta)
    if dt:
        return dt
    return datetime(1900, 1, 1)  # platform-safe minimal

def _truthy(val) -> bool:
    if val is None:
        return False
    s = str(val).strip().lower()
    return s in {"1", "true", "yes", "y", "on"}

def _should_include_in_cv(meta: dict) -> bool:
    if _truthy(meta.get("cv")):
        return True
    if _truthy(meta.get("cv_include")) or _truthy(meta.get("include_in_cv")):
        return True
    publish = (meta.get("publish") or "").lower()
    if "cv" in {p.strip() for p in publish.replace(";", ",").split(",")}:
        return True
    return False

# === Full preamble (inlined — no \input) ===
PREAMBLE_LATEX = r"""
\documentclass[10pt, letterpaper]{article}

% Packages:
\usepackage[
    ignoreheadfoot,
    top=2 cm,
    bottom=2 cm,
    left=2 cm,
    right=2 cm,
    footskip=1.0 cm
]{geometry}
\usepackage{titlesec}
\usepackage{tabularx}
\usepackage{array}
\usepackage[dvipsnames]{xcolor}
\definecolor{primaryColor}{RGB}{0, 0, 0}
\usepackage{enumitem}
\usepackage{fontawesome5}
\usepackage{amsmath}
\usepackage[
    pdftitle={Christian Garry's CV},
    pdfauthor={Christian Garry},
    pdfcreator={LaTeX with RenderCV},
    colorlinks=true,
    urlcolor=primaryColor
]{hyperref}
\usepackage[pscoord]{eso-pic}
\usepackage{calc}
\usepackage{bookmark}
\usepackage{lastpage}
\usepackage{changepage}
\usepackage{paracol}
\usepackage{ifthen}
\usepackage{needspace}
\usepackage{iftex}

\ifPDFTeX
    \input{glyphtounicode}
    \pdfgentounicode=1
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \usepackage{lmodern}
\fi

\usepackage{charter}

\newcommand{\leadershipitem}[3]{%
  \noindent\textbf{#1} — #2 \hfill \textit{#3}\par
}

\raggedright
\AtBeginEnvironment{adjustwidth}{\partopsep0pt}
\pagestyle{empty}
\setcounter{secnumdepth}{0}
\setlength{\parindent}{0pt}
\setlength{\topskip}{0pt}
\setlength{\columnsep}{0.15cm}
\pagenumbering{gobble}

\titleformat{\section}{\needspace{4\baselineskip}\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]
\titlespacing{\section}{-1pt}{0.2 cm}{0.2 cm}

\renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$}
\newenvironment{highlights}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=0 cm + 10pt
    ]
}{
    \end{itemize}
}
\newenvironment{highlightsforbulletentries}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=10pt
    ]
}{
    \end{itemize}
}
\newenvironment{onecolentry}{
    \begin{adjustwidth}{0 cm + 0.00001 cm}{0 cm + 0.00001 cm}
}{
    \end{adjustwidth}
}
\newenvironment{twocolentry}[2][]{
    \onecolentry
    \def\secondColumn{#2}
    \setcolumnwidth{\fill, 4.5 cm}
    \begin{paracol}{2}
}{
    \switchcolumn \raggedleft \secondColumn
    \end{paracol}
    \endonecolentry
}
\newenvironment{threecolentry}[3][]{
    \onecolentry
    \def\thirdColumn{#3}
    \setcolumnwidth{, \fill, 4.5 cm}
    \begin{paracol}{3}
    {\raggedright #2} \switchcolumn
}{
    \switchcolumn \raggedleft \thirdColumn
    \end{paracol}
    \endonecolentry
}
\newenvironment{header}{
    \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1.5}
}{
    \par\kern\topsep
}
\newcommand{\placelastupdatedtext}{%
  \AddToShipoutPictureFG*{%
    \put(
        \LenToUnit{\paperwidth-2 cm-0 cm+0.05cm},
        \LenToUnit{\paperheight-1.0 cm}
    ){\vtop{{\null}\makebox[0pt][c]{
        \small\color{gray}\textit{Last updated in September 2024}\hspace{\widthof{Last updated in September 2024}}
    }}}%
  }%
}
\let\hrefWithoutArrow\href

\begin{document}
    \newcommand{\AND}{\unskip
        \cleaders\copy\ANDbox\hskip\wd\ANDbox
        \ignorespaces
    }
    \newsavebox\ANDbox
    \sbox\ANDbox{$|$}

    \begin{header}
    {\fontsize{20pt}{24pt}\selectfont \textbf{Christian Garry}}\\[3pt]

    \vspace{5 pt}

    % --- Row 1: tagline (single line) ---
    \noindent\makebox[\textwidth][c]{%
        \small
        MSc Scientific Computing ~\textbar{}~ Probability · Statistics · Optimisation ~\textbar{}~ C++/Python ~\textbar{}~ Quantitative Methods
    }\\[2pt]

    % --- Row 2: contacts (single line) ---
    \noindent\makebox[\textwidth][c]{%
        \small
        \mbox{\hrefWithoutArrow{mailto:christiangarry.southafrica@gmail.com}{christiangarry.southafrica@gmail.com}}
        ~\textbar{}~
        \mbox{\hrefWithoutArrow{tel:+447932326827}{+44 79 3232 6827}}
        ~\textbar{}~
        \mbox{\hrefWithoutArrow{https://christiangarry.com}{christiangarry.com}}
        ~\textbar{}~
        \mbox{\hrefWithoutArrow{https://www.linkedin.com/in/christian-tt-garry/}{linkedin.com/in/christian-tt-garry}}
    }
    \end{header}

    \vspace{-0.35 cm}
"""

def main():
    if not ENTRIES_DIR.exists():
        raise SystemExit(f"[ERROR] entries folder not found: {ENTRIES_DIR}")

    sections = {key: [] for key, _ in SECTION_ORDER}

    # Collect items
    for md in sorted(ENTRIES_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        meta, body = _parse_front_matter(text)

        typ = ((meta.get("cv_section") or meta.get("type") or meta.get("section") or "")
               .strip().lower())
        if not typ:
            continue
        if not _should_include_in_cv(meta):
            continue

        latex = _extract_latex(body) or f"%% NOTE: No LaTeX snippet found in {md.name}\n"

        try:
            cv_order = int(meta.get("cv_order", ""))
        except Exception:
            cv_order = None

        sections.setdefault(typ, []).append({
            "path": md,
            "meta": meta,
            "latex": latex,
            "date": _parse_date(meta),
            "cv_order": cv_order,
        })

    # Sort items per section: (cv_order asc, date desc)
    for key in list(sections.keys()):
        items = sections.get(key) or []
        if not items:
            continue

        def sort_key(item):
            ord_key = item["cv_order"] if item["cv_order"] is not None else 10**9
            return (ord_key, -item["date"].toordinal())

        items.sort(key=sort_key)
        sections[key] = items

    # Stitch output (standalone)
    out = []
    out.append("% === Auto-generated by build_cv.py ===")
    out.append(PREAMBLE_LATEX.rstrip())

    for key, title in SECTION_ORDER:
        items = sections.get(key) or []
        if not items:
            continue
        out.append(f"\n\\section*{{{title}}}\n")

        # Append items; optionally insert spacer between them
        for idx, it in enumerate(items):
            out.append(it["latex"].rstrip())
            is_last = (idx == len(items) - 1)
            if (key in ENTRY_SPACED_SECTIONS) and (not is_last):
                out.append(ENTRY_SPACER)
            out.append("")  # ensure newline break

    out.append("\n\\end{document}\n")

    OUTPUT_TEX.write_text("\n".join(out), encoding="utf-8")
    print(f"[OK] Wrote {OUTPUT_TEX}")

if __name__ == "__main__":
    main()
