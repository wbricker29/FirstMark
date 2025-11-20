# Airtable Schema Exploration Reference

Complete guide to exploring and understanding Airtable database schemas using MCP tools.

## Table of Contents

1. [Core MCP Operations](#core-mcp-operations)
2. [Understanding Field Types](#understanding-field-types)
3. [Schema Validation Patterns](#schema-validation-patterns)
4. [Table Relationships](#table-relationships)
5. [Integration Examples](#integration-examples)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Core MCP Operations

### List Accessible Bases

```javascript
mcp__airtable__list_bases()
```

Returns all bases you have access to with their IDs and names. Copy the base ID for subsequent operations.

**Use when:**
- Starting schema exploration
- Discovering available databases
- Verifying API access

### List Tables in Base

```javascript
mcp__airtable__list_tables({
  baseId: "appXXXXXXXXXXXXXX"
})
```

Returns table IDs and names. Use `detailLevel: "full"` to include field lists.

**Detail levels:**
- `tableIdentifiersOnly` - Just table IDs and names
- `identifiersOnly` - Include field IDs
- `full` - Complete schema with field definitions (default)

**Use when:**
- Exploring base structure
- Mapping table relationships
- Documenting database

### Get Detailed Schema

```javascript
mcp__airtable__describe_table({
  baseId: "appXXXXXXXXXXXXXX",
  tableId: "People"  // or table ID like "tblXXXXXXXXXX"
})
```

Returns complete schema with all field definitions, types, and constraints.

**Use when:**
- Validating field constraints before operations
- Understanding single-select/multi-select options
- Checking required fields
- Mapping linked record relationships

---

## Understanding Field Types

Schema responses include field definitions. Key types for data validation:

### Single Select

- **Type:** `singleSelect`
- **Value:** String (must match one option exactly, case-sensitive)
- **Schema includes:** `options.choices` array with valid values

**Example schema:**
```json
{
  "name": "Status",
  "type": "singleSelect",
  "options": {"choices": [{"name": "Active"}, {"name": "Inactive"}]}
}
```

**Validation pattern:**
```python
# Extract valid options
status_field = next(f for f in schema["fields"] if f["name"] == "Status")
valid_statuses = [choice["name"] for choice in status_field["options"]["choices"]]

# Validate before record creation
if my_status not in valid_statuses:
    raise ValueError(f"'{my_status}' not in {valid_statuses}")
```

### Multi Select

- **Type:** `multipleSelects`
- **Value:** Array of strings (each must be a valid option)
- **Schema includes:** `options.choices` array

**Example:**
```json
{
  "name": "Skills",
  "type": "multipleSelects",
  "options": {"choices": [{"name": "Python"}, {"name": "Java"}, {"name": "Go"}]}
}
```

**Validation pattern:**
```python
# Validate each value in array
skills_field = next(f for f in schema["fields"] if f["name"] == "Skills")
valid_skills = {choice["name"] for choice in skills_field["options"]["choices"]}

for skill in my_skills_list:
    if skill not in valid_skills:
        raise ValueError(f"'{skill}' not in valid skills")
```

### Linked Records

- **Type:** `multipleRecordLinks`
- **Value:** Array of record IDs (format: `"recXXXXXXXXXXXXXX"`)
- **Schema includes:** `options.linkedTableId` (target table)

**Use for:**
- Mapping table relationships
- Validating record IDs exist in target table
- Understanding database structure

**Example:**
```json
{
  "name": "Portfolio Companies",
  "type": "multipleRecordLinks",
  "options": {"linkedTableId": "tblPortco"}
}
```

### Common Types

**Text fields:**
- `singleLineText` - Short text (no line breaks)
- `multilineText` - Long text (with line breaks)
- `email` - Email validation
- `url` - URL validation

**Number fields:**
- `number` - Decimal numbers
- `currency` - Formatted currency
- `percent` - Percentage (0.25 = 25%)

**Date fields:**
- `date` - Format: YYYY-MM-DD
- `dateTime` - Format: ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)

**Other:**
- `checkbox` - Boolean (true/false)
- `formula` - Computed field (read-only)
- `lookup` - Value from linked record (read-only)

---

## Schema Validation Patterns

### Pattern 1: Validate Before Record Creation

**Use case:** Creating records with single-select or multi-select fields

**Workflow:**
```
1. Call mcp__airtable__describe_table to get schema
2. Extract valid options for single-select/multi-select fields
3. Validate your data against options list
4. If valid, proceed with mcp__airtable__create_record
5. If invalid, adjust data or report error
```

**Complete example:**
```python
# Step 1: Get schema
schema = mcp__airtable__describe_table({
    "baseId": "appeY64iIwU5CEna7",
    "tableId": "People"
})

# Step 2: Extract valid options
function_field = next(f for f in schema["fields"] if f["name"] == "Normalized Title")
valid_functions = [choice["name"] for choice in function_field["options"]["choices"]]

# Step 3: Validate data
candidate_function = "CFO"
if candidate_function not in valid_functions:
    print(f"Error: '{candidate_function}' not in {valid_functions}")
else:
    # Step 4: Create record
    mcp__airtable__create_record({
        "baseId": "appeY64iIwU5CEna7",
        "tableId": "People",
        "fields": {
            "Name": "John Doe",
            "Normalized Title": candidate_function
        }
    })
```

### Pattern 2: Document Table Relationships

**Use case:** Understanding how tables link together

**Workflow:**
```
1. Call mcp__airtable__list_tables to get all tables
2. For each table, call mcp__airtable__describe_table
3. Identify fields with type "multipleRecordLinks"
4. Extract linkedTableId to map relationships
5. Create relationship diagram or documentation
```

**Example:**
```python
# Get all tables
tables_response = mcp__airtable__list_tables({"baseId": "appeY64iIwU5CEna7"})

# Map relationships
relationships = []
for table in tables_response["tables"]:
    schema = mcp__airtable__describe_table({
        "baseId": "appeY64iIwU5CEna7",
        "tableId": table["id"]
    })

    # Find linked record fields
    for field in schema["fields"]:
        if field["type"] == "multipleRecordLinks":
            relationships.append({
                "from_table": table["name"],
                "field_name": field["name"],
                "to_table": field["options"]["linkedTableId"]
            })

# Output documentation
for rel in relationships:
    print(f"{rel['from_table']}.{rel['field_name']} → {rel['to_table']}")
```

**Example output:**
```
People.Portfolio Companies → tblPortco
People.Roles → tblRoles
Searches.Portfolio Company → tblPortco
Searches.Matched Candidates → tblPeople
```

### Pattern 3: Schema-Driven Data Import

**Use case:** Loading data from external sources (CSV, JSON)

**Workflow:**
```
1. Get table schema with mcp__airtable__describe_table
2. Map external data columns to Airtable fields
3. Validate each record against schema:
   - Check required fields present
   - Validate single-select options
   - Convert dates to ISO format
   - Resolve linked record IDs
4. Create records only after validation passes
```

**Key validation checks:**

**Required fields:**
```python
required_fields = [f["name"] for f in schema["fields"] if f.get("required", False)]
for field in required_fields:
    if field not in record_data:
        raise ValueError(f"Required field '{field}' missing")
```

**Field types:**
```python
# Convert string to number
if field["type"] == "number":
    record_data[field_name] = float(record_data[field_name])

# Convert to ISO date
if field["type"] == "date":
    record_data[field_name] = datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
```

**Single-select validation:**
```python
if field["type"] == "singleSelect":
    valid_options = [c["name"] for c in field["options"]["choices"]]
    if record_data[field_name] not in valid_options:
        # Either skip field or raise error
        del record_data[field_name]
```

---

## Table Relationships

### Identifying Relationships

Linked record fields (`multipleRecordLinks`) create relationships between tables.

**Schema structure:**
```json
{
  "name": "Portfolio Companies",
  "type": "multipleRecordLinks",
  "options": {
    "linkedTableId": "tblPortco",
    "inverseLinkFieldId": "fldInverse",
    "prefersSingleRecordLink": false
  }
}
```

**Key properties:**
- `linkedTableId` - Target table ID
- `inverseLinkFieldId` - Reverse relationship field (optional)
- `prefersSingleRecordLink` - If true, UI suggests single selection

### Creating Linked Record References

**Format:** Array of record IDs
```python
mcp__airtable__create_record({
    "baseId": "appeY64iIwU5CEna7",
    "tableId": "Searches",
    "fields": {
        "Portfolio Company": ["recPortcoXXXXXXXX"],  # Single link
        "Matched Candidates": [                       # Multiple links
            "recPeople1XXXXXXX",
            "recPeople2XXXXXXX"
        ]
    }
})
```

### Resolving Record IDs

Before creating linked records, resolve names to IDs:

```python
# Find record by name
records = mcp__airtable__list_records({
    "baseId": "appeY64iIwU5CEna7",
    "tableId": "Portco",
    "filterByFormula": "{Company Name} = 'Pigment'"
})

if records["records"]:
    portco_id = records["records"][0]["id"]
else:
    raise ValueError("Portfolio company not found")
```

---

## Integration Examples

### Example 1: Validate Data Before Import

**Scenario:** Loading candidates from CSV into People table

```python
import csv

# Step 1: Get People table schema
schema = mcp__airtable__describe_table({
    "baseId": "appeY64iIwU5CEna7",
    "tableId": "People"
})

# Step 2: Extract validation rules
required_fields = [f["name"] for f in schema["fields"] if f.get("required")]
function_field = next(f for f in schema["fields"] if f["name"] == "Normalized Title")
function_options = {c["name"] for c in function_field["options"]["choices"]}

# Step 3: Validate each CSV row
with open('candidates.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Check required fields
        if not all(row.get(field) for field in required_fields):
            print(f"Skipping {row['Name']}: missing required fields")
            continue

        # Validate single-select
        if row.get("function"):
            if row["function"] not in function_options:
                print(f"Warning: '{row['function']}' not valid, skipping field")
                row.pop("function")

        # Create record
        mcp__airtable__create_record({
            "baseId": "appeY64iIwU5CEna7",
            "tableId": "People",
            "fields": row
        })
```

### Example 2: Document Database Structure

**Scenario:** Generate markdown documentation of base schema

```python
# Step 1: List all tables
tables = mcp__airtable__list_tables({"baseId": "appeY64iIwU5CEna7"})

# Step 2: Document each table
output = []
for table in tables["tables"]:
    output.append(f"## {table['name']}\n")

    # Get schema
    schema = mcp__airtable__describe_table({
        "baseId": "appeY64iIwU5CEna7",
        "tableId": table["id"]
    })

    # Document fields
    output.append("**Fields:**\n")
    for field in schema["fields"]:
        output.append(f"- **{field['name']}** ({field['type']})")

        # Show options for select fields
        if field["type"] in ["singleSelect", "multipleSelects"]:
            options = [c["name"] for c in field["options"]["choices"]]
            output.append(f"  - Options: {', '.join(options)}")

        # Show linked table for relationships
        if field["type"] == "multipleRecordLinks":
            linked_table = field["options"]["linkedTableId"]
            output.append(f"  - Links to: {linked_table}")

    output.append("\n")

print("\n".join(output))
```

---

## Troubleshooting

### "Invalid value for single-select field"

**Cause:** Value doesn't match options exactly (case-sensitive)

**Solution:**
1. Call `mcp__airtable__describe_table` to get schema
2. Extract valid options from field definition
3. Verify your value matches exactly (including case)
4. Update your data to use valid option

**Example:**
```
Schema options: ["CFO", "CTO", "CEO"]
Your value: "cfo"  ❌ (wrong case)
Correct value: "CFO"  ✅
```

### "Field not found"

**Cause:** Using field name that doesn't exist in table

**Solution:**
1. Call `mcp__airtable__describe_table` to see all fields
2. Check exact field name spelling and case
3. Use field name (not field ID) in record operations

### "Linked record ID not found"

**Cause:** Using invalid record ID in linked record field

**Solution:**
1. Call `mcp__airtable__list_records` on target table
2. Verify record ID exists
3. Use correct ID format: `"recXXXXXXXXXXXXXX"`

### "Date format invalid"

**Cause:** Date not in ISO 8601 format

**Solution:**
- Use `YYYY-MM-DD` for date fields
- Use `YYYY-MM-DDTHH:mm:ss.sssZ` for datetime fields
- Ensure timezone is UTC (Z suffix)

**Example:**
```python
from datetime import datetime

# Convert to date format
date_str = datetime.now().strftime("%Y-%m-%d")

# Convert to datetime format
datetime_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
```

---

## Best Practices

### 1. Always Validate Schema First

Before any record operations, retrieve the table schema to understand:
- Required fields
- Field types and constraints
- Valid options for select fields
- Linked table relationships

**Why:** Prevents 90% of common Airtable errors

### 2. Cache Schema Information

If performing multiple operations on the same table:
- Call `describe_table` once
- Store schema in memory
- Reuse for all validations
- Reduces API calls and improves performance

**Example:**
```python
# Cache schema
_schema_cache = {}

def get_schema(base_id, table_id):
    cache_key = f"{base_id}:{table_id}"
    if cache_key not in _schema_cache:
        _schema_cache[cache_key] = mcp__airtable__describe_table({
            "baseId": base_id,
            "tableId": table_id
        })
    return _schema_cache[cache_key]
```

### 3. Use Field Names, Not IDs

When creating/updating records, prefer field names over field IDs:

```json
// Preferred
{"fields": {"Name": "John", "Status": "Active"}}

// Avoid (unless necessary)
{"fields": {"fldXXXXXXXX": "John", "fldYYYYYYYY": "Active"}}
```

**Why:** Field names are more readable and maintainable

### 4. Handle Optional Fields Gracefully

Not all fields need values:
- Only set fields with available data
- Omit optional fields rather than sending null/empty
- Check schema for required fields

**Example:**
```python
# Good
fields = {"Name": "John"}
if company:
    fields["Company"] = company

# Avoid
fields = {
    "Name": "John",
    "Company": company or ""  # Don't send empty strings
}
```

### 5. Validate Linked Records Exist

Before creating linked record references:
1. Query target table to verify records exist
2. Use exact record IDs from query results
3. Handle missing records gracefully

**Example:**
```python
# Verify linked record exists
portco_records = mcp__airtable__list_records({
    "baseId": base_id,
    "tableId": "Portco",
    "filterByFormula": f"{{Company Name}} = '{company_name}'"
})

if not portco_records["records"]:
    print(f"Warning: Portfolio company '{company_name}' not found")
    # Skip or create placeholder
else:
    portco_id = portco_records["records"][0]["id"]
    # Use in linked field
```

---

## Additional Resources

- [Field Types Reference](field_types.md) - Complete field type catalog
- [Troubleshooting Guide](troubleshooting.md) - Common issues & solutions
- Official Airtable API: https://airtable.com/developers/web/api/introduction
- MCP Airtable Server: https://github.com/modelcontextprotocol/servers/tree/main/src/airtable
