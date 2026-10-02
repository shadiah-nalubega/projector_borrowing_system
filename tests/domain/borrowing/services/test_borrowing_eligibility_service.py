import pytest

from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.enums.borrower_type import BorrowerType
from projector_borrowing.domain.borrowing.enums.projector_category import (
    ProjectorCategory,
)
from projector_borrowing.domain.borrowing.exceptions.not_eligible import NotEligible
from projector_borrowing.domain.borrowing.projector import Projector
from projector_borrowing.domain.borrowing.services.borrowing_eligibility_service import (
    BorrowingEligibilityService,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, BorrowerId


def test_T4_BR4_student_is_not_eligible_for_premium_projector():
    service = BorrowingEligibilityService()
    student = Borrower(BorrowerId("S001"), BorrowerType.STUDENT)
    staff = Borrower(BorrowerId("T001"), BorrowerType.STAFF)
    premium = Projector(AssetTag("PRJ-002"), ProjectorCategory.PREMIUM)

    assert service.check_eligibility(student, premium) is False
    assert service.check_eligibility(staff, premium) is True

    with pytest.raises(NotEligible):
        service.ensure_eligible(student, premium)
