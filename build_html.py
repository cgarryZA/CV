#!/usr/bin/env python3
import re
from datetime import datetime
from pathlib import Path

# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parent
ENTRIES_DIR = ROOT / "entries"
OUTPUT_HTML = ROOT / "cv.html"

# ============================================================
# Section order — MUST MATCH build_cv.py
# ============================================================

SECTION_ORDER = [
    ("education",  "Education"),
    ("experience", "Experience"),
    ("research",   "Projects & Research"),
    ("skills",     "Key Skills"),
    ("leadership", "Leadership, Activities & Interests"),
]

# ============================================================
# Regex
# ============================================================

FRONT_MATTER_RE = re.compile(
    r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n",
    re.S | re.M
)

LATEX_BLOCK_RE = re.compile(
    r"```latex\s*(.*?)\s*```",
    re.S | re.I
)

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
    for key in ("date", "period"):
        val = meta.get(key)
        if not val:
            continue
        try:
            return datetime.strptime(val[:10], "%Y-%m-%d")
        except Exception:
            pass
    return datetime(1900, 1, 1)

# ============================================================
# LaTeX → HTML (STRICT CV DIALECT)
# ============================================================

def latex_to_html(lx: str) -> str:
    html = lx

    # -------------------------
    # Strip comments (FIXED)
    # -------------------------
    html = re.sub(r"(?<!\\)%.*", "", html)

    # -------------------------
    # Normalize LaTeX escapes
    # -------------------------
    html = html.replace("\\%", "%")
    html = html.replace("\\&", "&")
    html = html.replace("\\@", "")
    html = html.replace("\\textbar{}", "|")
    html = html.replace("~--~", " – ")
    html = html.replace("--", "–")
    html = html.replace("~", " ")

    # -------------------------
    # twocolentry → semantic entry
    # -------------------------
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

    # -------------------------
    # onecolentry
    # -------------------------
    html = re.sub(r"\\begin{onecolentry}", '<div class="onecol">', html)
    html = re.sub(r"\\end{onecolentry}", "</div>", html)

    # -------------------------
    # highlights → ul/li
    # -------------------------
    html = re.sub(r"\\begin{highlights}", "<ul>", html)
    html = re.sub(r"\\end{highlights}", "</ul>", html)
    html = re.sub(r"\\item\s*", "<li>", html)
    html = re.sub(r"(<li>.*?)(?=<li>|</ul>)", r"\1</li>", html, flags=re.S)

    # -------------------------
    # Text formatting
    # -------------------------
    html = re.sub(r"\\textbf\{(.*?)\}", r"<strong>\1</strong>", html)
    html = re.sub(r"\\textit\{(.*?)\}", r"<em>\1</em>", html)

    # -------------------------
    # Vertical spacing
    # -------------------------
    html = re.sub(r"\\vspace\{.*?\}", '<div class="spacer"></div>', html)

    # -------------------------
    # Line breaks
    # -------------------------
    html = html.replace("\\\\", "<br>")

    # Cleanup
    html = re.sub(r"\n\s*\n+", "\n", html)

    return html.strip()

# ============================================================
# Build
# ============================================================

def main():
    sections = {k: [] for k, _ in SECTION_ORDER}

    for md in sorted(ENTRIES_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        meta, body = parse_front_matter(text)

        if not should_include(meta):
            continue

        sec = (
            meta.get("cv_section")
            or meta.get("type")
            or meta.get("section")
            or ""
        ).strip().lower()

        if not sec:
            continue

        latex = extract_latex(body)
        if not latex:
            continue

        sections.setdefault(sec, []).append({
            "date": parse_date(meta),
            "html": latex_to_html(latex)
        })

    # Sort newest first
    for key in sections:
        sections[key].sort(key=lambda x: x["date"], reverse=True)

    # ========================================================
    # HTML output
    # ========================================================

    out = ["""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Christian Garry — CV</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
  max-width: 900px;
  margin: 48px auto;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  color: #111;
}

/* HEADER (PDF-like) */
.header {
  text-align: center;
  margin-bottom: 24px;
}
.header h1 {
  font-size: 32px;
  margin-bottom: 6px;
}
.header .tagline,
.header .contacts {
  font-size: 14px;
  margin-bottom: 4px;
}

/* Sections */
h2 {
  border-bottom: 1px solid #000;
  padding-bottom: 4px;
  margin-top: 28px;
  margin-bottom: 10px;
  font-size: 20px;
}

/* Entry layout */
.entry {
  margin-bottom: 4px;
}
.entry-header {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
  align-items: baseline;
}
.entry-right {
  text-align: right;
  white-space: nowrap;
  font-size: 0.95em;
}

/* Content blocks */
.onecol {
  margin-bottom: 6px;
}
ul {
  margin: 4px 0 0 18px;
  padding: 0;
}
li {
  margin-bottom: 2px;
}
.spacer {
  height: 8px;
}
</style>
</head>
<body>

<div class="header">
  <h1>Christian Garry</h1>
  <div class="tagline">
    MSc Scientific Computing | Probability · Statistics · Optimisation | C++/Python
  </div>
  <div class="contacts">
    christiangarry.southafrica@gmail.com |
    +44 79 3232 6827 |
    christiangarry.com |
    linkedin.com/in/christian-tt-garry
  </div>
</div>
"""]

    for key, title in SECTION_ORDER:
        items = sections.get(key)
        if not items:
            continue
        out.append(f"<h2>{title}</h2>")
        for it in items:
            out.append(it["html"])

    out.append("</body></html>")

    OUTPUT_HTML.write_text("\n".join(out), encoding="utf-8")
    print(f"[OK] Wrote {OUTPUT_HTML}")

# ============================================================

if __name__ == "__main__":
    main()
