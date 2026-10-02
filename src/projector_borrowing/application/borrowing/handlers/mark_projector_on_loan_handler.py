from projector_borrowing.application.borrowing.repositories.borrower_repository import (
    BorrowerRepository,
)
from projector_borrowing.application.borrowing.repositories.projector_repository import (
    ProjectorRepository,
)
from projector_borrowing.domain.borrowing.events.loan_requested import LoanRequested
from projector_borrowing.domain.borrowing.exceptions.projector_not_available import (
    ProjectorNotAvailable,
)


class MarkProjectorOnLoanHandler:
    """Handles LoanRequested (BR5): Aggregate A -> event -> Aggregate B.

    Asks the Projector to check itself out. The Projector decides using its
    own rule. The handler then confirms or cancels the loan on the Borrower.
    """

    def __init__(
        self,
        borrower_repository: BorrowerRepository,
        projector_repository: ProjectorRepository,
    ):
        self._borrowers = borrower_repository
        self._projectors = projector_repository

    def __call__(self, event: LoanRequested) -> None:
        projector = self._projectors.find_by_asset_tag(event.asset_tag)
        borrower = self._borrowers.find_by_id(event.borrower_id)

        try:
            projector.checkout()
        except ProjectorNotAvailable:
            borrower.cancel_loan(event.loan_id)
        else:
            self._projectors.save(projector)
            borrower.confirm_loan(event.loan_id)

        self._borrowers.save(borrower)
