from projector_borrowing.domain.borrowing.enums.projector_category import (
    ProjectorCategory,
)
from projector_borrowing.domain.borrowing.enums.projector_status import ProjectorStatus
from projector_borrowing.domain.borrowing.exceptions.projector_not_available import (
    ProjectorNotAvailable,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag


class Projector:
    """Aggregate Root (Aggregate B).

    Invariant: a projector is with at most one borrower at a time, so it can
    only be checked out while AVAILABLE. This is the rule it checks before
    accepting the BR5 follow-up action.
    """

    def __init__(
        self,
        asset_tag: AssetTag,
        category: ProjectorCategory,
        status: ProjectorStatus = ProjectorStatus.AVAILABLE,
    ):
        self.asset_tag = asset_tag
        self.category = category
        self.status = status

    def checkout(self) -> None:
        if self.status is not ProjectorStatus.AVAILABLE:
            raise ProjectorNotAvailable(
                f"Projector {self.asset_tag} is {self.status.value}"
            )
        self.status = ProjectorStatus.ON_LOAN
