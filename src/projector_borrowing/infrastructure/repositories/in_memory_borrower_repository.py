"""An in-memory BorrowerRepository."""

from __future__ import annotations

import copy

from projector_borrowing.application.borrowing.repositories import BorrowerRepository
from projector_borrowing.domain.borrowing import Borrower
from projector_borrowing.domain.borrowing.value_objects import BorrowerId


class InMemoryBorrowerRepository(BorrowerRepository):
    """Keep Borrower aggregates in a dictionary.

    Copies are stored and returned, like a real database: changes to a
    borrower are lost unless ``save`` is called.
    """

    def __init__(self) -> None:
        self._borrowers: dict[BorrowerId, Borrower] = {}

    def find_by_id(self, borrower_id: BorrowerId) -> Borrower | None:
        borrower = self._borrowers.get(borrower_id)
        return copy.deepcopy(borrower) if borrower is not None else None

    def save(self, borrower: Borrower) -> None:
        self._borrowers[borrower.borrower_id] = copy.deepcopy(borrower)
