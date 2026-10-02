import pytest

from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.enums.borrower_type import BorrowerType
from projector_borrowing.domain.borrowing.exceptions.loan_limit_exceeded import (
    LoanLimitExceeded,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, BorrowerId


def test_T3_BR3_student_cannot_hold_a_second_loan(period):
    student = Borrower(BorrowerId("S001"), BorrowerType.STUDENT)
    student.request_loan(AssetTag("PRJ-001"), period)

    with pytest.raises(LoanLimitExceeded):
        student.request_loan(AssetTag("PRJ-003"), period)

    assert student.active_or_pending_loan_count() == 1
