#!/usr/bin/env bash
# Initialization Script for aidev V4.2 - Python Edition
# Optimized for Python projects using UV for package management
# Creates directory structure, Python-specific templates, commands, and automation hooks
# Implements L1 (Project) and L2 (Unit) hierarchy with separation of concerns

set -euo pipefail

ROOT="$(pwd)"
CLAUDE_DIR="$ROOT/.claude"
CMD_DIR="$CLAUDE_DIR/commands"
HOOKS_DIR="$CLAUDE_DIR/hooks"
LOGS_DIR="$CLAUDE_DIR/logs"
TEMPLATES_DIR="$CLAUDE_DIR/templates"
SPEC_DIR="$ROOT/spec"
UNITS_DIR="$SPEC_DIR/units"

# ============================================================================
# TOGGLES (Enable/Disable Tests and Auto-Commit)
# ============================================================================

TOGGLES_FILE="$CLAUDE_DIR/toggles.env"

ensure_toggles() {
  mkdir -p "$CLAUDE_DIR"
  if [ ! -f "$TOGGLES_FILE" ]; then
    {
      echo "ENABLE_TESTS=0"
      echo "ENABLE_AUTOCOMMIT=1"
      echo "ENABLE_TYPE_CHECK=1"
      echo "ENABLE_COVERAGE=1"
    } > "$TOGGLES_FILE"
  fi
}

set_toggle() {
  local var="$1" val="$2"
  ensure_toggles
  awk -v var="$var" -v val="$val" '
    BEGIN{found=0}
    $0 ~ "^"var"=" {print var"="val; found=1; next}
    {print}
    END{if(!found) print var"="val}
  ' "$TOGGLES_FILE" > "$TOGGLES_FILE.tmp" && mv "$TOGGLES_FILE.tmp" "$TOGGLES_FILE"
}

print_status() {
  ensure_toggles
  . "$TOGGLES_FILE" 2>/dev/null || true
  echo "Toggle status:"
  echo "  ENABLE_TESTS=${ENABLE_TESTS:-0}"
  echo "  ENABLE_AUTOCOMMIT=${ENABLE_AUTOCOMMIT:-1}"
  echo "  ENABLE_TYPE_CHECK=${ENABLE_TYPE_CHECK:-1}"
  echo "  ENABLE_COVERAGE=${ENABLE_COVERAGE:-1}"
}

# Handle CLI toggles
if [ "${1:-}" = "--status" ]; then
  print_status
  exit 0
fi

# Track if any toggle was modified (to exit early and avoid re-initialization)
TOGGLE_MODIFIED=0

while [ $# -gt 0 ]; do
  case "$1" in
    --enable-tests) set_toggle ENABLE_TESTS 1 ; TOGGLE_MODIFIED=1 ; shift ;;
    --disable-tests) set_toggle ENABLE_TESTS 0 ; TOGGLE_MODIFIED=1 ; shift ;;
    --enable-commits) set_toggle ENABLE_AUTOCOMMIT 1 ; TOGGLE_MODIFIED=1 ; shift ;;
    --disable-commits) set_toggle ENABLE_AUTOCOMMIT 0 ; TOGGLE_MODIFIED=1 ; shift ;;
    --enable-type-check) set_toggle ENABLE_TYPE_CHECK 1 ; TOGGLE_MODIFIED=1 ; shift ;;
    --disable-type-check) set_toggle ENABLE_TYPE_CHECK 0 ; TOGGLE_MODIFIED=1 ; shift ;;
    --enable-coverage) set_toggle ENABLE_COVERAGE 1 ; TOGGLE_MODIFIED=1 ; shift ;;
    --disable-coverage) set_toggle ENABLE_COVERAGE 0 ; TOGGLE_MODIFIED=1 ; shift ;;
    *) break ;;
  esac
done

ensure_toggles

# If toggles were modified, show status and exit (don't re-initialize)
if [ "$TOGGLE_MODIFIED" = "1" ]; then
  echo "✅ Toggle settings updated"
  echo ""
  print_status
  exit 0
fi

# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================

mkdir -p "$CMD_DIR" "$HOOKS_DIR" "$LOGS_DIR" "$TEMPLATES_DIR" "$SPEC_DIR" "$UNITS_DIR"

# Helper to append unique lines
append_unique_line() {
  local file="$1"; shift
  local line="$*"
  mkdir -p "$(dirname "$file")"
  touch "$file"
  grep -qxF "$line" "$file" 2>/dev/null || echo "$line" >> "$file"
}

# ============================================================================
# .claude/settings.json (Hook Configuration)
# ============================================================================

cat > "$CLAUDE_DIR/settings.json" << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Create|Rename|Delete",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/format.sh",
            "timeout": 25
          },
          {
            "type": "command",
            "command": "./.claude/hooks/state-tracker.py",
            "timeout": 15
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/test.sh",
            "timeout": 120
          },
          {
            "type": "command",
            "command": "./.claude/hooks/type-check.sh",
            "timeout": 60
          },
          {
            "type": "command",
            "command": "./.claude/hooks/git-commit.sh",
            "timeout": 15
          },
          {
            "type": "command",
            "command": "if command -v osascript >/dev/null 2>&1; then osascript -e 'display notification \"Claude finished working\" with title \"Claude Code\"'; elif command -v notify-send >/dev/null 2>&1; then notify-send 'Claude Code' 'Claude finished working'; fi"
          }
        ]
      }
    ]
  }
}
EOF

# ============================================================================
# HOOKS (Python-Optimized Automation Layer)
# ============================================================================

# format.sh - Python-focused formatting with ruff
cat > "$HOOKS_DIR/format.sh" << 'EOF'
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
EOF
chmod +x "$HOOKS_DIR/format.sh"

# test.sh - Python testing with UV + pytest
cat > "$HOOKS_DIR/test.sh" << 'EOF'
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
EOF
chmod +x "$HOOKS_DIR/test.sh"

# type-check.sh - Python type checking with mypy or pyright
cat > "$HOOKS_DIR/type-check.sh" << 'EOF'
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
EOF
chmod +x "$HOOKS_DIR/type-check.sh"

# state-tracker.py - Language-agnostic state tracker (unchanged from v4)
cat > "$HOOKS_DIR/state-tracker.py" << 'PYTHONEOF'
#!/usr/bin/env python3
"""
State Tracker for aidev V4.2 (Python Edition)
Parses Markdown documents with YAML frontmatter
Generates comprehensive state snapshot in .claude/logs/state.json
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Optional PyYAML for robust frontmatter parsing (graceful degradation)
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Paths
ROOT = Path.cwd()
SPEC_DIR = ROOT / "spec"
UNITS_DIR = SPEC_DIR / "units"
LOGS_DIR = ROOT / ".claude" / "logs"
STATE_FILE = LOGS_DIR / "state.json"

def safe_load_markdown(path: Path) -> Optional[Dict[str, Any]]:
    """Load Markdown file with YAML frontmatter"""
    if not path.exists():
        return None

    try:
        with open(path, 'r') as f:
            content = f.read()
    except Exception:
        return None

    # Extract frontmatter (between --- delimiters)
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return {}

    frontmatter_text = frontmatter_match.group(1)

    if YAML_AVAILABLE:
        # Use PyYAML for robust parsing
        try:
            return yaml.safe_load(frontmatter_text) or {}
        except Exception:
            return {}
    else:
        # Fallback: simple key-value regex parsing
        data = {}
        for line in frontmatter_text.split('\n'):
            match = re.match(r'(\w+):\s*"?([^"]+)"?', line.strip())
            if match:
                key, value = match.groups()
                data[key] = value
        return data

def get_l1_status() -> Dict[str, Any]:
    """Check status of L1 documents (constitution, prd, spec)"""
    docs = {
        "constitution": SPEC_DIR / "constitution.md",
        "prd": SPEC_DIR / "prd.md",
        "spec": SPEC_DIR / "spec.md"
    }

    status = {}
    for name, path in docs.items():
        if path.exists():
            meta = safe_load_markdown(path)
            status[name] = {
                "exists": True,
                "version": meta.get('version') if meta else None,
                "updated": meta.get('updated') if meta else None
            }
        else:
            status[name] = {"exists": False}

    return status

def parse_status_from_markdown(content: str) -> Dict[str, Any]:
    """Parse status section from Markdown body"""
    info = {}

    # Find Status section
    status_match = re.search(r'##\s+Status\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not status_match:
        return info

    status_section = status_match.group(1)

    # Parse progress
    progress_match = re.search(r'\*\*Progress:\*\*\s*(\d+)%', status_section)
    if progress_match:
        info['progress'] = int(progress_match.group(1))

    # Parse coverage
    coverage_match = re.search(r'\*\*Coverage:\*\*\s*([\d.]+)%?', status_section)
    if coverage_match:
        info['coverage'] = float(coverage_match.group(1)) / 100 if '.' in coverage_match.group(1) else float(coverage_match.group(1))

    # Parse blockers
    blockers_match = re.search(r'\*\*Blockers:\*\*\s*(.+?)(?=\n\*\*|\Z)', status_section, re.DOTALL)
    if blockers_match:
        blockers_text = blockers_match.group(1).strip()
        if blockers_text.lower() not in ['none', 'n/a', '']:
            info['blockers'] = [b.strip() for b in blockers_text.split(',')]

    return info

def parse_tasks_from_markdown(content: str) -> Dict[str, Any]:
    """Parse tasks from Markdown body"""
    tasks = {}

    # Find Tasks section
    tasks_match = re.search(r'##\s+Tasks\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not tasks_match:
        return tasks

    tasks_section = tasks_match.group(1)

    # Find all task headers (### TK-##)
    task_blocks = re.split(r'###\s+(TK-\d+)', tasks_section)[1:]  # Skip first empty element

    for i in range(0, len(task_blocks), 2):
        if i + 1 >= len(task_blocks):
            break

        task_id = task_blocks[i].strip()
        task_content = task_blocks[i + 1]

        # Parse task fields
        title_match = re.search(r'\*\*Title:\*\*\s*(.+)', task_content)
        status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', task_content)
        completed_match = re.search(r'\*\*Completed:\*\*\s*(\d{4}-\d{2}-\d{2})', task_content)

        tasks[task_id] = {
            "title": title_match.group(1).strip() if title_match else "Unknown",
            "status": status_match.group(1).strip() if status_match else "unknown",
            "completed": completed_match.group(1) if completed_match else None
        }

    return tasks

def get_units_status() -> Dict[str, Any]:
    """Get status of all units"""
    units = {}

    if not UNITS_DIR.exists():
        return units

    for unit_dir in sorted(UNITS_DIR.iterdir()):
        if not unit_dir.is_dir():
            continue

        unit_name = unit_dir.name
        unit_status = {
            "design_exists": False,
            "plan_exists": False,
            "tasks": {},
            "blockers": [],
            "actual_coverage": None
        }

        # Check design
        design_path = unit_dir / "design.md"
        if design_path.exists():
            unit_status["design_exists"] = True

        # Check plan and parse tasks
        plan_path = unit_dir / "plan.md"
        if plan_path.exists():
            unit_status["plan_exists"] = True

            try:
                with open(plan_path, 'r') as f:
                    plan_content = f.read()

                # Parse tasks from Markdown body
                unit_status['tasks'] = parse_tasks_from_markdown(plan_content)

                # Parse status section from Markdown body
                status_info = parse_status_from_markdown(plan_content)
                unit_status['blockers'] = status_info.get('blockers', [])
                unit_status['actual_coverage'] = status_info.get('coverage', None)

            except Exception:
                pass

        units[unit_name] = unit_status

    return units

def parse_interfaces_from_markdown(content: str) -> Set[str]:
    """Parse interface names from Markdown body (### [interface_name] sections)"""
    interfaces = set()

    # Find Interfaces section
    interfaces_match = re.search(r'##\s+Interfaces\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not interfaces_match:
        return interfaces

    interfaces_section = interfaces_match.group(1)

    # Find all ### headers with optional brackets
    interface_matches = re.finditer(r'###\s+(?:\[(\w+)\]|(\w+))', interfaces_section)
    for match in interface_matches:
        interface_name = match.group(1) or match.group(2)
        if interface_name:
            interfaces.add(interface_name)

    return interfaces

def parse_entities_from_markdown(content: str) -> Set[str]:
    """Parse entity names from Markdown body (### Entity: [EntityName] sections)"""
    entities = set()

    # Find Data Model section
    data_model_match = re.search(r'##\s+Data Model\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if not data_model_match:
        return entities

    data_model_section = data_model_match.group(1)

    # Find all ### Entity: headers
    entity_matches = re.finditer(r'###\s+Entity:\s+(?:\[(\w+)\]|(\w+))', data_model_section)
    for match in entity_matches:
        entity_name = match.group(1) or match.group(2)
        if entity_name:
            entities.add(entity_name)

    return entities

def validate_alignment() -> Dict[str, Any]:
    """Validate document alignment and references"""
    issues = []

    # Load spec content
    spec_path = SPEC_DIR / "spec.md"
    if not spec_path.exists():
        return {"valid": True, "issues": []}

    try:
        with open(spec_path, 'r') as f:
            spec_content = f.read()
    except Exception:
        return {"valid": True, "issues": []}

    # Parse interfaces and entities from Markdown body
    spec_interfaces = parse_interfaces_from_markdown(spec_content)
    spec_entities = parse_entities_from_markdown(spec_content)

    # Check each unit's design references
    if UNITS_DIR.exists():
        for unit_dir in UNITS_DIR.iterdir():
            if not unit_dir.is_dir():
                continue

            design = safe_load_markdown(unit_dir / "design.md")
            if not design:
                continue

            # Check interface references
            interfaces_touched = design.get('interfaces_touched', [])
            if isinstance(interfaces_touched, list):
                for iface_ref in interfaces_touched:
                    if iface_ref and iface_ref not in spec_interfaces:
                        issues.append({
                            "type": "invalid_reference",
                            "unit": unit_dir.name,
                            "file": "design.md",
                            "message": f"References interface '{iface_ref}' which doesn't exist in spec.md"
                        })

            # Check entity references
            data_shapes = design.get('data_shapes', [])
            if isinstance(data_shapes, list):
                for entity_ref in data_shapes:
                    if entity_ref and entity_ref not in spec_entities:
                        issues.append({
                            "type": "invalid_reference",
                            "unit": unit_dir.name,
                            "file": "design.md",
                            "message": f"References entity '{entity_ref}' which doesn't exist in spec.md"
                        })

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }

def check_constitution_compliance() -> Dict[str, Any]:
    """Check compliance with constitution quality bars"""
    violations = []

    constitution = safe_load_markdown(SPEC_DIR / "constitution.md")
    if not constitution:
        return {"violations": []}

    quality_bars = constitution.get('quality_bars', {})
    coverage_target = quality_bars.get('coverage_target', 0.85) if isinstance(quality_bars, dict) else 0.85

    # Get actual coverage from unit status
    units_status = get_units_status()
    for unit_name, unit_data in units_status.items():
        actual_coverage = unit_data.get('actual_coverage')
        # Only report violation if coverage is explicitly set and below target
        if actual_coverage is not None and actual_coverage < coverage_target:
            violations.append({
                "type": "coverage",
                "unit": unit_name,
                "actual": actual_coverage,
                "required": coverage_target
            })

    return {"violations": violations}

def generate_state() -> Dict[str, Any]:
    """Generate complete state snapshot"""
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "l1_status": get_l1_status(),
        "units": get_units_status(),
        "alignment": validate_alignment(),
        "constitution_compliance": check_constitution_compliance()
    }

def main():
    """Main entry point"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        state = generate_state()
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        print("✅ State updated")
    except Exception as e:
        print(f"❌ State tracker failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
PYTHONEOF
chmod +x "$HOOKS_DIR/state-tracker.py"

# git-commit.sh - Auto-commit with toggle support
cat > "$HOOKS_DIR/git-commit.sh" << 'EOF'
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
EOF
chmod +x "$HOOKS_DIR/git-commit.sh"

# ============================================================================
# TEMPLATES (Python-Specific)
# ============================================================================

cat > "$TEMPLATES_DIR/CONSTITUTION-TEMPLATE.md" << 'EOF'
---
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---

# Project Constitution

Non-negotiable governance for Python development

## Principles

### KISS (Keep It Simple, Stupid)
- Prefer simple, readable Python code over clever solutions
- Explicit is better than implicit (PEP 20)
- Functions over classes when possible
- Minimize abstraction layers

### YAGNI (You Ain't Gonna Need It)
- Build only what's needed now
- Validate requirements before implementation
- Defer optimization until measured need
- No speculative features

### Type Safety
- All functions must have type hints (PEP 484)
- Use pyright or mypy for static type checking
- Prefer strict typing (avoid `Any` when possible)
- Document complex types with TypedDict or dataclasses

### Testing
- All features require tests (pytest)
- Tests must be readable and maintainable
- Use fixtures for reusable test setup
- Test both happy paths and edge cases

## Quality Bars

### Coverage
- **Target:** 85% (0.85)
- **Measure:** pytest-cov
- **Gate:** CI must pass coverage threshold

### Code Quality
- **Linting:** ruff (replaces flake8, isort, black)
- **Type Checking:** pyright or mypy
- **Formatting:** ruff format (black-compatible)
- **Docstrings:** Google or NumPy style

### Performance
- **Response Time:** [Define acceptable latency]
- **Memory:** [Define acceptable memory usage]
- **Profiling:** Use py-spy or cProfile when needed

## Constraints

### Python Version
- **Minimum:** Python 3.10+
- **Reason:** [Specify reason - pattern matching, better type hints, etc.]

### Package Management
- **Tool:** UV (https://github.com/astral-sh/uv)
- **Commands:**
  - `uv pip install <package>` - Install dependencies
  - `uv run python script.py` - Run Python scripts
  - `uv run pytest` - Run tests

### Project Structure
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── module.py
│       └── subpackage/
├── tests/
│   ├── __init__.py
│   └── test_module.py
├── pyproject.toml
├── README.md
└── .python-version
```

### Dependencies
- **Minimal:** Only essential dependencies
- **Pinned:** Use version constraints in pyproject.toml
- **Audited:** Run `uv pip audit` regularly

## Code Style

### Naming Conventions (PEP 8)
- **Modules:** lowercase_with_underscores
- **Classes:** PascalCase
- **Functions:** lowercase_with_underscores
- **Constants:** UPPERCASE_WITH_UNDERSCORES
- **Private:** _leading_underscore

### Docstrings
```python
def function_name(arg1: str, arg2: int) -> bool:
    """Short one-line summary.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When arg2 is negative
    """
    pass
```

### Type Hints
```python
from typing import Optional, List, Dict
from collections.abc import Callable

def process_items(
    items: List[str],
    callback: Optional[Callable[[str], bool]] = None
) -> Dict[str, int]:
    """Process items with optional callback."""
    pass
```

## CI/CD Gates

### Pre-Commit
1. ruff format (auto-fix)
2. ruff check (linting)
3. pyright/mypy (type checking)

### Pre-Merge
1. pytest (all tests pass)
2. pytest-cov (coverage >= 85%)
3. ruff check --no-fix (no linting issues)
4. pyright/mypy (no type errors)

## Security

### Input Validation
- Never trust external input
- Use Pydantic for API validation
- Sanitize SQL inputs (use ORMs or parameterized queries)

### Secrets Management
- Never commit secrets to git
- Use environment variables or secrets management tools
- Add `.env` to `.gitignore`

### Dependencies
- Run `uv pip audit` before releases
- Pin dependencies to specific versions
- Update dependencies regularly

## Non-Negotiables

1. **No merges without tests passing**
2. **No merges below coverage threshold**
3. **All public functions must have type hints**
4. **All public functions must have docstrings**
5. **Follow PEP 8 (enforced by ruff)**

## Exceptions

Exceptions to these rules require:
1. Documentation of reason in CLAUDE.md
2. Approval from [specify approval process]
3. Clear timeline for resolution
EOF

cat > "$TEMPLATES_DIR/PRD-TEMPLATE.md" << 'EOF'
---
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---

# Product Requirements Document

Python project requirements and goals

## Problem Statement

### Current Situation
[Describe the current state and pain points]

### Desired State
[Describe the ideal future state]

### Gap Analysis
[What's missing? Why does this gap exist?]

## Goals

### Primary Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

### Success Metrics
- **Metric 1:** [e.g., Process 10k records/second]
- **Metric 2:** [e.g., Reduce latency to <100ms]
- **Metric 3:** [e.g., Support 100+ concurrent users]

## Scope

### In Scope
- [Feature/capability 1]
- [Feature/capability 2]
- [Feature/capability 3]

### Out of Scope
- [Explicitly excluded feature 1]
- [Explicitly excluded feature 2]
- [Reason for exclusion]

### Future Considerations
- [Potential future enhancements]
- [Ideas for later iterations]

## User Stories

### Story 1: [Title]
**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria:**
- Given [context]
- When [action]
- Then [outcome]

### Story 2: [Title]
[Repeat pattern]

## Python-Specific Considerations

### Performance Requirements
- **Throughput:** [e.g., 1000 requests/second]
- **Latency:** [e.g., p95 < 200ms, p99 < 500ms]
- **Memory:** [e.g., < 512MB per worker]
- **Concurrency:** [e.g., async/await, threading, multiprocessing]

### Integration Points
- **APIs:** [REST, GraphQL, gRPC, etc.]
- **Databases:** [PostgreSQL, MongoDB, Redis, etc.]
- **Message Queues:** [RabbitMQ, Kafka, etc.]
- **External Services:** [AWS, GCP, third-party APIs]

### Data Requirements
- **Input Formats:** [JSON, CSV, Parquet, etc.]
- **Output Formats:** [JSON, CSV, Parquet, etc.]
- **Data Volume:** [Records per day, total size]
- **Data Retention:** [How long to keep data]

## Technical Constraints

### Python Version
- **Minimum:** Python 3.10+
- **Reason:** [Type hints, pattern matching, performance]

### Dependencies
- **Core:** [List essential packages - FastAPI, SQLAlchemy, etc.]
- **Dev:** [pytest, ruff, mypy, etc.]
- **Optional:** [Packages for optional features]

### Deployment
- **Environment:** [Docker, AWS Lambda, GCP Cloud Run, etc.]
- **Configuration:** [Environment variables, config files]
- **Monitoring:** [Logging, metrics, tracing]

## Risks & Assumptions

### Risks
1. **Risk:** [e.g., Third-party API rate limits]
   **Mitigation:** [Implement retry logic and caching]

2. **Risk:** [e.g., Data volume exceeds memory]
   **Mitigation:** [Stream processing with generators]

### Assumptions
- [Assumption 1 - e.g., Users have Python 3.10+ installed]
- [Assumption 2 - e.g., Input data is well-formed JSON]
- [Assumption 3 - e.g., Database supports concurrent connections]

## Timeline

### Phase 1: MVP (Week 1-2)
- [Core feature 1]
- [Core feature 2]

### Phase 2: Enhancement (Week 3-4)
- [Enhancement 1]
- [Enhancement 2]

### Phase 3: Optimization (Week 5+)
- [Performance tuning]
- [Additional features]

## Acceptance Criteria (Project-Level)

### Functional
- AC-PRD-01: All user stories implemented and tested
- AC-PRD-02: API endpoints documented with OpenAPI/Swagger
- AC-PRD-03: Error handling covers all edge cases

### Non-Functional
- AC-PRD-04: Tests achieve 85%+ coverage
- AC-PRD-05: Type checking passes with no errors
- AC-PRD-06: Performance meets specified metrics

### Documentation
- AC-PRD-07: README includes quickstart guide
- AC-PRD-08: All public functions have docstrings
- AC-PRD-09: Architecture documented in spec.md
EOF

cat > "$TEMPLATES_DIR/SPEC-TEMPLATE.md" << 'EOF'
---
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---

# Technical Specification

Engineering contract for Python implementation

## Architecture

### System Overview
[High-level description of the system architecture]

### Component Diagram
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │─────▶│   API       │─────▶│  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  Service    │
                     └─────────────┘
```

### Technology Stack
- **Language:** Python 3.10+
- **Framework:** [FastAPI, Flask, Django, etc.]
- **Database:** [PostgreSQL, MongoDB, etc.]
- **Cache:** [Redis, Memcached, etc.]
- **Task Queue:** [Celery, RQ, etc.]
- **Package Manager:** UV

### Project Structure
```
src/
├── package_name/
│   ├── __init__.py
│   ├── api/              # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/           # Data models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/         # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/            # Utilities
│       ├── __init__.py
│       └── helpers.py
tests/
├── __init__.py
├── test_api/
├── test_models/
└── test_services/
```

## Interfaces

### [parse_document]
**Purpose:** Parse document into structured data

**Signature:**
```python
from typing import Optional
from pathlib import Path

def parse_document(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = True
) -> Optional[Document]:
    """Parse document from file.

    Args:
        file_path: Path to document file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate document structure

    Returns:
        Parsed Document object, or None if parsing fails

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If document is invalid (when validate=True)
    """
    pass
```

**Examples:**
```python
# Success case
doc = parse_document(Path("data.json"))
assert doc is not None
assert doc.title == "Example"

# Error case
doc = parse_document(Path("invalid.json"))
assert doc is None
```

### [validate_record]
**Purpose:** Validate record against schema

**Signature:**
```python
from typing import Dict, Any, List

def validate_record(
    record: Dict[str, Any],
    schema: Dict[str, Any]
) -> tuple[bool, List[str]]:
    """Validate record against JSON schema.

    Args:
        record: Record data to validate
        schema: JSON schema definition

    Returns:
        Tuple of (is_valid, error_messages)
    """
    pass
```

## Data Model

### Entity: [User]
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User entity."""
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    last_login: Optional[datetime] = None
```

**Fields:**
- `id`: Unique identifier (auto-increment)
- `email`: User email (unique, indexed)
- `name`: Display name
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `is_active`: Account status flag
- `last_login`: Last login timestamp (nullable)

**Constraints:**
- email must be valid email format
- email must be unique
- name length: 1-100 characters

### Entity: [Record]
```python
from typing import Optional, Dict, Any
from enum import Enum

class RecordStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Record:
    """Data record entity."""
    id: str
    data: Dict[str, Any]
    status: RecordStatus
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
```

## Non-Functional Requirements

### Performance
- **API Response Time:** p95 < 200ms, p99 < 500ms
- **Database Queries:** All queries < 100ms
- **Throughput:** 1000 requests/second
- **Memory Usage:** < 512MB per worker

### Scalability
- **Horizontal Scaling:** Support 10+ worker processes
- **Concurrency:** async/await for I/O operations
- **Caching:** Redis for frequently accessed data
- **Database:** Connection pooling (min=5, max=20)

### Security
- **Authentication:** JWT tokens (1-hour expiry)
- **Authorization:** Role-based access control (RBAC)
- **Input Validation:** Pydantic models for all inputs
- **SQL Injection:** Use SQLAlchemy with parameterized queries
- **Secrets:** Environment variables (never in code)

### Reliability
- **Uptime:** 99.9% availability
- **Error Handling:** Graceful degradation
- **Logging:** Structured JSON logs
- **Monitoring:** Health check endpoint
- **Recovery:** Automatic retry with exponential backoff

### Testing
- **Unit Tests:** pytest (85%+ coverage)
- **Integration Tests:** Test database interactions
- **API Tests:** Test all endpoints
- **Type Checking:** pyright or mypy (strict mode)

### Deployment
- **Environment:** Docker containers
- **Configuration:** Environment variables + .env files
- **Dependencies:** Locked with uv (pyproject.toml + uv.lock)
- **Health Check:** GET /health endpoint

## Dependencies

### Core Dependencies
```toml
[project]
name = "package-name"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.5.0",
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.0",
]
```

### Development Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
```

## API Specification

### Endpoints

#### POST /api/v1/records
**Purpose:** Create new record

**Request:**
```python
{
    "data": {"field1": "value1", "field2": 123},
    "validate": true
}
```

**Response (200):**
```python
{
    "id": "rec_123abc",
    "status": "pending",
    "created_at": "2025-01-15T10:30:00Z"
}
```

**Response (400):**
```python
{
    "error": "Validation failed",
    "details": ["field1 is required", "field2 must be positive"]
}
```

#### GET /api/v1/records/{id}
**Purpose:** Retrieve record by ID

**Response (200):**
```python
{
    "id": "rec_123abc",
    "data": {"field1": "value1", "field2": 123},
    "status": "completed",
    "created_at": "2025-01-15T10:30:00Z",
    "processed_at": "2025-01-15T10:31:00Z"
}
```

## Configuration

### Environment Variables
```bash
# Application
APP_NAME=my-app
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DB_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
```

### Configuration Files
- `pyproject.toml`: Package metadata and dependencies
- `.python-version`: Python version (3.10.0)
- `ruff.toml`: Linter configuration
- `mypy.ini`: Type checker configuration
- `pytest.ini`: Test configuration

## Error Handling

### Error Hierarchy
```python
class AppError(Exception):
    """Base application error."""
    pass

class ValidationError(AppError):
    """Validation failed."""
    pass

class NotFoundError(AppError):
    """Resource not found."""
    pass

class DatabaseError(AppError):
    """Database operation failed."""
    pass
```

### Error Response Format
```python
{
    "error": "ValidationError",
    "message": "Invalid input data",
    "details": {
        "field": "email",
        "constraint": "must be valid email format"
    },
    "request_id": "req_xyz789"
}
```

## Observability

### Logging
```python
import structlog

logger = structlog.get_logger()
logger.info("record_created", record_id="rec_123", user_id=456)
```

### Metrics
- Request count (by endpoint, status)
- Response time (p50, p95, p99)
- Error rate (by type)
- Database connection pool usage

### Tracing
- Request ID propagation
- Distributed tracing (OpenTelemetry)
- Performance profiling (py-spy)
EOF

cat > "$TEMPLATES_DIR/DESIGN-TEMPLATE.md" << 'EOF'
---
unit_id: "[###-slug]"
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
status: "draft"
interfaces_touched: []
data_shapes: []
---

# Unit Design Template

Stable intent and acceptance criteria for Python feature

## Objective

[1-2 sentence summary of what this unit accomplishes]

## Success Metrics

- [Metric 1 - e.g., Parse 10k CSV rows/second]
- [Metric 2 - e.g., Handle files up to 1GB]
- [Metric 3 - e.g., 99% parsing accuracy]

## Behavior

### Description
[Detailed description of expected behavior]

### Inputs

#### Parameter: `file_path`
- **Type:** `pathlib.Path`
- **Description:** Path to CSV file
- **Examples:**
  - `Path("data/users.csv")`
  - `Path("/tmp/import.csv")`
- **Constraints:** File must exist and be readable

#### Parameter: `encoding`
- **Type:** `str`
- **Description:** Character encoding
- **Default:** `"utf-8"`
- **Examples:** `"utf-8"`, `"latin-1"`, `"cp1252"`

### Outputs

#### Return: `List[Dict[str, Any]]`
- **Description:** Parsed records as dictionaries
- **Examples:**
  ```python
  [
      {"name": "Alice", "age": 30, "email": "alice@example.com"},
      {"name": "Bob", "age": 25, "email": "bob@example.com"}
  ]
  ```

### Edge Cases

#### Empty File
- **Scenario:** File exists but has no rows
- **Behavior:** Return empty list `[]`

#### Invalid Encoding
- **Scenario:** File cannot be decoded with specified encoding
- **Behavior:** Raise `ValueError` with descriptive message

#### Malformed CSV
- **Scenario:** Row has wrong number of columns
- **Behavior:** Log warning, skip row, continue processing

## Interfaces & Data

### Interfaces Touched
[List interfaces from spec.md that this unit implements or modifies]
- `parse_document` (implements)
- `validate_record` (uses)

### Data Shapes Used
[List entities from spec.md that this unit creates or manipulates]
- `Record` (creates)
- `User` (reads)

## Constraints

### Functional
- Must support CSV files with headers
- Must handle UTF-8 and Latin-1 encodings
- Must validate each row against schema

### Non-Functional
- **Performance:** Parse 10k rows in < 1 second
- **Memory:** Stream large files (don't load entire file)
- **Errors:** Provide clear error messages with line numbers

### Python-Specific
- Use `csv.DictReader` for parsing
- Use generators for memory efficiency
- Type hints required for all functions
- Follow PEP 8 naming conventions

## Acceptance Criteria

### AC-001-01: Parse Valid CSV
- **Given** a valid CSV file with headers
- **When** `parse_csv(file_path)` is called
- **Then** return list of dictionaries with correct values

### AC-001-02: Handle Empty File
- **Given** an empty CSV file
- **When** parsing is attempted
- **Then** return empty list without errors

### AC-001-03: Validate Against Schema
- **Given** a CSV file and validation schema
- **When** parsing with `validate=True`
- **Then** raise `ValidationError` for invalid rows

### AC-001-04: Stream Large Files
- **Given** a CSV file larger than 100MB
- **When** parsing is attempted
- **Then** process without exceeding 50MB memory usage

### AC-001-05: Error Messages
- **Given** a malformed CSV row
- **When** parsing encounters the error
- **Then** error message includes line number and description

## Dependencies

### Blocks This
[What can't start until this unit is done?]
- Unit 002-data-validation (requires parse_csv function)
- Unit 003-api-endpoint (requires Record entity)

### Blocked By
[What must be done before this can start?]
- None (foundational unit)

## Implementation Notes

### Approach
```python
from pathlib import Path
from typing import List, Dict, Any
import csv

def parse_csv(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False
) -> List[Dict[str, Any]]:
    """Parse CSV file into list of dictionaries.

    Args:
        file_path: Path to CSV file
        encoding: Character encoding
        validate: Whether to validate rows

    Returns:
        List of parsed records

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If encoding is invalid
    """
    records = []

    with open(file_path, encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if validate:
                # Validation logic here
                pass
            records.append(row)

    return records
```

### Testing Strategy
- Unit tests with pytest
- Fixtures for sample CSV files
- Parametrize tests for different encodings
- Test edge cases (empty, malformed, large files)
- Coverage target: 90%+ for this unit

### Test Examples
```python
def test_parse_valid_csv(tmp_path):
    """Test parsing valid CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")

    result = parse_csv(csv_file)

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == "30"

def test_parse_empty_csv(tmp_path):
    """Test parsing empty CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")

    result = parse_csv(csv_file)

    assert result == []
```

## References

### Spec References
- `spec.md#Interfaces#parse_document`
- `spec.md#Data Model#Record`

### PRD References
- `prd.md#User Stories#Story 1`

### External Documentation
- [Python csv module](https://docs.python.org/3/library/csv.html)
- [Pandas CSV parsing](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
EOF

cat > "$TEMPLATES_DIR/PLAN-TEMPLATE.md" << 'EOF'
---
unit_id: "[###-slug]"
version: "1.0"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
---

# Unit Plan Template

Volatile task breakdown and verification plan for Python unit

## Tasks

### TK-01
- **Title:** Set up module structure and type stubs
- **Description:** Create Python module files, __init__.py, and type stubs. Set up basic imports and exports.
- **Status:** ready
- **Priority:** high
- **Estimate:** 1h
- **Dependencies:** None
- **Completed:** null

### TK-02
- **Title:** Implement core parsing logic
- **Description:** Implement the main parse_csv function with CSV.DictReader. Handle file opening, encoding, and basic parsing.
- **Status:** ready
- **Priority:** high
- **Estimate:** 3h
- **Dependencies:** TK-01
- **Completed:** null

### TK-03
- **Title:** Add input validation
- **Description:** Add validation for file_path (exists, readable) and encoding (valid encoding name). Raise appropriate exceptions.
- **Status:** ready
- **Priority:** high
- **Estimate:** 2h
- **Dependencies:** TK-02
- **Completed:** null

### TK-04
- **Title:** Implement schema validation
- **Description:** Add optional schema validation logic using Pydantic or custom validation. Handle validation errors gracefully.
- **Status:** ready
- **Priority:** medium
- **Estimate:** 3h
- **Dependencies:** TK-03
- **Completed:** null

### TK-05
- **Title:** Write unit tests
- **Description:** Write comprehensive pytest tests for all functions. Use fixtures for test CSV files. Test happy paths and edge cases. Aim for 90%+ coverage.
- **Status:** ready
- **Priority:** high
- **Estimate:** 4h
- **Dependencies:** TK-04
- **Completed:** null

### TK-06
- **Title:** Add type hints and docstrings
- **Description:** Ensure all functions have complete type hints. Add Google-style docstrings with Args, Returns, Raises sections.
- **Status:** ready
- **Priority:** medium
- **Estimate:** 2h
- **Dependencies:** TK-05
- **Completed:** null

### TK-07
- **Title:** Performance optimization
- **Description:** Profile CSV parsing performance. Implement streaming for large files using generators. Ensure memory usage stays under 50MB.
- **Status:** ready
- **Priority:** low
- **Estimate:** 3h
- **Dependencies:** TK-06
- **Completed:** null

## Verification

### Commands

1. **uv run pytest tests/ -v** - Run all unit tests (must pass: ✅)
2. **uv run pytest --cov=src --cov-report=term** - Check test coverage (must be ≥ 85%: ✅)
3. **uv run pyright src/** - Type checking with pyright (must pass: ✅)
4. **uv run ruff check src/** - Linting (must pass: ✅)
5. **uv run ruff format --check src/** - Format checking (must pass: ✅)

### Gates

- **tests:** All pytest tests must pass ✅
- **type_check:** pyright must report zero errors ✅
- **coverage:** Coverage must be ≥ 85% ✅
- **linting:** ruff check must report zero errors ✅
- **formatting:** ruff format must report no changes needed ✅

### Coverage Target

85% (0.85)

### Acceptance References

- AC-001-01: Parse Valid CSV
- AC-001-02: Handle Empty File
- AC-001-03: Validate Against Schema
- AC-001-04: Stream Large Files
- AC-001-05: Error Messages

## Status

**Progress:** 0%

**Coverage:** N/A (update after running tests)

**Blockers:** None

**Notes:**

## Python-Specific Notes

### Package Structure
```
src/
├── package_name/
│   ├── __init__.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── csv_parser.py
│   └── validators/
│       ├── __init__.py
│       └── schema_validator.py
tests/
├── __init__.py
├── test_parsers/
│   ├── __init__.py
│   └── test_csv_parser.py
└── fixtures/
    ├── __init__.py
    └── sample_files.py
```

### Test Fixtures Example
```python
import pytest
from pathlib import Path

@pytest.fixture
def valid_csv_file(tmp_path: Path) -> Path:
    """Create a valid test CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "name,age,email\n"
        "Alice,30,alice@example.com\n"
        "Bob,25,bob@example.com\n"
    )
    return csv_file

@pytest.fixture
def empty_csv_file(tmp_path: Path) -> Path:
    """Create an empty test CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    return csv_file
```

### Type Hints Example
```python
from pathlib import Path
from typing import List, Dict, Any, Optional

def parse_csv(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False,
    schema: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Parse CSV file."""
    pass
```

### Performance Profiling
```bash
# Profile with py-spy
uv run py-spy record -o profile.svg -- python -m package_name.parsers.csv_parser

# Profile with cProfile
uv run python -m cProfile -o profile.stats -m package_name.parsers.csv_parser
```
EOF

# ============================================================================
# COMMAND FILES (Python-Optimized)
# ============================================================================

cat > "$CMD_DIR/constitution.md" << 'EOF'
---
name: constitution
description: Create Python Project Governance
---

# /constitution - Create Python Project Governance

## Purpose
Establish non-negotiable Python development principles, quality bars, and constraints.

## Usage
```
/constitution
```

## Prerequisites
- None (this is typically the first command to run)

## Process

### Step 1: Gather Information
Ask the user about:
- Python version requirements (minimum 3.10+)
- Code quality standards (PEP 8, type hints, docstrings)
- Testing requirements (coverage target, pytest)
- Type checking preferences (mypy vs pyright)
- Performance constraints
- Security requirements

### Step 2: Define Principles
Establish:
- **KISS:** Simple, readable Python code
- **YAGNI:** Build only what's needed
- **Type Safety:** Comprehensive type hints
- **Testing:** pytest with high coverage

### Step 3: Set Quality Bars
Define measurable standards:
- Coverage target (default: 85%)
- Type checking strictness
- Code formatting (ruff)
- Linting rules (ruff)

### Step 4: Document Constraints
Capture:
- Python version (e.g., 3.10+)
- Package manager (UV)
- Project structure (src/ layout)
- Dependency management

### Step 5: Create Constitution
Generate `spec/constitution.md` using CONSTITUTION-TEMPLATE.md with:
- All gathered information
- Python-specific sections
- UV workflow commands
- pytest and type checking requirements

### Step 6: Validate
Check that:
- File created at correct path
- All sections populated
- Quality bars are measurable
- Constraints are specific

### Step 7: Confirm
Display summary and next steps

## Output
- **File:** `spec/constitution.md`
- **Status:** Active governance document

## Next Steps
Run `/prd` to capture product requirements
EOF

cat > "$CMD_DIR/prd.md" << 'EOF'
---
name: prd
description: Create Python Product Requirements
---

# /prd - Create Python Product Requirements

## Purpose
Capture product requirements, user stories, and success metrics for Python project.

## Usage
```
/prd
```

## Prerequisites
- `spec/constitution.md` should exist (run `/constitution` first)

## Process

### Step 1: Problem Statement
Ask user to describe:
- Current situation and pain points
- Desired state
- Gap analysis

### Step 2: Goals and Metrics
Define:
- Primary objectives
- Success metrics (performance, throughput, latency)
- Measurable outcomes

### Step 3: Scope Definition
Document:
- In scope features
- Out of scope features
- Future considerations

### Step 4: User Stories
Capture user stories in format:
- As a [user type]
- I want [goal]
- So that [benefit]
- With acceptance criteria (Given/When/Then)

### Step 5: Python-Specific Requirements
Document:
- Performance requirements (throughput, latency, memory)
- Integration points (APIs, databases, message queues)
- Data requirements (formats, volume, retention)
- Deployment constraints

### Step 6: Technical Constraints
Capture:
- Python version requirements
- Core dependencies
- Deployment environment
- Configuration needs

### Step 7: Risks and Timeline
Document:
- Known risks and mitigations
- Assumptions
- Phased timeline

### Step 8: Create PRD
Generate `spec/prd.md` using PRD-TEMPLATE.md

### Step 9: Validate
Check that:
- All user stories have acceptance criteria
- Success metrics are measurable
- Python-specific sections populated
- Technical constraints documented

### Step 10: Confirm
Display summary and next steps

## Output
- **File:** `spec/prd.md`
- **Status:** Product requirements captured

## Next Steps
Run `/spec` to create technical specification
EOF

cat > "$CMD_DIR/spec.md" << 'EOF'
---
name: spec
description: Create Python Technical Specification
---

# /spec - Create Python Technical Specification

## Purpose
Produce the engineering contract: architecture, interfaces, data models, and NFRs for Python implementation.

## Usage
```
/spec
```

## Prerequisites
- `spec/constitution.md` should exist
- `spec/prd.md` should exist

## Process

### Step 1: Architecture Design
Define:
- System overview and component diagram
- Technology stack (Python 3.10+, frameworks, databases)
- Project structure (src/ layout)
- Package organization

### Step 2: Interface Definitions
For each interface:
- Function signature with full type hints
- Purpose and behavior
- Parameters (name, type, description, examples)
- Return values (type, description, examples)
- Exceptions raised
- Docstring (Google or NumPy style)

**Example:**
```python
from pathlib import Path
from typing import Optional

def parse_document(
    file_path: Path,
    encoding: str = "utf-8"
) -> Optional[Document]:
    """Parse document from file.

    Args:
        file_path: Path to document file
        encoding: Character encoding

    Returns:
        Parsed Document or None if parsing fails

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    pass
```

### Step 3: Data Models
For each entity:
- Define using dataclass or Pydantic model
- List all fields with types
- Document constraints (unique, indexed, length limits)
- Show examples

**Example:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """User entity."""
    id: int
    email: str
    name: str
    created_at: datetime
```

### Step 4: Non-Functional Requirements
Document:
- **Performance:** Response times, throughput, memory limits
- **Scalability:** Horizontal scaling, concurrency model
- **Security:** Authentication, authorization, input validation
- **Reliability:** Uptime, error handling, retry logic
- **Testing:** Coverage targets, test types
- **Deployment:** Environment, configuration, health checks

### Step 5: Dependencies
List:
- Core dependencies (with version constraints)
- Development dependencies
- Optional dependencies

### Step 6: API Specification
For each endpoint:
- HTTP method and path
- Purpose
- Request format (with examples)
- Response formats (success and error cases)
- Status codes

### Step 7: Configuration
Document:
- Environment variables
- Configuration files (pyproject.toml, .env, etc.)
- Default values

### Step 8: Error Handling
Define:
- Error hierarchy
- Error response format
- Logging strategy

### Step 9: Observability
Plan:
- Logging (structured logs with structlog)
- Metrics (request count, latency, errors)
- Tracing (request IDs, distributed tracing)

### Step 10: Create Spec
Generate `spec/spec.md` using SPEC-TEMPLATE.md with all gathered information

### Step 11: Validate
Check that:
- All interfaces have complete type hints
- All entities have field descriptions
- NFRs are measurable
- API endpoints documented
- Dependencies listed with versions

### Step 12: Confirm
Display summary:
- Number of interfaces defined
- Number of entities defined
- Key NFRs established
- Next step: Run `/new SLUG` to create first unit

## Output
- **File:** `spec/spec.md`
- **Status:** Engineering contract established

## Validation
- ✅ Architecture diagram present
- ✅ All interfaces have type hints
- ✅ All entities use dataclass or Pydantic
- ✅ NFRs are measurable
- ✅ Dependencies include versions

## Next Steps
Run `/new SLUG` to create your first development unit
EOF

cat > "$CMD_DIR/new.md" << 'EOF'
---
name: new
description: Create New Python Unit
---

# /new - Create New Python Unit

## Purpose
Create a new development unit (feature) with design document for Python implementation.

## Usage
```
/new <slug>
```

**Example:**
```
/new csv-parser
/new user-authentication
/new data-validation
```

## Prerequisites
- `spec/spec.md` should exist (run `/spec` first)

## Process

### Step 1: Determine Unit Number
- Scan `spec/units/` directory
- Find highest existing unit number (###)
- Increment by 1 for new unit

### Step 2: Create Directory
Create `spec/units/###-SLUG/` directory

### Step 3: Gather Design Information
Ask user about:
- **Objective:** What does this unit accomplish?
- **Success Metrics:** How do we measure completion?
- **Behavior:** What is the expected behavior?
- **Inputs/Outputs:** Function signatures with types
- **Edge Cases:** What edge cases need handling?

### Step 4: Python Interface Design
For each function:
- Function name (snake_case)
- Type hints for all parameters
- Return type hint
- Docstring (Google or NumPy style)
- Examples

**Example:**
```python
from pathlib import Path
from typing import List, Dict, Any

def parse_csv(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False
) -> List[Dict[str, Any]]:
    """Parse CSV file into list of dictionaries.

    Args:
        file_path: Path to CSV file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate rows

    Returns:
        List of parsed records as dictionaries

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If encoding is invalid
    """
    pass
```

### Step 5: Interface & Data References
Ask:
- Which interfaces from spec.md does this touch?
- Which entities from spec.md does this use?
- **Validate:** All references exist in spec.md

### Step 6: Constraints
Document:
- Functional constraints
- Non-functional constraints (performance, memory)
- Python-specific constraints (use generators, async/await, etc.)

### Step 7: Acceptance Criteria
Define testable criteria in Given-When-Then format:

**Example:**
- **AC-001-01:** Parse Valid CSV
  - Given: A valid CSV file with headers
  - When: parse_csv() is called
  - Then: Return list of dicts with correct values

Assign IDs: AC-[UNIT]-01, AC-[UNIT]-02, etc.

### Step 8: Dependencies
Document:
- What blocks this unit?
- What does this unit block?

### Step 9: Implementation Notes
Add:
- Suggested approach with code examples
- Testing strategy (pytest fixtures, parametrize)
- Test examples
- Coverage target for this unit

### Step 10: Validate References
For each interface/entity referenced:
- Verify it exists in `spec/spec.md`
- If not found, warn user:
  - Update spec.md first, or
  - Revise design to use existing references

### Step 11: Generate Design
Create `spec/units/###-SLUG/design.md` with:
- All gathered information
- Status: "draft"
- Timestamps
- Python-specific sections

### Step 12: Validate Design
Check that:
- Directory created with correct numbering
- design.md exists and is valid Markdown
- All spec.md references are valid
- Acceptance criteria are testable
- Type hints are complete
- All required fields present

### Step 13: Confirm
Display summary:
- Unit created: ###-SLUG
- Interfaces touched: [list]
- Entities used: [list]
- Acceptance criteria count
- Next step: Run `/plan SLUG` to generate task breakdown

## Output
- **Directory:** `spec/units/###-SLUG/`
- **File:** `spec/units/###-SLUG/design.md`
- **Status:** draft

## Example Interaction
```
User: /new csv-parser

Claude: Creating new unit for CSV parser. This will be unit 001.

What is the objective? (1-2 sentences)
User: Parse CSV files into structured dictionaries for data processing

What success metrics define completion?
User: Parse 10k rows/second, handle files up to 1GB, 99% accuracy

[Gathering interface design...]

Which interfaces from spec.md does this implement?
User: parse_document

Which entities does this create?
User: Record

Checking references against spec.md...
✅ Interface 'parse_document' exists in spec.md
✅ Entity 'Record' exists in spec.md

Unit created: spec/units/001-csv-parser/
- Status: draft
- Interfaces: parse_document
- Entities: Record
- Acceptance criteria: 5 (AC-001-01 through AC-001-05)
- Type hints: Complete

Next step: Run `/plan csv-parser` to generate task breakdown
```

## Validation
- ✅ Directory created: `spec/units/###-SLUG/`
- ✅ design.md exists with valid Markdown
- ✅ All spec.md references are valid
- ✅ All functions have type hints
- ✅ Acceptance criteria in Given-When-Then format
- ✅ Test examples provided
- ✅ Status is "draft"

## Next Steps
Run `/plan SLUG` to break down the design into implementation tasks
EOF

cat > "$CMD_DIR/plan.md" << 'EOF'
---
name: plan
description: Generate Python Unit Plan
---

# /plan - Generate Python Unit Plan

## Purpose
Generate task breakdown and verification plan from design document.

## Usage
```
/plan <slug>
```

**Example:**
```
/plan csv-parser
/plan user-authentication
```

## Prerequisites
- `spec/units/###-SLUG/design.md` must exist (run `/new SLUG` first)

## Process

### Step 1: Locate Unit
- Find unit directory matching SLUG
- Load `design.md`
- Extract objective, behavior, acceptance criteria

### Step 2: Break Down Into Tasks
Generate granular tasks for Python implementation:

**Common Task Pattern:**
1. Set up module structure and type stubs
2. Implement core logic
3. Add input validation
4. Handle edge cases
5. Write unit tests with pytest
6. Add type hints and docstrings
7. Performance optimization (if needed)

### Step 3: Define Task Details
For each task:
- **Title:** Clear, action-oriented
- **Description:** What needs to be done
- **Status:** ready/doing/done/blocked
- **Priority:** high/medium/low
- **Estimate:** Time estimate (1h, 3h, 1d)
- **Dependencies:** Which tasks must finish first
- **Completed:** Date when done (YYYY-MM-DD)

### Step 4: Verification Commands
Define Python-specific verification:

**Required commands:**
```bash
# Tests
uv run pytest tests/ -v

# Coverage
uv run pytest --cov=src --cov-report=term

# Type checking
uv run pyright src/
# OR
uv run mypy src/

# Linting
uv run ruff check src/

# Formatting
uv run ruff format --check src/
```

### Step 5: Verification Gates
Define pass criteria:
- **tests:** All pytest tests must pass ✅
- **type_check:** Zero type errors ✅
- **coverage:** Must be ≥ constitution target ✅
- **linting:** Zero linting errors ✅
- **formatting:** No format changes needed ✅

### Step 6: Coverage Target
Extract from constitution.md (default: 85%)

### Step 7: Acceptance References
Link to acceptance criteria from design.md:
- AC-[UNIT]-01
- AC-[UNIT]-02
- etc.

### Step 8: Python-Specific Notes
Add:
- Package structure (src/, tests/)
- Test fixtures examples
- Type hints examples
- Performance profiling commands

### Step 9: Generate Plan
Create `spec/units/###-SLUG/plan.md` with:
- Task breakdown
- Verification commands
- Gates and coverage target
- Status tracking (progress, blockers)
- Python-specific notes

### Step 10: Validate Plan
Check that:
- All tasks have estimates
- Dependencies are valid (no cycles)
- Verification commands use UV
- All acceptance criteria covered
- Python structure documented

### Step 11: Update Design Status
Change `design.md` status from "draft" to "planned"

### Step 12: Confirm
Display summary:
- Task count
- Total estimated time
- Verification gates
- Next step: Run `/work SLUG TK-##` to start first task

## Output
- **File:** `spec/units/###-SLUG/plan.md`
- **Status:** Ready for implementation

## Example Interaction
```
User: /plan csv-parser

Claude: Loading design for unit 001-csv-parser...

Generated 7 tasks:
1. TK-01: Set up module structure (1h)
2. TK-02: Implement core parsing logic (3h)
3. TK-03: Add input validation (2h)
4. TK-04: Implement schema validation (3h)
5. TK-05: Write unit tests (4h)
6. TK-06: Add type hints and docstrings (2h)
7. TK-07: Performance optimization (3h)

Total estimate: 18 hours

Verification gates:
✅ Tests (uv run pytest tests/ -v)
✅ Coverage ≥ 85% (uv run pytest --cov=src)
✅ Type check (uv run pyright src/)
✅ Linting (uv run ruff check src/)
✅ Formatting (uv run ruff format --check src/)

Plan created: spec/units/001-csv-parser/plan.md
Design status updated: draft → planned

Next step: Run `/work csv-parser TK-01` to start first task
```

## Validation
- ✅ plan.md created in unit directory
- ✅ All tasks have estimates and priorities
- ✅ Dependencies form valid DAG (no cycles)
- ✅ Verification commands use UV
- ✅ Coverage target matches constitution
- ✅ All acceptance criteria referenced

## Next Steps
Run `/work SLUG TK-##` to implement first task with UPEVD pattern
EOF

cat > "$CMD_DIR/work.md" << 'EOF'
---
name: work
description: Execute Python Task (UPEVD Pattern)
---

# /work - Execute Python Task (UPEVD Pattern)

## Purpose
Implement a specific task following the UPEVD workflow:
**U**nderstand → **P**lan → **E**xecute → **V**alidate → **D**ocument

## Usage
```
/work <slug> [task-id]
```

**Examples:**
```
/work csv-parser TK-01
/work user-authentication TK-03
/work csv-parser  # Work on next ready task
```

## Prerequisites
- `spec/units/###-SLUG/plan.md` must exist (run `/plan SLUG` first)
- If task-id omitted, will select next "ready" task

## Process: UPEVD Workflow

### U - Understand (Load Context)

#### Step U1: Load Unit Context
- Read `design.md` for objective and acceptance criteria
- Read `plan.md` for task breakdown
- Identify the specific task to work on

#### Step U2: Check Dependencies
- Verify all dependency tasks are "done"
- If dependencies not met, suggest completing them first
- Update task status to "doing"

#### Step U3: Load Python Environment
- Check for `pyproject.toml` and dependencies
- Verify UV is available
- Note relevant type hints and interfaces from spec.md

#### Step U4: Regenerate State
- Run state-tracker.py to update state.json
- Review current project state

### P - Plan (Develop Strategy)

#### Step P1: Review Task Requirements
- Understand what code needs to be written
- Identify modules/functions to create or modify
- Note testing requirements

#### Step P2: Identify Risks
- What could go wrong?
- What edge cases need handling?
- What performance concerns exist?

#### Step P3: Outline Approach
Present approach to user:
```
Task: TK-02 - Implement core parsing logic

Approach:
1. Create src/package_name/parsers/csv_parser.py
2. Implement parse_csv() function with type hints
3. Use csv.DictReader for parsing
4. Handle encoding parameter
5. Add error handling for FileNotFoundError
6. Write docstring with Args, Returns, Raises

Files to create/modify:
- src/package_name/parsers/csv_parser.py (create)
- src/package_name/parsers/__init__.py (update exports)

Tests to write:
- tests/test_parsers/test_csv_parser.py

Estimated time: 3h
```

### E - Execute (Implement)

#### Step E1: Create/Modify Python Code
Write implementation with:
- **Complete type hints** for all functions
- **Google or NumPy style docstrings**
- **PEP 8 compliant** naming and structure
- **Error handling** with specific exceptions
- **Input validation** for parameters

**Example:**
```python
from pathlib import Path
from typing import List, Dict, Any
import csv

def parse_csv(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False
) -> List[Dict[str, Any]]:
    """Parse CSV file into list of dictionaries.

    Args:
        file_path: Path to CSV file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate rows against schema

    Returns:
        List of parsed records as dictionaries

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If encoding is invalid or file is malformed
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    records = []
    try:
        with open(file_path, encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if validate:
                    # Validation logic
                    pass
                records.append(row)
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid encoding '{encoding}': {e}")

    return records
```

#### Step E2: Write Tests
Create pytest tests with:
- **Fixtures** for test data (use tmp_path)
- **Parametrize** for multiple test cases
- **Coverage** of happy paths and edge cases
- **Clear test names** describing what is tested

**Example:**
```python
import pytest
from pathlib import Path
from package_name.parsers.csv_parser import parse_csv

@pytest.fixture
def valid_csv(tmp_path: Path) -> Path:
    """Create valid test CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "name,age,email\n"
        "Alice,30,alice@example.com\n"
        "Bob,25,bob@example.com\n"
    )
    return csv_file

def test_parse_valid_csv(valid_csv):
    """Test parsing valid CSV file."""
    result = parse_csv(valid_csv)

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == "30"
    assert result[1]["name"] == "Bob"

def test_parse_nonexistent_file():
    """Test error when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        parse_csv(Path("nonexistent.csv"))

@pytest.mark.parametrize("encoding", ["utf-8", "latin-1", "cp1252"])
def test_parse_different_encodings(tmp_path, encoding):
    """Test parsing with different encodings."""
    csv_file = tmp_path / f"test_{encoding}.csv"
    csv_file.write_text("name\nAlice\n", encoding=encoding)

    result = parse_csv(csv_file, encoding=encoding)
    assert len(result) == 1
```

#### Step E3: Follow Best Practices
- Use **generators** for memory efficiency (large files)
- Use **async/await** for I/O-bound operations (if applicable)
- Use **dataclasses** or **Pydantic** for data structures
- Follow **constitution** principles

### V - Validate (Run Verification)

#### Step V1: Run Tests
```bash
uv run pytest tests/ -v
```
**Gate:** All tests must pass ✅

#### Step V2: Check Coverage
```bash
uv run pytest --cov=src --cov-report=term-missing
```
**Gate:** Coverage must be ≥ target (e.g., 85%) ✅

#### Step V3: Type Check
```bash
uv run pyright src/
# OR
uv run mypy src/
```
**Gate:** Zero type errors ✅

#### Step V4: Lint
```bash
uv run ruff check src/
```
**Gate:** Zero linting errors ✅

#### Step V5: Format Check
```bash
uv run ruff format --check src/
```
**Gate:** No formatting changes needed ✅

#### Step V6: Verify Acceptance Criteria
Check that task satisfies relevant acceptance criteria from design.md

### D - Document (Update State)

#### Step D1: Update Task Status
In `plan.md`:
- Change task status: "doing" → "done"
- Set completed date: YYYY-MM-DD
- Update progress percentage

#### Step D2: Update Coverage
If tests were run, update **Coverage** field in Status section with actual coverage

#### Step D3: Recalculate Progress
```
Progress = (completed_tasks / total_tasks) * 100
```

#### Step D4: Update CLAUDE.md
Add to working memory:
- What was implemented
- Key decisions made
- Any learnings or gotchas
- What's next

#### Step D5: Regenerate State
Run state-tracker.py to update state.json

#### Step D6: Confirm Completion
Display summary:
```
✅ Task TK-02 completed

Implementation:
- Created src/package_name/parsers/csv_parser.py
- Implemented parse_csv() with full type hints
- Added comprehensive error handling

Tests:
- Wrote 8 tests in test_csv_parser.py
- All tests passing ✅
- Coverage: 92% ✅

Verification:
✅ Tests passed (8/8)
✅ Coverage: 92% (target: 85%)
✅ Type check: 0 errors
✅ Linting: 0 errors
✅ Formatting: compliant

Updated:
- plan.md: TK-02 status → done
- Progress: 28% → 42%
- CLAUDE.md: Added implementation notes

Next task: TK-03 - Add input validation
```

## Output
- **Code:** Implementation files created/modified
- **Tests:** Test files created/modified
- **Plan:** Task status updated to "done"
- **Coverage:** Actual coverage recorded
- **Memory:** CLAUDE.md updated with learnings

## Validation Checklist
- ✅ All verification gates passed
- ✅ Type hints complete for all functions
- ✅ Docstrings present (Google/NumPy style)
- ✅ Tests written and passing
- ✅ Coverage meets or exceeds target
- ✅ plan.md updated with completion date
- ✅ CLAUDE.md updated with notes
- ✅ state.json regenerated

## Next Steps
- If more tasks remain: `/work SLUG TK-##` for next task
- If all tasks done: `/verify SLUG` to run full verification
EOF

cat > "$CMD_DIR/verify.md" << 'EOF'
---
name: verify
description: Run Python Verification Gates
---

# /verify - Run Python Verification Gates

## Purpose
Run all verification gates defined in unit plan to ensure implementation meets quality standards.

## Usage
```
/verify <slug>
```

**Example:**
```
/verify csv-parser
/verify user-authentication
```

## Prerequisites
- `spec/units/###-SLUG/plan.md` must exist
- All tasks in plan should be "done"

## Process

### Step 1: Load Plan
- Read `plan.md` for unit ###-SLUG
- Extract verification commands
- Extract verification gates
- Extract coverage target

### Step 2: Check Task Completion
- Count tasks with status="done"
- If incomplete tasks exist, warn user:
  ```
  ⚠️ Warning: 2 tasks still incomplete
  - TK-05: Write unit tests (ready)
  - TK-07: Performance optimization (blocked)

  Continue verification anyway? [y/N]
  ```

### Step 3: Run Verification Commands
Execute each command from plan.md in order:

#### Command 1: Run Tests
```bash
uv run pytest tests/ -v
```
- Capture output
- Check exit code
- Gate: Must pass (exit code 0) ✅

#### Command 2: Check Coverage
```bash
uv run pytest --cov=src --cov-report=term-missing --cov-report=html
```
- Parse coverage percentage
- Compare to target from plan.md
- Gate: Coverage ≥ target ✅

#### Command 3: Type Check
```bash
uv run pyright src/
# OR
uv run mypy src/
```
- Capture error count
- Gate: Zero type errors ✅

#### Command 4: Linting
```bash
uv run ruff check src/
```
- Capture error/warning count
- Gate: Zero errors ✅

#### Command 5: Format Check
```bash
uv run ruff format --check src/
```
- Check if reformatting needed
- Gate: No changes needed ✅

### Step 4: Additional Python Checks
Run optional but recommended checks:

#### Security Audit
```bash
uv pip audit
```
- Check for known vulnerabilities
- Report findings (not a gate, but informational)

#### Import Order
```bash
uv run ruff check --select I src/
```
- Verify import organization (handled by ruff)

### Step 5: Evaluate Gates
For each gate in plan.md:
- **tests:** Did all tests pass?
- **type_check:** Zero type errors?
- **coverage:** Met or exceeded target?
- **linting:** Zero linting errors?
- **formatting:** No formatting changes?

### Step 6: Validate Acceptance Criteria
For each acceptance criterion in design.md:
- Which test(s) verify this criterion?
- Are those tests passing?
- Mark criteria as verified ✅ or failed ❌

### Step 7: Update Plan
In `plan.md`:
- Update **Coverage** in Status section with actual value
- Update **Blockers** if any gates failed
- Add verification timestamp

### Step 8: Generate Report
Create comprehensive verification report:

```
Verification Report: Unit 001-csv-parser
Generated: 2025-01-15 10:30:00

Task Completion:
✅ 7/7 tasks completed (100%)

Verification Commands:
✅ pytest tests/ -v (8 passed)
✅ pytest --cov (Coverage: 92%)
✅ pyright src/ (0 errors)
✅ ruff check src/ (0 errors)
✅ ruff format --check src/ (compliant)

Gates:
✅ tests: PASSED (8/8 tests passing)
✅ type_check: PASSED (0 errors)
✅ coverage: PASSED (92% ≥ 85% target)
✅ linting: PASSED (0 errors)
✅ formatting: PASSED (no changes needed)

Acceptance Criteria:
✅ AC-001-01: Parse Valid CSV (verified by test_parse_valid_csv)
✅ AC-001-02: Handle Empty File (verified by test_parse_empty_csv)
✅ AC-001-03: Validate Against Schema (verified by test_validate_schema)
✅ AC-001-04: Stream Large Files (verified by test_large_file_memory)
✅ AC-001-05: Error Messages (verified by test_error_messages)

Additional Checks:
ℹ️  Security Audit: 0 known vulnerabilities
ℹ️  Import Order: Compliant

Result: ✅ ALL GATES PASSED

Coverage Report:
HTML coverage report generated: htmlcov/index.html
View with: open htmlcov/index.html

Unit 001-csv-parser is ready for integration.
```

### Step 9: Update CLAUDE.md
Add verification results to working memory:
- Verification timestamp
- All gates passed/failed
- Actual coverage achieved
- Any issues found

### Step 10: Suggest Next Steps
If all gates passed:
```
✅ Unit verification complete!

Next steps:
- Review implementation for final polish
- Run /check to validate alignment with spec.md
- Integrate with other units
- Consider /reflect to capture learnings
```

If any gates failed:
```
❌ Verification failed

Failed gates:
- coverage: 78% < 85% target

Required actions:
1. Run /work csv-parser to add more tests
2. Focus on uncovered lines (see htmlcov/index.html)
3. Re-run /verify csv-parser when ready
```

## Output
- **Console:** Comprehensive verification report
- **HTML:** Coverage report (htmlcov/index.html)
- **Updated:** plan.md with actual coverage
- **Updated:** CLAUDE.md with verification results

## Validation
- ✅ All verification commands executed
- ✅ All gates evaluated
- ✅ Acceptance criteria checked
- ✅ Coverage report generated
- ✅ plan.md updated
- ✅ CLAUDE.md updated

## Next Steps
- If passed: Run `/check` to validate alignment
- If failed: Run `/work SLUG` to fix issues, then re-verify
EOF

cat > "$CMD_DIR/check.md" << 'EOF'
---
name: check
description: Validate Python Project Alignment
---

# /check - Validate Python Project Alignment

## Purpose
Validate alignment across project documents, detect drift, and ensure Python code matches specifications.

## Usage
```
/check [slug]
/check          # Check entire project
/check csv-parser  # Check specific unit
```

## Prerequisites
- At least one of: constitution.md, prd.md, spec.md should exist

## Process

### Step 1: Load State
Run state-tracker.py to generate current state.json

### Step 2: Validate L1 Documents

#### Check Constitution
- Does `spec/constitution.md` exist?
- Is version specified?
- Are quality bars measurable?
- Is Python version specified?
- Is UV usage documented?

#### Check PRD
- Does `spec/prd.md` exist?
- Are user stories complete (As/Want/So)?
- Do acceptance criteria use Given/When/Then?
- Are Python-specific requirements documented?
- Are performance metrics measurable?

#### Check Spec
- Does `spec/spec.md` exist?
- Are all interfaces defined with type hints?
- Are all entities defined (dataclass or Pydantic)?
- Are NFRs measurable?
- Is pyproject.toml structure documented?

### Step 3: Validate References

#### Interface References
For each unit design.md:
- Extract `interfaces_touched` list
- For each interface:
  - Does it exist in spec.md?
  - If not, report invalid reference ❌

#### Entity References
For each unit design.md:
- Extract `data_shapes` list
- For each entity:
  - Does it exist in spec.md?
  - If not, report invalid reference ❌

### Step 4: Validate Code Alignment

#### Check Module Structure
For each unit:
- Does the module exist in src/?
- Do the functions match interface signatures?
- Are type hints present?
- Are docstrings present?

#### Check Type Hints
For each function in spec.md interfaces:
- Does implementation have matching type hints?
- Are return types correct?
- Are parameter types correct?

**Example Check:**
```
Spec: def parse_csv(file_path: Path, encoding: str) -> List[Dict[str, Any]]
Code: def parse_csv(file_path: Path, encoding: str) -> List[Dict[str, Any]]
Result: ✅ Type hints match
```

#### Check Entities
For each entity in spec.md:
- Does implementation exist?
- Are fields correct?
- Are types correct?

**Example Check:**
```
Spec Entity: User(id: int, email: str, name: str)
Code Entity: User(id: int, email: str, name: str, created_at: datetime)
Result: ⚠️ Code has additional field 'created_at'
```

### Step 5: Check Constitution Compliance

#### Coverage Compliance
For each unit with actual_coverage:
- Compare to constitution coverage_target
- If below target, report violation ❌

#### Quality Bar Compliance
Check:
- Are all public functions type-hinted?
- Are all public functions documented?
- Does linting pass?
- Does type checking pass?

### Step 6: Detect Code Drift

#### Interface Drift
For each interface in spec.md:
- Find implementation in src/
- Compare signatures
- Report differences:
  - Missing parameters
  - Extra parameters
  - Type mismatches
  - Return type mismatches

#### Entity Drift
For each entity in spec.md:
- Find dataclass/Pydantic model in src/
- Compare fields
- Report differences:
  - Missing fields
  - Extra fields
  - Type mismatches

### Step 7: Check Test Coverage

For each unit:
- Does test file exist?
- Does test coverage meet target?
- Are all acceptance criteria tested?

**Example Check:**
```
Unit: 001-csv-parser
Design AC: 5 acceptance criteria
Tests: test_csv_parser.py (8 tests)
Coverage: 92% ≥ 85% ✅

AC-001-01: ✅ Tested (test_parse_valid_csv)
AC-001-02: ✅ Tested (test_parse_empty_csv)
AC-001-03: ✅ Tested (test_validate_schema)
AC-001-04: ✅ Tested (test_large_file_memory)
AC-001-05: ✅ Tested (test_error_messages)
```

### Step 8: Generate Validation Report

Create comprehensive alignment report:

```
Alignment Validation Report
Generated: 2025-01-15 10:30:00

L1 Documents:
✅ constitution.md (v1.0, Python 3.10+, UV usage documented)
✅ prd.md (v1.0, 5 user stories, all complete)
✅ spec.md (v1.0, 8 interfaces, 4 entities)

Reference Validation:
✅ All interface references valid (0 issues)
✅ All entity references valid (0 issues)

Code Alignment:
✅ Interface signatures match (8/8)
⚠️ Entity drift detected (1 issue):
  - User entity: Code has extra field 'last_login' not in spec

Constitution Compliance:
✅ Coverage targets met (2/2 units)
✅ Type hints complete (100%)
✅ Docstrings present (100%)

Test Coverage:
✅ Unit 001-csv-parser: 92% ≥ 85% target
✅ Unit 002-validator: 88% ≥ 85% target

Recommendations:
1. Update spec.md User entity to include 'last_login' field
2. All critical alignment checks passed

Overall: ✅ PROJECT ALIGNED
```

### Step 9: Update CLAUDE.md
Add validation results to working memory:
- Timestamp
- Issues found
- Recommendations
- Next actions

### Step 10: Suggest Fixes
For each issue:
- Describe the problem
- Suggest fix (update spec vs update code)
- Provide command to fix

**Example:**
```
Issue: Entity drift detected
  Spec: User(id, email, name)
  Code: User(id, email, name, created_at, last_login)

Recommendation:
Update spec.md to include new fields:

### Entity: [User]
```python
@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime  # ADD THIS
    last_login: Optional[datetime] = None  # ADD THIS
```

Then run: /check to verify alignment
```

## Output
- **Console:** Validation report
- **Updated:** CLAUDE.md with findings
- **Suggestions:** Specific fixes for issues

## Validation Types

### Critical Issues (Must Fix)
- Invalid interface references
- Invalid entity references
- Coverage below target
- Type hint mismatches

### Warnings (Should Fix)
- Entity drift (extra fields)
- Interface drift (compatible changes)
- Missing docstrings

### Informational
- Suggested improvements
- Best practice recommendations

## Next Steps
- If issues found: Run `/update` to fix alignment
- If aligned: Run `/reflect` to capture learnings
- Continue development: Run `/new SLUG` for next unit
EOF

cat > "$CMD_DIR/update.md" << 'EOF'
---
name: update
description: Update Python Project Documents
---

# /update - Update Python Project Documents

## Purpose
Apply coordinated updates across project artifacts (constitution, prd, spec, designs, plans) to maintain alignment.

## Usage
```
/update <document> <path>
/update spec interfaces#parse_document
/update spec entities#User
/update prd user-stories
/update constitution quality-bars
```

## Prerequisites
- Target document must exist
- Should run `/check` first to identify what needs updating

## Process

### Step 1: Parse Update Target
Extract:
- Document name (constitution, prd, spec, design, plan)
- Section path (e.g., interfaces#parse_document)
- Unit slug (if updating unit-specific docs)

### Step 2: Load Current Content
- Read target document
- Parse Markdown structure
- Locate target section

### Step 3: Gather Update Information
Ask user:
- What needs to change?
- Why is this change needed?
- What's the new value/content?

### Step 4: Validate Python Syntax
If updating Python code sections:

#### For Interfaces
Verify:
- Function signature has complete type hints
- Docstring follows Google/NumPy style
- Parameters documented with types
- Return type documented
- Exceptions documented

**Example:**
```python
from pathlib import Path
from typing import List, Dict, Any, Optional

def parse_document(
    file_path: Path,
    encoding: str = "utf-8",
    validate: bool = False,
    schema: Optional[Dict[str, Any]] = None  # NEW PARAMETER
) -> List[Dict[str, Any]]:
    """Parse document from file.

    Args:
        file_path: Path to document file
        encoding: Character encoding (default: utf-8)
        validate: Whether to validate against schema
        schema: Validation schema (required if validate=True)  # NEW

    Returns:
        List of parsed records

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If validation fails or schema invalid  # UPDATED
    """
    pass
```

#### For Entities
Verify:
- Uses dataclass or Pydantic BaseModel
- All fields have type hints
- Field descriptions documented
- Constraints specified

**Example:**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User entity."""
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None  # NEW FIELD
```

### Step 5: Apply Update
- Modify target document
- Update version number
- Update timestamp
- Add change note (if applicable)

### Step 6: Propagate Changes

#### If Updating spec.md Interface
Propagate to:
1. **Affected unit designs:** Update interfaces_touched
2. **Code implementation:** Flag for update
3. **Tests:** Flag for review

#### If Updating spec.md Entity
Propagate to:
1. **Affected unit designs:** Update data_shapes
2. **Data models:** Flag for update
3. **Database migrations:** Flag for creation

#### If Updating Constitution Quality Bars
Propagate to:
1. **All unit plans:** Update coverage target
2. **CI configuration:** Update thresholds
3. **CLAUDE.md:** Document change

### Step 7: Identify Impacted Units
Scan all units to find:
- Which designs reference updated interface/entity?
- Which plans need verification commands updated?
- Which implementations need code changes?

### Step 8: Create Update Checklist
Generate checklist of required changes:

```
Update Checklist for spec.md Interface: parse_document

Spec Changes:
✅ Updated parse_document signature (added schema parameter)
✅ Updated docstring
✅ Incremented version: 1.0 → 1.1

Propagation Required:
⬜ Unit 001-csv-parser design.md (references parse_document)
  - Review if new parameter affects design

⬜ src/package_name/parsers/csv_parser.py
  - Add schema parameter to implementation
  - Update type hints
  - Update docstring

⬜ tests/test_parsers/test_csv_parser.py
  - Add tests for schema parameter
  - Test validation logic

⬜ Unit 001-csv-parser plan.md
  - Add task for schema validation if not present
  - Update verification to test new parameter

Next Steps:
1. Review design: /check csv-parser
2. Update code: /work csv-parser TK-NEW
3. Run tests: /verify csv-parser
```

### Step 9: Execute Updates
For each item in checklist:
- Update document
- Increment version if needed
- Update timestamp
- Mark as complete ✅

### Step 10: Validate Alignment
Run `/check` to verify:
- All references still valid
- No new drift introduced
- Python syntax correct
- Type hints complete

### Step 11: Update CLAUDE.md
Document:
- What was updated and why
- Which units were affected
- What actions were taken
- Any learnings

### Step 12: Generate Update Report

```
Update Report: spec.md Interface parse_document
Generated: 2025-01-15 10:30:00

Changes Made:
✅ Added 'schema' parameter (Optional[Dict[str, Any]])
✅ Updated docstring with new parameter
✅ Updated Raises section (added schema validation error)
✅ Incremented version: 1.0 → 1.1

Propagated To:
✅ Unit 001-csv-parser design.md (reviewed, no changes needed)
✅ src/package_name/parsers/csv_parser.py (updated)
✅ tests/test_parsers/test_csv_parser.py (added 3 tests)
✅ Unit 001-csv-parser plan.md (added TK-08 for schema validation)

Verification:
✅ All references valid
✅ Type hints complete
✅ Tests passing (11/11)
✅ Coverage: 94% ≥ 85%

Result: ✅ UPDATE COMPLETE AND VERIFIED
```

## Common Update Scenarios

### Scenario 1: Add Field to Entity
```
/update spec entities#User

What to add: last_login field
Type: Optional[datetime]
Default: None
Reason: Track user activity for analytics
```

**Propagates to:**
- Data models in src/
- Database migrations
- Unit designs using User entity
- Tests for User entity

### Scenario 2: Add Parameter to Interface
```
/update spec interfaces#parse_csv

What to add: max_rows parameter
Type: Optional[int]
Default: None
Reason: Allow limiting parsed rows for testing
```

**Propagates to:**
- Function implementations
- Function tests
- Unit designs calling this interface

### Scenario 3: Update Coverage Target
```
/update constitution quality-bars

What to change: coverage_target
New value: 0.90 (90%)
Old value: 0.85 (85%)
Reason: Raising quality standards
```

**Propagates to:**
- All unit plans (coverage target)
- CI configuration
- Verification gates

## Output
- **Updated:** Target document with changes
- **Checklist:** Required propagation actions
- **Report:** Summary of changes and impacts
- **CLAUDE.md:** Documentation of update

## Validation
- ✅ Python syntax valid
- ✅ Type hints complete
- ✅ Docstrings updated
- ✅ Versions incremented
- ✅ Timestamps updated
- ✅ Propagation complete
- ✅ Alignment verified

## Next Steps
- Run `/check` to verify alignment
- Update affected code with `/work`
- Run `/verify` on affected units
EOF

cat > "$CMD_DIR/reflect.md" << 'EOF'
---
name: reflect
description: Capture Python Project Learnings
---

# /reflect - Capture Python Project Learnings

## Purpose
Capture project learnings, decisions, and insights into CLAUDE.md for future reference.

## Usage
```
/reflect [scope]
/reflect              # Reflect on recent work
/reflect unit csv-parser  # Reflect on specific unit
/reflect project      # Reflect on entire project
```

## Prerequisites
- CLAUDE.md should exist (created automatically if missing)

## Process

### Step 1: Determine Scope
Based on argument:
- **No arg:** Recent work (last 1-2 tasks)
- **unit:** Specific unit (completed or in progress)
- **project:** Entire project (L1 docs, all units, overall progress)

### Step 2: Gather Context

#### For Unit Reflection
Load:
- Unit design.md (objective, acceptance criteria)
- Unit plan.md (tasks, progress, blockers)
- Verification results (from last /verify)
- Code changes (what was implemented)
- Test results (coverage, passing/failing)

#### For Project Reflection
Load:
- Constitution, PRD, Spec
- All unit statuses from state.json
- Overall test coverage
- Number of units completed
- Key milestones reached

### Step 3: Analyze Learnings

#### Technical Learnings
- What Python patterns worked well?
- What libraries/tools were effective?
- What performance optimizations were needed?
- What type hints or abstractions helped?

**Example Learnings:**
```
- Using generators for CSV parsing reduced memory usage by 80%
- Pydantic validation caught edge cases before runtime
- pytest fixtures with tmp_path simplified file testing
- Type hints revealed logic errors during development
```

#### Process Learnings
- What worked in the workflow?
- What slowed development?
- What would we do differently?
- What verification gates were most valuable?

**Example Learnings:**
```
- Writing tests alongside implementation (TDD) caught bugs early
- Type checking with pyright found issues ruff missed
- 85% coverage target was appropriate (not too strict, not too lenient)
- Breaking tasks into 2-4 hour chunks improved focus
```

#### Architecture Learnings
- How well did the design hold up?
- What assumptions proved wrong?
- What would we redesign?
- What interfaces need refinement?

**Example Learnings:**
```
- Separating parsing from validation improved testability
- Original interface lacked schema parameter (added in update)
- Streaming approach critical for large file support
- Error messages with line numbers saved debugging time
```

### Step 4: Identify Patterns

#### Successful Patterns
What worked and should be repeated:
- Code structures (class hierarchies, function composition)
- Testing strategies (fixtures, parametrize, mocking)
- Python idioms (generators, context managers, decorators)
- Type hint patterns (Protocol, TypedDict, Generic)

#### Anti-Patterns
What didn't work and should be avoided:
- Overly complex abstractions
- Missing type hints in key places
- Insufficient error handling
- Tight coupling between modules

### Step 5: Document Decisions

#### Key Decisions Made
For each significant decision:
- **Decision:** What was decided
- **Rationale:** Why this choice was made
- **Alternatives:** What else was considered
- **Outcome:** How it worked out

**Example:**
```
Decision: Use csv.DictReader instead of pandas
Rationale: Lighter dependency, sufficient for simple parsing
Alternatives: pandas.read_csv (too heavy), manual parsing (too complex)
Outcome: Good choice - fast and memory efficient
```

### Step 6: Capture Python-Specific Insights

#### Type Hints
- Which type hints were most useful?
- Where did type hints catch bugs?
- What complex types needed TypedDict/Protocol?

#### Testing
- Which pytest features were most valuable?
- How effective was fixture design?
- What mocking strategies worked?
- Coverage gaps and how to address them

#### Performance
- Where were bottlenecks?
- What optimizations made impact?
- Memory usage patterns
- Profiling insights

#### Dependencies
- Which packages were essential?
- Any regretted dependencies?
- Version constraints that helped/hurt

### Step 7: Extract Recommendations

Generate actionable recommendations:

**For Future Units:**
```
1. Start with type stubs before implementation
2. Write test fixtures before tests
3. Use generators for any file processing
4. Profile early if performance matters
5. Document complex type hints with examples
```

**For Current Project:**
```
1. Consider adding schema validation to all parsers
2. Standardize error message format across units
3. Extract common test fixtures to conftest.py
4. Add performance benchmarks to test suite
```

**For Process:**
```
1. Continue UPEVD pattern - very effective
2. Run type check during development, not just at end
3. Use coverage HTML reports to find gaps
4. Keep tasks under 4 hours for better estimates
```

### Step 8: Update CLAUDE.md

Add reflection section with structure:

```markdown
## Reflections

### 2025-01-15 - Unit 001-csv-parser Complete {#reflection}

**Summary:** Implemented CSV parsing with streaming support, comprehensive validation, and 92% test coverage.

**Technical Learnings:**
- Generators critical for memory efficiency (processed 1GB file in 50MB memory)
- Type hints caught off-by-one error in row counting logic
- pytest parametrize reduced test boilerplate from 200 to 50 lines
- Pydantic validation 3x faster than manual validation

**Process Learnings:**
- UPEVD workflow kept tasks focused and complete
- Writing tests first (TDD) revealed edge cases early
- Type checking during development (not just verification) saved time
- 3-hour task estimates were accurate, 1-hour tasks often underestimated

**Architecture Learnings:**
- Separating parse_csv() from validate_record() improved testability
- Generic parse_document() interface accommodates future parsers (JSON, XML)
- Error hierarchy (ParseError, ValidationError) enables granular handling

**Key Decisions:**
1. **csv.DictReader over pandas**
   - Rationale: No heavy dependency for simple parsing
   - Outcome: ✅ Good choice - fast and lightweight

2. **Streaming with generators**
   - Rationale: Support large files without memory issues
   - Outcome: ✅ Excellent - 1GB file in 50MB memory

3. **Optional Pydantic validation**
   - Rationale: Flexibility for users who don't need validation
   - Outcome: ✅ Good - validate parameter makes it opt-in

**Patterns to Reuse:**
- Generator pattern for file processing
- Fixture-based testing with tmp_path
- Type hints with Union for flexible returns
- Comprehensive docstrings with examples

**Anti-Patterns to Avoid:**
- ❌ Loading entire file into memory (original prototype)
- ❌ Generic Exception (replaced with specific error types)
- ❌ Implicit encoding (made explicit with default utf-8)

**Recommendations:**
1. Extract CSV-specific logic to separate module
2. Add support for CSV writing (not just reading)
3. Consider async version for concurrent file processing
4. Add benchmarks to track performance regressions

**Metrics:**
- Tasks: 7/7 completed
- Coverage: 92% (target: 85%)
- Tests: 11 passing
- Type errors: 0
- Linting errors: 0
- Time: 16 hours (estimated: 18 hours)

**Next Steps:**
- Start Unit 002-validator
- Extract common test fixtures to conftest.py
- Add performance benchmarks
```

### Step 9: Identify Cross-Unit Patterns

If reflecting on project:
- Common patterns across units
- Shared utilities to extract
- Consistent approaches
- Divergent solutions (good or bad?)

### Step 10: Suggest Improvements

Based on reflections, suggest:
- **Code improvements:** Refactoring, abstractions, utilities
- **Process improvements:** Workflow adjustments, tooling
- **Documentation improvements:** Clarifications, examples
- **Test improvements:** Coverage gaps, test patterns

## Output
- **Updated:** CLAUDE.md with reflection section
- **Insights:** Technical, process, and architecture learnings
- **Recommendations:** Actionable next steps
- **Patterns:** Reusable approaches documented

## Reflection Types

### Unit Reflection
Focus on:
- Specific implementation details
- Testing approach
- Performance characteristics
- Type hint patterns
- Code organization

### Project Reflection
Focus on:
- Overall architecture
- Cross-unit patterns
- Process effectiveness
- Quality trends
- Timeline accuracy

### Technical Reflection
Focus on:
- Python idioms and patterns
- Library and tool choices
- Performance optimizations
- Type system usage
- Testing strategies

### Process Reflection
Focus on:
- UPEVD workflow effectiveness
- Task estimation accuracy
- Verification gate value
- Communication patterns
- Decision-making process

## Best Practices

### Be Specific
❌ "Tests were helpful"
✅ "pytest fixtures with tmp_path reduced test setup from 20 lines to 5 lines per test"

### Be Honest
Document what didn't work, not just successes

### Be Actionable
Each learning should suggest concrete next steps

### Be Forward-Looking
Focus on what to do differently next time

## Next Steps
- Apply learnings to next unit
- Implement recommended improvements
- Update process based on insights
- Share patterns with team
EOF

# ============================================================================
# CLAUDE.md (Python-Focused Working Memory Template)
# ============================================================================

if [ ! -f "$ROOT/CLAUDE.md" ]; then
  cat > "$ROOT/CLAUDE.md" << 'EOF'
# CLAUDE.md

Working memory for aidev V4.2 (Python Edition) - Session context and project learnings

## Session Context

**Project:** [Project Name]
**Python Version:** 3.10+
**Package Manager:** UV
**Framework:** [FastAPI/Flask/Django/None]
**Database:** [PostgreSQL/MongoDB/None]

**Current Focus:**
[What are you working on right now?]

**Active Units:**
- [Unit ###-slug - current status]

**Recent Activity:**
[What was done in the last session?]

## Quick Reference

### UV Commands
```bash
# Install package
uv pip install <package>

# Run Python script
uv run python script.py

# Run pytest
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Type check
uv run pyright src/
uv run mypy src/

# Lint and format
uv run ruff check src/
uv run ruff format src/
```

### Project Structure
```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── module.py
│       └── subpackage/
├── tests/
│   ├── __init__.py
│   └── test_module.py
├── spec/
│   ├── constitution.md
│   ├── prd.md
│   ├── spec.md
│   └── units/
├── pyproject.toml
├── .python-version
└── CLAUDE.md
```

### Aidev Commands
```bash
# L1 Foundation
/constitution  # Create governance
/prd          # Capture requirements
/spec         # Define technical contract

# L2 Development
/new SLUG           # Create unit design
/plan SLUG          # Generate task breakdown
/work SLUG TK-##    # Implement task (UPEVD)
/verify SLUG        # Run verification gates

# Maintenance
/check [SLUG]  # Validate alignment
/update DOC    # Update documents
/reflect       # Capture learnings
```

## Project State

### L1 Status
- [ ] constitution.md (Python governance)
- [ ] prd.md (Product requirements)
- [ ] spec.md (Technical specification)

### Units
[List units with status]

### Current Blockers
[Any blocking issues]

## Decisions

### [YYYY-MM-DD] - [Decision Title] {#decision}

**Context:** [Why was this decision needed?]

**Decision:** [What was decided?]

**Rationale:** [Why this choice?]

**Alternatives:** [What else was considered?]

**Outcome:** [How did it work out?]

---

## Learnings

### [YYYY-MM-DD] - [Learning Title] {#learning}

**What:** [What was learned?]

**Why:** [Why is this important?]

**Application:** [How to apply this learning?]

---

## Python-Specific Notes

### Type Hints
[Type hint patterns and complex types]

### Testing Patterns
[pytest fixtures, parametrize, mocking strategies]

### Performance
[Profiling results, optimization approaches]

### Dependencies
[Package choices, version constraints, why]

---

## TODO
- [ ] [Action item 1]
- [ ] [Action item 2]

---

## Notes
[Miscellaneous notes and reminders]
EOF
fi

# ============================================================================
# .gitignore (Python-Focused)
# ============================================================================

append_unique_line "$ROOT/.gitignore" "# Python"
append_unique_line "$ROOT/.gitignore" "__pycache__/"
append_unique_line "$ROOT/.gitignore" "*.py[cod]"
append_unique_line "$ROOT/.gitignore" '*$py.class'
append_unique_line "$ROOT/.gitignore" "*.so"
append_unique_line "$ROOT/.gitignore" ".Python"
append_unique_line "$ROOT/.gitignore" "build/"
append_unique_line "$ROOT/.gitignore" "develop-eggs/"
append_unique_line "$ROOT/.gitignore" "dist/"
append_unique_line "$ROOT/.gitignore" "downloads/"
append_unique_line "$ROOT/.gitignore" "eggs/"
append_unique_line "$ROOT/.gitignore" ".eggs/"
append_unique_line "$ROOT/.gitignore" "lib/"
append_unique_line "$ROOT/.gitignore" "lib64/"
append_unique_line "$ROOT/.gitignore" "parts/"
append_unique_line "$ROOT/.gitignore" "sdist/"
append_unique_line "$ROOT/.gitignore" "var/"
append_unique_line "$ROOT/.gitignore" "wheels/"
append_unique_line "$ROOT/.gitignore" "*.egg-info/"
append_unique_line "$ROOT/.gitignore" ".installed.cfg"
append_unique_line "$ROOT/.gitignore" "*.egg"
append_unique_line "$ROOT/.gitignore" ""
append_unique_line "$ROOT/.gitignore" "# Virtual Environments"
append_unique_line "$ROOT/.gitignore" ".env"
append_unique_line "$ROOT/.gitignore" ".venv"
append_unique_line "$ROOT/.gitignore" "env/"
append_unique_line "$ROOT/.gitignore" "venv/"
append_unique_line "$ROOT/.gitignore" "ENV/"
append_unique_line "$ROOT/.gitignore" "env.bak/"
append_unique_line "$ROOT/.gitignore" "venv.bak/"
append_unique_line "$ROOT/.gitignore" ""
append_unique_line "$ROOT/.gitignore" "# Testing"
append_unique_line "$ROOT/.gitignore" ".pytest_cache/"
append_unique_line "$ROOT/.gitignore" ".coverage"
append_unique_line "$ROOT/.gitignore" "htmlcov/"
append_unique_line "$ROOT/.gitignore" ".tox/"
append_unique_line "$ROOT/.gitignore" ".nox/"
append_unique_line "$ROOT/.gitignore" ""
append_unique_line "$ROOT/.gitignore" "# Type Checking"
append_unique_line "$ROOT/.gitignore" ".mypy_cache/"
append_unique_line "$ROOT/.gitignore" ".pytype/"
append_unique_line "$ROOT/.gitignore" ".pyre/"
append_unique_line "$ROOT/.gitignore" ""
append_unique_line "$ROOT/.gitignore" "# IDE"
append_unique_line "$ROOT/.gitignore" ".vscode/"
append_unique_line "$ROOT/.gitignore" ".idea/"
append_unique_line "$ROOT/.gitignore" "*.swp"
append_unique_line "$ROOT/.gitignore" "*.swo"
append_unique_line "$ROOT/.gitignore" "*~"
append_unique_line "$ROOT/.gitignore" ""
append_unique_line "$ROOT/.gitignore" "# OS"
append_unique_line "$ROOT/.gitignore" ".DS_Store"
append_unique_line "$ROOT/.gitignore" "Thumbs.db"
append_unique_line "$ROOT/.gitignore" ""
append_unique_line "$ROOT/.gitignore" "# aidev"
append_unique_line "$ROOT/.gitignore" ".claude/logs/"

echo ""
echo "✅ aidev V4.2 (Python Edition) initialized successfully!"
echo ""
echo "📁 Directory structure:"
echo "   .claude/commands/    (10 Python-focused commands)"
echo "   .claude/hooks/       (4 Python-optimized automation hooks)"
echo "   .claude/templates/   (5 Python-specific templates)"
echo "   .claude/logs/        (state tracking)"
echo "   spec/                (project artifacts)"
echo "   spec/units/          (unit designs and plans)"
echo ""
echo "🐍 Python Features:"
echo "   - UV-based workflow (uv run pytest, uv run mypy)"
echo "   - Type checking with pyright/mypy"
echo "   - Testing with pytest + coverage"
echo "   - Formatting with ruff"
echo "   - Python 3.10+ type hints"
echo ""
echo "⚙️  Toggles:"
echo "   ENABLE_TESTS=0       (run with: --enable-tests)"
echo "   ENABLE_AUTOCOMMIT=1  (disable with: --disable-commits)"
echo "   ENABLE_TYPE_CHECK=1  (disable with: --disable-type-check)"
echo "   ENABLE_COVERAGE=1    (disable with: --disable-coverage)"
echo ""
echo "📖 Next steps:"
echo "   1. Run /constitution to establish Python project governance"
echo "   2. Run /prd to capture product requirements"
echo "   3. Run /spec to define technical specification"
echo "   4. Run /new SLUG to create your first unit"
echo ""
echo "💡 Toggle management:"
echo "   ./wb_aidev4_python.sh --enable-tests"
echo "   ./wb_aidev4_python.sh --disable-commits"
echo "   ./wb_aidev4_python.sh --status"
echo ""
