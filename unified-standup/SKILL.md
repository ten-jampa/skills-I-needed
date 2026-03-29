---
name: unified-standup
description: >
  Generate a unified daily standup by scraping both Claude Code and Codex CLI session histories,
  git commits, and PROGRESS.md files. Synthesizes raw activity into a clean human-readable summary
  and saves it to the Obsidian WorkLogs folder and ~/.claude/STANDUP_LOG.md.
  Use when the user asks for a standup, daily update, worklog, or wants to summarize what they
  worked on today or on a specific past date (e.g. "standup for yesterday").
---

# Unified Standup

## Workflow

### Step 1 — Gather raw activity

Run the gatherer script:

```bash
python3 ~/.agents/skills/unified-standup/scripts/gather_sessions.py [--date YYYY-MM-DD]
```

Default is today. For yesterday on macOS: `--date $(date -v-1d +%Y-%m-%d)`

### Step 2 — Synthesize into a standup

Read the script output and write a standup with this structure:

```markdown
## YYYY-MM-DD

### What I worked on
- **[project-name]**: concise description of the work done (1-2 sentences per project)

### Key decisions / learnings
- (optional) notable choices made, bugs fixed, concepts learned

### Tomorrow / Next
- (optional) clear next steps if apparent from session history
```

Synthesis rules:
- Merge Claude + Codex sessions for the same project — they represent the same work
- Skip bare slash commands (`/exit`, `/model`, `/loop`) as standalone line items
- If git commits exist for a project, use them as the source of truth for what changed
- Keep it scannable — 1–3 bullets per project max
- Drop projects where no real work happened (only `/exit` or meta-commands)

### Step 3 — Save to both locations

**Obsidian WorkLogs** (one file per day):
```
/Users/tenzinjampa/Documents/Obsidian Vault/WorkLogs/YYYY-MM-DD.md
```
Create if missing. If already exists, append under a `---` separator.

**Global standup log**:
```
~/.claude/STANDUP_LOG.md
```
Prepend the new entry at the top (newest first). Create if missing.

### Step 4 — Show the standup to the user

Print the final standup in the chat so the user can see it immediately.
