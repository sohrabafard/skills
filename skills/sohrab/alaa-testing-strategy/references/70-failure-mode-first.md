# Failure-Mode-First Design

## One enumeration, two consumers

`/alaa-observability-soc` requires each change to enumerate the failure modes it introduces and name a signal for each. This skill names a test for each. **It is one enumeration, produced once, and its table lives in `alaa-observability-soc` `references/10-signal-model.md`, section "Start from the diff, not from the question".** Two lists would diverge invisibly, and each author would assume the other covered a mode. One list with both columns shows a dropped mode as an empty cell.

Never restate that table here or in a service repository. Read it, and extend the row.

## The row

One row per failure mode, five columns. Observability owns the first three, this skill the last two.

```text
mode | signal | query or alert | test that produces the mode | layer and proof level
```

- **mode** — what goes wrong, as an observable outcome, not a cause.
- **signal** — the metric family, log event or span that would show it.
- **query or alert** — the exact query an operator would run, and whether it pages, alerts or is diagnostic only.
- **test that produces the mode** — the name of the test that causes this mode on purpose and asserts what the system does, or `none`.
- **layer and proof level** — from `20-layers.md` and `40-proof-strength.md`.

A mode that fails `SKILL.md` *Whether a test is owed* carries `not written: <reason>` in its test cell, which is a recorded decision, not a gap. An empty test cell is a gap at the severity of the mode. A cell that says "existing tests cover it" names the test, or it counts as empty, because an unnamed coverage claim is how the gap ships.

## Deriving the test from the mode

1. **Name the mode as an outcome**, not a cause: "the consumer processes the same message twice", not "the broker redelivers".
2. **Name the mechanism that should prevent it.** If none exists, the mode is a design gap: report it and stop, because a test for absent behaviour asserts the current wrong behaviour.
3. **Name what must be real for the mode to be producible**, by the placement procedure in `20-layers.md`. The mode usually fixes the layer: redelivery needs a real broker, a constraint violation needs a real engine, a wrong branch needs neither.
4. **Name how to cause the mode on demand**: a double that produces it, an injected fault, a fixture in the offending state, two concurrent requests, a clock moved across a boundary. A mode with no way to cause it has no test. That way is the first legitimate reason to substitute in `30-doubles.md`.
5. **Assert the mechanism's observable effect, and separately the absence of the effect it prevents**, under the two properties in `SKILL.md` *The core rule*.
6. **Prove it by removal.** Remove the mechanism; the test must fail.

## Where the modes come from when the diff is small

Read all three inputs, in this order:

1. **The diff.** The enumeration table maps what a diff adds to the modes it introduces.
2. **The incident and defect history of this surface.** A mode that already happened here has demonstrated probability, and a fix with no test can be reverted silently (obligation 6 in `60-coverage.md`).
3. **The dependencies the change touches.** Each dependency call carries the modes in `/alaa-reliability-sla` `references/80-verification.md`, ordered there by how often they are missed. That skill owns which to inject; this file owns that they enter the enumeration.

## Ordering, and what it prevents

Write the failure tests first, then the happy path, because the order changes what gets written. A suite started from the happy path takes the shape of what the code does, so the branches it does not take go unnoticed and each mode arrives later as an incident. A suite started from the failure modes takes the shape of what can go wrong, and the happy path is one more case in the list.

Write one happy-path test per behaviour, last. It proves that the failure tests fail for the reason claimed, not because the arrangement could never succeed: a failure test that passes against an arrangement no implementation could satisfy proves nothing. A suite of happy paths alone proves only that the routes are routed.

## The enumeration is part of the change

Record the enumeration with the change, in the merge request, the design note or the repository's change record. An enumeration held only in the author's head cannot be reviewed, checked for empty cells, or read during the incident. Report a change with no recorded enumeration as an unmet obligation.
