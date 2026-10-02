from abc import ABC, abstractmethod
from typing import Optional

from projector_borrowing.domain.borrowing.projector import Projector
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag


class ProjectorRepository(ABC):
    """Stores the Projector aggregate."""

    @abstractmethod
    def find_by_asset_tag(self, asset_tag: AssetTag) -> Optional[Projector]: ...

    @abstractmethod
    def save(self, projector: Projector) -> None: ...
