"""
Data Access Utilities for Tiered Financial Data Architecture

Provides query functions for accessing tiered financial data without
loading entire datasets into context.

Part of the 100% Coverage Strategy - Zero Information Loss architecture.
See: /ma-system/docs/100-percent-coverage-strategy.md
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union


class TieredDataAccess:
    """
    Access tiered financial data efficiently.

    Three-tier architecture:
    - Tier 1 (Summary): Always loaded, 2k tokens
    - Tier 2 (Detailed): On-demand, 20k tokens per file
    - Tier 3 (Raw/Complete): Query-only, never fully loaded
    """

    def __init__(self, sandbox_path: str):
        """
        Initialize data access layer.

        Args:
            sandbox_path: Path to sandbox directory containing tier1/, tier2/, tier3/
        """
        self.sandbox_path = Path(sandbox_path)
        self.tier1_path = self.sandbox_path / "tier1" / "summary.json"
        self.tier2_path = self.sandbox_path / "tier2"
        self.tier3_path = self.sandbox_path / "tier3" / "raw_accounts_database.json"

        # Track which Tier 2 files are loaded
        self.tier2_loaded = {}

    def load_tier1(self) -> Dict[str, Any]:
        """
        Load Tier 1 summary data.

        Always called on agent activation.
        Cost: ~2k tokens

        Returns:
            Dictionary with annual_summary, key_findings, data_available
        """
        if not self.tier1_path.exists():
            raise FileNotFoundError(
                f"Tier 1 summary not found at {self.tier1_path}. "
                "Run data extraction workflow first."
            )

        with open(self.tier1_path, 'r') as f:
            return json.load(f)

    def load_tier2_file(self, filename: str) -> Dict[str, Any]:
        """
        Load specific Tier 2 detail file on-demand.

        Cost: ~20k tokens per file

        Args:
            filename: Name of tier2 file (e.g., 'revenue_detail.json')

        Returns:
            Detailed breakdown data for specific category
        """
        file_path = self.tier2_path / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Tier 2 file not found: {file_path}. "
                "Available files: {list(self.tier2_path.glob('*.json'))}"
            )

        # Load file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Track that this file is now in context
        self.tier2_loaded[filename] = True

        return data

    def query_tier3_account(
        self,
        account_number: str,
        period: Optional[str] = None,
        data_type: str = 'pl'
    ) -> Union[Dict[str, Any], float]:
        """
        Query specific account from Tier 3 without loading entire database.

        This is the key to 100% coverage without context explosion.
        Cost: ~50-200 tokens (just the specific account data)

        Args:
            account_number: Account number to query (e.g., '440000', '473600')
            period: Optional period filter (e.g., '2022', '2021.march')
                   If None, returns totals by year
            data_type: Type of accounts to search ('pl' or 'balance_sheet')

        Returns:
            Account data (totals dict if no period, specific value if period specified)

        Examples:
            >>> query_tier3_account('440000')
            {'2020': 11500000, '2021': 14200000, '2022': 18900000}

            >>> query_tier3_account('473600', period='2021.march')
            0
        """
        if not self.tier3_path.exists():
            raise FileNotFoundError(
                f"Tier 3 database not found: {self.tier3_path}. "
                "Run data extraction workflow first."
            )

        # Load Tier 3 database
        with open(self.tier3_path, 'r') as f:
            raw_db = json.load(f)

        # Determine which account list to search
        account_list_key = f"{data_type}_accounts"
        if account_list_key not in raw_db:
            raise ValueError(
                f"Invalid data_type '{data_type}'. "
                f"Available: {list(raw_db.keys())}"
            )

        accounts = raw_db[account_list_key]

        # Find specific account
        account_data = None
        for acc in accounts:
            if str(acc.get('account', '')).strip() == str(account_number).strip():
                account_data = acc
                break

        if account_data is None:
            raise ValueError(
                f"Account {account_number} not found in Tier 3 {data_type} accounts. "
                f"Total accounts available: {len(accounts)}"
            )

        # Return requested data
        if period is None:
            # Return all totals
            return account_data.get('totals', {})
        else:
            # Parse period (e.g., '2021.march' -> year='2021', month='march')
            if '.' in period:
                year, month = period.split('.')
                monthly_data = account_data.get('monthly_data', {})
                if year not in monthly_data:
                    raise ValueError(f"Year {year} not found for account {account_number}")
                if month not in monthly_data[year]:
                    raise ValueError(
                        f"Month {month} not found for account {account_number} in {year}"
                    )
                return monthly_data[year][month]
            else:
                # Just year requested
                return account_data.get('totals', {}).get(period)

    def search_tier3_accounts(
        self,
        search_term: str,
        data_type: str = 'pl'
    ) -> List[Dict[str, Any]]:
        """
        Search Tier 3 accounts by description keyword.

        Useful for finding accounts without knowing exact account number.

        Args:
            search_term: Keyword to search in account descriptions
            data_type: Type of accounts to search ('pl' or 'balance_sheet')

        Returns:
            List of matching accounts with their totals

        Example:
            >>> search_tier3_accounts('salary')
            [
                {'account': '602000', 'description': 'Salaries', 'totals': {...}},
                {'account': '602300', 'description': 'Profit-sharing salary', 'totals': {...}}
            ]
        """
        if not self.tier3_path.exists():
            raise FileNotFoundError(f"Tier 3 database not found: {self.tier3_path}")

        with open(self.tier3_path, 'r') as f:
            raw_db = json.load(f)

        account_list_key = f"{data_type}_accounts"
        accounts = raw_db.get(account_list_key, [])

        # Search for matching accounts
        matches = []
        search_lower = search_term.lower()

        for acc in accounts:
            description = str(acc.get('description', '')).lower()
            if search_lower in description:
                matches.append({
                    'account': acc.get('account'),
                    'description': acc.get('description'),
                    'totals': acc.get('totals', {})
                })

        return matches

    def get_tier2_trigger(self, question: str) -> Optional[str]:
        """
        Determine which Tier 2 file is needed based on question content.

        Args:
            question: User's question

        Returns:
            Filename of required Tier 2 file, or None if Tier 1 sufficient

        Example:
            >>> get_tier2_trigger("What are the main revenue sources?")
            'revenue_detail.json'
        """
        question_lower = question.lower()

        # Tier 2 file triggers (from financial-analyst.md)
        triggers = {
            'revenue_detail.json': [
                'revenue breakdown', 'revenue quality', 'revenue sources',
                'revenue composition', 'revenue line items', 'revenue concentration'
            ],
            'expense_detail.json': [
                'expense categories', 'normalization', 'cost structure',
                'expense breakdown', 'operating expenses', 'personnel costs'
            ],
            'working_capital_detail.json': [
                'working capital', 'nwc', 'dso', 'dpo', 'cash conversion',
                'receivables', 'payables', 'inventory'
            ],
            'balance_sheet_detail.json': [
                'balance sheet', 'assets', 'liabilities', 'equity',
                'debt', 'cash position'
            ]
        }

        # Check each file's triggers
        for filename, trigger_phrases in triggers.items():
            if any(phrase in question_lower for phrase in trigger_phrases):
                return filename

        return None

    def answer_question(self, question: str, tier1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligent question answering using tiered data.

        Strategy:
        1. Try to answer from Tier 1 (already in context)
        2. If need details, load appropriate Tier 2 file
        3. If very specific, query Tier 3

        Args:
            question: User's question
            tier1_data: Already-loaded Tier 1 summary

        Returns:
            Dictionary with 'answer', 'source_tier', 'context_cost'
        """
        # This would contain actual logic to answer from tiers
        # For now, returns metadata about which tier would be used

        result = {
            'question': question,
            'source_tier': None,
            'file_needed': None,
            'context_cost_tokens': 0
        }

        # Check if Tier 2 needed
        tier2_file = self.get_tier2_trigger(question)

        if tier2_file:
            result['source_tier'] = 'tier2'
            result['file_needed'] = tier2_file
            result['context_cost_tokens'] = 20000
        else:
            result['source_tier'] = 'tier1'
            result['file_needed'] = 'summary.json'
            result['context_cost_tokens'] = 0  # Already loaded

        return result


# Convenience functions for direct usage

def query_account(
    sandbox_path: str,
    account_number: str,
    period: Optional[str] = None,
    data_type: str = 'pl'
) -> Union[Dict[str, Any], float]:
    """
    Quick function to query a specific account.

    Usage:
        >>> from core.data_access import query_account
        >>> query_account('/path/to/sandbox', '440000', period='2022')
        18900000
    """
    accessor = TieredDataAccess(sandbox_path)
    return accessor.query_tier3_account(account_number, period, data_type)


def search_accounts(
    sandbox_path: str,
    search_term: str,
    data_type: str = 'pl'
) -> List[Dict[str, Any]]:
    """
    Quick function to search accounts by keyword.

    Usage:
        >>> from core.data_access import search_accounts
        >>> search_accounts('/path/to/sandbox', 'salary')
        [{'account': '602000', 'description': 'Salaries', ...}]
    """
    accessor = TieredDataAccess(sandbox_path)
    return accessor.search_tier3_accounts(search_term, data_type)
