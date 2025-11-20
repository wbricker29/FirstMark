#!/usr/bin/env bash
set -euo pipefail

# Respect toggles
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOGGLES_FILE="$ROOT/.claude/toggles.env"
if [ -f "$TOGGLES_FILE" ]; then
  . "$TOGGLES_FILE"
fi

if [ "${ENABLE_TYPE_CHECK:-1}" != "1" ]; then
  exit 0  # Silent exit when disabled
fi

# Only run if src directory exists
if [ ! -d "$ROOT/src" ]; then
  exit 0  # Silent exit - no Python code to check yet
fi

# Try pyright first (faster), fallback to mypy
# Only output on errors to prevent feedback loops
if command -v pyright >/dev/null 2>&1; then
  pyright >/dev/null 2>&1 || {
    echo "❌ Type check failed (pyright)" >&2
    exit 2
  }
elif command -v uv >/dev/null 2>&1; then
  uv run mypy src >/dev/null 2>&1 || {
    echo "❌ Type check failed (mypy)" >&2
    exit 2
  }
elif command -v mypy >/dev/null 2>&1; then
  mypy src >/dev/null 2>&1 || {
    echo "❌ Type check failed (mypy)" >&2
    exit 2
  }
fi

# Silent success - no output
exit 0
