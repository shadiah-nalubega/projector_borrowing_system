# Test organization

Tests are grouped first by Clean Architecture layer and then by feature:

```text
tests/
├── domain/
│   └── borrowing/          T1-T4: value object, entity, aggregate, domain service
└── application/
    └── borrowing/          T5-T8: event handler and the main use case
```

| Test | Rule | Checks | Kind |
|------|------|--------|------|
| T1 | BR1 | 7-day period accepted, 8-day period rejected | boundary + rejection |
| T2 | BR2 | A cancelled loan cannot be confirmed | rejection |
| T3 | BR3 | A student cannot hold a second loan | rejection |
| T4 | BR4 | A student is not eligible for a premium projector | rejection |
| T5 | BR5 | Handling `LoanRequested` checks out the projector | event |
| T6 | BR6 | An unknown borrower is rejected | rejection |
| T7 | -   | Main use case succeeds; the event changes the projector | success |
| T8 | -   | The projector refuses checkout; the loan ends CANCELLED | Aggregate B rejects |

Domain tests do not import application, infrastructure or interface code.

Application tests use the in-memory repositories, which the brief requires as the
persistence implementation. They store copies, so a missing `save` makes T5 and T7 fail.

Every test follows Arrange / Act / Assert. These folders intentionally have no
`__init__.py`: pytest discovers test modules by filename.
