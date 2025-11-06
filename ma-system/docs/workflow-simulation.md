# Workflow Simulation - Orchestrator-Driven M&A Process

**Deal:** Project Munich (TechTarget GmbH)
**Date:** 2024-11-06
**Purpose:** Demonstrate complete end-to-end workflow starting with orchestrator

---

## Starting State

**Knowledge Base:** Fresh deal, no work completed
**Dataroom:** Contains financial statements ready for analysis
**User Entry Point:** Natural language request to orchestrator

---

## Simulation: User Requests Valuation

### Step 1: User Request

```
User: "I need to value this company"
```

### Step 2: Orchestrator Receives Request

**Location:** `orchestrator/router.py`

```python
orchestrator = MAOrchestrator()
decision = orchestrator.route_request("I need to value this company")
```

**Intent Detection:**
```python
# Orchestrator analyzes keywords
detected_intent = 'financial_analysis'
confidence = 'high'

# Matches patterns:
# - "value", "valuation" → financial analysis
# - "company", "this" → uses current deal context
```

### Step 3: Knowledge Base Reading

**Orchestrator reads:** `knowledge-base/deal-insights.md`

```python
from orchestrator.knowledge_base_reader import get_current_deal_state

state = get_current_deal_state()

# Result:
KnowledgeBaseState(
    deal_name='Project Munich',
    target_company='TechTarget GmbH',
    deal_status='Active - Just Started',
    valuation_completed=False,
    valuation_version=None,
    financial_data_extracted=False,
    buyers_identified=0,
    cim_status='Not started',
    teaser_status='Not started'
)
```

**Key Findings:**
- ✅ Deal identified: Project Munich
- ❌ No existing valuation
- ❌ Financial data not yet extracted
- → **Action:** Create initial valuation (v1.0)

### Step 4: Routing Decision

```python
decision = RoutingDecision(
    primary_agent='financial-analyst',
    supporting_agents=['company-intelligence', 'market-intelligence', 'dd-manager'],
    rationale='Financial analysis requires Financial Analyst expertise',
    context_notes='Fresh start - no existing valuation found',
    orchestrator_context={
        'deal_name': 'Project Munich',
        'target_company': 'TechTarget GmbH',
        'existing_work': {},
        'suggested_action': 'create',
        'prerequisites': {
            'data_available': True,
            'met': True
        },
        'can_call_sub_agents': [
            'company-intelligence',
            'market-intelligence',
            'legal-tax-advisor',
            'dd-manager'
        ]
    }
)
```

### Step 5: Context Formatting for Agent

**Orchestrator calls:** `decision.format_for_agent()`

**Output passed to Financial Analyst:**

```
=== Orchestrator Context ===

Routing Rationale: Financial analysis requires Financial Analyst expertise

Notes: Fresh start - no existing valuation found

Deal: Project Munich (TechTarget GmbH)

Existing Work:
  None - fresh deal, no prior analysis

Suggested Action: create

Prerequisites:
  ✓ Financial data available in dataroom
  ✓ All prerequisites met

Available Sub-Agents:
  You can call these specialists if needed during analysis:
  - company-intelligence (for company/competitive research)
  - market-intelligence (for market data/comparables)
  - legal-tax-advisor (for legal/tax questions)
  - dd-manager (for data room queries)

=== End Orchestrator Context ===

User Request: "I need to value this company"

Begin your work...
```

### Step 6: Financial Analyst Activation

**Agent sees the context and understands:**
- This is Project Munich (TechTarget GmbH)
- No prior valuation exists → create v1.0
- Financial data available in dataroom
- Can call sub-agents if needed
- User wants a valuation

**Agent response:**
```
Financial Analyst (Project Munich)

I'll create an initial valuation for TechTarget GmbH. Let me start by extracting
financial data from the dataroom.

[Agent begins workflow - see next section]
```

---

## Workflow Execution: Financial Analyst

### Dialog Mode - Q&A Session

**Financial Analyst follows BMAD-style workflow:**

```
Financial Analyst: I'll guide you through creating a valuation for TechTarget GmbH.

First, let me extract the financial data from your dataroom...

[Agent reads files from dataroom/B.Financial general/]

Found:
- P&L statements: 2020-2023 (4 years)
- Balance sheets: 2020-2023
- Management accounts: 2024 (10 months)

=== Financial Data Extracted ===

Revenue (€000s):
  2020: 8,450
  2021: 9,280 (+9.8%)
  2022: 10,150 (+9.4%)
  2023: 11,320 (+11.5%)
  2024 (10m): 10,200 (projected: 12,240, +8.1%)

EBITDA (€000s):
  2020: 1,690 (20.0% margin)
  2021: 1,950 (21.0% margin)
  2022: 2,180 (21.5% margin)
  2023: 2,490 (22.0% margin)
  2024 (10m): 2,380 (projected: 2,856, 23.3% margin)

Key Observations:
- Consistent revenue growth (9-12% CAGR)
- Improving EBITDA margins (20% → 23%)
- Strong 2024 trajectory

Question 1: Revenue Growth Projection

I see historical revenue growth of 9-12% annually. For the DCF model, what
revenue growth rate should I project for the next 5 years?

Suggested Default: 8% (conservative, 80% of historical CAGR)
Confidence: HIGH
Rationale: Historical CAGR is 10.1%, suggest 8% as conservative estimate

Your input: [8%] or specify different rate _____
```

**This is where the smart defaults system helps:**
- Agent extracted data → Tier 1 summary created
- Generated smart default (8%) based on historical data
- User can accept or override
- Reduces back-and-forth questions

### Mid-Workflow: Sub-Agent Call Example

**Scenario:** While analyzing expenses, agent finds unusual item

```
Financial Analyst (analyzing 2022 data):

I notice a significant spike in legal/consulting fees in 2022:
  2020: €85k
  2021: €95k
  2022: €380k ← Spike
  2023: €120k

This looks like a one-time expense. Let me research what happened in 2022...

[Agent calls sub-agent]
```

**Sub-Agent Call:**

```python
from orchestrator.sub_agent_coordinator import call_sub_agent

result = call_sub_agent(
    primary_agent='financial-analyst',
    sub_agent='company-intelligence',
    task='Research TechTarget GmbH activities in 2022 - any M&A, legal matters, ' +
         'or major projects that would explain €380k in legal/consulting fees ' +
         '(vs €85k historical average)?',
    context={
        'account': '671000 - Legal and consulting fees',
        'amount': 380000,
        'year': 2022,
        'prior_years': [85000, 95000],
        'spike_magnitude': '4.5x increase'
    },
    expected_output='Brief description of 2022 activities and likely cause'
)
```

**Sub-Agent (Company Intelligence) Response:**

```
Company Intelligence Sub-Agent

Researching TechTarget GmbH 2022 activities...

[Searches web, company records, press releases]

Findings:
- Q2 2022: TechTarget acquired "DataPoint Analytics" (small competitor)
- Transaction closed June 2022
- Deal size: ~€1.2M (asset purchase)
- Legal costs for transaction: ~€300k

Summary:
The €380k legal/consulting spike in 2022 is attributable to the DataPoint
Analytics acquisition (Q2 2022). This was a one-time M&A transaction cost
and should be normalized when calculating recurring EBITDA.

Sources:
- German business registry (Handelsregister)
- Company press release (June 15, 2022)
- Local business news

Recommendation: Add back €295k (€380k - €85k historical) as one-time M&A cost
```

**Financial Analyst Integrates Finding:**

```
Financial Analyst:

Thanks to company research, I've identified the 2022 legal spike as a one-time
M&A transaction cost (DataPoint Analytics acquisition).

EBITDA Normalization:
  Reported 2022 EBITDA: €2,180k
  Add back: M&A legal costs: +€295k
  Normalized 2022 EBITDA: €2,475k

This normalization adjusts the 2022 margin from 21.5% to 24.4%, which is more
consistent with 2023-2024 performance.

Updated EBITDA History:
  2020: €1,690k (20.0%)
  2021: €1,950k (21.0%)
  2022: €2,475k (24.4%) ← Normalized
  2023: €2,490k (22.0%)
  2024: €2,856k (23.3%)

[Continues with valuation...]
```

**Key Points:**
- Financial analyst encountered question during analysis
- Called company-intelligence sub-agent for research
- Sub-agent performed focused research task
- Returned condensed findings
- Financial analyst integrated into normalization analysis
- **All in single context** - no manual coordination needed

### Valuation Completion

**After Q&A dialog completes:**

```
Financial Analyst:

=== Valuation Complete ===

DCF Analysis:
  Revenue CAGR (2025-2029): 8.0%
  EBITDA Margin: 23% (sustainable)
  WACC: 8.5%
  Terminal Growth: 2.0%

  DCF Valuation: €28.5M

Multiples Analysis:
  Comparable EV/Revenue: 2.5-3.0x
  Comparable EV/EBITDA: 9.0-11.0x

  Using 2024 metrics:
  Revenue Multiple: €30.6M (2.5x)
  EBITDA Multiple: €31.4M (11.0x)

Final Valuation Range:
  Low:      €26.0M (DCF -10%)
  Midpoint: €29.8M (Blended)
  High:     €32.5M (Multiples +5%)

Recommended Enterprise Value: €29.8M

Files Created:
- outputs/Project-Munich/financial/valuation/Project-Munich_Valuation_Model_v1.0.xlsx
- outputs/Project-Munich/financial/tier1/financial-summary-tier1.json
- outputs/Project-Munich/financial/tier2/revenue-analysis-tier2.json
- outputs/Project-Munich/financial/tier2/ebitda-analysis-tier2.json

[Updating knowledge base...]
```

### Step 7: Knowledge Base Update

**Financial Analyst updates:** `knowledge-base/deal-insights.md`

**Changes:**

```markdown
## Executive Summary
**Current Phase:** Preparation → **Valuation Complete**
**Enterprise Value:** Not yet determined → **€29.8M (€26.0M - €32.5M)**
**Equity Value:** Not yet determined → **€27.3M**

## Valuation
### Current Valuation
- **Latest Valuation:** Not started → **v1.0**
- **Status:** ○ Not completed → **✓ Complete**
- **Valuation Date:** → **2024-11-06**
- **Enterprise Value Range:** → **€26.0M - €32.5M**
- **Midpoint (EV):** → **€29.8M**
- **Equity Value:** → **€27.3M** (after net debt adjustment)
- **Method:** → **DCF + Multiples (blended)**

### Valuation History
| Date | Version | EV Midpoint | Range | Method | Key Changes |
|------|---------|-------------|-------|--------|-------------|
| - | - | - | - | - | No valuations yet |
| 2024-11-06 | v1.0 | €29.8M | €26.0M - €32.5M | DCF + Multiples | Initial valuation |

## Financial Analysis
### Data Extraction Status
- **Status:** ○ Not started → **✓ Complete**
- **Source Files:** None processed → **4 files (P&L 2020-2023, BS 2020-2023)**
- **Coverage:** 0% → **100%**
- **Tier 1 Summary:** Not created → **✓ Created (2024-11-06)**

## Timeline
| Date | Event | Agent | Notes |
|------|-------|-------|-------|
| 2024-11-06 | Deal initiated | Managing Director | Project Munich started |
| 2024-11-06 | Valuation v1.0 completed | Financial Analyst | Initial DCF + Multiples, EV: €29.8M |

## Next Steps
**Recommended Next Actions:**
1. ○ Extract and analyze financial data → **✓ DONE**
2. ○ Build initial valuation → **✓ DONE**
3. ○ Research target company and competitive landscape
4. ○ Identify potential strategic and financial buyers
5. ○ Create teaser document
6. ○ Develop CIM
```

**Agent returns control to user:**

```
Financial Analyst:

✓ Valuation v1.0 complete for Project Munich
✓ Enterprise Value: €29.8M (range: €26.0M - €32.5M)
✓ Knowledge base updated
✓ Files saved to outputs/

What would you like to do next?

Suggestions:
- Create a teaser document for buyer outreach
- Identify potential buyers (strategic/financial)
- Research company competitive position
- Develop detailed CIM
```

---

## Simulation: Second Request - Create Teaser

### User Request

```
User: "Create a teaser for this deal"
```

### Orchestrator Routes Request

**Intent Detection:** `document_creation`

**Knowledge Base Check:**
```python
state = get_current_deal_state()

# Finds:
- valuation_completed = True
- valuation_version = 'v1.0'
- valuation_ev_midpoint = 29.8
- teaser_status = 'Not started'
- financial_data_extracted = True
```

**Routing Decision:**

```python
decision = RoutingDecision(
    primary_agent='document-generator',
    supporting_agents=['financial-analyst', 'company-intelligence'],
    rationale='Document creation requires Document Generator expertise',
    context_notes='Valuation v1.0 exists (€29.8M), ready for teaser creation',
    orchestrator_context={
        'deal_name': 'Project Munich',
        'existing_work': {
            'valuation': 'v1.0',
            'financial_data': 'Extracted'
        },
        'suggested_action': 'create',
        'prerequisites': {
            'valuation_complete': True,
            'met': True
        },
        'can_call_sub_agents': [
            'financial-analyst',
            'company-intelligence',
            'market-intelligence'
        ]
    }
)
```

**Context Passed to Document Generator:**

```
=== Orchestrator Context ===

Routing Rationale: Document creation requires Document Generator expertise

Notes: Valuation v1.0 exists (€29.8M), ready for teaser creation

Deal: Project Munich (TechTarget GmbH)

Existing Work:
  - valuation: v1.0 (€29.8M)
  - financial_data: Extracted and analyzed

Suggested Action: create

Prerequisites:
  ✓ Valuation complete
  ✓ Financial data available
  ✓ All prerequisites met

Available Sub-Agents:
  - financial-analyst (for financial data/valuation)
  - company-intelligence (for company description)
  - market-intelligence (for market positioning)

=== End Orchestrator Context ===

User Request: "Create a teaser for this deal"

Begin your work...
```

**Document Generator activates with full context:**
- Knows valuation exists (€29.8M)
- Can pull financial data from Tier 1 summary
- Can call sub-agents if needs more info
- Creates teaser document

---

## Key Workflow Benefits

### 1. Context Continuity

**Without Orchestrator:**
```
User: "Create a teaser"
Document Generator: "What's the deal name?"
User: "Project Munich"
Document Generator: "Do you have a valuation?"
User: "Yes, €29.8M"
Document Generator: "What's the valuation range?"
User: "€26M to €32.5M"
...
```

**With Orchestrator:**
```
User: "Create a teaser"
Orchestrator: [Reads knowledge base, finds valuation v1.0]
Document Generator: "I'll create a teaser using your existing valuation (v1.0, €29.8M)..."
[Agent starts working immediately]
```

**Savings:** 5-7 back-and-forth questions eliminated

### 2. Sub-Agent Coordination

**Example from workflow above:**

```
Financial Analyst (primary)
    ↓ encounters question about 2022 expense spike
    ↓ spawns sub-agent
Company Intelligence (sub-agent)
    ↓ researches 2022 acquisition
    ↓ returns findings
Financial Analyst (primary)
    ↓ integrates findings into normalization
    ✓ continues with analysis
```

**All in single context** - no manual coordination needed

### 3. Smart Defaults

**Without Smart Defaults:**
```
Agent: "What revenue growth rate should I use?"
User: "Uh, I don't know... what's typical?"
Agent: "Depends on historical performance..."
User: "What was historical?"
Agent: "Let me check... 10.1% CAGR"
User: "Ok use 8%"
```

**With Smart Defaults:**
```
Agent: "Revenue growth projection?"
Agent: "Suggested: 8% (HIGH confidence - 80% of historical 10.1% CAGR)"
User: "✓" [or specify different]
```

**Savings:** ~1,500 tokens per Q&A session

### 4. Knowledge Base Persistence

**Benefit:** Every agent action updates shared knowledge base

```
Session 1: Create valuation → KB updated
Session 2: Create teaser → KB shows valuation exists
Session 3: Find buyers → KB shows valuation + teaser exist
Session 4: Update valuation → KB shows v1.0, agent creates v1.1
```

**No context loss between sessions**

---

## Token Usage Analysis

### Traditional Approach (No Orchestrator)
```
- User explains context: 500 tokens
- Agent asks clarifying questions: 800 tokens
- User provides answers: 600 tokens
- Agent loads all data: 80,000 tokens
- Agent performs analysis: 10,000 tokens
- Total: ~92,000 tokens
```

### Orchestrator-Driven Approach
```
- Orchestrator reads KB: 2,000 tokens
- Orchestrator passes context: 500 tokens
- Agent loads Tier 1 summary: 2,000 tokens
- Agent performs analysis: 10,000 tokens
- Smart defaults: -1,500 tokens saved
- Total: ~13,000 tokens
```

**Savings: 79,000 tokens (86% reduction)**

---

## Production Readiness

### ✅ Implemented Features

1. **Real Knowledge Base Reading**
   - `knowledge_base_reader.py` parses deal-insights.md
   - Extracts structured state (valuation, buyers, documents, etc.)
   - Used for routing decisions

2. **Context Passing to Agents**
   - `RoutingDecision.format_for_agent()` creates formatted context
   - Agents receive: rationale, existing work, suggested action, prerequisites
   - Eliminates redundant questions

3. **Sub-Agent Coordination**
   - `sub_agent_coordinator.py` enables agent-to-agent calls
   - Permission system (not all agents can call all sub-agents)
   - Example: Financial analyst → Company intelligence for research

4. **Optional But Preferred**
   - Direct agent calls still work: `/financial-analyst`
   - Orchestrator routing recommended: Better context, fewer questions
   - Users choose their preferred entry point

### 📊 Test Results

```bash
cd orchestrator
python3 router.py
```

**Output:**
```
M&A Orchestrator - Production-Ready Routing

Knowledge Base Loaded:
  Deal: Project Munich
  Target: TechTarget GmbH
  Valuation: ○ Not completed
  Financial Data: ○ Not extracted
  Buyers: 0 identified

User Request: 'Value this company'

Routing Decision:
  Primary Agent: financial-analyst
  Context Notes: Fresh start - no existing valuation found

Context for Agent Activation:
=== Orchestrator Context ===
Deal: Project Munich
Existing Work: None
Suggested Action: create
✓ All prerequisites met
Available Sub-Agents: company-intelligence, market-intelligence, ...
=== End Orchestrator Context ===

✓ Orchestrator is production-ready
```

---

## File Structure

```
ma-system/
├── orchestrator/
│   ├── router.py                        # Main orchestrator
│   ├── knowledge_base_reader.py         # KB parsing
│   └── sub_agent_coordinator.py         # Sub-agent coordination
│
├── knowledge-base/
│   └── deal-insights.md                 # Single source of truth
│
├── dataroom/
│   └── B.Financial general/
│       ├── TechTarget_PL_2020-2023.xlsx
│       └── TechTarget_BS_2020-2023.xlsx
│
├── outputs/
│   └── Project-Munich/
│       └── financial/
│           ├── valuation/
│           │   └── Project-Munich_Valuation_Model_v1.0.xlsx
│           ├── tier1/
│           │   └── financial-summary-tier1.json
│           └── tier2/
│               ├── revenue-analysis-tier2.json
│               └── ebitda-analysis-tier2.json
│
└── docs/
    ├── production-ready-orchestrator.md
    └── workflow-simulation.md           # This file
```

---

## Next Steps for Users

**Recommended Workflow:**

1. **Start with natural language:**
   ```
   "I need to value this company"
   "Create a teaser document"
   "Find potential buyers in Germany"
   ```

2. **Let orchestrator route:**
   - Orchestrator detects intent
   - Reads knowledge base
   - Routes to appropriate agent
   - Passes context

3. **Agent executes with context:**
   - Knows existing work
   - Can call sub-agents if needed
   - Uses smart defaults
   - Updates knowledge base

4. **Continue incrementally:**
   ```
   "Update the valuation"        → Loads v1.0, creates v1.1
   "Add buyers to the list"      → Expands existing buyer list
   "Revise the CIM"              → Loads v1.X, increments version
   ```

**All context preserved across sessions via knowledge base**

---

## Summary

✅ **Production-ready orchestrator** enables:
- Intent-based routing from natural language
- Context-aware agent activation
- Sub-agent coordination for specialized tasks
- Knowledge base persistence across sessions
- 86% token reduction vs traditional approach

✅ **Flexible architecture** supports:
- Direct agent calls (e.g., `/financial-analyst`)
- Orchestrator routing (recommended)
- Parallel or sequential execution
- Incremental updates to existing work

✅ **BMAD-style workflow** with:
- Dialog mode for user decisions
- Smart defaults to reduce Q&A
- Tier 1/2/3 data architecture
- 100% coverage guarantee

**The system is ready for production M&A workflows.**
