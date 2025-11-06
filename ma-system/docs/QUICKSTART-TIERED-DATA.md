# Quick Start - Tiered Data Architecture

5-minute guide to using the 100% coverage strategy in your agent workflows.

---

## The Problem

Loading raw Excel files into context is expensive:
- 20k tokens per file
- Context fills up quickly (81% after one analysis)
- Can't handle long conversations

## The Solution

3-tier data architecture:
- **Tier 1**: Summary (2k tokens, always loaded) → answers 90% of questions
- **Tier 2**: Details (20k per file, on-demand) → deep dives
- **Tier 3**: Complete raw data (query-only, never fully loaded) → 100% coverage

**Result:** 70-90% token reduction, 100% data coverage

---

## For Agent Developers

### 1. Import the utilities

```python
from core import TieredDataAccess, validate_extraction
```

### 2. Initialize on agent activation

```python
# In your agent's activation sequence
sandbox_path = "/path/to/sandbox"
accessor = TieredDataAccess(sandbox_path)

# Always load Tier 1 (2k tokens)
tier1 = accessor.load_tier1()
print(f"Revenue 2022: {tier1['annual_summary']['2022']['revenue']}")
```

### 3. Answer questions intelligently

```python
# Level 1: General questions (from Tier 1)
if user_asks_about == "annual totals":
    answer = tier1['annual_summary'][year][metric]
    # Cost: 0 additional tokens

# Level 2: Detailed questions (load Tier 2)
elif user_asks_about == "revenue breakdown":
    revenue_detail = accessor.load_tier2_file('revenue_detail.json')
    answer = revenue_detail['revenue_by_line_item']
    # Cost: +20k tokens (one-time)

# Level 3: Specific queries (query Tier 3)
elif user_asks_about == "specific account":
    value = accessor.query_tier3_account(account_number, period)
    # Cost: +50 tokens (just the answer)
```

### 4. Validate extraction

```python
# After extracting data to tiers
from core import validate_extraction

success = validate_extraction(
    sandbox_path='/path/to/sandbox',
    raw_data_path='/path/to/raw.xlsx'
)

if not success:
    raise Exception("Coverage validation failed")
```

---

## For Workflow Developers

### Use the standard extraction workflow

```yaml
# In your workflow.yaml
workflow_steps:
  1_extract_financial_data:
    workflow: "workflows/financial/data-extraction/workflow.yaml"
    inputs:
      data_room_path: "{data_room_path}"
      sandbox_path: "{sandbox_path}"
      deal_name: "{deal_name}"
```

This automatically:
1. Extracts to Tier 3 (100% coverage)
2. Aggregates to Tier 2
3. Summarizes to Tier 1
4. Validates mathematically
5. Updates knowledge base

---

## Common Patterns

### Pattern 1: Check if extraction already done

```python
from pathlib import Path

tier1_path = Path(sandbox_path) / "tier1" / "summary.json"

if tier1_path.exists():
    # Already extracted, just load
    tier1 = accessor.load_tier1()
else:
    # Not extracted yet, run workflow
    run_extraction_workflow()
```

### Pattern 2: Determine which Tier 2 file to load

```python
# Auto-detect based on question
tier2_file = accessor.get_tier2_trigger(user_question)

if tier2_file:
    detail = accessor.load_tier2_file(tier2_file)
    # Now answer from detail
```

### Pattern 3: Search by keyword

```python
# User doesn't know account number
matches = accessor.search_tier3_accounts('consulting')

for match in matches:
    print(f"{match['account']}: {match['description']}")
    print(f"  2022 total: {match['totals']['2022']}")
```

### Pattern 4: Query specific account/period

```python
# User asks: "What was account 440000 in March 2021?"
value = accessor.query_tier3_account(
    account_number='440000',
    period='2021.march'
)
print(f"Value: {value}")
```

---

## File Structure After Extraction

```
sandbox/
├── tier1/
│   └── summary.json              # Always load this (2k tokens)
│
├── tier2/                         # Load on-demand
│   ├── revenue_detail.json       # When user asks about revenue
│   ├── expense_detail.json       # When user asks about expenses
│   ├── working_capital_detail.json
│   └── balance_sheet_detail.json
│
└── tier3/
    └── raw_accounts_database.json # Never load entirely, query only
```

---

## Quick Reference: Which Tier?

| User Question | Tier | Cost | Example |
|---------------|------|------|---------|
| What was 2022 revenue? | Tier 1 | 0 tokens | `tier1['annual_summary']['2022']['revenue']` |
| What's the EBITDA margin? | Tier 1 | 0 tokens | `tier1['annual_summary']['2022']['ebitda_margin_pct']` |
| What are the revenue sources? | Tier 2 | +20k tokens | `load_tier2_file('revenue_detail.json')` |
| What expenses should we normalize? | Tier 2 | +20k tokens | `load_tier2_file('expense_detail.json')` |
| What was account 440010 in Jan 2021? | Tier 3 | +50 tokens | `query_tier3_account('440010', '2021.jan')` |

---

## Context Budget Planning

### Typical Session

```
Agent activation:
  Load Tier 1                        → 2k tokens

User asks 5 general questions:
  Answer from Tier 1                 → 2k tokens (no increase)

User deep dive on revenue:
  Load Tier 2 revenue                → +20k = 22k tokens

User asks 3 revenue detail questions:
  Answer from loaded Tier 2          → 22k tokens (no increase)

User asks about specific account:
  Query Tier 3                       → +50 = 22.05k tokens

Total session:                       → ~22k tokens
```

**vs. Old Approach:** Loading raw Excel multiple times = ~95k tokens

**Savings:** 77%

---

## Validation

Always validate after extraction:

```python
from core import validate_extraction

# Validates:
# ✓ Tier 1 revenue == sum(Tier 2 revenue items)
# ✓ Tier 2 revenue == sum(Tier 3 revenue accounts)
# ✓ EBITDA == EBIT + D&A
# ✓ All periods present
# ✓ Account count matches
# ✓ Tier 3 row count == Raw Excel row count

success = validate_extraction(sandbox_path)
# Prints detailed results

# For silent validation:
from core import validate_quick
if validate_quick(sandbox_path):
    print("✓ Ready to use")
```

---

## Error Handling

```python
from core import TieredDataAccess

accessor = TieredDataAccess(sandbox_path)

# Handle missing extraction
try:
    tier1 = accessor.load_tier1()
except FileNotFoundError:
    print("Data not extracted yet. Run extraction workflow first.")

# Handle account not found
try:
    value = accessor.query_tier3_account('999999')
except ValueError as e:
    print(f"Account not found: {e}")

# Handle missing Tier 2 file
try:
    detail = accessor.load_tier2_file('nonexistent.json')
except FileNotFoundError as e:
    print(f"File not found: {e}")
```

---

## Testing

```bash
# Test data access
python3 -c "
from core import query_account
value = query_account('./sandbox', '440000', period='2022')
print(f'Value: {value}')
"

# Test validation
python3 -c "
from core import validate_quick
if validate_quick('./sandbox'):
    print('✓ Validation passed')
else:
    print('✗ Validation failed')
"

# Test search
python3 -c "
from core import search_accounts
matches = search_accounts('./sandbox', 'salary')
for m in matches:
    print(f\"{m['account']}: {m['description']}\")
"
```

---

## Integration Example

```python
# In your agent code

from core import TieredDataAccess

class MyFinancialAgent:
    def __init__(self, sandbox_path):
        self.accessor = TieredDataAccess(sandbox_path)
        self.tier1 = self.accessor.load_tier1()
        self.tier2_loaded = {}

    def answer_question(self, question):
        # Try Tier 1 first
        if 'revenue' in question and 'total' in question:
            return self.tier1['annual_summary']['2022']['revenue']

        # Load Tier 2 if needed
        tier2_file = self.accessor.get_tier2_trigger(question)
        if tier2_file and tier2_file not in self.tier2_loaded:
            self.tier2_loaded[tier2_file] = self.accessor.load_tier2_file(tier2_file)

        if 'revenue sources' in question:
            return self.tier2_loaded['revenue_detail.json']['revenue_by_line_item']

        # Query Tier 3 for specific data
        if 'account' in question:
            account = extract_account_number(question)
            return self.accessor.query_tier3_account(account)

        return "I need more information to answer that."
```

---

## Key Principles

1. **Always load Tier 1** on agent activation (2k tokens)
2. **Load Tier 2 on-demand** when user asks for details
3. **Query Tier 3** for specific accounts, never load entirely
4. **Validate after extraction** to ensure 100% coverage
5. **Track loaded files** to avoid re-loading

---

## Need More Details?

- **Core utilities:** `/core/README.md`
- **Complete architecture:** `/docs/100-percent-coverage-strategy.md`
- **Implementation summary:** `/docs/implementation-summary.md`
- **Data schema:** `/docs/financial-data-extraction-schema.md`
- **Standard workflow:** `/workflows/financial/data-extraction/workflow.yaml`

---

## Support

Questions? Check:
1. `/core/README.md` - Comprehensive examples
2. `/docs/` - Full documentation
3. `/agents/financial-analyst.md` - Reference implementation

**Status:** Production ready ✓
