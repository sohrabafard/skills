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

The architecture case compares Fable explicitly at shared effort; it creates no default role
or fallback. Haiku needs a separately designed comparison because its missing effort control
prevents a model-only comparison at a shared effort.

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
  and `evidence`; controls contain resolved full IDs or null, with force recording the
  resolved forced target, not the raw boolean environment switch;
- `fallback`: kind none/safety/overload/unknown, boolean `disclosed`, and
  `safeguards_preserved: true`; a non-none kind requires evidence and cannot pass the
  requested configuration. Record actual safety-policy violations as failed work; never
  turn off safeguards to make this contract pass.

For a completed record, require a sourced model minimum Claude Code version in the canonical
policy. Candidate records additionally satisfy the role's minimum; use the higher requirement.
Comparator records require their own model minimum, including models with no assigned role.
A missing model minimum permits unrun or blocked records, not an activation or calibration
claim. A below-minimum runtime cannot support a completed record; report it as blocked.

Resolution checks apply to ordinary custom agents only, excluding forks, inherit, unresolved
aliases and provider substitutions. Those need separately verified host-resolution evidence;
the checker is not a runtime emulator. Unknown observed identity can support a configuration
claim only with separate `configuration_control_evidence`; it remains unknown. A concrete
mismatch cannot pass or verify the requested pair. Unknown usage is never zero cost.

## Calibration gate

The policy's evaluated status requires an existing repository-relative result JSON that
passes this contract, is complete and nonsynthetic, and contains two accepted candidate runs
matching the profile's requested and observed pair. No unrelated file or unknown identity
can calibrate a profile. Roles without representative scenarios remain unrun until the corpus
and its acceptance coverage are extended. The checker validates records; an independent
reviewer must establish that linked evidence is truthful and applicable.

Run `python scripts/check_claude_agent_evals.py --self-test` after checker changes. Fixtures
exercise identity uncertainty, old/new precedence, force overrides and fallback disclosure
without executing models. Exit 0 is clean, 1 findings, 2 unavailable proof; either nonzero
blocks the affected gate. No fixture or source pass proves live runtime behavior.
