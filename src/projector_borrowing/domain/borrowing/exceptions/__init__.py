"""Business-rule violations raised by the borrowing domain."""

from .domain_error import DomainError
from .invalid_borrowing_period import InvalidBorrowingPeriod
from .invalid_identifier import InvalidIdentifier
from .invalid_loan_state import InvalidLoanState
from .loan_limit_exceeded import LoanLimitExceeded
from .loan_not_found import LoanNotFound
from .not_eligible import NotEligible
from .projector_not_available import ProjectorNotAvailable

__all__ = [
    "DomainError",
    "InvalidBorrowingPeriod",
    "InvalidIdentifier",
    "InvalidLoanState",
    "LoanLimitExceeded",
    "LoanNotFound",
    "NotEligible",
    "ProjectorNotAvailable",
]
