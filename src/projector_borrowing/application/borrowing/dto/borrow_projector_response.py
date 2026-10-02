from dataclasses import dataclass


@dataclass(frozen=True)
class BorrowProjectorResponse:
    """Output DTO: the outcome of the request as plain data."""

    loan_id: str
    loan_status: str
    projector_status: str
