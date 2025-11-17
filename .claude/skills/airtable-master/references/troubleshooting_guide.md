# Airtable Troubleshooting Guide

Detailed error resolution and optimization tips for Airtable operations.

## Table of Contents

- [Quick Diagnostic Checklist](#quick-diagnostic-checklist)
- [Common Errors](#common-errors)
  - [1. Connection/Authentication Errors](#1-connectionauthentication-errors)
  - [2. Resource Not Found Errors](#2-resource-not-found-errors)
  - [3. Data Validation Errors](#3-data-validation-errors)
  - [4. Rate Limiting](#4-rate-limiting)
  - [5. Performance Issues](#5-performance-issues)
  - [6. Data Integrity Issues](#6-data-integrity-issues)
- [Optimization Tips](#optimization-tips)
  - [Schema Optimization](#schema-optimization)
  - [Query Optimization](#query-optimization)
  - [Batch Optimization](#batch-optimization)
- [Diagnostic Scripts](#diagnostic-scripts)
  - [Connection Test](#connection-test)
  - [Permission Test](#permission-test)
  - [Performance Profiler](#performance-profiler)
- [Getting Help](#getting-help)
  - [Information to Provide](#information-to-provide)
  - [Support Resources](#support-resources)
- [Troubleshooting Flowchart](#troubleshooting-flowchart)

## Quick Diagnostic Checklist

When encountering issues, check these first:

- [ ] Is the Airtable MCP server running?
- [ ] Is the API key valid and properly configured?
- [ ] Does the key have required permissions?
- [ ] Are base/table/record IDs correct?
- [ ] Is there network connectivity?
- [ ] Are there any rate limit warnings?

---

## Common Errors

### 1. Connection/Authentication Errors

#### "No API key provided"

**Symptoms:**
- Can't list bases
- Authentication failures
- Immediate errors on any operation

**Causes:**
- AIRTABLE_API_KEY not set
- API key not passed to MCP server
- Empty or whitespace-only key

**Solutions:**
```bash
# Check environment variable
echo $AIRTABLE_API_KEY

# Verify in MCP configuration
# Should see something like: "pat123.abc456..."

# Regenerate key if needed:
# 1. Go to https://airtable.com/create/tokens
# 2. Create new token
# 3. Update configuration
```

---

#### "INVALID_PERMISSIONS"

**Symptoms:**
- Can list bases but not access tables
- Can read but not write
- Missing operations

**Causes:**
- Token lacks required scopes
- Base-level permissions insufficient
- Workspace restrictions

**Solutions:**
```
1. Check token scopes:
   Required:
   - schema.bases:read
   - data.records:read
   - data.records:write (for modifications)
   - data.recordComments:read (for comments)
   - data.recordComments:write (for comments)

2. Check base access:
   - Token must have access to specific bases
   - Verify in token configuration

3. Verify workspace permissions:
   - User must have appropriate workspace role
```

---

### 2. Resource Not Found Errors

#### "NOT_FOUND" or "INVALID_REQUEST_UNKNOWN"

**Symptoms:**
- "Table not found"
- "Record does not exist"
- "Base not accessible"

**Causes:**
- Incorrect ID (typo, wrong base)
- Resource was deleted
- Insufficient permissions
- Case sensitivity issue

**Solutions:**
```python
# Verify base exists:
bases = list_bases()
print([b['name'] for b in bases])

# Verify table exists:
tables = list_tables(base_id, detailLevel='tableIdentifiersOnly')
print([t['name'] for t in tables])

# Verify record exists:
try:
    record = get_record(base_id, table_id, record_id)
    print("Record found")
except:
    print("Record not found - check ID")

# Common mistakes:
# - Using table name instead of ID
# - Copy/paste errors in IDs
# - IDs from different base
```

---

### 3. Data Validation Errors

#### "INVALID_VALUE_FOR_COLUMN"

**Symptoms:**
- Create/update fails
- "Field expects X but got Y"
- Type mismatch errors

**Causes:**
- Wrong data type for field
- Invalid choice for select field
- Bad format for date/email/URL
- Missing required fields

**Solutions:**
```python
# 1. Check field types:
table = describe_table(base_id, table_id)
for field in table['fields']:
    print(f"{field['name']}: {field['type']}")

# 2. Validate before operation:
from scripts.data_validator import DataValidator

validator = DataValidator(table_schema)
results = validator.validate_records(records)

if results['invalid'] > 0:
    print("Validation errors:")
    for error in results['errors']:
        print(error)

# 3. Common fixes:
# - Use number type for numeric fields (not string)
# - Match select options exactly (case-sensitive)
# - Use ISO date format: "2024-01-15"
# - Provide required fields
```

---

#### "INVALID_FILTER_BY_FORMULA"

**Symptoms:**
- Filter doesn't work
- Syntax error in formula
- Unexpected results

**Causes:**
- Formula syntax error
- Invalid field reference
- Wrong comparison operator
- Unclosed braces/parentheses

**Solutions:**
```
# 1. Test formula in Airtable UI first
#    - Create temporary formula field
#    - Verify it works
#    - Copy exact syntax

# 2. Common issues:
# - Field names must be in {curly braces}
# - Strings in "quotes"
# - Case-sensitive field names
# - Check for typos

# 3. Debug step by step:
# Start simple:
{Status} = "Active"

# Add complexity:
AND({Status} = "Active", {Priority} = "High")

# Full formula:
AND(
  {Status} = "Active",
  {Priority} = "High",
  {Due Date} < TODAY()
)
```

---

### 4. Rate Limiting

#### "Too many requests" / 429 errors

**Symptoms:**
- Operations fail after working
- Intermittent errors
- Slowdowns during bulk operations

**Causes:**
- Exceeding 5 requests/second per base
- Too many concurrent operations
- No rate limiting in custom code

**Solutions:**
```python
# 1. Use batch operations (built-in rate limiting):
from scripts.batch_operations import BatchOperations

batch = BatchOperations(base_id, table_id)
batch.create_records(records)  # Handles rate limits

# 2. Add delays in custom code:
import time

for record in records:
    create_record(base_id, table_id, record)
    time.sleep(0.2)  # 200ms delay = 5 req/sec

# 3. Implement exponential backoff:
def with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 1s, 2s, 4s
            else:
                raise

# 4. Reduce parallel operations:
# - Process sequentially instead of parallel
# - Batch operations together
# - Add delays between batches
```

---

### 5. Performance Issues

#### Slow Queries

**Symptoms:**
- Long wait times for results
- Timeouts on large tables
- High memory usage

**Diagnosis:**
```python
import time

# Measure query time:
start = time.time()
records = list_records(base_id, table_id)
elapsed = time.time() - start

print(f"Query took {elapsed:.2f} seconds")
print(f"Retrieved {len(records)} records")

# Check table size:
table = describe_table(base_id, table_id)
print(f"Table has {len(table['fields'])} fields")
```

**Solutions:**
```python
# 1. Use filtering to reduce data:
# Instead of:
all_records = list_records(base_id, table_id)
active = [r for r in all_records if r['fields']['Status'] == 'Active']

# Do:
active = list_records(
    base_id,
    table_id,
    filterByFormula='{Status}="Active"'
)

# 2. Limit record count:
records = list_records(
    base_id,
    table_id,
    maxRecords=100  # Get first 100 only
)

# 3. Use lighter detail levels:
tables = list_tables(
    base_id,
    detailLevel='tableIdentifiersOnly'  # Much faster
)

# 4. Cache schema:
schema_cache = describe_table(base_id, table_id)
# Reuse schema_cache instead of fetching repeatedly

# 5. Process in chunks:
offset = None
while True:
    batch = list_records(
        base_id,
        table_id,
        maxRecords=100,
        offset=offset
    )
    process_batch(batch)
    if not batch.get('offset'):
        break
    offset = batch['offset']
```

---

#### High Memory Usage

**Symptoms:**
- Python process uses lots of RAM
- Crashes on large datasets
- System slowdown

**Solutions:**
```python
# 1. Process in chunks (don't load all at once):
def process_large_table(base_id, table_id, processor):
    """Process records in chunks"""
    processed = 0
    offset = None
    
    while True:
        records = list_records(
            base_id,
            table_id,
            maxRecords=100,
            offset=offset
        )
        
        processor(records)
        processed += len(records)
        print(f"Processed {processed} records")
        
        if not records.get('offset'):
            break
        offset = records['offset']

# 2. Use generators instead of lists:
def record_generator(base_id, table_id):
    """Yield records one at a time"""
    offset = None
    while True:
        batch = list_records(base_id, table_id, maxRecords=100, offset=offset)
        for record in batch:
            yield record
        if not batch.get('offset'):
            break
        offset = batch['offset']

# 3. Export to file instead of keeping in memory:
from scripts.export_helpers import ExportHelpers

# Stream to CSV:
with open('export.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    
    for record in record_generator(base_id, table_id):
        writer.writerow(record['fields'])
```

---

### 6. Data Integrity Issues

#### Orphaned Linked Records

**Symptoms:**
- Linked record fields show deleted records
- Relationships broken
- Missing data in lookups

**Diagnosis:**
```python
# Find orphaned links:
records = list_records(base_id, table_id)

for record in records:
    linked_field = record['fields'].get('Customer', [])
    for linked_id in linked_field:
        try:
            get_record(base_id, 'Customers', linked_id)
        except:
            print(f"Orphaned link: {record['id']} -> {linked_id}")
```

**Solutions:**
```python
# 1. Remove orphaned links:
updates = []
for record in records_with_orphans:
    valid_links = []
    for linked_id in record['fields']['Customer']:
        try:
            get_record(base_id, 'Customers', linked_id)
            valid_links.append(linked_id)
        except:
            pass  # Skip orphaned
    
    if valid_links != record['fields']['Customer']:
        updates.append({
            'id': record['id'],
            'fields': {'Customer': valid_links}
        })

batch_ops.update_records(updates)

# 2. Verify before creating links:
def safe_link_records(base_id, source_table, record_id, target_table, target_ids):
    """Only link to existing records"""
    valid_targets = []
    for target_id in target_ids:
        try:
            get_record(base_id, target_table, target_id)
            valid_targets.append(target_id)
        except:
            print(f"Skipping invalid link: {target_id}")
    
    if valid_targets:
        update_records(
            base_id,
            source_table,
            [{
                'id': record_id,
                'fields': {'Linked Field': valid_targets}
            }]
        )
```

---

#### Duplicate Records

**Symptoms:**
- Same data appears multiple times
- Unique constraints violated
- Inflated record counts

**Detection:**
```python
from scripts.data_validator import DataValidator

# Check for duplicates:
validator = DataValidator(table_schema)
results = validator.validate_records(records, check_duplicates=True)

if results['errors']:
    for error in results['errors']:
        if error['type'] == 'duplicate':
            print(f"Duplicate {error['field']}: {error['value']}")
            print(f"Records: {error['records']}")
```

**Prevention:**
```python
def create_if_unique(base_id, table_id, fields, unique_field='Email'):
    """Only create if unique"""
    value = fields[unique_field]
    
    # Search for existing
    existing = search_records(
        base_id,
        table_id,
        value,
        fieldIds=[unique_field]
    )
    
    if existing:
        print(f"Duplicate found: {value}")
        return existing[0]
    
    return create_record(base_id, table_id, fields)
```

---

## Optimization Tips

### Schema Optimization

**1. Field Organization:**
```
✅ Good:
- Logical field grouping
- Clear naming conventions
- Minimal computed fields

❌ Bad:
- Random field order
- Cryptic names (fld1, fld2)
- Excessive formula fields
```

**2. Relationship Design:**
```
✅ Good:
- Bidirectional links
- Appropriate cardinality
- Lookup fields for display

❌ Bad:
- One-way links only
- Self-referential loops
- Excessive nested lookups
```

---

### Query Optimization

**1. Filtering:**
```
✅ Good:
# Server-side filtering
list_records(
    base_id,
    table_id,
    filterByFormula='{Status}="Active"'
)

❌ Bad:
# Client-side filtering
all_records = list_records(base_id, table_id)
active = [r for r in all_records if r['fields']['Status'] == 'Active']
```

**2. Field Selection:**
```
✅ Good:
# Minimal schema loading
tables = list_tables(base_id, detailLevel='tableIdentifiersOnly')

❌ Bad:
# Loading everything
tables = list_tables(base_id, detailLevel='full')
# When you only need names
```

---

### Batch Optimization

**1. Chunking:**
```
✅ Good:
# Proper batch size
batch_ops.create_records(records)  # Handles chunks of 10

❌ Bad:
# Individual operations
for record in records:
    create_record(base_id, table_id, record)
```

**2. Rate Limiting:**
```
✅ Good:
# Built-in delays
batch = BatchOperations(base_id, table_id)
# Includes 0.2s between batches

❌ Bad:
# No rate limiting
for batch in batches:
    process(batch)  # Will hit limits
```

---

## Diagnostic Scripts

### Connection Test
```python
def test_connection():
    """Test Airtable connection"""
    try:
        bases = list_bases()
        print(f"✓ Connected: Found {len(bases)} bases")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False
```

### Permission Test
```python
def test_permissions(base_id, table_id):
    """Test read/write permissions"""
    results = {
        'read_bases': False,
        'read_schema': False,
        'read_records': False,
        'write_records': False
    }
    
    try:
        list_bases()
        results['read_bases'] = True
    except:
        pass
    
    try:
        list_tables(base_id)
        results['read_schema'] = True
    except:
        pass
    
    try:
        list_records(base_id, table_id, maxRecords=1)
        results['read_records'] = True
    except:
        pass
    
    try:
        # Try creating/deleting test record
        test_record = create_record(
            base_id,
            table_id,
            {'Test Field': 'test'}
        )
        delete_records(base_id, table_id, [test_record['id']])
        results['write_records'] = True
    except:
        pass
    
    return results
```

### Performance Profiler
```python
import time
from functools import wraps

def profile(func):
    """Profile function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@profile
def my_operation():
    # Your code here
    pass
```

---

## Getting Help

### Information to Provide

When reporting issues, include:

1. **Error message** (full text)
2. **Operation attempted** (what you were trying to do)
3. **Base/table structure** (relevant schema)
4. **Code sample** (minimal reproduction)
5. **Environment** (OS, Python version, MCP version)

### Support Resources

- **Airtable API Docs**: https://airtable.com/developers/web/api/introduction
- **MCP Server Issues**: https://github.com/domdomegg/airtable-mcp-server/issues
- **Formula Reference**: https://support.airtable.com/docs/formula-field-reference

---

## Troubleshooting Flowchart

```
Problem occurs
    ├─> Can't connect?
    │   ├─> Check API key
    │   ├─> Verify MCP server running
    │   └─> Test network
    │
    ├─> Permission error?
    │   ├─> Check token scopes
    │   ├─> Verify base access
    │   └─> Check workspace role
    │
    ├─> Resource not found?
    │   ├─> Verify IDs correct
    │   ├─> Check resource exists
    │   └─> Test with list operations
    │
    ├─> Data validation error?
    │   ├─> Check field types
    │   ├─> Validate data format
    │   └─> Review required fields
    │
    ├─> Performance issue?
    │   ├─> Add filtering
    │   ├─> Reduce detail level
    │   ├─> Process in chunks
    │   └─> Cache schema
    │
    └─> Still stuck?
        └─> Review this guide
            Check examples
            Run diagnostic scripts
            Seek community help
```
