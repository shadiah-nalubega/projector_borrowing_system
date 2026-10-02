from datetime import date

import pytest

from projector_borrowing.application.borrowing.dto.borrow_projector_request import (
    BorrowProjectorRequest,
)
from projector_borrowing.application.borrowing.exceptions import BorrowerNotFound
from projector_borrowing.domain.borrowing.enums.loan_status import LoanStatus
from projector_borrowing.domain.borrowing.enums.projector_category import (
    ProjectorCategory,
)
from projector_borrowing.domain.borrowing.enums.projector_status import ProjectorStatus
from projector_borrowing.domain.borrowing.projector import Projector
from projector_borrowing.domain.borrowing.value_objects.ids import (
    AssetTag,
    BorrowerId,
    LoanId,
)

START = date(2026, 10, 5)
END = date(2026, 10, 8)


def test_T6_BR6_unknown_borrower_is_rejected(service, projectors):
    request = BorrowProjectorRequest("NOBODY", "PRJ-001", START, END)

    with pytest.raises(BorrowerNotFound):
        service.borrow_projector(request)

    projector = projectors.find_by_asset_tag(AssetTag("PRJ-001"))
    assert projector.status is ProjectorStatus.AVAILABLE


def test_T7_main_use_case_activates_loan_and_checks_out_projector(
    service, borrowers, projectors
):
    request = BorrowProjectorRequest("S001", "PRJ-001", START, END)

    response = service.borrow_projector(request)

    assert response.loan_status == "ACTIVE"
    assert response.projector_status == "ON_LOAN"
    # The event was handled: Aggregate B changed.
    assert projectors.find_by_asset_tag(AssetTag("PRJ-001")).status is ProjectorStatus.ON_LOAN
    loan = borrowers.find_by_id(BorrowerId("S001")).get_loan(LoanId(response.loan_id))
    assert loan.status is LoanStatus.ACTIVE


def test_T8_projector_already_on_loan_rejects_checkout_and_loan_is_cancelled(
    service, borrowers, projectors
):
    projectors.save(
        Projector(AssetTag("PRJ-001"), ProjectorCategory.STANDARD, ProjectorStatus.ON_LOAN)
    )
    request = BorrowProjectorRequest("S001", "PRJ-001", START, END)

    response = service.borrow_projector(request)

    assert response.loan_status == "CANCELLED"
    assert response.projector_status == "ON_LOAN"
    borrower = borrowers.find_by_id(BorrowerId("S001"))
    assert borrower.get_loan(LoanId(response.loan_id)).status is LoanStatus.CANCELLED
    assert borrower.active_or_pending_loan_count() == 0
