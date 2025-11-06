"""
Sub-Agent Coordination System

Enables primary agents to spawn sub-agents for specialized tasks,
collect their outputs, and integrate results back into the main workflow.

Example use case:
  Financial Analyst analyzing documents encounters a one-off expense item.
  → Spawns Company Intelligence agent to research the vendor
  → Gets context about the vendor and transaction
  → Integrates findings into normalization analysis
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SubAgentTaskStatus(Enum):
    """Status of a sub-agent task"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SubAgentTask:
    """
    A task assigned to a sub-agent.

    Example:
        SubAgentTask(
            agent_name='company-intelligence',
            task_description='Research vendor "Acme Consulting GmbH" - nature of services, typical engagement costs',
            context={'expense_item': '€380k legal/consulting spike in 2022'},
            expected_output='Brief description of vendor and typical project costs',
            priority='normal'
        )
    """
    task_id: str
    agent_name: str
    task_description: str
    context: Dict[str, Any]
    expected_output: str
    priority: str = "normal"  # low, normal, high, critical
    status: SubAgentTaskStatus = SubAgentTaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class SubAgentResult:
    """Result returned by sub-agent"""
    task_id: str
    agent_name: str
    status: SubAgentTaskStatus
    output: Dict[str, Any]
    context_tokens_used: int
    execution_time_seconds: float
    summary: str  # One-line summary for primary agent


class SubAgentCoordinator:
    """
    Coordinates sub-agent execution from primary agents.

    Primary agents can request sub-agent assistance for:
    - Research (company-intelligence, market-intelligence)
    - Specialized analysis (legal-tax-advisor)
    - Data gathering (dd-manager)

    The coordinator:
    1. Validates sub-agent is appropriate for task
    2. Spawns sub-agent with focused context
    3. Collects output
    4. Returns condensed results to primary agent
    """

    def __init__(self):
        self.tasks: List[SubAgentTask] = []
        self.task_counter = 0

        # Define which sub-agents primary agents can call
        self.allowed_sub_agents = {
            'financial-analyst': [
                'company-intelligence',
                'market-intelligence',
                'legal-tax-advisor',
                'dd-manager'
            ],
            'document-generator': [
                'financial-analyst',
                'company-intelligence',
                'market-intelligence'
            ],
            'buyer-relationship-manager': [
                'financial-analyst',
                'legal-tax-advisor',
                'company-intelligence'
            ],
            'dd-manager': [
                'financial-analyst',
                'legal-tax-advisor',
                'company-intelligence'
            ],
            'market-intelligence': [
                'company-intelligence',
                'financial-analyst'
            ]
        }

    def can_call_sub_agent(self, primary_agent: str, sub_agent: str) -> bool:
        """
        Check if primary agent is allowed to call specific sub-agent.

        Args:
            primary_agent: Name of the calling agent
            sub_agent: Name of the sub-agent to call

        Returns:
            True if allowed, False otherwise
        """
        allowed = self.allowed_sub_agents.get(primary_agent, [])
        return sub_agent in allowed

    def create_task(
        self,
        primary_agent: str,
        sub_agent: str,
        task_description: str,
        context: Dict[str, Any],
        expected_output: str,
        priority: str = "normal"
    ) -> SubAgentTask:
        """
        Create a sub-agent task.

        Args:
            primary_agent: Name of agent requesting sub-agent
            sub_agent: Name of sub-agent to execute task
            task_description: Clear description of what sub-agent should do
            context: Relevant context for the task
            expected_output: Description of expected result format
            priority: Task priority

        Returns:
            SubAgentTask object

        Raises:
            ValueError: If primary agent not allowed to call sub-agent
        """
        # Validate permission
        if not self.can_call_sub_agent(primary_agent, sub_agent):
            raise ValueError(
                f"{primary_agent} is not allowed to call {sub_agent}. "
                f"Allowed sub-agents: {self.allowed_sub_agents.get(primary_agent, [])}"
            )

        # Create task
        self.task_counter += 1
        task = SubAgentTask(
            task_id=f"{primary_agent}->{sub_agent}-{self.task_counter:03d}",
            agent_name=sub_agent,
            task_description=task_description,
            context=context,
            expected_output=expected_output,
            priority=priority,
            status=SubAgentTaskStatus.PENDING
        )

        self.tasks.append(task)
        return task

    def execute_task(self, task: SubAgentTask) -> SubAgentResult:
        """
        Execute sub-agent task.

        In production, this would:
        1. Spawn the sub-agent with focused context
        2. Execute the specific task
        3. Collect output
        4. Return condensed result

        For now, returns structured template for implementation.

        Args:
            task: SubAgentTask to execute

        Returns:
            SubAgentResult with output
        """
        # Update status
        task.status = SubAgentTaskStatus.IN_PROGRESS

        # Build sub-agent prompt
        sub_agent_prompt = self._build_sub_agent_prompt(task)

        # In production, this would invoke the actual sub-agent
        # For now, return template structure
        result = SubAgentResult(
            task_id=task.task_id,
            agent_name=task.agent_name,
            status=SubAgentTaskStatus.COMPLETED,
            output={
                'task_description': task.task_description,
                'findings': 'Sub-agent would execute here',
                'recommendations': [],
                'data_gathered': {}
            },
            context_tokens_used=0,  # Would be measured in production
            execution_time_seconds=0.0,  # Would be measured in production
            summary='Sub-agent task completed - integrate findings'
        )

        # Update task with result
        task.status = SubAgentTaskStatus.COMPLETED
        task.result = result.output

        return result

    def _build_sub_agent_prompt(self, task: SubAgentTask) -> str:
        """
        Build focused prompt for sub-agent.

        Includes:
        - Task description
        - Relevant context only
        - Expected output format
        - Constraints (time, depth)

        Returns:
            Formatted prompt string
        """
        prompt = f"""
You are being called as a sub-agent by another agent to help with a specific task.

**Your Role:** {task.agent_name}

**Task:** {task.task_description}

**Context Provided:**
{self._format_context(task.context)}

**Expected Output:** {task.expected_output}

**Constraints:**
- Keep response focused on the specific task
- Provide concise, actionable information
- If you need more context, state what's missing
- Estimated time: 5-10 minutes max

**Important:**
- You are a SUB-AGENT helping another agent
- Your output will be integrated into their workflow
- Be concise but thorough
- Provide sources/references where possible

Please execute this task now.
"""
        return prompt

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dict into readable string"""
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return '\n'.join(lines) if lines else "No additional context provided"

    def get_task_status(self, task_id: str) -> Optional[SubAgentTask]:
        """Get status of a specific task"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_pending_tasks(self) -> List[SubAgentTask]:
        """Get all pending tasks"""
        return [t for t in self.tasks if t.status == SubAgentTaskStatus.PENDING]

    def get_completed_tasks(self) -> List[SubAgentTask]:
        """Get all completed tasks"""
        return [t for t in self.tasks if t.status == SubAgentTaskStatus.COMPLETED]


# Convenience functions for agents to use

def call_sub_agent(
    primary_agent: str,
    sub_agent: str,
    task: str,
    context: Dict[str, Any],
    expected_output: str = "Brief summary of findings"
) -> SubAgentResult:
    """
    Convenience function for primary agents to call sub-agents.

    Usage (from financial-analyst):
        >>> from orchestrator.sub_agent_coordinator import call_sub_agent
        >>>
        >>> result = call_sub_agent(
        >>>     primary_agent='financial-analyst',
        >>>     sub_agent='company-intelligence',
        >>>     task='Research Acme Consulting GmbH - what services do they provide?',
        >>>     context={'expense_spike': '€380k in 2022', 'account': '671000 Legal/Consulting'},
        >>>     expected_output='Description of vendor and typical project costs'
        >>> )
        >>>
        >>> print(result.summary)
        >>> # Use result.output for detailed findings

    Args:
        primary_agent: Name of calling agent
        sub_agent: Name of sub-agent to call
        task: Task description
        context: Relevant context
        expected_output: Description of expected output

    Returns:
        SubAgentResult with findings
    """
    coordinator = SubAgentCoordinator()

    # Create task
    sub_task = coordinator.create_task(
        primary_agent=primary_agent,
        sub_agent=sub_agent,
        task_description=task,
        context=context,
        expected_output=expected_output
    )

    # Execute and return result
    return coordinator.execute_task(sub_task)


def format_sub_agent_result_for_context(result: SubAgentResult) -> str:
    """
    Format sub-agent result for inclusion in primary agent context.

    Keeps context minimal while preserving key findings.

    Args:
        result: SubAgentResult to format

    Returns:
        Formatted string (~200-500 tokens)
    """
    formatted = f"""
--- Sub-Agent Findings ({result.agent_name}) ---

Task: {result.output.get('task_description', 'Unknown')}

Summary: {result.summary}

Key Findings:
{_format_findings(result.output.get('findings', 'No findings'))}

Recommendations:
{_format_list(result.output.get('recommendations', []))}

Context cost: {result.context_tokens_used} tokens
---
"""
    return formatted


def _format_findings(findings: Any) -> str:
    """Format findings for display"""
    if isinstance(findings, str):
        return findings
    elif isinstance(findings, dict):
        return '\n'.join(f"- {k}: {v}" for k, v in findings.items())
    elif isinstance(findings, list):
        return '\n'.join(f"- {item}" for item in findings)
    return str(findings)


def _format_list(items: List[str]) -> str:
    """Format list for display"""
    if not items:
        return "None"
    return '\n'.join(f"- {item}" for item in items)


# Example usage patterns for different agents

USAGE_EXAMPLES = {
    'financial-analyst': """
# From financial-analyst workflow

# Scenario: Analyzing expenses, found unusual spike
expense_spike = {
    'account': '671000 - Legal and consulting fees',
    'amount': 380000,
    'year': 2022,
    'prior_years': [120000, 85000],
    'description': 'Spike from €85k to €380k'
}

# Call company-intelligence to research
result = call_sub_agent(
    primary_agent='financial-analyst',
    sub_agent='company-intelligence',
    task='Research the company activities in 2022 - any major projects, acquisitions, or legal matters that would explain €380k in legal/consulting fees?',
    context=expense_spike,
    expected_output='Brief description of 2022 activities and likely cause of legal/consulting spike'
)

# Integrate findings into normalization analysis
if 'one-time' in result.summary.lower():
    normalization_adjustments.append({
        'account': '671000',
        'amount': 380000 - 85000,  # Normalize to historical average
        'rationale': result.summary
    })
""",

    'buyer-relationship-manager': """
# From buyer-relationship-manager workflow

# Scenario: Received LOI, need financial context
loi_terms = {
    'buyer': 'Strategic Acquirer GmbH',
    'ev_offered': 28000000,
    'structure': 'All cash',
    'conditions': ['Subject to QoE', 'Working capital adjustment']
}

# Call financial-analyst for valuation context
result = call_sub_agent(
    primary_agent='buyer-relationship-manager',
    sub_agent='financial-analyst',
    task='Compare this LOI offer to our valuation range. Is €28M within our range? What are the key value drivers they might question in QoE?',
    context={'loi': loi_terms, 'our_valuation_midpoint': 29800000},
    expected_output='Analysis of offer vs. valuation and QoE risk areas'
)

# Use in LOI comparison
loi_analysis['valuation_comparison'] = result.output
"""
}
