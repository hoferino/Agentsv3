# M&A Agent Slash Commands

This directory contains slash commands for all 8 specialized M&A agents. Each command activates a specific agent with full context and capabilities.

## Available Commands

### `/md` - Managing Director
**Role**: Strategic orchestration and deal coordination

The Managing Director is your main orchestrator who:
- Provides high-level strategic guidance
- Coordinates all other agents
- Makes routing decisions
- Manages deal timeline and milestones

**Use when**: You need strategic advice or want to coordinate multiple agents for complex tasks.

**Example**: `/md` "Prepare for buyer meetings next week"

---

### `/financial-analyst` - Financial Analyst
**Role**: Valuation, financial modeling, and QoE analysis

Specializes in:
- DCF valuations and financial models
- Quality of Earnings (QoE) analysis
- Working capital analysis
- EBITDA normalization
- Sensitivity analysis

**Skills**: xlsx (Excel)

**Use when**: You need valuation, financial models, or financial analysis.

**Examples**:
- `/financial-analyst` "Value this company"
- `/financial-analyst` "Update the valuation with Q3 results"
- `/financial-analyst` "What's the normalized EBITDA?"

---

### `/market-intelligence` - Market Intelligence
**Role**: Buyer research, comparable transactions, and industry analysis

Specializes in:
- Strategic and financial buyer identification
- Comparable transaction research
- Industry and market analysis
- Buyer prioritization
- Market positioning

**Skills**: web_search, xlsx

**Use when**: You need buyer lists, market research, or industry analysis.

**Examples**:
- `/market-intelligence` "Who could buy this company?"
- `/market-intelligence` "Find comparable transactions"
- `/market-intelligence` "What's happening in this industry?"

---

### `/document-generator` - Document Generator
**Role**: Create CIMs, teasers, presentations, and process letters

Specializes in:
- Confidential Information Memorandums (CIM)
- Marketing teasers
- Management presentations
- Process letters

**Skills**: docx, pptx, pdf

**Use when**: You need to create or update transaction documents.

**Examples**:
- `/document-generator` "Create a CIM"
- `/document-generator` "Draft a teaser"
- `/document-generator` "Update the CIM with new valuation"

---

### `/dd-manager` - Due Diligence Manager
**Role**: Data room setup, Q&A tracking, and issue management

Specializes in:
- Virtual data room setup and structure
- Q&A log management
- Due diligence checklist creation
- Red flag identification
- Issue tracking

**Skills**: xlsx, pdf, docx

**Use when**: You need to manage the due diligence process.

**Examples**:
- `/dd-manager` "Set up the data room"
- `/dd-manager` "Track buyer questions"
- `/dd-manager` "What are the red flags?"

---

### `/buyer-relationship-manager` - Buyer Relationship Manager
**Role**: Track engagement, compare offers, manage negotiations

Specializes in:
- Buyer engagement tracking
- LOI comparison and analysis
- Meeting preparation
- Negotiation strategy
- Process management

**Skills**: xlsx, docx

**Use when**: You need to manage buyer relationships or compare offers.

**Examples**:
- `/buyer-relationship-manager` "What's the buyer status?"
- `/buyer-relationship-manager` "Compare the LOIs"
- `/buyer-relationship-manager` "Prepare for meeting with TechCorp"

---

### `/legal-tax-advisor` - Legal & Tax Advisor
**Role**: Transaction structure, tax planning, and legal due diligence

Specializes in:
- Asset sale vs. share sale analysis
- Tax optimization
- Legal due diligence
- Regulatory compliance
- Contract review

**Skills**: pdf, docx, xlsx

**Use when**: You need legal or tax guidance.

**Examples**:
- `/legal-tax-advisor` "Should this be an asset or share sale?"
- `/legal-tax-advisor` "Review this LOI"
- `/legal-tax-advisor` "What are the tax implications?"

---

### `/company-intelligence` - Company Intelligence
**Role**: Research target company, products, management, and competitive position

Specializes in:
- Company background research
- Product and service analysis
- Management team analysis
- Competitive analysis
- Technology assessment
- Investment thesis development

**Skills**: web_search

**Use when**: You need to research and understand the target company.

**Examples**:
- `/company-intelligence` "Research this company"
- `/company-intelligence` "Analyze the management team"
- `/company-intelligence` "Who are the competitors?"

---

## Quick Reference

| Command | Primary Use | Key Skills |
|---------|-------------|------------|
| `/md` | Strategic coordination | All agents |
| `/financial-analyst` | Valuation & models | xlsx |
| `/market-intelligence` | Buyer research | web_search, xlsx |
| `/document-generator` | CIM, teaser, presentations | docx, pptx, pdf |
| `/dd-manager` | Data room & Q&A | xlsx, pdf, docx |
| `/buyer-relationship-manager` | Buyer tracking & LOI comparison | xlsx, docx |
| `/legal-tax-advisor` | Legal & tax advice | pdf, docx, xlsx |
| `/company-intelligence` | Company research | web_search |

---

## How It Works

1. **Type the slash command** (e.g., `/financial-analyst`)
2. **Add your request** after the command
3. **The agent activates** with full context from:
   - `ma-system/knowledge-base/deal-insights.md`
   - Relevant files in `ma-system/outputs/`
   - Other agents' prior work

4. **The agent performs the task** using:
   - Specialized skills (xlsx, docx, pptx, pdf, web_search)
   - Best practices for M&A transactions
   - Context-aware approach (builds on existing work)

5. **Updates knowledge base** after completion

---

## Tips

- **Start with `/md`** if unsure which agent to use - the Managing Director will coordinate
- **Agents remember prior work** - they check the knowledge base before starting
- **Agents coordinate automatically** - they know when to involve other agents
- **Build incrementally** - "Update the valuation" loads the existing model and improves it
- **Agents work in parallel** - the Managing Director can coordinate multiple agents simultaneously

---

## Example Workflows

### Starting a New Deal
```
/company-intelligence Research the company TechTarget GmbH
/financial-analyst Value this company
/market-intelligence Who could buy this company?
/document-generator Create a teaser
```

### Preparing for Buyer Meetings
```
/md Prepare for buyer meetings next week
(This coordinates Financial Analyst, Document Generator, Market Intelligence, and Buyer Relationship Manager)
```

### Managing Due Diligence
```
/dd-manager Set up the data room
/dd-manager Track these buyer questions
/financial-analyst Answer the working capital questions
/legal-tax-advisor Review the material contracts
```

### Comparing Offers
```
/buyer-relationship-manager Compare the LOIs we received
/financial-analyst Calculate net proceeds for each offer
/legal-tax-advisor Review the terms and conditions
```

---

## System Architecture

All agents integrate with:
- **Knowledge Base**: `ma-system/knowledge-base/deal-insights.md` (single source of truth)
- **Outputs**: `ma-system/outputs/{deal-name}/` (version-controlled deliverables)
- **Configuration**: `ma-system/config.yaml` (deal settings)

For more details, see:
- `ma-system/README.md` - Complete system documentation
- `ma-system/CLAUDE.md` - Guidance for working with the system
- `ma-system/agents/*.md` - Individual agent definitions
