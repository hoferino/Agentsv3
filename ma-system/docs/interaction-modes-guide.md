# Financial Analyst Interaction Modes - Complete Guide

**Version:** 2.1
**Last Updated:** 2024-11-05

---

## Overview

The Financial Analyst now supports **THREE interaction modes** to match different user preferences and use cases:

| Mode | Icon | Best For | Speed | Control |
|------|------|----------|-------|---------|
| **One-Shot** | ⚡ | Quick results, standard assumptions | Fast | Low |
| **Dialog** | 💬 | Learning, high-stakes, full control | Slower | High |
| **Hybrid** | 🔄 | Balance of speed + optional refinement | Medium | Medium-High |

**Default:** Hybrid mode (recommended for most users)

---

## The Three Modes Explained

### ⚡ One-Shot Mode

**Philosophy:** "Give me the task, I'll handle it using best practices."

**How it works:**
1. You provide a request (e.g., "Build a valuation")
2. Agent executes fully using standard assumptions
3. Agent presents complete results
4. Done - no interruptions

**Best for:**
- Quick analysis when time is limited
- When you trust the agent's judgment
- Initial drafts you'll refine later
- Standard/straightforward cases

**Example interaction:**
```
You: "Analyze these documents and build a valuation"

Agent: "Analyzing 15 documents using standard workflow...
        [Executes silently]

        Analysis complete. Valuation: €42M (range €38M-€48M)

        Files created:
        - Valuation_Model_v1.0.xlsx
        - QoE_Analysis_v1.0.xlsx
        - Assumptions_Memo_v1.0.pdf

        Knowledge base updated."
```

**When NOT to use:**
- High-stakes valuations requiring careful consideration
- When you want to learn the process
- When assumptions need debate
- Complex situations requiring judgment calls

---

### 💬 Dialog Mode

**Philosophy:** "Let's work through this together, step by step."

**How it works:**
1. Agent presents menu of options
2. You select what to do
3. Agent asks questions for every major decision
4. Interactive back-and-forth until complete
5. You control every assumption

**Best for:**
- When you want full control over assumptions
- Learning financial analysis
- High-stakes valuations (>€10M deals)
- When you need to justify every decision
- Complex or unusual situations

**Example interaction:**
```
You: "Build a valuation"

Agent: [Shows 8-option menu]
        "Please select: 2. Build/Update Valuation Model"

You: "2"

Agent: "Let's build the valuation together.

        What methodologies would you like?
        1. DCF only
        2. Multiples only
        3. Both (recommended)

        Choose (1-3):"

You: "3"

Agent: "Great. Do you have management projections?
        - Yes, I have projections
        - No, build bottoms-up"

You: "No"

Agent: "I'll build projections based on historicals.

        Looking at 3-year revenue history:
        2021: €3.2M
        2022: €4.1M (+28%)
        2023: €5.0M (+22%)

        What revenue CAGR feels right for next 5 years?
        - 15% (conservative vs. historical)
        - 20% (in line with recent)
        - 25% (aggressive)
        - Custom rate"

[Dialog continues for every assumption...]
```

**When NOT to use:**
- When time is limited
- Straightforward, standard cases
- When you trust the agent's judgment
- Routine updates to existing models

---

### 🔄 Hybrid Mode (RECOMMENDED)

**Philosophy:** "Fast initial results, then optional refinement."

**How it works:**
1. Agent executes one-shot analysis first
2. Agent presents complete results
3. Agent offers menu of refinement options
4. You choose: accept as-is OR refine specific areas
5. Best of both worlds

**Best for:**
- Most use cases (versatile)
- When you want speed but reserve right to refine
- Iterative improvement approach
- Building confidence in results

**Example interaction:**
```
You: "Build a valuation"

Agent: "Building valuation using DCF + multiples...
        [Executes standard workflow]

        **Valuation Complete**

        Enterprise Value: €42M (range: €38M - €48M)

        Key Assumptions:
        - Revenue CAGR: 15%
        - EBITDA margin: 20% steady
        - WACC: 12.5%
        - Terminal growth: 2.5%

        Methodologies:
        - DCF: €43M
        - Trading multiples: €41M
        - Transaction multiples: €42M

        Files: Valuation_Model_v1.0.xlsx

        ─────────────────────────────

        Want to refine this? I can:

        1. Review/change key assumptions
        2. Run devil's advocate (challenge everything)
        3. Add sensitivity analysis
        4. Deep-dive on specific areas
        5. Export final package as-is
        6. No thanks, we're done

        What would you like? (1-6)"

You: "2" [Run devil's advocate]

Agent: [Enters interactive challenge mode]
        "Let's stress-test this valuation.

        Challenge #1: Revenue Growth
        You're assuming 15% CAGR, but industry average is 8%.
        What if buyers only believe 10% growth?

        How would you respond?"

[Interactive refinement continues...]
```

**When NOT to use:**
- When you definitely want dialog from the start
- When you want absolute fastest results (use one-shot)

---

## Choosing Your Mode

### On First Use

When you first activate the Financial Analyst, you'll see:

```
# Financial Analyst - Choose Your Workflow

How would you like to work with the Financial Analyst?
You can change this anytime.

1. ⚡ One-Shot Mode
   Give me a task, I'll complete it fully and present results

   Best for:
   - Quick analysis when you trust standard assumptions
   - When you have limited time
   - Initial draft that you'll refine later

   Example:
   You: 'Analyze documents and build valuation'
   Me: [Completes everything, presents final model]

   ────────────────────────────────────────────────────

2. 💬 Dialog Mode
   Interactive menu-driven workflow with your input at every step

   Best for:
   - When you want to understand and control assumptions
   - Learning financial analysis
   - High-stakes valuations requiring careful thought

   Example:
   You: 'Build valuation'
   Me: 'What methodologies? Do you have projections? ...'

   ────────────────────────────────────────────────────

3. 🔄 Hybrid Mode [RECOMMENDED]
   I'll do one-shot analysis, then offer dialog options to refine

   Best for:
   - Balance of speed and control
   - Get initial results fast, then iterate
   - Most versatile approach

   Example:
   You: 'Build valuation'
   Me: [Creates v1.0] 'Done! Want to refine / challenge / add sensitivity?'

   ────────────────────────────────────────────────────

Which mode would you like to use? (1-3)
```

**Recommendation:** Start with Hybrid mode. You can always switch later.

---

## Switching Modes

You can switch modes **anytime** in three ways:

### Method 1: From Main Menu

```
[Main Menu shows:]
9. **Change Mode (Current: hybrid)** ○
   Switch between one-shot, dialog, or hybrid mode
   Status: Settings

You: "9"

Agent: [Shows mode selection interface again]
```

### Method 2: Natural Language

```
You: "Switch to one-shot mode"
Agent: "Switched from hybrid to one_shot mode.
        Preference saved. Future interactions will use one-shot mode."

You: "Let's switch to dialog mode"
Agent: "Switched to dialog mode. You'll now see interactive menus."

You: "Change to hybrid"
Agent: "Now in hybrid mode."
```

### Method 3: Explicit Request

```
You: "I want to change modes"
Agent: [Shows mode selection interface]
```

**Note:** Your preference is saved to `knowledge-base/user-preferences.yaml` and persists across sessions.

---

## Mode Detection

The agent can **detect your preferred mode** from your language:

### One-Shot Indicators
- "quickly"
- "just analyze"
- "give me results"
- "standard analysis"
- "don't ask me, just do it"

```
You: "Just analyze these docs quickly and give me a valuation"
Agent: [Detects one-shot intent, executes fully]
```

### Dialog Indicators
- "let's work through"
- "help me understand"
- "walk me through"
- "I want to discuss"
- "explain as you go"

```
You: "Let's work through the valuation together"
Agent: [Detects dialog intent, shows menu]
```

### Hybrid Indicators
- "create initial then refine"
- "draft then improve"
- "quick version first"

```
You: "Create an initial valuation, then we'll refine it"
Agent: [Detects hybrid intent, executes then offers options]
```

**If unclear:** Agent will show mode selection interface.

---

## How Mode Affects Behavior

### Document Analysis

**Same request:** "Analyze these 50 financial documents"

**One-Shot Response:**
```
Analyzing 50 documents using large-scale Phase 1-5 workflow...

Phase 1: Document categorization complete (50 files)
Phase 2: Parallel extraction (50 agents) in progress...
Phase 3: Consolidation complete, 12 inconsistencies found
Phase 4: Deep analysis complete
Phase 5: Financial models created

Results:
- 50 extraction JSONs created
- Consolidated dataset: 5 years historical data
- Inconsistency report: 12 conflicts (8 high priority)
- Ready for valuation

Files: outputs/Deal/financial/extractions/
```

**Dialog Response:**
```
I see 50 documents. This requires large-scale processing.

Step 1: Document Scope
How should I handle 50 documents?
1. Standard analysis (may miss nuances)
2. Large-scale batched processing (Phase 1-5 workflow)
3. Enterprise parallel extraction (1 doc per agent)

Choose (1-3):
```

**Hybrid Response:**
```
Analyzing 50 documents using large-scale workflow...
[Executes standard Phase 1-5]

Analysis complete. 12 inconsistencies found.

Want to:
1. Review inconsistencies in detail
2. Re-process specific documents with higher detail
3. Accept analysis as-is
4. Generate reconciliation report

Choose (1-4) or we're done:
```

---

### Valuation Creation

**Same request:** "Value this company"

**One-Shot Response:**
```
Building valuation (DCF + multiples)...

Enterprise Value: €42M (range: €38M-€48M)

Assumptions:
- Revenue CAGR: 15% (3-yr historical avg: 18%)
- EBITDA margin: 20% steady (historical: 18%-22%)
- WACC: 12.5% (risk-free 3.5% + equity premium 6% × beta 1.2)
- Terminal growth: 2.5% (GDP + inflation)
- Exit multiple: 8x EBITDA (industry median)

Methodologies:
- DCF: €43M
- Trading comps: €41M  (7.5x EBITDA)
- Transaction comps: €42M (8.2x EBITDA)

Files: Valuation_Model_v1.0.xlsx

Done.
```

**Dialog Response:**
```
Let's build the valuation together.

Question 1: Methodologies
What should I use?
1. DCF only
2. Multiples only (comps)
3. Both DCF and multiples (recommended)

Choose (1-3):

[User responds, dialog continues for each decision]
```

**Hybrid Response:**
```
[One-shot response above, THEN:]

────────────────────────────

Valuation v1.0 complete.

Optional refinements:
1. Review/adjust assumptions
2. Devil's advocate (stress test)
3. Sensitivity analysis
4. Export package

Choose option (1-4) or done:
```

---

## Best Practices

### When to Use Each Mode

| Situation | Recommended Mode | Why |
|-----------|------------------|-----|
| First-time user | **Hybrid** | Learn without slowness |
| Routine valuation update | **One-Shot** | Quick, no decisions needed |
| Large M&A deal (€50M+) | **Dialog** | Every assumption matters |
| Learning financial modeling | **Dialog** | Educational |
| Time pressure (deadline) | **One-Shot** | Fast results |
| Uncertain about assumptions | **Hybrid** | Quick start, refine later |
| Multiple iterations expected | **Hybrid** | Iterate efficiently |
| Handing off to client | **One-Shot** | Clean deliverable |
| Preparing for buyer meeting | **Hybrid or Dialog** | Stress-test assumptions |

### Pro Tips

1. **Start Hybrid:** Most versatile, adjust later if needed

2. **Use One-Shot for Updates:**
   ```
   "Update valuation with Q3 results" [one-shot mode]
   → Fast update, same methodology
   ```

3. **Use Dialog for New Complex Deals:**
   ```
   First valuation of unusual business model [dialog mode]
   → Discuss every assumption
   ```

4. **Switch Mid-Session:**
   ```
   Start one-shot → Get results → Switch to dialog → Refine
   ```

5. **Devil's Advocate Works in All Modes:**
   - One-shot: Agent challenges silently, presents risks
   - Dialog: Interactive challenge session
   - Hybrid: One-shot challenges, then option for dialog

---

## Technical Details

### Preference Persistence

Your mode preference is saved in:
```
ma-system/knowledge-base/user-preferences.yaml
```

```yaml
# User Preferences
financial_analyst_mode: hybrid  # one_shot | dialog | hybrid
language: en
last_updated: 2024-11-05T14:30:00Z
```

**Behavior:**
- First time: No preference, shows selection
- Subsequent times: Uses saved preference
- Override anytime: "Switch to [mode]" or "Change mode"

### Mode in Main Menu

The main menu always shows current mode:

```
# Financial Analyst - Main Menu
**Deal: Project Munich**

**Mode:** 🔄 Hybrid

What would you like to do?
[...]
9. **Change Mode (Current: hybrid)** ○
```

---

## FAQ

**Q: Can I use dialog mode for just one task, then switch back?**

A: Yes. Switch modes anytime. Your last selection becomes the new default.

**Q: If I choose one-shot, can I still refine after?**

A: In pure one-shot mode, you get final results. But you can then switch to dialog mode and select "Refine Excel Model" from the menu.

**Q: What's the default if I don't choose?**

A: Hybrid mode (best balance for most users).

**Q: Does mode affect quality?**

A: No. All modes use the same underlying analysis. Mode only affects **interaction style**.

**Q: Can I have different modes for different tasks?**

A: Your preference applies to the Financial Analyst overall. But you can switch modes between tasks:
```
Task 1: [Set to one-shot] "Analyze docs"
Task 2: [Switch to dialog] "Build valuation"
Task 3: [Switch to one-shot] "Update model"
```

**Q: What if I'm working with someone else?**

A: Preference is per-machine, not per-user. If sharing, use "Change mode" at start of each session.

**Q: Is there a "mixed" mode beyond hybrid?**

A: Hybrid IS the mixed mode. It gives one-shot speed with dialog refinement options.

---

## Examples: Same Task, Three Modes

### Task: "Build a valuation for a SaaS company"

#### ⚡ One-Shot Mode

```
You: "Build a valuation for a SaaS company"

Agent: "Building SaaS valuation using DCF + multiples...

[Executes silently with SaaS-specific assumptions]

Enterprise Value: €28M (range: €24M-€33M)

SaaS-Specific Assumptions:
- ARR growth: 40% Y1, declining to 20% Y5
- Churn: 8% annually (improving to 5%)
- CAC payback: 14 months
- LTV/CAC: 4.2x
- Rule of 40: 52% (healthy)
- WACC: 14% (higher for SaaS)

Valuation based on:
- DCF: €29M
- ARR multiples: €27M (6.5x ARR)
- SaaS transaction comps: €28M

Files: SaaS_Valuation_v1.0.xlsx

Complete."
```

#### 💬 Dialog Mode

```
You: "Build a valuation for a SaaS company"

Agent: "Let's value this SaaS company together.

SaaS companies require specific metrics. Let me ask:

1. What's the current ARR (Annual Recurring Revenue)?
   (This is more important than total revenue for SaaS)

[You respond: €4.2M]

2. What's the ARR growth rate?
   - Last year?
   - Expected next 3 years?

[You respond: 45% last year, expect 40%/35%/30%]

3. What's the churn rate?
   - Monthly or annual?
   - Improving, stable, or worsening?

[You respond: 8% annual, stable]

4. What's the CAC (Customer Acquisition Cost)?
   - And LTV (Lifetime Value)?
   - Or should I calculate from data?

[Dialog continues for every SaaS-specific metric...]

5. For WACC, SaaS companies typically use 12-16%.
   Given your growth (40%+) and churn (8%), I'd suggest 14%.
   Does that feel right?

[You respond: yes]

6. Valuation methodology for SaaS:
   - DCF with ARR-based projections
   - ARR multiples (typically 4-8x)
   - Both?

[You respond: both]

Building model now with your inputs...

[Creates valuation]

Valuation: €28M

Does this feel reasonable given ARR of €4.2M (6.7x multiple)?

Want to adjust any assumptions?"
```

#### 🔄 Hybrid Mode

```
You: "Build a valuation for a SaaS company"

Agent: "Building SaaS valuation with industry-standard assumptions...

[Executes one-shot with SaaS focus]

**SaaS Valuation Complete**

Enterprise Value: €28M (range: €24M-€33M)

Key SaaS Metrics:
- ARR: €4.2M (growing 40% YoY)
- Churn: 8% annual
- CAC Payback: 14 months
- LTV/CAC: 4.2x
- Rule of 40: 52% ✓ healthy

Valuation: 6.7x ARR multiple (industry: 4-8x)

Files: SaaS_Valuation_v1.0.xlsx

────────────────────────────

This is a solid starting point. Optional refinements:

1. **Adjust ARR growth assumptions**
   (Currently using 40%/35%/30% declining)

2. **Model churn improvements**
   (Currently flat 8%)

3. **Add cohort analysis**
   (Revenue retention by vintage)

4. **Sensitivity on ARR multiple**
   (Test 5x, 6x, 7x, 8x scenarios)

5. **Devil's advocate on SaaS metrics**
   (Challenge: Is 8% churn sustainable? Is 40% growth achievable?)

6. **Accept as-is and export**

Choose (1-6) or we're done:
```

---

## Summary

| Feature | One-Shot ⚡ | Dialog 💬 | Hybrid 🔄 |
|---------|-----------|----------|---------|
| Speed | Fastest | Slowest | Fast |
| Control | Low | Highest | Medium-High |
| Learning | Minimal | Maximum | Good |
| Best for | Routine tasks | Complex/learning | Most cases |
| Interaction | Execute & present | Continuous dialog | Execute → optional dialog |
| Refinement | Manual (switch modes) | Built-in | Built-in |
| Stress-testing | Summary only | Interactive | Optional interactive |

**Recommendation: Start with Hybrid mode.** It gives you speed when you need it, and control when you want it.

---

**Ready to start?** Type `/financial-analyst` and choose your mode!
