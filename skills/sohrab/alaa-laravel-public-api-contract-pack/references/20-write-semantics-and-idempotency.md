# Write Semantics And Idempotency

Read this before documenting any route that is not a read, and before answering "may a
consumer retry this".

**Not owned here.** Why a caller retries at all, retry budgets, backoff, circuit breakers and
degradation are `alaa-reliability-sla` (`/alaa-reliability-sla`, `$alaa-reliability-sla`).
Every number — attempt counts, backoff bounds, the minimum key-retention period — and the
`Idempotency-Key` contract itself are `alaa-services-contract` (`/alaa-services-contract`,
`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`. The error
envelope is that skill's `references/10-core-service-contract.md`. On any conflict about a
value or a field name, that skill wins. This file fixes what the **pack** states per write
route so a consumer can decide, without reading service code, whether repeating a request is
safe.

## Four statements per write route, none optional

**1. The retry-safety verdict**, exactly one of `retry_safe`,
`retry_with_idempotency_key`, `not_retry_safe`. There is no fourth value and no prose hedge:
"generally safe" and "safe if the transport failed" are not verdicts, because a consumer
cannot branch on them. The verdict is read from the handler, not from the verb — see the verb
table below — and the pack cites the controller method that earns it.

**2. The key's spelling on this route**, when the verdict is
`retry_with_idempotency_key`: whether the route accepts the `Idempotency-Key` header or an
`idempotency_key` request field, taken from the FormRequest rule or middleware that reads it
and cited by path and line. Record the spelling the route actually accepts; a route
documented with the fleet's internal spelling while its FormRequest validates a body field
sends every consumer's retry to a `422`. Where the two differ, that difference is itself a
finding for the repository owner and goes in the pack's drift list.

**3. The conflict behaviour**: the status and the `code` returned when the same key arrives
with a different meaningful payload, cited from the code that returns it. A route that
accepts a key and silently performs the work twice is not
`retry_with_idempotency_key`; it is `not_retry_safe` and the mismatch is a drift finding.

**4. The replay window**: how long a stored key is honoured, read from the repository — a
config key, a cache TTL, a migration's retention column. When the repository does not fix it,
the route is documented `not_retry_safe`. Do not copy the fleet minimum into the pack as
though the repository proved it.

A `not_retry_safe` route additionally carries `x-idempotent: false` on its operation, per
`references/10-versioning-and-breaking-change-classification.md`, because that record is what
sets a caller's retry budget to zero.

## The verb table, and why the verb is not the answer

| Verb | Documented as | Condition |
|---|---|---|
| `GET`, `HEAD` | `retry_safe` | the handler performs no write, including no counter, no last-seen timestamp, no audit row |
| `PUT`, `DELETE` | `retry_safe` | the handler **sets** a state to the value in the request; a `PUT` that toggles, increments, or appends is `not_retry_safe` |
| `PATCH` | `retry_safe` | the patch replaces the named fields wholesale; a patch that appends to a collection or adjusts a value relative to its current one is `not_retry_safe` |
| `POST` | `not_retry_safe` | unless the route accepts a key, in which case `retry_with_idempotency_key` |

A `PUT .../favorite` that writes `favored = true` is idempotent. A `PUT` that flips the
current value is not, and it returns a different result on the second call. Observable: for
every write route the pack names the controller method and states which of the three verdicts
it earns; a route documented only by its verb has not been classified.

## Errors on a write route

The envelope is fixed fleet-wide and is not restated here. The pack's obligation is
**enumeration**: every `code` this write route can actually emit, derived from its validation
rules, its authorization gates, its dependency failures, and the service's committed code
registry — never guessed, and never widened to "any 4xx". What makes that enumeration
complete, and the saved-example coverage that proves it, is
`alaa-postman-collections` (`/alaa-postman-collections`, `$alaa-postman-collections`)
`references/41-response-contract-and-error-coverage.md`, which wins on coverage questions.

Where a write's failure is transient and the caller may try again, the retry hint travels in
the error envelope's `meta`, whose contents are bound by
`alaa-services-contract references/10-core-service-contract.md`. The pack documents which of
this route's failures are transient; it does not define the field.

## Asynchronous writes

A write that returns a queued receipt — a `201` or `202` whose body says the effect is not yet
persisted — documents three things or it is not documented: what a consumer may assume the
moment it receives the receipt, which read route reflects the effect once the worker has run,
and that the read is eventually consistent. Observable: the pack names that read route by
method and path, and a saved example shows the receipt body. A queued receipt documented as a
success with no named follow-up read is a contract that cannot be consumed, because the client
has no way to learn the work happened.

Queue, job, and retry mechanics behind such a route are
`alaa-async-messaging` (`/alaa-async-messaging`, `$alaa-async-messaging`) and
`alaa-laravel-job-rabbitmq` (`/alaa-laravel-job-rabbitmq`, `$alaa-laravel-job-rabbitmq`);
the pack documents only the consumer-visible half.
