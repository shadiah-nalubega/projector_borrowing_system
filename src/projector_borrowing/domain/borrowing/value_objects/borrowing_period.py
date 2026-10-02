from dataclasses import dataclass
from datetime import date

from projector_borrowing.domain.borrowing.exceptions.invalid_borrowing_period import (
    InvalidBorrowingPeriod,
)

MAX_LOAN_DAYS = 7


@dataclass(frozen=True)
class BorrowingPeriod:
    """Value Object enforcing BR1.

    Two periods with the same dates are the same period, so it needs no
    identity. It is immutable and validated on creation, so an invalid
    period can never exist.
    """

    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        if self.end_date <= self.start_date:
            raise InvalidBorrowingPeriod("End date must be after start date")
        if self.duration_in_days() > MAX_LOAN_DAYS:
            raise InvalidBorrowingPeriod(
                f"A loan cannot be longer than {MAX_LOAN_DAYS} days"
            )

    def duration_in_days(self) -> int:
        return (self.end_date - self.start_date).days
