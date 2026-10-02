"""An in-memory ProjectorRepository."""

from __future__ import annotations

import copy

from projector_borrowing.application.borrowing.repositories import ProjectorRepository
from projector_borrowing.domain.borrowing import Projector
from projector_borrowing.domain.borrowing.value_objects import AssetTag


class InMemoryProjectorRepository(ProjectorRepository):
    """Keep Projector aggregates in a dictionary.

    Copies are stored and returned, like a real database: changes to a
    projector are lost unless ``save`` is called.
    """

    def __init__(self) -> None:
        self._projectors: dict[AssetTag, Projector] = {}

    def find_by_asset_tag(self, asset_tag: AssetTag) -> Projector | None:
        projector = self._projectors.get(asset_tag)
        return copy.deepcopy(projector) if projector is not None else None

    def save(self, projector: Projector) -> None:
        self._projectors[projector.asset_tag] = copy.deepcopy(projector)
