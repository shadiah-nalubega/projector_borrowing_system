"""Business-rule violations raised by the borrowing domain.

Each rule has its own exception, so a violation names the rule it broke.
"""


class DomainError(Exception):
    """Base class for every business-rule violation in the borrowing domain."""


class InvalidBorrowingPeriod(DomainError):
    """BR1 - the borrowing period is not valid."""


class InvalidLoanState(DomainError):
    """BR2 - the loan is not in a state that allows this change."""


class LoanLimitExceeded(DomainError):
    """BR3 - the borrower already holds the maximum number of loans."""


class NotEligible(DomainError):
    """BR4 - this borrower type may not borrow this projector category."""


class ProjectorNotAvailable(DomainError):
    """BR5 - the projector cannot be checked out because it is not available."""


class InvalidIdentifier(DomainError):
    """An id or asset tag is empty."""


class LoanNotFound(DomainError):
    """The borrower has no loan with the given id."""
