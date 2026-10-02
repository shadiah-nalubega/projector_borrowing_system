"""The LoanRequested domain event, which starts the BR5 follow-up."""

from __future__ import annotations

from dataclasses import dataclass

from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
    LoanId,
)


@dataclass(frozen=True, slots=True)
class LoanRequested:
    """Record that a Borrower has requested a loan.

    A domain event describes something that already happened, so it is named
    in the past tense and cannot be changed. Borrower (Aggregate A) raises it
    after recording a PENDING loan. It asks Projector (Aggregate B) to be
    checked out, without Borrower changing Projector directly.
    """

    loan_id: LoanId
    borrower_id: BorrowerId
    asset_tag: AssetTag
    period: BorrowingPeriod
