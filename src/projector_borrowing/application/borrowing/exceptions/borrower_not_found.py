from .application_error import ApplicationError


class BorrowerNotFound(ApplicationError):
    """BR6 - no borrower exists with the given id."""
