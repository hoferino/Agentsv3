# Financial Analyst Dialog System - User Guide

**Version:** 2.0 (Dialog-Based)
**Last Updated:** 2024-11-05

---

## What Changed?

The Financial Analyst agent now operates in **interactive, menu-driven mode** instead of single-prompt execution.

### Old Approach (Single-Shot)
```
User: "Analyze these financials and value the company"
Agent: [Analyzes everything, builds valuation, done]
```

**Problems:**
- No user input during analysis
- Can't refine assumptions interatively
- No mechanism to challenge or test thinking
- "Black box" approach

### New Approach (Dialog-Based)
```
User: "/financial-analyst"
Agent: [Shows menu with 8 options]
User: Selects "Build Valuation"
Agent: "What methodologies? DCF, Multiples, or Both?"
User: "Both"
Agent: "Do you have management projections?"
User: "No"
Agent: "I'll build bottoms-up projections. Here are draft assumptions..."
Agent: "Revenue CAGR: 15%. Does this feel right?"
[Iterative back-and-forth until valuation complete]
```

**Benefits:**
- ✅ User involvement at every step
- ✅ Transparent assumptions
- ✅ Ability to refine iteratively
- ✅ Challenge mode to stress-test
- ✅ Educational (learn as you go)

---

## How to Start

### Activate the Financial Analyst

**Option 1 - Slash Command:**
```
/financial-analyst
```

**Option 2 - Natural Language:**
```
"I need financial analysis"
"Help me value this company"
"Let's work on the financials"
```

### What Happens Next

The agent **immediately presents a menu** based on the current state of your deal:

```
# Financial Analyst - Main Menu
**Deal: Your Deal Name**

What would you like to do?

1. **Analyze Financial Documents** ○
   Deep analysis of uploaded statements, tax returns, and reports
   Status: Ready

2. **Build or Update Valuation** ○
   Create or refresh DCF and multiples-based valuation
   Status: Not started

3. **Refine Valuation Model** ○
   Guided review of assumptions, scenarios, and model structure
   Status: Available after valuation

4. **Run Quality of Earnings** ○
   EBITDA normalization, adjustments, and earnings sustainability
   Status: Ready (after document analysis)

5. **Play Devil's Advocate** ○ [RECOMMENDED]
   Challenge assumptions, test downside scenarios, identify risks
   Status: Available after valuation

6. **Sensitivity & Scenario Analysis** ○
   Build sensitivities, compare scenarios, create visuals
   Status: Available after valuation

7. **Review & Export Package** ○
   Assemble deliverables and update knowledge base entries
   Status: Available after core analyses

8. **Ask Financial Questions** ○
   Free-form questions about financials, metrics, or analysis
   Status: Always available

9. **Change Interaction Mode** ○
   Switch between one-shot, dialog, or hybrid modes
   Status: Current mode displayed

Please select an option (1-9) or describe what you'd like to do.
```

**Key Feature:** Menu options adapt based on:
- What work has already been completed
- What files exist in the knowledge base
- Current valuation version
- Available documents

### Shared System Files
- `ma-system/_cfg/agent-manifest.csv` — single source of truth for agent definitions and linked prompts.
- `ma-system/_cfg/workflow-manifest.csv` — catalog of financial workflows executed by the analyst.
- `ma-system/agents/financial-analyst-menu.yaml` — menu configuration consumed by both Claude and the Python dialog system.
- `ma-system/core/tasks/workflow.xml` — workflow runner instructions executed whenever a menu option references a workflow.
- `.claude/commands/financial-analyst.md` — Claude prompt kept in sync with the above artifacts.

---

## The 8 Menu Options Explained

### 1. Analyze All Financial Documents

**When to use:** You've uploaded financial statements, tax returns, or reports and want deep analysis.

**What happens:**

**Step 1 - Scope Dialog:**
```
Agent: "How many financial documents have you uploaded?"
Options:
  1-10 documents → Standard analysis
  20-100 documents → Large-scale batched processing
  100+ documents → Enterprise parallel extraction
```

**Step 2 - Focus Areas:**
```
Agent: "What should I focus on? (Select multiple)"
☐ Historical financials (P&L, Balance Sheet, Cash Flow)
☐ Management projections
☐ Tax returns
☐ Key contracts
☐ Everything
```

**Step 3 - Detail Level:**
```
Agent: "How detailed should the extraction be?"
  Quick overview (30 min) - Key metrics only
  Standard analysis (2-4 hours) - Full extraction
  Deep dive (4-8 hours) - Line-by-line with anomalies
```

**Then:** Agent executes based on your selections, providing progress updates.

**Output:**
- Extracted data JSONs for each document
- Consolidated financial dataset
- Inconsistency report
- Historical analysis
- Updates knowledge base

---

### 2. Build/Update Valuation Model

**When to use:** You're ready to create or update a business valuation.

#### If No Existing Valuation:

**Dialog Flow:**
1. **Check prerequisites:**
   ```
   Agent: "Have you analyzed the financial documents yet?"
   If no → "I recommend doing that first. Should I start document analysis?"
   ```

2. **Choose methodologies:**
   ```
   Agent: "What valuation methodologies would you like?"
   ○ DCF only
   ○ Multiples only (trading comps + precedent transactions)
   ○ Both DCF and multiples (recommended)
   ```

3. **Projections source:**
   ```
   Agent: "Do you have management projections?"
   If Yes → "I'll use those as a starting point"
   If No → "I'll build bottoms-up projections based on historicals"
   ```

4. **Draft assumptions presented:**
   ```
   Agent: "Here are my draft assumptions:

   Revenue CAGR (2024-2028): 15%
     Rationale: Historical 3-year CAGR of 18%, conservative adjustment

   EBITDA Margin: 18% → 22% by 2028
     Rationale: Economies of scale, operating leverage

   WACC: 12.5%
     Risk-free: 3.5%, Equity risk premium: 6%, Beta: 1.2

   Terminal growth: 2.5%

   Does this feel right? Any concerns?"
   ```

5. **Iterative refinement:**
   ```
   User: "15% revenue growth seems high"
   Agent: "What would you be more comfortable with?"
   User: "12%"
   Agent: "Okay, adjusting to 12%. New valuation: €45M → €38M"
   Agent: "Should I also adjust the terminal value accordingly?"
   ```

6. **Save and document:**
   ```
   Agent: "Valuation complete: €38M (range: €34M - €42M)
   Saved as: YourDeal_Valuation_Model_v1.0.xlsx
   Updated knowledge base.

   Next steps:
   - Run sensitivity analysis (Option 6)
   - Challenge assumptions (Option 5 - Devil's Advocate)
   - Create CIM with this valuation"
   ```

#### If Existing Valuation Exists:

**Dialog Flow:**
```
Agent: "I see valuation v1.2 from 2024-10-15. What changed?"
Options:
  ○ New financials (specify period)
  ○ Market conditions update
  ○ Buyer feedback
  ○ Other (describe)

User: "New Q3 results"

Agent: "Got it. Loading v1.2...
Old revenue assumption: €5M (2024)
Q3 actuals show: €4.2M YTD (on pace for €5.6M)

Should I:
1. Update 2024 to €5.6M and increase projections?
2. Keep projections but note outperformance?
3. Wait for full year results?"
```

**Output:**
- Updated valuation model (incremented version)
- Side-by-side comparison table (old vs. new)
- Change memo explaining what drove the update
- Updated knowledge base

---

### 3. Refine Excel Model (Dialog Mode)

**When to use:** You have a valuation model and want to improve it through conversation.

**This is the most interactive mode.**

**Sub-Menu Options:**

#### 3a. Review Key Assumptions

**Dialog pattern:**
```
Agent: "Let's walk through your key assumptions.

WACC is currently 12.5%.
- Risk-free rate: 3.5%
- Beta: 1.2
- Equity risk premium: 6%

Does 12.5% feel right given the company's risk profile?"

User: "That seems high for a stable business"

Agent: "What beta would you use? Industry median is 0.9"

User: "Let's use 0.9"

Agent: "New WACC: 10.4%. This increases valuation by 15%.
But counter-point: Is the company truly as stable as industry median?
What company-specific risks might justify a higher beta?"

User: "Customer concentration - top 3 = 60% revenue"

Agent: "Fair point. What if we use beta 1.0 as a middle ground?
That gives WACC = 11.0%, valuation increase of ~8%."
```

#### 3b. Test 'What-If' Scenarios

**Interactive scenario testing:**
```
User: "What if revenue growth is only 10% instead of 15%?"

Agent: "Calculating...
- Base case (15% growth): €45M
- Scenario (10% growth): €38M
- Delta: -16%

Should I add this as a sensitivity case in the model?"

User: "Yes, and also test 8x EBITDA exit multiple instead of 10x"

Agent: "Running...
- Base (10x): €45M
- Scenario (8x): €39M
- Delta: -13%

These two scenarios combined (10% growth + 8x multiple):
€32M (-29% from base)

Want to test any other combinations?"
```

#### 3c. Add New Analysis

**Expanding the model:**
```
Agent: "What analysis is missing from the current model?"

User: "Customer concentration risk"

Agent: "Great idea. I'll add:
1. Customer revenue breakdown tab
2. Concentration risk metrics (HHI, top 5 %, etc.)
3. Scenario: 'What if top customer leaves?'
4. Recommendation for customer diversification

Sound good?"
```

#### 3d. Improve Model Structure

**Professional formatting:**
```
Agent: "Current model structure review:
✗ Inputs not color-coded
✗ No error checks on formulas
✗ Missing executive summary tab
✓ Good separation of inputs/calcs/outputs

Should I:
1. Add color coding (Blue=input, Black=calc, Green=output)?
2. Add formula error checks (IFERROR, data validation)?
3. Create executive summary tab?
4. All of the above?"
```

#### 3e. Data Quality Review

**Spot anomalies together:**
```
Agent: "I found some unusual data points. Let's review:

1. Revenue jumped 40% in 2022 (€3M → €4.2M)
   Is this correct? If so, what drove it?

2. EBITDA margin was negative in 2020 (-5%)
   One-time event? COVID impact?

3. Working capital spiked in Q4 2023
   Seasonal? Inventory build? Data error?

Let's go through each one."
```

#### 3f. Explain Model Sections

**Educational walkthrough:**
```
User: "Can you explain the terminal value calculation?"

Agent: "Absolutely. Terminal value represents the company's value
beyond our explicit forecast period (years 6+).

We use two methods:

**Perpetuity Growth Method:**
Terminal Value = FCF(Year 5) × (1 + g) / (WACC - g)
Where:
  FCF(Year 5) = €2.5M
  g = 2.5% (terminal growth)
  WACC = 12.5%

Result: €2.5M × 1.025 / (0.125 - 0.025) = €25.6M

**Exit Multiple Method:**
Terminal Value = EBITDA(Year 5) × Exit Multiple
€3.2M × 8x = €25.6M

Both give ~€25.6M, which is reassuring.

Want me to explain any other sections?"
```

---

### 4. Quality of Earnings (QoE) Analysis

**When to use:** You need to normalize EBITDA and assess earnings quality.

**Dialog Flow:**

**Step 1 - Known Adjustments:**
```
Agent: "Before I dig into the financials, are you aware of any
one-time expenses or unusual items?"

User: "Company had restructuring in 2023"

Agent: "Got it. Any others?
- Owner compensation above/below market?
- Related-party transactions?
- Non-recurring revenue?"
```

**Step 2 - Findings Presentation:**
```
Agent: "I found several potential adjustments:

1. Restructuring costs (2023): €200K
   Should we add this back? (Yes/No/Discuss)

2. CEO salary: €150K (market rate: €250K for this role/size)
   Adjust by €100K? (Yes/No/Discuss)

3. Related-party rent: €80K/year (market rate: €120K)
   Adjust by €40K? (Yes/No/Discuss)

4. One-time customer windfall (2022): €150K
   Remove this? (Yes/No/Discuss)

Let's go through each one."
```

**Step 3 - Build EBITDA Bridge:**
```
Agent: "Here's the normalized EBITDA bridge:

Reported EBITDA (2024):          €1,200K
  + Restructuring (one-time)      €  200K
  + Owner comp adjustment         €  100K
  + Below-market rent             €   40K
  - Customer windfall (non-rec)   (€ 150K)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Normalized EBITDA:               €1,390K
                                  (+16%)

Does this look reasonable? Any adjustments you'd remove?"
```

**Step 4 - Quality Assessment:**
```
Agent: "Let's assess earnings quality:

**Revenue Quality:**
- Customer concentration: Top 3 = 60% (Medium risk)
- Recurring revenue: 45% (Medium quality)
- Contract length: Avg 18 months (Good)

**Earnings Sustainability:**
- EBITDA margin trend: 15% → 18% → 20% (Improving ✓)
- Is this structural or temporary?

User: "New software platform improved margins"

Agent: "Structural improvement - good. But can margins expand
further or have we reached steady state?"
```

**Output:**
- QoE analysis spreadsheet
- Normalized EBITDA bridge
- Adjustments memo with rationale
- Quality assessment report
- Updated knowledge base

---

### 5. Play Devil's Advocate (Challenge Mode)

**When to use:** Before finalizing valuation, or before buyer meetings.

**Why it matters:** Identify weaknesses before buyers do. Stress-test your assumptions.

**Dialog Flow:**

**Step 1 - Choose Challenge Intensity:**
```
Agent: "How hard should I challenge you?"

Options:
1. Light challenge - Question a few key assumptions
2. Full challenge - Adversarial review of everything
3. Buyer perspective - Challenge as [PE firm / Strategic / Family office]
```

**Step 2 - Challenge Dialog (Example):**

#### Revenue Challenge:
```
Agent (Devil's Advocate):
"You're projecting 15% revenue CAGR over 5 years.
But industry average is only 8%.
What if buyers only believe you can do 10% growth?"

User: "We've been growing 18% historically"

Agent: "Past performance ≠ future results.
Counter-arguments buyers might make:
1. Market is maturing (harder to grow)
2. Larger competitors entering space
3. Customer acquisition costs rising

How would you respond to a buyer saying this in a meeting?"

User: "We have 3 new products launching next year"

Agent: "Okay, but:
- Are these products proven? Market validation?
- What's the success rate of new product launches historically?
- What if only 1 of 3 succeeds?

Let me model this: If growth is 10% instead of 15%:
- Base valuation: €45M
- 10% growth case: €38M (-16%)

Should we include this as a 'Conservative Case' scenario?"
```

#### EBITDA Margin Challenge:
```
Agent (Devil's Advocate):
"EBITDA margins expand from 18% to 22% in your model.
That's ambitious. What if margins stay flat at 18%?"

User: "Operating leverage - as we scale, fixed costs spread"

Agent: "I hear you, but consider:
- What if you need to hire more sales reps as you grow?
- What if customer acquisition costs increase?
- What if AWS prices go up?

PE firms are skeptical of margin expansion.
Let me stress test: Flat 18% margins → Valuation: €41M (-9%)

Also, what's your evidence that margins CAN expand to 22%?
Any comparable companies that achieved this?"
```

#### WACC Challenge:
```
Agent (Devil's Advocate):
"WACC of 12.5% feels low for a small company with:
- Customer concentration
- No long-term contracts
- Founder dependency

What if the true WACC is 15%?"

User: "Industry average WACC is 11%"

Agent: "For PUBLIC companies. You're private and smaller.
Small company premium could be 3-5%.
True WACC might be 14-16%.

At WACC = 15%: Valuation drops to €38M (-16%)

Should we at least show this as a 'Risk Case'?"
```

**Step 3 - Document Challenges:**
```
Agent: "We've identified 6 key challenges:
1. Revenue growth assumption (risk: -16%)
2. Margin expansion (risk: -9%)
3. WACC too low (risk: -16%)
4. Customer concentration
5. Terminal value optimistic
6. Working capital needs understated

I'll create a 'Risks & Sensitivities' tab in the model
documenting all challenges and downside scenarios.

I'm also adjusting the valuation RANGE:
- Old range: €40M - €50M
- New range: €35M - €50M (wider to reflect risks)

Sound reasonable?"
```

**Step 4 - Confidence Check:**
```
Agent: "After all these challenges, what's your confidence level?"

Options:
○ High - Assumptions are solid, risks manageable
○ Medium - Some concerns but generally comfortable
○ Low - Need to revise model significantly

User: "Medium"

Agent: "Understood. Recommendations:
1. Prepare strong rebuttals to buyer challenges
2. Have data ready to support growth assumptions
3. Build multiple scenarios for buyer meetings
4. Consider reducing asking price slightly to account for risks

Want me to help prepare buyer Q&A responses?"
```

**Output:**
- Risk assessment report
- Downside scenario models
- Buyer objection rebuttals
- Updated valuation range
- Sensitivity analysis

---

### 6. Sensitivity & Scenario Analysis

**When to use:** You want to understand how valuation changes with different assumptions.

**Dialog Flow:**

**Step 1 - Choose Analysis Type:**
```
Agent: "What type of sensitivity analysis?"

1. One-Way Sensitivity
   Vary one assumption at a time

2. Two-Way Sensitivity Tables
   Vary two assumptions simultaneously

3. Scenario Analysis
   Pre-defined scenarios (Base/Upside/Downside)

4. Monte Carlo Simulation
   Probabilistic analysis with distributions
```

#### Option 1: One-Way Sensitivity

```
Agent: "Which assumptions should we sensitize? (Select multiple)"

☐ Revenue growth: Test 10%, 12%, 15%, 18%, 20%
☐ EBITDA margin: Test 16%, 18%, 20%, 22%, 24%
☐ WACC: Test 10%, 11.25%, 12.5%, 13.75%, 15%
☐ Terminal growth: Test 1.5%, 2%, 2.5%, 3%, 3.5%
☐ Exit multiple: Test 6x, 7x, 8x, 9x, 10x

User: Selects "Revenue growth" and "WACC"

Agent: "Creating sensitivity tables...

**Revenue Growth Sensitivity:**
10% → €32M (-29%)
12% → €38M (-16%)
15% → €45M (Base)
18% → €52M (+16%)
20% → €57M (+27%)

**WACC Sensitivity:**
10.0% → €58M (+29%)
11.25% → €51M (+13%)
12.5% → €45M (Base)
13.75% → €40M (-11%)
15.0% → €35M (-22%)

Key insight: Valuation is MORE sensitive to WACC than growth!
Should we focus on refining WACC assumptions?"
```

#### Option 2: Two-Way Tables

```
Agent: "Pick two variables to cross-analyze:
Most common combinations:
- Revenue growth × EBITDA margin
- WACC × Terminal growth
- Exit multiple × EBITDA

User: "Revenue growth × EBITDA margin"

Agent: "Creating 2-way table...

         EBITDA Margin →
         16%    18%    20%    22%    24%
Rev   10% €28M  €32M  €36M  €40M  €44M
Growth 12% €33M  €38M  €43M  €48M  €53M
↓     15% €39M  €45M  €51M  €57M  €63M
      18% €45M  €52M  €59M  €66M  €73M
      20% €49M  €57M  €65M  €73M  €81M

Insight: Every 2% margin improvement = ~€6M value
Every 3% revenue growth = ~€6M value

Which do you think is easier to achieve?"
```

#### Option 3: Scenario Analysis

```
Agent: "Let's build three scenarios.

For each, I'll ask you to define the key assumption changes.

**Base Case** (Current model):
- Revenue CAGR: 15%
- EBITDA margin: 18% → 22%
- WACC: 12.5%
- Result: €45M

Now let's define **Upside Case**.
What changes in an optimistic scenario?"

User: "Revenue grows 20%, margins hit 24%"

Agent: "Okay. Other changes?
- WACC stays same? Or decreases (de-risked)?
- Exit multiple higher (more demand)?
- Working capital improves?"

[Iterative dialog to build upside]

Agent: "**Upside Case:**
- Revenue CAGR: 20%
- EBITDA margin: 24%
- WACC: 11.5% (de-risked)
- Exit multiple: 10x (vs 8x base)
- Result: €68M (+51%)

Now **Downside Case**. What goes wrong?"

[Continue building downside]

**Final Scenario Summary:**
                Base    Upside  Downside
Revenue CAGR    15%     20%     10%
EBITDA Margin   20%     24%     18%
WACC            12.5%   11.5%   14.5%
Exit Multiple   8x      10x     6x
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Valuation       €45M    €68M    €28M

This gives you a robust range: €28M - €68M
Midpoint: €48M

How does this feel?"
```

#### Option 4: Monte Carlo

```
Agent: "Monte Carlo requires defining probability distributions.

For each key variable, tell me:
1. Most likely value
2. Min/max range
3. Distribution shape (normal, triangular, uniform)

Example for Revenue Growth:
- Most likely: 15%
- Range: 8% - 22%
- Distribution: Normal (bell curve)

Want to proceed with Monte Carlo? (Y/N)"

[If yes, continue setup dialog]
```

**Output:**
- Sensitivity tables (Excel)
- Tornado charts
- Scenario comparison table
- Probability distribution charts (if Monte Carlo)
- Executive summary of findings

---

### 7. Review & Export Final Package

**When to use:** You're done with analysis and need to deliver final materials.

**Dialog Flow:**

**Step 1 - Scope:**
```
Agent: "What do you need to deliver?"

Options:
○ Valuation model only (.xlsx)
○ Valuation + QoE analysis (2 files)
○ Full financial package (valuation, QoE, sensitivities, memo)
○ Custom (specify)
```

**Step 2 - Audience:**
```
Agent: "Who's the audience?"

○ Internal (seller management)
  → More detailed, technical, work-in-progress OK

○ External (buyers, investors)
  → Polished, executive summary, hide detailed workings

○ Both (two versions)

User: "External - buyers"

Agent: "Got it. I'll:
1. Clean up model formatting
2. Hide technical tabs (only show Executive Summary + Inputs)
3. Add professional cover page
4. Create PDF summary memo
5. Prepare data quality disclaimer

Sound good?"
```

**Step 3 - Create Package:**
```
Agent: "Creating final package...

✓ Executive Summary (1-page PDF)
✓ Valuation Model (cleaned Excel)
✓ QoE Analysis (Excel with charts)
✓ Sensitivity Analysis (Excel + charts)
✓ Data Quality Memo (PDF)
✓ Assumption Documentation (PDF)

Package saved to:
outputs/YourDeal/financial/final_package/

Files:
1. YourDeal_Executive_Summary_v1.0.pdf
2. YourDeal_Valuation_Model_FINAL_v1.0.xlsx
3. YourDeal_QoE_Analysis_v1.0.xlsx
4. YourDeal_Sensitivities_v1.0.xlsx
5. YourDeal_Assumptions_Memo_v1.0.pdf
6. YourDeal_Data_Quality_Notes_v1.0.pdf

Want me to zip this into one file?"
```

**Output:**
- Clean, polished final files
- Executive summaries
- Supporting documentation
- Packaged for distribution

---

### 8. Ask Financial Questions

**When to use:** You have specific questions or need spot analysis.

**This is free-form dialog.**

**Examples:**

```
User: "What's the current working capital as % of revenue?"

Agent: "Let me check...
2024 working capital: €850K
2024 revenue: €5.2M
Ratio: 16.3%

Industry benchmark: 12-15%
Your company is slightly high.

Want me to analyze why? Could be:
- Slow receivables collection
- Excess inventory
- Favorable payables terms (actually good)"
```

```
User: "If I sell for €40M, what's the seller's net proceeds?"

Agent: "Need a few details:
1. Any outstanding debt to repay?
2. Transaction costs (banker, lawyer fees)?
3. Management bonuses/rollover?
4. Working capital adjustment?

User: "€2M debt, €1.5M fees, no bonuses"

Agent: "Estimated seller proceeds:
Enterprise Value:          €40.0M
- Debt repayment:         (€ 2.0M)
- Transaction costs:      (€ 1.5M)
- Working capital adj:    (€ 0.2M) estimated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Net Proceeds to Seller:    €36.3M

This assumes normalized working capital peg.
Want me to model different scenarios?"
```

```
User: "How does our EBITDA margin compare to competitors?"

Agent: "Let me research... [Uses web search]

Comparable companies:
- CompanyA: 22% EBITDA margin
- CompanyB: 19%
- CompanyC: 25%
- CompanyD: 18%

Median: 20.5%
Your company: 20%

You're right at median - solid! But room to improve to top quartile.

Want me to add this to the valuation model as justification
for margin expansion assumptions?"
```

---

## Best Practices

### 1. Start with Document Analysis

Always begin with **Option 1: Analyze Documents** before building valuation. This ensures you have clean, structured data.

### 2. Use Devil's Advocate Before Finalizing

Run **Option 5: Devil's Advocate** before any important milestone:
- Before sending valuation to seller
- Before buyer meetings
- Before finalizing asking price

### 3. Iterate, Don't Perfect

The beauty of dialog mode is you can refine over time. Don't aim for perfection on first pass.

### 4. Ask Questions Freely

Use **Option 8: Ask Questions** whenever you're unsure. The agent is there to help you learn.

### 5. Save Versions Frequently

The system auto-versions, but you can also manually request saves:
"Save the current state as v1.5 before I make major changes"

---

## Tips for Effective Dialog

### Be Specific
❌ "The valuation seems off"
✅ "Revenue growth of 15% seems high - can we test 12%?"

### Push Back
The agent welcomes disagreement. If a recommendation doesn't feel right, say so.

### Ask "Why?"
"Why did you choose beta = 1.2?"
"Why is this adjustment valid?"

### Request Alternatives
"What are alternative ways to think about this?"
"Can we test a different methodology?"

### Use Devil's Advocate Aggressively
Don't hold back. The harder you challenge now, the better prepared you'll be for buyers.

---

## Common Workflows

### Workflow 1: New Deal, No Documents Yet
```
1. /financial-analyst
2. Select Option 1 (Analyze Documents)
3. [Upload documents]
4. Select scope and detail level
5. [Wait for analysis]
6. Select Option 2 (Build Valuation)
7. Follow dialog to build model
8. Select Option 5 (Devil's Advocate)
9. Challenge assumptions
10. Select Option 6 (Sensitivity Analysis)
11. Create scenarios
12. Select Option 7 (Export Package)
```

### Workflow 2: Refine Existing Valuation
```
1. /financial-analyst
2. Select Option 3 (Refine Excel Model)
3. Choose refinement focus
4. Iterate on improvements
5. Select Option 5 (Devil's Advocate)
6. Re-test assumptions
7. Save updated version
```

### Workflow 3: Quick Question
```
1. /financial-analyst
2. Select Option 8 (Ask Questions)
3. Ask your question
4. Get answer + optional follow-up analysis
```

---

## Technical Notes

### File Locations
All outputs save to:
```
ma-system/outputs/{deal-name}/financial/
  ├── valuation/
  ├── qoe-analysis/
  ├── sensitivities/
  ├── final_package/
  └── extractions/
```

### Version Control
- `v1.0` = Initial version
- `v1.1, v1.2` = Minor updates
- `v2.0` = Major revision

### Knowledge Base Updates
After each session, the agent updates:
- `ma-system/knowledge-base/deal-insights.md`
- `ma-system/knowledge-base/valuation-history.md`

### State Persistence
Your session state persists across interactions. You can leave and return later, and the menu will reflect your progress.

---

## Troubleshooting

**Q: Agent isn't showing the menu, just responding to my prompt**

A: Explicitly invoke with `/financial-analyst` to trigger dialog mode. If using natural language, try "Show me the financial analyst menu"

**Q: Menu options are missing**

A: The menu is context-aware. Options appear based on what's been completed. For example, "Refine Excel Model" only shows after you've built a valuation.

**Q: I want to skip the dialog and just analyze everything**

A: You can, but you'll lose the benefits of iterative refinement. If you insist, say: "Analyze all documents and build valuation with standard assumptions, no dialog"

**Q: Devil's Advocate is too aggressive**

A: Choose "Light challenge" mode instead of "Full challenge". You control the intensity.

**Q: How do I restart from scratch?**

A: "Reset financial analysis state and start over". This clears session memory.

---

## Summary

The new dialog-based Financial Analyst is designed for:
- **Transparency** - See and control every assumption
- **Education** - Learn financial analysis as you go
- **Quality** - Challenge and stress-test your thinking
- **Flexibility** - Iterate and refine over time
- **Collaboration** - Work WITH the agent, not just receive outputs

The goal: Better financial analysis through conversation, not automation.

---

**Questions?** Use Option 8 (Ask Questions) to ask the agent directly!
