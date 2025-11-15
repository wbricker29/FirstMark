# Testing Claude Code Skills

## Table of Contents

- [Manual Testing Commands](#manual-testing-commands)
- [Testing Checklist](#testing-checklist)
- [Troubleshooting](#troubleshooting)
- [Performance Testing](#performance-testing)

---

## Manual Testing Commands

### Test UserPromptSubmit Hook

Test keyword and intent pattern triggers:

```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Expected output**: Your skill should appear in the suggestions

**Example**:
```bash
echo '{"session_id":"test","prompt":"help me process a PDF"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts```

Should output something like:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 RECOMMENDED SKILLS:
  → pdf-processing

ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Test PreToolUse Hook

Test file path and content triggers:

```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"frontend/src/components/Test.tsx"}}
EOF
```

**For blocking guardrails**, expected output (to stderr):
```
⚠️ BLOCKED - [Reason]

📋 REQUIRED ACTION:
1. Use Skill tool: 'skill-name'
2. [Steps...]

File: frontend/src/components/Test.tsx
```

**For non-matching files**, expected: No output (exit code 0)

---

## Testing Checklist

Use this comprehensive checklist when creating or updating Claude Code skills:

### Configuration Validation

- [ ] JSON syntax valid: `jq .claude/skills/skill-rules.json`
- [ ] Skill name matches SKILL.md frontmatter exactly
- [ ] All required fields present (type, enforcement, priority)
- [ ] Guardrails have `blockMessage` field
- [ ] Block messages use `{file_path}` placeholder correctly

### Keyword Triggers

- [ ] Tested with 3+ real user prompts (expected matches)
- [ ] Tested with 3+ unrelated prompts (no false positives)
- [ ] Keywords are case-insensitive
- [ ] Keywords appear in YAML description
- [ ] All common variations included

**Test command**:
```bash
# Should match
echo '{"prompt":"create react component"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# Should not match
echo '{"prompt":"unrelated task"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
```

---

### Intent Pattern Triggers

- [ ] Regex patterns tested on https://regex101.com/
- [ ] Patterns tested with real prompts
- [ ] Non-greedy matching used (`.*?` not `.*`)
- [ ] Patterns not too broad (false positives)
- [ ] Patterns not too specific (false negatives)
- [ ] Special regex characters escaped in JSON (`\\.`, `\\(`, etc.)

**Test examples**:
```bash
# Action-based intent
echo '{"prompt":"add user authentication"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# Question-based intent
echo '{"prompt":"how does the layout system work"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
```

---

### File Path Triggers

- [ ] Path patterns match actual project structure
- [ ] Glob syntax correct (`**` for recursive, `*` for single level)
- [ ] Test files excluded (`**/*.test.ts`, `**/*.spec.ts`)
- [ ] Tested with actual file paths from project
- [ ] No overly broad patterns (`**/*.ts` too general)

**Test command**:
```bash
# Should match pattern
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"frontend/src/components/Dashboard.tsx"}}
EOF

# Should not match (test file)
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"frontend/src/components/Dashboard.test.tsx"}}
EOF
```

---

### Content Pattern Triggers

- [ ] Patterns match actual code syntax
- [ ] Regex special characters escaped (`\\.`, `\\(`, `\\[`, etc.)
- [ ] Tested against real file content
- [ ] Performance acceptable (<200ms)
- [ ] Patterns not overly broad (check entire codebase)

**Test command**:
```bash
# Create test file with content
echo "import { PrismaClient } from '@prisma/client'" > test.ts

# Test content trigger
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"./test.ts"}}
EOF

rm test.ts
```

---

### Guardrail Specific

- [ ] Block message clear and actionable
- [ ] Block message includes {file_path} placeholder
- [ ] Session tracking enabled (`sessionSkillUsed: true`)
- [ ] File markers configured (e.g., `["@skip-validation"]`)
- [ ] Env override configured (e.g., `"SKIP_MY_SKILL"`)
- [ ] Skip conditions tested:
  - [ ] First edit blocks
  - [ ] Second edit in same session allows
  - [ ] File marker skips activation
  - [ ] Env var skips activation

**Test session tracking**:
```bash
# First edit (should block)
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test-session","tool_name":"Edit","tool_input":{"file_path":"services/user.ts"}}
EOF

# Simulate skill use (update session state manually or use actual skill)

# Second edit same session (should allow)
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test-session","tool_name":"Edit","tool_input":{"file_path":"services/profile.ts"}}
EOF
```

---

### Domain Skill Specific

- [ ] Comprehensive SKILL.md content (<500 lines)
- [ ] Clear use cases and examples
- [ ] Reference files for detailed information
- [ ] Triggers tested with realistic scenarios
- [ ] No blocking (enforcement: "suggest")

---

## Troubleshooting

### Skill Not Triggering (UserPromptSubmit)

**Symptoms**: Ask a question, but no skill suggestion appears

**Common causes**:

1. **Keywords don't match**
   - Check `promptTriggers.keywords` in skill-rules.json
   - Are keywords actually in your prompt?
   - Remember: case-insensitive substring matching

2. **Intent patterns too specific**
   - Test regex at https://regex101.com/
   - May need broader patterns
   - Use non-greedy `.*?` not `.*`

3. **Typo in skill name**
   - Skill name in SKILL.md frontmatter must match skill-rules.json exactly

4. **JSON syntax error**
   - Validate: `jq .claude/skills/skill-rules.json`
   - Common: trailing commas, missing quotes, single quotes

**Debug**:
```bash
echo '{"session_id":"debug","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

Expected: Your skill appears in output

---

### Skill Not Blocking (PreToolUse)

**Symptoms**: Edit a file that should trigger guardrail, but no block occurs

**Common causes**:

1. **File path doesn't match patterns**
   - Check file path being edited
   - Check `fileTriggers.pathPatterns`
   - Verify glob syntax (`**/*.tsx`)

2. **Content pattern doesn't match**
   - Check if file actually contains the pattern
   - Verify regex is correct (test on regex101.com)
   - Check special characters are escaped

3. **Skip condition active**
   - Skill already used in this session?
   - File has `@skip-validation` marker?
   - Env var set (`SKIP_*` or `SKIP_SKILL_GUARDRAILS`)?

4. **Hook not registered**
   - Check `.claude/settings.json`
   - Verify hook file exists and is executable

**Debug**:
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"debug","tool_name":"Edit","tool_input":{"file_path":"path/to/file.ts"}}
EOF
```

Expected for guardrail: Block message to stderr, exit code 2

---

### False Positives

**Symptoms**: Skill triggers when it shouldn't

**Common causes**:

1. **Keywords too broad**
   - "system", "work", "create" match everything
   - Use more specific keywords

2. **Intent patterns too broad**
   - `.*?` matches too much
   - Add more specific nouns/verbs

3. **File patterns too broad**
   - `**/*.ts` matches all TypeScript files
   - Narrow to specific directories

4. **Content patterns too simple**
   - `"import"` matches all imports
   - Make patterns more specific: `"import.*?SpecificLibrary"`

**Fix**: Tighten patterns, test thoroughly

---

### Hook Not Executing

**Symptoms**: Hook doesn't run at all

**Common causes**:

1. **Hook not registered in settings.json**
   - Check `.claude/settings.json`
   - Verify hook path and event type

2. **Permission issues**
   - Check hook file is executable: `chmod +x .claude/hooks/*.ts`

3. **Node modules missing**
   - Run `npm install` in project root
   - Verify `npx tsx` works

4. **Hook file errors**
   - Test hook directly: `npx tsx .claude/hooks/skill-activation-prompt.ts`
   - Check for syntax errors or crashes

**Debug**:
```bash
# Test hook directly
npx tsx .claude/hooks/skill-activation-prompt.ts <<< '{"prompt":"test"}'
```

Should output skill suggestions or nothing (if no match)

---

## Performance Testing

### Target Performance

- **UserPromptSubmit**: < 100ms (keyword + intent matching)
- **PreToolUse**: < 200ms (file path + content matching)

### Measure Performance

```bash
# Time UserPromptSubmit
time (echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts)

# Time PreToolUse
time (cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
)
```

### Performance Issues

**If UserPromptSubmit is slow (>100ms)**:
- Too many intent patterns (regex is expensive)
- Complex regex patterns
- Too many skills in skill-rules.json

**If PreToolUse is slow (>200ms)**:
- Too many content patterns (reads file multiple times)
- Large files being read
- Complex regex on large content

**Solutions**:
- Simplify regex patterns
- Reduce number of content patterns
- Cache file reads if possible
- Use file path triggers instead of content when possible

---

## Best Practices

### Testing Workflow

1. **Start small**: Test one trigger type at a time
2. **Test both paths**: Positive matches AND negative matches
3. **Use real data**: Test with actual prompts and file paths from project
4. **Automate**: Create test scripts for regression testing
5. **Document**: Keep examples of working/non-working prompts

### Validation Scripts

Create a test suite:

```bash
#!/bin/bash
# test-skills.sh

echo "Testing pdf-processing skill..."

# Should match
echo '{"prompt":"process PDF"}' | npx tsx .claude/hooks/skill-activation-prompt.ts | grep "pdf-processing" && echo "✓ Match" || echo "✗ No match"

# Should not match
echo '{"prompt":"unrelated task"}' | npx tsx .claude/hooks/skill-activation-prompt.ts | grep "pdf-processing" && echo "✗ False positive" || echo "✓ Correct"
```

Make executable: `chmod +x test-skills.sh`

Run: `./test-skills.sh`

---

## Next Steps

**Ready to deploy?**

1. **Complete checklist**: Run through all items above
2. **Test in real project**: Use skill in actual workflow
3. **Monitor false positives**: Adjust patterns as needed
4. **Document findings**: Update skill-rules.json comments
5. **Iterate**: Improve based on real usage

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) or [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md).
