from datetime import date

import pytest

from projector_borrowing.domain.borrowing.exceptions.invalid_borrowing_period import (
    InvalidBorrowingPeriod,
)
from projector_borrowing.domain.borrowing.value_objects.borrowing_period import (
    BorrowingPeriod,
)


def test_T1_BR1_period_of_exactly_7_days_is_valid_but_8_days_is_rejected():
    # Boundary: 7 days is the maximum allowed.
    period = BorrowingPeriod(date(2026, 10, 5), date(2026, 10, 12))
    assert period.duration_in_days() == 7

    # Rejection: one day over the limit.
    with pytest.raises(InvalidBorrowingPeriod):
        BorrowingPeriod(date(2026, 10, 5), date(2026, 10, 13))

    # Rejection: end date must be after start date.
    with pytest.raises(InvalidBorrowingPeriod):
        BorrowingPeriod(date(2026, 10, 5), date(2026, 10, 5))
