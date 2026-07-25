# Idempotency

Read whenever a caller may repeat a state-changing request, whenever a retry is being made legal under `20-retries.md`, and always before a key store is designed. This file owns the whole request-side contract. `/alaa-services-contract` (`$alaa-services-contract` in Codex) owns the header name, the key format, the retention period, and the response codes — `references/22-failure-load-and-deprecation-contract.md`. Consumer-side deduplication of broker messages belongs to `/alaa-async-messaging` (`$alaa-async-messaging`).

An idempotency guarantee is the precondition for every retry of a non-naturally-idempotent operation, so a gap anywhere in the eight sections below is a gap in every retry that depends on it.

## 1. Who supplies the key

**The client that originates the logical operation generates the key, once per operation, and sends it byte-for-byte unchanged on every retry of that operation.** The server never generates it, because a server-generated key is new on each arrival and therefore identifies nothing.

- A new key per attempt is not a retry. It is a second operation, and it will produce a second effect exactly as it asked to.
- A key must not be derived from the request content. A content hash cannot distinguish an honest retry from an intentional repeat — two legitimate identical transfers a minute apart hash identically — so it silently suppresses the second real operation. The key is supplied; the content is fingerprinted separately, per section 7.
- Where the originating client cannot hold a key across a retry — a browser form, a webhook sender with no key support — the first hop that *can* hold one generates it and owns the retry for the whole chain, and no layer above it retries. This is the same single-retrying-layer rule as `20-retries.md`, applied to key ownership.
- A key is opaque to the server: it is compared, never parsed, and never used to derive an identifier, a partition, or an ordering.

## 2. Absent or malformed

| State | Behaviour | Why |
|---|---|---|
| Absent, on a route that requires a key | Reject with the validation failure that names the header. Perform nothing | Proceeding accepts an unretryable write on a route documented as retryable, and the caller's retry policy will then duplicate it |
| Malformed — wrong format, wrong length, wrong character set | Reject with the same validation failure. Perform nothing | Never normalise, truncate, lowercase, or hash it into shape: the caller's retry produces a different normalisation of the same bad input and the two no longer collide, so the guarantee silently disappears |
| Present, on a route that does not store keys | Reject with the validation failure | Accepting a key and ignoring it is the worst available behaviour: it advertises a guarantee the route does not have, and every caller then retries safely-as-far-as-it-knows |
| Absent, on a route that does not require a key | Proceed. The route documents itself as non-idempotent, and every caller sets its retry count to zero | A route whose documentation is silent is treated by callers as non-idempotent, so it is not retried |

## 3. Scope

The key's uniqueness is scoped to **the tenant or project, the operation identity, and the key** — all three, together, as the constraint's columns.

- **Never a global namespace.** One tenant's key colliding with another's returns the first tenant's stored response to the second, which is a cross-tenant data leak rather than a duplicate-suppression bug.
- **Never wider than the operation.** The same key presented to two different operations is a conflict, not two independent successes, because a caller that reuses a key across operations has a defect and the guarantee it believes it has is void.
- **Never narrower than the operation**, and specifically not scoped per attempt, per connection, per process, or per node. A key store that is local to one instance guarantees nothing, since the retry lands on a different instance.

## 4. Retention, and what happens after expiry

Retention is derived from **the longest legal retry horizon of any caller of this route**, not from a convenient default. Enumerate the retry paths before choosing: the synchronous client's own budget, an outbox or queue worker draining after an outage, a scheduled reconciliation job, and a human pressing the button again. The retention exceeds the slowest of them.

After expiry the key is unknown, so a replay of it **executes as a new operation and produces a real duplicate.** That is the honest consequence and it is why the derivation matters. Two rules follow:

- The retention window is stated in the route's documentation, so a caller can know whether its own retry horizon fits inside it.
- A route whose duplicate would be unacceptable at *any* horizon does not rely on the key's retention alone. It also carries a **business-level uniqueness constraint** — one settlement per invoice per period, one enrolment per user per course — because an idempotency key bounds duplicates in time while a business constraint bounds them absolutely.

Expiry is a deletion of the record, not a reuse of the key: a key whose record has expired is treated as never seen, never as "seen and finished".

## 5. Where the guarantee actually lives

**The guarantee is a uniqueness constraint in the same transactional store as the effect. It is not a check in application code, and it is not a lock in a different system.**

The procedure:

1. Insert a key row — scope columns, key, state `in_progress`, a lease expiry, and the request fingerprint — inside the transaction that will perform the effect, or inside a transaction the effect joins.
2. If the insert succeeds, this request owns the operation. Perform the effect, then update the row to `completed` with the stored response, in the same transaction.
3. If the insert is rejected by the constraint, a first request exists. Go to section 6 if it is `in_progress`, section 7 if it is `completed`.

Why the constraint and not a check: **read-then-write is check-then-act, and two concurrent requests both pass it.** Both read "no key", both proceed, both perform the effect. This is not a rare interleaving; at any real concurrency with a retrying client it is the common case, and it is invisible in sequential testing. The database's unique index is the only component in the path that can decide the race, because it is the only one that serialises.

Why the same store as the effect: two stores can disagree. The key commits and the effect rolls back, so a legitimate retry is refused forever and the operation never happens. Or the effect commits and the key write fails, so the next retry duplicates. Where the key genuinely must live elsewhere — the effect is in an external system with no transaction to join — that design is the weaker one, and it is chosen explicitly, named in the route's documentation, and paired with a reconciliation path that detects and resolves the disagreement. A distributed lock is not a substitute: it fails open on expiry and on partition, which is the moment it was needed.

## 6. Two requests with the same key, both in flight

This is the case that breaks under load and passes every sequential test.

**The second concurrent request with a key already in `in_progress` never performs the work, and never waits without a bound.** The constraint's rejection in section 5 is what tells it a first request exists; its outcome is exactly one of two, chosen by the route in advance and stated in the route's documentation:

- **Reject as in-progress** — return the in-progress conflict status with a retry hint, immediately, having performed nothing. This is the default: it is honest, costs nothing, holds no resource, and the caller already has a retry policy that will bring it back.
- **Wait, then replay** — wait for the first request's completion for at most the caller's remaining deadline, then return the first request's stored response; on deadline expiry, return the in-progress conflict status. Permitted only where the route documents it, and the wait is bounded by the deadline, never by a fixed sleep loop and never by a retry count.

**Never let the second request proceed on the grounds that the first has not finished yet.** That is precisely the case an existence check cannot see, and it is the only case that appears exclusively under concurrency — which is why it survives into production.

The `in_progress` row carries a **lease** so that a caller which died mid-operation does not hold the key forever. The lease is longer than the operation's own total timeout, so a slow-but-live operation is never displaced by a second attempt; on expiry the row is claimable by a new attempt, and the claim is itself a conditional update that only one claimant can win. A lease shorter than the operation's timeout re-creates the duplicate it was added to prevent.

## 7. Replay versus conflict, after the first request completed

Distinguish them by a **fingerprint** of the request stored with the key, and return different things.

- **Replay — same key, same fingerprint.** Return the **stored** response: the same status, the same body, the same identifiers the first attempt minted. Perform nothing. Mark it as a replay in telemetry so a review can see the mechanism fired. Returning a fresh success with a new identifier is not idempotent — it has created a second resource under a key the caller believes is unique, and the caller now holds one of the two identifiers with no way to learn about the other.
- **Conflict — same key, different fingerprint.** Reject with the conflict status. Perform nothing, and do **not** return the first request's stored response. Both alternatives are wrong: performing the second operation duplicates under a key the caller believes is unique, and returning the first's response tells the caller that its own, different request succeeded when it never ran.

The fingerprint is computed over exactly the fields that determine the effect, canonicalised so that key order and encoding do not matter. It **excludes** everything that legitimately changes between retries — request and trace identifiers, timestamps, client-generated attempt counters, headers — because including any of them makes every honest retry read as a conflict, and the route then appears broken precisely when the mechanism is working.

The stored response is the **response**, not a status flag. A caller retrying after a lost reply needs the identifiers the first attempt created; storing only "succeeded" leaves it with a success it cannot act on.

## 8. When the idempotency store is unavailable

The guarantee is gone, so the choice is between a duplicate and a failure, and the route decides which is worse **in advance**.

- **Default: fail the request** with the dependency-unavailable outcome. A duplicated state change is frequently unrecoverable, while a failed request is retryable by a caller that already has a retry policy.
- **Never proceed unrecorded** on the reasoning that the operation "is not usually retried". Whether it is retried is decided by the caller's retry policy and by the human at the other end, not by the server's optimism.
- A route that must proceed anyway does three things in the same change: documents it, **names the downstream constraint that actually prevents the duplicate** — a business uniqueness index, a downstream provider's own idempotency — and emits a distinct event so the unguarded window is visible afterwards. "We accepted the risk" with no named constraint is an unbounded duplicate window.

When the key lives in the same store as the effect, per section 5, this case collapses into "the store that holds the effect is unavailable", the request fails for that reason, and there is no unguarded window at all. That is one more argument for co-locating them.

## Natural idempotency is not free

An operation described as naturally idempotent still needs checking against its actual implementation. A `PUT`-shaped full replacement is idempotent; the same route is not if it appends to a collection, increments a counter, emits an event per call, or writes an audit row per call. A delete is idempotent in effect and often not in reporting: the second delete must return the same success as the first rather than a not-found that a caller reads as a failure. A conditional update guarded by a version is idempotent for the first arrival and returns a conflict for the second, which is correct only if the caller can distinguish "someone else changed it" from "this is my own retry" — and it cannot, without a key.
