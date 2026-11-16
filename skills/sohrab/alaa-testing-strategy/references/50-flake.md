# Flake

## The classification procedure

Hold the product code constant, and change only what surrounds the test. Run the steps in order until one changes the outcome.

1. Run the test alone, with nothing else in the process.
2. Run it in a different order with the runner's seeded shuffle, and record the seed.
3. Run it at one worker and at many.
4. Run it on a loaded or slower machine, or with a reduced CPU allowance.
5. Run it 100 times in a loop, unchanged, and record the failure rate.
6. Run it under the language's race or concurrency detector, where one exists.

Classify by what changed the outcome:

| What changed the outcome | Classification | The defect |
|---|---|---|
| Test order, or running alone versus with others | **Broken test** | Mutable state shared between tests: a mutated fixture, a global, a database row, a temp file, a singleton, a cached connection |
| Worker count or parallelism, with no shared product state | **Broken test** | Tests contend for one external resource: a port, a fixed identifier, a shared schema, a named file |
| Machine load, or a changed sleep duration | **Broken test** | The test synchronises on elapsed time, not on the condition it waits for |
| The ambient environment: clock, timezone, locale, DNS, network, leftover files | **Broken test** | Missing hermeticity. When the product itself depends on that thing unbounded, it is a product defect |
| Worker count, where the product also runs that concurrency | **Product defect** | A race in the product, which the harness surfaced and did not cause |
| Nothing the test controls: same order, workers, environment and machine, still intermittent | **Product defect** | Non-determinism inside the product: a race, an unsynchronised structure, an uninitialised value, iteration-order dependence, an unordered query, a retry that is not idempotent |
| The race or concurrency detector reports a finding | **Product defect** | The finding is decisive: it names the defect |

**When the table leaves the case open, ask whether the varying mechanism also runs in production.** A goroutine or thread, a lock, a retry, a clock read, a map iteration, an isolation choice or a queue delivery runs in production, so the test found a product defect. A sleep, a mutated shared fixture, a leaked temp directory, another test's rows or a hardcoded port exists only in the harness, so the test is broken.

**A case that is still unclassified after every step and that question is a blocker.** Assign no default class. Stop and report blocked under `SKILL.md` *Stop conditions*, with the outcome of each step.

## What happens to a flaky test

**An intermittent failure is a product defect or a broken test, and it is classified as one of the two before any other action. A blanket retry is never the response to either: it hides a broken test that asserts nothing, and it suppresses a product defect until the incident.**

- **Broken test**: repair it in the same change, quarantine it with a named owner and a dated deadline, or delete it. Delete a quarantined test that is past its deadline, because it asserts nothing and still counts as coverage.
- **Product defect**: A test classified as a product defect is not quarantined at all. Report the defect at the severity of the behaviour it found, and keep the failing test in the suite as the reproduction. `/alaa-reliability-sla` owns the fix: retry legality, idempotency and concurrency bounds.

## Quarantine mechanics

A quarantine entry records a named owner (one person, not a team), a dated deadline (an absolute date, not "next sprint"), the procedure step that changed the outcome, and the observed failure rate.

A quarantined test leaves the gating suite and still runs on the same cadence, with its results reported. Report the number of quarantined tests with every suite run. At the deadline, repair or delete. An extension is a new deadline that the same owner records with a reason. A second extension means deletion.

## The only legitimate retry

**A retry keyed to a named infrastructure failure class, which never retries an assertion failure, is not a test retry and is permitted.** The named classes are a lost runner or agent, an image or package that could not be pulled, a failed network path to a registry or artifact store, and a container that failed to start. Identify each by its own signature, such as an exit code, a log line or an absent process, never by "the suite failed".

Every other retry is forbidden: a global retry count in the runner configuration, a per-test retry annotation, a rerun-failed-tests step, and a person who re-runs a job until it is green. `80-evidence-and-reporting.md` *Reruns* owns how a rerun is reported.

## Preventing flake by construction

Check these properties in review:

1. **Injected time and condition waits** (`SKILL.md` non-negotiable 11). A condition wait fails with a clear message when its timeout expires.
2. **Per-test isolation by construction** over shared infrastructure (`90-test-economy.md` *Setup once*).
3. **Seeded randomness**: seed all randomness in the product or the fixture, and print the seed on failure.
