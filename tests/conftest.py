from datetime import date

import pytest

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
from projector_borrowing.domain.borrowing.value_objects.borrowing_period import (
    BorrowingPeriod,
)
from projector_borrowing.domain.borrowing.value_objects.ids import AssetTag, BorrowerId
from projector_borrowing.infrastructure.repositories.in_memory_borrower_repository import (
    InMemoryBorrowerRepository,
)
from projector_borrowing.infrastructure.repositories.in_memory_projector_repository import (
    InMemoryProjectorRepository,
)

START = date(2026, 10, 5)
END = date(2026, 10, 8)


@pytest.fixture
def period():
    return BorrowingPeriod(START, END)


@pytest.fixture
def borrowers():
    repo = InMemoryBorrowerRepository()
    repo.save(Borrower(BorrowerId("S001"), BorrowerType.STUDENT))
    return repo


@pytest.fixture
def projectors():
    repo = InMemoryProjectorRepository()
    repo.save(Projector(AssetTag("PRJ-001"), ProjectorCategory.STANDARD))
    return repo


@pytest.fixture
def service(borrowers, projectors):
    """Wires the use case with in-memory repositories (dependency injection)."""
    dispatcher = EventDispatcher()
    dispatcher.subscribe(LoanRequested, MarkProjectorOnLoanHandler(borrowers, projectors))
    return BorrowProjectorService(
        borrowers, projectors, BorrowingEligibilityService(), dispatcher
    )
