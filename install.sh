#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/ten-jampa/skills-I-needed.git"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
TMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "📦 Fetching skills from $REPO..."
git clone --depth 1 --quiet "$REPO" "$TMP_DIR/repo"

# All directories containing a SKILL.md are skills
AVAILABLE=()
for dir in "$TMP_DIR/repo"/*/; do
  [ -f "$dir/SKILL.md" ] && AVAILABLE+=("$(basename "$dir")")
done

# If specific skills requested, install only those; otherwise install all
REQUESTED=("$@")
if [ ${#REQUESTED[@]} -eq 0 ]; then
  INSTALL=("${AVAILABLE[@]}")
else
  INSTALL=("${REQUESTED[@]}")
fi

mkdir -p "$SKILLS_DIR"

installed=0
for skill in "${INSTALL[@]}"; do
  src="$TMP_DIR/repo/$skill"
  dest="$SKILLS_DIR/$skill"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "⚠️  Skill '$skill' not found in repo. Available: ${AVAILABLE[*]}"
    continue
  fi

  if [ -d "$dest" ]; then
    echo "🔄 Updating $skill..."
    rm -rf "$dest"
  else
    echo "✨ Installing $skill..."
  fi

  cp -R "$src" "$dest"
  installed=$((installed + 1))
done

echo ""
echo "✅ Installed $installed skill(s) to $SKILLS_DIR"
echo ""
echo "Available skills: ${AVAILABLE[*]}"
