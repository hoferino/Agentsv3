# Changelog - Financial Analyst Updates

## Version 2.1 (2024-11-05)

### Major Feature: Multiple Interaction Modes

Added support for three distinct interaction modes to match different user preferences and use cases.

#### New Modes

1. **⚡ One-Shot Mode**
   - Traditional approach: give task, get complete results
   - No interruptions for decisions
   - Uses best-practice standard assumptions
   - Fast execution

2. **💬 Dialog Mode**
   - Interactive, menu-driven workflow
   - User input on every major decision
   - Educational and collaborative
   - Full transparency and control

3. **🔄 Hybrid Mode (Default)**
   - Execute one-shot first, then offer refinement options
   - Best of both: speed + optional control
   - Most versatile approach
   - Recommended for most users

#### Features

- **Mode Selection Interface**: First-time users see clear comparison of all three modes
- **Mode Detection**: Agent can infer preferred mode from user's language
- **Anytime Switching**: Change modes mid-session via "Change Mode" menu option or natural language
- **Preference Persistence**: Mode choice saved to `knowledge-base/user-preferences.yaml`
- **Mode Indicator**: Main menu always shows current mode (⚡/💬/🔄)

#### Files Modified

- `.claude/commands/financial-analyst.md` - Added mode detection and execution logic
- `agents/financial-analyst-dialog.py` - Added `InteractionMode` enum, mode switching, preference persistence
- `knowledge-base/user-preferences.yaml` - New file for storing user preferences

#### Files Added

- `docs/interaction-modes-guide.md` - Comprehensive guide to all three modes
- `docs/CHANGELOG.md` - This file

### Backward Compatibility

All existing functionality remains available. Users can still:
- Use pure dialog mode (like v2.0)
- Use one-shot commands (like v1.0)
- Mix and match approaches

Default mode is **Hybrid** to provide the best experience for most users.

---

## Version 2.0 (2024-11-05)

### Major Feature: Dialog-Based Financial Analysis

Transformed Financial Analyst from single-prompt execution to interactive, menu-driven workflow.

#### New Capabilities

- **8 Menu Options**:
  1. Analyze All Financial Documents
  2. Build/Update Valuation Model
  3. Refine Excel Model (Dialog Mode) - Interactive refinement
  4. Quality of Earnings (QoE) Analysis
  5. Play Devil's Advocate - Stress-test assumptions
  6. Sensitivity & Scenario Analysis
  7. Review & Export Final Package
  8. Ask Financial Questions

- **Devil's Advocate Mode**: Interactive challenge system to stress-test valuations
- **Excel Refinement Dialog**: 6 sub-modes for iterative model improvement
- **Context-Aware Menus**: Options adapt based on work completed
- **State Persistence**: Session state saved across interactions

#### Files Added

- `agents/financial-analyst-dialog.py` - Dialog system implementation
- `docs/financial-analyst-dialog-guide.md` - Comprehensive user guide (600+ lines)
- `docs/financial-analyst-quick-reference.md` - Quick reference card

#### Files Modified

- `.claude/commands/financial-analyst.md` - Added dialog workflows for all 8 options

### Philosophy Shift

> "Better financial analysis through conversation, not automation"

Changed from black-box execution to transparent, collaborative process where users understand and control every decision.

---

## Version 1.0 (2024-11-04)

### Initial Release

- 8 specialized M&A agents including Financial Analyst
- Task-based (not phase-based) architecture
- Knowledge base system for persistent context
- Orchestrator for intelligent routing
- Large-scale document processing (Phase 1-5 workflow)
- Version-controlled outputs
