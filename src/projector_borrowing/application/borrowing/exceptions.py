"""Use-case failures that are not domain rule violations."""


class ApplicationError(Exception):
    """Base class for application-layer failures."""


class BorrowerNotFound(ApplicationError):
    """BR6 - no borrower exists with the given id."""


class ProjectorNotFound(ApplicationError):
    """BR6 - no projector exists with the given asset tag."""
