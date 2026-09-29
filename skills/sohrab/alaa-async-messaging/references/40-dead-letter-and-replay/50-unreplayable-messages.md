# Unreplayable messages

## Unreplayable messages

A message in a dead-letter queue is not always work that is owed. These are unreplayable, and each is
handled by naming it rather than by replaying it:

- **Its effect has already happened by another path** — a human ran the operation manually, or a
  reconciliation job produced it. Replaying duplicates an effect that idempotency cannot catch, because the
  other path wrote no receipt.
- **Its owner-defined business validity ended or it was explicitly cancelled.** An expired one-time
  password or time-boxed instruction can mislead its recipient. Use the owning contract, never the
  originating HTTP deadline or an assumed universal lifetime.
- **The entity it references is permanently gone.** The replay will fail identically, so it is a way of
  making the same message fail twice.
- **Its body is malformed and the producer's defect is fixed.** The correct output is a new, well-formed
  message from the producer, not a replay of a body no consumer can parse.

**Record every unreplayable message**: its identifier, tenant, original routing key, and reason it was not
replayed. Apply the owner's observable terminal/reconciliation outcome and retention contract before any
discard; the record alone authorizes no deletion. If that policy is absent, report the missing decision
under `alaa-reliability-sla references/10-deadlines-and-timeouts.md`. Silent loss and indefinite execution
are not substitutes for that decision.
