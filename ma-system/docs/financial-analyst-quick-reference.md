# Financial Analyst - Quick Reference Card

**Version:** 2.0 (Dialog-Based)

---

## Activation

```
/financial-analyst
```
or
```
"I need help with financial analysis"
```

---

## Main Menu (8 Options)

### 1️⃣ Analyze All Financial Documents
**When:** You've uploaded financials
**Result:** Deep extraction, inconsistency detection, structured data
**Time:** 30min - 8 hours (based on detail level)

### 2️⃣ Build/Update Valuation Model
**When:** Ready to create/update valuation
**Result:** DCF + multiples valuation with your input on assumptions
**Time:** 2-4 hours initial, 30-60min for updates

### 3️⃣ Refine Excel Model (Dialog Mode)
**When:** Model exists, want to improve it
**Sub-options:**
- Review key assumptions
- Test "what-if" scenarios
- Add new analysis
- Improve structure
- Data quality review
- Explain sections

**Result:** Better model through conversation
**Time:** 30min - 2 hours

### 4️⃣ Quality of Earnings (QoE) Analysis
**When:** Need normalized EBITDA
**Result:** EBITDA adjustments bridge, quality assessment
**Time:** 1-2 hours

### 5️⃣ Play Devil's Advocate ⭐
**When:** Before finalizing valuation or buyer meetings
**Result:** Stress-tested assumptions, downside scenarios, risk assessment
**Time:** 1-2 hours

**Challenge areas:**
- Revenue assumptions
- Cost structure
- Working capital
- WACC / discount rate
- Terminal value
- EBITDA adjustments

**Modes:**
- Light challenge (a few key assumptions)
- Full challenge (everything)
- Buyer perspective (PE, Strategic, Family Office)

### 6️⃣ Sensitivity & Scenario Analysis
**When:** Want to understand valuation range
**Options:**
- One-way sensitivity (change one variable)
- Two-way tables (change two variables)
- Scenarios (Base/Upside/Downside)
- Monte Carlo simulation

**Result:** Sensitivity tables, tornado charts, scenario comparisons
**Time:** 1-2 hours

### 7️⃣ Review & Export Final Package
**When:** Ready to deliver
**Result:** Polished final files, executive summaries, packaged deliverables
**Time:** 30 minutes

### 8️⃣ Ask Financial Questions
**When:** Anytime
**Result:** Answers + optional follow-up analysis
**Time:** Immediate

---

## Key Benefits of Dialog Mode

✅ **Transparent** - See every assumption
✅ **Collaborative** - Provide input throughout
✅ **Educational** - Learn as you go
✅ **Iterative** - Refine over time
✅ **Challenged** - Test your thinking

---

## Typical Workflow

```
1. Analyze Documents (Option 1)
   ↓
2. Build Valuation (Option 2)
   ↓
3. Refine Model (Option 3)
   ↓
4. Devil's Advocate (Option 5) ⭐
   ↓
5. Sensitivity Analysis (Option 6)
   ↓
6. Export Package (Option 7)
```

**Throughout:** Use Option 8 (Ask Questions) anytime

---

## Devil's Advocate - Example Dialog

**You:** "Build valuation"
**Agent:** [Creates model with 15% revenue growth]

**You:** "Run devil's advocate"
**Agent:** *"You're projecting 15% CAGR but industry average is 8%. What if buyers only believe 10%?"*

**You:** "We've been growing 18% historically"

**Agent:** *"Past ≠ future. Counter-arguments buyers will make:*
*1. Market maturing*
*2. Competition increasing*
*3. CAC rising*
*How would you respond in a meeting?"*

**You:** "3 new products launching"

**Agent:** *"Okay, but what if only 1 succeeds? Let me model 10% growth:*
*- Base (15%): €45M*
*- Conservative (10%): €38M (-16%)*
*Should we include as downside scenario?"*

**You:** "Yes"

**Agent:** *"Added. Now let's challenge WACC..."*

---

## Sample Questions (Option 8)

- "What's working capital as % of revenue?"
- "How do our margins compare to competitors?"
- "If we sell for €40M, what are net proceeds?"
- "What drives the biggest sensitivity in valuation?"
- "Walk me through the terminal value calculation"
- "Is our WACC reasonable?"
- "What EBITDA adjustments are risky?"

---

## Tips

### Do:
✅ Use devil's advocate before important milestones
✅ Ask "why?" frequently
✅ Push back if something doesn't feel right
✅ Test multiple scenarios
✅ Iterate - don't aim for perfection on first pass

### Don't:
❌ Skip document analysis
❌ Accept assumptions without understanding
❌ Finalize without devil's advocate review
❌ Provide single-point estimate (always use ranges)

---

## File Outputs

All saved to: `ma-system/outputs/{deal-name}/financial/`

**Valuation:** `{deal}_Valuation_Model_v{X}.xlsx`
**QoE:** `{deal}_QoE_Analysis_v{X}.xlsx`
**Sensitivities:** `{deal}_Sensitivity_Analysis_v{X}.xlsx`
**Extractions:** `{deal}_Extract_{doc-name}.json`
**Final Package:** Multiple files in `final_package/`

---

## Version Control

- **v1.0** - Initial version
- **v1.1, v1.2** - Minor updates (data refresh)
- **v2.0** - Major revision (methodology change)

---

## Knowledge Base Updates

After each session, agent updates:
- `knowledge-base/deal-insights.md` (current state)
- `knowledge-base/valuation-history.md` (assumption evolution)

---

## State Persistence

Your progress persists across sessions. Menu adapts to show:
- ✓ = Completed
- ○ = Available
- Grayed out = Prerequisites not met

---

## Getting Help

**In-agent:** Select Option 8 and ask any question
**Documentation:** See `docs/financial-analyst-dialog-guide.md` for full guide
**Test run:** `python3 ma-system/agents/financial-analyst-dialog.py`

---

## Philosophy

> "Better financial analysis through conversation, not automation"

The goal is **transparent, collaborative, iterative analysis** where you understand and control every decision.

---

**Ready?** Type `/financial-analyst` to begin!
