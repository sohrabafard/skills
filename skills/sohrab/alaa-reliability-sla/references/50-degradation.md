# Graceful Degradation

Read when a dependency may be optional, when a cache is used to survive an outage, or when a response can be partial. `SKILL.md` holds the binding rules: every dependency is declared required or optional before it fails and an undeclared one behaves as required, a degraded response says so in a machine-readable field, and an untested degraded path is not a degraded path. This file is the classification test, the response shapes, and the cache rules.

Degradation is availability work and applies only to contributors. A dependency that decides whether a caller may act is a gate and has no degraded mode — see the discrimination rule in `SKILL.md` and `/alaa-security-review` (`$alaa-security-review` in Codex).

## Classifying a dependency before it fails

One question does the work: **if this dependency returns nothing, is there a response that is still correct — merely smaller, older, or less precise?**

- Yes → optional. The response omits or substitutes the contribution and marks itself.
- No → required. The request fails.

Two clarifications that decide most real cases:

- "Correct" means a caller acting on the response cannot be misled. A recommendation list that is empty because the recommender is down is correct-but-smaller. A balance that is missing a pending-charges lookup is not smaller, it is **wrong**, and rendering it as a balance misleads. The test is not whether a field can be omitted; it is whether the remaining fields still mean what they claim.
- Classification is **per route and per operation**, not per dependency. The same search index is optional on a browse page and required on a search results page. A single service-wide list of optional dependencies is the shape this rule is most often violated in.

Record the classification where the code that calls the dependency reads it — a constant, a policy object, or a configuration key at the call site — and in the route's documentation. Two reasons the location matters: a classification held only in a runbook cannot change the code's behaviour, and a classification made during an incident is made under the belief that everything is required, which is why the rule requires it in advance.

**Classify the aggregate, not only the parts.** A route with six optional dependencies whose contributions are each individually omissible may still be worthless with all six missing. Where that is true, declare the minimum set that must be present for the response to be worth returning, and fail below it.

## The degradation ladder

Take the highest rung the route can honestly reach. Each rung is a different answer, and the marker in the response says which one was used.

1. **Complete** — every contribution present.
2. **Substituted** — the contribution came from a cheaper or older source: a cached value inside its stale bound, a precomputed default, a coarser aggregate. The response names the substitution and the value's age.
3. **Omitted** — the contribution is absent, and the field is explicitly absent or explicitly null rather than zero, empty, or a plausible default. A degraded value that looks like data is worse than a missing one, because nothing downstream can detect it.
4. **Reduced scope** — fewer items, a shorter window, one page instead of all pages. Honest, and often the best rung under load.
5. **Rejected** — the request fails, because a required contribution or the declared minimum set is unavailable.

Two rungs are not on the ladder and are never used: returning a fabricated value in place of the missing one, and returning success with a shape the caller cannot distinguish from complete.

## How the caller knows

A degraded response carries an explicit, machine-readable marker naming **which** contribution is missing or substituted and, for a substituted value, **how old** it is. Human-readable text in an error field is not a marker, because no client branches on it.

Why this is not optional: a silent degradation is by construction indistinguishable from real data. A client caches it, a downstream service aggregates it into a report, a batch job writes it to a warehouse, and the incident surfaces weeks later as a data-quality question that nobody connects to an outage. The marker is the only thing that lets a caller decide whether to retry, to show its own degraded state, or to refuse to cache.

Three obligations that follow:

- **Do not cache a degraded response** as if it were complete, and do not let an intermediary cache it. A degraded response's cacheability is decided by the marker's presence, not by the status code.
- **Propagate degradation up the chain.** A service whose optional dependency degraded returns its own marker; a service whose upstream returned a marker either resolves the gap itself or forwards the fact. Degradation that stops being reported at the first hop makes the top-level response a lie by omission.
- **Emit the signal.** A degraded response is an event, distinct from a failure and from a success, and its rate is the only way to know the degraded path is running at all. `/alaa-observability-soc` (`$alaa-observability-soc`) owns the signal's requirement level; `/alaa-services-contract` (`$alaa-services-contract`) owns the field and event names.

The status code stays a success code when a degraded response is genuinely useful, because a caller that treats it as a failure will retry and multiply the load during the incident. The marker, not the status, carries the degradation.

## A degraded path exists only if it is exercised

The rule is in `SKILL.md`. What it requires concretely, per route and per declared-optional dependency: an automated test that runs the route with that dependency failing — timing out, refusing the connection, and returning an error, since the three take different code paths — and asserts the status, the marker's contents, and that the rest of the response is complete.

When such a test does not exist, the dependency is treated as required, because that is the behaviour the code will actually have. Declaring a dependency optional without the test is a claim about untested code, and the claim is usually wrong: the common defects are an exception that escapes the fallback, a fallback that itself calls the failing dependency, and a fallback that returns a zero value the caller reads as data.

`80-verification.md` owns the injection method and what evidence a review accepts.

## Caches: which outage a cache may absorb

**A cache may absorb an outage of the cache. It must never absorb an outage of the system that owns the truth.**

The asymmetry is not a preference. On a cache failure, a correct answer is still available — the origin has it — so bypassing the cache is a latency and load problem and nothing more. On an origin failure there is **no** correct answer available, so serving a cached value substitutes a statement about the past for a statement about the present, and the caller cannot tell which one it received.

The rules that follow:

- **On a cache outage**, serve from the origin, bounded by the request deadline, and bound the origin's exposure: at most one origin computation per key in flight per instance, with later callers for that key waiting on the in-flight one until the deadline rather than starting their own. Without that, N concurrent callers plus one cold cache equals N origin calls, and the origin becomes the second outage. This platform's form of the rule is in `/alaa-services-contract` (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`.
- **On an origin outage**, serving stale is permitted only where all four hold: the route documents it, there is a **maximum stale age** past which the value is not served at all, the response is **marked** with the substitution and the value's age, and a caller that cannot accept staleness has a way to demand a fresh value or a failure. Missing any one of the four, the request fails instead. Unbounded stale service is not degradation; it is silent incorrectness with a cache in front of it.
- **Never stale-serve a decision about whether a caller may act, or an entitlement, quota, or balance whose whole purpose is to be current.** For the authorization case this is the gate rule, owned by `/alaa-security-review` (`$alaa-security-review`). For a quota or balance it is the same shape for a different reason: a stale value cannot represent the consumption that has happened since, so serving it authorises spending that has already occurred.
- **A cache is a dependency and takes the same bounds** as any other: an explicit timeout tighter than the origin it fronts, and its own failure classification. A cache client with no timeout converts a cache incident into a total outage, which is the most common single defect in this whole area.
- **Warm the cache deliberately after an outage**, at a bounded rate. A cold cache plus full traffic is an origin overload even when nothing else is wrong, and the single-flight rule above bounds it per key but not in aggregate.

## Feature flags and kill switches

A declared-optional dependency needs a way to be turned off without a deploy, because the fastest mitigation for a dependency that is slow-but-succeeding is to stop calling it. Two rules make a kill switch trustworthy: the switch's own store is not on the path it disables — a flag that cannot be read during the incident is not a control — and the disabled path takes exactly the same degraded branch that the injection test exercises, so the mitigation runs tested code. A kill switch with its own untested branch is a second failure path introduced during an incident.
