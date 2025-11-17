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

- **Tool:** UV (<https://github.com/astral-sh/uv>)
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
