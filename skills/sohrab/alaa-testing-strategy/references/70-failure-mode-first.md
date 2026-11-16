# Failure-Mode-First Design

## Design order

Do these steps in order. Read the reference beside a step when you do that step.

1. Enumerate the change's failure modes from the diff, once, in the shared row below.
2. Decide which modes are owed a test (`SKILL.md` *Whether a test is owed*), and record the others. Cite an existing test that already fails when the mode is injected instead of writing a duplicate (`90-test-economy.md`).
3. Derive each owed mode's broken implementation (`10-what-makes-a-test.md`).
4. Place each test at one layer (`20-layers.md`).
5. Choose the doubles, and bind each one that can drift (`30-doubles.md`).
6. Give each test its topic and layer selector and its shared setup, reusing existing fixtures first (`90-test-economy.md`).
7. Assign each claim's proof level, and confirm that this environment reaches it before you write the test (`40-proof-strength.md`).
8. Add the tests that an unmet coverage obligation requires (`60-coverage.md`).
9. Add one happy-path test per behaviour, last. Confirm that each failure test fails when its mode is injected and passes otherwise.
10. Run the focused selectors, and report at the level reached, with the blocker for each level not reached (`80-evidence-and-reporting.md`).

## One enumeration, two consumers

`/alaa-observability-soc` requires each change to enumerate the failure modes it introduces and to name a signal for each. This skill names a test for each. **It is one enumeration, produced once. Its table lives in `alaa-observability-soc` `references/10-signal-model.md`, section "Start from the diff, not from the question".** Never restate that table here or in a service repository: read it, and extend the row. One list with both columns shows a dropped mode as an empty cell; two lists diverge unseen.

## The row

One row per failure mode. Observability owns the first three columns, and this skill the last two.

```text
mode | signal | query or alert | test that produces the mode | layer and proof level
```

- **mode**: what goes wrong, as an observable outcome, not a cause.
- **signal**: the metric family, log event or span that shows it.
- **query or alert**: the exact query an operator runs, and whether it pages, alerts or is diagnostic only.
- **test that produces the mode**: the name of the test that causes this mode on purpose and asserts what the system does, or `none`.
- **layer and proof level**: from `20-layers.md` and `40-proof-strength.md`.

A mode that fails `SKILL.md` *Whether a test is owed* carries `not written: <reason>` in its test cell. That is a recorded decision, not a gap. An empty or `none` test cell is a gap at the severity of the mode. A cell that says "existing tests cover it" without the test's name counts as empty.

## Deriving the test from the mode

Name the mode as an outcome: "the consumer processes the same message twice", not "the broker redelivers". Then name two things:

- **The mechanism that should prevent the mode.** If none exists, the mode is a design gap. Report it and stop, because a test for absent behaviour asserts the current wrong behaviour.
- **How to cause the mode on demand**: a double that produces it, an injected fault, a fixture in the offending state, two concurrent requests, a clock moved across a boundary. A mode that nothing can cause has no test.

## Where the modes come from when the diff is small

Read all three inputs, in this order:

1. **The diff.** The enumeration table maps what a diff adds to the modes it introduces.
2. **The incident and defect history of this surface.** A mode that already happened here has demonstrated probability (obligation 6 in `60-coverage.md`).
3. **The dependencies the change touches.** Each dependency call carries the modes in `/alaa-reliability-sla` `references/80-verification.md`. That skill owns which modes to inject.

## The enumeration is part of the change

Record the enumeration with the change: in the merge request, the design note or the repository's change record. Report a change with no recorded enumeration as an unmet obligation.
