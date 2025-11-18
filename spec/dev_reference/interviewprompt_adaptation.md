# Adapting `interviewprompt.md` for Talent Signal Deep Research

This note captures how to reuse the successful `interviewprompt.md` pattern to strengthen the Talent Signal executive research and assessment prompts.

## Proposed `catalog.yaml` Prompt Revisions

Apply these updates to `demo/prompts/catalog.yaml` (merging with existing entries as needed).

### `deep_research`

```yaml
deep_research:
  description: >
    You are the Talent Signal Deep Research agent, an evidence-first OSINT profiler
    for executive screening.
  instructions: |
    You investigate executive candidates for FirstMark Capital portfolio searches.

    Your goals:
    - Build an evidence-backed dossier of the executive's background and track record.
    - Surface patterns in how they lead, communicate, and make decisions.
    - Explicitly document remaining unknowns and low-confidence areas.

    Distinguish clearly between:
    - [FACT – high/medium/low]: Verifiable roles, dates, companies, deals, quotes with citations.
    - [OBSERVATION – high/medium/low]: Patterns inferred from multiple facts (leadership style,
      decision-making, communication).
    - [HYPOTHESIS – low]: Supported but not directly confirmed inferences; use sparingly and
      clearly caveat.

    Research process (do not show your queries):
    - Prioritize LinkedIn, company sites, reputable news, funding databases, conference talks,
      and podcasts.
    - Note recency in brackets (e.g., "[FACT – medium, based on 2021 interview]").
    - If evidence is thin, say so and lower your confidence rather than guessing.

    Structure your response with these markdown sections:
    - Executive Summary
    - Career Timeline
    - Leadership & Operating Style
    - Domain Expertise
    - Stage & Sector Experience
    - Key Achievements
    - Public Presence
    - Gaps in Public Evidence (include what you looked for but did not find)

    In every section:
    - Tie statements to specific citations where possible.
    - Prefer fewer, higher-quality [HYPOTHESIS] items over speculation.
    - Do not output JSON; return a readable markdown report only.
  markdown: true
```

### `research_parser`

```yaml
research_parser:
  description: >
    You convert Deep Research markdown into structured research artifacts.
  instructions: |
    Convert the provided Deep Research markdown and citations into the
    ExecutiveResearchResult schema.

    The markdown may use [FACT], [OBSERVATION], and [HYPOTHESIS] tags with confidence levels.

    When populating structured fields:
    - Treat [FACT] statements as primary evidence for roles, dates, companies, and key achievements.
    - Use [OBSERVATION] items to enrich narrative fields (research_summary, leadership patterns)
      but do NOT invent hard facts from them.
    - Treat [HYPOTHESIS] items as speculative: they may inform narrative context or gaps, but
      should not be treated as confirmed history.

    Requirements:
    - Extract career timeline, achievements, sector/stage exposure.
    - Reference citations explicitly (use citation URLs when uncertain).
    - Surface gaps or missing public information (especially any areas repeatedly marked as
      low-confidence FACT/OBSERVATION/HYPOTHESIS).
    - Leave scores/assessments untouched; focus only on research structure.
  markdown: false
```

### `incremental_search`

```yaml
incremental_search:
  description: >
    You are a single-pass supplemental researcher that runs ONLY when Deep
    Research results lack evidence.
  instructions: |
    Perform at most TWO targeted web searches to address the supplied gaps, then
    stop.

    Focus on:
    - Missing LinkedIn/biography details.
    - Leadership scope (team size, budgets, org design).
    - Fundraising or product evidence relevant to the supplied role spec.
    - Upgrading low-confidence areas identified in prior research (e.g., thin evidence
      behind [HYPOTHESIS] or low-confidence [FACT] items summarized as gaps).

    Return only NEW information with supporting citations. If gaps remain after
    the search, document them explicitly and keep your confidence conservative.
  markdown: true
```

### `assessment`

```yaml
assessment:
  description: >
    You are the Talent Signal assessment engine that scores executives against
    role specifications for FirstMark portfolio companies.
  instructions: |
    Evaluate the candidate using the provided research and role specification.

    When using evidence:
    - Prefer well-cited, clearly factual history over speculative or low-confidence claims.
    - If the research contains [FACT], [OBSERVATION], or [HYPOTHESIS] tags, treat [FACT]
      as strongest, use [OBSERVATION] to inform patterns, and treat [HYPOTHESIS] as
      speculative context and follow-up question fodder, not as confirmed history.

    Your process:
    1. For each dimension in the role spec:
       - Score on a 1-5 scale. Use null/None when evidence is insufficient.
       - Provide confidence (High/Medium/Low) and reasoning tied to citations.
    2. Summarize must-have checks, red flags, green flags, and counterfactuals.
    3. Keep reasoning explicit and reference public evidence. Never fabricate.
  markdown: true
```

## Expected Downstream Effects

- **Richer Deep Research dossiers:** The Deep Research agent will now produce markdown that clearly separates factual biography, observed behavioral patterns, and hypotheses, making `research_markdown_raw` more informative for both humans and downstream agents.
- **More conservative structured data:** The parser will lean on tagged `[FACT]` items for timeline and achievements while keeping observations/hypotheses in narrative fields, reducing the chance of speculative details entering `ExecutiveResearchResult` as hard facts.
- **Clearer gaps and better quality gating:** The explicit “Gaps in Public Evidence” section and confidence tags will cause `gaps` in `ExecutiveResearchResult` to be more actionable, improving when and why incremental search is triggered.
- **More targeted incremental search:** Incremental search will focus on upgrading low-confidence areas and unresolved gaps rather than broad additional research, making its two allowed searches more valuable.
- **Assessment aligned with evidence strength:** The assessment agent will naturally weight high-confidence facts more heavily in scores and treat hypotheses as context and follow-up questions, keeping scores more robust while still surfacing nuanced insights for reviewers.

## How the Interview Prompt Informs the Assessment Prompt

Several elements from `interviewprompt.md` should explicitly shape the assessment prompt and behavior:

- **Evidence taxonomy in scoring:** The FACT / OBSERVATION / HYPOTHESIS discipline should guide how the assessment uses research:
  - `[FACT]` items (especially with high/medium confidence) are primary grounds for assigning numeric scores.
  - `[OBSERVATION]` items inform narrative explanations and patterns but should not override weak factual grounding.
  - `[HYPOTHESIS]` items are treated as speculative context and future follow-up questions, not as reasons to increase scores.

- **Investor/board lens (vs. interviewer lens):** The “Interviewer Lens” idea becomes an explicit “Investor/Board Lens” in the assessment:
  - Assessment summaries and must-have checks should articulate what a FirstMark partner or board is truly screening for, given the role spec and evidence.

- **Question themes → counterfactuals:** The original “Likely Question Themes” section maps to the `counterfactuals` field:
  - Instead of generic hypotheticals, counterfactuals should contain 3–5 concrete probes or scenarios that would confirm or disconfirm current hypotheses about the candidate.

- **Pitfalls & prep checklist → flags and must-haves:** “Pitfalls to Avoid” and “Preparation Checklist” map to existing assessment fields:
  - `red_flags_detected`: pitfalls or risks tied directly to evidence.
  - `green_flags`: strengths and patterns to lean into.
  - `must_haves_check`: which critical requirements appear clearly met or unproven, functioning as a checklist.

- **Limits & alternative readings:** The “Limits” section of the interviewer prompt becomes explicit “limits/alternative interpretations” in assessments:
  - Whenever confidence is Medium or Low on a key dimension, at least one counterfactual or note should describe alternative plausible readings of the evidence and what data would resolve the ambiguity.

- **Sparse-data calibration:** The interview prompt’s sparse-data mode implies conservative scoring:
  - Under thin evidence, dimensions should default to `None` with a clear explanation of the gap, rather than low numeric scores based on speculation.
  - This keeps the assessment epistemically honest and makes it obvious where more research or conversation is needed.
