from projector_borrowing.domain.borrowing.exceptions.domain_error import DomainError


class InvalidBorrowingPeriod(DomainError):
    """BR1 - the borrowing period is not valid."""
