from .domain_error import DomainError


class LoanLimitExceeded(DomainError):
    """BR3 - the borrower already holds the maximum number of loans."""
