"""Identity value objects.

Wrapping identities in small types stops a LoanId from being passed where a
BorrowerId is expected, and stops empty identities from entering the domain.
"""

from __future__ import annotations

from dataclasses import dataclass

from projector_borrowing.domain.borrowing.exceptions import InvalidIdentifier


@dataclass(frozen=True, slots=True)
class BorrowerId:
    """Identify a Borrower aggregate."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidIdentifier("BorrowerId cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LoanId:
    """Identify a LoanRecord entity inside its Borrower."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidIdentifier("LoanId cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class AssetTag:
    """Identify a Projector aggregate: the label stuck on it, e.g. "PRJ-001"."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidIdentifier("AssetTag cannot be empty")

    def __str__(self) -> str:
        return self.value
