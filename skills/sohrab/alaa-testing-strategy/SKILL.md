---
name: alaa-testing-strategy
description: "Test design and execution doctrine: owed tests, layers, doubles, proof strength, selectors, shared setup, build reuse, flake diagnosis, check collection, batch repair, result classification, CPU budgets and comparative timing. Use to write, review, repair or run tests and validation commands; investigate slow, flaky or falsely green suites; choose check breadth or resources; or report a check result, directly or through either runtime. Do not use for framework syntax (per-language skills, /golang-testing), fault injection (/alaa-reliability-sla), security controls (/alaa-security-review), contract values (/alaa-services-contract) or Postman tests (/alaa-postman-collections). Runtime orchestrators own allocation, independence and the scheduling of phases and reviews; this skill requires no orchestrator."
---

# Alaa Testing Strategy

Decide what to test, at which layer, with which doubles, at which proof level, and what evidence a reviewer may accept. This skill owns test design and generic execution policy. It owns no framework syntax, fixture library or Ala value. Activating it installs nothing and grants no environment-mutation authority.

## When this applies

Apply it to a change that adds or alters a behaviour, a control, a contract, a dependency call, a stored effect or a failure path; to any work on a test or a suite; and to selecting, running or reporting validation commands, CPU-heavy checks or comparative timing.

A change that alters no behaviour and no test (a comment, formatting, a rename with no call-site semantics, a docs-only edit) carries no test-design obligation. Execution and reporting policy still applies when it runs validation.

**No shipped surface is exempt.** Every route, queue consumer, job, scheduled task and published request carries at least one test that meets the core rule. A credential-issuing surface is the least exempt, because its silent breakage grants access.

**A repository's own validation-policy file outranks this skill inside that repository.** It decides which checks gate a change, when, and what may be cited instead of re-run. This skill is the default for what that file leaves open.

## The core rule: what makes a test a test

**A test names the broken implementation it defends against. A test that still passes against a plausible broken implementation is not a test: a reviewer counts its green result as coverage and stops looking.**

Derive the broken implementation in four steps:

1. **Name the decision the code makes** in one sentence: a branch, comparison, filter, limit, transformation or effect. Without that sentence, do not design the test.
2. **Write the plausible wrong version** that a competent engineer ships by mistake, never a crash. `references/10-what-makes-a-test.md` maps each code shape to its characteristic break.
3. **Require the candidate assertion to fail against that version.** An assertion that passes measures something else, usually that the code is reachable.
4. **Prove every control by removal.** A control is a mechanism whose absence is a defect: an authentication or authorization check, a tenancy filter, a limit, an idempotency key, a validation. Delete or invert it in a scratch copy, run the test and require a failure. Repair or delete, in the same change, a test that passes both ways.

Every negative test:

- **asserts the absence of the effect, not only the error.** A status-only assertion passes against code that rejects after it did the work. Assert zero outbound requests, rows written, events emitted, files created, credentials minted and messages published, beside the refusal.
- **asserts a control claimed at several layers separately at each layer, with the other layers neutralised.** The inner layers run when the outer one is bypassed, and one passing outer assertion hides a missing inner layer.

The second property does not conflict with non-negotiable 2. **Remove the mechanism at one layer and run all its tests. If only that layer's test fails, the mechanisms are independent and every test stays. If all fail, they are one test written several times: keep the one that `references/20-layers.md` *The rule against triplication* selects, and delete the others.**

## Whether a test is owed

**A test is owed only for a decision this project makes, against a failure that can reach it.** Check both conditions before you write a candidate. Record a candidate that fails either one under `Not written` with its reason, and do not write it: an unowed test costs run and maintenance time on every change and proves nothing about this project.

- **Owned decision.** No test is owed for behaviour that the language, the runtime, the framework, a dependency's own suite, a generator, or a type, schema, lint or render gate already proves. Record `covered by <owner> <suite>`. A conformance harness that the owner requires the consumer to run stays required: it tests the consumer.
- **Reachable failure.** A failure mode earns a test only when it cites one source: a path in this diff, or in the code it changes, that can produce it; an incident or defect on this surface; a dependency failure mode this deployment exercises; or a contract obligation the code must honour. Otherwise record `not reachable: <reason>`.
- **A changed decision, not a changed file, is the reason for a test.**
- **Always owed, whatever the two conditions say:** every control `/alaa-security-review` names, every reported defect's regression test, every boundary that parses untrusted input (obligations 1, 6 and 9 in `references/60-coverage.md`), and the floor under *No shipped surface is exempt*. An upstream check never makes a mode unreachable across a trust boundary: the downstream check runs when the upstream one is bypassed.

When a candidate is not owed a test, or a mode looks unreachable, read `references/90-test-economy.md` *Candidates that are not owed a test* for what the consumer tests instead.

Before you add a discretionary test, review, specialist, proof tool or gate beyond the declared cadence or repository requirements, state its concrete uncovered risk and why existing evidence is insufficient. Without that answer, do not add it. Required checks stay required. Record the answer in the admitted plan's check list, or without a plan in the existing evidence owner.

## Non-negotiables

1. Every test names the failure it defends against, in its name or in one comment beside it.
2. Verify each behaviour at exactly one layer, chosen by the placement procedure in `references/20-layers.md`.
3. Use the real dependency whenever it runs deterministically inside the suite's time budget. Substitute a double only for a state the real dependency cannot enter on demand, or for that budget, and record which beside the double.
4. Bind every double that can drift by a parity suite: the same cases against the double and the real implementation, with identical results required.
5. Report every claim at the proof level that ran, never at the level it was meant to reach.
6. Classify an intermittent failure as a product defect or a broken test before any other action on it. A blanket retry is never that action.
7. Name coverage obligations. Never set a percentage target: executing code without asserting anything satisfies it.
8. Derive the test list from the change's failure modes that pass *Whether a test is owed*. Add the happy path last, as the control that the failure tests fail for the reason claimed.
9. Report a check that you did not observe to run as not run.
10. Make every test hermetic over its mutable state: it creates the data it asserts on, asserts only on that data and leaves none behind. A failed reset or cleanup makes every later result over that state `CONTAMINATED`: report it, and stop the cases that depend on that state. Before you create or share test infrastructure, or write or review a test over it, read `references/90-test-economy.md` *Setup once*.
11. No test synchronises on wall-clock sleeping. Inject a controllable clock, and wait on the condition with a bounded timeout.
12. Choose check breadth from the changed inputs, the required proof and the uncovered risk. A new phase, agent or reviewer earns no rerun.
13. Make every test this change adds or changes selectable by its topic and by its layer, through the runner's native selector, and record the selecting command in the repository (`references/90-test-economy.md` *Topic and layer selectors*).
14. Produce one build, compile, render or image per tree state and environment, and make every step of that pass consume it (`references/90-test-economy.md` *Build once per tree state*).
15. A case failing never stops an independent case from running. A case that depends on another case's outcome or state declares that dependency. When the precondition fails, the case is reported `SKIPPED` naming that precondition, and never runs against the broken state.

## Designing the tests for a change

Before you design the tests for a change, read `references/70-failure-mode-first.md` and follow its *Design order*.

## Proof levels

Six levels, weakest first: 1 static, 2 unit or in-memory, 3 parity, 4 local smoke, 5 in-runtime service, 6 live-dependency. A level never substitutes for a higher one. Before you assign, report or review a proof level, read `references/40-proof-strength.md`.

## Scope tiers: how much of the suite runs, and when

A proof level states how strong one claim is. A **tier** states how much of the suite runs now. Tiers choose check breadth, not review timing: `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own the review cadence, the review authority and the scheduling. Pass a nested orchestration the workflow's whole-engagement boundary, so that it does not treat its own end as the final candidate.

| Tier | What runs | Who runs it | When |
|---|---|---|---|
| **Focused** | the smallest test, path or scenario that distinguishes the subtask's changed behavior from its plausible failure, plus the lint, type-check and build steps the touched files need | the implementing lane | subtask end under the declared cadence |
| **Task acceptance** | bounded acceptance selectors that combine the focused selectors of that task's subtasks, with still-valid coverage cited | the task owner | task end under the declared cadence |
| **Affected** | selectors of topics reachable from changed surfaces, including callers, shared fixtures and contract checks | the required boundary observer | the final gate stage by default, or earlier when repository policy requires |
| **Exhaustive** | the whole suite and only the race, end-to-end and higher-level proofs the claims require | the required final observer | once, on the whole engagement's final candidate, when required |

A focused check adds no expensive setup and runs no full suite; it reuses reset-safe infrastructure that is already available. No fixed duration and no blanket container ban apply. Labels never narrow an actual command's scope.

**Run the exhaustive tier only on the tree that ships.** A merge, rebase or cherry-pick after the run produces a tree that nothing has run against. A clean integration is no exception: no conflict proves that no edit was needed, never that the combination was observed. Integrate first and then run, or run again after integrating.

### A result stays valid until something named invalidates it

Cite a recorded result, with its original command and timestamp, while all four of these are unchanged since it was observed:

- the tracked tree at the paths the check reads;
- the tool, runner, and dependency versions;
- the environment and service state the check depends on;
- the flags, seed, configuration, and working directory it ran under.

When one of them changes, say which one, and re-run every result downstream of it. A phase transition, new agent or compaction alone invalidates nothing. Three limits apply:

- A required exhaustive tier on the final candidate is always fresh.
- A failed, flaky, contaminated, timed-out or environment-blocked result cannot discharge a required check.
- A required final aggregate discharges a narrower check only when the covered inputs, environment, flags and required observer match demonstrably. Markdown files and templates may be checker inputs, so a documentation-only difference proves no equivalence.

After a batch repair, select retests under `references/100-test-execution.md`. Reuse passing evidence only where its inputs, observer and freshness requirements still match.

### A failing tier is classified before it is repaired

Classify first, then act: a repair aimed at the wrong class turns a host problem into a product edit. Four classes stay separate:

- a defect in the product;
- a defect in the test harness, fixture or runner;
- a host-environment block: the shell, the container runtime, a permission, a missing executable or service;
- a contaminated tree, including a stale build or test cache.

`references/120-result-classification.md` holds the status vocabulary and the host sub-classes. No class permits reporting the change as passed.

Repair the defect and rerun its failing path. Never make a check pass by deleting or weakening an assertion, suppressing a finding, lowering a threshold, widening a tolerance, adding an assertion retry, skipping a case, altering a fixture, hard-coding an expected result or lowering a review standard. Report an unreachable tier as unreached, with its blocker.

## Executing checks

For any direct or delegated validation run, read `references/100-test-execution.md` before you choose commands, resources or a result status.

After you change this skill's execution policy or consumer routes, run `python3 scripts/check_execution_contracts.py` from this skill directory: `0` clean, `1` findings, `2` unavailable input. Either nonzero blocks the affected claim: repair within the caller's existing budget, or report blocked. Never treat `2` as a pass. This maintainer check does not run on ordinary application tasks.

## Output contract

Return these fields, in this order, for every test design, test review or reported test run. Before you write them, read `references/80-evidence-and-reporting.md` *The report fields* for what each field holds.

```text
Decision: pass | pass-with-actions | blocked
Scope
Failure modes
Not written: candidate -> framework | owner suite <owner> <suite> | generated | declaration gate | not reachable: <reason>
Broken implementations
Layer placement
Doubles: real|fake|stub|mock|spy, can-drift yes|no
Coverage obligations
Selectors
Shared setup: scope run | package | worker
Build reuse
Evidence
Tier: focused | task acceptance | affected | exhaustive -> run now | cited
Execution
Status
Flake: product defect | broken test
Gaps
```

## Stop conditions

Stop successfully when all of these hold:

- every enumerated failure mode has a test that fails when its mode is injected, or a `Not written` reason;
- every test this change adds or changes has a topic selector;
- every control is proven by removal;
- every double that can drift is bound;
- every named coverage obligation is met or recorded as a gap;
- every reported claim carries an observed result at a stated level and tier;
- every required check has valid evidence, including a fresh exhaustive tier on the final candidate when required.

Stop and report blocked when any one of these holds:

- no arrangement available here can produce a behaviour's failure, so the behaviour has no layer;
- a required proof level is unreachable, and the claim depends on what that level alone decides;
- an intermittent failure stays unclassified after the procedure in `references/50-flake.md` ran to completion;
- a control cannot be proven by removal, because removing it breaks compilation of unrelated code and no equivalent inversion exists;
- a test the change requires cannot run, and the repository has no skip mechanism to record it.

## When NOT to use

- The question is framework idiom or assertion syntax. The per-language skill owns it.
- No test is designed, reviewed or repaired, and no validation command, resource decision, timing comparison or result claim is involved.
- The question is fault injection, a security control, an envelope or code, or a Postman request test. `references/00-topic-map.md` *Owned by another skill* names each owner.

## Reference routing

For a reference that no pointer above names, read `references/00-topic-map.md` first; it states when to read each one. Before you assert a contract value, design fault injection, test a security control or write a request test, read its *Owned by another skill* section.
