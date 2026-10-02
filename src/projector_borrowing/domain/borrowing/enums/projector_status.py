"""Whether a projector can be checked out."""

from enum import Enum


class ProjectorStatus(Enum):
    AVAILABLE = "AVAILABLE"
    ON_LOAN = "ON_LOAN"
