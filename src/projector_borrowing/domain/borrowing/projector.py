"""The Projector aggregate root (Aggregate B)."""

from __future__ import annotations

from projector_borrowing.domain.borrowing.enums import (
    ProjectorCategory,
    ProjectorStatus,
)
from projector_borrowing.domain.borrowing.exceptions import ProjectorNotAvailable
from projector_borrowing.domain.borrowing.value_objects import AssetTag


class Projector:
    """A physical projector that can be lent out.

    Invariant: a projector is with at most one borrower at a time, so it can
    only be checked out while AVAILABLE. This is the rule it checks before
    accepting the BR5 follow-up action.
    """

    def __init__(
        self,
        asset_tag: AssetTag,
        category: ProjectorCategory,
        status: ProjectorStatus = ProjectorStatus.AVAILABLE,
    ) -> None:
        self._asset_tag = asset_tag
        self._category = category
        self._status = status

    @property
    def asset_tag(self) -> AssetTag:
        """Return the identity of this aggregate."""

        return self._asset_tag

    @property
    def category(self) -> ProjectorCategory:
        """Return whether this is a STANDARD or PREMIUM projector."""

        return self._category

    @property
    def status(self) -> ProjectorStatus:
        """Return whether this projector is AVAILABLE or ON_LOAN."""

        return self._status

    def checkout(self) -> None:
        """Hand the projector out, refusing if it is already on loan."""

        if self._status is not ProjectorStatus.AVAILABLE:
            raise ProjectorNotAvailable(
                f"Projector {self._asset_tag} is {self._status.value}"
            )
        self._status = ProjectorStatus.ON_LOAN
