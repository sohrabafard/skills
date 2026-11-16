# Test Economy

The per-stack skills own the native mechanism for each rule in this file.

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

Never place an always-owed test from `SKILL.md` in a row above.

**A hard case turns on one question: could this project's code be wrong in a way the test catches?** If only the dependency could be wrong, the dependency's suite owns the test. If this project's choice, input or wiring could be wrong, the test is owed and asserts that choice.

Report an existing test that falls into a row above as a finding with its reason, because it passes against every implementation this project can ship. Delete it only after the lead, or the reviewer that its verification decision names, accepts the finding. The lane whose change it fails on never deletes it, and nobody deletes an always-owed test this way.

A failure alone never justifies deleting a test. Repair a failing test, or classify it under `50-flake.md`, whose quarantine deadline is the only failure-driven deletion. Every other deletion follows the acceptance rule above and keeps the obligations of `60-coverage.md`.

## Existing tests on a touched topic

Repair, in the same change, only the existing tests of topics the change touches, and only to: name the failure a test defends against, add its topic and layer selector, split independent scenarios into independent cases, and remove a duplicate that the removal discriminator in `SKILL.md` *The core rule* proves. Record a redesign of shared test infrastructure or a migration of untouched topics as a separate follow-up task, because it widens review scope and retest breadth beyond the behaviour that changed.

## Topic and layer selectors

- **Every test belongs to one topic**: the behaviour or surface it defends, at the granularity one change touches, such as a route family, a use case, a consumer, a policy or a migration.
- **Express the topic through the runner's native selector**: a package or directory, a name prefix the runner's filter matches, a group or tag, or a project. Layer is a second, independent selector, so a topic's unit tests run without its integration tests.
- **Record the selector map in the repository's validation policy**: each topic and layer, and the exact command that runs it. `/alaa-project-constitution` carries the slot. Without a map, derive the selector from test location, use it, and report the missing map as a gap.
- `SKILL.md` *Scope tiers: how much of the suite runs, and when* owns which selectors each tier runs.
- **Put a new test in an existing topic** when its behaviour belongs to one. Create a topic only for a new behaviour or surface.

## Setup once

Expensive resettable infrastructure is an engine or container, a migrated schema, a booted application, a built artifact, or immutable fixture data. Per-test creation multiplies the suite's cost by its test count and buys no isolation that a rollback or a namespace does not.

Choose the widest scope at which the resource is reset-safe:

| Scope | Holds |
|---|---|
| Run or session — where a runner executes each package as its own process, the package process | engine and broker processes, containers, the built artifact, immutable reference data |
| Package or module | a migrated schema, a booted application, a seeded read-only dataset |
| Worker | one copy of each run- or package-scope resource per parallel worker, created once per worker |
| Test | only the data the test asserts on |

- **Isolate each test over shared infrastructure, in this order of preference**: a transaction rolled back after the test; a unique namespace (schema, key prefix, queue or topic name, tenant identifier); a reset of exactly the data the test touched. Use a fresh instance per test when creation is the behaviour under test, or under the no-reset exception below.
- **Migrate once per run.** Re-migrate only when the migration sources changed since the last run.
- **Keep shared fixture data immutable.** A test that must change it builds its own copy through a factory.
- **Prove a new shared resource reset-safe** by running its suite once in the runner's seeded shuffle order when you introduce it (`50-flake.md`, step 2), because leaking shared state shows first as order dependence.
- **Keep a setup that cannot be reset per test**, with the reason recorded beside it. Such a resource has no rollback, no namespace and no cheap reset.

## Build once per tree state

- **A test step that compiles is the compile check.** Keep a separate build step only when it builds something the test step does not, such as the shipped binary or image.
- **Type-check once.** Run exactly one type-check per tree state over each project configuration. Drop a separate type-check step only when the build runs the same checker over the same configurations.
- **Render once.** Write rendered manifests, configuration or templates once, and let every check read that output.
- **Build an image once and promote it by digest.** Every gate and environment that needs the image references that digest and never rebuilds it.
- **Share the build cache between lanes and the verifier** when they run in one environment. Run a clean build only when a failure is classified as a contaminated tree or stale cache.
- **Let the container gates of one pass share one container and one run of the CI job's setup.**
- **Never run the same suite twice in one pass.** Cite a sub-suite that a wider command of the pass already ran, such as a contract suite inside the whole-suite run, from that run.

## Review checks

Each check is observable in a diff or a pipeline definition:

1. Every new test names a failure that can reach this project's code under `SKILL.md` *Reachable failure*, or it is an always-owed test. Otherwise it is a finding.
2. No consumer test re-proves behaviour that a framework, a kit or package, a vendor library or a generator owns; test the consumer's configuration and wiring. Keep the tests of behaviour owned by a kit or package that is itself under development.
3. A topic selector narrower than the whole suite reaches every new test.
4. No new setup creates an engine, container, schema, migration or application boot per test without a recorded reason.
5. No step of the pass rebuilds, re-renders, re-type-checks or re-runs what another step of the same pass already produced.
