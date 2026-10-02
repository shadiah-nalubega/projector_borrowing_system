"""The LoanRecord child entity in the Borrower aggregate. It enforces BR2."""

from __future__ import annotations

from projector_borrowing.domain.borrowing.enums import LoanStatus
from projector_borrowing.domain.borrowing.exceptions import InvalidLoanState
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowingPeriod,
    LoanId,
)


class LoanRecord:
    """Represent one identifiable loan whose status changes over time.

    ``loan_id`` is the entity's identity: two loans for the same projector and
    the same dates are still different loans. ``status`` is mutable state.

    BR2: a loan may only move PENDING -> ACTIVE or PENDING -> CANCELLED.
    """

    def __init__(
        self,
        loan_id: LoanId,
        asset_tag: AssetTag,
        period: BorrowingPeriod,
    ) -> None:
        self._loan_id = loan_id
        self._asset_tag = asset_tag
        self._period = period
        self._status = LoanStatus.PENDING

    @property
    def loan_id(self) -> LoanId:
        """Return this entity's stable identity within its Borrower."""

        return self._loan_id

    @property
    def asset_tag(self) -> AssetTag:
        """Return the projector this loan is for."""

        return self._asset_tag

    @property
    def period(self) -> BorrowingPeriod:
        """Return the dates of this loan."""

        return self._period

    @property
    def status(self) -> LoanStatus:
        """Return the current state of this loan."""

        return self._status

    def is_active_or_pending(self) -> bool:
        """Return whether this loan counts towards the borrower's limit (BR3)."""

        return self._status in (LoanStatus.PENDING, LoanStatus.ACTIVE)

    def _activate(self) -> None:
        """Confirm the loan after the Borrower has approved the change.

        The leading underscore marks this as aggregate-internal behaviour.
        Calling code should use ``Borrower.confirm_loan`` instead.
        """

        self._ensure_pending("confirm")
        self._status = LoanStatus.ACTIVE

    def _cancel(self) -> None:
        """Cancel the loan. Calling code should use ``Borrower.cancel_loan``."""

        self._ensure_pending("cancel")
        self._status = LoanStatus.CANCELLED

    def _ensure_pending(self, action: str) -> None:
        """Protect BR2: only a PENDING loan can change state."""

        if self._status is not LoanStatus.PENDING:
            raise InvalidLoanState(
                f"Cannot {action} loan {self._loan_id}: it is {self._status.value}"
            )

    def __eq__(self, other: object) -> bool:
        """Entities are equal when their identities are equal."""

        return isinstance(other, LoanRecord) and other.loan_id == self._loan_id

    def __hash__(self) -> int:
        return hash(self._loan_id)
