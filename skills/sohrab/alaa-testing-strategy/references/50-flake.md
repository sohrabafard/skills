# Flake

## Why the classification comes first

A flaky test and an intermittent product defect show one symptom, a test that passes and fails on unchanged code, and need opposite responses. Repairing a product defect as a test defect suppresses it. Repairing a test defect as a product defect burns days on a race that is not there. Make and record the classification first, because every other decision here depends on it.

## The classification procedure

Hold the product code constant and change only what surrounds the test. Run each step until one changes the outcome.

1. **Run the test alone**, with nothing else in the process.
2. **Run it in a different order**, using the runner's seeded shuffle, and record the seed.
3. **Run it at one worker and at many.**
4. **Run it on a loaded or slower machine**, or with the runner's CPU allowance reduced.
5. **Run it 100 times in a loop**, unchanged, and record the failure rate.
6. **Run it under the language's race or concurrency detector**, where one exists.

Classify by what changed the outcome:

| What changed the outcome | Classification | The defect |
|---|---|---|
| Test order, or running alone versus with others | **Broken test** | Mutable state shared between tests — a mutated fixture, a global, a database row, a temp file, a singleton, a cached connection |
| Worker count or parallelism, with no shared product state | **Broken test** | Tests contending for the same external resource: a port, a fixed identifier, a shared schema, a named file |
| Machine load, or a changed sleep duration | **Broken test** | The test synchronises on elapsed time rather than on the condition it is waiting for |
| The ambient environment — clock, timezone, locale, DNS, network, leftover files | **Broken test** | Missing hermeticity, unless the product itself depends on that thing unbounded, which is a product defect |
| Worker count, where the product also runs that concurrency | **Product defect** | A race in the product, surfaced by the harness rather than caused by it |
| Nothing the test controls — same order, workers, environment, machine, still intermittent | **Product defect** | Non-determinism inside the product: a race, an unsynchronised structure, an uninitialised value, iteration-order dependence, an unordered query, a retry that is not idempotent |
| The race or concurrency detector reports a finding | **Product defect** | Treat a detector finding as decisive; it names the defect directly |

**When the table leaves it open, ask whether the varying mechanism also runs in production.** A goroutine or thread, a lock, a retry, a clock read, a map iteration, an isolation choice or a queue delivery runs in production, so the test found a real defect. A sleep, a mutated shared fixture, a leaked temp directory, another test's rows or a hardcoded port exists only in the harness, so the test is broken.

Treat and report an unclassifiable case as a product defect, because a suppressed product defect returns as an incident and a suppressed test defect returns as an annoyance.

## What happens to a flaky test

**A test that fails intermittently is either a product defect or a broken test, and it is classified as one of the two before any other action. A blanket retry is never the response to either: retrying a broken test hides that it asserts nothing, and retrying a real intermittent failure suppresses a production defect that will next appear as an incident. A test classified as broken is repaired in the same change, or quarantined with a named owner and a dated deadline, or deleted — and a quarantined test past its deadline is deleted, because a permanently retried or permanently quarantined test asserts nothing while still being counted as coverage.**

A test classified as a product defect is not quarantined at all. Report it as a defect at the severity of the behaviour it found, and keep the failing test in the suite as the reproduction, because it is the only evidence.

## Quarantine mechanics

Quarantine is a bounded state with an exit, not a folder.

- **Named owner**: one person, recorded in the quarantine entry, not a team.
- **Dated deadline**: an absolute date, not "next sprint".
- **Classification and evidence**: the procedure step that changed the outcome, and the observed failure rate.
- **Excluded from the gating suite, and still run**: the quarantined suite runs on the same cadence and its results are reported, because a test that stops running stops producing the information needed to fix it.
- **Visible count**: report the number of quarantined tests with every suite run, so that nobody lets quarantine grow undecided.
- **At the deadline**: repair or delete, with no third option. An extension is a new deadline recorded by the same owner with a reason. A second extension means deletion, because two extensions show that nobody will fix it.

## The only legitimate retry

**A retry keyed to a named infrastructure failure class, which never retries an assertion failure, is not a test retry and is permitted.** The named classes are a lost runner or agent, an image or package that could not be pulled, a failed network path to a registry or artifact store, and a container that failed to start. Identify each by its own signature, such as an exit code, a log line or an absent process, never by "the suite failed".

Every other retry is forbidden: a global retry count in the runner configuration, a per-test retry annotation, a rerun-failed-tests step, and a person re-running a job until it goes green. Each converts an intermittent product defect into an invisible one and adds latency to every run.

`80-evidence-and-reporting.md` *Reruns* owns the reporting consequence.

## Preventing flake by construction

Check these properties in review:

1. **Injected time and condition waits**, under `SKILL.md` non-negotiable 11.
2. **Per-test isolation by construction** over shared infrastructure, under `90-test-economy.md` *Setup once*.
3. **Seeded randomness**: seed all randomness in the product or the fixture, and print the seed on failure so that the run is reproducible.

`/alaa-reliability-sla` owns the product-side mechanisms whose absence produces genuine intermittency: retry legality, idempotency and concurrency bounds. When the classification is product defect, that skill owns the fix, and this file owns only the classification.
