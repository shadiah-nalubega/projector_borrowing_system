"""The handler for LoanRequested: the second use case, triggered by BR5."""

from __future__ import annotations

from projector_borrowing.application.borrowing.repositories import (
    BorrowerRepository,
    ProjectorRepository,
)
from projector_borrowing.domain.borrowing.events import LoanRequested
from projector_borrowing.domain.borrowing.exceptions import ProjectorNotAvailable


class MarkProjectorOnLoanHandler:
    """Carry the BR5 follow-up from Borrower (A) to Projector (B).

    The handler only coordinates. Projector decides whether it can be checked
    out, and Borrower decides whether the loan can be confirmed or cancelled
    (BR2). The aggregates never change each other directly.
    """

    def __init__(
        self,
        borrower_repository: BorrowerRepository,
        projector_repository: ProjectorRepository,
    ) -> None:
        self._borrowers = borrower_repository
        self._projectors = projector_repository

    def __call__(self, event: LoanRequested) -> None:
        """Check out the projector, then confirm or cancel the loan."""

        projector = self._projectors.find_by_asset_tag(event.asset_tag)
        borrower = self._borrowers.find_by_id(event.borrower_id)

        try:
            projector.checkout()
        except ProjectorNotAvailable:
            # Aggregate B refused, so the PENDING loan in Aggregate A is cancelled.
            borrower.cancel_loan(event.loan_id)
        else:
            self._projectors.save(projector)
            borrower.confirm_loan(event.loan_id)

        self._borrowers.save(borrower)
