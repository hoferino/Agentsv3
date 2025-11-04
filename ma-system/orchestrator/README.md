# M&A System Orchestrator

## Purpose

The orchestrator provides intelligent routing of user requests to the appropriate specialized agents. Unlike rigid phase-based systems, this orchestrator makes context-aware decisions based on:

1. **User Intent** - What is the user trying to accomplish?
2. **Available Information** - What work has already been done?
3. **Dependencies** - What needs to happen first?
4. **Optimal Agent** - Who can best handle this request?

## Key Features

### 🎯 Intent-Based Routing
- Analyzes natural language requests
- Detects multiple intents in complex requests
- Routes to appropriate specialist agents
- No artificial phase restrictions

### 🧠 Context Awareness
- Checks knowledge base for prior work
- Identifies incremental vs. new tasks
- Tracks document versions
- Maintains deal state

### ⚡ Parallel Execution
- Enables multiple agents to work simultaneously
- Identifies independent tasks
- Optimizes workflow efficiency

### 🔄 Dynamic Adaptation
- Learns from deal progression
- Adjusts routing based on context
- Suggests next logical steps

## Architecture

```
User Request
     ↓
Intent Analyzer
     ↓
Context Checker ← Knowledge Base
     ↓
Router (Selects Agent)
     ↓
Agent Executor
     ↓
Knowledge Base Update
     ↓
Response to User
```

## Core Components

### 1. Intent Analyzer (`router.py`)
Analyzes user input to determine what they want to accomplish.

**Intent Categories:**
- `financial_analysis` - Valuation, modeling, QoE
- `document_creation` - CIM, teaser, presentations
- `market_intelligence` - Buyer research, market analysis
- `due_diligence` - Data room, Q&A, issues
- `deal_execution` - LOI comparison, negotiations
- `legal_tax` - Structure, legal review

### 2. Context Manager
Maintains awareness of current deal state.

**Tracks:**
- Completed work (valuation done? CIM created?)
- Document versions
- Buyer engagement status
- Outstanding issues
- Timeline and milestones

### 3. Agent Router
Selects optimal agent(s) for each request.

**Routing Logic:**
```python
Intent → Agent Mapping:
- financial_analysis → Financial Analyst
- document_creation → Document Generator
- market_intelligence → Market Intelligence
- due_diligence → DD Manager
- deal_execution → Buyer Relationship Manager
- legal_tax → Legal Tax Advisor
```

### 4. Dependency Checker
Identifies prerequisites before executing tasks.

**Examples:**
- CIM creation → Requires valuation first
- Buyer outreach → Requires teaser/CIM
- LOI comparison → Requires multiple LOIs

## Usage Examples

### Example 1: Simple Routing
```python
from orchestrator.router import MAOrchestrator

orchestrator = MAOrchestrator()

# User request
decision = orchestrator.route_request("Value this company")

# Result
decision.primary_agent = "financial-analyst"
decision.required_skills = ["xlsx"]
decision.supporting_agents = ["market-intelligence"]
```

### Example 2: Context-Aware Update
```python
# First valuation
orchestrator.route_request("Create a valuation")
# → Routes to Financial Analyst, creates v1.0

# Later update
orchestrator.route_request("Update the valuation")
# → Routes to Financial Analyst, loads v1.0, creates v1.1
```

### Example 3: Multi-Agent Coordination
```python
# Complex request
orchestrator.route_request("Prepare for buyer meetings")

# Routes to multiple agents:
# 1. Financial Analyst - Update financial model
# 2. Document Generator - Refresh presentation
# 3. Market Intelligence - Research buyers
# 4. Buyer Relationship Manager - Prepare strategy
```

### Example 4: Parallel Execution
```python
# Independent tasks
orchestrator.route_request("Update valuation and find new buyers")

# Both can run in parallel:
# - Financial Analyst (valuation)
# - Market Intelligence (buyers)
# No dependencies between them
```

## Integration with Claude Code

### Using as Slash Commands

Create slash commands that map to agent workflows:

```bash
# .claude/commands/valuation.md
/valuation - Perform business valuation
Trigger Financial Analyst to create comprehensive valuation

# .claude/commands/create-cim.md
/create-cim - Create Confidential Information Memorandum
Trigger Document Generator to create CIM with all supporting data
```

### Using with Agent System

```python
# In Claude Code agent configuration
from orchestrator.router import MAOrchestrator

orchestrator = MAOrchestrator()

# Route user request
decisions = orchestrator.route_request(user_input)

# Execute with appropriate agent
for decision in decisions:
    agent = load_agent(decision.primary_agent)
    result = agent.execute(
        task=user_input,
        skills=decision.required_skills,
        context=decision.context_notes
    )
```

## Routing Decision Structure

```python
@dataclass
class RoutingDecision:
    primary_agent: str              # Main agent to handle request
    supporting_agents: List[str]    # Agents that may be consulted
    required_skills: List[str]      # Skills needed (xlsx, docx, etc.)
    rationale: str                  # Why this routing decision
    parallel_execution: bool        # Can run parallel to other tasks
    context_notes: str              # Relevant context from KB
```

## Extending the Orchestrator

### Adding New Intent Patterns

Edit `router.py`:

```python
self.intent_patterns = {
    # ... existing patterns ...
    'new_category': [
        r'\b(keyword1|keyword2)\b',
        r'\b(pattern)\s+(match)\b'
    ]
}
```

### Adding New Agent

1. Create agent markdown file in `/agents/`
2. Add to `agent_capabilities` in router:

```python
'new-agent': {
    'role': 'specialist',
    'skills': ['required', 'skills'],
    'specializations': ['task1', 'task2']
}
```

3. Add routing logic:

```python
def _route_new_category(self, user_input: str) -> RoutingDecision:
    return RoutingDecision(
        primary_agent='new-agent',
        # ... configuration ...
    )
```

### Adding Context Checks

Extend `check_dependencies()`:

```python
def check_dependencies(self, routing_decision):
    prerequisites = []

    # Add your dependency logic
    if condition_not_met:
        prerequisites.append('Complete X before Y')

    return prerequisites
```

## Testing the Orchestrator

Run the test suite:

```bash
cd orchestrator
python router.py
```

This will test routing decisions for common requests.

## Best Practices

1. **Trust the Router**: Don't override routing decisions without good reason
2. **Update Knowledge Base**: Always update KB after completing tasks
3. **Context is Key**: Provide context in requests for better routing
4. **Parallel When Possible**: Enable parallel execution for independent tasks
5. **Check Dependencies**: Review prerequisites before starting complex tasks

## Troubleshooting

### Issue: Wrong agent selected
- Check intent patterns - may need refinement
- Add more specific keywords
- Provide more context in request

### Issue: Missing dependencies
- Update `check_dependencies()` logic
- Ensure knowledge base is current
- Add prerequisite checks

### Issue: No route found
- Falls back to Managing Director
- Add new intent patterns if needed
- Check for typos in request

## Future Enhancements

Potential improvements:
- [ ] Machine learning for intent detection
- [ ] Agent performance tracking
- [ ] Automatic workflow optimization
- [ ] Predictive next-step suggestions
- [ ] Natural language feedback on routing decisions
- [ ] Multi-language support refinement

---

**Note**: This orchestrator is designed to be flexible and adaptive. It learns from the deal progression and adjusts routing accordingly. There are no rigid phase gates - all agents are available at all times.
