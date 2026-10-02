from projector_borrowing.application.borrowing.dto.borrow_projector_request import (
    BorrowProjectorRequest,
)
from projector_borrowing.application.borrowing.dto.borrow_projector_response import (
    BorrowProjectorResponse,
)
from projector_borrowing.application.borrowing.exceptions import (
    BorrowerNotFound,
    ProjectorNotFound,
)
from projector_borrowing.application.borrowing.repositories.borrower_repository import (
    BorrowerRepository,
)
from projector_borrowing.application.borrowing.repositories.projector_repository import (
    ProjectorRepository,
)
from projector_borrowing.application.events.event_dispatcher import EventDispatcher
from projector_borrowing.domain.borrowing.exceptions.not_eligible import NotEligible
from projector_borrowing.domain.borrowing.services.borrowing_eligibility_service import (
    BorrowingEligibilityService,
)
from projector_borrowing.domain.borrowing.value_objects.borrowing_period import (
    BorrowingPeriod,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, BorrowerId


class BorrowProjectorService:
    """Application Service for the main use case: request a projector loan.

    It coordinates the work (look up, ask the domain, save, publish). The
    business rules themselves live in the domain objects. Every dependency is
    passed in from outside (dependency injection).
    """

    def __init__(
        self,
        borrower_repository: BorrowerRepository,
        projector_repository: ProjectorRepository,
        eligibility_service: BorrowingEligibilityService,
        event_dispatcher: EventDispatcher,
    ):
        self._borrowers = borrower_repository
        self._projectors = projector_repository
        self._eligibility = eligibility_service
        self._events = event_dispatcher

    def borrow_projector(self, request: BorrowProjectorRequest) -> BorrowProjectorResponse:
        # BR6: both aggregates must exist before we continue.
        borrower_id = BorrowerId(request.borrower_id)
        borrower = self._borrowers.find_by_id(borrower_id)
        if borrower is None:
            raise BorrowerNotFound(f"No borrower with id {borrower_id}")

        asset_tag = AssetTag(request.asset_tag)
        projector = self._projectors.find_by_asset_tag(asset_tag)
        if projector is None:
            raise ProjectorNotFound(f"No projector with asset tag {asset_tag}")

        period = BorrowingPeriod(request.start_date, request.end_date)  # BR1

        if not self._eligibility.check_eligibility(borrower, projector):  # BR4
            raise NotEligible(
                f"{borrower.borrower_type.value} borrowers cannot borrow "
                f"{projector.category.value} projectors"
            )

        event = borrower.request_loan(asset_tag, period)  # BR3, raises BR5 event
        self._borrowers.save(borrower)
        self._events.publish(event)  # BR5: handler acts on the Projector

        borrower = self._borrowers.find_by_id(borrower_id)
        projector = self._projectors.find_by_asset_tag(asset_tag)
        return BorrowProjectorResponse(
            loan_id=str(event.loan_id),
            loan_status=borrower.get_loan(event.loan_id).status.value,
            projector_status=projector.status.value,
        )
