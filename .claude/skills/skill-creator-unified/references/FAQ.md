# Frequently Asked Questions

## Table of Contents

- [General Questions](#general-questions)
- [Claude Code Specific Questions](#claude-code-specific-questions)
- [Configuration Questions](#configuration-questions)
- [Troubleshooting Questions](#troubleshooting-questions)

---

## General Questions

### Q: Should I create a general or Claude Code skill?

**A**: Start with **general** if you're unsure. General skills:
- Work everywhere (Claude Desktop, CLI, API)
- Simpler to create and maintain
- Can be migrated to Claude Code later if needed

Use **Claude Code** only if you need:
- Automatic activation based on triggers
- Guardrails that block edits
- Session tracking
- Advanced testing

See [Quick Decision Matrix](../SKILL.md#quick-decision-matrix) in main SKILL.md.

---

### Q: How do I make my skill discoverable?

**A**: Write a rich, detailed description in YAML frontmatter:

**Good example**:
```yaml
description: Guide for processing PDF files. Use when working with PDFs, extracting text from documents, parsing PDF structure, converting PDF to other formats, or analyzing PDF content. Covers PyPDF2, pdfplumber, and pdf2image libraries.
```

**Bad example**:
```yaml
description: PDF tool
```

**Tips**:
- Explain what the skill does
- Explain when to use it
- Include specific trigger words (file extensions, operations, keywords)
- Include library/framework names
- Max 1024 characters
- For Claude Code skills: these keywords also trigger auto-activation

See [IMPLEMENTATION_PHASE.md - Making Skills Discoverable](IMPLEMENTATION_PHASE.md#making-skills-discoverable)

---

### Q: What goes in scripts/ vs references/ vs assets/?

**A**:

**scripts/** - Executable code that the skill runs:
- Python, Bash, TypeScript, etc.
- Helper utilities
- Validation tools
- Initialization scripts
- Examples: `init_skill.py`, `validate_schema.py`

**references/** - Documentation that provides context:
- Markdown files with detailed information
- API documentation
- Schema definitions
- Implementation guides
- Examples: `API_GUIDE.md`, `SCHEMA.md`

**assets/** - Files used in output:
- Templates (config files, boilerplate code)
- Example files
- Images/diagrams
- Configuration samples
- Examples: `template.json`, `example-config.yaml`

See [IMPLEMENTATION_PHASE.md - Bundled Resources](IMPLEMENTATION_PHASE.md#bundled-resources-guide)

---

### Q: What validation checks should I run?

**A**: Run the validation script:
```bash
uv run python scripts/quick_validate.py path/to/skill
```

This checks:
- YAML frontmatter syntax and required fields
- Naming conventions (lowercase-hyphens)
- Description completeness
- Line count (<500 lines for SKILL.md)
- File organization
- Resource references
- For Claude Code: skill-rules.json syntax and schema

For Claude Code skills, also test triggers manually. See [Testing Claude Code](TESTING_CLAUDE_CODE.md)

See [DELIVERY_PHASE.md - Pre-Packaging Validation](DELIVERY_PHASE.md#step-45-pre-packaging-validation)

---

### Q: How do I package my skill for distribution?

**A**:
```bash
# Creates skill-name.zip in current directory
uv run python scripts/package_skill.py path/to/skill-name

# Specify output directory
uv run python scripts/package_skill.py path/to/skill-name ./dist
```

The script automatically:
1. Validates the skill
2. Creates zip file with proper directory structure
3. Reports any errors before packaging
4. Ready for distribution or installation

See [DELIVERY_PHASE.md - Packaging](DELIVERY_PHASE.md#step-5-packaging-a-skill)

---

### Q: How long should SKILL.md be?

**A**: **Under 500 lines** (Anthropic best practice)

Use progressive disclosure:
- **Level 1** (Description): ~100 words, always in context
- **Level 2** (SKILL.md): <500 lines, loaded when triggered
- **Level 3** (References): Unlimited, loaded only when needed

**If SKILL.md exceeds 500 lines**:
- Move detailed content to `references/*.md`
- Keep core workflow in SKILL.md
- Link to reference files for details
- Add table of contents to reference files >100 lines

See [Progressive Disclosure](../SKILL.md#progressive-disclosure)

---

## Claude Code Specific Questions

### Q: Can I add Claude Code features to an existing general skill?

**A**: Yes! Follow the migration guide:

1. Add skill-rules.json entry with triggers
2. Update SKILL.md description with trigger keywords
3. Test triggers with manual commands
4. (Optional) Add file or content triggers
5. (Optional) Configure skip conditions
6. Validate and test

See [Migration Guide](CLAUDE_CODE_OVERVIEW.md#migration-guide) for complete steps.

---

### Q: Do Claude Code skills work outside Claude Code?

**A**: Yes, they gracefully degrade to general skills in other environments:
- The skill-rules.json is simply ignored
- The skill works based on its YAML description only
- No special handling needed
- Users in other environments can still manually invoke the skill

This is why you should:
- Write a clear YAML description
- Make SKILL.md standalone and useful without automation
- Don't rely solely on auto-activation

---

### Q: When should I use BLOCK vs SUGGEST enforcement?

**A**:

**Use BLOCK when** (rare, disruptive):
- Mistakes cause runtime errors (database column names)
- Data corruption or loss possible
- Security vulnerabilities introduced
- Breaking changes to APIs or contracts
- Critical compatibility issues

**Use SUGGEST when** (most skills):
- Providing best practices
- Complex domain knowledge needed
- Architectural guidance helpful
- Framework-specific patterns
- How-to procedures

**Golden rule**: If the consequence is a production outage or data loss, use BLOCK. Otherwise, use SUGGEST.

See [Enforcement Levels - Decision Guide](ENFORCEMENT_LEVELS.md#decision-guide)

---

### Q: How do I debug why my Claude Code skill isn't triggering?

**A**: Test triggers manually:

**For UserPromptSubmit (suggestions)**:
```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

Expected: Your skill should appear in suggestions

**For PreToolUse (guardrails)**:
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

Expected: Block message if file matches patterns

**Common issues**:
- Keywords don't match (check case-insensitive substring)
- Intent patterns too specific (test regex on regex101.com)
- File paths don't match glob patterns
- Content patterns don't match actual code
- Typo in skill name
- JSON syntax error in skill-rules.json

See [Testing Claude Code - Troubleshooting](TESTING_CLAUDE_CODE.md#troubleshooting)

---

### Q: What are session tracking and skip conditions?

**A**: Session tracking prevents repeated nagging:

**How it works**:
- **First edit** → Hook blocks/suggests, updates session state
- **Second edit** (same session) → Hook allows (already used skill)
- **Different session** → Blocks/suggests again

**Skip conditions** provide escape hatches:
- **Session tracking**: Automatic (enable with `sessionSkillUsed: true`)
- **File markers**: Add `// @skip-validation` to permanently skip
- **Env vars**: `export SKIP_MY_SKILL=true` for temporary disable

**Example**:
```json
"skipConditions": {
  "sessionSkillUsed": true,
  "fileMarkers": ["@skip-validation", "@verified"],
  "envOverride": "SKIP_DB_VERIFICATION"
}
```

See [Enforcement Levels - Skip Conditions](ENFORCEMENT_LEVELS.md#skip-conditions--user-control)

---

## Configuration Questions

### Q: What's the difference between keywords and intent patterns?

**A**:

**Keywords** (explicit):
- Simple substring matching (case-insensitive)
- User explicitly mentions the topic
- Fast, reliable
- Example: "prisma", "database", "react"

**Intent patterns** (implicit):
- Regex matching for actions/intent
- User describes what they want to do
- Catches variations
- Example: `"(create|add).*?(component|UI)"`

**When to use**:
- Keywords: User will mention the topic ("help with Prisma")
- Intent: User describes actions ("add user authentication")
- Best: Use both for comprehensive coverage

See [Hooks & Triggers - Trigger Types](HOOKS_AND_TRIGGERS.md#trigger-types)

---

### Q: How do I write good intent patterns?

**A**: Follow these guidelines:

**Good patterns**:
```regex
(create|add|build).*?(component|UI)       # Action + noun
(how does|explain|what is).*?             # Question words
(fix|handle|catch|debug).*?(error|bug)    # Problem-solving
```

**Bad patterns**:
```regex
.*?component.*?                           # Too broad
create a React component                 # Too specific (literal)
(create|add|build|make|construct|...)    # Too many alternatives
```

**Tips**:
- Capture common action verbs
- Include domain-specific nouns
- Use non-greedy matching: `.*?` not `.*`
- Test on regex101.com
- Test with real prompts
- Balance specificity vs coverage

See [Hooks & Triggers - Intent Pattern Triggers](HOOKS_AND_TRIGGERS.md#2-intent-pattern-triggers)

---

### Q: How do I test glob patterns for file paths?

**A**: Test manually with actual project file paths:

**Pattern**: `frontend/src/**/*.tsx`

**Matches**:
- `frontend/src/components/Dashboard.tsx` ✅
- `frontend/src/pages/Home.tsx` ✅
- `frontend/src/components/forms/LoginForm.tsx` ✅ (recursive)

**Doesn't match**:
- `frontend/components/Test.tsx` ❌ (missing `src/`)
- `backend/src/Test.tsx` ❌ (different directory)
- `frontend/src/utils.ts` ❌ (different extension)

**Test command**:
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"frontend/src/components/Test.tsx"}}
EOF
```

See [Hooks & Triggers - File Path Triggers](HOOKS_AND_TRIGGERS.md#3-file-path-triggers)

---

## Troubleshooting Questions

### Q: My skill triggers too often (false positives). How do I fix it?

**A**: Tighten your trigger patterns:

**If keywords too broad**:
- Remove generic words: "system", "work", "create"
- Use more specific terms: "prisma query" not "query"
- Add qualifying context

**If intent patterns too broad**:
- Add more specific nouns: `(create).*?(component)` not `(create).*?`
- Narrow action verbs: `(implement|build)` not `(do|make|work|create|...)`
- Test patterns thoroughly

**If file patterns too broad**:
- Narrow directories: `form/src/services/**` not `**/*.ts`
- Add exclusions: `pathExclusions: ["**/*.test.ts"]`
- Be more specific

**Test after each change** to ensure you didn't break valid matches.

See [Testing Claude Code - False Positives](TESTING_CLAUDE_CODE.md#false-positives)

---

### Q: My skill doesn't trigger when it should (false negatives). How do I fix it?

**A**: Broaden your trigger patterns:

**If keywords too specific**:
- Add variations: "layout", "layouts", "layout system"
- Add synonyms: "grid", "grid layout", "grid system"
- Check case-sensitivity (should be case-insensitive)

**If intent patterns too specific**:
- Broaden action verbs: `(create|add|build|make)`
- Broaden nouns: `(component|UI|widget|element)`
- Use `.*?` to allow words in between

**If file patterns too specific**:
- Check actual file paths in project
- Use `**` for recursive matching
- Verify glob syntax

**Test with real prompts and file paths** from your project.

See [Testing Claude Code - Skill Not Triggering](TESTING_CLAUDE_CODE.md#skill-not-triggering-userpromptsubmit)

---

### Q: How do I handle special characters in regex patterns for JSON?

**A**: Escape backslashes in JSON strings:

**Regex** (for regex101.com):
```regex
\.findMany\(
```

**JSON** (for skill-rules.json):
```json
{
  "contentPatterns": [
    "\\.findMany\\("
  ]
}
```

**Common special characters to escape**:
- `.` → `\\.`
- `(` → `\\(`
- `)` → `\\)`
- `[` → `\\[`
- `]` → `\\]`
- `{` → `\\{`
- `}` → `\\}`
- `\` → `\\\\` (backslash itself)

**Rule**: In JSON, backslashes must be doubled.

See [Skill Rules Config - Common JSON Errors](SKILL_RULES_CONFIG.md#common-json-errors)

---

### Q: Can I have multiple skills trigger at once?

**A**: Yes! This is normal and useful.

**Example**: User asks "add Prisma user authentication"

Might trigger:
1. `database-verification` (guardrail - blocks)
2. `backend-guidelines` (domain - suggests)
3. `error-tracking` (domain - suggests)

**Priority order**:
1. Critical guardrails block first
2. High priority suggestions shown
3. Medium/low priority suggestions mentioned

**Best practice**: Design skills with specific, non-overlapping purposes to minimize confusion.

---

### Q: How do I temporarily disable a Claude Code skill?

**A**: Three options:

**1. Environment variable** (recommended for temporary disable):
```bash
export SKIP_MY_SKILL=true
```

Configure in skill-rules.json:
```json
"skipConditions": {
  "envOverride": "SKIP_MY_SKILL"
}
```

**2. File marker** (permanent skip for specific files):
```typescript
// @skip-validation
import { PrismaClient } from "@prisma/client"
```

**3. Global disable** (emergency, disables ALL guardrails):
```bash
export SKIP_SKILL_GUARDRAILS=true
```

**Warning**: Global disable bypasses all safety checks. Use with caution.

See [Enforcement Levels - Skip Conditions](ENFORCEMENT_LEVELS.md#skip-conditions--user-control)

---

## Next Steps

**Still have questions?**

1. Check the reference guides:
   - [Design Phase](DESIGN_PHASE.md)
   - [Implementation Phase](IMPLEMENTATION_PHASE.md)
   - [Delivery Phase](DELIVERY_PHASE.md)
   - [Claude Code Overview](CLAUDE_CODE_OVERVIEW.md)
   - [Hooks & Triggers](HOOKS_AND_TRIGGERS.md)
   - [Skill Rules Config](SKILL_RULES_CONFIG.md)
   - [Enforcement Levels](ENFORCEMENT_LEVELS.md)
   - [Testing Claude Code](TESTING_CLAUDE_CODE.md)
   - [Patterns Library](PATTERNS_LIBRARY.md)

2. Test with real examples
3. Iterate based on actual usage

---

**Status**: Complete ✅

Return to [main SKILL.md](../SKILL.md) for overview.
