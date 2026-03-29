---
name: code-distiller
description: Collapse any complex feature into one minimal, annotated, self-contained file. Use when the user says "distill", "extract", "collapse", "minimize", "strip down", or asks to understand a feature by seeing it as a single readable file. Also triggers on "show me just the X logic" or "give me a minimal version of Y". Works with any language — infer from the codebase.
---

# Code Distiller

Collapse a feature into one minimal, fully-annotated, self-contained file.

## Inputs

The user provides one or more of:
- A feature name or description ("the upload pipeline", "the section parser")
- File paths or function names
- A vague pointer ("this part", "the logic for Y")

If the target is ambiguous, ask which entry point or behavior they mean.

## Process

### Step 1: Trace Dependencies

1. Read the target code (entry function / class / module).
2. Follow every call, import, constant, and type reference transitively.
3. Build a dependency list: functions, classes, constants, config references.
4. Stop at stdlib boundaries and external packages (note them as imports).

### Step 2: Extract Minimal Code

Copy only code paths required for the feature. Remove:
- Sibling features sharing the same file but not called
- Dead code, unused branches, defensive checks for impossible states
- Logging, metrics, telemetry unless core to the feature
- Verbose print/debug statements (replace with terse equivalents only if needed for flow control)

The output must be **functionally complete** — it should run the full feature end-to-end (modulo external services). Do NOT simplify away functionality. Fewer lines of code, not fewer capabilities.

### Step 3: Collapse to One File

**Always target a single file.** Do not split unless the user explicitly asks. Even 500+ line features stay in one file — that is the point.

- Merge all pieces in dependency order (helpers first, entry point last).
- Inline trivially small helpers (<5 lines) at their call site.
- Remove ceremony: docstrings restating the obvious, decorative comment blocks, redundant type aliases.
- Compress verbose patterns (collapse repetitive if/elif to dicts, deduplicate near-identical code).
- Keep fewest lines possible while preserving full functionality.

### Step 4: Annotate Every Line

Above **every single line of code**, add a short inline comment:

```
# <type/shape> / example: <realistic runtime value>
```

Rules:
- State the variable's type, structure, or dimensions.
- Show a realistic example value at runtime.
- For expressions without assignment, describe effect: `# appends "x" to list Y`.
- One line max. Be terse.
- Use the target language's type notation (e.g., `dict[str, list[str]]` for Python, `Record<string, string[]>` for TS).

See [references/annotation-examples.md](references/annotation-examples.md) for a concrete exemplar.

### Step 5: Output

1. Create `minimal/` in the project root if it does not exist.
2. Write the distilled file with a descriptive name (e.g., `minimal/section_parser.py`).
3. Print a short summary: what was extracted, line count, external deps remaining.

## Edge Cases

| Situation | Action |
|-----------|--------|
| External service deps (APIs, DBs) | Comment at top: `# requires: <service>`. No mocks/stubs. |
| Deep helper chains (A→B→C→D) | Flatten in dependency order. Inline if <5 lines. |
| Shared constants (dicts, config maps) | Copy only the subset used by the feature. |
| Config files referenced by path | Note the path in a top-level comment. Do not embed contents. |
| Multi-language features | Use the primary language. Note cross-language boundaries in comments. |
| Very large features (>500 lines) | Keep in one file. Single-file constraint > line count. |

## Verification

Before finishing, confirm:
1. The output is syntactically valid (e.g., `python -c "import ast; ast.parse(open('minimal/X.py').read())"` or equivalent for the target language).
2. Every code line has an annotation comment above it.
3. No unnecessary imports, functions, or constants remain.
4. The file reads top-to-bottom without jumping to other files.
5. **Functionally complete**: the distilled code could run the feature end-to-end given external services. No capabilities dropped — only ceremony removed.
