# Applying, Rolling Out, And Proving A MongoDB Change

Read this file before handing back a MongoDB design, before rolling out an index, TTL, validator, or backfill
change, and when deciding what proof that change needs. Every server behaviour stated here was verified against
the MongoDB manual on 2026-07-26; the page that settles each one is listed in `source-map.md`.

## What a MongoDB change hands back

State all nine, in this order, for every change this skill produces:

1. The collection and document shape, with the ceiling on every field that can grow and where that ceiling is
   enforced.
2. The query set the shape serves — filter fields, sort fields, expected result size — including the tenant
   filter.
3. Each index, with the query or invariant that justifies it and the plan evidence that it is used.
4. The write pattern chosen (insert, upsert, bulk, transaction) and the deduplication key that makes a replay
   safe.
5. The retention rule, its TTL mechanism if any, and the explicit revocation check where expiry carries security
   meaning.
6. The failure behaviour: deadline, retry budget, and what the caller receives when the operation fails.
7. The knobs and environment keys the change introduces, with the owner of each value named.
8. The signals that make the change observable, using registered names only.
9. The risks — write amplification, contention, document growth, expiry backlog — each with the mitigation that
   answers it.

A change missing one of the nine is incomplete, because the missing item is the one nobody will notice until it
fails.

## Proof

The six proof levels, and which level a given claim requires before merge, are owned by
`/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`. This file states only the
floor that MongoDB mechanics impose:

1. A change to document-shape code, mapping code, or a query builder is provable at level 2, because the claim is
   about the code's output rather than about the server.
2. A claim that an index is selected, that a unique index rejects a duplicate, that a TTL rule removes a
   document, that a resume token resumes a stream, or that a transaction aborts at its limit requires level 6
   against a real MongoDB. A test double reproduces neither the query planner, nor the removal task, nor the
   oplog.
3. A claim about retryable writes, retryable reads, or election behaviour requires level 6 against a replica set,
   because the manual states retryable writes are not supported on standalone instances — a single-node
   deployment proves nothing about them.
4. A claim about query performance requires the plan and the timing from a collection of comparable size and
   distribution, stated with that size. A plan taken from an empty collection describes an empty collection.

## Rollout

1. Create an index before deploying the code that depends on it, and drop an index only after the code that used
   it is gone. The reverse order makes the first request after deploy a collection scan.
2. Build an index on a populated collection through the deployment's non-blocking path, and confirm the build
   finished before treating the query as fast. An unfinished build is not an index.
3. State the expected drain time before changing a TTL rule on a large collection, and watch the backlog signal
   until it returns to the stated steady state. Each removal pass stops at 50,000 documents or one second per
   index, so a large retention change deletes over hours and can outrun that budget indefinitely.
4. Deploy a stricter validator only after every writer that would fail it is gone, and record the writer versions
   checked. A validator is a write outage for any code that predates it.
5. Make every backfill idempotent, resumable from its last committed position, and batched, and run it with the
   same write concern as the production path. A backfill that cannot resume restarts from zero on every
   interruption.
6. Record the reversal for each step — drop the index, restore the previous `expireAfterSeconds`, remove the
   validator — before starting. A step with no stated reversal turns a rollback into an incident.

## Anti-patterns and what replaces each

| Do not | Do instead |
|---|---|
| Propose MongoDB for a repository that does not run it | Route the store decision to `/alaa-data-layer` (`$alaa-data-layer`) and stop |
| Add an index "in case a query needs it" | Add the index the written query set requires, and record that query beside it |
| Let an array grow with the parent's activity | Give the array a ceiling enforced at write time, or one document per element |
| Rely on a TTL index to revoke access | Check revocation explicitly on the read path, and use TTL only to reclaim storage |
| Rely on the deployment's default write concern | State the concern on the write path, per `30-writes-consistency-and-change-streams.md` |
| Retry a failed write in application code without a budget | State the total attempt budget under `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Consume at-least-once delivery without a deduplication key | Back the deduplication key with a unique index and acknowledge the duplicate-key error |
| Page with `skip` | Page with a range predicate on the ordering index, under `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) |
| Query a tenant-owned collection without the tenant filter | Filter on the tenant key and treat its absence as a security finding |
