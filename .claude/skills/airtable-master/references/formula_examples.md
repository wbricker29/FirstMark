# Airtable Formula Examples

Comprehensive library of Airtable formulas for filtering, calculations, and data manipulation.

## Quick Reference

| Category | Examples |
|----------|----------|
| [Comparison](#comparison-formulas) | Equals, not equals, greater than |
| [Logical](#logical-formulas) | AND, OR, NOT, IF |
| [Text](#text-formulas) | SEARCH, CONCATENATE, LOWER, UPPER |
| [Date](#date-formulas) | TODAY, DATEADD, DATETIME_DIFF |
| [Numeric](#numeric-formulas) | SUM, AVERAGE, ROUND, MIN, MAX |
| [Filtering](#common-filtering-patterns) | Status, date ranges, search |

---

## Comparison Formulas

### Equals
```
{Status} = "Active"
{Priority} = 1
{Name} = "John Doe"
```

### Not Equals
```
{Status} != "Archived"
NOT({Status} = "Deleted")
```

### Greater Than / Less Than
```
{Price} > 100
{Quantity} < 10
{Score} >= 80
{Stock} <= 5
```

### Contains (Text Search)
```
SEARCH("keyword", {Description})
SEARCH("urgent", LOWER({Title}))
```

---

## Logical Formulas

### AND - All conditions must be true
```
AND({Status} = "Active", {Priority} = "High")
AND({Price} > 50, {Stock} > 0, {Category} = "Electronics")
```

### OR - Any condition can be true
```
OR({Status} = "Urgent", {Status} = "Critical")
OR({Type} = "Bug", {Type} = "Issue", {Type} = "Error")
```

### NOT - Inverse condition
```
NOT({Status} = "Complete")
NOT({Archived})
```

### IF - Conditional logic
```
IF({Score} >= 90, "A", IF({Score} >= 80, "B", "C"))
IF({Stock} < 10, "Low Stock", "In Stock")
```

---

## Text Formulas

### CONCATENATE - Combine text
```
CONCATENATE({First Name}, " ", {Last Name})
CONCATENATE("Order #", {Order Number})
```

### SEARCH - Find text (case-insensitive)
```
SEARCH("urgent", {Description})
SEARCH("@", {Email})  # Check if email contains @
```

### LOWER / UPPER - Change case
```
LOWER({Email})
UPPER({Status})
```

### LEN - Text length
```
LEN({Description}) > 100
```

### SUBSTITUTE - Replace text
```
SUBSTITUTE({Phone}, "-", "")  # Remove dashes
```

---

## Date Formulas

### TODAY - Current date
```
{Due Date} < TODAY()  # Overdue
{Due Date} = TODAY()  # Due today
```

### THIS_WEEK / THIS_MONTH
```
{Created Date} >= THIS_WEEK()
{Order Date} >= THIS_MONTH()
```

### DATEADD - Add/subtract time
```
{Due Date} < DATEADD(TODAY(), -7, 'days')  # Overdue by 7+ days
{Expiry} < DATEADD(TODAY(), 30, 'days')    # Expires in 30 days
```

### DATETIME_DIFF - Calculate difference
```
DATETIME_DIFF({End Date}, {Start Date}, 'days')
DATETIME_DIFF(TODAY(), {Created}, 'hours')
```

### IS_SAME - Compare dates
```
IS_SAME({Date}, TODAY(), 'day')
IS_SAME({Meeting}, TODAY(), 'week')
```

---

## Numeric Formulas

### Basic Math
```
{Price} * {Quantity}
{Total} - {Discount}
{Subtotal} * 1.08  # Add 8% tax
```

### ROUND - Round numbers
```
ROUND({Price}, 2)  # 2 decimal places
ROUND({Score})     # Nearest integer
```

### MIN / MAX
```
MAX({Q1 Sales}, {Q2 Sales}, {Q3 Sales}, {Q4 Sales})
MIN({Option A}, {Option B}, {Option C})
```

---

## Common Filtering Patterns

### Status-Based Filtering

**Active records:**
```
{Status} = "Active"
```

**Multiple statuses:**
```
OR({Status} = "Active", {Status} = "Pending", {Status} = "In Progress")
```

**Exclude archived:**
```
NOT({Status} = "Archived")
```

---

### Date-Based Filtering

**Overdue tasks:**
```
AND({Due Date} < TODAY(), NOT({Status} = "Complete"))
```

**This week:**
```
AND(
  {Start Date} >= THIS_WEEK(),
  {Start Date} < DATEADD(THIS_WEEK(), 7, 'days')
)
```

**Last 30 days:**
```
{Created} >= DATEADD(TODAY(), -30, 'days')
```

**Next 7 days:**
```
AND(
  {Due Date} >= TODAY(),
  {Due Date} <= DATEADD(TODAY(), 7, 'days')
)
```

---

### Priority-Based Filtering

**High priority active items:**
```
AND({Priority} = "High", {Status} = "Active")
```

**Critical or urgent:**
```
OR({Priority} = "Critical", {Priority} = "Urgent")
```

---

### Numeric Range Filtering

**Price range:**
```
AND({Price} >= 50, {Price} <= 100)
```

**Low stock:**
```
{Stock} < {Reorder Point}
```

**High value deals:**
```
{Deal Value} >= 10000
```

---

### Text Search Filtering

**Contains keyword:**
```
SEARCH("urgent", LOWER({Description}))
```

**Multiple keywords (OR):**
```
OR(
  SEARCH("bug", LOWER({Title})),
  SEARCH("error", LOWER({Title})),
  SEARCH("issue", LOWER({Title}))
)
```

**Starts with:**
```
LEFT({Product Code}, 2) = "AB"
```

---

### Empty/Missing Field Filtering

**Has value:**
```
{Email} != ""
NOT({Phone} = "")
```

**Is empty:**
```
{Email} = ""
OR({Email} = "", {Email} = BLANK())
```

**No linked records:**
```
{Customer} = BLANK()
```

---

### Complex Multi-Condition Filters

**Active high-priority tasks due this week:**
```
AND(
  {Status} = "Active",
  {Priority} = "High",
  {Due Date} >= THIS_WEEK(),
  {Due Date} < DATEADD(THIS_WEEK(), 7, 'days')
)
```

**Customers with recent orders:**
```
AND(
  {Customer Status} = "Active",
  {Last Order Date} >= DATEADD(TODAY(), -90, 'days'),
  {Total Orders} > 0
)
```

**Products needing reorder:**
```
AND(
  {Stock} < {Reorder Point},
  {Status} = "Active",
  NOT({On Order})
)
```

---

## Formula Debugging Tips

### Test formulas step by step
```
# Instead of:
AND({A} = "X", {B} > 10, SEARCH("test", {C}))

# Test each part:
{A} = "X"         # Test first
{B} > 10          # Test second
SEARCH("test", {C}) # Test third
# Then combine
```

### Use IF to debug
```
IF(
  {Status} = "Active",
  "Status OK",
  CONCATENATE("Status is: ", {Status})
)
```

### Check for blank values
```
# May fail if blank:
{Price} > 100

# Better:
AND({Price} != BLANK(), {Price} > 100)
```

---

## Performance Tips

### ✅ Good: Simple comparisons
```
{Status} = "Active"
{Price} > 100
```

### ⚠️  Moderate: Text functions
```
SEARCH("keyword", {Description})
LOWER({Email})
```

### ❌ Slow: Complex nested formulas
```
# Avoid deeply nested logic
IF(
  IF(
    IF(condition1, result1, condition2),
    result2,
    condition3
  ),
  result3,
  result4
)
```

---

## Common Errors

### "Invalid formula"
**Cause:** Syntax error, wrong field name

**Fix:**
- Check field names are exact (case-sensitive)
- Verify field names in curly braces: `{Field Name}`
- Check for missing commas, parentheses

### "Invalid field reference"
**Cause:** Field doesn't exist or was renamed

**Fix:**
- Use correct current field name
- Update formulas after renaming fields

### Formula returns blank
**Cause:** Field is empty or formula has error

**Fix:**
- Check for BLANK() values
- Add IF checks for empty fields:
  ```
  IF({Field} != BLANK(), {Field} * 2, 0)
  ```

---

## Real-World Examples

### CRM Lead Scoring
```
# Score based on multiple factors
(
  IF({Company Size} = "Enterprise", 30, 0) +
  IF({Budget} > 50000, 25, 0) +
  IF({Timeline} = "Immediate", 20, 0) +
  IF({Decision Maker}, 25, 0)
)
```

### Project Status Badge
```
IF(
  {Progress} = 100,
  "✅ Complete",
  IF(
    {Due Date} < TODAY(),
    "🔴 Overdue",
    IF(
      {Due Date} < DATEADD(TODAY(), 3, 'days'),
      "🟡 Due Soon",
      "🟢 On Track"
    )
  )
)
```

### Inventory Alert
```
IF(
  {Stock} = 0,
  "🚨 OUT OF STOCK",
  IF(
    {Stock} < {Reorder Point},
    "⚠️  LOW STOCK",
    "✅ In Stock"
  )
)
```

### Email Validation
```
AND(
  SEARCH("@", {Email}),
  SEARCH(".", {Email}),
  LEN({Email}) > 5
)
```
