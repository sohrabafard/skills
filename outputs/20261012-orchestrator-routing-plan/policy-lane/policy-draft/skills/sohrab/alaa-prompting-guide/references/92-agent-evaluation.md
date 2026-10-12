# Evaluating agent profiles

Use `assets/evals/agent-comparisons.json` for eight representative comparisons. Each includes
a concrete prompt, supplied source fixtures, acceptance criteria, forbidden actions, candidate,
comparator, and two independent repetitions. The reusable corpus stays `unrun`; results are
separate evidence. It proves test design, never runtime availability or model quality.

## Historical comparison isolation

The original comparison corpus and policy under `assets/evals/history/20261009/` are dated historical-only evidence. Validate their manifest with `python scripts/check_agent_evals.py --history-manifest assets/evals/history/20261009/manifest.json` from this skill directory. This path checks original hashes/provenance and historical support; it cannot combine with active `--corpus`, `--results` or `--self-test`, authorize ordinary task allocation, or reenable old Sol. Active redesigned comparisons remain separate unrun hypotheses.

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

When testing task selection, use `assets/evals/allocation-cases.json` and the separate reviewer-only `assets/evals/allocation-oracle.json`. These inputs test R1-R15 decisions, not worker quality. The corpus has two neutral variants per case and two repetitions. Give an allocator only neutral inputs; never expose the oracle or another run's answer. Observe two fresh runs per authorized available allocator configuration with the same loaded contracts, authority and inputs; record unavailable configurations as blocked or unassessed. No child worker, paid comparison, installation or configuration mutation is authorized.

From this skill directory run `python scripts/check_allocation_evals.py` for corpus/oracle structure. Add `--self-test` after checker changes, `--results <path>` for records, and `--require-live` with results for complete nonsynthetic observations and independent grading. `--corpus <path>` and `--oracle <path>` select explicit files. `--probe-input codex` or `--probe-input claude-code` prints neutral cases and the response contract, excludes the oracle, and performs no inference or writes. Exit 0 is clean, 1 findings, 2 unavailable proof; either nonzero blocks the affected claim. Follow the authorized failure/retry limit rather than changing controls or checks to pass.

Results use `schema_version: 1`, `purpose: allocation-results`, boolean `synthetic`/`complete`, `corpus_sha256`, `oracle_sha256`, `configurations`, and `runs`. Each configuration records `id`, `runtime`, `allocator_requested`, `allocator_effective`, `allocator_observed`, `control_evidence`, and `loaded_contracts` entries with repository-relative path/SHA-256. Keep actual allocator controls separate from simulated scenario controls and proposed worker controls.

Every declared configuration represents each case/variant/repetition, including unrun/blocked rows. Runs carry `case`, `variant`, `configuration`, `runtime`, `repetition`, `status`, `input_sha256`, and a blocker when blocked. Completed rows add `response`, `output_evidence`, `output_sha256`, `reviewer`, `independent_review`, `criterion_verdicts`, `forbidden_effects_observed`, `elapsed_seconds`, `usage`, and `correction_count`; unobservable counters stay unknown.

The response records `action`, `role` matching the neutral task authority, explicit `proposed_worker` model/effort or null, `model_reason`, `effort_reason`, `fit` with verdict/evidence for every named predicate, `alternatives` with failed predicate or stronger evidence, `admission`, `continuity`, and `compression` with preserved-invariant verdicts. Decision-only probes set `worker_dispatched: false` and leave `worker_effective`/`worker_observed` unknown. A simulated pin/availability answer proves no actual child realization.

An independent reviewer grades captured decisions against the withheld oracle and checks linked evidence truth. Concrete allocator-control mismatch or unknown effective controls prevents a live pass. Unknown observed serving identity requires separate control evidence and stays unknown. Synthetic records prove only consumer discrimination; live sampled allocation answers prove neither worker dispatch/quality, actual scenario availability, universal suitability, cost nor savings. Keep those claims separate from source checks and controlled worker comparisons above.
