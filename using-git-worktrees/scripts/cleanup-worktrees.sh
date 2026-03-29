#!/usr/bin/env bash
set -euo pipefail

# cleanup-worktrees.sh — Remove merged worktrees and prune stale entries
# Usage: cleanup-worktrees.sh [--dry-run]

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# --- Must be in a git repo ---
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "Error: not inside a git repository"
    exit 1
}
cd "$REPO_ROOT"

MAIN_BRANCH="main"
# Fallback to master if main doesn't exist
git show-ref --verify --quiet "refs/heads/main" 2>/dev/null || MAIN_BRANCH="master"

echo "Scanning worktrees (base: $MAIN_BRANCH)..."
echo ""

REMOVED=0
KEPT=0

# List all worktrees except the main one
git worktree list --porcelain | grep '^worktree ' | sed 's/^worktree //' | while read -r WT_PATH; do
    # Skip the main repo
    [[ "$WT_PATH" == "$REPO_ROOT" ]] && continue

    BRANCH=$(git -C "$WT_PATH" branch --show-current 2>/dev/null || echo "")
    if [ -z "$BRANCH" ]; then
        echo "  SKIP  $WT_PATH (detached HEAD)"
        continue
    fi

    # Check if branch is merged into main
    if git branch --merged "$MAIN_BRANCH" 2>/dev/null | grep -q "[* +] *${BRANCH}$"; then
        if $DRY_RUN; then
            echo "  WOULD REMOVE  $WT_PATH ($BRANCH) — merged into $MAIN_BRANCH"
        else
            echo "  REMOVING  $WT_PATH ($BRANCH) — merged into $MAIN_BRANCH"
            git worktree remove --force "$WT_PATH" 2>/dev/null || {
                echo "    Failed to remove worktree. May have staged changes — inspect manually."
                continue
            }
            git branch -d "$BRANCH" 2>/dev/null || true
        fi
        REMOVED=$((REMOVED + 1))
    else
        echo "  KEEP  $WT_PATH ($BRANCH) — not yet merged"
        KEPT=$((KEPT + 1))
    fi
done

# Prune stale worktree entries
if ! $DRY_RUN; then
    echo ""
    echo "Pruning stale worktree entries..."
    git worktree prune
fi

echo ""
echo "Done."
if $DRY_RUN; then
    echo "(dry run — no changes made)"
fi
