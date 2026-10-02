from projector_borrowing.domain.borrowing.exceptions.domain_error import DomainError


class InvalidLoanState(DomainError):
    """BR2 - the loan is not in a state that allows this change."""
