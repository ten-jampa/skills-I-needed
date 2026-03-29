#!/usr/bin/env bash
set -euo pipefail

# create-worktree.sh — Create an isolated git worktree with env setup and TASK.md
# Usage: create-worktree.sh <type> <description> [base-branch]
#   type: feat|bug|hotfix|exp
#   description: kebab-case name (e.g. auth-oauth2)
#   base-branch: defaults to main

VALID_TYPES="feat bug hotfix exp"

usage() {
    echo "Usage: $0 <type> <description> [base-branch]"
    echo "  type: feat|bug|hotfix|exp"
    echo "  description: kebab-case name (e.g. auth-oauth2)"
    echo "  base-branch: defaults to main"
    exit 1
}

# --- Args ---
[[ $# -lt 2 ]] && usage

TYPE="$1"
DESC="$2"
BASE="${3:-main}"

if ! echo "$VALID_TYPES" | grep -qw "$TYPE"; then
    echo "Error: type must be one of: $VALID_TYPES"
    exit 1
fi

# --- Must be in a git repo ---
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "Error: not inside a git repository"
    exit 1
}
cd "$REPO_ROOT"

NAME="${TYPE}-${DESC}"
WORKTREE_DIR=".worktrees/$NAME"
BRANCH_NAME="$NAME"

# --- Safety: ensure .worktrees/ is gitignored ---
mkdir -p .worktrees
if ! git check-ignore -q .worktrees 2>/dev/null; then
    echo "Adding .worktrees/ to .gitignore..."
    echo ".worktrees/" >> .gitignore
    git add .gitignore
    git commit -m "chore: add .worktrees/ to .gitignore"
fi

# --- Check branch doesn't already exist ---
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME" 2>/dev/null; then
    echo "Error: branch '$BRANCH_NAME' already exists"
    echo "  To use existing branch: git worktree add \"$WORKTREE_DIR\" \"$BRANCH_NAME\""
    exit 1
fi

# --- Create worktree ---
echo "Creating worktree at $WORKTREE_DIR (branch: $BRANCH_NAME from $BASE)..."
git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME" "$BASE"

cd "$WORKTREE_DIR"

# --- Environment setup (auto-detect) ---
echo "Detecting environment..."
if [ -f environment.yml ]; then
    ENV_NAME=$(grep 'name:' environment.yml | head -1 | awk '{print $2}')
    echo "Found environment.yml (conda env: $ENV_NAME)"
    if conda env list 2>/dev/null | grep -q "$ENV_NAME"; then
        echo "Conda env '$ENV_NAME' already exists — activate with: conda activate $ENV_NAME"
    else
        echo "Creating conda env from environment.yml..."
        conda env create -f environment.yml
        echo "Activate with: conda activate $ENV_NAME"
    fi
elif [ -f requirements.txt ]; then
    echo "Found requirements.txt — installing..."
    pip install -r requirements.txt
elif [ -f pyproject.toml ]; then
    echo "Found pyproject.toml — running poetry install..."
    poetry install
elif [ -f package.json ]; then
    echo "Found package.json — running npm install..."
    npm install
elif [ -f Cargo.toml ]; then
    echo "Found Cargo.toml — running cargo build..."
    cargo build
elif [ -f go.mod ]; then
    echo "Found go.mod — running go mod download..."
    go mod download
else
    echo "No recognized dependency file found — skipping env setup."
fi

# --- Create TASK.md ---
DATE=$(date +%Y-%m-%d)
cat > TASK.md <<EOF
# Task: ${DESC}
Created: ${DATE}
Branch: ${BRANCH_NAME}
Base: ${BASE}

## Objective
[What this worktree is for]

## Files to modify
-

## Success criteria
-

## Notes
-
EOF

echo ""
echo "========================================="
echo "Worktree ready at: $(pwd)"
echo "Branch: $BRANCH_NAME (based on $BASE)"
echo "TASK.md created — fill in the objective"
echo ""
echo "Next steps:"
echo "  cd $REPO_ROOT/$WORKTREE_DIR"
echo "  claude   # start Claude Code session"
echo "========================================="
