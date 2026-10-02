from projector_borrowing.domain.borrowing.borrower import Borrower
from projector_borrowing.domain.borrowing.enums.borrower_type import BorrowerType
from projector_borrowing.domain.borrowing.enums.projector_category import (
    ProjectorCategory,
)
from projector_borrowing.domain.borrowing.exceptions.not_eligible import NotEligible
from projector_borrowing.domain.borrowing.projector import Projector


class BorrowingEligibilityService:
    """Domain Service enforcing BR4.

    The decision needs the borrower's type and the projector's category. It
    does not belong to Borrower or to Projector alone, so it lives here.
    """

    def check_eligibility(self, borrower: Borrower, projector: Projector) -> bool:
        if (
            borrower.borrower_type is BorrowerType.STUDENT
            and projector.category is ProjectorCategory.PREMIUM
        ):
            return False
        return True

    def ensure_eligible(self, borrower: Borrower, projector: Projector) -> None:
        if not self.check_eligibility(borrower, projector):
            raise NotEligible(
                f"{borrower.borrower_type.value} borrowers cannot borrow "
                f"{projector.category.value} projectors"
            )
