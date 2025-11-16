# Phase Playbooks: Deep-Dive Execution Guidance

## Overview

This reference provides comprehensive per-phase execution guidance for the 5-phase multi-agent orchestration workflow. Each phase includes extended examples, edge cases, common failures, quality standards, tool usage recommendations, and decision points.

Use this reference when encountering unusual situations, complex scenarios, or when needing detailed guidance beyond the core SKILL.md workflow.

---

## Phase 1: Analyze (UNDERSTAND)

### Purpose

Establish comprehensive understanding of work requirements, gather necessary context, validate orchestration feasibility, and identify dependencies before planning agent deployment.

### Extended Examples

#### Example 1: Feature Implementation with Missing Context

**Scenario**: User requests "Add search filters to the product catalog" but provides no design specifications.

**Analysis steps:**
1. **Identify gaps in requirements:**
   - Which fields should be filterable?
   - What UI patterns exist for filters?
   - Are there performance constraints?
   - What's the expected user experience?

2. **Gather context proactively:**
   - Read existing product catalog code
   - Review UI component patterns
   - Check database schema for available fields
   - Look for similar filter implementations

3. **Ask clarifying questions:**
   ```
   Before proceeding, need clarity on:
   - Filter fields: [price, category, brand, rating]?
   - Filter UI: Sidebar, modal, or inline?
   - Performance: Expected product count? Pagination needed?
   - Existing patterns: Should match /users filter UI?
   ```

4. **Document understanding:**
   - Create analysis document with assumptions
   - List decided vs pending decisions
   - Map dependencies (UI → API → Database)

**Tool usage:**
- `Glob`: Find existing filter implementations (`**/*filter*.{ts,tsx}`)
- `Grep`: Search for filter patterns (`"Filter|filter" --type typescript`)
- `Read`: Examine product catalog files
- Output: Present clarifying questions to user before planning

**Decision point**: Do NOT proceed to planning until requirements are clear. Ambiguous requirements lead to wasted agent work.

#### Example 2: Refactoring Request with Broad Scope

**Scenario**: "Refactor the authentication system" - too vague, potentially massive scope.

**Analysis steps:**
1. **Explore current implementation:**
   ```
   - Use Grep to find all auth-related files
   - Map authentication flow (login → session → authorization)
   - Identify pain points (technical debt, security issues, maintainability)
   ```

2. **Scope boundaries:**
   ```
   Ask user:
   - What's driving this refactor? (Security, maintainability, performance?)
   - Which aspects: Session management? Auth middleware? Token handling? All?
   - Are there breaking changes acceptable?
   - Timeline constraints?
   ```

3. **Break down potential sub-tasks:**
   ```
   Possible scopes:
   A. Minimal: Refactor auth middleware only (narrow, safe)
   B. Moderate: Update session management + middleware (medium complexity)
   C. Comprehensive: Rebuild entire auth system (high risk, large scope)
   ```

4. **Risk assessment:**
   - Security implications (must maintain security guarantees)
   - Breaking changes (API compatibility)
   - Test coverage (existing tests as safety net)
   - Rollback strategy (if refactor fails)

**Tool usage:**
- `Grep`: Map auth usage (`"auth|Auth" --type typescript -C 2`)
- `Read`: Review critical auth files (middleware, session handler)
- `Bash`: Run tests to establish baseline (`pnpm test auth`)
- Output: Present scope options with risk/effort matrix

**Decision point**: Propose narrowest viable scope first. User can expand if needed. Prevents overwhelming orchestration.

#### Example 3: Bug Fix with System-Wide Impact

**Scenario**: "Fix the race condition in data sync" - potentially touches many components.

**Analysis steps:**
1. **Understand the bug:**
   - Reproduce the issue (if possible)
   - Identify affected components
   - Map data flow involved in race condition

2. **Assess blast radius:**
   ```
   Components involved:
   - Data sync service
   - State management
   - UI components reading sync state
   - Background workers
   - Database transactions
   ```

3. **Identify dependencies:**
   ```
   Fix requires:
   - Understanding async operation sequencing
   - Locking or coordination strategy
   - State consistency guarantees
   - Testing concurrent scenarios
   ```

4. **Validation strategy:**
   - How to verify fix works?
   - How to prevent regression?
   - What tests are needed?

**Tool usage:**
- `Grep`: Find sync-related code (`"sync|Sync" --type typescript`)
- `Read`: Study sync service implementation
- `Bash`: Check for existing race condition tests
- Output: Detailed analysis of race condition + proposed fix approach

**Decision point**: If analysis reveals complexity beyond 2-3 agents, propose incremental fix (address most critical path first, defer comprehensive solution).

### Edge Cases and Handling

#### Edge Case 1: Documentation Doesn't Exist

**Situation**: Orchestration requires project constitution/standards, but files don't exist.

**Handling:**
```
1. Ask user: "No project standards found. Options:
   a. Create constitution.md first (recommended)
   b. Proceed with general best practices
   c. User provides standards inline"

2. If user chooses (a):
   - Deploy /constitution command first
   - Resume orchestration after constitution created

3. If user chooses (b):
   - Document assumption: Using KISS/YAGNI/Quality principles
   - Proceed with orchestration
   - Note in deliverables: "Constitution recommended for future work"
```

**Key point**: Don't invent standards. Either use explicit standards or acknowledge using general principles.

#### Edge Case 2: Requirements Conflict

**Situation**: User requests "optimize for performance" AND "keep code simple" but these conflict for specific task.

**Handling:**
```
1. Identify specific conflict:
   "Performance optimization requires caching layer (adds complexity).
    This conflicts with 'keep simple' directive."

2. Present trade-off:
   "Options:
    a. Prioritize performance (add cache, accept complexity)
    b. Prioritize simplicity (skip cache, accept slower)
    c. Hybrid (simple cache, document trade-off)"

3. Wait for user decision before planning
```

**Key point**: Never resolve requirement conflicts autonomously. Always escalate to user.

#### Edge Case 3: Circular Dependencies Detected

**Situation**: Task A requires Task B, but Task B requires Task A (impossible to sequence).

**Handling:**
```
1. Document circular dependency:
   "Task A (implement UI) needs API shape from Task B
    Task B (implement API) needs UI requirements from Task A"

2. Identify break point:
   "Can break cycle by:
    a. Define API contract first (interface only)
    b. Implement stub API, then UI, then real API
    c. Design both together before implementing"

3. Propose resolution:
   "Recommended: Add Task 0 (design API contract)
    Then: Task A (UI) and Task B (API) can proceed"
```

**Tool usage:**
- Visual: Draw dependency graph to show cycle
- Document: Create interface definitions to break cycle

#### Edge Case 4: Scope Exceeds Context Budget

**Situation**: Pre-flight validation shows estimated 250k tokens (exceeds 200k limit).

**Handling:**
```
1. Run scripts/check_context_bounds.py to identify token usage

2. Identify reduction strategies:
   a. Split into multiple orchestrations (Phase 1 now, Phase 2 later)
   b. Reduce context files (only read essential files)
   c. Use smaller model (haiku instead of sonnet for simple agents)
   d. Parallelize less (reduces simultaneous context)

3. Present options:
   "Orchestration exceeds context budget by 50k tokens.
    Options:
    a. Split: Implement modules 1-3 now, 4-5 later (2 orchestrations)
    b. Optimize: Reduce reference docs loaded per agent
    c. Sequential: Deploy agents one-by-one (slower but lower peak)"

4. Adjust plan based on user choice
```

**Tool usage:**
- `Bash`: Run `scripts/check_context_bounds.py --phase 1 --files <list>`
- Output: Token usage report with breakdown

### Common Failures and Prevention

#### Failure 1: Proceeding with Ambiguous Requirements

**Symptom**: Agent produces work that doesn't match user intent.

**Root cause**: Skipped clarifying questions during analysis.

**Prevention:**
```
Checklist before planning:
  ✅ Deliverables are clearly defined (what files, what changes)
  ✅ Quality criteria are explicit (what makes it "done"?)
  ✅ Constraints are documented (what NOT to change)
  ✅ Edge cases are identified (what unusual scenarios to handle)
  ❌ If any unchecked, ask clarifying questions
```

**Recovery**: Pause orchestration, clarify with user, restart planning phase.

#### Failure 2: Missing Critical Context

**Symptom**: Agent fails because it needs information not available in briefing.

**Root cause**: Incomplete context gathering during analysis.

**Prevention:**
```
Context gathering checklist:
  ✅ Project structure understood (where things live)
  ✅ Standards/conventions identified (constitution, style guide)
  ✅ Dependencies mapped (what depends on what)
  ✅ Existing patterns found (how similar things are done)
  ✅ Integration points known (APIs, interfaces, contracts)
```

**Recovery**: Provide missing context to agent, allow retry with adjusted briefing.

#### Failure 3: Underestimating Task Complexity

**Symptom**: Single agent takes hours or fails due to scope too large.

**Root cause**: Didn't break down task into sub-tasks during analysis.

**Prevention:**
```
Complexity assessment:
  - Single agent task should be completable in ~15-30 minutes
  - If task involves 3+ distinct phases, split into multiple agents
  - If task touches 5+ files, consider parallelizing
  - If task requires extensive design, add planning agent first
```

**Recovery**: Pause agent, break task into smaller agents, redeploy with focused scopes.

### Quality Standards for Analysis Phase

**Phase complete when:**

- ✅ Task scope clearly defined in 2-3 sentences
- ✅ All deliverables specified (files, changes, artifacts)
- ✅ Dependencies mapped (what needs what)
- ✅ Context files identified (what to read)
- ✅ Validation criteria defined (how to verify success)
- ✅ Edge cases documented (unusual scenarios to handle)
- ✅ Ambiguities resolved (no unanswered questions)
- ✅ Context budget validated (won't exceed token limits)

**Quality check questions:**
```
1. Can I describe each sub-task in one sentence? (If no: scope unclear)
2. Do I know which files each agent will modify? (If no: incomplete analysis)
3. Can agents run independently or do they need sequencing? (Determines coordination)
4. What would "success" look like for each agent? (Defines validation)
5. Are there any blockers or missing information? (Identifies risks)
```

### Tool Usage Recommendations

**Primary tools for Phase 1:**

| Tool | Use Case | Example |
|------|----------|---------|
| `Glob` | Find files by pattern | `Glob("**/*auth*.ts")` |
| `Grep` | Search code for patterns | `Grep("import.*Auth", type="typescript")` |
| `Read` | Examine specific files | `Read("lib/auth.ts")` |
| `Bash` | Run validation scripts | `Bash("pnpm test")` to establish baseline |
| `Task` | Deploy exploration agent | `Task(subagent_type="Explore", prompt="Map auth flows")` |

**Tool selection criteria:**
- Use `Glob` when searching by filename pattern
- Use `Grep` when searching by code content
- Use `Read` when examining specific known files
- Use `Task` (Explore agent) when analysis is complex/exploratory
- Use `Bash` to validate current state (tests pass, builds work)

### Decision Points

#### Decision 1: Explore Agent vs Direct Analysis

**When to deploy Explore agent:**
- Codebase unfamiliar
- Task touches many unknown files
- Need to map architectural patterns
- Analysis itself is complex (>30 min)

**When to analyze directly:**
- Small, focused scope
- Familiar codebase
- Clear requirements
- Simple dependency structure

**Decision criteria**: If you would spend >10 file reads exploring, deploy Explore agent instead.

#### Decision 2: Ask User vs Make Assumption

**Ask user when:**
- Design decisions (UI patterns, API structure)
- Requirement ambiguities (what features to include)
- Trade-off choices (performance vs simplicity)
- Breaking changes (acceptable or not?)
- Priority conflicts (what's more important?)

**Make assumption when:**
- Following established patterns (use existing conventions)
- Technical implementation details (how to structure code)
- File organization (where to put new files)
- Test structure (how to organize tests)

**Rule**: Business/product decisions → ask user. Technical implementation → use judgment.

#### Decision 3: Validate Feasibility Before Planning

**Always validate:**
- Context budget (run check_context_bounds.py)
- Dependency cycles (check for circular dependencies)
- Agent availability (do necessary agent types exist?)
- Resource availability (files, APIs, data exist?)

**Proceed only if:**
- ✅ Context budget sufficient
- ✅ Dependencies are acyclic
- ✅ Agent types available
- ✅ Resources accessible

**If validation fails**: Adjust scope or approach before planning.

---

## Phase 2: Plan (DESIGN SUB-AGENT STRATEGY)

### Purpose

Design optimal sub-agent deployment strategy, establish coordination protocols, define agent scopes and interfaces, and secure user approval before execution.

### Extended Examples

#### Example 1: Simple Parallel Decomposition

**Scenario**: Add validation functions for 4 different data types (independent tasks).

**Planning steps:**
1. **Identify sub-tasks:**
   ```
   Task 1: Email validation function
   Task 2: Phone number validation function
   Task 3: Credit card validation function
   Task 4: Address validation function
   ```

2. **Validate independence:**
   ```
   ✅ Each creates separate file (lib/validators/email.ts, etc.)
   ✅ No shared types (each self-contained)
   ✅ No dependencies between validators
   ✅ Can test independently
   → Parallel execution safe
   ```

3. **Define agent scopes:**
   ```
   Agent A (task-implementor):
     Scope: Implement email validation with regex patterns
     Files: lib/validators/email.ts, lib/validators/email.test.ts
     Context: Existing validator pattern from lib/validators/string.ts
     Validation: 80%+ coverage, all edge cases tested

   Agent B (task-implementor):
     Scope: Implement phone validation with international formats
     Files: lib/validators/phone.ts, lib/validators/phone.test.ts
     Context: Existing validator pattern
     Validation: 80%+ coverage, support US/EU formats

   [Similar for Agents C and D]
   ```

4. **Establish coordination:**
   ```
   Execution: Parallel (all 4 agents deploy simultaneously)
   Handoff: None required (independent)
   Merge: Auto-merge (no conflicts possible)
   Validation: Run all tests after completion
   ```

**Plan presentation:**
```
🤖 Sub-Agent Orchestration Plan

Agents to deploy: 4
├─ Agent A (task-implementor): Email validation
├─ Agent B (task-implementor): Phone validation
├─ Agent C (task-implementor): Credit card validation
└─ Agent D (task-implementor): Address validation

Execution strategy: Parallel (all agents simultaneously)
Coordination points: None (fully independent)
Expected deliverables: 8 files (4 implementations + 4 test suites)
Validation gates: format|lint|types|tests|coverage(80%+)

Estimated time: ~20 minutes
Context budget: 45k tokens (well within limits)

Proceed? (y/n)
```

#### Example 2: Sequential Pipeline with Handoffs

**Scenario**: Optimize database queries - requires analysis, implementation, validation, documentation.

**Planning steps:**
1. **Identify phases:**
   ```
   Phase A: Analysis (identify slow queries)
   Phase B: Implementation (optimize queries)
   Phase C: Validation (verify performance)
   Phase D: Documentation (update perf docs)
   ```

2. **Map dependencies:**
   ```
   B depends on A (needs list of slow queries)
   C depends on B (needs optimized code)
   D depends on C (needs performance results)
   → Sequential execution required
   ```

3. **Define agent scopes:**
   ```
   Agent A (Explore):
     Scope: Profile database queries, identify top 5 slowest
     Output: query-analysis.md with query locations + metrics
     Time: ~10 minutes

   Agent B (task-implementor):
     Scope: Optimize top 3 queries from analysis
     Input: query-analysis.md
     Files: Modify query implementations
     Time: ~25 minutes

   Agent C (systematic-debugger):
     Scope: Run performance benchmarks, verify improvements
     Input: Modified query files
     Output: benchmark-results.md
     Time: ~15 minutes

   Agent D (documentation-manager):
     Scope: Update performance documentation
     Input: benchmark-results.md
     Files: docs/performance.md
     Time: ~10 minutes
   ```

4. **Design handoff protocol:**
   ```
   A → B: Pass query-analysis.md (top 3 queries + file locations)
   B → C: Pass modified files + optimization summary
   C → D: Pass benchmark results (before/after metrics)
   ```

**Plan presentation:**
```
🤖 Sub-Agent Orchestration Plan

Agents to deploy: 4
├─ Agent A (Explore): Profile queries → Identify slow queries
├─ Agent B (task-implementor): Optimize top 3 queries
├─ Agent C (systematic-debugger): Benchmark performance
└─ Agent D (documentation-manager): Update docs

Execution strategy: Sequential (4 phases)
Coordination points:
  - A → B: Query analysis report
  - B → C: Optimized code + summary
  - C → D: Benchmark results

Expected deliverables:
  - query-analysis.md
  - Modified query files (3-5 files)
  - benchmark-results.md
  - Updated docs/performance.md

Validation gates: format|lint|types|tests|performance(>2x improvement)

Estimated time: ~60 minutes
Context budget: 65k tokens

Proceed? (y/n)
```

#### Example 3: Hybrid Strategy (Analysis → Parallel → Synthesis)

**Scenario**: Add i18n support across UI, API, and email templates.

**Planning steps:**
1. **Identify workflow structure:**
   ```
   Wave 1 (Sequential): Setup i18n infrastructure
   Wave 2 (Parallel): Apply i18n to different areas
   Wave 3 (Sequential): Validate consistency
   ```

2. **Design agent deployment:**
   ```
   Wave 1:
     Agent A: Create i18n infrastructure (lib/i18n.ts, locale files)
     → Foundation for other agents

   Wave 2 (parallel after Wave 1):
     Agent B: Add i18n to UI components
     Agent C: Add i18n to API messages
     Agent D: Add i18n to email templates
     → Independent implementations

   Wave 3:
     Agent E: Validate i18n consistency
     Agent F: Update documentation
   ```

3. **Define coordination:**
   ```
   A completes → Handoff i18n API to B, C, D
   B, C, D complete → Wait for all, then deploy E
   E completes → Deploy F
   ```

**Plan presentation:**
```
🤖 Sub-Agent Orchestration Plan

Agents to deploy: 6

Wave 1 (Foundation):
├─ Agent A (task-implementor): i18n infrastructure

Wave 2 (Parallel implementation):
├─ Agent B (task-implementor): i18n for UI
├─ Agent C (task-implementor): i18n for API
└─ Agent D (task-implementor): i18n for emails

Wave 3 (Validation):
├─ Agent E (principle-evaluator): Consistency check
└─ Agent F (documentation-manager): Update docs

Execution strategy: Hybrid (sequential → parallel → sequential)
Coordination points:
  - Wave 1 → 2: i18n API + usage patterns
  - Wave 2 → 3: All i18n implementations complete

Expected deliverables:
  - lib/i18n.ts + locale files
  - ~20 modified component files
  - ~10 modified API files
  - ~5 modified email templates
  - docs/i18n-guide.md

Validation gates: format|lint|types|tests|coverage(80%+)

Estimated time: ~90 minutes (30 + 45 + 15)
Context budget: 110k tokens

Proceed? (y/n)
```

### Edge Cases and Handling

#### Edge Case 1: Agent Type Doesn't Exist

**Situation**: Need specialized agent (e.g., "SQL optimizer") but no such agent type exists.

**Handling:**
```
Option A: Use general-purpose agent with detailed instructions
  Agent: task-implementor
  Brief: "Act as SQL optimization expert. Analyze queries for N+1
         problems, missing indexes, inefficient joins..."

Option B: Deploy Explore agent first for analysis, then task-implementor
  Agent 1 (Explore): "Profile and identify optimization opportunities"
  Agent 2 (task-implementor): "Implement optimizations from analysis"

Option C: Ask user if specialized agent should be created
  "This task would benefit from specialized 'SQL optimizer' agent.
   For now, will use task-implementor with detailed SQL expertise brief.
   Consider creating specialized agent for future?"

Choose: Usually Option A (general-purpose with instructions)
```

#### Edge Case 2: User Requests Infeasible Parallelization

**Situation**: User says "deploy all agents in parallel" but tasks have dependencies.

**Handling:**
```
1. Explain dependency conflict:
   "Agent B (API implementation) requires types from Agent A (schema).
    Cannot deploy in parallel due to dependency."

2. Propose alternative:
   "Can partially parallelize:
    Wave 1: Agent A (schema)
    Wave 2: Agents B, C, D in parallel (all depend on A, independent of each other)"

3. Show trade-off:
   "Fully sequential: 80 minutes
    Hybrid approach: 50 minutes (saves 30 min)
    Risk: None (respects dependencies)"

4. Wait for user approval of adjusted plan
```

#### Edge Case 3: Context Budget Tight

**Situation**: Plan exceeds context budget during planning phase.

**Handling:**
```
1. Run scripts/check_context_bounds.py on planned agents

2. Identify context-heavy agents:
   "Agent B will load 15 files (40k tokens)
    Agent D will load 20 files (50k tokens)
    Total: 125k / 200k tokens"

3. Reduce context:
   Strategy A: Load only essential files
   Strategy B: Use file excerpts (line ranges) instead of full files
   Strategy C: Split agent into smaller scopes

4. Adjust plan:
   "Modified Agent B brief: Read only lib/core.ts (lines 1-200)
    instead of all 15 files. Reduces context by 25k tokens."

5. Re-validate budget
```

#### Edge Case 4: No Clear Validation Criteria

**Situation**: User request doesn't specify how to validate success.

**Handling:**
```
1. Propose validation based on task type:
   - Code implementation: Tests pass + coverage ≥80%
   - Refactoring: Behavior unchanged (all tests pass)
   - Documentation: Completeness + accuracy + clarity
   - Bug fix: Reproduction test passes + no regression

2. Present to user:
   "Validation plan:
    ✅ All existing tests pass (no regression)
    ✅ New tests for added functionality
    ✅ Coverage ≥80% on modified files
    ✅ Linting and formatting pass
    ✅ Type checking passes

    Additional validation needed? (y/n)"

3. Adjust based on user feedback
```

### Common Failures and Prevention

#### Failure 1: Over-Ambitious Parallelization

**Symptom**: Parallel agents conflict, modify same files, produce incompatible outputs.

**Root cause**: Incorrectly assumed task independence, skipped independence validation.

**Prevention:**
```
Independence validation checklist (perform during planning):
  For each pair of parallel agents:
    ✅ Modify different files OR different sections
    ✅ Create different types/interfaces (no naming conflicts)
    ✅ No information flow required between agents
    ✅ Can validate independently
    ✅ Merge strategy is clear

  If ANY check fails → Agents are NOT independent → Use sequential
```

**Recovery**: Switch to sequential or hybrid strategy, redeploy agents one-by-one.

#### Failure 2: Vague Agent Scopes

**Symptom**: Agent produces output that doesn't match expectations or exceeds scope.

**Root cause**: Agent brief was too vague, lacked specific constraints.

**Prevention:**
```
Scope definition checklist:
  ✅ Specific task described in 1-2 sentences
  ✅ Files to modify are listed explicitly
  ✅ Constraints are documented (what NOT to do)
  ✅ Expected output format specified
  ✅ Integration points defined (how output will be used)
  ✅ Time estimate provided (helps scope sizing)

Bad scope: "Improve the search feature"
Good scope: "Add price range filter to product search in components/ProductSearch.tsx.
            Use existing FilterControls pattern. Update search API query parameters.
            Do not modify search algorithm or ranking logic."
```

#### Failure 3: Missing Handoff Information

**Symptom**: Sequential agent fails because it doesn't have information from previous agent.

**Root cause**: Handoff protocol not defined during planning.

**Prevention:**
```
Handoff definition checklist:
  For each sequential transition (Agent A → Agent B):
    ✅ What information B needs from A (specific)
    ✅ Format of handoff (file path, summary, artifact)
    ✅ What B should NOT get (avoid context bloat)
    ✅ Where handoff information lives (file, in-memory)

Example handoff plan:
  "Agent A → Agent B:
   Pass: File paths of modified components (list)
   Pass: Summary of changes (3-5 bullets)
   Pass: Validation results (pass/fail + coverage %)
   Do NOT pass: Full implementation details (B will read files)
   Do NOT pass: Design discussions (not needed for B's task)"
```

### Quality Standards for Planning Phase

**Phase complete when:**

- ✅ All sub-agents identified with clear types
- ✅ Each agent has specific, bounded scope
- ✅ Execution strategy defined (parallel/sequential/hybrid)
- ✅ Dependencies mapped and validated (no cycles)
- ✅ Handoff protocols defined (for sequential agents)
- ✅ Context budget validated (within limits)
- ✅ Validation gates specified per agent
- ✅ User approval obtained (plan presented and confirmed)

**Quality check questions:**
```
1. Can each agent scope be described in 1-2 sentences? (If no: scope too vague)
2. Is execution order unambiguous? (If no: dependencies unclear)
3. Are parallel agents truly independent? (If no: will conflict)
4. Are handoff points defined? (If no: sequential agents may fail)
5. Is context budget realistic? (If no: will exceed limits)
6. Would I approve this plan if I were the user? (If no: revise)
```

### Tool Usage Recommendations

**Primary tools for Phase 2:**

| Tool | Use Case | Example |
|------|----------|---------|
| None | Planning is primarily cognitive | Design agent strategy mentally |
| `Read` | Review templates for plan | `Read("assets/orchestration-plan.tmpl")` |
| `Bash` | Validate scripts exist | `Bash("ls scripts/validate_orchestration.py")` |

**Note**: Planning phase is mostly cognitive work. Primary output is structured plan presented to user.

### Decision Points

#### Decision 1: Parallel vs Sequential

**Choose parallel when:**
- ✅ Tasks are independent (validated)
- ✅ No information flow between agents
- ✅ Speed is important
- ✅ Context budget allows multiple agents

**Choose sequential when:**
- ✅ Dependencies exist
- ✅ Information must flow between agents
- ✅ Later agents need outputs from earlier agents
- ✅ Context budget is tight

**Validation**: Run independence checklist for parallel candidates.

#### Decision 2: How Many Agents?

**Too few agents** (under-decomposition):
- Single agent takes >45 minutes
- Agent scope spans multiple domains
- High risk of failure due to complexity

**Too many agents** (over-decomposition):
- Each agent takes <5 minutes
- Coordination overhead > execution time
- Context budget wasted on handoffs

**Right-sizing**:
- Target: 15-30 minutes per agent
- Max: 3-5 agents per orchestration (sweet spot)
- Consider: Can 2 agents be combined? Should 1 agent be split?

#### Decision 3: When to Present Plan to User

**Always present plan when:**
- Complex orchestration (3+ agents)
- User provided high-level request (need confirmation on approach)
- Multiple valid strategies exist (user should choose)
- Significant time investment (>30 min total)

**Can skip presentation when:**
- User provided detailed, explicit plan
- Trivial orchestration (2 simple agents)
- User explicitly requested auto-execution

**Default**: Present plan. Better to over-communicate than under-communicate.

---

## Phase 3: Execute (DEPLOY & COORDINATE)

### Purpose

Deploy sub-agents with clear briefings, manage coordination and handoffs, monitor execution, track progress, and handle issues as they arise.

### Extended Examples

#### Example 1: Parallel Deployment (4 Independent Agents)

**Scenario**: Implement 4 validation utilities (from planning example).

**Execution steps:**

1. **Prepare all agent briefings:**
   ```
   [Prepare 4 detailed briefings offline before deploying]

   Agent A brief: Email validation
   Agent B brief: Phone validation
   Agent C brief: Credit card validation
   Agent D brief: Address validation
   ```

2. **Deploy all agents simultaneously (single message with 4 Task calls):**
   ```
   Deploy all 4 task-implementor agents in parallel:
   - Agent A: Email validation
   - Agent B: Phone validation
   - Agent C: Credit card validation
   - Agent D: Address validation
   ```

3. **Wait for all agents to complete:**
   ```
   Monitor progress:
   ✅ Agent A: Completed in 18 minutes
   ✅ Agent B: Completed in 22 minutes
   ✅ Agent C: Completed in 20 minutes
   ✅ Agent D: Completed in 25 minutes

   Total elapsed: 25 minutes (longest agent)
   ```

4. **Collect outputs:**
   ```
   Agent A delivered: lib/validators/email.ts, lib/validators/email.test.ts
   Agent B delivered: lib/validators/phone.ts, lib/validators/phone.test.ts
   Agent C delivered: lib/validators/card.ts, lib/validators/card.test.ts
   Agent D delivered: lib/validators/address.ts, lib/validators/address.test.ts

   Total: 8 files created
   ```

**Coordination notes:**
- No handoffs needed (parallel execution)
- No conflicts (different files)
- Proceed directly to validation phase

#### Example 2: Sequential Deployment (4-Agent Pipeline)

**Scenario**: Query optimization pipeline (from planning example).

**Execution steps:**

1. **Deploy Agent A (Explore):**
   ```
   Deploy: Agent A (Explore)
   Scope: Profile database queries, identify slow queries
   Context: Database query files in lib/queries/
   Output: query-analysis.md

   [Wait for completion - 12 minutes]

   ✅ Agent A completed:
      Created: query-analysis.md
      Identified: 5 slow queries (2 in lib/users.ts, 3 in lib/posts.ts)
   ```

2. **Extract handoff information for Agent B:**
   ```
   Read query-analysis.md (lines showing top 3 queries)

   Handoff info:
   - Query 1: lib/users.ts (line 45) - N+1 problem, 850ms avg
   - Query 2: lib/posts.ts (line 120) - Missing index, 650ms avg
   - Query 3: lib/posts.ts (line 200) - Inefficient join, 550ms avg
   ```

3. **Deploy Agent B (task-implementor):**
   ```
   Deploy: Agent B (task-implementor)
   Scope: Optimize top 3 slow queries
   Context:
     - query-analysis.md (top 3 queries section)
     - lib/users.ts (lines 40-60, focus on query at line 45)
     - lib/posts.ts (lines 115-125, 195-205)
   Instructions:
     - Fix N+1 in users query (use JOIN instead of multiple queries)
     - Add database index for posts query 1
     - Optimize join in posts query 2

   [Wait for completion - 28 minutes]

   ✅ Agent B completed:
      Modified: lib/users.ts, lib/posts.ts, migrations/add-index.sql
      Optimizations: N+1 resolved, index added, join optimized
   ```

4. **Extract handoff information for Agent C:**
   ```
   Handoff info:
   - Modified files: lib/users.ts, lib/posts.ts
   - Optimization summary: N+1 fix, new index, optimized join
   - Expected improvement: 850ms → ~100ms (users), 650ms → ~50ms (posts 1), 550ms → ~200ms (posts 2)
   ```

5. **Deploy Agent C (systematic-debugger):**
   ```
   Deploy: Agent C (systematic-debugger)
   Scope: Run performance benchmarks, verify improvements
   Context:
     - lib/users.ts (modified query)
     - lib/posts.ts (modified queries)
     - tests/performance/ (benchmark utilities)
   Instructions:
     - Benchmark modified queries (10 runs each)
     - Compare before/after metrics
     - Verify no functionality regressions

   [Wait for completion - 18 minutes]

   ✅ Agent C completed:
      Created: benchmark-results.md
      Results: Users 850→95ms (11x), Posts 650→48ms (13x), Posts 550→215ms (2.5x)
      Validation: All tests pass, no regressions
   ```

6. **Deploy Agent D (documentation-manager):**
   ```
   Deploy: Agent D (documentation-manager)
   Scope: Update performance documentation
   Context:
     - benchmark-results.md
     - docs/performance.md
   Instructions:
     - Document optimizations made
     - Add before/after metrics
     - Update performance expectations

   [Wait for completion - 10 minutes]

   ✅ Agent D completed:
      Modified: docs/performance.md
      Added: Query optimization case study section
   ```

**Total elapsed time:** 68 minutes (sequential pipeline)

#### Example 3: Hybrid Deployment (3 Waves)

**Scenario**: i18n implementation (from planning example).

**Execution steps:**

**Wave 1 (Sequential - Foundation):**
```
Deploy: Agent A (task-implementor)
Scope: Create i18n infrastructure
Deliverables: lib/i18n.ts, locales/en.json, locales/es.json

[Wait for completion - 25 minutes]

✅ Agent A completed:
   Created: lib/i18n.ts (i18n hook + provider)
   Created: locales/en.json, locales/es.json (structure)
   Updated: app/layout.tsx (added i18n provider)
```

**Wave 2 (Parallel - Implementation):**
```
Extract handoff info from Agent A:
  - i18n API: useTranslation() hook
  - Translation key format: "section.subsection.key"
  - Locale file structure: Nested JSON objects

Deploy 3 agents in parallel:

Agent B (task-implementor):
  Scope: Add i18n to UI components
  Context: lib/i18n.ts (API), components/**/*.tsx
  Pattern: Replace hardcoded strings with t('key')

Agent C (task-implementor):
  Scope: Add i18n to API messages
  Context: lib/i18n.ts (API), app/api/**/*.ts
  Pattern: Use i18n in server-side responses

Agent D (task-implementor):
  Scope: Add i18n to email templates
  Context: lib/i18n.ts (API), lib/email/**/*.ts
  Pattern: Use i18n in email content generation

[Deploy all 3 simultaneously]

[Wait for all to complete]

✅ Agent B completed in 30 minutes:
   Modified: 15 component files
   Updated: locales/en.json, locales/es.json (UI strings)

✅ Agent C completed in 25 minutes:
   Modified: 8 API route files
   Updated: locales/en.json, locales/es.json (API messages)

✅ Agent D completed in 20 minutes:
   Modified: 5 email template files
   Updated: locales/en.json, locales/es.json (email strings)

Total Wave 2 time: 30 minutes (longest agent)
```

**Wave 3 (Sequential - Validation):**
```
Deploy: Agent E (principle-evaluator)
Scope: Validate i18n consistency
Context: All modified files from B, C, D
Checks: All strings externalized, consistent key naming, no hardcoded text

[Wait for completion - 12 minutes]

✅ Agent E completed:
   Report: 98% strings externalized (3 exceptions in error handlers - documented)
   Validation: Consistent key naming, proper i18n usage
   Issues: None critical

Deploy: Agent F (documentation-manager)
Scope: Update documentation
Context: Agent E report, lib/i18n.ts
Deliverables: docs/i18n-guide.md

[Wait for completion - 10 minutes]

✅ Agent F completed:
   Created: docs/i18n-guide.md (usage guide)
   Updated: README.md (added i18n section)
```

**Total orchestration time:** 77 minutes (25 + 30 + 22)

### Edge Cases and Handling

#### Edge Case 1: Agent Exceeds Time Estimate

**Situation**: Agent expected to complete in 20 minutes, still running after 40 minutes.

**Handling:**
```
1. Check agent status:
   - Is it making progress? (new outputs appearing)
   - Is it stuck? (no activity for 10+ minutes)
   - Is it in loop? (repeating same actions)

2. If making progress:
   "Agent B is still working (40 min elapsed, expected 20 min).
    Task scope may have been larger than estimated.
    Continue waiting? (y/n)"

3. If stuck or looping:
   "Agent B appears stuck (no progress for 15 minutes).
    Options:
    a. Interrupt and redeploy with adjusted scope
    b. Provide additional context/guidance
    c. Wait longer (may resolve itself)"

4. Learn from experience:
   Document: "Task-implementor on refactoring tasks takes 2x estimate"
   Adjust future estimates accordingly
```

#### Edge Case 2: Context Overflow During Execution

**Situation**: Agent runs out of context mid-execution.

**Handling:**
```
1. Immediate action:
   "Agent C encountered context overflow.
    Current token usage: 185k / 200k"

2. Reduce context:
   Options:
   a. Remove unnecessary files from agent context
   b. Use file excerpts instead of full files
   c. Split agent scope into 2 smaller agents

3. Redeploy with reduced context:
   Agent C1: Focus on core implementation (reduced scope)
   Agent C2: Handle remaining work (if needed)

4. Prevention for remaining agents:
   Check context budget before deploying next agent
   Use scripts/check_context_bounds.py
```

#### Edge Case 3: Agent Produces Unexpected Output

**Situation**: Agent completes but output doesn't match expectations.

**Handling:**
```
1. Analyze mismatch:
   Expected: Modified 3 files with caching logic
   Actual: Modified 5 files, refactored entire module

2. Determine cause:
   - Brief was too vague? (scope not specific enough)
   - Agent over-optimized? (exceeded scope)
   - Misunderstood instructions? (clarity issue)

3. Decide on action:
   Option A: Accept if output is valid and beneficial
   Option B: Revert and redeploy with clearer scope
   Option C: Partially accept (keep good parts, redo others)

4. For this case:
   "Agent exceeded scope but improvements are valid.
    Accepting expanded changes.
    Note: Future briefs will emphasize scope boundaries more clearly."

5. Update remaining agents:
   Adjust downstream agent briefs to account for expanded changes
```

#### Edge Case 4: Parallel Agents Conflict

**Situation**: Two parallel agents modified same file, creating conflict.

**Handling:**
```
1. Detect conflict:
   "Merge conflict detected:
    Agent B modified lib/config.ts (lines 20-30)
    Agent C modified lib/config.ts (lines 25-35)
    Overlap: lines 25-30"

2. Analyze conflict:
   - Can changes coexist? (different sections → merge safe)
   - Are changes incompatible? (same lines → need resolution)

3. Resolution strategy:
   If coexist:
     Manually merge changes (verify no logical conflicts)

   If incompatible:
     Deploy resolution agent:
       Agent X (task-implementor):
         Scope: Reconcile conflicting config changes
         Context: Both versions of changes
         Instructions: Merge both features, resolve conflicts

4. Prevent future conflicts:
   Lesson: "Validate file-level independence more strictly"
   Action: During planning, explicitly list files per agent
```

### Common Failures and Prevention

#### Failure 1: Insufficient Agent Briefing

**Symptom**: Agent asks many questions or produces incorrect output.

**Root cause**: Briefing lacked critical information or context.

**Prevention:**
```
Briefing completeness checklist:
  ✅ Task scope: Exactly what to do (1-2 sentences)
  ✅ Context files: What to read with focus areas
  ✅ Background: Relevant decisions/constraints (brief)
  ✅ Instructions: Specific directives (3-5 bullets)
  ✅ Expected output: Files to create/modify, format
  ✅ Validation: Success criteria
  ✅ Constraints: What NOT to do (important!)
  ✅ Patterns: Examples to follow (if applicable)

Bad brief:
  "Implement caching for search"

Good brief:
  "Add Redis caching to vector search function in lib/vector-search.ts.
   Cache query results with 5-min TTL. Key format: hash(query+filters).
   Maintain existing function signature (no breaking changes).
   Use error handling pattern from lib/cache-utils.ts.
   Create helper module lib/vector-search-cache.ts.
   Update tests to mock cache calls.
   Expected: Modified lib/vector-search.ts + new lib/vector-search-cache.ts + tests."
```

#### Failure 2: Lost Context During Handoffs

**Symptom**: Sequential agent fails because it doesn't have information from previous agent.

**Root cause**: Handoff information wasn't explicitly passed.

**Prevention:**
```
Handoff execution pattern:
1. Agent A completes
2. Explicitly extract handoff info:
   - Read relevant output files
   - Summarize key points (3-5 bullets)
   - List deliverable locations
3. Brief Agent B with handoff info:
   "Agent A completed X. Deliverables: [files].
    Key points for your task: [bullets].
    Your task: [scope].
    Context: [handoff info + files to read]."
4. Do NOT assume Agent B will discover handoff info

Template:
  "Previous agent (Agent A) completed [task].
   Deliverables: [file list]
   Key information for your task:
     - [Point 1]
     - [Point 2]
     - [Point 3]
   Your task: [specific scope]
   Context to read: [specific files/sections]"
```

#### Failure 3: Parallel Execution Bottleneck

**Symptom**: One parallel agent takes much longer than others, negating parallelization benefit.

**Root cause**: Scope imbalance - agents not evenly sized.

**Prevention:**
```
Load balancing for parallel agents:
1. During planning, estimate each agent's time
2. If estimates vary significantly (>2x difference), rebalance:

   Before:
   Agent A: 10 minutes
   Agent B: 15 minutes
   Agent C: 45 minutes  ← Bottleneck
   Total: 45 minutes

   After rebalancing:
   Agent A: 10 minutes
   Agent B: 15 minutes
   Agent C1: 20 minutes (split C)
   Agent C2: 20 minutes (split C)
   Total: 20 minutes (then sequential C2: 20 min) = 40 minutes total

   Or: Run C1, C2 after A, B complete (still better)

Rule: In parallel wave, no agent should be >2x longest other agent
```

### Quality Standards for Execution Phase

**Phase complete when:**

- ✅ All planned agents deployed
- ✅ All agents completed (or handled failures)
- ✅ Outputs collected and organized
- ✅ Handoffs executed successfully (sequential)
- ✅ No unresolved conflicts (parallel)
- ✅ Preliminary validation passed (agents self-validated)

**Quality check questions:**
```
1. Did each agent complete its assigned scope? (If no: incomplete execution)
2. Were handoffs successful? (If no: information loss)
3. Are all deliverables present? (If no: missing outputs)
4. Did any agents exceed scope significantly? (If yes: scope creep)
5. Were conflicts detected and resolved? (If unresolved: validation will fail)
```

### Tool Usage Recommendations

**Primary tools for Phase 3:**

| Tool | Use Case | Example |
|------|----------|---------|
| `Task` | Deploy sub-agents | `Task(subagent_type="task-implementor", description="Implement caching", prompt="[detailed brief]")` |
| `Read` | Extract handoff info | `Read("query-analysis.md")` to extract top queries |
| `Bash` | Monitor progress | `Bash("ls -lt lib/")` to see recent file changes |

**Deployment patterns:**

**Parallel deployment (single message):**
```
Deploy all agents in parallel by using multiple Task tool calls in one message:
- Task(agent A)
- Task(agent B)
- Task(agent C)
[All deploy simultaneously]
```

**Sequential deployment (multiple messages):**
```
Message 1: Task(agent A)
[Wait for response]
Message 2: Extract handoff, Task(agent B)
[Wait for response]
Message 3: Extract handoff, Task(agent C)
[And so on...]
```

### Decision Points

#### Decision 1: Continue or Abort After Agent Failure

**Continue if:**
- ✅ Failure is isolated (other agents unaffected)
- ✅ Retry likely to succeed
- ✅ Partial completion has value
- ✅ Remaining work is substantial

**Abort if:**
- ❌ Failure invalidates entire orchestration
- ❌ Multiple retry attempts failed
- ❌ Fundamental assumption wrong
- ❌ User requests cancellation

**Example**: Agent 2 of 5 fails → Continue (retry Agent 2, others can proceed)
**Example**: Agent 1 of 5 fails (foundation) → Consider abort (others depend on it)

#### Decision 2: Provide Additional Context vs Redeploy

**Provide additional context when:**
- Agent asks clarifying question
- Agent on right track but needs guidance
- Quick context addition will unblock

**Redeploy when:**
- Agent went wrong direction
- Brief was fundamentally inadequate
- Scope needs adjustment
- Faster to restart than correct

**Rule**: If agent <30% done and off-track → redeploy. If >70% done → provide context to finish.

#### Decision 3: Intervene or Let Agent Finish

**Intervene when:**
- Agent clearly going wrong direction
- Agent exceeding scope significantly
- Agent will violate constraints
- Agent stuck in loop

**Let finish when:**
- Agent making progress (even if slow)
- Approach is valid (even if not expected)
- Near completion
- Uncertainty about whether approach is wrong

**Rule**: Don't intervene prematurely. Give agent chance to complete. Intervene only if confident there's a problem.

---

## Phase 4: Validate (SYNTHESIZE & VERIFY)

### Purpose

Synthesize sub-agent outputs into coherent result, verify completeness and quality, run comprehensive validation, identify gaps or issues, and ensure all requirements met.

### Extended Examples

#### Example 1: Parallel Agent Output Synthesis

**Scenario**: 4 validation utilities completed (from execution example).

**Validation steps:**

1. **Collect all outputs:**
   ```
   Agent A: lib/validators/email.ts, lib/validators/email.test.ts
   Agent B: lib/validators/phone.ts, lib/validators/phone.test.ts
   Agent C: lib/validators/card.ts, lib/validators/card.test.ts
   Agent D: lib/validators/address.ts, lib/validators/address.test.ts

   Total: 8 files
   ```

2. **Verify completeness:**
   ```
   ✅ All 4 agents completed their scopes
   ✅ All expected files created
   ✅ No missing deliverables
   ```

3. **Check for conflicts:**
   ```
   ✅ No file conflicts (each agent wrote to different files)
   ✅ No type name conflicts (run Grep for duplicate exports)
   ✅ No import conflicts
   → Clean merge, no manual reconciliation needed
   ```

4. **Synthesize outputs:**
   ```
   No synthesis needed - outputs are independent modules.
   Ready for validation gates.
   ```

5. **Run validation gates:**
   ```
   Bash("pnpm format") → ✅ All files formatted
   Bash("pnpm lint") → ✅ No linting errors
   Bash("pnpm type-check") → ✅ TypeScript validates
   Bash("pnpm test validators") → ✅ All tests pass (32 tests, 0 failures)

   Check coverage:
   Bash("pnpm test:coverage validators") → ✅ 87% average coverage
   ```

6. **Verify quality standards:**
   ```
   ✅ Format: All files formatted per project style
   ✅ Lint: No linting violations
   ✅ Types: Full type safety, no `any` types
   ✅ Tests: All tests pass, coverage >80%
   ✅ Documentation: Functions have docstrings
   ✅ Patterns: Consistent with existing validators
   ```

7. **Evidence of completion:**
   ```
   ✅ 8 files created as expected
   ✅ Test output shows 32 passing tests
   ✅ Coverage report confirms ≥80% coverage
   ✅ All quality gates passed
   → Validation complete, ready to report
   ```

#### Example 2: Sequential Pipeline Output Synthesis

**Scenario**: Query optimization pipeline completed (from execution example).

**Validation steps:**

1. **Collect outputs from each phase:**
   ```
   Agent A: query-analysis.md (identified slow queries)
   Agent B: Modified lib/users.ts, lib/posts.ts, migrations/add-index.sql
   Agent C: benchmark-results.md (performance metrics)
   Agent D: Updated docs/performance.md
   ```

2. **Verify completeness of pipeline:**
   ```
   Phase 1 (Analysis): ✅ query-analysis.md present, identifies 5 slow queries
   Phase 2 (Implementation): ✅ Top 3 queries optimized as planned
   Phase 3 (Benchmarking): ✅ Performance improvements verified
   Phase 4 (Documentation): ✅ Performance docs updated

   Pipeline complete: ✅ All phases delivered expected outputs
   ```

3. **Synthesize into coherent story:**
   ```
   Analysis identified 5 slow queries (850ms, 650ms, 550ms, 380ms, 320ms).
   Optimized top 3 queries:
     - Query 1: 850ms → 95ms (N+1 problem fixed)
     - Query 2: 650ms → 48ms (index added)
     - Query 3: 550ms → 215ms (join optimized)

   Total improvement: ~1.5 seconds saved per request cycle.
   Documentation updated to reflect new performance characteristics.
   ```

4. **Verify end-to-end:**
   ```
   Read lib/users.ts → ✅ N+1 fix implemented correctly (JOIN used)
   Read lib/posts.ts → ✅ Queries optimized as described
   Read migrations/add-index.sql → ✅ Index migration present
   Read benchmark-results.md → ✅ Metrics confirm improvements
   Read docs/performance.md → ✅ Documentation updated with new metrics
   ```

5. **Run validation gates:**
   ```
   Bash("pnpm format") → ✅ Formatted
   Bash("pnpm lint") → ✅ No errors
   Bash("pnpm type-check") → ✅ Types valid
   Bash("pnpm test queries") → ✅ All query tests pass

   Performance validation:
   Bash("pnpm test:performance queries") → ✅ Meets <100ms target
   ```

6. **Check for gaps:**
   ```
   ✅ All top 3 queries optimized (scope met)
   ⚠️  Queries 4 and 5 not optimized (expected, lower priority)
   ✅ Migration provided for database changes
   ✅ Tests pass (no regressions)
   ✅ Documentation reflects changes

   No critical gaps identified.
   ```

7. **Evidence of completion:**
   ```
   ✅ Performance metrics demonstrate success (quantified improvements)
   ✅ All tests pass (no functional regressions)
   ✅ Code review shows correct optimizations applied
   ✅ Documentation updated (completeness verified)
   → Validation complete
   ```

#### Example 3: Hybrid Execution Output Synthesis

**Scenario**: i18n implementation completed (from execution example).

**Validation steps:**

1. **Collect outputs from all waves:**
   ```
   Wave 1 (Foundation):
     Agent A: lib/i18n.ts, locales/en.json, locales/es.json, modified app/layout.tsx

   Wave 2 (Parallel implementation):
     Agent B: 15 modified components, updated locale files
     Agent C: 8 modified API routes, updated locale files
     Agent D: 5 modified email templates, updated locale files

   Wave 3 (Validation):
     Agent E: i18n-consistency-report.md
     Agent F: docs/i18n-guide.md, updated README.md
   ```

2. **Synthesize multi-wave outputs:**
   ```
   Infrastructure created: i18n system with 2 locales (en, es)

   Applied across application:
     - UI: 15 components internationalized
     - API: 8 endpoints return localized messages
     - Email: 5 templates support localization

   Total strings externalized: ~150 strings

   Validation: 98% strings externalized (3 exceptions documented)
   Documentation: Complete usage guide created
   ```

3. **Verify integration across waves:**
   ```
   Check: Do all waves use consistent i18n API?
     Read 5 random components → ✅ All use useTranslation() hook
     Read 3 API routes → ✅ All use i18n.t() function
     Read 2 email templates → ✅ All use i18n helpers

   Check: Are locale files complete?
     Read locales/en.json → ✅ Contains UI + API + email strings
     Read locales/es.json → ✅ All keys present (parallel to en.json)
     Validate structure → ✅ Nested structure consistent
   ```

4. **Check for conflicts/inconsistencies:**
   ```
   Grep for hardcoded strings:
   Grep('"[A-Z][a-z]+ [a-z]+"', glob="**/*.{ts,tsx}")
   → Found 3 instances (all in error handlers, documented by Agent E)

   Check translation key naming:
     Consistent pattern: section.component.key
     ✅ All keys follow pattern (validated by Agent E)
   ```

5. **Run validation gates:**
   ```
   Bash("pnpm format") → ✅
   Bash("pnpm lint") → ✅
   Bash("pnpm type-check") → ✅
   Bash("pnpm test") → ✅ All tests pass

   Manual validation:
   - Load app in browser, switch to Spanish → ✅ UI translates correctly
   - Test API with locale parameter → ✅ Returns Spanish messages
   - Generate test email in Spanish → ✅ Email content in Spanish
   ```

6. **Verify requirements met:**
   ```
   Original requirement: Add multi-language support

   ✅ Infrastructure: i18n system created
   ✅ Coverage: UI, API, emails all internationalized
   ✅ Quality: Consistent patterns, proper usage
   ✅ Documentation: Usage guide complete
   ✅ Testing: Manual validation confirms functionality

   Requirements fully met.
   ```

7. **Evidence of completion:**
   ```
   ✅ Agent E validation report (quantified: 98% strings externalized)
   ✅ Manual testing confirms translation works
   ✅ All quality gates passed
   ✅ Documentation complete
   ✅ Locale files contain all strings
   → Validation complete
   ```

### Edge Cases and Handling

#### Edge Case 1: Conflicting Outputs from Parallel Agents

**Situation**: Two agents modified same file differently, changes conflict.

**Handling:**
```
1. Identify conflict:
   Read lib/config.ts from Agent B → Added cache config (lines 20-30)
   Read lib/config.ts from Agent C → Added auth config (lines 20-35)
   Conflict: Both modified overlapping lines

2. Analyze compatibility:
   - Are changes logically compatible? (Both add config sections → YES)
   - Can they coexist? (Different config keys → YES)
   - Is merge safe? (No logic conflicts → YES)

3. Merge strategy:
   Manually merge:
     Lines 20-30: Cache config (from Agent B)
     Lines 31-45: Auth config (from Agent C, adjusted line numbers)

   Result: lib/config.ts contains both cache and auth config

4. Validate merged version:
   Bash("pnpm type-check") → ✅ Types valid
   Bash("pnpm test config") → ✅ Tests pass

   Merged version validated.

5. Document resolution:
   "Agents B and C both modified lib/config.ts.
    Manually merged both changes (cache + auth config).
    Validation confirms merge is correct."
```

#### Edge Case 2: Output Missing from Agent

**Situation**: Agent reported completion but expected file doesn't exist.

**Handling:**
```
1. Verify claim:
   Agent D claimed: "Created docs/api-guide.md"
   Check: Bash("ls docs/api-guide.md") → File not found

2. Investigate:
   - Agent error? (misreported completion)
   - File location wrong? (created in wrong directory)
   - Naming difference? (api-reference.md vs api-guide.md)

3. Search for file:
   Glob("**/api-*.md") → Found docs/api-reference.md (not api-guide.md)
   Read docs/api-reference.md → Contains expected content

4. Resolution:
   Agent created file with different name than claimed.
   Expected: docs/api-guide.md
   Actual: docs/api-reference.md

   Action: Accept actual file (content is correct)
   Note: "Agent D created docs/api-reference.md (not api-guide.md as claimed)"

5. Decide: Rename or keep?
   Check specs: No requirement for specific name
   Decision: Keep as api-reference.md (more conventional name)
```

#### Edge Case 3: Validation Gate Fails

**Situation**: Agent completed but tests fail.

**Handling:**
```
1. Identify failure:
   Bash("pnpm test") → 3 tests failing in lib/search.test.ts

2. Analyze failures:
   Read test output:
     - Test "should return empty for no results" fails
     - Test "should handle special characters" fails
     - Test "should validate input" fails

   All failures in search module (Agent B's scope)

3. Investigate root cause:
   Read lib/search.ts (Agent B's changes) → Implementation correct
   Read lib/search.test.ts → Tests not updated for new behavior

   Root cause: Agent B changed function signature but didn't update tests

4. Resolution options:
   Option A: Redeploy Agent B to fix tests
   Option B: Fix tests manually (if trivial)
   Option C: Deploy new agent to fix tests

   Choose: Option B (3 simple test updates)

5. Fix and re-validate:
   Edit lib/search.test.ts → Update 3 test calls with new signature
   Bash("pnpm test") → ✅ All tests pass

   Validation now passes, can proceed.

6. Document:
   "Agent B implementation correct but tests needed updates.
    Manually updated 3 tests to match new function signature.
    All tests now passing."
```

#### Edge Case 4: Incomplete Coverage of Requirements

**Situation**: Agents completed but some requirements not met.

**Handling:**
```
1. Compare deliverables to requirements:
   Requirement: "Add filters for price, category, and brand"

   Delivered:
     ✅ Price filter implemented
     ✅ Category filter implemented
     ❌ Brand filter missing

2. Investigate why:
   Review Agent C scope: "Implement price and category filters"
   → Agent completed its assigned scope
   → Brand filter was missed during planning

3. Determine criticality:
   Ask user: "Brand filter was not implemented. Is this required for completion?"

   If critical: Deploy additional agent for brand filter
   If optional: Document as follow-up work

4. Resolution (if critical):
   Deploy Agent E (task-implementor):
     Scope: Add brand filter
     Context: Existing price and category filters
     Pattern: Follow same pattern as other filters

   [Wait for completion]

   Re-validate with brand filter included.

5. Document:
   "Initial planning missed brand filter requirement.
    Deployed Agent E to complete brand filter.
    All filters now implemented and validated."
```

### Common Failures and Prevention

#### Failure 1: Skipping Validation Gates

**Symptom**: Proceed to reporting phase without running tests/linting/formatting.

**Root cause**: Assume agents validated their own work, skip comprehensive validation.

**Prevention:**
```
Mandatory validation checklist:
  ✅ Format check: pnpm format:check (or pnpm format)
  ✅ Lint check: pnpm lint
  ✅ Type check: pnpm type-check
  ✅ Tests: pnpm test [relevant scope]
  ✅ Coverage: pnpm test:coverage (if applicable)
  ✅ Build: pnpm build (if applicable)
  ✅ Project-specific: Any custom validation (benchmarks, integration tests)

NEVER skip these gates. They catch issues agents missed.
```

**Recovery**: Run validation gates before finalizing. Fix any failures found.

#### Failure 2: Not Verifying Completeness

**Symptom**: Proceed without checking if all requirements met.

**Root cause**: Trust agents completed work without verification.

**Prevention:**
```
Completeness verification:
1. List original requirements (from Phase 1)
2. List agent deliverables (from Phase 3)
3. Map each requirement to deliverable
4. Identify gaps:
   ✅ Requirement met
   ⚠️  Partially met (document gap)
   ❌ Not met (critical issue)

If ANY requirement not met → Investigate and address before reporting.
```

**Recovery**: Identify missing work, deploy additional agent or document as limitation.

#### Failure 3: Accepting Poor Quality Output

**Symptom**: Agent output works but violates quality standards (no tests, hardcoded values, poor naming).

**Root cause**: Validate only functionality, ignore code quality.

**Prevention:**
```
Quality standards checklist:
  ✅ Code follows project conventions (naming, structure)
  ✅ No hardcoded values (use config/constants)
  ✅ No placeholder comments ("TODO", "FIXME")
  ✅ Tests present and meaningful (not trivial)
  ✅ Coverage meets target (≥80% for modified code)
  ✅ Documentation present (docstrings, comments for complex logic)
  ✅ Error handling appropriate (no silent failures)
  ✅ Types explicit (no excessive `any` usage)

If quality issues found → Fix before reporting (manual edits or redeploy agent).
```

**Recovery**: Address quality issues through manual fixes or additional agent deployment.

### Quality Standards for Validation Phase

**Phase complete when:**

- ✅ All agent outputs collected and organized
- ✅ Completeness verified (all requirements met)
- ✅ Conflicts resolved (if any)
- ✅ Outputs synthesized into coherent result
- ✅ All validation gates passed (format|lint|types|tests)
- ✅ Quality standards met (coverage, documentation, conventions)
- ✅ Evidence of completion documented
- ✅ No critical issues remaining

**Quality check questions:**
```
1. Did all agents produce expected deliverables? (If no: investigate gaps)
2. Do validation gates pass? (If no: fix issues)
3. Are requirements fully met? (If no: deploy additional work)
4. Is code quality acceptable? (If no: refine outputs)
5. Is there evidence of correctness? (If no: add validation)
6. Can I confidently report success? (If no: identify what's missing)
```

### Tool Usage Recommendations

**Primary tools for Phase 4:**

| Tool | Use Case | Example |
|------|----------|---------|
| `Read` | Review agent outputs | `Read("lib/feature.ts")` |
| `Grep` | Search for issues | `Grep("TODO", output_mode="files_with_matches")` |
| `Bash` | Run validation gates | `Bash("pnpm test && pnpm lint && pnpm type-check")` |
| `Glob` | Find deliverables | `Glob("lib/**/*.test.ts")` to find all tests |

**Validation pattern:**
```
1. Collect outputs: Use Read/Glob to gather all deliverables
2. Check completeness: Map deliverables to requirements
3. Run gates: Use Bash to run project validation commands
4. Verify quality: Use Read to manually inspect critical files
5. Document evidence: Note all validation results
```

### Decision Points

#### Decision 1: Accept or Reject Agent Output

**Accept when:**
- ✅ Deliverables match expectations
- ✅ Validation gates pass
- ✅ Quality standards met
- ✅ No critical issues

**Reject when:**
- ❌ Missing deliverables
- ❌ Validation failures
- ❌ Poor quality (violates standards)
- ❌ Doesn't meet requirements

**Partial accept when:**
- ⚠️  Most work is good but has fixable issues
- ⚠️  Core functionality present, refinement needed
- Fix minor issues manually or with small agent deployment

#### Decision 2: Fix Issues Manually or Redeploy Agent

**Fix manually when:**
- Issue is trivial (typo, formatting, simple logic fix)
- Fix takes <5 minutes
- High confidence in correctness
- Redeploy would take longer

**Redeploy agent when:**
- Issue is complex (requires design thought)
- Multiple related issues (systematic problem)
- Uncertain about correct fix
- Want agent to validate its own fix

**Rule**: Manual fixes for <5 min issues. Redeploy for anything more complex.

#### Decision 3: Continue or Deploy Additional Agents

**Continue to reporting when:**
- ✅ All requirements met
- ✅ All validation passes
- ✅ Quality acceptable
- ✅ No critical gaps

**Deploy additional agents when:**
- ❌ Requirement not met (scope gap)
- ❌ Quality issues need dedicated agent (e.g., test coverage too low)
- ❌ Integration work needed (outputs need coordination)
- ❌ Documentation gaps (need documentation-manager)

**Example**: All code done but no docs → Deploy documentation-manager agent.

---

## Phase 5: Confirm (REPORT & DOCUMENT)

### Purpose

Generate comprehensive synthesis report, document orchestration results, update project documentation, communicate outcomes to user, and prompt for next actions.

### Extended Examples

#### Example 1: Simple Parallel Orchestration Report

**Scenario**: 4 validation utilities completed and validated.

**Reporting steps:**

1. **Generate synthesis report:**
   ```
   📊 Multi-Agent Orchestration Complete

   ## Deployed Agents
   - Agent A (task-implementor): Email validation ✅
   - Agent B (task-implementor): Phone validation ✅
   - Agent C (task-implementor): Credit card validation ✅
   - Agent D (task-implementor): Address validation ✅

   ## Deliverables
   Created 8 files:
   - lib/validators/email.ts (email validation with regex patterns)
   - lib/validators/email.test.ts (18 tests, 92% coverage)
   - lib/validators/phone.ts (international phone validation)
   - lib/validators/phone.test.ts (15 tests, 88% coverage)
   - lib/validators/card.ts (credit card number validation)
   - lib/validators/card.test.ts (12 tests, 85% coverage)
   - lib/validators/address.ts (address format validation)
   - lib/validators/address.test.ts (14 tests, 90% coverage)

   ## Validation Results
   ✅ Format check: PASS
   ✅ Lint check: PASS
   ✅ Type check: PASS
   ✅ Tests: PASS (59 tests, 0 failures)
   ✅ Coverage: 89% average (target: 80%)

   ## Changes Made
   - Files created: 8
   - Tests added: 59
   - Lines of code: ~850

   ## Execution Summary
   Execution strategy: Parallel (all agents simultaneously)
   Total time: 25 minutes
   Agents deployed: 4
   Success rate: 100%

   ## Next Steps
   - Import validators in application code
   - Add validators to form validation pipeline
   - Consider adding more validator types (URL, date, etc.)
   ```

2. **Update project documentation (if applicable):**
   ```
   No documentation updates needed - validators are self-documenting
   with TypeScript types and docstrings.
   ```

3. **Prompt user for next action:**
   ```
   Orchestration complete. What would you like to do next?
   - Continue: Integrate validators into application
   - Review: Examine specific validator implementation
   - Test: See example usage
   - Document: Create usage guide
   - Exit: Orchestration finished
   ```

#### Example 2: Complex Sequential Pipeline Report

**Scenario**: Query optimization pipeline completed.

**Reporting steps:**

1. **Generate synthesis report:**
   ```
   📊 Multi-Agent Orchestration Complete

   ## Deployed Agents
   - Agent A (Explore): Query analysis ✅
   - Agent B (task-implementor): Query optimization ✅
   - Agent C (systematic-debugger): Performance benchmarking ✅
   - Agent D (documentation-manager): Documentation update ✅

   ## Deliverables

   Analysis:
   - query-analysis.md (profiling report, identified 5 slow queries)

   Implementation:
   - lib/users.ts (optimized user query - N+1 fix)
   - lib/posts.ts (optimized 2 post queries - index + join optimization)
   - migrations/add-post-index.sql (database migration for new index)

   Validation:
   - benchmark-results.md (performance metrics before/after)

   Documentation:
   - docs/performance.md (updated with optimization case study)

   ## Validation Results
   ✅ Format check: PASS
   ✅ Lint check: PASS
   ✅ Type check: PASS
   ✅ Tests: PASS (all query tests pass, no regressions)
   ✅ Performance: PASS (all targets met)

   ## Performance Improvements
   Query 1 (users): 850ms → 95ms (9x faster, N+1 eliminated)
   Query 2 (posts): 650ms → 48ms (13.5x faster, index added)
   Query 3 (posts): 550ms → 215ms (2.6x faster, join optimized)

   Total improvement: ~1.5 seconds saved per request cycle

   ## Changes Made
   - Files modified: 3 (lib/users.ts, lib/posts.ts, docs/performance.md)
   - Files created: 3 (query-analysis.md, benchmark-results.md, migrations/add-post-index.sql)
   - Database migrations: 1 (index creation)
   - Performance improvements: 3 queries optimized

   ## Execution Summary
   Execution strategy: Sequential (4-phase pipeline)
   Total time: 68 minutes
   Phases: Analysis(12m) → Implementation(28m) → Benchmarking(18m) → Documentation(10m)
   Success rate: 100%

   ## Next Steps
   - Run database migration: `pnpm db:migrate`
   - Deploy optimizations to production
   - Monitor query performance in production
   - Consider optimizing remaining 2 queries (lower priority)
   ```

2. **Update project documentation:**
   ```
   Documentation already updated by Agent D:
   - docs/performance.md now includes query optimization case study
   - Benchmark results documented
   - Performance expectations updated

   No additional documentation needed.
   ```

3. **Document decision log (if significant decisions made):**
   ```
   No architectural decisions made. Implementation followed standard
   optimization patterns (eliminate N+1, add indexes, optimize joins).
   Decision log update not required.
   ```

4. **Prompt user for next action:**
   ```
   Orchestration complete. Database migration pending.

   Next steps:
   1. Run migration: `pnpm db:migrate` (creates index)
   2. Restart development server
   3. Verify query improvements in development

   What would you like to do?
   - Run migration now
   - Review optimization details
   - Test in development environment
   - Commit changes
   - Exit
   ```

#### Example 3: Large Hybrid Orchestration Report

**Scenario**: i18n implementation completed.

**Reporting steps:**

1. **Generate comprehensive synthesis report:**
   ```
   📊 Multi-Agent Orchestration Complete

   ## Deployed Agents (6 agents, 3 waves)

   Wave 1 - Foundation:
   - Agent A (task-implementor): i18n infrastructure ✅

   Wave 2 - Implementation (parallel):
   - Agent B (task-implementor): UI components i18n ✅
   - Agent C (task-implementor): API messages i18n ✅
   - Agent D (task-implementor): Email templates i18n ✅

   Wave 3 - Validation:
   - Agent E (principle-evaluator): Consistency validation ✅
   - Agent F (documentation-manager): Documentation ✅

   ## Deliverables

   Infrastructure:
   - lib/i18n.ts (i18n hook, provider, utilities)
   - locales/en.json (English translations - 158 strings)
   - locales/es.json (Spanish translations - 158 strings)
   - app/layout.tsx (added i18n provider)

   UI Internationalization:
   - 15 component files modified (components/**/*.tsx)
   - All UI text externalized using useTranslation() hook

   API Internationalization:
   - 8 API route files modified (app/api/**/*.ts)
   - All response messages externalized using i18n.t()

   Email Internationalization:
   - 5 email template files modified (lib/email/**/*.ts)
   - All email content supports localization

   Validation & Documentation:
   - i18n-consistency-report.md (validation results)
   - docs/i18n-guide.md (usage guide for developers)
   - README.md (added i18n section)

   ## Validation Results
   ✅ Format check: PASS
   ✅ Lint check: PASS
   ✅ Type check: PASS
   ✅ Tests: PASS (all tests pass, i18n doesn't break functionality)
   ✅ String externalization: 98% (3 exceptions documented)
   ✅ Manual testing: PASS (UI, API, emails all translate correctly)

   ## Changes Made
   - Files created: 5 (i18n infrastructure + docs)
   - Files modified: 29 (15 components + 8 API routes + 5 emails + 1 layout)
   - Strings externalized: 158
   - Languages supported: 2 (English, Spanish)
   - Translation coverage: 100% (all keys translated)

   ## Execution Summary
   Execution strategy: Hybrid (sequential → parallel → sequential)
   Total time: 77 minutes
   Wave 1: 25 minutes (foundation)
   Wave 2: 30 minutes (parallel implementation)
   Wave 3: 22 minutes (validation + docs)
   Agents deployed: 6
   Success rate: 100%

   ## Quality Notes
   - 98% strings externalized (3 exceptions in error handlers - acceptable)
   - Consistent translation key naming (section.component.key pattern)
   - All locale files use nested JSON structure (maintainable)
   - Documentation includes usage examples and guidelines

   ## Known Limitations
   - 3 error handler strings remain hardcoded (technical limitation documented)
   - Only 2 languages supported initially (more can be added easily)
   - Date/time formatting not yet localized (future enhancement)

   ## Next Steps
   - Test application in both languages (English/Spanish)
   - Add more language support if needed (French, German, etc.)
   - Consider adding date/time localization
   - Deploy to staging for QA testing
   ```

2. **Update project documentation:**
   ```
   Agent F already updated:
   - docs/i18n-guide.md (new developer guide)
   - README.md (added i18n section)

   Additional recommended updates:
   - specs/constitution.md: Add i18n as project standard
   - specs/spec.md: Update to reflect i18n requirement

   Would you like me to update these files? (y/n)
   ```

3. **Document decision log:**
   ```
   Significant architectural decision made:

   Decision: Use client-side i18n with React hooks
   Rationale: Next.js 15 App Router with Server Components
   Alternatives considered:
     - Server-side i18n (rejected: complex with React Server Components)
     - Route-based i18n (rejected: adds complexity to routing)
   Impact:
     - Translation happens client-side (acceptable performance)
     - Locale state managed in React context
     - SEO: Can add server-side metadata translation later if needed

   Would you like me to document this in project decision log? (y/n)
   ```

4. **Prompt user for next action:**
   ```
   Orchestration complete. i18n fully implemented.

   Recommended next steps:
   1. Test application:
      - Load app, switch to Spanish, verify UI translates
      - Test API endpoints with locale parameter
      - Generate test emails in both languages

   2. Deploy to staging for QA testing

   3. Add more languages (if needed):
      - Create locales/[lang].json
      - Copy key structure from en.json
      - Translate strings

   4. Commit changes:
      - 34 files changed
      - Recommend commit message: "feat: add i18n support for UI, API, and emails"

   What would you like to do next?
   - Test: Manually test i18n functionality
   - Expand: Add more languages
   - Review: Examine specific implementation
   - Commit: Commit all changes
   - Document: Update specs with i18n decision
   - Exit: Orchestration finished
   ```

### Edge Cases and Handling

#### Edge Case 1: Orchestration Partially Failed

**Situation**: Some agents succeeded, some failed, proceeded with partial completion.

**Handling:**
```
📊 Multi-Agent Orchestration: Partial Completion

## Status: ⚠️  PARTIAL SUCCESS

## Deployed Agents
- Agent A (Explore): Analysis ✅
- Agent B (task-implementor): Module 1 implementation ✅
- Agent C (task-implementor): Module 2 implementation ❌ FAILED
- Agent D (documentation-manager): Not deployed (blocked by C)

## Completed Work

Successfully delivered:
- query-analysis.md (analysis report)
- lib/module1.ts (implementation)
- lib/module1.test.ts (tests, 85% coverage)

## Failed Components

Agent C failure:
- Scope: Implement Module 2
- Error: Context overflow during execution
- Root cause: Module 2 scope too large for single agent
- Status: Not completed

Agent D:
- Status: Not deployed (depends on Agent C)
- Scope: Update documentation

## Partial Deliverables Status
✅ Analysis: Complete
✅ Module 1: Complete and validated
❌ Module 2: Not completed
❌ Documentation: Not completed

## Validation Results (Partial)
✅ Format check: PASS (for completed work)
✅ Lint check: PASS
✅ Type check: PASS
✅ Tests: PASS (Module 1 tests)
⚠️  Coverage: Module 1 only (Module 2 pending)

## Recommended Next Steps

Option A: Resume orchestration
- Break Agent C scope into 2 smaller agents (C1, C2)
- Deploy C1 and C2 sequentially
- Deploy Agent D after C1, C2 complete
- Estimated time: 40 minutes

Option B: Accept partial completion
- Keep Module 1 implementation
- Defer Module 2 to future work
- Update documentation for Module 1 only
- Estimated time: 15 minutes

Option C: Rollback and redesign
- Revert Module 1 changes
- Redesign orchestration with different scope
- Restart with revised plan
- Estimated time: 60+ minutes

Recommendation: Option A (resume with adjusted scope)

What would you like to do?
- Resume: Complete Module 2 with adjusted approach
- Accept: Keep Module 1, defer Module 2
- Rollback: Revert and redesign
- Review: Examine failure details
```

#### Edge Case 2: User Requests Additional Work During Reporting

**Situation**: During confirmation phase, user asks "also add feature X".

**Handling:**
```
Current orchestration complete (4 agents deployed successfully).

User request: "Also add logging to all validator functions"

This is new scope, not part of original orchestration.

Options:
1. Start new orchestration:
   - Treat as separate task
   - Plan agent deployment for logging feature
   - Estimate: 20 minutes (1 agent)

2. Extend current orchestration:
   - Deploy Agent E for logging
   - Continue current session
   - Update synthesis report after completion

3. Document as follow-up:
   - Add to task list / backlog
   - Complete current orchestration first
   - Address logging in future session

Recommendation: Option 1 (new orchestration)
Rationale: Keeps orchestrations focused, separate concern

Would you like me to:
a. Start new orchestration for logging feature now
b. Complete current orchestration and add logging to backlog
c. Extend current orchestration with logging agent
```

#### Edge Case 3: No Clear Next Steps

**Situation**: Work is complete but no obvious next action.

**Handling:**
```
📊 Multi-Agent Orchestration Complete

[... standard synthesis report ...]

## Next Steps

Work is complete. Possible follow-up actions:

Development:
- Use new validators in application forms
- Add more validator types (URL, date, etc.)
- Extend existing validators with additional rules

Quality:
- Review validator implementation details
- Add more test cases for edge cases
- Perform code review

Deployment:
- Commit changes to version control
- Create pull request for review
- Deploy to staging environment

Documentation:
- Create usage guide for validators
- Add examples to documentation
- Update API reference

Planning:
- Identify next feature to implement
- Review project backlog
- Plan next orchestration

What would you like to do?
- Review: Examine implementation details
- Test: See example usage
- Commit: Commit all changes
- Plan: Identify next task
- Exit: Orchestration finished

(Or describe specific next action)
```

#### Edge Case 4: Validation Passed But User Not Satisfied

**Situation**: All validation gates passed but user says "this isn't what I wanted".

**Handling:**
```
All validation gates passed but output doesn't meet expectations.

Let's identify the gap:
1. What's wrong with the current implementation?
   [Wait for user response]

2. What was expected instead?
   [Wait for user response]

3. Was the initial requirement clear?
   - If unclear: Requirement ambiguity caused mismatch
   - If clear: Implementation deviated from requirement

Analysis:
[Based on user response]

Options:
A. Adjust and redeploy:
   - Modify agent scopes to match expectations
   - Redeploy affected agents
   - Re-validate

B. Refine current implementation:
   - Keep core work, refine details
   - Deploy refinement agent with specific adjustments
   - Faster than full redeploy

C. Start over with clearer requirements:
   - Revert current changes
   - Clarify requirements in detail
   - Restart orchestration with adjusted plan

Based on the gap you described, I recommend: [option with rationale]

How would you like to proceed?
```

### Common Failures and Prevention

#### Failure 1: Vague or Incomplete Synthesis Report

**Symptom**: Report doesn't clearly communicate what was accomplished.

**Root cause**: Report omits key details or uses vague language.

**Prevention:**
```
Synthesis report must include:
  ✅ All agents deployed (with types and scopes)
  ✅ All deliverables with descriptions
  ✅ Validation results (explicit pass/fail per gate)
  ✅ Quantitative metrics (files, tests, coverage, performance)
  ✅ Changes made (files created/modified, lines of code)
  ✅ Execution summary (time, strategy, success rate)
  ✅ Next steps (specific, actionable)

Bad: "Implemented search feature"
Good: "Implemented product search with price filters (components/ProductSearch.tsx),
      added 12 tests (85% coverage), all validation gates passed"
```

#### Failure 2: Not Prompting for Next Action

**Symptom**: Report ends without asking user what to do next.

**Root cause**: Assume orchestration fully complete, don't prompt for continuation.

**Prevention:**
```
Always end reporting phase with clear next action prompt:

Bad:
  "Orchestration complete."
  [End]

Good:
  "Orchestration complete. What would you like to do next?
   - Test: Manually test new feature
   - Review: Examine implementation details
   - Commit: Commit all changes
   - Continue: Implement next feature
   - Exit: Orchestration finished"

Provide specific options relevant to completed work.
```

#### Failure 3: Missing Documentation Updates

**Symptom**: Code changes complete but documentation not updated.

**Root cause**: Forget to check if documentation needs updates.

**Prevention:**
```
Documentation update checklist:
  ✅ API changes → Update API reference docs
  ✅ New features → Update user guides
  ✅ Architecture changes → Update architecture docs / decision log
  ✅ Configuration changes → Update configuration guides
  ✅ Breaking changes → Update migration guides
  ✅ Performance changes → Update performance docs

If ANY documentation should be updated → Either:
  - Deploy documentation-manager agent (if not already done)
  - Recommend documentation updates to user
  - Document as follow-up work

Never assume documentation updates can be skipped.
```

### Quality Standards for Confirmation Phase

**Phase complete when:**

- ✅ Comprehensive synthesis report generated
- ✅ All deliverables documented with descriptions
- ✅ Validation results explicitly stated
- ✅ Changes quantified (files, lines, tests, etc.)
- ✅ Documentation updated (or flagged for update)
- ✅ Next steps clearly identified
- ✅ User prompted for next action
- ✅ Session can be closed cleanly

**Quality check questions:**
```
1. Does report clearly communicate what was accomplished? (If no: add detail)
2. Are all deliverables listed and described? (If no: complete list)
3. Are validation results explicit? (If no: add validation details)
4. Does user know what to do next? (If no: provide options)
5. Is documentation up to date? (If no: update or flag)
6. Can orchestration session close cleanly? (If no: address remaining items)
```

### Tool Usage Recommendations

**Primary tools for Phase 5:**

| Tool | Use Case | Example |
|------|----------|---------|
| `Read` | Review template | `Read("assets/synthesis-report.tmpl")` |
| `Bash` | Generate report script | `Bash("python scripts/synthesize_reports.py")` |
| `Write` | Save report to file | `Write("reports/orchestration-report.md", content)` (if needed) |

**Reporting pattern:**
```
1. Gather information from all phases
2. Structure using template or manual format
3. Include all required sections (agents, deliverables, validation, next steps)
4. Present to user
5. Prompt for next action
6. Document session outcome (if significant)
```

### Decision Points

#### Decision 1: Detailed vs Summary Report

**Detailed report when:**
- Complex orchestration (5+ agents)
- Multiple waves or phases
- Significant architectural changes
- Many deliverables

**Summary report when:**
- Simple orchestration (2-3 agents)
- Single straightforward task
- Few deliverables
- Self-evident outcomes

**Default**: Err toward more detail. Better to over-communicate than under-communicate.

#### Decision 2: Update Documentation Now or Defer

**Update now when:**
- Documentation-manager agent already deployed
- Quick updates (<5 minutes)
- Critical documentation (must be in sync with code)

**Defer when:**
- Documentation updates are extensive (>15 minutes)
- User prefers to handle documentation separately
- Documentation can wait for PR review

**Ask user**: "Documentation updates recommended. Update now or defer?"

#### Decision 3: Close Session or Continue

**Close session when:**
- All work complete
- User satisfied
- No immediate follow-up
- Natural stopping point

**Continue when:**
- User requests additional work
- Follow-up orchestration needed
- Issues discovered requiring fixes
- User wants to proceed immediately

**Prompt user**: Always ask "What would you like to do next?" Don't assume session should end.

---

## Cross-Phase Guidance

### Decision Tree: When to Escalate to User

Use this decision tree throughout all phases:

```
Question or issue arises
│
├─ Can I answer based on existing context?
│  ├─ YES → Proceed autonomously
│  └─ NO → Continue down tree
│
├─ Is this a technical implementation detail?
│  ├─ YES → Use judgment, proceed autonomously
│  └─ NO → Continue down tree
│
├─ Does this affect user-facing behavior or requirements?
│  ├─ YES → Ask user
│  └─ NO → Continue down tree
│
├─ Are there multiple valid approaches?
│  ├─ YES → Present options to user
│  └─ NO → Continue down tree
│
├─ Am I uncertain about the correct approach?
│  ├─ YES → Ask user
│  └─ NO → Proceed autonomously
│
└─ Default: When in doubt, ask user
```

### Tool Selection Matrix

| Task | Best Tool | Alternative | When to Use Alternative |
|------|-----------|-------------|-------------------------|
| Find files by name | `Glob` | `Bash(ls)` | Need file metadata (dates, sizes) |
| Search code content | `Grep` | `Bash(grep)` | Never (always use Grep tool) |
| Read specific file | `Read` | - | Always for reading files |
| Deploy sub-agent | `Task` | - | Always for sub-agents |
| Run validation | `Bash` | - | Always for commands (tests, lint, etc.) |
| Explore codebase | `Task(Explore)` | `Grep` + `Read` | Small scope: manual; Large scope: agent |

### Common Anti-Patterns to Avoid

**Anti-pattern 1: Over-orchestration**
```
Bad: Deploy 10 agents for simple task
Good: Deploy 3-5 agents for complex tasks, fewer for simple tasks
Rule: If task can be done in <30 min without orchestration, don't orchestrate
```

**Anti-pattern 2: Under-specification**
```
Bad: "Agent A: Fix bugs"
Good: "Agent A (systematic-debugger): Debug failing test in lib/search.test.ts
       (test 'handles empty query'). Root cause analysis, fix, verify."
Rule: Every agent scope should be 1-2 specific sentences
```

**Anti-pattern 3: Assuming success**
```
Bad: Agent completes → Move to next phase (no validation)
Good: Agent completes → Verify deliverables → Check quality → Then proceed
Rule: Always validate before proceeding to next phase
```

**Anti-pattern 4: Context bloat**
```
Bad: Pass entire conversation history to each agent
Good: Pass only specific handoff information (file paths, summaries)
Rule: Minimal context principle - only what's needed for agent's specific task
```

**Anti-pattern 5: Silent failures**
```
Bad: Agent fails → Proceed anyway, report success
Good: Agent fails → Analyze → Retry or adjust → Report actual status
Rule: Never hide failures, always address them explicitly
```

---

**This playbook provides comprehensive phase guidance. For coordination patterns, see `references/agent-coordination.md`. For error handling, see `references/error-scenarios.md`.**
