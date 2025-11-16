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
