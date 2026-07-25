# The Call In A Loop

Load when a loop body reaches a database, service, cache, authorization check, or file.

`SKILL.md` owns the detection rule — a call that leaves the process, inside a loop whose iteration count is not a
constant written in the code — and the four resolutions in the order to try them. This file says how to find the
call when nothing at the call site looks like a call, how each resolution behaves in each medium, and what a batch
must state before it is finished.

## Finding the call when it is invisible

The defect is defined by effect, not syntax, and the expensive cases are the ones with no visible call. Look for
these shapes inside any loop over a non-constant collection:

| Shape | What it hides |
|---|---|
| A property or accessor on a domain object | A lazily loaded relation issuing one query per access |
| A getter that returns a related collection | One query per element, plus one per element of each result |
| A helper named `get`, `find`, `resolve`, `lookup`, or `ensure` | A cache miss path that falls through to the store |
| A permission or policy check | One authorization query or remote evaluation per element |
| A formatter, serialiser, or presenter | A lookup of a name, label, or translation per element |
| A logger or metric call carrying a resolved value | A resolution performed per element to build the message |
| A validation rule | A uniqueness query per element |
| A configuration or feature-flag read | A remote read per element where one read would do |

Two detection methods beat reading:

- **Count, do not inspect.** Assert the number of queries, outbound requests, or cache operations for a request over
  a fixture with more than one element, then over a fixture with more elements. A count that grows with the fixture
  is the defect, and this assertion is also the regression test that keeps it fixed. Whether such an assertion
  counts as evidence, and at which proof level, belongs to `/alaa-testing-strategy` (`$alaa-testing-strategy`).
- **Read the trace, not the code.** One request's trace shows the repeated span directly, and it finds the calls
  hidden behind three layers of abstraction that reading never finds. Trace and span design belongs to
  `/alaa-observability-soc` (`$alaa-observability-soc`).

## The resolutions, per medium

**Database.** One query with a join or an `IN` list over the collected keys; or the framework's eager-loading
mechanism, which each per-language clean-code skill owns. Two constraints on the `IN` list: it is chunked to a
stated maximum, because a very long list degrades planning and can exceed a parameter limit; and the query is
covered by an index on the queried column, which is `/alaa-data-layer` (`$alaa-data-layer`)'s decision.

**HTTP fan-out.** A batch endpoint where the callee offers one. Where it does not, bounded concurrency with an
explicit limit — never one request per element sequentially, and never unbounded parallelism, which converts your
loop into a denial of service against a service that is probably yours. The concurrency limit, the per-attempt
timeout, and the retry policy belong to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

**Cache.** A multi-key read or a pipeline, in one round trip. A cache lookup per element replaces a database N+1
with a cache N+1, which is faster per call and identical in shape — the round trips still grow with the collection.

**Authorization.** A bulk check that returns the permitted subset in one evaluation, rather than one check per
element. Where the authorization system offers no bulk operation, fetch the subject's relevant grants once and
evaluate in memory, provided the evaluation semantics are exactly the system's. The authorization model itself is
owned elsewhere; the shape of the call is owned here.

**Files.** One read of the whole index, or a streaming pass, rather than an open per element.

## Prefetch and index, in detail

The general resolution when no batch operation exists:

1. Walk the collection once and collect the distinct keys needed, deduplicated through the normalisation rules in
   `30-choosing-a-structure.md`.
2. Fetch every key in one call, chunked to a stated maximum when the key set can be large.
3. Build a map from key to result.
4. Walk the collection again, reading the map.
5. Decide explicitly what a missing key means — a default, a skip, or an error — because a prefetch turns "the
   lookup failed for this element" into "this key is absent from the map", and an unhandled absence reads as a
   silent skip rather than as a failure.

Step 5 is the one that gets omitted, and it is the one that changes behaviour rather than performance.

## What a batch must state before it is finished

Batching is not free; it trades many small independent failures for one large correlated one. A batch is unfinished
until all four are written down:

1. **Its maximum size**, enforced in code, with the reasoning for that maximum: a parameter limit, a payload limit, a
   memory bound, or a latency bound on the single call.
2. **What happens when part of it fails** — whether the whole batch is rejected, whether successes are kept, and how
   the caller learns which elements succeeded. A batch API returning one status for many elements hides partial
   success unless it reports per element.
3. **Whether the batch is retryable as a whole**, which requires that re-applying the successful elements is safe.
   Idempotency is `/alaa-reliability-sla` (`$alaa-reliability-sla`)'s and the fingerprint that identifies a repeat
   is normalised per `30-choosing-a-structure.md`.
4. **Its timeout**, which is not the per-element timeout multiplied by the batch size — that product usually exceeds
   the request deadline, and the deadline is owned by `/alaa-services-contract` (`$alaa-services-contract`).

## Anti-patterns

- fixing an N+1 by fetching the whole table into memory and filtering there, which replaces a bounded per-element
  query with one unbounded query;
- an `IN` list built from an unbounded collection;
- unbounded parallel requests introduced as the fix for a sequential loop;
- a batch with no maximum, no partial-failure semantics, and no timeout of its own;
- a prefetch with no decision about a missing key;
- eager loading applied everywhere by default, which loads relations no path uses and moves the cost from many small
  queries into one large one;
- declaring the defect fixed with no query-count or call-count assertion, so the next refactor reintroduces it
  invisibly.
