# Orchestrator → Financial Analyst Workflow Review

**Current Implementation Analysis**

---

## Overview

This document reviews how user requests flow from the orchestrator to the financial analyst agent, including routing logic, agent activation, workflow execution, and knowledge base updates.

---

## Current Workflow Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. User Request (Natural Language)                              │
│    "Ich möchte eine financial analysis machen"                  │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. Orchestrator (router.py)                                     │
│    - analyze_intent() → Detects 'financial_analysis'            │
│    - route_request() → Returns RoutingDecision                  │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. RoutingDecision                                              │
│    primary_agent: 'financial-analyst'                           │
│    supporting_agents: ['market-intelligence']                   │
│    required_skills: ['xlsx']                                    │
│    context_notes: 'New valuation - will build from scratch'     │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. Financial Analyst Agent Activation (financial-analyst.md)   │
│    Step 1: Load persona and reference material                 │
│    Step 2: Read config.yaml (deal_name, output_folder, etc.)   │
│    Step 3: Initialize tiered data architecture                 │
│    Step 4: Load menu configuration                             │
│    Step 5: Initialize FinancialAnalystDialog                   │
│    Step 6: Greet user, render main menu                        │
│    Step 7: STOP and wait for user input                        │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. User Selects Menu Option                                    │
│    Example: "1. Analyze Financial Documents"                   │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. Workflow Execution (if workflow menu item)                  │
│    - Load workflow.xml processor                               │
│    - Execute workflow.yaml (e.g., data-extraction)             │
│    - Follow steps sequentially                                 │
│    - Save outputs to sandbox/                                  │
│    - Update knowledge base                                     │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. Return to Menu                                              │
│    Agent shows menu again, waits for next action               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed Workflow Stages

### Stage 1: User Request

**Input:**
```
User: "Ich möchte eine financial analysis machen. im ordner data room
       habe ich einige dokumente zu financials hochgeladen"
```

**Analysis:**
- Natural language (German/English mix)
- Contains financial keywords: "financial analysis"
- Provides context: dataroom location

---

### Stage 2: Orchestrator Intent Detection

**File:** `/orchestrator/router.py`

**Code:**
```python
def analyze_intent(self, user_input: str) -> List[str]:
    """Analyze user input to determine intent(s)."""
    intents = []
    user_input_lower = user_input.lower()

    for intent_category, patterns in self.intent_patterns.items():
        for pattern in patterns:
            if re.search(pattern, user_input_lower, re.IGNORECASE):
                intents.append(intent_category)
                break

    return list(set(intents))
```

**Intent Patterns for Financial Analysis:**
```python
'financial_analysis': [
    r'\b(valuation|bewertung|dcf|value|worth|financial model|finanzmodell)\b',
    r'\b(qoe|quality of earnings|normalized ebitda)\b',
    r'\b(working capital|betriebskapital|nwc)\b'
]
```

**Result:**
- Detects: `['financial_analysis']`

---

### Stage 3: Routing Decision

**File:** `/orchestrator/router.py:_route_financial()`

**Code:**
```python
def _route_financial(self, user_input: str) -> RoutingDecision:
    """Route financial analysis requests"""

    # Check if updating existing work or new work
    context = ""
    if self.knowledge_base['valuation']['completed']:
        context = f"Existing valuation: {self.knowledge_base['valuation']['latest']}"

    return RoutingDecision(
        primary_agent='financial-analyst',
        supporting_agents=['market-intelligence'],  # For comparable data
        required_skills=['xlsx'],
        rationale='Financial analysis requires Financial Analyst expertise',
        parallel_execution=False,
        context_notes=context or 'New valuation - will build from scratch'
    )
```

**Output:**
```python
RoutingDecision(
    primary_agent='financial-analyst',
    supporting_agents=['market-intelligence'],
    required_skills=['xlsx'],
    rationale='Financial analysis requires Financial Analyst expertise',
    parallel_execution=False,
    context_notes='New valuation - will build from scratch'
)
```

**Notes:**
- Orchestrator checks knowledge base for existing valuation
- If exists → context mentions "updating existing"
- If not exists → context says "new valuation"
- Supporting agents listed but **not automatically spawned** (Task 2 confirmed this)

---

### Stage 4: Financial Analyst Activation

**File:** `/agents/financial-analyst.md`

**Activation Steps (Critical - MANDATORY):**

```xml
<activation critical="MANDATORY">
  <step n="1">Load persona and reference material from this file.</step>

  <step n="2">Read {project-root}/ma-system/config.yaml and store:
      - {deal_name} = project_config.deal_name
      - {output_folder} = project_config.output_folder
      - {communication_language} = user_preferences.language
      - {sandbox_path} = {output_folder}/sandbox</step>

  <step n="3">Initialize tiered data architecture:
      - Check if {sandbox_path}/tier1/summary.json exists
      - If exists: Load Tier 1 summary (2k tokens max)
      - If not exists: Flag for data extraction on first workflow
      - Store tier2_loaded = {} (empty dict for on-demand loading)
      - Set tier3_path = {sandbox_path}/tier3/raw_accounts_database.json</step>

  <step n="4">Load menu configuration from
      {project-root}/ma-system/agents/financial-analyst-menu.yaml
      into session variable menu_options.</step>

  <step n="5">Import `FinancialAnalystDialog` from
      {project-root}/ma-system/agents/financial-analyst-dialog.py
      and initialize: dialog = FinancialAnalystDialog(deal_name={deal_name}).</step>

  <step n="6">Greet the user using {communication_language}, mention {deal_name},
      then render the main menu using dialog._format_main_menu().</step>

  <step n="7">STOP and wait for input. Accept either menu number, command trigger,
      or natural language mapped to menu_options. Confirm any ambiguous matches.</step>

  <step n="8">Persist updated interaction mode preferences by calling
      dialog._save_user_preference when user changes mode.</step>
</activation>
```

**What Happens:**

1. **Persona loaded** - Agent becomes financial analyst character
2. **Config loaded** - Gets deal name ("Project Munich"), paths, language
3. **Tiered data initialized:**
   - Checks if data already extracted
   - If yes: Loads Tier 1 (2k tokens)
   - If no: Flags for extraction workflow
4. **Menu loaded** - Available actions from YAML
5. **Dialog initialized** - Menu-driven interface ready
6. **User greeted** - Shows menu in German (or user's language)
7. **Waits for input** - User chooses menu option or types command

**Example Agent Greeting:**
```
Guten Tag! Ich bin Ihr Financial Analyst für Project Munich.

Hauptmenü:
1. Analyze Financial Documents
2. Build or Update Valuation
3. Refine Valuation Model
4. Run Quality of Earnings
5. Play Devil's Advocate
6. Sensitivity & Scenario Analysis
7. Review & Export Package
8. Ask Financial Questions
9. Change Interaction Mode

Was möchten Sie tun?
→
```

---

### Stage 5: User Selects Menu Option

**User Input:**
```
User: "1"  (or "Analyze Financial Documents")
```

**Agent Processing:**

```xml
<menu-handlers>
  <handler type="workflow">
    When menu item includes workflow="path/to/workflow.yaml":
      1. Load {project-root}/ma-system/core/tasks/workflow.xml.
      2. Execute workflow.xml with parameter workflow-config set to the provided path.
      3. Follow every workflow step sequentially, saving interim outputs when instructed.
  </handler>
</menu-handlers>
```

**Menu Item Configuration:**
```yaml
# From financial-analyst-menu.yaml
- number: 1
  label: "Analyze Financial Documents"
  command: "*analyze-documents"
  workflow: "workflows/financial/document-analysis/workflow.yaml"
  description: "Extract and analyze financial statements from data room"
```

---

### Stage 6: Workflow Execution

**Workflow File:** `/workflows/financial/document-analysis/workflow.yaml`

**Typical Workflow Structure:**

```yaml
name: "Financial Document Analysis"
version: "1.0"
agent: "financial-analyst"

prerequisites:
  required_data:
    data_room_path: "required"

workflow_steps:
  1_validate_inputs:
    description: "Validate data room path and files"
    actions:
      - Check data room path exists
      - List all financial files
      - Verify file types

  2_extract_data:
    description: "Extract financial data to tiered structure"
    actions:
      - Run data extraction workflow
      - Create tier1/, tier2/, tier3/
      - Validate 100% coverage

  3_analyze:
    description: "Analyze extracted data"
    actions:
      - Calculate key metrics
      - Identify trends
      - Flag issues

  4_update_knowledge_base:
    description: "Update deal insights"
    updates:
      - file: "knowledge-base/deal-insights.md"
        section: "Financial Analysis"

outputs:
  primary:
    - file: "{sandbox_path}/tier1/summary.json"
```

**Execution:**
- Agent loads `workflow.xml` processor
- Executes each step sequentially
- Saves outputs to specified locations
- Updates knowledge base
- Returns summary to user

---

### Stage 7: Return to Menu

After workflow completes:

```
✓ Financial document analysis complete

Summary:
  - Files analyzed: 3
  - Time periods: 2020-2023 (H1)
  - Data extracted to: sandbox/tier1/summary.json
  - Coverage validated: 100%

Hauptmenü:
1. Analyze Financial Documents ✓
2. Build or Update Valuation
3. Refine Valuation Model
...

Was möchten Sie als nächstes tun?
→
```

---

## Knowledge Base Integration

### Before Workflow

**Orchestrator checks:**
```python
# In router.py:_route_financial()
if self.knowledge_base['valuation']['completed']:
    context = f"Existing valuation: {self.knowledge_base['valuation']['latest']}"
```

**Knowledge Base Structure:**
```yaml
# knowledge-base/deal-insights.md
## Financial Analysis
Status: Not started
Last updated: -

## Valuation
Status: Not completed
Latest version: -
```

### After Workflow

**Agent updates:**
```yaml
## Financial Analysis
Status: ✓ Complete
Last updated: 2024-11-06
Files analyzed: 3
Time periods: 2020-2023
Coverage: 100%

## Valuation
Status: Not completed
Latest version: -
```

**Next time user requests financial analysis:**
- Orchestrator sees `financial_analysis: completed`
- Routes with context: "Updating existing analysis"
- Agent loads existing Tier 1 data (2k tokens)
- User can iterate/refine instead of starting over

---

## Critical Design Decisions

### 1. Menu-Driven vs. Direct Execution

**Current Approach (Menu-Driven):**
```
User → Orchestrator → Financial Analyst → Menu → User selects option → Workflow
```

**Alternative (Direct Execution):**
```
User → Orchestrator → Financial Analyst → Auto-detect workflow → Execute
```

**Why Menu-Driven?**
- ✅ User has control over what happens
- ✅ Can choose specific workflows (valuation, QoE, sensitivity)
- ✅ Transparent about available actions
- ✅ Can refine/iterate easily
- ❌ Requires extra user input (menu selection)

### 2. Workflow-Based vs. Conversational

**Current (Workflow-Based):**
- Menu item triggers YAML workflow
- Steps executed sequentially
- Structured outputs

**Alternative (Conversational):**
- Agent interprets user intent in conversation
- Adaptive questioning
- Flexible execution

**Why Workflow-Based?**
- ✅ Repeatable, auditable processes
- ✅ Consistent outputs
- ✅ Easy to version control
- ✅ Clear documentation
- ❌ Less flexible for ad-hoc requests

**Solution:** Hybrid approach
- Menu offers workflows
- Menu item #8: "Ask Financial Questions" → conversational mode
- Best of both worlds

### 3. Supporting Agents Listed But Not Auto-Spawned

**Current:**
```python
supporting_agents=['market-intelligence']  # Listed but not spawned
```

**Behavior:**
- Orchestrator notes which agents *could* help
- Primary agent (financial-analyst) executes
- Primary agent *may* call supporting agents if needed
- No automatic multi-agent spawning (Task 2 confirmed)

**Why?**
- ✅ Context efficient (single agent context)
- ✅ Flexible (primary agent decides if/when to involve others)
- ✅ User has control
- ❌ Requires manual coordination

---

## Context Management in Workflow

### Tiered Data Usage

```
Agent Activation:
  └─ Load Tier 1 (2k tokens) if exists
     └─ Context: 2k tokens

User selects workflow:
  └─ Workflow reads Tier 1
     └─ Context: Still 2k tokens (already loaded)

Workflow needs details:
  └─ Load Tier 2 revenue_detail.json
     └─ Context: 22k tokens (2k + 20k)

User asks specific question:
  └─ Query Tier 3 for account 440000
     └─ Context: 22.05k tokens (22k + 50 tokens)

Total session:
  └─ 22.05k tokens vs 95k with old approach (77% savings)
```

---

## Issues / Potential Improvements

### Issue 1: Orchestrator → Agent Handoff

**Current:**
- Orchestrator returns `RoutingDecision`
- Unclear HOW agent actually gets activated in Claude Code
- Seems to rely on `/financial-analyst` slash command?

**Question:**
- Is orchestrator used in production?
- Or is it just design documentation?
- How does `RoutingDecision` trigger agent activation?

**Recommendation:**
- Document the actual mechanism
- If using slash commands, orchestrator should map to them
- Example: `RoutingDecision.primary_agent='financial-analyst'` → Execute `/financial-analyst` command

### Issue 2: Supporting Agents Coordination

**Current:**
- `supporting_agents=['market-intelligence']` listed
- But no mechanism to actually invoke them
- Primary agent would need to manually spawn them

**Question:**
- Should orchestrator pre-load supporting agent context?
- Should primary agent have API to call supporting agents?
- Or is it just documentation for human understanding?

**Recommendation:**
- If supporting agents needed, provide coordination mechanism
- Example: `call_supporting_agent('market-intelligence', task='find comparables')`

### Issue 3: Context Notes Not Passed to Agent

**Current:**
```python
RoutingDecision(
    context_notes='New valuation - will build from scratch'
)
```

**Issue:**
- These notes created by orchestrator
- But how do they reach the financial analyst?
- Agent activation doesn't show loading `context_notes`

**Recommendation:**
- Pass context notes to agent on activation
- Example: Add to greeting: "Note: New valuation - will build from scratch"
- Or: Pass as parameter to agent

### Issue 4: Knowledge Base Loading

**Orchestrator checks knowledge base:**
```python
self.knowledge_base['valuation']['completed']
```

**But:**
- `_load_knowledge_base()` has TODO comment
- Returns hardcoded dict, not actual file read

**Recommendation:**
- Implement actual knowledge base reading
- Read from `knowledge-base/deal-insights.md`
- Parse status fields
- Return real state

---

## Suggested Workflow Improvements

### Improvement 1: Make Orchestrator Optional

**Current Flow:**
```
User → Orchestrator → Financial Analyst
```

**Improved:**
```
User → /financial-analyst (direct activation)
OR
User → Orchestrator → /financial-analyst (routed)
```

**Why:**
- Some users want direct access
- Orchestrator adds value for complex routing
- But simple "I want financial analysis" doesn't need routing
- Let user choose

### Improvement 2: Auto-Detect Workflow from User Input

**Current:**
```
User: "I want financial analysis"
→ Orchestrator routes to Financial Analyst
→ Agent shows menu
→ User selects "1. Analyze Documents"
→ Workflow executes
```

**Improved:**
```
User: "Analyze financial documents from dataroom"
→ Orchestrator detects specific intent
→ Routes to Financial Analyst with context: "Auto-trigger: document-analysis"
→ Agent greets, then says: "I see you want to analyze documents. Starting workflow..."
→ Workflow executes (with confirmation prompt)
→ Then returns to menu
```

**Why:**
- Fewer clicks for common workflows
- Still gives user control (confirmation prompt)
- Maintains menu for exploration

### Improvement 3: Pass Orchestrator Context to Agent

**Implementation:**
```xml
<activation>
  <step n="2">Read config.yaml AND orchestrator context if provided:
      - If context_notes provided: Display to user
      - If existing_work flag: Load previous version
      - If supporting_agents listed: Note for potential collaboration
  </step>
</activation>
```

**Example:**
```
Guten Tag! Ich bin Ihr Financial Analyst für Project Munich.

Orchestrator Note: Existing valuation found (v1.0). You can update or create new version.

Hauptmenü:
1. Update Existing Valuation (v1.0 → v1.1)
2. Create New Valuation (v2.0)
...
```

---

## Current State Summary

### ✅ Works Well

1. **Intent detection** - Regex patterns catch financial keywords
2. **Agent activation** - Clear 8-step activation process
3. **Menu-driven interface** - User-friendly, transparent
4. **Workflow execution** - YAML-based, auditable, repeatable
5. **Tiered data architecture** - Context efficient (2k vs 95k)
6. **Knowledge base updates** - Workflows document findings
7. **Single-agent pattern** - No multi-spawning (Task 2 confirmed)

### ⚠️ Needs Clarification

1. **Orchestrator → Agent handoff mechanism** - How does routing trigger activation?
2. **Supporting agents** - Listed but no coordination mechanism
3. **Context notes** - Created by orchestrator, but how passed to agent?
4. **Knowledge base reading** - TODO in orchestrator, not implemented

### 🔧 Potential Improvements

1. Make orchestrator optional (direct agent activation)
2. Auto-detect workflow from user input (fewer clicks)
3. Pass orchestrator context to agent (better continuity)
4. Implement actual knowledge base reading in orchestrator

---

## Questions for Review

1. **How does RoutingDecision actually trigger agent activation in Claude Code?**
   - Via slash commands?
   - Manual copy-paste of agent markdown?
   - Automatic invocation?

2. **Are supporting agents meant to be used in production?**
   - Or just documentation?
   - If used, what's the coordination mechanism?

3. **Should orchestrator be mandatory or optional?**
   - Always route through orchestrator?
   - Or allow direct `/financial-analyst` activation?

4. **How should context_notes from orchestrator reach the agent?**
   - Pass as activation parameter?
   - Write to temporary file?
   - Ignore (just for orchestrator logging)?

---

**Document Status:** Ready for review
**Last Updated:** 2024-11-06
