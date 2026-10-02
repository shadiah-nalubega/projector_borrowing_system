"""Input DTO for the borrow-projector use case."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class BorrowProjectorRequest:
    """Carry the request from the interface as plain data, with no domain types.

    The application service turns these values into domain objects, so the
    interface never needs to know about the domain model.
    """

    borrower_id: str
    asset_tag: str
    start_date: date
    end_date: date
