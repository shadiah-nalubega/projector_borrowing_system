from dataclasses import dataclass

from projector_borrowing.domain.borrowing.value_objects.borrowing_period import (
    BorrowingPeriod,
)
from projector_borrowing.domain.borrowing.value_objects.ids import (
    AssetTag,
    BorrowerId,
    LoanId,
)


@dataclass(frozen=True)
class LoanRequested:
    """Domain Event for BR5.

    Raised by Borrower (Aggregate A) after a PENDING loan is recorded. It asks
    Projector (Aggregate B) to be checked out.
    """

    loan_id: LoanId
    borrower_id: BorrowerId
    asset_tag: AssetTag
    period: BorrowingPeriod
