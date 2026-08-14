---
name: alaa-testing-strategy
description: "Test design doctrine for services that must not fail: what makes a test a test rather than a replay of the happy path, which layer a behaviour belongs at, when to fake or stub or use the real dependency, the six proof levels and which one a claim requires, and telling a flaky test from an intermittent product defect. Use when writing, reviewing, or repairing tests; deciding where a test belongs or whether a double is honest; when a suite is slow, flaky, or green against broken code; when a route, consumer, or job has no test; and before reporting any check as passed. Do not use for framework idiom and assertion syntax, which are the per-language skills and /golang-testing. Route fault injection to /alaa-reliability-sla; security controls to /alaa-security-review; envelopes and codes to /alaa-services-contract; Postman request tests to /alaa-postman-collections; command execution to /alaa-cc-orchestrator."
---

# Alaa Testing Strategy

Decide what to test, where to test it, what to substitute for a real dependency, how strong the resulting proof is, and what a reviewer may accept as evidence — so every service in the fleet ships a test suite of the same shape. Uniformity is the deliverable: a suite whose shape differs per service can be read only by whoever wrote it, so no reviewer can tell a covered service from an uncovered one, and the fleet's real coverage becomes unknowable at exactly the scale where it matters.

This skill owns the decision. It owns no framework, no assertion syntax, no fixture library, and no Ala value. Companion skills are written `/name` for Claude Code and `$name` for Codex; both forms appear at every call site.

## When this applies

Any change that adds or alters a behaviour, a control, a contract, a dependency call, a stored effect, or a failure path; any work on a test suite itself — writing, reviewing, repairing, quarantining, deleting, or speeding up; any diagnosis of a test that fails intermittently or passes against broken code; and any moment before a check is reported as passed.

It does not apply to a change that alters no behaviour and no test: a comment, a formatting pass, a rename with no call-site semantics, or a docs-only edit.

**No shipped surface is exempt.** Every route, queue consumer, job, scheduled task, and published request carries at least one test meeting the core rule below. The surface that issues credentials is the least exempt of all: a validator run over this platform's own API collection found 73 requests with no test at all, including the entire Auth folder — the requests that issue tokens asserted nothing. That is the failure this skill exists to prevent, because a credential surface is the one place where silent breakage grants access rather than removing it.

**A repository's own validation-policy file outranks this skill inside that repository.** Where a repository states which checks gate a change, at which moment, and what may be cited instead of re-run, that file decides and this skill supplies only what it leaves open. What follows is the fleet default for a repository that has not written its own.

## The core rule: what makes a test a test

**A test names the broken implementation it defends against. A test that still passes against a plausible broken implementation is not a test — it is an execution of the code under a different name, and its green result is worse than no test, because a reviewer counts it as coverage and stops looking.**

Derive that broken implementation from the code under test in four steps:

1. **Name the decision the code makes.** Every unit under test decides something (a branch, a comparison, a filter, a limit), transforms something, or causes an effect. Write it as one sentence. Code you cannot write that sentence for is code whose test you cannot design yet — get the sentence first.
2. **Write the plausible wrong version.** Not a crash and not nonsense: the version a competent engineer ships by mistake. The check omitted, the comparison inverted, the tenant filter dropped, the configured default returned, the first row returned, the input echoed back unchanged, the error swallowed and success returned, the effect applied twice, the effect silently skipped, or the inner layer trusting an outer layer that no longer checks. `references/10-what-makes-a-test.md` carries the catalogue and the mapping from code shape to its characteristic break.
3. **Ask whether the candidate assertion fails against that version.** If it passes, the assertion measures something else — usually that the code is reachable — and the real test has not been written yet.
4. **Prove it by removal, for every control.** For an authentication check, an authorization check, a tenancy filter, a limit, an idempotency key, a validation, or any mechanism whose absence is a defect: delete or invert the mechanism in a scratch copy, run the test, and require it to fail. A test that passes both ways is repaired or deleted in the same change, because it will be read as protection that is not there.

Two properties every negative test carries:

- **It asserts the absence of the effect, not only the presence of the error.** A rejection test asserting only the status or error code passes against an implementation that rejects *after* doing the work — after the outbound request, after the write, after the token was minted. Assert zero outbound requests, zero rows written, zero events emitted, alongside the refusal.
- **A control claimed at more than one layer is asserted separately at each layer, with the other layers neutralised.** One passing assertion at the outermost layer hides every missing layer beneath it, and the layers beneath are the ones that run when the outer one is bypassed.

That second property and the rule against testing one behaviour at three layers do not conflict, and the discriminator is observable: **remove the mechanism at one layer and run all three tests. If only that layer's test fails, they are three tests for three independent mechanisms and all three stay. If all three fail, they are one test written three times, and two are deleted.**

## Non-negotiables

1. Every test names the failure it defends against, in the test's own name or in one comment beside it. A reader who cannot tell what a test protects can neither judge that deleting it is safe nor repair it when it breaks, so it is kept forever and skipped when inconvenient.
2. Each behaviour is verified at exactly one layer, chosen by the placement procedure in `references/20-layers.md`. The same behaviour verified at three layers buys one confidence and charges three maintenance obligations on every future change to it, and the second and third failures carry no information because all three fail for the same cause.
3. The real dependency is used whenever it runs deterministically inside the suite's time budget. A substitution is made for exactly one of two reasons — a state the real dependency cannot be put into on demand, or the suite's time budget — and which of the two applies is recorded beside the double.
4. Every double that can drift from the real implementation is bound by a parity suite that runs the same cases against both and requires identical results. An unbound double eventually asserts a contract nobody implements, and the suite then stays green while production is broken.
5. Every claim is reported at the proof level that actually ran, never at the level it was meant to reach. The level is what lets a reviewer decide whether to re-run a claim; a mislabelled level removes that decision.
6. A test that fails intermittently is classified as a product defect or a broken test before any other action is taken on it. A blanket retry is never that action.
7. Coverage obligations are named, never expressed as a percentage target. A percentage is satisfied by executing code without asserting anything.
8. The test list is derived from the enumerated failure modes of the change; the happy path is added last, as a control proving the failure tests fail for the reason claimed, never as the starting point.
9. A check that was not observed to run is reported as not run. An unexecuted check has no result, and reporting one invents evidence.
10. Every test is hermetic: it creates the state it needs, asserts only on state it created, and leaves none behind. A test depending on another test's leftovers passes in one order and fails in another, and the order is not part of anyone's contract.
11. No test synchronises on wall-clock sleeping. Time is injected as a controllable clock, and waiting is done on the condition the test is waiting for, with a bounded timeout. A sleeping test flakes on a loaded machine and charges its sleep on every run forever.
12. Breadth is earned by a change in the tree, never by a change of phase, agent, or reviewer. A result whose four validity conditions still hold is cited, not re-run, and the exhaustive tier runs once, fresh, on the final candidate. Re-running a heavy suite against an unchanged tree buys no confidence and produces the worst evidence available, because a warm cache and a warm environment are hardest to tell apart from a real pass.

## Designing the tests for a change

Walk this in order. Each step names the reference that owns its detail.

1. **Enumerate the failure modes the change introduces**, from the diff rather than from the ticket. This enumeration is shared with `/alaa-observability-soc` (`$alaa-observability-soc`) and is produced once, not twice. (`references/70-failure-mode-first.md`)
2. **Write the broken implementation for each mode**, by the four-step derivation above. (`references/10-what-makes-a-test.md`)
3. **Place each test at one layer**, by naming the smallest set of components that must be real for that failure to be producible. (`references/20-layers.md`)
4. **Decide the doubles**, and for each one whether it can drift and what binds it if it can. (`references/30-doubles.md`)
5. **Assign the proof level each claim requires**, and check that the level is reachable in this environment before writing the test that assumes it. (`references/40-proof-strength.md`)
6. **Check the named coverage obligations** and add the tests any unmet obligation requires. (`references/60-coverage.md`)
7. **Add one happy-path test per behaviour**, last, and confirm each failure test fails when its mode is injected and passes otherwise. (`references/10-what-makes-a-test.md`)
8. **Run, and report at the level reached**, with the blocker named for every claim whose level was not reachable. (`references/80-evidence-and-reporting.md`)

## Proof levels

Six levels, named so a claim's strength can be stated in one word across every service and language in the fleet. The ordering is by what a level can rule out; a level never substitutes for a higher one.

1. **Static proof** — inspection only: the code, the configuration, the types, a linter, a schema validation. Proves an artifact says something. Proves nothing about behaviour.
2. **Unit or in-memory proof** — the behaviour executed in process against in-memory or embedded substitutes: an embedded database standing in for the production engine, an in-memory broker, a controllable clock. Proves the logic. Proves nothing that the substituted engine decides.
3. **Parity proof** — one suite run against the double and against the real implementation, with identical results required. Proves the double is honest, and proves nothing else.
4. **Local smoke proof** — the built artifact started in its real container or process form and exercised from outside itself over its real interface. Proves it boots, wires, and answers.
5. **In-runtime service proof** — the service running inside the composed local runtime with its declared dependencies present, exercised through its real transport. Proves the behaviour in the shape it is deployed in.
6. **Live-dependency proof** — the behaviour exercised against the real production-grade dependency engine, with real drivers, transactions, ordering, and delivery. Proves what only that engine decides.

`references/40-proof-strength.md` owns the mapping from a claim to the minimum level that supports it, and the rule for a level that cannot be reached in this environment.

## Scope tiers: how much of the suite runs, and when

A proof level says how strong one claim is. A **tier** says how much of the suite has earned the right to run at this moment. The two are independent, and conflating them is what produces a pipeline that runs the whole suite four times against a tree that changed once.

Three tiers. Each has exactly one owner and exactly one moment, and no tier is run by the author of the change it is judging except the first.

| Tier | What runs | Who runs it | When |
|---|---|---|---|
| **Focused** | the tests naming this change's failure modes, plus lint, type, and build checks scoped to the touched files | the lane that wrote the change | at the end of every subtask, before that subtask is reported complete |
| **Affected** | every suite reachable from the changed surfaces — callers, shared fixtures, the contract tests of the touched surface — plus the acceptance criteria this phase claims | an authority other than the lane that wrote the change | once per phase, after the phase's lanes are reconciled |
| **Exhaustive** | the whole suite under its normal configuration, then the race, end-to-end, and highest-level proofs the claims require | an authority other than any implementing lane | exactly once, on the final candidate tree, after every lane and every fix has landed |

**The exhaustive tier is not an early-warning system.** Run on an intermediate tree it observes a combination that is about to change, so its result expires before it is read while its cost is charged in full — and the tree it was meant to judge still goes unobserved. Its whole value is that it runs on the tree that ships.

**It runs on the tree that will land, and integration is what moves that target.** Merging, rebasing, or cherry-picking anything into the branch after the run produces a tree nothing has run against. A clean integration is no exception, and this is the case that gets missed: no conflict means no edit was needed to combine the two sides, never that the combination was observed. Two orderings satisfy the invariant — integrate first and then run, or run again after integrating — and a run that ends without one of them has shipped an unobserved tree.

### A result stays valid until something named invalidates it

A recorded result remains citable evidence for a later claim while **all four** of these are unchanged since it was observed: the tracked tree at the paths the check reads; the tool, runner, and dependency versions; the environment and service state the check depends on; and the flags, seed, configuration, and working directory it ran under. While all four hold, cite the result with its original command and timestamp. Re-running it produces no new information and its cost is real.

When one of them changes, say which one, and re-run every result downstream of it. Two results are never reused whatever the four conditions say: the exhaustive tier on the final candidate, which is always fresh; and any result classified `FLAKY`, `CONTAMINATED`, `TIMEOUT`, or environment-blocked, which carries no evidence in either direction.

### A failing tier is classified before it is repaired

Classify first, then act, because a repair applied to the wrong class is how a host-environment problem becomes an edit to the product. Four classes stay separate: a defect in the product; a defect in the test harness, fixture, or runner; a host-environment block — the shell, the container runtime, a permission, a missing executable or service; and a contaminated tree, including stale build or test cache. `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) `references/failure-taxonomy.md` owns the status vocabulary and the host sub-classes; this skill owns what each class licenses you to conclude, and no class licenses reporting the change as passed.

A tier is never made to pass by deleting an assertion, widening a tolerance, adding a retry, skipping a case, or lowering a threshold. An unreachable tier is reported unreached with its blocker named, under `references/80-evidence-and-reporting.md`.

## Output contract

Return these fields, in this order, for every test design, test review, or reported test run:

```text
Decision: pass | pass-with-actions | blocked
Scope: the change, and the surfaces and suites examined
Failure modes: mode -> the test that produces it -> layer -> proof level -> signal owner
Broken implementations: per test, the broken implementation it defends against
Layer placement: per behaviour, the layer and the components that had to be real
Doubles: per double, real|fake|stub|mock|spy, the reason for substituting, can-drift yes|no, and what binds it
Coverage obligations: each named obligation -> met by which test, or unmet
Evidence: per claim -> command run, working directory, proof level reached, observed outcome, artifact path
Tier: focused | affected | exhaustive -> run now, or cited from an earlier run with the four validity conditions named as still holding
Flake: any intermittent result -> classified product defect | broken test -> action taken and owner
Gaps: claims with no test, levels not reached and the blocker, quarantined tests and their deadlines
```

## Stop conditions

Stop successfully when every enumerated failure mode has a test that fails when its mode is injected, every control has been proven by removal, every double that can drift is bound, every named coverage obligation is met or recorded as a gap, every reported claim carries an observed result at a stated level and tier, and the exhaustive tier has run once on the final candidate tree.

Stop and report blocked when: a behaviour cannot be placed at any layer because its failure is not producible in any arrangement available here; a required proof level is unreachable and the claim depends on what that level alone decides; an intermittent failure cannot be classified as product or test defect after the procedure in `references/50-flake.md` has been run to completion; a control cannot be proven by removal because removing it breaks compilation of unrelated code, and no equivalent inversion exists; or a test the change requires cannot be run and the repository has no skip mechanism to record it.

## When NOT to use

- The question is framework idiom or assertion syntax: which matcher to call, how to name the file, which
  helper the runner already provides. The per-language skill owns that.
- No test is being written, reviewed, repaired, or claimed as passing.
- The question is fault injection, a security control, an envelope or code, or a Postman request test. The
  routing table below names each owner.

## Reference routing

Read only the files whose stated condition the task meets. Loading the whole tree means the task was not scoped.

- `references/10-what-makes-a-test.md` — when writing or reviewing any individual test, and whenever an existing test's value is in question.
- `references/20-layers.md` — when deciding where a behaviour is tested, when a suite is slow, or when the same behaviour appears to be tested more than once.
- `references/30-doubles.md` — when substituting anything for a real dependency, when a double already exists, or when a suite passes while an integration breaks.
- `references/40-proof-strength.md` — before reporting any claim as validated, and whenever an environment cannot reach the level a claim needs.
- `references/50-flake.md` — when any test has produced two different outcomes on the same code, and when a retry is being proposed anywhere.
- `references/60-coverage.md` — when coverage is being measured, gated, or cited as evidence, and when deciding what still needs a test.
- `references/70-failure-mode-first.md` — at the start of every change, before any test is written.
- `references/80-evidence-and-reporting.md` — when reporting a test result, when reviewing someone else's reported result, when a test cannot be run at all, and when deciding whether an earlier result may be cited instead of re-run.

## What this skill does not own

- `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns fault injection doctrine, the failure modes worth injecting at a dependency boundary, the per-mechanism evidence table, load testing at saturation, production experiments, and the rule that an untested degraded path is a broken path — `references/80-verification.md`. This skill owns where those tests sit in the plan, at which layer, and at which proof level.
- `/alaa-security-review` (`$alaa-security-review`) owns which controls must be security-tested and its own minimum negative tests for credentials and cryptography — `references/50-credentials-and-cryptography.md`. This skill generalises the method those tests are built on; it does not restate them and it names no security control.
- `/alaa-services-contract` (`$alaa-services-contract`) owns every envelope, code, header, field name, and value a contract test asserts against. Assert what that skill declares and report drift, rather than asserting the drift.
- `/alaa-postman-collections` (`$alaa-postman-collections`) owns API-level request tests, their five minimum assertions, examples, and scripts. This skill owns the layer that work sits at and the rule that no request is exempt.
- `/alaa-observability-soc` (`$alaa-observability-soc`) owns the failure-mode enumeration table and the signal, query, and alert each mode needs — `references/10-signal-model.md`. This skill consumes the same enumeration to derive tests; neither skill maintains a second list.
- `/alaa-controlled-ops` (`$alaa-controlled-ops`) owns its own package and adopter release gates and its boundary-check script. This skill owns the proof-level vocabulary those gates report in.
- The per-language skills and the vendored `/golang-testing` (`$golang-testing`) own framework idiom, assertion syntax, fixture and mock libraries, table-driven form, and runner flags. This skill owns the decision; it names no framework construct.
- The `alaa-verifier` role in `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) owns command execution, resource policy, low-priority runners, artifact directories, and the status vocabulary a run is reported in — `references/failure-taxonomy.md`. This skill owns what each status licenses a reader to conclude, which tier had the right to run, and whether an earlier result is still citable.
- `/alaa-prompting-guide` (`$alaa-prompting-guide`) owns every model and effort question. This skill names no model.

## Anti-patterns

- asserting only the status or error code on a rejection path, which passes against an implementation that rejects after doing the work;
- one assertion at the outermost layer standing in for a control implemented at three, which reports two missing layers as present;
- the same behaviour tested at unit, integration, and end-to-end level, which buys one confidence and charges three maintenance obligations;
- a mock asserting the sequence of calls where the outcome was observable, which fails on every behaviour-preserving refactor and trains the team to update tests without reading them;
- a hand-written double of a dependency nobody owns, with no parity suite, which encodes a belief about the vendor rather than the vendor's behaviour;
- reporting an in-memory or embedded-engine result as though the production engine had run, which is the specific way a query, migration, index, constraint, or isolation defect reaches production;
- retrying a failing test until it passes, which converts an intermittent product defect into an invisible one;
- quarantining a test with no owner and no deadline, which is deletion with extra steps and a lingering claim of coverage;
- a coverage percentage cited as validation, when the number rises by executing code that asserts nothing;
- writing the happy path first and stopping there, which produces a suite that proves only that the routes are routed;
- a test that sleeps to wait for a condition, which is a flake on a loaded machine and a permanent tax on every run;
- re-running the full suite, the race detector, or the acceptance set against a tree that has not changed since the last run, which charges the whole cost for no new information and produces the pass that is hardest to distinguish from a cached one;
- an implementing lane running the exhaustive tier on its own work, which is both the wrong authority and the wrong moment;
- repairing the product in response to a shell, container-runtime, permission, or stale-cache failure that was never classified;
- deleting or weakening an assertion so a test can run in a constrained environment, instead of recording the level not reached and the blocker.
