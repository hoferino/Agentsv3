# Context Management Strategy - Financial Analyst Agent

**Goal:** Enable long-running conversations without context overflow, transparently to the user.

---

## Problem Statement

Current implementation uses **81% of 200k context** in a single analysis session. This leaves insufficient room for:
- Extended discussions
- Multiple iterations
- Deep dives into specific topics
- Follow-up analyses

---

## Solution Architecture

### 1. Extract-Once Pattern (Quick Win: ~15k tokens saved)

**Implementation:**

```python
# In financial-analyst workflow initialization
def ensure_data_extracted():
    """
    Extract financial data once, persist to compact JSON.
    Never reload raw Excel files after initial extraction.
    """
    summary_file = f"{sandbox}/financial_summary.json"

    if os.path.exists(summary_file):
        return load_json(summary_file)

    # Extract from raw data room files
    raw_data = extract_from_excel(dataroom_path)

    # Create compact summary (only essentials)
    summary = {
        'revenue': extract_revenue_by_year(raw_data),
        'ebitda': extract_ebitda_by_year(raw_data),
        'working_capital': extract_wc_essentials(raw_data),
        'metadata': {
            'extracted_at': timestamp(),
            'source_files': list_source_files()
        }
    }

    save_json(summary_file, summary)

    # CRITICAL: Return only confirmation, not full data
    return {
        'status': 'extracted',
        'file': summary_file,
        'size': get_file_size(summary_file)
    }
```

**Result:**
- Raw Excel read: 1x only
- Subsequent operations: Load compact JSON (~500 lines vs. 12,000 cells)
- Context savings: ~15k tokens

---

### 2. Compact Output Format (Quick Win: ~12k tokens saved)

**Current (Verbose):**
```
=== COMPREHENSIVE FINANCIAL EXTRACTION ===

Total Revenue:
  2020: €12,462,910.90
  2021: €16,663,771.45
  2022: €22,591,934.94
  2023 H1: €11,203,754.13

Total Gross profit:
  2020: €10,759,502.18
  [... 50 more lines ...]
```

**Optimized (Compact):**
```
✓ Financial extraction complete

Key metrics (2020-2023):
  Revenue: €12.5M → €22.6M (81% growth)
  EBITDA: €0.6M → €3.3M (450% growth)
  Margin: 4.6% → 14.5%

📄 Full data: /sandbox/financial_summary.json
```

**Implementation Rule:**
- Default: Summary only (3-5 lines)
- User can request: `show details` → Then show full table
- Tables in conversation: Max 10 rows, rest in file with reference

**Context savings:** ~12k tokens per major output

---

### 3. Sequential Dialog with Smart Defaults (Medium: ~5k tokens saved)

**Current:** Ask all questions upfront
```
Q1: Is margin sustainable?
Q2: Revenue plateau reasons?
Q3: Normalization adjustments?
Q4: Working capital typical?
[... 10 questions ...]
```

**Optimized:** Ask only critical questions, use smart defaults
```
Q1: Is the 14.5% EBITDA margin sustainable? [Yes/No/Discuss]
  → If "Yes": Skip Q2-Q5 about margin drivers
  → If "No": Deep dive into margin questions

Q2: Revenue CAGR projection [16% suggested based on history]
  → If accepted: Skip detailed revenue discussion
  → If challenged: Sequential follow-ups
```

**Implementation:**
- Identify 3-5 critical decision points
- Provide smart defaults based on data
- Only drill down if user challenges assumption
- Early exit when consensus reached

**Context savings:** ~5k tokens (fewer back-and-forth turns)

---

### 4. Automatic Session Management (Critical: Transparent to User)

**Goal:** Agent automatically manages context without user intervention or data loss.

#### Architecture:

```
Session 1: Data Extraction & Initial Analysis
├─ Extract data from data room → Save to /sandbox/state/
├─ Initial financial analysis
├─ User Q&A about historicals
└─ Context usage: 45k tokens
    └─ AUTO-CHECKPOINT: Save state before threshold

Session 2: Valuation Build (Auto-Started)
├─ Load state from Session 1 (compact format)
├─ Build DCF model
├─ User iterations on assumptions
└─ Context usage: 40k tokens
    └─ AUTO-CHECKPOINT: Save state

Session 3: Export & Refinements (Auto-Started)
├─ Load state from Session 2
├─ Excel export
├─ Sensitivity analysis
└─ Context usage: 25k tokens
```

#### Implementation Details:

**A) State Persistence Format**

```json
{
  "session_id": "fa-2024-11-05-001",
  "deal_name": "Project Munich",
  "checkpoint_at": "2024-11-05T14:30:00Z",

  "state": {
    "phase": "valuation_complete",
    "decisions_made": {
      "margin_sustainable": true,
      "revenue_cagr": "16%",
      "wacc": "12.5%",
      "normalization_adjustments": "none"
    },

    "data_files": {
      "financial_summary": "/sandbox/financial_summary.json",
      "qoe_analysis": "/sandbox/qoe_analysis.json",
      "valuation_model": "/sandbox/valuation_final.json"
    },

    "context_summary": {
      "historical_performance": "Strong growth: 34% CAGR 2020-2022, EBITDA margin expanded from 4.6% to 14.5%",
      "key_findings": ["Clean QoE", "Strong cash position €4.95M", "Low CapEx model"],
      "valuation_result": "EV €29.8M (range €26.0M-€32.5M)"
    }
  },

  "next_steps": [
    "Sensitivity analysis",
    "CIM creation",
    "Buyer identification"
  ]
}
```

**B) Auto-Checkpoint Triggers**

```python
def should_checkpoint():
    """
    Automatically checkpoint when context usage reaches threshold.
    No user interaction required.
    """
    context_usage = get_context_usage()

    # Checkpoint at 60% usage (120k of 200k)
    if context_usage > 0.60:
        return True

    # Or after major workflow completion
    if workflow_phase_complete():
        return True

    return False

def auto_checkpoint():
    """
    Transparently save state and prepare for continuation.
    User sees: "✓ Progress saved - continuing..."
    """
    state = {
        'session_id': generate_session_id(),
        'deal_name': get_deal_name(),
        'checkpoint_at': now(),
        'state': extract_current_state(),
        'data_files': list_data_files(),
        'context_summary': generate_summary(),
        'next_steps': identify_next_steps()
    }

    save_json(f"{sandbox}/state/checkpoint_{state['session_id']}.json", state)

    return f"✓ Progress saved (Session {state['session_id'][-3:]})"
```

**C) Auto-Resume on Next Interaction**

```python
def on_agent_activation():
    """
    Check for existing session state on activation.
    Automatically resume if found.
    """
    latest_checkpoint = find_latest_checkpoint(deal_name)

    if latest_checkpoint:
        state = load_json(latest_checkpoint)

        # Reconstruct context from compact state
        context = f"""
Session continuation (#{state['session_id'][-3:]})

Previous work completed:
- Phase: {state['state']['phase']}
- Key decisions: {format_decisions(state['state']['decisions_made'])}
- Result: {state['state']['context_summary']['valuation_result']}

Data files available:
{format_file_list(state['state']['data_files'])}

Next steps: {format_steps(state['next_steps'])}

Ready to continue. What would you like to do next?
"""

        return context  # ~500 tokens vs. 15k for full history

    else:
        # Fresh start
        return initialize_new_session()
```

**D) User Experience**

**Scenario: Long session reaches 120k context**

```
User: "Now create a sensitivity analysis"

Agent: [Internally detects 122k context usage]
       [Triggers auto-checkpoint]

       ✓ Progress saved

       Building sensitivity analysis...
       [Continues seamlessly in same conversation]
       [Behind the scenes: New session started with compact state]
```

**User sees:** Normal continuation
**System does:** State saved, context compacted, resumed transparently

---

### 5. File Reference Strategy (Complement to #2)

**Principle:** Large data lives in files, conversation references files.

**Implementation:**

```python
# Instead of outputting full table
print("""
Revenue Projections (2024-2028):
  2024: €26.0M
  2025: €30.2M
  [... 3 more years ...]

  Full projection details: /sandbox/revenue_projections.json
""")

# User can request details
if user_asks_for_details():
    load_and_display_file('revenue_projections.json')
```

**Context savings:** ~3k tokens per large dataset reference

---

## Implementation Priority

### Phase 1: Quick Wins (This Week)
1. ✅ Extract-Once Pattern (~15k saved)
2. ✅ Compact Output Format (~12k saved)
3. ✅ File Reference Strategy (~3k saved)

**Expected result:** 45k → 70k token usage (35% improvement)

### Phase 2: Dialog Optimization (Next Week)
4. ✅ Sequential Dialog with Smart Defaults (~5k saved)
5. ✅ Remove redundant file reads (~8k saved)

**Expected result:** 45k → 60k token usage (48% improvement)

### Phase 3: Auto Session Management (Week 3)
6. ✅ State Persistence Format
7. ✅ Auto-Checkpoint System
8. ✅ Auto-Resume Logic
9. ✅ Transparent Session Switching

**Expected result:** Unlimited conversation length, transparent to user

---

## Success Metrics

**Target:** Same analysis uses ≤50k tokens (vs. current 95k)

**Measurement:**
- Context usage after Phase 1 implementation
- Number of sessions needed for complex analysis
- User interruptions (should be zero)
- State persistence reliability

---

## Testing Plan

### Test Case 1: Simple Valuation
- **Current:** 95k tokens, 81% usage
- **Target:** 50k tokens, 40% usage
- **Test:** Run same analysis with optimizations

### Test Case 2: Extended Session
- **Scenario:** Valuation + Sensitivity + Export + Discussion
- **Current:** Would exceed 200k, fail
- **Target:** Auto-checkpoint at 120k, resume transparently
- **Success:** User completes full workflow without interruption

### Test Case 3: Multi-Day Work
- **Scenario:** User works Monday, returns Wednesday
- **Current:** No state persistence
- **Target:** Auto-resume from last checkpoint
- **Success:** User continues where they left off

---

## Rollout Plan

1. **Week 1:** Implement Extract-Once + Compact Output
   - Update financial-analyst.md
   - Test with sample data room

2. **Week 2:** Add Sequential Dialog + File References
   - Update dialog flows
   - Test conversation length

3. **Week 3:** Build Auto Session Management
   - Implement state persistence
   - Test checkpoint/resume logic

4. **Week 4:** Polish & Document
   - User-facing documentation
   - Edge case handling

---

## Open Questions

1. **State file format:** JSON vs. SQLite vs. Custom?
   - **Recommendation:** JSON for simplicity, human-readable

2. **Checkpoint threshold:** 60% or 70% of context?
   - **Recommendation:** 60% (120k) to leave buffer

3. **State retention:** How long to keep checkpoints?
   - **Recommendation:** 30 days, auto-cleanup

4. **Failure recovery:** What if checkpoint fails?
   - **Recommendation:** Graceful degradation, warn user

---

## Notes

- All optimizations must maintain clarity (per Point 3 feedback)
- Session management must be completely transparent (per Point 6 feedback)
- No user decisions required for session continuation
- State must be portable (can move between machines)
