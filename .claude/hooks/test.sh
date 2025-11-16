#!/usr/bin/env bash
set -euo pipefail

# Respect toggles
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOGGLES_FILE="$ROOT/.claude/toggles.env"
if [ -f "$TOGGLES_FILE" ]; then
  . "$TOGGLES_FILE"
fi

if [ "${ENABLE_TESTS:-0}" != "1" ]; then
  echo "🟡 Tests disabled via toggles"
  exit 0
fi

# Determine coverage threshold from constitution.md (default: 85)
COVERAGE_TARGET=85
if [ -f "spec/constitution.md" ]; then
  # Extract coverage target from constitution.md
  # Matches patterns like: coverage_target: 0.85 or coverage_target: 85
  EXTRACTED=$(grep -iE "coverage.?target" spec/constitution.md | grep -oE "[0-9]+\.?[0-9]*" | head -1)
  if [ -n "$EXTRACTED" ]; then
    # Convert decimal to percentage if needed (0.85 -> 85)
    if echo "$EXTRACTED" | grep -q "^0\."; then
      COVERAGE_TARGET=$(echo "$EXTRACTED * 100" | bc | cut -d. -f1)
    else
      COVERAGE_TARGET=$(echo "$EXTRACTED" | cut -d. -f1)
    fi
  fi
fi

# Run pytest with UV (supports coverage if enabled)
if command -v uv >/dev/null 2>&1; then
  if [ -d "tests" ] || [ -d "test" ]; then
    if [ "${ENABLE_COVERAGE:-1}" = "1" ]; then
      # Run with coverage AND enforce threshold
      if uv run pytest \
          --cov=src \
          --cov-fail-under="$COVERAGE_TARGET" \
          --cov-report=term-missing \
          --cov-report=html \
          -q --tb=line 2>&1; then
        echo "✅ Tests passing with coverage ≥ ${COVERAGE_TARGET}%"
      else
        echo "❌ Tests failed or coverage < ${COVERAGE_TARGET}%"
        exit 2
      fi
    else
      # Run without coverage
      if uv run pytest -q --tb=line 2>&1; then
        echo "✅ Tests passing"
      else
        echo "❌ Tests failed"
        exit 2
      fi
    fi
  else
    echo "🟡 No test directory found"
  fi
elif command -v pytest >/dev/null 2>&1; then
  # Fallback to direct pytest if UV not available
  if [ -d "tests" ] || [ -d "test" ]; then
    if [ "${ENABLE_COVERAGE:-1}" = "1" ] && [ -f "spec/constitution.md" ]; then
      # Run with coverage enforcement
      if pytest \
          --cov=src \
          --cov-fail-under="$COVERAGE_TARGET" \
          --cov-report=term-missing \
          -q --tb=line 2>&1; then
        echo "✅ Tests passing with coverage ≥ ${COVERAGE_TARGET}%"
      else
        echo "❌ Tests failed or coverage < ${COVERAGE_TARGET}%"
        exit 2
      fi
    else
      # Run without coverage
      if pytest -q --tb=line 2>&1; then
        echo "✅ Tests passing"
      else
        echo "❌ Tests failed"
        exit 2
      fi
    fi
  fi
else
  echo "🟡 pytest not available (install with: uv pip install pytest)"
fi
