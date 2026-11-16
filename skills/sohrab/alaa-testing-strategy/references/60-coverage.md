# Coverage

## What coverage measures, and what it does not

A coverage tool records which lines, branches or statements were **executed** while the suite ran, and nothing else. It does not record whether anything was asserted, whether an assertion would fail against a broken implementation, whether the risky case ran, or whether the code is correct. A test with no assertions raises coverage as much as a test that asserts the value.

## Why a percentage target is not a rule

A percentage can be satisfied without testing anything:

- **Execution alone satisfies it.** Calling code from a test and asserting nothing moves the number.
- **It directs effort to the cheapest uncovered lines** — accessors, generated code, constructors, string formatting — and away from risky branches, because a branch that needs a fixture, a failure injection and a real engine costs far more per point.
- **It makes deleting untested code the fastest way to comply**, which usually loses an untested edge case instead of testing it.

An existing pipeline percentage is not evidence, and never report it as validation. Where the gate cannot be removed, report it as a gate that ran, and report the obligations below separately as the coverage claim.

## The rule that replaces it: the named obligations

**Every item below has at least one test that names the broken implementation it defends against. Nothing else carries a coverage obligation, and an item with no such test is an unmet obligation reported at the severity of what the item protects.** An item applies only to a decision this project owns and a failure that can reach it, under `SKILL.md` *Whether a test is owed*. Record an item outside that under `Not written`; it is not an unmet obligation. Obligations 1, 6 and 9 are always owed.

1. **Every branch of every control**, in both directions — admitted and refused: authentication, authorization, tenancy, rate limits, admission and shedding decisions, and any flag that gates access. `/alaa-security-review` names which controls a change has.
2. **Every failure mode enumerated for the change**, each with the test that produces it. `alaa-observability-soc references/10-signal-model.md` ("Start from the diff, not from the question") owns the shared enumeration, and `70-failure-mode-first.md` converts its modes into tests.
3. **Every state transition of anything with states**, including the transitions that must be refused, because an unrefused illegal transition puts data in a state no code handles.
4. **Every boundary of every bound the code enforces**: the value at the limit, one inside, one outside, and the empty and maximal cases of every collection, string and page whose size the code branches on or limits.
5. **Every error the code can return**, at the layer that returns it, asserted for the declared code and shape. `/alaa-services-contract` owns the codes and shapes.
6. **Every reported defect**, with a test that fails against the code as it stood when the defect was reported, added in the same change as the fix, because otherwise the fix cannot later be told apart from a reverted fix.
7. **Every contract this service publishes or consumes**, at the contract layer, on both sides where both are in this fleet.
8. **Every mechanism whose removal must break a test** — retry, timeout, breaker, bulkhead, shed, degradation, idempotency. `/alaa-reliability-sla` owns the list and the injection.
9. **Every boundary where untrusted input is parsed, decoded or deserialised**, with at least one malformed and one hostile input asserted to be refused.
10. **Every published request in a shipped API artifact**, asserted at the request layer. `/alaa-postman-collections` owns those assertions. Reason: a validator run over this platform's own API collection found 73 requests with no test, including the entire Auth folder, so the token-issuing requests asserted nothing.

The obligations are the review checklist and the report's `Coverage obligations` field. Each is met or unmet, with no partial credit, because a partially covered control is uncovered on the path nobody tested.

## The one legitimate use of the coverage tool

**Read coverage as a diff, not as a number.** A changed line that no test executes means either a missing test or an unreachable line that should not exist.

1. Run coverage over the suite with the change applied.
2. Intersect the executed set with the change's diff.
3. For each changed line that nothing executes, add the test or delete the line.
4. Report the decision per line, not a number.

## Mutation as the honest measure

A mutation-testing tool introduces a plausible broken implementation and reports whether any test failed: the core rule, automated. Where the language has one, use it as an investigation, not a gate. Run it over the changed code, read the surviving mutants, and treat each survivor as a candidate missing test. Never gate on a mutation score, because killing cheap mutants in code nobody depends on raises it.

Where no such tool exists, use the audit in `10-what-makes-a-test.md` *Auditing tests that already exist*, and report its survivor count.
