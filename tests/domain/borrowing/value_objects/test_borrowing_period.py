from datetime import date

import pytest

from projector_borrowing.domain.borrowing.exceptions import InvalidBorrowingPeriod
from projector_borrowing.domain.borrowing.value_objects import BorrowingPeriod


def test_T1_BR1_period_of_exactly_7_days_is_valid_but_8_days_is_rejected() -> None:
    # Arrange
    start = date(2026, 10, 5)

    # Act
    seven_day_period = BorrowingPeriod(start, date(2026, 10, 12))

    # Assert: boundary - 7 days is the maximum allowed.
    assert seven_day_period.duration_in_days() == 7

    # Assert: rejection - one day over the limit.
    with pytest.raises(InvalidBorrowingPeriod) as exception_info:
        BorrowingPeriod(start, date(2026, 10, 13))
    assert "cannot be longer than 7 days" in str(exception_info.value)

    # Assert: rejection - the end date must be after the start date.
    with pytest.raises(InvalidBorrowingPeriod):
        BorrowingPeriod(start, start)
