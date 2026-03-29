---
name: using-git-worktrees
description: "Manage git worktrees for parallel isolated development. Use when: (1) starting feature/bug/experiment work that needs isolation, (2) user says 'worktree', 'parallel work', 'isolate branch', 'set up branch for X', (3) before executing implementation plans requiring isolation, (4) cleaning up finished worktrees, (5) listing active worktrees."
---

# Git Worktrees for Parallel Development

## Core Concept

Git worktrees = multiple branch checkouts as separate directories, sharing one `.git` history. Each worktree gets its own Claude Code session with full, independent context. No stashing, no context loss, no branch switching.

## Create a Worktree

### 1. Safety Check

```bash
# Ensure .worktrees/ directory exists and is gitignored
mkdir -p .worktrees
git check-ignore -q .worktrees 2>/dev/null || echo ".worktrees/" >> .gitignore
```

If `.gitignore` was modified, commit it before proceeding.

### 2. Naming Convention

Format: `{type}-{description}` (kebab-case)

| Prefix   | Use for                        | Example                    |
|----------|--------------------------------|----------------------------|
| `feat`   | New features                   | `feat-auth-oauth2`         |
| `bug`    | Bug fixes                      | `bug-payment-timeout`      |
| `hotfix` | Urgent production fixes        | `hotfix-data-corruption`   |
| `exp`    | Experiments, spikes, migrations| `exp-pytorch-migration`    |

### 3. Create

```bash
NAME="feat-auth-oauth2"
git worktree add ".worktrees/$NAME" -b "$NAME"
cd ".worktrees/$NAME"
```

### 4. Environment Setup

Auto-detect and run the appropriate setup:

```bash
# Priority order — run first match
if [ -f environment.yml ]; then
    env_name=$(grep 'name:' environment.yml | head -1 | awk '{print $2}')
    conda activate "$env_name" 2>/dev/null || conda env create -f environment.yml
elif [ -f requirements.txt ]; then
    pip install -r requirements.txt
elif [ -f pyproject.toml ]; then
    poetry install
elif [ -f package.json ]; then
    npm install
elif [ -f Cargo.toml ]; then
    cargo build
elif [ -f go.mod ]; then
    go mod download
fi
```

### 5. Create TASK.md

Generate a task spec so Claude has immediate context in this worktree:

```markdown
# Task: {description}
Created: {date}
Branch: {name}
Base: main

## Objective
[What this worktree is for]

## Files to modify
-

## Success criteria
-

## Notes
-
```

### 6. Baseline Verification

Run project tests to confirm clean starting state. If tests fail, report failures and ask whether to proceed.

## List Worktrees

```bash
git worktree list
```

Present as a readable table with branch name, path, and HEAD commit.

## Cleanup

### Remove a single worktree

```bash
NAME="feat-auth-oauth2"
cd "$(git rev-parse --show-toplevel)"  # back to main repo
git worktree remove ".worktrees/$NAME"
# Delete branch if merged
git branch -d "$NAME" 2>/dev/null
```

### Batch cleanup — remove all merged worktrees

```bash
git worktree list --porcelain | grep 'worktree ' | sed 's/worktree //' | while read wt; do
    branch=$(git -C "$wt" branch --show-current)
    if [ "$branch" ] && git branch --merged main | grep -q "$branch"; then
        echo "Removing merged: $wt ($branch)"
        git worktree remove "$wt"
        git branch -d "$branch"
    fi
done
git worktree prune
```

### Prune stale entries

```bash
git worktree prune
```

Run this when worktree directories were manually deleted.

## Parallel Sessions

The power move: run multiple Claude Code instances, each in its own worktree.

### Setup

```bash
# Terminal 1 — feature work
cd .worktrees/feat-auth-oauth2 && claude

# Terminal 2 — bug fix
cd .worktrees/bug-payment-timeout && claude

# Terminal 3 — experiment
cd .worktrees/exp-pytorch-migration && claude
```

Each session has:
- Independent file state (different branch checkout)
- Shared git history (commits, remotes synchronized)
- Full Claude context (no cross-contamination)
- Its own TASK.md for immediate orientation

### With tmux

```bash
tmux new-session -d -s feat -c .worktrees/feat-auth-oauth2
tmux new-session -d -s bug -c .worktrees/bug-payment-timeout
tmux new-session -d -s exp -c .worktrees/exp-pytorch-migration
# Attach: tmux attach -t feat
```

## Bundled Scripts

### `scripts/create-worktree.sh`

Automates the full create workflow: safety check, branch creation, env setup, TASK.md generation.

```
Usage: create-worktree.sh <type> <description> [base-branch]
  type: feat|bug|hotfix|exp
  base-branch: defaults to main
```

### `scripts/cleanup-worktrees.sh`

Lists all worktrees, removes merged ones, prunes stale entries.

```
Usage: cleanup-worktrees.sh [--dry-run]
```

## Common Pitfalls

| Problem | Fix |
|---------|-----|
| "branch already checked out" | `git worktree list` to find conflict, remove or use `--force` |
| `.worktrees/` showing in git status | Add to `.gitignore` and commit |
| Wrong conda env in worktree | Each worktree needs explicit `conda activate` — envs don't follow `cd` |
| Too many stale worktrees | Run `cleanup-worktrees.sh` or `git worktree prune` |
| Forgot which worktree does what | Check `TASK.md` in each worktree, or `git worktree list` |

## Red Flags

**Never:**
- Create project-local worktree without verifying `.gitignore`
- Skip baseline test verification
- Leave merged worktrees lingering indefinitely

**Always:**
- Use the naming convention (`type-description`)
- Create TASK.md in each worktree
- Clean up after merging
