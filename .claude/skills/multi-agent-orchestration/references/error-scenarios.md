# Error Scenarios: Comprehensive Error Catalog

## Overview

This reference provides a comprehensive catalog of errors encountered during multi-agent orchestrations, with structured resolution protocols, prevention strategies, and communication templates.

Each error includes:
- **Error code**: Unique identifier (ORG-001 through ORG-008)
- **Symptoms**: How to detect the error
- **Root causes**: Why the error occurs
- **Resolution protocol**: Step-by-step fix
- **Prevention strategies**: How to avoid
- **User communication template**: What to tell user
- **Escalation criteria**: When to escalate vs retry

Use this reference to quickly diagnose and resolve orchestration issues.

---

## Error Categories

1. **ORG-001**: Missing Project Context
2. **ORG-002**: Ambiguous Requirements
3. **ORG-003**: Sub-Agent Failure
4. **ORG-004**: Context Overflow
5. **ORG-005**: Validation Failure
6. **ORG-006**: Synthesis Conflicts
7. **ORG-007**: Integration Issues
8. **ORG-008**: Performance Issues

---

## ORG-001: Missing Project Context

### Error Code
`ORG-001: Missing Project Context`

### Symptoms

**How to detect:**
- Cannot locate expected documentation files (constitution.md, specs/, etc.)
- Agent asks questions that should be answered by project docs
- Agent produces work that violates project standards (unknown to orchestration)
- References to standards or conventions fail (file not found)
- User mentions "project follows X pattern" but no documentation found

**Example symptoms:**
```
- Error reading specs/constitution.md: File not found
- Agent asks: "What naming conventions should I use?"
- Agent produces camelCase when project uses snake_case
- Cannot validate against quality standards (no standards document)
```

### Root Causes

**Why this occurs:**
1. **New project**: Project doesn't have established documentation yet
2. **Documentation missing**: Expected files deleted or never created
3. **Wrong directory**: Orchestration running in wrong directory
4. **Documentation not standardized**: Docs exist but in non-standard locations
5. **Incomplete setup**: Project partially initialized

**Common scenarios:**
- Fresh repository without constitution/specs
- Developer deleted docs thinking they were unnecessary
- Working in subdirectory instead of project root
- Legacy project without documented standards

### Resolution Protocol

**Step-by-step fix:**

1. **Confirm missing context:**
   ```
   Bash("ls specs/constitution.md") → File not found
   Bash("ls .claude/") → Directory exists
   Bash("pwd") → Verify current directory
   ```

2. **Identify what's missing:**
   ```
   Critical:
   - specs/constitution.md (project principles, quality standards)
   - specs/spec.md (project specification)

   Optional:
   - Project-specific guidelines
   - Architecture documentation
   - Contributing guidelines
   ```

3. **Present options to user:**
   ```
   "Project context missing. Required file not found: specs/constitution.md

   This file should contain project principles, quality standards, and
   development guidelines.

   Options:
   a. Create constitution.md now (recommended, 10-15 minutes)
      - Use /constitution command to create
      - Resume orchestration after creation

   b. Proceed with general best practices
      - Use KISS/YAGNI/Quality principles
      - Note: May not match project-specific standards

   c. User provides standards inline
      - Describe standards in this conversation
      - Use for this orchestration only

   Which option do you prefer?"
   ```

4. **Execute user choice:**

   **If option (a):**
   ```
   Pause current orchestration.
   Run /constitution command.
   Wait for constitution creation.
   Resume orchestration with constitution context.
   ```

   **If option (b):**
   ```
   Document assumption: "Proceeding with general best practices
                         (KISS, YAGNI, quality-first)"
   Continue orchestration with general standards.
   Flag in synthesis report: "Constitution recommended for future work"
   ```

   **If option (c):**
   ```
   Collect standards from user.
   Document in conversation context.
   Use standards for agent briefings.
   Note: Standards not persisted to project.
   ```

5. **Resume orchestration:**
   ```
   With resolved context (constitution or general standards),
   proceed with planning phase using available standards.
   ```

### Prevention Strategies

**How to avoid:**

1. **Pre-flight context check:**
   ```
   Before starting any orchestration, verify:
   ✅ specs/constitution.md exists
   ✅ specs/spec.md exists (if project-specific)
   ✅ .claude/ directory present
   ✅ Running in project root directory

   If any missing → Resolve before planning agents
   ```

2. **Constitution as prerequisite:**
   ```
   For projects without constitution:
   - Suggest creating constitution first
   - Offer to run /constitution command
   - Don't proceed until standards established
   ```

3. **Graceful degradation:**
   ```
   If context missing:
   - Use general principles explicitly
   - Document assumptions clearly
   - Flag for future documentation
   ```

4. **Directory validation:**
   ```
   At orchestration start:
   Bash("git rev-parse --show-toplevel")
   Verify in correct directory before proceeding.
   ```

### User Communication Template

**Initial detection:**
```
⚠️  Missing Project Context

Required documentation not found: specs/constitution.md

This file defines project principles, quality standards, and development
guidelines. Without it, I'll need to make assumptions about project standards.

Options:
1. Create constitution now (/constitution command) - Recommended
2. Proceed with general best practices (KISS, YAGNI, quality-first)
3. Provide standards inline for this session

Which option works best for you?
```

**After resolution:**
```
Context resolved: [Using constitution.md / Using general standards]
Proceeding with orchestration.
```

### Escalation Criteria

**Retry without escalation when:**
- File temporarily missing (can be created)
- Wrong directory (can navigate to correct location)
- File moved (can locate alternate location)

**Escalate to user when:**
- Missing context is critical and cannot be inferred
- User input needed to create context
- Multiple context files missing (systematic issue)
- Unclear what standards to apply

**Abort orchestration when:**
- User declines to provide context
- Context requirements cannot be met
- Project structure fundamentally incompatible

---

## ORG-002: Ambiguous Requirements

### Error Code
`ORG-002: Ambiguous Requirements`

### Symptoms

**How to detect:**
- User request has multiple valid interpretations
- Critical details missing from request (scope, constraints, deliverables)
- Agent asks clarifying questions during execution (should've been answered earlier)
- Agent produces output that doesn't match user intent (mismatch despite correct execution)
- Requirements conflict with each other

**Example symptoms:**
```
User: "Optimize the search feature"
Ambiguities:
  - Which aspect? (Performance, UX, accuracy, code quality)
  - What's the baseline? (Current performance metrics unknown)
  - What's the target? (How much optimization needed)
  - What's acceptable trade-off? (Complexity vs performance)

User: "Make it faster"
Ambiguities:
  - What is "it"? (Specific component, entire app, particular operation)
  - How much faster? (10%, 2x, <100ms?)
  - What's the budget? (Caching OK? Complexity increase acceptable?)
```

### Root Causes

**Why this occurs:**
1. **Vague user request**: High-level request without specifics
2. **Assumed context**: User assumes shared understanding
3. **Missing constraints**: No explicit boundaries or limitations
4. **Implied requirements**: Important details not stated
5. **Multiple valid paths**: Several approaches possible, unclear which to take

**Common scenarios:**
- "Improve X" (improve how?)
- "Fix the bug" (which bug, where?)
- "Refactor the code" (which code, refactor how?)
- "Add feature X" (detailed behavior unclear)

### Resolution Protocol

**Step-by-step fix:**

1. **Identify specific ambiguities:**
   ```
   Parse user request, identify unclear aspects:
   - Scope: What exactly to modify?
   - Constraints: What NOT to change?
   - Deliverables: What should be produced?
   - Success criteria: What makes it "done"?
   - Trade-offs: What's acceptable to sacrifice?
   ```

2. **Categorize ambiguities:**
   ```
   Critical (must resolve before planning):
   - Scope boundaries
   - Success criteria
   - Breaking changes acceptable?

   Important (should resolve before planning):
   - Implementation approach
   - Performance targets
   - Quality standards

   Optional (can infer reasonable defaults):
   - Specific file organization
   - Code style details (use project standards)
   ```

3. **Formulate clarifying questions:**
   ```
   Structure questions as:
   - Specific and focused (one aspect per question)
   - With options if applicable (helps user choose)
   - With context (explain why asking)

   Bad: "What do you want?"
   Good: "When you say 'optimize search', which aspect matters most?
          a. Speed (reduce query time)
          b. Accuracy (improve result relevance)
          c. UX (better filtering/sorting UI)
          d. Code quality (refactor for maintainability)"
   ```

4. **Present questions to user:**
   ```
   Template:
   "To plan the orchestration effectively, I need clarification on:

   1. [Ambiguity 1]: [Question with options if applicable]
      Context: [Why this matters for orchestration]

   2. [Ambiguity 2]: [Question]
      Context: [Why this matters]

   [List 3-5 questions max - don't overwhelm user]

   Once clarified, I can create a detailed orchestration plan."
   ```

5. **Collect user responses:**
   ```
   Wait for user responses.
   Incorporate into requirements understanding.
   Document clarified requirements for agent briefings.
   ```

6. **Verify understanding:**
   ```
   "Based on your responses, here's my understanding:
   - Scope: [Clarified scope]
   - Approach: [Chosen approach]
   - Constraints: [Identified constraints]
   - Success criteria: [How to measure success]

   Is this correct? (y/n)"
   ```

7. **Proceed to planning:**
   ```
   With clarified requirements, proceed to Phase 2 (planning).
   Use clarified requirements in agent briefings.
   ```

### Prevention Strategies

**How to avoid:**

1. **Requirement checklist during analysis:**
   ```
   Before planning, verify all are clear:
   ✅ Scope: Exactly what to modify (files, components, features)
   ✅ Deliverables: What will be produced (files, docs, tests)
   ✅ Constraints: What NOT to change (boundaries)
   ✅ Success criteria: What makes it "done" (measurable)
   ✅ Trade-offs: What's acceptable to sacrifice (if any)
   ✅ Edge cases: Unusual scenarios to handle

   If ANY unclear → Ask clarifying questions before planning
   ```

2. **Proactive questioning:**
   ```
   Don't wait for ambiguity to block progress.
   During Phase 1 (analysis), proactively ask about:
   - Critical design decisions
   - Scope boundaries
   - Quality expectations
   - Integration requirements
   ```

3. **Clarify vague requests immediately:**
   ```
   User: "Optimize the API"

   Immediate response:
   "To optimize effectively, I need to understand:
   1. Which aspect: Response time, throughput, or resource usage?
   2. Current baseline: What are current metrics?
   3. Target: What performance do you want to achieve?
   4. Trade-offs: Is increased complexity acceptable?

   This helps me plan the right optimization approach."
   ```

4. **Provide examples to disambiguate:**
   ```
   "When you say 'improve search', here are some interpretations:

   Example A: Improve performance
     - Optimize database queries
     - Add caching
     - Target: <50ms response time

   Example B: Improve user experience
     - Add filters (price, category)
     - Improve result sorting
     - Add search suggestions

   Example C: Improve result quality
     - Better ranking algorithm
     - Relevance scoring
     - Handle typos/synonyms

   Which example is closest to what you want?"
   ```

### User Communication Template

**Initial detection:**
```
⚠️  Requirements Need Clarification

Your request: "[User's request]"

To create an effective orchestration plan, I need clarification on:

1. [Critical ambiguity 1]: [Question]
   Context: [Why this matters]
   Options: [If applicable]

2. [Critical ambiguity 2]: [Question]
   Context: [Why this matters]

3. [Important ambiguity 3]: [Question]
   Context: [Why this matters]

Once these are clarified, I can design a detailed multi-agent plan.
```

**After clarification:**
```
✅ Requirements Clarified

My understanding:
- Scope: [Clarified scope]
- Deliverables: [What will be produced]
- Success criteria: [How to measure done]
- Constraints: [Boundaries]

Proceeding to create orchestration plan with these requirements.
```

**If user provides partial clarification:**
```
Thanks for clarifying [aspect]. I still need clarification on:
- [Remaining ambiguity]: [Question]

This is needed to ensure the orchestration meets your expectations.
```

### Escalation Criteria

**Retry without escalation when:**
- Minor details unclear (can make reasonable assumptions)
- User provides partial clarification (ask remaining questions)
- Ambiguity can be resolved with examples/options

**Escalate to user when:**
- Critical scope/requirements unclear
- Multiple valid interpretations exist
- User intent is ambiguous
- Assumptions would be risky

**Abort orchestration when:**
- User cannot or will not clarify
- Requirements remain fundamentally unclear
- Multiple escalation attempts unsuccessful

---

## ORG-003: Sub-Agent Failure

### Error Code
`ORG-003: Sub-Agent Failure`

### Symptoms

**How to detect:**
- Agent reports error or exception during execution
- Agent produces no output or incomplete output
- Agent exceeds time estimate significantly (>2x)
- Agent output fails validation
- Agent asks repeated questions (stuck in loop)
- Agent reports "cannot complete task"

**Example symptoms:**
```
Agent A (task-implementor): Error: "Cannot resolve module path"
Agent B (systematic-debugger): Incomplete output (analysis only, no fix)
Agent C (code-prettier): Timeout after 60 minutes (expected 20 minutes)
Agent D (documentation-manager): Output fails lint check
Agent E (Explore): Asks same clarifying question 3 times
```

### Root Causes

**Why this occurs:**

**Category A: Scope Issues**
1. **Scope too large**: Agent overwhelmed by task size
2. **Scope too vague**: Agent doesn't understand what to do
3. **Scope mismatch**: Agent type wrong for task

**Category B: Context Issues**
4. **Missing context**: Agent lacks information needed
5. **Context overflow**: Too much context, exceeds token limits
6. **Wrong context**: Given irrelevant files/information

**Category C: Technical Issues**
7. **Dependency unavailable**: Required file/library missing
8. **Environment issue**: Tool or command not available
9. **Circular dependency**: Agent stuck in loop

**Category D: Quality Issues**
10. **Agent produced poor quality**: Output violates standards
11. **Agent exceeded scope**: Did more than asked
12. **Agent misunderstood instructions**: Wrong interpretation

### Resolution Protocol

**Step-by-step fix:**

1. **Analyze failure:**
   ```
   Identify failure type:
   - Error message? (technical failure)
   - Incomplete output? (scope too large or context issue)
   - Timeout? (task complexity or infinite loop)
   - Poor quality? (instructions unclear or agent limitations)
   - Wrong output? (misunderstood requirements)
   ```

2. **Determine root cause:**
   ```
   Scope issues:
     - Read agent brief → Was scope clear and bounded?
     - Check task complexity → Single agent task or needs split?

   Context issues:
     - Check context files provided → Were they correct?
     - Check token usage → Did agent hit context limits?

   Technical issues:
     - Check error message → What specifically failed?
     - Check dependencies → Are required files present?

   Quality issues:
     - Read agent output → Does it match brief?
     - Check validation results → Which gates failed?
   ```

3. **Choose resolution strategy:**

   **Strategy A: Adjust and retry (same agent type, modified brief)**
   ```
   Use when:
   - Root cause is fixable (scope adjustment, context correction)
   - Agent type is appropriate for task
   - Retry likely to succeed with adjustments

   Actions:
   - Modify agent brief (clarify scope, adjust context)
   - Redeploy same agent type
   - Document retry attempt
   - Set retry limit (max 3 attempts per agent)
   ```

   **Strategy B: Split and redeploy (break into smaller agents)**
   ```
   Use when:
   - Scope too large for single agent
   - Task naturally breaks into sub-tasks
   - Agent timed out due to complexity

   Actions:
   - Split scope into 2-3 smaller agents
   - Define clear boundaries for each
   - Deploy agents sequentially or parallel (based on dependencies)
   ```

   **Strategy C: Change agent type**
   ```
   Use when:
   - Wrong agent type for task
   - Specialized agent needed
   - General-purpose agent insufficient

   Actions:
   - Identify correct agent type
   - Redeploy with appropriate agent type
   - Adjust brief for new agent type
   ```

   **Strategy D: Manual intervention**
   ```
   Use when:
   - Issue is trivial (<5 min fix)
   - Agent repeatedly fails on same issue
   - Manual fix faster than redeploy

   Actions:
   - Fix issue manually
   - Document what was fixed
   - Continue orchestration
   ```

   **Strategy E: Escalate to user**
   ```
   Use when:
   - Multiple retries failed
   - Fundamental issue (design flaw, missing dependency)
   - User decision needed
   - Cannot resolve autonomously

   Actions:
   - Document failure analysis
   - Present options to user
   - Wait for user decision
   ```

4. **Execute resolution:**
   ```
   Implement chosen strategy.
   Document resolution attempt.
   Track retry count (abort after 3 attempts).
   Validate resolution success.
   ```

5. **Update orchestration state:**
   ```
   If resolved:
     - Mark agent as complete
     - Update deliverables
     - Continue orchestration

   If unresolved:
     - Mark agent as failed
     - Document failure
     - Escalate or abort orchestration
   ```

### Prevention Strategies

**How to avoid:**

1. **Scope validation before deployment:**
   ```
   Before deploying agent, verify:
   ✅ Scope is specific and bounded (1-2 sentences)
   ✅ Scope is appropriate for agent type
   ✅ Estimated time is reasonable (15-30 minutes)
   ✅ Context is complete and relevant
   ✅ Dependencies are available

   If any unclear → Adjust before deploying
   ```

2. **Clear agent briefings:**
   ```
   Every agent brief must include:
   ✅ Specific scope (exactly what to do)
   ✅ Context files (what to read, with focus areas)
   ✅ Instructions (specific directives)
   ✅ Expected output (deliverables)
   ✅ Constraints (what NOT to do)
   ✅ Validation criteria (success measures)

   See references/agent-coordination.md for briefing templates.
   ```

3. **Context budget checks:**
   ```
   Before deploying each agent:
   - Estimate token usage (files to read + brief + tools)
   - Run scripts/check_context_bounds.py if available
   - Reduce context if approaching limits
   - Use file excerpts instead of full files if needed
   ```

4. **Right-size agent scopes:**
   ```
   Agent scope should be:
   - Completable in 15-30 minutes
   - Touches 1-5 files (not 20+)
   - Single focused task (not multi-phase)

   If scope larger → Split into multiple agents
   If scope smaller → Combine with other agents
   ```

5. **Pre-deployment validation:**
   ```
   Run pre-flight check:
   - Verify dependencies exist (files, tools)
   - Validate context is accessible
   - Check agent type appropriate for task
   - Estimate token usage within budget

   Only deploy if all checks pass.
   ```

### User Communication Template

**Initial failure:**
```
⚠️  Agent Failure: [Agent ID] ([Agent Type])

Agent: [Agent ID] ([Agent Type])
Scope: [Agent's assigned scope]
Status: FAILED
Error: [Error message or symptom]

Analyzing failure...
```

**After analysis (propose resolution):**
```
Failure Analysis Complete

Root cause: [Identified root cause]
Example: "Agent scope too large - task requires 2 agents instead of 1"

Resolution plan:
Strategy: [Chosen strategy, e.g., "Split into 2 smaller agents"]
Actions:
  - [Action 1]
  - [Action 2]
Expected outcome: [What this will achieve]

Proceeding with resolution? (y/n)
[Or present options if multiple strategies viable]
```

**After successful resolution:**
```
✅ Agent Failure Resolved

Resolution: [What was done]
Result: [Outcome]
Status: Continuing orchestration

[Continue with next phase]
```

**If escalation needed:**
```
❌ Unable to Resolve Agent Failure

Agent: [Agent ID]
Scope: [Scope]
Attempts: [Number of retry attempts]
Last error: [Error message]

I've tried:
- [Resolution attempt 1] → [Result]
- [Resolution attempt 2] → [Result]
- [Resolution attempt 3] → [Result]

Options:
a. Adjust approach: [Describe alternative approach]
b. Simplify scope: [Describe reduced scope]
c. Manual intervention: [What user could do]
d. Abort orchestration: Accept partial completion

Which option would you like to pursue?
```

### Escalation Criteria

**Retry without escalation when:**
- ✅ Root cause identified and fixable
- ✅ Retry likely to succeed (>70% confidence)
- ✅ Retry count < 3 attempts
- ✅ Adjustment is straightforward

**Escalate to user when:**
- ❌ 3 retry attempts exhausted
- ❌ Root cause unclear or unfixable
- ❌ Requires user decision (design choice, priority)
- ❌ Fundamental issue (missing dependency, design flaw)

**Abort orchestration when:**
- ❌ Critical agent fails repeatedly
- ❌ Failure invalidates entire orchestration
- ❌ User requests cancellation
- ❌ No viable resolution path

---

## ORG-004: Context Overflow

### Error Code
`ORG-004: Context Overflow`

### Symptoms

**How to detect:**
- Agent reports "approaching context limit" or "token limit exceeded"
- Agent slows significantly (processing large context)
- Agent output truncated or incomplete
- Token usage >180k (approaching 200k limit)
- Warning from scripts/check_context_bounds.py

**Example symptoms:**
```
Agent A: Warning: "Context usage 185k/200k tokens (92%)"
Agent B: Error: "Cannot load file - context limit exceeded"
Agent C: Response truncated mid-sentence
scripts/check_context_bounds.py: "CRITICAL: 195k tokens used, 5k remaining"
```

### Root Causes

**Why this occurs:**
1. **Too many files loaded**: Agent brief includes many large files
2. **Large file content**: Individual files very large (>10k lines)
3. **Redundant context**: Same information loaded multiple times
4. **Deep conversation history**: Long orchestration with accumulated context
5. **Parallel agents**: Multiple agents deployed simultaneously (context multiplier)

**Common scenarios:**
- Agent asked to read entire codebase
- Multiple agents loading same large files
- Long sequential pipeline with context accumulation
- Large documentation files in every agent brief
- Parallel deployment of 5+ agents

### Resolution Protocol

**Step-by-step fix:**

1. **Assess context usage:**
   ```
   Run context check:
   Bash("python scripts/check_context_bounds.py --phase 3")
   Or manual estimate:
     - Count files in agent briefs
     - Estimate tokens per file (~4 tokens per word)
     - Sum across all active agents
   ```

2. **Identify context sources:**
   ```
   Break down token usage:
   - Agent briefs: [X]k tokens
   - File reads: [Y]k tokens
   - Conversation history: [Z]k tokens
   - Tool outputs: [W]k tokens

   Identify largest contributors.
   ```

3. **Choose reduction strategy:**

   **Strategy A: Reduce file context (most common)**
   ```
   Instead of: "Read entire file"
   Use: "Read lines 50-150 (focus on function X)"

   Instead of: Loading 20 files
   Use: Loading 5 most critical files

   Actions:
   - Identify essential vs optional context
   - Use file excerpts (line ranges)
   - Remove redundant files
   ```

   **Strategy B: Split into smaller agents**
   ```
   Instead of: 1 agent with large scope
   Use: 2-3 agents with focused scopes

   Actions:
   - Split agent scope
   - Each agent reads subset of files
   - Deploy sequentially to avoid parallel context multiplier
   ```

   **Strategy C: Sequential instead of parallel**
   ```
   Instead of: Deploy 5 agents in parallel
   Use: Deploy 2-3 agents at a time (waves)

   Actions:
   - Break parallel wave into sub-waves
   - Deploy agents in groups (2-3 per wave)
   - Reduces peak context usage
   ```

   **Strategy D: Remove optional context**
   ```
   Instead of: Loading reference docs + specs + examples
   Use: Loading only specs (essentials)

   Actions:
   - Distinguish critical vs nice-to-have context
   - Remove nice-to-have context
   - Agent can ask for additional context if needed
   ```

   **Strategy E: Use smaller model**
   ```
   Instead of: Sonnet for all agents
   Use: Haiku for simple agents, Sonnet for complex

   Note: Haiku has same 200k context limit, but this is for
         reducing quality overhead, not context limits directly.

   Actions:
   - Identify agents with simple tasks
   - Deploy with model: "haiku"
   - Reserve Sonnet for complex agents
   ```

4. **Implement reduction:**
   ```
   Apply chosen strategy:
   - Modify agent briefs with reduced context
   - Redeploy affected agents
   - Monitor token usage during execution
   ```

5. **Validate reduction:**
   ```
   After reduction:
   - Check token usage < 150k (safe buffer)
   - Verify agents still have necessary context
   - Confirm agents complete successfully
   ```

6. **Resume orchestration:**
   ```
   With reduced context, continue execution.
   Monitor token usage for remaining agents.
   Apply reduction proactively to prevent recurrence.
   ```

### Prevention Strategies

**How to avoid:**

1. **Pre-flight context budget:**
   ```
   Before starting orchestration:
   - Estimate total token usage (all agents)
   - Run scripts/check_context_bounds.py --phase 1
   - If estimate >150k tokens → Reduce scope or split orchestration
   ```

2. **Minimal context principle:**
   ```
   For every agent brief, ask:
   "Does agent NEED this file or is it nice-to-have?"

   Include:
   ✅ Files agent will modify
   ✅ Critical reference files
   ✅ Direct dependencies

   Exclude:
   ❌ Entire codebase "for context"
   ❌ Tangentially related files
   ❌ Files agent won't use
   ```

3. **Use file excerpts:**
   ```
   Instead of: "Read lib/large-file.ts"
   Use: "Read lib/large-file.ts (lines 100-250, focus on function processData)"

   This:
   - Reduces tokens significantly
   - Focuses agent attention
   - Prevents context bloat
   ```

4. **Limit parallel agents:**
   ```
   Parallel agents multiply context usage:
   - 1 agent with 40k context = 40k total
   - 5 agents with 40k each = 200k total

   Guidelines:
   - Max 3-4 agents in parallel
   - If more needed, use waves (deploy in groups)
   - Monitor context usage between waves
   ```

5. **Progressive context loading:**
   ```
   Start with minimal context:
   - Core files only
   - If agent needs more, provide incrementally
   - Don't front-load all possible context

   Pattern:
   Deploy agent → Agent asks for X → Provide X → Agent continues
   (vs: Provide everything upfront → Agent overwhelmed)
   ```

6. **Regular context checks:**
   ```
   During orchestration:
   - Check token usage after each agent deployment
   - Run scripts/check_context_bounds.py between phases
   - Alert if approaching 150k (warning threshold)
   - Adjust remaining agents if needed
   ```

### User Communication Template

**Warning (approaching limit):**
```
⚠️  Context Budget Warning

Current usage: [X]k / 200k tokens ([Y]%)
Threshold: 150k tokens (safe operating limit)

Status: APPROACHING LIMIT

Impact:
- [N] agents remaining
- Estimated additional usage: [Z]k tokens
- Projected total: [X+Z]k tokens

Action needed to stay within budget.

Reduction options:
a. Reduce context per agent (load fewer files)
b. Split remaining agents into smaller scopes
c. Deploy remaining agents sequentially (not parallel)

Recommendation: [Recommended option with rationale]

Proceed with reduction? (y/n)
```

**Critical (exceeded limit):**
```
❌ Context Limit Exceeded

Agent [ID] failed: Context overflow
Usage: [X]k / 200k tokens ([Y]%)

Agent was unable to complete due to context limit.

Reduction required. Options:

1. Reduce agent context (recommended):
   - Load only essential files
   - Use file excerpts instead of full files
   - Estimated reduction: [Z]k tokens

2. Split agent scope:
   - Break into 2 smaller agents
   - Each agent handles subset of work
   - Deploy sequentially

3. Adjust orchestration:
   - Complete current agents
   - Defer remaining work to new orchestration
   - Start fresh with reduced context

Which option do you prefer?
```

**After resolution:**
```
✅ Context Overflow Resolved

Action taken: [Reduction strategy]
Result: Usage reduced from [X]k → [Y]k tokens ([Z]% reduction)
Status: Within safe limits

Continuing orchestration with reduced context.
```

### Escalation Criteria

**Retry without escalation when:**
- ✅ Context reduction straightforward (remove files, use excerpts)
- ✅ Agent scope can be split easily
- ✅ Alternative deployment strategy available (sequential vs parallel)

**Escalate to user when:**
- ❌ Reduction requires scope changes (affects deliverables)
- ❌ Multiple reduction strategies needed (user should choose)
- ❌ Context overflow persists after reduction attempts

**Abort orchestration when:**
- ❌ Cannot reduce context sufficiently
- ❌ Scope too large for available context budget
- ❌ Need to redesign entire orchestration

---

## ORG-005: Validation Failure

### Error Code
`ORG-005: Validation Failure`

### Symptoms

**How to detect:**
- Tests fail after agent completes work
- Linting errors in agent output
- Type checking fails
- Format check fails
- Coverage below target
- Build fails
- Custom validation fails (performance benchmarks, integration tests)

**Example symptoms:**
```
Bash("pnpm test") → 5 tests failing
Bash("pnpm lint") → 12 linting errors
Bash("pnpm type-check") → 3 type errors
Bash("pnpm test:coverage") → Coverage 65% (target 80%)
Bash("pnpm build") → Build failed with compilation errors
```

### Root Causes

**Why this occurs:**

**Category A: Agent Quality Issues**
1. **Agent didn't run validation**: Agent completed without testing
2. **Agent introduced bugs**: Implementation incorrect
3. **Agent broke existing code**: Unintended side effects

**Category B: Incomplete Work**
4. **Tests not updated**: Code changed but tests not adjusted
5. **Missing tests**: New code lacks test coverage
6. **Incomplete implementation**: Partial work that doesn't function

**Category C: Standard Violations**
7. **Style violations**: Doesn't follow project conventions
8. **Type errors**: TypeScript errors, missing types
9. **Lint violations**: Code quality issues

**Category D: Integration Issues**
10. **Breaking changes**: Changes broke dependent code
11. **Missing dependencies**: Required imports or packages missing

### Resolution Protocol

**Step-by-step fix:**

1. **Identify validation failures:**
   ```
   Run all validation gates:
   Bash("pnpm format:check") → Check formatting
   Bash("pnpm lint") → Check linting
   Bash("pnpm type-check") → Check types
   Bash("pnpm test") → Check tests
   Bash("pnpm build") → Check build (if applicable)

   Document which gates failed and specific errors.
   ```

2. **Analyze failure severity:**
   ```
   Trivial (quick fixes):
   - Formatting issues (auto-fixable)
   - Minor lint issues (missing semicolon, etc.)
   - Simple type errors (missing type annotation)

   Moderate (requires thought):
   - Test failures due to signature changes
   - Lint violations requiring refactoring
   - Type errors requiring design changes

   Severe (fundamental issues):
   - Multiple test failures indicating logic bugs
   - Build failures indicating broken code
   - Integration failures indicating breaking changes
   ```

3. **Choose resolution strategy:**

   **Strategy A: Auto-fix (for trivial issues)**
   ```
   Use when:
   - Formatting issues
   - Auto-fixable lint issues

   Actions:
   Bash("pnpm format") → Auto-fix formatting
   Bash("pnpm lint:fix") → Auto-fix linting
   Re-run validation to confirm fixes
   ```

   **Strategy B: Manual fix (for moderate issues)**
   ```
   Use when:
   - Quick fixes (<5 minutes)
   - Clear fix path
   - High confidence in solution

   Actions:
   - Identify specific issues (read error messages)
   - Make surgical fixes (Edit tool)
   - Re-run validation to confirm
   - Document fixes made
   ```

   **Strategy C: Redeploy agent (for severe issues)**
   ```
   Use when:
   - Multiple related failures
   - Systematic issues (agent misunderstood requirements)
   - Fixes require design thought
   - Low confidence in manual fix

   Actions:
   - Analyze what agent did wrong
   - Adjust agent brief (clarify requirements)
   - Redeploy agent with validation emphasis:
     "CRITICAL: Run tests before reporting completion.
      All tests must pass. Fix any failures before completing."
   ```

   **Strategy D: Deploy corrective agent (for complex issues)**
   ```
   Use when:
   - Validation failures require new agent expertise
   - Original agent completed but quality issues remain
   - Systematic corrections needed

   Actions:
   - Deploy specialized agent (e.g., systematic-debugger for test failures)
   - Focus agent on fixing specific validation issues
   - Re-validate after correction
   ```

4. **Implement resolution:**
   ```
   Execute chosen strategy.
   Document fixes made.
   Track resolution attempts (abort after 3 attempts).
   ```

5. **Re-validate:**
   ```
   After fix, run all validation gates again:
   Bash("pnpm format:check && pnpm lint && pnpm type-check && pnpm test")

   Verify:
   ✅ All gates pass
   ✅ No new issues introduced
   ✅ Coverage meets target

   If still failing → Retry with different strategy
   If passing → Continue orchestration
   ```

6. **Document resolution:**
   ```
   Note in synthesis report:
   "Agent [ID] output required validation fixes:
    - [Issue 1]: [How fixed]
    - [Issue 2]: [How fixed]
    All validation gates now pass."
   ```

### Prevention Strategies

**How to avoid:**

1. **Validate validation in agent briefs:**
   ```
   Every agent brief should include:

   "Before reporting completion:
    ✅ Run pnpm format
    ✅ Run pnpm lint
    ✅ Run pnpm type-check
    ✅ Run pnpm test [relevant scope]
    ✅ Verify all pass

    If any fail, fix issues before completing.
    Do NOT report completion with failing validation."
   ```

2. **Set clear quality standards:**
   ```
   In agent briefs, specify:
   - Code must be formatted per project style
   - Linting must pass with zero errors
   - Type checking must pass (no `any` escapes)
   - All tests must pass
   - Coverage must be ≥80% on modified code
   - No placeholder comments (TODO, FIXME)
   ```

3. **Emphasize testing:**
   ```
   For code-producing agents:
   "CRITICAL: Write tests for all new functionality.
    Update existing tests if behavior changes.
    Ensure all tests pass before completion.
    Target coverage: 80%+ on modified code."
   ```

4. **Validation as acceptance criteria:**
   ```
   In orchestration planning phase:
   "Validation gates (all must pass):
    - format|lint|types|tests|coverage(80%)

    Agents must self-validate before reporting completion.
    Orchestration validation will verify gates again."
   ```

5. **Use validation-focused agents:**
   ```
   If quality issues persist:
   - Add principle-evaluator agent (validates KISS/YAGNI/Quality)
   - Add systematic-debugger agent (fixes test failures)
   - Deploy after implementation agents to catch issues
   ```

### User Communication Template

**Validation failure detected:**
```
⚠️  Validation Failure

Agent [ID] completed but validation failed.

Failed gates:
❌ [Gate 1]: [Error summary]
❌ [Gate 2]: [Error summary]

Details:
[Specific error messages]

Analyzing failures...
```

**After analysis (propose resolution):**
```
Failure Analysis Complete

Severity: [Trivial / Moderate / Severe]
Root cause: [Identified cause]

Resolution plan:
Strategy: [Auto-fix / Manual fix / Redeploy agent]
Actions:
  - [Action 1]
  - [Action 2]
Estimated time: [Time estimate]

Proceeding with fix.
```

**After successful resolution:**
```
✅ Validation Failures Resolved

Fixed:
- [Gate 1]: [How fixed]
- [Gate 2]: [How fixed]

All validation gates now pass:
✅ Format: PASS
✅ Lint: PASS
✅ Types: PASS
✅ Tests: PASS ([N] tests, 0 failures)
✅ Coverage: [X]% (target: [Y]%)

Continuing orchestration.
```

**If resolution fails:**
```
❌ Unable to Resolve Validation Failures

Attempted:
- [Strategy 1] → [Result]
- [Strategy 2] → [Result]

Remaining failures:
- [Failure 1]: [Description]
- [Failure 2]: [Description]

This requires deeper investigation. Options:
a. Deploy systematic-debugger agent to investigate
b. Manual review and fix (requires your expertise)
c. Revert agent work and try different approach

Which option do you prefer?
```

### Escalation Criteria

**Retry without escalation when:**
- ✅ Trivial fixes (auto-fixable)
- ✅ Clear fix path (<5 min manual fix)
- ✅ Moderate issues with known solution

**Escalate to user when:**
- ❌ Severe failures persisting after 2 fix attempts
- ❌ Unclear how to fix (requires design decision)
- ❌ Fixes introduce new failures (whack-a-mole)
- ❌ Fundamental implementation issues

**Abort orchestration when:**
- ❌ Validation failures indicate agent produced unusable work
- ❌ Multiple agents failing validation systematically
- ❌ Cannot meet quality standards within reasonable effort

---

## ORG-006: Synthesis Conflicts

### Error Code
`ORG-006: Synthesis Conflicts`

### Symptoms

**How to detect:**
- Multiple agents modified same file in conflicting ways
- Duplicate type definitions from different agents
- Conflicting imports or exports
- Inconsistent patterns across agent outputs
- Merge conflicts when combining outputs
- Integration failures after combining agent work

**Example symptoms:**
```
Agent A: Created interface User { id: string; name: string; }
Agent B: Created interface User { id: number; email: string; }
→ Conflict: Duplicate type names, incompatible definitions

Agent C: Modified lib/config.ts (lines 20-30)
Agent D: Modified lib/config.ts (lines 25-40)
→ Conflict: Overlapping modifications

Agent E: Used pattern X (async/await)
Agent F: Used pattern Y (promises/then)
→ Conflict: Inconsistent patterns for similar operations
```

### Root Causes

**Why this occurs:**
1. **Failed independence validation**: Parallel agents not actually independent
2. **Insufficient coordination**: Agents lacked clear boundaries
3. **Overlapping scopes**: Agent scopes not properly delineated
4. **Shared resources**: Multiple agents modifying shared files/types
5. **Missing integration planning**: Didn't anticipate integration issues

**Common scenarios:**
- Parallel agents both updating shared configuration
- Multiple agents creating types with same names
- Agents using different coding patterns for similar tasks
- Agents not aware of each other's changes

### Resolution Protocol

**Step-by-step fix:**

1. **Detect conflicts:**
   ```
   After parallel agents complete:
   - Check for duplicate files/types (Grep for exports)
   - Check for overlapping modifications (read modified files)
   - Check for inconsistent patterns (manual review)
   - Check for integration failures (run tests)
   ```

2. **Categorize conflicts:**
   ```
   Type A: File-level conflicts (same file modified by multiple agents)
   Type B: Type-level conflicts (duplicate type names)
   Type C: Import-level conflicts (circular or conflicting imports)
   Type D: Pattern-level conflicts (inconsistent approaches)
   Type E: Logic-level conflicts (incompatible implementations)
   ```

3. **Assess conflict severity:**
   ```
   Trivial (easy to merge):
   - Non-overlapping sections of same file
   - Different keys in same config object
   - Independent functions in same module

   Moderate (requires thought):
   - Overlapping lines with compatible changes
   - Duplicate types with similar structure
   - Different patterns that can coexist

   Severe (requires redesign):
   - Incompatible type definitions
   - Conflicting logic in same function
   - Mutually exclusive implementations
   ```

4. **Choose resolution strategy:**

   **Strategy A: Manual merge (for trivial conflicts)**
   ```
   Use when:
   - Changes are compatible
   - Clear how to combine
   - Low risk of errors

   Actions:
   - Read both versions
   - Manually merge into single coherent version
   - Validate merged version (tests pass)
   - Document merge decisions
   ```

   **Strategy B: Deploy resolution agent (for moderate conflicts)**
   ```
   Use when:
   - Multiple conflicts to resolve
   - Requires technical judgment
   - Want automated resolution

   Actions:
   - Deploy task-implementor agent
   - Scope: "Resolve conflicts between Agent A and Agent B outputs"
   - Context: Both versions of conflicting files
   - Instructions: Specific merge requirements
   - Validate: Merged version meets both agents' goals
   ```

   **Strategy C: Prioritize one agent (when incompatible)**
   ```
   Use when:
   - Implementations are mutually exclusive
   - One approach clearly better
   - User indicates preference

   Actions:
   - Choose agent's approach to keep
   - Discard or adapt conflicting agent's work
   - Document decision rationale
   - Ensure chosen approach meets requirements
   ```

   **Strategy D: Redesign and redeploy (for severe conflicts)**
   ```
   Use when:
   - Conflicts indicate fundamental design issue
   - Resolution would be hacky/brittle
   - Better to start over with clearer boundaries

   Actions:
   - Revert conflicting agents' work
   - Redesign with clearer separation of concerns
   - Redeploy agents with adjusted scopes
   - Prevent recurrence of conflicts
   ```

5. **Implement resolution:**
   ```
   Execute chosen strategy.
   Document resolution decisions.
   Validate resolved version (all gates pass).
   ```

6. **Update orchestration state:**
   ```
   Document in synthesis report:
   "Synthesis conflicts detected between Agent [X] and Agent [Y]:
    - Conflict: [Description]
    - Resolution: [How resolved]
    - Validated: [Confirmation tests pass]"
   ```

### Prevention Strategies

**How to avoid:**

1. **Strict independence validation:**
   ```
   Before deploying parallel agents, verify:
   ✅ Each agent modifies DIFFERENT files
   ✅ No shared types/interfaces created by multiple agents
   ✅ No overlapping imports/exports
   ✅ No shared configuration keys modified
   ✅ Integration points are well-defined

   If ANY overlap detected → Use sequential or hybrid strategy
   ```

2. **Pre-define shared interfaces:**
   ```
   If multiple agents need shared types:
   - Define types BEFORE deploying agents
   - Instruct agents: "Import types from X, DO NOT modify"
   - Agents use shared types, don't create conflicting ones
   ```

3. **Clear scope boundaries:**
   ```
   In agent briefs, specify explicitly:
   "Your scope:
    - Modify: lib/feature-a.ts, lib/feature-a.test.ts
    - DO NOT modify: lib/shared-types.ts, lib/config.ts
    - Import from: lib/shared-types.ts (do not create types)

   Clear boundaries prevent scope creep and conflicts."
   ```

4. **File-level ownership:**
   ```
   Assign files to specific agents:
   Agent A: Owns components/A/
   Agent B: Owns components/B/
   Agent C: Owns lib/utils-a.ts
   Agent D: Owns lib/utils-b.ts

   No file assigned to multiple agents.
   Shared files assigned to integration agent (deployed last).
   ```

5. **Integration agent for shared resources:**
   ```
   Pattern:
   Wave 1: Parallel agents (independent scopes)
   Wave 2: Integration agent (handles shared resources)

   Example:
   Agents A, B, C create features (parallel)
   Agent D integrates features into routing/config (sequential after A,B,C)

   Prevents conflicts by centralizing shared modifications.
   ```

6. **Pattern consistency enforcement:**
   ```
   In orchestration planning:
   - Define coding patterns for agents to follow
   - Include pattern examples in agent briefs
   - Use principle-evaluator agent to check consistency

   Example:
   "All agents must use async/await (not promises/then).
    Example pattern: [code snippet].
    Follow this pattern for consistency."
   ```

### User Communication Template

**Conflict detected:**
```
⚠️  Synthesis Conflicts Detected

Agents: [Agent X] and [Agent Y]

Conflicts:
1. [Conflict type]: [Description]
   Agent X: [What X did]
   Agent Y: [What Y did]
   Impact: [Why this is a conflict]

2. [Conflict type]: [Description]
   [Similar structure]

Analyzing conflicts and determining resolution strategy...
```

**After analysis (propose resolution):**
```
Conflict Analysis Complete

Severity: [Trivial / Moderate / Severe]
Conflicts: [Number] total

Resolution plan:
Strategy: [Chosen strategy]
Actions:
  - [Action 1]
  - [Action 2]
Outcome: [Expected result]

Estimated time: [Time estimate]

Proceed with resolution? (y/n)
```

**If user choice needed:**
```
Conflict Resolution: User Decision Required

Conflict: [Description]

Agent A approach:
[Description of A's implementation]
Pros: [Benefits]
Cons: [Drawbacks]

Agent B approach:
[Description of B's implementation]
Pros: [Benefits]
Cons: [Drawbacks]

Options:
a. Keep Agent A approach (discard B's conflicting work)
b. Keep Agent B approach (discard A's conflicting work)
c. Merge both (combine compatible aspects)
d. Redesign (deploy new agent with unified approach)

Which option do you prefer?
```

**After resolution:**
```
✅ Synthesis Conflicts Resolved

Resolution: [Strategy used]
Actions taken:
- [Action 1]
- [Action 2]

Result:
- [Outcome 1]
- [Outcome 2]

Validation: All tests pass, no integration issues.

Continuing orchestration.
```

### Escalation Criteria

**Retry without escalation when:**
- ✅ Trivial conflicts (non-overlapping sections)
- ✅ Clear merge strategy
- ✅ Manual merge is straightforward

**Escalate to user when:**
- ❌ Incompatible implementations (user must choose)
- ❌ Design decision required (architectural choice)
- ❌ Multiple resolution attempts failed

**Abort orchestration when:**
- ❌ Conflicts indicate fundamental design flaw
- ❌ Resolution would produce brittle/hacky code
- ❌ Better to revert and restart with better planning

---

## ORG-007: Integration Issues

### Error Code
`ORG-007: Integration Issues`

### Symptoms

**How to detect:**
- Agent outputs work individually but fail when integrated
- Integration tests fail
- Missing integration code (routing, imports, exports)
- Components don't communicate correctly
- API contracts mismatched
- Incomplete feature end-to-end

**Example symptoms:**
```
Agent A created feature module → ✅ Works in isolation
Agent B created API endpoint → ✅ Works in isolation
Integration: Feature can't call API → ❌ Missing connection

Agent C created UI component → ✅ Renders correctly
Agent D updated routing → ✅ Routes defined
Integration: Component not routed → ❌ Not integrated into app

Tests: Unit tests pass ✅, Integration tests fail ❌
```

### Root Causes

**Why this occurs:**
1. **Missing integration agent**: No agent responsible for connecting pieces
2. **Incomplete planning**: Integration not considered during planning
3. **Agents too isolated**: Each agent worked independently, no communication
4. **Missing glue code**: Connections between components not implemented
5. **Interface mismatches**: Agents made incompatible assumptions

**Common scenarios:**
- Created components but didn't add to routing
- Created API but didn't connect UI to call it
- Created utilities but didn't export from index
- Created features but didn't integrate into main app

### Resolution Protocol

**Step-by-step fix:**

1. **Identify integration gaps:**
   ```
   Review agent deliverables:
   - List all components created
   - Map expected connections between components
   - Check actual connections exist
   - Identify missing integration points
   ```

2. **Categorize integration issues:**
   ```
   Type A: Missing imports/exports
     - Module created but not exported
     - Component created but not imported

   Type B: Missing routing/navigation
     - Page created but no route
     - Component created but not added to navigation

   Type C: Missing API connections
     - Backend endpoint exists, frontend doesn't call it
     - Frontend calls API that doesn't exist

   Type D: Missing configuration
     - Feature implemented but not configured
     - Service created but not registered

   Type E: Interface mismatches
     - Components expect different data shapes
     - Function signatures incompatible
   ```

3. **Choose resolution strategy:**

   **Strategy A: Deploy integration agent (recommended)**
   ```
   Use when:
   - Multiple integration points needed
   - Integration is non-trivial
   - Want comprehensive integration

   Actions:
   - Deploy task-implementor agent
   - Scope: "Integrate components from Agents X, Y, Z"
   - Context: All created components + integration points
   - Instructions:
     - Add routing for new pages
     - Connect UI to API endpoints
     - Export modules from index
     - Update configuration
     - Write integration tests
   - Validate: End-to-end functionality works
   ```

   **Strategy B: Manual integration (for simple cases)**
   ```
   Use when:
   - Few integration points (<5)
   - Integration is straightforward
   - Quick fixes (<10 minutes)

   Actions:
   - Manually add missing imports/exports
   - Manually add routing entries
   - Manually connect API calls
   - Validate integration works
   ```

   **Strategy C: Extend existing agents (if minor gaps)**
   ```
   Use when:
   - Agent almost integrated but missed one step
   - Clear which agent should've done integration
   - Small addition to existing agent scope

   Actions:
   - Redeploy agent with expanded scope
   - Include: "Also integrate into [main app/routing/etc.]"
   - Agent completes original work + integration
   ```

4. **Implement resolution:**
   ```
   Execute chosen strategy.
   Document integration work.
   Validate end-to-end functionality.
   ```

5. **Run integration validation:**
   ```
   After integration:
   - Run integration tests (if available)
   - Manually test end-to-end flows
   - Verify all components connected
   - Check no integration points missed
   ```

6. **Update documentation:**
   ```
   Document integration in synthesis report:
   "Integration work performed:
    - Connected [Component A] to [Component B]
    - Added routing for [Feature X]
    - Configured [Service Y]
    All components now integrated and functional."
   ```

### Prevention Strategies

**How to avoid:**

1. **Plan integration during Phase 2:**
   ```
   During orchestration planning, explicitly identify:
   ✅ Integration agent needed? (yes, if >2 components)
   ✅ Integration points: What needs connecting?
   ✅ Integration scope: Routing, imports, configuration, etc.
   ✅ Integration validation: How to verify it works?

   If integration needed → Include integration agent in plan
   ```

2. **Include integration in agent scopes:**
   ```
   In agent briefs, include integration requirements:

   Agent A (feature implementation):
     Scope: "Implement feature X
            AND integrate into main application:
              - Add route in app/routes.ts
              - Export from lib/index.ts
              - Add to navigation menu"

   Don't assume integration will happen automatically.
   ```

3. **Use integration agent pattern:**
   ```
   Standard pattern for multi-component orchestrations:

   Wave 1: Implementation agents (parallel)
     - Agent A: Component 1
     - Agent B: Component 2
     - Agent C: Component 3

   Wave 2: Integration agent (sequential after Wave 1)
     - Agent D: Integrate A, B, C into main app
       - Routing
       - Navigation
       - Configuration
       - Integration tests

   Explicitly separate implementation from integration.
   ```

4. **Integration checklist in briefs:**
   ```
   For any agent creating user-facing components:

   "Integration checklist (complete before reporting done):
    ✅ Component exported from module
    ✅ Route added (if applicable)
    ✅ Navigation updated (if applicable)
    ✅ Configuration updated (if needed)
    ✅ Integration tested (manually verify works in app)"
   ```

5. **End-to-end validation:**
   ```
   During validation phase (Phase 4):
   - Don't just test units in isolation
   - Test end-to-end flows
   - Verify user-facing functionality works
   - Check all integration points

   If end-to-end fails → Integration issue exists
   ```

### User Communication Template

**Integration issue detected:**
```
⚠️  Integration Issue Detected

Individual components work ✅
Integration incomplete ❌

Gaps identified:
1. [Component X] → [Component Y]: [Missing connection]
2. [Feature A] → [Main app]: [Not integrated]
[List all gaps]

Impact: [How this affects functionality]

Determining resolution strategy...
```

**Propose resolution:**
```
Integration Resolution Plan

Strategy: [Deploy integration agent / Manual integration / Extend agent]

Work needed:
- [Integration point 1]: [What needs to be done]
- [Integration point 2]: [What needs to be done]

Expected outcome: [Description of fully integrated system]
Estimated time: [Time estimate]

Proceed with integration? (y/n)
```

**After resolution:**
```
✅ Integration Complete

Integrated:
- [Component X] → [Component Y]: [How connected]
- [Feature A] → [Main app]: [How integrated]

Validation:
✅ Unit tests: PASS
✅ Integration tests: PASS
✅ End-to-end testing: PASS
✅ Manual verification: Feature works in application

All components now fully integrated and functional.
```

### Escalation Criteria

**Retry without escalation when:**
- ✅ Integration gaps identified and fixable
- ✅ Clear path to resolution
- ✅ Integration agent can handle it

**Escalate to user when:**
- ❌ Integration requirements unclear
- ❌ Design decision needed (how to integrate)
- ❌ Multiple integration attempts failed

**Abort orchestration when:**
- ❌ Components fundamentally incompatible
- ❌ Integration not feasible without redesign
- ❌ Better to restart with integration-aware planning

---

## ORG-008: Performance Issues

### Error Code
`ORG-008: Performance Issues`

### Symptoms

**How to detect:**
- Agent takes much longer than estimated (>2x time)
- Orchestration overall very slow
- Multiple agents timeout
- System unresponsive during orchestration
- Context loading very slow
- Repeated work (agents doing same tasks)

**Example symptoms:**
```
Agent A: Estimated 20 min, took 65 min
Agent B: Estimated 15 min, took 45 min
Total orchestration: Estimated 60 min, took 180 min

Agent C: Timeout after 90 minutes
Agent D: Repeatedly reading same large files
Multiple agents: Each profiling same codebase (redundant work)
```

### Root Causes

**Why this occurs:**
1. **Scope too large**: Individual agents doing too much
2. **Inefficient approach**: Poor task decomposition
3. **Redundant work**: Multiple agents doing same analysis
4. **Context loading**: Reading very large files repeatedly
5. **Insufficient parallelization**: Sequential when could be parallel
6. **Agent exploration**: Agents exploring too broadly

**Common scenarios:**
- Single agent refactoring 50 files (should be split)
- 3 agents each analyzing entire codebase (redundant)
- Sequential pipeline when waves could be parallel
- Each agent reading 100k line file (context loading slow)

### Resolution Protocol

**Step-by-step fix:**

1. **Identify performance bottleneck:**
   ```
   Analyze time spent:
   - Which agents took longest?
   - Which phase took longest?
   - What were agents doing? (reading, analyzing, implementing)
   - Any redundant work observed?
   ```

2. **Categorize performance issue:**
   ```
   Type A: Agent scope too large
     - Single agent doing work that should be split

   Type B: Inefficient sequencing
     - Sequential execution when parallel possible

   Type C: Redundant work
     - Multiple agents repeating same analysis

   Type D: Context loading overhead
     - Large files loaded repeatedly

   Type E: Agent exploration overhead
     - Agents exploring broadly instead of focused work
   ```

3. **Choose optimization strategy:**

   **Strategy A: Split large agents (most common)**
   ```
   Use when:
   - Agent scope too large (>45 minutes)
   - Agent doing multiple distinct tasks
   - Agent overwhelmed by complexity

   Actions:
   - Split scope into 2-3 smaller agents
   - Each agent handles subset of work
   - Deploy in parallel (if independent) or sequential (if dependent)
   - Reduces per-agent time
   ```

   **Strategy B: Parallelize more aggressively**
   ```
   Use when:
   - Sequential execution but tasks are independent
   - Waves could be larger
   - Time savings from parallelization significant

   Actions:
   - Identify independent agents in sequential plan
   - Redeploy in parallel waves
   - Validate independence (no conflicts)
   - Reduces total orchestration time
   ```

   **Strategy C: Eliminate redundant work**
   ```
   Use when:
   - Multiple agents doing same analysis
   - Same files read by many agents
   - Repeated exploration of same code

   Actions:
   - Deploy single analysis agent first
   - Analysis agent produces report
   - Subsequent agents use report (don't re-analyze)
   - Saves time on redundant work
   ```

   **Strategy D: Optimize context loading**
   ```
   Use when:
   - Large files loaded repeatedly
   - Context loading is bottleneck

   Actions:
   - Use file excerpts (line ranges) instead of full files
   - Load shared files once, reference in briefs
   - Reduce number of files per agent
   - Pre-extract relevant sections for agents
   ```

   **Strategy E: Focus agent scopes**
   ```
   Use when:
   - Agents exploring too broadly
   - Agents doing extensive analysis when implementation needed

   Actions:
   - Tighten agent scopes (specific files, specific tasks)
   - Provide focused context (not entire codebase)
   - Emphasize implementation over exploration
   - Use Explore agent first if exploration needed
   ```

4. **Implement optimization:**
   ```
   Apply chosen strategy to remaining agents.
   If already in progress:
     - Learn from slow agents
     - Optimize remaining agents
     - Document for future orchestrations

   If can restart:
     - Abort current orchestration
     - Redesign with optimization
     - Restart with optimized plan
   ```

5. **Monitor performance:**
   ```
   After optimization:
   - Track agent completion times
   - Compare to estimates
   - Adjust future estimates based on actuals
   - Document lessons learned
   ```

### Prevention Strategies

**How to avoid:**

1. **Right-size agent scopes:**
   ```
   During planning, verify:
   ✅ Each agent: 15-30 minute estimate
   ✅ No agent scope spans >5 files
   ✅ No agent doing multiple unrelated tasks

   If larger → Split into multiple agents
   If smaller → Combine with other agents
   ```

2. **Maximize parallelization:**
   ```
   During planning:
   - Identify all independent tasks
   - Group into parallel waves
   - Only sequential when dependencies exist

   Default: Parallel unless proven dependent
   ```

3. **Avoid redundant work:**
   ```
   Pattern:
   If multiple agents need same information:
     Deploy analysis agent first → Produce report
     Other agents use report → No re-analysis

   Example:
     Agent A: Analyze codebase → Report
     Agents B, C, D: Use report → Implement (parallel)
   ```

4. **Optimize context from start:**
   ```
   In agent briefs:
   - Load only essential files
   - Use file excerpts (line ranges)
   - Reference files, don't duplicate content
   - Pre-extract relevant sections

   Template:
   "Context: Read lib/feature.ts (lines 50-120, focus on function X)
    Do NOT read entire file, focus on specified section only."
   ```

5. **Use Explore agent efficiently:**
   ```
   If codebase exploration needed:
   - Deploy single Explore agent first
   - Explore agent produces map/report
   - Implementation agents use map (don't explore themselves)

   Don't: Each agent explores codebase independently
   Do: Single exploration, shared results
   ```

6. **Realistic time estimates:**
   ```
   Estimate agent time realistically:
   - Simple task (read 1 file, simple change): 10-15 min
   - Moderate task (read 3 files, implementation + tests): 20-30 min
   - Complex task (read 5+ files, complex logic): 30-45 min

   If estimate >45 min → Split agent

   Build buffer: Actual time often 1.5-2x estimate
   ```

### User Communication Template

**Performance issue detected:**
```
⚠️  Performance Issue Detected

Agent [ID]: Estimated [X] min, took [Y] min ([Z]% over estimate)

Analyzing performance bottleneck...
```

**After analysis:**
```
Performance Analysis

Issue: [Identified bottleneck]
Root cause: [Why slow]

Impact on remaining orchestration:
- [N] agents remaining
- Current trajectory: [X] hours total
- With optimization: [Y] hours total (saves [Z] hours)

Optimization plan:
Strategy: [Chosen strategy]
Changes:
  - [Change 1]
  - [Change 2]
Expected improvement: [Percentage or time saved]

Apply optimization to remaining agents? (y/n)
```

**If major redesign needed:**
```
⚠️  Orchestration Performance Poor

Current status:
- Progress: [X]% complete
- Time elapsed: [Y] hours
- Estimated remaining: [Z] hours (unacceptable)

Issue: [Performance bottleneck]

Options:
a. Continue with current plan (accept slow performance)
   - Total time: ~[X] hours

b. Optimize remaining agents (reduce redundant work, parallelize more)
   - Total time: ~[Y] hours (saves [Z] hours)

c. Abort and restart with optimized plan (if early enough)
   - Total time: ~[W] hours (but starts over)

Recommendation: [Recommended option with rationale]

Which option do you prefer?
```

**After optimization:**
```
✅ Performance Optimized

Changes applied:
- [Optimization 1]
- [Optimization 2]

Performance improvement:
- Agent [ID]: [X] min → [Y] min ([Z]% faster)
- Estimated total time: [A] hours → [B] hours ([C]% faster)

Continuing orchestration with optimized approach.
```

### Escalation Criteria

**Retry without escalation when:**
- ✅ Optimization strategy clear (split agents, parallelize, etc.)
- ✅ Performance issue isolated (doesn't affect entire orchestration)
- ✅ Optimization can be applied to remaining work

**Escalate to user when:**
- ❌ Major redesign needed (abort and restart decision)
- ❌ Performance unacceptable even with optimization
- ❌ User should choose between speed and scope

**Abort orchestration when:**
- ❌ Performance makes orchestration impractical (>4 hours total)
- ❌ Better to redesign entirely with performance in mind
- ❌ User requests cancellation due to time

---

## Quick Reference: Error Code Lookup

Use this quick reference to jump to specific error documentation:

| Error Code | Error Name | Common Symptoms | Primary Resolution |
|------------|------------|-----------------|-------------------|
| **ORG-001** | Missing Project Context | File not found, unknown standards | Create constitution or use general standards |
| **ORG-002** | Ambiguous Requirements | Multiple interpretations, unclear scope | Ask clarifying questions |
| **ORG-003** | Sub-Agent Failure | Agent error, timeout, poor output | Adjust and retry, split scope, or change agent type |
| **ORG-004** | Context Overflow | Token limit exceeded, truncated output | Reduce context per agent, use file excerpts |
| **ORG-005** | Validation Failure | Tests fail, lint errors, type errors | Auto-fix trivial, manual fix moderate, redeploy for severe |
| **ORG-006** | Synthesis Conflicts | Duplicate types, overlapping changes | Manual merge, resolution agent, or prioritize one |
| **ORG-007** | Integration Issues | Components don't connect, missing glue code | Deploy integration agent |
| **ORG-008** | Performance Issues | Agent too slow, orchestration takes too long | Split agents, parallelize, eliminate redundancy |

---

## Error Pattern Recognition

### Detecting Errors Early

**Phase 1 (Analysis) Warning Signs:**
- Requirements unclear after initial review → **ORG-002 likely**
- Cannot locate expected documentation → **ORG-001 likely**
- Scope estimate >2 hours → **ORG-008 likely** (too large)

**Phase 2 (Planning) Warning Signs:**
- Parallel agents modifying same files → **ORG-006 likely**
- Agent scopes vague or overlapping → **ORG-003 likely**
- Estimated token usage >150k → **ORG-004 likely**
- No integration agent in multi-component plan → **ORG-007 likely**

**Phase 3 (Execution) Warning Signs:**
- Agent running >2x estimate → **ORG-003 or ORG-008**
- Agent asking clarifying questions → **ORG-002** (should've been resolved in Phase 1)
- Context warnings appearing → **ORG-004**

**Phase 4 (Validation) Warning Signs:**
- Tests failing → **ORG-005**
- Type conflicts → **ORG-006**
- End-to-end flows broken → **ORG-007**

### Error Combinations

Some errors occur together:

**ORG-002 + ORG-003**: Ambiguous requirements lead to agent failure
- Resolution: Clarify requirements (ORG-002) before retrying agent (ORG-003)

**ORG-004 + ORG-008**: Context overflow causes performance issues
- Resolution: Reduce context (ORG-004) which often improves performance (ORG-008)

**ORG-006 + ORG-007**: Synthesis conflicts prevent integration
- Resolution: Resolve conflicts (ORG-006) then integrate (ORG-007)

**ORG-003 + ORG-005**: Agent fails, produces output that fails validation
- Resolution: Redeploy agent with validation emphasis (ORG-003), validate output (ORG-005)

---

**For coordination patterns, see `references/agent-coordination.md`. For phase-specific guidance, see `references/phase-playbooks.md`.**
