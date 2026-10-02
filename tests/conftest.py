"""Shared fixtures: in-memory repositories and a fully wired use case."""

from datetime import date

import pytest

from projector_borrowing.application.borrowing.handlers import MarkProjectorOnLoanHandler
from projector_borrowing.application.borrowing.services import BorrowProjectorService
from projector_borrowing.domain.borrowing import Borrower, Projector
from projector_borrowing.domain.borrowing.enums import BorrowerType, ProjectorCategory
from projector_borrowing.domain.borrowing.events import LoanRequested
from projector_borrowing.domain.borrowing.services import BorrowingEligibilityService
from projector_borrowing.domain.borrowing.value_objects import (
    AssetTag,
    BorrowerId,
    BorrowingPeriod,
)
from projector_borrowing.infrastructure.events import InProcessEventDispatcher
from projector_borrowing.infrastructure.repositories import (
    InMemoryBorrowerRepository,
    InMemoryProjectorRepository,
)

START = date(2026, 10, 5)
END = date(2026, 10, 8)


@pytest.fixture
def period() -> BorrowingPeriod:
    return BorrowingPeriod(START, END)


@pytest.fixture
def borrowers() -> InMemoryBorrowerRepository:
    repository = InMemoryBorrowerRepository()
    repository.save(Borrower(BorrowerId("S001"), BorrowerType.STUDENT))
    return repository


@pytest.fixture
def projectors() -> InMemoryProjectorRepository:
    repository = InMemoryProjectorRepository()
    repository.save(Projector(AssetTag("PRJ-001"), ProjectorCategory.STANDARD))
    return repository


@pytest.fixture
def service(
    borrowers: InMemoryBorrowerRepository,
    projectors: InMemoryProjectorRepository,
) -> BorrowProjectorService:
    """Wire the use case by injecting repositories from outside."""

    dispatcher = InProcessEventDispatcher()
    dispatcher.subscribe(LoanRequested, MarkProjectorOnLoanHandler(borrowers, projectors))
    return BorrowProjectorService(
        borrowers, projectors, BorrowingEligibilityService(), dispatcher
    )
