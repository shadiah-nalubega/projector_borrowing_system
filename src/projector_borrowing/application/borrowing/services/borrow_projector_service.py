"""The BorrowProjectorService: the main use case, request a projector loan."""

from __future__ import annotations

from projector_borrowing.application.borrowing.dto import (
    BorrowProjectorRequest,
    BorrowProjectorResponse,
)
from projector_borrowing.application.borrowing.exceptions import (
    BorrowerNotFound,
    ProjectorNotFound,
)
from projector_borrowing.application.borrowing.repositories import (
    BorrowerRepository,
    ProjectorRepository,
)
from projector_borrowing.application.events import EventPublisher
from projector_borrowing.domain.borrowing.services import BorrowingEligibilityService
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
)


class BorrowProjectorService:
    """Coordinate a loan request from input DTO to output DTO.

    The service looks things up, asks the domain to decide, saves, and
    publishes the event. The business rules themselves live in the domain
    objects. Every dependency is passed in from outside (dependency
    injection), so the service never creates a concrete repository.
    """

    def __init__(
        self,
        borrower_repository: BorrowerRepository,
        projector_repository: ProjectorRepository,
        eligibility_service: BorrowingEligibilityService,
        event_publisher: EventPublisher,
    ) -> None:
        self._borrowers = borrower_repository
        self._projectors = projector_repository
        self._eligibility = eligibility_service
        self._events = event_publisher

    def borrow_projector(
        self,
        request: BorrowProjectorRequest,
    ) -> BorrowProjectorResponse:
        """Run the use case and report the final loan and projector state."""

        # BR6: both aggregates must exist before the request can continue.
        borrower_id = BorrowerId(request.borrower_id)
        borrower = self._borrowers.find_by_id(borrower_id)
        if borrower is None:
            raise BorrowerNotFound(f"No borrower with id {borrower_id}")

        asset_tag = AssetTag(request.asset_tag)
        projector = self._projectors.find_by_asset_tag(asset_tag)
        if projector is None:
            raise ProjectorNotFound(f"No projector with asset tag {asset_tag}")

        period = BorrowingPeriod(request.start_date, request.end_date)  # BR1
        self._eligibility.ensure_eligible(borrower, projector)  # BR4

        event = borrower.request_loan(asset_tag, period)  # BR3, raises BR5 event
        self._borrowers.save(borrower)
        self._events.publish(event)  # BR5: the handler acts on the Projector

        # Reload both aggregates to report what the handler did.
        borrower = self._borrowers.find_by_id(borrower_id)
        projector = self._projectors.find_by_asset_tag(asset_tag)
        return BorrowProjectorResponse(
            loan_id=str(event.loan_id),
            loan_status=borrower.get_loan(event.loan_id).status.value,
            projector_status=projector.status.value,
        )
