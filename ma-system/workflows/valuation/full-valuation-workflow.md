# Full Valuation Workflow

## Overview
Comprehensive business valuation using DCF, comparable companies, and precedent transactions to triangulate enterprise value range.

## Activation Triggers
- "complete valuation"
- "full valuation"
- "detailed DCF"
- "comprehensive valuation"
- "business valuation"

## Prerequisites

### Required Data
- **Historical financials** (minimum 3 years) - P&L statements required
- **Company information** - Industry, products, geography
- **Revenue and EBITDA** - At minimum for current year

### Optional Data (Improves Accuracy)
- Management projections (5 year forecast)
- Balance sheet and cash flow statements
- Customer concentration data
- Industry reports or market data
- Cap table / ownership structure

## Agents Involved
- **Primary**: Financial Analyst
- **Supporting**: Market Intelligence (for comparables research)

## Context Awareness
- **Check existing**: Load `knowledge-base/deal-insights.md` for prior valuations
- **Incremental update**: If valuation v1.X exists, load and ask what changed
- **Version control**: Save as new version with change notes

## Execution Mode
- **Mode**: Flexible (can adapt to available data)
- **Parallel execution**: Can run alongside market research, not documents
- **Update knowledge base**: Yes, always

## Workflow Steps

### Step 1: Document Analysis & Data Collection
**Financial Analyst Actions:**
1. Read all provided financial documents
2. Extract historical financial data (3-5 years):
   - Revenue
   - EBITDA
   - EBIT
   - Net Income
   - Cash flows (if available)
3. Identify any data quality issues or gaps
4. Flag missing information to user

**Data Authority Check:**
- All numbers must be sourced from provided documents
- If data missing, ASK USER before proceeding
- Mark data quality: [Confirmed], [Estimated], [Assumed]

**Output:** Data collection summary with gaps identified

---

### Step 2: EBITDA Normalization (QoE Lite)
**Financial Analyst Actions:**
1. Review EBITDA for one-time items:
   - Extraordinary expenses
   - Owner compensation adjustments
   - Non-recurring costs
   - Related party transactions
2. Calculate normalized EBITDA
3. Document all adjustments with rationale
4. Get user confirmation on major adjustments (>5% of EBITDA)

**Data Authority Check:**
- Only adjust items with documented basis
- If uncertain whether to adjust, ASK USER
- Record all assumptions in `knowledge-base/valuation-history.md`

**Output:** Normalized EBITDA with adjustment schedule

---

### Step 3: Build DCF Model
**Financial Analyst Actions:**
1. Project free cash flows (5 years):
   - Revenue growth assumptions
   - EBITDA margin assumptions
   - Working capital changes
   - Capex requirements
   - Tax rate
2. Determine terminal value:
   - Terminal growth rate (typically 2-3%)
   - Exit multiple method (alternative)
3. Calculate WACC (Weighted Average Cost of Capital):
   - Risk-free rate
   - Equity risk premium
   - Beta (use comparable companies)
   - Cost of debt
   - Target capital structure
4. Discount cash flows to present value
5. Calculate enterprise value and equity value

**Data Authority Check:**
- Assumptions must be sourced or user-approved:
  - Growth rates: From management projections OR industry research [cite] OR user assumption
  - WACC inputs: From market data [cite sources] OR industry benchmarks [cite]
  - Terminal growth: Standard range (2-3%) OR user-specified
- If using industry benchmarks, cite source and date
- Run sensitivity analysis on key assumptions

**Output:** DCF valuation model with sensitivity tables

---

### Step 4: Comparable Company Analysis
**Financial Analyst + Market Intelligence Actions:**
1. **Market Intelligence**: Research 5-10 comparable public companies
   - Similar industry / business model
   - Similar size (ideally 0.5x - 2x revenue)
   - Similar geography
   - Document sources with URLs
2. **Financial Analyst**: Extract trading multiples:
   - EV / Revenue
   - EV / EBITDA
   - P / E (if applicable)
   - Calculate median and mean multiples
3. Apply multiples to target company
4. Adjust for size premium / illiquidity discount

**Data Authority Check:**
- All comparable companies must be real, publicly traded [Verified]
- Multiples must be sourced from: Yahoo Finance, Google Finance, Capital IQ, etc.
- Cite data source and date accessed
- If using size premium, cite study (e.g., Duff & Phelps, Ibbotson)

**Output:** Comparable company analysis with multiples table

---

### Step 5: Precedent Transaction Analysis
**Market Intelligence + Financial Analyst Actions:**
1. **Market Intelligence**: Research recent M&A transactions (3-5 deals):
   - Same industry
   - Similar size
   - Last 2-3 years
   - Document deal details and sources
2. **Financial Analyst**: Extract transaction multiples:
   - EV / Revenue
   - EV / EBITDA
   - Note: Transaction multiples include control premium
3. Calculate median multiples
4. Apply to target company

**Data Authority Check:**
- Transaction details must be sourced: Press releases, M&A databases, news articles
- If deal multiple not disclosed, mark as [Not Available]
- Don't invent transaction multiples
- Cite all sources with dates

**Output:** Precedent transaction analysis table

---

### Step 6: Triangulation & Valuation Range
**Financial Analyst Actions:**
1. Compare all three valuation methods:
   - DCF valuation
   - Trading comps valuation
   - Transaction comps valuation
2. Assign weights based on data quality:
   - Strong data: Higher weight
   - Limited data: Lower weight
   - Typical weighting: 40% DCF, 30% Trading Comps, 30% Transaction Comps
3. Calculate weighted average valuation
4. Define valuation range (low / base / high)
5. Sensitivity analysis on key assumptions

**Output:** Valuation summary with range and key sensitivities

---

### Step 7: Documentation & Knowledge Base Update
**Financial Analyst Actions:**
1. Create comprehensive Excel valuation model
2. Include all methodology tabs:
   - Assumptions summary
   - Historical financials
   - EBITDA normalization
   - DCF model with sensitivities
   - Comparable companies
   - Precedent transactions
   - Valuation summary
3. Update `knowledge-base/deal-insights.md`:
   - Valuation range
   - Key assumptions
   - Date completed
   - Version number
4. Update `knowledge-base/valuation-history.md`:
   - Document all assumptions
   - Note data sources
   - Record sensitivities
5. Save output file: `{deal-name}_Valuation_Model_v{X}.xlsx`

---

## Outputs

### Primary Output
**File**: `outputs/{deal-name}/financial/valuation/{deal-name}_Valuation_Model_v{X}.xlsx`

**Sheets**:
1. Executive Summary - Valuation range and key metrics
2. Assumptions - All assumptions documented with sources
3. Historical Financials - 3-5 years of data
4. EBITDA Normalization - Adjustments schedule
5. DCF Model - Cash flow projections and NPV calculation
6. WACC Calculation - Cost of capital breakdown
7. Comparable Companies - Trading multiples analysis
8. Precedent Transactions - Transaction multiples analysis
9. Valuation Summary - Triangulation and weighted valuation
10. Sensitivity Analysis - Key assumption sensitivities

### Knowledge Base Updates
1. `knowledge-base/deal-insights.md`:
   ```markdown
   ## Valuation
   **Status:** Completed
   **Date:** {date}
   **Version:** v{X}
   **Enterprise Value Range:** €{low}M - €{high}M (Base: €{base}M)
   **Methodology:** DCF (40%), Trading Comps (30%), Transaction Comps (30%)
   **Key Assumptions:**
   - Normalized EBITDA: €{X}M
   - Revenue growth: {X}%
   - WACC: {X}%
   - Terminal growth: {X}%
   **Output File:** `outputs/{deal-name}/financial/valuation/{filename}`
   **Next Steps:** Use valuation for CIM, teaser, negotiations
   ```

2. `knowledge-base/valuation-history.md`:
   - Full assumption documentation
   - Sensitivity analysis results
   - Data quality notes
   - Methodology choices and rationale

---

## Data Quality Levels

| Level | Description | Action |
|-------|-------------|--------|
| **High** | 3+ years audited financials, management projections, industry data | Full DCF + Comps + Transactions |
| **Medium** | 3 years unaudited financials, limited projections | DCF + Comps, note limitations |
| **Low** | 1-2 years financials, no projections | Comps-focused, simplified DCF, wide range |
| **Minimal** | Revenue + EBITDA margin only | Comps only, very wide range, flag uncertainty |

---

## Estimated Time
- **High data quality**: 2-3 hours
- **Medium data quality**: 3-4 hours (more research needed)
- **Low data quality**: 4-6 hours (extensive assumptions, sensitivity analysis)

---

## Success Criteria
✅ Valuation model created with all three methodologies
✅ All assumptions documented with sources
✅ Sensitivity analysis shows impact of key assumptions
✅ Knowledge base updated with valuation range
✅ User understands valuation basis and confidence level

---

## When to Use This Workflow
- Initial business valuation for deal preparation
- Updating valuation with new financial data
- Preparing for buyer negotiations
- Setting asking price expectations
- Due diligence preparation

## When NOT to Use This Workflow
- Quick ballpark estimate (use `quick-valuation-workflow.md`)
- QoE-focused analysis only (use `qoe-analysis-workflow.md`)
- Updating existing model with minor changes (manual update)
