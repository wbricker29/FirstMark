# Claude Code Integration Overview

## Table of Contents

- [Purpose \& When to Use](#purpose--when-to-use)
- [When to Use Claude Code Features](#when-to-use-claude-code-features)
- [System Architecture](#system-architecture)
- [Skill Types](#skill-types)
- [Migration Guide](#migration-guide)

---

## Purpose & When to Use

Use this guide when:
- Deciding whether to create a general or Claude Code skill
- Understanding Claude Code's auto-activation system
- Planning to add automation features to skills
- Migrating from general skills to Claude Code skills

**Previous step**: [Design Phase](DESIGN_PHASE.md) - Understanding use cases

---

## When to Use Claude Code Features

### Use General Skills When:

- ✅ Skill needs to work across all Claude environments (Desktop, CLI, API)
- ✅ Manual invocation is acceptable
- ✅ Simpler setup and maintenance preferred
- ✅ No need for automatic activation

**Examples**:
- PDF processing workflows
- Data analysis procedures
- API integration guides
- General documentation assistance

### Use Claude Code Skills When:

- ✅ Need automatic activation based on context (keywords, file paths, content)
- ✅ Enforcing critical practices (guardrails that block edits)
- ✅ Proactive suggestions for specific technologies or frameworks
- ✅ Session tracking (don't nag repeatedly in same session)
- ✅ Complex trigger patterns (intent detection, content analysis)

**Examples**:
- Database schema verification (blocks edits until verified)
- Error handling enforcement (suggests Sentry integration)
- Framework-specific guides (auto-activates for React + TypeScript)
- Technology-specific best practices (triggers on Prisma queries)

### Decision Matrix

| Feature | General | Claude Code |
|---------|---------|-------------|
| Works everywhere | ✅ | ❌ (Claude Code only) |
| Auto-triggers | ❌ | ✅ |
| Can block edits (guardrails) | ❌ | ✅ |
| Session tracking | ❌ | ✅ |
| Setup complexity | Low | Medium |
| Maintenance | Easy | Moderate |
| Testing tools | Basic | Advanced |

**Recommendation**: Start with general skills. Add Claude Code features only when automation or enforcement is needed.

---

## System Architecture & Hooks

Claude Code skills use a **two-hook architecture** for auto-activation, backed by multiple hook types and trigger patterns. Start with this section for a complete picture; no separate hooks reference is needed.

### Core Claude Code Capabilities

Before wiring hooks, make sure you understand the native capabilities Claude Code exposes:

- **Agentic subagents**: Specialized workers (planner, tester, debugger, docs-manager, ui-ux-designer, database-admin, etc.) that Claude orchestrates automatically for planning, implementation, diagnostics, and documentation.
- **Agent Skills**: Modular knowledge bundles (like this skill) that Claude loads contextually. They live in `.claude/skills/<skill-name>/` alongside references and scripts.
- **Slash Commands**: Short aliases stored in `.claude/commands/` that expand into prompts (e.g., `/cook`, `/fix:fast`, `/docs:init`, `/git:pr`). Each command can accept arguments and trigger relevant subagents.
- **Hooks**: Shell entry points (UserPromptSubmit, PreToolUse/PostToolUse, etc.) that intercept requests to suggest or enforce skills before/after edits.
- **MCP Servers**: Model Context Protocol integrations that expose remote tools/resources (databases, ticketing systems) for Claude Code sessions.

Together these capabilities let Claude plan work, run commands/tests, and enforce guardrails without referencing external skills—everything resides in the `.claude` directory next to your repositories.

### Hook Mechanisms

#### UserPromptSubmit Hook (Proactive Suggestions)

**File**: `.claude/hooks/skill-activation-prompt.ts`

**Trigger**: BEFORE Claude sees user's prompt

**Purpose**: Suggest relevant skills based on keywords + intent patterns

**Method**: Injects formatted reminder as context (stdout → Claude's input)

**Use Cases**:
- Topic-based skills (e.g., "error tracking")
- Implicit work detection (e.g., "create" + "API")
- Technology mentions (e.g., "Prisma", "React")

**Example**:
```
User types: "Add Sentry error tracking"
↓
Hook detects keywords: "sentry", "error", "tracking"
↓
Injects reminder: "Consider using the error-tracking skill"
↓
Claude sees reminder + user prompt
```

---

#### PreToolUse Hook (Guardrails)

**File**: `.claude/hooks/skill-verification-guard.ts`

**Purpose**: BLOCK file edits until critical skill is used (enforcement)

**How it works**:
1. Claude calls Edit or Write tool
2. Hook executes and reads tool details from stdin (JSON)
3. Hook loads skill-rules.json
4. Hook checks file path patterns (glob matching)
5. Hook reads file content for content patterns (if file exists)
6. Hook checks session state (was skill already used?)
7. Hook checks skip conditions (file markers, env vars)
8. If matched and not skipped:
   - Update session state
   - Output block message to stderr
   - Exit with code 2 (BLOCK)
9. If not matched or skipped:
   - Exit with code 0 (ALLOW)

**Exit codes**:
- **0**: Allow tool execution
- **2**: Block tool execution + send message to Claude (stderr)

**Use cases**:
- Critical guardrails (database verification, security checks)
- File-based activation (editing specific files)
- Content-based activation (code uses specific libraries)

#### Stop Hook (Gentle Reminders)

**File**: `.claude/hooks/error-handling-reminder.ts`

**Trigger**: AFTER Claude finishes responding

**Purpose**: Gentle reminder to self-assess code quality (error handling, best practices)

**Method**: Analyzes edited files for risky patterns, displays reminder if needed

**Use Cases**:
- Error handling awareness
- Code quality reminders
- Non-blocking best practice suggestions

**Philosophy** (2025-10-27): Gentle post-response reminders instead of blocking PreToolUse hooks. Maintains awareness without workflow friction.

---

### Trigger Types

Triggers determine WHEN skills activate. Claude Code supports four trigger types:

#### 1. Keyword Triggers (Explicit)
- **How it works**: Case-insensitive substring matching in user's prompt
- **Use for**: Topic-based activation where user explicitly mentions the subject
- **Config**:
  ```json
  "promptTriggers": {
    "keywords": ["layout", "grid", "toolbar", "submission"]
  }
  ```

#### 2. Intent Pattern Triggers (Implicit)
- **How it works**: Regex pattern matching to detect intent
- **Use for**: Action-based activation (“create API”, “implement error handling”)
- **Tips**: Anchor verbs (`(create|build|implement)`), include context nouns.

#### 3. File Path Triggers (Guardrails)
- **How it works**: Glob patterns that match tool inputs (`**/*.tsx`)
- **Use for**: Framework-specific guardrails (React, Prisma)
- **Config**:
  ```json
  "fileTriggers": {
    "pathPatterns": ["frontend/src/**/*.tsx"],
    "pathExclusions": ["**/*.test.tsx"],
    "createOnly": false
  }
  ```

#### 4. Content Pattern Triggers (Deep Inspection)
- **How it works**: Regex applied to file contents before edit (requires existing file)
- **Use for**: Detecting dangerous imports, API usage, schema references.

Best practice: combine trigger types (keyword + intent + file path) to minimize false positives and avoid blocking legitimate work.

### Configuration File

**Location**: `.claude/skills/skill-rules.json`

**Defines**:
- All skills and their trigger conditions
- Enforcement levels (block, suggest, warn)
- File path patterns (glob)
- Content detection patterns (regex)
- Skip conditions (session tracking, file markers, env vars)

See [Skill Rules Config](SKILL_RULES_CONFIG.md) for complete schema.

---

## Skill Types

Claude Code supports two skill patterns:

### 1. Guardrail Skills

**Purpose**: Enforce critical best practices that prevent errors

**Characteristics**:
- Type: `"guardrail"`
- Enforcement: `"block"`
- Priority: `"critical"` or `"high"`
- Blocks file edits until skill used
- Prevents common mistakes (column names, critical errors)
- Session-aware (don't repeat nag in same session)

**Examples**:
- `database-verification` - Verify table/column names before Prisma queries
- `frontend-dev-guidelines` - Enforce React/TypeScript patterns

**When to Use**:
- Mistakes that cause runtime errors
- Data integrity concerns
- Critical compatibility issues
- Security vulnerabilities

**Warning**: Use sparingly! Blocking is disruptive. Only for critical issues.

---

### 2. Domain Skills

**Purpose**: Provide comprehensive guidance for specific areas

**Characteristics**:
- Type: `"domain"`
- Enforcement: `"suggest"`
- Priority: `"high"` or `"medium"`
- Advisory, not mandatory
- Topic or domain-specific
- Comprehensive documentation

**Examples**:
- `backend-dev-guidelines` - Node.js/Express/TypeScript patterns
- `frontend-dev-guidelines` - React/TypeScript best practices
- `error-tracking` - Sentry integration guidance

**When to Use**:
- Complex systems requiring deep knowledge
- Best practices documentation
- Architectural patterns
- How-to guides

**Recommendation**: Most skills should be domain skills with `"suggest"` enforcement.

---

## Migration Guide

### Migrating General Skill to Claude Code

Follow these steps to add Claude Code features to an existing general skill:

#### Migration Step 1: Add skill-rules.json Entry

Create or update `.claude/skills/skill-rules.json`:

```json
{
  "my-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?something"]
    }
  }
}
```

#### Migration Step 2: Update SKILL.md Description

Add trigger keywords to YAML frontmatter description:

**Before**:
```yaml
description: Guide for processing PDF files
```

**After**:
```yaml
description: Guide for processing PDF files. Use when working with PDFs, extracting text, parsing documents, or converting file formats.
```

Include specific keywords that should trigger the skill.

#### Migration Step 3: Test Triggers

Test that the skill activates correctly:

```bash
# Test UserPromptSubmit hook
echo '{"session_id":"test","prompt":"help me process a PDF"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

Expected output should mention your skill.

#### Migration Step 4: Add File or Content Triggers (Optional)

For file-based activation, add to skill-rules.json:

```json
{
  "my-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["pdf", "document"],
      "intentPatterns": ["(process|parse|extract).*?(pdf|document)"]
    },
    "fileTriggers": {
      "paths": ["**/*.pdf", "**/documents/**"]
    },
    "contentTriggers": {
      "patterns": ["import.*?pdf", "PdfDocument"]
    }
  }
}
```

#### Migration Step 5: Configure Skip Conditions (Optional)

Add session tracking to prevent repeated nagging:

```json
{
  "my-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": { ... },
    "skipConditions": {
      "sessionTracking": {
        "enabled": true,
        "skipAfterFirstUse": true
      }
    }
  }
}
```

#### Migration Step 6: Validate and Test

Run validation:
```bash
uv run python scripts/quick_validate.py path/to/my-skill
```

Test activation with various prompts and file paths.

---

### Migration Checklist

- [ ] skill-rules.json entry created with trigger conditions
- [ ] SKILL.md description updated with trigger keywords
- [ ] Trigger type selected (keywords, intent, file paths, content)
- [ ] Enforcement level chosen (suggest recommended)
- [ ] Priority set (high/medium/low)
- [ ] Skip conditions configured (session tracking)
- [ ] Tested with real prompts
- [ ] Tested with file paths (if applicable)
- [ ] Validated with quick_validate.py
- [ ] No false positives in testing
- [ ] No false negatives in testing

---

## Best Practices

### Do ✅

- Start with general skills, add Claude Code features when needed
- Use `"suggest"` enforcement for most skills
- Test triggers with 3+ real scenarios
- Configure session tracking to prevent nagging
- Include all trigger keywords in description
- Validate configuration with validation script

### Don't ❌

- Don't use `"block"` enforcement unless critical
- Don't create complex intent patterns without testing
- Don't skip validation before deployment
- Don't assume triggers work without testing
- Don't block workflow unnecessarily

---

## Next Steps

**Ready to build Claude Code skills?**

1. **Understand triggers**: See [Trigger Types](#trigger-types) above
2. **Configure skill-rules.json**: [Skill Rules Config](SKILL_RULES_CONFIG.md)
3. **Choose enforcement**: [Enforcement Levels](ENFORCEMENT_LEVELS.md)
4. **Test and debug**: [Testing Claude Code](TESTING_CLAUDE_CODE.md)
5. **Use patterns**: [Patterns Library](PATTERNS_LIBRARY.md)

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) for overview.
