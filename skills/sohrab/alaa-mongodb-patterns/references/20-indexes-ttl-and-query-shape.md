# Indexes, TTL, And Query Shape

Read this file before adding, dropping, or reordering an index, before setting or changing a TTL rule, and when
explaining why a query or a deep page is slow. Every server behaviour stated here was verified against the
MongoDB manual on 2026-07-26; the page that settles each one is listed in `source-map.md`.

## Index rules

1. Every index names the query or invariant that justifies it, recorded next to the index definition. An index
   nobody can attribute to a query is write cost and resident memory buying no read.
2. Order compound keys by the manual's ESR guideline: equality fields first, because that keeps the remaining
   index fields in sorted order. Then place sort before range (ESR) when avoiding an in-memory sort matters
   most, or range before sort (ERS) when the range predicate is highly selective — state which of the two you
   chose and why.
3. Count `$ne`, `$nin`, and `$regex` as range operators when applying that order, as the manual does. Treating
   them as equality fields puts them in the wrong position and the sort falls back to memory.
4. Design the index so its prefix serves the shorter queries too: a compound index supports queries on the
   beginning subsets of its fields, so `{tenantId, contentId, createdAt}` also serves a `tenantId`-only filter
   and a `tenantId + contentId` filter, and a separate index for those is duplicated cost.
5. Keep a compound index within 32 fields, the manual's hard limit; an index approaching that number is a schema
   problem, not an index problem.
6. Enforce idempotency with a unique index rather than a read-then-write check. A read-then-write race admits the
   duplicate the check was added to prevent.
7. Justify each additional index on a write-heavy collection against its write cost, and delete an index no
   current query uses. Every index is updated on every insert and on every update touching its keys.
8. Attach `explain()` output from before and after to any claim that an index change helped. A plan claim without
   a plan is an assertion.

Default shapes for this estate:

```js
// tenant-scoped timeline or feed
db.comments.createIndex({ tenantId: 1, contentId: 1, createdAt: -1 });

// idempotent ingestion: the uniqueness that makes a replay safe
db.events.createIndex({ tenantId: 1, eventKey: 1 }, { unique: true });

// expiry of ephemeral records; single-field only
db.tokens.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
```

## TTL

1. Create a TTL index as a single-field index only. The manual states compound indexes do not support TTL and
   ignore `expireAfterSeconds`, so a compound TTL index silently never expires anything.
2. Keep query acceleration in a separate compound index when the collection is both tenant-scoped and expiring,
   because the TTL field cannot carry the tenant prefix.
3. Expire on a dedicated date field rather than on `_id`, because the manual states `_id` does not support TTL
   indexes.
4. Design every consumer of an expiring collection for a document that is past its expiry and still present. The
   removal task runs every 60 seconds, and each pass stops at 50,000 documents or one second of work per index,
   so expiry is eventual and falls behind under high delete volume.
5. Never use TTL as a security control: implement an explicit revocation check the read path performs, and use
   TTL only to reclaim storage. A token whose expiry is enforced solely by the sweep stays usable during the
   delay.
6. Expect no expiry at all while a replica set has no primary: the manual states the TTL thread deletes only on a
   primary and is idle on a secondary, which replicates the deletions. A long election is a retention pause.
7. State the expected steady-state size of an expiring collection, and make the gap between actual and expected
   observable per `40-failure-configuration-and-observability.md`. A sweep falling behind is invisible until the
   disk is full.
8. Reuse an existing single-field index by adding `expireAfterSeconds` to it from MongoDB 5.1; below that
   version, expiry requires a new index and a rollout.

## Query shape

1. Write the query's filter fields, sort fields, and expected result size before choosing an index, and confirm
   the tenant key leads the filter.
2. Add the smallest index that serves filter and sort together; adding one index per query is how a write-heavy
   collection acquires an index set nobody can remove.
3. Return only the fields the caller uses. A projection that covers the query is served from the index alone.
4. Resolve a query that runs once per element of a result set — the N+1 shape — before tuning the index it uses.
   The complexity bound and the decision of what to do about it belong to `/alaa-algorithms-data-structures`
   (`$alaa-algorithms-data-structures`) `references/40-call-in-a-loop.md`; the index and query shape the chosen
   fix lands on belong here.
5. Page with a range predicate on the same fields and directions as the ordering index, never with `skip` for a
   deep page: the manual states `skip()` requires the server to scan from the beginning of the result set and
   becomes slower as the offset grows. The cursor contract — its encoding, its sort allowlist, its stability
   rules and its error cases — is owned by `/alaa-keyset-pagination` (`$alaa-keyset-pagination`), and only the
   Mongo-side predicate and index are decided here.
6. Confirm the sort is served by the index rather than performed in memory before calling a paging query
   finished, because an in-memory sort re-reads and re-sorts the whole candidate set on every page.
