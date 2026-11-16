# Test Economy

The per-stack skills own the native mechanism for each rule in this file.

## Candidates that are not owed a test

| Kind | Example | What this project tests instead |
|---|---|---|
| Language or runtime behaviour | that a map lookup returns the stored value, that a type conversion rounds | nothing |
| Framework behaviour | that the router dispatches, the ORM persists a field, the validator rejects a type mismatch, the container injects a binding | what this project configured: the route's guard, the validation rule's boundary, the binding it chose |
| A shared kit or package that its own suite proves | an alaa-go-chi middleware's envelope, trust-header parsing, outbox relay mechanics; an `@alaa/*` component's rendering | the consumer's use: the options it passes, the handler or policy it plugs in, the route family it chose, and the kit's required conformance harness |
| A vendor library | a client's retry loop, a parser's grammar | the configuration chosen, and the caller's handling of each response it uses; bind a double per `30-doubles.md` |
| Generated code | a generated client, mapper or schema type | the generator's input, by the gate that regenerates and diffs it |
| A declaration that a gate already rejects | a typed field, a schema shape, a lint-enforced convention, a chart that fails to render | nothing beyond that gate |
| An unreachable mode | input already refused by an owned, tested check upstream inside the same trust boundary; a dependency this path never calls; a configuration that never ships | nothing; record `not reachable: <reason>` |

Never place an always-owed test from `SKILL.md` in a row above.

**A hard case turns on one question: could this project's code be wrong in a way that the test catches?** If only the dependency could be wrong, the dependency's suite owns the test. If this project's choice, input or wiring could be wrong, the test is owed and asserts that choice.

Report an existing test that falls into a row above as a finding with its reason. Delete it only after the lead, or the reviewer that its verification decision names, accepts the finding. The lane whose change it fails on never deletes it, and nobody deletes an always-owed test this way. A kit or package that is itself under development keeps the tests of the behaviour it owns.

A failure alone never justifies deleting a test. Repair a failing test, or classify it under `50-flake.md`, whose quarantine deadline is the only failure-driven deletion. Every other deletion follows the acceptance rule above and keeps the obligations of `60-coverage.md`.

## Existing tests on a touched topic

In the same change, repair only the existing tests of topics the change touches, and only to:

- name the failure a test defends against;
- add its topic and layer selector;
- split independent scenarios into independent cases;
- remove a duplicate that the removal discriminator in `SKILL.md` *The core rule* proves.

Record a redesign of shared test infrastructure, or a migration of untouched topics, as a separate follow-up task.

## Topic and layer selectors

- **Every test belongs to one topic**: the behaviour or surface it defends, at the granularity one change touches, such as a route family, a use case, a consumer, a policy or a migration. Put a new test in an existing topic when its behaviour belongs to one.
- **Express the topic through the runner's native selector**: a package or directory, a name prefix that the runner's filter matches, a group or tag, or a project. A test reachable only through the whole-suite command makes every change pay for the whole suite.
- **Layer is a second, independent selector**, so that a topic's unit tests run without its integration tests.
- **Record the selector map in the repository's validation policy**: each topic and layer, and the exact command that runs it. `/alaa-project-constitution` carries the slot. Without a map, derive the selector from the test's location, use it, and report the missing map as a gap.

## Setup once

Expensive resettable infrastructure is an engine or container, a migrated schema, a booted application, a built artifact, or immutable fixture data. Create it once and share it, at the widest scope at which it is reset-safe:

| Scope | Holds |
|---|---|
| Run or session; where a runner executes each package as its own process, the package process | engine and broker processes, containers, the built artifact, immutable reference data |
| Package or module | a migrated schema, a booted application, a seeded read-only dataset |
| Worker | one copy of each run- or package-scope resource per parallel worker, created once per worker |
| Test | only the data the test asserts on |

- **Isolate each test over shared infrastructure, in this order of preference**: a transaction rolled back after the test; a unique namespace (schema, key prefix, queue or topic name, tenant identifier); a reset of exactly the data the test touched.
- **Create a fresh instance per test only** when creation is the behaviour under test, or when the resource has no rollback, no namespace and no cheap reset. Record the reason beside that setup.
- **Migrate once per run.** Re-migrate only when the migration sources changed since the last run.
- **Keep shared fixture data immutable.** A test that must change it builds its own copy through a factory.
- **Prove a new shared resource reset-safe**: when you introduce it, run its suite once in the runner's seeded shuffle order (`50-flake.md`, step 2).

## Build once per tree state

Every lint, type, test and smoke step of a pass consumes the one build's output, cache or image digest.

- **A test step that compiles is the compile check.** Keep a separate build step only when it builds something the test step does not, such as the shipped binary or image.
- **Type-check once** per tree state over each project configuration. Drop a separate type-check step only when the build runs the same checker over the same configurations.
- **Render once.** Write rendered manifests, configuration or templates once, and let every check read that output.
- **Build an image once and promote it by digest.** Every gate and environment that needs the image references that digest.
- **Share the build cache between lanes and the verifier** when they run in one environment. Run a clean build only when a failure is classified as a contaminated tree or a stale cache.
- **Let the container gates of one pass share one container and one run of the CI job's setup.**
- **Never run the same suite twice in one pass.** Cite a sub-suite that a wider command of the pass already ran, such as a contract suite inside the whole-suite run, from that run.
