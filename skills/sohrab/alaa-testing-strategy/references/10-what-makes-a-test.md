# What Makes A Test A Test

Read when writing or reviewing any individual test, and whenever an existing test's value is in question. `SKILL.md` holds the core rule and the four-step derivation; this file holds the catalogue that step 2 draws on, the assertion rules that follow from it, and the procedure for auditing tests that already exist.

## The catalogue of plausible broken implementations

Step 2 of the derivation asks for the version a competent engineer ships by mistake. Find the row that matches the shape of the code under test and take its break; the list is the floor, not the ceiling.

| Shape of the code under test | Its characteristic break | The assertion that catches it |
|---|---|---|
| A guard that admits or refuses | The guard is absent, so everything is admitted | A refused case, asserted with its effect absent |
| A comparison against a limit | `>` where `>=` was meant, or the reverse | The value exactly at the limit, plus one either side, each asserting which side passes |
| A filter narrowing a set — tenant, owner, status, soft-delete | The filter is dropped, or applied in one query and not its sibling | A row that must not be returned exists in the fixture and is asserted absent |
| A branch on a state | The branch is unreachable, or every input takes the same branch | One case per branch, each asserting an outcome the other branches cannot produce |
| A transformation | The input is returned unchanged, or a fixed value is returned | An input whose correct output differs from both the input and any constant |
| A lookup by key | The first row is returned regardless of key | Two rows present, each fetched, each asserting the other's fields absent |
| An update | The stored value is returned instead of the new one | The response and a re-read both asserted to carry the new state, not the old |
| An effect with a precondition | The effect runs before the precondition is checked | Zero effects asserted on the refusal path |
| An effect that must happen once | It happens twice on retry, or zero times and reports success | The effect counted, with the count asserted exactly |
| An error path | The error is swallowed and success is returned | The declared error code and shape asserted, and the success path asserted absent |
| A layered control | An inner layer trusts an outer layer that no longer checks | Each layer exercised with the others neutralised |
| A parser or decoder | Malformed input is accepted and coerced to a default | Malformed input asserted to be refused with its declared code |
| An ordering or a sequence | The order is whatever the map or the query planner produced | An input whose correct order differs from insertion order |
| A configuration read | The configured value is ignored and a hardcoded default used | Two configurations, each producing an observably different outcome |
| A time-dependent rule | The rule reads the ambient clock and cannot be exercised at the boundary | An injected clock set to each side of the boundary |

## Assertion rules

- **Assert the value, not its presence.** `is not null` passes against a placeholder, another tenant's record, and the previous version of the resource. Assert the value a correct implementation produces and no plausible broken one does.
- **Assert the absence of every effect a refusal was supposed to prevent.** Outbound requests, rows written, events emitted, files created, credentials minted, messages published. A refusal asserted only by its status code proves the code was returned, not that nothing happened.
- **Assert exactly one behaviour per test.** A test asserting five unrelated things reports one failure for five possible causes, and the reader must run it to find out which — which is the cost the test was supposed to remove.
- **Assert on the observable outcome rather than the call sequence**, except where the call *is* the outcome. Zero outbound requests, exactly one effect, and an emitted audit event are outcomes; the order in which two internal collaborators were invoked is not. `30-doubles.md` owns the rest of that boundary.
- **Never assert on a value the test computed with the same expression the code uses.** A test that recomputes the expected value with the production formula passes against every formula, including a wrong one. Write the expected value as a literal, or derive it by an independent route.
- **Test data carries the discriminating property, not realistic-looking noise.** A fixture whose two records differ in every field cannot show which field the code filtered on; a fixture whose records differ in exactly the field under test can.

## Auditing tests that already exist

Run this over a suite whose value is unknown — a suite inherited, a suite that stayed green through an incident, or a suite about to be cited as evidence.

1. **Take the tests covering the mechanism in question.** Delete or invert that mechanism in a scratch copy of the repository.
2. **Run the suite.** Every test that still passes is a test of something other than the mechanism.
3. **For each survivor, decide one of three outcomes in the same change**: repair it so it fails, delete it, or record in one line what it does defend against if that turns out to be something real.
4. **Report the survivor count**, because it is the only honest measure of the suite's strength and it is the number a coverage percentage conceals.

Three survivor patterns are worth naming because they are common and each looks fine in review: a test that asserts only the status of a response; a test whose fixture makes every branch produce the same output; and a test whose double is configured to return the value the assertion expects, so the assertion tests the test's own setup.

## The happy path's job

One happy-path test per behaviour, written last. Its job is to prove that the failure tests fail for the reason claimed rather than because the arrangement never worked — a failure test passing against an arrangement that could not succeed under any implementation proves nothing. A suite of happy paths alone proves the routes are routed.
