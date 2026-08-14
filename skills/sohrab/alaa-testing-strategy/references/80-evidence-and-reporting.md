# Evidence And Reporting

Read when reporting a test result, when reviewing someone else's reported result, and when a test cannot be run at all. `SKILL.md` holds the binding rule: a check not observed to run is reported as not run.

## What a reviewer needs, per claim

A reviewer's job is to decide whether to trust a claim without re-running it. That decision needs five facts, and a claim missing any one of them is reported back as unverified rather than accepted:

1. **The command, verbatim**, including its flags and its environment overrides.
2. **The working directory** it ran in.
3. **The proof level reached**, by name from `40-proof-strength.md`.
4. **The observed outcome** — the exit status, plus the specific assertion that mattered. "Suite passed" is not the assertion that mattered; "the refusal path asserted zero outbound requests" is.
5. **The artifact path**, where the run produced logs, coverage, profiles, or screenshots.

Two claims are never accepted, however confidently they are written: a check that was not executed, and a check whose result was not observed by whoever is reporting it. Both are reported as `not run`, with the reason.

## Reruns

**A rerun that passes after a failure is a flaky result, never a clean pass.** Report both outcomes — the failure and the pass — and enter the classification procedure in `50-flake.md`. The failing run is the observation that carries information; the passing run only shows that the failure is not deterministic, which is the input to the classification, not a resolution of it.

Reporting the second run alone is the single most common way a real intermittent defect is lost, because the first run is the only evidence it ever produced.

## Scoping a pass

**A pass runs the gates the change's paths reach, and cites the rest.** Reachability is computed from the changed paths — the suites, contract tests, and checks that read them, directly or through a caller — and is never re-decided as a per-phase judgement. A gate no changed path can reach observes nothing new, so running it charges its full cost for a result already recorded.

**The pass names the gates it cited, not only the ones it ran.** List each cited gate beside the run ones in the `Tier` field, with its command and timestamp. A report showing only what ran leaves a reader unable to tell a gate that was unreachable from one that was forgotten, and both read as coverage.

## Reusing an earlier result instead of re-running it

`SKILL.md` carries the binding rule and the four validity conditions. This section owns how a reused result is reported, because a cited result and a fresh one are not interchangeable in a report even when they are interchangeable as evidence.

A cited claim carries the five facts above **plus two more**: the timestamp of the run it is citing, and the tree identity it ran against — the commit or, on an uncommitted tree, the exact paths and their state. Without the second, no reader can check the first validity condition, and the citation degrades into an assertion that nothing changed.

Write it as one row, marked: `cited` rather than `run`. A report that presents a cited result as a fresh one has misstated when the evidence was obtained, which is the same class of error as misstating the proof level.

Three rules settle the common disputes:

- **A reviewer may demand one re-run**, and gets it without argument. The reuse rule exists to stop unprompted repetition, not to refuse a check that a reviewer has a reason to want.
- **A citation across a subagent boundary names the agent that observed it.** A result the reporting agent did not observe is reported as not run — that rule is not relaxed by citation; the observing lane's evidence is carried forward with its owner attached.
- **A merge, rebase, or conflict resolution invalidates every result taken before it.** The merged tree is a tree nothing has run against, whatever both parents returned.

## A result obtained after changing the command

Changing a command, a flag, a timeout, an environment variable, a fixture, or a seed produces a result for a *different* check. Report both: the original command with its failure, and the altered command with its result, stated as two separate rows. The reviewer decides whether the alteration was legitimate; the report does not decide it by omitting the first row.

`/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) owns the execution-side rule about which commands may be run and under what resource policy through its `alaa-verifier` role. This file owns only how the result is reported and what it means.

## A removal or mutation experiment

`SKILL.md` requires every control to be proven by removal, and that experiment is evidence only when its observed failure output is reported — the test that failed and the assertion that produced it. An experiment reported as having failed as expected, with no output, is indistinguishable from one that was never run, and is recorded as not run.

**A surviving mutation is reported as surviving, before anything is repaired.** When the test still passes with the mechanism removed or inverted, that outcome is written down and reported first. What is then repaired is the cause — the test that failed to defend the control — and never the experiment: adjusting the mutation until the test fails converts a missing test into a report of a passing one.

## When a test cannot be run at all

Five steps, in order, and none of them is optional:

1. **Name the level reached and the level required**, from `40-proof-strength.md`.
2. **Name the blocker in one line** — the runtime that would not start, the dependency absent, the credential missing, the platform unsupported, the fixture data unavailable.
3. **Write the test anyway**, at the level the claim requires, and mark it with the repository's own skip mechanism carrying the blocker as its reason string. A test that exists and skips is recovered the moment the environment appears and is visible in every run's skip count; a test never written is invisible forever, and the claim it would have proven is indistinguishable from a claim nobody thought of.
4. **Record the claim as a gap**, at the severity the claim carries, in the report's `Gaps` field.
5. **Report the whole change as `pass-with-actions` or `blocked`**, never `pass`. It is `blocked` when the claim depends on what the unreachable level alone decides — a query, a constraint, an isolation behaviour, a delivery guarantee, a datastore-enforced control. It is `pass-with-actions` when the unreachable level would only have raised confidence in a claim already proven at a lower level.

Two things are never done in place of these five: deleting the assertion so the test can run, and weakening the assertion until it passes at a lower level. Both convert a visible gap into an invisible false claim, which is the exact failure this whole skill exists to prevent.

## Reviewing someone else's reported result

Four checks, each mechanical:

1. **Does every claim carry the five facts above?** Missing facts make the claim unverified regardless of how the run went.
2. **Does the level named match the components that were actually real?** An embedded engine reported as level 6 is the specific error to look for, and the command in fact 1 usually reveals it.
3. **Does any claim rest on a test that would pass against a broken implementation?** Ask for the broken implementation the test names; a claim whose test cannot name one is not evidence. `10-what-makes-a-test.md` owns the audit that settles it.
4. **Was any run repeated?** A report showing one pass where the transcript shows two runs is a flaky result reported as clean, and it is returned for reclassification.

Findings are reported most severe first, and a finding at any of these four is reported before the substance of the change, because the substance cannot be assessed on evidence that has not been established as evidence.

## The report field

The `Evidence` and `Gaps` fields of the output contract in `SKILL.md` are where all of this lands. One line per claim in `Evidence`; one line per unproven claim in `Gaps`, each carrying the blocker and the severity. No other output contract exists in this skill, and no reference defines another.
