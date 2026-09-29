## 7. A replay produced duplicates

**Symptom.** Duplicate business effects appearing immediately after a replay, with the duplicate counter
still flat.

**Diagnosis.** The replay re-published messages with new identifiers, or the effects had already been
produced by another path — a manual operation or a reconciliation job — that wrote no receipt row. Check one
duplicated effect: a receipt row from the original delivery with a different key on the replayed message
proves the identifier was regenerated.

**Smallest safe action.** Stop the replay. Do not replay the remainder while identifiers are being
regenerated, because every remaining message will duplicate too.

**Escalation.** Reconcile the duplicated effects deliberately, one class at a time, before resuming.
Preserve the original identifier and idempotency key on any subsequent replay, and record the count
replayed, as `40-dead-letter-and-replay.md` requires.
