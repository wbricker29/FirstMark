#!/usr/bin/env bash
set -euo pipefail

# Respect toggles
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOGGLES_FILE="$ROOT/.claude/toggles.env"
if [ -f "$TOGGLES_FILE" ]; then
  . "$TOGGLES_FILE"
fi

if [ "${ENABLE_AUTOCOMMIT:-1}" != "1" ]; then
  echo "🟡 Auto-commit disabled via toggles"
  exit 0
fi

# Check if in git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "🟡 Not a git repository"
  exit 0
fi

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
  echo "🟡 No changes to commit"
  exit 0
fi

# Auto-commit
git add spec/ CLAUDE.md 2>/dev/null || true
if ! git diff --cached --quiet; then
  git commit -m "aidev: Auto-commit project artifacts" --no-verify 2>&1 || true
  echo "✅ Changes committed"
else
  echo "🟡 No staged changes"
fi
