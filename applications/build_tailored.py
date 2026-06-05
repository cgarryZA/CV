#!/usr/bin/env python3
"""
build_tailored.py — render a tailored Markdown CV (applications/*.md) into a PDF
that matches the canonical CV's look, by reusing build_cv.py's PREAMBLE_LATEX
(charter font, section rules, highlights/onecolentry macros) and compiling with
the local MiKTeX toolchain.

Usage:
    python build_tailored.py jane-street-ml-researcher.md
Produces:
    applications/jane-street-ml-researcher.tex
    applications/jane-street-ml-researcher.pdf
"""
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../CV/applications
CV_ROOT = HERE.parent                            # .../CV
sys.path.insert(0, str(CV_ROOT))
from build_cv import PREAMBLE_LATEX               # noqa: E402

GENERIC_TAGLINE = r"MSc Scientific Computing~\textbar{}~Probability · Statistics · Optimisation~\textbar{}~C++/Python"

# ---- unicode -> latex (defensive; covers what appears in the tailored docs) ----
UNI = {
    "—": "---", "–": "--", "‑": "-", "·": r"\textperiodcentered{}",
    "×": r"$\times$", "≈": r"$\approx$", "→": r"$\rightarrow$",
    "↔": r"$\leftrightarrow$", "√": r"$\surd$", "∞": r"$\infty$",
    "≤": r"$\leq$", "≥": r"$\geq$", "≠": r"$\neq$",
    "’": "'", "‘": "'", "“": "``", "”": "''", "…": r"\ldots{}",
    "²": r"$^2$", "³": r"$^3$", "₁": r"$_1$", "₉": r"$_9$",
    "ρ": r"$\rho$", "χ": r"$\chi$", "π": r"$\pi$", "α": r"$\alpha$",
    "β": r"$\beta$", "γ": r"$\gamma$", "δ": r"$\delta$", "ε": r"$\varepsilon$",
    "→": r"$\rightarrow$", "ï": r'\"{\i}', "ô": r"\^{o}", "é": r"\'{e}",
}


def esc(text: str) -> str:
    for k, v in UNI.items():
        text = text.replace(k, v)
    text = text.replace("&", r"\&").replace("%", r"\%")
    text = text.replace("#", r"\#").replace("_", r"\_")
    text = text.replace("~", r"\textasciitilde{}")
    return text


def inline(text: str) -> str:
    """Convert markdown inline (links, bold, italic) + escape, to LaTeX."""
    links = []

    def grab(m):
        links.append((m.group(1), m.group(2)))
        return f"\x00{len(links) - 1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", grab, text)
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*(.+?)\*", r"\\textit{\1}", text)

    def back(m):
        t, u = links[int(m.group(1))]
        return rf"\href{{{u}}}{{{esc(t)}}}"

    text = re.sub("\x00(\\d+)\x00", back, text)
    return text


def convert(md: str):
    lines = md.split("\n")

    # ---- find the role tagline: first **bold** line before the first '## ' ----
    tagline = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("## "):
            break
        m = re.match(r"^\*\*(.+)\*\*$", s)
        if m:
            tagline = inline(m.group(1))
            break

    # ---- body: from first '## ' onward ----
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith("## ")), len(lines))
    body = lines[start:]

    out = []
    para, bullets = [], []
    in_comment = False

    def flush_para():
        if para:
            joined = "\\\\[2pt]\n".join(inline(p) for p in para)
            out.append("\\begin{onecolentry}\n" + joined + "\n\\end{onecolentry}")
            out.append("\\vspace{0.06 cm}")
            para.clear()

    def flush_bullets():
        if bullets:
            out.append("\\begin{onecolentry}\n\\begin{highlights}")
            for b in bullets:
                out.append("  \\item " + inline(b))
            out.append("\\end{highlights}\n\\end{onecolentry}")
            out.append("\\vspace{0.10 cm}")
            bullets.clear()

    for ln in body:
        s = ln.strip()
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--"):
            in_comment = "-->" not in s
            continue
        if not s or s == "---":
            flush_para(); flush_bullets()
            continue
        if s.startswith("## "):
            flush_para(); flush_bullets()
            out.append("\n\\section*{" + inline(s[3:].strip()) + "}\n")
            continue
        if s.startswith("- "):
            flush_para()
            bullets.append(s[2:].strip())
            continue
        # ordinary text / entry-header line
        flush_bullets()
        para.append(s)

    flush_para(); flush_bullets()
    return tagline, "\n".join(out)


def build(md_path: Path):
    md = md_path.read_text(encoding="utf-8")
    tagline, body = convert(md)

    preamble = PREAMBLE_LATEX
    if tagline:
        preamble = preamble.replace(GENERIC_TAGLINE, tagline)

    tex = preamble + "\n" + body + "\n\\end{document}\n"
    tex_path = md_path.with_suffix(".tex")
    tex_path.write_text(tex, encoding="utf-8")
    print(f"[OK] wrote {tex_path.name}")

    latexmk = shutil.which("latexmk")
    pdflatex = shutil.which("pdflatex")
    env = dict(os.environ)
    if latexmk:
        cmd = [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    else:
        cmd = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    print("[..] compiling:", " ".join(cmd))
    for _ in range(1 if latexmk else 2):
        r = subprocess.run(cmd, cwd=str(md_path.parent), env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="ignore")
    pdf_path = md_path.with_suffix(".pdf")
    if pdf_path.exists():
        print(f"[OK] built {pdf_path.name}")
        # tidy aux files
        for ext in (".aux", ".log", ".fls", ".fdb_latexmk", ".out", ".synctex.gz"):
            p = md_path.with_suffix(ext)
            if p.exists():
                p.unlink()
    else:
        print("[FAIL] no PDF produced. Tail of log:")
        print((r.stdout or "")[-3000:])
        print((r.stderr or "")[-1500:])
        sys.exit(1)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if not target:
        print("usage: python build_tailored.py <file.md>")
        sys.exit(2)
    build((HERE / target).resolve())
