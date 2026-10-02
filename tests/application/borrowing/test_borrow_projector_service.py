from datetime import date

import pytest

from projector_borrowing.application.borrowing.dto import BorrowProjectorRequest
from projector_borrowing.application.borrowing.exceptions import BorrowerNotFound
from projector_borrowing.application.borrowing.services import BorrowProjectorService
from projector_borrowing.domain.borrowing import Projector
from projector_borrowing.domain.borrowing.enums import (
    LoanStatus,
    ProjectorCategory,
    ProjectorStatus,
)
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    LoanId,
)
from projector_borrowing.infrastructure.repositories import (
    InMemoryBorrowerRepository,
    InMemoryProjectorRepository,
)

START = date(2026, 10, 5)
END = date(2026, 10, 8)


def test_T6_BR6_unknown_borrower_is_rejected(
    service: BorrowProjectorService,
    projectors: InMemoryProjectorRepository,
) -> None:
    # Arrange
    request = BorrowProjectorRequest("NOBODY", "PRJ-001", START, END)

    # Act
    with pytest.raises(BorrowerNotFound) as exception_info:
        service.borrow_projector(request)

    # Assert
    assert "NOBODY" in str(exception_info.value)
    projector = projectors.find_by_asset_tag(AssetTag("PRJ-001"))
    assert projector.status is ProjectorStatus.AVAILABLE


def test_T7_main_use_case_activates_loan_and_checks_out_projector(
    service: BorrowProjectorService,
    borrowers: InMemoryBorrowerRepository,
    projectors: InMemoryProjectorRepository,
) -> None:
    # Arrange
    request = BorrowProjectorRequest("S001", "PRJ-001", START, END)

    # Act
    response = service.borrow_projector(request)

    # Assert: the returned outcome.
    assert response.loan_status == "ACTIVE"
    assert response.projector_status == "ON_LOAN"
    # Assert: the event was handled and Aggregate B changed.
    projector = projectors.find_by_asset_tag(AssetTag("PRJ-001"))
    assert projector.status is ProjectorStatus.ON_LOAN
    loan = borrowers.find_by_id(BorrowerId("S001")).get_loan(LoanId(response.loan_id))
    assert loan.status is LoanStatus.ACTIVE


def test_T8_projector_already_on_loan_rejects_checkout_and_loan_is_cancelled(
    service: BorrowProjectorService,
    borrowers: InMemoryBorrowerRepository,
    projectors: InMemoryProjectorRepository,
) -> None:
    # Arrange
    projectors.save(
        Projector(AssetTag("PRJ-001"), ProjectorCategory.STANDARD, ProjectorStatus.ON_LOAN)
    )
    request = BorrowProjectorRequest("S001", "PRJ-001", START, END)

    # Act
    response = service.borrow_projector(request)

    # Assert: the returned outcome.
    assert response.loan_status == "CANCELLED"
    assert response.projector_status == "ON_LOAN"
    # Assert: the final state. Aggregate B refused, so the loan was cancelled.
    borrower = borrowers.find_by_id(BorrowerId("S001"))
    assert borrower.get_loan(LoanId(response.loan_id)).status is LoanStatus.CANCELLED
    assert borrower.active_or_pending_loan_count() == 0
