#!/usr/bin/env python3
"""Generate self-contained HTML evaluation packs from JSON input."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
from pathlib import Path
from typing import Any


VERDICT_COLORS = {
    "PASS": "#2E7D32",
    "PARTIAL": "#ED6C02",
    "FAIL": "#D32F2F",
}

STATUS_META = {
    "pass": ("PASS", "#2E7D32"),
    "partial": ("PARTIAL", "#ED6C02"),
    "fail": ("FAIL", "#D32F2F"),
}

LANGUAGE_KEYWORDS = {
    "python": {
        "def",
        "class",
        "if",
        "elif",
        "else",
        "for",
        "while",
        "return",
        "import",
        "from",
        "try",
        "except",
        "with",
        "as",
        "yield",
        "async",
        "await",
        "lambda",
        "in",
        "is",
        "and",
        "or",
        "not",
        "None",
        "True",
        "False",
    },
    "javascript": {
        "function",
        "const",
        "let",
        "var",
        "if",
        "else",
        "for",
        "while",
        "return",
        "import",
        "export",
        "async",
        "await",
        "try",
        "catch",
        "finally",
        "new",
        "class",
        "extends",
        "true",
        "false",
        "null",
        "undefined",
    },
    "typescript": {
        "function",
        "const",
        "let",
        "var",
        "if",
        "else",
        "for",
        "while",
        "return",
        "import",
        "export",
        "async",
        "await",
        "try",
        "catch",
        "finally",
        "new",
        "class",
        "extends",
        "interface",
        "type",
        "implements",
        "public",
        "private",
        "protected",
        "readonly",
    },
    "bash": {
        "if",
        "then",
        "else",
        "fi",
        "for",
        "do",
        "done",
        "case",
        "esac",
        "function",
        "while",
        "in",
        "export",
        "local",
        "echo",
        "grep",
        "sed",
        "awk",
    },
}


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled-task"


def default_output_path(
    eval_data: dict[str, Any],
    output_dir: str | Path = "eval-packs",
    slug: str | None = None,
) -> Path:
    """Return default output path: output_dir/eval-pack-<slug>/eval_pack.html."""
    source = (slug or str(eval_data.get("task_name", "untitled-task"))).strip()
    pack_slug = _slugify(source)
    return Path(output_dir) / f"eval-pack-{pack_slug}" / "eval_pack.html"


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def _status_meta(status: str) -> tuple[str, str]:
    key = str(status or "").strip().lower()
    return STATUS_META.get(key, ("UNKNOWN", "#616161"))


def _highlight_code(content: str, language: str) -> str:
    lang = (language or "").strip().lower()
    tokens = LANGUAGE_KEYWORDS.get(lang, set())
    escaped = _escape(content)

    if not tokens:
        return escaped

    pattern = r"\b(" + "|".join(re.escape(token) for token in sorted(tokens)) + r")\b"
    highlighted = re.sub(pattern, r'<span class="tok-kw">\1</span>', escaped)
    highlighted = re.sub(r"\b(\d+(?:\.\d+)?)\b", r'<span class="tok-num">\1</span>', highlighted)

    if lang in {"python", "bash"}:
        highlighted = re.sub(r"(^\s*#.*$)", r'<span class="tok-cmt">\1</span>', highlighted, flags=re.M)
    if lang in {"javascript", "typescript"}:
        highlighted = re.sub(r"(//.*$)", r'<span class="tok-cmt">\1</span>', highlighted, flags=re.M)

    highlighted = re.sub(
        r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')',
        r'<span class="tok-str">\1</span>',
        highlighted,
    )
    return highlighted


def _render_code_block(content: str, language: str) -> str:
    lang_label = _escape(language or "text")
    highlighted = _highlight_code(content, language or "")
    return (
        f'<div class="code-lang">{lang_label}</div>'
        f'<pre class="code-block"><code>{highlighted}</code></pre>'
    )


def _render_list(items: list[str], empty_message: str) -> str:
    if not items:
        return f'<p class="empty">{_escape(empty_message)}</p>'
    rows = "".join(f"<li>{_escape(item)}</li>" for item in items)
    return f"<ul>{rows}</ul>"


def _render_requirements(requirements: list[dict[str, Any]]) -> str:
    if not requirements:
        return '<p class="empty">No requirements provided.</p>'

    cards = []
    for req in requirements:
        label, color = _status_meta(str(req.get("status", "")))
        name = _escape(req.get("name", "Unnamed requirement"))
        note = _escape(req.get("note", ""))
        cards.append(
            (
                '<div class="requirement-card">'
                f'<div class="status-pill" style="background:{color}">{label}</div>'
                f"<h4>{name}</h4>"
                f"<p>{note}</p>"
                "</div>"
            )
        )
    return "".join(cards)


def _render_table(headers: list[Any], rows: list[list[Any]]) -> str:
    if not headers and not rows:
        return '<p class="empty">No table data.</p>'

    head_html = ""
    if headers:
        head_cells = "".join(f"<th>{_escape(cell)}</th>" for cell in headers)
        head_html = f"<thead><tr>{head_cells}</tr></thead>"

    body_rows = []
    for row in rows or []:
        cells = "".join(f"<td>{_escape(cell)}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    body_html = f"<tbody>{''.join(body_rows)}</tbody>" if body_rows else ""
    return f'<div class="table-wrap"><table>{head_html}{body_html}</table></div>'


def _render_evidence_item(item: dict[str, Any], index: int) -> str:
    item_type = str(item.get("type", "unknown")).strip().lower()
    title = _escape(item.get("title", f"Evidence {index}"))

    body = ""
    if item_type == "code":
        body = _render_code_block(str(item.get("content", "")), str(item.get("language", "text")))
    elif item_type == "terminal":
        body = _render_code_block(str(item.get("content", "")), "bash")
    elif item_type == "file_tree":
        body = _render_code_block(str(item.get("content", "")), "text")
    elif item_type == "image":
        media_type = _escape(item.get("media_type", "image/png"))
        data = str(item.get("data", "")).strip()
        if data:
            body = (
                '<div class="image-wrap">'
                f'<img alt="{title}" src="data:{media_type};base64,{data}" />'
                "</div>"
            )
        else:
            body = '<p class="empty">Image evidence is missing base64 data.</p>'
    elif item_type == "table":
        body = _render_table(item.get("headers", []), item.get("rows", []))
    elif item_type == "highlight":
        body = f'<blockquote class="highlight">{_escape(item.get("content", ""))}</blockquote>'
    else:
        raw = json.dumps(item, indent=2, ensure_ascii=False)
        body = _render_code_block(raw, "json")

    type_label = _escape(item_type)
    return (
        '<article class="evidence-card">'
        f'<div class="evidence-head"><h4>{title}</h4><span>{type_label}</span></div>'
        f"{body}"
        "</article>"
    )


def _render_test_results(data: dict[str, Any]) -> str:
    passed = int(data.get("passed", 0) or 0)
    failed = int(data.get("failed", 0) or 0)
    skipped = int(data.get("skipped", 0) or 0)
    failures = data.get("failures", [])

    summary = (
        '<div class="test-summary">'
        f'<div><strong>{passed}</strong><span>Passed</span></div>'
        f'<div><strong>{failed}</strong><span>Failed</span></div>'
        f'<div><strong>{skipped}</strong><span>Skipped</span></div>'
        "</div>"
    )

    if not failures:
        return summary + '<p class="empty">No failing tests reported.</p>'

    rows = []
    for failure in failures:
        test_name = _escape(failure.get("test", "Unnamed test"))
        error = _escape(failure.get("error", ""))
        rows.append(f"<li><strong>{test_name}</strong><pre>{error}</pre></li>")
    return summary + f"<ul class=\"failures\">{''.join(rows)}</ul>"


def _normalize_eval_data(eval_data: dict[str, Any]) -> dict[str, Any]:
    now_label = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    verdict = str(eval_data.get("verdict", "PARTIAL")).strip().upper()
    if verdict not in VERDICT_COLORS:
        verdict = "PARTIAL"

    return {
        "task_name": str(eval_data.get("task_name", "Untitled Task")),
        "timestamp": str(eval_data.get("timestamp", now_label)),
        "agent": str(eval_data.get("agent", "Unknown Agent")),
        "duration": str(eval_data.get("duration", "Unknown")),
        "verdict": verdict,
        "verdict_reason": str(eval_data.get("verdict_reason", "No verdict reason supplied.")),
        "summary": str(eval_data.get("summary", "")),
        "requirements": list(eval_data.get("requirements", [])),
        "evidence": list(eval_data.get("evidence", [])),
        "test_results": dict(eval_data.get("test_results", {})),
        "known_issues": list(eval_data.get("known_issues", [])),
        "next_steps": list(eval_data.get("next_steps", [])),
    }


def _build_html(eval_data: dict[str, Any]) -> str:
    data = _normalize_eval_data(eval_data)
    verdict_color = VERDICT_COLORS[data["verdict"]]
    summary = _escape(data["summary"] or "No executive summary provided.")

    evidence_html = "".join(
        _render_evidence_item(item, idx + 1) for idx, item in enumerate(data["evidence"])
    ) or '<p class="empty">No evidence captured.</p>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Evaluation Pack - {_escape(data["task_name"])}</title>
  <style>
    :root {{
      --bg: #f6f7fb;
      --card: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --border: #e5e7eb;
      --accent: #0f766e;
      --code-bg: #0f172a;
      --code-text: #e2e8f0;
      --shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
      --radius: 12px;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Palatino, serif;
      color: var(--text);
      background:
        radial-gradient(circle at 10% 10%, #d1fae5 0%, transparent 28%),
        radial-gradient(circle at 90% 5%, #e0f2fe 0%, transparent 30%),
        var(--bg);
      line-height: 1.45;
    }}
    .wrap {{
      max-width: 1120px;
      margin: 28px auto;
      padding: 0 16px 40px;
      display: grid;
      gap: 16px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 18px;
    }}
    h1, h2, h3, h4 {{
      margin: 0 0 10px;
      line-height: 1.2;
    }}
    h1 {{
      font-size: 1.8rem;
    }}
    h2 {{
      font-size: 1.25rem;
      margin-bottom: 14px;
      color: #0f172a;
    }}
    .meta {{
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      margin-top: 12px;
    }}
    .meta div {{
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px;
    }}
    .meta span {{
      display: block;
      font-size: 0.8rem;
      color: var(--muted);
      margin-bottom: 2px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .verdict {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
    }}
    .verdict-pill {{
      font-weight: 700;
      color: #fff;
      padding: 8px 14px;
      border-radius: 999px;
      background: {verdict_color};
      letter-spacing: 0.03em;
    }}
    .requirements-grid {{
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }}
    .requirement-card {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      background: #fbfdff;
    }}
    .status-pill {{
      display: inline-block;
      color: #fff;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 999px;
      margin-bottom: 10px;
    }}
    .requirement-card h4 {{
      margin: 0 0 8px;
      font-size: 1rem;
    }}
    .requirement-card p {{
      margin: 0;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    .evidence-grid {{
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }}
    .evidence-card {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      background: #ffffff;
    }}
    .evidence-head {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .evidence-head span {{
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
    }}
    .code-lang {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #93c5fd;
      margin-bottom: 8px;
    }}
    .code-block {{
      margin: 0;
      padding: 12px;
      border-radius: 10px;
      overflow-x: auto;
      background: var(--code-bg);
      color: var(--code-text);
      border: 1px solid #1e293b;
      font-size: 0.86rem;
      line-height: 1.35;
    }}
    .code-block code {{
      font-family: "JetBrains Mono", "SFMono-Regular", Menlo, Consolas, monospace;
      white-space: pre;
    }}
    .tok-kw {{ color: #f472b6; font-weight: 700; }}
    .tok-num {{ color: #93c5fd; }}
    .tok-str {{ color: #86efac; }}
    .tok-cmt {{ color: #94a3b8; font-style: italic; }}
    .table-wrap {{
      overflow-x: auto;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 8px;
      text-align: left;
      font-size: 0.9rem;
    }}
    thead {{
      background: #f8fafc;
    }}
    .image-wrap {{
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
      background: #f8fafc;
    }}
    .image-wrap img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .highlight {{
      margin: 0;
      padding: 12px;
      border-left: 4px solid var(--accent);
      background: #f0fdfa;
      color: #134e4a;
      border-radius: 8px;
    }}
    .test-summary {{
      display: grid;
      grid-template-columns: repeat(3, minmax(100px, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }}
    .test-summary div {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px;
      text-align: center;
      background: #f8fafc;
    }}
    .test-summary strong {{
      display: block;
      font-size: 1.3rem;
    }}
    .test-summary span {{
      color: var(--muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .failures {{
      margin: 8px 0 0;
      padding-left: 20px;
    }}
    .failures pre {{
      margin-top: 6px;
      white-space: pre-wrap;
      background: #fff7ed;
      border: 1px solid #fed7aa;
      border-radius: 8px;
      padding: 8px;
      color: #9a3412;
      font-size: 0.84rem;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 6px;
    }}
    .empty {{
      color: var(--muted);
      margin: 0;
      font-style: italic;
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="card">
      <h1>{_escape(data["task_name"])}</h1>
      <div class="meta">
        <div><span>Timestamp</span>{_escape(data["timestamp"])}</div>
        <div><span>Agent</span>{_escape(data["agent"])}</div>
        <div><span>Duration</span>{_escape(data["duration"])}</div>
      </div>
    </section>

    <section class="card verdict">
      <div class="verdict-pill">{_escape(data["verdict"])}</div>
      <p>{_escape(data["verdict_reason"])}</p>
    </section>

    <section class="card">
      <h2>Executive Summary</h2>
      <p>{summary}</p>
    </section>

    <section class="card">
      <h2>Requirements Checklist</h2>
      <div class="requirements-grid">
        {_render_requirements(data["requirements"])}
      </div>
    </section>

    <section class="card">
      <h2>Evidence Gallery</h2>
      <div class="evidence-grid">
        {evidence_html}
      </div>
    </section>

    <section class="card">
      <h2>Test Results</h2>
      {_render_test_results(data["test_results"])}
    </section>

    <section class="card">
      <h2>Known Issues</h2>
      {_render_list(data["known_issues"], "No known issues reported.")}
    </section>

    <section class="card">
      <h2>Next Steps</h2>
      {_render_list(data["next_steps"], "No follow-up steps provided.")}
    </section>
  </main>
</body>
</html>
"""


def generate_eval_pack(eval_data: dict[str, Any], output_path: str | Path) -> Path:
    """Generate eval-pack HTML from a dictionary and write to output_path."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_build_html(eval_data), encoding="utf-8")
    return output


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a self-contained evaluation pack HTML file."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to eval_data JSON config file.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Explicit output HTML file path (overrides --output-dir/--slug).",
    )
    parser.add_argument(
        "--output-dir",
        default="eval-packs",
        help="Base directory for default output mode (default: eval-packs).",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Optional slug to use in default output mode: eval-pack-<slug>/eval_pack.html.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config_path = Path(args.config)
    if not config_path.exists():
        raise SystemExit(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        eval_data = json.load(handle)
    if not isinstance(eval_data, dict):
        raise SystemExit("Config JSON must contain a top-level object.")

    output_path = Path(args.output) if args.output else default_output_path(
        eval_data,
        output_dir=args.output_dir,
        slug=args.slug,
    )
    output = generate_eval_pack(eval_data, output_path)
    print(f"[OK] Wrote evaluation pack: {output}")


if __name__ == "__main__":
    main()
