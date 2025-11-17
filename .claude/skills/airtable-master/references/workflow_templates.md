# Airtable Workflow Templates

Pre-built workflow templates for common Airtable use cases.

## Table of Contents

1. [CRM Workflows](#crm-workflows)
2. [Project Management](#project-management)
3. [Inventory Management](#inventory-management)
4. [Content Planning](#content-planning)
5. [Event Management](#event-management)
6. [Invoice Tracking](#invoice-tracking)

---

## CRM Workflows

### Lead Qualification Workflow

**Use case:** Qualify and route new leads

**Steps:**
1. **Capture leads** from form/import
2. **Validate data** (email format, required fields)
3. **Score leads** based on criteria
4. **Assign to rep** based on territory/score
5. **Create follow-up tasks**

**Implementation:**
```
1. List new leads:
   list_records(
     baseId,
     'Leads',
     filterByFormula='{Status}="New"'
   )

2. Validate each lead:
   validator = DataValidator(leads_schema)
   results = validator.validate_records(leads)

3. Score and route:
   for lead in valid_leads:
     score = calculate_lead_score(lead)
     assigned_rep = assign_rep_by_territory(lead['Territory'])
     
     update_records(
       baseId,
       'Leads',
       [{
         'id': lead['id'],
         'fields': {
           'Score': score,
           'Assigned To': assigned_rep,
           'Status': 'Qualified'
         }
       }]
     )

4. Create tasks:
   create_record(
     baseId,
     'Tasks',
     {
       'Title': f"Follow up with {lead['Company']}",
       'Linked Lead': [lead['id']],
       'Due Date': tomorrow
     }
   )
```

---

### Pipeline Management Workflow

**Use case:** Move deals through sales stages

**Triggers:**
- Deal stage changes
- Milestone reached
- Time-based (weekly review)

**Automation:**
```
1. Get deals by stage:
   deals = list_records(
     baseId,
     'Deals',
     filterByFormula='{Stage}="Negotiation"'
   )

2. Check stale deals:
   for deal in deals:
     days_in_stage = calculate_days_in_stage(deal)
     
     if days_in_stage > 14:
       create_comment(
         baseId,
         'Deals',
         deal['id'],
         f"Deal has been in Negotiation for {days_in_stage} days. Please update."
       )

3. Update probabilities:
   stage_probabilities = {
     'Prospecting': 10,
     'Qualification': 25,
     'Proposal': 50,
     'Negotiation': 75,
     'Closed Won': 100
   }
   
   updates = [
     {
       'id': deal['id'],
       'fields': {
         'Probability': stage_probabilities[deal['Stage']]
       }
     }
     for deal in deals
   ]
   
   batch_ops.update_records(updates)
```

---

## Project Management

### Sprint Planning Workflow

**Use case:** Create and populate sprint backlog

**Steps:**
1. **Query backlog** items by priority
2. **Calculate capacity** per team member
3. **Assign tasks** to sprint
4. **Set dependencies**

**Implementation:**
```
1. Get prioritized backlog:
   backlog = list_records(
     baseId,
     'Tasks',
     filterByFormula='AND({Status}="Backlog", {Priority}="High")',
     sort=[
       {'field': 'Priority Order', 'direction': 'asc'}
     ]
   )

2. Calculate team capacity:
   team_capacity = {}
   team = list_records(baseId, 'Team Members')
   
   for member in team:
     available_hours = member['fields']['Sprint Capacity']
     current_load = sum_linked_tasks(member['id'])
     team_capacity[member['id']] = available_hours - current_load

3. Assign tasks:
   sprint_tasks = []
   
   for task in backlog:
     estimated_hours = task['fields']['Estimate']
     
     # Find team member with capacity
     for member_id, capacity in team_capacity.items():
       if capacity >= estimated_hours:
         sprint_tasks.append({
           'id': task['id'],
           'fields': {
             'Sprint': ['recCurrentSprint'],
             'Assigned To': [member_id],
             'Status': 'Sprint Backlog'
           }
         })
         team_capacity[member_id] -= estimated_hours
         break
   
   batch_ops.update_records(sprint_tasks)

4. Create sprint report:
   export = ExportHelpers(sprint_tasks, schema)
   export.to_excel('sprint_plan.xlsx')
```

---

### Task Dependencies Workflow

**Use case:** Manage task dependencies and blockers

**Implementation:**
```
1. Check for blocked tasks:
   tasks = list_records(
     baseId,
     'Tasks',
     filterByFormula='{Blocked By} != BLANK()'
   )

2. Verify dependencies:
   for task in tasks:
     blocking_tasks = task['fields'].get('Blocked By', [])
     
     # Check if any blockers are complete
     blockers = [
       get_record(baseId, 'Tasks', blocker_id)
       for blocker_id in blocking_tasks
     ]
     
     all_complete = all(
       b['fields']['Status'] == 'Complete'
       for b in blockers
     )
     
     if all_complete:
       # Unblock and notify
       update_records(
         baseId,
         'Tasks',
         [{
           'id': task['id'],
           'fields': {
             'Status': 'Ready',
             'Blocked': False
           }
         }]
       )
       
       # Notify assignee
       create_comment(
         baseId,
         'Tasks',
         task['id'],
         f"All blocking tasks complete. Ready to start!"
       )
```

---

## Inventory Management

### Stock Replenishment Workflow

**Use case:** Automated reorder notifications

**Triggers:**
- Daily check
- Stock level changes
- Manual trigger

**Implementation:**
```
1. Find low stock items:
   low_stock = list_records(
     baseId,
     'Inventory',
     filterByFormula='{Current Stock} < {Reorder Point}'
   )

2. Check if already on order:
   needs_reorder = [
     item for item in low_stock
     if not item['fields'].get('On Order', False)
   ]

3. Create purchase orders:
   for item in needs_reorder:
     reorder_qty = item['fields']['Reorder Quantity']
     supplier = item['fields']['Supplier'][0]
     
     # Create PO record
     po = create_record(
       baseId,
       'Purchase Orders',
       {
         'Item': [item['id']],
         'Supplier': [supplier],
         'Quantity': reorder_qty,
         'Status': 'Draft',
         'Order Date': today
       }
     )
     
     # Mark item as on order
     update_records(
       baseId,
       'Inventory',
       [{
         'id': item['id'],
         'fields': {'On Order': True}
       }]
     )
     
     # Add comment
     create_comment(
       baseId,
       'Inventory',
       item['id'],
       f"Purchase order created: {reorder_qty} units"
     )

4. Generate report:
   export = ExportHelpers(needs_reorder, schema)
   export.to_csv('reorder_report.csv')
```

---

### Inventory Reconciliation Workflow

**Use case:** Match physical count with system

**Implementation:**
```
1. Export current inventory:
   current = list_records(baseId, 'Inventory')
   ExportHelpers(current).to_csv('system_inventory.csv')

2. Load physical count:
   with open('physical_count.csv') as f:
     physical_count = csv.DictReader(f)

3. Compare and identify variances:
   variances = []
   
   for system_item in current:
     sku = system_item['fields']['SKU']
     system_qty = system_item['fields']['Current Stock']
     
     # Find in physical count
     physical = next(
       (p for p in physical_count if p['SKU'] == sku),
       None
     )
     
     if physical:
       physical_qty = int(physical['Count'])
       variance = physical_qty - system_qty
       
       if variance != 0:
         variances.append({
           'id': system_item['id'],
           'sku': sku,
           'system': system_qty,
           'physical': physical_qty,
           'variance': variance
         })

4. Update system with physical counts:
   updates = [
     {
       'id': v['id'],
       'fields': {
         'Current Stock': v['physical'],
         'Last Reconciled': today,
         'Variance': v['variance']
       }
     }
     for v in variances
   ]
   
   batch_ops.update_records(updates)

5. Generate variance report:
   print(f"Found {len(variances)} variances")
   for v in variances:
     print(f"{v['sku']}: {v['variance']:+d}")
```

---

## Content Planning

### Editorial Calendar Workflow

**Use case:** Plan and track content production

**Implementation:**
```
1. Get content due this week:
   this_week = list_records(
     baseId,
     'Content',
     filterByFormula='''
       AND(
         {Publish Date} >= THIS_WEEK(),
         {Publish Date} < DATEADD(THIS_WEEK(), 7, 'days'),
         {Status} != "Published"
       )
     '''
   )

2. Check production status:
   statuses = {
     'Idea': [],
     'Outline': [],
     'Draft': [],
     'Review': [],
     'Ready': []
   }
   
   for content in this_week:
     status = content['fields']['Status']
     statuses[status].append(content)

3. Send reminders:
   for content in statuses['Draft']:
     days_until_publish = calculate_days_until(
       content['fields']['Publish Date']
     )
     
     if days_until_publish <= 2:
       assignee = content['fields']['Writer'][0]
       create_comment(
         baseId,
         'Content',
         content['id'],
         f"@{assignee} - Content publishes in {days_until_publish} days!"
       )

4. Generate weekly report:
   report = {
     'week': 'This Week',
     'total': len(this_week),
     'by_status': {k: len(v) for k, v in statuses.items()},
     'at_risk': [
       c['fields']['Title']
       for c in statuses['Draft'] + statuses['Idea']
     ]
   }
   
   print(json.dumps(report, indent=2))
```

---

## Event Management

### Event Registration Workflow

**Use case:** Process event registrations

**Implementation:**
```
1. Get new registrations:
   new_regs = list_records(
     baseId,
     'Registrations',
     filterByFormula='{Status}="New"'
   )

2. Validate registrations:
   validator = DataValidator(reg_schema)
   valid = validator.validate_records(new_regs)

3. Check capacity:
   event_capacity = {}
   
   for reg in new_regs:
     event_id = reg['fields']['Event'][0]
     
     if event_id not in event_capacity:
       event = get_record(baseId, 'Events', event_id)
       capacity = event['fields']['Capacity']
       current = count_linked_records(event_id, 'Registrations')
       event_capacity[event_id] = capacity - current

4. Process registrations:
   for reg in new_regs:
     event_id = reg['fields']['Event'][0]
     
     if event_capacity.get(event_id, 0) > 0:
       # Confirm registration
       update_records(
         baseId,
         'Registrations',
         [{
           'id': reg['id'],
           'fields': {
             'Status': 'Confirmed',
             'Confirmation Date': today
           }
         }]
       )
       event_capacity[event_id] -= 1
     else:
       # Waitlist
       update_records(
         baseId,
         'Registrations',
         [{
           'id': reg['id'],
           'fields': {
             'Status': 'Waitlisted'
           }
         }]
       )
```

---

## Invoice Tracking

### Invoice Processing Workflow

**Use case:** Track invoice lifecycle

**Implementation:**
```
1. Get overdue invoices:
   overdue = list_records(
     baseId,
     'Invoices',
     filterByFormula='''
       AND(
         {Due Date} < TODAY(),
         {Status} != "Paid",
         {Status} != "Cancelled"
       )
     '''
   )

2. Calculate aging:
   for invoice in overdue:
     days_overdue = calculate_days_overdue(
       invoice['fields']['Due Date']
     )
     
     # Determine aging category
     if days_overdue < 30:
       aging = '0-30 days'
     elif days_overdue < 60:
       aging = '30-60 days'
     elif days_overdue < 90:
       aging = '60-90 days'
     else:
       aging = '90+ days'
     
     # Update invoice
     update_records(
       baseId,
       'Invoices',
       [{
         'id': invoice['id'],
         'fields': {
           'Days Overdue': days_overdue,
           'Aging': aging
         }
       }]
     )

3. Send reminders:
   for invoice in overdue:
     days = invoice['fields']['Days Overdue']
     
     if days in [7, 14, 30, 60]:  # Reminder schedule
       customer = invoice['fields']['Customer'][0]
       create_comment(
         baseId,
         'Invoices',
         invoice['id'],
         f"Reminder sent to customer ({days} days overdue)"
       )

4. Generate aging report:
   aging_summary = {}
   for invoice in overdue:
     aging = invoice['fields']['Aging']
     amount = invoice['fields']['Amount']
     aging_summary[aging] = aging_summary.get(aging, 0) + amount
   
   print("Accounts Receivable Aging:")
   for category, amount in aging_summary.items():
     print(f"{category}: ${amount:,.2f}")
```

---

## Workflow Best Practices

### General Principles

1. **Validate before action**
   - Check data integrity
   - Verify relationships
   - Test with dry-run mode

2. **Handle errors gracefully**
   - Try/catch around operations
   - Log failures for review
   - Provide clear error messages

3. **Maintain audit trails**
   - Use comments for actions
   - Track status changes
   - Record who did what when

4. **Batch where possible**
   - Group related operations
   - Respect rate limits
   - Show progress for long operations

5. **Test incrementally**
   - Start with small batches
   - Verify results
   - Scale up gradually

### Workflow Checklist

- [ ] Clear trigger conditions defined
- [ ] Data validation implemented
- [ ] Error handling in place
- [ ] Audit trail maintained
- [ ] Rate limiting respected
- [ ] Progress indication provided
- [ ] Results verified
- [ ] Documentation updated
