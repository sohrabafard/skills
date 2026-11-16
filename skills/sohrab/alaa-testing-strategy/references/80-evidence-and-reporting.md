# Evidence And Reporting

## The report fields

The output contract in `SKILL.md` fixes the field names, their order and the tokens of `Decision`, `Not written` and `Tier`. The other fields hold:

```text
Scope: the change, and the surfaces and suites examined
Failure modes: mode -> the test that produces it -> layer -> proof level -> signal owner
Broken implementations: per test, the broken implementation it defends against
Layer placement: per behaviour, the layer and the components that had to be real
Doubles: per double, real|fake|stub|mock|spy, the reason for substituting, can-drift yes|no, and what binds it
Coverage obligations: each named obligation -> the test that meets it, or unmet
Selectors: per test, topic selector and layer selector
Shared setup: per expensive resource, scope (run | package | worker) and per-test isolation
Build reuse: per build, compile, render or image -> the steps that consumed it
Evidence: per claim -> the five facts below
Tier: a cited tier names the four validity conditions as still holding
Execution: check-list snapshot; expected, selected and executed cases; machine-readable reports; resources; the collection, repair and retest state
Status: per command -> class under 120-result-classification.md; timing claims -> samples and limits under 110-execution-resources.md
Flake: per intermittent result, the action taken and its owner
Gaps: one line per unproven claim, with its blocker and severity: claims with no test, levels not reached, quarantined tests and their deadlines
```

## What a reviewer needs, per claim

Return a claim that lacks any of these five facts as unverified:

1. **The command, verbatim**, with its flags and environment overrides.
2. **The working directory** it ran in.
3. **The proof level reached**, named from `40-proof-strength.md`.
4. **The observed outcome**: the exit status and the specific assertion that mattered. "Suite passed" is not that assertion; "the refusal path asserted zero outbound requests" is.
5. **The artifact path**, where the run produced logs, coverage, profiles or screenshots.

Report as `not run`, with the reason, a check that was not executed and a check whose result the reporter did not observe.

## Reruns

**An unchanged rerun that passes after a failure is a flaky result, never a clean pass.** Report both outcomes and enter the classification procedure in `50-flake.md`. A named defect repair changes the input, so its passing retest is not flaky: report the failure, the repair, the new tested identity and the retest separately. Never conceal the original failure.

## Scoping a pass

**A pass runs the gates that the change's paths reach, and cites the others.** Compute reachability from the changed paths: the suites, contract tests and checks that read them, directly or through a caller. Never re-decide it per phase.

**Name the cited gates beside the run ones** in the `Tier` field, each with its command and timestamp, so that a reader can tell an unreachable gate from a forgotten one.

## Reusing an earlier result instead of re-running it

`SKILL.md` *A result stays valid until something named invalidates it* decides when reuse is valid. Write a cited claim as one row marked `cited`, not `run`. It carries the five facts, the timestamp of the cited run and the tree identity it ran against: the commit, or on an uncommitted tree the exact paths and their state. Without the tree identity, nobody can check the first validity condition.

- **A reviewer may demand one re-run**, and gets it without argument. The reuse rule stops unprompted repetition only.
- **A citation across a subagent boundary names the agent that observed the result.** It does not relax the not-run rule above.
- **A merge, rebase or conflict resolution requires evidence reconciliation.** Invalidate the affected inputs and integration claims. Unchanged narrower checks stay citable while all four validity conditions hold. Required final exhaustive proof still runs fresh on the resulting candidate.

## A result obtained after changing the command

A changed command, flag, timeout, environment variable, fixture or seed produces a result for a different check. Report two rows: the original command with its failure, and the altered command with its result. The reviewer decides whether the alteration was legitimate.

## A removal or mutation experiment

A removal experiment is evidence only when its observed failure output is reported: the test that failed and the assertion that produced it. Record an experiment reported as "failed as expected" with no output as not run.

**Report a surviving mutation as surviving, before you repair anything.** Then repair the test that failed to defend the control. Never adjust the experiment until the test fails: that turns a missing test into a reported passing one.

## When a test cannot be run at all

Do all five steps, in order:

1. **Name the level reached and the level required**, from `40-proof-strength.md`.
2. **Name the blocker in one line**: the runtime that would not start, the dependency absent, the credential missing, the platform unsupported, the fixture data unavailable.
3. **Write the test anyway**, at the required level, and mark it with the repository's own skip mechanism, with the blocker as its reason string. An unwritten test is invisible; a skipped test shows in every skip count.
4. **Record the claim as a gap**, at its severity, in the `Gaps` field.
5. **Report the change as `pass-with-actions` or `blocked`**, never `pass`. It is `blocked` when the claim depends on what the unreachable level alone decides: a query, a constraint, an isolation behaviour, a delivery guarantee, a datastore-enforced control. It is `pass-with-actions` when that level would only raise confidence in a claim already proven at a lower level.

These steps replace any assertion change. `SKILL.md` *A failing tier is classified before it is repaired* bans a deleted or weakened assertion.

## Reviewing someone else's reported result

Check four things, and report their findings before the substance of the change, most severe first:

1. Every claim carries the five facts.
2. The level named matches the components that were real. Look for an embedded engine reported as level 6; the command usually reveals it.
3. Every test behind a claim can name the broken implementation it defends against (`10-what-makes-a-test.md` *Auditing tests that already exist*).
4. No reported pass hides a repeated run. Return one as a flaky result for reclassification.
