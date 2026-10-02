import copy
from typing import Optional

from projector_borrowing.application.borrowing.repositories.borrower_repository import (
    BorrowerRepository,
)
from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.value_objects.ids import BorrowerId


class InMemoryBorrowerRepository(BorrowerRepository):
    """Keeps copies, like a real database: changes are lost unless saved."""

    def __init__(self) -> None:
        self._borrowers: dict[BorrowerId, Borrower] = {}

    def find_by_id(self, borrower_id: BorrowerId) -> Optional[Borrower]:
        borrower = self._borrowers.get(borrower_id)
        return copy.deepcopy(borrower) if borrower is not None else None

    def save(self, borrower: Borrower) -> None:
        self._borrowers[borrower.borrower_id] = copy.deepcopy(borrower)
