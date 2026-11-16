# Routing Matrix

Spawn only agents that materially reduce uncertainty or enforce a required authority boundary. The catalog is a menu, not a role quota.

## Default roles

- Non-trivial repository change: an implementation profile from Implementation routing below, or the Ent specialist route for Ent-owned work.
- Independent checks that a decision or floor in `verification-and-gates.md` requires: `alaa-verifier`.
- Independent ship-quality judgment that a decision or floor requires: `alaa-reviewer`.
- Behavior, API, configuration or operations changed: `alaa-documenter`, after review.

## Specification and evidence agents

| Role | Spawn when any of these holds | Skip when |
|---|---|---|
| `alaa-spec-analyst` | The request uses quality language that is not yet checkable ("make it robust"). Two competent readers would define "done" differently. A contract is implied but never stated. The goal bundles several outcomes that need separating before lanes can be drawn. | The request names the change, the files and the observable result. |
| `alaa-explorer` | The owner module or execution path is unclear. The task crosses unfamiliar packages or services. Tests and local conventions are not known. The lead would otherwise guess file scope. | Current context establishes the relevant paths and contracts. |
| `alaa-researcher` | A prior session, decision, file or shared contract must be recalled and verified. An external API, library or tool version controls correctness. Official docs or standards are needed. Sources disagree or current behavior may have changed. The task asks for an evidence-based comparison. | |
| `alaa-test-strategist` | Acceptance criteria are easy to satisfy superficially. Legacy behavior has weak coverage. Concurrency, retry, idempotency, migration, security or failure-mode testing matters. Test layer selection and flake control need design. | |

Name `/alaa-testing-strategy` in the test-strategist dispatch. Read it yourself when you decide a test layer, a double, a proof level or a scope tier.

## Planning profile selection

Before planning, separate missing facts from coupled design judgment, and retrieve or clarify the missing facts.

1. Use `alaa-planner` when scope, contracts and constraints are clear. Use `alaa-planner-high` when forming the plan requires resolving interacting uncertainties.
2. Select the planning model AND effort for the planning task through All-role task allocation below.
3. The lead may plan inline only when its effective controls match that recorded pair. Otherwise dispatch a compatible registered planner.
4. A planner draft is advisory. The lead ratifies it and persists the durable plan.
5. Before worker allocation, finalize the lane outcomes, scopes, exclusions, dependencies, decisions, and failure and invariant reasoning.

## Batch allocation

After workflow tasks, dependencies and consolidation decisions are finalized, allocate the ready plan once through All-role task allocation below.

- Before dispatch, record each role with its explicit model AND effort: evidence, planning, implementation, verification, review, specialist and documentation lanes.
- Compare the ready tasks so that no task inherits the complexity of the whole goal.
- Reopen allocation only for remaining work, at a material scope change or a fix follow-up. Reuse unchanged allocations and evidence.

## All-role task allocation

This orchestrator decides the task complexity, priority, model and effort for EVERY role. Before allocation, read `alaa-prompting-guide references/90-model-selection.md` and its `references/50-effort-and-thinking.md`; they inform the decision and assign no default pair to a role.

Role identities are compatibility identities: a role name, including a legacy ID named for a model or effort, selects neither control. Every pair preserves the role's tools, skills, verdicts and independent gates.

1. **Ground the task.** Establish each task's scope, acceptance, settled and open decisions, and remaining reasoning need. Retrieve missing facts. Repair context, specification or tool failures before you attribute a shortfall to model capacity.
2. **Set the priority.** Use the balanced default priority; priority is not an effort value. Deviate only on an explicit user priority or model choice, or a documented task-based reason. Role title, sensitivity, duration, whole-goal labels and a second independent lens alone never select a frontier or stronger model. Independence comes from context and authority, not model diversity.
3. **Select the cheapest suitable pair.**
   1. Evaluate the cheapest eligible supported available model AND effort pair for EVERY role, the rule-writer included.
   2. A task has bounded suitability only when it has all of these: an explicit outcome, a finite named scope, grounded local contracts/known invariants, a known pattern or causal path, settled cross-boundary decisions, bounded local discretion and a discriminating check.
   3. Non-bug semantic work needs no reproduced failure. The mechanical branch keeps its own predicates below.
   4. Select the least costly suitable available pair. Depart from it only on an explicit user choice or recorded task evidence. Apply no quotas.
   5. Justify model and effort separately, each from the remaining reasoning need, the priority, current official guidance and applicable prior evidence.
   6. When you reject a cheaper pair, record the actual failed fit predicate or stronger task-specific evidence. Titles, volume, priority labels and whole-goal complexity are not failed predicates.
   7. Select directly. Use no mandatory trial ladder, synthetic experiment or replay.
4. **Admit an exceptional model only on evidence.** On ANY role, an exceptional model needs one of these:
   - an exact official recommendation for the task and priority that the canonical owner supports, recorded with the remaining reasoning need and the rejected cheaper or decomposed alternatives;
   - applicable documented inadequacy of the high-effort workhorse, established after context, specification and tool correction and after decomposition was considered;
   - an explicit user selection.

   A repairable defect or an imagined insufficiency is not model inadequacy. A model mention alone is not a selection instruction.
5. **Record the allocation** once, in the workflow plan, or in the dispatch's `<task_controls>` when no durable plan is admitted: the role, the scope and workload class, a priority that departs from the default with its reason, the selected model AND effort, and the admission with its evidence. A bounded standalone delegation needs no full pipeline and no workflow artifact solely for model selection.
6. **Realize the pair.** Before EVERY dispatch, follow `model-effort-policy.md`. Unknown serving identity is a reporting limit, not evidence of a control mismatch and not a reason for paid calibration.

## Ent specialist route

For Ent or PostgreSQL work owned by /alaa-ent-go-orm-db, select `alaa-ent-specialist` for the affected lane through the catalog's External companion admission. Resolve its lane mode through `alaa-ent-go-orm-db references/85-specialist-delegation.md`. A review lane is read-only and independent of the work it reviews. Preserve the inherited cadence and the required correctness, verification and specialist gates.

## Implementation routing

Choose directly from the completed lane record; no mandatory sequence of attempts applies. Copy the admission predicates you verified for the selected route into the dispatch; the lane rechecks them before editing. These routes classify workload fit only. Apply All-role task allocation separately.

Select the exact mechanical branch of `alaa-implementer-haiku` only when ALL of these are recorded before dispatch:

- the exact transformation and its exclusions;
- a finite, explicitly enumerated scope of existing files;
- the expected result;
- a settled design with no semantic discretion;
- a known pattern;
- cheap discriminating checks that detect wrong, incomplete or out-of-scope results.

File count alone neither qualifies nor disqualifies a task. Ambiguous matches, undefined scope or design changes fail admission.

Select the bounded semantic branch of `alaa-implementer-haiku` only when the plan records explicit expected behavior, a settled local causal path or pattern, named scope, known invariants, bounded decisions and discriminating behavior/regression checks. Use `alaa-implementer-haiku-high` for longer or stricter work that satisfies the same predicates. Interacting design, or unresolved decisions about cross-boundary contracts, trust, shared state or consistency, select a workhorse route below.

These routes are uncalibrated workload admissions. Priority or a model preference never waives fit or independent gates. If fit ceases, stop dependent work, preserve valid edits and return the remaining scope for reclassification. Require no lightweight trial and no replay of completed work. No route expands command authority.

- `alaa-implementer`: everyday grounded coding, features, local refactoring or debugging with known patterns, explicit contracts and acceptance, and bounded local decisions. The architecture need not prescribe every edit.
- `alaa-implementer-sonnet-high`: harder or longer grounded work with bounded decisions and local failure reasoning.
- `alaa-implementer-opus`: materially coupled unresolved system decisions beyond the bounded routes.
- `alaa-implementer-opus-high`: interacting unresolved design decisions and demanding system reasoning.

The legacy exceptional ID `alaa-implementer-fable` remains an implementation authority identity. Apply the exceptional model admission above only when the selected task pair is exceptional, and record its evidence before dispatch. Return missing facts, unavailable tools and unresolved product intent to their owners. An unresolved decision alone never establishes model inadequacy.

### Stack-bound roles

A stack-bound role is an implementation authority identity bound to one stack family. It carries the owning skills of that stack and changes no tool, verdict or independent gate. Select it when both of these hold:

- Every owned file belongs to one stack family, apart from incidental files of another family that the lane record lists by path. Decide the family from the repository manifests and the owned file types, never from the repository name.
- The lane is not admitted to the mechanical or the bounded semantic branch above.

| Owned files | Role |
|---|---|
| PHP or Laravel code, migrations and their tests | `alaa-implementer-laravel` |
| Vue or Quasar frontend code in TypeScript or JavaScript, and its tests | `alaa-implementer-frontend` |
| Go code and its tests, except work on the Ent specialist route | `alaa-implementer-go` |
| Dockerfile, Compose or Swarm stack, Helm chart, Kubernetes manifest, CI pipeline, HAProxy configuration, Ansible file, Makefile or shell script | `alaa-implementer-infra` |

- The stack-bound role replaces `alaa-implementer`, `alaa-implementer-sonnet-high`, `alaa-implementer-opus`, `alaa-implementer-opus-high` and `alaa-implementer-fable`. An admitted exceptional pair runs on the stack-bound role.
- Record the lane's workload class in the allocation record: everyday, harder or longer, materially coupled, or interacting design. For a stack-bound lane the class informs the task pair and selects no role identity.
- Split a lane that owns files of two families when the parts are independent. Otherwise, and for a stack with no bound role, dispatch the generic role for its workload class and name each stack's skills in the dispatch as calls.
- When the selected stack-bound role is not available in this session, do not block the lane for that reason. Record the generic role for the workload class as the registered profile, with the unavailable stack-bound role as its reason. Dispatch it and name the stack's skills in the dispatch as calls. This fallback replaces only the role identity; the pair rules still apply.

### Reassignment

Reassess remaining work only at the initial assignment, a material scope change or a fix follow-up. Before you replace a writer, apply the stopped-writer recovery in `alaa-workflow references/workspace-and-integration.md` and retire its assignment. Hand off the remaining scope, acceptance criteria and evidence. Never overlap writers or replay completed work.

## Correctness review depth

Select the deep route when review involves complex interactions among subsystems, a broad failure impact, or documented insufficiency of the standard review. Both routes use `alaa-reviewer`; select its model AND effort through All-role task allocation. Record the trigger and select one profile per scope. When you replace an insufficient standard review, retire that assignment and pass its evidence to the deep route. Never run the two reviews concurrently.

## Specialist gates

`verification-and-gates.md` decides whether a holding trigger dispatches its gate, and schedules the judgment at the declared review boundary.

| Gate | Trigger |
|---|---|
| `alaa-instruction-reviewer` | Prompts, skills, agent definitions or repository instructions change behavior, authority, routing or wording that controls another agent. This gate does not replace correctness review of scripts or generated artifacts. |
| `alaa-architecture-critic` | Cross-cutting design: public contracts, service boundaries, consistency models, concurrency, caching semantics, distributed workflows. Also the three `/alaa-system-design` triggers: the change moves which component writes a piece of data, adds or removes a dependency between two components, or creates a new deployable unit. Any of the three requires a design pass in Stage A even when no contract shape changes. Record the trigger and the design before implementation. Skip it for a local bug fix whose contract and ownership are established. |
| `alaa-api-contract-reviewer` | A public HTTP or RPC endpoint, event or message schema, shared DTO, SDK surface or persisted serialization format changes shape. A contract change discovered during implementation reopens the affected plan and gate. Skip it when the change is internal to one module and no consumer outside it can observe the difference. |
| `alaa-security-reviewer` | Authentication or authorization, tokens and sessions, secrets, untrusted inputs, upload and download, query or command construction, serialization, webhooks, payments, cryptography, tenant isolation or privileged operations. |
| `alaa-migration-guardian` | DDL, constraints, defaults, nullability, index creation, data backfills, format transforms, cleanup or deletion, compatibility windows or production data movement. |
| `alaa-dependency-auditor` | A dependency is added, upgraded, removed or replaced, a lockfile changes outside a scoped upgrade lane, or a transitive tree shifts materially. |
| `alaa-accessibility-reviewer` | New or changed user-visible interface: components, forms, dialogs, navigation, tables, and any flow a user completes with a keyboard or a screen reader. |
| `alaa-browser-qa` | User-visible browser behavior. Require an exact URL, environment and scenario. |
| `alaa-performance-profiler` | Only a measurable question with a comparable baseline and a budget; never generic optimization advice. `/alaa-algorithms-data-structures` owns the budget. State it during implementation planning when the change adds a loop, query, fan-out, batch, export or in-memory collection that grows with tenants, rows, history or events. Report a growing path that reaches this gate with no stated bound as a missing budget; do not measure it into one. |
| `alaa-observability-reviewer` | Async jobs, queues, retries, external service calls, failure and degraded paths, production critical flows or new operational states. |
| `alaa-release-guardian` | CI/CD, Docker or container, package, lock or version, configuration and environment, feature flags, deployment order, health checks, startup and shutdown, release notes or rollback changes. |
| `alaa-adversarial-reviewer` | Only when the change is irreversible or has high blast radius (production data movement, auth or tenancy boundaries, a public contract break, deployment topology), or when `alaa-reviewer` and a specialist return conflicting verdicts that repository evidence does not settle. |

Where two gates overlap, each keeps its own question:

- The API contract reviewer judges whether the transition is safe for existing consumers; the architecture critic judges whether the design is sound.
- The dependency auditor asks whether a dependency is safe to depend on; the release guardian asks whether the change deploys and operates cleanly.
- The accessibility reviewer judges use without a mouse or sight; browser QA gathers functional evidence that a flow works.

The adversarial reviewer runs after the reviewer and any specialist gates, against the same complete change. Its output is a report to the user, not another fix cycle, because a fresh adversarial pass always finds something. A substantive Ent review finding that contradicts correctness approval on the same candidate is a conflicting specialist judgment when repository evidence cannot settle it. A blocked or incomplete Ent status alone is not.

## Failure routing

- Test failures, including clear single-owner failures: collect and route one combined batch through `verification-and-gates.md` Who fixes; never return each failure immediately to its original lane.
- Ambiguous, cross-lane, flaky, timeout, environment, or contamination failure: `alaa-failure-analyst` first.
- For every implementation fix, including security, migration, architecture and contract-compatibility blockers, select the repair role for the remaining work: the Ent specialist route for Ent-owned repairs, Implementation routing for the rest. Preserve the finding verbatim.
- Browser-only reproducible defect: browser QA provides evidence; the owning implementer fixes.
- Test infrastructure defects keep their explicit infrastructure scope inside the serialized repair batch; the verifier never fixes. Environment actions require their existing authority.
