# Writes, Consistency, And Change Streams

Read this file before writing, upserting, or batch-loading documents, before choosing a read or write concern,
before opening a transaction, before incrementing a counter, and before reading a change stream. Every server
behaviour stated here was verified against the MongoDB manual on 2026-07-26; the page that settles each one is
listed in `source-map.md`.

Why a write must be idempotent, how many times it may be attempted, and what a caller sees when it is not
applied are doctrine owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`)
`references/60-idempotency.md` and `references/20-retries.md`. This file owns only the MongoDB mechanism that
implements that doctrine.

## Idempotent writes

1. Give every ingested record a deduplication key derived from the source event, not from arrival time, and back
   it with a unique index. A key generated at write time cannot recognise a replay.
2. Express the ingest as an upsert whose insert-only fields sit under `$setOnInsert`, so a replay updates
   nothing:

```js
db.events.updateOne(
  { tenantId, eventKey },
  { $setOnInsert: { tenantId, eventKey, createdAt: new Date(), payload } },
  { upsert: true }
);
```

3. Treat a duplicate-key error on the deduplication key as "already applied" and acknowledge, because
   at-least-once delivery makes that error the expected outcome of a replay rather than a fault.
4. Make a write that must both insert and mutate carry a monotonic source version, and apply it only when the
   stored version is older. Last-write-wins on out-of-order delivery silently reverts state.

## Batch writes

1. Use `bulkWrite` when the batch is known up front, because each round trip costs a full network latency.
2. Set `ordered` explicitly. The manual's default is `true`, which stops at the first failing operation and
   leaves the rest unapplied; `false` continues past failures, so the choice decides whether a batch is
   all-or-nothing-so-far or best-effort.
3. Handle the per-operation result rather than the call's return alone: with `ordered: false` some operations
   succeed while others fail, and only the per-operation errors say which.
4. Size a batch against `maxWriteBatchSize`, documented at 100,000 operations, above which the driver splits the
   batch into groups. A batch large enough to be split is a batch whose failure boundary you no longer control.
5. Build a batch from single-document operations when retryability matters, because multi-document operations
   such as `updateMany` and `deleteMany` are outside the retryable-write contract described in
   `40-failure-configuration-and-observability.md`.

## Write and read concern

1. State the write concern on every write path instead of relying on the deployment default. The manual computes
   the implicit default as `w: "majority"` except in topologies with arbiters where data-bearing voting members
   do not exceed the voting majority, in which case it is `w: 1` — the same code is then durable in one
   deployment and not in another.
2. Use `w: "majority"` for any write whose loss would be visible to a caller or to another service, because a
   `w: 1` write can be rolled back when the primary that accepted it fails.
3. Set `wtimeout` on any write that must not block indefinitely: the manual states that without it an
   unachievable write concern blocks forever, and that exceeding it does not undo the write. The Ala values for
   these bounds are owned by `/alaa-services-contract` (`$alaa-services-contract`)
   `references/22-failure-load-and-deprecation-contract.md`.
4. Check `writeConcernMajorityJournalDefault` on the deployment before describing a `w: "majority"` write as
   durable on disk. It defaults to `true`, and where it has been disabled a majority write can still roll back
   after a crash.
5. Read with `readConcern: "majority"` when the read must not observe data that may roll back; the manual's
   default is `"local"`, which carries no such guarantee. Reserve `"linearizable"` for the case that needs it —
   the manual warns it may be significantly slower.

## Transactions

1. Do the work in a single document where the invariant allows, because the manual guarantees atomicity at the
   single-document level even when the write modifies several values.
2. Open a multi-document transaction only when an invariant spans documents. A multi-document write that is not
   in a transaction is atomic per document and not as a whole.
3. Keep a transaction under the server's runtime limit, documented as one minute by default
   (`transactionLifetimeLimitSeconds`), after which a periodic cleanup process aborts it as expired.
4. Perform no network call, no broker publish, and no external write inside a transaction. External work cannot
   be rolled back with the transaction, and it extends the transaction toward the abort limit.
5. Retry on `TransientTransactionError` and `UnknownTransactionCommitResult`, which the driver's callback API
   already does, and abort rather than retry on `TransactionTooLargeForCache` — the manual states the server
   stops retrying that one from MongoDB 6.2.
6. Keep each transaction's oplog entry within the 16 MB BSON limit that the manual still applies per entry, and
   split a bulk change into batches rather than one transaction.

## Counters and aggregates

1. Bound the write rate any single counter document receives, because every increment serialises on that
   document and the contention is invisible in a query plan.
2. Shard a hot counter across a bounded set of documents and sum on read, or compute the aggregate periodically
   in the analytical store owned by `/clickhouse-performance-schema-ops`
   (`$clickhouse-performance-schema-ops`). State which of the two you chose and the staleness it accepts.
3. Use `$inc` on a document designed for it when the rate is low enough to be stated. A counter with no stated
   rate has no design.

## Change streams

1. Confirm the deployment supports a change stream before designing around one: the manual requires a replica
   set or sharded cluster on WiredTiger with replica set protocol version 1.
2. Persist the resume token in the same write as the effect it records; when the effect lands in another store
   and no single write covers both, persist the token only after that effect is durable. A token stored ahead of
   its effect skips every event between the two on restart.
3. Handle the case where the resume point has aged out of the oplog: the manual requires the oplog to still
   contain the operation the token refers to, so the consumer needs a documented recovery path rather than a
   crash loop.
4. Use `startAfter` to resume past an invalidate event such as a collection drop or rename, since the manual
   states `resumeAfter` cannot resume after one.
5. Treat the stream as one delivery source among others and stop at the boundary: consumer acknowledgement,
   retry, dead-letter and replay mechanics are owned by `/alaa-async-messaging` (`$alaa-async-messaging`), and
   remain owned there while that skill is thin, because two owners for one rule produce two answers.
