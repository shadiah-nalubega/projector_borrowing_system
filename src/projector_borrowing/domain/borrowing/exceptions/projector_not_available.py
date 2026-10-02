from .domain_error import DomainError


class ProjectorNotAvailable(DomainError):
    """BR5 - the projector cannot be checked out because it is not available."""
