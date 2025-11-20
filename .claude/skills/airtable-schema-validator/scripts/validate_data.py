#!/usr/bin/env python3
"""
Airtable Data Quality Validator

Validates data quality in Airtable People table after import.
Checks for duplicates, missing fields, invalid formats, and completeness.

Usage:
    python validate_data.py [--csv reference.csv] [--report output.txt] [--verbose]

Examples:
    python validate_data.py
    python validate_data.py --csv ../../../
    python validate_data.py --report quality_report.txt --verbose
"""

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional

# Import Airtable utilities
from airtable_utils import list_records  # noqa: F401

# Airtable configuration
BASE_ID = "appeY64iIwU5CEna7"
PEOPLE_TABLE_ID = "tblHqYymo3Av9hLeC"

# Validation rules
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
LINKEDIN_REGEX = re.compile(r"^https?://(?:www\.)?linkedin\.com/in/[\w-]+/?$")
VALID_FUNCTIONS = {"CFO", "CTO", "CPO", "CRO", "COO", "CMO", "CEO", "Other"}
VALID_SOURCES = {
    "FMGuildPage",
    "FMLinkedIN",
    "FMCFO",
    "FMCTOSummit",
    "FMFounder",
    "FMProduct",
}

# Required fields for completeness check
REQUIRED_FIELDS = ["Name", "Added Date"]
IMPORTANT_FIELDS = ["Title", "Company", "LinkedIn URL", "Normalized Title"]


class DataQualityReport:
    """Container for data quality validation results."""

    def __init__(self):
        self.total_records = 0
        self.complete_records = 0
        self.incomplete_records = 0
        self.duplicates: List[Tuple[str, int]] = []
        self.missing_required: List[str] = []
        self.missing_important: Dict[str, List[str]] = defaultdict(list)
        self.invalid_emails: List[str] = []
        self.invalid_linkedin: List[str] = []
        self.invalid_functions: List[str] = []
        self.invalid_sources: List[str] = []
        self.orphaned_records: List[str] = []
        self.csv_comparison: Optional[Dict[str, any]] = None

    def add_duplicate(self, name: str, count: int):
        """Add duplicate name to report."""
        self.duplicates.append((name, count))

    def add_missing_required(self, record_id: str, field: str):
        """Add missing required field."""
        self.missing_required.append(f"{record_id}: Missing {field}")

    def add_missing_important(self, field: str, record_id: str):
        """Add missing important field."""
        self.missing_important[field].append(record_id)

    def add_invalid_email(self, record_id: str, email: str):
        """Add invalid email format."""
        self.invalid_emails.append(f"{record_id}: {email}")

    def add_invalid_linkedin(self, record_id: str, url: str):
        """Add invalid LinkedIn URL."""
        self.invalid_linkedin.append(f"{record_id}: {url}")

    def add_invalid_function(self, record_id: str, function: str):
        """Add invalid function value."""
        self.invalid_functions.append(f"{record_id}: {function}")

    def add_invalid_source(self, record_id: str, source: str):
        """Add invalid source value."""
        self.invalid_sources.append(f"{record_id}: {source}")

    def add_orphaned(self, record_id: str):
        """Add orphaned record (no linked roles)."""
        self.orphaned_records.append(record_id)

    def set_csv_comparison(self, expected: int, loaded: int, missing: List[str]):
        """Set CSV comparison results."""
        self.csv_comparison = {
            "expected": expected,
            "loaded": loaded,
            "missing": missing,
        }

    def has_issues(self) -> bool:
        """Check if any issues were found."""
        return (
            len(self.duplicates) > 0
            or len(self.missing_required) > 0
            or len(self.invalid_emails) > 0
            or len(self.invalid_linkedin) > 0
            or len(self.invalid_functions) > 0
            or len(self.invalid_sources) > 0
        )

    def print_report(self, verbose: bool = False):
        """Print formatted report to console."""
        print("\n📊 Data Quality Report - People Table")
        print("━" * 60)
        print(f"Total Records: {self.total_records}")
        print(
            f"✅ Complete: {self.complete_records} ({self._percentage(self.complete_records)}%)"
        )
        print(
            f"⚠️  Incomplete: {self.incomplete_records} ({self._percentage(self.incomplete_records)}%)"
        )

        # Critical issues
        if self.has_issues():
            print("\n🚨 CRITICAL ISSUES:")
            print("-" * 60)

            if self.duplicates:
                print(f"\n❌ Duplicate Names ({len(self.duplicates)}):")
                for name, count in self.duplicates[:10]:  # Show first 10
                    print(f"  • {name} (appears {count} times)")
                if len(self.duplicates) > 10:
                    print(f"  ... and {len(self.duplicates) - 10} more")

            if self.missing_required:
                print(f"\n❌ Missing Required Fields ({len(self.missing_required)}):")
                for item in self.missing_required[:10]:
                    print(f"  • {item}")
                if len(self.missing_required) > 10:
                    print(f"  ... and {len(self.missing_required) - 10} more")

            if self.invalid_emails:
                print(f"\n❌ Invalid Email Formats ({len(self.invalid_emails)}):")
                for item in self.invalid_emails[:5]:
                    print(f"  • {item}")
                if len(self.invalid_emails) > 5:
                    print(f"  ... and {len(self.invalid_emails) - 5} more")

            if self.invalid_linkedin:
                print(f"\n❌ Invalid LinkedIn URLs ({len(self.invalid_linkedin)}):")
                for item in self.invalid_linkedin[:5]:
                    print(f"  • {item}")
                if len(self.invalid_linkedin) > 5:
                    print(f"  ... and {len(self.invalid_linkedin) - 5} more")

            if self.invalid_functions:
                print(f"\n❌ Invalid Function Values ({len(self.invalid_functions)}):")
                for item in self.invalid_functions[:5]:
                    print(f"  • {item}")

            if self.invalid_sources:
                print(f"\n❌ Invalid Source Values ({len(self.invalid_sources)}):")
                for item in self.invalid_sources[:5]:
                    print(f"  • {item}")

        # Warnings
        if self.missing_important or self.orphaned_records:
            print("\n⚠️  WARNINGS (Non-Critical):")
            print("-" * 60)

            for field, records in self.missing_important.items():
                if records:
                    print(f"\n• Missing {field} ({len(records)} records)")
                    if verbose:
                        for record_id in records[:5]:
                            print(f"    - {record_id}")
                        if len(records) > 5:
                            print(f"    ... and {len(records) - 5} more")

            if self.orphaned_records:
                print(
                    f"\n• Orphaned Records - No Roles ({len(self.orphaned_records)} records)"
                )
                if verbose:
                    for record_id in self.orphaned_records[:5]:
                        print(f"    - {record_id}")

        # CSV comparison
        if self.csv_comparison:
            print("\n📋 CSV Comparison:")
            print("-" * 60)
            expected = self.csv_comparison["expected"]
            loaded = self.csv_comparison["loaded"]
            missing = self.csv_comparison["missing"]

            print(f"Expected (from CSV): {expected} records")
            print(f"Found in Airtable: {loaded} records")

            if missing:
                print(f"❌ Missing from Airtable: {len(missing)} records")
                if verbose:
                    for name in missing[:10]:
                        print(f"  • {name}")
                    if len(missing) > 10:
                        print(f"  ... and {len(missing) - 10} more")
            else:
                print("✅ All CSV records found in Airtable")

        # Summary
        print("\n" + "=" * 60)
        if not self.has_issues():
            print("✅ Data quality validation passed!")
            if self.incomplete_records > 0:
                print(
                    f"   {self.incomplete_records} records have optional fields missing"
                )
        else:
            print("❌ Data quality issues detected!")
            print("   Review critical issues above and fix in Airtable")

    def _percentage(self, count: int) -> int:
        """Calculate percentage of total."""
        if self.total_records == 0:
            return 0
        return int((count / self.total_records) * 100)

    def save_report(self, filepath: Path):
        """Save report to file."""
        with open(filepath, "w") as f:
            # Redirect print to file
            original_stdout = sys.stdout
            sys.stdout = f
            self.print_report(verbose=True)
            sys.stdout = original_stdout
        print(f"✅ Report saved to: {filepath}")


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return True  # Empty is ok (optional field)
    return EMAIL_REGEX.match(email) is not None


def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL format."""
    if not url:
        return True  # Empty is ok (optional field)
    return LINKEDIN_REGEX.match(url) is not None


def check_record_completeness(record: Dict) -> Tuple[bool, List[str]]:
    """Check if record has all important fields populated."""
    missing = []

    for field in IMPORTANT_FIELDS:
        value = record.get(field, "")
        if isinstance(value, str):
            if not value.strip():
                missing.append(field)
        elif value is None or value == "":
            missing.append(field)

    return len(missing) == 0, missing


def load_csv_names(csv_path: Path) -> Set[str]:
    """Load names from CSV file for comparison."""
    names = set()
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try common name column variations
                name = (
                    row.get("full_name")
                    or row.get("name")
                    or row.get("Name")
                    or row.get("executive_name")
                    or ""
                )
                if name:
                    names.add(name.strip())
    except Exception as e:
        print(f"⚠️  Warning: Could not read CSV file: {e}")

    return names


def validate_people_table(
    csv_path: Optional[Path] = None, verbose: bool = False
) -> DataQualityReport:
    """
    Validate data quality in People table.

    Args:
        csv_path: Optional path to source CSV for comparison
        verbose: Show detailed progress

    Returns:
        DataQualityReport with validation results
    """
    report = DataQualityReport()

    try:
        if verbose:
            print("🔍 Fetching records from Airtable...")

        # Fetch all records from People table
        records = list_records(
            base_id=BASE_ID,
            table_id=PEOPLE_TABLE_ID,
            max_records=1000,  # Adjust if needed
        )

        if not records:
            if verbose:
                print("\n⚠️  No records found in People table")
            return report

        report.total_records = len(records)

        # Track names for duplicate detection
        name_counts = Counter()

        # Validate each record
        for record in records:
            fields = record.get("fields", {})
            record_id = record.get("id", "unknown")
            name = fields.get("Name", "")

            # Count names for duplicate detection
            if name:
                name_counts[name] += 1

            # Check required fields
            for field in REQUIRED_FIELDS:
                if not fields.get(field):
                    report.add_missing_required(record_id, field)

            # Check completeness
            is_complete, missing = check_record_completeness(fields)
            if is_complete:
                report.complete_records += 1
            else:
                report.incomplete_records += 1
                for field in missing:
                    report.add_missing_important(field, name or record_id)

            # Validate email format
            email = fields.get("Email", "")
            if email and not validate_email(email):
                report.add_invalid_email(name or record_id, email)

            # Validate LinkedIn URL
            linkedin = fields.get("LinkedIn URL", "")
            if linkedin and not validate_linkedin_url(linkedin):
                report.add_invalid_linkedin(name or record_id, linkedin)

            # Validate Normalized Title
            function = fields.get("Normalized Title", "")
            if function and function not in VALID_FUNCTIONS:
                report.add_invalid_function(name or record_id, function)

            # Validate Source
            source = fields.get("Source", "")
            if source and source not in VALID_SOURCES:
                report.add_invalid_source(name or record_id, source)

            # Check for orphaned records (no roles)
            roles = fields.get("Roles", [])
            if not roles:
                report.add_orphaned(name or record_id)

        # Check for duplicates
        for name, count in name_counts.items():
            if count > 1:
                report.add_duplicate(name, count)

        # CSV comparison if provided
        if csv_path:
            if verbose:
                print("📄 Comparing with source CSV...")

            csv_names = load_csv_names(csv_path)
            airtable_names = set(name_counts.keys())

            missing_names = csv_names - airtable_names
            report.set_csv_comparison(
                len(csv_names), len(airtable_names), list(missing_names)
            )

        return report

    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Validate Airtable People table data quality"
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="Source CSV file for comparison (optional)",
        default=None,
    )
    parser.add_argument(
        "--report", type=Path, help="Save report to file (optional)", default=None
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show detailed validation progress"
    )

    args = parser.parse_args()

    print("🔍 Airtable Data Quality Validator")
    print("=" * 60)

    # Run validation
    report = validate_people_table(csv_path=args.csv, verbose=args.verbose)

    # Print report
    report.print_report(verbose=args.verbose)

    # Save to file if requested
    if args.report:
        report.save_report(args.report)

    # Exit code based on results
    return 0 if not report.has_issues() else 1


if __name__ == "__main__":
    sys.exit(main())
