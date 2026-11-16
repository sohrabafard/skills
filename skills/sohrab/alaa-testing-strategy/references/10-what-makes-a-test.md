# What Makes A Test A Test

## The catalogue of plausible broken implementations

Find the row that matches the shape of the code under test, and take its break for step 2 of the derivation in `SKILL.md`. A row applies only to code this project owns and to a break that can reach it, under `SKILL.md` *Whether a test is owed*. For a shape the table lacks, derive the break by the same four steps.

| Shape of the code under test | Its characteristic break | The assertion that catches it |
|---|---|---|
| A guard that admits or refuses | The guard is absent, so everything is admitted | A refused case, asserted with its effect absent |
| A comparison against a limit | `>` where `>=` was meant, or the reverse | The value exactly at the limit, plus one either side, each asserting which side passes |
| A filter narrowing a set — tenant, owner, status, soft-delete | The filter is dropped, or applied in one query and not its sibling | A row that must not be returned exists in the fixture and is asserted absent |
| A branch on a state | The branch is unreachable, or every input takes the same branch | One case per branch, each asserting an outcome the other branches cannot produce |
| A transformation | The input is returned unchanged, or a fixed value is returned | An input whose correct output differs from both the input and any constant |
| A lookup by key | The first row is returned regardless of key | Two rows present, each fetched, each asserting the other's fields absent |
| An update | The stored value is returned instead of the new one | The response and a re-read both asserted to carry the new state |
| An effect with a precondition | The effect runs before the precondition is checked | Zero effects asserted on the refusal path |
| An effect that must happen once | It happens twice on retry, or zero times and reports success | The effect counted, with the count asserted exactly |
| An error path | The error is swallowed and success is returned | The declared error code and shape asserted, and the success path asserted absent |
| A layered control | An inner layer trusts an outer layer that no longer checks | Each layer exercised with the others neutralised |
| A parser or decoder | Malformed input is accepted and coerced to a default | Malformed input asserted to be refused with its declared code |
| An ordering or a sequence | The order is whatever the map or the query planner produced | An input whose correct order differs from insertion order |
| A configuration read | The configured value is ignored and a hardcoded default used | Two configurations, each producing an observably different outcome |
| A time-dependent rule | The rule reads the ambient clock and cannot be exercised at the boundary | An injected clock set to each side of the boundary |

## Assertion rules

- **Assert the value, not its presence.** `is not null` passes against a placeholder, another tenant's record and the previous version of the resource. Assert the value that a correct implementation produces and no plausible broken one does.
- **Assert exactly one behaviour per test.** Several assertions are allowed when all prove that one behaviour. A test that asserts five unrelated things reports one failure for five possible causes, and the reader must run it to find which.
- **Assert the observable outcome, not the call sequence**, except where the call is the outcome: zero outbound requests, exactly one effect, an emitted audit event. `30-doubles.md` owns the rest of that boundary.
- **Never compute the expected value with the expression the code uses**, because that test passes against every formula, including a wrong one. Write the expected value as a literal, or derive it by an independent route.
- **Give test data the discriminating property, not realistic noise.** Two records that differ in every field cannot show which field the code filtered on. Records that differ only in the field under test can.

## Auditing tests that already exist

Run this audit over a suite whose value is unknown: an inherited suite, a suite that stayed green through an incident, or a suite about to be cited as evidence.

1. **Take the tests that cover the mechanism.** Delete or invert that mechanism in a scratch copy of the repository.
2. **Run the suite.** Every test that still passes tests something other than the mechanism.
3. **Decide one outcome for each survivor in the same change:** repair it so it fails, delete it, or record in one line what real thing it defends against.
4. **Report the survivor count**, because it is the only honest measure of the suite's strength, and a coverage percentage conceals it.

Three common survivor patterns look fine in review: a test that asserts only a response status; a test whose fixture makes every branch produce the same output; and a test whose double returns the value the assertion expects, so the assertion tests the test's own setup.

## Anti-patterns

Check a test, a suite and a test plan against each item. The owner file states the rule and its reason.

- a rejection test that asserts only the status or error code (`SKILL.md` *The core rule*);
- one outermost assertion standing in for a control implemented at several layers (`SKILL.md` *The core rule*);
- one behaviour tested at unit, integration and end-to-end level (`20-layers.md`);
- a mock that asserts the call sequence where the outcome was observable (`30-doubles.md`);
- a hand-written double of a dependency nobody here owns, with no parity suite (`30-doubles.md`);
- an in-memory or embedded-engine result reported as the production engine (`40-proof-strength.md`);
- retrying a failing test until it passes (`50-flake.md`);
- quarantine with no owner and no deadline (`50-flake.md`);
- a coverage percentage cited as validation (`60-coverage.md`);
- the happy path written first, and nothing after it (`70-failure-mode-first.md`);
- a test that sleeps to wait for a condition (`SKILL.md` non-negotiable 11);
- the full suite, the race detector or the acceptance set re-run against an unchanged tree (`SKILL.md` *A result stays valid until something named invalidates it*);
- an implementing lane that runs the exhaustive tier on its own work (`SKILL.md` *Scope tiers: how much of the suite runs, and when*);
- a product repair for an unclassified shell, container-runtime, permission or stale-cache failure (`120-result-classification.md`);
- a deleted or weakened assertion where the level not reached and its blocker should be recorded (`80-evidence-and-reporting.md`);
- a consumer test that re-proves framework, kit, package or vendor behaviour (`90-test-economy.md`);
- a test for a failure that cannot reach this project's code (`SKILL.md` *Reachable failure*);
- an engine, container, migration or application boot created per test (`90-test-economy.md` *Setup once*);
- a test reachable only through the whole-suite command (`90-test-economy.md`);
- a build, compile, type check, render or image produced twice in one pass (`90-test-economy.md`).
