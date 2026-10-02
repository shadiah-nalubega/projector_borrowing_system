"""Use-case failures that are not domain rule violations."""

from .application_error import ApplicationError
from .borrower_not_found import BorrowerNotFound
from .projector_not_found import ProjectorNotFound

__all__ = ["ApplicationError", "BorrowerNotFound", "ProjectorNotFound"]
