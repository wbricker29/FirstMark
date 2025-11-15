# Enforcement Levels & Skill Types

## Table of Contents

- [Enforcement Levels](#enforcement-levels)
- [Skill Types](#skill-types)
- [Skip Conditions \& User Control](#skip-conditions--user-control)
- [Decision Guide](#decision-guide)

---

## Enforcement Levels

Claude Code supports three enforcement levels that control how skills activate and interact with the user's workflow.

### BLOCK (Critical Guardrails)

**Mechanism**: Exit code 2 from PreToolUse hook, stderr → Claude

**Behavior**:
- Physically prevents Edit/Write tool execution
- Claude sees block message and must use skill to proceed
- Cannot bypass without using skill or skip condition

**Use for**:
- Critical mistakes that cause runtime errors
- Data integrity concerns (database schema validation)
- Security vulnerabilities
- Breaking compatibility issues

**Configuration**:
```json
{
  "my-skill": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "critical",
    "blockMessage": "⚠️ BLOCKED ...",
    "fileTriggers": { ... }
  }
}
```

**Example conversation flow**:
```
User: "Add a new user service with Prisma"

Claude: "I'll create the user service..."
    [Attempts to Edit form/src/services/user.ts]

PreToolUse Hook: [Exit code 2]
    stderr: "⚠️ BLOCKED - Use database-verification skill"

Claude: "I need to use the database-verification skill first..."
    [Uses Skill tool]
    [Retries Edit - now allowed]
```

**Warning**: Use sparingly! Blocking is disruptive to workflow. Only for critical issues.

---

### SUGGEST (Recommended)

**Mechanism**: UserPromptSubmit hook injects context before Claude sees prompt

**Behavior**:
- Advisory, not mandatory
- Claude is aware of relevant skills
- Claude can choose to use skill or proceed without it
- Non-blocking, maintains workflow momentum

**Use for**:
- Domain guidance (React best practices)
- Complex systems requiring deep knowledge
- Best practices documentation
- How-to guides
- Architectural patterns

**Configuration**:
```json
{
  "my-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": { ... },
    "fileTriggers": { ... }
  }
}
```

**Example conversation flow**:
```
User: "Create a React dashboard component"

UserPromptSubmit Hook: [Exit code 0]
    stdout: "📚 RECOMMENDED SKILLS: frontend-guidelines"

Claude: [Sees recommendation + user prompt]
    "I'll use the frontend-guidelines skill for best practices..."
    [Uses Skill tool]
    [Creates component following guidelines]
```

**Recommendation**: Most skills should use `"suggest"` enforcement.

---

### WARN (Optional)

**Mechanism**: Similar to SUGGEST but lower priority

**Behavior**:
- Low priority suggestions
- Advisory only, minimal enforcement
- Mentioned but not emphasized
- Minimal impact on workflow

**Use for**:
- Nice-to-have suggestions
- Informational reminders
- Optional optimizations
- Context-aware tips

**Configuration**:
```json
{
  "my-skill": {
    "type": "domain",
    "enforcement": "warn",
    "priority": "low",
    "promptTriggers": { ... }
  }
}
```

**Rarely used** - most skills are either BLOCK or SUGGEST.

---

## Skill Types

### 1. Guardrail Skills

**Purpose**: Enforce critical best practices that prevent errors

**Characteristics**:
- Type: `"guardrail"`
- Enforcement: `"block"`
- Priority: `"critical"` or `"high"`
- Blocks file edits until skill used
- Prevents common mistakes
- Session-aware (don't repeat nag in same session)

**Examples**:
- `database-verification` - Verify table/column names before Prisma queries
- `security-check` - Enforce security patterns before deployment
- `schema-validation` - Validate data structures before API changes

**When to use**:
- Mistakes that cause runtime errors
- Data corruption risks
- Security vulnerabilities
- Breaking changes to APIs or schemas
- Critical compatibility issues

**Configuration template**:
```json
{
  "guardrail-skill": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "critical",

    "fileTriggers": {
      "pathPatterns": ["**/critical-files/**/*.ts"],
      "contentPatterns": ["dangerousOperation\\("]
    },

    "blockMessage": "⚠️ BLOCKED - Critical Operation Detected\n\n📋 REQUIRED ACTION:\n1. Use Skill tool: 'guardrail-skill'\n2. Verify preconditions\n3. Then retry\n\nReason: {reason}\nFile: {file_path}",

    "skipConditions": {
      "sessionSkillUsed": true,
      "fileMarkers": ["@verified"],
      "envOverride": "SKIP_GUARDRAIL"
    }
  }
}
```

**Important**:
- Always include `blockMessage` with clear actionable steps
- Always include `skipConditions` with session tracking
- Test thoroughly to avoid false positives
- Document skip mechanisms for users

---

### 2. Domain Skills

**Purpose**: Provide comprehensive guidance for specific areas

**Characteristics**:
- Type: `"domain"`
- Enforcement: `"suggest"` or `"warn"`
- Priority: `"high"`, `"medium"`, or `"low"`
- Advisory, not mandatory
- Topic or domain-specific
- Comprehensive documentation

**Examples**:
- `frontend-dev-guidelines` - React/TypeScript best practices
- `backend-dev-guidelines` - Node.js/Express/TypeScript patterns
- `error-tracking` - Sentry integration guidance
- `testing-patterns` - Unit/integration testing guide

**When to use**:
- Complex systems requiring deep knowledge
- Best practices for frameworks or libraries
- Architectural patterns and design principles
- Step-by-step how-to guides
- Technology-specific workflows

**Configuration template**:
```json
{
  "domain-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",

    "promptTriggers": {
      "keywords": ["react", "component", "typescript"],
      "intentPatterns": ["(create|build|add).*?(component|UI)"]
    },

    "fileTriggers": {
      "pathPatterns": ["frontend/src/**/*.tsx"],
      "pathExclusions": ["**/*.test.tsx"]
    }
  }
}
```

**Recommendation**: Start with domain skills. Upgrade to guardrails only when enforcement is critical.

---

## Skip Conditions & User Control

Skip conditions provide escape hatches and prevent workflow disruption. Essential for guardrails, optional for domain skills.

### 1. Session Tracking

**Purpose**: Don't nag repeatedly in same session

**How it works**:
- First edit → Hook blocks/suggests, updates session state
- Second edit (same session) → Hook allows (already used skill)
- Different session → Blocks/suggests again
- State persists for session duration only

**State file**: `.claude/hooks/state/skills-used-{session_id}.json`

**Configuration**:
```json
"skipConditions": {
  "sessionSkillUsed": true
}
```

**Example**:
```
Session A:
  Edit 1: user.ts → BLOCKED "Use database-verification" → User uses skill
  Edit 2: user.ts → ALLOWED (already used in this session)
  Edit 3: profile.ts → ALLOWED (already used in this session)

Session B (new day):
  Edit 1: user.ts → BLOCKED "Use database-verification" (new session)
```

**Recommendation**: Always enable for guardrails (`sessionSkillUsed: true`).

---

### 2. File Markers

**Purpose**: Permanent skip for verified files

**Marker**: `// @skip-validation` (or custom)

**Usage**:
```typescript
// @skip-validation
import { PrismaClient } from "@prisma/client"
// This file has been manually verified
```

**Configuration**:
```json
"skipConditions": {
  "fileMarkers": ["@skip-validation", "@verified"]
}
```

**How it works**:
- Hook reads file content
- Searches for marker comment
- If found, skips activation for this file
- Permanent (until marker removed)

**Warning**: Use sparingly! Defeats the purpose if overused. Only for thoroughly verified files.

---

### 3. Environment Variables

**Purpose**: Emergency disable, temporary override

**Global disable**:
```bash
export SKIP_SKILL_GUARDRAILS=true  # Disables ALL PreToolUse blocks
```

**Skill-specific**:
```bash
export SKIP_DB_VERIFICATION=true
export SKIP_SECURITY_CHECK=true
```

**Configuration**:
```json
"skipConditions": {
  "envOverride": "SKIP_DB_VERIFICATION"
}
```

**How it works**:
- Hook checks if environment variable is set
- If set to `"true"`, skips activation
- Persists until variable unset or shell closed

**Use cases**:
- Emergency situations (broken hook, false positives)
- Temporary disable during refactoring
- Testing without guardrails
- CI/CD pipelines (if needed)

**Warning**: Global disable (`SKIP_SKILL_GUARDRAILS`) bypasses all safety checks. Use with caution.

---

## Decision Guide

Use this guide to choose the right enforcement level and skill type:

### When to use BLOCK enforcement

✅ **Use BLOCK when**:
- Mistakes cause runtime errors (database column names)
- Data corruption or loss possible
- Security vulnerabilities introduced
- Breaking changes to APIs or contracts
- Critical compatibility issues

❌ **Don't use BLOCK when**:
- Best practices or style preferences
- Performance optimizations
- Code organization suggestions
- Non-critical guidance

**Golden rule**: If the consequence is a production outage or data loss, use BLOCK. Otherwise, use SUGGEST.

---

### When to use SUGGEST enforcement

✅ **Use SUGGEST when**:
- Providing best practices
- Complex domain knowledge needed
- Architectural guidance helpful
- Framework-specific patterns
- How-to procedures
- Most skills

❌ **Don't use SUGGEST when**:
- Critical errors must be prevented (use BLOCK)
- Suggestion is optional/nice-to-have (use WARN)

**Golden rule**: If the skill significantly helps but isn't critical, use SUGGEST.

---

### When to use WARN enforcement

✅ **Use WARN when**:
- Optional nice-to-have suggestions
- Informational tips
- Context-aware reminders
- Low-priority optimizations

❌ **Don't use WARN when**:
- Guidance is important (use SUGGEST)
- Enforcement is critical (use BLOCK)

**Golden rule**: Rarely used. Most skills should be SUGGEST or BLOCK.

---

### Guardrail vs Domain

| Aspect | Guardrail | Domain |
|--------|-----------|--------|
| **Purpose** | Prevent errors | Provide guidance |
| **Enforcement** | BLOCK | SUGGEST/WARN |
| **Priority** | Critical/High | High/Medium/Low |
| **Disruption** | High (blocks) | Low (suggests) |
| **Use when** | Critical issues | Best practices |
| **Skip conditions** | Required | Optional |
| **Block message** | Required | Not applicable |

---

## Best Practices

### For Guardrails (BLOCK)

✅ **Do**:
- Test extensively before deploying
- Provide clear, actionable block messages
- Enable session tracking to prevent nagging
- Provide file markers for verified files
- Provide env override for emergencies
- Document skip mechanisms
- Use specific file/content patterns to avoid false positives

❌ **Don't**:
- Block for style preferences or best practices
- Create overly broad patterns (blocks too much)
- Forget to test with real workflows
- Skip validation without good reason
- Use blocking as first resort

---

### For Domain Skills (SUGGEST)

✅ **Do**:
- Provide comprehensive guidance in SKILL.md
- Use clear, specific trigger keywords
- Test activation with real prompts
- Include examples and code snippets
- Make skill genuinely helpful

❌ **Don't**:
- Create overly broad triggers (false positives)
- Make triggers too specific (false negatives)
- Forget to update YAML description with keywords

---

## Next Steps

**Ready to configure enforcement?**

1. **Configure skill-rules.json**: [Skill Rules Config](SKILL_RULES_CONFIG.md)
2. **Understand triggers**: [Hooks & Triggers](HOOKS_AND_TRIGGERS.md)
3. **Test configuration**: [Testing Claude Code](TESTING_CLAUDE_CODE.md)
4. **Use patterns**: [Patterns Library](PATTERNS_LIBRARY.md)

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) or [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md).
