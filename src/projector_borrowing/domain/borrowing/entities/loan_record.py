from projector_borrowing.domain.borrowing.enums.loan_status import LoanStatus
from projector_borrowing.domain.borrowing.exceptions.invalid_loan_state import (
    InvalidLoanState,
)
from projector_borrowing.domain.borrowing.value_objects.borrowing_period import (
    BorrowingPeriod,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, LoanId


class LoanRecord:
    """Entity enforcing BR2. Child of the Borrower aggregate.

    Its identity is the LoanId: two loans for the same projector and the same
    dates are still different loans. Its state may only move
    PENDING -> ACTIVE or PENDING -> CANCELLED.
    """

    def __init__(self, loan_id: LoanId, asset_tag: AssetTag, period: BorrowingPeriod):
        self.loan_id = loan_id
        self.asset_tag = asset_tag
        self.period = period
        self.status = LoanStatus.PENDING

    def activate(self) -> None:
        self._ensure_pending("confirm")
        self.status = LoanStatus.ACTIVE

    def cancel(self) -> None:
        self._ensure_pending("cancel")
        self.status = LoanStatus.CANCELLED

    def is_active_or_pending(self) -> bool:
        return self.status in (LoanStatus.PENDING, LoanStatus.ACTIVE)

    def _ensure_pending(self, action: str) -> None:
        if self.status is not LoanStatus.PENDING:
            raise InvalidLoanState(
                f"Cannot {action} loan {self.loan_id}: it is {self.status.value}"
            )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LoanRecord) and other.loan_id == self.loan_id

    def __hash__(self) -> int:
        return hash(self.loan_id)
