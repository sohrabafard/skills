# Coverage

## Why a percentage target is not a rule

A coverage tool records which lines, branches or statements were **executed**, and no assertion: a test with no assertions raises coverage as much as a test that asserts the value. A percentage target also directs effort to the cheapest uncovered lines, away from the risky branches.

Never report an existing pipeline percentage as validation. Where the gate cannot be removed, report it as a gate that ran, and report the obligations below separately as the coverage claim.

## The rule that replaces it: the named obligations

**Every item below has at least one test that names the broken implementation it defends against. An item with no such test is an unmet obligation, reported at the severity of what the item protects. Nothing else carries a coverage obligation.** An item applies only to a decision this project owns and a failure that can reach it (`SKILL.md` *Whether a test is owed*); record an item outside that under `Not written`. Obligations 1, 6 and 9 are always owed.

1. **Every branch of every control**, admitted and refused: authentication, authorization, tenancy, rate limits, admission and shedding decisions, and any flag that gates access. `/alaa-security-review` names which controls a change has.
2. **Every failure mode enumerated for the change**, each with the test that produces it (`70-failure-mode-first.md`).
3. **Every state transition of anything with states**, including the transitions that must be refused. An unrefused illegal transition puts data in a state that no code handles.
4. **Every boundary of every bound the code enforces**: the value at the limit, one inside, one outside, and the empty and maximal cases of every collection, string and page whose size the code branches on or limits.
5. **Every error the code can return**, at the layer that returns it, asserted for the declared code and shape. `/alaa-services-contract` owns the codes and shapes.
6. **Every reported defect**, with a test that fails against the code as it stood when the defect was reported, added in the same change as the fix. Without it, nobody can tell the fix from a reverted fix.
7. **Every contract this service publishes or consumes**, at the contract layer, on both sides where both are in this fleet.
8. **Every mechanism whose removal must break a test**: retry, timeout, breaker, bulkhead, shed, degradation, idempotency. `/alaa-reliability-sla` owns the list and the injection.
9. **Every boundary where untrusted input is parsed, decoded or deserialised**, with at least one malformed and one hostile input asserted refused.
10. **Every published request in a shipped API artifact**, asserted at the request layer. `/alaa-postman-collections` owns those assertions. Reason: a validator run over this platform's own API collection found 73 requests with no test, including the whole Auth folder.

The obligations are the review checklist and the report's `Coverage obligations` field. Each is met or unmet, with no partial credit: a partially covered control is uncovered on the path nobody tested.

## The one legitimate use of the coverage tool

**Read coverage as a diff, not as a number.** Run coverage over the suite with the change applied, and intersect the executed lines with the change's diff. For each changed line that no test executes, add the test or delete the line. Report the decision per line, not a number.

## Mutation as the honest measure

A mutation-testing tool automates the core rule. Where the language has one, run it over the changed code as an investigation, and treat each surviving mutant as a candidate missing test. Never gate on a mutation score: killing cheap mutants in code nobody depends on raises it.

Where no such tool exists, use the audit in `10-what-makes-a-test.md` *Auditing tests that already exist*, and report its survivor count.
