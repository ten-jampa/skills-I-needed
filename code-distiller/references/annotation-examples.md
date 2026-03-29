# Annotation Examples

Reference for the `# <type/shape> / example: <value>` comment style.

## Python Example: Section Parser

```python
# requires: python-docx (docx)

# str / example: "## Company: Acme Corp\n- Founded 2019\n## Team:\n- Alice (CEO)"
cleaned_notes = choose_and_clean_md_notes(enhanced, full)

# dict[str, list[str]] / example: {}
sections = {}
# str | None / example: None
current_section = None

# list[str] / example: ["## Company: Acme Corp", "- Founded 2019", "## Team:", "- Alice (CEO)"]
lines = cleaned_notes.splitlines()

# str / example: "## Company: Acme Corp"
for raw_line in lines:
    # str / example: "## Company: Acme Corp"
    line = raw_line.strip()

    # bool / example: True
    is_header = line.startswith('#')
    if is_header:
        # str / example: "Company"
        section_name = line.lstrip('#').split(':', 1)[0].strip()
        # str / example: "Acme Corp"
        content_after = line.lstrip('#').split(':', 1)[1].strip() if ':' in line else ""

        # str / example: "Company"
        current_section = section_name
        # list[str] -> added to sections dict / example: sections["Company"] = []
        sections.setdefault(current_section, [])

        if content_after:
            # appends "Acme Corp" to sections["Company"]
            sections[current_section].append(content_after)
        # skip to next line
        continue

    if current_section is not None:
        # appends "- Founded 2019" to sections["Company"]
        sections[current_section].append(raw_line.rstrip())

# dict[str, str] / example: {"Company": "Acme Corp\n- Founded 2019", "Team": "- Alice (CEO)"}
result = {name: "\n".join(lines).strip() for name, lines in sections.items()}
```

## Key Principles

1. **Every line gets a comment** -- no exceptions, even for `continue` or `return`.
2. **Types use Python typing notation** -- `str`, `dict[str, list[str]]`, `int | None`.
3. **Examples are realistic** -- use plausible domain values, not `"foo"` or `123`.
4. **One line max** -- if the type is complex, abbreviate: `dict[str, str] (16 entries)`.
5. **Expressions without assignment** -- describe the effect: `# appends "x" to list Y`.
