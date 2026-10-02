"""The BorrowerRepository contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from projector_borrowing.domain.borrowing import Borrower
from projector_borrowing.domain.borrowing.value_objects import BorrowerId


class BorrowerRepository(ABC):
    """Store and retrieve whole Borrower aggregates, including their loans.

    There is no LoanRecord repository: a LoanRecord is only reached through
    its Borrower, so it is saved together with it.
    """

    @abstractmethod
    def find_by_id(self, borrower_id: BorrowerId) -> Borrower | None:
        """Return the borrower, or ``None`` when no borrower has this id."""

    @abstractmethod
    def save(self, borrower: Borrower) -> None:
        """Store the borrower and all of its loans."""
