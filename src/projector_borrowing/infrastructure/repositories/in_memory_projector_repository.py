import copy
from typing import Optional

from projector_borrowing.application.borrowing.repositories.projector_repository import (
    ProjectorRepository,
)
from projector_borrowing.domain.borrowing.projector import Projector
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag


class InMemoryProjectorRepository(ProjectorRepository):
    """Keeps copies, like a real database: changes are lost unless saved."""

    def __init__(self) -> None:
        self._projectors: dict[AssetTag, Projector] = {}

    def find_by_asset_tag(self, asset_tag: AssetTag) -> Optional[Projector]:
        projector = self._projectors.get(asset_tag)
        return copy.deepcopy(projector) if projector is not None else None

    def save(self, projector: Projector) -> None:
        self._projectors[projector.asset_tag] = copy.deepcopy(projector)
