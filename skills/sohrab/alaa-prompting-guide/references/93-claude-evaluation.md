# Evaluating Claude profiles

The `assets/evals/claude-agent-comparisons.json` corpus carries eight concrete tasks,
fixtures, acceptance criteria and forbidden actions. Each compares two configurations twice in fresh contexts. Every case stays unrun; results belong in separate evidence records.
The corpus is test design, not model-quality evidence. The GPT corpus remains independent.

## Execution contract

Before an authorized comparison, run `python scripts/check_claude_agent_evals.py` from this
skill directory. Then verify target CLI, provider/account access, model mapping, overrides,
effort caps and effective permissions using `references/41-claude-code-runtime-features.md`.
Stop a comparison whose required pair cannot be established; do not silently downgrade.
Source checks do not authorize installation, configuration changes, paid model calls or benchmarks.

Use separate disposable inputs and fresh context per run, identical prompts/tools/authority
and acceptance criteria, and change only the declared factor. Preserve outputs and tool
evidence. A distinct reviewer grades every criterion and forbidden action; models do not
approve their own result. Reject configurations that violate scope, fabricate success or
miss a blocking defect. Compare cost only among quality-passing configurations. Two runs
are a bounded initial comparison, never proof of universal superiority.

The architecture case compares an explicitly selected Fable task pair with Opus at shared effort; the corpus does not prove that routing choice or authorize fallback. Current Haiku 5.5 has effort-enabled candidate pairs. Historical Haiku 4.5 needs a separate control-regime comparison.

## Result records

Validate records with `python scripts/check_claude_agent_evals.py --results <path>`.
Top-level fields: integer `schema_version: 1`, matching `policy_version`, boolean `complete`
and `synthetic`, and `runs`. Represent all 32 scenario/configuration/repetition keys; retain
missing work as `unrun`, blocked work as `blocked` with its reason. Each row records the
requested pair. A completed row also requires:

- `status` passed/failed; `output_evidence`, `reviewer`, `independent_review: true`,
  `execution_surface`, `account_type`, and `fixture_revision`;
- `criterion_verdicts` (pass/fail/unknown per criterion), `forbidden_actions_observed`,
  boolean `configuration_verified`, and `observed` model/effort (unknown when unavailable);
- `elapsed_seconds`, `usage`, and `correction_count`, nonnegative numbers or unknown;
- `resolution`: exact `claude_code_version`, `model_controls` with invocation/frontmatter/
  environment/parent/force values, `selected_source`, `provider_and_caps_checked: true`,
  `effort_controls` with invocation/frontmatter/environment/parent, `selected_effort_source`,
  `non_fork: true`, and `evidence`; controls contain resolved full IDs/efforts or null, with force recording the
  resolved forced target, not the raw boolean environment switch;
- `fallback`: kind none/safety/overload/unknown, boolean `disclosed`, and
  `safeguards_preserved: true`; a non-none kind requires evidence and cannot pass the
  requested configuration. Record actual safety-policy violations as failed work; never
  turn off safeguards to make this contract pass.

Completed records require a sourced model minimum Claude Code version in the canonical
policy. Both candidate and comparator additionally require the dynamic non-fork invocation-effort boundary, and explicit invocation model AND effort. Roles carry no model minimum or effort default.
A missing model minimum permits unrun or blocked records, not an activation or calibration
claim. A below-minimum runtime cannot support a completed record; report it as blocked.

Resolution checks apply to ordinary custom agents only, excluding forks, inherit, unresolved
aliases and provider substitutions. Those need separately verified host-resolution evidence;
the checker is not a runtime emulator. Unknown observed identity can support a configuration
claim only with separate `configuration_control_evidence`; it remains unknown. A concrete
mismatch cannot pass or verify the requested pair. Unknown usage is never zero cost.

## Calibration gate

Task-pair calibration requires complete nonsynthetic result evidence and two accepted candidate runs matching the explicit requested and observed pair for the scenario/role. Unknown identity cannot calibrate that pair. Calibration of one task never assigns a role-wide default. The checker validates records; an independent reviewer establishes whether linked evidence is truthful and applicable.

Run `python scripts/check_claude_agent_evals.py --self-test` after checker changes. Fixtures
exercise identity uncertainty, old/new precedence, force overrides and fallback disclosure
without executing models. Exit 0 is clean, 1 findings, 2 unavailable proof; either nonzero
blocks the affected gate. No fixture or source pass proves live runtime behavior.
