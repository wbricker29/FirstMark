#!/usr/bin/env python3
"""
Validate FirstMark case study deliverables before submission.

This script checks that all required deliverables are present and meet basic requirements.

Usage:
    python validate_deliverables.py --project ./my-case-study
"""

import argparse
from pathlib import Path
import sys


def check_file_exists(filepath: Path, description: str) -> bool:
    """Check if a file exists and print status."""
    exists = filepath.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {filepath}")
    return exists


def check_writeup(project_dir: Path) -> bool:
    """Check for writeup or slide deck."""
    print("\n1. Writeup or Slide Deck (1-2 pages)")

    # Look for common writeup files
    writeup_patterns = [
        "writeup.md",
        "case_study.md",
        "deliverable.md",
        "writeup.pdf",
        "case_study.pdf",
        "slides.pdf",
        "slides.pptx",
    ]

    found_files = []
    for pattern in writeup_patterns:
        matches = list(project_dir.glob(f"**/{pattern}"))
        found_files.extend(matches)

    if found_files:
        print(f"  ✓ Found writeup: {found_files[0]}")

        # Check file size/length for markdown
        if found_files[0].suffix == ".md":
            content = found_files[0].read_text()
            num_lines = len(content.split("\n"))
            word_count = len(content.split())

            print(f"    Lines: {num_lines}, Words: {word_count}")

            if word_count > 1500:
                print(
                    f"    ⚠️  Warning: {word_count} words might be too long for 1-2 pages"
                )
                print("        Target: ~500-1000 words for 1-2 pages")

        return True
    else:
        print("  ✗ No writeup found")
        print("    Expected: writeup.md, case_study.pdf, or slides.pptx")
        return False


def check_prototype(project_dir: Path) -> bool:
    """Check for Python prototype and requirements."""
    print("\n2. Python Prototype")

    checks = []

    # Check for main entry point
    main_files = (
        list(project_dir.glob("**/main.py"))
        + list(project_dir.glob("**/app.py"))
        + list(project_dir.glob("**/agent.py"))
    )

    if main_files:
        print(f"  ✓ Found main script: {main_files[0]}")
        checks.append(True)
    else:
        print("  ✗ No main.py, app.py, or agent.py found")
        checks.append(False)

    # Check for requirements.txt
    req_file = project_dir / "requirements.txt"
    if check_file_exists(req_file, "requirements.txt"):
        # Read and validate requirements
        content = req_file.read_text()
        if content.strip():
            print(f"    Dependencies listed: {len(content.strip().split())} packages")
            checks.append(True)
        else:
            print("    ⚠️  Warning: requirements.txt is empty")
            checks.append(False)
    else:
        checks.append(False)

    # Check for Python files
    py_files = list(project_dir.glob("**/*.py"))
    if py_files:
        print(f"  ✓ Found {len(py_files)} Python file(s)")
        checks.append(True)
    else:
        print("  ✗ No Python files found")
        checks.append(False)

    return all(checks)


def check_readme(project_dir: Path) -> bool:
    """Check for README."""
    print("\n3. README (Optional but Recommended)")

    readme_files = list(project_dir.glob("**/README.md")) + list(
        project_dir.glob("**/README.txt")
    )

    if readme_files:
        print(f"  ✓ Found README: {readme_files[0]}")

        content = readme_files[0].read_text()
        has_usage = "run" in content.lower() or "install" in content.lower()
        has_explanation = "implement" in content.lower() or "design" in content.lower()

        if has_usage:
            print("    ✓ Contains usage instructions")
        else:
            print("    ⚠️  Warning: Should include how to run the code")

        if has_explanation:
            print("    ✓ Contains implementation explanation")
        else:
            print("    ⚠️  Warning: Should explain what's implemented")

        return True
    else:
        print("  ⚠️  No README found (optional but strongly recommended)")
        return False


def check_mock_data(project_dir: Path) -> bool:
    """Check for mock data files."""
    print("\n4. Mock Data Files")

    required_files = {
        "mock_guilds.csv": "Guild members CSV",
        "exec_network.csv": "Extended network CSV",
        "open_roles.csv": "Open roles CSV",
        "executive_bios.json": "Executive bios JSON",
    }

    checks = []
    for filename, description in required_files.items():
        matches = list(project_dir.glob(f"**/{filename}"))
        if matches:
            print(f"  ✓ {description}: {matches[0]}")
            checks.append(True)
        else:
            print(f"  ✗ {description}: {filename} not found")
            checks.append(False)

    # Check for job descriptions directory
    jd_dirs = list(project_dir.glob("**/job_descriptions"))
    if jd_dirs and jd_dirs[0].is_dir():
        jd_files = list(jd_dirs[0].glob("*.txt"))
        print(f"  ✓ Job descriptions: {len(jd_files)} file(s) in {jd_dirs[0]}")
        checks.append(True)
    else:
        print("  ✗ Job descriptions: job_descriptions/ directory not found")
        checks.append(False)

    return all(checks)


def check_rubric_coverage(project_dir: Path) -> bool:
    """Check if writeup addresses rubric criteria."""
    print("\n5. Rubric Coverage Check")

    writeup_files = list(project_dir.glob("**/*.md")) + list(
        project_dir.glob("**/*writeup*.pdf")
    )

    if not writeup_files:
        print("  ⚠️  Cannot check rubric coverage - no writeup found")
        return False

    # For markdown files, do simple keyword checking
    if writeup_files[0].suffix == ".md":
        content = writeup_files[0].read_text().lower()

        criteria = {
            "Product Thinking": ["guild", "firstmark", "talent team", "workflow"],
            "Technical Design": ["architecture", "design", "pattern", "llm"],
            "Data Integration": ["structured", "unstructured", "data", "csv"],
            "Insight Generation": ["ranking", "score", "reasoning", "match"],
            "Communication": ["tradeoff", "decision", "production"],
        }

        print("  Checking for rubric criteria keywords:")
        for criterion, keywords in criteria.items():
            found = sum(1 for kw in keywords if kw in content)
            status = "✓" if found >= 2 else "⚠️ "
            print(f"    {status} {criterion}: {found}/{len(keywords)} keywords found")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Validate FirstMark case study deliverables"
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path("."),
        help="Project directory to validate (default: current directory)",
    )

    args = parser.parse_args()

    if not args.project.exists():
        print(f"Error: Project directory not found: {args.project}")
        sys.exit(1)

    print("=" * 60)
    print("FirstMark Case Study Deliverables Validation")
    print("=" * 60)
    print(f"\nProject directory: {args.project.absolute()}\n")

    results = []

    # Run all checks
    results.append(("Writeup/Slides", check_writeup(args.project)))
    results.append(("Python Prototype", check_prototype(args.project)))
    results.append(("README", check_readme(args.project)))
    results.append(("Mock Data", check_mock_data(args.project)))
    results.append(("Rubric Coverage", check_rubric_coverage(args.project)))

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} checks passed")

    if passed == total:
        print("\n✓ All checks passed! Your deliverables look good.")
        print("  Review everything one more time before submitting.")
        sys.exit(0)
    else:
        print("\n⚠️  Some checks failed. Please review and fix before submitting.")
        print("  See details above for what's missing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
