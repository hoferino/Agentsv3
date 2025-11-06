# Core Utilities - Tiered Data Architecture

System-wide utilities for the 100% Coverage Strategy implementing zero information loss with context efficiency.

## Overview

These utilities enable:
- **100% data coverage** - Every cell from raw Excel preserved in Tier 3
- **Context efficiency** - 70-90% reduction in token usage
- **Mathematical validation** - Proof of zero information loss
- **Query-based access** - Access any data point without loading full datasets

## Architecture

```
Tier 1 (Summary)     → Always loaded    → 2k tokens
Tier 2 (Detailed)    → On-demand        → 20k tokens per file
Tier 3 (Raw/Complete)→ Query-only       → 50-200 tokens per query
```

## Modules

### `data_access.py` - Tiered Data Access

Query tiered financial data without loading entire datasets into context.

**Key Classes:**
- `TieredDataAccess` - Main access layer for all three tiers

**Key Functions:**
- `query_account()` - Quick function to query specific accounts from Tier 3
- `search_accounts()` - Search accounts by keyword

#### Usage Examples

```python
from core.data_access import TieredDataAccess, query_account

# Initialize accessor
accessor = TieredDataAccess(sandbox_path='/path/to/sandbox')

# Load Tier 1 (always called on agent activation)
summary = accessor.load_tier1()
print(summary['annual_summary']['2022']['revenue'])
# Output: 22600000

# Load Tier 2 file on-demand (when user asks for details)
revenue_detail = accessor.load_tier2_file('revenue_detail.json')
print(revenue_detail['revenue_by_line_item'][0])
# Output: {'account': '440000', '2022': 18900000, 'pct_of_total_2022': 83.7}

# Query Tier 3 for specific account (never load entire file)
account_440000_totals = accessor.query_tier3_account('440000')
print(account_440000_totals)
# Output: {'2020': 11500000, '2021': 14200000, '2022': 18900000}

# Query specific month
march_2021 = accessor.query_tier3_account('473600', period='2021.march')
print(march_2021)
# Output: 0

# Search by keyword
salary_accounts = accessor.search_tier3_accounts('salary')
print(salary_accounts)
# Output: [
#   {'account': '602000', 'description': 'Salaries', 'totals': {...}},
#   {'account': '602300', 'description': 'Profit-sharing salary', 'totals': {...}}
# ]

# Quick convenience functions
from core.data_access import query_account, search_accounts

value = query_account('/path/to/sandbox', '440000', period='2022')
# Output: 18900000

matches = search_accounts('/path/to/sandbox', 'consulting')
# Output: [{'account': '671000', 'description': 'Legal and consulting fees', ...}]
```

#### Intelligent Question Answering

```python
# Determine which tier is needed for a question
tier2_file = accessor.get_tier2_trigger("What are the main revenue sources?")
print(tier2_file)
# Output: 'revenue_detail.json'

# Get metadata about answering strategy
strategy = accessor.answer_question(
    "What was 2022 revenue?",
    tier1_data=summary
)
print(strategy)
# Output: {
#   'source_tier': 'tier1',
#   'file_needed': 'summary.json',
#   'context_cost_tokens': 0  # Already loaded
# }
```

### `validation.py` - 100% Coverage Validation

Mathematical validation framework ensuring zero information loss across tiers.

**Key Classes:**
- `CoverageValidator` - Validates data consistency across all tiers
- `ValidationResult` - Dataclass for validation check results

**Key Functions:**
- `validate_extraction()` - Convenience function for complete validation
- `validate_quick()` - Quick validation without verbose output

#### Usage Examples

```python
from core.validation import CoverageValidator, validate_extraction

# Full validation with output
validate_extraction(
    sandbox_path='/path/to/sandbox',
    raw_data_path='/path/to/raw/excel.xlsx'
)
# Output:
# ============================================================
# VALIDATION RESULTS - 100% Coverage Check
# ============================================================
#
# ✓ Account Count Match
# ✓ All Periods Present
# ✓ Tier 1/2 Revenue Match (2020)
# ✓ Tier 2/3 Revenue Match (2020)
# ✓ EBITDA Calculation (2020)
# ✓ Tier 1/2 Revenue Match (2021)
# ✓ Tier 2/3 Revenue Match (2021)
# ✓ EBITDA Calculation (2021)
# ✓ Tier 1/2 Revenue Match (2022)
# ✓ Tier 2/3 Revenue Match (2022)
# ✓ EBITDA Calculation (2022)
# ✓ Tier 3 vs Raw Excel Coverage
#
# ------------------------------------------------------------
# Summary: 12/12 checks passed
#
# ✓ 100% COVERAGE VALIDATED
#   - All tiers mathematically consistent
#   - Zero information loss confirmed
#   - Ready for production use
# ============================================================

# Quick validation (returns boolean)
from core.validation import validate_quick

if validate_quick('/path/to/sandbox'):
    print("Ready to use")
else:
    print("Validation failed - re-run extraction")
```

#### Detailed Validation

```python
# Use validator class for more control
validator = CoverageValidator(
    sandbox_path='/path/to/sandbox',
    raw_data_path='/path/to/raw.xlsx'
)

# Run all checks
results = validator.validate_all(years=['2020', '2021', '2022'])

# Check specific validations
revenue_check = validator.validate_tier1_tier2_revenue('2022')
print(revenue_check)
# Output: ✓ Tier 1/2 Revenue Match (2022)

ebitda_check = validator.validate_tier1_tier2_ebitda('2022')
print(ebitda_check)
# Output: ✓ EBITDA Calculation (2022)

# Print only failures
validator.print_failures(results)

# Check if all passed
if validator.all_passed(results):
    print("All validations passed")
```

## Integration with Agents

### Financial Analyst Agent

The financial-analyst agent uses these utilities in its activation sequence:

```xml
<step n="3">Initialize tiered data architecture:
    - Check if {sandbox_path}/tier1/summary.json exists
    - If exists: Load Tier 1 summary (2k tokens max)
    - If not exists: Flag for data extraction on first workflow
    - Store tier2_loaded = {} (empty dict for on-demand loading)
    - Set tier3_path = {sandbox_path}/tier3/raw_accounts_database.json</step>
```

### Question Answering Strategy

```python
from core.data_access import TieredDataAccess

accessor = TieredDataAccess(sandbox_path)
tier1 = accessor.load_tier1()

# Level 1: General question
if "What was 2022 revenue?" in user_question:
    answer = tier1['annual_summary']['2022']['revenue']
    # Context: 2k tokens (Tier 1 only)

# Level 2: Detailed question
if "What are the revenue sources?" in user_question:
    revenue_detail = accessor.load_tier2_file('revenue_detail.json')
    answer = revenue_detail['revenue_by_line_item']
    # Context: 22k tokens (Tier 1 + Tier 2 revenue)

# Level 3: Specific query
if "What was account 440010 in March 2021?" in user_question:
    value = accessor.query_tier3_account('440010', period='2021.march')
    # Context: 2.1k tokens (Tier 1 + query result only)
```

## Workflow Integration

These utilities are used by the standard data extraction workflow:

`/workflows/financial/data-extraction/workflow.yaml`

**Key workflow steps:**
1. Extract raw data to Tier 3 (100% coverage)
2. Aggregate to Tier 2 (detailed breakdowns)
3. Summarize to Tier 1 (high-level metrics)
4. **Validate using `core.validation.validate_extraction()`**

```python
# In workflow step 5_validate_100_percent_coverage
from core.validation import validate_extraction

success = validate_extraction(
    sandbox_path=sandbox_path,
    raw_data_path=data_room_path
)

if not success:
    raise Exception("Coverage validation failed - data loss detected")
```

## Context Savings

| Scenario | Old Approach | New Tiered | Savings |
|----------|--------------|------------|---------|
| Simple question | 20k tokens | 2k tokens | **90%** |
| Detailed analysis | 20k tokens | 22k tokens | -10% |
| Specific query | 20k tokens | 2.1k tokens | **90%** |
| **Full analysis session** | **95k tokens** | **25k tokens** | **74%** |

## File Structure

After running data extraction workflow:

```
sandbox/
├── tier1/
│   └── summary.json              (~500 lines, 2k tokens)
│
├── tier2/
│   ├── revenue_detail.json       (~1,500 lines, 6k tokens)
│   ├── expense_detail.json       (~1,500 lines, 6k tokens)
│   ├── working_capital_detail.json (~500 lines, 2k tokens)
│   └── balance_sheet_detail.json  (~500 lines, 2k tokens)
│
└── tier3/
    └── raw_accounts_database.json (~15,000 lines, 60k tokens)
                                   [Never fully loaded]
```

## Error Handling

```python
from core.data_access import TieredDataAccess

accessor = TieredDataAccess(sandbox_path='/path/to/sandbox')

try:
    # Try to query account
    value = accessor.query_tier3_account('999999')
except ValueError as e:
    # Handle account not found
    print(f"Account not found: {e}")

try:
    # Try to load Tier 2 file
    detail = accessor.load_tier2_file('nonexistent.json')
except FileNotFoundError as e:
    # Handle missing file
    print(f"File not found: {e}")
```

## Dependencies

```bash
pip install pandas openpyxl
```

## Testing

```bash
# Test data access
python3 -c "from core.data_access import query_account; print(query_account('/path/to/sandbox', '440000'))"

# Test validation
python3 -c "from core.validation import validate_quick; print(validate_quick('/path/to/sandbox'))"
```

## Documentation

See comprehensive documentation:
- `/docs/100-percent-coverage-strategy.md` - Complete architecture
- `/docs/context-management-strategy.md` - Design decisions
- `/docs/financial-data-extraction-schema.md` - Data schema details
- `/workflows/financial/data-extraction/workflow.yaml` - Extraction workflow

## Key Principles

1. **100% Coverage** - Every cell from Excel → Tier 3
2. **Lazy Loading** - Load only what's needed, when needed
3. **Mathematical Validation** - Proof of zero information loss
4. **Context Efficiency** - 70-90% token reduction
5. **Transparent to User** - They don't see tiers, just get answers
