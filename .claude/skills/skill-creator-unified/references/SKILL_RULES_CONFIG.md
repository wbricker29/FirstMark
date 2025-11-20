# Skill Rules Configuration

## Table of Contents

- [File Location](#file-location)
- [Complete TypeScript Schema](#complete-typescript-schema)
- [Field Guide](#field-guide)
- [Configuration Examples](#configuration-examples)
- [Validation](#validation)

---

## File Location

**Path**: `.claude/skills/skill-rules.json`

This JSON file defines all Claude Code skills and their trigger conditions for the auto-activation system.

**Note**: This file is only needed for Claude Code skills. General skills don't require skill-rules.json.

---

## Complete TypeScript Schema

```typescript
interface SkillRules {
  version: string
  skills: Record<string, SkillRule>
}

interface SkillRule {
  type: "guardrail" | "domain"
  enforcement: "block" | "suggest" | "warn"
  priority: "critical" | "high" | "medium" | "low"

  promptTriggers?: {
    keywords?: string[]
    intentPatterns?: string[] // Regex strings
  }

  fileTriggers?: {
    pathPatterns: string[] // Glob patterns
    pathExclusions?: string[] // Glob patterns
    contentPatterns?: string[] // Regex strings
    createOnly?: boolean // Only trigger on file creation
  }

  blockMessage?: string // For guardrails, {file_path} placeholder

  skipConditions?: {
    sessionSkillUsed?: boolean // Skip if used in session
    fileMarkers?: string[] // e.g., ["@skip-validation"]
    envOverride?: string // e.g., "SKIP_DB_VERIFICATION"
  }
}
```

---

## Field Guide

### Top Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Schema version (currently "1.0") |
| `skills` | object | Yes | Map of skill name → SkillRule |

**Example**:
```json
{
  "version": "1.0",
  "skills": {
    "my-skill": { ... },
    "another-skill": { ... }
  }
}
```

---

### SkillRule Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | "guardrail" (enforced) or "domain" (advisory) |
| `enforcement` | string | Yes | "block" (PreToolUse), "suggest" (UserPromptSubmit), or "warn" |
| `priority` | string | Yes | "critical", "high", "medium", or "low" |
| `promptTriggers` | object | Optional | Triggers for UserPromptSubmit hook |
| `fileTriggers` | object | Optional | Triggers for PreToolUse hook |
| `blockMessage` | string | Optional* | Required if enforcement="block". Use `{file_path}` placeholder |
| `skipConditions` | object | Optional | Escape hatches and session tracking |

*Required for guardrails (enforcement="block")

---

### promptTriggers Fields

Used by **UserPromptSubmit hook** to detect when skill should be suggested.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `keywords` | string[] | Optional | Exact substring matches (case-insensitive) |
| `intentPatterns` | string[] | Optional | Regex patterns for intent detection |

**Example**:
```json
"promptTriggers": {
  "keywords": ["pdf", "document", "extract"],
  "intentPatterns": [
    "(process|parse|extract).*?(pdf|document)",
    "(convert|transform).*?(pdf)"
  ]
}
```

See [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md#trigger-types) for complete trigger documentation.

---

### fileTriggers Fields

Used by **PreToolUse hook** to detect file operations that should activate the skill.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pathPatterns` | string[] | Yes* | Glob patterns for file paths |
| `pathExclusions` | string[] | Optional | Glob patterns to exclude (e.g., test files) |
| `contentPatterns` | string[] | Optional | Regex patterns to match file content |
| `createOnly` | boolean | Optional | Only trigger when creating new files |

*Required if fileTriggers is present

**Example**:
```json
"fileTriggers": {
  "pathPatterns": [
    "frontend/src/**/*.tsx",
    "**/*.test.ts"
  ],
  "pathExclusions": [
    "**/*.spec.ts"
  ],
  "contentPatterns": [
    "import.*?React",
    "from ['\"]react['\"]"
  ]
}
```

See [Claude Code Overview - Trigger Types](CLAUDE_CODE_OVERVIEW.md#trigger-types) for complete documentation.

---

### skipConditions Fields

Controls when to skip activation (user override mechanisms).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sessionSkillUsed` | boolean | Optional | Skip if skill already used this session |
| `fileMarkers` | string[] | Optional | Skip if file contains comment marker |
| `envOverride` | string | Optional | Environment variable name to disable skill |

**Example**:
```json
"skipConditions": {
  "sessionSkillUsed": true,
  "fileMarkers": ["@skip-validation", "@verified"],
  "envOverride": "SKIP_MY_SKILL"
}
```

**Session tracking**: First edit triggers, second edit in same session skips.

**File markers**: Add `// @skip-validation` comment to permanently skip.

**Env override**: `export SKIP_MY_SKILL=true` disables skill temporarily.

See [Enforcement Levels - Skip Conditions](ENFORCEMENT_LEVELS.md#skip-conditions--user-control) for complete documentation.

---

## Configuration Examples

### Example 1: Simple Domain Skill (Suggestion-based)

**Use case**: Suggest a skill when user mentions specific topics.

```json
{
  "version": "1.0",
  "skills": {
    "pdf-processing": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "medium",
      "promptTriggers": {
        "keywords": ["pdf", "document", "extract text"],
        "intentPatterns": [
          "(process|parse|extract).*?(pdf|document)"
        ]
      }
    }
  }
}
```

**When it activates**:
- User says "help me process a PDF"
- User says "extract text from documents"
- UserPromptSubmit hook suggests the skill to Claude

---

### Example 2: File-Based Domain Skill

**Use case**: Auto-activate when editing specific files.

```json
{
  "version": "1.0",
  "skills": {
    "frontend-guidelines": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["react", "component", "typescript"],
        "intentPatterns": ["(create|add|build).*?(component|UI)"]
      },
      "fileTriggers": {
        "pathPatterns": [
          "frontend/src/**/*.tsx",
          "frontend/src/**/*.ts"
        ],
        "pathExclusions": [
          "**/*.test.tsx",
          "**/*.test.ts"
        ]
      }
    }
  }
}
```

**When it activates**:
- User mentions "react component"
- Editing .tsx files in frontend/src/
- PreToolUse hook suggests the skill before file edits

---

### Example 3: Critical Guardrail Skill (Blocking)

**Use case**: Block file edits until critical verification performed.

```json
{
  "version": "1.0",
  "skills": {
    "database-verification": {
      "type": "guardrail",
      "enforcement": "block",
      "priority": "critical",

      "promptTriggers": {
        "keywords": ["prisma", "database", "query", "schema"],
        "intentPatterns": [
          "(add|create|implement).*?(user|login|feature)",
          "(query|select|find).*?(data|user)"
        ]
      },

      "fileTriggers": {
        "pathPatterns": [
          "**/services/**/*.ts",
          "**/repositories/**/*.ts"
        ],
        "pathExclusions": ["**/*.test.ts"],
        "contentPatterns": [
          "import.*?PrismaClient",
          "\\.findMany\\(",
          "\\.create\\(",
          "\\.update\\("
        ]
      },

      "blockMessage": "⚠️ BLOCKED - Database Operation Detected\n\n📋 REQUIRED ACTION:\n1. Use Skill tool: 'database-verification'\n2. Verify ALL table and column names against schema\n3. Check database structure with DESCRIBE commands\n4. Then retry this edit\n\nReason: Prevent column name errors in Prisma queries\nFile: {file_path}\n\n💡 TIP: Add '// @skip-validation' comment to skip future checks",

      "skipConditions": {
        "sessionSkillUsed": true,
        "fileMarkers": ["@skip-validation"],
        "envOverride": "SKIP_DB_VERIFICATION"
      }
    }
  }
}
```

**When it activates**:
- User mentions "prisma" or "database"
- Editing service files containing Prisma code
- PreToolUse hook BLOCKS the edit
- Claude must use skill before retrying

**Important**:
- `blockMessage` is required for guardrails
- Use `{file_path}` placeholder for file name
- `sessionSkillUsed: true` prevents repeated blocking in same session

---

### Example 4: Content-Based Activation

**Use case**: Activate when file contains specific libraries/frameworks.

```json
{
  "version": "1.0",
  "skills": {
    "nestjs-guidelines": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",

      "promptTriggers": {
        "keywords": ["nestjs", "controller", "service", "module"]
      },

      "fileTriggers": {
        "pathPatterns": ["backend/src/**/*.ts"],
        "pathExclusions": ["**/*.test.ts"],
        "contentPatterns": [
          "@Controller",
          "@Injectable",
          "class.*?Controller",
          "class.*?Service"
        ]
      }
    }
  }
}
```

**When it activates**:
- Editing backend .ts files
- File contains NestJS decorators (`@Controller`, `@Injectable`)
- File defines controllers or services

---

## Validation

### Check JSON Syntax

```bash
# Validate JSON syntax
cat .claude/skills/skill-rules.json | jq .
```

If valid, jq will pretty-print the JSON. If invalid, it will show the error.

---

### Common JSON Errors

**Trailing comma**:
```json
{
  "keywords": ["one", "two"], // ❌ Trailing comma
}
```

**Missing quotes**:
```json
{
  type: "guardrail" // ❌ Missing quotes on key
}
```

**Single quotes** (invalid JSON):
```json
{
  "type": 'guardrail' // ❌ Must use double quotes
}
```

**Unescaped regex backslashes**:
```json
{
  "contentPatterns": ["\.findMany\("] // ❌ Single backslash
}
```

Should be:
```json
{
  "contentPatterns": ["\\.findMany\\("] // ✅ Escaped backslashes
}
```

---

### Validation Checklist

Use this checklist before deploying:

- [ ] JSON syntax valid (use `jq .claude/skills/skill-rules.json`)
- [ ] All skill names match SKILL.md filenames
- [ ] Guardrails have `blockMessage` field
- [ ] Block messages use `{file_path}` placeholder
- [ ] Intent patterns are valid regex (test on regex101.com)
- [ ] File path patterns use correct glob syntax
- [ ] Content patterns escape special regex characters (`\\(`, `\\.`, etc.)
- [ ] Priority matches enforcement level (critical/high for guardrails)
- [ ] No duplicate skill names
- [ ] Session tracking enabled for guardrails (`sessionSkillUsed: true`)

---

### Test Configuration

After editing skill-rules.json, test triggers manually:

**Test UserPromptSubmit**:
```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Test PreToolUse**:
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

See [Testing Claude Code](TESTING_CLAUDE_CODE.md) for complete testing guide.

---

## Best Practices

### Do ✅

- Use `"suggest"` enforcement for most skills
- Configure session tracking for guardrails
- Provide clear, actionable block messages
- Test all regex patterns on regex101.com
- Validate JSON syntax with jq
- Use specific file path patterns to avoid false positives
- Include pathExclusions for test files

### Don't ❌

- Don't use `"block"` enforcement unless critical
- Don't forget to escape regex special characters in JSON
- Don't use overly broad file patterns (`**/*.ts`)
- Don't skip validation before deployment
- Don't create circular dependencies between skills
- Don't forget blockMessage for guardrails

---

## Next Steps

**Ready to configure skills?**

1. **Understand enforcement**: [Enforcement Levels](ENFORCEMENT_LEVELS.md)
2. **Learn triggers**: [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md#trigger-types)
3. **Test configuration**: [Testing Claude Code](TESTING_CLAUDE_CODE.md)
4. **Use patterns**: [Patterns Library](PATTERNS_LIBRARY.md)

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) or [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md).
