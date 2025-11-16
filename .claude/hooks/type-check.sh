#!/usr/bin/env bash
set -euo pipefail

# Respect toggles
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOGGLES_FILE="$ROOT/.claude/toggles.env"
if [ -f "$TOGGLES_FILE" ]; then
  . "$TOGGLES_FILE"
fi

if [ "${ENABLE_TYPE_CHECK:-1}" != "1" ]; then
  echo "🟡 Type checking disabled via toggles"
  exit 0
fi

# Try pyright first (faster), fallback to mypy
if command -v pyright >/dev/null 2>&1; then
  if pyright 2>&1; then
    echo "✅ Type check passed (pyright)"
  else
    echo "❌ Type check failed (pyright)"
    exit 2
  fi
elif command -v uv >/dev/null 2>&1; then
  # Try mypy via UV
  if uv run mypy src 2>&1; then
    echo "✅ Type check passed (mypy)"
  else
    echo "❌ Type check failed (mypy)"
    exit 2
  fi
elif command -v mypy >/dev/null 2>&1; then
  if mypy src 2>&1; then
    echo "✅ Type check passed (mypy)"
  else
    echo "❌ Type check failed (mypy)"
    exit 2
  fi
else
  echo "🟡 No type checker available (install with: uv pip install mypy or pyright)"
fi
