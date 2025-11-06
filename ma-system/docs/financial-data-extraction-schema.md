# Financial Data Extraction Schema

**Purpose:** Define what data to extract from raw financial documents to enable comprehensive analysis while minimizing context usage.

**Design Principle:** Extract everything needed for 95% of analyses, with fallback to raw data for edge cases.

---

## Extraction Schema (Level 2 - Standard)

### 1. Annual Summary Metrics

```json
{
  "annual_summary": {
    "2020": {
      "revenue": 12462910.90,
      "gross_profit": 10759502.18,
      "personnel_expenses": -8106098.68,
      "depreciation_amortization": -70591.90,
      "ebit": 505647.45,
      "ebitda": 576239.35,
      "ebitda_margin_pct": 4.6,

      // CRITICAL: Derived metrics for validation
      "calculated_ebitda": 576239.35,  // ebit + D&A
      "gross_margin_pct": 86.3,
      "personnel_as_pct_revenue": 65.0
    },
    "2021": { /* same structure */ },
    "2022": { /* same structure */ },
    "2023_h1": { /* same structure */ }
  }
}
```

**Why:** Core metrics for valuation, trend analysis, margin analysis
**Context cost:** ~200 lines JSON

---

### 2. Monthly Revenue & EBITDA (Seasonality Detection)

```json
{
  "monthly_metrics": {
    "2020": {
      "jan": {"revenue": 954000, "ebitda": 45000},
      "feb": {"revenue": 932000, "ebitda": 38000},
      // ... 12 months
    },
    "2021": { /* 12 months */ },
    "2022": { /* 12 months */ },
    "2023": { /* 6 months */ }
  }
}
```

**Why:**
- Detect seasonality patterns (critical for working capital)
- Identify unusual months (spikes/dips)
- Validate annual totals

**Context cost:** ~150 lines JSON

---

### 3. Revenue Breakdown (Quality of Earnings)

```json
{
  "revenue_detail": {
    "by_line_item": [
      {
        "account": "440000 - Revenue Services- standard VAT",
        "2020": 11500000,
        "2021": 14200000,
        "2022": 18900000,
        "2023_h1": 9800000,
        "pct_of_total_2022": 83.7,
        "description": "Core recurring services"
      },
      {
        "account": "440010 - Revenue Goods - standard VAT",
        "2020": 800000,
        "2021": 1200000,
        "2022": 1800000,
        "2023_h1": 900000,
        "pct_of_total_2022": 8.0,
        "description": "Product sales"
      },
      // Top 20 revenue line items (covers 95%+ of revenue)
    ],

    "revenue_quality_flags": {
      "one_time_items": [
        {
          "account": "490000 - Income from disposal of fixed assets",
          "year": 2022,
          "amount": 25667.59,
          "description": "Asset sale - non-recurring"
        }
      ],
      "unusual_items": [
        {
          "account": "400000 - Sales (free text)",
          "note": "Negative revenue in some months - investigate",
          "months_affected": ["2020-01", "2020-02"]
        }
      ]
    }
  }
}
```

**Why:**
- Revenue concentration analysis
- Identify one-time revenue items
- Quality assessment (recurring vs. non-recurring)
- Customer concentration risk (if derivable from accounts)

**Context cost:** ~400 lines JSON

---

### 4. Operating Expense Categories (Normalization)

```json
{
  "expense_detail": {
    "personnel": {
      "total_2020": -8106098.68,
      "total_2021": -9884716.66,
      "total_2022": -12136571.61,

      "breakdown": [
        {
          "category": "602000 - Salaries",
          "2020": -6800000,
          "2021": -8200000,
          "2022": -10500000,
          "pct_of_personnel": 86.5
        },
        {
          "category": "602300 - Profit-sharing salary management",
          "2020": -450000,
          "2021": -620000,
          "2022": -800000,
          "normalization_flag": "⚠ Potential adjustment for owner compensation"
        },
        // Top 15 personnel expense categories
      ]
    },

    "operating_expenses": {
      "total_2020": -2324163.15,

      "breakdown": [
        {
          "category": "640000 - Rent and leases",
          "2020": -450000,
          "2021": -480000,
          "2022": -510000,
          "normalization_flag": null
        },
        {
          "category": "671000 - Legal and consulting fees",
          "2020": -120000,
          "2021": -85000,
          "2022": -380000,
          "normalization_flag": "⚠ 2022 spike - potential one-time item"
        },
        // Top 20 operating expense categories
      ]
    },

    "potential_normalizations": [
      {
        "account": "602300 - Profit-sharing salary management",
        "year": 2022,
        "amount": -800000,
        "flag": "Owner compensation - verify if above market"
      },
      {
        "account": "671000 - Legal and consulting fees",
        "year": 2022,
        "amount": -380000,
        "flag": "Spike vs. prior years - one-time cost?"
      }
    ]
  }
}
```

**Why:**
- Identify normalization adjustments
- Spot one-time expenses
- Owner compensation analysis
- Cost structure understanding

**Context cost:** ~500 lines JSON

---

### 5. Working Capital Components

```json
{
  "working_capital": {
    "2020_year_end": {
      "trade_receivables": 1850000,
      "other_receivables": 420000,
      "trade_payables": -95000,
      "deferred_income": -180000,
      "net_working_capital": 1995000,
      "nwc_as_pct_revenue": 16.0,
      "dso_days": 54
    },
    "2021_year_end": { /* same */ },
    "2022_year_end": { /* same */ },

    "monthly_nwc": {
      "2022": {
        "jan": 1800000,
        "feb": 1850000,
        // ... 12 months
      }
    }
  }
}
```

**Why:**
- Working capital trend analysis
- Seasonality in NWC (critical for cash flow)
- DSO/DPO calculations
- Peg NWC for transaction

**Context cost:** ~250 lines JSON

---

### 6. Balance Sheet Summary

```json
{
  "balance_sheet": {
    "2022_year_end": {
      "assets": {
        "fixed_assets": 125000,
        "current_assets": 7989536.87,
        "total_assets": 8114536.87
      },
      "liabilities": {
        "current_liabilities": 350000,
        "long_term_debt": 0,
        "total_liabilities": 350000
      },
      "equity": 7764536.87,
      "cash": 4954269.92,
      "net_debt": -4954269.92  // Negative = net cash
    },
    "2021_year_end": { /* same */ },
    "2020_year_end": { /* same */ }
  }
}
```

**Why:**
- Capital structure
- Net debt calculation
- Equity value bridge

**Context cost:** ~150 lines JSON

---

### 7. Metadata & Validation

```json
{
  "metadata": {
    "extraction_date": "2024-11-05T14:30:00Z",
    "source_files": [
      {
        "file": "Group_ProfitAndLoss_2020-Jun_2023_per_Months.xlsx",
        "sheet": "PGPLConsolidated",
        "rows": 242,
        "columns": 47,
        "hash": "abc123..."
      },
      {
        "file": "Consolidated_Balance_Sheet_2022_by_Subsidiaries.xlsx",
        "sheet": "PGBalanceSheetConsolidate",
        "rows": 180,
        "columns": 8
      }
    ],

    "validation_checks": {
      "revenue_totals_match": true,
      "ebitda_calculation_valid": true,
      "no_missing_periods": true,
      "balance_sheet_balances": true
    },

    "coverage": {
      "revenue_line_items_extracted": 18,
      "revenue_coverage_pct": 97.8,
      "expense_categories_extracted": 25,
      "expense_coverage_pct": 94.2
    }
  }
}
```

**Why:**
- Audit trail
- Validation that nothing critical was missed
- Re-extraction trigger if needed

**Context cost:** ~100 lines JSON

---

## Total Extraction Size

**Estimated JSON size:** ~2,000 lines
**Context cost:** ~8,000 tokens (vs. 20,000 for raw Excel)
**Savings:** 60% reduction
**Information loss:** <3% (edge cases only)

---

## Validation Rules

After extraction, run automatic validation:

```python
def validate_extraction(extract):
    """
    Ensure no critical data was lost in extraction.
    """
    checks = []

    # 1. Revenue totals match
    annual_total = sum(extract['annual_summary'][y]['revenue'] for y in years)
    monthly_total = sum(all monthly revenue values)
    assert abs(annual_total - monthly_total) < 1000, "Revenue mismatch"
    checks.append("✓ Revenue totals consistent")

    # 2. EBITDA calculation correct
    for year in years:
        ebit = extract['annual_summary'][year]['ebit']
        da = extract['annual_summary'][year]['depreciation_amortization']
        ebitda_calc = ebit + abs(da)
        ebitda_reported = extract['annual_summary'][year]['ebitda']
        assert abs(ebitda_calc - ebitda_reported) < 100, f"EBITDA calc error {year}"
    checks.append("✓ EBITDA calculations valid")

    # 3. Coverage check
    revenue_coverage = extract['metadata']['coverage']['revenue_coverage_pct']
    assert revenue_coverage > 95.0, "Insufficient revenue coverage"
    checks.append(f"✓ Revenue coverage: {revenue_coverage}%")

    # 4. No missing periods
    expected_years = ['2020', '2021', '2022', '2023_h1']
    for year in expected_years:
        assert year in extract['annual_summary'], f"Missing year {year}"
    checks.append("✓ All periods present")

    return checks
```

---

## Fallback Mechanism

If analysis requires data not in extract:

```python
def get_detailed_data(account, period):
    """
    Fallback: Re-read specific data from raw Excel if needed.
    Only used for edge cases not covered by standard extract.
    """
    # Check if in extract first
    if account in extract['revenue_detail']['by_line_item']:
        return extract['revenue_detail']['by_line_item'][account]

    # Otherwise, read from raw Excel
    warning("Reading raw data - consider updating extraction schema")
    raw_data = pd.read_excel(raw_file)
    value = raw_data.loc[account, period]

    return value
```

---

## Update Triggers

Re-extract financial data if:
1. New financial data uploaded (e.g., full year 2023)
2. User challenges a specific number → Validate against raw
3. Extraction schema updated (new fields added)
4. Validation check fails

---

## Example: Full Extracted File

```json
{
  "deal_name": "Project Munich",
  "target_company": "TechTarget GmbH",
  "extraction_version": "1.0",
  "extracted_at": "2024-11-05T14:30:00Z",

  "annual_summary": { /* ... */ },
  "monthly_metrics": { /* ... */ },
  "revenue_detail": { /* ... */ },
  "expense_detail": { /* ... */ },
  "working_capital": { /* ... */ },
  "balance_sheet": { /* ... */ },
  "metadata": { /* ... */ }
}
```

**File size:** ~2,000 lines JSON (~80 KB)
**Load time:** <100ms
**Context cost:** ~8,000 tokens
**Information completeness:** 97%+

---

## Benefits vs. Raw Excel Approach

| Aspect | Raw Excel | Extracted JSON | Improvement |
|--------|-----------|----------------|-------------|
| Context cost | ~20k tokens | ~8k tokens | **60% reduction** |
| Load time | 2-3 seconds | <100ms | **20x faster** |
| Readability | Poor (11k cells) | Excellent (structured) | ✓ |
| QoE analysis | ✓ Possible | ✓ Possible | Same |
| Normalization | ✓ Possible | ✓ Possible | Same |
| Seasonality | ✓ Possible | ✓ Possible | Same |
| Validation | Manual | Automated | Better |
| Re-use | Read Excel each time | Load JSON once | ✓ |

---

## Implementation Checklist

- [ ] Define extraction schema (this document)
- [ ] Implement extraction function
- [ ] Add validation checks
- [ ] Test with Project Munich data
- [ ] Verify all analyses still work
- [ ] Add fallback mechanism
- [ ] Document edge cases
- [ ] Update financial-analyst.md workflow

---

## Open Questions

1. **How to handle multi-entity consolidation?**
   - Current: Extract consolidated view only
   - Alternative: Also extract by legal entity (for detailed DD)

2. **Historical depth: 3 years or 5 years?**
   - Current: Whatever is available
   - Recommendation: Always extract all available years

3. **Quarterly data needed?**
   - Current: Annual + monthly for seasonality
   - Could add: Quarterly summaries for trending

4. **Currency handling?**
   - Current: Assume EUR
   - TODO: Add currency metadata if multi-currency

---

## Next Steps

1. Implement extraction function for Project Munich
2. Run validation checks
3. Compare valuation results (raw vs. extract)
4. If identical → Deploy extract-once pattern
5. Monitor for edge cases requiring raw data access
