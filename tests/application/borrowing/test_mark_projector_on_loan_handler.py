from projector_borrowing.application.borrowing.handlers.mark_projector_on_loan_handler import (
    MarkProjectorOnLoanHandler,
)
from projector_borrowing.domain.borrowing.enums.loan_status import LoanStatus
from projector_borrowing.domain.borrowing.enums.projector_status import ProjectorStatus
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, BorrowerId


def test_T5_BR5_loan_requested_event_checks_out_the_projector(
    borrowers, projectors, period
):
    borrower = borrowers.find_by_id(BorrowerId("S001"))
    event = borrower.request_loan(AssetTag("PRJ-001"), period)
    borrowers.save(borrower)

    MarkProjectorOnLoanHandler(borrowers, projectors)(event)

    projector = projectors.find_by_asset_tag(AssetTag("PRJ-001"))
    assert projector.status is ProjectorStatus.ON_LOAN
    loan = borrowers.find_by_id(BorrowerId("S001")).get_loan(event.loan_id)
    assert loan.status is LoanStatus.ACTIVE
