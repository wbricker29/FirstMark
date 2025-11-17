# Airtable Field Types Reference

Comprehensive catalog of all Airtable field types with validation rules, JSON schema structures, and common errors.

## Table of Contents

1. [Text Fields](#text-fields)
2. [Number Fields](#number-fields)
3. [Select Fields](#select-fields)
4. [Date Fields](#date-fields)
5. [Linked Records](#linked-records)
6. [Attachment Fields](#attachment-fields)
7. [Computed Fields](#computed-fields)
8. [Other Fields](#other-fields)

---

## Text Fields

### Single Line Text

**Type:** `singleLineText`

**Description:** Short text without line breaks

**Value format:** String (max ~100,000 characters)

**Schema example:**
```json
{
  "name": "Name",
  "type": "singleLineText"
}
```

**Validation:**
- No special validation required
- Line breaks automatically stripped
- Very large strings may be truncated

**Common errors:**
- None (most flexible field type)

### Multiline Text

**Type:** `multilineText`

**Description:** Long text with line breaks

**Value format:** String with `\n` for line breaks

**Schema example:**
```json
{
  "name": "Bio",
  "type": "multilineText"
}
```

**Validation:**
- Preserves line breaks
- Supports very long text

**Common errors:**
- None

### Email

**Type:** `email`

**Description:** Email address with validation

**Value format:** String (valid email format)

**Schema example:**
```json
{
  "name": "Contact Email",
  "type": "email"
}
```

**Validation:**
- Must be valid email format: `user@domain.com`
- Case-insensitive

**Common errors:**
- `"Invalid email address"` - Format doesn't match email pattern

### URL

**Type:** `url`

**Description:** Web URL with validation

**Value format:** String (valid URL format)

**Schema example:**
```json
{
  "name": "LinkedIn URL",
  "type": "url"
}
```

**Validation:**
- Must start with `http://` or `https://`
- Domain must be valid

**Common errors:**
- `"Invalid URL"` - Missing protocol or invalid format
- **Fix:** Prepend `https://` to bare domains

---

## Number Fields

### Number

**Type:** `number`

**Description:** Decimal number

**Value format:** Number (integer or float)

**Schema example:**
```json
{
  "name": "Years Experience",
  "type": "number",
  "options": {
    "precision": 2  // Optional: decimal places
  }
}
```

**Validation:**
- Must be numeric (not string)
- Respects precision setting

**Common errors:**
- `"Invalid number"` - Value is string, not number
- **Fix:** Convert with `float(value)` or `int(value)`

### Currency

**Type:** `currency`

**Description:** Formatted monetary value

**Value format:** Number

**Schema example:**
```json
{
  "name": "Salary",
  "type": "currency",
  "options": {
    "precision": 2,
    "symbol": "$"
  }
}
```

**Validation:**
- Must be numeric
- Formatted with currency symbol in UI

**Common errors:**
- Don't include currency symbol in value (e.g., use `50000`, not `"$50,000"`)

### Percent

**Type:** `percent`

**Description:** Percentage value

**Value format:** Number (0.25 = 25%)

**Schema example:**
```json
{
  "name": "Completion Rate",
  "type": "percent",
  "options": {
    "precision": 1
  }
}
```

**Validation:**
- Must be numeric
- Typically 0-1 range (but not enforced)
- Displayed as percentage in UI

**Common errors:**
- Using 25 instead of 0.25 for 25%
- **Fix:** Divide by 100: `value / 100`

### Rating

**Type:** `rating`

**Description:** Star rating (1-10)

**Value format:** Number (integer)

**Schema example:**
```json
{
  "name": "Candidate Rating",
  "type": "rating",
  "options": {
    "max": 5,  // Max stars
    "icon": "star",
    "color": "yellowBright"
  }
}
```

**Validation:**
- Must be integer
- Must be between 1 and max value

**Common errors:**
- Using 0 or values exceeding max

---

## Select Fields

### Single Select

**Type:** `singleSelect`

**Description:** Choose one option from predefined list

**Value format:** String (exact match required, case-sensitive)

**Schema example:**
```json
{
  "name": "Normalized Function",
  "type": "singleSelect",
  "options": {
    "choices": [
      {"name": "CFO", "id": "selXXX1"},
      {"name": "CTO", "id": "selXXX2"},
      {"name": "CEO", "id": "selXXX3"}
    ]
  }
}
```

**Validation:**
```python
# Extract valid options
valid_options = [choice["name"] for choice in field["options"]["choices"]]

# Validate
if value not in valid_options:
    raise ValueError(f"'{value}' not in {valid_options}")
```

**Common errors:**
- `"Invalid value for single-select field"` - Value not in options list
- **Case-sensitive:** "cfo" ≠ "CFO"
- **Exact match:** "Chief Financial Officer" ≠ "CFO"

**Best practices:**
- Always call `describe_table` to get current options
- Validate before creating records
- Handle missing options gracefully (skip field or raise error)

### Multi Select

**Type:** `multipleSelects`

**Description:** Choose multiple options from predefined list

**Value format:** Array of strings

**Schema example:**
```json
{
  "name": "Skills",
  "type": "multipleSelects",
  "options": {
    "choices": [
      {"name": "Python", "id": "selXXX1"},
      {"name": "Java", "id": "selXXX2"},
      {"name": "Go", "id": "selXXX3"}
    ]
  }
}
```

**Validation:**
```python
# Extract valid options
valid_options = {choice["name"] for choice in field["options"]["choices"]}

# Validate each value
for value in values_array:
    if value not in valid_options:
        raise ValueError(f"'{value}' not in valid options")
```

**Common errors:**
- Sending string instead of array: `"Python"` instead of `["Python"]`
- Invalid option in array
- **Fix:** Always use array, even for single selection

---

## Date Fields

### Date

**Type:** `date`

**Description:** Date without time

**Value format:** `YYYY-MM-DD` (ISO 8601 date)

**Schema example:**
```json
{
  "name": "Added Date",
  "type": "date"
}
```

**Validation:**
```python
from datetime import datetime

# Validate format
try:
    datetime.strptime(value, "%Y-%m-%d")
except ValueError:
    raise ValueError(f"Invalid date format: {value}")
```

**Common errors:**
- Wrong format: `"11/17/2025"` instead of `"2025-11-17"`
- Including time: `"2025-11-17T10:30:00Z"` instead of `"2025-11-17"`

**Format conversion:**
```python
# US format to ISO
us_date = "11/17/2025"
iso_date = datetime.strptime(us_date, "%m/%d/%Y").strftime("%Y-%m-%d")
# Result: "2025-11-17"
```

### Date Time

**Type:** `dateTime`

**Description:** Date with time

**Value format:** ISO 8601 with UTC timezone

**Schema example:**
```json
{
  "name": "Created At",
  "type": "dateTime",
  "options": {
    "timeZone": "utc"
  }
}
```

**Validation:**
- Must be ISO 8601: `YYYY-MM-DDTHH:mm:ss.sssZ`
- Must include timezone (Z for UTC)

**Common errors:**
- Missing timezone: `"2025-11-17T10:30:00"` instead of `"2025-11-17T10:30:00Z"`
- Wrong timezone format

**Format examples:**
```python
from datetime import datetime

# Current time in ISO 8601 UTC
iso_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
# Result: "2025-11-17T15:30:45.000Z"

# Parse from string
dt = datetime.strptime("2025-11-17T15:30:45.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
```

---

## Linked Records

### Multiple Record Links

**Type:** `multipleRecordLinks`

**Description:** Links to records in another table

**Value format:** Array of record IDs (format: `"recXXXXXXXXXXXXXX"`)

**Schema example:**
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

**Validation:**
```python
# Validate record ID format
import re
if not re.match(r'^rec[a-zA-Z0-9]{14}$', record_id):
    raise ValueError(f"Invalid record ID format: {record_id}")

# Verify record exists in target table
records = mcp__airtable__list_records({
    "baseId": base_id,
    "tableId": linked_table_id,
    "filterByFormula": f"RECORD_ID() = '{record_id}'"
})
if not records["records"]:
    raise ValueError(f"Record {record_id} not found in target table")
```

**Common errors:**
- Using names instead of IDs: `["Pigment"]` instead of `["recXXXXXXXXXXXXXX"]`
- Invalid record ID format
- Record doesn't exist in target table

**Best practices:**
```python
# Resolve name to ID before creating link
def resolve_record_id(base_id, table_id, name_field, name_value):
    records = mcp__airtable__list_records({
        "baseId": base_id,
        "tableId": table_id,
        "filterByFormula": f"{{{name_field}}} = '{name_value}'"
    })
    if records["records"]:
        return records["records"][0]["id"]
    return None

# Use in linked field
portco_id = resolve_record_id("appeY64iIwU5CEna7", "Portco", "Company Name", "Pigment")
if portco_id:
    fields["Portfolio Company"] = [portco_id]
```

---

## Attachment Fields

### Attachments

**Type:** `multipleAttachments`

**Description:** File uploads (images, PDFs, etc.)

**Value format:** Array of attachment objects

**Schema example:**
```json
{
  "name": "Resume",
  "type": "multipleAttachments"
}
```

**Value structure:**
```json
[
  {
    "url": "https://dl.airtable.com/...",
    "filename": "resume.pdf",
    "size": 102400,
    "type": "application/pdf"
  }
]
```

**Creating attachments:**
```python
# Upload from URL
fields["Resume"] = [
    {"url": "https://example.com/resume.pdf"}
]
```

**Common errors:**
- URL must be publicly accessible
- File size limits apply (depends on plan)

---

## Computed Fields

### Formula

**Type:** `formula`

**Description:** Computed value based on formula

**Value format:** Read-only (cannot set)

**Schema example:**
```json
{
  "name": "Full Name",
  "type": "formula",
  "options": {
    "formula": "CONCATENATE({First Name}, ' ', {Last Name})"
  }
}
```

**Important:**
- **Cannot write to formula fields**
- Omit from record creation/update
- Values automatically computed by Airtable

### Lookup

**Type:** `lookup`

**Description:** Value from linked record

**Value format:** Read-only (cannot set)

**Schema example:**
```json
{
  "name": "Company HQ",
  "type": "lookup",
  "options": {
    "fieldIdInLinkedTable": "fldAddress",
    "recordLinkFieldId": "fldPortco"
  }
}
```

**Important:**
- **Cannot write to lookup fields**
- Automatically populated from linked records

### Rollup

**Type:** `rollup`

**Description:** Aggregation of linked record values

**Value format:** Read-only (cannot set)

**Schema example:**
```json
{
  "name": "Total Searches",
  "type": "rollup",
  "options": {
    "fieldIdInLinkedTable": "fldStatus",
    "recordLinkFieldId": "fldSearches",
    "aggregationFunction": "COUNT"
  }
}
```

**Important:**
- **Cannot write to rollup fields**
- Automatically computed

### Count

**Type:** `count`

**Description:** Count of linked records

**Value format:** Read-only (cannot set)

**Important:**
- **Cannot write to count fields**
- Automatically updated when links change

---

## Other Fields

### Checkbox

**Type:** `checkbox`

**Description:** Boolean true/false

**Value format:** Boolean

**Schema example:**
```json
{
  "name": "Active",
  "type": "checkbox"
}
```

**Validation:**
- Must be boolean: `true` or `false`
- Don't use strings: `"true"` will fail

**Common errors:**
- Using 1/0 or "true"/"false" strings
- **Fix:** Use actual boolean values

### Barcode

**Type:** `barcode`

**Description:** Barcode/QR code

**Value format:** Object with text

**Schema example:**
```json
{
  "name": "Product Code",
  "type": "barcode"
}
```

**Value structure:**
```json
{"text": "123456789"}
```

### Button

**Type:** `button`

**Description:** Clickable button (read-only in API)

**Value format:** Read-only (cannot set)

**Important:**
- Cannot interact with buttons via API
- Used for automation triggers in UI

---

## Field Type Summary Table

| Type | Writable | Value Format | Key Validation |
|------|----------|--------------|----------------|
| singleLineText | ✅ | String | None |
| multilineText | ✅ | String | None |
| email | ✅ | String | Valid email format |
| url | ✅ | String | Valid URL with protocol |
| number | ✅ | Number | Must be numeric |
| currency | ✅ | Number | Must be numeric |
| percent | ✅ | Number | Must be numeric (0-1) |
| rating | ✅ | Number | Integer within max |
| singleSelect | ✅ | String | Must match option exactly |
| multipleSelects | ✅ | Array[String] | Each must match option |
| date | ✅ | String | YYYY-MM-DD format |
| dateTime | ✅ | String | ISO 8601 with timezone |
| multipleRecordLinks | ✅ | Array[String] | Valid record IDs |
| multipleAttachments | ✅ | Array[Object] | Valid URL or file |
| checkbox | ✅ | Boolean | true or false |
| barcode | ✅ | Object | {text: string} |
| formula | ❌ | (varies) | Read-only |
| lookup | ❌ | (varies) | Read-only |
| rollup | ❌ | (varies) | Read-only |
| count | ❌ | Number | Read-only |
| button | ❌ | N/A | Read-only |

---

## Common Validation Patterns

### Validate All Fields Before Record Creation

```python
def validate_record(schema, record_data):
    """Validate record data against schema"""
    validated = {}
    errors = []

    for field in schema["fields"]:
        field_name = field["name"]
        field_type = field["type"]
        value = record_data.get(field_name)

        # Skip if no value provided
        if value is None:
            # Check if required
            if field.get("required", False):
                errors.append(f"Required field '{field_name}' missing")
            continue

        # Skip read-only fields
        if field_type in ["formula", "lookup", "rollup", "count", "button"]:
            continue

        # Type-specific validation
        if field_type == "singleSelect":
            valid_options = [c["name"] for c in field["options"]["choices"]]
            if value not in valid_options:
                errors.append(f"'{value}' not in {valid_options} for {field_name}")
                continue

        elif field_type == "multipleSelects":
            valid_options = {c["name"] for c in field["options"]["choices"]}
            for v in value:
                if v not in valid_options:
                    errors.append(f"'{v}' not valid for {field_name}")
                    continue

        elif field_type == "date":
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Invalid date format for {field_name}: {value}")
                continue

        elif field_type == "dateTime":
            if not value.endswith("Z"):
                errors.append(f"DateTime must have UTC timezone (Z) for {field_name}")
                continue

        elif field_type in ["number", "currency", "percent", "rating"]:
            if not isinstance(value, (int, float)):
                errors.append(f"{field_name} must be numeric, got {type(value)}")
                continue

        elif field_type == "checkbox":
            if not isinstance(value, bool):
                errors.append(f"{field_name} must be boolean, got {type(value)}")
                continue

        # Add to validated data
        validated[field_name] = value

    return validated, errors
```

---

## Additional Resources

- [Schema Reference](schema_reference.md) - Complete schema exploration guide
- [Troubleshooting Guide](troubleshooting.md) - Common issues & solutions
- Official Airtable Field Types: https://airtable.com/developers/web/api/field-model
