"""An in-memory BorrowerRepository."""

from __future__ import annotations

from projector_borrowing.application.borrowing.repositories import BorrowerRepository
from projector_borrowing.domain.borrowing import Borrower
from projector_borrowing.domain.borrowing.value_objects import BorrowerId

from .in_memory_store import InMemoryStore


class InMemoryBorrowerRepository(BorrowerRepository):
    """Keep Borrower aggregates, with their loans, in memory."""

    def __init__(self) -> None:
        self._store: InMemoryStore[BorrowerId, Borrower] = InMemoryStore()

    def find_by_id(self, borrower_id: BorrowerId) -> Borrower | None:
        return self._store.get(borrower_id)

    def save(self, borrower: Borrower) -> None:
        self._store.put(borrower.borrower_id, borrower)
