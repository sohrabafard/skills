# Lifecycle, Idempotency, And Validation Semantics

## Dry-run and approval

Dry-run must precede approval and execution when the operation is approval-based.

Approval and execution paths must compare the reviewed dry-run hash with current operation state. Do not weaken this into "latest payload wins" unless the current repository explicitly implements that policy.

## Idempotency and conflict behavior

When reviewing or changing idempotency:

- identify the current fingerprint inputs from code
- distinguish same-key/same-fingerprint replay from same-key/different-fingerprint conflict
- keep volatile values out of canonical hashes unless the current code deliberately includes them
- add deterministic hash tests for any canonicalization change

## Lifecycle helpers

Package helpers for cancel, retry-failed, fatal recovery, worker claim, or completion aggregation are admission and classification surfaces. The service still owns locks, state writes, queue dispatch, domain mutations, sibling-drift checks, and outbox safety.

## Validation target

For lifecycle work, prefer focused tests that prove:

- invalid status transitions fail closed
- reviewed hash mismatches fail closed
- duplicate or conflicting idempotency attempts are classified correctly
- service-owned domain writes do not move into the package
- public docs and Postman examples still match implemented behavior
