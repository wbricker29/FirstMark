# Hooks & Triggers - Auto-Activation System

## Table of Contents

- [Hook Mechanisms](#hook-mechanisms)
- [Trigger Types](#trigger-types)
- [Best Practices](#best-practices)

---

## Hook Mechanisms

Claude Code uses hooks to automatically activate skills based on context. Understanding how these hooks work is essential for creating effective Claude Code skills.

### UserPromptSubmit Hook (Proactive Suggestions)

**File**: `.claude/hooks/skill-activation-prompt.ts`

**Purpose**: Suggest relevant skills BEFORE Claude processes the user's prompt

**How it works**:

1. User submits prompt
2. Hook executes and reads prompt from stdin (JSON)
3. Hook loads skill-rules.json
4. Hook matches keywords and intent patterns
5. Hook groups matches by priority (critical → high → medium → low)
6. Hook outputs formatted message to stdout
7. Claude sees the message as additional context
8. Claude responds with awareness of suggested skills

**Exit code**: Always 0 (non-blocking, advisory only)

**Input format**:

```json
{
  "session_id": "abc-123",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/project/path",
  "permission_mode": "normal",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "how does the layout system work?"
}
```

**Output format** (stdout → Claude's context):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 RECOMMENDED SKILLS:
  → project-catalog-developer

ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Use cases**:

- Topic-based skills (e.g., "error tracking", "database")
- Implicit work detection (e.g., "create API")
- Technology mentions (e.g., "Prisma", "React")

---

### PreToolUse Hook (Guardrails)

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

**Input format**:

```json
{
  "session_id": "abc-123",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/project/path",
  "permission_mode": "normal",
  "hook_event_name": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/project/form/src/services/user.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

**Output format** (stderr → Claude when blocked):

```
⚠️ BLOCKED - Database Operation Detected

📋 REQUIRED ACTION:
1. Use Skill tool: 'database-verification'
2. Verify ALL table and column names against schema
3. Check database structure with DESCRIBE commands
4. Then retry this edit

Reason: Prevent column name errors in Prisma queries
File: form/src/services/user.ts

💡 TIP: Add '// @skip-validation' comment to skip future checks
```

**Use cases**:

- Critical guardrails (database verification, security checks)
- File-based activation (editing specific files)
- Content-based activation (code uses specific libraries)

**Warning**: Use sparingly! Blocking is disruptive. Only for critical issues.

---

### Stop Hook (Gentle Reminders)

**File**: `.claude/hooks/error-handling-reminder.ts`

**Purpose**: Gentle reminder AFTER Claude responds to self-assess code quality

**How it works**:

1. Claude finishes responding
2. Hook executes and analyzes edited files
3. Hook detects risky patterns (missing error handling, etc.)
4. Hook displays reminder if needed (non-blocking)

**Philosophy** (2025-10-27): Gentle post-response reminders instead of blocking PreToolUse. Maintains awareness without workflow friction.

**Use cases**:

- Error handling awareness
- Code quality reminders
- Non-blocking best practice suggestions

---

### Exit Code Reference

| Exit Code | Hook Type | stdout | stderr | Tool Execution | Claude Sees |
|-----------|-----------|--------|--------|----------------|-------------|
| 0 | UserPromptSubmit | → Claude context | → User only | N/A | stdout content |
| 0 | PreToolUse | → User only | → User only | **Proceeds** | Nothing |
| 2 | PreToolUse | → User only | → **Claude** | **BLOCKED** | stderr content |

**Critical**: Exit code 2 from PreToolUse is THE mechanism for enforcement. stderr content is sent to Claude, who sees the block message and knows what to do.

---

## Trigger Types

Triggers determine WHEN skills activate. Claude Code supports four trigger types:

### 1. Keyword Triggers (Explicit)

**How it works**: Case-insensitive substring matching in user's prompt

**Use for**: Topic-based activation where user explicitly mentions the subject

**Configuration**:

```json
"promptTriggers": {
  "keywords": ["layout", "grid", "toolbar", "submission"]
}
```

**Example**:

- User prompt: "how does the **layout** system work?"
- Matches: "layout" keyword
- Activates: skill

**Best practices**:

- ✅ Use specific, unambiguous terms
- ✅ Include common variations ("layout", "layout system", "grid layout")
- ✅ Test with real prompts
- ❌ Avoid overly generic words ("system", "work", "create")

---

### 2. Intent Pattern Triggers (Implicit)

**How it works**: Regex pattern matching to detect user's intent

**Use for**: Action-based activation where user describes what they want to do

**Configuration**:

```json
"promptTriggers": {
  "intentPatterns": [
    "(create|add|implement).*?(feature|endpoint)",
    "(how does|explain).*?(layout|workflow)"
  ]
}
```

**Examples**:

User prompt: "add user tracking feature"

- Matches: `(add).*?(feature)`
- Activates: skill

User prompt: "create a dashboard widget"

- Matches: `(create).*?(component)` (if component in pattern)
- Activates: skill

**Best practices**:

- ✅ Capture common action verbs: `(create|add|modify|build|implement)`
- ✅ Include domain-specific nouns: `(feature|endpoint|component|workflow)`
- ✅ Use non-greedy matching: `.*?` instead of `.*`
- ✅ Test patterns thoroughly (<https://regex101.com/>)
- ❌ Don't make patterns too broad (false positives)
- ❌ Don't make patterns too specific (false negatives)

**Common patterns**:

```regex
# Database Work
(add|create|implement).*?(user|login|auth|feature)

# Explanations
(how does|explain|what is|describe).*?

# Frontend Work
(create|add|make|build).*?(component|UI|page|modal|dialog)

# Error Handling
(fix|handle|catch|debug).*?(error|exception|bug)

# Workflow Operations
(create|add|modify).*?(workflow|step|branch|condition)
```

---

### 3. File Path Triggers

**How it works**: Glob pattern matching against the file path being edited

**Use for**: Domain/area-specific activation based on file location

**Configuration**:

```json
"fileTriggers": {
  "pathPatterns": [
    "frontend/src/**/*.tsx",
    "form/src/**/*.ts"
  ],
  "pathExclusions": [
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
```

**Glob pattern syntax**:

- `**` = Any number of directories (including zero)
- `*` = Any characters within a directory name
- Examples:
  - `frontend/src/**/*.tsx` = All .tsx files in frontend/src and subdirs
  - `**/schema.prisma` = schema.prisma anywhere in project
  - `form/src/**/*.ts` = All .ts files in form/src subdirs

**Example**:

- File being edited: `frontend/src/components/Dashboard.tsx`
- Matches: `frontend/src/**/*.tsx`
- Activates: skill

**Best practices**:

- ✅ Be specific to avoid false positives
- ✅ Use exclusions for test files: `**/*.test.ts`
- ✅ Consider subdirectory structure
- ✅ Test patterns with actual file paths
- ✅ Use narrower patterns: `form/src/services/**` not `form/**`

**Common patterns**:

```glob
# Frontend
frontend/src/**/*.tsx        # All React components
frontend/src/**/*.ts         # All TypeScript files
frontend/src/components/**   # Only components directory

# Backend Services
form/src/**/*.ts            # Form service
email/src/**/*.ts           # Email service
users/src/**/*.ts           # Users service

# Database
**/schema.prisma            # Prisma schema (anywhere)
**/migrations/**/*.sql      # Migration files
database/src/**/*.ts        # Database scripts

# Test Exclusions
**/*.test.ts                # TypeScript tests
**/*.test.tsx               # React component tests
**/*.spec.ts                # Spec files
```

---

### 4. Content Pattern Triggers

**How it works**: Regex pattern matching against the file's actual content

**Use for**: Technology-specific activation based on what the code imports or uses

**Configuration**:

```json
"contentTriggers": {
  "patterns": [
    "import.*?PrismaClient",
    "@Controller",
    "class.*?Controller"
  ]
}
```

**Examples**:

File contains: `import { PrismaClient } from '@prisma/client'`

- Matches: `import.*?PrismaClient`
- Activates: database-verification skill

File contains: `@Controller('users')`

- Matches: `@Controller`
- Activates: backend-dev-guidelines skill

**Best practices**:

- ✅ Match import statements: `import.*?LibraryName`
- ✅ Match class decorators: `@Decorator`
- ✅ Match specific patterns: `class.*?Controller`
- ✅ Test patterns against actual code
- ❌ Don't use overly broad patterns
- ❌ Remember performance: content matching reads entire file

**Common patterns**:

```regex
# Prisma
import.*?PrismaClient
import.*?@prisma/client

# NestJS Controllers
@Controller
class.*?Controller
export class.*?Controller

# Services/Repositories
class.*?Service
class.*?Repository

# React
import.*?React
from ['"]react['"]

# Error Handling
Sentry
@sentry/

# Testing
describe\(
it\(
test\(
```

---

## Best Practices

### Trigger Selection

**Use keyword triggers when**:

- User will explicitly mention the topic
- Clear, unambiguous terminology
- Simple substring matching sufficient

**Use intent patterns when**:

- User describes actions ("create", "add", "fix")
- Need to detect implicit work
- Want to catch variations of intent

**Use file path triggers when**:

- Skill applies to specific directories or file types
- Domain-specific by location (frontend/, backend/, database/)
- Technology-specific by extension (.tsx, .prisma, .sql)

**Use content triggers when**:

- Skill applies to specific libraries or frameworks
- Detection based on imports or decorators
- Technology-specific by usage (Prisma, NestJS, React)

---

### Testing Triggers

**Manual testing - UserPromptSubmit**:

```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Manual testing - PreToolUse**:

```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

**Test checklist**:

- [ ] Triggers on expected prompts (no false negatives)
- [ ] Doesn't trigger on unrelated prompts (no false positives)
- [ ] File path patterns match actual project structure
- [ ] Content patterns match actual code syntax
- [ ] Intent patterns tested with regex tool
- [ ] Performance acceptable (<100ms for prompts, <200ms for file ops)

---

### Performance Considerations

**Keyword triggers**: Fast (~1-5ms)

- Simple substring matching
- Always enabled

**Intent patterns**: Moderate (~5-20ms)

- Regex matching, depends on pattern complexity
- Keep patterns simple

**File path triggers**: Fast (~1-5ms)

- Glob matching against single path
- Always enabled for PreToolUse

**Content triggers**: Slow (~50-200ms)

- Reads entire file content
- Regex matching against potentially large files
- Use sparingly
- Consider file size limits

**Recommendation**: Prefer keyword + intent + file path triggers. Use content triggers only when necessary.

---

### Combining Trigger Types

Most effective skills use **multiple trigger types**:

**Example - Database Verification Skill**:

```json
{
  "database-verification": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "critical",
    "promptTriggers": {
      "keywords": ["prisma", "database", "query", "schema"],
      "intentPatterns": [
        "(add|create|implement).*?(user|login|auth|feature)",
        "(query|select|find).*?(user|data)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "**/services/**/*.ts",
        "**/repositories/**/*.ts"
      ]
    },
    "contentTriggers": {
      "patterns": [
        "import.*?PrismaClient",
        "\\.findMany\\(",
        "\\.findFirst\\(",
        "\\.create\\("
      ]
    }
  }
}
```

This skill activates when:

- User mentions "prisma" or "database" (keyword)
- User wants to "add user feature" (intent)
- Editing service files (file path)
- Code uses Prisma client methods (content)

**Result**: Comprehensive coverage with minimal false positives.

---

## Next Steps

**Ready to configure triggers?**

1. **Configure skill-rules.json**: [Skill Rules Config](SKILL_RULES_CONFIG.md)
2. **Choose enforcement**: [Enforcement Levels](ENFORCEMENT_LEVELS.md)
3. **Test and debug**: [Testing Claude Code](TESTING_CLAUDE_CODE.md)
4. **Use patterns**: [Patterns Library](PATTERNS_LIBRARY.md)

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) or [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md).
