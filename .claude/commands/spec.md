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
