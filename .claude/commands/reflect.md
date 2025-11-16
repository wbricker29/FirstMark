---
name: reflect
description: Capture Python Project Learnings
---

# /reflect - Capture Python Project Learnings

## Purpose
Capture project learnings, decisions, and insights into CLAUDE.md for future reference.

## Usage
```
/reflect [scope]
/reflect              # Reflect on recent work
/reflect unit csv-parser  # Reflect on specific unit
/reflect project      # Reflect on entire project
```

## Prerequisites
- CLAUDE.md should exist (created automatically if missing)

## Process

### Step 1: Determine Scope
Based on argument:
- **No arg:** Recent work (last 1-2 tasks)
- **unit:** Specific unit (completed or in progress)
- **project:** Entire project (L1 docs, all units, overall progress)

### Step 2: Gather Context

#### For Unit Reflection
Load:
- Unit design.md (objective, acceptance criteria)
- Unit plan.md (tasks, progress, blockers)
- Verification results (from last /verify)
- Code changes (what was implemented)
- Test results (coverage, passing/failing)

#### For Project Reflection
Load:
- Constitution, PRD, Spec
- All unit statuses from state.json
- Overall test coverage
- Number of units completed
- Key milestones reached

### Step 3: Analyze Learnings

#### Technical Learnings
- What Python patterns worked well?
- What libraries/tools were effective?
- What performance optimizations were needed?
- What type hints or abstractions helped?

**Example Learnings:**
```
- Using generators for CSV parsing reduced memory usage by 80%
- Pydantic validation caught edge cases before runtime
- pytest fixtures with tmp_path simplified file testing
- Type hints revealed logic errors during development
```

#### Process Learnings
- What worked in the workflow?
- What slowed development?
- What would we do differently?
- What verification gates were most valuable?

**Example Learnings:**
```
- Writing tests alongside implementation (TDD) caught bugs early
- Type checking with pyright found issues ruff missed
- 85% coverage target was appropriate (not too strict, not too lenient)
- Breaking tasks into 2-4 hour chunks improved focus
```

#### Architecture Learnings
- How well did the design hold up?
- What assumptions proved wrong?
- What would we redesign?
- What interfaces need refinement?

**Example Learnings:**
```
- Separating parsing from validation improved testability
- Original interface lacked schema parameter (added in update)
- Streaming approach critical for large file support
- Error messages with line numbers saved debugging time
```

### Step 4: Identify Patterns

#### Successful Patterns
What worked and should be repeated:
- Code structures (class hierarchies, function composition)
- Testing strategies (fixtures, parametrize, mocking)
- Python idioms (generators, context managers, decorators)
- Type hint patterns (Protocol, TypedDict, Generic)

#### Anti-Patterns
What didn't work and should be avoided:
- Overly complex abstractions
- Missing type hints in key places
- Insufficient error handling
- Tight coupling between modules

### Step 5: Document Decisions

#### Key Decisions Made
For each significant decision:
- **Decision:** What was decided
- **Rationale:** Why this choice was made
- **Alternatives:** What else was considered
- **Outcome:** How it worked out

**Example:**
```
Decision: Use csv.DictReader instead of pandas
Rationale: Lighter dependency, sufficient for simple parsing
Alternatives: pandas.read_csv (too heavy), manual parsing (too complex)
Outcome: Good choice - fast and memory efficient
```

### Step 6: Capture Python-Specific Insights

#### Type Hints
- Which type hints were most useful?
- Where did type hints catch bugs?
- What complex types needed TypedDict/Protocol?

#### Testing
- Which pytest features were most valuable?
- How effective was fixture design?
- What mocking strategies worked?
- Coverage gaps and how to address them

#### Performance
- Where were bottlenecks?
- What optimizations made impact?
- Memory usage patterns
- Profiling insights

#### Dependencies
- Which packages were essential?
- Any regretted dependencies?
- Version constraints that helped/hurt

### Step 7: Extract Recommendations

Generate actionable recommendations:

**For Future Units:**
```
1. Start with type stubs before implementation
2. Write test fixtures before tests
3. Use generators for any file processing
4. Profile early if performance matters
5. Document complex type hints with examples
```

**For Current Project:**
```
1. Consider adding schema validation to all parsers
2. Standardize error message format across units
3. Extract common test fixtures to conftest.py
4. Add performance benchmarks to test suite
```

**For Process:**
```
1. Continue UPEVD pattern - very effective
2. Run type check during development, not just at end
3. Use coverage HTML reports to find gaps
4. Keep tasks under 4 hours for better estimates
```

### Step 8: Update CLAUDE.md

Add reflection section with structure:

```markdown
## Reflections

### 2025-01-15 - Unit 001-csv-parser Complete {#reflection}

**Summary:** Implemented CSV parsing with streaming support, comprehensive validation, and 92% test coverage.

**Technical Learnings:**
- Generators critical for memory efficiency (processed 1GB file in 50MB memory)
- Type hints caught off-by-one error in row counting logic
- pytest parametrize reduced test boilerplate from 200 to 50 lines
- Pydantic validation 3x faster than manual validation

**Process Learnings:**
- UPEVD workflow kept tasks focused and complete
- Writing tests first (TDD) revealed edge cases early
- Type checking during development (not just verification) saved time
- 3-hour task estimates were accurate, 1-hour tasks often underestimated

**Architecture Learnings:**
- Separating parse_csv() from validate_record() improved testability
- Generic parse_document() interface accommodates future parsers (JSON, XML)
- Error hierarchy (ParseError, ValidationError) enables granular handling

**Key Decisions:**
1. **csv.DictReader over pandas**
   - Rationale: No heavy dependency for simple parsing
   - Outcome: ✅ Good choice - fast and lightweight

2. **Streaming with generators**
   - Rationale: Support large files without memory issues
   - Outcome: ✅ Excellent - 1GB file in 50MB memory

3. **Optional Pydantic validation**
   - Rationale: Flexibility for users who don't need validation
   - Outcome: ✅ Good - validate parameter makes it opt-in

**Patterns to Reuse:**
- Generator pattern for file processing
- Fixture-based testing with tmp_path
- Type hints with Union for flexible returns
- Comprehensive docstrings with examples

**Anti-Patterns to Avoid:**
- ❌ Loading entire file into memory (original prototype)
- ❌ Generic Exception (replaced with specific error types)
- ❌ Implicit encoding (made explicit with default utf-8)

**Recommendations:**
1. Extract CSV-specific logic to separate module
2. Add support for CSV writing (not just reading)
3. Consider async version for concurrent file processing
4. Add benchmarks to track performance regressions

**Metrics:**
- Tasks: 7/7 completed
- Coverage: 92% (target: 85%)
- Tests: 11 passing
- Type errors: 0
- Linting errors: 0
- Time: 16 hours (estimated: 18 hours)

**Next Steps:**
- Start Unit 002-validator
- Extract common test fixtures to conftest.py
- Add performance benchmarks
```

### Step 9: Identify Cross-Unit Patterns

If reflecting on project:
- Common patterns across units
- Shared utilities to extract
- Consistent approaches
- Divergent solutions (good or bad?)

### Step 10: Suggest Improvements

Based on reflections, suggest:
- **Code improvements:** Refactoring, abstractions, utilities
- **Process improvements:** Workflow adjustments, tooling
- **Documentation improvements:** Clarifications, examples
- **Test improvements:** Coverage gaps, test patterns

## Output
- **Updated:** CLAUDE.md with reflection section
- **Insights:** Technical, process, and architecture learnings
- **Recommendations:** Actionable next steps
- **Patterns:** Reusable approaches documented

## Reflection Types

### Unit Reflection
Focus on:
- Specific implementation details
- Testing approach
- Performance characteristics
- Type hint patterns
- Code organization

### Project Reflection
Focus on:
- Overall architecture
- Cross-unit patterns
- Process effectiveness
- Quality trends
- Timeline accuracy

### Technical Reflection
Focus on:
- Python idioms and patterns
- Library and tool choices
- Performance optimizations
- Type system usage
- Testing strategies

### Process Reflection
Focus on:
- UPEVD workflow effectiveness
- Task estimation accuracy
- Verification gate value
- Communication patterns
- Decision-making process

## Best Practices

### Be Specific
❌ "Tests were helpful"
✅ "pytest fixtures with tmp_path reduced test setup from 20 lines to 5 lines per test"

### Be Honest
Document what didn't work, not just successes

### Be Actionable
Each learning should suggest concrete next steps

### Be Forward-Looking
Focus on what to do differently next time

## Next Steps
- Apply learnings to next unit
- Implement recommended improvements
- Update process based on insights
- Share patterns with team
