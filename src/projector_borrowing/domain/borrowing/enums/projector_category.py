"""The kind of projector: PREMIUM projectors are restricted by BR4."""

from enum import Enum


class ProjectorCategory(Enum):
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
