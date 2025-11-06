"""
Knowledge Base Reader for Orchestrator

Parses knowledge-base/deal-insights.md to extract current deal state,
enabling context-aware routing and incremental work detection.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class KnowledgeBaseState:
    """Current state extracted from knowledge base"""
    deal_name: str
    target_company: str
    last_updated: str
    deal_status: str

    # Valuation
    valuation_completed: bool
    valuation_version: Optional[str]
    valuation_ev_midpoint: Optional[float]
    valuation_date: Optional[str]

    # Buyers
    buyers_identified: int
    buyers_contacted: int
    ndas_signed: int
    lois_received: int

    # Documents
    teaser_status: str
    cim_status: str
    financial_model_status: str

    # Financial Analysis
    financial_data_extracted: bool
    data_extraction_date: Optional[str]

    # Raw data for custom queries
    raw_sections: Dict[str, str]


class KnowledgeBaseReader:
    """
    Reads and parses knowledge-base/deal-insights.md

    Usage:
        reader = KnowledgeBaseReader()
        state = reader.load_current_state()

        if state.valuation_completed:
            print(f"Existing valuation: {state.valuation_version}")
    """

    def __init__(self, kb_path: str = None):
        """
        Initialize reader.

        Args:
            kb_path: Optional path to knowledge-base directory.
                    If None, uses default relative to this file.
        """
        if kb_path is None:
            # Default: ../knowledge-base from this file
            current_dir = Path(__file__).parent
            kb_path = current_dir.parent / "knowledge-base"

        self.kb_path = Path(kb_path)
        self.deal_insights_path = self.kb_path / "deal-insights.md"

    def load_current_state(self) -> KnowledgeBaseState:
        """
        Load and parse current deal state from knowledge base.

        Returns:
            KnowledgeBaseState with all extracted information

        Raises:
            FileNotFoundError: If deal-insights.md doesn't exist
        """
        if not self.deal_insights_path.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {self.deal_insights_path}\n"
                "Please ensure knowledge-base/deal-insights.md exists."
            )

        with open(self.deal_insights_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self._parse_content(content)

    def _parse_content(self, content: str) -> KnowledgeBaseState:
        """Parse markdown content into structured state"""

        # Split into sections
        sections = self._split_sections(content)

        # Extract header fields
        deal_name = self._extract_field(content, r'\*\*Deal Name:\*\* (.+)')
        target_company = self._extract_field(content, r'\*\*Target Company:\*\* (.+)')
        last_updated = self._extract_field(content, r'\*\*Last Updated:\*\* (.+)')
        deal_status = self._extract_field(content, r'\*\*Deal Status:\*\* (.+)')

        # Extract valuation info
        valuation_section = sections.get('Valuation', '')
        valuation_completed = '✓' in valuation_section or 'Complete' in valuation_section
        valuation_version = self._extract_field(
            valuation_section,
            r'\*\*Latest Valuation:\*\* (v[\d.]+)'
        )
        valuation_ev = self._extract_number(
            valuation_section,
            r'\*\*Midpoint \(EV\):\*\* \*\*€([\d.]+)M\*\*'
        )
        valuation_date = self._extract_field(
            valuation_section,
            r'\*\*Valuation Date:\*\* ([\d-]+)'
        )

        # Extract buyer info
        buyers_section = sections.get('Identified Buyers', '')
        buyers_identified = self._extract_number(
            buyers_section,
            r'\*\*Strategic Buyers Identified:\*\* (\d+)'
        ) or 0
        buyers_identified += self._extract_number(
            buyers_section,
            r'\*\*Financial Buyers Identified:\*\* (\d+)'
        ) or 0

        buyers_contacted = self._extract_number(
            buyers_section,
            r'\*\*Total Contacted:\*\* (\d+)'
        ) or 0

        ndas_signed = self._extract_number(
            buyers_section,
            r'\*\*NDAs Signed:\*\* (\d+)'
        ) or 0

        lois_received = self._extract_number(
            buyers_section,
            r'\*\*LOIs Received:\*\* (\d+)'
        ) or 0

        # Extract document status
        docs_section = sections.get('Transaction Documents', '')
        teaser_status = self._extract_doc_status(docs_section, 'Teaser')
        cim_status = self._extract_doc_status(docs_section, 'CIM')
        financial_model_status = self._extract_doc_status(docs_section, 'Financial Model')

        # Extract financial data extraction status
        financial_section = sections.get('Financial Highlights', '') or sections.get('Financial Analysis', '')
        financial_data_extracted = 'extracted' in financial_section.lower() or 'complete' in financial_section.lower()
        data_extraction_date = self._extract_field(
            financial_section,
            r'extracted.*?([\d-]+)'
        )

        return KnowledgeBaseState(
            deal_name=deal_name or "Unknown",
            target_company=target_company or "Unknown",
            last_updated=last_updated or "Unknown",
            deal_status=deal_status or "Unknown",
            valuation_completed=valuation_completed,
            valuation_version=valuation_version,
            valuation_ev_midpoint=valuation_ev,
            valuation_date=valuation_date,
            buyers_identified=buyers_identified,
            buyers_contacted=buyers_contacted,
            ndas_signed=ndas_signed,
            lois_received=lois_received,
            teaser_status=teaser_status,
            cim_status=cim_status,
            financial_model_status=financial_model_status,
            financial_data_extracted=financial_data_extracted,
            data_extraction_date=data_extraction_date,
            raw_sections=sections
        )

    def _split_sections(self, content: str) -> Dict[str, str]:
        """Split markdown into sections by H2 headers"""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            # Check for H2 header (## Section Name)
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content)

                # Start new section
                current_section = line[3:].strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _extract_field(self, text: str, pattern: str) -> Optional[str]:
        """Extract field using regex pattern"""
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    def _extract_number(self, text: str, pattern: str) -> Optional[float]:
        """Extract number using regex pattern"""
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def _extract_doc_status(self, docs_section: str, doc_name: str) -> str:
        """Extract document status from table"""
        # Look for table row with document name
        pattern = rf'\| {doc_name}\s*\|\s*([^|]+)\s*\|'
        match = re.search(pattern, docs_section)
        if match:
            status = match.group(1).strip()
            return status
        return "Not found"

    def format_context_summary(self, state: KnowledgeBaseState) -> str:
        """
        Format knowledge base state into human-readable summary.

        Useful for passing to agents as context.

        Returns:
            Formatted string with key deal status
        """
        lines = [
            f"Deal: {state.deal_name} ({state.target_company})",
            f"Status: {state.deal_status}",
            ""
        ]

        # Valuation status
        if state.valuation_completed:
            lines.append(
                f"✓ Valuation: {state.valuation_version} "
                f"(EV: €{state.valuation_ev_midpoint}M, dated {state.valuation_date})"
            )
        else:
            lines.append("○ Valuation: Not completed")

        # Financial data status
        if state.financial_data_extracted:
            lines.append(f"✓ Financial data extracted ({state.data_extraction_date})")
        else:
            lines.append("○ Financial data: Not extracted")

        # Documents status
        docs_status = []
        if state.cim_status != "Not started":
            docs_status.append(f"CIM: {state.cim_status}")
        if state.teaser_status != "Not started":
            docs_status.append(f"Teaser: {state.teaser_status}")

        if docs_status:
            lines.append(f"Documents: {', '.join(docs_status)}")

        # Buyer status
        if state.buyers_identified > 0:
            lines.append(
                f"Buyers: {state.buyers_identified} identified, "
                f"{state.buyers_contacted} contacted, "
                f"{state.ndas_signed} NDAs, "
                f"{state.lois_received} LOIs"
            )

        return '\n'.join(lines)

    def get_routing_context(self, state: KnowledgeBaseState, intent: str) -> Dict[str, Any]:
        """
        Get routing context for specific intent.

        Args:
            state: Current knowledge base state
            intent: Intent category (e.g., 'financial_analysis')

        Returns:
            Dictionary with relevant context for routing
        """
        context = {
            'deal_name': state.deal_name,
            'target_company': state.target_company
        }

        if intent == 'financial_analysis':
            context.update({
                'valuation_exists': state.valuation_completed,
                'valuation_version': state.valuation_version,
                'data_extracted': state.financial_data_extracted,
                'suggested_action': 'update' if state.valuation_completed else 'create'
            })

        elif intent == 'document_creation':
            context.update({
                'valuation_ready': state.valuation_completed,
                'cim_status': state.cim_status,
                'teaser_status': state.teaser_status,
                'prerequisites_met': state.valuation_completed
            })

        elif intent == 'market_intelligence':
            context.update({
                'buyers_identified': state.buyers_identified,
                'suggested_action': 'expand' if state.buyers_identified > 0 else 'initial_research'
            })

        return context


# Convenience function for quick access
def get_current_deal_state(kb_path: str = None) -> KnowledgeBaseState:
    """
    Quick function to get current deal state.

    Usage:
        >>> from orchestrator.knowledge_base_reader import get_current_deal_state
        >>> state = get_current_deal_state()
        >>> if state.valuation_completed:
        >>>     print(f"Valuation exists: {state.valuation_version}")

    Args:
        kb_path: Optional path to knowledge-base directory

    Returns:
        KnowledgeBaseState
    """
    reader = KnowledgeBaseReader(kb_path)
    return reader.load_current_state()
