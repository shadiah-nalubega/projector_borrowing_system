from .domain_error import DomainError


class LoanNotFound(DomainError):
    """The borrower has no loan with the given id."""
