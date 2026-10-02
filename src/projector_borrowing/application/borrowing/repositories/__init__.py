"""Repository contracts used by the borrowing use cases.

The application layer owns these abstractions. Infrastructure provides the
implementations, so the dependency points inward.
"""

from .borrower_repository import BorrowerRepository
from .projector_repository import ProjectorRepository

__all__ = ["BorrowerRepository", "ProjectorRepository"]
