---
name: alaa-testing-strategy
description: "Test design and execution doctrine: owed tests, layers, doubles, proof strength, selectors, shared setup, build reuse, flake diagnosis, check collection, batch repair, result classification, CPU budgets and comparative timing. Use to write, review, repair or run tests and validation commands; investigate slow, flaky or falsely green suites; choose check breadth or resources; or report a check result, directly or through either runtime. Do not use for framework syntax (per-language skills, /golang-testing), fault injection (/alaa-reliability-sla), security controls (/alaa-security-review), contract values (/alaa-services-contract) or Postman tests (/alaa-postman-collections). Runtime orchestrators own allocation, independence and the scheduling of phases and reviews; this skill requires no orchestrator."
---

# Alaa Testing Strategy

Decide what to test, where, with which doubles, at which proof strength, and what evidence a reviewer may accept, so that every fleet service ships a suite of one shape, because a reviewer cannot tell covered from uncovered in a suite shaped by its author alone. This skill owns test design and generic execution policy, directly or through either runtime, and no framework syntax, fixture library or Ala value. Activating it installs nothing and grants no environment-mutation authority.

## When this applies

Apply it to a change that adds or alters a behaviour, a control, a contract, a dependency call, a stored effect or a failure path; to writing, reviewing, repairing, quarantining, deleting or speeding up tests; to diagnosing a test that fails intermittently or passes against broken code; and to selecting, running or reporting validation commands, CPU-heavy checks or comparative timing.

Test-design obligations do not apply to a change that alters no behaviour and no test: a comment, a formatting pass, a rename with no call-site semantics or a docs-only edit. Execution and reporting policy still applies when that change runs validation.

**No shipped surface is exempt.** Every route, queue consumer, job, scheduled task and published request this project ships carries at least one test that meets the core rule. *Whether a test is owed* decides which behaviour behind it is owed a test. A credential-issuing surface is the least exempt, because its silent breakage grants access.

**A repository's own validation-policy file outranks this skill inside that repository.** Where it states which checks gate a change, when, and what may be cited instead of re-run, it decides. This skill is the fleet default for what it leaves open.

## The core rule: what makes a test a test

**A test names the broken implementation it defends against. A test that still passes against a plausible broken implementation is not a test. Its green result is worse than no test, because a reviewer counts it as coverage and stops looking.**

Derive that broken implementation in four steps:

1. **Name the decision the code makes** (a branch, a comparison, a filter, a limit, a transformation or an effect) in one sentence. Without that sentence, do not design the test.
2. **Write the plausible wrong version** that a competent engineer ships by mistake, not a crash or nonsense. Take it from the catalogue in `references/10-what-makes-a-test.md`, which maps each code shape to its characteristic break.
3. **Check that the candidate assertion fails against that version.** If it passes, it measures something else, usually that the code is reachable, and the real test is not written yet.
4. **Prove every control by removal**: an authentication or authorization check, a tenancy filter, a limit, an idempotency key, a validation, or any mechanism whose absence is a defect. Delete or invert the mechanism in a scratch copy, run the test, and require it to fail. Repair or delete a test that passes both ways in the same change, because it reads as protection that is not there.

Every negative test has two properties:

- **It asserts the absence of the effect, not only the error.** A test that asserts only the status or error code passes against an implementation that rejects after the outbound request, the write or the minted token. Assert zero outbound requests, rows written, events emitted, files created, credentials minted and messages published, beside the refusal.
- **It asserts a control claimed at several layers separately at each layer, with the other layers neutralised.** One passing outer assertion hides every missing layer beneath it, and those layers run when the outer one is bypassed.

This property does not conflict with non-negotiable 2. **Remove the mechanism at one layer and run all the tests. If only that layer's test fails, the mechanisms are independent and every test stays. If all fail, they are one test written several times: keep one and delete the others.** `references/20-layers.md` *The rule against triplication* decides which one stays.

## Whether a test is owed

**A test is owed only for a decision this project makes, against a failure that can reach it.** Check both conditions for every candidate before you write it. Record a candidate that fails either condition under `Not written` with its reason, and do not write it, because an unowed test charges run and maintenance cost on every change and proves nothing about this project.

- **Owned decision.** No test is owed for language, runtime or framework behaviour; behaviour that a dependency's own suite proves (a kit such as alaa-go-chi, an `@alaa/*` package, a vendor library); generated code, which its generator's suite owns; or a declaration that a type, schema, lint or render gate already rejects. Record `covered by <owner> <suite>` instead. A conformance harness that its owner requires the consumer to run stays required, because it tests the consumer, not the owner.
- **Reachable failure.** A failure mode earns a test only when it cites one source: a path in this diff, or in the code it changes, that can produce it; an incident or defect on this surface; a dependency failure mode this deployment exercises; or a contract obligation the code must honour. Record a mode with no source as `not reachable: <reason>`.
- **A changed decision, not a changed file, is the reason for a test.**
- **Always owed, whatever the conditions above say:** every control `/alaa-security-review` names, every reported defect's regression test, every boundary that parses untrusted input (obligations 1, 6 and 9 in `references/60-coverage.md`), and the floor under *No shipped surface is exempt*. An upstream check never makes a mode unreachable across a trust boundary, because the downstream check runs when the upstream one is bypassed.

When a candidate is not owed a test, or a mode looks unreachable, read `references/90-test-economy.md` *Candidates that are not owed a test* for what the consumer tests instead.

Before you add a discretionary test, review, specialist, proof tool or gate beyond the declared cadence or repository requirements, state its concrete uncovered risk and why existing evidence is insufficient. Without that answer, do not add it. Required checks stay required. Record the answer in the plan's check list when a plan is admitted, and otherwise in the existing evidence owner.

## Non-negotiables

1. Every test names the failure it defends against, in its name or in one comment beside it, because nobody can safely delete or repair a test whose purpose is unknown.
2. Verify each behaviour at exactly one layer, chosen by the placement procedure in `references/20-layers.md`. Each extra layer adds a maintenance cost and a failure that carries no new information.
3. Use the real dependency whenever it runs deterministically inside the suite's time budget. Substitute a double only for a state the real dependency cannot be put into on demand, or for the time budget. Record the reason beside the double.
4. Bind every double that can drift by a parity suite that runs the same cases against both and requires identical results, because an unbound double keeps the suite green while production is broken.
5. Report every claim at the proof level that actually ran, never at the level it was meant to reach. A mislabelled level removes the reviewer's decision whether to re-run the claim.
6. Classify an intermittent failure as a product defect or a broken test before any other action on it. A blanket retry is never that action.
7. Name coverage obligations. Never set a percentage target, because executing code without asserting anything satisfies a percentage.
8. Derive the test list from the change's enumerated failure modes that pass *Whether a test is owed*. Add the happy path last, as a control that the failure tests fail for the reason claimed. Never start with it.
9. Report a check that was not observed to run as not run. An unexecuted check has no result, and reporting one invents evidence.
10. Make every test hermetic over its mutable state: it creates the data it asserts on, asserts only on that data, and leaves none behind. A failed reset or cleanup makes every later result over that state `CONTAMINATED`. Report it and stop the cases that depend on that state. A test that depends on another test's leftovers passes in one order only. Create expensive resettable infrastructure once per suite, package or worker, and share it. A test creates that infrastructure for itself only when creation is the behaviour under test. Before you create or share test infrastructure, or write or review a test over shared infrastructure, read `references/90-test-economy.md` *Setup once* for scopes and isolation.
11. No test synchronises on wall-clock sleeping. Inject time as a controllable clock, and wait on the condition with a bounded timeout. A sleeping test flakes on a loaded machine and charges its sleep on every run.
12. Choose check breadth from the changed inputs, the required proof and the uncovered risk. A new phase, agent or reviewer earns no rerun. Apply the validity and retest rules below.
13. Make every test this change adds or changes selectable by its topic and by its layer, through the runner's native selector. The topic is the behaviour or surface the test defends. Record in the repository which command selects which topic. A test reachable only through the whole-suite command makes every change pay for the whole suite.
14. Produce one build, compile, render or image per tree state and environment. Every lint, type, test and smoke step of that pass consumes its output, cache or image digest. Remove a step that rebuilds what an earlier step produced, or a separate compile that the test step already performs, because it charges the build again for no information.
15. A case failing never stops an independent case from running. A case that depends on another case's outcome or state declares that dependency. When the precondition fails, the case is reported `SKIPPED` naming that precondition. Never run it against the broken state. A suite whose first failure hides the rest costs one repair cycle per hidden failure.

## Designing the tests for a change

Do these steps in order. When you do a step, read the reference named beside it.

1. Enumerate the change's failure modes from the diff, once, shared with `/alaa-observability-soc` (`references/70-failure-mode-first.md`).
2. Decide which modes are owed a test, and record the others. Cite an existing topic test that already fails when the mode is injected, instead of writing a duplicate (`references/90-test-economy.md`).
3. Derive each owed mode's broken implementation (`references/10-what-makes-a-test.md`).
4. Place each test at one layer (`references/20-layers.md`).
5. Choose the doubles, and bind each one that can drift (`references/30-doubles.md`).
6. Give each test its topic and layer selector and shared setup, reusing existing fixtures first (`references/90-test-economy.md`).
7. Assign each claim's proof level, and confirm that this environment reaches it before you write the test (`references/40-proof-strength.md`).
8. Add the tests that an unmet named coverage obligation requires (`references/60-coverage.md`).
9. Add one happy-path test per behaviour, last. Confirm that each failure test fails when its mode is injected and passes otherwise (`references/70-failure-mode-first.md`).
10. Run the focused selectors, and report at the level reached, with the blocker for each level not reached (`references/80-evidence-and-reporting.md`).

## Proof levels

Six levels, ordered by what each rules out: 1 static, 2 unit or in-memory, 3 parity, 4 local smoke, 5 in-runtime service, 6 live-dependency. A level never substitutes for a higher one. Before you assign, report or review a proof level, read `references/40-proof-strength.md` for each definition, the minimum level per claim, and what to do when that level is unreachable.

## Scope tiers: how much of the suite runs, and when

A proof level says how strong one claim is. A **tier** says how much of the suite runs now. Keep the two separate: conflating them runs the whole suite four times against a tree that changed once.

Tiers choose check breadth, not review timing. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own the phase or final review cadence, the review authority and the scheduling. When you dispatch nested orchestration, pass it the workflow's whole-engagement boundary, so that it does not treat its own end as the final candidate.

| Tier | What runs | Who runs it | When |
|---|---|---|---|
| **Focused** | the smallest test, path or scenario that distinguishes the subtask's changed behavior from its plausible failure, plus the lint, type-check and build steps the touched files need | the implementing lane | subtask end under the declared cadence |
| **Task acceptance** | bounded acceptance selectors that combine the focused selectors of that task's subtasks, with still-valid coverage cited | the task owner | task end under the declared cadence |
| **Affected** | selectors of topics reachable from changed surfaces, including callers, shared fixtures and contract checks | the required boundary observer | in the final gate stage by default, or earlier when repository policy requires |
| **Exhaustive** | the whole suite and only the race, end-to-end and higher-level proofs the claims require | the required final observer | once on the whole engagement's final candidate, when required |

A subtask's short check adds no expensive setup and runs no full suite. When it needs infrastructure, it reuses reset-safe infrastructure that is already available. No fixed duration and no blanket container ban apply. At task acceptance, combine the focused selectors. Plan required broad coverage for the whole engagement's final candidate. Keep every stricter repository gate. Labels never narrow an actual command's scope.

**Run the exhaustive tier only on the tree that ships**, because on an intermediate tree its result expires before it is read and the shipped tree stays unobserved. A merge, rebase or cherry-pick after the run produces a tree that nothing has run against. A clean integration is no exception: no conflict proves only that no edit was needed, never that the combination was observed. Either integrate first and then run, or run again after integrating.

### A result stays valid until something named invalidates it

A recorded result stays citable for a later claim while **all four** of these are unchanged since it was observed:

- the tracked tree at the paths the check reads;
- the tool, runner, and dependency versions;
- the environment and service state the check depends on;
- the flags, seed, configuration, and working directory it ran under.

While all four hold, cite the result with its original command and timestamp, because a re-run adds no information at a real cost. When one of them changes, say which one, and re-run every result downstream of it. A required exhaustive tier on the final candidate is always fresh. A failed, flaky, contaminated, timed-out or environment-blocked result cannot discharge a required check.

After batch repair, select retests under `references/100-test-execution.md`. Reuse passing evidence only where its inputs, observer and freshness requirements still match.

A required final aggregate may discharge covered narrower checks only when the covered inputs, environment, flags and required observer match demonstrably. Cite its coverage instead of dispatching those checks again. Markdown files and templates may be checker inputs, so a documentation-only difference proves no equivalence. A phase transition, new agent or compaction alone invalidates nothing. Repair a defect and rerun its failing path. Never weaken assertions, suppress findings, lower standards or alter fixtures to conceal a failure. `references/80-evidence-and-reporting.md` separates a repaired input from an unchanged flaky rerun.

### A failing tier is classified before it is repaired

Classify first, then act, because a repair aimed at the wrong class turns a host problem into a product edit. Four classes stay separate:

- a defect in the product;
- a defect in the test harness, fixture or runner;
- a host-environment block: the shell, the container runtime, a permission, a missing executable or service;
- a contaminated tree, including a stale build or test cache.

`references/120-result-classification.md` owns the status vocabulary and the host sub-classes. This skill owns what each class licenses you to conclude. No class licenses reporting the change as passed.

A tier is never made to pass by deleting an assertion, widening a tolerance, adding a retry, skipping a case, or lowering a threshold. Report an unreachable tier as unreached, with its blocker named, under `references/80-evidence-and-reporting.md`.

## Executing checks

For any direct or delegated validation run, use the execution routes in `references/00-topic-map.md` before you choose commands, resources or result status. Runtime orchestration is optional. Role allocation, observer independence and the scheduling of phases and reviews stay with the caller's runtime orchestrator.

When you change this skill's execution policy or consumer routes, run `python3 scripts/check_execution_contracts.py` from this skill directory. It returns `0` clean, `1` findings, `2` unavailable input. Either nonzero blocks the affected claim. Preserve evidence. Repair within the caller's existing budget, or report blocked. Never treat `2` as a pass. This maintainer check does not run on ordinary application tasks. Source checks prove no live-agent compliance.

## Output contract

Return these fields, in this order, for every test design, test review or reported test run:

```text
Decision: pass | pass-with-actions | blocked
Scope: the change, and the surfaces and suites examined
Failure modes: mode -> the test that produces it -> layer -> proof level -> signal owner
Not written: candidate -> framework | owner suite <owner> <suite> | generated | declaration gate | not reachable: <reason>
Broken implementations: per test, the broken implementation it defends against
Layer placement: per behaviour, the layer and the components that had to be real
Doubles: per double, real|fake|stub|mock|spy, the reason for substituting, can-drift yes|no, and what binds it
Coverage obligations: each named obligation -> met by which test, or unmet
Selectors: per test, topic selector and layer selector
Shared setup: per expensive resource, scope (run | package | worker) and per-test isolation
Build reuse: per build, compile, render, or image -> the steps that consumed it
Evidence: per claim -> command run, working directory, proof level reached, observed outcome, artifact path
Tier: focused | task acceptance | affected | exhaustive -> run now, or cited from an earlier run with the four validity conditions named as still holding
Execution: check-list snapshot, expected, selected and executed cases, machine-readable reports, resources, and the collection, repair and retest state
Status: per command -> classification under references/120-result-classification.md; timing claims -> samples and limits under references/110-execution-resources.md
Flake: any intermittent result -> classified product defect | broken test -> action taken and owner
Gaps: claims with no test, levels not reached and the blocker, quarantined tests and their deadlines
```

## Stop conditions

Stop successfully when all of these hold:

- every enumerated failure mode has a test that fails when its mode is injected, or a `Not written` reason;
- every test this change adds or changes has a topic selector;
- every control has been proven by removal;
- every double that can drift is bound;
- every named coverage obligation is met or recorded as a gap;
- every reported claim carries an observed result at a stated level and tier;
- every required check has valid evidence, including a fresh exhaustive tier on the final candidate when required.

Stop and report blocked when any one of these holds:

- a behaviour cannot be placed at any layer, because no arrangement available here can produce its failure;
- a required proof level is unreachable, and the claim depends on what that level alone decides;
- an intermittent failure cannot be classified as a product or test defect after the procedure in `references/50-flake.md` has run to completion;
- a control cannot be proven by removal, because removing it breaks compilation of unrelated code, and no equivalent inversion exists; or
- a test the change requires cannot run, and the repository has no skip mechanism to record it.

## When NOT to use

- The question is framework idiom or assertion syntax: which matcher to call, how to name the file, which runner helper exists. The per-language skill owns it.
- No test is designed, reviewed or repaired, and no validation command, resource decision, timing comparison or result claim is involved.
- The question is fault injection, a security control, an envelope or code, or a Postman request test. `references/00-topic-map.md` *Owned by another skill* names each owner.

## Reference routing

Before you read any reference, read `references/00-topic-map.md`; it states when to read each one. Before you assert a contract value, design fault injection, test a security control or write a request test, read its *Owned by another skill* section. When you design, review or execute a test, a suite or a test plan, read `references/10-what-makes-a-test.md` *Anti-patterns*.
