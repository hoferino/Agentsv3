# M&A Agent System - Setup Guide

This guide will walk you through setting up and running your M&A advisory agent system.

---

## 📋 Prerequisites

### Required Software
- Python 3.8 or higher
- Claude Code CLI
- Text editor (VS Code recommended)

### Required Claude Code Skills
Ensure these skills are available:
- `xlsx` - Excel file handling
- `docx` - Word document creation
- `pptx` - PowerPoint presentations
- `pdf` - PDF reading and creation
- `web_search` - Internet research

Check skills availability:
```bash
# In Claude Code
/skills list
```

---

## 🚀 Installation Steps

### Step 1: Verify Directory Structure

Ensure you have this structure:

```
ma-system/
├── config.yaml
├── README.md
├── SETUP.md (this file)
├── agents/ (8 .md files)
├── workflows/ (organized subdirectories)
├── knowledge-base/
│   ├── deal-insights.md
│   ├── valuation-history.md
│   └── buyer-profiles/
├── orchestrator/
│   ├── router.py
│   └── README.md
└── outputs/
    └── README.md
```

Verify:
```bash
cd ma-system
ls -la
```

### Step 2: Install Python Dependencies

```bash
# Install PyYAML for config loading
pip install pyyaml

# Optional: Install other useful libraries
pip install pandas  # For data manipulation
pip install openpyxl  # For Excel files
```

### Step 3: Configure Your Deal

Edit `config.yaml`:

```yaml
project_config:
  deal_name: "Your Deal Name"  # Change this
  target_company: "Target Company"  # Change this
  created_date: "2024-11-04"  # Today's date

  deal_info:
    industry: "Technology"  # Update
    geography: "Germany"  # Update
    deal_type: "sell-side"  # or buy-side
    transaction_size: "mid-market"  # small | mid-market | large-cap
```

### Step 4: Initialize Knowledge Base

Edit `knowledge-base/deal-insights.md`:

```markdown
**Deal Name:** [Your Deal Name]
**Target Company:** [Target Company]
**Last Updated:** [Today's Date]

## Executive Summary
[Brief 2-3 sentence overview of the deal]

## Company Profile Summary
### Company Basics
- **Industry:** [Industry]
- **Founded:** [Year or TBD]
- **Employees:** [Number or TBD]
- **Geography:** [Primary markets]
- **Revenue:** [Amount or TBD]
```

### Step 5: Test the Orchestrator

```bash
cd orchestrator
python router.py
```

Expected output:
```
M&A Orchestrator - Routing Examples
============================================================

User Request: 'Value this company'
  Routing Decision #1:
    Primary Agent: financial-analyst
    Supporting: market-intelligence
    Skills: xlsx
    ...
```

If this works, your orchestrator is functioning correctly!

---

## ✅ Verification Checklist

Run through this checklist to ensure everything is set up:

- [ ] Directory structure is complete
- [ ] `config.yaml` is configured with your deal
- [ ] `knowledge-base/deal-insights.md` is initialized
- [ ] Python 3.8+ is installed
- [ ] PyYAML is installed (`pip install pyyaml`)
- [ ] Orchestrator test runs successfully
- [ ] All 8 agent files exist in `/agents/`
- [ ] Workflow templates exist in `/workflows/`
- [ ] Claude Code skills are available

---

## 🎯 First Run

### Starting Your First Deal

1. **Initialize the System**
   ```bash
   cd ma-system
   ```

2. **Set Up Your Deal Context**
   - Edit `config.yaml` with deal details
   - Update `knowledge-base/deal-insights.md` with basic info

3. **Run Your First Task**

   In Claude Code, try:
   ```
   "Research the target company: [Company Name]"
   ```

   The system will:
   - Detect intent: company_intelligence
   - Route to: Company Intelligence agent
   - Execute: Web research on the company
   - Update: knowledge-base/deal-insights.md
   - Output: Company overview document

4. **Continue with Core Tasks**

   ```
   "Perform a business valuation"
   → Routes to Financial Analyst
   → Creates valuation model

   "Create a teaser for this company"
   → Routes to Document Generator
   → Creates teaser presentation

   "Identify potential strategic buyers"
   → Routes to Market Intelligence
   → Creates buyer list
   ```

---

## 🔧 Configuration Options

### Language Settings

For German language:
```yaml
user_preferences:
  language: "de"
```

For English:
```yaml
user_preferences:
  language: "en"
```

### Agent Behavior

Enable/disable features:
```yaml
user_preferences:
  auto_agent_switching: true  # Seamless agent transitions
  skill_auto_load: true  # Auto-load required skills
  verbose_mode: false  # Show detailed reasoning

orchestration:
  allow_parallel_execution: true  # Run independent tasks simultaneously
  auto_detect_dependencies: true  # Check prerequisites
  context_aware: true  # Use knowledge base context
```

### Output Preferences

Customize output formats:
```yaml
user_preferences:
  output_format:
    financial_models: "xlsx"
    documents: "docx"
    presentations: "pptx"
    reports: "pdf"
```

---

## 🧪 Testing Your Setup

### Test 1: Orchestrator Routing

```bash
cd orchestrator
python router.py
```

✅ Should display routing decisions for sample requests

### Test 2: Agent File Integrity

```bash
ls agents/
```

✅ Should show 8 `.md` files:
- managing-director.md
- financial-analyst.md
- market-intelligence.md
- document-generator.md
- dd-manager.md
- buyer-relationship-manager.md
- legal-tax-advisor.md
- company-intelligence.md

### Test 3: Workflow Templates

```bash
ls workflows/financial/valuation/
```

✅ Should show `workflow.yaml`

### Test 4: Knowledge Base

```bash
cat knowledge-base/deal-insights.md
```

✅ Should display formatted deal insights template

---

## 🐛 Troubleshooting

### Issue: Python import errors

**Problem:** `ModuleNotFoundError: No module named 'yaml'`

**Solution:**
```bash
pip install pyyaml
```

### Issue: Orchestrator test fails

**Problem:** router.py throws errors

**Solution:**
1. Check Python version: `python --version` (need 3.8+)
2. Verify file exists: `ls orchestrator/router.py`
3. Check for syntax errors in router.py

### Issue: Agent files not found

**Problem:** "Agent file not found" errors

**Solution:**
```bash
# Verify all agent files exist
ls agents/
# Should show 8 .md files

# If missing, they should be in your ma-system directory
```

### Issue: Config not loading

**Problem:** YAML parsing errors

**Solution:**
1. Check YAML syntax in `config.yaml`
2. Ensure proper indentation (use spaces, not tabs)
3. Validate YAML online: http://www.yamllint.com/

### Issue: Knowledge base not updating

**Problem:** Agents don't update deal-insights.md

**Solution:**
1. Check file permissions: `ls -la knowledge-base/`
2. Ensure file is writable
3. Verify path in config.yaml is correct

---

## 📚 Next Steps

Once setup is complete:

1. **Read the Main README**
   - `README.md` for system overview
   - `orchestrator/README.md` for routing details

2. **Review Agent Capabilities**
   - Read agent files in `/agents/`
   - Understand what each agent can do

3. **Explore Workflows**
   - Check `/workflows/` for task templates
   - Customize for your needs

4. **Start Your First Deal**
   - Configure deal in `config.yaml`
   - Initialize knowledge base
   - Run first tasks

---

## 🎓 Learning Resources

### Understanding the System

1. **System Architecture**
   - Read: `README.md` - Overview section
   - Understand: Task-based vs. phase-based approach

2. **Agent Capabilities**
   - Review: All 8 agent definition files
   - Note: Activation triggers and capabilities

3. **Orchestrator Logic**
   - Read: `orchestrator/README.md`
   - Understand: Intent detection and routing

4. **Workflow Design**
   - Examine: Sample workflows in `/workflows/`
   - Learn: Workflow structure and customization

### Best Practices

1. **Start Simple**
   - Begin with basic tasks
   - Build understanding gradually
   - Experiment with different requests

2. **Use Natural Language**
   - Describe what you need clearly
   - Let the orchestrator handle routing
   - Provide context when helpful

3. **Leverage Context**
   - System remembers prior work
   - Reference existing outputs
   - Update iteratively

4. **Review Outputs**
   - Check generated files in `/outputs/`
   - Verify knowledge base updates
   - Track version history

---

## 🎉 Quick Start Commands

Once setup is complete, try these:

```
# Company research
"Research the company [Company Name]"

# Valuation
"Create a business valuation"
"Update the valuation with new data"

# Documents
"Create a teaser"
"Generate a CIM"
"Build a management presentation"

# Market research
"Find strategic buyers"
"Research comparable transactions"
"Analyze the industry"

# Due diligence
"Set up the data room"
"Track buyer questions"
"Identify red flags"

# Deal execution
"Compare the LOIs"
"Prepare for buyer meetings"
"What's the buyer status?"
```

---

## 📞 Support

### Documentation
- Main README: `README.md`
- Orchestrator Guide: `orchestrator/README.md`
- Output Standards: `outputs/README.md`
- Agent Definitions: `agents/*.md`

### Common Questions

**Q: Can I skip certain steps?**
A: Yes! This system is flexible. You can start with any task based on your needs.

**Q: How do I add custom workflows?**
A: Create new YAML files in `/workflows/` following existing templates.

**Q: Can I customize agents?**
A: Yes! Edit agent markdown files to adjust capabilities and triggers.

**Q: How does version control work?**
A: All outputs are automatically versioned (v1.0, v1.1, v2.0, etc.)

**Q: Can agents work in parallel?**
A: Yes! Independent tasks can run simultaneously for efficiency.

---

## ✨ You're Ready!

Your M&A agent system is now set up and ready to use.

**Next:** Read the main `README.md` and start your first deal!

**Remember:** This system is **flexible** - you can approach M&A tasks in any order that makes sense for your situation.

Good luck with your M&A advisory work! 🎯
