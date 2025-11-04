# M&A Advisory Agent System

**Version:** 1.0
**Last Updated:** 2024-11-04
**Status:** Ready for Implementation

---

## 🎯 Overview

A flexible, task-based M&A advisory system powered by specialized AI agents. Unlike traditional phase-based M&A systems, this architecture allows **any agent to be activated at any time** based on user needs, available information, and task requirements.

### Key Innovation: Context-Aware, Not Phase-Restricted

Traditional M&A systems enforce rigid phase gates (e.g., "you can only create a CIM after completing due diligence"). This system breaks that paradigm:

- ✅ **Valuation can be updated anytime** new information arrives
- ✅ **Buyer research can run in parallel** with document creation
- ✅ **Due diligence prep can start early** even before buyer outreach
- ✅ **All agents share knowledge** through persistent context
- ✅ **Tasks can be performed iteratively** and refined over time

---

## 🏗️ Architecture

### System Components

```
ma-system/
├── config.yaml                 # Global configuration
├── agents/                     # 8 specialized agents (always available)
├── workflows/                  # Task-based workflow templates
├── knowledge-base/            # Persistent deal intelligence
├── orchestrator/              # Intelligent routing system
└── outputs/                   # Generated deliverables
```

### 8 Specialized Agents

1. **Managing Director** - Orchestrator and strategic advisor
2. **Financial Analyst** - Valuation, modeling, QoE, working capital
3. **Market Intelligence** - Buyer research, market analysis, comparables
4. **Document Generator** - CIM, teasers, presentations, letters
5. **DD Manager** - Data room, Q&A tracking, issue management
6. **Buyer Relationship Manager** - Buyer tracking, LOI comparison, negotiations
7. **Legal & Tax Advisor** - Transaction structure, legal DD, tax analysis
8. **Company Intelligence** - Company research, competitive analysis

---

## 🚀 Getting Started

### Prerequisites

- Claude Code environment
- Skills enabled: `xlsx`, `docx`, `pptx`, `pdf`, `web_search`
- Python 3.8+ (for orchestrator)

### Initial Setup

1. **Configure your deal:**
   ```yaml
   # Edit config.yaml
   project_config:
     deal_name: "Your Deal Name"
     target_company: "Target Company Name"
   ```

2. **Initialize knowledge base:**
   - Edit `knowledge-base/deal-insights.md` with basic deal info
   - Agents will auto-populate as work progresses

3. **Test orchestrator:**
   ```bash
   cd orchestrator
   python router.py
   ```

### First Tasks

**Recommended starting sequence:**
1. "Research the target company" → Company Intelligence
2. "Perform valuation" → Financial Analyst
3. "Create a CIM" → Document Generator
4. "Identify potential buyers" → Market Intelligence

**But remember:** You can do these in **any order** based on your needs!

---

## 💡 How to Use

### Natural Language Interaction

Simply describe what you need:

```
✅ "Value this company"
✅ "Create a teaser"
✅ "Find strategic buyers"
✅ "Set up the data room"
✅ "Compare the LOIs"
✅ "Update the valuation with Q3 results"
```

The orchestrator automatically:
1. Analyzes your intent
2. Checks what work already exists
3. Routes to the appropriate agent(s)
4. Provides context-aware execution
5. Updates knowledge base

### Common Workflows

#### Workflow 1: Initial Deal Setup
```
User: "Let's start this M&A process"

System routes to:
1. Company Intelligence → Research target
2. Financial Analyst → Initial valuation
3. Document Generator → Create teaser
4. Market Intelligence → Identify buyers

All can run in parallel!
```

#### Workflow 2: Buyer Outreach
```
User: "Prepare for buyer outreach"

System checks:
- Teaser ready? If not, creates it
- Buyer list ready? If not, researches
- Valuation current? If not, updates

Then routes to:
- Buyer Relationship Manager → Coordinate outreach
```

#### Workflow 3: Due Diligence
```
User: "Buyer is ready for DD"

System routes to:
1. DD Manager → Set up data room
2. Financial Analyst → Prepare financial materials
3. Legal Tax Advisor → Organize legal documents
```

### Iterative Refinement

```
User: "Create valuation" → v1.0 created
[New info arrives]
User: "Update valuation" → v1.1 created (builds on v1.0)
[Buyer feedback received]
User: "Refine valuation based on buyer questions" → v1.2 created
```

---

## 📁 Directory Structure

### `/agents/` - Agent Definitions

Each agent is defined in a markdown file with:
- Core capabilities
- Activation triggers
- Required skills
- Workflow examples
- Output specifications
- Integration points

**Key Feature:** All agents are **always available** - no phase restrictions.

### `/workflows/` - Task Templates

Pre-defined workflow templates for common tasks:
- Financial analysis (valuation, modeling)
- Document creation (CIM, teaser, presentations)
- Market research (buyers, comparables, industry)
- Due diligence (data room, Q&A, issues)
- Deal execution (LOI comparison, negotiations)

**Key Feature:** Workflows are **flexible** - can be triggered at any time.

### `/knowledge-base/` - Persistent Intelligence

Central repository for all deal intelligence:
- `deal-insights.md` - Current deal status, valuation, buyers, issues
- `valuation-history.md` - Track valuation evolution
- `buyer-profiles/` - Detailed buyer intelligence

**Key Feature:** **Auto-updated** by all agents after task completion.

### `/orchestrator/` - Routing Logic

Intelligent routing system that:
- Analyzes user intent
- Checks context and prior work
- Routes to optimal agent(s)
- Manages dependencies
- Enables parallel execution

**Key Feature:** **Context-aware** routing, not phase-based.

### `/outputs/` - Generated Deliverables

All generated files organized by type:
- Financial models (`.xlsx`)
- Transaction documents (`.docx`, `.pptx`, `.pdf`)
- Market research reports
- Due diligence materials
- Deal execution tools

**Key Feature:** **Version controlled** with clear naming conventions.

---

## 🧠 Intelligent Features

### 1. Context Awareness

The system remembers prior work:

```
First request: "Value the company"
→ Creates valuation v1.0

Later request: "Update valuation"
→ Loads v1.0, updates to v1.1 (doesn't start from scratch)
```

### 2. Dependency Detection

The system identifies prerequisites:

```
Request: "Create CIM"
System checks: Valuation exists? No.
Response: "I'll first complete the valuation, then create the CIM"
```

### 3. Parallel Execution

Independent tasks run simultaneously:

```
Request: "Update valuation and find new buyers"
→ Financial Analyst works on valuation
→ Market Intelligence researches buyers (in parallel)
```

### 4. Proactive Suggestions

The system recommends next steps:

```
After completing valuation:
"Valuation complete (€28M). I recommend:
1. Creating the CIM to incorporate this valuation
2. Identifying strategic buyers in this value range"
```

### 5. Cross-Agent Intelligence

Agents share information:

```
Market Intelligence finds buyers
→ Updates knowledge base
→ Buyer Relationship Manager uses buyer list for outreach
→ Document Generator creates buyer-specific presentations
```

---

## 🔧 Configuration

### Global Settings (`config.yaml`)

```yaml
project_config:
  deal_name: "Project Munich"
  target_company: "TechTarget GmbH"

user_preferences:
  language: "de"  # or "en"
  auto_agent_switching: true
  skill_auto_load: true

orchestration:
  allow_parallel_execution: true
  auto_detect_dependencies: true
  context_aware: true
```

### Agent-Specific Settings

Each agent can be customized in its markdown definition file.

### Workflow Customization

Edit workflow YAML files in `/workflows/` to:
- Adjust activation triggers
- Modify workflow steps
- Change output formats
- Add custom prerequisites

---

## 📊 Typical M&A Process Flow

While agents can be used in any order, here's a typical sequence:

### Phase 1: Preparation (Week 1-2)
- ✅ Company Intelligence: Research target
- ✅ Financial Analyst: Create valuation
- ✅ Document Generator: Create teaser and CIM
- ✅ Market Intelligence: Identify buyers

### Phase 2: Marketing (Week 3-6)
- ✅ Buyer Relationship Manager: Distribute teaser
- ✅ Buyer Relationship Manager: Track buyer engagement
- ✅ DD Manager: Prepare data room
- ✅ Document Generator: Create management presentation

### Phase 3: Negotiations (Week 7-10)
- ✅ Buyer Relationship Manager: Coordinate meetings
- ✅ DD Manager: Manage Q&A process
- ✅ Buyer Relationship Manager: Compare LOIs
- ✅ Legal Tax Advisor: Review transaction structure

### Phase 4: Due Diligence (Week 11-14)
- ✅ DD Manager: Manage data room access
- ✅ Financial Analyst: Support financial DD
- ✅ Legal Tax Advisor: Support legal DD
- ✅ Buyer Relationship Manager: Manage buyer relationship

### Phase 5: Closing (Week 15-16)
- ✅ Legal Tax Advisor: Review purchase agreement
- ✅ Buyer Relationship Manager: Negotiation support
- ✅ Managing Director: Coordinate closing

**Important:** This is illustrative only - you can jump to any step at any time!

---

## 🛠️ Advanced Usage

### Custom Workflows

Create custom workflow files in `/workflows/`:

```yaml
name: "Custom Workflow"
activation_triggers:
  - "keyword1"
  - "keyword2"

agents_needed:
  primary: "agent-name"
  supporting: ["agent2", "agent3"]

workflow_steps:
  1: "Step description"
  2: "Step description"
```

### Extending the Orchestrator

Add new intent patterns in `orchestrator/router.py`:

```python
self.intent_patterns['new_category'] = [
    r'\b(pattern1|pattern2)\b',
]
```

### Integration with External Tools

Agents can integrate with:
- Excel for financial modeling (`xlsx` skill)
- Word for documents (`docx` skill)
- PowerPoint for presentations (`pptx` skill)
- Web search for research (`web_search` skill)
- PDF processing (`pdf` skill)

---

## 📈 Best Practices

### 1. Keep Knowledge Base Updated
- Agents auto-update after tasks
- Manually review and refine as needed
- Track key decisions and rationale

### 2. Version Everything
- All outputs are version controlled
- Old versions archived
- Changes documented

### 3. Use Natural Language
- Describe what you need clearly
- System handles routing automatically
- Provide context for better results

### 4. Leverage Parallel Execution
- Request multiple independent tasks at once
- System will run them in parallel
- Saves significant time

### 5. Iterate and Refine
- Start with rough drafts
- Refine as you gather more information
- Update valuations, documents, etc. as needed

---

## 🔍 Troubleshooting

### Agent Not Activating?
- Check activation triggers in agent markdown file
- Verify orchestrator intent patterns
- Try more specific language in request

### Missing Dependencies?
- Review `check_dependencies()` in orchestrator
- Ensure prerequisite tasks are completed
- Check knowledge base for prior work

### Output Not Generated?
- Verify required skills are available
- Check output path in configuration
- Review agent execution logs

### Knowledge Base Not Updating?
- Ensure agents complete tasks successfully
- Check file permissions on knowledge-base directory
- Verify auto-update is enabled in config

---

## 📚 Documentation

- **Agent Definitions**: See `/agents/*.md`
- **Workflow Templates**: See `/workflows/**/*.yaml`
- **Orchestrator Guide**: See `/orchestrator/README.md`
- **Output Standards**: See `/outputs/README.md`
- **Knowledge Base**: See `/knowledge-base/deal-insights.md`

---

## 🎓 Example Scenarios

### Scenario 1: Starting Fresh
```
User: "I have a new M&A deal to advise on"
System: "Let's start with the basics. What's the company?"
User: "Industrial automation software company, €13M revenue"
System: Routes to Company Intelligence
→ Researches company
→ Updates knowledge base
→ Suggests: "Next steps: valuation, CIM creation, buyer identification"
```

### Scenario 2: Mid-Process Update
```
User: "We just received Q3 results - revenue up 25%"
System: Checks knowledge base - valuation exists at v1.2
→ Routes to Financial Analyst
→ Updates valuation to v1.3 with Q3 data
→ Routes to Document Generator
→ Updates CIM with new valuation
→ Notifies: "Valuation and CIM updated with stronger growth story"
```

### Scenario 3: Multiple Parallel Tasks
```
User: "Prepare for management meetings next week with 3 buyers"
System: Identifies multiple independent tasks
→ Market Intelligence: Research 3 buyers (parallel)
→ Document Generator: Update management presentation (parallel)
→ Financial Analyst: Refresh financial model (parallel)
→ Buyer Relationship Manager: Create meeting strategy
→ Completes all in optimal time
```

---

## 🚦 System Status

✅ **Complete Components:**
- Agent definitions (8 agents)
- Workflow templates (4 key workflows)
- Knowledge base structure
- Orchestrator routing logic
- Output management system
- Configuration system

⏳ **In Progress:**
- Integration testing
- Real deal testing
- Performance optimization

🎯 **Future Enhancements:**
- Machine learning for intent detection
- Automated workflow optimization
- Multi-language refinement
- Advanced analytics dashboard

---

## 📞 Support & Contribution

### Questions?
- Review agent documentation in `/agents/`
- Check workflow templates in `/workflows/`
- Consult orchestrator README in `/orchestrator/`

### Improvements?
- Extend agent capabilities in markdown files
- Add new workflows in `/workflows/`
- Enhance orchestrator routing in `router.py`
- Update intent patterns for better detection

---

## 🎉 Quick Start Checklist

- [ ] Review `config.yaml` and update deal information
- [ ] Test orchestrator: `python orchestrator/router.py`
- [ ] Initialize knowledge base with deal basics
- [ ] Run first task: Company research
- [ ] Create initial valuation
- [ ] Generate teaser document
- [ ] Identify potential buyers
- [ ] Begin buyer outreach

**You're ready to run M&A processes with flexible, intelligent agent support!**

---

**Built with:** Claude Code + Specialized AI Agents
**Philosophy:** Task-based, not phase-based. Context-aware, not rule-restricted.
**Goal:** Make M&A advisory more flexible, efficient, and intelligent.
