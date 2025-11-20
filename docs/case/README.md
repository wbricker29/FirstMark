# Case Folder Overview

This folder contains the core working documents for the FirstMark Talent Signal Agent case. Use this as a map so you know where to look (and what is canonical) as you prep and iterate.

## Core Documents

- `case_requirements.md`  
  - Clean extraction of the original FirstMark case brief.  
  - Use this to re-anchor on the problem, constraints, and evaluation rubric.

- `solution_strategy.md`  
  - Strategic framing of how you’re attacking the case (Ingest → Match → Explain, guiding principles, major tradeoffs).  
  - Read after `case_requirements.md` when you want the “why” behind the solution.

- `technical_spec_V2.md`  
  - **Canonical technical implementation spec for the current demo.**  
  - Defines the Airtable + Flask + AGNO architecture, modules (especially Module 4: Screen), data models, agents, and execution flow.  
  - Treat this as the source of truth when writing or modifying demo code.

- `presentation_plan.md`  
  - Narrative and flow for the 60‑minute interview session (intro, case story, demo beats, Q&A).  
  - Use this to align the live walkthrough with what the demo actually implements.

- `tracking.md`  
  - Implementation checklist and status tracker for the case and demo.  
  - Use this to decide what to work on next and to keep the spec and reality in sync.

## Archive

- `archive/`  
  - Historical and working docs: original case PDF, older tech specs, and multiple versions of WB’s case notes (`WB-case_notes.md`, `wbcasenotes_*`).  
  - Safe to mine for ideas and prior thinking; avoid editing these directly—create new notes in `case/` instead.

## Note on the Case Brief

- The detailed narrative case brief currently lives in `reference/case_brief.md`.  
- Over time, you can either mirror or move the “final interview” narrative into `case/` (e.g., as `case_brief.md`) so this folder fully owns both the **story** and the **implementation**.***
