# Diagrams

These diagrams match the source code. Use them for slides 5, 8 and 10.

## Class diagram

```mermaid
classDiagram
    direction LR

    class BorrowProjectorService {
        <<Application Service>>
        +borrow_projector(request: BorrowProjectorRequest) BorrowProjectorResponse
    }
    class MarkProjectorOnLoanHandler {
        <<Event Handler>>
        +__call__(event: LoanRequested)
    }
    class BorrowerRepository {
        <<interface>>
        +find_by_id(borrower_id: BorrowerId) Borrower
        +save(borrower: Borrower)
    }
    class ProjectorRepository {
        <<interface>>
        +find_by_asset_tag(asset_tag: AssetTag) Projector
        +save(projector: Projector)
    }
    class EventPublisher {
        <<interface>>
        +publish(event)
    }
    class BorrowingEligibilityService {
        <<Domain Service>>
        +check_eligibility(borrower, projector) bool
        +ensure_eligible(borrower, projector)
    }
    class Borrower {
        <<Aggregate Root A>>
        -borrower_id: BorrowerId
        -borrower_type: BorrowerType
        -loans: list~LoanRecord~
        +request_loan(asset_tag, period) LoanRequested
        +confirm_loan(loan_id)
        +cancel_loan(loan_id)
        +active_or_pending_loan_count() int
        +get_loan(loan_id) LoanRecord
    }
    class LoanRecord {
        <<Entity>>
        -loan_id: LoanId
        -asset_tag: AssetTag
        -period: BorrowingPeriod
        -status: LoanStatus
        -_activate()
        -_cancel()
        +is_active_or_pending() bool
    }
    class BorrowingPeriod {
        <<Value Object>>
        -start_date: date
        -end_date: date
        +duration_in_days() int
    }
    class Projector {
        <<Aggregate Root B>>
        -asset_tag: AssetTag
        -category: ProjectorCategory
        -status: ProjectorStatus
        +checkout()
    }
    class LoanRequested {
        <<Domain Event>>
        loan_id: LoanId
        borrower_id: BorrowerId
        asset_tag: AssetTag
        period: BorrowingPeriod
    }

    BorrowProjectorService ..> BorrowerRepository
    BorrowProjectorService ..> ProjectorRepository
    BorrowProjectorService ..> BorrowingEligibilityService
    BorrowProjectorService ..> EventPublisher
    MarkProjectorOnLoanHandler ..> BorrowerRepository
    MarkProjectorOnLoanHandler ..> ProjectorRepository
    Borrower "1" *-- "0..*" LoanRecord
    LoanRecord --> BorrowingPeriod
    Borrower ..> LoanRequested : raises
    MarkProjectorOnLoanHandler ..> LoanRequested : handles
    MarkProjectorOnLoanHandler ..> Projector : checkout()
```

Value objects for identity: `BorrowerId`, `LoanId`, `AssetTag` (all share the `Identifier` base).
Enums: `BorrowerType` (STUDENT, STAFF), `LoanStatus` (PENDING, ACTIVE, CANCELLED),
`ProjectorCategory` (STANDARD, PREMIUM), `ProjectorStatus` (AVAILABLE, ON_LOAN).

## Clean Architecture dependencies

Arrows point from the importing layer to the imported layer. Nothing points outward.

```mermaid
flowchart TB
    Interface["Interface<br/>cli.py, container.py (composition root)"]
    Infrastructure["Infrastructure<br/>InMemoryBorrowerRepository, InMemoryProjectorRepository<br/>InProcessEventDispatcher"]
    Application["Application<br/>BorrowProjectorService, MarkProjectorOnLoanHandler<br/>DTOs, repository and EventPublisher interfaces"]
    Domain["Domain<br/>Borrower, Projector, LoanRecord, BorrowingPeriod<br/>BorrowingEligibilityService, LoanRequested, exceptions"]

    Interface --> Application
    Interface --> Infrastructure
    Interface --> Domain
    Infrastructure --> Application
    Infrastructure --> Domain
    Application --> Domain
```

## BR5 event flow

```mermaid
sequenceDiagram
    participant CLI as Interface (CLI)
    participant S as BorrowProjectorService
    participant B as Borrower (Aggregate A)
    participant D as InProcessEventDispatcher
    participant H as MarkProjectorOnLoanHandler
    participant P as Projector (Aggregate B)

    CLI->>S: BorrowProjectorRequest
    S->>B: request_loan(asset_tag, period)
    B-->>S: LoanRequested (loan is PENDING)
    S->>D: publish(LoanRequested)
    D->>H: handle event
    H->>P: checkout()
    alt projector AVAILABLE
        P-->>H: status = ON_LOAN
        H->>B: confirm_loan -> ACTIVE
    else projector ON_LOAN
        P-->>H: ProjectorNotAvailable
        H->>B: cancel_loan -> CANCELLED
    end
    S-->>CLI: BorrowProjectorResponse(loan_id, loan_status, projector_status)
```
