#!/usr/bin/env python3
import re
import json
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

    html = re.sub(r"(?<!\\)%.*", "", html)

    html = html.replace("\\%", "%")
    html = html.replace("\\&", "&")
    html = html.replace("\\@", "")
    html = html.replace("\\textbar{}", "|")
    html = html.replace("~--~", " – ")
    html = html.replace("--", "–")
    html = html.replace("~", " ")

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
        f'<a href="{c["href"]}">{latex_inline_to_html(c["value"])}</a>'
        for c in header["contacts"]
    )

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

    for key in sections:
        sections[key].sort(key=lambda x: x["date"], reverse=True)

    out = [f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{name} — CV</title>
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

.spacer {{ height: 8px; }}
</style>
</head>
<body>

<div class="header">
  <h1>{name}</h1>
  <div class="tagline">{headline}</div>
  <div class="contacts">{contacts_html}</div>
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
