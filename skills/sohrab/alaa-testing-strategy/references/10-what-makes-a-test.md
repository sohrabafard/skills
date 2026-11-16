# What Makes A Test A Test

## The catalogue of plausible broken implementations

Find the row that matches the shape of the code under test, and take its break for step 2 of the derivation in `SKILL.md`. A row applies only to code this project owns and to a break that can reach it (`SKILL.md` *Whether a test is owed*). For a shape that the table lacks, derive the break by the same four steps.

| Shape of the code under test | Its characteristic break | The assertion that catches it |
|---|---|---|
| A guard that admits or refuses | The guard is absent, so everything is admitted | A refused case, with its effect asserted absent |
| A comparison against a limit | `>` where `>=` was meant, or the reverse | The value at the limit and one either side, each asserting which side passes |
| A filter that narrows a set: tenant, owner, status, soft-delete | The filter is dropped, or applied in one query and not in its sibling | A fixture row that must not be returned, asserted absent |
| A branch on a state | The branch is unreachable, or every input takes one branch | One case per branch, each asserting an outcome that no other branch produces |
| A transformation | The input or a fixed value is returned | An input whose correct output differs from the input and from any constant |
| A lookup by key | The first row is returned whatever the key | Two rows, each fetched, each asserting the other's fields absent |
| An update | The stored value is returned instead of the new one | The response and a re-read, both asserted to carry the new state |
| An effect with a precondition | The effect runs before the precondition is checked | Zero effects asserted on the refusal path |
| An effect that must happen once | It happens twice on retry, or never and reports success | The effect counted, and the count asserted exactly |
| An error path | The error is swallowed and success is returned | The declared error code and shape asserted, and the success path asserted absent |
| A layered control | An inner layer trusts an outer layer that no longer checks | Each layer exercised with the others neutralised |
| A parser or decoder | Malformed input is accepted and coerced to a default | Malformed input asserted refused with its declared code |
| An ordering or a sequence | The order is whatever the map or the query planner produced | An input whose correct order differs from insertion order |
| A configuration read | The configured value is ignored and a hardcoded default is used | Two configurations, each with an observably different outcome |
| A time-dependent rule | The rule reads the ambient clock, so no test reaches the boundary | An injected clock set to each side of the boundary |

## Assertion rules

- **Assert the value, not its presence.** `is not null` passes against a placeholder, another tenant's record and the previous version of the resource. Assert the value that only a correct implementation produces.
- **Assert one behaviour per test.** Several assertions are allowed when all prove that behaviour. A test of five unrelated things reports one failure for five possible causes.
- **Assert the observable outcome, not the call sequence**, unless the call is the outcome: zero outbound requests, exactly one effect, an emitted audit event (`30-doubles.md`).
- **Never compute the expected value with the expression the code uses**: that test passes against every formula. Write a literal, or derive the value by an independent route.
- **Give test data the discriminating property, not realistic noise.** Only records that differ in the field under test alone show which field the code filtered on.

## Auditing tests that already exist

Audit a suite whose value is unknown: an inherited suite, a suite that stayed green through an incident, or a suite about to be cited as evidence.

1. Delete or invert the mechanism in a scratch copy of the repository, and run the tests that cover it.
2. Every test that still passes tests something else. In the same change, repair it so that it fails, delete it, or record in one line what it defends against.
3. Report the survivor count. A coverage percentage conceals it.

Three survivor patterns pass review: a test that asserts only a response status; a fixture that makes every branch produce the same output; and a double that returns the value the assertion expects, so the assertion tests its own setup.
