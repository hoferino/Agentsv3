# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Overview

This is a **flexible, task-based M&A advisory agent system** that breaks from traditional phase-based M&A workflows. The core innovation: **any agent can be activated at any time** based on user intent, available context, and task requirements - not rigid phase gates.

### Key Architectural Principle
**Task-based, not phase-based.** Agents share persistent context through a knowledge base and can work in parallel or sequentially based on dependencies, not arbitrary workflow rules.

## Testing the System

```bash
# Test orchestrator routing
cd orchestrator
python3 router.py

# This validates intent detection and agent routing logic
# Should output routing decisions for sample M&A requests
```

## System Architecture

### Core Components

1. **Orchestrator** (`orchestrator/router.py`)
   - Intent analyzer using regex patterns
   - Context-aware routing based on knowledge base state
   - Dependency checker for prerequisites
   - Returns `RoutingDecision` objects with primary agent, supporting agents, required skills

2. **Context Management System** (NEW - Critical for long conversations)
   - **Tiered Data Architecture**: All agents use 3-tier data model for efficiency
     - Tier 1 (Summary): Always loaded, 2k tokens - answers 90% of questions
     - Tier 2 (Detailed): On-demand loading, 20k tokens per file - deep dives
     - Tier 3 (Raw/Complete): Query-only, never fully loaded - 100% coverage guarantee
   - **Auto-Checkpointing**: Sessions automatically save state at 60% context usage (120k tokens)
   - **Transparent Session Management**: Context refresh happens behind the scenes, user sees continuous flow
   - **100% Coverage Guarantee**: All data from source files preserved in Tier 3, zero information loss
   - See `docs/100-percent-coverage-strategy.md` for complete architecture

3. **Agents** (`agents/*.md`) - 8 specialized agents, always available:
   - `managing-director` - Orchestration & strategy
   - `financial-analyst` - Valuation, models, QoE (uses `xlsx` skill)
   - `market-intelligence` - Buyer research, comparables (uses `web_search`, `xlsx`)
   - `document-generator` - CIM, teasers, presentations (uses `docx`, `pptx`, `pdf`)
   - `dd-manager` - Data room, Q&A, issues (uses `xlsx`, `pdf`)
   - `buyer-relationship-manager` - LOI comparison, negotiations (uses `xlsx`, `docx`)
   - `legal-tax-advisor` - Transaction structure, legal DD (uses `pdf`, `docx`)
   - `company-intelligence` - Company research, competitive analysis (uses `web_search`)

3. **Knowledge Base** (`knowledge-base/`)
   - `deal-insights.md` - Single source of truth, auto-updated by all agents
   - `valuation-history.md` - Tracks assumption evolution over time
   - `buyer-profiles/` - Individual buyer intelligence files
   - **Critical:** Agents MUST update knowledge base after completing tasks

4. **Workflows** (`workflows/`)
   - YAML templates defining activation triggers, workflow steps, outputs
   - Can be triggered at any time (no phase restrictions)
   - Example: `workflows/financial/valuation/workflow.yaml`

5. **Outputs** (`outputs/`)
   - Version-controlled deliverables: `{deal-name}_{type}_v{X}.{ext}`
   - Organized by category: financial/, documents/, market-research/, etc.

### Intent Detection Flow

```
User Request (natural language)
    ↓
Orchestrator analyzes intent (regex patterns in router.py)
    ↓
Context Checker queries knowledge-base/deal-insights.md
    ↓
Router selects primary agent + supporting agents
    ↓
Dependency Checker validates prerequisites
    ↓
Agent(s) execute with required skills
    ↓
Update knowledge base + outputs/
```

## Configuration

### Global Config (`config.yaml`)

```yaml
project_config:
  deal_name: "Project Munich"           # Update per deal
  target_company: "TechTarget GmbH"     # Update per deal

context:
  completed_tasks:                      # Auto-updated by agents
    valuation: false
    cim_created: false
    # ... tracks progress

orchestration:
  intent_keywords:                      # Defines routing patterns
    financial_analysis: ["valuation", "bewertung", "DCF"]
    document_creation: ["CIM", "teaser", "erstellen"]
    # ... see full file for all patterns
```

**Important:** `config.yaml` contains intent detection keywords for routing. When adding new capabilities, update the relevant `intent_keywords` section.

## Working with Agents

### Agent Definition Structure (in `agents/*.md`)

Each agent markdown file contains:
- **Core Capabilities** - What the agent does
- **Triggers** - Keywords that activate this agent
- **Required Skills** - Which Claude Code skills needed (`xlsx`, `docx`, etc.)
- **Outputs Created** - File naming conventions and formats
- **Workflow Examples** - Common usage patterns
- **Context Awareness** - How agent checks/uses prior work
- **Knowledge Base Integration** - What gets updated after execution

### Adding New Agent Capabilities

1. Edit agent's markdown file to document new capability
2. Add activation triggers to agent file
3. Update `orchestrator/router.py`:
   - Add regex patterns to `intent_patterns` dict
   - Add routing logic to appropriate `_route_*` method
4. Update `config.yaml` with intent keywords if needed

## Knowledge Base Workflow

**Critical Pattern:** All agents follow this flow:

1. **Check context** - Read `knowledge-base/deal-insights.md` for prior work
2. **Execute task** - Perform analysis, research, or document creation
3. **Update knowledge base** - Write findings back to `deal-insights.md`
4. **Save outputs** - Version-controlled files to `outputs/{deal-name}/`

Example: Financial Analyst updating valuation:
```python
# 1. Check for existing valuation in knowledge base
existing_valuation = check_knowledge_base("valuation")

# 2. If exists, load v1.X and increment; else create v1.0
version = "v1.1" if existing_valuation else "v1.0"

# 3. Perform valuation analysis

# 4. Update knowledge base
update_deal_insights("valuation", new_valuation_data)

# 5. Save output file
save_file(f"outputs/{deal_name}/financial/valuation/{deal_name}_Valuation_Model_{version}.xlsx")
```

## Version Control Convention

All outputs use semantic versioning:
- `v1.0` - Initial version
- `v1.1, v1.2` - Minor updates (data refresh, typo fixes)
- `v2.0` - Major revision (methodology change, significant updates)

File naming: `{deal-name}_{document-type}_{description}_v{X}.{ext}`

Examples:
- `Project-Munich_Valuation_Model_v1.0.xlsx`
- `Project-Munich_CIM_v2.3.docx`
- `Project-Munich_Strategic_Buyers_v1.5.xlsx`

## Extending the Orchestrator

### Adding New Intent Category

In `orchestrator/router.py`:

```python
# 1. Add to intent_patterns dict
self.intent_patterns['new_category'] = [
    r'\b(keyword1|keyword2)\b',
    r'\b(specific pattern)\s+(match)\b'
]

# 2. Create routing method
def _route_new_category(self, user_input: str) -> RoutingDecision:
    return RoutingDecision(
        primary_agent='agent-name',
        supporting_agents=['helper1', 'helper2'],
        required_skills=['xlsx', 'web_search'],
        rationale='Why this routing',
        parallel_execution=True/False,
        context_notes='Relevant context'
    )

# 3. Add to routing_map in _route_by_intent()
routing_map = {
    # ... existing mappings
    'new_category': self._route_new_category
}
```

### Adding Dependency Checks

In `orchestrator/router.py`, update `check_dependencies()`:

```python
def check_dependencies(self, routing_decision: RoutingDecision) -> List[str]:
    prerequisites = []

    # Example: New document requires valuation
    if routing_decision.primary_agent == 'document-generator':
        if 'new_doc' in routing_decision.context_notes.lower():
            if not self.knowledge_base['valuation']['completed']:
                prerequisites.append('Complete valuation before creating new document')

    return prerequisites
```

## Bilingual Support

System supports German and English:
- Intent patterns include both languages (e.g., "valuation" / "bewertung")
- User can set preferred language in `config.yaml`: `user_preferences.language: "de"` or `"en"`
- All agent outputs respect language preference
- Natural language requests work in both languages

## Common Patterns

### Context-Aware Updates
When user requests "update the valuation":
1. Orchestrator checks `knowledge-base/deal-insights.md` for existing valuation
2. Finds version (e.g., v1.2)
3. Routes to Financial Analyst with context: "existing valuation v1.2"
4. Agent loads existing file, updates, saves as v1.3
5. Updates knowledge base with new version

### Parallel Execution
When user requests "update valuation and find new buyers":
1. Orchestrator detects two independent intents
2. Returns two `RoutingDecision` objects, both with `parallel_execution=True`
3. Financial Analyst and Market Intelligence work simultaneously
4. Both update knowledge base upon completion

### Dependency Handling
When user requests "create CIM" but valuation doesn't exist:
1. Orchestrator checks dependencies
2. Returns prerequisite: "Complete valuation first"
3. Routes to Financial Analyst for valuation
4. Then routes to Document Generator for CIM
5. Sequential execution enforced by dependency

## Output File Locations

Outputs organized by deal and type:
```
outputs/
└── {deal-name}/
    ├── financial/
    │   ├── valuation/
    │   ├── financial-models/
    │   ├── qoe-analysis/
    │   └── working-capital/
    ├── documents/
    │   ├── cim/
    │   ├── teasers/
    │   ├── presentations/
    │   └── letters/
    ├── market-research/
    ├── due-diligence/
    └── deal-execution/
```

## Key Design Decisions

1. **No Phase Gates**: Any agent can run at any time. The `current_phase` in config is informational only, never used for access control.

2. **Shared Intelligence**: All agents read/write to single knowledge base (`deal-insights.md`). This enables cross-agent coordination without explicit communication.

3. **Idempotent Updates**: Agents check for existing work before creating new. "Update valuation" loads v1.X and increments, never starts from scratch.

4. **Natural Language Routing**: Intent detection uses regex patterns on natural language, not structured commands. Easier to use, harder to predict edge cases.

5. **Skill-Based Execution**: Agents declare required skills (`xlsx`, `docx`, etc.). Claude Code auto-loads these for execution.

## Workflow YAML Structure

Workflow templates define reusable task sequences:

```yaml
name: "Workflow Name"
activation_triggers:          # Keywords that trigger this workflow
  - "keyword1"
  - "keyword2"

prerequisites:
  required_data:
    field_name: "required" | "optional"

agents_needed:
  primary: "agent-name"
  supporting: ["agent2", "agent3"]

context_awareness:
  check_existing: true        # Look for prior work
  incremental_update: true    # Build on existing
  version_control: true       # Track versions

execution:
  mode: "flexible"            # Can run with partial info
  parallel_execution: true    # Can run with other tasks
  update_knowledge_base: true # Update after completion

workflow_steps:               # Ordered execution steps
  1_step_name: "Description"
  2_next_step: "Description"

outputs:
  primary:
    - file: "{deal-name}_{type}_v{X}.ext"
      description: "What it contains"

  updates:                    # Knowledge base updates
    - "knowledge-base/deal-insights.md (what changed)"
```

## Prerequisites

- Python 3.8+
- PyYAML: `pip install pyyaml`
- Claude Code skills enabled: `xlsx`, `docx`, `pptx`, `pdf`, `web_search`

## Starting a New Deal

1. Edit `config.yaml`:
   ```yaml
   project_config:
     deal_name: "Your Deal Name"
     target_company: "Target Company"
   ```

2. Initialize `knowledge-base/deal-insights.md`:
   - Update deal name, company, industry
   - Set initial status fields

3. Begin with natural language requests:
   - "Research the company [Name]"
   - "Perform a business valuation"
   - "Create a teaser"
   - "Identify potential buyers"

The orchestrator routes automatically based on intent.
