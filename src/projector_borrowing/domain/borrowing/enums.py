"""Fixed sets of values used by the borrowing domain."""

from enum import Enum


class BorrowerType(Enum):
    """Who is borrowing: the type decides the BR3 loan limit and BR4 eligibility."""

    STUDENT = "STUDENT"
    STAFF = "STAFF"


class LoanStatus(Enum):
    """The states a LoanRecord can be in (see BR2)."""

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"


class ProjectorCategory(Enum):
    """The kind of projector: PREMIUM projectors are restricted by BR4."""

    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"


class ProjectorStatus(Enum):
    """Whether a projector can be checked out."""

    AVAILABLE = "AVAILABLE"
    ON_LOAN = "ON_LOAN"
