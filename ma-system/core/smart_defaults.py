"""
Smart Defaults - Context Management Suggestion #3

Provides intelligent defaults for financial analysis questions based on
data-driven analysis. Reduces back-and-forth Q&A by suggesting defaults
that users can accept or override.

This is NOT caching (which was rejected). This is about:
- Analyzing data to suggest reasonable defaults
- Presenting "Accept or Discuss" options
- Early-exit when user agrees with data-driven suggestions
- Reducing conversation tokens through smart questioning
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class DefaultConfidence(Enum):
    """Confidence level in the suggested default"""
    HIGH = "high"       # >90% confidence, strong data support
    MEDIUM = "medium"   # 70-90% confidence, reasonable support
    LOW = "low"         # <70% confidence, weak support
    UNKNOWN = "unknown" # No data available for default


@dataclass
class SmartDefault:
    """
    A suggested default value with supporting rationale.

    Example:
        SmartDefault(
            question="Is the 14.5% EBITDA margin sustainable?",
            suggested_value="Yes",
            confidence=DefaultConfidence.HIGH,
            rationale="Margin has consistently improved: 4.6% → 9.5% → 14.5% over 3 years",
            data_points=["2020: 4.6%", "2021: 9.5%", "2022: 14.5%"],
            alternatives=["No, expect decline", "Discuss factors"]
        )
    """
    question: str
    suggested_value: Any
    confidence: DefaultConfidence
    rationale: str
    data_points: List[str]
    alternatives: List[str]
    user_can_override: bool = True


class SmartDefaultsEngine:
    """
    Generates intelligent defaults for financial analysis questions.

    Uses tiered data to analyze patterns and suggest defaults, reducing
    the need for lengthy back-and-forth questioning.
    """

    def __init__(self, tier1_summary: Dict[str, Any]):
        """
        Initialize with financial data summary.

        Args:
            tier1_summary: Tier 1 summary data (already in context)
        """
        self.tier1 = tier1_summary

    def generate_margin_sustainability_default(self) -> SmartDefault:
        """
        Suggest whether current margin is sustainable based on trend.

        Returns:
            SmartDefault with margin sustainability suggestion
        """
        annual_data = self.tier1.get('annual_summary', {})
        years = sorted([y for y in annual_data.keys() if y != 'metadata'])

        # Calculate margin trend
        margins = []
        for year in years:
            if 'ebitda_margin_pct' in annual_data[year]:
                margins.append({
                    'year': year,
                    'margin': annual_data[year]['ebitda_margin_pct']
                })

        if len(margins) < 2:
            return SmartDefault(
                question="Is the current EBITDA margin sustainable?",
                suggested_value="Unknown",
                confidence=DefaultConfidence.UNKNOWN,
                rationale="Insufficient historical data to assess trend",
                data_points=[],
                alternatives=["Yes", "No", "Discuss factors"]
            )

        # Analyze trend
        latest_margin = margins[-1]['margin']
        trend_improving = all(
            margins[i]['margin'] <= margins[i+1]['margin']
            for i in range(len(margins)-1)
        )

        if trend_improving and len(margins) >= 3:
            # Strong upward trend
            confidence = DefaultConfidence.HIGH
            suggested_value = "Yes"
            rationale = f"Margin has consistently improved over {len(margins)} years"
        elif trend_improving:
            confidence = DefaultConfidence.MEDIUM
            suggested_value = "Yes"
            rationale = "Margin shows improvement but limited history"
        else:
            confidence = DefaultConfidence.MEDIUM
            suggested_value = "Needs discussion"
            rationale = "Margin trend is inconsistent"

        data_points = [
            f"{m['year']}: {m['margin']:.1f}%"
            for m in margins
        ]

        return SmartDefault(
            question=f"Is the {latest_margin:.1f}% EBITDA margin sustainable?",
            suggested_value=suggested_value,
            confidence=confidence,
            rationale=rationale,
            data_points=data_points,
            alternatives=["Yes", "No", "Discuss factors"]
        )

    def generate_revenue_growth_default(self) -> SmartDefault:
        """
        Suggest revenue growth projection based on historical CAGR.

        Returns:
            SmartDefault with growth rate suggestion
        """
        annual_data = self.tier1.get('annual_summary', {})
        years = sorted([y for y in annual_data.keys() if y != 'metadata' and not y.endswith('_h1')])

        if len(years) < 2:
            return SmartDefault(
                question="What revenue CAGR should we project?",
                suggested_value="Unknown",
                confidence=DefaultConfidence.UNKNOWN,
                rationale="Insufficient historical data",
                data_points=[],
                alternatives=["Conservative", "Moderate", "Aggressive", "Specify %"]
            )

        # Calculate historical CAGR
        first_year_revenue = annual_data[years[0]]['revenue']
        last_year_revenue = annual_data[years[-1]]['revenue']
        num_years = len(years) - 1

        historical_cagr = ((last_year_revenue / first_year_revenue) ** (1 / num_years) - 1) * 100

        # Determine confidence
        if num_years >= 3:
            confidence = DefaultConfidence.HIGH
            rationale = f"Based on {num_years}-year historical CAGR"
        else:
            confidence = DefaultConfidence.MEDIUM
            rationale = f"Limited to {num_years}-year historical CAGR"

        # Suggest slightly conservative (0.8x historical)
        suggested_cagr = round(historical_cagr * 0.8, 1)

        data_points = [
            f"{year}: €{annual_data[year]['revenue']/1_000_000:.1f}M"
            for year in years
        ]
        data_points.append(f"Historical CAGR: {historical_cagr:.1f}%")

        return SmartDefault(
            question="What revenue CAGR should we project for next 3-5 years?",
            suggested_value=f"{suggested_cagr:.1f}%",
            confidence=confidence,
            rationale=f"{rationale} ({historical_cagr:.1f}%), discounted 20% for conservatism",
            data_points=data_points,
            alternatives=[
                f"Use full historical ({historical_cagr:.1f}%)",
                "More conservative",
                "Specify custom %"
            ]
        )

    def generate_normalization_default(self, tier2_expense: Dict[str, Any] = None) -> SmartDefault:
        """
        Suggest whether EBITDA normalization is needed.

        Args:
            tier2_expense: Optional Tier 2 expense detail (if loaded)

        Returns:
            SmartDefault for normalization decision
        """
        if tier2_expense:
            # Use Tier 2 data if available
            candidates = tier2_expense.get('normalization_candidates', [])

            if len(candidates) == 0:
                return SmartDefault(
                    question="Should we normalize EBITDA?",
                    suggested_value="No normalizations needed",
                    confidence=DefaultConfidence.HIGH,
                    rationale="No normalization candidates identified in detailed expense analysis",
                    data_points=[],
                    alternatives=["Accept", "Review potential adjustments"]
                )
            else:
                return SmartDefault(
                    question="Should we normalize EBITDA?",
                    suggested_value=f"Review {len(candidates)} candidates",
                    confidence=DefaultConfidence.MEDIUM,
                    rationale=f"Found {len(candidates)} potential normalization items",
                    data_points=[
                        f"{c['account']}: {c['flag']}"
                        for c in candidates[:3]
                    ],
                    alternatives=["Review each", "Skip normalizations", "Accept all"]
                )

        # Fallback to Tier 1 heuristics
        key_findings = self.tier1.get('key_findings', {})
        normalization_count = key_findings.get('normalization_candidates', 0)

        if normalization_count == 0:
            return SmartDefault(
                question="Should we normalize EBITDA?",
                suggested_value="No normalizations needed",
                confidence=DefaultConfidence.MEDIUM,
                rationale="Initial analysis found no obvious normalization candidates",
                data_points=[],
                alternatives=["Accept", "Deep dive into expenses"]
            )

        return SmartDefault(
            question="Should we normalize EBITDA?",
            suggested_value="Review candidates",
            confidence=DefaultConfidence.MEDIUM,
            rationale=f"Initial analysis flagged {normalization_count} potential items",
            data_points=[],
            alternatives=["Review details", "Skip normalizations"]
        )

    def generate_working_capital_default(self) -> SmartDefault:
        """
        Suggest whether working capital level is typical.

        Returns:
            SmartDefault for WC assessment
        """
        annual_data = self.tier1.get('annual_summary', {})
        latest_year = sorted([y for y in annual_data.keys() if not y.endswith('_h1')])[-1]

        if 'nwc_pct_revenue' not in annual_data[latest_year]:
            return SmartDefault(
                question="Is the working capital level typical?",
                suggested_value="Unknown",
                confidence=DefaultConfidence.UNKNOWN,
                rationale="Working capital data not available",
                data_points=[],
                alternatives=["Yes", "No", "Analyze in detail"]
            )

        nwc_pct = annual_data[latest_year]['nwc_pct_revenue']

        # Industry benchmark: 10-20% is typical for services/software
        if 10 <= nwc_pct <= 20:
            confidence = DefaultConfidence.HIGH
            suggested_value = "Yes, typical"
            rationale = f"NWC at {nwc_pct:.1f}% of revenue is within typical range (10-20%)"
        elif 5 <= nwc_pct < 10 or 20 < nwc_pct <= 25:
            confidence = DefaultConfidence.MEDIUM
            suggested_value = "Borderline"
            rationale = f"NWC at {nwc_pct:.1f}% of revenue is on the edge of typical range"
        else:
            confidence = DefaultConfidence.HIGH
            suggested_value = "No, unusual"
            rationale = f"NWC at {nwc_pct:.1f}% of revenue is outside typical range (10-20%)"

        return SmartDefault(
            question="Is the working capital level typical for this business?",
            suggested_value=suggested_value,
            confidence=confidence,
            rationale=rationale,
            data_points=[f"NWC: {nwc_pct:.1f}% of revenue", "Typical range: 10-20%"],
            alternatives=["Accept", "Analyze seasonality", "Deep dive"]
        )

    def generate_all_defaults(self) -> List[SmartDefault]:
        """
        Generate all applicable smart defaults for efficient questioning.

        Returns:
            List of SmartDefault objects
        """
        defaults = []

        # Core valuation questions
        defaults.append(self.generate_margin_sustainability_default())
        defaults.append(self.generate_revenue_growth_default())
        defaults.append(self.generate_normalization_default())
        defaults.append(self.generate_working_capital_default())

        return defaults

    def format_question_with_default(self, default: SmartDefault) -> str:
        """
        Format a question with smart default for presentation to user.

        Args:
            default: SmartDefault to format

        Returns:
            Formatted question string

        Example output:
            ```
            Q: Is the 14.5% EBITDA margin sustainable?

            📊 Suggested: Yes (High confidence)

            Rationale: Margin has consistently improved over 3 years
            Data: 2020: 4.6%, 2021: 9.5%, 2022: 14.5%

            Options:
            1. Accept suggestion (Yes)
            2. No, expect decline
            3. Discuss factors in detail

            →
            ```
        """
        confidence_icon = {
            DefaultConfidence.HIGH: "✓",
            DefaultConfidence.MEDIUM: "→",
            DefaultConfidence.LOW: "?",
            DefaultConfidence.UNKNOWN: "○"
        }

        icon = confidence_icon[default.confidence]
        conf_label = default.confidence.value.capitalize()

        output = f"\n{default.question}\n\n"
        output += f"{icon} Suggested: {default.suggested_value} ({conf_label} confidence)\n\n"
        output += f"Rationale: {default.rationale}\n"

        if default.data_points:
            output += f"Data: {', '.join(default.data_points)}\n"

        if default.user_can_override and default.alternatives:
            output += f"\nOptions:\n"
            output += f"1. Accept suggestion ({default.suggested_value})\n"
            for i, alt in enumerate(default.alternatives, 2):
                output += f"{i}. {alt}\n"

        output += "\n→ "

        return output


def create_smart_defaults_from_tier1(tier1_summary: Dict[str, Any]) -> List[SmartDefault]:
    """
    Convenience function to create smart defaults from Tier 1 data.

    Usage:
        >>> from core import TieredDataAccess
        >>> from core.smart_defaults import create_smart_defaults_from_tier1
        >>>
        >>> accessor = TieredDataAccess('/path/to/sandbox')
        >>> tier1 = accessor.load_tier1()
        >>> defaults = create_smart_defaults_from_tier1(tier1)
        >>>
        >>> for default in defaults:
        >>>     print(default.format_question_with_default(default))
        >>>     user_choice = input()  # User accepts or overrides

    Args:
        tier1_summary: Tier 1 summary data

    Returns:
        List of SmartDefault objects
    """
    engine = SmartDefaultsEngine(tier1_summary)
    return engine.generate_all_defaults()
