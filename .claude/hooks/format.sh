#!/usr/bin/env bash
set -euo pipefail

# Python formatting with ruff (optimized for UV environments)
if command -v ruff >/dev/null 2>&1; then
  ruff check --fix . >/dev/null 2>&1 || true
  ruff format . >/dev/null 2>&1 || true
elif command -v uv >/dev/null 2>&1; then
  # Try via UV if ruff not in PATH
  uv run ruff check --fix . >/dev/null 2>&1 || true
  uv run ruff format . >/dev/null 2>&1 || true
fi

echo "✅ Format complete"
