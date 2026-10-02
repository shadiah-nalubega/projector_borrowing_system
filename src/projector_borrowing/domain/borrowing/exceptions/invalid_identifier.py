from .domain_error import DomainError


class InvalidIdentifier(DomainError):
    """An id or asset tag is empty."""
