# Evaluating agent profiles

Use `assets/evals/agent-comparisons.json` for eight representative comparisons. Each includes
a concrete prompt, supplied source fixtures, acceptance criteria, forbidden actions, candidate,
comparator, and two independent repetitions. The reusable corpus stays `unrun`; results are
separate evidence. It proves test design, never runtime availability or model quality.

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
4. Run both configurations twice. Change only the factor named by their difference. Custom
   agent pins override spawn settings: use explicitly configured isolated evaluation profiles
   when authorized, or mark the comparison blocked. Source-prompt runs do not prove installed
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
a selected profile calibrated until the comparison's required runs and independent grading are
complete with preserved evidence. Policy `evaluation_evidence` points to that report.

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
