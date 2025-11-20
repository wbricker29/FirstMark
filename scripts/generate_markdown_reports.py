#!/usr/bin/env python3
"""
Generate Markdown reports from workflow research content in SQLite database.

This script extracts research and assessment data from the Agno workflow sessions
and generates comprehensive Markdown reports for each candidate screening.

Usage:
    python scripts/generate_markdown_reports.py
    # or with uv:
    uv run python scripts/generate_markdown_reports.py
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def parse_timestamp(timestamp: int) -> str:
    """Convert Unix timestamp to readable date string."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def extract_candidate_info(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract candidate information from session data."""
    workflow_data = session_data.get("session_state", {}).get("workflow_data", {})
    candidate = workflow_data.get("candidate", {})

    return {
        "name": candidate.get("name", "Unknown"),
        "title": candidate.get("title", ""),
        "company": candidate.get("company", ""),
        "linkedin": candidate.get("linkedin", ""),
        "location": candidate.get("location", ""),
        "bio": candidate.get("bio", ""),
    }


def extract_research_data(session_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract research data from session data."""
    workflow_data = session_data.get("session_state", {}).get("workflow_data", {})
    return workflow_data.get("research")


def extract_assessment_data(runs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Extract assessment data from workflow runs."""
    if not runs:
        return None

    # Get the most recent run
    latest_run = runs[-1]
    content = latest_run.get("content", {})
    return content.get("assessment")


def format_score_bar(score: Optional[int]) -> str:
    """Create a visual score bar."""
    if score is None:
        return "─────"
    filled = "█" * score
    empty = "░" * (5 - score)
    return f"{filled}{empty}"


def generate_markdown_report(
    session_id: str,
    candidate_info: Dict[str, Any],
    research: Optional[Dict[str, Any]],
    assessment: Optional[Dict[str, Any]],
    role_spec: str,
    created_at: int,
) -> str:
    """Generate a comprehensive Markdown report."""

    report_lines = []

    # Header
    report_lines.append(f"# Executive Assessment Report: {candidate_info['name']}")
    report_lines.append("")
    report_lines.append(f"**Session ID:** `{session_id}`")
    report_lines.append(f"**Generated:** {parse_timestamp(created_at)}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # Executive Summary
    if assessment:
        report_lines.append("## Executive Summary")
        report_lines.append("")
        overall_score = assessment.get("overall_score", 0)
        overall_confidence = assessment.get("overall_confidence", "Unknown")

        # Score visualization
        score_pct = int(overall_score)
        report_lines.append(f"**Overall Score:** {overall_score}/100 ({score_pct}%)")
        report_lines.append(f"**Confidence Level:** {overall_confidence}")
        report_lines.append("")

        # Progress bar
        bars = int(score_pct / 5)
        progress = "█" * bars + "░" * (20 - bars)
        report_lines.append("```")
        report_lines.append(f"{progress} {score_pct}%")
        report_lines.append("```")
        report_lines.append("")

        # Summary text
        summary = assessment.get("summary", "No summary available.")
        report_lines.append("### Summary")
        report_lines.append("")
        report_lines.append(summary)
        report_lines.append("")

    report_lines.append("---")
    report_lines.append("")

    # Candidate Information
    report_lines.append("## Candidate Profile")
    report_lines.append("")
    report_lines.append(f"**Name:** {candidate_info['name']}")
    if candidate_info["title"]:
        report_lines.append(f"**Current Title:** {candidate_info['title']}")
    if candidate_info["company"]:
        report_lines.append(f"**Current Company:** {candidate_info['company']}")
    if candidate_info["location"]:
        report_lines.append(f"**Location:** {candidate_info['location']}")
    if candidate_info["linkedin"]:
        report_lines.append(f"**LinkedIn:** {candidate_info['linkedin']}")
    report_lines.append("")

    # Research Summary
    if research:
        report_lines.append("## Research Summary")
        report_lines.append("")

        report_lines.append(
            f"**Research Model:** {research.get('research_model', 'Unknown')}"
        )
        report_lines.append(
            f"**Research Timestamp:** {research.get('research_timestamp', 'Unknown')}"
        )
        report_lines.append(
            f"**Confidence:** {research.get('research_confidence', 'Unknown')}"
        )
        report_lines.append("")

        # Career Timeline
        career_timeline = research.get("career_timeline", [])
        if career_timeline:
            report_lines.append("### Career Timeline")
            report_lines.append("")
            for role in career_timeline:
                company = role.get("company", "Unknown")
                role_title = role.get("role", "Unknown")
                start = role.get("start_date", "Unknown")
                end = role.get("end_date", "Present")
                report_lines.append(f"#### {role_title} at {company}")
                report_lines.append(f"*{start} - {end}*")
                report_lines.append("")
                achievements = role.get("key_achievements", [])
                if achievements:
                    for achievement in achievements:
                        report_lines.append(f"- {achievement}")
                report_lines.append("")

        # Experience Summary
        report_lines.append("### Experience Highlights")
        report_lines.append("")
        if research.get("total_years_experience"):
            report_lines.append(
                f"**Total Years of Experience:** {research.get('total_years_experience')}"
            )
            report_lines.append("")

        if research.get("fundraising_experience"):
            report_lines.append(
                f"**Fundraising:** {research.get('fundraising_experience')}"
            )
            report_lines.append("")

        if research.get("operational_finance_experience"):
            report_lines.append(
                f"**Operational Finance:** {research.get('operational_finance_experience')}"
            )
            report_lines.append("")

        # Sector Expertise
        sectors = research.get("sector_expertise", [])
        if sectors:
            report_lines.append(f"**Sector Expertise:** {', '.join(sectors)}")
            report_lines.append("")

        # Stage Exposure
        stages = research.get("stage_exposure", [])
        if stages:
            report_lines.append(f"**Stage Exposure:** {', '.join(stages)}")
            report_lines.append("")

        # Research Gaps
        gaps = research.get("gaps", [])
        if gaps:
            report_lines.append("### Research Gaps & Limitations")
            report_lines.append("")
            for gap in gaps:
                report_lines.append(f"- {gap}")
            report_lines.append("")

    report_lines.append("---")
    report_lines.append("")

    # Assessment Details
    if assessment:
        report_lines.append("## Detailed Assessment")
        report_lines.append("")

        # Role Specification
        report_lines.append("### Role Requirements")
        report_lines.append("")
        report_lines.append(role_spec)
        report_lines.append("")

        # Dimension Scores
        dimension_scores = assessment.get("dimension_scores", [])
        if dimension_scores:
            report_lines.append("### Dimension Scores")
            report_lines.append("")

            for dim in dimension_scores:
                dimension_name = dim.get("dimension", "Unknown")
                score = dim.get("score", 0)
                confidence = dim.get("confidence", "Unknown")
                evidence_level = dim.get("evidence_level", "Unknown")

                report_lines.append(f"#### {dimension_name}")
                report_lines.append("")
                if score is not None:
                    report_lines.append(
                        f"**Score:** {score}/5 {format_score_bar(score)}"
                    )
                else:
                    report_lines.append(f"**Score:** Unknown {format_score_bar(None)}")
                report_lines.append(
                    f"**Confidence:** {confidence} | **Evidence Level:** {evidence_level}"
                )
                report_lines.append("")

                # Reasoning
                reasoning = dim.get("reasoning", "No reasoning provided.")
                report_lines.append("**Reasoning:**")
                report_lines.append("")
                report_lines.append(reasoning)
                report_lines.append("")

                # Evidence Quotes
                evidence_quotes = dim.get("evidence_quotes", [])
                if evidence_quotes:
                    report_lines.append("**Evidence Quotes:**")
                    report_lines.append("")
                    for quote in evidence_quotes:
                        report_lines.append(f"> {quote}")
                    report_lines.append("")

                # Citation URLs
                citation_urls = dim.get("citation_urls", [])
                if citation_urls:
                    report_lines.append("**Citations:**")
                    report_lines.append("")
                    for url in citation_urls:
                        report_lines.append(f"- {url}")
                    report_lines.append("")

        # Must-Haves Check
        must_haves = assessment.get("must_haves_check", [])
        if must_haves:
            report_lines.append("### Must-Haves Assessment")
            report_lines.append("")
            for req in must_haves:
                requirement = req.get("requirement", "Unknown")
                met = req.get("met", False)
                evidence = req.get("evidence", "No evidence provided.")

                status = "✅ MET" if met else "❌ NOT MET"
                report_lines.append(f"**{requirement}:** {status}")
                report_lines.append("")
                report_lines.append(evidence)
                report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

        # Red Flags
        red_flags = assessment.get("red_flags_detected", [])
        if red_flags:
            report_lines.append("## 🚨 Red Flags")
            report_lines.append("")
            for flag in red_flags:
                report_lines.append(f"- {flag}")
            report_lines.append("")

        # Green Flags
        green_flags = assessment.get("green_flags", [])
        if green_flags:
            report_lines.append("## ✅ Green Flags")
            report_lines.append("")
            for flag in green_flags:
                report_lines.append(f"- {flag}")
            report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

        # Counterfactuals
        counterfactuals = assessment.get("counterfactuals", [])
        if counterfactuals:
            report_lines.append("## Counterfactual Analysis")
            report_lines.append("")
            report_lines.append("*What could change this assessment?*")
            report_lines.append("")
            for cf in counterfactuals:
                report_lines.append(f"- {cf}")
            report_lines.append("")

    # Research Citations
    if research:
        citations = research.get("citations", [])
        if citations:
            report_lines.append("---")
            report_lines.append("")
            report_lines.append("## Research Citations")
            report_lines.append("")
            for i, citation in enumerate(citations, 1):
                title = citation.get("title", "Untitled")
                url = citation.get("url", "")
                snippet = citation.get("snippet", "")
                relevance = citation.get("relevance_note", "")

                report_lines.append(f"### [{i}] {title}")
                report_lines.append("")
                if url:
                    report_lines.append(f"**URL:** {url}")
                if snippet:
                    report_lines.append(f"**Snippet:** {snippet}")
                if relevance:
                    report_lines.append(f"**Relevance:** {relevance}")
                report_lines.append("")

    # Footer
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("*Report generated by Talent Signal Agent*")
    report_lines.append("")

    return "\n".join(report_lines)


def main():
    """Main execution function."""
    # Configuration
    db_path = Path("tmp/agno_sessions.db")
    output_dir = Path("reports/candidate_assessments")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Connecting to database: {db_path}")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all workflow sessions
    cursor.execute("""
        SELECT session_id, workflow_id, session_data, runs, created_at
        FROM workflow_session
        ORDER BY created_at DESC
    """)

    sessions = cursor.fetchall()
    print(f"📊 Found {len(sessions)} workflow sessions")
    print()

    if not sessions:
        print("⚠️  No sessions found in database")
        conn.close()
        return

    # Process each session
    reports_generated = 0
    for session_id, workflow_id, session_data_json, runs_json, created_at in sessions:
        try:
            print(f"📝 Processing session: {session_id}")

            # Parse JSON data (handle double-encoding)
            session_data = json.loads(session_data_json)
            if isinstance(session_data, str):
                session_data = json.loads(session_data)

            runs = json.loads(runs_json)
            if isinstance(runs, str):
                runs = json.loads(runs)

            # Extract data
            candidate_info = extract_candidate_info(session_data)
            research = extract_research_data(session_data)
            assessment = extract_assessment_data(runs)

            # Get role spec
            workflow_data = session_data.get("session_state", {}).get(
                "workflow_data", {}
            )
            role_spec = workflow_data.get(
                "role_spec_markdown", "Role specification not available."
            )

            # Generate report
            report_content = generate_markdown_report(
                session_id=session_id,
                candidate_info=candidate_info,
                research=research,
                assessment=assessment,
                role_spec=role_spec,
                created_at=created_at,
            )

            # Save report
            candidate_name = candidate_info["name"].replace(" ", "_").replace("/", "-")
            timestamp = datetime.fromtimestamp(created_at).strftime("%Y%m%d_%H%M%S")
            filename = f"{candidate_name}_{timestamp}.md"
            output_path = output_dir / filename

            output_path.write_text(report_content)

            print(f"   ✅ Generated report: {filename}")
            print(f"   📍 Location: {output_path}")

            # Print summary stats
            if assessment:
                overall_score = assessment.get("overall_score", 0)
                confidence = assessment.get("overall_confidence", "Unknown")
                print(f"   📊 Score: {overall_score}/100 (Confidence: {confidence})")

            print()
            reports_generated += 1

        except Exception as e:
            import traceback

            print(f"   ❌ Error processing session {session_id}: {e}")
            print("   Traceback:")
            traceback.print_exc()
            print()
            continue

    conn.close()

    print("=" * 70)
    print("✨ Report generation complete!")
    print(f"📁 Generated {reports_generated} reports in: {output_dir.absolute()}")
    print()


if __name__ == "__main__":
    main()
