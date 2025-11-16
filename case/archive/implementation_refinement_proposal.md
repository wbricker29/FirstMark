# Talent Signal Agent – Implementation Refinement Proposal

> Proposal to tighten scope, architecture, and evaluation of the Talent Signal Agent demo, grounded in `case/case_requirements.md` and `case/technical_spec.md`.

This proposal addresses the main gaps in the current spec and converts them into a concrete, demo‑ready plan. Each section lists the proposed actions and why they are the right tradeoffs for this case.

---

## 1. Clarify Minimal Demo Scope

**Proposed Actions**
- Designate one “hero” flow as the core of the demo: pre‑loaded People + Roles in Airtable → create `Screen` → click “Start Screening” → ranked matches with reasoning written back.
- Treat other flows (Upload, New Role, New Search, Deep Research UI) as simplified or conceptual: use static records and simple forms in Airtable, with no additional automation beyond what is required for screening.
- Restrict the live candidate set to ~10–20 executives and 3–4 roles (2 CFO, 2 CTO) so that a full screen can run end‑to‑end in a few minutes.

**Rationale**
- Aligns with the rubric’s emphasis on clear value and insight generation rather than breadth of features; one excellent workflow beats many half‑finished ones.
- Reduces implementation risk and cognitive load for the interview; most of the 30 minutes can be spent on the matching logic and reasoning trail, not on plumbing.
- Still shows extensibility: Upload, New Role, and New Search remain visible in the Airtable schema and UI, but the demo story centers on the screening workflow that is explicitly called out as most important in `solution_strategy.md`.

---

## 2. Make Airtable Schemas Concrete

**Proposed Actions**
- Define a small, explicit Airtable schema and treat it as the contract between Airtable and the Python workflow:
  - `People`: `exec_id`, `Name`, `Current Title`, `Company`, `Role Type` (CTO/CFO), `Stage`, `Sector`, `Location`, `LinkedIn URL`, `Bio (long text)`, `Relationship Type`, `Research Summary (long text)`.
  - `Portcos`: `portco_id`, `Name`, `Stage`, `Sector`, `HQ Location`, `Notes`.
  - `Roles`: `role_id`, linked `Portco`, `Role Type`, `Seniority`, `JD Text (long text)`, `Status`.
  - `Role Specs`: linked `Role`, `Spec JSON` (single‑line text), `Spec Markdown` (long text), `Source` (Base/Custom).
  - `Search`: linked `Role`, linked `Spec`, `Search Name`, `Notes`, `Created At`.
  - `Screen`: linked `Search`, linked `Candidates (People)`, `Status` (Ready → Processing → Complete/Error), `Results Markdown`, `Run Started`, `Run Ended`.
  - `Role Evals`: linked `Screen`, linked `Person`, `Overall Score`, `Confidence`, `Rank`, `Dimension Scores JSON`, `Reasoning (long text)`, `Counterfactuals (long text)`.
- Document these tables and fields explicitly in the spec, with 1–2 example rows per table to show how records relate.

**Rationale**
- Converts the current high‑level “tables list” into a concrete data model that the Python code can target; avoids last‑minute Airtable schema drift.
- Makes the demo more credible from a product thinking perspective: the tables look like something a real platform team could extend post‑case.
- Keeps the scope manageable by prioritizing the tables that are needed for the demo flow (especially `People`, `Roles`, `Search`, `Screen`, and `Role Evals`), while leaving room for future tables like a generalized Research Log.

---

## 3. Specify Retrieval & Ranking Logic

**Proposed Actions**
- Implement a simple deterministic pre‑filter before calling the LLM:
  - Filter candidates by `Role Type` (CTO vs CFO).
  - Prefer candidates whose `Stage` and `Sector` overlap with the role’s stage/sector; mark others explicitly as “stretch”.
  - Optionally filter by geography if the role requires it.
- Define a rubric with a small set of dimensions (e.g., `Domain Experience`, `Stage Fit`, `Team Scale`, `Capital Markets / Fundraising`, `Context Fit`) and a 1–5 score plus weight for each.
- Ask the LLM to return structured JSON per candidate: per‑dimension score, confidence (H/M/L), and a one‑sentence rationale for each dimension.
- Compute an overall weighted score in Python, not in the LLM, and rank candidates by:
  - `Overall Score` (descending),
  - then `Confidence` (H > M > L),
  - then a relationship heuristic (e.g., Guild > Portfolio Exec > Partner 1st‑degree > Event).
- Enforce a minimum score threshold and label any candidate below it as “Not Recommended” rather than silently burying them.

**Rationale**
- Makes the matching process explainable and repeatable, directly addressing the “reasoning trail” requirement in `case/case_requirements.md`.
- Uses the LLM where it is strongest (textual interpretation and scoring against a rubric) while keeping the aggregation and ranking logic deterministic and inspectable.
- Enables a compelling “diagnose the match” story in the demo: you can point to specific rubric dimensions and how they influenced rank, not just a black‑box score.

---

## 4. Define Prompting & Context Strategy

**Proposed Actions**
- Split the LLM work into two clear steps with distinct prompts:
  1. **Research step** (Deep Research API):
     - Inputs: LinkedIn URL (if available), any existing bio text, current title/company, role type.
     - Output: a concise JSON summary of career history, stage/sector exposure, team scale, fundraising/exit experience, and notable signals or red flags.
  2. **Assessment step** (assessment model call):
     - Inputs: role JD text, role spec (JSON + brief Markdown), research summary JSON, and basic People fields.
     - Output: rubric‑aligned scores, confidence levels, short rationales, and 1–2 counterfactuals, all in a strict JSON schema.
- For long bios or job descriptions, first ask the model to generate a 300–400‑word normalized summary that is then used as the context for assessment.
- Use sectioned prompts (e.g., `CONTEXT:`, `ROLE:`, `CANDIDATE:`, `TASK:`) and enforce a fixed JSON response format; validate and coerce responses in Python.

**Rationale**
- Separating research from assessment matches how a human would work (first understand the candidate, then judge fit) and makes debugging easier.
- Keeps prompt length under control and reduces redundancy; the assessment step reads a compact summary instead of raw, messy bios or full JDs.
- A strict, documented JSON schema reduces demo‑day surprises and lets you show “structured outputs” explicitly, which maps to the Technical Design and Data Integration rubric categories.

---

## 5. Add Error & Edge‑Case Handling

**Proposed Actions**
- Wrap each candidate’s processing in try/except blocks so a single failure does not kill the entire screen:
  - If research fails: log the error, mark the role eval for that candidate as `Error` with a clear reason, and optionally run a degraded assessment using only structured fields.
  - If assessment JSON fails validation: retry once with a stricter prompt asking for “valid JSON only”; on second failure, store the raw reasoning text and assign `Low` confidence.
  - If no candidates pass filters or thresholds: write a “No strong matches” summary into the `Screen` record, including 1–2 borderline candidates with explanations of why they are weak fits.
  - If Airtable write operations fail: log the error and keep the process idempotent (re‑running the same screen overwrites or upserts existing evals rather than duplicating them).
- Use a simple state machine for `Screen.Status`: `Ready` → `Processing` → `Complete` or `Error`, and ensure that status is updated even when partial failures occur.

**Rationale**
- Demonstrates pragmatic engineering discipline: the system behaves predictably under partial failure, which is something a real platform team would care about.
- Supports a smoother live demo; you avoid awkward hard failures and can talk through how the system responds to imperfect data or flaky external APIs.
- Adds credibility under the “Product Thinking” and “Technical Design” rubric elements by showing that error paths are intentionally designed, not ignored.

---

## 6. Cover Non‑Functional Concerns

**Proposed Actions**
- Introduce basic guardrails for rate limits and cost:
  - Cap the number of live candidates per screen (e.g., 10–15).
  - Expose configuration for max candidates and model choices via environment variables or a small config file.
  - Prefer “light” Deep Research settings appropriate for short, focused executive checks.
- Handle secrets and connectivity cleanly:
  - Store all API keys (OpenAI, Tavily, ngrok) only in `.env` and load via `python-dotenv`; never hard‑code secrets or commit them.
  - Document the minimal steps to start Flask + ngrok + Airtable automations for the demo.
- Add a lightweight validation and testing loop:
  - Build a small offline fixture dataset (5–10 people, 2 roles) and a script to run the screening logic without Airtable (pure Python) for quick iteration.
  - Add minimal tests or assertions around JSON parsing and scoring logic to ensure regression‑free changes.

**Rationale**
- Shows that the design is production‑aware even though this is a demo; reviewers see that cost, rate limits, and security are acknowledged and managed.
- Makes it easier for you to iterate safely before the interview and rerun the demo in a controlled way.
- Directly supports the Communication & Clarity rubric item by giving a simple, repeatable “how to run this” story.

---

## 7. Define Agent Evaluation & Success Criteria

**Proposed Actions**
- Create a tiny “gold set” of candidates for each of the 3–4 demo roles, manually labeled as `Strong Fit`, `Maybe`, or `No` based on your own judgment and the role spec.
- After running the agent, compare:
  - Whether the system’s top‑3 per role roughly aligns with the `Strong Fit` and `Maybe` labels.
  - Where the agent disagrees and whether its reasoning is still defensible or reveals useful counter‑signals.
- Collect 2–3 concrete stories to highlight in the presentation, for example:
  - A non‑obvious candidate that the agent surfaces as a strong fit and why.
  - A candidate who looks good on paper but is correctly downgraded because stage/sector/context don’t match.
- Use these examples as a mini “user study” within the presentation, showing how a FirstMark partner or platform lead might respond to the rankings.

**Rationale**
- Translates the rubric from abstract criteria into tangible outcomes: “Would I actually use this ranking?” becomes a question you can answer with examples.
- Reinforces that this is not just a toy demo: the evaluation loop mirrors how you would validate such a system if it were launched inside the firm.
- Gives you compelling, story‑driven moments in the presentation that tie together product thinking, technical design, and insight generation.

---

## Summary

Collectively, these actions narrow the demo to one excellent, end‑to‑end screening workflow while still showcasing a thoughtful, extensible architecture. They make the Airtable schema, matching logic, prompts, and error handling concrete enough to implement quickly, and they create a clear evaluation story that maps directly to FirstMark’s case rubric. This should help the interviewers see both how you think and how you would build a real, usable Talent Signal Agent over time.

