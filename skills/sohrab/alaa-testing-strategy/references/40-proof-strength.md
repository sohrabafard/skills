# Proof Strength

Read before reporting any claim as validated, and whenever an environment cannot reach the level a claim needs. `SKILL.md` names the six levels and defines each; this file owns the mapping from a claim to the minimum level that supports it, the escalation rule, and what to do when the level is unreachable.

The vocabulary exists so that one word carries the same meaning in every service, language, and report in the fleet. A reviewer reading "level 2" knows what was ruled out and what was not, without asking. That is the entire value, and it is destroyed the moment one report uses a level name loosely.

## The mapping: which level a claim requires

Find the claim being made. The level named is the **minimum**; a higher level satisfies the requirement and a lower one never does.

| The claim | Minimum level |
|---|---|
| "The code follows the convention" / "the configuration declares this value" | 1 — static |
| "This type or schema rejects that shape" | 1 — static |
| "This decision, calculation, validation, state transition, parse, or format is correct" | 2 — unit |
| "This caller behaves correctly when its dependency times out, refuses, or answers wrongly" | 2, with the fault injected at the boundary |
| "This double behaves like the real implementation" | 3 — parity |
| "The service starts, wires its dependencies, and serves its interface" | 4 — local smoke |
| "This configuration value reaches the component that reads it" | 4 |
| "This route, consumer, or job behaves correctly in the shape it is deployed in" | 5 — in-runtime |
| "This retry, timeout, breaker, bulkhead, shed, degradation, or idempotency mechanism fired" | 5, with injection at the boundary the mechanism guards |
| "Credential issue, verification, refresh, and revocation behave correctly" | 5, and 6 wherever a datastore holds the revocation or the key state |
| "This query returns the right rows at the right cost" | 6 — live dependency |
| "This index is used" / "this constraint holds" / "this migration is safe on existing data" | 6 |
| "This isolation level, lock, or transaction boundary behaves correctly under concurrency" | 6 |
| "This delivery, acknowledgement, redelivery, ordering, or dead-letter behaviour is correct" | 6 |
| "This control cannot be bypassed" | 6 wherever the datastore enforces it — a row-level policy, a unique constraint, a tenant filter; 2 only where the control is entirely in process. `/alaa-security-review` (`$alaa-security-review`) owns which controls exist and what each must refuse |
| "Latency, throughput, pool, or contention behaviour is acceptable" | 6, under load, because the pool, planner, and lock behaviour is the claim |

Two claims recur and have no level, because no test produces them: "this is fast enough" with no stated budget, and "this is secure". Convert each into a claim from the table above or record it as an unmade decision.

## The escalation rule

**A level is escalated when the substituted component is the one that decides the outcome.** That single question settles most disputes:

- An embedded database proves the calling code's logic and proves nothing about the production engine's planner, its constraint behaviour, its isolation semantics, or its type coercion. A claim about any of those escalates to level 6.
- An in-memory broker proves the handler's logic and proves nothing about acknowledgement, redelivery, prefetch, or ordering. A claim about any of those escalates to level 6.
- A stubbed HTTP client proves the caller's handling and proves nothing about the real endpoint's shape. A claim about the shape escalates to level 3 against the published schema, or to level 5 against the real service.

## The prohibition, and what to report instead

**Never report a proof at a level above the one that actually ran, and never describe a lower level in language that implies a higher one.** "Tested against the database" for an embedded substitute, and "verified end to end" for a local smoke run, are the two specific errors. A level is what a reviewer uses to decide whether to re-run a claim before trusting it; a mislabelled level removes that decision without the reviewer knowing it was removed.

When the required level cannot be reached in this environment, report all four of these:

1. the highest level actually reached, named;
2. the level the claim requires, named;
3. the blocker in one line — the runtime that would not start, the dependency absent, the credential missing, the platform unsupported;
4. the claim recorded as a gap, at the severity the claim carries.

Then write the test anyway at the required level and mark it with the repository's skip mechanism, carrying the blocker as its reason string. `80-evidence-and-reporting.md` owns that procedure. A test that exists and skips is recovered the moment the environment appears; a test never written is invisible forever.

## Where the runtimes come from

Levels 4, 5, and 6 need a running local runtime. Obtain it through `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) — its render, bootstrap, and validate path — rather than assembling one per service, because a per-service runtime makes level 5 mean something different in every repository and the vocabulary stops carrying information.

Level 6 needs the production-grade engine itself. Where the fleet's own release gates name the engines and the commands, `/alaa-controlled-ops` (`$alaa-controlled-ops`) owns those gate lists; this file owns only what the resulting proof is called and what it rules out.
