# Command Execution Framework

## Table of Contents

- [Overview](#overview)
- [Command Template](#command-template)
- [Purpose](#purpose)
- [Prerequisites](#prerequisites)
- [Execution Pattern](#execution-pattern)
- [Error Handling](#error-handling)
- [Reference](#reference)
- [Prompting Patterns](#prompting-patterns)
- [Validation Patterns](#validation-patterns)
- [Error Handling Patterns](#error-handling-patterns)
- [Information Gathering Strategies](#information-gathering-strategies)
- [User Interaction Principles](#user-interaction-principles)
- [Implementation Notes](#implementation-notes)
- [Version History](#version-history)

---

## Overview

This document defines the **execution patterns** that all aidev-workflow commands must follow. It provides reusable templates, prompting patterns, validation patterns, and error handling strategies.

**Audience**: Claude (implementing commands) + Maintainers (updating system)

**Purpose**: Enforce consistency, promote reusability, and ensure all commands are executable and maintainable.

---

## Command Template

All commands in the aidev-workflow system follow this **5-phase execution pattern**:

### Standard Command Structure

```markdown
---
name: command-name
description: Brief Description
---

# /command - Brief Description

One-line purpose statement.

## Purpose
Why this command exists and what problem it solves.

## Prerequisites
What must exist before running this command.

## Execution Pattern

### Phase 1: Validate
Specific checks to run before proceeding.

### Phase 2: Gather
Specific prompts to ask the user:
- Prompt: "Exact question to ask?" → Validate: criteria
- Prompt: "Next question?" → Validate: criteria

### Phase 3: Generate
Specific files to create and their structure.

### Phase 4: Validate
Specific validation checklist:
- ✅ Check 1
- ✅ Check 2
- ✅ Check 3

### Phase 5: Confirm
What to display to the user (summary format).

## Error Handling
Specific failure modes for this command and how to handle them.

## Reference
For framework patterns, detailed context, and examples:
aidev-workflow skill → execution-framework.md, commands-reference.md
```

### Phase Definitions

#### Phase 1: Validate (Prerequisites)

**Purpose**: Verify system state before beginning execution.

**Common Checks**:

- Required files exist (constitution.md, PRD.md, state.json)
- Required directories exist (spec/, .claude/)
- Prerequisites from other commands are met
- User has necessary permissions

**Action on Failure**: Stop execution, explain what's missing, suggest remedy.

#### Phase 2: Gather (Information Collection)

**Purpose**: Collect all required information from the user.

**Principles**:

- Ask specific, clear questions
- Provide examples when helpful
- Offer defaults when appropriate
- Validate each response before proceeding
- Group related questions together

**Action on Invalid Input**: Re-prompt with explanation of validation criteria.

#### Phase 3: Generate (File Creation/Modification)

**Purpose**: Create or modify files based on gathered information.

**Principles**:

- Use Read tool before editing existing files
- Follow established templates and schemas
- Maintain consistent formatting
- Preserve existing content when merging
- Create backups if modifying critical files

**Action on Failure**: Roll back changes, explain error, suggest fix.

#### Phase 4: Validate (Output Verification)

**Purpose**: Verify generated output meets quality standards.

**Common Checks**:

- Files exist at expected paths
- Content follows schema/template
- References are valid (no broken links)
- Formatting is correct
- State tracking is updated

**Action on Failure**: Fix automatically if possible, otherwise report and suggest manual fix.

#### Phase 5: Confirm (User Feedback)

**Purpose**: Provide clear summary of what was accomplished.

**Principles**:

- List files created/modified with absolute paths
- Summarize key changes
- Explain next steps
- Reference related commands
- Be concise but informative

---

## Prompting Patterns

### Pattern: Gather with Validation

**Use Case**: Collect required input with specific validation criteria.

**Structure**:

```markdown
Prompt: "What is the [item]? (must meet: [criteria])"
Validate: [validation logic]
On Invalid: "Invalid input: [reason]. Please provide [criteria]."
```

**Example**:

```markdown
Prompt: "What is the feature name? (lowercase, hyphens, 2-30 chars)"
Validate: matches /^[a-z0-9-]{2,30}$/
On Invalid: "Invalid feature name. Use lowercase letters, numbers, and hyphens only (2-30 characters)."
```

### Pattern: Gather with Default

**Use Case**: Collect optional input with a sensible default value.

**Structure**:

```markdown
Prompt: "What is the [item]? (default: [value])"
Handle: If empty/skip, use default value
Validate: [validation logic]
```

**Example**:

```markdown
Prompt: "What is the priority? (default: Medium)"
Handle: If empty, use "Medium"
Validate: Must be one of: Low, Medium, High, Critical
```

### Pattern: Gather List Items

**Use Case**: Collect multiple items in sequence (tasks, requirements, etc.).

**Structure**:

```markdown
Prompt: "Enter [item] (or 'done' to finish):"
Loop: Continue until user enters 'done'
Validate: Each item meets criteria
Store: Accumulate in list
```

**Example**:

```markdown
Prompt: "Enter requirement (or 'done' to finish):"
Loop: While not 'done'
Validate: Non-empty, reasonable length (<200 chars)
Store: Add to requirements array
```

### Pattern: Gather with Confirmation

**Use Case**: Collect input, then confirm understanding before proceeding.

**Structure**:

```markdown
Gather: Ask question(s)
Summarize: Display collected information
Confirm: "Is this correct? (yes/no)"
On No: Re-gather or allow edits
On Yes: Proceed to generation
```

**Example**:

```markdown
Gather: Feature name, description, priority
Summarize: "Feature: [name], Description: [desc], Priority: [priority]"
Confirm: "Is this correct? (yes/no)"
On No: "What would you like to change?"
On Yes: Proceed to generate spec
```

### Pattern: Gather with Context

**Use Case**: Provide helpful context before asking question.

**Structure**:

```markdown
Context: "Currently: [current state]"
Guidance: "[helpful information]"
Prompt: "[question]"
Validate: [criteria]
```

**Example**:

```markdown
Context: "Current features in PRD: [list]"
Guidance: "New features should build on existing capabilities."
Prompt: "What feature would you like to add?"
Validate: Not duplicate, fits architecture
```

### Pattern: Multi-Part Question

**Use Case**: Break complex input into manageable parts.

**Structure**:

```markdown
Part 1: "First aspect: [question]"
Part 2: "Second aspect: [question]"
Part 3: "Third aspect: [question]"
Synthesize: Combine into structured output
```

**Example**:

```markdown
Part 1: "What is the problem this feature solves?"
Part 2: "Who is the target user?"
Part 3: "What is the expected outcome?"
Synthesize: Create problem statement from three answers
```

### Pattern: Choice Selection

**Use Case**: User selects from predefined options.

**Structure**:

```markdown
Prompt: "Select [choice]:"
Options:
  1. [Option A] - [description]
  2. [Option B] - [description]
  3. [Option C] - [description]
Validate: Number 1-N
Map: Number → option value
```

**Example**:

```markdown
Prompt: "Select priority:"
Options:
  1. Low - Minor improvement
  2. Medium - Standard feature
  3. High - Critical for release
Validate: Must be 1, 2, or 3
Map: 1→Low, 2→Medium, 3→High
```

---

## Validation Patterns

### Pattern: File Exists

**Use Case**: Verify required file exists before proceeding.

**Check**:

```markdown
Use: Read tool on file path
On Success: File exists, continue
On Failure: File missing, halt execution
Error: "[file] not found. Run [prerequisite command] first."
```

### Pattern: Valid Markdown

**Use Case**: Verify generated markdown follows structure.

**Check**:

```markdown
Verify: Front matter present (if required)
Verify: Required headings exist
Verify: No malformed links [text]() or ![](missing)
Verify: Consistent indentation
Verify: No duplicate headings (if prohibited)
```

### Pattern: Reference Exists

**Use Case**: Verify referenced files/sections exist.

**Check**:

```markdown
Parse: Extract all [references](paths) and [[cross-refs]]
For Each: Verify target exists (file or heading)
On Missing: Report broken reference with suggestion
```

### Pattern: Schema Compliance

**Use Case**: Verify content matches expected schema.

**Check**:

```markdown
Verify: Required fields present
Verify: Field types correct (string, number, array, etc.)
Verify: Enum values valid (if applicable)
Verify: Nesting structure correct
Verify: No unexpected fields (if strict)
```

### Pattern: Format Consistency

**Use Case**: Verify content follows formatting conventions.

**Check**:

```markdown
Verify: Headings follow hierarchy (no skipped levels)
Verify: Lists use consistent markers (-, *, 1.)
Verify: Code blocks have language tags
Verify: Task items follow schema: - [ ] | - [x] | - [!]
Verify: Dates in ISO format (YYYY-MM-DD)
```

### Pattern: No Duplication

**Use Case**: Verify content doesn't duplicate existing entries.

**Check**:

```markdown
Read: Existing content
Parse: Extract identifiers (names, IDs, keys)
Compare: New content against existing
On Duplicate: Halt with error or offer merge
```

### Pattern: Valid State Transition

**Use Case**: Verify state change is valid according to workflow.

**Check**:

```markdown
Read: Current state from state.json
Verify: Transition allowed (e.g., planning → in_progress)
Verify: Prerequisites met for new state
On Invalid: Explain valid transitions, suggest correct command
```

---

## Error Handling Patterns

### Pattern: Missing Prerequisites

**Scenario**: User runs command before prerequisites are met.

**Detection**: Phase 1 validation fails.

**Response**:

```markdown
Error: "[Prerequisite] is missing."
Explanation: "[Why prerequisite is needed]"
Remedy: "Run [command] first to create [prerequisite]."
Example: "Example: /constitution to create spec/constitution.md"
```

### Pattern: Invalid User Input

**Scenario**: User provides input that fails validation.

**Detection**: Phase 2 validation fails.

**Response**:

```markdown
Error: "Invalid [input type]: [reason]"
Expected: "[Validation criteria]"
Example: "[Valid example]"
Re-prompt: "Please try again: [question]"
```

**Handling**:

- Explain what's wrong clearly
- Show validation criteria
- Provide example of valid input
- Allow multiple retry attempts (3-5)
- Offer "cancel" option

### Pattern: Template Not Found

**Scenario**: Command cannot find required template or reference file.

**Detection**: Attempt to read template file fails.

**Response**:

```markdown
Error: "Template not found: [path]"
Explanation: "[What template was needed and why]"
Remedy: "Check aidev-workflow skill integrity or contact maintainer."
Fallback: "Attempting to generate without template..."
```

### Pattern: File Write Failure

**Scenario**: Cannot write to file (permissions, disk space, etc.).

**Detection**: Write/Edit tool fails.

**Response**:

```markdown
Error: "Failed to write [file]: [reason]"
Explanation: "[What was being written]"
Remedy: "[Specific fix based on error type]"
Rollback: "No changes were made to existing files."
```

### Pattern: Validation Failure

**Scenario**: Generated output fails Phase 4 validation.

**Detection**: Post-generation validation check fails.

**Response**:

```markdown
Error: "Generated content failed validation: [check]"
Explanation: "[What's wrong and why it matters]"
Auto-Fix: "[If possible] Attempting to fix automatically..."
Manual Fix: "[If not] Please manually correct: [instructions]"
```

---

## Information Gathering Strategies

### Strategy: Progressive Disclosure

Start with essential questions, add detail only as needed.

**Approach**:

1. Ask minimum required questions first
2. Assess complexity of user's needs
3. Ask follow-up questions if clarification needed
4. Don't burden user with unnecessary detail

**Example** (/new command):

- Essential: Feature name, description
- Conditional: Ask about dependencies if feature is complex
- Conditional: Ask about acceptance criteria if user mentions testing

### Strategy: Contextual Defaults

Provide intelligent defaults based on current system state.

**Approach**:

1. Read current state (PRD, state.json, existing specs)
2. Infer sensible defaults from context
3. Offer defaults in prompts
4. Accept empty input as consent to use default

**Example** (/plan command):

- Default priority: "Medium" (most common)
- Default assignee: Current user from git config
- Default milestone: Next unreleased milestone from PRD

### Strategy: Validation-First Gathering

Validate each input immediately before moving to next question.

**Approach**:

1. Ask question
2. Validate response
3. If invalid, explain and re-prompt immediately
4. Only proceed when valid input received
5. Don't accumulate multiple invalid inputs

**Example** (/new command):

- Ask feature name → validate format → proceed
- Ask description → validate length → proceed
- Ask priority → validate enum → proceed

### Strategy: Summarize and Confirm

After gathering information, summarize and confirm understanding.

**Approach**:

1. Collect all required inputs
2. Display summary in structured format
3. Ask explicit confirmation
4. Allow user to correct or proceed
5. Only generate after confirmation

**Example** (/spec command):

- Gather: Problem, solution, success metrics
- Summary: Display all three in readable format
- Confirm: "Proceed with this specification? (yes/no)"
- On yes: Generate spec file

### Strategy: Guided Discovery

Help user think through requirements by asking leading questions.

**Approach**:

1. Ask open-ended question
2. Listen to response
3. Ask clarifying follow-ups based on answer
4. Help user articulate implicit assumptions
5. Synthesize into clear requirement

**Example** (/new command):

- Open: "Describe the feature you'd like to build."
- Follow-up: "Who is the primary user of this feature?"
- Follow-up: "What problem does it solve for them?"
- Synthesize: "So this feature helps [user] achieve [goal] by [mechanism]."

---

## User Interaction Principles

### Principle: Clarity Over Brevity

Be clear and explicit, even if it takes more words.

**Good**:

```
Enter the feature name (lowercase, hyphens, 2-30 characters).
Example: "user-authentication" or "dark-mode-toggle"
```

**Bad**:

```
Feature name? (2-30 chars)
```

### Principle: Actionable Feedback

Always tell the user what to do next, don't just report status.

**Good**:

```
Constitution created successfully at spec/constitution.md.
Next: Run /prd to define your project's feature roadmap.
```

**Bad**:

```
Constitution created.
```

### Principle: Helpful Error Messages

Explain what went wrong AND how to fix it.

**Good**:

```
Error: PRD.md not found at spec/PRD.md.
Fix: Run /prd to create the project requirements document.
```

**Bad**:

```
Error: File not found.
```

### Principle: Respectful Tone

Be professional, helpful, and encouraging.

**Guidelines**:

- Use "please" and "thank you" appropriately
- Avoid condescending language
- Assume user has good reasons for their choices
- Celebrate progress: "Great! Constitution created successfully."
- Be patient with invalid input: "Let's try again..."

### Principle: Progressive Information

Show just enough information at each step.

**Approach**:

- Start with high-level summary
- Offer "more details" if user needs it
- Don't overwhelm with full file contents unless asked
- Use "..." to indicate truncated output
- Provide file paths so user can read full content

### Principle: Consistent Language

Use the same terms throughout all commands.

**Standard Terms**:

- "spec/" (not "specifications folder")
- "PRD" (not "requirements doc")
- "feature" (not "initiative" or "project")
- "task" (not "todo" or "action item")
- "constitution" (not "principles doc")
- "prerequisite" (not "dependency" when referring to commands)

### Principle: Evidence-Based Responses

Show file paths and confirmation of actions taken.

**Good**:

```
Created: spec/features/001-user-auth/spec.md
Created: spec/features/001-user-auth/plan.md
Updated: spec/PRD.md (added feature to Part B)
Updated: .claude/logs/state.json (status: planning)
```

**Bad**:

```
Feature created successfully.
```

---

## Implementation Notes

### For Command Authors

When implementing a command:

1. **Follow the template exactly** - All 5 phases, all required sections
2. **Use patterns from this framework** - Don't invent new patterns
3. **Be specific** - Exact prompts, exact validations, exact file paths
4. **Keep it concise** - Target 70-90 lines per command
5. **Reference the skill** - Point to execution-framework.md and commands-reference.md

### For Framework Maintainers

When updating this framework:

1. **Consider impact** - Changes affect all commands
2. **Update all commands** - If template changes, update all 10 commands
3. **Document rationale** - Explain why patterns exist
4. **Provide examples** - Show good and bad implementations
5. **Maintain consistency** - Ensure patterns don't conflict

### For Skill Users

When using commands:

1. **Trust the process** - Commands follow proven patterns
2. **Provide clear input** - Follow validation criteria
3. **Read error messages** - They contain remediation steps
4. **Follow sequences** - Commands build on each other
5. **Consult reference** - See commands-reference.md for "when/why/examples"

---

## Version History

- **v1.0.0** (2025-10-28): Initial framework defining 5-phase template, prompting patterns, validation patterns, error handling patterns, information gathering strategies, and user interaction principles.
