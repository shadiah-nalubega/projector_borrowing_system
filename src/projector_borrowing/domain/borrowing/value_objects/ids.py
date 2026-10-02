from dataclasses import dataclass


@dataclass(frozen=True)
class BorrowerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("BorrowerId cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class LoanId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("LoanId cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class AssetTag:
    """The label stuck on a projector, e.g. "PRJ-001"."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("AssetTag cannot be empty")

    def __str__(self) -> str:
        return self.value
