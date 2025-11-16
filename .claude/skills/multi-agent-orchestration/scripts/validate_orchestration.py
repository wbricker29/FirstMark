#!/usr/bin/env python3
"""
Pre-flight validation for multi-agent orchestration workflows.

Validates that task scope is clearly defined, context files exist, and
context bounds are manageable before deploying sub-agents.
"""

import json
import argparse
import sys
from pathlib import Path


def validate_scope(scope: str) -> tuple[bool, list[str]]:
    """
    Validate that scope is clearly defined.

    Args:
        scope: Task scope description

    Returns:
        Tuple of (is_valid, warnings)
    """
    warnings = []

    # Check if scope is empty
    if not scope or not scope.strip():
        return False, ["Scope cannot be empty"]

    # Check minimum length
    if len(scope) < 10:
        warnings.append("Scope is very brief (<10 chars) - consider more detail")

    # Check if scope is excessively large
    if len(scope) > 500:
        warnings.append(
            "Scope is large (>500 chars) - consider chunking into smaller sub-tasks"
        )

    return True, warnings


def validate_context_files(file_paths: list[str]) -> tuple[list[bool], list[str]]:
    """
    Validate that context files exist.

    Args:
        file_paths: List of file paths to check

    Returns:
        Tuple of (existence_list, missing_files)
    """
    existence = []
    missing = []

    for file_path in file_paths:
        path = Path(file_path).expanduser()
        exists = path.exists()
        existence.append(exists)

        if not exists:
            missing.append(file_path)

    return existence, missing


def estimate_complexity(scope: str) -> int:
    """
    Estimate basic dependency complexity.

    Args:
        scope: Task scope description

    Returns:
        Estimated number of sub-tasks (comma-separated items in scope)
    """
    # Count comma-separated items as a rough complexity metric
    items = [item.strip() for item in scope.split(",") if item.strip()]
    return len(items)


def validate_dependencies(dependencies: str) -> tuple[bool, list[str]]:
    """
    Validate that dependencies are acyclic.

    Args:
        dependencies: Dependency specification (e.g., "A->B,B->C")

    Returns:
        Tuple of (is_acyclic, warnings)
    """
    warnings = []

    if not dependencies or not dependencies.strip():
        return True, []

    # Parse dependencies into adjacency list
    edges = []
    for dep in dependencies.split(","):
        dep = dep.strip()
        if "->" in dep:
            parts = dep.split("->")
            if len(parts) == 2:
                from_node = parts[0].strip()
                to_node = parts[1].strip()
                if from_node and to_node:
                    edges.append((from_node, to_node))

    if not edges:
        return True, []

    # Build adjacency list
    graph = {}
    for from_node, to_node in edges:
        if from_node not in graph:
            graph[from_node] = []
        graph[from_node].append(to_node)
        if to_node not in graph:
            graph[to_node] = []

    # Detect cycles using DFS
    visited = set()
    rec_stack = set()

    def has_cycle(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    # Check for cycles
    for node in graph:
        if node not in visited:
            if has_cycle(node):
                warnings.append(
                    "Cyclic dependency detected - dependencies must be acyclic"
                )
                return False, warnings

    return True, warnings


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate orchestration configuration before deploying sub-agents"
    )
    parser.add_argument(
        "--scope",
        required=True,
        help="Task scope description (clearly define what agents should do)",
    )
    parser.add_argument(
        "--context-files",
        default=None,
        help="Comma-separated list of context file paths to validate",
    )
    parser.add_argument(
        "--dependencies",
        default=None,
        help="Comma-separated dependency specifications (e.g., 'A->B,B->C')",
    )

    args = parser.parse_args()

    # Validate scope
    scope_valid, scope_warnings = validate_scope(args.scope)

    # Validate context files if provided
    context_files_exist = []
    context_warnings = []
    if args.context_files:
        file_paths = [f.strip() for f in args.context_files.split(",") if f.strip()]
        context_files_exist, missing_files = validate_context_files(file_paths)
        if missing_files:
            context_warnings.append(
                f"Missing context files: {', '.join(missing_files)}"
            )

    # Validate dependencies if provided
    dependencies_valid = True
    dependency_warnings = []
    if args.dependencies:
        dependencies_valid, dependency_warnings = validate_dependencies(
            args.dependencies
        )

    # Estimate complexity
    complexity = estimate_complexity(args.scope)

    # Build recommendations
    recommendations = []
    if not scope_valid:
        recommendations.append("Refine scope definition before proceeding")
    if not dependencies_valid:
        recommendations.append(
            "Resolve cyclic dependencies before deploying sub-agents"
        )
    if complexity > 5:
        recommendations.append(
            f"Scope involves {complexity} sub-tasks - consider breaking into phases"
        )
    if args.context_files and (
        missing_files := [
            f
            for f, exists in zip(args.context_files.split(","), context_files_exist)
            if not exists
        ]
    ):
        recommendations.append(
            f"Locate missing files or update paths: {', '.join(missing_files)}"
        )

    # Combine all warnings
    all_warnings = scope_warnings + context_warnings + dependency_warnings

    # Build report
    report = {
        "valid": scope_valid
        and dependencies_valid
        and (all(context_files_exist) if context_files_exist else True),
        "scope_defined": scope_valid,
        "context_files_exist": context_files_exist,
        "dependencies_acyclic": dependencies_valid,
        "complexity_estimate": complexity,
        "warnings": all_warnings,
        "recommendations": recommendations,
    }

    # Output JSON report
    print(json.dumps(report, indent=2))

    # Return exit code
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
