# Workflow Prompt Pack - {{task}}

- Plan: `{{plan_path}}`
- Verification status: {{verification_status}}
- Verified on: {{verified_on}}
- Verification sources: {{verification_sources}}
- Implementer runtime/model: {{implementer_runtime}} / {{implementer_model}}
- Independent reviewer runtime/model: {{reviewer_runtime}} / {{reviewer_model}}

Before use, load the runtime-correct prompting guide and re-check official documentation when any value above is unresolved or stale.

## Implementer

**Outcome:** Execute the selected phase in `{{plan_path}}` and leave repository behavior, tests, documentation, and workflow status consistent.

**Read first:** Repository instructions, the plan, and every source named by the selected phase.

**Scope:** Change only the phase-owned surfaces. Preserve unrelated work. Delegate only independent, disjoint work or high-volume context isolation; the main agent owns integration.

**Validation:** Run the plan's affected commands, repair in-scope failures, and record concise evidence.

**Done:** The phase acceptance criteria pass and status reflects verified reality.

**Blocked:** Record the exact blocker, attempted safe checks, and next executable action; do not claim completion.

## Independent reviewer

**Outcome:** Independently review the implemented phase for correctness, production risk, contract drift, and missing evidence.

**Read first:** Repository instructions, `{{plan_path}}`, the resulting diff/artifacts, and affected tests.

**Scope:** Report confirmed findings first. Separate out-of-scope recommendations. Do not inherit the implementer's conclusions.

**Validation:** Re-run or inspect the smallest decisive gates and cite exact evidence.

**Done:** Return findings by severity, a verdict, and validation status.

**Blocked:** Name unavailable evidence and the smallest action needed to obtain it.
