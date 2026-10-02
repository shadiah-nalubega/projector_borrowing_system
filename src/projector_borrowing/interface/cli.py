"""A minimal command-line entry point.

Example:
    python -m projector_borrowing.interface.cli S001 PRJ-001 2026-10-05 2026-10-08
"""

from __future__ import annotations

import argparse
import sys
from datetime import date

from projector_borrowing.application.borrowing.dto import BorrowProjectorRequest
from projector_borrowing.application.borrowing.exceptions import ApplicationError
from projector_borrowing.application.borrowing.handlers import MarkProjectorOnLoanHandler
from projector_borrowing.application.borrowing.services import BorrowProjectorService
from projector_borrowing.domain.borrowing import Borrower, Projector
from projector_borrowing.domain.borrowing.enums import BorrowerType, ProjectorCategory
from projector_borrowing.domain.borrowing.events import LoanRequested
from projector_borrowing.domain.borrowing.exceptions import DomainError
from projector_borrowing.domain.borrowing.services import BorrowingEligibilityService
from projector_borrowing.domain.borrowing.value_objects import AssetTag, BorrowerId
from projector_borrowing.infrastructure.events import InProcessEventDispatcher
from projector_borrowing.infrastructure.repositories import (
    InMemoryBorrowerRepository,
    InMemoryProjectorRepository,
)


def build_service() -> BorrowProjectorService:
    """Composition root: create the concrete objects and inject them."""

    borrowers = InMemoryBorrowerRepository()
    projectors = InMemoryProjectorRepository()

    borrowers.save(Borrower(BorrowerId("S001"), BorrowerType.STUDENT))
    borrowers.save(Borrower(BorrowerId("T001"), BorrowerType.STAFF))
    projectors.save(Projector(AssetTag("PRJ-001"), ProjectorCategory.STANDARD))
    projectors.save(Projector(AssetTag("PRJ-002"), ProjectorCategory.PREMIUM))

    dispatcher = InProcessEventDispatcher()
    dispatcher.subscribe(LoanRequested, MarkProjectorOnLoanHandler(borrowers, projectors))
    return BorrowProjectorService(
        borrowers, projectors, BorrowingEligibilityService(), dispatcher
    )


def main(argv: list[str] | None = None) -> int:
    """Parse the arguments, run the use case and print the outcome."""

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
    except (DomainError, ApplicationError) as error:
        print(f"Rejected: {type(error).__name__}: {error}")
        return 1

    print(
        f"Loan {response.loan_id}: {response.loan_status} "
        f"(projector is {response.projector_status})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
