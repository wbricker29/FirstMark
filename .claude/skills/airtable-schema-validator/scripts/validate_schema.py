#!/usr/bin/env python3
"""
Airtable Schema Validator

Validates Airtable schema against expected structure for FirstMark Talent Signal Agent.
Checks People table only: required fields, single-select options, and relationships.

Usage:
    python validate_schema.py [--fix-suggestions] [--verbose]

Examples:
    python validate_schema.py
    python validate_schema.py --fix-suggestions
    python validate_schema.py --verbose
"""

import argparse
import sys
from typing import Dict, List, Tuple

# Import Airtable utilities
from airtable_utils import get_table_schema, list_tables  # noqa: F401

# Airtable configuration
BASE_ID = "appeY64iIwU5CEna7"

# Expected schema structure (People table only)
# Updated to match actual Airtable schema as of Nov 19, 2025
EXPECTED_TABLES = {
    "People": {
        "id": "tblHqYymo3Av9hLeC",
        "required_fields": ["Name"],  # Only Name is truly required
        "optional_fields": [
            "Current Title",
            "Current Company",
            "LinkedIn URL",
            "LinkedIn Headline",
            "Location",
            "Normalized Title",
            "Source",
            "Bio",
            "Assessments",
            "Screens",
            "Photo",
        ],
        "single_selects": {
            "Normalized Title": [
                "CFO (Chief Financial Officer)",
                "CTO (Chief Technology Officer)",
                "CPO (Chief Product Officer)",
                "CPO (Chief People Officer)",
                "CEO (Chief Executive Officer)",
                "CMO (Chief Marketing Officer)",
                "COO (Chief Operating Officer)",
                "CRO (Chief Revenue Officer)",
                "Exec_Finance",
                "Exec_Technology",
                "Exec_Marketing",
                "Exec_People",
                "CDO (Chief Development Officer)",
            ],
            "Source": [
                "FMGuildPage",
                "FMLinkedIN",
            ],
        },
    },
}


def check_table_exists(table_name: str, all_tables: List[Dict]) -> Tuple[bool, str]:
    """Check if table exists in base."""
    for table in all_tables:
        if table.get("name") == table_name:
            return True, table.get("id", "")
    return False, ""


def check_fields(
    table_name: str,
    expected_fields: List[str],
    actual_fields: List[Dict],
    required: bool = True,
) -> Tuple[List[str], List[str]]:
    """Check if expected fields exist in table."""
    actual_field_names = [field.get("name", "") for field in actual_fields]
    missing = []
    present = []

    for field in expected_fields:
        if field in actual_field_names:
            present.append(field)
        else:
            missing.append(field)

    return present, missing


def check_single_select_options(
    field_name: str, expected_options: List[str], actual_field: Dict
) -> Tuple[List[str], List[str]]:
    """Check single-select field options."""
    if actual_field.get("type") != "singleSelect":
        return [], expected_options  # Field exists but wrong type

    choices = actual_field.get("options", {}).get("choices", [])
    actual_options = [choice.get("name", "") for choice in choices]

    present = [opt for opt in expected_options if opt in actual_options]
    missing = [opt for opt in expected_options if opt not in actual_options]

    return present, missing


def check_linked_fields(
    field_name: str, expected_table: str, actual_field: Dict, all_tables: List[Dict]
) -> Tuple[bool, str]:
    """Check linked record field configuration."""
    if actual_field.get("type") != "multipleRecordLinks":
        return False, "Field exists but is not a linked record field"

    linked_table_id = actual_field.get("options", {}).get("linkedTableId", "")

    # Find linked table name by ID
    linked_table_name = None
    for table in all_tables:
        if table.get("id") == linked_table_id:
            linked_table_name = table.get("name")
            break

    if linked_table_name == expected_table:
        return True, ""
    else:
        return False, f"Links to '{linked_table_name}' instead of '{expected_table}'"


def validate_schema(
    verbose: bool = False,
) -> Tuple[bool, List[str], List[str], List[str]]:
    """
    Validate Airtable schema against expected structure.

    Returns:
        Tuple of (success, errors, warnings, info_messages)
    """
    errors = []
    warnings = []
    info = []

    try:
        if verbose:
            info.append("Connecting to Airtable base...")

        # Fetch all tables from the base
        all_tables = list_tables(BASE_ID)

        info.append(f"Validating base: {BASE_ID}")
        info.append(f"Expected tables: {len(EXPECTED_TABLES)}")
        info.append(f"Found tables: {len(all_tables)}")

        # Check each expected table
        for table_name, table_config in EXPECTED_TABLES.items():
            if verbose:
                info.append(f"\nChecking table: {table_name}")

            # Check if table exists
            exists, table_id = check_table_exists(table_name, all_tables)
            if not exists:
                errors.append(f"Table '{table_name}' not found in base")
                continue

            # Get detailed table schema
            table_schema = get_table_schema(BASE_ID, table_id)
            if not table_schema:
                errors.append(f"Could not fetch schema for table '{table_name}'")
                continue

            actual_fields = table_schema.get("fields", [])

            # Check required fields
            required_fields = table_config.get("required_fields", [])
            present, missing = check_fields(
                table_name, required_fields, actual_fields, required=True
            )
            if missing:
                errors.append(
                    f"{table_name}: Missing required fields: {', '.join(missing)}"
                )

            # Check optional fields (warnings only)
            optional_fields = table_config.get("optional_fields", [])
            present, missing = check_fields(
                table_name, optional_fields, actual_fields, required=False
            )
            if missing and verbose:
                warnings.append(
                    f"{table_name}: Missing optional fields: {', '.join(missing)}"
                )

            # Check single-select field options
            single_selects = table_config.get("single_selects", {})
            for field_name, expected_options in single_selects.items():
                # Find the field in actual schema
                actual_field = next(
                    (f for f in actual_fields if f.get("name") == field_name), None
                )
                if not actual_field:
                    warnings.append(f"{table_name}: Field '{field_name}' not found")
                    continue

                present_options, missing_options = check_single_select_options(
                    field_name, expected_options, actual_field
                )
                if missing_options:
                    warnings.append(
                        f"{table_name} → {field_name}: Missing options: {', '.join(missing_options)}"
                    )

            # Check linked record fields
            links = table_config.get("links", {})
            for field_name, expected_linked_table in links.items():
                actual_field = next(
                    (f for f in actual_fields if f.get("name") == field_name), None
                )
                if not actual_field:
                    warnings.append(
                        f"{table_name}: Link field '{field_name}' not found"
                    )
                    continue

                is_valid, error_msg = check_linked_fields(
                    field_name, expected_linked_table, actual_field, all_tables
                )
                if not is_valid:
                    warnings.append(f"{table_name} → {field_name}: {error_msg}")

        return len(errors) == 0, errors, warnings, info

    except Exception as e:
        errors.append(f"Failed to connect to Airtable: {str(e)}")
        return False, errors, warnings, info


def generate_fix_suggestions(errors: List[str], warnings: List[str]) -> List[str]:
    """Generate actionable fix suggestions based on validation results."""
    suggestions = []

    if not errors and not warnings:
        suggestions.append("✅ No fixes needed - schema is valid!")
        return suggestions

    suggestions.append("\n📋 RECOMMENDED FIXES:")
    suggestions.append("=" * 60)

    # Group suggestions by table
    for table_name, table_config in EXPECTED_TABLES.items():
        table_suggestions = []

        # Check for missing single-select options
        if "single_selects" in table_config:
            for field_name, options in table_config["single_selects"].items():
                table_suggestions.append(f"\n{table_name} → {field_name}:")
                table_suggestions.append(
                    f"  1. Open Airtable and navigate to {table_name} table"
                )
                table_suggestions.append(f"  2. Click on '{field_name}' column header")
                table_suggestions.append("  3. Click 'Edit field' → 'Edit options'")
                table_suggestions.append(
                    f"  4. Add missing options: {', '.join(options)}"
                )

        if table_suggestions:
            suggestions.extend(table_suggestions)

    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description="Validate Airtable schema for FirstMark Talent Signal Agent"
    )
    parser.add_argument(
        "--fix-suggestions",
        action="store_true",
        help="Show actionable fix suggestions for schema issues",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation progress",
    )
    args = parser.parse_args()

    print("🔍 Airtable Schema Validator")
    print("=" * 60)

    # Run validation
    success, errors, warnings, info = validate_schema(verbose=args.verbose)

    # Print info messages
    if args.verbose and info:
        for msg in info:
            print(msg)

    # Print errors
    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  • {error}")

    # Print warnings
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")

    # Print fix suggestions if requested
    if args.fix_suggestions:
        suggestions = generate_fix_suggestions(errors, warnings)
        for suggestion in suggestions:
            print(suggestion)

    # Summary
    print("\n" + "=" * 60)
    if success and not errors:
        print("✅ Schema validation passed!")
        if warnings:
            print(f"   {len(warnings)} warnings (non-critical)")
        return 0
    else:
        print("❌ Schema validation failed!")
        print(f"   {len(errors)} errors, {len(warnings)} warnings")
        return 1


if __name__ == "__main__":
    sys.exit(main())
