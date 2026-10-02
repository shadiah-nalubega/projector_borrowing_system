"""The states a LoanRecord can be in (see BR2)."""

from enum import Enum


class LoanStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
