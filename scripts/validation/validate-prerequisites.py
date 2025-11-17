#!/usr/bin/env python3
"""
Pre-flight validator for /work command execution.

Validates all Phase 1 (UNDERSTAND) prerequisites before loading context:
- Unit directory exists
- Required files exist (plan.md, design.md, spec.md, constitution.md)
- Task ID exists with valid status
- All dependencies are complete

Exit codes:
- 0: All validations passed
- 1: Validation failed (descriptive error to stderr)

Output: JSON with task metadata on success
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


class ValidationError(Exception):
    """Custom exception for validation failures."""

    pass


def find_project_root() -> Path:
    """Find project root by looking for spec/ directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "spec").is_dir():
            return current
        current = current.parent
    raise ValidationError("Could not find project root (no spec/ directory found)")


def validate_file_structure(unit_path: Path) -> Dict[str, bool]:
    """Validate that required files exist in unit directory.

    Args:
        unit_path: Path to unit directory (e.g., spec/units/001-phase-1)

    Returns:
        Dict mapping filename to existence status

    Raises:
        ValidationError: If unit directory doesn't exist
    """
    if not unit_path.is_dir():
        raise ValidationError(f"Unit directory not found: {unit_path}")

    required_files = {
        "plan.md": unit_path / "plan.md",
        "design.md": unit_path / "design.md",
    }

    # spec.md and constitution.md are at project root
    project_root = find_project_root()
    required_files["spec.md"] = project_root / "spec" / "spec.md"
    required_files["constitution.md"] = project_root / "spec" / "constitution.md"

    file_status = {}
    missing_files = []

    for name, path in required_files.items():
        exists = path.is_file()
        file_status[name] = exists
        if not exists:
            missing_files.append(str(path))

    if missing_files:
        raise ValidationError(
            "Missing required files:\n  " + "\n  ".join(missing_files)
        )

    return file_status


def parse_task_from_plan(plan_path: Path, task_id: str) -> Dict[str, any]:
    """Extract task metadata from plan.md.

    Args:
        plan_path: Path to plan.md
        task_id: Task ID (e.g., "TK-01")

    Returns:
        Dict with task metadata (title, description, status, dependencies, files, etc.)

    Raises:
        ValidationError: If task not found or invalid
    """
    with open(plan_path, "r") as f:
        content = f.read()

    # Find task section (### TK-##: Title OR ### TK-##)
    # Try format with title first
    task_pattern_with_title = rf"###\s+{re.escape(task_id)}:\s+(.+?)$"
    task_match = re.search(task_pattern_with_title, content, re.MULTILINE)

    # If not found, try format without title
    if not task_match:
        task_pattern_no_title = rf"###\s+{re.escape(task_id)}\s*$"
        task_match = re.search(task_pattern_no_title, content, re.MULTILINE)

    if not task_match:
        # List available tasks for helpful error
        available_tasks = re.findall(r"###\s+(TK-\d+)", content)
        raise ValidationError(
            f"Task {task_id} not found in plan.md\n"
            f"Available tasks: {', '.join(available_tasks) if available_tasks else 'None'}"
        )

    # Extract task section (from ### TK-## to next ### or end)
    task_start = task_match.start()
    next_task_match = re.search(r"\n###\s+TK-\d+", content[task_start + 1 :])
    task_end = task_start + next_task_match.start() if next_task_match else len(content)
    task_section = content[task_start:task_end]

    # Parse task metadata
    task_data = {
        "id": task_id,
        "title": task_match.group(1).strip() if task_match.lastindex else None,
    }

    # Extract fields using regex
    field_patterns = {
        "title": r"- \*\*Title:\*\*\s+(.+?)(?=\n|$)",
        "description": r"- \*\*Description:\*\*\s+(.+?)(?=\n- \*\*|\n###|\Z)",
        "status": r"- \*\*Status:\*\*\s+(\w+)",
        "priority": r"- \*\*Priority:\*\*\s+(\w+)",
        "estimate": r"- \*\*Estimate:\*\*\s+(.+?)(?=\n|$)",
        "dependencies": r"- \*\*Dependencies:\*\*\s+(.+?)(?=\n|$)",
        "acceptance_criteria": r"- \*\*Acceptance Criteria:\*\*\s+(.+?)(?=\n|$)",
        "note": r"- \*\*Note:\*\*\s+(.+?)(?=\n|$)",
        "completed": r"- \*\*Completed:\*\*\s+(.+?)(?=\n|$)",
    }

    for field, pattern in field_patterns.items():
        match = re.search(pattern, task_section, re.DOTALL)
        extracted_value = match.group(1).strip() if match else None
        # Use extracted title if header didn't have one
        if field == "title" and extracted_value:
            task_data["title"] = extracted_value
        elif field != "title":
            task_data[field] = extracted_value

    # Parse file list
    files_match = re.search(r"- \*\*Files:\*\*\s*\n((?:  - `.+?`\n?)+)", task_section)
    if files_match:
        files_text = files_match.group(1)
        task_data["files"] = [
            line.strip().strip("`").strip("- ")
            for line in files_text.split("\n")
            if line.strip()
        ]
    else:
        task_data["files"] = []

    return task_data


def validate_task_status(task_data: Dict[str, any]) -> None:
    """Validate task status is valid for execution.

    Args:
        task_data: Task metadata dict

    Raises:
        ValidationError: If task status is invalid
    """
    status = task_data.get("status")
    valid_statuses = ["ready", "doing"]

    if status == "done":
        raise ValidationError(
            f"Task {task_data['id']} is already complete (status: done)\n"
            f"If you want to re-run it, manually change status to 'ready' in plan.md"
        )

    if status not in valid_statuses:
        raise ValidationError(
            f"Task {task_data['id']} has invalid status: {status}\n"
            f"Valid statuses for execution: {', '.join(valid_statuses)}"
        )


def validate_dependencies(task_data: Dict[str, any], plan_path: Path) -> List[str]:
    """Validate all task dependencies are complete.

    Args:
        task_data: Task metadata dict
        plan_path: Path to plan.md (to check dependency statuses)

    Returns:
        List of dependency task IDs

    Raises:
        ValidationError: If any dependencies are incomplete
    """
    dependencies_field = task_data.get("dependencies", "").strip()

    # Handle "None" or empty dependencies
    if not dependencies_field or dependencies_field.lower() == "none":
        return []

    # Parse dependency list (e.g., "TK-01, TK-02" or "TK-01")
    dependency_ids = [
        dep.strip()
        for dep in re.split(r"[,\s]+", dependencies_field)
        if dep.strip() and dep.strip().startswith("TK-")
    ]

    if not dependency_ids:
        return []

    # Check each dependency status
    incomplete_deps = []
    with open(plan_path, "r") as f:
        plan_content = f.read()

    for dep_id in dependency_ids:
        try:
            dep_task = parse_task_from_plan(plan_path, dep_id)
            if dep_task.get("status") != "done":
                incomplete_deps.append(f"{dep_id} (status: {dep_task.get('status')})")
        except ValidationError:
            incomplete_deps.append(f"{dep_id} (not found)")

    if incomplete_deps:
        raise ValidationError(
            f"Task {task_data['id']} has incomplete dependencies:\n  "
            + "\n  ".join(incomplete_deps)
            + "\n\nComplete these dependencies first before running this task."
        )

    return dependency_ids


def validate_prerequisites(slug: str, task_id: str) -> Dict[str, any]:
    """Run all validation checks and return task metadata.

    Args:
        slug: Unit slug (e.g., "phase-1")
        task_id: Task ID (e.g., "TK-01")

    Returns:
        Dict with validation results and task metadata

    Raises:
        ValidationError: If any validation fails
    """
    project_root = find_project_root()

    # Find unit directory (supports both ###-slug and slug formats)
    units_dir = project_root / "spec" / "units"

    # Try to find matching unit directory
    matching_units = list(units_dir.glob(f"*{slug}"))
    if not matching_units:
        matching_units = list(units_dir.glob(slug))

    if not matching_units:
        available_units = [d.name for d in units_dir.iterdir() if d.is_dir()]
        raise ValidationError(
            f"No unit directory found matching slug: {slug}\n"
            f"Available units: {', '.join(available_units) if available_units else 'None'}"
        )

    if len(matching_units) > 1:
        raise ValidationError(
            f"Multiple unit directories match slug '{slug}': "
            + ", ".join(str(u.name) for u in matching_units)
        )

    unit_path = matching_units[0]
    plan_path = unit_path / "plan.md"

    # Run validations
    file_status = validate_file_structure(unit_path)
    task_data = parse_task_from_plan(plan_path, task_id)
    validate_task_status(task_data)
    dependencies = validate_dependencies(task_data, plan_path)

    # Return comprehensive metadata
    return {
        "validation": "passed",
        "unit_path": str(unit_path),
        "unit_id": unit_path.name,
        "task": task_data,
        "dependencies": dependencies,
        "files_validated": file_status,
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate /work command prerequisites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s phase-1 TK-01
  %(prog)s 001-phase-1 TK-02
  %(prog)s agent-implementation TK-03

Exit codes:
  0 - All validations passed (JSON output to stdout)
  1 - Validation failed (error message to stderr)
        """,
    )
    parser.add_argument(
        "slug", help="Unit slug or ID (e.g., 'phase-1' or '001-phase-1')"
    )
    parser.add_argument("task_id", help="Task ID (e.g., 'TK-01')")
    parser.add_argument(
        "--json", action="store_true", help="Output JSON only (no pretty print)"
    )

    args = parser.parse_args()

    try:
        result = validate_prerequisites(args.slug, args.task_id)

        if args.json:
            print(json.dumps(result))
        else:
            print(json.dumps(result, indent=2))

        return 0

    except ValidationError as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
