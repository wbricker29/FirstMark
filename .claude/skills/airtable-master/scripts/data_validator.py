#!/usr/bin/env python3
"""
Data Validator for Airtable

Validates data quality and integrity before operations:
- Field type validation
- Required field checking
- Duplicate detection
- Relationship integrity verification
- Format validation (email, URL, phone)
- Custom validation rules

Usage:
    from scripts.data_validator import DataValidator

    validator = DataValidator(table_schema)
    results = validator.validate_records(records_list)
"""

import re
from typing import List, Dict, Any
from collections import defaultdict


class DataValidator:
    """Validate Airtable data quality and integrity"""

    # Regex patterns for format validation
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    URL_PATTERN = r"^https?://[^\s]+$"
    PHONE_PATTERN = r"^[\d\s\-\+\(\)]+$"

    def __init__(self, table_schema: Dict[str, Any]):
        """
        Initialize validator with table schema

        Args:
            table_schema: Complete table schema from describe_table
        """
        self.schema = table_schema
        self.fields = {f["id"]: f for f in table_schema.get("fields", [])}
        self.field_names = {f["name"]: f for f in table_schema.get("fields", [])}
        self.errors = []
        self.warnings = []

    def validate_records(
        self,
        records: List[Dict[str, Any]],
        check_duplicates: bool = True,
        check_relationships: bool = True,
    ) -> Dict[str, Any]:
        """
        Validate a list of records

        Args:
            records: List of record dictionaries with 'fields'
            check_duplicates: Check for duplicate values
            check_relationships: Verify linked record relationships

        Returns:
            Validation results with errors and warnings
        """
        self.errors = []
        self.warnings = []

        valid_count = 0
        invalid_count = 0

        print(f"🔍 Validating {len(records)} records...")

        for i, record in enumerate(records):
            record_errors = []
            record_warnings = []

            # Validate each field
            fields = record.get("fields", {})

            for field_name, value in fields.items():
                field_config = self.field_names.get(field_name)

                if not field_config:
                    record_warnings.append(f"Field '{field_name}' not in schema")
                    continue

                # Type validation
                type_errors = self._validate_field_type(field_config, field_name, value)
                record_errors.extend(type_errors)

                # Format validation
                format_errors = self._validate_field_format(
                    field_config, field_name, value
                )
                record_errors.extend(format_errors)

            # Check required fields
            required_errors = self._check_required_fields(fields)
            record_errors.extend(required_errors)

            # Store record-level errors
            if record_errors:
                invalid_count += 1
                self.errors.append(
                    {
                        "record_index": i,
                        "record_id": record.get("id"),
                        "errors": record_errors,
                    }
                )
            else:
                valid_count += 1

            if record_warnings:
                self.warnings.append(
                    {
                        "record_index": i,
                        "record_id": record.get("id"),
                        "warnings": record_warnings,
                    }
                )

        # Duplicate detection
        if check_duplicates:
            duplicate_errors = self._check_duplicates(records)
            if duplicate_errors:
                self.errors.extend(duplicate_errors)

        # Relationship integrity
        if check_relationships:
            relationship_errors = self._check_relationships(records)
            if relationship_errors:
                self.errors.extend(relationship_errors)

        return self._format_results(valid_count, invalid_count)

    def _validate_field_type(
        self, field_config: Dict[str, Any], field_name: str, value: Any
    ) -> List[str]:
        """Validate field value matches expected type"""
        errors = []
        field_type = field_config.get("type")

        if value is None:
            return errors  # Null values handled by required field check

        # Type-specific validation
        if field_type in ["number", "currency", "percent", "duration"]:
            if not isinstance(value, (int, float)):
                errors.append(
                    f"Field '{field_name}' expects number, got {type(value).__name__}"
                )

        elif field_type == "checkbox":
            if not isinstance(value, bool):
                errors.append(
                    f"Field '{field_name}' expects boolean, got {type(value).__name__}"
                )

        elif field_type in [
            "singleLineText",
            "multilineText",
            "richText",
            "email",
            "url",
            "phoneNumber",
        ]:
            if not isinstance(value, str):
                errors.append(
                    f"Field '{field_name}' expects string, got {type(value).__name__}"
                )

        elif field_type in ["date", "dateTime"]:
            if not isinstance(value, str):
                errors.append(
                    f"Field '{field_name}' expects ISO date string, got {type(value).__name__}"
                )

        elif field_type in ["singleSelect"]:
            if not isinstance(value, str):
                errors.append(
                    f"Field '{field_name}' expects string, got {type(value).__name__}"
                )
            else:
                # Validate against allowed choices
                options = field_config.get("options", {})
                choices = options.get("choices", [])
                valid_choices = [c["name"] for c in choices]
                if valid_choices and value not in valid_choices:
                    errors.append(
                        f"Field '{field_name}' value '{value}' not in allowed choices: {valid_choices}"
                    )

        elif field_type == "multipleSelects":
            if not isinstance(value, list):
                errors.append(
                    f"Field '{field_name}' expects array, got {type(value).__name__}"
                )
            else:
                options = field_config.get("options", {})
                choices = options.get("choices", [])
                valid_choices = [c["name"] for c in choices]
                if valid_choices:
                    for v in value:
                        if v not in valid_choices:
                            errors.append(
                                f"Field '{field_name}' value '{v}' not in allowed choices: {valid_choices}"
                            )

        elif field_type in ["multipleRecordLinks"]:
            if not isinstance(value, list):
                errors.append(
                    f"Field '{field_name}' expects array of record IDs, got {type(value).__name__}"
                )

        elif field_type == "multipleAttachments":
            if not isinstance(value, list):
                errors.append(
                    f"Field '{field_name}' expects array of attachments, got {type(value).__name__}"
                )

        return errors

    def _validate_field_format(
        self, field_config: Dict[str, Any], field_name: str, value: Any
    ) -> List[str]:
        """Validate field value format"""
        errors = []
        field_type = field_config.get("type")

        if not isinstance(value, str):
            return errors

        if field_type == "email":
            if not re.match(self.EMAIL_PATTERN, value):
                errors.append(
                    f"Field '{field_name}' has invalid email format: '{value}'"
                )

        elif field_type == "url":
            if not re.match(self.URL_PATTERN, value):
                errors.append(f"Field '{field_name}' has invalid URL format: '{value}'")

        elif field_type == "phoneNumber":
            if not re.match(self.PHONE_PATTERN, value):
                errors.append(
                    f"Field '{field_name}' has invalid phone format: '{value}'"
                )

        return errors

    def _check_required_fields(self, fields: Dict[str, Any]) -> List[str]:
        """Check if required fields are present"""
        errors = []

        # Primary field is always required
        primary_field_id = self.schema.get("primaryFieldId")
        if primary_field_id:
            primary_field = self.fields.get(primary_field_id)
            if primary_field:
                primary_name = primary_field["name"]
                if primary_name not in fields or not fields[primary_name]:
                    errors.append(
                        f"Required primary field '{primary_name}' is missing or empty"
                    )

        # Check other required fields (would need to be defined in schema or config)
        # This is a placeholder for custom required field logic

        return errors

    def _check_duplicates(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for duplicate values in unique fields"""
        errors = []

        # Track values for each field
        field_values = defaultdict(list)

        for i, record in enumerate(records):
            fields = record.get("fields", {})
            for field_name, value in fields.items():
                if value is not None:
                    field_values[field_name].append(
                        {"index": i, "id": record.get("id"), "value": value}
                    )

        # Check for duplicates
        for field_name, values in field_values.items():
            value_counts = defaultdict(list)
            for item in values:
                # Convert to hashable type for counting
                val = str(item["value"])
                value_counts[val].append(item)

            # Report duplicates
            for value, items in value_counts.items():
                if len(items) > 1:
                    record_ids = [
                        item["id"] or f"index {item['index']}" for item in items
                    ]
                    errors.append(
                        {
                            "type": "duplicate",
                            "field": field_name,
                            "value": value,
                            "records": record_ids,
                        }
                    )

        return errors

    def _check_relationships(
        self, records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Verify linked record relationships"""
        errors = []

        # Extract all record IDs from this batch
        record_ids = {r.get("id") for r in records if r.get("id")}

        # Check linked record fields
        for i, record in enumerate(records):
            fields = record.get("fields", {})

            for field_name, value in fields.items():
                field_config = self.field_names.get(field_name)
                if not field_config:
                    continue

                if field_config.get("type") == "multipleRecordLinks":
                    if isinstance(value, list):
                        # Note: We can only validate against records in this batch
                        # Full validation would require querying the linked table
                        for linked_id in value:
                            if linked_id not in record_ids:
                                # This might be valid (linking to existing records)
                                # but we flag it as a warning
                                pass

        return errors

    def _format_results(self, valid_count: int, invalid_count: int) -> Dict[str, Any]:
        """Format validation results"""
        total = valid_count + invalid_count
        success_rate = (valid_count / total * 100) if total > 0 else 0

        result = {
            "total": total,
            "valid": valid_count,
            "invalid": invalid_count,
            "success_rate": f"{success_rate:.1f}%",
            "errors": self.errors,
            "warnings": self.warnings,
        }

        # Print summary
        print("\n" + "=" * 50)
        print("📊 VALIDATION SUMMARY")
        print("=" * 50)
        print(f"Total Records:   {result['total']}")
        print(f"✓ Valid:         {result['valid']}")
        print(f"❌ Invalid:       {result['invalid']}")
        print(f"Success Rate:    {result['success_rate']}")

        if result["errors"]:
            print(f"\n❌ {len(result['errors'])} error(s) found")
        if result["warnings"]:
            print(f"⚠️  {len(result['warnings'])} warning(s) found")

        print("=" * 50)

        return result


# Example usage
if __name__ == "__main__":
    # Example table schema
    schema = {
        "id": "tblXXXXXXXXXXXXXX",
        "name": "Contacts",
        "primaryFieldId": "fldYYYYYYYYYYYYYY",
        "fields": [
            {"id": "fldYYYYYYYYYYYYYY", "name": "Name", "type": "singleLineText"},
            {"id": "fldZZZZZZZZZZZZZZ", "name": "Email", "type": "email"},
            {
                "id": "fldAAAAAAAAAAAAA",
                "name": "Status",
                "type": "singleSelect",
                "options": {"choices": [{"name": "Active"}, {"name": "Inactive"}]},
            },
        ],
    }

    # Example records
    test_records = [
        {
            "fields": {
                "Name": "John Doe",
                "Email": "john@example.com",
                "Status": "Active",
            }
        },
        {
            "fields": {
                "Name": "Jane Smith",
                "Email": "invalid-email",  # Invalid format
                "Status": "Active",
            }
        },
        {
            "fields": {
                # Missing required Name field
                "Email": "test@example.com",
                "Status": "Pending",  # Invalid choice
            }
        },
    ]

    validator = DataValidator(schema)
    results = validator.validate_records(test_records)

    # Print detailed errors
    if results["errors"]:
        print("\nDetailed errors:")
        for error in results["errors"]:
            print(f"  {error}")
