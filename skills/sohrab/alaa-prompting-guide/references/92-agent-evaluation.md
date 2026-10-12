# Evaluating agent profiles

Use `assets/evals/agent-comparisons.json` for eight representative comparisons. Each includes
a concrete prompt, supplied source fixtures, acceptance criteria, forbidden actions, candidate,
comparator, and two independent repetitions. The reusable corpus stays `unrun`; results are
separate evidence. It proves test design, never runtime availability or model quality.

## Historical comparison isolation

The original corpus/policy under `assets/evals/history/20261009/` are historical-only. Here run `python scripts/check_agent_evals.py --history-manifest assets/evals/history/20261009/manifest.json` for hash integrity, provenance-field syntax and historical support. Verify source identity independently. It cannot combine with active `--corpus`, `--results` or `--self-test`, authorize ordinary allocation or reenable old Sol. Active redesigned comparisons remain separate unrun hypotheses.

## Execution

1. Run `python scripts/check_agent_evals.py` from this skill directory. Nonzero means the
   corpus is invalid or unreadable; fix the reported cause before evaluation.
2. Verify model and effort selection on the intended runtime and account. Stop the affected
   comparison if the runtime rejects a pair or cannot establish its effective configuration.
   Do not downgrade silently. Repository files, desktop tool inventories, and CLI availability
   are separate evidence surfaces.
3. Materialize each scenario's supplied files in a separate disposable directory per run.
   Start a fresh context with the same role contract, prompt, inputs, tools, permissions, and
   resource limits for both configurations. Never use an evaluated answer as another run's input.
4. Run both configurations twice. Change only the factor named by their difference. Use model-neutral roles with explicit controls on a verified compatible surface. Stale
   custom pins can override spawn settings; an available exact verified realization or
   a blocked affected comparison is required. Source-prompt runs do not prove installed
   custom-agent activation. Do not modify installed agents to enable an experiment implicitly.
5. Have an independent reviewer assess the captured outputs against each acceptance criterion
   and forbidden action. The implementer or evaluated model does not grade its own result.
   Scope violation, fabricated success, or missed blocking defect rejects that configuration
   for the scenario; cost comparisons include only quality-passing configurations.

No paid API client or automatic installation is part of this corpus. Use the current host's
authorized execution path, and stop after its bounded failure/retry policy is exhausted.

## Evidence record

Optionally validate a result matrix with `python scripts/check_agent_evals.py --results <path>`.
Its top-level fields are `schema_version: 1`, `complete` (boolean), and `runs`. Each run is
keyed by `scenario`, `configuration` (`candidate` or `comparator`), and `repetition`;
`requested` contains model and effort. All 32 keys must exist, with missing execution explicitly
`unrun`. For each intended run record:

- scenario ID, repetition (1 or 2), candidate/comparator, policy version and fixture revision;
- requested model/effort, observed model/effort or `unknown`, and execution surface/account type;
- status `passed`, `failed`, `blocked`, or `unrun`; output/evidence path and exact blocker when any;
- criterion verdicts with supporting output excerpts, forbidden actions observed, reviewer verdict;
- correction or redispatch count, elapsed time, and observed usage or `unknown`.

Missing runtime metadata is not a match. Missing price or token telemetry is not zero cost.
Record configuration-control evidence separately from self-reported model identity. Do not label
a selected task pair calibrated until the comparison's required runs and independent grading are
complete with preserved evidence. Keep the role/task/pair and evidence together in the result record; no role-wide calibrated default follows.

## Interpretation

Keep repository validation, runtime selection/activation, and comparative quality conclusions
separate. A validator pass supports structural consistency. A runtime smoke proves only the
tested surface. Two repetitions are a bounded initial comparison, not statistical proof of
universal model superiority. Re-run affected comparisons when the role contract, fixtures,
runtime behavior, or policy changes enough to invalidate the previous result.

Completed result rows also require `output_evidence`, `reviewer`, `execution_surface`,
`fixture_revision`, `criterion_verdicts` (one pass/fail/unknown per criterion),
`forbidden_actions_observed`, `configuration_verified`, and `observed` model/effort.
For passed and failed rows alike, `forbidden_actions_observed` is a list of nonempty strings
(empty when none occurred), and `configuration_verified` is boolean. A concrete observed
model or effort mismatch forbids a pass or a verified-configuration claim; record it as a
failed run with `configuration_verified: false`. Unknown identity stays `unknown`; verifying
that configuration requires a separate nonempty `configuration_control_evidence` reference
to host resolution or equivalent control evidence, not the agent's self-report.
A pass requires all criteria passed, no forbidden action, and verified configuration.
The checker validates record completeness; the independent reviewer must verify evidence truth.

## Allocation-only observations

For task-selection tests use `assets/evals/allocation-cases.json` and separate reviewer-only `assets/evals/allocation-oracle.json`: R1-R15 decisions, not worker quality. Each case has two neutral variants and two repetitions. Give allocators only neutral inputs, never the oracle or another run's answer. Observe two fresh runs per authorized available allocator configuration with identical loaded contracts, authority and inputs; record unavailable configurations blocked/unassessed. This authorizes no worker dispatch, paid comparison, installation or configuration mutation.

Here run `python scripts/check_allocation_evals.py` for corpus/oracle structure. Add `--self-test` after checker changes, `--results <path>` for records, and `--require-live` with results for complete nonsynthetic observations/independent grading. `--corpus <path>`/`--oracle <path>` select files. `--probe-input codex` or `--probe-input claude-code` prints neutral cases/response contract without oracle, inference or writes. Exit 0 clean, 1 findings, 2 unavailable proof; either nonzero blocks the affected claim. Follow authorized failure/retry limits; never alter controls/checks to pass.

Results: `schema_version: 1`, `purpose: allocation-results`, boolean `synthetic`/`complete`, `corpus_sha256`, `oracle_sha256`, `configurations`, `runs`. Configurations: `id`, `runtime`, `allocator_requested`, `allocator_effective`, `allocator_observed`, `control_evidence`, `loaded_contracts` (repository-relative path/SHA-256). Separate actual allocator controls, simulated scenario controls and proposed worker controls.

Represent every declared configuration's case/variant/repetition, including unrun/blocked work. Runs: `case`, `variant`, `configuration`, `runtime`, `repetition`, `status`, `input_sha256`; blocked rows require `blocker`. Completed rows add `response`, `output_evidence`, `output_sha256`, `reviewer`, `independent_review`, `criterion_verdicts`, `forbidden_effects_observed`, `elapsed_seconds`, `usage`, `correction_count`. Unobservable counters stay unknown.

Responses: `action`, `role` matching neutral task authority, explicit `proposed_worker` model/effort or null, `model_reason`, `effort_reason`, `fit` verdict/evidence per named predicate, `alternatives` with failed predicate or stronger evidence, `admission`, `continuity`, `compression` with preserved-invariant verdicts. Decision-only probes require `worker_dispatched: false`, unknown `worker_effective`/`worker_observed`. Simulated pin/availability answers prove no child realization.

An independent reviewer grades decisions against the withheld oracle and checks linked evidence truth. Concrete allocator-control mismatch or unknown effective controls prevents a live pass. Unknown serving identity stays unknown and needs separate control evidence. Synthetic records prove consumer discrimination only; sampled live answers prove no worker dispatch/quality, actual scenario availability, universal suitability, cost or savings. Keep source checks, allocation observations and worker comparisons distinct.
