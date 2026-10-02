import uuid

from projector_borrowing.domain.borrowing.entities.loan_record import LoanRecord
from projector_borrowing.domain.borrowing.enums.borrower_type import BorrowerType
from projector_borrowing.domain.borrowing.events.loan_requested import LoanRequested
from projector_borrowing.domain.borrowing.exceptions.loan_limit_exceeded import (
    LoanLimitExceeded,
)
from projector_borrowing.domain.borrowing.value_objects.borrowing_period import (
    BorrowingPeriod,
)
from projector_borrowing.domain.borrowing.value_objects.ids import (
    AssetTag,
    BorrowerId,
    LoanId,
)

LOAN_LIMITS = {
    BorrowerType.STUDENT: 1,
    BorrowerType.STAFF: 3,
}


class Borrower:
    """Aggregate Root (Aggregate A) enforcing BR3.

    Invariant: a borrower never holds more active or pending loans than the
    limit for their type. LoanRecords are only changed through this root, so
    the invariant cannot be bypassed.
    """

    def __init__(self, borrower_id: BorrowerId, borrower_type: BorrowerType):
        self.borrower_id = borrower_id
        self.borrower_type = borrower_type
        self._loans: list[LoanRecord] = []

    @property
    def loans(self) -> tuple[LoanRecord, ...]:
        return tuple(self._loans)

    def request_loan(self, asset_tag: AssetTag, period: BorrowingPeriod) -> LoanRequested:
        limit = LOAN_LIMITS[self.borrower_type]
        if self.active_or_pending_loan_count() >= limit:
            raise LoanLimitExceeded(
                f"{self.borrower_type.value} borrowers may hold at most {limit} loan(s)"
            )
        loan = LoanRecord(LoanId(uuid.uuid4().hex[:8]), asset_tag, period)
        self._loans.append(loan)
        return LoanRequested(loan.loan_id, self.borrower_id, asset_tag, period)

    def confirm_loan(self, loan_id: LoanId) -> None:
        self.get_loan(loan_id).activate()

    def cancel_loan(self, loan_id: LoanId) -> None:
        self.get_loan(loan_id).cancel()

    def active_or_pending_loan_count(self) -> int:
        return sum(1 for loan in self._loans if loan.is_active_or_pending())

    def get_loan(self, loan_id: LoanId) -> LoanRecord:
        for loan in self._loans:
            if loan.loan_id == loan_id:
                return loan
        raise KeyError(f"Borrower {self.borrower_id} has no loan {loan_id}")
