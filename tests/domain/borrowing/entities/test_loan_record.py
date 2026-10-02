import pytest

from projector_borrowing.domain.borrowing.entities.loan_record import LoanRecord
from projector_borrowing.domain.borrowing.enums.loan_status import LoanStatus
from projector_borrowing.domain.borrowing.exceptions.invalid_loan_state import (
    InvalidLoanState,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, LoanId


def test_T2_BR2_cancelled_loan_cannot_be_confirmed(period):
    loan = LoanRecord(LoanId("L1"), AssetTag("PRJ-001"), period)
    loan.cancel()

    with pytest.raises(InvalidLoanState):
        loan.activate()

    assert loan.status is LoanStatus.CANCELLED
