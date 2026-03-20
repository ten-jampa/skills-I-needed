---
name: progress
description: "Log completed work to PROGRESS.md with timestamps and verification evidence. Use when the user asks for a progress update, after completing steps, or at session end."
---

# Progress Logger

## Workflow

1. Get the current timestamp by running `date -u +"%Y-%m-%d %H:%M UTC"`.
2. Review what was done since the last PROGRESS.md entry (or session start if no entries exist).
- Read the current `PROGRESS.md` if it exists.
- Look at recent tool calls, task list state, and conversation context.
- Identify completed steps with their verification evidence.
3. Append new entries to `PROGRESS.md` in the project root. Do not overwrite existing content.
4. Include proof in every entry (test output, command snippet, metric, or observable outcome). If you cannot verify, mark the entry `🔄 In Progress`.

## Entry Format

```markdown
### [YYYY-MM-DD HH:MM UTC] Short description of what was done
**Status**: ✅ Complete / ⚠️ Failed → Fixed / 🔄 In Progress
**Changes**: List of files modified and what changed (1 line each)
**Verification**: Concrete proof it works (test output, command result, metric)
**Notes**: Any gotchas, learnings, or decisions made (optional)
```

## Rules

- Append only — never delete or rewrite previous entries.
- No entry without proof — if you cannot verify, mark it `🔄 In Progress`.
- Keep it concise — 3-5 lines per entry, not paragraphs.
- Group related changes — one entry per logical step, not per file.
- If `PROGRESS.md` does not exist, create it with a session header.
- If invoked with an argument (e.g., `/progress clustering fix`), log only that specific item.

## Session Header

When creating a new session section, add:

```markdown
## Session: YYYY-MM-DD — Brief description of what this session is about
```

Only add a new session header if the date differs from the last session in the file.
