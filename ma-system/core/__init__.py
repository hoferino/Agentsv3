"""
Core Utilities - Tiered Data Architecture

System-wide utilities for 100% coverage with context efficiency.

Quick Start:
    >>> from core import query_account, validate_extraction
    >>> value = query_account('/path/to/sandbox', '440000', period='2022')
    >>> validate_extraction('/path/to/sandbox')
"""

from .data_access import (
    TieredDataAccess,
    query_account,
    search_accounts,
)

from .validation import (
    CoverageValidator,
    ValidationResult,
    validate_extraction,
    validate_quick,
)

from .smart_defaults import (
    SmartDefaultsEngine,
    SmartDefault,
    DefaultConfidence,
    create_smart_defaults_from_tier1,
)

__all__ = [
    # Data Access
    'TieredDataAccess',
    'query_account',
    'search_accounts',
    # Validation
    'CoverageValidator',
    'ValidationResult',
    'validate_extraction',
    'validate_quick',
    # Smart Defaults
    'SmartDefaultsEngine',
    'SmartDefault',
    'DefaultConfidence',
    'create_smart_defaults_from_tier1',
]

__version__ = '1.0.0'
