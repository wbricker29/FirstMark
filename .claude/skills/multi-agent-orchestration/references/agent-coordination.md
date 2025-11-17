# Agent Coordination Patterns

## Overview

This reference provides detailed coordination patterns for managing complex multi-agent workflows. Use these patterns when orchestrating 3+ sub-agents with varying dependencies, execution requirements, and integration points.

## Sequential Execution Patterns

### When to Use Sequential Execution

Use sequential execution when:

- **Task dependencies exist**: Agent B requires outputs from Agent A
- **State must be preserved**: Each agent builds upon previous agent's work
- **Resource constraints**: Cannot run multiple agents simultaneously
- **Validation gates**: Each phase must pass validation before proceeding
- **Contextual learning**: Later agents need insights from earlier agents

**Do not use sequential when:**

- Tasks are independent and can run in parallel
- No information flows between agents
- Speed is critical and parallel execution is feasible

### Handoff Protocols

Effective handoffs between sequential agents require clear information transfer.

**Minimal handoff (preferred):**

```
Agent A completes → Extract key artifacts → Brief Agent B with:
  - Location of artifacts (file paths)
  - Summary of changes made (3-5 bullets)
  - Validation results (what passed/failed)
  - Context needed for next phase (NOT full context from A)
```

**Example handoff:**

```
Agent A (task-implementor) completed:
✅ Created lib/vector-search.ts with HNSW implementation
✅ Added unit tests with 85% coverage
✅ Type checking passes

Agent B (documentation-manager) brief:
- Update reference docs to reflect new vector search API
- Read lib/vector-search.ts (lines 1-120 only, focus on exported functions)
- Document performance characteristics from comments
- DO NOT reimplement or modify vector search logic
```

**What to pass:**

- ✅ File paths and line ranges
- ✅ High-level summaries
- ✅ Validation results
- ✅ Specific instructions for next agent
- ❌ Full conversation history
- ❌ Redundant context already in files
- ❌ Implementation details unless directly needed

### State Management Across Agents

Track orchestration state to maintain coherence across sequential agents.

**State tracking structure:**

```json
{
  "orchestration_id": "orch-2025-01-30-001",
  "phase": "execute",
  "agents_deployed": [
    {
      "agent_id": "agent-001",
      "type": "task-implementor",
      "status": "completed",
      "scope": "Implement vector search",
      "deliverables": ["lib/vector-search.ts", "lib/vector-search.test.ts"],
      "validation": {"format": "pass", "lint": "pass", "types": "pass", "tests": "pass"}
    },
    {
      "agent_id": "agent-002",
      "type": "documentation-manager",
      "status": "in_progress",
      "scope": "Update API documentation",
      "depends_on": ["agent-001"]
    }
  ],
  "context_budget": {
    "used_tokens": 45000,
    "limit_tokens": 200000,
    "threshold_warning": 150000
  }
}
```

**State update triggers:**

- Agent deployment (add entry with status: "in_progress")
- Agent completion (update status to "completed", record deliverables)
- Validation completion (record validation results)
- Context check (update token usage estimates)

**Use state to:**

- Prevent duplicate agent deployment
- Skip completed phases during retry
- Provide continuation context after interruptions
- Generate synthesis reports

### Sequential Execution Examples

**Example 1: Two-agent sequence (simple dependency)**

```
Scope: Add authentication feature

Agent A (task-implementor):
  Scope: Implement auth middleware
  Deliverables: lib/auth.ts, lib/auth.test.ts

  ↓ Handoff: Pass file paths + validation results

Agent B (principle-evaluator):
  Scope: Validate KISS/YAGNI adherence
  Context: lib/auth.ts (implementation only)
  Validation: Check for over-engineering, unnecessary abstractions
```

**Example 2: Three-agent sequence (linear pipeline)**

```
Scope: Refactor database layer

Agent A (Explore):
  Scope: Map all database access patterns
  Deliverables: database-patterns.md with file locations

  ↓ Handoff: Pass patterns report

Agent B (code-prettier):
  Scope: Refactor identified patterns
  Context: Files from patterns report
  Deliverables: Refactored db/*.ts files

  ↓ Handoff: Pass modified files + refactoring summary

Agent C (systematic-debugger):
  Scope: Verify no regressions introduced
  Context: Modified db/*.ts files + test suite
  Validation: Run tests, verify behavior unchanged
```

**Example 3: Four-agent sequence (iterative refinement)**

```
Scope: Optimize RAG pipeline performance

Agent A (Explore):
  Scope: Profile current performance bottlenecks
  Deliverables: performance-analysis.md

  ↓ Handoff: Pass analysis with top 3 bottlenecks

Agent B (task-implementor):
  Scope: Implement optimization for top bottleneck
  Context: Specific code sections from analysis
  Deliverables: Optimized code + benchmarks

  ↓ Handoff: Pass benchmark results

Agent C (principle-evaluator):
  Scope: Validate optimization maintains code quality
  Context: Modified code only
  Validation: Check complexity hasn't increased

  ↓ Handoff: Pass validation report

Agent D (documentation-manager):
  Scope: Document performance characteristics
  Context: Benchmark results + validation report
  Deliverables: Updated performance docs
```

## Parallel Execution Patterns

### When to Use Parallel Execution

Use parallel execution when:

- **Tasks are independent**: No information flows between agents
- **No shared resources**: Agents modify different files or isolated sections
- **Speed is critical**: Need to complete multiple tasks quickly
- **Validation can be deferred**: Can validate all outputs together at end

**Do not use parallel when:**

- Agents might conflict (modify same files)
- Dependencies exist between tasks
- Sequential learning is beneficial
- Context budget is tight (parallel = more context usage)

### Task Independence Validation

Before deploying agents in parallel, verify independence:

**Independence checklist:**

```
For each pair of parallel agents (A, B):
  ✅ Agent A and B modify different files
  ✅ Agent A does not need outputs from B (and vice versa)
  ✅ Agent A and B can validate independently
  ✅ Synthesis can merge outputs without conflicts
  ❌ If ANY check fails → Use sequential or hybrid pattern
```

**Common false independence:**

- "Add feature X" + "Add feature Y" → May share files (e.g., routes, types)
- "Refactor module A" + "Refactor module B" → May share interfaces
- "Write tests for X" + "Write tests for Y" → May conflict in test setup

**Verify independence:**

```
1. List files each agent will modify
2. Check for overlap → If overlap exists, agents are NOT independent
3. List data/types each agent will create → Check for naming conflicts
4. Consider integration points → Do agents affect same interfaces?
```

### Output Merging Strategies

When parallel agents complete, merge outputs into coherent result.

**Strategy 1: File-based merging (preferred for independent files)**

```
Agent A creates: lib/feature-a.ts, lib/feature-a.test.ts
Agent B creates: lib/feature-b.ts, lib/feature-b.test.ts
Agent C updates: docs/api-reference.md (section A)
Agent D updates: docs/api-reference.md (section D)

Merge:
  - Agents A, B have no conflicts (different files) ✅
  - Agents C, D may conflict (same file) ⚠️

Resolution:
  - Auto-merge A + B outputs
  - Manual review C + D outputs for doc conflicts
  - If C and D modify different sections → Auto-merge safe
  - If C and D modify overlapping sections → Manual reconciliation
```

**Strategy 2: Section-based merging (for shared files)**

```
Shared file: lib/config.ts

Agent A adds: Section "Database Config" (lines 10-25)
Agent B adds: Section "Cache Config" (lines 30-45)
Agent C updates: Section "API Config" (lines 50-60)

Merge:
  - Each agent modifies distinct section → Auto-merge safe ✅
  - Verify imports don't conflict
  - Verify no duplicate exports
```

**Strategy 3: Aggregate merging (for reports/documentation)**

```
Multiple agents generate analysis reports:

Agent A: performance-report.md
Agent B: security-report.md
Agent C: quality-report.md

Merge:
  - Create aggregate report with sections:
    ## Performance Analysis
    [Content from Agent A]

    ## Security Analysis
    [Content from Agent B]

    ## Quality Analysis
    [Content from Agent C]
```

**Conflict detection:**

```
After parallel execution, check for:
  - File overwrites (multiple agents modified same file)
  - Type definition conflicts (duplicate type names)
  - Import path conflicts (different agents added conflicting imports)
  - Test name conflicts (duplicate test descriptions)

If conflicts detected:
  - Document conflict locations
  - Deploy resolution agent to reconcile
  - Re-validate after resolution
```

### Parallel Execution Examples

**Example 1: Three parallel agents (fully independent)**

```
Scope: Implement three independent utility modules

Deploy simultaneously:

Agent A (task-implementor):
  Scope: Implement string utility functions
  Files: lib/utils/string.ts, lib/utils/string.test.ts

Agent B (task-implementor):
  Scope: Implement date utility functions
  Files: lib/utils/date.ts, lib/utils/date.test.ts

Agent C (task-implementor):
  Scope: Implement array utility functions
  Files: lib/utils/array.ts, lib/utils/array.test.ts

Independence verified:
  ✅ No shared files
  ✅ No shared types
  ✅ No dependencies between modules

Merge: Auto-merge all outputs (no conflicts possible)
```

**Example 2: Four parallel agents (document sections)**

```
Scope: Update technical documentation across multiple areas

Deploy simultaneously:

Agent A (documentation-manager):
  Scope: Update deployment documentation
  Files: docs/deployment.md

Agent B (documentation-manager):
  Scope: Update API reference
  Files: docs/api-reference.md

Agent C (documentation-manager):
  Scope: Update configuration guide
  Files: docs/configuration.md

Agent D (documentation-manager):
  Scope: Update troubleshooting guide
  Files: docs/troubleshooting.md

Independence verified:
  ✅ Each agent modifies different file
  ✅ No cross-references that would conflict

Merge: Auto-merge all outputs
```

**Example 3: Four parallel agents (feature modules)**

```
Scope: Implement four feature endpoints

Deploy simultaneously:

Agent A (task-implementor):
  Scope: Implement /api/users endpoint
  Files: app/api/users/route.ts, app/api/users/route.test.ts

Agent B (task-implementor):
  Scope: Implement /api/posts endpoint
  Files: app/api/posts/route.ts, app/api/posts/route.test.ts

Agent C (task-implementor):
  Scope: Implement /api/comments endpoint
  Files: app/api/comments/route.ts, app/api/comments/route.test.ts

Agent D (task-implementor):
  Scope: Implement /api/tags endpoint
  Files: app/api/tags/route.ts, app/api/tags/route.test.ts

Independence verified:
  ✅ Each agent has isolated route files
  ✅ Shared types predefined (not modified by agents)
  ⚠️  All may update lib/types.ts → CONFLICT RISK

Resolution:
  - Predefine types before deploying agents
  - Instruct agents: "Import types from lib/types.ts, DO NOT modify"
  - If types needed, list in agent brief explicitly
```

## Hybrid Patterns

Hybrid patterns combine sequential and parallel execution for complex workflows with mixed dependencies.

### Mixed Sequential + Parallel Workflows

**Pattern: Parallel → Sequential**

```
Use when: Multiple independent setup tasks, then unified integration

Setup phase (parallel):
  Agent A: Feature module 1
  Agent B: Feature module 2
  Agent C: Feature module 3

  ↓ Wait for all to complete

Integration phase (sequential):
  Agent D: Integrate modules + add routing
  Agent E: Generate integration tests
  Agent F: Update documentation
```

**Pattern: Sequential → Parallel**

```
Use when: Foundation task required, then parallel implementation

Foundation phase (sequential):
  Agent A: Analyze requirements + design architecture

  ↓ Handoff: Pass architecture design

Implementation phase (parallel):
  Agent B: Implement component 1 per design
  Agent C: Implement component 2 per design
  Agent D: Implement component 3 per design
```

**Pattern: Sequential → Parallel → Sequential**

```
Use when: Analysis, parallel work, then synthesis

Analysis phase (sequential):
  Agent A: Explore codebase + identify refactoring targets

  ↓ Handoff: Pass refactoring plan

Execution phase (parallel):
  Agent B: Refactor module 1
  Agent C: Refactor module 2
  Agent D: Refactor module 3

  ↓ Wait for all to complete

Validation phase (sequential):
  Agent E: Integration testing
  Agent F: Performance benchmarking
  Agent G: Documentation updates
```

### Dependency Graphs and Execution Order

Model complex dependencies using directed acyclic graphs (DAGs).

**Example dependency graph:**

```
       A (Explore codebase)
       |
       +--> B (Design architecture)
            |
            +----> C (Implement auth)
            |      |
            +----> D (Implement database layer)
            |      |
            +----> E (Implement API routes)
                   |
                   +-> F (Integration tests) <--+
                   |                            |
                   +-> G (Performance tests) ---+
                                                |
                                                v
                                           H (Documentation)
```

**Execution order:**

```
Wave 1: A (sequential - must run first)
Wave 2: B (sequential - depends on A)
Wave 3: C, D, E (parallel - all depend on B, independent of each other)
Wave 4: F, G (parallel - depend on C+D+E, independent of each other)
Wave 5: H (sequential - depends on F+G)
```

**Determining execution waves:**

```
1. Start with nodes that have no dependencies (root nodes)
2. Group all nodes with same maximum dependency depth
3. Within each wave, nodes can execute in parallel
4. Between waves, execution is sequential
```

**Complex dependency example:**

```
Scope: Migrate authentication system

A: Analyze current auth implementation
B: Design new auth architecture (depends on A)
C: Implement new auth middleware (depends on B)
D: Implement session management (depends on B)
E: Update user model (depends on B)
F: Migrate auth routes (depends on C, D, E)
G: Update frontend auth (depends on C, D, E)
H: Write migration guide (depends on B)
I: Integration tests (depends on F, G)
J: Update documentation (depends on H, I)

DAG:
       A
       |
       B
     / | \
    C  D  E
    |\ | /|
    | \|/ |
    |  F  G
     \ | /
       I
       |
       J

H runs parallel with F, G (depends only on B)

Execution:
Wave 1: A
Wave 2: B
Wave 3: C, D, E, H (parallel - all depend only on B)
Wave 4: F, G (parallel - depend on C+D+E)
Wave 5: I (sequential - depends on F+G)
Wave 6: J (sequential - depends on H+I)
```

### Hybrid Execution Examples

**Example 1: Analysis → Parallel implementation → Synthesis**

```
Scope: Optimize database queries across application

Wave 1 (Sequential - Analysis):
  Agent A (Explore):
    Scope: Profile all database queries, identify slow queries
    Deliverables: query-analysis.md with prioritized list

  ↓ Handoff: Top 5 slow queries with file locations

Wave 2 (Parallel - Implementation):
  Agent B (task-implementor):
    Scope: Optimize query in lib/users.ts
    Context: query-analysis.md + lib/users.ts

  Agent C (task-implementor):
    Scope: Optimize query in lib/posts.ts
    Context: query-analysis.md + lib/posts.ts

  Agent D (task-implementor):
    Scope: Optimize query in lib/search.ts
    Context: query-analysis.md + lib/search.ts

  ↓ Wait for all agents to complete

Wave 3 (Sequential - Validation):
  Agent E (systematic-debugger):
    Scope: Run performance benchmarks
    Context: Modified files from B, C, D
    Validation: Verify performance improvements

  ↓ Handoff: Benchmark results

  Agent F (documentation-manager):
    Scope: Document optimization approach
    Context: Modified files + benchmark results
    Deliverables: Updated performance docs
```

**Example 2: Foundation → Mixed parallel/sequential → Integration**

```
Scope: Add multi-language support to application

Wave 1 (Sequential - Foundation):
  Agent A (task-implementor):
    Scope: Implement i18n infrastructure
    Deliverables: lib/i18n.ts, locale files structure

  ↓ Handoff: i18n API + usage instructions

Wave 2 (Parallel - Content translation):
  Agent B (task-implementor):
    Scope: Add i18n to UI components
    Files: components/**/*.tsx

  Agent C (task-implementor):
    Scope: Add i18n to API messages
    Files: app/api/**/*.ts

Wave 3 (Sequential - Validation after Wave 2):
  Agent D (principle-evaluator):
    Scope: Validate consistent i18n usage
    Context: All files modified by B, C

  ↓ Handoff: Validation results

Wave 4 (Parallel - Documentation):
  Agent E (documentation-manager):
    Scope: Update developer documentation
    Files: docs/i18n-guide.md

  Agent F (documentation-manager):
    Scope: Update user-facing documentation
    Files: docs/languages.md
```

## Context Sharing

Efficient context sharing prevents redundant information transfer and manages token budgets.

### What to Pass Between Agents

**Minimal context principle:**
Pass only what the next agent needs to complete its specific task.

**Good context handoff:**

```
Agent A completed: Implemented feature X

Agent B brief:
  Scope: Write tests for feature X
  Context:
    - Read lib/feature-x.ts (lines 10-150, focus on exported functions)
    - Feature implements search with filters (summary)
    - Expected behavior: See function docstrings in implementation
  Instructions:
    - Test happy path + edge cases
    - Target 80%+ coverage
    - Use existing test patterns from lib/feature-y.test.ts
```

**Bad context handoff:**

```
Agent A completed: Implemented feature X

Agent B brief:
  Scope: Write tests for feature X
  Context:
    [Include full conversation history from Agent A]
    [Include all files Agent A read]
    [Include all design discussions]
    [Repeat entire feature spec]
```

**Context categories:**

| Category | Include | Exclude |
|----------|---------|---------|
| **File references** | Specific paths + line ranges | Full file contents (let agent read) |
| **Summaries** | Key decisions, changes made | Full implementation details |
| **Validation** | Pass/fail results | Full test output (link to files) |
| **Instructions** | Specific directives | General project knowledge |
| **Dependencies** | What agent needs from previous work | How previous agent completed work |

### How to Brief Agents Without Duplication

**Briefing structure:**

```
Agent: [agent-type]
Scope: [specific task, 1-2 sentences]

Context to read:
  - [file-path]: [what to focus on]
  - [file-path]: [specific sections]
  - [reference-doc]: [particular guidelines]

Background (minimal):
  - [Brief summary of relevant previous work]
  - [Key decisions affecting this task]

Instructions:
  - [Specific directive 1]
  - [Specific directive 2]
  - [Constraint 1]

Expected output:
  - [Deliverable 1]: [format/location]
  - [Deliverable 2]: [format/location]

Validation:
  - [Criteria 1]
  - [Criteria 2]
```

**Example brief:**

```
Agent: task-implementor
Scope: Add caching layer to vector search function

Context to read:
  - lib/vector-search.ts (lines 45-120, focus on searchVectors function)
  - spec/constitution.md (performance requirements section)
  - .env.example (cache configuration options)

Background:
  - Vector search currently hits database on every query
  - Performance target: <50ms for cached queries
  - Cache should use Redis (already configured in project)

Instructions:
  - Add Redis caching with 5-minute TTL
  - Cache key should include query hash + filters
  - Maintain existing function signature (no breaking changes)
  - Follow error handling pattern from lib/cache-utils.ts

Expected output:
  - Modified lib/vector-search.ts with caching
  - New lib/vector-search-cache.ts helper module
  - Unit tests in lib/vector-search.test.ts
  - Update existing tests to mock cache

Validation:
  - All existing tests pass
  - New tests cover cache hit/miss scenarios
  - Performance: cached queries <50ms (add benchmark)
```

### When to Use Shared Files vs In-Memory State

**Use shared files when:**

- Information needed by multiple agents across time
- Information should persist beyond orchestration session
- Information is structured and reusable (specs, reports, artifacts)
- Agent needs to reference exact content (code, documentation)

**Use in-memory state when:**

- Temporary coordination data (status tracking)
- Simple handoff information (file paths, summaries)
- Metadata about orchestration (agent status, token usage)
- Information not useful after orchestration completes

**Shared file examples:**

```
Create temporary shared files:
  - .claude/tmp/orchestration-state.json (agent status, dependencies)
  - .claude/tmp/analysis-results.md (exploration findings)
  - .claude/tmp/refactoring-plan.md (design for subsequent agents)

Cleanup after orchestration:
  - Move useful artifacts to permanent locations
  - Delete temporary coordination files
```

**In-memory state examples:**

```
Track in orchestration conversation:
  - Agent deployment order
  - Completion status
  - Brief summaries of deliverables
  - Validation results (pass/fail)
  - Handoff instructions to next agent
```

## Error Recovery

Handle failures gracefully and recover from partial completion.

### Retry Logic

**When to retry:**

- Transient errors (network timeouts, temporary resource unavailability)
- Context overflow (can reduce context and retry)
- Agent misunderstood instructions (can clarify and retry)
- Validation failure with clear fix (can adjust and retry)

**When NOT to retry:**

- Fundamental design issue (need to revise plan)
- Missing critical information (need to gather context first)
- Task exceeds agent capabilities (need different approach)
- Multiple retries already failed (need escalation)

**Retry protocol:**

```
1. Analyze failure:
   - What went wrong?
   - Why did it fail?
   - Is it retriable?

2. Determine adjustment:
   - Reduce context?
   - Clarify instructions?
   - Change validation criteria?
   - Split into smaller tasks?

3. Redeploy with adjustments:
   - Use same agent type
   - Modified brief with fixes
   - Document retry attempt
   - Set retry limit (max 3 attempts)

4. If retry succeeds:
   - Continue orchestration
   - Document lesson learned

5. If retry fails:
   - Escalate to user
   - Propose alternative approach
```

**Retry example:**

```
Agent A (task-implementor) failed:
  Error: "Context overflow - approaching token limit"

Analysis:
  - Agent was given too many files to read
  - Task scope too broad

Adjustment:
  - Split into two agents:
    Agent A1: Implement core functionality
    Agent A2: Implement helper utilities
  - Reduce context by removing unnecessary reference files

Retry:
  - Deploy Agent A1 with reduced scope
  - If succeeds, deploy Agent A2
  - If fails again, escalate
```

### Fallback Strategies

**Fallback hierarchy:**

```
Primary approach fails
  ↓
Try fallback approach 1
  ↓
Try fallback approach 2
  ↓
Escalate to user
```

**Fallback strategy examples:**

**Example 1: Parallel → Sequential fallback**

```
Primary: Deploy 4 agents in parallel
Failure: Context budget exceeded

Fallback:
  - Split into 2 sequential waves of 2 parallel agents each
  - Wave 1: Agents A, B (parallel)
  - Wave 2: Agents C, D (parallel)
```

**Example 2: Automated → Manual fallback**

```
Primary: Automated test generation
Failure: Agent cannot determine test scenarios

Fallback:
  - Ask user for test scenarios
  - Deploy agent with explicit test cases
  - Focus agent on test implementation, not design
```

**Example 3: Complex → Simple fallback**

```
Primary: Comprehensive refactoring
Failure: Scope too large, agent overwhelmed

Fallback:
  - Reduce to minimum viable refactoring
  - Focus on highest-impact changes only
  - Document remaining work as follow-up tasks
```

### Partial Completion Handling

**Scenarios:**

- Some agents succeed, others fail
- Orchestration interrupted mid-execution
- Validation passes for some outputs, fails for others

**Handling strategy:**

**1. Assess partial completion:**

```
Completed agents: [A, B]
Failed agents: [C]
Not yet deployed: [D, E]

Questions:
  - Can we use outputs from A, B?
  - Is C's work necessary for D, E?
  - Can we proceed without C?
```

**2. Determine continuation approach:**

**Option A: Fix and continue**

```
- Retry failed agent C
- If succeeds, continue with D, E
- Complete orchestration
```

**Option B: Partial acceptance**

```
- Accept work from A, B
- Defer C, D, E to later orchestration
- Document partial completion
- Update task status accordingly
```

**Option C: Rollback and redesign**

```
- Outputs from A, B unusable without C
- Rollback changes from A, B
- Redesign orchestration plan
- Restart with revised approach
```

**3. Document partial state:**

```json
{
  "orchestration_id": "orch-2025-01-30-002",
  "status": "partial_completion",
  "completed_agents": [
    {"id": "agent-001", "deliverables": ["file1.ts"], "validated": true},
    {"id": "agent-002", "deliverables": ["file2.ts"], "validated": true}
  ],
  "failed_agents": [
    {"id": "agent-003", "error": "context overflow", "retry_count": 2}
  ],
  "pending_agents": [
    {"id": "agent-004", "blocked_by": "agent-003"},
    {"id": "agent-005", "blocked_by": "agent-003"}
  ],
  "next_steps": [
    "Reduce context for agent-003 and retry",
    "If retry fails, escalate to user",
    "Consider splitting agent-003 scope into two agents"
  ]
}
```

### When to Abort vs Continue

**Abort orchestration when:**

- Fundamental assumption invalidated (requirements changed)
- Critical dependency unavailable (missing required files/APIs)
- Multiple retry attempts exhausted
- User requests cancellation
- Project state changed significantly (merge conflict, breaking changes)

**Continue orchestration when:**

- Failures are isolated and retriable
- Partial outputs are useful
- Remaining agents can proceed independently
- Fixes are straightforward
- User confirms continuation

**Decision criteria:**

```
Abort if:
  - Progress < 30% AND critical agent failed
  - Retry count > 3 for any agent
  - Context budget exhausted with no workaround
  - Validation failures indicate design flaw

Continue if:
  - Progress > 70% AND failures are minor
  - Retry likely to succeed
  - Partial completion has value
  - Alternative approaches available
```

## Integration Points

### How Agents Interact with Documentation Managers

Documentation managers ensure cross-document consistency and alignment.

**When to involve documentation-manager:**

- API changes requiring doc updates
- Cross-cutting changes affecting multiple docs
- Architecture decisions needing documentation
- New features requiring user guides

**Integration pattern:**

```
Task agents complete implementation
  ↓
Collect: Changed files + summaries
  ↓
Brief documentation-manager:
  - Changes made (implementation summary)
  - Documentation to update (specific files)
  - Standards to follow (docs style guide)
  ↓
Documentation-manager updates docs
  ↓
Validate: Documentation consistency
```

**Example integration:**

```
Agent A (task-implementor):
  Completed: New vector search API
  Files: lib/vector-search.ts
  Changes: Added 3 new exported functions

↓ Handoff to documentation-manager:

Agent B (documentation-manager):
  Scope: Update API reference for vector search changes
  Context:
    - Read lib/vector-search.ts (focus on exported functions + docstrings)
    - Update docs/api-reference.md (Vector Search section)
  Instructions:
    - Document new functions with examples
    - Update search options table
    - Add performance notes from code comments
  Validation:
    - Cross-reference all exported functions documented
    - Examples are runnable and correct
```

### How to Coordinate with Context Managers

Context managers handle context loading, token budgets, and scope management.

**Coordination touchpoints:**

**1. Pre-orchestration context check:**

```
Before deploying agents:
  - Estimate token usage for planned agents
  - Identify critical vs optional context
  - Determine if scope reduction needed
  - Use scripts/check_context_bounds.py
```

**2. During execution monitoring:**

```
While agents running:
  - Track cumulative token usage
  - Monitor context growth per agent
  - Alert if approaching limits
  - Suggest chunking if needed
```

**3. Post-execution cleanup:**

```
After orchestration:
  - Clear temporary context files
  - Archive important artifacts
  - Reset token usage counters
```

**Integration example:**

```
Orchestration Plan:
  5 agents, estimated 150k tokens total

Pre-flight:
  Context manager: "Token budget OK, proceed"

During execution (after 3 agents):
  Context manager: "120k tokens used, 80k remaining"
  Context manager: "Warning: Approaching limit"

Adjustment:
  Reduce context for remaining 2 agents
  Deploy with minimal briefings
  Reference files instead of loading full content

Post-execution:
  Context manager: "170k tokens used (within limits)"
  Cleanup temporary analysis files (15k tokens freed)
```

### When to Use Specialized Agents vs General-Purpose

**Specialized agents** (task-specific):

- Focused on narrow, well-defined tasks
- Deep expertise in particular domain
- Prescribed workflow or methodology
- Examples: systematic-debugger, principle-evaluator

**General-purpose agents** (flexible):

- Handle broad range of tasks
- Adaptable to various contexts
- No prescribed methodology
- Examples: task-implementor, Explore

**Decision criteria:**

| Use Specialized When | Use General-Purpose When |
|---------------------|-------------------------|
| Task fits agent's exact purpose | Task requires flexibility |
| Agent has specific methodology | No specialized agent exists |
| Domain expertise critical | Task spans multiple domains |
| Prescribed validation needed | Custom validation needed |
| Consistent output format required | Output format varies |

**Example decisions:**

```
Task: Debug failing test
Decision: Use systematic-debugger (specialized)
Reason: Prescribed debugging methodology ensures thorough investigation

Task: Implement new feature with tests
Decision: Use task-implementor (general-purpose)
Reason: Broad task requiring flexibility across implementation, testing, docs

Task: Validate code adheres to KISS principle
Decision: Use principle-evaluator (specialized)
Reason: Specific evaluation criteria and methodology

Task: Explore codebase to understand architecture
Decision: Use Explore (general-purpose)
Reason: Open-ended exploration, no specific methodology

Task: Refactor code for readability
Decision: Use code-prettier (specialized)
Reason: Specific focus on readability, prescribed refactoring patterns
```

**Mixing specialized and general-purpose:**

```
Wave 1: Explore (general-purpose) - Understand codebase
Wave 2: task-implementor (general-purpose) - Implement changes
Wave 3: principle-evaluator (specialized) - Validate KISS compliance
Wave 4: documentation-manager (specialized) - Update docs consistently
```

---

**Next Steps**: For phase-specific guidance, see `references/phase-playbooks.md`. For error handling details, see `references/error-scenarios.md`.
