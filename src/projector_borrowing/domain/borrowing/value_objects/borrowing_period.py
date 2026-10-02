"""The BorrowingPeriod value object, which enforces BR1."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from projector_borrowing.domain.borrowing.exceptions import InvalidBorrowingPeriod

# This named constant communicates a domain fact and avoids a magic number.
MAX_LOAN_DAYS = 7


@dataclass(frozen=True, slots=True)
class BorrowingPeriod:
    """The dates a projector is borrowed for.

    BR1: a period must end after it starts and last at most 7 days.

    A value object is defined by its values rather than an identity. Two periods
    with the same dates are the same period. ``frozen=True`` prevents the dates
    from changing after creation, so every instance stays valid.
    """

    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        """Protect BR1 so an invalid period can never exist."""

        if self.end_date <= self.start_date:
            raise InvalidBorrowingPeriod("End date must be after start date")
        if self.duration_in_days() > MAX_LOAN_DAYS:
            raise InvalidBorrowingPeriod(
                f"A loan cannot be longer than {MAX_LOAN_DAYS} days"
            )

    def duration_in_days(self) -> int:
        """Number of days between the start and end dates."""

        return (self.end_date - self.start_date).days
