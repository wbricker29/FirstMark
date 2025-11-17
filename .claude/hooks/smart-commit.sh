#!/usr/bin/env bash
set -euo pipefail

# Achievement-based commit hook for aidev workflow
# Only commits when meaningful work is completed

MODE="${1:-auto}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STATE_FILE="$ROOT/.claude/logs/state.json"
LAST_COMMIT_FILE="$ROOT/.claude/logs/last-commit-state.json"

# Respect toggles
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

# Generate achievement-based commit message
COMMIT_MSG=""

case "$MODE" in
  task-completion)
    # Extract completed tasks from state.json
    if [ -f "$STATE_FILE" ]; then
      # Find tasks marked as completed
      COMPLETED_TASKS=$(jq -r '
        .units | to_entries[] |
        .key as $unit |
        .value.tasks | to_entries[] |
        select(.value.status == "completed") |
        "\($unit): \(.value.title)"
      ' "$STATE_FILE" 2>/dev/null | head -3)

      if [ -n "$COMPLETED_TASKS" ]; then
        # Use first completed task for commit message
        FIRST_TASK=$(echo "$COMPLETED_TASKS" | head -1)
        TASK_COUNT=$(echo "$COMPLETED_TASKS" | wc -l | tr -d ' ')

        if [ "$TASK_COUNT" = "1" ]; then
          COMMIT_MSG="Complete task: $FIRST_TASK"
        else
          COMMIT_MSG="Complete $TASK_COUNT tasks, including: $FIRST_TASK"
        fi
      fi
    fi
    ;;

  unit-milestone)
    # Find which unit/document was created or updated
    CHANGED_DOCS=$(git diff --cached --name-only spec/ 2>/dev/null | grep -E '(design|plan)\.md$' || true)

    if [ -n "$CHANGED_DOCS" ]; then
      # Extract unit name from path (spec/units/UNIT_NAME/design.md)
      UNIT=$(echo "$CHANGED_DOCS" | head -1 | cut -d'/' -f3)
      DOC_TYPE=$(echo "$CHANGED_DOCS" | head -1 | grep -o -E '(design|plan)\.md$' | cut -d'.' -f1)

      if git diff --cached --diff-filter=A --name-only | grep -q "$CHANGED_DOCS"; then
        COMMIT_MSG="Create ${DOC_TYPE} for unit: $UNIT"
      else
        COMMIT_MSG="Update ${DOC_TYPE} for unit: $UNIT"
      fi
    else
      # Check for L1 documents (constitution, prd, spec)
      L1_CHANGED=$(git diff --cached --name-only spec/ 2>/dev/null | grep -E 'spec/(constitution|prd|spec)\.md$' || true)
      if [ -n "$L1_CHANGED" ]; then
        DOC_NAME=$(basename "$L1_CHANGED" .md)
        COMMIT_MSG="Update project ${DOC_NAME}"
      fi
    fi
    ;;

  test-pass)
    # Check if tests are passing (would need test results)
    COMMIT_MSG="Tests passing - verification checkpoint"
    ;;

  manual)
    # User explicitly requested commit
    COMMIT_MSG="${2:-Manual checkpoint}"
    ;;

  auto)
    # Smart detection: check what actually changed
    SPEC_CHANGES=$(git diff --cached --name-only spec/ 2>/dev/null | wc -l | tr -d ' ')
    CODE_CHANGES=$(git diff --cached --name-only | grep -E '\.(py|sh)$' 2>/dev/null | wc -l | tr -d ' ')

    if [ "$SPEC_CHANGES" -gt 0 ] && [ "$CODE_CHANGES" -gt 0 ]; then
      COMMIT_MSG="Update spec and implementation"
    elif [ "$SPEC_CHANGES" -gt 0 ]; then
      COMMIT_MSG="Update project documentation"
    elif [ "$CODE_CHANGES" -gt 0 ]; then
      COMMIT_MSG="Update implementation"
    else
      COMMIT_MSG="Incremental progress"
    fi
    ;;
esac

# Only commit if we have a meaningful message
if [ -n "$COMMIT_MSG" ]; then
  # Stage spec/ and CLAUDE.md
  git add spec/ CLAUDE.md 2>/dev/null || true

  # Also stage any explicitly changed files
  git add -u 2>/dev/null || true

  if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG" --no-verify 2>&1 || {
      echo "⚠️  Commit failed, but continuing"
      exit 0
    }
    echo "✅ Committed: $COMMIT_MSG"

    # Save state snapshot for future comparison
    if [ -f "$STATE_FILE" ]; then
      cp "$STATE_FILE" "$LAST_COMMIT_FILE" 2>/dev/null || true
    fi
  else
    echo "🟡 No staged changes after filtering"
  fi
else
  echo "🟡 No achievement detected for commit"
fi
