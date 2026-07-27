# Source Map

Read this file before repeating any version-sensitive claim about MongoDB, its drivers, or its Laravel
integration. TTL behaviour, retryable reads and writes, concern defaults, transaction limits, and connection
defaults have each changed across server and driver releases, so a claim carried from memory is a claim about
some earlier version.

## Source order

1. Repository truth first: the installed driver or ODM version, the collection access code, the index bootstrap
   or migration scripts, the runtime configuration, and the deployment topology. A local answer beats a general
   one, and the topology decides whether retryable writes, transactions, and change streams exist at all.
2. The MongoDB manual for server behaviour, at the version the deployment runs.
3. The driver, extension, or ODM documentation for client behaviour and defaults, because timeout and pool
   defaults are set by the driver and differ from the manual's connection-string page.
4. Community answers for troubleshooting only, and never as the source of an index restriction, a default, or a
   planner claim; verify each against the manual and against `explain()` before writing it down.

## Verified pages

Each row was fetched and read on 2026-07-26 and resolved.

| Page | What it settles |
|---|---|
| https://www.mongodb.com/docs/manual/ | Entry point for server behaviour at a specific version |
| https://www.mongodb.com/docs/manual/core/index-ttl/ | TTL indexes are single-field; compound indexes ignore `expireAfterSeconds`; `_id` unsupported; removal task runs every 60 s and stops at 50,000 documents or one second per index; deletion runs only on a primary; `expireAfterSeconds` addable to an existing index from 5.1 |
| https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/ | Index prefix behaviour; 32-field limit; sort-order rules |
| https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/ | ESR and ERS key ordering, and that `$ne`, `$nin`, and `$regex` count as range operators |
| https://www.mongodb.com/docs/manual/reference/method/cursor.skip/ | `skip()` scans from the beginning of the result set and degrades with offset; range queries are the documented alternative |
| https://www.mongodb.com/docs/manual/reference/write-concern/ | Implicit default `w: "majority"`, the arbiter formula that reduces it to `w: 1`, `wtimeout` semantics, and journal behaviour via `writeConcernMajorityJournalDefault` |
| https://www.mongodb.com/docs/manual/reference/read-concern/ | `"local"` is the default; the guarantees of `"majority"` and `"linearizable"` |
| https://www.mongodb.com/docs/manual/core/retryable-writes/ | Enabled by default for drivers compatible with 4.2+; one retry; replica set or sharded cluster only; multi-document writes and `w: 0` excluded; `serverSelectionTimeoutMS` bounds the failover wait |
| https://www.mongodb.com/docs/manual/core/retryable-reads/ | Enabled by default for drivers compatible with Server 6.0+; one retry; `getMore`, `mapReduce`, generic `runCommand`, and `$out`/`$merge` pipelines excluded |
| https://www.mongodb.com/docs/manual/core/write-operations-atomicity/ | Single-document writes are atomic even when modifying several values; multi-document atomicity requires a transaction |
| https://www.mongodb.com/docs/manual/core/transactions/ | Callback API retries `TransientTransactionError` and `UnknownTransactionCommitResult`; no server retry for `TransactionTooLargeForCache` from 6.2 |
| https://www.mongodb.com/docs/manual/core/transactions-production-consideration/ | Default runtime under one minute (`transactionLifetimeLimitSeconds`), aborted by a cleanup process; per-entry 16 MB oplog limit |
| https://www.mongodb.com/docs/manual/changeStreams/ | Replica set or sharded cluster on WiredTiger with protocol version 1; resume tokens need oplog history; `startAfter` for resuming past an invalidate event |
| https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/ | Monotonic shard keys bottleneck one shard; hashed sharding as the remedy; cardinality and frequency; `reshardCollection` from 5.0 |
| https://www.mongodb.com/docs/manual/reference/connection-string-options/ | `maxPoolSize` 100, `minPoolSize` 0, `connectTimeoutMS` 10,000 ms, `socketTimeoutMS` no timeout, `readPreference` `primary` |
| https://www.mongodb.com/docs/manual/reference/method/db.collection.bulkWrite/ | `ordered` defaults to `true` and stops at the first error; `maxWriteBatchSize` of 100,000 splits larger batches |
| https://www.mongodb.com/docs/manual/core/schema-validation/ | Validator concepts; validation level and action are documented on its child page, not here |
| https://www.mongodb.com/docs/php-library/current/ | MongoDB PHP library, current major version v2.x |
| https://www.php.net/manual/en/book.mongodb.php | The `mongodb` PHP extension the library sits on |
| https://laravel.com/docs/13.x/mongodb | `composer require mongodb/laravel-mongodb`, which requires the `mongodb` PHP extension |

## Read before quoting, not verified here

1. `serverSelectionTimeoutMS` — the connection-string page states no default; take the value from the driver's
   own documentation for the driver and version in use.
2. `validationLevel` and `validationAction` defaults — documented on the child page
   `https://www.mongodb.com/docs/manual/core/schema-validation/specify-validation-level/`, which was not read on
   2026-07-26; set both explicitly rather than assuming either.
3. `waitQueueTimeoutMS` and `maxIdleTimeMS` defaults — the manual defers to driver documentation.

## Freshness triggers

Re-verify against the manual and the driver documentation, and record the date, whenever the task mentions:
`latest`, `current`, an upgrade, a CVE or security fix, a server major version, Atlas-specific behaviour, TTL,
time series collections, compound indexes, transactions, retryable reads or writes, read or write concern
defaults, sharding, connection defaults, or a query-planner change.
