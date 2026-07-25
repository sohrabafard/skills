# Coverage

Read when coverage is being measured, gated, or cited as evidence, and when deciding what still needs a test. `SKILL.md` holds the binding rule: coverage obligations are named, never expressed as a percentage target.

## What coverage measures, and what it does not

A coverage tool records which lines, branches, or statements were **executed** while the suite ran. That is all it records.

It does not record whether anything was asserted, whether an assertion would fail against a broken implementation, whether the case that carries the risk was among those executed, or whether the code is correct. A test with no assertions at all raises coverage. A test asserting that a returned value is not null raises coverage by the same amount as a test asserting the value.

## Why a percentage target is not a rule

A percentage is the classic abstract-noun target: it can be satisfied without testing anything, so it cannot be complied with or violated in any way that means what it appears to mean.

Three specific consequences, each observed in real repositories:

- **It is satisfiable by execution alone.** Calling code from a test and asserting nothing moves the number.
- **It directs effort to the cheapest uncovered lines** — accessors, generated code, constructors, string formatting — and away from the branches that carry risk, because the branch that needs a fixture, a failure injection, and a real engine costs a hundred times more per point.
- **It makes deletion of untested code the fastest way to comply**, which is occasionally right and usually a way to lose an untested edge case rather than test it.

A percentage that already exists in the pipeline is not evidence of anything and is not reported as validation. Where a gate cannot be removed, report it as a gate that ran and report the obligations below separately as the actual coverage claim.

## The rule that replaces it: the named obligations

**Every item below has at least one test that names the broken implementation it defends against. Nothing else carries a coverage obligation, and an item with no such test is an unmet obligation reported at the severity of what the item protects.**

1. **Every branch of every control**, in both directions — admitted and refused. Authentication, authorization, tenancy, rate limits, admission and shedding decisions, and any flag that gates access. `/alaa-security-review` (`$alaa-security-review`) names which controls a given change has.
2. **Every failure mode enumerated for the change**, each with the test that produces it. `70-failure-mode-first.md` owns the enumeration.
3. **Every state transition of anything with states**, including the transitions that must be refused. An unrefused illegal transition is how data reaches a state no code was written to handle.
4. **Every boundary of every bound**: the value at the limit, one inside, one outside, and the empty and maximal cases of every collection, string, and page.
5. **Every error the code can return**, at the layer that returns it, asserted for the declared code and shape. `/alaa-services-contract` (`$alaa-services-contract`) owns the codes and shapes.
6. **Every reported defect**, with a test that fails against the code as it stood when the defect was reported, added in the same change as the fix. A fix with no such test cannot be distinguished later from a fix that was reverted.
7. **Every contract this service publishes or consumes**, at the contract layer, on both sides where both are in this fleet.
8. **Every mechanism whose removal must break a test** — retry, timeout, breaker, bulkhead, shed, degradation, idempotency. `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the list and the injection.
9. **Every boundary where untrusted input is parsed, decoded, or deserialised**, with at least one malformed and one hostile input asserted to be refused.
10. **Every published request in a shipped API artifact**, asserted at the request layer. `/alaa-postman-collections` (`$alaa-postman-collections`) owns those assertions.

The obligations are the review's checklist and the report's `Coverage obligations` field. Each is met or unmet; there is no partial credit, because a partially covered control is an uncovered control on the path nobody tested.

## The one legitimate use of the coverage tool

**Read coverage as a diff, not as a number.** A line added or changed by this change and executed by no test is a question with an answer: either a test is missing, or the line is unreachable and should not have been written. Both answers are worth having, and neither is visible in a repository-wide percentage.

The procedure:

1. Run coverage over the suite with the change applied.
2. Intersect the executed set with the change's diff.
3. For each changed line executed by nothing, decide: add the test, or delete the line.
4. Report the decision per line, not a number.

Use the tool this way and it is useful. Use it as a gate and it measures the team's willingness to write assertion-free tests.

## Mutation as the honest measure

Where the language has a mutation-testing tool, it measures the property this skill actually cares about: it introduces a plausible broken implementation and reports whether any test failed. That is the core rule, automated.

Use it as an investigation, not a gate: run it over the code carrying the change, read the surviving mutants, and treat each survivor as a candidate missing test. Do not gate on a mutation score, for the same reason a coverage percentage is not a gate — the number can be raised by killing cheap mutants in code nobody depends on.

Where no such tool exists, the audit procedure in `10-what-makes-a-test.md` is the manual equivalent, and its survivor count is the number to report.
