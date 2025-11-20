#!/usr/bin/env python3
"""
Shared Airtable utilities for airtable-operations skill.

Provides direct pyairtable API access without MCP dependencies.
Reads credentials from environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pyairtable import Api, Table


# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)


def get_api_key() -> str:
    """Get Airtable API key from environment."""
    api_key = os.getenv("AIRTABLE_API_KEY")
    if not api_key:
        raise ValueError(
            "AIRTABLE_API_KEY not found in environment. "
            "Please set it in .env file or environment variables."
        )
    return api_key.strip()


def get_table(base_id: str, table_id: str) -> Table:
    """Get a pyairtable Table instance.

    Args:
        base_id: Airtable base ID (e.g., 'appeY64iIwU5CEna7')
        table_id: Table ID or name (e.g., 'tblHqYymo3Av9hLeC' or 'People')

    Returns:
        pyairtable Table instance
    """
    api_key = get_api_key()
    api = Api(api_key)
    return api.table(base_id, table_id)


def list_records(
    base_id: str,
    table_id: str,
    max_records: Optional[int] = None,
    formula: Optional[str] = None,
    view: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List records from an Airtable table.

    Args:
        base_id: Airtable base ID
        table_id: Table ID or name
        max_records: Maximum number of records to retrieve
        formula: Filter formula (Airtable formula syntax)
        view: View name to use

    Returns:
        List of record dictionaries with 'id' and 'fields' keys
    """
    table = get_table(base_id, table_id)

    kwargs = {}
    if max_records is not None:
        kwargs["max_records"] = max_records
    if formula is not None:
        kwargs["formula"] = formula
    if view is not None:
        kwargs["view"] = view

    # pyairtable returns RecordDict objects, convert to plain dicts
    records = table.all(**kwargs)
    return [dict(record) for record in records]


def create_record(
    base_id: str,
    table_id: str,
    fields: Dict[str, Any],
) -> Dict[str, Any]:
    """Create a new record in an Airtable table.

    Args:
        base_id: Airtable base ID
        table_id: Table ID or name
        fields: Dictionary of field names to values

    Returns:
        Created record dictionary with 'id' and 'fields' keys
    """
    table = get_table(base_id, table_id)
    record = table.create(fields)
    return dict(record)


def get_base_schema(base_id: str) -> Dict[str, Any]:
    """Get schema information for an Airtable base.

    Args:
        base_id: Airtable base ID

    Returns:
        Dictionary containing base metadata and table schemas
    """
    api_key = get_api_key()
    api = Api(api_key)

    # Use pyairtable's schema method
    # The schema() method returns a BaseSchema object with a 'tables' attribute
    schema_obj = api.base(base_id).schema()

    # Helper to serialize field options to dict format
    def serialize_field_options(field):
        """Serialize field options to dict format."""
        if not hasattr(field, "options") or field.options is None:
            return None

        options = field.options
        result = {}

        # Handle single-select and multi-select fields
        if hasattr(options, "choices"):
            result["choices"] = [
                {"id": choice.id, "name": choice.name} for choice in options.choices
            ]

        # Handle linked record fields
        if hasattr(options, "linked_table_id"):
            result["linkedTableId"] = options.linked_table_id

        return result if result else None

    # Convert BaseSchema to dictionary format
    return {
        "tables": [
            {
                "id": table.id,
                "name": table.name,
                "fields": [
                    {
                        "id": field.id,
                        "name": field.name,
                        "type": field.type,
                        "options": serialize_field_options(field),
                    }
                    for field in table.fields
                ],
            }
            for table in schema_obj.tables
        ]
    }


def get_table_schema(base_id: str, table_id_or_name: str) -> Optional[Dict[str, Any]]:
    """Get schema for a specific table.

    Args:
        base_id: Airtable base ID
        table_id_or_name: Table ID (tblXXX) or table name

    Returns:
        Table schema dictionary or None if not found
    """
    schema = get_base_schema(base_id)
    tables = schema.get("tables", [])

    # Try to match by ID or name
    for table in tables:
        if table.get("id") == table_id_or_name or table.get("name") == table_id_or_name:
            return table

    return None


def list_tables(base_id: str) -> List[Dict[str, Any]]:
    """List all tables in a base.

    Args:
        base_id: Airtable base ID

    Returns:
        List of table schemas
    """
    schema = get_base_schema(base_id)
    return schema.get("tables", [])


# Configuration constants
# Base ID - can be overridden via environment variable
DEFAULT_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appeY64iIwU5CEna7")

# Table IDs and names - use names where possible for clarity
PEOPLE_TABLE_NAME = "People"
PEOPLE_TABLE_ID = "tblHqYymo3Av9hLeC"

PORTCOS_TABLE_NAME = "Portcos"
PORTCOS_TABLE_ID = "tblPortco"

PORTCO_ROLES_TABLE_NAME = "Portco_Roles"
PORTCO_ROLES_TABLE_ID = "tblPortcoRoles"

ROLE_SPECS_TABLE_NAME = "Role_Specs"
ROLE_SPECS_TABLE_ID = "tblRoleSpecs"

SEARCHES_TABLE_NAME = "Searches"
SEARCHES_TABLE_ID = "tblSearches"

ASSESSMENTS_TABLE_NAME = "Assessments"
ASSESSMENTS_TABLE_ID = "tblAssessments"
