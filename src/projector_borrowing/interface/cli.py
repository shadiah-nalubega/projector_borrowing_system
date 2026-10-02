"""Minimal command-line entry point.

Example:
    python -m projector_borrowing.interface.cli S001 PRJ-001 2026-10-05 2026-10-08
"""

import argparse
import sys
from datetime import date

from projector_borrowing.application.borrowing.dto.borrow_projector_request import (
    BorrowProjectorRequest,
)
from projector_borrowing.application.borrowing.handlers.mark_projector_on_loan_handler import (
    MarkProjectorOnLoanHandler,
)
from projector_borrowing.application.borrowing.services.borrow_projector_service import (
    BorrowProjectorService,
)
from projector_borrowing.application.events.event_dispatcher import EventDispatcher
from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.enums.borrower_type import BorrowerType
from projector_borrowing.domain.borrowing.enums.projector_category import (
    ProjectorCategory,
)
from projector_borrowing.domain.borrowing.events.loan_requested import LoanRequested
from projector_borrowing.domain.borrowing.projector import Projector
from projector_borrowing.domain.borrowing.services.borrowing_eligibility_service import (
    BorrowingEligibilityService,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, BorrowerId
from projector_borrowing.infrastructure.repositories.in_memory_borrower_repository import (
    InMemoryBorrowerRepository,
)
from projector_borrowing.infrastructure.repositories.in_memory_projector_repository import (
    InMemoryProjectorRepository,
)


def build_service() -> BorrowProjectorService:
    """Composition root: creates the concrete objects and injects them."""
    borrowers = InMemoryBorrowerRepository()
    projectors = InMemoryProjectorRepository()

    borrowers.save(Borrower(BorrowerId("S001"), BorrowerType.STUDENT))
    borrowers.save(Borrower(BorrowerId("T001"), BorrowerType.STAFF))
    projectors.save(Projector(AssetTag("PRJ-001"), ProjectorCategory.STANDARD))
    projectors.save(Projector(AssetTag("PRJ-002"), ProjectorCategory.PREMIUM))

    dispatcher = EventDispatcher()
    dispatcher.subscribe(LoanRequested, MarkProjectorOnLoanHandler(borrowers, projectors))
    return BorrowProjectorService(
        borrowers, projectors, BorrowingEligibilityService(), dispatcher
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Request a projector loan.")
    parser.add_argument("borrower_id", help="e.g. S001 (student) or T001 (staff)")
    parser.add_argument("asset_tag", help="e.g. PRJ-001 (standard) or PRJ-002 (premium)")
    parser.add_argument("start_date", type=date.fromisoformat, help="YYYY-MM-DD")
    parser.add_argument("end_date", type=date.fromisoformat, help="YYYY-MM-DD")
    args = parser.parse_args(argv)

    service = build_service()
    request = BorrowProjectorRequest(
        args.borrower_id, args.asset_tag, args.start_date, args.end_date
    )
    try:
        response = service.borrow_projector(request)
    except Exception as error:
        print(f"Rejected: {type(error).__name__}: {error}")
        return 1

    print(
        f"Loan {response.loan_id}: {response.loan_status} "
        f"(projector is {response.projector_status})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
