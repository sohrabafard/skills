# Ent specialist delegation

Read this before dispatching or receiving an Ent specialist lane.
The canonical `SKILL.md` owns domain guidance, authority, validation, and failure limits; this reference owns delegation and grants no permissions.

## Route and bound the lane

When acting as an orchestrator, route Ent/PostgreSQL work to `alaa-ent-specialist`, including Ent setup/adoption, replacing handwritten SQL, design, implementation, diagnosis, and review.
Direct requests outside orchestration may use the skill inline.
The lead owns allocation, shared-file ownership, integration, and acceptance.
The specialist executes its assigned lane without further delegation or self-redispatch.
Review lanes are read-only; implementation lanes edit only authorized paths.
The specialist cannot independently approve its own changes or replace the lead's required gates.

Before dispatch, the lead resolves the installed role and canonical skill using [90-surfaces.md](90-surfaces.md).
A bundled template is not an installed role.
If the active orchestrator requires managed-role admission, satisfy its existing policy before dispatch; never silently substitute a generic role or modify registries, installers, or permissions.
The runtime policy owns model and effort selection; adapters pin neither.
Verify effective settings when that policy requires it, reporting unavailable identity as unknown.

## Dispatch contract

Pass only facts relevant to the lane:

- Outcome and mode: inspect, design, review, implement, or diagnose.
- Exact readable `skill_source` for `alaa-ent-go-orm-db/SKILL.md`, with accessible sibling resources.
- Checkout, baseline, owned paths, exclusions, and concurrent dependencies.
- Source files, query behavior, invariants, and known Go/Ent/PostgreSQL versions.
- Authorized effects and identified database target, distinguishing disposable fixtures from persistent data.
- Acceptance criteria and established check commands with working directories and timeouts.
- Missing evidence, constraints, and any lead review gate.

Exclude credentials and unrelated private inputs.
Use observed registry identifiers; namespaces can change them.
A dispatch summary does not replace reading the canonical source, and Claude's preload does not load all linked references.

## Execution and result

Read the skill and references triggered by the lane before dependent work; inspect owned context before editing.
Recommend additional work to the lead without expanding scope.
Complete safe independent work when a dependency blocks another part, identify the remainder, and apply the canonical failure budget.

Start the final report with exactly one line:

- `STATUS: COMPLETE` — scoped acceptance is evidenced.
- `STATUS: BLOCKED` — missing evidence, authority, a dependency, or a failed operation prevents required work.
- `STATUS: INCOMPLETE` — execution ended before acceptance without a resolved blocker.

Report only applicable items:

1. Outcome, changed or inspected paths, and canonical skill/references actually loaded.
2. Required query/index and projection decisions, evidence, and assumptions.
3. Findings: location, severity (`blocker`, `major`, `minor`, `nit`), confidence (0–1), effect, and remedy.
4. Checks run: command, working directory, result, and evidence location; distinguish static reasoning from measured behavior.
5. Unassessed scope, unrun checks, residual risks, and actions awaiting the lead or user.

Keep requested work distinct from observed results; omit empty sections.
Stop after the lane report. The lead decides integration and any next lane.
