import pytest

from projector_borrowing.domain.borrowing import Borrower
from projector_borrowing.domain.borrowing.enums import BorrowerType, LoanStatus
from projector_borrowing.domain.borrowing.exceptions import InvalidLoanState
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
)


def test_T2_BR2_cancelled_loan_cannot_be_confirmed(period: BorrowingPeriod) -> None:
    # Arrange
    borrower = Borrower(BorrowerId("S001"), BorrowerType.STUDENT)
    event = borrower.request_loan(AssetTag("PRJ-001"), period)
    borrower.cancel_loan(event.loan_id)

    # Act
    with pytest.raises(InvalidLoanState) as exception_info:
        borrower.confirm_loan(event.loan_id)

    # Assert
    assert "it is CANCELLED" in str(exception_info.value)
    assert borrower.get_loan(event.loan_id).status is LoanStatus.CANCELLED
