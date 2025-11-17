# Airtable Field Types Guide

Complete reference for all Airtable field types, configuration options, and best practices.

## Table of Contents

1. [Text Fields](#text-fields)
2. [Numeric Fields](#numeric-fields)
3. [Date & Time Fields](#date--time-fields)
4. [Selection Fields](#selection-fields)
5. [Relationship Fields](#relationship-fields)
6. [Attachment Fields](#attachment-fields)
7. [Collaborator Fields](#collaborator-fields)
8. [Computed Fields](#computed-fields)
9. [Special Fields](#special-fields)

---

## Text Fields

### Single Line Text (`singleLineText`)

**Purpose:** Short text entries (names, titles, IDs)

**Configuration:**
```json
{
  "name": "Product Name",
  "type": "singleLineText",
  "description": "The product display name"
}
```

**Best practices:**
- Use for names, identifiers, short labels
- Avoid for long descriptions (use multilineText)
- Maximum ~100,000 characters (practical limit)

**Common use cases:**
- Names, titles, labels
- SKUs, product codes
- Short descriptions

---

### Long Text (`multilineText`)

**Purpose:** Multi-line text with line breaks

**Configuration:**
```json
{
  "name": "Description",
  "type": "multilineText",
  "description": "Detailed product description"
}
```

**Best practices:**
- Use for descriptions, notes, comments
- Supports line breaks and basic formatting
- Better for content > 100 characters

**Common use cases:**
- Descriptions, notes
- Comments, feedback
- Multi-paragraph content

---

### Rich Text (`richText`)

**Purpose:** Formatted text with styling

**Configuration:**
```json
{
  "name": "Content",
  "type": "richText",
  "description": "Formatted article content"
}
```

**Best practices:**
- Use when formatting is important
- Supports bold, italic, links, lists
- Larger storage requirement

---

## Numeric Fields

### Number (`number`)

**Purpose:** Numeric values with decimals

**Configuration:**
```json
{
  "name": "Quantity",
  "type": "number",
  "description": "Item quantity",
  "options": {
    "precision": 2
  }
}
```

**Options:**
- `precision`: Decimal places (0-8)

**Best practices:**
- Use for quantities, measurements, calculations
- Set appropriate precision
- Consider currency type for money

---

### Currency (`currency`)

**Purpose:** Monetary values

**Configuration:**
```json
{
  "name": "Price",
  "type": "currency",
  "description": "Product price",
  "options": {
    "precision": 2,
    "symbol": "$"
  }
}
```

**Options:**
- `precision`: Decimal places (0-7)
- `symbol`: Currency symbol ($, €, £, etc.)

**Best practices:**
- Always use for money
- Match precision to currency (2 for USD/EUR)
- Be consistent with symbol across base

---

### Percent (`percent`)

**Purpose:** Percentage values

**Configuration:**
```json
{
  "name": "Discount",
  "type": "percent",
  "description": "Discount percentage",
  "options": {
    "precision": 1
  }
}
```

**Options:**
- `precision`: Decimal places (0-8)

**Best practices:**
- Stores as decimal (0.15 = 15%)
- Use for rates, percentages, ratios
- Set precision based on use case

---

### Duration (`duration`)

**Purpose:** Time durations

**Configuration:**
```json
{
  "name": "Task Duration",
  "type": "duration",
  "description": "Time to complete task",
  "options": {
    "durationFormat": "h:mm:ss"
  }
}
```

**Options:**
- `durationFormat`: "h:mm", "h:mm:ss", "h:mm:ss.S", "h:mm:ss.SS", "h:mm:ss.SSS"

**Best practices:**
- Use for time tracking, video lengths
- Choose format based on precision needed
- Stored as seconds internally

---

## Date & Time Fields

### Date (`date`)

**Purpose:** Date without time

**Configuration:**
```json
{
  "name": "Due Date",
  "type": "date",
  "description": "Task due date",
  "options": {
    "dateFormat": {
      "name": "us",
      "format": "M/D/YYYY"
    }
  }
}
```

**Options:**
- `dateFormat.name`: "local", "friendly", "us", "european", "iso"
- `dateFormat.format`: "l", "LL", "M/D/YYYY", "D/M/YYYY", "YYYY-MM-DD"

**Best practices:**
- Use when time is not relevant
- Choose format for your locale
- ISO format for data exchange

---

### Date & Time (`dateTime`)

**Purpose:** Date with time and timezone

**Configuration:**
```json
{
  "name": "Created At",
  "type": "dateTime",
  "description": "Record creation timestamp",
  "options": {
    "dateFormat": {
      "name": "iso",
      "format": "YYYY-MM-DD"
    },
    "timeFormat": {
      "name": "24hour",
      "format": "HH:mm"
    },
    "timeZone": "America/New_York"
  }
}
```

**Options:**
- `dateFormat`: Same as date field
- `timeFormat.name`: "12hour" or "24hour"
- `timeFormat.format`: "h:mma" or "HH:mm"
- `timeZone`: IANA timezone string

**Best practices:**
- Use for timestamps, appointments
- Be explicit about timezone
- ISO format for APIs

---

## Selection Fields

### Single Select (`singleSelect`)

**Purpose:** Choose one option from list

**Configuration:**
```json
{
  "name": "Status",
  "type": "singleSelect",
  "description": "Current status",
  "options": {
    "choices": [
      {"name": "Active", "color": "greenBright"},
      {"name": "Pending", "color": "yellowBright"},
      {"name": "Inactive", "color": "grayBright"}
    ]
  }
}
```

**Options:**
- `choices`: Array of {name, color, id}
- Colors: greenBright, blueBright, redBright, etc.

**Best practices:**
- Use for status, category, priority
- Limit to 10-15 choices max
- Use descriptive names
- Color code logically

---

### Multiple Selects (`multipleSelects`)

**Purpose:** Choose multiple options from list

**Configuration:**
```json
{
  "name": "Tags",
  "type": "multipleSelects",
  "description": "Content tags",
  "options": {
    "choices": [
      {"name": "Featured"},
      {"name": "Urgent"},
      {"name": "Archived"}
    ]
  }
}
```

**Best practices:**
- Use for tags, categories, features
- Better than many checkbox fields
- Keep choice list manageable

---

### Checkbox (`checkbox`)

**Purpose:** Boolean true/false value

**Configuration:**
```json
{
  "name": "Is Complete",
  "type": "checkbox",
  "description": "Task completion status",
  "options": {
    "color": "greenBright",
    "icon": "check"
  }
}
```

**Options:**
- `icon`: check, xCheckbox, star, heart, thumbsUp, flag, dot
- `color`: greenBright, blueBright, etc.

**Best practices:**
- Use for binary states
- Choose meaningful icons
- Default is unchecked

---

## Relationship Fields

### Linked Records (`multipleRecordLinks`)

**Purpose:** Link to records in another table

**Configuration:**
```json
{
  "name": "Customers",
  "type": "multipleRecordLinks",
  "description": "Related customer records",
  "options": {
    "linkedTableId": "tblXXXXXXXXXXXXXX",
    "viewIdForRecordSelection": "viwYYYYYYYYYYYYYY"
  }
}
```

**Options:**
- `linkedTableId`: Target table ID (required)
- `viewIdForRecordSelection`: View to show when selecting
- `prefersSingleRecordLink`: Limit to one record

**Best practices:**
- Create bidirectional links
- Name clearly (plural for multiple)
- Use views for record selection filtering

**Common patterns:**
- One-to-many: Orders → Customer
- Many-to-many: Students ↔ Courses
- Self-referential: Tasks → Blocked By Tasks

---

## Attachment Fields

### Attachments (`multipleAttachments`)

**Purpose:** Upload files and images

**Configuration:**
```json
{
  "name": "Documents",
  "type": "multipleAttachments",
  "description": "Related documents and files"
}
```

**Best practices:**
- Use for images, PDFs, documents
- No file type restrictions
- 20 GB per base limit
- Accessible via URL

---

## Collaborator Fields

### Single Collaborator (`singleCollaborator`)

**Purpose:** Assign one person

**Configuration:**
```json
{
  "name": "Owner",
  "type": "singleCollaborator",
  "description": "Record owner"
}
```

**Best practices:**
- Use for ownership, responsibility
- Limited to base collaborators
- Useful for permissions

---

### Multiple Collaborators (`multipleCollaborators`)

**Purpose:** Assign multiple people

**Configuration:**
```json
{
  "name": "Team Members",
  "type": "multipleCollaborators",
  "description": "Assigned team"
}
```

**Best practices:**
- Use for team assignments
- Good for notification triggers

---

## Computed Fields

### Formula (Read-only)

**Purpose:** Calculated values

**Note:** Cannot be created via API (Airtable limitation)

**Best practices:**
- Create manually in Airtable UI
- Use for calculations, concatenation
- Reference other fields
- Cannot be written to via API

---

### Rollup

**Purpose:** Aggregate linked records

**Configuration:**
```json
{
  "name": "Total Revenue",
  "type": "rollup",
  "description": "Sum of order amounts",
  "options": {
    "fieldIdInLinkedTable": "fldAmount",
    "recordLinkFieldId": "fldOrders"
  }
}
```

**Options:**
- `recordLinkFieldId`: Linked record field
- `fieldIdInLinkedTable`: Field to aggregate
- `formula`: Aggregation function

**Best practices:**
- Use for summaries, counts
- Common functions: SUM, COUNT, AVG

---

### Lookup

**Purpose:** Display linked record fields

**Configuration:**
```json
{
  "name": "Customer Name",
  "type": "lookup",
  "description": "Name from customer record",
  "options": {
    "recordLinkFieldId": "fldCustomer",
    "fieldIdInLinkedTable": "fldName"
  }
}
```

**Best practices:**
- Use to show linked data
- More efficient than formulas
- Read-only field

---

## Special Fields

### Auto Number (`autoNumber`)

**Purpose:** Automatically incrementing number

**Configuration:**
```json
{
  "name": "Order Number",
  "type": "autoNumber",
  "description": "Unique order identifier"
}
```

**Best practices:**
- Use for sequential IDs
- Cannot be edited or reset
- Starts at 1

---

### Created Time (`createdTime`)

**Purpose:** Record creation timestamp

**Configuration:**
```json
{
  "name": "Created",
  "type": "createdTime"
}
```

**Best practices:**
- Automatically set
- Cannot be edited
- Useful for auditing

---

### Last Modified Time (`lastModifiedTime`)

**Purpose:** Last edit timestamp

**Configuration:**
```json
{
  "name": "Last Modified",
  "type": "lastModifiedTime",
  "options": {
    "referencedFieldIds": ["fldStatus", "fldPriority"]
  }
}
```

**Options:**
- `referencedFieldIds`: Track specific fields only

**Best practices:**
- Track all changes or specific fields
- Good for change tracking

---

### Created By (`createdBy`)

**Purpose:** Who created the record

**Configuration:**
```json
{
  "name": "Created By",
  "type": "createdBy"
}
```

**Best practices:**
- Automatically set
- Shows collaborator
- Good for accountability

---

### Last Modified By (`lastModifiedBy`)

**Purpose:** Who last edited

**Configuration:**
```json
{
  "name": "Last Modified By",
  "type": "lastModifiedBy"
}
```

**Best practices:**
- Tracks last editor
- Useful for auditing

---

## Field Type Selection Guide

| Use Case | Recommended Field Type |
|----------|----------------------|
| Names, titles | singleLineText |
| Long descriptions | multilineText |
| Money amounts | currency |
| Quantities | number |
| Percentages | percent |
| Dates only | date |
| Timestamps | dateTime |
| Status/category | singleSelect |
| Tags | multipleSelects |
| Yes/no | checkbox |
| Relationships | multipleRecordLinks |
| Files/images | multipleAttachments |
| Person assignment | singleCollaborator |
| Team assignment | multipleCollaborators |
| Calculations | formula |
| Aggregations | rollup |
| Sequential IDs | autoNumber |

---

## Common Pitfalls

### ❌ Wrong Field Types

**Problem:** Using text for numbers
```json
{"name": "Price", "type": "singleLineText"}
```

**Solution:** Use proper numeric type
```json
{"name": "Price", "type": "currency", "options": {"precision": 2}}
```

---

### ❌ Too Many Single Selects

**Problem:** Separate field for each tag
```json
{"name": "Is Featured", "type": "checkbox"}
{"name": "Is Urgent", "type": "checkbox"}
{"name": "Is Archived", "type": "checkbox"}
```

**Solution:** Use multipleSelects
```json
{"name": "Tags", "type": "multipleSelects"}
```

---

### ❌ Missing Descriptions

**Problem:** Unclear field purpose
```json
{"name": "Value", "type": "number"}
```

**Solution:** Add clear descriptions
```json
{"name": "Value", "type": "number", "description": "Total order value in USD"}
```

---

## API Limitations

**Cannot create via API:**
- Formula fields
- Button fields
- AI text fields

**Cannot modify via API:**
- Field type changes
- Field options (after creation)
- Computed field formulas

**Workarounds:**
- Create formulas manually in UI
- Plan field structure carefully
- Test with duplicate base first
