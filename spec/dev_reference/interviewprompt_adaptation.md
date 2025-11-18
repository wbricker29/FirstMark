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

    Use this 1-5 scale consistently:
    - 1 = strong negative / clearly misaligned with the dimension
    - 2 = weak / meaningfully below expectations
    - 3 = mixed / partial fit with notable gaps
    - 4 = solid / generally strong with minor caveats
    - 5 = strong positive / clear strength on this dimension

    Your process:
    1. For each dimension in the role spec:
       - Score on a 1-5 scale. Use null/None when evidence is insufficient
         or supported only by [HYPOTHESIS] or low-confidence [OBSERVATION].
       - Provide confidence (High/Medium/Low) and reasoning tied to citations.
       - Make clear when the limiting factor is lack of evidence rather than
         negative evidence.
    2. Write the assessment summary so that:
       - The first sentence is a headline verdict in natural language
         (e.g., "[Overall: Strong] CFO fit for Pigment; strongest on
         capital markets, risks around scaling post-IPO.").
       - The remaining 1-2 sentences explain what a FirstMark partner or
         board is likely to care about most, and where this candidate is
         most likely to surprise on the upside or downside.
    3. Populate must_haves_check, red_flags_detected, and green_flags:
       - must_haves_check: checklist-style items indicating which critical
         requirements appear clearly met or unproven.
       - red_flags_detected: 3-5 concise bullets phrased as "board-ready"
         risks, each tied to specific evidence or citations.
       - green_flags: 3-5 concise bullets for strengths to lean on in
         conversations, each tied to specific evidence or citations.
    4. Use counterfactuals to propose concrete follow-up questions:
       - Each counterfactual should describe a specific probe or scenario a
         partner could use in conversation and how the answer might move a
         dimension score (e.g., "If they have led a 300+ person org post-Series D,
         Leadership and Scaling scores could move from 3→4.").
    5. Keep reasoning explicit, tie claims to public evidence, and prefer
       null/None over guessing when evidence is thin. Never fabricate.
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

## Demo-Focused Assessment Enhancements and Dependencies

The enhanced assessment prompt is designed to make demo outputs easier to narrate while remaining compatible with existing code and tests.

- **Headline verdict in `summary`:**
  - First sentence becomes a demo-friendly headline (e.g., "[Overall: Strong] CTO fit...").
  - No schema changes required: this is just stronger guidance for how to populate the existing `summary: str` field in `AssessmentResult` (see `demo/models.py`).

- **Explicit 1–5 scale semantics:**
  - Clarified scale is reflected only in the assessment prompt; `DimensionScore.score` remains `Optional[int]` with `ge=1, le=5`.
  - `calculate_overall_score()` in `demo/agents.py` continues to work as-is (simple average × 20); what changes is the interpretability of each integer in the demo narrative.

- **Evidence-aware null/None behavior:**
  - Instructions now explicitly say to use `None` when evidence is thin or only hypothetical, aligning with the existing model constraint that `None` represents "Unknown / insufficient evidence".
  - This behavior is consistent with spec expectations and keeps downstream consumers (Airtable JSON, tests, and any analytics) unchanged.

- **Board-ready flags and must-haves:**
  - `must_haves_check`, `red_flags_detected`, and `green_flags` are already part of `AssessmentResult`.
  - The new guidance simply standardizes their phrasing and density (3–5 bullets) so that Airtable-rendered assessments read like concise partner briefs during the demo.

- **Counterfactuals as follow-up questions:**
  - `counterfactuals` remains a `list[str]`; the prompt now nudges each entry to be a concrete question plus a short "how this might move the score" clause.
  - This makes the array directly usable as a follow-up interview checklist demo without any code changes.

- **Test and loader compatibility:**
  - `tests/test_prompts.py` asserts that the assessment instructions contain the phrase "Score on a 1-5 scale"; the updated prompt preserves this exact wording.
  - `demo/prompts/library.py` and `get_prompt("assessment")` behavior remain unchanged; only the `instructions` text grows richer.

- **Airtable and API integration:**
  - `AirtableClient.write_assessment()` continues to serialize `AssessmentResult` into Airtable long-text fields; more structured and legible `summary`, flags, and counterfactuals yield more compelling records in the demo UI with no integration changes.
  - Both Flask (`demo/app.py`) and AgentOS (`demo/agentos_app.py`) entrypoints continue to treat `AssessmentResult` as an opaque structured payload; only the human-facing content improves.
