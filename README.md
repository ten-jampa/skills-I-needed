# Skills I Needed

Custom Claude Code skills for my agent workflows.

## Install

**All skills:**

```bash
curl -sSL https://raw.githubusercontent.com/ten-jampa/skills-I-needed/main/install.sh | bash
```

**Specific skills:**

```bash
curl -sSL https://raw.githubusercontent.com/ten-jampa/skills-I-needed/main/install.sh | bash -s -- code-distiller karpathy-guidelines
```

Skills are installed to `~/.claude/skills/`.

## Skills

| Skill | Description |
|-------|-------------|
| `code-distiller` | Collapse any complex feature into one minimal, annotated, self-contained file |
| `karpathy-guidelines` | Behavioral guidelines to reduce common LLM coding mistakes |
| `progress` | Log completed work to PROGRESS.md with timestamps and verification |
| `unified-standup` | Generate unified daily standup from Claude Code and Codex CLI sessions |
| `using-git-worktrees` | Manage git worktrees for parallel isolated development |

## Adding New Skills

Drop a folder with a `SKILL.md` at the root. The install script auto-discovers any directory containing `SKILL.md`.
