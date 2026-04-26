# Skills I Needed

Custom skills for coding-agent workflows.

## Install

**All skills:**

```bash
curl -sSL https://raw.githubusercontent.com/ten-jampa/skills-I-needed/main/install.sh | bash
```

**Specific skills:**

```bash
curl -sSL https://raw.githubusercontent.com/ten-jampa/skills-I-needed/main/install.sh | bash -s -- code-distiller karpathy-guidelines
```

Skills are installed to `~/.agents/skills/` (canonical) with symlinks in both `~/.claude/skills/` and `~/.codex/skills/`.

## Skills

| Skill | Description |
|-------|-------------|
| `build-filter` | Run project ideas through 7 go/no-go gates before building |
| `code-distiller` | Collapse any complex feature into one minimal, annotated, self-contained file |
| `create-learning-pipeline` | Generate complete Obsidian-native learning pipelines for any domain |
| `domain-onboarding` | Interactively learn any domain via the SEPA method (Structure → Enumeration → Process → Axiology) |
| `eval-pack` | Build a self-contained HTML proof-of-work pack for quick review |
| `karpathy-guidelines` | Behavioral guidelines to reduce common LLM coding mistakes |
| `ml-paper-writing` | Draft, structure, revise, and tighten machine learning papers and paper outlines |
| `progress` | Log completed work to PROGRESS.md with timestamps and verification |
| `unified-standup` | Generate unified daily standup from Claude Code and Codex CLI sessions |
| `using-git-worktrees` | Manage git worktrees for parallel isolated development |

## Adding New Skills

1. Create a new root-level folder named after the skill (`kebab-case`).
2. Add `SKILL.md` with only `name` and `description` in frontmatter.
3. Add `agents/openai.yaml` interface metadata (`display_name`, `short_description`, `default_prompt`).
4. Optionally add `scripts/`, `references/`, and/or `assets/` if the workflow needs reusable resources.

The install script auto-discovers any directory containing `SKILL.md`.

## Eval Pack Output Convention

`eval-pack` writes to a structured artifact directory by default:

```text
eval-packs/eval-pack-{task-slug}/eval_pack.html
```

Override behavior when needed:

```bash
python3 eval-pack/scripts/eval_pack_generator.py --config eval_data.json --output-dir artifacts/evals --slug my-task
python3 eval-pack/scripts/eval_pack_generator.py --config eval_data.json --output /tmp/eval_pack.html
```
