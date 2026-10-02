"""The BorrowingEligibilityService domain service. It enforces BR4."""

from __future__ import annotations

from projector_borrowing.domain.borrowing import Borrower, Projector
from projector_borrowing.domain.borrowing.enums import BorrowerType, ProjectorCategory
from projector_borrowing.domain.borrowing.exceptions import NotEligible


class BorrowingEligibilityService:
    """Decide whether a borrower may borrow a particular projector.

    BR4: a STUDENT cannot borrow a PREMIUM projector.

    The decision needs the borrower's type and the projector's category. It does
    not belong naturally to Borrower or to Projector alone, so it lives in a
    stateless domain service.
    """

    # Each pair is a borrower type that may not borrow a projector category.
    # A new restriction is a new entry here, not a new if-statement.
    RESTRICTED = frozenset({
        (BorrowerType.STUDENT, ProjectorCategory.PREMIUM),
    })

    def check_eligibility(self, borrower: Borrower, projector: Projector) -> bool:
        """Return whether the borrower is allowed this projector."""

        return (borrower.borrower_type, projector.category) not in self.RESTRICTED

    def ensure_eligible(self, borrower: Borrower, projector: Projector) -> None:
        """Raise NotEligible when BR4 is violated."""

        if not self.check_eligibility(borrower, projector):
            raise NotEligible(
                f"{borrower.borrower_type.value} borrowers cannot borrow "
                f"{projector.category.value} projectors"
            )
