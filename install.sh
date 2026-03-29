#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/ten-jampa/skills-I-needed.git"
AGENTS_DIR="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
CLAUDE_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
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

mkdir -p "$AGENTS_DIR" "$CLAUDE_DIR"

installed=0
for skill in "${INSTALL[@]}"; do
  src="$TMP_DIR/repo/$skill"
  agents_dest="$AGENTS_DIR/$skill"
  claude_dest="$CLAUDE_DIR/$skill"

  if [ ! -f "$src/SKILL.md" ]; then
    echo "⚠️  Skill '$skill' not found in repo. Available: ${AVAILABLE[*]}"
    continue
  fi

  if [ -d "$agents_dest" ]; then
    echo "🔄 Updating $skill..."
    rm -rf "$agents_dest"
  else
    echo "✨ Installing $skill..."
  fi

  # Install to ~/.agents/skills (canonical location)
  cp -R "$src" "$agents_dest"

  # Symlink from ~/.claude/skills if not already pointing there
  if [ -L "$claude_dest" ]; then
    rm "$claude_dest"
  elif [ -d "$claude_dest" ]; then
    rm -rf "$claude_dest"
  fi
  ln -s "$agents_dest" "$claude_dest"

  installed=$((installed + 1))
done

echo ""
echo "✅ Installed $installed skill(s)"
echo "   📂 $AGENTS_DIR (canonical)"
echo "   🔗 $CLAUDE_DIR (symlinked)"
echo ""
echo "Available skills: ${AVAILABLE[*]}"
