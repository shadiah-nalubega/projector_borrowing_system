from projector_borrowing.application.borrowing.handlers import MarkProjectorOnLoanHandler
from projector_borrowing.domain.borrowing.enums import LoanStatus, ProjectorStatus
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
)
from projector_borrowing.infrastructure.repositories import (
    InMemoryBorrowerRepository,
    InMemoryProjectorRepository,
)


def test_T5_BR5_loan_requested_event_checks_out_the_projector(
    borrowers: InMemoryBorrowerRepository,
    projectors: InMemoryProjectorRepository,
    period: BorrowingPeriod,
) -> None:
    # Arrange
    borrower = borrowers.find_by_id(BorrowerId("S001"))
    event = borrower.request_loan(AssetTag("PRJ-001"), period)
    borrowers.save(borrower)
    handler = MarkProjectorOnLoanHandler(borrowers, projectors)

    # Act
    handler(event)

    # Assert
    projector = projectors.find_by_asset_tag(AssetTag("PRJ-001"))
    loan = borrowers.find_by_id(BorrowerId("S001")).get_loan(event.loan_id)
    assert projector.status is ProjectorStatus.ON_LOAN
    assert loan.status is LoanStatus.ACTIVE
