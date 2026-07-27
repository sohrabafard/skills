# Modeling, Tenancy, And Collection Shape

Read this file before creating a collection, changing which fields a document carries, adding a schema validator,
or choosing a shard key. Every server behaviour stated here was verified against the MongoDB manual on
2026-07-26; the page that settles each one is listed in `source-map.md`.

Whether the fact belongs in MongoDB at all is not decided here: that is the store-selection decision owned by
`/alaa-data-layer` (`$alaa-data-layer`). Whether a stale read is acceptable, and which component may write a
field, are owned by `/alaa-system-design` (`$alaa-system-design`) `references/30-data-and-consistency.md`.

## Model around the query set

1. Write the read set before the schema: for each query, its filter fields, its sort fields, and the number of
   documents it returns. A schema designed without its query set produces indexes discovered under production
   load instead of at review.
2. Embed a sub-object when it is read with its parent and written with its parent. Embedding data written on a
   different cadence turns every child write into a rewrite of the whole parent document.
3. Reference by id when the related data is large, shared between parents, or written independently. The cost of
   the extra read is bounded; the cost of a rewritten parent is proportional to document size.
4. Give each collection one document shape. A collection holding several shapes needs an index per shape, and
   every added index is write cost paid on every insert.
5. Store the field the query filters on, not a value the query must compute. A filter over a computed expression
   cannot use an index.

## Bounded documents

1. MongoDB refuses a document above the 16 MB BSON limit, so every array or map field has a stated ceiling and a
   write-time enforcement point. Unbounded growth surfaces as a write failure in production, not as a slow query.
2. Write one document per event, comment, or reaction when the count per parent has no natural bound. The
   parent-embedded timeline has no upper bound and therefore no safe ceiling.
3. Use a bucket document only with a cap on both element count and time window, enforced in the write itself —
   for example `$push` with `$slice`, or a bucket key derived from the time window. A cap that only appears in a
   comment is not enforced.
4. State the expected growth before shipping: write rate multiplied by retention window gives collection size and
   index size. A design with no stated growth number cannot be capacity-reviewed.
5. Keep large payloads out of the collection the hot queries read. Store the payload where it belongs and keep a
   reference, because every read of the hot collection pays for the bytes it does not use.

## Tenancy

1. Every tenant-owned document carries the tenant key as a real field, not as a value encoded inside another
   field. A key that must be parsed cannot be indexed or filtered on directly.
2. Every query against a tenant-owned collection filters on the tenant key, and every uniqueness constraint on
   such a collection includes it. A global unique key lets one tenant's business key block another's.
3. Treat a missing tenant filter as a security finding, not a performance finding: the failure mode is a
   well-formed `200` carrying another tenant's data. The threat class, the review trigger, and the fail-closed
   rule are owned by `/alaa-security-review` (`$alaa-security-review`)
   `references/40-authorization-and-tenancy.md`.
4. State the largest expected tenant's share of the collection when a tenant-prefixed index is proposed. One
   tenant holding most of the documents removes the selectivity the prefix was chosen for.

## Schema validation

1. Declare `validationLevel` and `validationAction` explicitly on every validator instead of relying on the
   server default, because the applied behaviour differs by level and the default is version-sensitive; confirm
   current behaviour through `source-map.md` before quoting one.
2. Validate the invariants other code already assumes: tenant key present, business key present and typed,
   timestamps present. A validator that repeats the whole document is a second schema to keep in sync.
3. Ship a validator that rejects writes only after the writers that would fail are gone. Adding a required field
   while an older writer is still deployed converts a deploy into a write outage; the rollout order is in
   `50-applying-and-proving.md`.

## Shard key, when the deployment is sharded

1. Choose a shard key whose values do not increase or decrease monotonically, because the manual states all new
   inserts then route to the chunk holding `maxKey` or `minKey` and that one shard becomes the write
   bottleneck.
2. Use hashed sharding when the data model requires sharding on a monotonic value, which is the manual's own
   remedy for that case.
3. Choose a shard key with high cardinality, because cardinality caps the number of chunks the balancer can
   create and each shard-key value lives in at most one chunk.
4. Check value frequency as well as cardinality: if most documents carry a small subset of the key's values, the
   chunks holding those values become the bottleneck.
5. Treat a shard key as changeable but expensive — `reshardCollection` exists from MongoDB 5.0 and rewrites the
   collection's distribution. Plan the key as if the change were unavailable.
