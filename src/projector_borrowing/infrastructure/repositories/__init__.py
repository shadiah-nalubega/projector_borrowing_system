"""In-memory implementations of the repository contracts."""

from .in_memory_borrower_repository import InMemoryBorrowerRepository
from .in_memory_projector_repository import InMemoryProjectorRepository

__all__ = ["InMemoryBorrowerRepository", "InMemoryProjectorRepository"]
