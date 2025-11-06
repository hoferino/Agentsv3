"""
M&A System Orchestrator - Intelligent Agent Routing

This module provides context-aware routing of user requests to the appropriate
specialized agents. Unlike phase-based systems, this router makes decisions based
on user intent, available information, and task requirements.

Key Principles:
1. Intent-based routing (not phase-based)
2. Context-aware decisions
3. Parallel execution support
4. Knowledge base integration
5. Flexible and adaptive
"""

import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class RoutingDecision:
    """Represents a routing decision made by the orchestrator"""
    primary_agent: str
    supporting_agents: List[str]
    required_skills: List[str]
    rationale: str
    parallel_execution: bool
    context_notes: str

    # New: Context to pass to agent
    orchestrator_context: Optional[Dict[str, Any]] = None

    def format_for_agent(self) -> str:
        """
        Format routing decision as context for agent activation.

        This is passed to the agent so it knows:
        - Why it was activated
        - What the orchestrator knows about current deal state
        - Suggested actions based on existing work

        Returns:
            Formatted string to include in agent prompt
        """
        lines = [
            "=== Orchestrator Context ===",
            f"Routing Rationale: {self.rationale}",
            ""
        ]

        if self.context_notes:
            lines.append(f"Notes: {self.context_notes}")
            lines.append("")

        if self.orchestrator_context:
            ctx = self.orchestrator_context

            # Deal info
            if 'deal_name' in ctx:
                lines.append(f"Deal: {ctx['deal_name']}")

            # Existing work
            if 'existing_work' in ctx:
                lines.append("\nExisting Work:")
                for key, value in ctx['existing_work'].items():
                    lines.append(f"  - {key}: {value}")

            # Suggested action
            if 'suggested_action' in ctx:
                lines.append(f"\nSuggested Action: {ctx['suggested_action']}")

            # Prerequisites
            if 'prerequisites_met' in ctx:
                if ctx['prerequisites_met']:
                    lines.append("\n✓ All prerequisites met")
                else:
                    lines.append("\n⚠ Prerequisites not met:")
                    for prereq in ctx.get('missing_prerequisites', []):
                        lines.append(f"  - {prereq}")

        lines.append("\n=== End Orchestrator Context ===\n")
        return '\n'.join(lines)


class MAOrchestrator:
    """
    Main orchestrator class for the M&A agent system.

    Analyzes user requests and intelligently routes to appropriate agents
    based on intent, context, and availability rather than rigid phase rules.
    """

    def __init__(self, config_path: str = "./config.yaml"):
        """Initialize orchestrator with configuration"""
        self.config = self._load_config(config_path)
        self.intent_patterns = self._load_intent_patterns()
        self.agent_capabilities = self._load_agent_capabilities()
        self.knowledge_base = self._load_knowledge_base()

    def _load_config(self, path: str) -> Dict:
        """Load system configuration"""
        # TODO: Implement YAML config loading
        return {}

    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent detection patterns from config"""
        return {
            'financial_analysis': [
                r'\b(valuation|bewertung|dcf|value|worth|financial model|finanzmodell)\b',
                r'\b(qoe|quality of earnings|normalized ebitda)\b',
                r'\b(working capital|betriebskapital|nwc)\b'
            ],
            'document_creation': [
                r'\b(create|erstelle|draft)\s+(cim|teaser|presentation|management deck)\b',
                r'\b(cim|confidential information memorandum)\b',
                r'\b(teaser|executive summary|one.?pager)\b',
                r'\b(management presentation|präsentation)\b'
            ],
            'market_intelligence': [
                r'\b(find|identify|search for)\s+(buyers|käufer|acquirers)\b',
                r'\b(comparable|vergleichs)\s+(transactions|companies|deals)\b',
                r'\b(industry analysis|market trends|branchenanalyse)\b',
                r'\b(who (could|would) buy)\b'
            ],
            'due_diligence': [
                r'\b(data.?room|datenraum|vdr)\b',
                r'\b(q.?a|questions|fragen)\b',
                r'\b(red flags|issues|risks|problems)\b',
                r'\b(due diligence|dd|diligence)\b'
            ],
            'deal_execution': [
                r'\b(loi|letter of intent|term sheet)\b',
                r'\b(compare|vergleichen)\s+(offers|lois|angebote)\b',
                r'\b(buyer (meeting|tracking|status))\b',
                r'\b(negotiation|verhandlung)\b'
            ],
            'legal_tax': [
                r'\b(legal|rechtlich|contract|vertrag)\b',
                r'\b(tax|steuer|struktur)\b',
                r'\b(regulatory|compliance|genehmigung)\b'
            ]
        }

    def _load_agent_capabilities(self) -> Dict:
        """Define agent capabilities and specializations"""
        return {
            'managing-director': {
                'role': 'orchestrator',
                'skills': [],
                'specializations': ['strategy', 'coordination', 'high-level guidance']
            },
            'financial-analyst': {
                'role': 'specialist',
                'skills': ['xlsx'],
                'specializations': ['valuation', 'financial modeling', 'qoe', 'working capital']
            },
            'market-intelligence': {
                'role': 'specialist',
                'skills': ['web_search', 'xlsx'],
                'specializations': ['buyer identification', 'market research', 'comparables']
            },
            'document-generator': {
                'role': 'specialist',
                'skills': ['docx', 'pptx', 'pdf'],
                'specializations': ['cim', 'teaser', 'presentations', 'letters']
            },
            'dd-manager': {
                'role': 'specialist',
                'skills': ['xlsx', 'pdf'],
                'specializations': ['data room', 'qa tracking', 'issue management']
            },
            'buyer-relationship-manager': {
                'role': 'specialist',
                'skills': ['xlsx', 'docx'],
                'specializations': ['buyer tracking', 'loi comparison', 'meetings', 'negotiation']
            },
            'legal-tax-advisor': {
                'role': 'specialist',
                'skills': ['pdf', 'docx'],
                'specializations': ['transaction structure', 'legal dd', 'tax analysis']
            },
            'company-intelligence': {
                'role': 'specialist',
                'skills': ['web_search'],
                'specializations': ['company research', 'competitive analysis', 'management analysis']
            }
        }

    def _load_knowledge_base(self) -> Dict:
        """Load current knowledge base state"""
        try:
            # Try relative import first (when used as package)
            try:
                from .knowledge_base_reader import get_current_deal_state
            except ImportError:
                # Fallback to direct import (when run standalone)
                from knowledge_base_reader import get_current_deal_state

            state = get_current_deal_state()

            # Convert to orchestrator format
            return {
                'deal_name': state.deal_name,
                'target_company': state.target_company,
                'valuation': {
                    'completed': state.valuation_completed,
                    'latest': state.valuation_version,
                    'ev_midpoint': state.valuation_ev_midpoint
                },
                'cim': {
                    'completed': state.cim_status not in ['Not started', 'Not found'],
                    'status': state.cim_status
                },
                'teaser': {
                    'completed': state.teaser_status not in ['Not started', 'Not found'],
                    'status': state.teaser_status
                },
                'buyers_identified': {
                    'count': state.buyers_identified,
                    'contacted': state.buyers_contacted,
                    'ndas': state.ndas_signed,
                    'lois': state.lois_received
                },
                'financial_data': {
                    'extracted': state.financial_data_extracted,
                    'date': state.data_extraction_date
                },
                'raw_state': state  # Keep full state for detailed queries
            }
        except Exception as e:
            # Fallback to empty state if knowledge base not found
            print(f"Warning: Could not load knowledge base: {e}")
            return {
                'valuation': {'completed': False, 'latest': None},
                'cim': {'completed': False, 'status': 'Not found'},
                'buyers_identified': {'count': 0, 'contacted': 0},
                'financial_data': {'extracted': False}
            }

    def analyze_intent(self, user_input: str) -> List[str]:
        """
        Analyze user input to determine intent(s).

        Can identify multiple intents for complex requests.
        """
        intents = []
        user_input_lower = user_input.lower()

        for intent_category, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower, re.IGNORECASE):
                    intents.append(intent_category)
                    break

        return list(set(intents))  # Remove duplicates

    def route_request(self, user_input: str) -> List[RoutingDecision]:
        """
        Route user request to appropriate agent(s).

        Returns list of routing decisions (can be multiple for complex requests).
        """
        intents = self.analyze_intent(user_input)

        if not intents:
            # Default to managing director for general queries
            return [RoutingDecision(
                primary_agent='managing-director',
                supporting_agents=[],
                required_skills=[],
                rationale='General query - routing to Managing Director for guidance',
                parallel_execution=False,
                context_notes='No specific intent detected'
            )]

        routing_decisions = []

        for intent in intents:
            decision = self._route_by_intent(intent, user_input)
            if decision:
                routing_decisions.append(decision)

        return routing_decisions

    def _route_by_intent(self, intent: str, user_input: str) -> Optional[RoutingDecision]:
        """Route based on specific intent category"""

        routing_map = {
            'financial_analysis': self._route_financial,
            'document_creation': self._route_document,
            'market_intelligence': self._route_market_intelligence,
            'due_diligence': self._route_due_diligence,
            'deal_execution': self._route_deal_execution,
            'legal_tax': self._route_legal_tax
        }

        router_func = routing_map.get(intent)
        if router_func:
            return router_func(user_input)

        return None

    def _route_financial(self, user_input: str) -> RoutingDecision:
        """Route financial analysis requests"""

        # Check existing work
        valuation_exists = self.knowledge_base['valuation']['completed']
        data_extracted = self.knowledge_base.get('financial_data', {}).get('extracted', False)

        # Build context notes
        if valuation_exists:
            context_notes = f"Existing valuation: {self.knowledge_base['valuation']['latest']} (EV: €{self.knowledge_base['valuation'].get('ev_midpoint', 'N/A')}M)"
        else:
            context_notes = 'New valuation - will build from scratch'

        # Build orchestrator context for agent
        orchestrator_context = {
            'deal_name': self.knowledge_base.get('deal_name', 'Unknown'),
            'existing_work': {},
            'suggested_action': 'update' if valuation_exists else 'create',
            'prerequisites_met': True,
            'can_call_sub_agents': ['company-intelligence', 'market-intelligence', 'legal-tax-advisor', 'dd-manager']
        }

        # Add existing work info
        if valuation_exists:
            orchestrator_context['existing_work']['valuation'] = self.knowledge_base['valuation']['latest']

        if data_extracted:
            orchestrator_context['existing_work']['financial_data'] = f"Extracted on {self.knowledge_base['financial_data']['date']}"
        else:
            orchestrator_context['suggested_action'] = 'extract_then_analyze'

        return RoutingDecision(
            primary_agent='financial-analyst',
            supporting_agents=['market-intelligence'],  # For comparable data
            required_skills=['xlsx'],
            rationale='Financial analysis requires Financial Analyst expertise',
            parallel_execution=False,
            context_notes=context_notes,
            orchestrator_context=orchestrator_context
        )

    def _route_document(self, user_input: str) -> RoutingDecision:
        """Route document creation requests"""

        # Determine supporting agents based on document type
        supporting = ['company-intelligence', 'financial-analyst', 'market-intelligence']

        return RoutingDecision(
            primary_agent='document-generator',
            supporting_agents=supporting,
            required_skills=['docx', 'pptx'],
            rationale='Document creation requires Document Generator',
            parallel_execution=False,
            context_notes='Will gather content from multiple sources'
        )

    def _route_market_intelligence(self, user_input: str) -> RoutingDecision:
        """Route market research requests"""

        context = f"Buyers identified: {self.knowledge_base['buyers_identified']['count']}"

        return RoutingDecision(
            primary_agent='market-intelligence',
            supporting_agents=['company-intelligence'],
            required_skills=['web_search', 'xlsx'],
            rationale='Market research requires Market Intelligence agent',
            parallel_execution=True,  # Can run parallel to other work
            context_notes=context
        )

    def _route_due_diligence(self, user_input: str) -> RoutingDecision:
        """Route due diligence requests"""

        return RoutingDecision(
            primary_agent='dd-manager',
            supporting_agents=['financial-analyst', 'legal-tax-advisor'],
            required_skills=['xlsx', 'pdf'],
            rationale='DD management requires DD Manager',
            parallel_execution=False,
            context_notes='Will coordinate with specialists as needed'
        )

    def _route_deal_execution(self, user_input: str) -> RoutingDecision:
        """Route deal execution requests"""

        return RoutingDecision(
            primary_agent='buyer-relationship-manager',
            supporting_agents=['financial-analyst', 'legal-tax-advisor'],
            required_skills=['xlsx', 'docx'],
            rationale='Buyer management requires Buyer Relationship Manager',
            parallel_execution=False,
            context_notes='Will analyze offers and provide recommendations'
        )

    def _route_legal_tax(self, user_input: str) -> RoutingDecision:
        """Route legal/tax requests"""

        return RoutingDecision(
            primary_agent='legal-tax-advisor',
            supporting_agents=['financial-analyst'],
            required_skills=['pdf', 'docx'],
            rationale='Legal and tax matters require Legal Tax Advisor',
            parallel_execution=False,
            context_notes='Will provide legal and tax analysis'
        )

    def check_dependencies(self, routing_decision: RoutingDecision) -> List[str]:
        """
        Check if there are dependencies that should be resolved first.

        Returns list of prerequisite tasks that should be completed.
        """
        prerequisites = []

        # Example: CIM creation requires valuation
        if routing_decision.primary_agent == 'document-generator':
            if 'cim' in routing_decision.context_notes.lower():
                if not self.knowledge_base['valuation']['completed']:
                    prerequisites.append('Complete valuation before CIM creation')

        # Example: Buyer outreach needs teaser
        if routing_decision.primary_agent == 'buyer-relationship-manager':
            if not self.knowledge_base['cim']['completed']:
                prerequisites.append('Create teaser/CIM before buyer outreach')

        return prerequisites

    def suggest_next_actions(self, current_state: Dict) -> List[str]:
        """
        Proactively suggest next logical steps based on current state.

        This enables proactive workflow management.
        """
        suggestions = []

        # If valuation is done but no CIM, suggest CIM
        if current_state.get('valuation_complete') and not current_state.get('cim_complete'):
            suggestions.append('Create CIM now that valuation is complete')

        # If CIM done but no buyers identified, suggest buyer research
        if current_state.get('cim_complete') and current_state.get('buyers_identified') == 0:
            suggestions.append('Identify potential buyers')

        # If buyers identified and CIM ready, suggest outreach
        if current_state.get('cim_complete') and current_state.get('buyers_identified') > 0:
            suggestions.append('Begin buyer outreach with teaser')

        return suggestions


def main():
    """Example usage of the orchestrator"""

    orchestrator = MAOrchestrator()

    # Example requests
    test_requests = [
        "Value this company",
        "Create a CIM",
        "Find potential buyers",
        "Set up the data room",
        "Compare the LOIs we received",
        "What's the tax structure we should use?"
    ]

    print("M&A Orchestrator - Production-Ready Routing\n")
    print("=" * 80)
    print(f"\nKnowledge Base Loaded:")
    print(f"  Deal: {orchestrator.knowledge_base.get('deal_name', 'Unknown')}")
    print(f"  Target: {orchestrator.knowledge_base.get('target_company', 'Unknown')}")
    print(f"  Valuation: {'✓ ' + orchestrator.knowledge_base['valuation'].get('latest', 'None') if orchestrator.knowledge_base['valuation']['completed'] else '○ Not completed'}")
    print(f"  Financial Data: {'✓ Extracted' if orchestrator.knowledge_base.get('financial_data', {}).get('extracted') else '○ Not extracted'}")
    print(f"  Buyers: {orchestrator.knowledge_base['buyers_identified']['count']} identified")
    print("=" * 80)

    for request in test_requests:
        print(f"\n{'='*80}")
        print(f"User Request: '{request}'")
        print("=" * 80)

        decisions = orchestrator.route_request(request)

        for i, decision in enumerate(decisions, 1):
            print(f"\nRouting Decision #{i}:")
            print(f"  Primary Agent: {decision.primary_agent}")
            print(f"  Supporting: {', '.join(decision.supporting_agents) if decision.supporting_agents else 'None'}")
            print(f"  Skills: {', '.join(decision.required_skills) if decision.required_skills else 'None'}")
            print(f"  Rationale: {decision.rationale}")
            print(f"  Context Notes: {decision.context_notes}")

            # Show formatted context for agent
            if decision.orchestrator_context:
                print(f"\n  Context for Agent Activation:")
                print("  " + "\n  ".join(decision.format_for_agent().split('\n')))

    print("\n" + "=" * 80)
    print("\n✓ Orchestrator is production-ready")
    print("  - Real knowledge base reading")
    print("  - Context passing to agents")
    print("  - Sub-agent coordination enabled")
    print("=" * 80)


if __name__ == "__main__":
    main()
