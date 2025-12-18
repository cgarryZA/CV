#!/usr/bin/env python3
from __future__ import annotations

import re
import json
import html as _html
from datetime import datetime
from pathlib import Path

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parent
ENTRIES_DIR = ROOT / "entries"
HEADER_JSON = ROOT / "header.json"
OUTPUT_HTML = ROOT / "cv.html"

# ============================================================
# Section order — MUST MATCH build_cv.py
# ============================================================

SECTION_ORDER = [
    ("education",      "Education"),
    ("experience",     "Experience"),
    ("research",       "Projects & Research"),
    ("certifications", "Certifications"),
    ("leadership",     "Leadership, Activities & Interests"),
    ("skills",         "Key Skills"),
]

# ============================================================
# Regex
# ============================================================

FRONT_MATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.S | re.M)
LATEX_BLOCK_RE  = re.compile(r"```latex\s*(.*?)\s*```", re.S | re.I)

# Link macros commonly seen in your CV LaTeX
HREF_RE = re.compile(r"\\href(?:WithoutArrow)?\{(.*?)\}\{(.*?)\}", re.S)
LEADERSHIPITEM_RE = re.compile(
    r"\\leadershipitem\{(.*?)\}\{(.*?)\}\{(.*?)\}",
    re.S
)

_MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5, "jun": 6, "jul": 7,
    "aug": 8, "sep": 9, "sept": 9,
    "oct": 10, "nov": 11, "dec": 12,
}

# ============================================================
# Front matter helpers
# ============================================================

def parse_front_matter(text: str):
    meta = {}
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return meta, text

    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")

    return meta, text[m.end():]

def truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}

def should_include(meta: dict) -> bool:
    if truthy(meta.get("cv")):
        return True
    if truthy(meta.get("cv_include")) or truthy(meta.get("include_in_cv")):
        return True
    publish = (meta.get("publish") or "").lower()
    return "cv" in {p.strip() for p in publish.replace(";", ",").split(",")}

def extract_latex(body: str) -> str:
    m = LATEX_BLOCK_RE.search(body)
    return m.group(1).strip() if m else ""

def parse_date(meta: dict):
    """
    Match build_cv.py behaviour more closely:
    - Try YYYY-MM-DD, YYYY-MM, YYYY
    - If 'period' exists, try parsing left side like 'Sep 2024'
    """
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

# ============================================================
# LaTeX → HTML (STRICT CV DIALECT)
# ============================================================

def latex_to_html(lx: str) -> str:
    html = lx

    # Strip LaTeX comments (but leave escaped \%)
    html = re.sub(r"(?<!\\)%.*", "", html)

    # Basic escapes / symbols
    html = html.replace("\\%", "%")
    html = html.replace("\\&", "&")
    html = html.replace("\\@", "")
    html = html.replace("\\textbar{}", "|")
    html = html.replace("~--~", " – ")
    html = html.replace("--", "–")
    html = html.replace("~", " ")

    # Links: \href{url}{text} and \hrefWithoutArrow{url}{text}
    def _href_sub(m: re.Match) -> str:
        url = m.group(1).strip()
        txt = m.group(2).strip()
        url_esc = _html.escape(url, quote=True)
        txt_esc = _html.escape(txt)
        return f'<a href="{url_esc}">{txt_esc}</a>'
    html = HREF_RE.sub(_href_sub, html)

    # leadershipitem macro (defined in build_cv preamble)
    def _leadership_sub(m: re.Match) -> str:
        a = _html.escape(m.group(1).strip())
        b = _html.escape(m.group(2).strip())
        c = _html.escape(m.group(3).strip())
        return (
            '<div class="leadership-item">'
            f'<div class="leadership-left"><strong>{a}</strong> — {b}</div>'
            f'<div class="leadership-right"><em>{c}</em></div>'
            '</div>'
        )
    html = LEADERSHIPITEM_RE.sub(_leadership_sub, html)

    # twocolentry blocks
    html = re.sub(
        r"\\begin{twocolentry}\s*\{(.*?)\}\s*(.*?)\\end{twocolentry}",
        r"""
<div class="entry">
  <div class="entry-header">
    <div class="entry-left">\2</div>
    <div class="entry-right">\1</div>
  </div>
</div>
""",
        html,
        flags=re.S
    )

    html = re.sub(r"\\begin{onecolentry}", '<div class="onecol">', html)
    html = re.sub(r"\\end{onecolentry}", "</div>", html)

    html = re.sub(r"\\begin{highlights}", "<ul>", html)
    html = re.sub(r"\\end{highlights}", "</ul>", html)
    html = re.sub(r"\\item\s*", "<li>", html)
    html = re.sub(r"(<li>.*?)(?=<li>|</ul>)", r"\1</li>", html, flags=re.S)

    html = re.sub(r"\\textbf\{(.*?)\}", r"<strong>\1</strong>", html)
    html = re.sub(r"\\textit\{(.*?)\}", r"<em>\1</em>", html)

    html = re.sub(r"\\vspace\{.*?\}", '<div class="spacer"></div>', html)

    html = html.replace("\\\\", "<br>")
    html = re.sub(r"\n\s*\n+", "\n", html)

    return html.strip()

# ============================================================
# INLINE LaTeX NORMALISATION (FOR HEADER.JSON)
# ============================================================

def latex_inline_to_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = s.replace("\\%", "%")
    s = s.replace("\\&", "&")
    s = s.replace("\\@", "")
    s = s.replace("\\textbar{}", "|")
    s = s.replace("~", " ")
    return s.strip()

# ============================================================
# Build
# ============================================================

def main():
    header = json.loads(HEADER_JSON.read_text(encoding="utf-8"))

    name = latex_inline_to_html(header["name"])
    headline = latex_inline_to_html(header["headline"])

    contacts_html = " | ".join(
        f'<a href="{_html.escape(c["href"], quote=True)}">{_html.escape(latex_inline_to_html(c["value"]))}</a>'
        for c in header["contacts"]
    )

    sections = {k: [] for k, _ in SECTION_ORDER}

    for md in sorted(ENTRIES_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        meta, body = parse_front_matter(text)

        if not should_include(meta):
            continue

        # IMPORTANT: Match build_cv.py logic:
        # Prefer cv_section or section; only fall back to type if section isn't set.
        sec = (meta.get("cv_section") or meta.get("section") or meta.get("type") or "").strip().lower()
        if not sec:
            continue

        latex = extract_latex(body)
        if not latex:
            continue

        sections.setdefault(sec, []).append({
            "date": parse_date(meta),
            "html": latex_to_html(latex),
        })

    for key in sections:
        sections[key].sort(key=lambda x: x["date"], reverse=True)

    out = [f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{_html.escape(name)} — CV</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
@import url("https://cdn.jsdelivr.net/npm/latex.css@1.0.0/dist/latex.min.css");

body {{
  max-width: 900px;
  margin: 48px auto;
  font-family: "Latin Modern Roman", "Computer Modern Serif", "CMU Serif", serif;
  color: #111;
}}

.header {{
  text-align: center;
  margin-bottom: 24px;
}}

.header h1 {{
  font-size: 32px;
  margin-bottom: 6px;
}}

.header .tagline,
.header .contacts {{
  font-size: 14px;
  margin-bottom: 4px;
}}

/* Make header links look like plain text */
.header a,
.header a:visited,
.header a:hover,
.header a:active {{
  color: inherit;
  text-decoration: none;
}}

h2 {{
  border-bottom: 1px solid #000;
  padding-bottom: 4px;
  margin-top: 28px;
  margin-bottom: 10px;
  font-size: 20px;
}}

.entry {{ margin-bottom: 4px; }}

.entry-header {{
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
}}

.entry-right {{
  text-align: right;
  white-space: nowrap;
}}

.onecol {{ margin-bottom: 6px; }}

ul {{ margin: 4px 0 0 18px; padding: 0; }}
li {{ margin-bottom: 2px; }}

.spacer {{ height: 0px; }}

/* leadershipitem rendering */
.leadership-item {{
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
  margin-bottom: 4px;
}}
.leadership-right {{
  text-align: right;
  white-space: nowrap;
}}
</style>
</head>
<body>

<div class="header">
  <h1>{_html.escape(name)}</h1>
  <div class="tagline">{_html.escape(headline)}</div>
  <div class="contacts">{contacts_html}</div>
</div>
"""]

    for key, title in SECTION_ORDER:
        items = sections.get(key)
        if not items:
            continue
        out.append(f"<h2>{_html.escape(title)}</h2>")
        for it in items:
            out.append(it["html"])

    out.append("</body></html>")

    OUTPUT_HTML.write_text("\n".join(out), encoding="utf-8")
    print(f"[OK] Wrote {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
