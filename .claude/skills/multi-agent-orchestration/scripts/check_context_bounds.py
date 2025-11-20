#!/usr/bin/env python3
"""
Monitor token usage during multi-agent orchestration.

Estimates context consumption from files and warns when approaching
model context limits (200k tokens).
"""

import json
import argparse
import sys
from pathlib import Path


# Constants for token limits
TOKEN_LIMIT = 200000
WARNING_THRESHOLD = 0.75  # 150k tokens (75%)
CRITICAL_THRESHOLD = 0.90  # 180k tokens (90%)
CHARS_PER_TOKEN = 4  # Rough approximation


def estimate_tokens(character_count: int) -> int:
    """
    Estimate token count from character count.

    Uses rough approximation of ~4 characters per token.

    Args:
        character_count: Number of characters

    Returns:
        Estimated token count
    """
    return character_count // CHARS_PER_TOKEN


def read_file_content(file_path: str) -> tuple[int, str | None]:
    """
    Read file and return character count and error message if failed.

    Args:
        file_path: Path to file to read

    Returns:
        Tuple of (character_count, error_message)
        error_message is None if successful
    """
    path = Path(file_path).expanduser()

    if not path.exists():
        return 0, f"File not found: {file_path}"

    if not path.is_file():
        return 0, f"Not a file: {file_path}"

    try:
        content = path.read_text(encoding="utf-8")
        return len(content), None
    except UnicodeDecodeError:
        return 0, f"File is not text: {file_path}"
    except Exception as e:
        return 0, f"Error reading file: {str(e)}"


def get_status(percentage_used: float) -> str:
    """
    Determine status based on percentage of context used.

    Args:
        percentage_used: Percentage of context limit used (0-100)

    Returns:
        Status string: "ok", "warning", or "critical"
    """
    if percentage_used >= CRITICAL_THRESHOLD * 100:
        return "critical"
    elif percentage_used >= WARNING_THRESHOLD * 100:
        return "warning"
    else:
        return "ok"


def generate_recommendations(percentage_used: float, tokens: int) -> list[str]:
    """
    Generate recommendations based on token usage.

    Args:
        percentage_used: Percentage of context used
        tokens: Estimated token count

    Returns:
        List of recommendation strings
    """
    recommendations = []

    if percentage_used >= CRITICAL_THRESHOLD * 100:
        recommendations.append(
            "CRITICAL: Context approaching limit. Break work into smaller phases."
        )
        recommendations.append(
            "Reduce context files or summarize content to free capacity."
        )
    elif percentage_used >= WARNING_THRESHOLD * 100:
        recommendations.append(
            "WARNING: Context usage at 75%. Consider chunking large tasks."
        )
        recommendations.append("Review which files are essential or can be summarized.")

    if tokens > TOKEN_LIMIT:
        recommendations.append(
            f"Currently {tokens:,} tokens (limit: {TOKEN_LIMIT:,}). "
            "Split into multiple orchestration cycles."
        )

    return recommendations


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Monitor token usage during multi-agent orchestration"
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3, 4, 5],
        required=True,
        help="Orchestration phase (1-5)",
    )
    parser.add_argument(
        "--files", default=None, help="Comma-separated list of file paths to analyze"
    )

    args = parser.parse_args()

    # Initialize counters
    total_chars = 0
    file_errors = []

    # Process files if provided
    if args.files:
        file_paths = [f.strip() for f in args.files.split(",") if f.strip()]

        for file_path in file_paths:
            char_count, error = read_file_content(file_path)

            if error:
                file_errors.append(error)
            else:
                total_chars += char_count

    # Estimate tokens
    estimated_tokens = estimate_tokens(total_chars)

    # Calculate percentage
    percentage_used = (estimated_tokens / TOKEN_LIMIT) * 100

    # Determine status
    status = get_status(percentage_used)

    # Generate recommendations
    recommendations = generate_recommendations(percentage_used, estimated_tokens)

    # Build report
    report = {
        "phase": args.phase,
        "estimated_tokens": estimated_tokens,
        "token_limit": TOKEN_LIMIT,
        "percentage_used": round(percentage_used, 2),
        "status": status,
        "recommendations": recommendations,
    }

    # Add file errors if any
    if file_errors:
        report["file_errors"] = file_errors

    # Output JSON report
    print(json.dumps(report, indent=2))

    # Return appropriate exit code
    if status == "critical":
        return 2
    elif status == "warning":
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
