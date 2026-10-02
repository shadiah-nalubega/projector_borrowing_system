from .domain_error import DomainError


class InvalidLoanState(DomainError):
    """BR2 - the loan is not in a state that allows this change."""
