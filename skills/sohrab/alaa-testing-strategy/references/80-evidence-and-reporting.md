# Evidence And Reporting

## What a reviewer needs, per claim

A reviewer decides whether to trust a claim without re-running it. Return a claim that lacks any of these five facts as unverified:

1. **The command, verbatim**, with its flags and environment overrides.
2. **The working directory** it ran in.
3. **The proof level reached**, named from `40-proof-strength.md`.
4. **The observed outcome**: the exit status and the specific assertion that mattered. "Suite passed" is not that assertion; "the refusal path asserted zero outbound requests" is.
5. **The artifact path**, where the run produced logs, coverage, profiles or screenshots.

Report as `not run`, with the reason, both a check that was not executed and a check whose result the reporter did not observe, however confidently either is written.

## Reruns

**An unchanged rerun that passes after a failure is a flaky result, never a clean pass.** Report both outcomes and enter the classification procedure in `50-flake.md`, because the first run is often the only evidence an intermittent defect ever produces. A named defect repair changes the input: report the failure, the repair, the new tested identity and the retest separately. A successful repaired path is not automatically flaky. Never conceal the original failure.

## Scoping a pass

**A pass runs the gates the change's paths reach, and cites the rest.** Compute reachability from the changed paths: the suites, contract tests and checks that read them, directly or through a caller. Never re-decide it per phase. A gate that no changed path reaches observes nothing new.

**Name the cited gates beside the run ones** in the `Tier` field, each with its command and timestamp. A report that shows only what ran cannot tell an unreachable gate from a forgotten one.

## Reusing an earlier result instead of re-running it

`SKILL.md` *A result stays valid until something named invalidates it* owns when reuse is valid. This section owns how to report it.

A cited claim carries the five facts **plus** the timestamp of the cited run and the tree identity it ran against: the commit, or on an uncommitted tree the exact paths and their state. Without the tree identity, nobody can check the first validity condition.

Write it as one row marked `cited`, not `run`. Presenting a cited result as fresh misstates when the evidence was obtained, the same class of error as misstating the proof level.

- **A reviewer may demand one re-run**, and gets it without argument. The reuse rule stops unprompted repetition, not a check that a reviewer has a reason to want.
- **A citation across a subagent boundary names the agent that observed it.** Citation does not relax the not-run rule above; the observing lane's evidence carries its owner.
- **A merge, rebase or conflict resolution requires evidence reconciliation.** Invalidate the affected inputs and integration claims. Unchanged narrower checks stay citable when all four validity conditions hold. Required final exhaustive proof still runs fresh on the resulting candidate.

## A result obtained after changing the command

A changed command, flag, timeout, environment variable, fixture or seed produces a result for a different check. Report two rows: the original command with its failure, and the altered command with its result. The reviewer decides whether the alteration was legitimate.

This file owns claim evidence and proof reporting. Before you choose or run commands, read `100-test-execution.md` and `110-execution-resources.md`. Before you interpret outcomes, read `120-result-classification.md`.

## A removal or mutation experiment

A removal experiment is evidence only when its observed failure output is reported: the test that failed and the assertion that produced it. Record an experiment reported as "failed as expected" with no output as not run.

**Report a surviving mutation as surviving, before you repair anything.** Then repair the cause, the test that failed to defend the control, and never the experiment, because adjusting the mutation until the test fails turns a missing test into a reported passing one.

## When a test cannot be run at all

Do all five steps, in order:

1. **Name the level reached and the level required**, from `40-proof-strength.md`.
2. **Name the blocker in one line**: the runtime that would not start, the dependency absent, the credential missing, the platform unsupported, the fixture data unavailable.
3. **Write the test anyway**, at the required level, and mark it with the repository's own skip mechanism, with the blocker as its reason string. A skipping test is recovered when the environment appears and shows in every skip count; a test never written is invisible, and its claim looks like one nobody thought of.
4. **Record the claim as a gap**, at its severity, in the report's `Gaps` field.
5. **Report the change as `pass-with-actions` or `blocked`**, never `pass`. It is `blocked` when the claim depends on what the unreachable level alone decides: a query, a constraint, an isolation behaviour, a delivery guarantee, a datastore-enforced control. It is `pass-with-actions` when that level would only raise confidence in a claim already proven at a lower level.

These steps replace any assertion change. Never delete or weaken an assertion so that the test runs or passes at a lower level, because that turns a visible gap into an invisible false claim.

## Reviewing someone else's reported result

1. **Does every claim carry the five facts?** A claim with a missing fact is unverified, however the run went.
2. **Does the level named match the components that were real?** Look for an embedded engine reported as level 6; the command usually reveals it.
3. **Does any claim rest on a test that would pass against a broken implementation?** Ask for the broken implementation the test names. A test that cannot name one is not evidence. The audit in `10-what-makes-a-test.md` settles it.
4. **Was any run repeated?** One reported pass where the transcript shows two runs is a flaky result reported as clean. Return it for reclassification.

Report findings most severe first, and report a finding from these four checks before the substance of the change, because unestablished evidence cannot support an assessment.

## The report field

All of this lands in the `Evidence` and `Gaps` fields of the output contract in `SKILL.md`: one line per claim in `Evidence`, and one line per unproven claim in `Gaps` with its blocker and severity. No other output contract exists in this skill.
