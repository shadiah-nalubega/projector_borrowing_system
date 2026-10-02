"""Who is borrowing: the type decides the BR3 loan limit and BR4 eligibility."""

from enum import Enum


class BorrowerType(Enum):
    STUDENT = "STUDENT"
    STAFF = "STAFF"
