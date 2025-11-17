# AIdev Workflow System

A structured development workflow system for Claude Code that enforces quality, consistency, and alignment across software projects through constitutional governance, evidence-based task completion, and automated validation.

## What is AIdev?

AIdev is a lightweight project management framework that transforms ad-hoc development into a systematic, traceable workflow. It provides:

- **Constitutional Governance**: Non-negotiable principles that guide all decisions
- **Hierarchical Documentation**: Constitution → PRD → Spec → Design → Plan
- **Evidence-Based Completion**: No task is "done" without proof (tests, coverage, validation)
- **Automated Quality Gates**: Pre-flight checks, drift detection, alignment validation
- **Single Source of Truth**: One canonical location for each concept

## Quick Start

### First-Time Setup (One-Time Per Project)

```bash
/constitution  # Establish project principles and quality bars
/prd          # Define problem, outcomes, success metrics
/spec         # Create technical specification (architecture, interfaces, data models)
```

### Per-Feature Workflow

```bash
/new SLUG     # Create feature design (objectives, acceptance criteria)
/plan SLUG    # Generate implementation plan (tasks, dependencies, estimates)
/work SLUG TK-##  # Implement specific task (UPEVD pattern)
/verify SLUG  # Run verification gates (tests, coverage, quality checks)
```

### Ongoing Validation

```bash
/check        # Validate alignment (L1: project-level, L2: unit-level, CROSS: cross-level)
/reflect      # Capture learnings and patterns for reuse
/update       # Change and propagate updates across documents
```

## Directory Structure

```
.claude/
├── README.md                    # This file
├── AIDEV_REVIEW.md             # System evaluation and enhancement recommendations
├── skills/
│   └── aidev-workflow/
│       ├── SKILL.md            # Single source of truth for workflow logic
│       ├── references/         # Detailed documentation
│       │   ├── workflow-details.md
│       │   ├── commands-reference.md
│       │   └── execution-framework.md
│       └── assets/
│           └── templates/      # Document templates (CONSTITUTION, PRD, SPEC, etc.)
├── commands/                   # Slash commands (thin wrappers around skill)
│   ├── constitution.md
│   ├── prd.md
│   ├── spec.md
│   ├── new.md
│   ├── plan.md
│   ├── work.md
│   ├── verify.md
│   ├── check.md
│   ├── reflect.md
│   └── update.md
├── hooks/                      # Automation triggers
│   └── state-tracker.py        # Auto-updates state.json on file writes
├── logs/
│   └── state.json             # AUTO-GENERATED: Project state (never edit manually)
└── toggles.env                # Environment variables for automation control

spec/
├── constitution.md            # Non-negotiable project principles
├── PRD.md                    # Product requirements (problem, outcomes, metrics)
├── spec.md                   # Technical specification (architecture, interfaces)
└── units/###-SLUG/          # Feature-specific documentation
    ├── design.md             # Stable: Architecture & design intent
    └── plan.md              # Volatile: Task execution & progress
```

## Core Principles

### 1. Single Source of Truth (SSOT)

Every concept has exactly one canonical location:

- **Workflow logic**: `.claude/skills/aidev-workflow/SKILL.md`
- **Templates**: `.claude/skills/aidev-workflow/assets/templates/`
- **Commands**: Thin wrappers that invoke skill + provide context
- **Project governance**: `spec/constitution.md`
- **Product requirements**: `spec/PRD.md`

### 2. Evidence = Completion

Tasks are only "done" when validated:

- Tests pass (unit, integration, edge cases)
- Coverage meets threshold (≥80%)
- Acceptance criteria satisfied
- No placeholders or TODOs
- Code follows constitution standards

### 3. Context Discipline

Documents have boundaries to prevent scope creep:

- Constitution: Project-wide principles (max ~500 lines)
- PRD: Problem, outcomes, scope (max ~300 lines)
- Design: Feature architecture (max ~400 lines)
- Plan: Task breakdown (living document)

### 4. Constitutional Governance

Non-negotiable principles block progress when violated:

- Quality bars must be met before merging
- Architecture patterns enforced via `/check`
- Drift detection prevents spec/code misalignment

## Command Execution Pattern

All commands follow a standardized 5-phase pattern:

### Phase 1: Validate
Check prerequisites before proceeding (files exist, dependencies met, permissions granted).

### Phase 2: Gather
Collect information from user (guided prompts, smart defaults, validation criteria).

### Phase 3: Generate
Create artifacts (populate templates, format data, write files).

### Phase 4: Validate
Run verification checklist (structure, completeness, alignment).

### Phase 5: Confirm
Display summary to user (what was created, next steps).

## Automation & Hooks

### Available Hooks

- **state-tracker.py**: Auto-updates `state.json` when `spec/**/*.md` files change
- **auto-commit**: Git commit on task completion (enabled by default)

### Environment Variables

Toggle automation behavior:

```bash
export ENABLE_TESTS=0        # Disable tests (default)
export ENABLE_TESTS=1        # Enable tests
export ENABLE_AUTOCOMMIT=1   # Auto-commit on task completion (default)
export ENABLE_AUTOCOMMIT=0   # Disable auto-commits
```

Set in `.claude/toggles.env` for persistent configuration.

## Skill vs. Command Relationship

### Skill: The Brain (Logic + Knowledge)

- Contains all workflow logic, validation rules, templates
- Provides detailed guidance via reference documents
- Single source of truth for AIdev system behavior

### Commands: The Interface (Entry Points + Context)

- Thin wrappers that invoke the skill
- Provide command-specific context and phase structure
- No logic duplication (delegate to skill)

**Example Flow:**

1. User runs `/work SLUG TK-01`
2. Command invokes `aidev-workflow` skill (Step 0)
3. Skill provides UPEVD pattern, validation criteria, standards
4. Command executes 5 phases using skill guidance
5. Result: Task implemented with evidence-based completion

## Key Commands Reference

### `/constitution` - Create Project Governance
Establish non-negotiable principles, quality bars, and constraints.

**Prerequisites**: None (typically first command run)

**Output**: `spec/constitution.md`

---

### `/prd` - Create Product Requirements
Define problem, audience, outcomes, scope, and success metrics.

**Prerequisites**: `spec/constitution.md` (recommended)

**Output**: `spec/PRD.md`

---

### `/spec` - Create Engineering Contract
Define architecture, interfaces, data models, and module boundaries.

**Prerequisites**: `spec/constitution.md`, `spec/PRD.md`

**Output**: `spec/spec.md`

---

### `/new SLUG` - Create New Unit
Create feature design with objectives, acceptance criteria, and architecture.

**Prerequisites**: `spec/constitution.md`, `spec/PRD.md`, `spec/spec.md`

**Output**: `spec/units/###-SLUG/design.md`

---

### `/plan SLUG` - Generate Unit Plan
Break down feature into tasks with dependencies, estimates, and verification gates.

**Prerequisites**: `spec/units/###-SLUG/design.md`

**Output**: `spec/units/###-SLUG/plan.md`

---

### `/work SLUG TK-##` - Implement Task
Execute task using UPEVD pattern (Understand, Plan, Execute, Validate, Document).

**Prerequisites**: `spec/units/###-SLUG/plan.md`, task status "ready" or "doing", dependencies complete

**Output**: Code, tests, updated task status

---

### `/verify SLUG` - Run Verification Gates
Execute quality checks (tests, coverage, linting, type-checking, constitution compliance).

**Prerequisites**: `spec/units/###-SLUG/plan.md`, at least one task complete

**Output**: Verification report (pass/fail for each gate)

---

### `/check [SLUG]` - Validate Alignment & Drift
Detect misalignment between documents and code at different architectural levels.

**Modes**:
- **L1**: Project-level (constitution, PRD, spec vs. code)
- **L2**: Unit-level (design, plan vs. code)
- **CROSS**: Cross-level (L2 references valid in L1 documents)

**Prerequisites**: Depends on mode (L1: project docs, L2: unit docs, CROSS: both)

**Output**: Alignment report (✅ pass, ⚠️ warning, ❌ critical)

---

### `/reflect [SCOPE]` - Capture Learnings
Extract patterns, decisions, and insights for reuse.

**Scopes**: Task, feature, project, codebase

**Prerequisites**: At least one completed task

**Output**: Updated documentation (CLAUDE.md, design.md, or new reference doc)

---

### `/update` - Change & Propagate Updates
Update documents and propagate changes to dependent artifacts.

**Prerequisites**: Depends on what's being updated

**Output**: Updated documents with cascading changes

---

## Getting Help

### Documentation Hierarchy (Authority Order)

1. `.claude/skills/aidev-workflow/SKILL.md` (HIGHEST)
2. `.claude/skills/aidev-workflow/references/` (Detailed guides)
3. `.claude/commands/` (Command-specific execution patterns)
4. `spec/constitution.md` (Project-specific governance)

### Common Questions

**Q: Which command do I run first?**
A: `/constitution` → `/prd` → `/spec` (one-time setup)

**Q: How do I add a new feature?**
A: `/new SLUG` → `/plan SLUG` → `/work SLUG TK-##` → `/verify SLUG`

**Q: How do I check if my code aligns with the spec?**
A: Run `/check` (defaults to CROSS mode for comprehensive validation)

**Q: Can I skip the constitution?**
A: Not recommended. Constitution establishes quality bars enforced by `/work` and `/verify`.

**Q: What if I need to update the PRD mid-project?**
A: Run `/prd` (choose "update" option) → Run `/update` to propagate changes → Run `/check` to validate alignment

**Q: How do I disable auto-commit?**
A: `export ENABLE_AUTOCOMMIT=0` in `.claude/toggles.env`

## Philosophy

AIdev is built on three core beliefs:

1. **Quality requires structure**: Ad-hoc development creates technical debt. Systematic workflows prevent it.

2. **Documentation is a contract**: Documents aren't just notes—they're enforceable agreements between stakeholders and engineers.

3. **Automation enables discipline**: Humans are fallible. Hooks, validation scripts, and quality gates ensure consistency.

The goal is not to add bureaucracy—it's to make good practices automatic and effortless.

## Learn More

- **Skill Documentation**: `.claude/skills/aidev-workflow/SKILL.md`
- **Command Reference**: `.claude/skills/aidev-workflow/references/commands-reference.md`
- **Workflow Details**: `.claude/skills/aidev-workflow/references/workflow-details.md`
- **Execution Framework**: `.claude/skills/aidev-workflow/references/execution-framework.md`
- **System Evaluation**: `.claude/AIDEV_REVIEW.md`

---

**Version**: 1.0
**Last Updated**: 2025-11-17
