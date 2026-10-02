"""The ProjectorRepository contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from projector_borrowing.domain.borrowing import Projector
from projector_borrowing.domain.borrowing.value_objects import AssetTag


class ProjectorRepository(ABC):
    """Store and retrieve Projector aggregates."""

    @abstractmethod
    def find_by_asset_tag(self, asset_tag: AssetTag) -> Projector | None:
        """Return the projector, or ``None`` when no projector has this tag."""

    @abstractmethod
    def save(self, projector: Projector) -> None:
        """Store the projector."""
