#!/usr/bin/env python3
"""
Validate AirtableClient alignment with actual Airtable schema.

This script:
1. Loads the AirtableClient class
2. Connects to Airtable and lists all tables
3. Compares client constants/accessors with actual table names
4. Reports any misalignment
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from pyairtable import Api

# Load environment
load_dotenv()

# Configuration
BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appeY64iIwU5CEna7")
API_KEY = os.getenv("AIRTABLE_API_KEY")

if not API_KEY:
    print("❌ ERROR: AIRTABLE_API_KEY not found in environment")
    sys.exit(1)


def get_actual_tables(api: Api, base_id: str) -> dict[str, str]:
    """Get all tables from Airtable base.

    Returns:
        Dict mapping table name to table ID
    """
    base = api.base(base_id)
    schema = base.schema()

    tables = {}
    for table in schema.tables:
        tables[table.name] = table.id

    return tables


def validate_client():
    """Validate AirtableClient alignment with actual Airtable schema."""

    print("🔍 AirtableClient Validation")
    print("=" * 60)

    # Import AirtableClient
    from demo.airtable_client import AirtableClient

    # Get expected tables from AirtableClient constants
    # Note: AirtableClient is write-only and only defines tables it writes to
    expected_tables = {
        "Platform-Screens": AirtableClient.SCREENS_TABLE,
        "Platform-Assessments": AirtableClient.ASSESSMENTS_TABLE,
        "Operations-Automation_Log": AirtableClient.AUTOMATION_LOG_TABLE,
    }

    # Get actual tables from Airtable
    api = Api(API_KEY)
    actual_tables = get_actual_tables(api, BASE_ID)

    print("\n📊 Comparison Results:\n")
    print(f"{'Table Name':<30} {'In Client?':<15} {'Accessor':<20} {'Status'}")
    print("-" * 90)

    all_aligned = True

    # Check each expected table
    for table_name, constant_value in expected_tables.items():
        in_airtable = "✅ Yes" if table_name in actual_tables else "❌ Missing"

        # Map table names to accessor names used in AirtableClient.__init__
        accessor_mapping = {
            "Platform-Screens": "screens",
            "Platform-Assessments": "assessments",
            "Operations-Automation_Log": "automation_log",
        }
        accessor_name = accessor_mapping.get(table_name, table_name.lower())

        # Instantiate client to check accessor
        try:
            client = AirtableClient(API_KEY, BASE_ID)
            has_accessor = hasattr(client, accessor_name)
            accessor_status = "✅ Yes" if has_accessor else "❌ Missing"
        except Exception as e:
            has_accessor = False
            accessor_status = f"❌ Error: {e}"

        status = (
            "✅ OK" if (table_name in actual_tables and has_accessor) else "⚠️  Issue"
        )

        if status != "✅ OK":
            all_aligned = False

        print(f"{table_name:<30} {in_airtable:<15} {accessor_name:<20} {status}")

    # Summary
    print("\n" + "=" * 60)
    if all_aligned:
        print("✅ VALIDATION PASSED: All tables aligned!")
    else:
        print("⚠️  VALIDATION ISSUES: Misalignment detected")
        print("\nRecommended fixes:")
        print("1. Add missing table constants to AirtableClient")
        print("2. Add missing table accessors in __init__")
        print("3. Verify table names match Airtable exactly")

    print("=" * 60)

    return 0 if all_aligned else 1


if __name__ == "__main__":
    sys.exit(validate_client())
