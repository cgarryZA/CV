#!/usr/bin/env python3
import re
import json
from datetime import datetime
from pathlib import Path

# --- Paths ---
ROOT = Path(__file__).resolve().parent
ENTRIES_DIR = ROOT / "entries"
HEADER_JSON = ROOT / "header.json"
OUTPUT_TEX  = ROOT / "cv.tex"
OUTPUT_PDF  = ROOT / "cv.pdf"

# --- Sections & order ---
SECTION_ORDER = [
    ("education",      "Education"),
    ("experience",     "Experience"),
    ("research",       "Projects \\& Research"),
    ("certifications", "Certifications"),
    ("leadership",     "Leadership, Activities \\& Interests"),
    ("skills",         "Key Skills")
]

ENTRY_SPACED_SECTIONS = {"education", "experience", "research"}
ENTRY_SPACER = r"\vspace{0.10 cm}"

FRONT_MATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.S | re.M)
LATEX_BLOCK_RE  = re.compile(r"```latex\s*(.*?)\s*```", re.S | re.I)

_MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5, "jun": 6, "jul": 7,
    "aug": 8, "sep": 9, "sept": 9,
    "oct": 10, "nov": 11, "dec": 12,
}

def _parse_front_matter(text: str):
    m = FRONT_MATTER_RE.match(text)
    meta, body = {}, text
    if m:
        body = text[m.end():]
        for raw in m.group(1).splitlines():
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

def _parse_date(meta: dict):
    d = (meta.get("date") or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(d[:len(fmt)], fmt)
        except Exception:
            pass

    period = (meta.get("period") or "").replace("–", "-").replace("—", "-")
    if period:
        left = period.split("-", 1)[0].strip()
        parts = left.replace(",", " ").split()
        if len(parts) >= 2 and parts[0].lower() in _MONTHS:
            year = next((p for p in parts if p.isdigit() and len(p) == 4), None)
            if year:
                return datetime(int(year), _MONTHS[parts[0].lower()], 1)

    return datetime(1900, 1, 1)

def _truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}

def _should_include_in_cv(meta: dict) -> bool:
    if _truthy(meta.get("cv")):
        return True
    if _truthy(meta.get("cv_include")) or _truthy(meta.get("include_in_cv")):
        return True
    publish = (meta.get("publish") or "").lower()
    return "cv" in {p.strip() for p in publish.replace(";", ",").split(",")}

# === PREAMBLE — UNCHANGED ===
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

\ifPDFTeX{}
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

\raggedright{}
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
    \onecolentry{}
    \def\secondColumn{#2}
    \setcolumnwidth{\fill, 4.5 cm}
    \begin{paracol}{2}
}{
    \switchcolumn{} \raggedleft{} \secondColumn{}
    \end{paracol}
    \endonecolentry{}
}
\newenvironment{threecolentry}[3][]{
    \onecolentry{}
    \def\thirdColumn{#3}
    \setcolumnwidth{, \fill, 4.5 cm}
    \begin{paracol}{3}
    {\raggedright{} #2} \switchcolumn{}
}{
    \switchcolumn{} \raggedleft{} \thirdColumn{}
    \end{paracol}
    \endonecolentry{}
}
\newenvironment{header}{
    \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1.5}
}{
    \par\kern\topsep{}
}
\newcommand{\placelastupdatedtext}{%
  \AddToShipoutPictureFG*{%
    \put(\LenToUnit{\paperwidth-2 cm-0 cm+0.05cm},\LenToUnit{\paperheight-1.0 cm})
    {\vtop{{\null}\makebox[0pt][c]{
        \small\color{gray}\textit{Last updated in September 2024}\hspace{\widthof{Last updated in September 2024}}
    }}}%
  }%
}
\let\hrefWithoutArrow\href{}

\begin{document}
    \newcommand{\AND}{\unskip{}
        \cleaders\copy\ANDbox\hskip\wd\ANDbox{}
        \ignorespaces{}
    }
    \newsavebox\ANDbox{}
    \sbox\ANDbox{$|$}

    \begin{header}
    {\fontsize{20pt}{24pt}\selectfont \textbf{Christian Garry}}\\[3pt]

    \vspace{5 pt}

    % --- Row 1: tagline (single line) ---
    \noindent\makebox[\textwidth][c]{%
        \small
        MSc Scientific Computing~\textbar{}~Probability · Statistics · Optimisation~\textbar{}~C++/Python
    }\\[2pt]

    % --- Row 2: contacts (single line) ---
    \noindent\makebox[\textwidth][c]{%
        \small
        \mbox{\hrefWithoutArrow{mailto:christiangarry.southafrica@gmail.com}{christiangarry.southafrica@gmail.com}}~\textbar{}~\mbox{\hrefWithoutArrow{tel:+447932326827}{+44 79 3232 6827}}~\textbar{}~\mbox{\hrefWithoutArrow{https://christiangarry.com}{christiangarry.com}}~\textbar{}~\mbox{\hrefWithoutArrow{https://www.linkedin.com/in/christian-tt-garry/}{linkedin.com/in/christian-tt-garry}}
    }
    \end{header}

    \vspace{-0.35 cm}
"""

def main():
    header = json.loads(HEADER_JSON.read_text(encoding="utf-8"))

    contacts = r"~\textbar{}~".join(
        rf"\mbox{{\hrefWithoutArrow{{{c['href']}}}{{{c['value']}}}}}"
        for c in header["contacts"]
    )

    preamble = (
        PREAMBLE_LATEX
        .replace("<<NAME>>", header["name"])
        .replace("<<HEADLINE>>", header["headline"])
        .replace("<<CONTACTS>>", contacts)
    )

    sections = {k: [] for k, _ in SECTION_ORDER}

    for md in sorted(ENTRIES_DIR.glob("*.md")):
        meta, body = _parse_front_matter(md.read_text(encoding="utf-8", errors="ignore"))
        typ = (meta.get("cv_section") or meta.get("section") or "").lower()
        if not typ or not _should_include_in_cv(meta):
            continue
        sections.setdefault(typ, []).append({
            "latex": _extract_latex(body),
            "date": _parse_date(meta)
        })

    out = ["% === Auto-generated by build_cv.py ===", preamble]

    for key, title in SECTION_ORDER:
        items = sections.get(key, [])
        if not items:
            continue
        out.append(f"\n\\section*{{{title}}}\n")
        items.sort(key=lambda x: -x["date"].toordinal())
        for i, it in enumerate(items):
            out.append(it["latex"])
            if key in ENTRY_SPACED_SECTIONS and i < len(items) - 1:
                out.append(ENTRY_SPACER)

    out.append("\n\\end{document}\n")
    OUTPUT_TEX.write_text("\n".join(out), encoding="utf-8")
    print("[OK] Wrote cv.tex")

    # ===============================
    # CLEANUP (ONLY AFTER PDF EXISTS)
    # ===============================
    #if OUTPUT_PDF.exists():
    #    for ext in (
    #        ".aux",
    #        ".log",
    #        ".fls",
    #        ".fdb_latexmk",
    #        ".synctex.gz",
    #        ".tex",
    #    ):
    #        p = ROOT / f"cv{ext}"
    #        if p.exists():
    #            p.unlink()
    #            print(f"[CLEAN] Deleted {p.name}")

if __name__ == "__main__":
    main()
