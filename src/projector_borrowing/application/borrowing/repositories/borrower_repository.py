from abc import ABC, abstractmethod
from typing import Optional

from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.value_objects.ids import BorrowerId


class BorrowerRepository(ABC):
    """Stores the Borrower aggregate, including its LoanRecords."""

    @abstractmethod
    def find_by_id(self, borrower_id: BorrowerId) -> Optional[Borrower]: ...

    @abstractmethod
    def save(self, borrower: Borrower) -> None: ...
