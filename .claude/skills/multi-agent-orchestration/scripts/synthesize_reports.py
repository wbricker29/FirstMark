#!/usr/bin/env python3
"""
Generate synthesis reports from sub-agent orchestration outputs.

Creates structured markdown or JSON reports summarizing agent completion,
deliverables, and validation results.
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path


def load_template(template_path: str) -> str:
    """
    Load report template from file.

    Args:
        template_path: Path to template file

    Returns:
        Template content as string
    """
    path = Path(template_path).expanduser()

    if not path.exists():
        # Return basic template if file doesn't exist
        return """# Multi-Agent Orchestration Report

## Deployed Agents
{agent_summaries}

## Deliverables
{deliverable_list_with_locations}

## Timestamp
{timestamp}

## Summary
Report generated from sub-agent orchestration output.
"""

    return path.read_text()


def substitute_template(template: str, variables: dict) -> str:
    """
    Substitute variables in template.

    Args:
        template: Template string with {variable} placeholders
        variables: Dictionary of variable -> value mappings

    Returns:
        Substituted template
    """
    result = template
    for key, value in variables.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, str(value))
    return result


def format_agent_summaries(agents: list[str]) -> str:
    """
    Format agent list as markdown bullet points.

    Args:
        agents: List of agent names

    Returns:
        Formatted markdown
    """
    if not agents:
        return "No agents deployed"

    lines = []
    for agent in agents:
        lines.append(f"- **{agent}**: Completed ✅")

    return "\n".join(lines)


def format_deliverables(deliverables: list[str]) -> str:
    """
    Format deliverable list as markdown bullet points.

    Args:
        deliverables: List of deliverable paths/descriptions

    Returns:
        Formatted markdown
    """
    if not deliverables:
        return "No deliverables produced"

    lines = []
    for deliverable in deliverables:
        lines.append(f"- `{deliverable}`")

    return "\n".join(lines)


def generate_json_report(
    agents: list[str], deliverables: list[str], timestamp: str
) -> dict:
    """
    Generate structured JSON report.

    Args:
        agents: List of agent names
        deliverables: List of deliverables
        timestamp: Report timestamp

    Returns:
        JSON-serializable dictionary
    """
    return {
        "timestamp": timestamp,
        "agents_deployed": agents,
        "deliverables": deliverables,
        "status": "completed",
        "validation": {
            "agents_count": len(agents),
            "deliverables_count": len(deliverables),
        },
    }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthesis reports from sub-agent orchestration outputs"
    )
    parser.add_argument(
        "--agents", required=True, help="Comma-separated list of agent names"
    )
    parser.add_argument(
        "--deliverables",
        required=True,
        help="Comma-separated list of deliverable paths/descriptions",
    )
    parser.add_argument(
        "--template",
        default=None,
        help="Path to template file (defaults to ../assets/synthesis-report.tmpl)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (if not provided, writes to stdout)",
    )

    args = parser.parse_args()

    # Parse input lists
    agents = [a.strip() for a in args.agents.split(",") if a.strip()]
    deliverables = [d.strip() for d in args.deliverables.split(",") if d.strip()]

    # Generate timestamp
    timestamp = datetime.now().isoformat()

    if args.format == "json":
        # Generate JSON report
        report = generate_json_report(agents, deliverables, timestamp)
        output = json.dumps(report, indent=2)
    else:
        # Generate markdown report
        if args.template:
            template_path = Path(args.template)
        else:
            template_path = (
                Path(__file__).parent.parent / "assets" / "synthesis-report.tmpl"
            )

        template = load_template(str(template_path))

        variables = {
            "agent_summaries": format_agent_summaries(agents),
            "deliverable_list_with_locations": format_deliverables(deliverables),
            "timestamp": timestamp,
        }

        output = substitute_template(template, variables)

    # Output to file or stdout
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
