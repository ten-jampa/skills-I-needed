---
name: eval-pack
description: Generate a self-contained HTML evaluation pack (`eval_pack.html`) that proves completed agent work with clear verdicts, requirement checks, and concrete evidence artifacts. Use at the end of substantive tasks, when asked to "show what you built", "generate an eval pack", "summarize your work", or when work took long enough that the human needs a 5-minute visual review instead of transcript spelunking.
---

# Evaluation Pack

Create a single, scannable proof-of-work artifact: `eval_pack.html`.
By default, write it to:
`eval-packs/eval-pack-{slug}/eval_pack.html`.

## Workflow

1. Capture task context.
2. Collect evidence continuously while working.
3. Build the eval data payload.
4. Generate `eval_pack.html` with `scripts/eval_pack_generator.py`.
5. Verify that required sections are present.
6. Present the path and short verdict summary to the user.

## Required Output Sections

Ensure the generated HTML includes all of these:

1. Header: task name, timestamp, agent, duration estimate.
2. Verdict: `PASS`, `PARTIAL`, or `FAIL` plus one-line reason.
3. Executive summary: 2-3 concise sentences.
4. Requirements checklist: each requirement with pass/fail note.
5. Evidence gallery: code, terminal output, screenshots, tables, sample outputs, and file trees.
6. Test results: pass/fail/skipped counts and failure details.
7. Known issues: honest list of risks or gaps.
8. Next steps: what the human should do next.

## Evidence Collection Rules

1. Append evidence as you go; do not reconstruct at the end.
2. Prefer raw artifacts over explanations.
3. Never skip known issues.
4. Keep the page scannable; prioritize signal.
5. If evidence is missing, downgrade verdict accordingly.

## `eval_data` Contract

Create a JSON payload with this shape:

```json
{
  "task_name": "Build data ingestion pipeline",
  "timestamp": "2026-04-16 10:30 AM EST",
  "agent": "Codex CLI",
  "duration": "~25 minutes",
  "verdict": "PASS",
  "verdict_reason": "All requirements met and tests pass.",
  "summary": "2-3 sentence summary.",
  "requirements": [
    {"name": "Requirement A", "status": "pass", "note": "Evidence note"},
    {"name": "Requirement B", "status": "partial", "note": "Known limitation"}
  ],
  "evidence": [
    {"type": "code", "title": "Parser", "language": "python", "content": "def f(): pass"},
    {"type": "terminal", "title": "Test run", "content": "$ pytest -q\n12 passed"},
    {"type": "file_tree", "title": "Changed files", "content": "src/\n  main.py"},
    {"type": "image", "title": "UI screenshot", "media_type": "image/png", "data": "<base64>"},
    {"type": "table", "title": "Results", "headers": ["A", "B"], "rows": [["1", "2"]]},
    {"type": "highlight", "title": "Key finding", "content": "Important takeaway."}
  ],
  "test_results": {
    "passed": 12,
    "failed": 0,
    "skipped": 1,
    "failures": []
  },
  "known_issues": ["Issue 1"],
  "next_steps": ["Review output", "Run staging test"]
}
```

Status values accepted in `requirements[*].status`: `pass`, `partial`, `fail` (case-insensitive).

## Generator Usage

Run the bundled script:

```bash
python3 eval-pack/scripts/eval_pack_generator.py \
  --config /path/to/eval_data.json
```

Default output path pattern:
`eval-packs/eval-pack-{slug}/eval_pack.html`
where `{slug}` comes from `task_name`.

Set a custom folder/slug:

```bash
python3 eval-pack/scripts/eval_pack_generator.py \
  --config /path/to/eval_data.json \
  --output-dir artifacts/evals \
  --slug backend-smoke-test
```

Set an explicit file path (full override):

```bash
python3 eval-pack/scripts/eval_pack_generator.py \
  --config /path/to/eval_data.json \
  --output /path/to/eval_pack.html
```

Or call it from Python:

```python
# Run from the directory that contains eval_pack_generator.py
from eval_pack_generator import default_output_path, generate_eval_pack
path = default_output_path(eval_data, output_dir="eval-packs", slug=None)
generate_eval_pack(eval_data, path)
```

## Verdict Guidelines

1. `PASS`: requirements met, evidence complete, major tests passing.
2. `PARTIAL`: useful outcome with important gaps.
3. `FAIL`: core requirements not met or verification missing.

Choose honesty over optimism.

## Task-Type Focus

1. Code and pipeline tasks: code snippets, terminal runs, test outputs, file tree.
2. UI tasks: screenshots across key states and viewport sizes.
3. Research tasks: tables, highlighted findings, source links.
4. Refactors: before/after snippets plus regression tests.
5. Bug fixes: repro evidence, patch proof, non-repro verification.
