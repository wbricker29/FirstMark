# Delivery Phase - Validating & Packaging

## Table of Contents

- [Delivery Phase - Validating \& Packaging](#delivery-phase---validating--packaging)
  - [Table of Contents](#table-of-contents)
  - [Purpose \& When to Use](#purpose--when-to-use)
  - [Step 4.5: Pre-Packaging Validation](#step-45-pre-packaging-validation)
    - [YAML Frontmatter](#yaml-frontmatter)
    - [File Structure](#file-structure)
    - [Content Quality](#content-quality)
    - [Testing](#testing)
  - [Step 5: Packaging a Skill](#step-5-packaging-a-skill)
  - [Step 6: Iteration](#step-6-iteration)

---

## Purpose & When to Use

Use this guide when:

- Preparing to package and distribute a skill
- Validating skill quality before release
- Iterating on an existing skill based on feedback

**Previous step:** [Implementation Phase](IMPLEMENTATION_PHASE.md)

---

## Step 4.5: Pre-Packaging Validation

Before packaging the skill, verify it meets quality standards using this checklist. The `package_skill.py` script automates many of these checks, but manual verification ensures nothing is missed.

### YAML Frontmatter

- [ ] Frontmatter starts with `---` and ends with `---`
- [ ] `name` field present (max 64 chars, lowercase-hyphens format)
- [ ] `description` field present (max 1024 chars)
- [ ] Description includes both "what it does" AND "when to use it"
- [ ] Description includes specific trigger words (file extensions, operations, user phrases)
- [ ] No YAML syntax errors (no tabs, proper formatting)

### File Structure

- [ ] SKILL.md exists in the skill directory
- [ ] Directory name matches the `name` field in frontmatter
- [ ] SKILL.md is under 500 lines (or content is split into reference files)
- [ ] Unused example files have been deleted (scripts/, references/, assets/)

### Content Quality

- [ ] Clear overview/purpose section exists
- [ ] Step-by-step instructions are provided where applicable
- [ ] At least 1-2 concrete examples included
- [ ] All scripts are referenced in SKILL.md with usage instructions
- [ ] All reference files are mentioned with when/how to use them
- [ ] All asset files are documented
- [ ] Writing uses imperative/infinitive form (not second person)

### Testing

- [ ] Skill validates successfully: `scripts/quick_validate.py <path/to/skill>`
- [ ] Scripts execute without errors (if included)
- [ ] Examples work as documented
- [ ] Test activation by using trigger words in a conversation

Once all checks pass, proceed to packaging.

---

## Step 5: Packaging a Skill

Once the skill is ready, it should be packaged into a distributable zip file that gets shared with the user. The packaging process automatically validates the skill first to ensure it meets all requirements:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory specification:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references

2. **Package** the skill if validation passes, creating a zip file named after the skill (e.g., `my-skill.zip`) that includes all files and maintains the proper directory structure for distribution.

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

---

## Step 6: Iteration

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Analyze execution and results
3. Notice relevant and important weaknesses
4. Identify how SKILL.md or bundled resources could be updated to directly address weaknesses
5. Select the most valuable update(s) that should be implemented
6. Implement changes and test again

**Key principle**: Iterate on evidence (skill doesn't activate, instructions unclear) not preference (different style).

---

**Status**: Delivery phase complete ✅

Return to [main SKILL.md](../SKILL.md) for overview.
