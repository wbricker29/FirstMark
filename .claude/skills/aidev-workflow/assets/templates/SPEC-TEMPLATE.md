---
version: "1.0"
last_updated: "YYYY-MM-DD"
status: "draft"
---

# Engineering Specification Template

Technical contract between product and implementation

## Architecture

**Pattern:** [e.g., ports-and-adapters, layered, microservices]

**Rationale:** [Why this architecture was chosen]

### Modules

#### [module_name]
- **Responsibility:** [What this module does]
- **Dependencies:** [other_module]
- **Location:** [File path or package]

#### [another_module]
- **Responsibility:** [Responsibility]
- **Dependencies:** None
- **Location:** [Location]

### Data Flow

1. [Step 1: Component A receives input]
2. [Step 2: Component A calls Component B]
3. [Step 3: Component B returns result]
4. [Step 4: Component A returns to user]

## Interfaces

### [interface_name]
- **Module:** [module_name]
- **Description:** [What this interface does]

#### Inputs
- **[param_name]** ([type]): [Description] - Constraints: [e.g., non-empty, positive, etc.]

#### Outputs
- **[return_name]** ([type]): [Description]

#### Errors
- [ErrorType: when it occurs]
- [AnotherError: condition]

#### Preconditions
- [Condition that must be true before calling]

#### Postconditions
- [Condition guaranteed true after successful call]

### [another_interface]
- **Module:** [module_name]
- **Description:** [Description]

#### Outputs
- **[result]** ([type]): [Description]

## Data Model

### Entity: [EntityName]

**Description:** [What this entity represents]

#### Fields
- **[field_name]** ([type]): [Field purpose] - Constraints: [e.g., unique, non-null, max length]
- **[another_field]** ([type]): [Description] - Constraints: [constraints]

#### Relationships
- [Relationship to other entities]

### Entity: [AnotherEntity]

**Description:** [Description]

#### Fields
- **[field]** ([type]): [Description] - Constraints: [constraints]

## Non-Functional Requirements

### Performance
- **Requirement:** [e.g., API endpoints respond in <200ms p95]
- **Measurement:** [How to verify]

### Reliability
- **Requirement:** [e.g., 99.9% uptime]
- **Measurement:** [How to track]

### Observability
- **Requirement:** [e.g., All errors logged with context]
- **Measurement:** [Logging strategy]

### Security
- **Requirement:** [e.g., All inputs validated]
- **Measurement:** [How to verify]
