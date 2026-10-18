# Test Economy

Read when deciding whether a candidate is owed a test, giving a test its selector, creating or sharing setup, choosing which commands a gate runs, or finding a build, compile, render, or image produced more than once in a pass. `SKILL.md` holds the binding rules: *Whether a test is owed* and non-negotiables 10, 13, and 14. This file holds the detail; the per-stack skills own the native mechanism for each rule.

## Candidates that are not owed a test

| Kind | Example | What this project tests instead |
|---|---|---|
| Language or runtime behaviour | that a map lookup returns the stored value, that a type conversion rounds | nothing |
| Framework behaviour | that the router dispatches, that the ORM persists a field, that the validator rejects a type mismatch, that the container injects a binding | the rule this project configured: the route's guard, the validation rule's boundary, the binding this project chose |
| A shared kit or package its own suite proves | an alaa-go-chi middleware's envelope, trust-header parsing, outbox relay mechanics; an `@alaa/*` component's rendering | the consumer's use: the options it passes, the handler or policy it plugs in, the route family it chose, and the kit's required conformance harness |
| A vendor library | a client's retry loop, a parser's grammar | the configuration chosen and the caller's handling of each response it uses; a double is bound per `30-doubles.md` |
| Generated code | a generated client, mapper, or schema type | the generator's input, by the gate that regenerates and diffs it |
| A declaration a gate already rejects | a typed field, a schema shape, a lint-enforced convention, a chart that fails to render | nothing beyond that gate |
| An unreachable mode | input already refused by an owned, tested check upstream inside the same trust boundary; a dependency this path never calls; a configuration that never ships | nothing; record `not reachable: <reason>` |

The always-owed tests in `SKILL.md` — named security controls, reported-defect regressions, untrusted-input boundaries, and the per-surface floor — are never placed in a row above.

**The boundary that decides a hard case: could this project's code be wrong in a way the test catches?** If only the dependency could be wrong, the dependency's suite owns the test. If this project's choice, input, or wiring could be wrong, the test is owed and it asserts that choice.

A test already in the suite that falls into a row above is reported as a finding with its reason, because it passes against every implementation this project can ship. It is deleted only after an independent reviewer accepts that finding, never by the lane whose change it is failing on, and never when it is an always-owed test.

## Topic and layer selectors

- **Every test belongs to one topic**: the behaviour or surface it defends, at the granularity a single change touches — a route family, a use case, a consumer, a policy, a migration.
- **The topic is expressed through the runner's native selector**: a package or directory, a name prefix matched by the runner's filter, a group or tag, or a project. Layer is a second, independent selector, so the unit tests of one topic run without its integration tests.
- **The repository records the selector map** — each topic and layer, and the exact command that runs it — in its validation policy. `/alaa-project-constitution` carries the slot. When a repository has no map, derive the selector from test location, use it, and report the missing map as a gap.
- **The focused tier runs the selectors of the changed topics. The affected tier runs the union of selectors for every topic reachable from the changed surfaces.** The whole-suite command is the exhaustive tier only.
- **A new test joins an existing topic** when its behaviour belongs to one; a new topic is created only for a new behaviour or surface.

## Setup once

Choose the widest scope at which the resource is reset-safe:

| Scope | Holds |
|---|---|
| Run or session — where a runner executes each package as its own process, the package process | engine and broker processes, containers, the built artifact, immutable reference data |
| Package or module | a migrated schema, a booted application, a seeded read-only dataset |
| Worker | one copy of each run- or package-scope resource per parallel worker, created once per worker |
| Test | only the data the test asserts on |

- **Isolate each test over shared infrastructure, in this order of preference**: a transaction rolled back after the test; a unique namespace — schema, key prefix, queue or topic name, tenant identifier; a reset of exactly the data the test touched. A fresh instance per test is used when creation is the behaviour under test; resources without safe reset follow the per-test exception below.
- **Migrate once per run.** Re-migrate only when the migration sources changed since the last run.
- **Shared fixture data is immutable.** A test that needs to change it builds its own copy through a factory.
- **Prove a new shared resource reset-safe** by running its suite in the runner's seeded shuffle order once when it is introduced (`50-flake.md`, step 2), because shared state that leaks shows up first as order dependence.
- **A setup that cannot be reset** — a resource with no rollback, no namespace, and no cheap reset — stays per test, and the reason is recorded beside it.

## Build once per tree state

- **One build, compile, render, or image per tree state and environment.** Every lint, type, test, render, and smoke step of the pass consumes that output, the runner's build cache, or the image digest.
- **A test step that compiles is the compile check.** A separate build step remains only when it builds something the test step does not — the shipped binary or image.
- **Type-check once.** Exactly one type-check runs per tree state over each project configuration. A separate type-check step is dropped only when the build runs the same checker over the same configurations.
- **Render once.** Rendered manifests, configuration, or templates are written once, and every check reads that output.
- **Build an image once and promote it by digest.** Every gate and environment that needs the image references that digest and never rebuilds it.
- **Lanes and the verifier share the build cache** when they run in the same environment. A clean build is run only when a failure is classified as a contaminated tree or stale cache.
- **Container gates of one pass share one container and one run of the CI job's setup.**
- **The same suite never runs twice in one pass.** A sub-suite already included in a wider command of the same pass, such as a contract suite inside the whole-suite run, is cited from that run.

## Review checks

Each is observable in a diff or a pipeline definition:

1. Every new test names a failure that can reach this project's code under *Reachable failure*, or it is an always-owed test; otherwise it is a finding.
2. No consumer test re-proves dependency-owned framework, kit/package, vendor, or generated behaviour; test the consumer’s configuration and wiring, and retain tests of behaviour owned by a kit/package under development.
3. Every new test is reachable through a topic selector narrower than the whole suite.
4. No new setup creates an engine, container, schema, migration, or application boot per test without a recorded reason.
5. No step of the pass rebuilds, re-renders, re-type-checks, or re-runs what another step of the same pass already produced.
