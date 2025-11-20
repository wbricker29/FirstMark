---
version: "1.0"
created: "2025-11-16"
updated: "2025-11-16"
project: "Talent Signal Agent"
context: "FirstMark Capital AI Lead Case Study"
---

# Project Constitution

Non-negotiable governance for Talent Signal Agent Python development

## Project Context

**Purpose:** AI-powered agent prototype for FirstMark's talent team to match executives with portfolio company roles

**Constraints:**

- 48-hour execution window
- Case study/demo quality (not production)
- Focus on demonstrating thinking quality over completeness
- Mock/synthetic data only

**Success Criteria:**

- Working prototype that demonstrates core matching capability
- Clear reasoning trails for matches
- Integration of structured + unstructured data
- Explainable, ranked outputs

## Principles

### KISS (Keep It Simple, Stupid)

- Prefer simple, readable Python code over clever solutions
- Explicit is better than implicit (PEP 20)
- Functions over classes when possible
- Minimize abstraction layers
- **Case-specific:** Prototype clarity > production patterns

### YAGNI (You Ain't Gonna Need It)

- Build only what's needed to demonstrate matching capability
- Validate requirements before implementation
- Defer optimization until measured need
- No speculative features
- **Case-specific:** MVP matching engine, minimal infrastructure

### Type Safety

- All public functions must have type hints (PEP 484)
- Use mypy with standard settings (not strict)
- Prefer explicit types over `Any`, but allow pragmatic exceptions
- Document complex types with TypedDict or dataclasses
- **Case-specific:** Type hints required, enforcement balanced with speed

### Testing

- Core matching logic requires tests (pytest)
- Tests must be readable and maintainable
- Use fixtures for reusable test setup
- Focus on happy paths for demo; edge cases as time permits
- **Case-specific:** 50% coverage target (core logic only)

## Quality Bars

### Coverage

- **Target:** 50% (0.50)
- **Measure:** pytest-cov
- **Scope:** Core matching logic, ranking, and reasoning
- **Rationale:** Demonstrate testing capability without over-engineering for 48hr case study

### Code Quality

- **Formatting:** ruff format (black-compatible)
- **Linting:** ruff check
- **Type Checking:** mypy (standard mode, not strict)
- **Docstrings:** Google style for public functions
- **Rationale:** Fast, comprehensive tooling without manual configuration

### Performance

- **Response Time:** < 10 seconds for full matching pipeline on mock data
- **Memory:** No specific constraint (mock data is small)
- **Profiling:** Not required for case study
- **Rationale:** Demo performance should feel responsive; no production SLAs

## Constraints

### Python Version

- **Minimum:** Python 3.11+
- **Reason:**
  - Matches existing `.python-version` in repo
  - Modern type hints and pattern matching features
  - Better error messages for debugging
  - Agno framework compatibility

### Package Management

- **Tool:** UV (<https://github.com/astral-sh/uv>)
- **Commands:**
  - `uv pip install <package>` - Install dependencies
  - `uv pip install -e .` - Install project in editable mode
  - `uv run python script.py` - Run Python scripts
  - `uv run pytest` - Run tests
  - `source .venv/bin/activate` - Activate virtual environment

### Project Structure

```
firstmark/
├── demo_files/              # Prototype implementation
│   ├── agents/              # Agent components
│   ├── data/                # Mock data (CSVs, bios, JDs)
│   ├── models/              # Data models
│   └── utils/               # Helper functions
├── tests/                   # Test files (mirror demo_files/)
│   ├── test_agents.py
│   └── test_matching.py
├── pyproject.toml           # Dependency management
├── .python-version          # Python version pinning (3.11+)
└── README.md                # Implementation documentation
```

### Dependencies

- **Minimal:** Only essential dependencies for Agno and core functionality
- **Pinned:** Use version constraints in pyproject.toml
- **Required:**
  - agno-ai (agent framework)
  - pydantic (data validation)
  - pytest (testing)
  - pytest-cov (coverage)
  - ruff (formatting + linting)
  - mypy (type checking)
- **Optional:** Additional dependencies only when clearly justified

## Code Style

### Naming Conventions (PEP 8)

- **Modules:** lowercase_with_underscores
- **Classes:** PascalCase
- **Functions:** lowercase_with_underscores
- **Constants:** UPPERCASE_WITH_UNDERSCORES
- **Private:** _leading_underscore

### Docstrings

```python
def match_candidates(
    role: Role,
    candidates: list[Candidate],
    threshold: float = 0.7
) -> list[Match]:
    """Match candidates to a role based on skills and experience.

    Args:
        role: The role to fill with requirements and context
        candidates: Pool of potential candidates to evaluate
        threshold: Minimum match score (0.0 to 1.0) to include in results

    Returns:
        Ranked list of matches with scores and reasoning

    Example:
        >>> role = Role(title="CTO", company="AcmeCo")
        >>> matches = match_candidates(role, all_candidates, threshold=0.8)
        >>> print(matches[0].reasoning)
    """
    pass
```

### Type Hints

```python
from typing import Optional
from collections.abc import Callable

def process_candidates(
    candidates: list[Candidate],
    filter_fn: Optional[Callable[[Candidate], bool]] = None
) -> dict[str, list[Candidate]]:
    """Process and group candidates by role type."""
    pass
```

## Development Workflow

### Pre-Commit (Automated via Git Hooks)

1. `ruff format` - Auto-format code
2. `ruff check` - Linting
3. **Note:** Type checking run manually (not blocking for speed)

### Manual Verification

1. `uv run pytest` - Run tests
2. `uv run pytest --cov=demo_files` - Check coverage
3. `uv run mypy demo_files/` - Type checking

### Pre-Demo Checklist

1. All tests passing
2. Coverage ≥ 50% for core logic
3. No ruff errors
4. README documents implementation
5. Demo script works end-to-end

## Security

### Input Validation

- Use Pydantic for structured data validation
- Sanitize any external inputs (mock data should be safe)
- No SQL injection risk (using CSV/JSON for mock data)

### Secrets Management

- Never commit API keys or secrets
- Use environment variables for OpenAI/LLM API keys
- Add `.env` to `.gitignore`

### Dependencies

- Minimal dependencies = minimal attack surface
- Review dependencies before adding
- No need for `uv pip audit` for case study

## Case Study-Specific Rules

### Scope Discipline

1. **Build only what demonstrates the concept**
   - Core matching engine
   - Basic reasoning explanation
   - Simple ranking logic
   - No production features (auth, API, monitoring)

2. **Prioritize clarity over cleverness**
   - Clear variable names
   - Simple functions
   - Obvious data flow
   - Well-commented complex logic

3. **Documentation matters**
   - README explains implementation choices
   - Code comments explain "why" not "what"
   - Docstrings for all public functions

### Time Management

- **Hour 1-8:** Core matching logic
- **Hour 9-16:** Data integration + reasoning
- **Hour 17-24:** Testing + refinement
- **Hour 25-32:** Documentation + demo prep
- **Hour 33-40:** Presentation prep + buffer
- **Hour 41-48:** Final review + practice

### Quality vs. Speed Tradeoffs

**Acceptable shortcuts for case study:**

- Hardcoded configurations (vs. config files)
- Simplified error handling (basic try/except)
- Mock data generation scripts without tests
- Inline documentation vs. separate docs

**Non-negotiable quality:**

- Type hints on all public functions
- Tests for core matching logic
- Clear, readable code
- Working end-to-end demo

## Non-Negotiables

1. **No untested core matching logic**
2. **All public functions must have type hints**
3. **All public functions must have docstrings**
4. **Follow PEP 8 (enforced by ruff)**
5. **Working demo before documentation**
6. **README explains implementation choices**

## Exceptions

Given the 48-hour case study constraint, the following exceptions are pre-approved:

1. **Lower coverage (50% vs. 85%)** - Focus on core logic only
2. **Standard mypy (vs. strict)** - Balance safety with speed
3. **Minimal edge case testing** - Happy path priority
4. **Simplified error handling** - Basic try/except vs. comprehensive error hierarchy
5. **Mock data without validation** - Trust synthetic data quality

**Exception documentation:** Any additional exceptions must be documented in code comments with `# CASE_EXCEPTION:` prefix

## Success Definition

This constitution succeeds if:

1. ✅ Prototype demonstrates clear thinking about the problem
2. ✅ Code is readable and maintainable by FirstMark team
3. ✅ Core matching logic is tested and type-safe
4. ✅ Implementation can be explained in 30 minutes
5. ✅ Quality signals professionalism without over-engineering

**Remember:** The goal is demonstrating quality of thinking through minimal, working code—not building production infrastructure.
