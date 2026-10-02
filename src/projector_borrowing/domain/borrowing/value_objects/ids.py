"""Identity value objects.

Wrapping identities in small types stops a LoanId from being passed where a
BorrowerId is expected, and stops empty identities from entering the domain.
"""

from __future__ import annotations

from dataclasses import dataclass

from projector_borrowing.domain.borrowing.exceptions import InvalidIdentifier


@dataclass(frozen=True, slots=True)
class Identifier:
    """Shared behaviour for every identity: a non-empty text value.

    Dataclass equality also compares the class, so ``BorrowerId("A1")`` is
    never equal to ``LoanId("A1")``.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidIdentifier(f"{type(self).__name__} cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class BorrowerId(Identifier):
    """Identify a Borrower aggregate."""


@dataclass(frozen=True, slots=True)
class LoanId(Identifier):
    """Identify a LoanRecord entity inside its Borrower."""


@dataclass(frozen=True, slots=True)
class AssetTag(Identifier):
    """Identify a Projector aggregate: the label stuck on it, e.g. "PRJ-001"."""
