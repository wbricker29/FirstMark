---
name: aidev-workflow
description: Comprehensive guidance for the AIdev workflow system used for structured software project management with Claude Code. Covers AIdev commands (/constitution, /prd, /plan, /work, /check, /verify, /reflect, /new, /spec), file structure (specs/ directory with constitution, PRD, units), task execution with evidence-based completion, constitutional governance, quality gates, Single Source of Truth principle, Context Discipline, pre-implementation checks, task schema format, automation hooks, template management, and workflow sequences for feature planning and implementation. Use when working with specs/, creating product requirements, designing features, managing tasks, or validating project alignment.
---

# AIdev Workflow Skill

## Purpose

Provides systematic guidance for managing software projects using Claude Code with structured planning, constitutional governance, and automated quality checks. Navigate the AIdev system and use its commands effectively.

## When to Use This Skill

Use this skill when:
- Needing guidance on AIdev commands (/constitution, /prd, /plan, /work, /check, etc.)
- Understanding the file structure (specs/, supabase/, .claude/)
- Learning workflow sequences (one-time setup, per-project, per-feature)
- Clarifying core principles (Single Source of Truth, Evidence = Completion, Context Discipline)
- Asking about pre-implementation checks or quality gates
- Understanding task schema and progress tracking
- Configuring automation hooks and toggle controls

## Key Concepts

Core principles governing the AIdev workflow:

- **Single Source of Truth**: Constitution, PRD, spec, design, and plan documents form a hierarchy
- **Evidence = Completion**: Tasks require test output + code + explanation before marking done
- **Context Discipline**: Document size limits and boundaries prevent scope creep
- **Constitutional Governance**: Non-negotiable principles block progress when violated

See `references/workflow-details.md` for detailed explanations and file structure.

## How to Use This Skill

Provides bundled resources for understanding and implementing the AIdev system.

**Documentation Location:** `.claude/skills/aidev-workflow/references/`

Reference documents are available for loading as needed when this skill is invoked. Access them directly via:
- `@.claude/skills/aidev-workflow/references/workflow-details.md`
- `@.claude/skills/aidev-workflow/references/commands-reference.md`
- `@.claude/skills/aidev-workflow/references/execution-framework.md`

### References

1. **references/workflow-details.md** — Covers comprehensive documentation:
   - Complete file structure explanation
   - Detailed core principles with examples
   - PRD structure and maintenance rules (supports optional expanded PRD with link-first Feature Inventory/Current State)
   - Full workflow sequences
   - Pre-implementation checks
   - Automation hooks and configuration
   - Task schema format
   - Testing philosophy

2. **references/commands-reference.md** — Documents commands in detail:
   - /constitution (one-time project governance)
   - /prd (create/update project requirements)
   - /plan FEATURE_NAME (technical design with constitution check)
   - /work NNN x.y (implement with pre-checks)
   - /check NNN (five quality gates)
   - /reflect [scope] (extract learnings)

3. **references/execution-framework.md** — Provides implementation guidance for executing workflows

### Templates

**Location:** `.claude/skills/aidev-workflow/assets/templates/` (single source of truth)

Available templates:
- **CONSTITUTION-TEMPLATE.md** — Project governance (used by `/constitution`)
- **PRD-TEMPLATE.md** — Product requirements (used by `/prd`)
- **SPEC-TEMPLATE.md** — Technical specifications (used by `/spec`)
- **DESIGN-TEMPLATE.md** — Feature designs (used by `/new`)
- **PLAN-TEMPLATE.md** — Implementation plans (used by `/plan`)

Note: The default PRD template is reference-based and lean. Teams may adopt an optional “expanded PRD” pattern (Feature Inventory, Current Project State, Critical Path, Document Hierarchy) as documented in `references/workflow-details.md` and `references/commands-reference.md`. Keep expanded sections link-first and derive any numbers from automation (state.json, `/status`).

Edit templates in `assets/templates/` only. Commands reference these templates directly from the skill directory. See `references/workflow-details.md` for template management details.

## Quick Start

**First-time setup:** Run `/constitution` → `/prd` → `/spec`

**Per-feature:** Run `/new SLUG` → `/plan SLUG` → `/work SLUG TK-##` → `/verify SLUG`

**Ongoing:** Run `/check` for validation, `/reflect` for learnings

See `references/workflow-details.md` for detailed workflow sequences and `references/commands-reference.md` for command documentation.

## Environment Variables

Toggle automation behavior by setting these before running Claude Code:

```bash
export ENABLE_TESTS=0        # Disable tests (default)
export ENABLE_TESTS=1        # Enable tests
export ENABLE_AUTOCOMMIT=1   # Auto-commit on task completion (default)
export ENABLE_AUTOCOMMIT=0   # Disable auto-commits
```

See `references/workflow-details.md` for full automation documentation.

## File Structure Reference

```
specs/
├── constitution.md              # Non-negotiable project principles
├── PRD.md                       # Product requirements (unified document)
└── units/###-SLUG/
    ├── design.md                # Stable architecture & design intent
    └── plan.md                  # Volatile task execution (includes tasks)

.claude/
├── skills/aidev-workflow/
│   ├── SKILL.md                 # This file
│   ├── references/              # Detailed documentation
│   │   ├── workflow-details.md
│   │   ├── commands-reference.md
│   │   └── execution-framework.md
│   └── assets/templates/        # Document templates
└── logs/
    └── state.json               # AUTO-GENERATED (never edit manually)
```
