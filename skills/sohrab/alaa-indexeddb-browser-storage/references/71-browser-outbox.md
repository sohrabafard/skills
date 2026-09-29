# The browser-side outbox

A mutation the user made that must survive a reload, a tab close, or an offline period.

## This is not the server-side outbox, and the difference is structural

When comparing browser and server delivery state, read [Browser outbox boundary](./71-browser-outbox/10-browser-outbox-boundary.md) for why the browser reaper and statuses differ.

## The record

When defining or indexing an outbox row, read [Record and cursor invariant](./71-browser-outbox/20-record-and-cursor-invariant.md) for its fields and exact status-range requirement.

## The flush

When implementing a flush, read [Flush and classification](./71-browser-outbox/30-flush-and-classification.md) for lock, claim, send, and result ordering.

## Classification

When mapping a response or failure to a row state, read [Flush and classification](./71-browser-outbox/30-flush-and-classification.md) for the 401/403 distinction and retry ownership.

## Retry, and who owns it

When defining retry ownership or an attempt limit, read [Retry policy](./71-browser-outbox/60-retry-policy.md) for the configuration boundary and terminal disposition.

## The reaper — the failure class the server outbox does not have

When diagnosing or recovering a row left in `sending`, read [Reaper and recovery](./71-browser-outbox/40-reaper-and-recovery.md) for stale-claim detection and idempotency safety.

## Bounds, triggers, reporting

When setting capacity or operating flush triggers, read [Bounds and operations](./71-browser-outbox/50-bounds-and-operations.md) for drop policy, triggers, telemetry, and logging limits.
