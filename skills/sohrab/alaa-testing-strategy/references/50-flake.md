# Flake

Read when any test has produced two different outcomes on the same code, and when a retry is being proposed anywhere. `SKILL.md` holds the binding rule: classify before acting, and never retry blindly.

## Why the classification comes first

A flaky test and an intermittent product defect produce the identical symptom — a test that passes and fails on unchanged code — and the correct response to them is opposite. Repairing a product defect as though it were a test defect suppresses it; repairing a test defect as though it were a product defect burns days looking for a race that is not there. Every other decision in this file depends on the classification, so it is made first and recorded.

## The classification procedure

Hold the product code constant and change only what surrounds the test. Run each step until one of them changes the outcome.

1. **Run the test alone**, with nothing else in the process.
2. **Run it in a different order**, using the runner's seeded shuffle, and record the seed.
3. **Run it at one worker and at many.**
4. **Run it on a loaded or slower machine**, or with the runner's CPU allowance reduced.
5. **Run it 100 times in a loop**, unchanged, and record the failure rate.
6. **Run it under the language's race or concurrency detector**, where one exists.

Classify by what changed the outcome:

| What changed the outcome | Classification | The defect |
|---|---|---|
| Test order, or running alone versus with others | **Broken test** | Shared state between tests — a fixture, a global, a database row, a temp file, a singleton, a cached connection |
| Worker count or parallelism, with no shared product state | **Broken test** | Tests contending for the same external resource: a port, a fixed identifier, a shared schema, a named file |
| Machine load, or a changed sleep duration | **Broken test** | The test synchronises on elapsed time rather than on the condition it is waiting for |
| The ambient environment — clock, timezone, locale, DNS, network, leftover files | **Broken test** | Missing hermeticity, unless the product itself depends on that thing unbounded, which is a product defect |
| Worker count, where the product also runs that concurrency | **Product defect** | A race in the product, surfaced by the harness rather than caused by it |
| Nothing the test controls — same order, workers, environment, machine, still intermittent | **Product defect** | Non-determinism inside the product: a race, an unsynchronised structure, an uninitialised value, iteration-order dependence, an unordered query, a retry that is not idempotent |
| The race or concurrency detector reports a finding | **Product defect** | Treat a detector finding as decisive; it names the defect directly |

**The deciding question, when the table leaves it open: does the varying mechanism also run in production?** A goroutine or thread, a lock, a retry, a clock read, a map iteration, a database isolation choice, a queue delivery — all run in production, so the test found a real defect and did its job. A sleep, a shared fixture, a leaked temp directory, another test's rows, a hardcoded port — exist only in the harness, so the test is broken.

An unclassifiable case is treated as a product defect and reported as such, because a suppressed product defect returns as an incident while a suppressed test defect returns as an annoyance.

## What happens to a flaky test

**A test that fails intermittently is either a product defect or a broken test, and it is classified as one of the two before any other action. A blanket retry is never the response to either: retrying a broken test hides that it asserts nothing, and retrying a real intermittent failure suppresses a production defect that will next appear as an incident. A test classified as broken is repaired in the same change, or quarantined with a named owner and a dated deadline, or deleted — and a quarantined test past its deadline is deleted, because a permanently retried or permanently quarantined test asserts nothing while still being counted as coverage.**

A test classified as a product defect is not quarantined at all. It is reported as a defect at the severity of the behaviour it found, and the failing test stays in the suite as the reproduction — removing it removes the only evidence anyone has.

## Quarantine mechanics

Quarantine is a bounded state with an exit, not a folder.

- **Named owner**: one person, recorded in the quarantine entry, not a team.
- **Dated deadline**: an absolute date, not "next sprint".
- **The classification and the evidence**: the step from the procedure above that changed the outcome, and the observed failure rate.
- **Excluded from the gating suite, and still run**: the quarantined suite runs on the same cadence and its results are reported, because a quarantined test that stops running stops producing the information that would let anyone fix it.
- **Visible count**: the number of quarantined tests is reported with every suite run. A quarantine with no visible count grows without anyone deciding that it should.
- **At the deadline**: repaired, or deleted, with no third option. An extension is a new deadline recorded by the same owner with a stated reason, and a second extension means the test is deleted, because two extensions have already demonstrated that nobody will fix it.

## The only legitimate retry

**A retry keyed to a named infrastructure failure class, which never retries an assertion failure, is not a test retry and is permitted.** The named classes are: the runner or agent was lost, an image or package could not be pulled, the network to a registry or artifact store failed, or a container failed to start. Each is identified by its own signature — an exit code, a log line, an absent process — and never by "the suite failed".

Everything else is forbidden, including all of these: a global retry count in the runner configuration; a per-test retry annotation; a rerun-failed-tests step; and a human re-running a job until it goes green. Each converts an intermittent product defect into an invisible one and adds latency to every future run.

`80-evidence-and-reporting.md` owns the reporting consequence: a pass after a failure is a flaky result, never a clean pass.

## Preventing flake by construction

Most flake is prevented by the same four properties, and every one of them is checkable in review:

1. **Injected time.** The product reads a clock it was given, so the test sets it. No test sleeps to reach a boundary.
2. **Waiting on conditions.** A test waits for the condition it needs, with a bounded timeout and a clear failure message, never for a duration.
3. **Per-test isolation by construction.** A fresh schema, a transaction rolled back, or a unique namespace per test — so no order exists in which tests interfere.
4. **Seeded randomness.** Any randomness in the product or the fixture is seeded, and the seed is printed on failure so the run is reproducible.

`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the product-side mechanisms whose absence produces genuine intermittency — retry legality, idempotency, and concurrency bounds. When the classification lands on product defect, that skill owns the fix and this file owns only the classification.
