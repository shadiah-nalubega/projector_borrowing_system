from projector_borrowing.domain.borrowing.exceptions.domain_error import DomainError


class NotEligible(DomainError):
    """BR4 - this borrower type may not borrow this projector category."""
