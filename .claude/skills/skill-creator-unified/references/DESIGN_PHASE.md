# Design Phase - Planning Your Skill

## Table of Contents

1. [Purpose & When to Use](#purpose--when-to-use)
2. [Step 1: Understanding with Concrete Examples](#step-1-understanding-with-concrete-examples)
3. [Step 2: Planning Reusable Contents](#step-2-planning-reusable-contents)
4. [What Skills Provide](#what-skills-provide)

---

## Purpose & When to Use

Use this guide when:
- Starting to design a new skill
- Understanding what the skill should do
- Planning bundled resources (scripts, references, assets)
- Gathering concrete examples of skill usage

**Next steps:** After design, proceed to [IMPLEMENTATION_PHASE.md](IMPLEMENTATION_PHASE.md)

---

## Step 1: Understanding with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

---

## Step 2: Planning Reusable Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

**Example: `pdf-editor` skill** - When handling queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

**Example: `frontend-webapp-builder` skill** - For queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

**Example: `big-query` skill** - When handling queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

---

## What Skills Provide

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### Four Types of Skill Resources

**1. Specialized workflows** - Multi-step procedures for specific domains
   - Example: Multi-stage document processing workflows, data analysis pipelines
   - When to use: Repetitive complex tasks with clear procedural steps
   - Benefit: Ensures consistent execution of complex processes

**2. Tool integrations** - Instructions for working with specific file formats or APIs
   - Example: PDF manipulation, Excel analysis, API client libraries
   - When to use: Deterministic operations on specific file types or services
   - Benefit: Provides domain-specific knowledge about tools and formats

**3. Domain expertise** - Company-specific knowledge, schemas, business logic
   - Example: Database schemas, brand guidelines, compliance rules
   - When to use: Contextual knowledge that varies by organization
   - Benefit: Encodes organizational knowledge for reuse

**4. Bundled resources** - Scripts, references, and assets for complex tasks
   - Example: Boilerplate templates, validation scripts, reference documentation
   - When to use: Reusable code/content used repeatedly
   - Benefit: Avoids rewriting the same code or recreating the same content

---

**Status**: Design phase complete → Proceed to [Implementation Phase](IMPLEMENTATION_PHASE.md)
