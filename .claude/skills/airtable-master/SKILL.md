---
name: airtable-master
description: Comprehensive Airtable database management through MCP integration. Use for querying records, managing data (create, update, delete), exploring schemas (tables, fields, views), searching content, workflow automation, data validation, batch operations, commenting on records, and working with Airtable bases, tables, fields, records, views, formulas, linked records, attachments, collaborators, and API integration. Supports CRM, project management, inventory tracking, content planning, and custom database applications.
---

# Airtable Skill

Work effectively with Airtable databases through MCP integration for data management, schema exploration, and automation.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Core Operations](#core-operations)
  - [1. Schema Exploration](#1-schema-exploration)
  - [2. Record Operations](#2-record-operations)
  - [3. Filtering & Sorting](#3-filtering--sorting)
  - [4. Schema Modification](#4-schema-modification)
  - [5. Comments](#5-comments)
- [Advanced Features](#advanced-features)
  - [Batch Operations](#batch-operations)
  - [Data Validation](#data-validation)
  - [Schema Analysis](#schema-analysis)
  - [Data Export](#data-export)
- [Performance Optimization](#performance-optimization)
- [Error Handling](#error-handling)
- [Workflow Patterns](#workflow-patterns)
- [Use Case Examples](#use-case-examples)
- [Helper Scripts](#helper-scripts)
- [Reference Documentation](#reference-documentation)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Related Skills](#related-skills)
- [Resources](#resources)

## Prerequisites

Requires Airtable MCP server configured with valid API token. See [Airtable MCP Server](https://github.com/domdomegg/airtable-mcp-server).

## Quick Start

**List bases:** `list_bases` → base IDs and names
**Explore tables:** `list_tables(baseId, detailLevel='tableIdentifiersOnly')` → table names
**Query records:** `list_records(baseId, tableId, filterByFormula='{Status}="Active"')` → filtered results
**Create records:** `create_record(baseId, tableId, {fields})` → new record
**Search:** `search_records(baseId, tableId, searchTerm)` → matching records

## Core Operations

### 1. Schema Exploration

**Progressive detail loading** for efficiency:
- `tableIdentifiersOnly`: Table IDs/names only (lightest)
- `identifiersOnly`: Add field/view IDs/names  
- `full`: Complete schema with configurations (default)

**Workflow:**
```
list_bases() → list_tables(baseId, 'tableIdentifiersOnly') → describe_table(baseId, tableId, 'full')
```

**Tools:**
- `list_bases`: All accessible bases
- `list_tables(baseId, detailLevel)`: Tables in base
- `describe_table(baseId, tableId, detailLevel)`: Single table detail

**Best practice:** Use light detail levels for large bases (100+ tables), load full detail only when needed.

### 2. Record Operations

**List records:**
```
list_records(baseId, tableId, {
  maxRecords: 100,
  filterByFormula: '{Status}="Active"',
  view: 'High Priority',
  sort: [{field: 'Due Date', direction: 'asc'}]
})
```
Automatically handles pagination.

**Search records:**
```
search_records(baseId, tableId, searchTerm, {
  fieldIds: ['fldEmail', 'fldName'],  # Optional: specific fields
  maxRecords: 100,
  view: 'Active Customers'
})
```

**Get single record:**
```
get_record(baseId, tableId, recordId)
```

**Create record:**
```
create_record(baseId, tableId, {
  'Name': 'John Doe',
  'Email': 'john@example.com',
  'Status': 'Active'
})
```

**Update records** (batch up to 10):
```
update_records(baseId, tableId, [
  {id: 'rec1', fields: {Status: 'Complete'}},
  {id: 'rec2', fields: {Priority: 'High'}}
])
```

**Delete records:**
```
delete_records(baseId, tableId, ['rec1', 'rec2'])
```
Warning: Permanent deletion.

### 3. Filtering & Sorting

**Formulas:**
```
'{Priority}="High"'
'AND({Status}="Active", {Due Date}<TODAY())'
'OR({Type}="Bug", {Type}="Issue")'
'SEARCH("keyword", {Description})'
```

See [formula_examples.md](references/formula_examples.md) for comprehensive library.

**Views:** Use pre-configured filters/sorts
```
list_records(baseId, tableId, view='My Active Tasks')
```

**Sorting:**
```
sort: [{field: 'Priority', direction: 'desc'}, {field: 'Date', direction: 'asc'}]
```

### 4. Schema Modification

**Create table:**
```
create_table(baseId, name, fields, description)
```
Requirements: At least one field; primary field must be text, date, number, etc.

**Create field:**
```
create_field(baseId, tableId, {nested: {field: fieldConfig}})
```
See [field_types_guide.md](references/field_types_guide.md) for all field types.

**Update table/field:**
- Tables: Can modify name, description
- Fields: Can modify name, description only (not type/options)

Note: Cannot create formula fields via API (Airtable limitation).

### 5. Comments

**Create:**
```
create_comment(baseId, tableId, recordId, text, parentCommentId?)
```

**List:**
```
list_comments(baseId, tableId, recordId, pageSize?, offset?)
```
Returns newest to oldest with author, reactions, mentions.

## Advanced Features

### Batch Operations

For 10+ records, use `scripts/batch_operations.py`:
- Automatic chunking (10 records/batch)
- Progress tracking with ETA
- Error handling and partial success reporting
- Dry-run mode for testing
- Rate limiting built-in

**Example:**
```python
batch = BatchOperations(base_id, table_id)
results = batch.create_records(records, dry_run=False)
```

### Data Validation

Pre-flight checks with `scripts/data_validator.py`:
- Field type validation
- Required field checking
- Duplicate detection
- Format validation (email, URL, phone)
- Relationship integrity

**Example:**
```python
validator = DataValidator(table_schema)
results = validator.validate_records(records)
```

### Schema Analysis

Generate documentation with `scripts/schema_analyzer.py`:
- Entity-relationship diagrams
- Field statistics
- Relationship mapping
- Complexity metrics

**Example:**
```python
analyzer = SchemaAnalyzer(base_schema)
docs = analyzer.generate_documentation()
```

### Data Export

Export to multiple formats with `scripts/export_helpers.py`:
- CSV, JSON, Markdown, HTML, Excel
- Handles large datasets efficiently
- Custom formatting options

**Example:**
```python
exporter = ExportHelpers(records, schema)
exporter.to_excel('output.xlsx', include_formatting=True)
```

## Performance Optimization

### Large Bases (100+ tables)
1. Use `tableIdentifiersOnly` initially
2. Load full details only for target tables
3. Cache schema during session
4. Leverage views for filtering

### Large Datasets (1000+ records)
1. Filter server-side with `filterByFormula`
2. Limit `maxRecords` parameter
3. Process in chunks with batch operations
4. Use pagination for large results

### Rate Limiting
Airtable limits: 5 requests/second per base
- Batch operations handle automatically
- Add 0.2s delays in custom code
- Implement exponential backoff for retries

## Error Handling

**Common errors:**

**"INVALID_REQUEST_UNKNOWN"** - Invalid ID
→ Verify IDs with list_bases/list_tables

**"NOT_FOUND"** - Resource missing or no permission
→ Check token scopes and access

**"INVALID_VALUE_FOR_COLUMN"** - Data type mismatch
→ Validate with scripts/data_validator.py before operations

**"INVALID_PERMISSIONS"** - Token lacks scopes
→ Required: data.records:read, data.records:write, schema.bases:read

**"INVALID_FILTER_BY_FORMULA"** - Formula syntax error
→ Test in Airtable UI first, see formula_examples.md

### Validation Best Practices

**Before bulk operations:**
- Run data_validator.py
- Verify field types match
- Check required fields populated
- Confirm relationships exist

**Before deletions:**
- List records to confirm IDs
- Check for dependent linked records
- Consider archiving instead
- Maintain audit trail

**Before schema changes:**
- Document current structure
- Test on duplicate base
- Consider impact on existing data
- Plan rollback strategy

## Workflow Patterns

### Data Import
```
1. Validate source → scripts/data_validator.py
2. Map fields → describe_table for schema
3. Batch create → scripts/batch_operations.py
4. Verify → list_records with count
```

### Data Quality Audit
```
1. Export current → scripts/export_helpers.py
2. Validate → scripts/data_validator.py
3. Bulk fix → update_records or batch_operations.py
4. Verify → Re-run validation
```

### Schema Evolution
```
1. Document current → scripts/schema_analyzer.py
2. Create tables/fields → create_table, create_field
3. Migrate data → Batch operations with validation
4. Verify → Check relationships and data
```

See [workflow_templates.md](references/workflow_templates.md) for complete examples (CRM, projects, inventory, content, events, invoices).

## Use Case Examples

**CRM - Lead qualification:**
```
list_records(baseId, 'Leads', filterByFormula='AND({Status}="Demo Requested", {Last Contact}<DATEADD(TODAY(),-7,"days"))')
```

**Project Mgmt - Task assignment:**
```
update_records(baseId, 'Tasks', [{id: taskId, fields: {Assigned: [userId], Status: 'In Progress'}}])
create_comment(baseId, 'Tasks', taskId, 'Task assigned')
```

**Inventory - Stock alerts:**
```
list_records(baseId, 'Products', filterByFormula='{Current Stock}<{Reorder Point}')
```

**Content - Editorial calendar:**
```
list_records(baseId, 'Content', filterByFormula='AND({Publish Date}>=THIS_WEEK(), {Status}!="Published")')
```

## Helper Scripts

**batch_operations.py** - Bulk CRUD with chunking, progress, error handling
**data_validator.py** - Pre-flight validation, duplicate detection
**schema_analyzer.py** - Generate schema documentation, ER diagrams
**export_helpers.py** - Export to CSV/JSON/Excel/Markdown/HTML

When to use: 10+ records (batch), before imports (validator), documentation (analyzer), reporting (export).

## Reference Documentation

- **field_types_guide.md**: All field types with configuration examples
- **api_patterns.md**: Best practices, common patterns, anti-patterns
- **formula_examples.md**: Formula library organized by use case
- **workflow_templates.md**: Pre-built workflows for common scenarios
- **troubleshooting_guide.md**: Detailed error resolution and optimization

## Best Practices

**Data:** Validate before bulk operations, use dry-run, maintain audit trails, batch in chunks of 10
**Schema:** Document purposes, use descriptive names, test changes on duplicates
**Performance:** Progressive loading, cache schema, server-side filtering, leverage views
**Collaboration:** Use comments, document decisions, track changes, notify stakeholders

## Troubleshooting

**Skill not activating?**
1. Check MCP server running
2. Verify AIRTABLE_API_KEY set
3. Test: `list_bases()`

**Performance slow?**
1. Use lighter detail levels
2. Apply server-side filters
3. Cache schema
4. Process in chunks

**Permission errors?**
1. Verify token scopes
2. Check base access
3. Ensure token valid

See [troubleshooting_guide.md](references/troubleshooting_guide.md) for comprehensive diagnostics.

## Related Skills

- **xlsx**: Excel exports from Airtable
- **pdf**: Generate reports from data
- **docx**: Create documentation

## Resources

- [Airtable API Docs](https://airtable.com/developers/web/api/introduction)
- [Formula Reference](https://support.airtable.com/docs/formula-field-reference)
- [MCP Server GitHub](https://github.com/domdomegg/airtable-mcp-server)
