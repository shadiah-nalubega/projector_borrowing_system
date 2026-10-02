class ApplicationError(Exception):
    """Base class for use-case failures that are not domain rule violations."""


class BorrowerNotFound(ApplicationError):
    """BR6 - no borrower exists with the given id."""


class ProjectorNotFound(ApplicationError):
    """BR6 - no projector exists with the given asset tag."""
