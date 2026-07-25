# Failure-Mode-First Design

Read at the start of every change, before any test is written. `SKILL.md` holds the binding rule: the test list is derived from the enumerated failure modes, and the happy path is added last as a control.

## One enumeration, two consumers

`/alaa-observability-soc` (`$alaa-observability-soc`) requires every change to enumerate the failure modes it introduces and to name a signal for each. This skill requires every change to enumerate the failure modes it introduces and to name a test for each. **It is the same enumeration, produced once, and the enumeration table lives in that skill — `references/10-signal-model.md`, the section "Start from the diff, not from the question".**

Two lists would diverge, the divergence would be invisible because neither list names the other's gaps, and each list's author would assume the other had covered the mode. Producing one list with both columns makes a mode dropped from either half visible immediately, because the row exists with an empty cell.

Do not restate that table here or in any service repository. Read it, and extend the row.

## The row

One row per failure mode, five columns. The first three belong to observability, the last two to this skill.

```text
mode | signal | query or alert | test that produces the mode | layer and proof level
```

- **mode** — what goes wrong, stated as an observable outcome rather than a cause.
- **signal** — the metric family, log event, or span that would show it.
- **query or alert** — the exact query an operator would run, and whether it pages, alerts, or is diagnostic only.
- **test that produces the mode** — the test that makes this mode happen on purpose and asserts what the system does. Its name, or `none` if it does not exist yet.
- **layer and proof level** — from `20-layers.md` and `40-proof-strength.md`.

A row with an empty test cell is a gap reported at the severity of the mode. A row whose test cell says "existing tests cover it" names the existing test, or it is an empty cell — an unnamed claim of coverage is how the gap ships.

## Deriving the test from the mode

The enumeration produces modes; this converts each into a test.

1. **Name the mode as an outcome**, not a cause. "The consumer processes the same message twice" rather than "the broker redelivers".
2. **Name the mechanism that is supposed to prevent it.** If there is none, the mode is a design gap and the test cannot be written yet — report it and stop; writing a test for absent behaviour produces a test asserting the current wrong behaviour.
3. **Name what must be real for the mode to be producible** — the placement procedure in `20-layers.md`. The mode usually fixes the layer by itself: a redelivery mode needs a real broker, a constraint-violation mode needs a real engine, a wrong-branch mode needs neither.
4. **Name how the mode is caused on demand.** A double that produces it, an injected fault, a fixture in the offending state, two concurrent requests, a clock moved across a boundary. A mode with no way to cause it on demand is a mode with no test, and the way to cause it is what `30-doubles.md` calls the first legitimate reason to substitute.
5. **Write the assertion as the mechanism's observable effect**, and separately assert the absence of the effect the mechanism was there to prevent — the two-property rule in `SKILL.md`.
6. **Prove it by removal.** Remove the mechanism; the test must fail.

## Where the modes come from when the diff is small

Three inputs, in this order, and all three are read:

1. **The diff.** The enumeration table maps what a diff adds to the modes it introduces.
2. **The incident and defect history of this surface.** Every mode that has already happened here is a mode with demonstrated probability, and a fix with no test is a fix that can be reverted silently — obligation 6 in `60-coverage.md`.
3. **The dependencies the change touches.** Each dependency call carries the modes in `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/80-verification.md`, ordered there by how often they are missed. That skill owns which to inject; this file owns that they enter the enumeration.

## Ordering, and what it prevents

Write the failure tests first, then the happy path. The order is not a preference — it changes what gets written.

- Starting from the happy path produces a suite shaped by what the code does, so the branches the code does not take are never noticed, and every mode arrives later as a production incident.
- Starting from the failure modes produces a suite shaped by what can go wrong, and the happy path is then one more case in a list rather than the frame the whole suite is built in.

The happy path still gets written, last, and its job is stated in `10-what-makes-a-test.md`: it proves the failure tests fail for the reason claimed rather than because the arrangement could never have succeeded.

## The enumeration is part of the change

A change ships with its enumeration recorded — in the merge request, the design note, or the repository's own change record. An enumeration held only in the author's head cannot be reviewed, cannot be checked for empty cells, and cannot be read by whoever handles the incident. A change with no recorded enumeration is reported as an unmet obligation, not as an oversight to raise informally.
