# AIdev Commands Reference

## Table of Contents

- [/constitution](#constitution)
- [/prd](#prd)
- [/spec](#spec)
- [/new SLUG](#new-slug)
- [/plan SLUG](#plan-slug)
- [/work SLUG TK-##](#work-slug-tk-)
- [/check [SLUG]](#check-slug)
- [/verify SLUG](#verify-slug)
- [/reflect](#reflect)
- [/update DOCUMENT PATH](#update-document-path)
- [Command Sequence Summary](#command-sequence-summary)
- [Notes on Command Evolution](#notes-on-command-evolution)

---

## /constitution

### Purpose
Create or update project governance. Establishes non-negotiable principles, quality bars, and constraints that guide all development work.

### When to Use
- **First-time project setup**: Starting a new codebase and need to establish foundational rules
- **Tech stack changes**: Migrating from REST to GraphQL, adopting a new framework, or changing deployment platforms
- **Quality standard evolution**: Team learns better practices and needs to codify them (e.g., adopting strict TypeScript after encountering too many runtime errors)
- **Post-incident governance**: After a production issue reveals missing constraints (e.g., "All DB queries must have timeouts")
- **Team scaling**: Growing from solo to team development and need explicit decision rights

### Why It Works This Way
The constitution serves as the foundation for all technical and product decisions, ensuring consistency and alignment across features. Implicit standards don't scale—when principles live in someone's head, they get lost in code reviews, violated under pressure, and cause inconsistent decisions. By codifying governance upfront, we create enforcement points that catch violations early—before they become production incidents.

The constitution is intentionally hard to change (requires strong evidence of ≥2 violations) because stability matters. If principles shift constantly, teams lose confidence and revert to "just ship it" mode. The constitution should reflect lessons learned, not aspirational thinking.

The structure (principles + quality bars + constraints + decision rights) covers the four dimensions of governance: "how we think" (principles), "what good looks like" (quality bars), "what we can't do" (constraints), and "who decides" (decision rights). This prevents gaps where someone says "I didn't know who could approve that."

### Usage
```bash
/constitution
```

### Process Overview
1. Load template from `.claude/skills/aidev-workflow/assets/templates/CONSTITUTION-TEMPLATE.md`
2. Gather information through structured prompts
3. Generate `specs/constitution.md` with YAML frontmatter
4. Validate completeness and required sections
5. Display summary and confirm with user

### Output
Creates `specs/constitution.md` with:
- Architecture principles (name, rule, rationale, examples)
- Quality bars (coverage target, typing requirements, linting, performance targets)
- Constraints (runtime requirements, security, dependency management)
- Decision rights (who owns what decisions)

### Examples

#### Example 1: New Next.js Project with Strict TypeScript
**Context**: Starting a greenfield Next.js app, team has been burned by runtime type errors before.

**Execution**:
```bash
/constitution
```

**Prompts and Responses**:
- "What architecture principles should guide development?"
  - "Strict TypeScript: No `any` types except for untyped library interfaces"
  - "Server-first: Default to Server Components, use Client Components only when needed"
  - "Sufficiency over assumptions: Ask questions early rather than fill gaps with guesses"

- "What quality bars should all code meet?"
  - Coverage: ≥80% on modified modules (measured via Vitest)
  - Type checking: Must pass `tsc --noEmit` with strict mode
  - Linting: Zero ESLint errors (warnings OK during dev)
  - Performance: <3s time to first byte on all pages

- "What constraints must be respected?"
  - Runtime: Node.js ≥18, deployed to Vercel
  - Security: All secrets in environment variables (never committed)
  - Dependencies: Only approved packages (React 19, Next.js 15, TypeScript 5+)

- "Who has decision rights?"
  - Architecture: Tech lead approves, documents in spec.md
  - Features: Product owner prioritizes, documents in PRD.md
  - Implementation: Engineers own within established patterns

**Result**: `specs/constitution.md` created with version 1.0.0, establishes guardrails that prevent common mistakes.

#### Example 2: Post-Incident Governance Update
**Context**: Production incident caused by missing DB query timeout. Need to add constraint.

**Execution**:
```bash
/constitution
```

**Prompt**: "Add constraint: All database queries must have explicit timeout (≤5s default, document if higher)"

**Result**: Constitution updated to v1.1.0, now `/work` and `/verify` commands enforce timeout checks.

### Troubleshooting

#### Issue 1: "My team keeps violating principles"
**Solution**: Principles may be too aspirational or not measurable. Update quality bars to include automated checks (e.g., "No `any` types" → add ESLint rule). Move from "we should" to "we must, and here's how we verify."

#### Issue 2: "Constitution is too long and nobody reads it"
**Solution**: Keep it focused. Aim for 5-7 principles, 4-6 quality bars, 3-5 constraints. If it's longer, you're documenting implementation details (those belong in spec.md).

#### Issue 3: "When do I update the constitution?"
**Solution**: Only when you have evidence (≥2 instances) that the current version is wrong or incomplete. One-off issues don't warrant governance changes. Look for patterns.

#### Issue 4: "What if constitution conflicts with PRD requirements?"
**Solution**: Constitution wins. It's non-negotiable governance. If PRD asks for something that violates constitution (e.g., "store passwords in localStorage"), reject it or update constitution with strong justification.

#### Issue 5: "Template not found"
**Solution**: Check that `.claude/skills/aidev-workflow/assets/templates/CONSTITUTION-TEMPLATE.md` exists. If missing, ensure the aidev-workflow skill is properly installed with its assets directory.

### Integration
- **Runs first**: Before `/prd` and `/spec` to establish governance baseline
- **Informs /spec**: Architecture principles guide interface design and module structure
- **Enforces /work**: Quality bars become verification gates in `/work` and `/verify`
- **Blocks /update**: Constitution changes cascade to all dependent documents (plan.md verification sections update automatically)

---

## /prd

### Purpose
Create or update product requirements document. Defines the problem, audience, outcomes, scope, and success metrics for the project.

### When to Use
- **Initial project planning**: Right after `/constitution`, before any features are built
- **Feature expansion**: Adding major new capabilities to an existing project (e.g., adding authentication to a content site)
- **Requirement changes**: Stakeholder needs shift, market feedback changes direction
- **Scope clarification**: Team disagrees on what's in/out of scope and needs written record
- **Success metric definition**: Need measurable goals before writing code

### Why It Works This Way
The PRD answers "what problem are we solving and how do we know if we succeeded?" before anyone writes code. This document drives all subsequent technical decisions and implementation work, preventing the common failure mode of building the wrong thing well—where teams ship polished features that don't move the needle.

The structure focuses on outcomes over outputs because "shipped login page" (output) doesn't guarantee "users can authenticate" (outcome). Measurable success metrics force clarity: "improve performance" is vague, "reduce time-to-first-byte to <3s for 95th percentile" is testable.

The PRD intentionally excludes "how" (no technical decisions) because that's the spec's job. This separation lets product and engineering have different rates of change. Requirements stabilize while implementation evolves. If the PRD says "use PostgreSQL" instead of "need persistent storage," you've coupled product to implementation.

Reference-based Part B (linking to plan.md instead of duplicating it) eliminates maintenance overhead. Early versions duplicated task summaries in PRD, causing drift when tasks changed. Now PRD stays stable, references stay current.

### Usage
```bash
/prd
```

### Process Overview
1. Load template from `.claude/skills/aidev-workflow/assets/templates/PRD-TEMPLATE.md`
2. Gather problem definition, outcomes, success metrics through prompts
3. Define scope (what IS and what is NOT included)
4. Create acceptance criteria in Given-When-Then format
5. Generate `specs/PRD.md` with all gathered information
6. Validate structure and completeness
7. Display summary and next steps

### Output
Creates `specs/PRD.md` with:
- **Problem Definition**: Problem statement, target audience, impact
- **Desired Outcomes**: Primary and secondary outcomes (measurable)
- **Success Metrics**: Metric name, target value, measurement method
- **Scope**: What IS in scope, what is NOT in scope
- **Acceptance Criteria**: Given-When-Then format with IDs (AC-PRD-01, AC-PRD-02, etc.)
- **Roadmap**: Key milestones with dates and deliverables
- **Assumptions & Risks**: Assumptions, risks with likelihood/impact/mitigation

Optional (Expanded PRD variant):
- **Feature Inventory**: Link-first one-line-per-feature table (no task lists). Status tags and effort ranges acceptable. Numbers must be derived from automation (state.json) and dated.
- **Current Project State**: Short narrative plus links to `.claude/logs/state.json`, `/status`, and `/check` for live metrics.
- **Critical Path**: Bulleted blockers with links to unit `plan.md` and evidence reports.
- **Document Hierarchy**: Brief orientation showing relationships between PRD/spec/design/plan.

### Examples

#### Example 1: Digital Portfolio with AI Chatbot
**Context**: Building a portfolio site that lets visitors ask questions about your professional experience.

**Execution**:
```bash
/prd
```

**Prompts and Responses**:
- "What problem are you solving?"
  - Problem: Recruiters want to learn about my background but don't want to read long resumes
  - Target audience: Technical recruiters, hiring managers, potential collaborators
  - Impact: Increase interview conversion by making experience discoverable

- "What are the desired outcomes?"
  - Primary: Visitors can ask natural language questions and get accurate answers about my experience
  - Secondary: Responses cite specific projects/roles, chatbot feels professional (not a personal clone)

- "What success metrics will you measure?"
  - Chat engagement: ≥30% of visitors ask at least one question (measured via analytics)
  - Response quality: ≥90% of queries get relevant answers (measured via manual review of 100 sample queries)
  - Performance: <3s streaming start time (measured via Vercel metrics)

- "What is IN scope and what is OUT of scope?"
  - IN: Hero section, project showcase, AI chat interface, RAG pipeline with resume content
  - OUT: Blog, CMS, real-time collaboration, multiple language support, user accounts

- "What are the acceptance criteria?"
  - AC-PRD-01: Given a visitor opens the site, When they view the hero section, Then they see name, tagline, and call-to-action
  - AC-PRD-02: Given a visitor asks a question in chat, When the query relates to experience, Then the response cites specific projects/roles from resume
  - AC-PRD-03: Given 100 test queries, When evaluated for relevance, Then ≥90 have accurate answers

**Result**: `specs/PRD.md` created with version 1.0.0, provides clear target for engineering work. Team can now create spec.md with technical contracts.

#### Example 2: Adding Authentication to Existing App
**Context**: Current app is public, now need user accounts for personalized features.

**Execution**:
```bash
/prd
```

**Update Focus**: Add authentication requirements to existing PRD

**New Content**:
- Outcome: Users can create accounts and log in securely
- Metric: ≥95% of login attempts succeed within 2s (measured via Supabase logs)
- Scope IN: Email/password auth, session management, password reset
- Scope OUT: OAuth (Google/GitHub), 2FA, account deletion (future phases)

**Result**: PRD updated to v1.1.0, now includes auth requirements alongside original portfolio features.

### Troubleshooting

#### Issue 1: "PRD is too technical (mentions databases, APIs)"
**Solution**: Move technical decisions to spec.md. PRD should say "users need persistent storage" not "use PostgreSQL." Focus on capabilities, not implementation.

#### Issue 2: "Success metrics are vague or unmeasurable"
**Solution**: Every metric needs three parts: what to measure, target value, measurement method. "Improve performance" → "Reduce TTFB to <3s (measured via Vercel analytics)."

#### Issue 3: "Scope keeps expanding during development"
**Solution**: Use scope's OUT section explicitly. When stakeholders request new features, add them to OUT with note "future phase" or update PRD version with clear rationale.

#### Issue 4: "Acceptance criteria overlap with unit tests"
**Solution**: PRD criteria are user-facing (AC-PRD-01: "User can log in"). Unit design.md criteria are feature-specific (AC-003: "Invalid email shows error message"). Different granularity.

#### Issue 5: "PRD Part B is out of sync with plan.md"
**Solution**: Default to the reference-based approach—link to `plan.md` instead of duplicating tasks. If using the optional expanded PRD, keep it link-first with one-line feature summaries and clearly mark any counts/percentages as "derived from state.json (as of YYYY-MM-DD)". Example: "See specs/units/003-authentication/plan.md for implementation details."

### Integration
- **Runs after /constitution**: Constitution defines governance, PRD defines product goals
- **Informs /spec**: Technical architecture should support PRD outcomes
- **Guides /new**: Each feature unit should trace to PRD outcomes and acceptance criteria
- **Validated by /check**: Checks that spec.md aligns with PRD requirements (no orphaned features)

---

## /spec

### Purpose
Create engineering contract. Defines architecture, interfaces, data models, and non-functional requirements. This is the technical contract between product (PRD) and implementation.

### When to Use
- **After /constitution and /prd**: Foundation documents must exist first
- **Before implementing features**: Establishes contracts that features will reference
- **Architecture refactoring**: When changing from monolith to modules, or adopting new patterns
- **Interface documentation**: Team needs explicit contracts for API boundaries
- **Performance baseline**: When NFRs need measurable targets before optimization

### Why It Works This Way
The spec is where "what" (from PRD) becomes "how" (interfaces and architecture), ensuring technical decisions align with product goals and constitutional principles. Without explicit contracts, teams build incompatible pieces: authentication expects user IDs as strings, database uses integers, chaos ensues.

Interface contracts (inputs, outputs, errors, pre/postconditions) prevent integration failures. When a contract says `parse_document(file_path: str) -> Document | ParseError`, both sides know the deal. No "I thought it returned null on failure" surprises.

The spec lives between PRD and code because it changes at a different rate. PRD is stable (requirements don't shift daily), code is volatile (refactoring is constant), spec is semi-stable (interfaces change when architecture changes). Separating them prevents cascade failures where a variable rename forces PRD updates.

Smart defaults (detecting Next.js and suggesting Server Component patterns) reduce boilerplate. The command reads package.json and tsconfig.json to infer stack, then prompts with context-appropriate suggestions.

### Usage
```bash
/spec
```

### Process Overview
1. Validate prerequisites (constitution.md and PRD.md exist)
2. Detect project stack by analyzing codebase
3. Load template and gather architecture decisions
4. Define interfaces with complete contracts
5. Document data model entities and relationships
6. Specify measurable non-functional requirements
7. Generate `specs/spec.md` with all technical contracts
8. Validate completeness and confirm with user

### Output
Creates `specs/spec.md` with:
- **Architecture**: Pattern (ports-and-adapters, layered, etc.), module definitions, rationale
- **Data Flow**: Step-by-step flow through the system
- **Interface Contracts**: For each interface—name, module, inputs (type/constraints), outputs, errors, pre/postconditions
- **Data Model**: Entities with fields (name, type, constraints), relationships
- **Non-Functional Requirements**: Performance, reliability, observability, security (all measurable)

### Examples

#### Example 1: RAG Pipeline Specification
**Context**: Building AI chatbot that answers questions using resume content. Need to define interfaces before implementation.

**Execution**:
```bash
/spec
```

**Prompts and Responses**:
- "What architecture pattern will you use?"
  - Pattern: Ports-and-adapters (hexagonal)
  - Rationale: Isolate AI/vector logic from Next.js, makes testing easier
  - Modules: `app` (Next.js), `lib/rag` (vector search), `lib/ai` (OpenAI), `lib/db` (Supabase)

- "What is the data flow?"
  - User submits query → embed query → vector search → augment prompt → stream response → display

- "What interfaces will features reference?"
  - `embed_text(text: string): Promise<number[]>` — Generate embedding vector (1536 dimensions)
  - `search_vectors(embedding: number[], limit: number): Promise<Chunk[]>` — Find similar content
  - `generate_response(prompt: string, context: string): Promise<Stream>` — Stream AI response

- "What are the data model entities?"
  - `Document`: id (uuid), content (text), embedding (vector(1536)), metadata (jsonb)
  - `Chunk`: section of document with metadata (source file, line numbers)

- "What non-functional requirements must be met?"
  - Performance: <3s streaming start, <50ms vector search (p95)
  - Reliability: Retry OpenAI calls 3x with exponential backoff
  - Observability: Log all query embeddings and retrieved chunks
  - Security: API keys in env vars, Supabase RLS enabled

**Result**: `specs/spec.md` created with version 1.0.0. Now `/new` commands can reference `embed_text` and `search_vectors` interfaces.

#### Example 2: Authentication Spec Addition
**Context**: Existing spec has content pipeline, now adding user authentication.

**Execution**:
```bash
/spec
```

**Update Focus**: Add auth interfaces to existing spec

**New Interfaces**:
```typescript
interface AuthService {
  login(email: string, password: string): Promise<Session | AuthError>
  logout(sessionId: string): Promise<void>
  // Precondition: email format valid, password ≥8 characters
  // Postcondition: Session created with expiry, user authenticated
}
```

**New Entities**:
- `User`: id, email, password_hash, created_at
- `Session`: id, user_id, token, expires_at

**Result**: Spec updated to v1.1.0, now includes auth contracts. Feature designs can reference `AuthService.login()`.

### Troubleshooting

#### Issue 1: "Interfaces have no error handling defined"
**Solution**: Every interface must list possible errors. `search_vectors` should specify: `VectorSearchError` (query failed), `EmbeddingDimensionError` (wrong size), `TimeoutError` (>5s). This prevents "why did it crash" debugging.

#### Issue 2: "Data model is too detailed (includes indexes, constraints)"
**Solution**: Spec defines logical model (entities, fields, relationships). Database migrations define physical model (indexes, FK constraints). Keep spec focused on "what" not "how."

#### Issue 3: "NFRs are not measurable"
**Solution**: Every NFR needs measurement method. "Fast queries" → "<50ms p95 (measured via Supabase logs)." If you can't measure it, you can't verify it.

#### Issue 4: "Features reference interfaces not in spec"
**Solution**: Run `/check` to detect drift. If feature design references `process_csv` but spec doesn't define it, either add to spec or fix design. Spec is source of truth for interfaces.

#### Issue 5: "Spec is too long (>500 lines)"
**Solution**: You're likely documenting implementation, not contracts. Spec defines interfaces, not how they're implemented. Move implementation details to feature design.md files.

### Integration
- **Runs after /constitution and /prd**: Requires governance and requirements to exist
- **Informs /new**: Feature designs reference spec interfaces and entities
- **Validated by /check**: Detects when code implements interfaces not in spec (drift)
- **Updated via /update**: When interfaces change, `/update` propagates to dependent features

---

## /new SLUG

### Purpose
Initialize a new unit of work (feature) with a design document that captures stable intent and acceptance criteria.

### When to Use
- **Starting a new feature**: After spec.md is complete, before writing code
- **Breaking down large features**: Split "authentication" into units like "login", "password-reset", "session-management"
- **Establishing feature contracts**: Need clear acceptance criteria before implementation
- **Documenting feature scope**: Team needs agreement on what this feature includes/excludes
- **Setting success metrics**: Define measurable outcomes for feature completion

### Why It Works This Way
Design documents are stable intent while plans are volatile execution. Separating them prevents feature drift—when "add login" becomes "add login plus OAuth plus 2FA plus password policies" mid-implementation.

The design references spec.md interfaces/entities instead of defining new ones. This forces consistency: if design needs a new interface, update spec.md first. Prevents per-feature proliferation of incompatible contracts.

Acceptance criteria in Given-When-Then format are testable. "User can log in" is vague; "Given valid credentials, When user submits login form, Then session created and dashboard displayed" is a test case. This makes `/verify` possible.

Sequential unit numbers (001, 002, 003) create order without dates. Units can be implemented in any sequence (dependencies control order), but numbers provide stable references. Feature "003-authentication" doesn't become "2024-01-15-authentication" when you rename the branch.

### Usage
```bash
/new authentication
/new csv-ingestion
/new rag-pipeline
```

### Process Overview
1. Validate that `specs/spec.md` exists
2. Determine next unit number by scanning `specs/units/`
3. Create directory `specs/units/###-SLUG/`
4. Gather feature objective, behavior, constraints, acceptance criteria
5. Validate that all interface/entity references exist in spec.md
6. Generate `design.md` with status "draft"
7. Confirm with user and display next steps

### Output
Creates `specs/units/###-SLUG/design.md` with:
- **Objective**: Summary (1-2 sentences), success metrics
- **Behavior**: Detailed description, inputs, outputs, edge cases
- **Interfaces & Data**: Which interfaces from spec.md, which entities from spec.md
- **Constraints**: Functional and non-functional constraints
- **Acceptance Criteria**: Given-When-Then format with IDs (AC-[UNIT]-01, AC-[UNIT]-02, etc.)
- **Dependencies**: What blocks this unit, what this unit blocks

### Examples

#### Example 1: RAG Pipeline Feature
**Context**: spec.md defines `embed_text`, `search_vectors`, `generate_response` interfaces. Now need feature that uses them.

**Execution**:
```bash
/new rag-pipeline
```

**Prompts and Responses**:
- "What is the objective of this unit?"
  - Objective: Implement vector search pipeline that retrieves relevant resume content for user queries
  - Success metric: ≥90% of test queries retrieve relevant chunks (measured via eval set)

- "What is the expected behavior?"
  - Input: User query (string)
  - Process: Embed query → search vectors → return top 5 chunks
  - Output: Array of chunks with content + metadata
  - Edge cases: Empty query (return error), no matches above threshold (return empty), OpenAI timeout (retry 3x)

- "Which interfaces and entities will this use?"
  - Interfaces: `embed_text` (from spec.md), `search_vectors` (from spec.md)
  - Entities: `Document` (from spec.md), `Chunk` (from spec.md)

- "What constraints must be respected?"
  - Performance: <50ms p95 for vector search
  - Reliability: Retry embedding calls 3x with exponential backoff
  - Quality: Similarity threshold ≥0.7 (configurable via env var)

- "What are the acceptance criteria?"
  - AC-001-01: Given user query "Python experience", When pipeline runs, Then returns chunks mentioning Python projects
  - AC-001-02: Given empty query, When pipeline runs, Then returns EmptyQueryError
  - AC-001-03: Given 100 test queries, When evaluated for relevance, Then ≥90 have correct chunks

**Result**: `specs/units/001-rag-pipeline/design.md` created with status "draft". Command validates that `embed_text` and `search_vectors` exist in spec.md.

#### Example 2: Feature with Missing Interface
**Context**: Trying to create feature that uses `parse_csv` interface not yet in spec.md.

**Execution**:
```bash
/new csv-ingestion
```

**During Prompts**: User specifies interface `parse_csv(file_path: string): Promise<Record[]>`

**Validation Warning**:
```
⚠️  Interface 'parse_csv' not found in specs/spec.md
Options:
1. Update spec.md to include parse_csv interface (recommended)
2. Continue with design (will fail /check until spec updated)
```

**User Choice**: Update spec.md first, then re-run `/new csv-ingestion`

**Result**: Design waits until spec has required interface, preventing inconsistency.

### Troubleshooting

#### Issue 1: "Design references interfaces not in spec"
**Solution**: Run `/spec` or `/update spec` to add missing interfaces. Design must reference spec, not define new contracts. This ensures consistency.

#### Issue 2: "Acceptance criteria are not testable"
**Solution**: Rewrite in Given-When-Then format with concrete values. "User sees success message" → "Given valid login, When form submitted, Then 'Welcome' message displayed in header."

#### Issue 3: "Don't know what unit number to use"
**Solution**: Command auto-detects by scanning `specs/units/`. If units/002-foo exists, next is 003. If directory is empty, starts at 001.

#### Issue 4: "Feature is too large for one unit"
**Solution**: Break into multiple units. "Authentication" → "001-login", "002-password-reset", "003-session-management". Each gets its own design/plan.

#### Issue 5: "Design keeps changing during implementation"
**Solution**: That's why plan.md exists (volatile execution). Design should be stable intent. If design changes, use `/update` to propagate changes to plan.md.

### Integration
- **Runs after /spec**: Requires spec.md to exist (validates interface references)
- **Informs /plan**: Design provides input for task breakdown
- **Validated by /check**: Checks that all design references exist in spec.md
- **Updated via /update**: Changes to design.md cascade to plan.md (tasks may need adjustment)

---

## /plan SLUG

### Purpose
Generate implementation plan from an approved design. Creates task breakdown with verification plan and tracks progress.

### When to Use
- **After design approval**: `/new` created design.md, now ready for implementation breakdown
- **Replanning**: Original plan has issues, need fresh task decomposition
- **Scope clarification**: Team needs concrete tasks before estimating effort
- **Verification definition**: Need to establish quality gates from constitution
- **Progress tracking setup**: Initialize status section for monitoring work

### Why It Works This Way
Plans are volatile (change as you learn), designs are stable (change only when requirements shift). Separating them prevents coupling execution details to feature intent. When you discover a task needs splitting, update plan.md without touching design.md.

Task granularity (1-3 files, <4 hours) balances progress visibility with overhead. Too granular ("TK-01: Add import statement") creates busywork. Too coarse ("TK-01: Build entire feature") hides progress and creates merge conflicts.

Task ordering (data models → core logic → integration → tests) reduces rework. Building logic before defining types means rewriting when types clarify constraints. This ordering isn't strict (TDD reverses it), but it's a sensible default.

Verification sections pull from constitution quality bars. If constitution says "≥80% coverage," plan.md verification says "pnpm test:coverage" with gate "must_pass: true, target: 80%." This eliminates per-feature negotiation of quality standards.

### Usage
```bash
/plan authentication
/plan csv-ingestion
/plan rag-pipeline
```

### Process Overview
1. Locate unit directory and validate design.md exists
2. Load context from design.md, spec.md, constitution.md
3. Generate atomic task breakdown (TK-01, TK-02, ...)
4. Create verification plan from constitution quality bars
5. Initialize status section (progress_pct: 0, blockers: [], notes: [])
6. Write plan.md and validate structure
7. Update design.md status from "draft" to "approved"
8. Display summary and next steps

### Output
Creates `specs/units/###-SLUG/plan.md` with:
- **Tasks**: ID, title, description, status, priority, estimate, dependencies, completed_at
- **Verification**: Commands (lint/test/coverage), gates (must_pass flags), coverage target, acceptance refs
- **Status**: progress_pct, blockers, notes

### Examples

#### Example 1: RAG Pipeline Task Breakdown
**Context**: design.md exists for unit 001-rag-pipeline, ready to create plan.

**Execution**:
```bash
/plan rag-pipeline
```

**Generated Tasks**:
- TK-01: Define TypeScript types for Chunk and SearchResult | Priority: High | Est: 1h | Deps: []
- TK-02: Implement embed_text wrapper with retry logic | Priority: High | Est: 2h | Deps: [TK-01]
- TK-03: Implement search_vectors with threshold filtering | Priority: High | Est: 3h | Deps: [TK-01]
- TK-04: Create integration function that combines embed + search | Priority: High | Est: 2h | Deps: [TK-02, TK-03]
- TK-05: Write unit tests for embed_text (edge cases: empty string, API failure) | Priority: Medium | Est: 2h | Deps: [TK-02]
- TK-06: Write integration tests for full pipeline (100 test queries) | Priority: Medium | Est: 3h | Deps: [TK-04]
- TK-07: Add performance monitoring (log query latency) | Priority: Low | Est: 1h | Deps: [TK-04]

**Verification**:
```yaml
commands:
  - name: lint
    cmd: pnpm lint
  - name: type-check
    cmd: pnpm type-check
  - name: test
    cmd: pnpm test lib/rag
  - name: coverage
    cmd: pnpm test:coverage lib/rag
gates:
  - lint: { must_pass: true }
  - type-check: { must_pass: true }
  - test: { must_pass: true }
  - coverage: { must_pass: true, target: 80% }
coverage_target: 80%
acceptance_refs: [AC-001-01, AC-001-02, AC-001-03]
```

**Result**: plan.md created, design.md updated to "approved", ready for `/work rag-pipeline TK-01`.

#### Example 2: Discovering Task Needs Splitting
**Context**: During implementation, TK-03 (3h estimate) actually needs 8h.

**Execution**: Edit plan.md to split TK-03:
- TK-03a: Implement basic vector search | Priority: High | Est: 2h
- TK-03b: Add threshold filtering logic | Priority: High | Est: 2h
- TK-03c: Add metadata extraction from results | Priority: High | Est: 2h

**Result**: Plan updated (volatile document), design unchanged (stable intent). Progress tracking continues.

### Troubleshooting

#### Issue 1: "Tasks are too vague to implement"
**Solution**: Each task needs clear validation criteria. "Implement search" → "Implement search_vectors that accepts embedding array, returns top N chunks with similarity ≥threshold."

#### Issue 2: "Task dependencies are circular"
**Solution**: TK-02 depends on TK-05, TK-05 depends on TK-02 = deadlock. Re-order or split tasks. Usually data models/types should be first (no dependencies).

#### Issue 3: "Verification commands fail immediately"
**Solution**: Start with gates that currently pass, add stricter gates as implementation progresses. Begin with "lint: must_pass=false" until code is lintable.

#### Issue 4: "Don't know how to break down feature into tasks"
**Solution**: Follow design.md acceptance criteria. Each AC becomes 1-3 tasks (setup, implementation, tests). Use task ordering template: data models → core logic → integration → tests.

#### Issue 5: "Plan is out of sync with actual work"
**Solution**: Plan.md is volatile—edit it! Discovered new tasks? Add them. Finished tasks out of order? Update status. State-tracker.py auto-generates state.json from plan.md.

### Integration
- **Runs after /new**: Requires approved design.md to exist
- **Informs /work**: Tasks become input for UPEVD implementation pattern
- **Validated by /verify**: Verification section defines quality gates for the unit
- **Tracked by /check**: State-tracker.py reads plan.md to generate progress metrics in state.json

---

## /work SLUG TK-##

### Purpose
Implement a specific task following the UPEVD pattern: Understand, Plan, Execute, Validate, Document.

### When to Use
- **Implementing a task**: After `/plan` creates task breakdown, ready to write code
- **Sequential work**: Complete one task before starting next (respects dependencies)
- **Structured development**: Need systematic approach (not ad-hoc coding)
- **Quality enforcement**: Want verification gates to run automatically
- **Progress tracking**: Need task completion recorded in plan.md

### Why It Works This Way
UPEVD (Understand → Plan → Execute → Validate → Document) prevents "code first, think later" failures. Understanding the task and planning approach before coding reduces thrashing. Validation before marking "done" prevents false progress and maintains quality standards—preventing premature completion that leads to technical debt.

Dependencies ensure correct ordering. If TK-03 depends on TK-01, /work blocks TK-03 until TK-01 status is "done". This prevents integration failures from out-of-order work.

The command updates plan.md task status automatically (ready → doing → done with timestamps). This makes state-tracker.py work—it reads plan.md to generate state.json for `/check`. Manual status updates get forgotten.

Verification gates from plan.md run automatically (lint, type-check, test, coverage). If any must_pass gate fails, task stays "doing" (not marked "done"). This enforces constitution quality bars per-task, ensuring each piece of work meets standards before moving forward.

Hooks run automatically: format-hook.sh (Prettier), state-tracker.py (regenerate state.json), test-hook.sh (if ENABLE_TESTS=1), git-commit-hook.sh (if ENABLE_AUTOCOMMIT=1). This reduces manual steps.

### Phase Naming Convention

The /work command uses the UPEVD pattern (Understand → Plan → Execute → Validate → Document) rather than the standard 5-phase pattern (Validate → Gather → Generate → Validate → Confirm) used by other commands. This deviation is intentional:

- **UPEVD is task-centric**: Emphasizes the implementation mindset needed when writing code
- **Standard pattern is document-centric**: Emphasizes the structured data gathering needed when creating specifications
- **Different mental models**: Task implementation requires understanding existing context before planning changes; document creation requires validating prerequisites before gathering requirements

While the patterns differ in naming, both follow the same underlying philosophy: validate prerequisites, gather information, generate output, validate results, confirm completion.

### Usage
```bash
/work csv-ingestion TK-01
/work authentication TK-03
/work rag-pipeline TK-05
```

### Process Overview

#### Phase 1: UNDERSTAND
1. Locate unit and load plan.md
2. Verify task exists and dependencies are complete
3. Load context (task description, design.md, spec.md, constitution)
4. Update task status to "doing"

#### Phase 2: PLAN
1. Develop strategy (files to modify, code changes, tests)
2. Identify risks (breaking changes, edge cases, performance)
3. Outline approach with steps

#### Phase 3: EXECUTE
1. Implement code (follow constitution, adhere to spec contracts, handle edge cases)
2. Write tests (unit, integration, edge cases, aim for coverage target)
3. Follow best practices (types, docs, error handling, logging)

#### Phase 4: VALIDATE
1. Run verification commands (lint, type-check, test, coverage)
2. Check all must_pass gates pass
3. Validate against design.md acceptance criteria
4. Handle failures (keep status "doing", document, fix)

#### Phase 5: DOCUMENT
1. Update task status to "done" with completed_at timestamp
2. Recalculate progress_pct, update blockers/notes
3. Add brief entry to CLAUDE.md reflection patterns
4. Commit (git-commit hook runs if ENABLE_AUTOCOMMIT=1)

### Output
- Updated plan.md with task status "done" and timestamp
- Code implementation in specified files
- Tests with ≥target coverage
- Updated state.json (via state-tracker hook)
- Git commit (if auto-commit enabled)

### Examples

#### Example 1: Implementing embed_text Wrapper
**Context**: plan.md has TK-02: "Implement embed_text wrapper with retry logic", depends on TK-01 (types, already done).

**Execution**:
```bash
/work rag-pipeline TK-02
```

**UNDERSTAND Phase**:
- Task: Wrap OpenAI embeddings API with retry logic (3 attempts, exponential backoff)
- Dependencies: TK-01 (types) is "done" ✅
- Context: spec.md defines `embed_text(text: string): Promise<number[]>` interface
- Constitution: Must have error handling, retry pattern for external APIs

**PLAN Phase**:
- Files: Create `lib/ai/embeddings.ts`
- Strategy: Use Vercel AI SDK's embed function, wrap in retry utility
- Tests: Unit test with mock (success, failure, retry scenarios)
- Edge cases: Empty string (error), API timeout (retry), rate limit (backoff)

**EXECUTE Phase**:
```typescript
// lib/ai/embeddings.ts
import { embed } from 'ai'
import { openai } from './config'

export async function embed_text(text: string): Promise<number[]> {
  if (!text.trim()) throw new Error('Empty text')

  const { embedding } = await retry(
    () => embed({ model: openai.embedding('text-embedding-3-small'), value: text }),
    { attempts: 3, backoff: 'exponential' }
  )

  return embedding
}
```

Tests written in `lib/ai/embeddings.test.ts` with mocked API calls.

**VALIDATE Phase**:
```bash
pnpm lint          # ✅ Passes
pnpm type-check    # ✅ Passes
pnpm test lib/ai   # ✅ 5/5 tests pass
pnpm test:coverage # ✅ 92% coverage (target: 80%)
```

**DOCUMENT Phase**:
- Task TK-02 status → "done", completed_at: 2025-01-28T14:30:00Z
- Progress: 2/7 tasks done (28.6%)
- CLAUDE.md: "2025-01-28: Retry pattern with exponential backoff handles API rate limits gracefully"
- Git commit (auto): "feat: implement embed_text with retry logic"

**Result**: Task complete, ready for TK-03 (depends on TK-02).

#### Example 2: Task Fails Verification
**Context**: Working on TK-05 (tests), but coverage is only 65% (target: 80%).

**Execution**:
```bash
/work rag-pipeline TK-05
```

**UNDERSTAND → PLAN → EXECUTE**: Write tests...

**VALIDATE Phase**:
```bash
pnpm test:coverage # ❌ Fails: 65% coverage (target: 80%)
```

**Result**:
- Task TK-05 status remains "doing" (NOT "done")
- Blocker added: "Coverage 65% < 80% target, need tests for edge cases"
- No git commit (validation failed)
- Next action: Add more tests, re-run /work rag-pipeline TK-05

#### Example 3: Blocked by Dependencies
**Context**: Trying to work on TK-04 (integration) but TK-02 (embed) is still "doing".

**Execution**:
```bash
/work rag-pipeline TK-04
```

**UNDERSTAND Phase**:
- Task TK-04 depends on [TK-02, TK-03]
- TK-02 status: "doing" ❌
- TK-03 status: "done" ✅

**Result**:
```
❌ Cannot start TK-04: dependency TK-02 is not complete.
Complete TK-02 first, then retry.
```

### Troubleshooting

#### Issue 1: "Verification gates fail but I want to mark done"
**Solution**: Don't bypass gates. If coverage is 65% and target is 80%, add tests or update constitution (with strong justification) to lower target. Quality bars exist to prevent technical debt.

#### Issue 2: "Task is too large, can't complete in one session"
**Solution**: Edit plan.md to split the task. TK-03 → TK-03a, TK-03b. Keep original done? Complete what you can, split remainder. Plan.md is volatile.

#### Issue 3: "Dependencies are wrong, need to work out of order"
**Solution**: Edit plan.md to fix dependencies. If TK-04 doesn't actually need TK-02, remove the dependency. Update plan.md as you learn.

#### Issue 4: "Hooks are failing (format, state-tracker)"
**Solution**: Check hook logs in `.claude/logs/`. Format hook failing? Run `pnpm format` manually. State-tracker failing? Check plan.md YAML syntax. Fix root cause before continuing.

#### Issue 5: "Task marked done but tests are actually failing"
**Solution**: Validation phase has bugs. Re-run verification commands manually. If tests fail, task should NOT be "done". Edit plan.md to fix status, add blocker, re-run /work.

### Integration
- **Runs after /plan**: Requires plan.md with tasks to exist
- **Updates /check**: Task status changes trigger state-tracker.py to regenerate state.json
- **Enforces /constitution**: Verification gates pull from constitution quality bars
- **Validates against /new**: Implementation must satisfy design.md acceptance criteria

---

## /check [SLUG]

### Purpose
Validate document alignment, detect implementation drift, and check constitution compliance across the project or for a specific unit.

### When to Use
- Periodically to check project health
- Before major releases
- When documents may have drifted from implementation
- To verify state.json accuracy

### Why It Works This Way
Without /check, documents can diverge from implementation, creating confusion and inconsistency. As code evolves, it's easy for specs to become outdated, designs to reference non-existent interfaces, or implementations to drift from their documented contracts. By systematically validating alignment between documents (constitution → PRD → spec → design → plan) and comparing spec contracts with actual code, /check catches drift early before it becomes a maintenance nightmare. This ensures documentation remains a reliable source of truth rather than historical fiction.

### Usage
```bash
/check                    # Check entire project
/check csv-ingestion     # Check specific unit
```

### Prerequisites
- L1 documents should exist (constitution, prd, spec)
- State tracker hook should be functional

### Process
1. **Determine Scope**: Check specific unit or entire project
2. **Run State Tracker**: Execute state-tracker.py to generate fresh state.json
3. **Load State**: Read state.json for L1 status, units status, alignment issues
4. **Validate L1 Documents**: Check constitution, prd, spec exist and are valid
5. **Validate Document Alignment**: Verify design→spec, plan→design references
6. **Detect Implementation Drift**: Compare spec contracts with actual code (modules, interfaces, data models)
7. **Check Constitution Compliance**: Verify coverage targets, quality standards
8. **Generate Report**: Create comprehensive report with issues categorized by severity
9. **Display Report**: Show with color coding (✅ pass, ⚠️ warning, ❌ critical)
10. **Provide Recommendations**: Suggest which documents or code need updates, priority order

### Output
Report with sections:
- **L1 Status**: Constitution, PRD, Spec versions and status
- **Alignment Issues**: Invalid interface/entity references, missing implementations, signature mismatches
- **Drift Detection**: Modules in code not in spec, modules in spec not in code, interface mismatches
- **Constitution Compliance**: Coverage violations, quality bar violations
- **Per-Unit Status** (if specific unit): Design status, plan status, progress, blockers

### Validation
- ✅ State tracker executed successfully
- ✅ state.json contains current data
- ✅ All alignment checks performed
- ✅ Drift detection completed
- ✅ Constitution compliance verified
- ✅ Clear recommendations provided
- ✅ Issues prioritized by severity

### Notes
- Focuses on document consistency and spec alignment
- Different from /verify (which runs quality gates)
- Reads from state.json (auto-generated, never edit manually)
- Use for health checks and alignment verification

---

## /verify SLUG

### Purpose
Run all verification gates for a unit to ensure quality standards are met before considering it complete.

### When to Use
- After completing several tasks
- Before considering feature ready
- To validate quality baseline
- After fixing issues from previous verification

### Why It Works This Way
Without /verify, units can be marked complete without meeting quality bars, leading to technical debt. By running comprehensive verification gates (linting, type-checking, tests, coverage) against the standards defined in the constitution, we ensure that each unit meets the project's quality requirements before being considered done. This systematic validation prevents the accumulation of shortcuts and ensures that "complete" means "meets all standards," not just "code exists."

### Usage
```bash
/verify csv-ingestion
/verify authentication
```

### Prerequisites
- plan.md must exist for the unit
- At least some tasks should be complete

### Process
1. **Locate Unit**: Find `specs/units/###-SLUG/`
2. **Load Verification Plan**: Read plan.md verification section (commands, gates, coverage_target, acceptance_refs)
3. **Run Verification Commands**: Execute linting, type checking, tests, coverage measurement
4. **Evaluate Gates**: Determine pass/fail for each gate, check must_pass flags
5. **Check Acceptance Criteria**: Review design.md criteria and determine if satisfied
6. **Generate Report**: Create comprehensive report with results
7. **Update Unit Status**: If all gates pass, consider unit ready; if fail, add to blockers
8. **Display Report**: Show with color-coded status (✅ pass, ❌ fail, ⚠️ warning)

### Verification Commands
- **Linting**: Run linter for stack (ruff, eslint, etc.)
- **Type Checking**: Run type checker (pyright, tsc, etc.)
- **Tests**: Run test suite, capture coverage metrics
- **Coverage**: Check if coverage meets target from constitution

### Output
Report showing:
- Each verification command result
- Each gate result (pass/fail with must_pass status)
- Coverage achieved vs. target
- Acceptance criteria status
- List of blockers or issues
- Overall pass/fail status

### Validation
- ✅ All verification commands executed
- ✅ Gates evaluated with correct must_pass logic
- ✅ Coverage measured against constitution target
- ✅ Clear pass/fail status provided
- ✅ Actionable feedback for failures

### Notes
- Different from /check (which checks alignment/drift)
- /verify runs actual quality gates (tests, linting, coverage)
- Must pass before feature is considered complete
- Re-run after fixing issues

---

## /reflect

### Purpose
Capture important learnings, decisions, and insights from development work to improve future iterations and preserve project knowledge.

### When to Use
- After feature completes
- When discovering useful patterns or anti-patterns
- Periodically (weekly or after major milestones)
- To document "aha moments" and insights

### Why It Works This Way
Without /reflect, valuable learnings are lost, mistakes get repeated, and team knowledge doesn't accumulate. Development work generates insights constantly—"this pattern worked well," "that approach caused problems," "here's why we made this decision"—but these insights vanish unless captured. By systematically recording reflections in CLAUDE.md, we build institutional memory that informs future work. When someone faces a similar problem six months later, they can learn from past experience instead of rediscovering solutions. This transforms experience into reusable knowledge and prevents teams from repeatedly stepping on the same rakes.

### Usage
```bash
/reflect
```

### Prerequisites
- None (can be run at any time)

### Process
1. **Prompt for Reflection**: Ask what user wants to reflect on
2. **Gather Reflection Content**: Prompt for topic, context, observation, impact, actions
3. **Categorize Reflection**: Determine category (Technical, Process, Quality, Collaboration, Performance, Other)
4. **Add to CLAUDE.md**: Append to Reflection Patterns section with date, topic, category
5. **Check for Actionable Items**: If reflection includes actions, ask if should update documents
6. **Optional: Update Documents**: Offer to update constitution, spec, PRD if learnings suggest changes
7. **Confirm**: Display summary of reflection added and any updates made

### Reflection Format
```markdown
- YYYY-MM-DD: [Context]: [Learning]. [Why it matters]. [Application].
```

### Categories
- **Technical**: Code patterns, architecture decisions
- **Process**: Workflow improvements, tool usage
- **Quality**: Testing strategies, bug patterns
- **Collaboration**: Communication, clarifications needed
- **Performance**: Speed, efficiency learnings
- **Other**: Uncategorized insights

### Output
- **Updated**: CLAUDE.md with new learning entry
- **Optional**: constitution.md, spec.md, or other docs if actionable updates identified

### Examples

#### Example 1: Process Improvement Reflection
**Context**: Completed migration from duplicating task summaries in PRD Part B to using reference-based approach.

**Execution**:
```bash
/reflect
```

**Prompts and Responses**:
- "What would you like to reflect on?"
  - PRD maintenance overhead and how we eliminated it

- "What did you learn or observe?"
  - By making Part B reference-based (linking to plan.md instead of duplicating summaries), we eliminated significant maintenance overhead. Using state.json for progress tracking instead of manual updates reduced the Part B from ~260 to ~100 lines.

- "Why does this matter? What is the impact?"
  - Reduces documentation drift, eliminates duplicate maintenance work, and makes PRD more sustainable as project evolves

- "How should this be applied in the future?"
  - Always prefer references over duplication in documentation. Use automated state tracking where possible. Keep documents focused on stable information.

- "Which category does this fall under?"
  - Process

**Result**: Added to CLAUDE.md Reflection Patterns:
```markdown
- 2025-10-24: PRD maintenance overhead eliminated by making Part B reference-based: link to plan.md instead of duplicating summaries; use state.json for progress instead of manual tracking; reduced Part B from ~260 to ~100 lines
```

#### Example 2: Technical Pattern Reflection
**Context**: After implementing retry logic for OpenAI API calls, discovered exponential backoff handles rate limits better than fixed delays.

**Execution**:
```bash
/reflect
```

**Result**: Added to CLAUDE.md:
```markdown
- 2025-01-28: Retry pattern with exponential backoff handles API rate limits gracefully; use 3 attempts with 2x backoff instead of fixed delays; prevents overwhelming rate-limited services
```

### Validation
- ✅ Reflection added to CLAUDE.md
- ✅ Proper date format (YYYY-MM-DD)
- ✅ Category tag applied
- ✅ Content is clear and actionable
- ✅ Relevant documents updated if applicable
- ✅ Action items captured

### Notes
- Reflections are optional but highly valuable
- Capturing patterns early prevents repeating mistakes
- Insights inform future /plan and /work
- Keep 5-10 most recent patterns (remove oldest when list grows)

---

## /update DOCUMENT PATH

### Purpose
Make changes to L1 or L2 documents and automatically identify dependent documents that need updates, ensuring consistency across the system.

### When to Use
- When constitution principles change
- When PRD requirements evolve
- When spec interfaces need modification
- When design or plan needs updates

### Why It Works This Way
Without /update, changes to core documents can create cascading inconsistencies across specs, designs, and plans. When a constitution principle changes (e.g., coverage target from 70% to 80%), every unit's plan.md needs updating. When a spec interface changes signature, every design.md that references it needs review. Manual propagation is error-prone and easy to forget. By automatically identifying dependencies and offering guided propagation, /update ensures that changes ripple through the system correctly, maintaining consistency across all documentation layers while giving you control over when and how updates happen.

### Usage
```bash
/update constitution quality_bars.coverage_target
/update spec interfaces.parse_document.inputs
/update prd outcomes.primary
```

### Prerequisites
- Target document must exist

### Process
1. **Parse Arguments**: Determine which document and section to update
2. **Load Current Document**: Read target file and navigate to specified path
3. **Show Current Value**: Display current value at path
4. **Prompt for New Value**: Ask for new value and rationale
5. **Identify Dependencies**: Based on document type, identify what depends on it
6. **Make Primary Change**: Update target document with new value, updated timestamp, incremented version
7. **Analyze Impact**: For each dependent document, check if it references the changed value, determine if needs updating
8. **Generate Impact Report**: Create report showing what was changed, which documents affected, required updates, priority/severity
9. **Prompt for Propagation**: Ask user if changes should be propagated automatically, which dependencies to update now, which to defer
10. **Propagate Changes (if approved)**: Update approved dependencies, maintain consistency, update timestamps
11. **Flag Remaining Updates**: For deferred updates, add to blockers, mark in state.json, remind user

### Dependency Identification

**If updating constitution.md:**
- All units' plan.md (coverage_target, quality standards)
- spec.md (may reference principles)

**If updating prd.md:**
- spec.md (technical decisions based on outcomes)
- All units' design.md (aligned to outcomes)

**If updating spec.md:**
- All units' design.md (interface/entity references)
- All units' plan.md (verification may change)
- Actual code implementations

**If updating design.md:**
- Same unit's plan.md (tasks may need adjustment)
- Other units that depend on this one

**If updating plan.md:**
- Less impact (volatile document)
- May affect dependent units

### Output
- **Updated**: Primary document
- **Updated**: Propagated documents (if approved)
- **Report**: Impact analysis and update status

### Validation
- ✅ Target document updated with new value
- ✅ Version incremented (if appropriate)
- ✅ Timestamp updated
- ✅ All dependencies identified
- ✅ Impact severity correctly assessed
- ✅ Propagated changes are consistent
- ✅ Blockers added for manual updates
- ✅ User prompted before automatic changes

### Notes
- Use to maintain consistency across documents
- Impact analysis prevents cascading inconsistencies
- Prompts for propagation give user control
- Deferred updates tracked in blockers

---

## Command Sequence Summary

### First-Time Project Setup
1. `/constitution` — Define governance
2. `/prd` — Create project requirements
3. `/spec` — Create engineering contract

### Per-Feature Development
1. `/new FEATURE_NAME` — Create feature design document
2. `/plan FEATURE_NAME` — Generate task breakdown and verification plan
3. `/work FEATURE_NAME TK-##` (repeat) — Implement each task (UPEVD pattern)
4. `/verify FEATURE_NAME` — Run quality gates (tests, linting, coverage)
5. `/check [FEATURE_NAME]` — Validate alignment and drift (optional)
6. `/reflect` (optional) — Extract learnings

### Ongoing Maintenance
- `/check` — Validate project alignment and drift
- `/update DOCUMENT PATH` — Make changes and propagate updates
- `/reflect` — Capture patterns periodically

### Key Rules
- Complete workflow in sequence
- Never skip validation steps
- Run /verify before considering feature "done"
- Use /check periodically for health checks
- Use /update for document changes to ensure consistency

---

## Notes on Command Evolution

This reference reflects the actual implementation of commands in `.claude/commands/`. Some key distinctions:

1. **Task breakdown**: Task breakdown is part of /plan, not a separate command
2. **Progress tracking**: Progress tracked via state.json and /check, not a separate status command
3. **/verify vs /check distinction**:
   - /verify runs quality gates (tests, linting, coverage)
   - /check validates alignment and detects drift
4. **Argument format**: Uses SLUG and TK-## format (e.g., `csv-ingestion TK-01`)
5. **/update command**: Handles document changes with dependency propagation

These patterns reflect practical evolution of the system toward simpler, more maintainable workflows.
