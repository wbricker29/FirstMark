---
version: "1.0"
last_updated: "YYYY-MM-DD"
---

# Project Constitution Template

Non-negotiable principles guiding all development

## Principles

### Sufficiency over assumptions
- **Rule:** Ask questions early rather than fill gaps with guesses
- **Rationale:** Reduces rework, ensures alignment with actual requirements
- **Examples:**
  - When a requirement is ambiguous, ask for clarification before implementing
  - When encountering conflicting information, surface it immediately

### [Principle Name]
- **Rule:** [Specific, enforceable requirement]
- **Rationale:** [Why this matters]
- **Examples:**
  - [Concrete example of compliance]
  - [Another example]

## Quality Bars

- **Coverage target:** 85% (0.85)
- **Typing:** strict
- **Linting:** enabled
- **Performance targets:**
  - API response time: p95 < 200ms (measured via logging middleware)
  - [Custom metric]: [Target value] (measured via [How to verify])

## Constraints

### Runtime
- Python 3.11+
- [Other runtime requirements]

### Security
- All user input must be validated via schemas
- No secrets in code or logs
- [Other security requirements]

### Dependencies
- Minimize external dependencies
- All dependencies must be pinned
- [Other dependency rules]

## Decision Rights

- **Architecture:** Tech Lead
- **API contracts:** Product + Engineering
- **Infrastructure:** DevOps Team
- **Testing strategy:** QA + Engineering
