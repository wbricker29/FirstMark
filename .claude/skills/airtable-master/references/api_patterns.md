# Airtable API Patterns

Common patterns, best practices, and anti-patterns for working with the Airtable API through MCP.

## Table of Contents

1. [Core Patterns](#core-patterns)
2. [Performance Patterns](#performance-patterns)
3. [Error Handling](#error-handling)
4. [Data Integrity Patterns](#data-integrity-patterns)
5. [Anti-Patterns](#anti-patterns)

---

## Core Patterns

### Pattern: Progressive Schema Loading

**Problem:** Loading full schema for large bases wastes context

**Solution:** Use detail levels strategically

```
# Step 1: Light exploration
list_tables(baseId, detailLevel='tableIdentifiersOnly')
→ Returns: table IDs and names only

# Step 2: Targeted detail
describe_table(baseId, targetTableId, detailLevel='full')
→ Returns: complete schema for one table
```

**Benefits:**
- Reduces context usage
- Faster initial queries
- Load detail only when needed

---

### Pattern: View-Based Filtering

**Problem:** Complex filters are hard to maintain

**Solution:** Use pre-configured views

```
# Instead of:
list_records(
  baseId, 
  tableId,
  filterByFormula='AND({Status}="Active", {Priority}="High", {Due Date}<TODAY())'
)

# Use:
list_records(baseId, tableId, view='High Priority Active Tasks')
```

**Benefits:**
- Filters maintained in Airtable UI
- Reusable across operations
- Easier to test and modify

---

### Pattern: Batch with Validation

**Problem:** Bulk operations can fail partially

**Solution:** Validate before batch operations

```python
# 1. Validate data
validator = DataValidator(table_schema)
results = validator.validate_records(records)

if results['invalid'] > 0:
    print(f"Found {results['invalid']} invalid records")
    # Handle or fix errors
    return

# 2. Dry run
batch = BatchOperations(base_id, table_id)
batch.create_records(records, dry_run=True)

# 3. Execute
batch.create_records(records, dry_run=False)
```

**Benefits:**
- Catch errors before API calls
- Reduce failed batches
- Better error messages

---

### Pattern: Pagination Handling

**Problem:** Large result sets need pagination

**Solution:** MCP tools handle this automatically

```
# This automatically paginates:
all_records = list_records(baseId, tableId)

# Behind the scenes:
# - Fetches in pages
# - Follows offset tokens
# - Returns complete results
```

**Manual pagination (if needed):**
```python
offset = None
all_records = []

while True:
    params = {'offset': offset} if offset else {}
    result = api.list_records(baseId, tableId, **params)
    all_records.extend(result['records'])
    offset = result.get('offset')
    if not offset:
        break
```

---

### Pattern: Rate Limit Handling

**Problem:** Airtable limits 5 requests/second per base

**Solution:** Built into batch operations

```python
# Automatic rate limiting:
batch = BatchOperations(base_id, table_id)
# Includes 0.2s delay between batches

# Manual rate limiting:
import time
for batch in batches:
    process_batch(batch)
    time.sleep(0.2)  # 200ms delay
```

**Best practices:**
- Use batch operations for bulk work
- Add delays for custom implementations
- Monitor for 429 errors
- Implement exponential backoff

---

## Performance Patterns

### Pattern: Field Selection

**Problem:** Fetching unnecessary fields wastes bandwidth

**Solution:** Request only needed fields (when supported)

```
# Better: Minimal data transfer
records = list_records(
    baseId,
    tableId,
    filterByFormula='{Status}="Active"'
)

# Extract only needed fields
needed_data = [
    {'id': r['id'], 'name': r['fields']['Name']}
    for r in records
]
```

---

### Pattern: Server-Side Filtering

**Problem:** Client-side filtering wastes resources

**Solution:** Use filterByFormula

```
# ❌ Don't do this:
all_records = list_records(baseId, tableId)
active = [r for r in all_records if r['fields'].get('Status') == 'Active']

# ✅ Do this:
active = list_records(
    baseId,
    tableId,
    filterByFormula='{Status}="Active"'
)
```

**Benefits:**
- Less data transfer
- Faster response
- Lower memory usage

---

### Pattern: Caching Schema

**Problem:** Schema rarely changes but is fetched often

**Solution:** Cache schema during session

```python
class AirtableSession:
    def __init__(self):
        self.schema_cache = {}
    
    def get_table_schema(self, base_id, table_id):
        cache_key = f"{base_id}:{table_id}"
        
        if cache_key not in self.schema_cache:
            self.schema_cache[cache_key] = describe_table(
                base_id, table_id
            )
        
        return self.schema_cache[cache_key]
```

**When to clear cache:**
- After schema modifications
- At session end
- On explicit user request

---

### Pattern: Chunked Processing

**Problem:** Large datasets overwhelm memory

**Solution:** Process in chunks

```python
def process_large_dataset(base_id, table_id, processor_func):
    """Process records in manageable chunks"""
    offset = None
    chunk_size = 100
    
    while True:
        records = list_records(
            base_id,
            table_id,
            maxRecords=chunk_size,
            offset=offset
        )
        
        # Process chunk
        processor_func(records)
        
        # Check for more
        if len(records) < chunk_size:
            break
```

---

## Error Handling

### Pattern: Retry with Exponential Backoff

**Problem:** Transient failures need retry logic

**Solution:** Implement backoff strategy

```python
import time
from random import random

def retry_with_backoff(func, max_retries=3):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # Calculate delay: 2^attempt + random jitter
            delay = (2 ** attempt) + random()
            print(f"Retry {attempt + 1}/{max_retries} after {delay:.2f}s")
            time.sleep(delay)
```

---

### Pattern: Partial Success Handling

**Problem:** Batch operations can partially fail

**Solution:** Track and report partial success

```python
results = {
    'successful': [],
    'failed': [],
    'errors': []
}

for batch in batches:
    try:
        created = create_records(batch)
        results['successful'].extend(created)
    except Exception as e:
        results['failed'].extend(batch)
        results['errors'].append({
            'batch': batch,
            'error': str(e)
        })

# Report results
print(f"Success: {len(results['successful'])}")
print(f"Failed: {len(results['failed'])}")

# Handle failures
if results['failed']:
    retry_failed_records(results['failed'])
```

---

### Pattern: Validation Error Recovery

**Problem:** Invalid data causes cryptic errors

**Solution:** Validate and provide clear feedback

```python
def safe_create_record(base_id, table_id, fields, schema):
    """Create record with validation"""
    # Validate
    validator = DataValidator(schema)
    validation = validator.validate_records([{'fields': fields}])
    
    if validation['invalid'] > 0:
        errors = validation['errors'][0]['errors']
        raise ValueError(
            f"Validation failed: {', '.join(errors)}"
        )
    
    # Create
    return create_record(base_id, table_id, fields)
```

---

## Data Integrity Patterns

### Pattern: Relationship Verification

**Problem:** Linked records may not exist

**Solution:** Verify relationships before linking

```python
def verify_linked_records(
    base_id,
    source_table_id,
    target_table_id,
    record_ids
):
    """Verify target records exist"""
    existing = {}
    
    for record_id in record_ids:
        try:
            record = get_record(base_id, target_table_id, record_id)
            existing[record_id] = True
        except:
            existing[record_id] = False
    
    invalid = [rid for rid, exists in existing.items() if not exists]
    
    if invalid:
        raise ValueError(f"Invalid record IDs: {invalid}")
    
    return True
```

---

### Pattern: Duplicate Prevention

**Problem:** Creating duplicate records

**Solution:** Check before create

```python
def create_if_not_exists(
    base_id,
    table_id,
    fields,
    unique_field='Email'
):
    """Create record only if it doesn't exist"""
    unique_value = fields[unique_field]
    
    # Search for existing
    existing = search_records(
        base_id,
        table_id,
        unique_value,
        fieldIds=[get_field_id(table_id, unique_field)]
    )
    
    if existing:
        return existing[0]  # Return existing
    
    # Create new
    return create_record(base_id, table_id, fields)
```

---

### Pattern: Atomic Updates

**Problem:** Multi-step updates can fail partially

**Solution:** Plan rollback strategy

```python
def atomic_update(base_id, table_id, updates):
    """Update with rollback on failure"""
    original_values = []
    updated_records = []
    
    try:
        # Save original values
        for update in updates:
            record = get_record(base_id, table_id, update['id'])
            original_values.append(record)
        
        # Perform updates
        updated = update_records(base_id, table_id, updates)
        updated_records = updated
        
        return updated
        
    except Exception as e:
        # Rollback on error
        if original_values:
            print("Rolling back changes...")
            rollback_updates = [
                {'id': r['id'], 'fields': r['fields']}
                for r in original_values
            ]
            update_records(base_id, table_id, rollback_updates)
        
        raise
```

---

## Anti-Patterns

### ❌ Anti-Pattern: Fetching Full Base Repeatedly

**Problem:**
```python
# Bad: Fetches everything every time
for operation in operations:
    all_tables = list_tables(base_id, detailLevel='full')
    target_table = find_table(all_tables, operation.table_name)
    process(target_table)
```

**Solution:**
```python
# Good: Cache schema
schema_cache = list_tables(base_id, detailLevel='identifiersOnly')

for operation in operations:
    table_id = get_table_id(schema_cache, operation.table_name)
    # Fetch details only if needed
    if operation.needs_full_schema:
        table = describe_table(base_id, table_id, detailLevel='full')
    process(table)
```

---

### ❌ Anti-Pattern: Client-Side Joins

**Problem:**
```python
# Bad: Manual joins
customers = list_records(base_id, 'Customers')
orders = list_records(base_id, 'Orders')

# Inefficient client-side join
for customer in customers:
    customer['orders'] = [
        o for o in orders
        if customer['id'] in o['fields'].get('Customer', [])
    ]
```

**Solution:**
```python
# Good: Use Airtable's linked records
customers = list_records(base_id, 'Customers')
# Linked records already contain order IDs
# Use lookup/rollup fields for aggregations
```

---

### ❌ Anti-Pattern: Ignoring Rate Limits

**Problem:**
```python
# Bad: No rate limiting
for record in large_batch:
    create_record(base_id, table_id, record)
    # Will hit rate limits!
```

**Solution:**
```python
# Good: Batch with rate limiting
batch_ops = BatchOperations(base_id, table_id)
batch_ops.create_records(large_batch)
# Handles chunking and rate limiting
```

---

### ❌ Anti-Pattern: Hard-Coded IDs

**Problem:**
```python
# Bad: Hard-coded IDs break on copy
base_id = 'appABC123'
table_id = 'tblXYZ456'
```

**Solution:**
```python
# Good: Discover dynamically
bases = list_bases()
base = next(b for b in bases if b['name'] == 'Production CRM')
base_id = base['id']

tables = list_tables(base_id, detailLevel='tableIdentifiersOnly')
table = next(t for t in tables if t['name'] == 'Customers')
table_id = table['id']
```

---

### ❌ Anti-Pattern: Missing Error Context

**Problem:**
```python
# Bad: Generic error
try:
    create_record(base_id, table_id, fields)
except Exception as e:
    print("Error creating record")
```

**Solution:**
```python
# Good: Detailed context
try:
    create_record(base_id, table_id, fields)
except Exception as e:
    print(f"Failed to create record in table {table_id}")
    print(f"Fields: {fields}")
    print(f"Error: {e}")
    # Log full context for debugging
```

---

## Pattern Library Summary

| Pattern | Use When | Benefit |
|---------|----------|---------|
| Progressive Loading | Large bases | Reduced context usage |
| View-Based Filtering | Complex filters | Maintainability |
| Batch with Validation | Bulk operations | Fewer failures |
| Rate Limiting | High volume | Avoid API errors |
| Caching | Repeated queries | Performance |
| Retry with Backoff | Transient errors | Reliability |
| Relationship Verification | Linked records | Data integrity |
| Duplicate Prevention | Unique records | Data quality |

---

## Next Steps

- Review [Formula Examples](formula_examples.md) for filtering patterns
- See [Workflow Templates](workflow_templates.md) for complete examples
- Check [Troubleshooting Guide](troubleshooting_guide.md) for error resolution
