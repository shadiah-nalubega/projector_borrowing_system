from projector_borrowing.domain.borrowing.exceptions.domain_error import DomainError


class InvalidIdentifier(DomainError):
    """An id or asset tag is empty."""
