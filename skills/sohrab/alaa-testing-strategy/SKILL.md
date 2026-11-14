---
name: alaa-testing-strategy
description: "Test design and execution doctrine: owed tests, layers, doubles, proof strength, selectors, shared setup, build reuse, flake diagnosis, check collection, batch repair, result classification, CPU budgets and comparative timing. Use to write, review, repair or run tests and validation commands; investigate slow, flaky or falsely green suites; choose check breadth or resources; or report a check result, directly or through either runtime. Do not use for framework syntax, owned by per-language skills and /golang-testing; fault injection belongs to /alaa-reliability-sla, security controls to /alaa-security-review, contract values to /alaa-services-contract and Postman tests to /alaa-postman-collections. Runtime orchestrators own allocation, independence and the scheduling of phases and reviews; this skill requires no orchestrator."
---

# Alaa Testing Strategy

Decide what to test, where to test it, what to substitute for a real dependency, how strong the resulting proof is, and what a reviewer may accept as evidence, so every service in the fleet ships a test suite of the same shape. Uniformity is the deliverable. A suite whose shape differs per service can be read only by whoever wrote it, so no reviewer can tell a covered service from an uncovered one, and the fleet's real coverage becomes unknowable at exactly the scale where it matters.

This skill owns test design and generic execution policy, usable directly or through either runtime. It owns no framework syntax, fixture library or Ala value. Activating it installs nothing and grants no environment-mutation authority.

## When this applies

This skill applies to:

- any change that adds or alters a behaviour, a control, a contract, a dependency call, a stored effect, or a failure path;
- any work on a test suite itself: writing, reviewing, repairing, quarantining, deleting, or speeding up;
- any diagnosis of a test that fails intermittently or passes against broken code;
- any selection, execution or reporting of validation commands, CPU-heavy checks or comparative timing.

Test-design obligations do not apply to a change that alters no behaviour and no test: a comment, formatting pass, rename with no call-site semantics or docs-only edit. Execution and reporting policy still applies when that change runs validation.

**No shipped surface is exempt.** Every route, queue consumer, job, scheduled task, and published request this project ships carries at least one test meeting the core rule below. Decide under *Whether a test is owed* which behaviour behind it is owed a test. The surface that issues credentials is the least exempt of all, because a credential surface is the one place where silent breakage grants access rather than removing it.

**A repository's own validation-policy file outranks this skill inside that repository.** Where a repository states which checks gate a change, at which moment, and what may be cited instead of re-run, that file decides. This skill supplies only what it leaves open. What follows is the fleet default for a repository that has not written its own.

## The core rule: what makes a test a test

**A test names the broken implementation it defends against. A test that still passes against a plausible broken implementation is not a test. It is an execution of the code under a different name. Its green result is worse than no test, because a reviewer counts it as coverage and stops looking.**

Derive that broken implementation from the code under test in four steps:

1. **Name the decision the code makes.** Every unit under test decides something (a branch, a comparison, a filter, a limit), transforms something, or causes an effect. Write the decision as one sentence. If you cannot write that sentence, you cannot design the test yet. Get the sentence first.
2. **Write the plausible wrong version.** Write the version a competent engineer ships by mistake. It is not a crash and not nonsense. Examples: the check omitted, the comparison inverted, the tenant filter dropped, the configured default returned, the first row returned, the input echoed back unchanged, the error swallowed and success returned, the effect applied twice, the effect silently skipped, or the inner layer trusting an outer layer that no longer checks. `references/10-what-makes-a-test.md` carries the catalogue and the mapping from code shape to its characteristic break.
3. **Ask whether the candidate assertion fails against that version.** If it passes, the assertion measures something else, usually that the code is reachable. The real test has not been written yet.
4. **Prove it by removal, for every control.** Apply this to an authentication check, an authorization check, a tenancy filter, a limit, an idempotency key, a validation, or any mechanism whose absence is a defect. Delete or invert the mechanism in a scratch copy. Run the test. Require it to fail. Repair or delete a test that passes both ways in the same change, because it will be read as protection that is not there.

Two properties every negative test carries:

- **It asserts the absence of the effect, not only the presence of the error.** A rejection test that asserts only the status or error code passes against an implementation that rejects *after* doing the work: after the outbound request, after the write, after the token was minted. Assert zero outbound requests, zero rows written and zero events emitted, alongside the refusal.
- **A control claimed at more than one layer is asserted separately at each layer, with the other layers neutralised.** One passing assertion at the outermost layer hides every missing layer beneath it. The layers beneath are the ones that run when the outer one is bypassed.

That second property and the rule against testing one behaviour at three layers do not conflict. The discriminator is observable: **remove the mechanism at one layer and run all three tests. If only that layer's test fails, they are three tests for three independent mechanisms and all three stay. If all three fail, they are one test written three times, and two are deleted.**

## Whether a test is owed

**A test is owed only for a decision this project makes, against a failure that can reach it.** Check both conditions for every candidate before writing it. Record a candidate that fails either condition under `Not written` with its reason, and do not write it. An unowed test charges its run and maintenance cost on every future change while proving nothing about this project.

- **Owned decision.** No test is owed for:
  - language, runtime, or framework behaviour;
  - behaviour a dependency's own suite proves, such as a shared kit like alaa-go-chi, an `@alaa/*` package, or a vendor library;
  - generated code, which its generator's suite owns;
  - a declaration that a type, schema, lint, or render gate already rejects when it is wrong.

  The consumer tests only its own use of the dependency: the configuration it chooses, the inputs it passes, the policy it applies, and wiring that can be wrong. Record the owner instead: `covered by <owner> <suite>`. A conformance harness its owner requires the consumer to run stays required, because it tests the consumer's conformance, not the owner.
- **Reachable failure.** A failure mode earns a test only when it cites one reachability source:
  - a path in this diff, or in the code it changes, that can produce it;
  - an incident or defect on this surface;
  - a dependency failure mode this deployment exercises;
  - a contract obligation the code must honour.

  Record a mode with no source as `not reachable: <reason>`. Examples: input already refused by an owned, tested check upstream, a dependency this path never calls, a configuration that never ships.
- **A changed file is not a reason for a test; a changed decision is.**
- **Always owed, whatever the conditions above say:** every control `/alaa-security-review` names, every reported defect's regression test, and every boundary where untrusted input is parsed — obligations 1, 6 and 9 in `references/60-coverage.md` — plus the per-surface floor under *No shipped surface is exempt*. A check upstream never makes a mode unreachable across a trust boundary, because the downstream check is what runs when the upstream one is bypassed.

When a candidate is not owed a test, read `references/90-test-economy.md` for what the consumer tests instead.

Before adding a discretionary test, review, specialist, proof tool or gate beyond the declared cadence or repository requirements, state its concrete uncovered risk and why existing evidence is insufficient. Without that answer, do not add it. Required checks remain required. Record the answer in the plan's check list when a plan is admitted, and otherwise in the existing evidence owner.

## Non-negotiables

1. Every test names the failure it defends against, in the test's own name or in one comment beside it. A reader who cannot tell what a test protects can neither judge that deleting it is safe nor repair it when it breaks, so that test is kept forever and skipped when inconvenient.
2. Each behaviour is verified at exactly one layer, chosen by the placement procedure in `references/20-layers.md`. The same behaviour verified at three layers buys one confidence and charges three maintenance obligations on every future change to it. The second and third failures carry no information, because all three fail for the same cause.
3. Use the real dependency whenever it runs deterministically inside the suite's time budget. Substitute a double only for one of these two reasons: a state the real dependency cannot be put into on demand, or the suite's time budget. Record beside the double which reason applies.
4. Bind every double that can drift from the real implementation by a parity suite. The suite runs the same cases against both and requires identical results. An unbound double eventually asserts a contract nobody implements. The suite then stays green while production is broken.
5. Report every claim at the proof level that actually ran, never at the level it was meant to reach. The level lets a reviewer decide whether to re-run a claim. A mislabelled level removes that decision.
6. Classify a test that fails intermittently as a product defect or a broken test before any other action is taken on it. A blanket retry is never that action.
7. Name coverage obligations. Never express them as a percentage target. A percentage is satisfied by executing code without asserting anything.
8. Derive the test list from the enumerated failure modes of the change that pass *Whether a test is owed*. Add the happy path last, as a control proving the failure tests fail for the reason claimed. Never start with it.
9. Report a check that was not observed to run as not run. An unexecuted check has no result, and reporting one invents evidence.
10. Make every test hermetic over its mutable state: it creates the data it asserts on, asserts only on that data, and leaves none behind. A failed reset or cleanup makes every later result over that state `CONTAMINATED`. Report it and stop the cases that depend on that state. A test that depends on another test's leftovers passes in one order and fails in another. The order is not part of anyone's contract. Create expensive resettable infrastructure once per suite, package, or worker, and share it. A test creates that infrastructure for itself only when creation is the behaviour under test. Before you create or share test infrastructure, or write or review a test that runs over shared infrastructure, read `references/90-test-economy.md` *Setup once*. It defines that infrastructure, its scopes and the isolation of each test over it.
11. No test synchronises on wall-clock sleeping. Inject time as a controllable clock. Wait on the condition the test is waiting for, with a bounded timeout. A sleeping test flakes on a loaded machine and charges its sleep on every run forever.
12. Choose check breadth from the changed inputs, the required proof and the uncovered risk. A new phase, agent or reviewer earns no rerun. Apply the evidence validity and retest rules below.
13. Make every test this change adds or changes selectable by its topic and by its layer, through the runner's native selector. The topic is the behaviour or surface the test defends. Record in the repository which command selects which topic. A test reachable only through the whole-suite command forces every change to pay for the whole suite, because the focused tier cannot select it.
14. Produce one build, compile, render, or image per tree state and environment. Every lint, type, test, and smoke step of that pass consumes its output, cache, or image digest. Remove a step that rebuilds what an earlier step of the same pass produced, or a separate compile that the test step already performs, because such a step charges the build again for no new information.
15. A case failing never stops an independent case from running. A case that depends on another case's outcome or state declares that dependency. When the precondition fails, the case is reported `SKIPPED` naming that precondition. Never run it against the broken state. A suite whose first failure hides the rest costs one repair cycle per hidden failure.

## Designing the tests for a change

Walk this in order. Each step names the reference that owns its detail.

1. **Enumerate the failure modes the change introduces**, from the diff rather than from the ticket. This enumeration is shared with `/alaa-observability-soc` and is produced once, not twice. (`references/70-failure-mode-first.md`)
2. **Decide whether each mode is owed a test**, under *Whether a test is owed*, and record every mode that is not. Before writing an owed test, check the topic's existing tests. Cite one that already fails when the mode is injected. Do not duplicate it. (`references/90-test-economy.md`)
3. **Write the broken implementation for each owed mode**, by the four-step derivation above. (`references/10-what-makes-a-test.md`)
4. **Place each test at one layer**, by naming the smallest set of components that must be real for that failure to be producible. (`references/20-layers.md`)
5. **Decide the doubles**, and for each one whether it can drift and what binds it if it can. (`references/30-doubles.md`)
6. **Give each test its topic and layer selector and its shared setup**, reusing the suite's existing fixtures before creating one. (`references/90-test-economy.md`)
7. **Assign the proof level each claim requires**, and check that the level is reachable in this environment before writing the test that assumes it. (`references/40-proof-strength.md`)
8. **Check the named coverage obligations** and add the tests any unmet obligation requires. (`references/60-coverage.md`)
9. **Add one happy-path test per behaviour**, last, and confirm each failure test fails when its mode is injected and passes otherwise. (`references/10-what-makes-a-test.md`)
10. **Run the focused selectors, and report at the level reached**, with the blocker named for every claim whose level was not reachable. (`references/80-evidence-and-reporting.md`)

## Proof levels

Six levels, ordered by what each can rule out: 1 static, 2 unit or in-memory, 3 parity, 4 local smoke, 5 in-runtime service, 6 live-dependency. A level never substitutes for a higher one. Before you assign, report or review a proof level, read `references/40-proof-strength.md`. It defines each level, maps a claim to the minimum level that supports it, and states what to do when that level cannot be reached in this environment.

## Scope tiers: how much of the suite runs, and when

A proof level says how strong one claim is. A **tier** says how much of the suite has earned the right to run at this moment. The two are independent. Conflating them produces a pipeline that runs the whole suite four times against a tree that changed once.

These scope definitions choose check breadth, not review timing. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own the declared phase or final review cadence, the review authority and the scheduling. When you dispatch nested orchestration, pass it the workflow's whole-engagement boundary, so the nested run does not treat its own end as the final candidate.

| Tier | What runs | Who runs it | When |
|---|---|---|---|
| **Focused** | the smallest test, path or scenario that distinguishes the subtask's changed behavior from its plausible failure, plus the lint, type-check and build steps the touched files need | the implementing lane | subtask end under the declared cadence |
| **Task acceptance** | bounded acceptance selectors that combine the focused selectors of that task's subtasks, with still-valid coverage cited | the task owner | task end under the declared cadence |
| **Affected** | selectors of topics reachable from changed surfaces, including callers, shared fixtures and contract checks | the required boundary observer | in the final gate stage by default, or earlier when repository policy requires |
| **Exhaustive** | the whole suite and only the race, end-to-end and higher-level proofs the claims require | independent final authority | once on the whole engagement's final candidate, when required |

A subtask's short check adds no expensive setup and runs no full suite. When it needs infrastructure, it reuses reset-safe infrastructure that is already available. This rule sets no fixed duration and no blanket ban on containers. At task acceptance, combine the focused selectors. Plan required broad coverage for the whole engagement's final candidate. Keep every stricter repository gate. Labels never narrow an actual command's scope.

**The exhaustive tier is not an early-warning system.** Run on an intermediate tree, it observes a combination that is about to change. Its result expires before it is read, while its cost is charged in full. The tree it was meant to judge still goes unobserved. Its whole value is that it runs on the tree that ships.

**It runs on the tree that will land, and integration is what moves that target.** Merging, rebasing, or cherry-picking anything into the branch after the run produces a tree nothing has run against. A clean integration is no exception. This is the case that gets missed. No conflict means no edit was needed to combine the two sides. It never means the combination was observed. Two orderings satisfy the invariant: integrate first and then run, or run again after integrating. A run that ends without one of them has shipped an unobserved tree.

### A result stays valid until something named invalidates it

A recorded result remains citable evidence for a later claim while **all four** of these are unchanged since it was observed:

- the tracked tree at the paths the check reads;
- the tool, runner, and dependency versions;
- the environment and service state the check depends on;
- the flags, seed, configuration, and working directory it ran under.

While all four hold, cite the result with its original command and timestamp. Re-running it produces no new information, and its cost is real.

When one of them changes, say which one, and re-run every result downstream of it. A required exhaustive tier on the final candidate is always fresh. A failed, flaky, contaminated, timed-out or environment-blocked result cannot discharge a required check.

After batch repair, apply `references/100-test-execution.md` to select retests. Reuse passing evidence only where its inputs, observer and freshness requirements still match.

A required final aggregate may discharge covered narrower checks only when the covered inputs, environment, flags and required observer match demonstrably. Cite its coverage instead of dispatching those checks again. Markdown files and templates may be checker inputs, so a documentation-only difference proves no equivalence. A phase transition, new agent or compaction alone invalidates nothing. Repair a defect and rerun its failing path. Never weaken assertions, suppress findings, lower standards or alter fixtures to conceal a failure. `references/80-evidence-and-reporting.md` distinguishes a repaired input from an unchanged flaky rerun.

### A failing tier is classified before it is repaired

Classify first, then act. A repair applied to the wrong class is how a host-environment problem becomes an edit to the product. Four classes stay separate:

- a defect in the product;
- a defect in the test harness, fixture, or runner;
- a host-environment block: the shell, the container runtime, a permission, a missing executable or service;
- a contaminated tree, including stale build or test cache.

`references/120-result-classification.md` owns the status vocabulary and the host sub-classes. This skill owns what each class licenses you to conclude. No class licenses reporting the change as passed.

A tier is never made to pass by deleting an assertion, widening a tolerance, adding a retry, skipping a case, or lowering a threshold. Report an unreachable tier as unreached, with its blocker named, under `references/80-evidence-and-reporting.md`.

## Executing checks

For any direct or delegated validation run, use the execution routes in `references/00-topic-map.md` before choosing commands, resources or result status. Runtime orchestration is optional. Role allocation, observer independence and the scheduling of phases and reviews remain with the caller's runtime orchestrator.

When changing this skill's execution policy or consumer routes, run `python3 scripts/check_execution_contracts.py` from this skill directory. It returns `0` clean, `1` findings, `2` unavailable input. Either nonzero blocks the affected claim. Preserve evidence. Repair within the caller's existing budget, or report blocked. Never treat `2` as a pass. This maintainer check does not run on ordinary application tasks. Source checks prove no live-agent compliance.

## Output contract

Return these fields, in this order, for every test design, test review, or reported test run:

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

- every enumerated failure mode has either a test that fails when its mode is injected or a `Not written` reason;
- every test this change adds or changes has a topic selector;
- every control has been proven by removal;
- every double that can drift is bound;
- every named coverage obligation is met or recorded as a gap;
- every reported claim carries an observed result at a stated level and tier;
- every required check has valid evidence, including a fresh exhaustive tier on the final candidate when required.

Stop and report blocked when any one of these holds:

- a behaviour cannot be placed at any layer because its failure is not producible in any arrangement available here;
- a required proof level is unreachable and the claim depends on what that level alone decides;
- an intermittent failure cannot be classified as product or test defect after the procedure in `references/50-flake.md` has been run to completion;
- a control cannot be proven by removal because removing it breaks compilation of unrelated code, and no equivalent inversion exists; or
- a test the change requires cannot be run and the repository has no skip mechanism to record it.

## When NOT to use

- The question is framework idiom or assertion syntax: which matcher to call, how to name the file, which
  helper the runner already provides. The per-language skill owns that.
- No test is being designed, reviewed or repaired, and no validation command, resource decision, timing comparison or result claim is involved.
- The question is fault injection, a security control, an envelope or code, or a Postman request test.
  `references/00-topic-map.md` *Owned by another skill* names each owner.

## Reference routing

Before reading any reference, read `references/00-topic-map.md`; it names the condition under which each reference is read. Before you assert a contract value, design fault injection, test a security control or write a request test, read its *Owned by another skill* section. When you design, review or execute a test, a suite or a test plan, read `references/10-what-makes-a-test.md` *Anti-patterns*.
