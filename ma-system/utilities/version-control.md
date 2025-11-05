# Version Control Utility

## Purpose
Standardized version control system for all M&A agent outputs to ensure consistency, traceability, and proper version history management.

## Usage
**All agents** creating file outputs MUST follow these conventions.

---

## Semantic Versioning

### Format
`v{major}.{minor}`

Examples: `v1.0`, `v1.1`, `v2.0`, `v2.3`

### Version Increment Rules

#### Major Version Increment (X.0 → X+1.0)
Increment major version when:
- **Methodology change** - Different valuation approach, new analytical framework
- **Complete rebuild** - Starting analysis from scratch with new data set
- **Significant assumption changes** - Material changes to core assumptions (>20% impact)
- **Structural changes** - Major reorganization of document, new sections added
- **User requests major revision** - "Rebuild the valuation", "Start over"

Examples:
- `v1.5` → `v2.0`: Changed from DCF-only to DCF + comps valuation
- `v2.3` → `v3.0`: Rebuilt model with new 3-year actuals (replacing projections)
- `v1.2` → `v2.0`: Changed WACC from 12% to 8% (major assumption revision)

#### Minor Version Increment (X.Y → X.Y+1)
Increment minor version when:
- **Data refresh** - Updated with new quarterly results, latest financials
- **Small corrections** - Fixed calculation errors, typos, formatting
- **Incremental updates** - Added sensitivity analysis, new comparable company
- **Content additions** - Added section without changing existing content
- **User requests refinement** - "Update with Q3 results", "Add this buyer"

Examples:
- `v1.0` → `v1.1`: Updated with Q3 2024 results
- `v2.3` → `v2.4`: Fixed typo in executive summary, corrected one formula
- `v1.5` → `v1.6`: Added 2 additional comparable companies

---

## File Naming Convention

### Standard Format
```
{deal-name}_{type}_{description}_v{major}.{minor}.{ext}
```

### Components

| Component | Description | Rules |
|-----------|-------------|-------|
| `{deal-name}` | Project code name | - Use hyphen-separated words<br>- No spaces<br>- Examples: `Project-Munich`, `TechTarget-Sale` |
| `{type}` | Document category | - Valuation_Model<br>- Financial_Model<br>- CIM<br>- Teaser<br>- Strategic_Buyers<br>- QA_Log |
| `{description}` | Specific identifier | - Optional, use when needed<br>- Examples: QoE_Analysis, Working_Capital |
| `v{major}.{minor}` | Version number | - Always include<br>- Format: v1.0, v2.3 |
| `{ext}` | File extension | - .xlsx, .docx, .pptx, .pdf |

### Examples

**Financial Models:**
```
Project-Munich_Valuation_Model_v1.0.xlsx
Project-Munich_Valuation_Model_v1.1.xlsx
Project-Munich_Valuation_Model_v2.0.xlsx
Project-Munich_Financial_Model_v1.0.xlsx
Project-Munich_QoE_Analysis_v1.0.xlsx
Project-Munich_Working_Capital_Analysis_v1.2.xlsx
```

**Documents:**
```
Project-Munich_CIM_v1.0.docx
Project-Munich_CIM_v2.3.docx
Project-Munich_Teaser_v1.0.pptx
Project-Munich_Management_Presentation_v1.5.pptx
Project-Munich_Process_Letter_v1.0.docx
```

**Market Research:**
```
Project-Munich_Strategic_Buyers_v1.0.xlsx
Project-Munich_Strategic_Buyers_v1.5.xlsx
Project-Munich_Financial_Buyers_v2.0.xlsx
Project-Munich_Industry_Analysis_v1.0.docx
Project-Munich_Comparable_Transactions_v1.2.xlsx
```

**Due Diligence:**
```
Project-Munich_QA_Log_v1.0.xlsx
Project-Munich_QA_Log_v3.2.xlsx
Project-Munich_DD_Checklist_v1.0.xlsx
Project-Munich_Red_Flags_Summary_v1.1.xlsx
```

---

## Version History Tracking

### In Excel Models
Every Excel file MUST include a "Version History" sheet with:

| Version | Date | Author | Changes | Impact |
|---------|------|--------|---------|--------|
| v1.0 | 2024-01-15 | Financial Analyst | Initial valuation model | Baseline |
| v1.1 | 2024-02-03 | Financial Analyst | Updated Q4 results | EBITDA +5% |
| v1.2 | 2024-02-10 | Financial Analyst | Added 3 comps | Valuation range narrowed |
| v2.0 | 2024-03-01 | Financial Analyst | Methodology change: Added transaction comps | Valuation +15% |

### In Documents (Word/PowerPoint)
Include version history on last page or footer:

```
Document Version History:
- v1.0 (2024-01-20): Initial CIM draft
- v1.1 (2024-01-25): Updated financial section with normalized EBITDA
- v1.2 (2024-02-01): Added management team bios
- v2.0 (2024-02-15): Major revision: New positioning strategy, updated financials
```

### In Knowledge Base
Update `knowledge-base/deal-insights.md` with version notes:

```markdown
## Valuation
**Current Version:** v2.0
**Date:** 2024-03-01
**Key Changes from v1.2:**
- Added precedent transaction analysis (10 deals researched)
- Updated WACC from 12% to 10% based on current market conditions
- Valuation range narrowed: €24-28M (was €22-30M)
**Impact:** Base case valuation increased from €25M to €26M
```

---

## Checking for Existing Versions

### Before Creating New File
All agents MUST check for existing versions:

1. **Check knowledge base first**:
   ```
   Read knowledge-base/deal-insights.md
   Look for section matching task (e.g., "## Valuation")
   Check if version exists and what the latest version number is
   ```

2. **Check output directory**:
   ```
   List files in outputs/{deal-name}/{category}/
   Find files matching {deal-name}_{type}_*
   Identify highest version number
   ```

3. **Decide on version number**:
   - If no existing file: Start with `v1.0`
   - If existing file found: Assess whether major or minor increment
   - Ask user if unclear whether major or minor

### Example Decision Flow
```
User: "Update the valuation"

Agent checks:
1. knowledge-base/deal-insights.md → Finds "Valuation v1.2, dated 2024-02-10"
2. outputs/Project-Munich/financial/valuation/ → Finds "Project-Munich_Valuation_Model_v1.2.xlsx"

Agent asks user:
"I found existing valuation v1.2 from Feb 10. What has changed?
- If data refresh or small update → Will save as v1.3
- If methodology change or major revision → Will save as v2.0"

User: "Q3 results are now available"

Agent decision: Minor update → v1.3
```

---

## Version Control in Knowledge Base

### Update Pattern
When saving new version:

1. **Update deal-insights.md**:
   ```markdown
   ## Valuation
   **Status:** Completed
   **Current Version:** v1.3
   **Date:** 2024-03-15
   **Previous Version:** v1.2 (2024-02-10)
   **Changes:** Updated with Q3 2024 results, EBITDA increased from €8M to €8.5M
   **Valuation Range:** €25M - €29M (Base: €27M, up from €26M in v1.2)
   **Output File:** `outputs/Project-Munich/financial/valuation/Project-Munich_Valuation_Model_v1.3.xlsx`
   ```

2. **Update valuation-history.md** (for financial analyst):
   ```markdown
   ### Version 1.3 (2024-03-15)
   **Changes from v1.2:**
   - Updated EBITDA: €8.0M → €8.5M (Q3 actuals)
   - Revenue growth revised: 15% → 18% based on Q3 momentum
   - Valuation impact: +€1M in base case

   **Assumptions maintained:**
   - WACC: 10% (unchanged)
   - Terminal growth: 2.5% (unchanged)
   - Multiple range: 8-10x EBITDA (unchanged)
   ```

---

## Special Cases

### Parallel Versions
If creating alternative scenarios, use descriptive names:

```
Project-Munich_Valuation_Model_Base_Case_v1.0.xlsx
Project-Munich_Valuation_Model_Optimistic_Case_v1.0.xlsx
Project-Munich_Valuation_Model_Conservative_Case_v1.0.xlsx
```

### Draft vs Final
Use status indicator for documents:

```
Project-Munich_CIM_Draft_v1.0.docx
Project-Munich_CIM_Final_v1.0.docx
```

Or use version numbering:
- v0.X = Draft
- v1.0+ = Final / Released

### Client-Facing vs Internal
Use separate file names:

```
Project-Munich_Teaser_Client_Version_v1.0.pptx
Project-Munich_Teaser_Internal_Notes_v1.0.pptx
```

---

## Error Handling

### If Wrong Version Number Used
Document in version history and correct going forward:

```
Version History:
v1.0 (2024-01-15): Initial model
v1.1 (2024-02-01): Updated financials
v2.0 (2024-02-05): [ERROR: Should have been v1.2, no methodology change]
v2.1 (2024-02-10): Corrected version numbering, minor update with Q1 projections
```

### If File Not Found
If agent cannot find expected file:

1. List all files in directory
2. Report to user what was found
3. Ask user to confirm expected file name
4. Proceed with user guidance

---

## Compliance Checklist

Before saving any output file, verify:

- [ ] File name follows convention: `{deal-name}_{type}_{description}_v{X}.{Y}.{ext}`
- [ ] Version number is correct (checked existing versions)
- [ ] Version history is included in file
- [ ] Knowledge base is updated with new version
- [ ] Changes from previous version are documented
- [ ] User is informed of version number and file location

---

## Benefits of This System

1. **Traceability** - Every change is documented
2. **No confusion** - Clear which version is current
3. **Easy rollback** - Can return to previous versions if needed
4. **Audit trail** - Shows evolution of analysis over time
5. **Collaboration** - Multiple agents can work on same deal without conflicts
6. **Professional** - Demonstrates organized, methodical approach
