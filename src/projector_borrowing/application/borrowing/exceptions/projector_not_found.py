from .application_error import ApplicationError


class ProjectorNotFound(ApplicationError):
    """BR6 - no projector exists with the given asset tag."""
