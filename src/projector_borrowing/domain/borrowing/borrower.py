"""The Borrower aggregate root (Aggregate A). It enforces BR3.

An aggregate is a group of domain objects that must remain consistent together.
The aggregate root is the only object that outside code should use to change that
group. Here, Borrower protects the loan limit across all of its LoanRecords.
"""

from __future__ import annotations

import uuid

from projector_borrowing.domain.borrowing.entities import LoanRecord
from projector_borrowing.domain.borrowing.enums import BorrowerType
from projector_borrowing.domain.borrowing.events import LoanRequested
from projector_borrowing.domain.borrowing.exceptions import (
    LoanLimitExceeded,
    LoanNotFound,
)
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
    LoanId,
)


class Borrower:
    """Own LoanRecord entities and keep the borrower within their loan limit.

    BR3: a borrower never holds more active or pending loans than the limit for
    their type. Loans are only created and changed through this root, so the
    invariant cannot be bypassed.
    """

    # The loan limit for each borrower type is a domain fact.
    LOAN_LIMITS = {
        BorrowerType.STUDENT: 1,
        BorrowerType.STAFF: 3,
    }

    def __init__(self, borrower_id: BorrowerId, borrower_type: BorrowerType) -> None:
        """Start a borrower who has no loans yet."""

        self._borrower_id = borrower_id
        self._borrower_type = borrower_type
        # The dictionary uses LoanId as the identity of a LoanRecord inside
        # this aggregate.
        self._loans: dict[LoanId, LoanRecord] = {}

    @property
    def borrower_id(self) -> BorrowerId:
        """Return the identity of this aggregate."""

        return self._borrower_id

    @property
    def borrower_type(self) -> BorrowerType:
        """Return whether this borrower is a student or staff member."""

        return self._borrower_type

    @property
    def loans(self) -> tuple[LoanRecord, ...]:
        """Return the loans as a read-only tuple."""

        return tuple(self._loans.values())

    def request_loan(
        self,
        asset_tag: AssetTag,
        period: BorrowingPeriod,
    ) -> LoanRequested:
        """Create a PENDING loan after checking BR3, and raise LoanRequested.

        Loan creation belongs here rather than in application code because the
        Borrower must guarantee the loan limit across all of its loans.
        """

        limit = self.LOAN_LIMITS[self._borrower_type]
        if self.active_or_pending_loan_count() >= limit:
            raise LoanLimitExceeded(
                f"{self._borrower_type.value} borrowers may hold at most {limit} loan(s)"
            )

        # Only the aggregate root creates and stores child LoanRecord entities.
        loan = LoanRecord(LoanId(uuid.uuid4().hex[:8]), asset_tag, period)
        self._loans[loan.loan_id] = loan
        return LoanRequested(loan.loan_id, self._borrower_id, asset_tag, period)

    def confirm_loan(self, loan_id: LoanId) -> None:
        """Make a PENDING loan ACTIVE. The LoanRecord checks BR2."""

        self.get_loan(loan_id)._activate()

    def cancel_loan(self, loan_id: LoanId) -> None:
        """Make a PENDING loan CANCELLED. The LoanRecord checks BR2."""

        self.get_loan(loan_id)._cancel()

    def active_or_pending_loan_count(self) -> int:
        """Return how many loans count towards the BR3 limit."""

        return sum(1 for loan in self._loans.values() if loan.is_active_or_pending())

    def get_loan(self, loan_id: LoanId) -> LoanRecord:
        """Find a child entity by its identity within this aggregate."""

        try:
            return self._loans[loan_id]
        except KeyError as error:
            raise LoanNotFound(
                f"Borrower {self._borrower_id} has no loan {loan_id}"
            ) from error
