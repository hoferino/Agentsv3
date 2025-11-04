# 🚀 M&A Agent System - Quick Start

**Ready to use in 5 minutes!**

---

## ⚡ Installation (2 minutes)

```bash
# 1. Navigate to the system
cd ma-system

# 2. Install Python dependencies
pip install pyyaml

# 3. Test the orchestrator
cd orchestrator && python3 router.py && cd ..

# ✅ If you see routing examples, you're ready!
```

---

## 🎯 Configure Your Deal (2 minutes)

Edit `config.yaml`:

```yaml
project_config:
  deal_name: "Project Alpha"           # ← Your deal name
  target_company: "Target Company"     # ← Company name
```

Edit `knowledge-base/deal-insights.md`:

```markdown
**Deal Name:** Project Alpha
**Target Company:** Target Company
**Industry:** [Your industry]
**Revenue:** [Estimated]
```

---

## 💡 Start Working (1 minute)

Try these commands:

```
"Research the company: [Company Name]"
"Perform a business valuation"
"Create a teaser"
"Find strategic buyers"
```

The system automatically:
- ✅ Detects what you want
- ✅ Routes to the right agent
- ✅ Uses prior work as context
- ✅ Generates outputs
- ✅ Updates knowledge base

---

## 📋 8 Agents Available

| Agent | What It Does | Trigger Examples |
|-------|--------------|------------------|
| **Financial Analyst** | Valuation, models | "value the company", "create DCF" |
| **Document Generator** | CIM, teaser, presentations | "create CIM", "make a teaser" |
| **Market Intelligence** | Buyer research, market analysis | "find buyers", "industry analysis" |
| **DD Manager** | Data room, Q&A, issues | "setup data room", "track questions" |
| **Buyer Relationship** | LOI comparison, meetings | "compare LOIs", "buyer status" |
| **Legal Tax Advisor** | Structure, legal DD | "transaction structure", "tax impact" |
| **Company Intelligence** | Company research | "research the company" |
| **Managing Director** | Strategy, coordination | "overall strategy", "next steps" |

---

## 🎨 Key Features

### ✅ Use Any Order
```
Traditional: Must complete valuation → then CIM → then buyers
This System: Do any task anytime based on your needs!
```

### ✅ Update Anytime
```
"Update the valuation"         → Loads v1.0, creates v1.1
"Refresh the CIM"              → Updates existing CIM
"Add more buyers to the list"  → Expands buyer research
```

### ✅ Parallel Work
```
"Update valuation and find new buyers"
→ Both run simultaneously!
```

### ✅ Smart Context
```
System remembers:
- Prior valuations
- Existing documents
- Buyer lists
- All work history
```

---

## 📁 Where Things Are

```
ma-system/
├── config.yaml           ← Configure your deal here
├── agents/               ← 8 agent definitions (read these!)
├── knowledge-base/       ← Auto-updates with deal intelligence
│   └── deal-insights.md  ← Current deal status
├── orchestrator/         ← Routing logic (works automatically)
├── workflows/            ← Task templates
└── outputs/              ← Generated files appear here
```

---

## 💬 Example Session

```
User: "I have a new deal: TechCo, €20M revenue software company"

System: [Routes to Company Intelligence]
→ Researches TechCo
→ Updates knowledge-base/deal-insights.md
✅ "Company profile created. Next: valuation?"

User: "Yes, create a valuation"

System: [Routes to Financial Analyst]
→ Builds DCF model
→ Creates outputs/Project-Alpha/financial/valuation/TechCo_Valuation_v1.0.xlsx
✅ "Valuation complete: €15-25M range (midpoint €20M)"

User: "Create a teaser with that valuation"

System: [Routes to Document Generator]
→ Uses company profile + valuation
→ Creates outputs/Project-Alpha/documents/teasers/TechCo_Teaser_v1.0.pptx
✅ "Teaser ready for distribution"

User: "Find 10 strategic buyers"

System: [Routes to Market Intelligence]
→ Researches buyers in software sector
→ Creates buyer list
✅ "Identified 10 strategic buyers, prioritized by fit"

[All in parallel, any order, fully flexible!]
```

---

## 🎓 Learn More

- **Full Documentation:** `README.md`
- **Setup Guide:** `SETUP.md`
- **Agent Details:** `agents/*.md`
- **Project Summary:** `PROJECT_SUMMARY.md`

---

## 🆘 Quick Troubleshooting

**Issue:** "Python not found"
**Fix:** Use `python3` instead of `python`

**Issue:** "Module not found: yaml"
**Fix:** `pip install pyyaml`

**Issue:** "Agent not routing correctly"
**Fix:** Be more specific in your request

**Issue:** "Can't find output files"
**Fix:** Check `outputs/[deal-name]/` folder

---

## 🎯 First 5 Tasks to Try

1. ✅ "Research the target company"
2. ✅ "Perform a business valuation"
3. ✅ "Create a teaser"
4. ✅ "Identify 10 potential buyers"
5. ✅ "Set up the data room"

**Remember:** You can do these in ANY order!

---

## 💡 Pro Tips

### Tip 1: Be Specific
❌ "Help with this deal"
✅ "Create a valuation for this €20M software company"

### Tip 2: Update Iteratively
✅ "Update valuation with Q3 results"
✅ "Add 5 more strategic buyers"
✅ "Refresh CIM with new market data"

### Tip 3: Request Multiple Tasks
✅ "Update valuation AND find new buyers"
→ Runs in parallel!

### Tip 4: Check Knowledge Base
→ `knowledge-base/deal-insights.md` shows current status

### Tip 5: Use Natural Language
✅ Just describe what you need
✅ System handles the routing
✅ Works in English or German

---

## ✨ You're Ready!

Your M&A advisory system is set up and ready to use.

**Start with:** "Research [your target company]"

**Then:** Use any agent, any time, in any order!

---

**🎉 Welcome to flexible, intelligent M&A advisory!**
