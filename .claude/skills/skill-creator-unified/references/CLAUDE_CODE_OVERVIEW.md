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

### Use General Skills When

- ✅ Skill needs to work across all Claude environments (Desktop, CLI, API)
- ✅ Manual invocation is acceptable
- ✅ Simpler setup and maintenance preferred
- ✅ No need for automatic activation

**Examples**:

- PDF processing workflows
- Data analysis procedures
- API integration guides
- General documentation assistance

### Use Claude Code Skills When

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

## System Architecture

Claude Code skills use a **two-hook architecture** for auto-activation:

### 1. UserPromptSubmit Hook (Proactive Suggestions)

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

### 2. Stop Hook (Gentle Reminders)

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

#### Step 1: Add skill-rules.json Entry

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

#### Step 2: Update SKILL.md Description

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

#### Step 3: Test Triggers

Test that the skill activates correctly:

```bash
# Test UserPromptSubmit hook
echo '{"session_id":"test","prompt":"help me process a PDF"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

Expected output should mention your skill.

#### Step 4: Add File or Content Triggers (Optional)

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

#### Step 5: Configure Skip Conditions (Optional)

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

#### Step 6: Validate and Test

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

1. **Understand triggers**: [Hooks & Triggers](HOOKS_AND_TRIGGERS.md)
2. **Configure skill-rules.json**: [Skill Rules Config](SKILL_RULES_CONFIG.md)
3. **Choose enforcement**: [Enforcement Levels](ENFORCEMENT_LEVELS.md)
4. **Test and debug**: [Testing Claude Code](TESTING_CLAUDE_CODE.md)
5. **Use patterns**: [Patterns Library](PATTERNS_LIBRARY.md)

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) for overview.
