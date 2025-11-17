---
name: skill-creator-unified
description: Guide for creating skills that extend Claude's capabilities. Use when creating new skills, updating existing skills, understanding skill structure, YAML frontmatter, bundled resources (scripts/references/assets), validation, or packaging. For Claude Code: covers hooks, triggers, skill-rules.json, enforcement levels, and testing. Includes design, implementation, and delivery phases.
---

# Skill Creator (Unified)

Create effective skills that extend Claude's capabilities - general-purpose or Claude Code-specific.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

See [DESIGN_PHASE.md](references/DESIGN_PHASE.md#what-skills-provide) for detailed explanations of each type.

---

## Skill Anatomy

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/          - Executable code
    ├── references/       - Documentation for context
    └── assets/           - Files used in output
```

**YAML Frontmatter**: Required metadata (name + description) that determines when Claude uses the skill. See [IMPLEMENTATION_PHASE.md - YAML Specification](references/IMPLEMENTATION_PHASE.md#yaml-frontmatter-specification) for complete details.

**Bundled Resources**: Optional directories for scripts, references, and assets. See [IMPLEMENTATION_PHASE.md - Bundled Resources](references/IMPLEMENTATION_PHASE.md#bundled-resources-guide) for when and how to use each.

---

## Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, ideally <500 lines)
3. **Bundled resources** - As needed by Claude

**Key principle**: Keep SKILL.md lean (<500 lines). Move detailed content to `references/` files.

---

## Choose Your Path

Use this decision matrix to determine which type of skill to create:

| Aspect | General Skills | Claude Code Skills |
|--------|----------------|-------------------|
| **Use when** | Portable workflows, manual invocation acceptable | Need auto-activation, guardrails, or enforcement |
| **Works in** | All Claude environments (Desktop, CLI, API) | Claude Code only |
| **Setup complexity** | Simple (YAML only) | Advanced (YAML + skill-rules.json) |
| **Auto-triggers** | ❌ Manual invocation | ✅ Keywords, files, content |
| **Can block edits** | ❌ No enforcement | ✅ Guardrails (critical only) |
| **Session tracking** | ❌ Not applicable | ✅ Skip after first use |
| **Testing tools** | Basic validation | Advanced (hook testing, troubleshooting) |

### Path A: General Skills

**Best for:**

- PDF processing, data analysis, API integration
- Skills that work across all Claude environments
- Simple, portable workflows
- Manual invocation is acceptable

**Characteristics:**

- ✅ Portable - works everywhere
- ✅ Simple setup - YAML frontmatter only
- ✅ Easy to maintain
- ❌ No auto-activation

**Start here**: [Design Phase](references/DESIGN_PHASE.md) → Follow 6-step process

---

### Path B: Claude Code Skills with Auto-Activation

**Best for:**

- Database schema verification (blocks edits until verified)
- Error handling enforcement (suggests patterns)
- Framework-specific guides (auto-activates for .tsx files)
- Technology-specific best practices (triggers on keywords)

**Characteristics:**

- ✅ Auto-activation based on triggers
- ✅ Can enforce guardrails (blocking)
- ✅ Session tracking and skip conditions
- ✅ Advanced testing and troubleshooting
- ⚠️ Claude Code only
- ⚠️ More complex configuration

**Start here**: [Design Phase](references/DESIGN_PHASE.md) → [Claude Code Overview](references/CLAUDE_CODE_OVERVIEW.md) → Follow 6-step process

---

**Not sure?** Start with **General** (Path A). You can always migrate to Claude Code later. See [Migration Guide](references/CLAUDE_CODE_OVERVIEW.md#migration-guide).

---

## The 6-Step Process

Follow these steps in order for both General and Claude Code skills:

### Design Phase (Planning)

**Step 1: Understand** - Gather concrete examples of how the skill will be used

- List 3+ real prompts that should activate this skill
- Define what should NOT trigger it (edge cases)
- Determine success criteria

**Step 2: Plan** - Identify scripts, references, and assets to include

- What executable code is needed? (scripts/)
- What documentation aids understanding? (references/)
- What files are used in output? (assets/)

📖 **Detailed guide**: [Design Phase](references/DESIGN_PHASE.md)

---

### Implementation Phase (Writing)

**Step 3: Initialize** - Create skill directory using initialization script

**Initialize skill directory:**

```bash
uv run python scripts/init_skill.py my-skill --path ./
```

This creates:

- SKILL.md with proper YAML frontmatter template
- references/ directory with example documentation
- scripts/ directory with example script
- assets/ directory with example asset

**Note**: Claude Code-specific templates (skill-rules.json) must be created manually after initialization. See [Skill Rules Config](references/SKILL_RULES_CONFIG.md) for templates.

---

**Step 4: Edit** - Write SKILL.md, configure YAML, organize resources

**For General skills:**

1. Edit SKILL.md with your content (<500 lines)
2. Fill in YAML frontmatter (name + description)
3. Add bundled resources (scripts, references, assets)
4. Link to reference files from SKILL.md

**For Claude Code skills (additional steps):**

1. Configure skill-rules.json with triggers and enforcement
2. Define trigger patterns (keywords, intent, file paths, content)
3. Set enforcement level (block, suggest, warn)
4. Configure skip conditions (session tracking, file markers, env vars)

📖 **Detailed guides**:

- [Implementation Phase](references/IMPLEMENTATION_PHASE.md) - Universal SKILL.md writing
- [Claude Code Overview](references/CLAUDE_CODE_OVERVIEW.md) - When to use Claude Code features
- [Hooks & Triggers](references/HOOKS_AND_TRIGGERS.md) - How auto-activation works
- [Skill Rules Config](references/SKILL_RULES_CONFIG.md) - skill-rules.json schema
- [Enforcement Levels](references/ENFORCEMENT_LEVELS.md) - Block, suggest, warn

---

### Delivery Phase (Shipping)

**Step 5: Validate** - Check quality standards, run validation script

```bash
# Validates both general and Claude Code skills
uv run python scripts/quick_validate.py path/to/my-skill
```

Checks:

- YAML frontmatter format and required fields
- Skill naming conventions and directory structure
- Description completeness (trigger keywords for Claude Code)
- File organization and resource references
- Line count compliance (<500 lines for SKILL.md)
- For Claude Code: skill-rules.json validation

**For Claude Code skills (additional testing):**

```bash
# Test trigger activation manually
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

📖 **Detailed guides**:

- [Delivery Phase](references/DELIVERY_PHASE.md) - Validation checklist
- [Testing Claude Code](references/TESTING_CLAUDE_CODE.md) - Hook testing, troubleshooting

---

**Step 6: Package** - Create distributable zip file, iterate based on feedback

```bash
# Creates my-skill.zip in current directory
uv run python scripts/package_skill.py path/to/my-skill

# Specify output directory
uv run python scripts/package_skill.py path/to/my-skill ./dist
```

The packaging script:

1. Validates the skill automatically
2. Creates a zip file with proper structure
3. Ready for distribution or installation

📖 **Detailed guide**: [Delivery Phase - Packaging](references/DELIVERY_PHASE.md#step-5-packaging-a-skill)

---

## Reference Guide Directory

### Universal References (Both Paths)

**[Design Phase](references/DESIGN_PHASE.md)** - Use when:

- Starting a new skill
- Unclear what the skill should include
- Planning bundled resources
- Understanding skill purpose

**[Implementation Phase](references/IMPLEMENTATION_PHASE.md)** - Use when:

- Writing SKILL.md content
- Configuring YAML frontmatter
- Making skills discoverable
- Organizing scripts/references/assets
- Need writing guidelines

**[Delivery Phase](references/DELIVERY_PHASE.md)** - Use when:

- Validating before release
- Packaging for distribution
- Iterating on existing skill
- Quality assurance needed

---

### Claude Code Specific References (Path B)

**[Claude Code Overview](references/CLAUDE_CODE_OVERVIEW.md)** - Start here for Claude Code skills:

- When to use Claude Code features vs general skills
- System architecture (two-hook system)
- Skill types (guardrail vs domain)
- Migration guide (general → Claude Code)

**[Hooks & Triggers](references/HOOKS_AND_TRIGGERS.md)** - Auto-activation system:

- Hook mechanisms (UserPromptSubmit, PreToolUse, Stop)
- Trigger types (keywords, intent patterns, file paths, content patterns)
- How Claude Code detects when to activate skills
- Performance considerations

**[Skill Rules Config](references/SKILL_RULES_CONFIG.md)** - Configuration schema:

- Complete skill-rules.json specification
- Field explanations and examples
- Configuration templates
- JSON validation

**[Enforcement Levels](references/ENFORCEMENT_LEVELS.md)** - Control how skills activate:

- BLOCK: Critical guardrails (prevents edits)
- SUGGEST: Proactive guidance (advisory)
- WARN: Optional reminders (low priority)
- Guardrail vs Domain skill patterns
- Skip conditions (session tracking, file markers, env vars)

**[Testing Claude Code](references/TESTING_CLAUDE_CODE.md)** - Testing & troubleshooting:

- Manual hook testing commands
- Debugging activation issues (not triggering, false positives)
- Testing checklist (19 validation points)
- Performance testing
- Troubleshooting common problems

**[Patterns Library](references/PATTERNS_LIBRARY.md)** - Copy-paste examples:

- Keyword patterns for common use cases
- Intent regex patterns (implicit action detection)
- File path glob patterns
- Content detection regex
- Complete skill-rules.json examples

---

## Scripts

This skill includes helper scripts that work for both general and Claude Code skills:

### scripts/init_skill.py - Initialize New Skill

Create a new skill directory with proper structure and templates:

```bash
uv run python scripts/init_skill.py my-skill --path ./
```

**Required:**

- `--path <directory>` - Specify output directory for the skill

**Future enhancement**: `--claude-code` flag will generate skill-rules.json template automatically. Currently, create skill-rules.json manually using templates in [Skill Rules Config](references/SKILL_RULES_CONFIG.md).

Creates:

- SKILL.md with proper YAML frontmatter template
- references/ directory with example documentation
- scripts/ directory with example script
- assets/ directory with example asset

---

### scripts/quick_validate.py - Validate Skill Structure

Validates YAML frontmatter, structure, and quality standards:

```bash
uv run python scripts/quick_validate.py path/to/my-skill
```

Checks:

- YAML frontmatter syntax and required fields
- Naming conventions (lowercase-hyphens)
- Description completeness
- Line count (<500 lines for SKILL.md)
- File organization
- Resource references
- For Claude Code: skill-rules.json syntax and schema

---

### scripts/package_skill.py - Package for Distribution

Creates distributable zip file with automatic validation:

```bash
# Default: creates my-skill.zip in current directory
uv run python scripts/package_skill.py path/to/my-skill

# Specify output directory
uv run python scripts/package_skill.py path/to/my-skill ./dist
```

The script:

1. Runs validation automatically
2. Creates zip file with proper directory structure
3. Reports any errors before packaging
4. Ready for distribution or installation

---

## Common Questions

See [FAQ.md](references/FAQ.md) for comprehensive answers to:

- Should I create general or Claude Code skill?
- How do I make my skill discoverable?
- What goes in scripts/ vs references/ vs assets/?
- When should I use BLOCK vs SUGGEST enforcement?
- How do I debug activation issues?
- Can I migrate from general to Claude Code?
- And more...

---

## Quick Reference Summary

### Create New Skill (6 Steps)

1. **Understand** - Gather 3+ concrete use case examples
2. **Plan** - Identify scripts, references, assets needed
3. **Initialize** - Run init script: `uv run python scripts/init_skill.py my-skill --path ./`
4. **Edit** - Write SKILL.md, configure YAML (+ skill-rules.json for Claude Code)
5. **Validate** - Run validation script + test triggers (Claude Code)
6. **Package** - Create distributable zip file

### Best Practices

✅ **500-line rule**: Keep SKILL.md under 500 lines
✅ **Progressive disclosure**: Move details to references/
✅ **Rich descriptions**: Include all trigger keywords (max 1024 chars)
✅ **Test first**: Build 3+ evaluations before extensive documentation
✅ **Imperative writing**: Use "Create X" not "You should create X"
✅ **Table of contents**: Add to reference files > 100 lines

### Path Selection

- **General**: Portable, simple, manually invoked
- **Claude Code**: Auto-activation, guardrails, testing

Start general, migrate to Claude Code if needed.

---

## Next Steps

**Ready to create a skill?**

1. **Choose your path**: General or Claude Code (see [Choose Your Path](#choose-your-path))
2. **Start with Design Phase**: [Design Phase](references/DESIGN_PHASE.md)
3. **For Claude Code**: Also read [Claude Code Overview](references/CLAUDE_CODE_OVERVIEW.md)
4. **Initialize your skill**: Run `uv run python scripts/init_skill.py my-skill --path ./`

---

**Skill Status**: Complete ✅
**Line Count**: < 500 (following 500-line rule) ✅
**Progressive Disclosure**: Universal + Claude Code references ✅
**Mode Support**: General + Claude Code with auto-activation ✅
