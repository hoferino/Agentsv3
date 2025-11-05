# Dialog Mode Pattern

## Purpose
Reusable interaction pattern for complex, high-stakes agent tasks that benefit from user involvement. Provides three modes of interaction to balance speed with control.

## When to Use
Apply this pattern to agents where:
- Tasks are complex with multiple decision points
- High stakes (e.g., valuation, negotiation strategy, legal structure)
- User may want to learn the process
- Customization is important
- Standard assumptions may not fit

## Applicable Agents
- **Financial Analyst** ✅ (Already implemented)
- **DD Manager** - Data room setup has many decisions
- **Document Generator** - CIM creation involves content choices
- **Buyer Relationship Manager** - Negotiation strategy requires user input
- **Legal & Tax Advisor** - Deal structure has many options

---

## Three Interaction Modes

### Mode 1: One-Shot (⚡)
**Description:** Agent completes entire task without interruption

**Best for:**
- Quick tasks
- User trusts standard assumptions
- Time-sensitive deliverables
- Repeat tasks where preferences are known

**User Experience:**
```
User: "Build a valuation model"
Agent: [Completes full analysis]
Agent: "Valuation complete. Range: €24-28M (Base: €26M).
        Model saved as Project-Munich_Valuation_Model_v1.0.xlsx"
```

**Characteristics:**
- Fastest completion
- Uses agent's default assumptions
- Documents all choices for transparency
- User receives completed deliverable

---

### Mode 2: Dialog Mode (💬)
**Description:** Interactive Q&A at every major decision point

**Best for:**
- Learning how the process works
- High-stakes decisions requiring careful consideration
- First-time tasks where user wants control
- Non-standard situations

**User Experience:**
```
User: "Build a valuation model in dialog mode"

Agent: "I'll guide you through the valuation step-by-step.

Step 1: EBITDA Normalization
I found these potential adjustments:
1. Owner salary (€300K, market rate €150K) → Adjustment: +€150K
2. One-time consulting fees (€80K) → Adjustment: +€80K
3. Legal dispute settlement (€50K) → Adjustment: +€50K

Which adjustments should I include?
A) All three (+€280K total)
B) Only #1 and #2 (+€230K)
C) Let me customize"

User: "B"

Agent: "Great. Normalized EBITDA = €8.2M.

Step 2: DCF Assumptions
Revenue growth for projections?"
[... continues with questions]
```

**Characteristics:**
- Most control for user
- Educational - user sees reasoning
- Slower but more thorough
- Best for understanding trade-offs

---

### Mode 3: Hybrid Mode (🔄) - RECOMMENDED
**Description:** Agent completes one-shot analysis first, then offers refinement options

**Best for:**
- Most tasks (best balance of speed and control)
- When user wants speed but may want tweaks
- Building on agent's work efficiently
- Iterative improvement

**User Experience:**
```
User: "Create a valuation"

Agent: [Performs complete analysis]

Agent: "Valuation complete. Here are the results:

Enterprise Value Range: €24M - €28M (Base: €26M)
Key Assumptions:
- Normalized EBITDA: €8M (adjusted for owner salary and one-time items)
- Revenue growth: 15% (based on 3-year average)
- WACC: 10% (based on industry benchmarks)
- Terminal growth: 2.5%

Model saved as Project-Munich_Valuation_Model_v1.0.xlsx

Would you like to refine any assumptions?
1. Adjust EBITDA normalization
2. Change growth assumptions
3. Modify WACC calculation
4. Add sensitivity analysis
5. Looks good, no changes needed"

User: "2"

Agent: "Current revenue growth assumption: 15%
Based on:
- Year 1-2: 18% growth
- Year 2-3: 12% growth
- 3-year average: 15%

What growth rate would you like?
A) 18% (optimistic, based on recent momentum)
B) 12% (conservative, accounts for market maturity)
C) Custom rate"
```

**Characteristics:**
- Fast initial result
- User can refine if needed
- Agent does heavy lifting
- Iterative improvement without starting over

---

## Implementation Pattern

### 1. Mode Detection
Agent must detect preferred mode from:

#### A. User Preferences (Persistent)
Check `knowledge-base/user-preferences.yaml`:
```yaml
interaction_modes:
  financial_analyst: "hybrid"
  dd_manager: "one-shot"
  document_generator: "dialog"
```

#### B. User Request (Explicit)
Keywords in user input:
- **One-shot**: "quick", "fast", "just do it", "one-shot"
- **Dialog**: "walk me through", "dialog mode", "interactive", "step by step"
- **Hybrid**: "create and let me refine", "hybrid", "build first"

#### C. Task Complexity (Heuristic)
If no preference specified:
- **Simple update**: Default to one-shot
- **First-time task**: Suggest dialog or hybrid
- **High stakes**: Suggest dialog or hybrid

### 2. Mode Execution

#### One-Shot Implementation
```yaml
steps:
  1_complete_analysis:
    - Use agent's best judgment on all decisions
    - Document all assumptions made
    - Proceed without user interruption

  2_deliver_results:
    - Present final deliverable
    - Include assumption summary
    - Note: "I made these assumptions: [list]"
    - Offer: "Would you like to adjust anything?"
```

#### Dialog Implementation
```yaml
steps:
  1_break_into_steps:
    - Identify all major decision points
    - Create menu for each decision

  2_present_options:
    - Show 2-4 options for each decision
    - Explain trade-offs
    - Wait for user choice

  3_execute_choice:
    - Implement user's selection
    - Confirm and move to next step

  4_iterate:
    - Repeat for all steps
    - Allow backtracking if needed
```

#### Hybrid Implementation
```yaml
steps:
  1_complete_analysis:
    - Same as one-shot
    - Complete full task

  2_present_results_with_menu:
    - Show final deliverable
    - Display refinement menu
    - List key assumptions with options to modify

  3_wait_for_user:
    - If user satisfied: Done
    - If user wants refinement: Enter interactive refinement

  4_refinement_loop:
    - User selects what to refine
    - Agent shows options for that area
    - Agent updates and shows new results
    - Return to refinement menu
```

### 3. Mode Persistence
After first interaction, save preference:

Update `knowledge-base/user-preferences.yaml`:
```yaml
interaction_modes:
  financial_analyst: "hybrid"  # User's choice
  last_updated: "2024-03-15"

# Optional: Track per-task preferences
financial_analyst_preferences:
  valuation: "hybrid"
  qoe_analysis: "one-shot"
  sensitivity_analysis: "dialog"
```

### 4. Mode Switching
Always offer ability to change modes:

**In Menu (for agents with menus):**
```
Financial Analyst Main Menu:
1. Analyze Financial Documents
2. Build Valuation Model
3. QoE Analysis
...
9. Change Interaction Mode (Current: Hybrid 🔄)

Select option: 9

Available Modes:
⚡ One-Shot - Fast, automated completion
💬 Dialog - Interactive, step-by-step guidance
🔄 Hybrid - Quick result, then refine (RECOMMENDED)

Your choice:
```

**Mid-Task:**
```
Agent: "Working on DCF model..."

User: "Switch to dialog mode"

Agent: "Switching to dialog mode. Let me ask you about the assumptions..."
```

---

## User Communication Pattern

### Mode Indication
Always show current mode:
```
Agent: "Starting valuation in Hybrid Mode 🔄"
Agent: "Running QoE analysis in One-Shot Mode ⚡"
Agent: "Beginning data room setup in Dialog Mode 💬"
```

### Mode Explanation (First Time)
When user encounters dialog mode for first time:
```
Agent: "I can work in three modes:

⚡ ONE-SHOT: I complete the task fully and deliver results (fastest)
💬 DIALOG: I ask for your input at each step (most control)
🔄 HYBRID: I complete the task, then let you refine (RECOMMENDED)

Which would you prefer?
[If unsure, Hybrid is a great starting point]"
```

### Progress Indication
In dialog mode, show progress:
```
Agent: "Valuation Progress: [▓▓▓░░] Step 3 of 5"
Agent: "CIM Creation Progress: [▓▓▓▓▓▓░░] Section 6 of 8"
```

---

## Refinement Menu Pattern (Hybrid Mode)

### Menu Structure
```
{Task} Complete!

Results Summary:
[Key metrics / outcomes]

Refinement Options:
1. {Major area 1} - {Current setting}
2. {Major area 2} - {Current setting}
3. {Major area 3} - {Current setting}
4. Add {additional analysis type}
5. Review detailed {output type}
6. Looks good, no changes needed

Select option (or ask a question):
```

### Example: Financial Analyst Refinement Menu
```
Valuation Complete!

Enterprise Value: €24M - €28M (Base: €26M)
Methodology: DCF (40%), Trading Comps (30%), Transaction Comps (30%)

Refinement Options:
1. EBITDA Normalization - Currently: €8M with 3 adjustments
2. Growth Assumptions - Currently: 15% revenue growth
3. WACC Calculation - Currently: 10.0%
4. Add Scenario Analysis (Best / Worst case)
5. Add More Comparable Companies (Currently: 5 comps)
6. Review Detailed Sensitivity Tables
7. Looks good, no changes needed

Select option:
```

---

## Implementation Checklist

To add dialog mode to an agent:

### Step 1: Add Mode Detection
- [ ] Create `{agent-name}-dialog.py` script (if complex logic needed)
- [ ] Add mode detection from user-preferences.yaml
- [ ] Add keyword detection in user input
- [ ] Default mode selection based on task complexity

### Step 2: Update Agent Markdown
- [ ] Document three modes in agent file
- [ ] Add mode triggers to agent description
- [ ] Explain when each mode is best

### Step 3: Implement Mode Execution
- [ ] One-shot: Straight-through execution
- [ ] Dialog: Break task into steps with menus
- [ ] Hybrid: Execute + refinement menu

### Step 4: Add Mode Switching
- [ ] Include "Change Mode" option in menus (if agent has menu)
- [ ] Allow mid-task mode switching
- [ ] Save mode preference after use

### Step 5: Update Knowledge Base Structure
- [ ] Add user-preferences.yaml section for this agent
- [ ] Document mode preferences
- [ ] Track mode usage over time

---

## Benefits

1. **Flexibility** - Users choose their preferred interaction style
2. **Learning** - Dialog mode helps users understand the process
3. **Speed** - One-shot delivers fast results
4. **Balance** - Hybrid offers best of both worlds
5. **Consistency** - Same pattern across multiple agents
6. **Personalization** - Remembers user preferences

---

## Anti-Patterns to Avoid

❌ **Don't**: Ask questions in one-shot mode
✅ **Do**: Complete task fully, then offer refinements

❌ **Don't**: Make dialog mode too granular (decision fatigue)
✅ **Do**: Focus on major decisions only (3-7 steps max)

❌ **Don't**: Force a mode on the user
✅ **Do**: Suggest recommended mode but allow choice

❌ **Don't**: Forget to save mode preferences
✅ **Do**: Remember for future interactions

❌ **Don't**: Use dialog mode for simple tasks
✅ **Do**: Reserve dialog for complex, high-stakes work

---

## Code Example: Mode Detection

```python
# financial-analyst-dialog.py
def detect_mode(user_input, user_preferences, task_type):
    """Detect which interaction mode to use"""

    # 1. Check explicit keywords
    if any(kw in user_input.lower() for kw in ['dialog', 'interactive', 'step by step', 'walk me through']):
        return 'dialog'
    if any(kw in user_input.lower() for kw in ['quick', 'fast', 'one-shot', 'just do it']):
        return 'one-shot'
    if any(kw in user_input.lower() for kw in ['hybrid', 'then refine', 'build first']):
        return 'hybrid'

    # 2. Check user preferences
    if 'financial_analyst' in user_preferences.get('interaction_modes', {}):
        return user_preferences['interaction_modes']['financial_analyst']

    # 3. Check task-specific preferences
    if task_type in user_preferences.get('financial_analyst_preferences', {}):
        return user_preferences['financial_analyst_preferences'][task_type]

    # 4. Default based on task complexity
    if task_type in ['valuation', 'financial_model']:
        return 'hybrid'  # Complex tasks default to hybrid
    else:
        return 'one-shot'  # Simple tasks default to one-shot
```

---

## Success Metrics

Track effectiveness:
- **Mode usage**: Which modes are used most?
- **Mode switching**: Do users change modes mid-task?
- **Task completion**: Does mode affect completion rate?
- **User satisfaction**: Do users understand the options?
- **Efficiency**: Does hybrid save time vs pure dialog?
