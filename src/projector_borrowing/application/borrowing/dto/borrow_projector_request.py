from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BorrowProjectorRequest:
    """Input DTO: plain data from the interface, no domain types."""

    borrower_id: str
    asset_tag: str
    start_date: date
    end_date: date
