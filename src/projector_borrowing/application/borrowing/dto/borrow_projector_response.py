"""Output DTO for the borrow-projector use case."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BorrowProjectorResponse:
    """Report the outcome as plain data the interface can display."""

    loan_id: str
    loan_status: str
    projector_status: str
