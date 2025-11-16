---
name: multi-agent-orchestration
description: General-purpose multi-agent orchestration patterns and tooling. Use when coordinating 3+ sub-agents for complex tasks, managing parallel/sequential work streams, synthesizing distributed outputs, or validating cross-agent work quality. Works with any project structure or workflow system.
---

# Multi-Agent Orchestration

## Overview

Orchestrate complex multi-step workflows by deploying specialized sub-agents, managing their coordination, ensuring quality standards, and synthesizing results into coherent deliverables. This skill provides universal orchestration patterns applicable to any project.

## When to Use This Skill

**Trigger this skill when:**
- Task requires coordinating 3+ specialized sub-agents
- Workflow has complex dependencies between sub-tasks
- Need to manage parallel development streams
- Complex validation requiring multiple quality checks
- Synthesizing outputs from distributed work
- Managing handoffs between different agent types

**Do not use for:**
- Single-agent tasks (deploy agent directly)
- Simple linear workflows (standard command chains sufficient)
- Pure exploration or research (use Explore agent)

## Core Orchestration Workflow

Follow this 5-phase workflow for all orchestrations:

### Phase 1: Analyze (UNDERSTAND)

**Read Project Context:**
1. Identify and load relevant project documentation (requirements, standards, guidelines)
2. Understand quality expectations and constraints
3. Review existing work logs or decision history if available
4. Gather all context needed to understand the task scope

**Analyze Work Requirements:**
1. Parse user request to identify scope and deliverables
2. Identify dependencies between sub-tasks
3. Map requirements to quality standards
4. Determine validation criteria for success

**Run Pre-Flight Validation:**
Execute `scripts/validate_orchestration.py` (optional) to verify:
- Task scope is clearly defined
- Dependencies are identified and acyclic
- Context bounds are manageable (token limits)
- Required resources are available

**Validation Checklist:**
- ✅ Task scope is clearly defined
- ✅ Dependencies are identified and mapped
- ✅ Quality requirements understood
- ✅ Context bounds are manageable
- ✅ All necessary context is accessible

### Phase 2: Plan (DESIGN SUB-AGENT STRATEGY)

**Determine Sub-Agent Deployment:**

Identify which specialized sub-agents are needed:
- `task-implementor`: Complete specific tasks from tasks.md
- `systematic-debugger`: Investigate bugs or errors
- `code-prettier`: Refactor and code cleanup
- `principle-evaluator`: Validate KISS/YAGNI adherence
- `documentation-manager`: Document updates and alignment
- `Explore`: Codebase exploration and analysis
- Other specialized agents as needed

**For each sub-agent, define:**
- **Scope**: Specific tasks and boundaries
- **Context**: Required files, documents, reference materials
- **Instructions**: Clear directives and constraints
- **Integration points**: How outputs will be synthesized
- **Validation criteria**: What constitutes success

**Establish Coordination Protocol:**
- **Execution order**: Parallel vs sequential (use `references/agent-coordination.md` for patterns)
- **Handoff points**: Information flow between agents
- **Dependencies**: What each agent needs from others

**Present Plan to User:**
Use `assets/orchestration-plan.tmpl` to generate:
```
🤖 Sub-Agent Orchestration Plan

Agents to deploy: [count]
├─ [agent-1]: [scope]
├─ [agent-2]: [scope]
└─ [agent-n]: [scope]

Execution strategy: [parallel/sequential/mixed]
Coordination points: [handoffs]
Expected deliverables: [outputs]
Validation gates: [quality checks]

Proceed? (y/n)
```

### Phase 3: Execute (DEPLOY & COORDINATE)

**Deploy Sub-Agents:**

For each sub-agent in the plan:

1. **Prepare agent briefing:**
   - Task scope and boundaries
   - Constitutional constraints (from constitution.md)
   - Context files to read
   - Reference materials
   - Integration requirements
   - Expected output format

2. **Deploy agent using Task tool:**
   ```
   Task tool parameters:
   - subagent_type: [appropriate agent type]
   - description: [short 3-5 word summary]
   - prompt: [detailed briefing including all context and instructions]
   - model: [sonnet for complex tasks, haiku for simple tasks]
   ```

3. **Monitor execution:**
   - Track progress and status
   - Ensure constitutional compliance
   - Use `scripts/check_context_bounds.py` to prevent context overflow
   - Provide additional context if needed

4. **Coordinate handoffs:**
   - If sequential: Wait for completion before deploying next agent
   - If parallel: Deploy all agents simultaneously in single message
   - Manage information flow between agents per coordination protocol

**Track During Execution:**
- Agent deployment timestamps
- Progress status for each agent
- Blockers or issues encountered
- Preliminary outputs or findings

### Phase 4: Validate (SYNTHESIZE & VERIFY)

**Synthesize Sub-Agent Outputs:**
1. Collect outputs from all deployed sub-agents
2. Verify each agent completed its assigned scope
3. Check for gaps or inconsistencies
4. Integrate outputs into coherent result
5. Resolve any conflicts or overlaps

**Run Comprehensive Validation:**

**Quality Standards:**
- ✅ All outputs meet project quality standards
- ✅ Code/content follows established conventions
- ✅ Performance targets satisfied (if applicable)
- ✅ Constraints enforced

**Completeness Verification:**
- ✅ All required tasks completed
- ✅ All deliverables produced
- ✅ No placeholders or incomplete work remaining
- ✅ Edge cases handled

**Technical Validation (adapt to project):**
- ✅ Code formatted per project standards
- ✅ Linting passes
- ✅ Type checking passes (if applicable)
- ✅ Tests pass
- ✅ Coverage meets target

**Evidence Requirements:**
- ✅ Each sub-task has verifiable evidence of completion
- ✅ Results demonstrate correctness
- ✅ Documentation updated where needed
- ✅ Decision logs updated if architectural changes made

**If validation fails:**
- Document specific failures
- Determine which sub-agent needs to re-run
- Deploy corrective agents with focused scope
- Re-validate after corrections

### Phase 5: Confirm (REPORT & DOCUMENT)

**Generate Synthesis Report:**

Use `scripts/synthesize_reports.py` with `assets/synthesis-report.tmpl` to generate:
```
📊 Multi-Agent Orchestration Complete

## Deployed Agents
- [agent-1]: [scope] ✅
- [agent-2]: [scope] ✅

## Deliverables
- [deliverable-1]: [location/description]

## Validation Results
✅ Constitutional compliance: PASS
✅ Completeness: PASS
✅ Quality gates: PASS [format|lint|types|tests]
✅ Coverage: [X]% (target: [Y]%)
✅ Evidence: All tasks verified

## Changes Made
- Files modified: [count]
- Files created: [count]
- Tests added: [count]
- Documentation updated: [list]

## Next Steps
[Recommended follow-up actions]
```

**Update Documentation:**
1. **Task Status**: Update task tracking system with completed work
2. **Decision Log**: If significant decisions were made, document them:
   - What was decided and why
   - Alternatives considered
   - Impact on the project
3. **Session Summary**: Document orchestration results, patterns identified, recommended next actions

**Coordinate Documentation Updates:**
If cross-document updates are needed:
- Deploy appropriate agent to handle documentation consistency
- Ensure all changes are reflected across relevant documentation

**Prompt User for Next Action:**
- Continue with next task?
- Validate overall completion?
- Commit changes?
- Generate detailed summary?

## Available Sub-Agents

Quick reference for agent selection:

| Agent Type | Use Case | Integration Notes |
|------------|----------|-------------------|
| `task-implementor` | Complete tasks from tasks.md | Reads plan.md, writes code/tests/docs |
| `systematic-debugger` | Debug errors methodically | Needs error context, produces fix + test |
| `code-prettier` | Refactor for readability | No functional changes, preserves behavior |
| `principle-evaluator` | Validate KISS/YAGNI/Quality | Reads constitution.md, produces report |
| `documentation-manager` | Update docs for consistency | Reads all specs/, produces alignment report |
| `Explore` | Codebase exploration | Fast discovery, minimal context usage |
| `Plan` | Generate implementation plans | Similar to Explore but planning-focused |

## Error Handling

For detailed error scenarios and resolutions, see `references/error-scenarios.md`.

**Common errors:**
- **Missing project context** → Gather required documentation before proceeding
- **Ambiguous requirements** → Ask clarifying questions before planning
- **Sub-agent failure** → Analyze failure, adjust briefing, redeploy
- **Context overflow** → Break work into smaller chunks, use check_context_bounds.py
- **Validation failure** → Deploy corrective agents, re-validate
- **Synthesis conflicts** → Manual review, determine correct approach, redeploy if needed

For specific error codes and detailed troubleshooting, grep `references/error-scenarios.md`.

## Resources

### scripts/validate_orchestration.py
Pre-flight validation ensuring:
- Task scope is clearly defined
- Context bounds are manageable (token limits)
- Dependencies are identified and acyclic
- Returns structured JSON validation report

**Usage:**
```bash
python3 scripts/validate_orchestration.py --scope "task description" [--context-files file1,file2]
```

### scripts/synthesize_reports.py
Template-based report generation from sub-agent outputs:
- Parses sub-agent completion messages
- Extracts deliverables, validation results, changes
- Generates markdown synthesis report using template
- Supports JSON output for decision logging

**Usage:**
```bash
python3 scripts/synthesize_reports.py --agents agent1,agent2 --deliverables file1.ts,file2.ts
```

### scripts/check_context_bounds.py
Token usage monitoring during orchestration:
- Estimates token usage from file reads and agent briefings
- Warns when approaching model context limits (200k tokens)
- Suggests chunking strategies if limits exceeded
- Tracks token usage per phase

**Usage:**
```bash
python3 scripts/check_context_bounds.py --phase [1-5] --files file1.ts,file2.ts
```

### references/agent-coordination.md
Detailed coordination patterns for complex multi-agent workflows:
- Sequential execution: When to use, handoff protocols, state management
- Parallel execution: Task independence validation, output merging strategies
- Hybrid patterns: Mixed sequential + parallel workflows
- Context sharing: Minimizing redundancy between agents
- Error recovery: Retry logic, fallback strategies, partial completion handling
- Integration points: How agents interact with documentation-manager, context-manager

Load this reference when planning complex coordination protocols or troubleshooting handoff issues.

### references/phase-playbooks.md
Comprehensive per-phase execution guidance:
- Extended examples with real-world scenarios
- Edge cases and unusual situations
- Common failure patterns and prevention strategies
- Constitutional mapping (which principles apply per phase)
- Tool usage recommendations per phase
- Decision points (when to ask user vs proceed autonomously)

Load this reference when encountering edge cases or needing detailed phase guidance.

### references/error-scenarios.md
Comprehensive error catalog with resolution strategies:
- Error codes (ORG-001 through ORG-008)
- Root cause analysis for each error type
- Step-by-step resolution protocols
- Prevention strategies
- User communication templates
- When to escalate vs retry

Grep this file for specific error codes or search by symptom (e.g., "context overflow", "validation failure").

### assets/orchestration-plan.tmpl
Markdown template for presenting orchestration plans to users. Variables:
- `{scope_description}`: High-level scope summary
- `{agent_count}`: Number of agents to deploy
- `{agent_list_with_scopes}`: Bulleted list of agents + scopes
- `{execution_strategy}`: parallel/sequential/mixed
- `{coordination_points}`: Handoff descriptions
- `{deliverables}`: Expected outputs
- `{validation_gates}`: Quality checks

### assets/synthesis-report.tmpl
Markdown template for final synthesis reports. Variables:
- `{agent_summaries}`: Per-agent completion summaries
- `{deliverable_list_with_locations}`: Files created/modified with paths
- `{gate_results}`: format|lint|types|tests|coverage results
- `{evidence_status}`: Verification of completion evidence
- `{recommended_actions}`: Next steps for user

---

**Note:** This skill provides general orchestration patterns. For project-specific workflows (like aidev), combine this skill with project-specific guidance.
