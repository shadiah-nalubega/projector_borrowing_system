"""An in-memory ProjectorRepository."""

from __future__ import annotations

from projector_borrowing.application.borrowing.repositories import ProjectorRepository
from projector_borrowing.domain.borrowing import Projector
from projector_borrowing.domain.borrowing.value_objects import AssetTag

from .in_memory_store import InMemoryStore


class InMemoryProjectorRepository(ProjectorRepository):
    """Keep Projector aggregates in memory."""

    def __init__(self) -> None:
        self._store: InMemoryStore[AssetTag, Projector] = InMemoryStore()

    def find_by_asset_tag(self, asset_tag: AssetTag) -> Projector | None:
        return self._store.get(asset_tag)

    def save(self, projector: Projector) -> None:
        self._store.put(projector.asset_tag, projector)
