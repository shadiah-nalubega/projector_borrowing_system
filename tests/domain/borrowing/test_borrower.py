import pytest

from projector_borrowing.domain.borrowing import Borrower
from projector_borrowing.domain.borrowing.enums import BorrowerType
from projector_borrowing.domain.borrowing.exceptions import LoanLimitExceeded
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
)


def test_T3_BR3_student_cannot_hold_a_second_loan(period: BorrowingPeriod) -> None:
    # Arrange
    student = Borrower(BorrowerId("S001"), BorrowerType.STUDENT)
    student.request_loan(AssetTag("PRJ-001"), period)

    # Act
    with pytest.raises(LoanLimitExceeded) as exception_info:
        student.request_loan(AssetTag("PRJ-003"), period)

    # Assert
    assert "at most 1 loan" in str(exception_info.value)
    assert student.active_or_pending_loan_count() == 1
