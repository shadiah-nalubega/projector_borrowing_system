import pytest

from projector_borrowing.domain.borrowing import Borrower, Projector
from projector_borrowing.domain.borrowing.enums import BorrowerType, ProjectorCategory
from projector_borrowing.domain.borrowing.exceptions import NotEligible
from projector_borrowing.domain.borrowing.services import BorrowingEligibilityService
from projector_borrowing.domain.borrowing.value_objects import AssetTag, BorrowerId


def test_T4_BR4_student_is_not_eligible_for_premium_projector() -> None:
    # Arrange
    service = BorrowingEligibilityService()
    student = Borrower(BorrowerId("S001"), BorrowerType.STUDENT)
    staff = Borrower(BorrowerId("T001"), BorrowerType.STAFF)
    premium = Projector(AssetTag("PRJ-002"), ProjectorCategory.PREMIUM)

    # Act
    student_is_eligible = service.check_eligibility(student, premium)
    staff_is_eligible = service.check_eligibility(staff, premium)

    # Assert
    assert not student_is_eligible
    assert staff_is_eligible
    with pytest.raises(NotEligible):
        service.ensure_eligible(student, premium)
