# The three routes out of a handler

## The three routes out of a handler

Every handler outcome takes exactly one of these, and the choice is made by the failure's class rather than
by its severity.

| Outcome | Route | What the broker does | Crash window |
|---|---|---|---|
| The work succeeded, or a duplicate was recognised | **ack** | removes the message | between commit and ack: redelivery, recognised as a duplicate |
| Transient failure — dependency unreachable, lock contention, timeout | **verified bounded retry path** under `../40-dead-letter-and-replay.md` | redelivers; counter effects depend on broker version and AMQP method | none only if nonexecution or rollback is proven; an uncertain commit requires identity-based reconciliation |
| Permanent failure — the message can never succeed as written: schema violation, unknown type, referenced entity absent for good | **reject without requeue** | dead-letters it | none: nothing committed |

**A timeout is not proof that no effect committed.** Preserve identity on redelivery and resolve the
receipt/effect outcome before repeating an uncertain effect. The same-store transaction below owns local
deduplication; external effects use the reconciliation contract in
`alaa-reliability-sla references/60-idempotency.md`. Attempt expiry and job disposition are distinct under
`alaa-reliability-sla references/10-deadlines-and-timeouts.md`.

**A permanent failure is never requeued.** Requeuing it produces an immediate redelivery to the same or
another consumer, which fails identically and requeues again, and the loop consumes the whole consumer fleet
at the broker's redelivery rate. Classification and the DLQ route are `../40-dead-letter-and-replay.md`.

**A handler never acknowledges a message it did not process in order to clear a backlog.** That is deletion
with extra steps, and it is indistinguishable afterwards from successful processing.
