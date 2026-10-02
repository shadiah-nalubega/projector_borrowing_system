from typing import Optional

from projector_borrowing.application.borrowing.repositories.borrower_repository import (
    BorrowerRepository,
)
from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.value_objects.ids import BorrowerId


class InMemoryBorrowerRepository(BorrowerRepository):
    def __init__(self) -> None:
        self._borrowers: dict[BorrowerId, Borrower] = {}

    def find_by_id(self, borrower_id: BorrowerId) -> Optional[Borrower]:
        return self._borrowers.get(borrower_id)

    def save(self, borrower: Borrower) -> None:
        self._borrowers[borrower.borrower_id] = borrower
