# 100% Coverage Strategy - Zero Information Loss

**Requirement:** ALL data must be accessible, NO edge cases excluded.

**Challenge:** Raw data (20k tokens) vs. Context limits (200k total)

**Solution:** Tiered data storage with intelligent lazy-loading

---

## Architecture: Three-Tier Data Model

```
Tier 1: Summary (ALWAYS in context)
  ↓
Tier 2: Detailed (Load on demand)
  ↓
Tier 3: Raw/Granular (Query-based access)
```

---

## Tier 1: Summary Layer (Always Loaded)

**Purpose:** High-level metrics for 90% of questions
**Size:** ~500 lines JSON, ~2k tokens
**When loaded:** Immediately on agent activation

```json
{
  "summary": {
    "annual_totals": {
      "2020": {
        "revenue": 12462910.90,
        "ebitda": 576239.35,
        "ebitda_margin_pct": 4.6
      },
      // 2021, 2022, 2023
    },

    "key_findings": {
      "revenue_cagr_2020_2022": 34.6,
      "margin_expansion": "4.6% → 14.5%",
      "one_time_items_flagged": 3,
      "normalization_candidates": 2
    },

    "data_available": {
      "detailed_pl": "tier2/detailed_pl.json",
      "detailed_bs": "tier2/detailed_bs.json",
      "monthly_data": "tier2/monthly_breakdowns.json",
      "account_level": "tier3/raw_accounts.json"
    }
  }
}
```

**This stays in context always.** User can ask: "What's the revenue?" → Instant answer.

---

## Tier 2: Detailed Layer (Load on Specific Request)

**Purpose:** Detailed breakdowns when user drills down
**Size:** ~5,000 lines JSON, ~20k tokens
**When loaded:** Only when user asks specific questions

### Tier 2A: Revenue Detail
**File:** `tier2/revenue_detail.json`
**Loaded when:** User asks about revenue composition, quality, line items

```json
{
  "revenue_by_line_item": [
    {
      "account": "440000 - Revenue Services- standard VAT",
      "account_number": "440000",
      "2020": 11500000,
      "2021": 14200000,
      "2022": 18900000,
      "2023_h1": 9800000,
      "pct_of_total_2022": 83.7,
      "monthly_2022": {
        "jan": 1580000,
        "feb": 1620000,
        // ... all 12 months
      },
      "flags": []
    },
    // ALL revenue accounts, not just top 20
    // 100% coverage
  ],

  "revenue_analytics": {
    "concentration": {
      "top_1_account_pct": 83.7,
      "top_3_accounts_pct": 96.5
    },
    "one_time_items": [
      {
        "account": "490000 - Income from disposal of fixed assets",
        "year": 2022,
        "amount": 25667.59,
        "monthly_detail": {...}
      }
    ]
  }
}
```

### Tier 2B: Expense Detail
**File:** `tier2/expense_detail.json`
**Loaded when:** User asks about costs, normalization, specific expense categories

```json
{
  "expense_by_category": [
    {
      "category": "Personnel",
      "total_2022": -12136571.61,
      "accounts": [
        {
          "account": "602000 - Salaries",
          "2020": -6800000,
          "2021": -8200000,
          "2022": -10500000,
          "monthly_2022": {...}
        },
        // ALL personnel accounts
      ]
    },
    {
      "category": "Operating Expenses",
      "accounts": [
        // ALL operating expense accounts
      ]
    }
    // COMPLETE expense structure
  ],

  "normalization_candidates": [
    {
      "account": "602300 - Profit-sharing salary management",
      "reason": "Owner compensation - verify market rate",
      "2022": -800000,
      "historical": {...},
      "context": "Increased from €450k in 2020"
    }
    // ALL potential adjustments identified
  ]
}
```

### Tier 2C: Working Capital Detail
**File:** `tier2/working_capital_detail.json`

### Tier 2D: Balance Sheet Detail
**File:** `tier2/balance_sheet_detail.json`

---

## Tier 3: Raw Granular Layer (Query-Based)

**Purpose:** Complete raw data for ANY edge case query
**Size:** ~15,000 lines JSON, ~60k tokens
**When loaded:** NEVER loaded entirely. Query-based access only.

**File:** `tier3/raw_accounts_database.json`

```json
{
  "pl_accounts": [
    {
      "row_id": 7,
      "account": "473600",
      "description": "Cash discounts granted, Standard VAT",
      "monthly_data": {
        "2020": {
          "jan": 0,
          "feb": 0,
          // ... all months, all years
        }
      },
      "adjustments": {
        "2020_adjust": 0
      },
      "totals": {
        "2020": -3750,
        "2021": 0,
        "2022": 0,
        "2023_h1": -7371.97
      }
    }
    // EVERY SINGLE ACCOUNT from raw Excel
    // Row 7 through Row 242
    // 100% complete
  ],

  "metadata": {
    "source": "Group_ProfitAndLoss_2020-Jun_2023_per_Months.xlsx",
    "total_accounts": 235,
    "total_data_points": 11374
  }
}
```

**Access pattern:**

```python
def query_account(account_number, period=None):
    """
    Load ONLY the specific account requested.
    Never load entire Tier 3 into context.
    """
    # Load Tier 3 file (happens outside context)
    raw_db = load_json_file('tier3/raw_accounts_database.json')

    # Find specific account
    account_data = [a for a in raw_db['pl_accounts']
                    if a['account'] == account_number][0]

    if period:
        return account_data['monthly_data'][period]
    else:
        return account_data['totals']

# Example usage
user_asks: "What was the exact amount in account 473600 in March 2021?"
→ query_account('473600', period='2021.mar')
→ Returns: 0
→ Context cost: ~50 tokens (just the answer, not entire database)
```

---

## Intelligent Loading Strategy

### Agent Workflow

```python
class FinancialAnalystAgent:
    def __init__(self):
        # ALWAYS load Tier 1 (2k tokens)
        self.summary = load_tier1()

        # Tier 2 - load on demand
        self.tier2_loaded = {}

        # Tier 3 - never fully loaded
        self.tier3_path = 'tier3/raw_accounts_database.json'

    def answer_question(self, question):
        # 1. Try to answer from Tier 1
        if can_answer_from_summary(question):
            return answer_from_tier1(question)

        # 2. Identify what Tier 2 data needed
        needed_tier2 = identify_needed_data(question)

        if needed_tier2 and needed_tier2 not in self.tier2_loaded:
            # Load specific Tier 2 file
            self.tier2_loaded[needed_tier2] = load_tier2(needed_tier2)
            # Context cost: +20k tokens (but only once)

        if can_answer_from_tier2(question):
            return answer_from_tier2(question)

        # 3. Very specific query → Query Tier 3
        result = query_tier3(question)
        # Context cost: ~50-200 tokens for specific answer
        return result
```

### Example Conversation Flow

**Question 1:** "What was the 2022 revenue?"
→ **Tier 1** loaded (2k tokens)
→ Answer: €22.6M
→ **Total context: 2k tokens**

**Question 2:** "What are the main revenue sources?"
→ Load **Tier 2A: Revenue Detail** (+20k tokens)
→ Answer: Services 83.7%, Goods 8.0%, Other 8.3%
→ **Total context: 22k tokens**

**Question 3:** "Show me the exact monthly breakdown for account 440010 in 2021"
→ Query **Tier 3** for specific account
→ Return only that account's 2021 monthly data (~100 tokens)
→ **Total context: 22.1k tokens**

**Question 4:** "What about another specific account 602300?"
→ Query **Tier 3** again for different account
→ Return only that account's data (~100 tokens)
→ **Total context: 22.2k tokens**

---

## Context Usage Comparison

### Old Approach (Load Everything)
```
Load raw Excel → 20k tokens
Every question uses same 20k
10 questions = 20k context (static)
```

### New Approach (Tiered)
```
Load Tier 1 → 2k tokens
Question needs detail → +20k tokens (Tier 2)
Specific query → +100 tokens (Tier 3 query)
Total: 22.1k tokens

BUT: Most conversations stay at Tier 1 (2k tokens)
```

### Real-World Scenario
```
Analysis workflow:
1. Load Tier 1 (2k)
2. Ask 5 general questions (Tier 1) → Still 2k
3. Deep dive revenue (load Tier 2A) → Now 22k
4. Ask 3 revenue questions (Tier 2A) → Still 22k
5. Query specific account (Tier 3 query) → 22.1k
6. Build valuation (uses Tier 1 + some Tier 2) → ~25k

Total for full analysis: ~25k tokens
vs. Old approach: ~95k tokens

Savings: 74%
Coverage: 100%
```

---

## Implementation: Complete Extraction Process

### Step 1: Extract All Data to Tiered Files

```python
def extract_financial_data_complete():
    """
    Extract 100% of data from raw Excel into tiered structure.
    No information loss whatsoever.
    """

    raw_excel = pd.read_excel('Group_ProfitAndLoss_2020-Jun_2023.xlsx')

    # === TIER 1: Summary ===
    tier1 = {
        'annual_totals': extract_annual_totals(raw_excel),
        'key_findings': calculate_key_findings(raw_excel),
        'data_available': {
            'detailed_pl': 'tier2/revenue_detail.json',
            'detailed_expenses': 'tier2/expense_detail.json',
            # ... references to all Tier 2 files
        }
    }
    save_json('tier1/summary.json', tier1)

    # === TIER 2: Detailed Breakdowns ===
    tier2_revenue = {
        'revenue_by_line_item': extract_all_revenue_accounts(raw_excel),
        'revenue_analytics': analyze_revenue_quality(raw_excel),
        'monthly_breakdowns': extract_monthly_revenue(raw_excel)
    }
    save_json('tier2/revenue_detail.json', tier2_revenue)

    tier2_expenses = {
        'expense_by_category': extract_all_expense_accounts(raw_excel),
        'normalization_candidates': identify_adjustments(raw_excel)
    }
    save_json('tier2/expense_detail.json', tier2_expenses)

    # ... other Tier 2 files

    # === TIER 3: Complete Raw Data ===
    tier3 = {
        'pl_accounts': []
    }

    # Extract EVERY SINGLE ROW from Excel
    for row_idx in range(len(raw_excel)):
        account_data = {
            'row_id': row_idx,
            'account': raw_excel.iloc[row_idx, 0],
            'description': get_description(raw_excel.iloc[row_idx, 0]),
            'monthly_data': extract_all_monthly_values(raw_excel, row_idx),
            'totals': calculate_totals(raw_excel, row_idx)
        }
        tier3['pl_accounts'].append(account_data)

    save_json('tier3/raw_accounts_database.json', tier3)

    # Validation: Ensure 100% coverage
    validate_completeness(tier1, tier2_revenue, tier2_expenses, tier3)
```

### Step 2: Validation (100% Coverage Check)

```python
def validate_completeness(tier1, tier2, tier3):
    """
    Prove mathematically that no data was lost.
    """

    # Check 1: Tier 1 totals = Tier 2 sum
    tier1_revenue_2022 = tier1['annual_totals']['2022']['revenue']
    tier2_revenue_2022 = sum(item['2022'] for item in tier2['revenue_by_line_item'])

    assert abs(tier1_revenue_2022 - tier2_revenue_2022) < 1, \
        "Tier 1/2 revenue mismatch"

    # Check 2: Tier 2 sum = Tier 3 sum
    tier3_revenue_2022 = sum(
        acc['totals']['2022']
        for acc in tier3['pl_accounts']
        if is_revenue_account(acc['account'])
    )

    assert abs(tier2_revenue_2022 - tier3_revenue_2022) < 1, \
        "Tier 2/3 revenue mismatch"

    # Check 3: Tier 3 accounts = Raw Excel rows
    raw_excel = pd.read_excel('source.xlsx')
    assert len(tier3['pl_accounts']) == len(raw_excel), \
        "Tier 3 missing rows from raw Excel"

    # Check 4: Every cell accounted for
    for row_idx in range(len(raw_excel)):
        for col_idx in range(1, len(raw_excel.columns)):  # Skip description column
            raw_value = raw_excel.iloc[row_idx, col_idx]
            tier3_value = tier3['pl_accounts'][row_idx]['monthly_data'][get_period(col_idx)]

            assert raw_value == tier3_value, \
                f"Cell mismatch at row {row_idx}, col {col_idx}"

    print("✓ 100% coverage validated")
    print(f"  - {len(tier3['pl_accounts'])} accounts")
    print(f"  - {count_data_points(tier3)} data points")
    print(f"  - Zero information loss")
```

---

## Agent Instructions Update

```markdown
# Financial Analyst - Data Access Pattern

## On Activation
1. ALWAYS load Tier 1 summary (2k tokens)
2. Present user with high-level overview
3. Wait for questions

## Question Answering Strategy

### Level 1: General Questions
"What was 2022 revenue?" → Answer from Tier 1

### Level 2: Detailed Analysis
"What are the revenue sources?" → Load Tier 2 Revenue Detail
"Show me expense categories?" → Load Tier 2 Expense Detail

### Level 3: Specific Queries
"What was account 440010 in March 2021?" → Query Tier 3

## Context Management
- Tier 1: Always in context (2k)
- Tier 2: Load on-demand, keep in context once loaded (~20k per file)
- Tier 3: Never fully load, query-based only (~100 tokens per query)

## When to Load Tier 2
- User asks for "breakdown", "detail", "composition"
- Normalization analysis needed
- QoE deep dive requested
- User challenges a summary number

## When to Query Tier 3
- User asks for specific account by number
- User requests specific month/year combination
- Validation of unusual item needed
- Audit trail requested

## 100% Coverage Guarantee
- If data exists in raw Excel → It exists in Tier 3
- If user asks for it → Query returns it
- No edge cases excluded
- Complete audit trail always available
```

---

## Benefits

| Metric | Old Approach | New Tiered | Improvement |
|--------|-------------|------------|-------------|
| **Coverage** | 100% | 100% | Same ✓ |
| **Context (simple question)** | 20k | 2k | **90% reduction** |
| **Context (detailed analysis)** | 20k | 22k | -10% (acceptable) |
| **Context (specific query)** | 20k | 2.1k | **90% reduction** |
| **Average conversation** | 95k | 25k | **74% reduction** |
| **Edge case handling** | ✓ | ✓ | Same ✓ |

---

## File Structure

```
sandbox/
├── tier1/
│   └── summary.json              (~500 lines, 2k tokens)
│
├── tier2/
│   ├── revenue_detail.json       (~1,500 lines, 6k tokens)
│   ├── expense_detail.json       (~1,500 lines, 6k tokens)
│   ├── working_capital_detail.json (~500 lines, 2k tokens)
│   ├── balance_sheet_detail.json  (~500 lines, 2k tokens)
│   └── monthly_breakdowns.json    (~1,000 lines, 4k tokens)
│
└── tier3/
    └── raw_accounts_database.json (~15,000 lines, 60k tokens)
                                   [Never fully loaded]
```

---

## Next Steps

1. Implement tiered extraction for Project Munich
2. Validate 100% coverage mathematically
3. Test query-based Tier 3 access
4. Run same valuation analysis with new approach
5. Measure context savings
6. Deploy if validation passes

---

## Key Principles

1. **100% Coverage:** Every cell from Excel → Tier 3
2. **Lazy Loading:** Load only what's needed, when needed
3. **No Information Loss:** Mathematical validation proves completeness
4. **Context Efficiency:** Most questions answered with <5k tokens
5. **Transparent to User:** They don't see the tiers, just get answers
