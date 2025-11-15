# Implementation Phase - Writing Your Skill

## Table of Contents

1. [Purpose & When to Use](#purpose--when-to-use)
2. [Step 3: Initializing the Skill](#step-3-initializing-the-skill)
3. [YAML Frontmatter Specification](#yaml-frontmatter-specification)
4. [Making Skills Discoverable](#making-skills-discoverable)
5. [Bundled Resources Guide](#bundled-resources-guide)
6. [Step 4: Editing the Skill](#step-4-editing-the-skill)
7. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## Purpose & When to Use

Use this guide when:
- Initializing a new skill directory
- Writing SKILL.md content
- Configuring YAML frontmatter
- Organizing scripts, references, and assets
- Ensuring discoverability

**Previous step:** [Design Phase](DESIGN_PHASE.md)
**Next step:** [Delivery Phase](DELIVERY_PHASE.md)

---

## Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

**Usage:**

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

**The script:**

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

---

## YAML Frontmatter Specification

Every SKILL.md must begin with valid YAML frontmatter enclosed by `---` delimiters.

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

### Required Fields

**name** (required)
- Type: String
- Max length: 64 characters
- Format: lowercase-with-hyphens (e.g., `my-skill-name`)
- Must match the directory name
- Example: `pdf-editor`, `brand-guidelines`, `sql-query-helper`

**description** (required)
- Type: String
- Max length: 1024 characters
- Must include BOTH what the skill does AND when to use it
- Use third-person language (e.g., "This skill should be used when...")
- See "Making Skills Discoverable" section below for optimization guidance

### Example Valid Frontmatter

```yaml
---
name: pdf-editor
description: Provides tools and scripts for editing PDF files including rotation, merging, splitting, and form filling. This skill should be used when working with PDF files or when users request PDF manipulation tasks.
---
```

### Common YAML Syntax Errors to Avoid

- Missing opening or closing `---` delimiters
- Using tabs instead of spaces for indentation
- Missing required fields (`name` or `description`)
- Name exceeds 64 characters or uses invalid format
- Description exceeds 1024 characters
- Unescaped special characters in description (use quotes if needed)

---

## Making Skills Discoverable

The `description` field is critical for skill activation. Claude uses the description to determine when to load and use the skill. A well-crafted description ensures the skill activates at the right time.

### Description Formula

`[What it does] + [When to use it] + [Key trigger words]`

### Good Description Examples

```
Extract text and tables from PDF files, fill forms, merge and split documents.
This skill should be used when working with PDF files or when users mention
PDFs, forms, or document manipulation.
```

```
Analyze Excel spreadsheets, create pivot tables, and generate charts. This
skill should be used when working with .xlsx files, analyzing tabular data,
or creating data visualizations.
```

### Tips for Discoverability

1. **Include specific file extensions** - `.pdf`, `.xlsx`, `.json`, `.csv`
2. **Mention common user phrases** - "analyze", "extract", "generate", "convert"
3. **List concrete operations** - Not just "helps with documents" but "merge, split, rotate, fill forms"
4. **Add context clues** - "Use when...", "For...", "When users mention..."
5. **Front-load keywords** - Place the most important trigger words in the first 200 characters
6. **Be specific, not generic** - "PDF manipulation" not "document processing"

### Poor Description Example

```
Helps with documents and files. Use when needed.
```

Why it's poor: Too vague, no trigger words, no file types, no specific operations.

---

## Bundled Resources Guide

Skills can include three types of bundled resources to support complex workflows.

### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

### Progressive Disclosure Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited*)

*Unlimited because scripts can be executed without reading into context window.

---

## Step 4: Editing the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should Claude use the skill? All reusable skill contents developed above should be referenced so that Claude knows how to use them.

---

## Common Mistakes to Avoid

When creating skills, avoid these anti-patterns that reduce effectiveness:

### ❌ Narrative Examples

```
Bad: "In session 2025-10-03, we found that when projectDir was empty it caused..."
```

**Why:** Too specific to one instance, not reusable across different contexts.
**Better:** Use generic examples that illustrate the pattern, not specific session narratives.

### ❌ Multi-Language Dilution

```
Bad: Including example-js.js, example-py.py, example-go.go for the same functionality
```

**Why:** Spreading effort across multiple languages results in mediocre quality and maintenance burden.
**Better:** Provide one excellent, well-tested example in the most relevant language for the domain.

### ❌ Code in Flowcharts

```
Bad: Flowchart nodes containing actual code snippets
```

**Why:** Users can't copy-paste code from diagrams, making them less useful.
**Better:** Use flowcharts for logic flow only, put actual code in markdown code blocks.

### ❌ Generic Labels

```
Bad: helper1, helper2, step3, utils
```

**Why:** Labels should convey semantic meaning for clarity.
**Better:** validate_input, process_data, format_output, parse_configuration

### ❌ Overly Broad Descriptions

```
Bad: "Helps with documents" or "Useful for data processing"
```

**Why:** Too vague to trigger appropriately, won't activate when needed.
**Better:** Specific operations and file types (see "Making Skills Discoverable" section).

---

**Status**: Implementation complete → Proceed to [Delivery Phase](DELIVERY_PHASE.md)
