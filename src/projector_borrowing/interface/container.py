"""Composition root: the one place that knows every concrete class.

It creates the infrastructure objects and injects them into the use case.
Nothing else in the system creates its own dependencies.
"""

from __future__ import annotations

from projector_borrowing.application.borrowing.handlers import MarkProjectorOnLoanHandler
from projector_borrowing.application.borrowing.repositories import (
    BorrowerRepository,
    ProjectorRepository,
)
from projector_borrowing.application.borrowing.services import BorrowProjectorService
from projector_borrowing.domain.borrowing.events import LoanRequested
from projector_borrowing.domain.borrowing.services import BorrowingEligibilityService
from projector_borrowing.infrastructure.events import InProcessEventDispatcher


def create_borrow_projector_service(
    borrowers: BorrowerRepository,
    projectors: ProjectorRepository,
) -> BorrowProjectorService:
    """Wire the use case: subscribe the BR5 handler and inject everything."""

    dispatcher = InProcessEventDispatcher()
    dispatcher.subscribe(LoanRequested, MarkProjectorOnLoanHandler(borrowers, projectors))
    return BorrowProjectorService(
        borrowers, projectors, BorrowingEligibilityService(), dispatcher
    )
