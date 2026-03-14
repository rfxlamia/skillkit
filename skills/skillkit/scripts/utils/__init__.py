"""
Shared utilities for skillkit automation scripts.

Modules:
- output_formatter: Standardized JSON/text output (v1.0)
- budget_tracker: File content budget enforcement (v1.2)
- reference_validator: Cross-reference validation (v1.2)
"""

from .output_formatter import (
    add_format_argument,
    output_json,
    output_error,
    format_success_response,
    format_error_response
)

from .budget_tracker import (
    FileContentBudget,
    BudgetExceeded,
    TokenCounter,
    create_budget,
    STANDARD_BUDGETS
)

from .reference_validator import (
    CrossReferenceValidator,
    SkillPackageValidator,
    ValidationResult
)

__all__ = [
    # Output formatting (v1.0)
    'add_format_argument',
    'output_json',
    'output_error',
    'format_success_response',
    'format_error_response',
    # Budget tracking (v1.2)
    'FileContentBudget',
    'BudgetExceeded',
    'TokenCounter',
    'create_budget',
    'STANDARD_BUDGETS',
    # Reference validation (v1.2)
    'CrossReferenceValidator',
    'SkillPackageValidator',
    'ValidationResult'
]
