# Projector Borrowing System

DDD, TDD and Clean Architecture group coursework. A small domain for lending
projectors to students and staff, with in-memory persistence.

## Layers

- `domain`: aggregates, entities, value objects, domain services, domain events and business rules
- `application`: use cases, DTOs, repository and event-publisher contracts, application-specific errors
- `infrastructure`: in-memory repositories and the in-process event dispatcher
- `interface`: the command-line entry point (`cli.py`) and the composition root (`container.py`)

Dependencies point inward: interface and infrastructure depend on application/domain,
application depends on domain, and domain depends on nothing outside itself.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run the tests

```bash
python3 -m pytest -v
```

Requires Python 3.12+ and pytest. See `tests/README.md` for what each test checks. Test identifiers T1-T8 appear in the test names.

## Run the use case

```bash
cd src
python3 -m projector_borrowing.interface.cli S001 PRJ-001 2026-10-05 2026-10-08
```

Seeded data: `S001` (student), `T001` (staff), `PRJ-001` (standard), `PRJ-002` (premium).

## Business rules

| Rule | Type           | Statement                                                                                  | Enforced by                                                                     | On violation                                 |
| ---- | -------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------- |
| BR1  | Value          | A borrowing period must end after it starts and last at most 7 days                        | `BorrowingPeriod`                                                             | `InvalidBorrowingPeriod`                   |
| BR2  | Identity/state | A loan can only be confirmed or cancelled while PENDING                                    | `LoanRecord`                                                                  | `InvalidLoanState`                         |
| BR3  | Invariant      | A borrower holds at most 1 (student) or 3 (staff) active or pending loans                  | `Borrower`                                                                    | `LoanLimitExceeded`                        |
| BR4  | Cross-concept  | A student cannot borrow a PREMIUM projector                                                | `BorrowingEligibilityService`                                                 | `NotEligible`                              |
| BR5  | Follow-up      | After a loan is requested, the projector must be checked out; it accepts only if AVAILABLE | `LoanRequested` -> `MarkProjectorOnLoanHandler` -> `Projector.checkout()` | `ProjectorNotAvailable`, loan cancelled    |
| BR6  | Lookup         | Borrower and projector must exist before a loan request continues                          | `BorrowProjectorService` + repositories                                       | `BorrowerNotFound` / `ProjectorNotFound` |

## Diagrams

See `docs/diagrams.md` (class diagram, layer dependencies, BR5 event flow).

## Evidence

- `evidence/tdd_t1_1_fail.txt` - T1 written first; fails because `BorrowingPeriod` does not exist.
- `evidence/tdd_t1_2_fail.txt` - minimal `BorrowingPeriod` without the rule; T1 fails on the assertion.
- `evidence/tdd_t1_3_pass.txt` - BR1 implemented; T1 passes.
- `evidence/test_run.txt` - final full run of T1-T8.
