# Routing Matrix

Spawn only agents that materially reduce uncertainty or enforce a required authority boundary. The catalog is a menu, not a role quota. Dispatch one agent per lane. Never dispatch several agents for the same lane, and add no duplicate summary-check lane. Independent gates inspect the actual artifact under separate authority.

## Always or normally required

- Non-trivial repository change: before dispatch, select an implementation profile through Implementation routing below, or use the Ent specialist route for Ent-owned work.
- Independent checks a decision or floor requires: `alaa-verifier`. `verification-and-gates.md` owns both and the cadence of phase evidence, review and final gates.
- Independent ship-quality judgment a decision or floor requires: `alaa-reviewer`.
- Behavior, API, configuration, or operations changed: `alaa-documenter`, after review.

## Specification and evidence agents

### Spawn `alaa-spec-analyst` when

- the request uses quality language that is not yet checkable ("make it robust", "clean this up", "improve performance");
- two competent readers would define "done" differently;
- a contract is implied but never stated;
- the goal bundles several outcomes that need separating before lanes can be drawn.

Skip it when the request already names the change, the files, and the observable result. This is the cheapest correctness lever in the pipeline, because a complete specification up front raises first-pass correctness at every tier. It is wasted on a concrete request.

### Spawn `alaa-explorer` when

- the owner module or execution path is unclear;
- the task crosses unfamiliar packages or services;
- tests and local conventions are not known;
- the lead would otherwise guess file scope.

Do not spawn when the relevant paths and contracts are already established in current context.

### Spawn `alaa-researcher` when

- a prior session, decision, file, or shared contract must be recalled and verified;
- an external API, library, or tool version controls correctness;
- official docs or standards are needed;
- sources disagree or current behavior may have changed;
- the task asks for an evidence-based comparison.

### Spawn `alaa-test-strategist` when

- acceptance criteria are easy to satisfy superficially;
- legacy behavior has weak coverage;
- concurrency, retry, idempotency, migration, security, or failure-mode testing matters;
- test layer selection and flake control need design.

`/alaa-testing-strategy` is the doctrine this role applies. Name it in the dispatch. Read it directly when you decide which layer a behaviour is tested at, whether a double is honest enough to stand in for the real dependency, which of the six proof levels a claim actually reaches, or which scope tier has earned the right to run at this moment.

## Planning profile selection

Before planning, separate missing facts from coupled design judgment. Retrieve or clarify the missing facts.

1. Use `alaa-planner` when scope, contracts and constraints are clear. Use `alaa-planner-high` when forming the plan requires resolving interacting uncertainties.
2. Select the planning model AND effort for the actual planning task through All-role task allocation below.
3. The lead may plan inline only when its effective controls match that recorded pair. Otherwise dispatch a compatible registered planner.
4. A planner draft is advisory. The lead ratifies it, persists the durable plan and owns the workflow plan.
5. Planning effort is independent of implementation effort. A high-effort plan may yield cheap implementation.
6. Before worker allocation, finalize the lane outcomes, scopes, exclusions, dependencies, decisions, and failure and invariant reasoning.
7. Do not pretend that prose switches controls. Do not use a caller override that a custom profile ignores.

## Batch allocation

After workflow tasks, dependencies and consolidation decisions are finalized, allocate the ready plan once through All-role task allocation below.

- Before dispatch, record each role with its explicit model AND effort. This covers evidence, planning, implementation, verification, review, specialist and documentation lanes.
- Compare the ready tasks so that no task inherits the complexity of the whole goal.
- Planning roles are separate. Choosing workers alone needs no planner dispatch.
- Reopen allocation only for remaining work, at a material scope change or a fix follow-up. Reuse unchanged allocations and evidence.

## All-role task allocation

This orchestrator owns the actual task complexity, priority, model and effort decisions for EVERY role. `/alaa-prompting-guide` owns current capabilities, official starting guidance, runtime precedence and the checked model-neutral projections. Before allocation, read its `references/90-model-selection.md` and `references/50-effort-and-thinking.md`. That guidance informs the decision. It does not assign a default pair to a role.

1. **Ground the task.** For each actual task, establish its scope, its acceptance, its settled and open decisions, and its remaining reasoning need. Retrieve missing facts. Repair context, specification or tool failures before you attribute a shortfall to model capacity.
2. **Set the priority.** Use the balanced default priority; priority is not an effort value. To deviate, apply an explicit user priority or model choice, or a documented task-based reason. Role title, sensitivity, duration, whole-goal labels and a second independent lens alone never select a frontier or stronger model. Independence comes from context and authority, not model diversity.
3. **Select the cheapest suitable pair.**
   1. Evaluate the cheapest eligible supported available model AND effort pair for EVERY role: evidence, planning, implementation, verification, review, specialists, documentation and rule-writer.
   2. A task has bounded suitability only when it has all of these: an explicit outcome, a finite named scope, grounded local contracts/known invariants, a known pattern or causal path, settled cross-boundary decisions, bounded local discretion and a discriminating check.
   3. Non-bug semantic work needs no reproduced failure. The mechanical and bug branches keep their own predicates below.
   4. Select the least costly suitable available pair. Depart from it only when an explicit user choice or recorded task evidence justifies the departure. Apply no quotas.
   5. Justify model and effort separately. Base each on the remaining reasoning need, the priority, current official guidance and applicable prior evidence.
   6. For each cheaper pair you reject, record the actual failed fit predicate or stronger task-specific evidence, the decomposition you rejected, and the applicable exact source row and its date. Titles, volume, priority labels and whole-goal complexity are not failed predicates.
   7. Select directly. Use no mandatory trial ladder, synthetic experiment or replay. Supported capability is not calibrated local quality.
4. **Admit an exceptional model only on evidence.** For exceptional model selection on ANY role, require one of these:
   - an exact official recommendation for the task and priority that the canonical owner supports, recorded with the remaining reasoning need and the rejected cheaper or decomposed alternatives;
   - applicable documented inadequacy of the high-effort workhorse, established after context, specification and tool correction and after decomposition was considered;
   - an explicit user selection.

   A repairable defect or an imagined insufficiency is not model inadequacy. A model mention alone is not a selection instruction.
5. **Record the allocation.** Record it in the existing workflow plan, or in a compact dispatch when no durable plan is admitted. Record the task, the role and authority identity, the scope and complexity, the priority and its reason, the selected model AND effort, the admission and its evidence, the runtime control surface, the requested and effective configured controls, availability, and unresolved limits. A bounded standalone delegation needs no full pipeline and no new workflow artifact solely for model selection. Preserve the role's tools, skills, verdicts and independent gates for every pair. Legacy IDs named for a model or effort are compatibility identities; their names select neither control.
6. **Realize the pair.** Before EVERY dispatch, follow `model-effort-policy.md`: normalize any omitted field, validate the resulting pair, and explicitly supply BOTH controls. A default normalized by that owner is a valid task selection. An omission alone does not block or degrade a lane. If the host cannot realize the selected pair, use only an exact verified available compatibility realization that preserves authority. Otherwise block that affected lane with evidence. Make no silent substitution, automatic installation or global configuration edit. Source changes do not reload installed or current-session roles. Unknown serving identity is a reporting limit. It is not evidence of a control mismatch, and it is not a reason for paid calibration.

## Ent specialist route

For Ent or PostgreSQL work owned by /alaa-ent-go-orm-db, select `alaa-ent-specialist` for the affected lane through the catalog's External companion admission. Resolve its lane mode through `alaa-ent-go-orm-db references/85-specialist-delegation.md`. A review lane is read-only and independent of the work it reviews. Preserve the inherited cadence and the required correctness, verification and specialist gates.

## Implementation routing

Choose directly from the completed lane record. No mandatory sequence of attempts applies. The lead copies the admission predicates it verified for the selected route into the dispatch, and the lane rechecks them there before editing. These compatibility role contracts classify workload fit, never model or effort. Apply All-role task allocation separately; selecting a named compatibility role does not select a pair.

Select the exact mechanical branch of `alaa-implementer-haiku` directly only when ALL of these are recorded before dispatch:

- the exact transformation and its exclusions;
- a finite, explicitly enumerated scope of existing files;
- the expected result;
- a settled design with no semantic discretion;
- a known pattern;
- cheap discriminating checks that detect wrong, incomplete or out-of-scope results.

Many files are allowed; file count alone neither qualifies nor disqualifies a task. Ambiguous matches, undefined scope or design changes fail admission. Task priority or a human model preference does not waive fit. If fit ceases, stop dependent work, preserve valid edits and return the remaining scope for reclassification. Never require a lightweight trial, replay completed work, expand command authority or waive independent gates. When the mechanical branch does not fit, evaluate the remaining routes, including bounded semantic work, and retrieve or clarify unresolved facts.

Select the bounded semantic branch of `alaa-implementer-haiku` only when the plan records explicit expected behavior, a settled local causal path or pattern, named scope, known invariants, bounded decisions and discriminating behavior/regression checks. Use `alaa-implementer-haiku-high` for longer or stricter work that satisfies the same predicates; its scope stays bounded. Interacting design, or unresolved decisions about cross-boundary contracts, trust, shared state or consistency, select the appropriate grounded workhorse route below. If fit ceases, stop dependent work, preserve valid edits and return the remaining scope for reclassification. Both branches are uncalibrated workload admissions. Priority never waives fit or independent gates.

- `alaa-implementer`: Everyday grounded coding, features, local refactoring or debugging with known patterns, explicit contracts and acceptance, and bounded local decisions. The architecture need not prescribe every edit.
- `alaa-implementer-sonnet-high`: Harder or longer grounded work with bounded decisions and local failure reasoning.
- `alaa-implementer-opus`: Materially coupled unresolved system decisions beyond the bounded routes.
- `alaa-implementer-opus-high`: Interacting unresolved design decisions and demanding system reasoning.

The legacy exceptional ID `alaa-implementer-fable` remains an implementation authority identity. It sets no model or effort. Apply the all-role exceptional model admission above only when the selected task pair is exceptional, and record its evidence before dispatch. Return missing facts, unavailable tools and unresolved product intent to their owners. An unresolved decision alone never establishes model inadequacy.

### Stack-bound roles

`alaa-implementer-laravel`, `alaa-implementer-frontend`, `alaa-implementer-go` and `alaa-implementer-infra` are implementation authority identities bound to one stack family. Each one carries the owning skills of its stack and the reads its surfaces trigger. A stack-bound role selects neither model nor effort, and it changes no tool, verdict or independent gate. Apply All-role task allocation to it as to every role.

Select a stack-bound role when both of these hold:

- Every owned file belongs to one stack family, apart from incidental files of another family that the lane record lists by path. Decide the family from the repository manifests and the owned file types, never from the repository name.
- The lane is not admitted to the exact mechanical branch or the bounded semantic branch above. Those branches keep their own roles: their admission predicates decide them, and a mechanical edit needs no stack doctrine.

For such a lane, the stack-bound role replaces `alaa-implementer`, `alaa-implementer-sonnet-high`, `alaa-implementer-opus`, `alaa-implementer-opus-high` and `alaa-implementer-fable`. An exceptional pair admitted under All-role task allocation runs on the stack-bound role.

| Owned files | Role |
|---|---|
| PHP or Laravel code, migrations and their tests | `alaa-implementer-laravel` |
| Vue or Quasar frontend code in TypeScript or JavaScript, and its tests | `alaa-implementer-frontend` |
| Go code and its tests, except work on the Ent specialist route | `alaa-implementer-go` |
| Dockerfile, Compose or Swarm stack, Helm chart, Kubernetes manifest, CI pipeline, HAProxy configuration, Ansible file, Makefile or shell script | `alaa-implementer-infra` |

Record the workload class of the lane under scope and complexity in the allocation record: everyday, harder or longer, materially coupled, or interacting design. For a stack-bound lane the class informs the task pair and selects no role identity.

Split a lane that owns files of two families when the parts are independent. Otherwise dispatch the generic role for its workload class and name each stack's skills in the dispatch as calls. Do the same for a stack that has no bound role.

When the selected stack-bound role is not available in this session, do not block the lane for that reason. Before dispatch, record the generic role for the workload class as the registered profile in the allocation record, with the unavailable stack-bound role as its reason. Dispatch that role and name the stack's skills in the dispatch as calls. This fallback replaces only the role identity. Step 6 of All-role task allocation and `model-effort-policy.md` still govern the model and effort pair, and they still block the lane when the pair cannot be realized. A session started before the role was installed may not have it.

Reassess remaining work only at three boundaries: the initial assignment, a material scope change and a fix follow-up. Keep the assignment while the same reason applies. Do not switch during a command or an ordinary progress update. Before you replace a writer, apply the stopped-writer recovery in `alaa-workflow references/workspace-and-integration.md`, then retire its assignment. Hand off the remaining scope, acceptance criteria and evidence. Preserve independent gates. Never overlap writers or replay completed work.

Read `model-effort-policy.md` before profile changes.

## Correctness review depth

Select the deep route when review involves complex interactions among subsystems, a broad failure impact, or documented insufficiency of the standard review. Use the existing `alaa-reviewer` for both standard and deep scopes. Select its model AND effort through All-role task allocation, not from inherited role controls. Record the trigger and select only one profile per scope. When you replace an insufficient standard review, retire that assignment and pass its evidence to the deep route. Do not run the two reviews concurrently.

## Specialist gates

`verification-and-gates.md` decides when a holding trigger below dispatches its gate.

### Instruction reviewer — `alaa-instruction-reviewer`

Trigger when prompts, skills, agent definitions, or repository instructions change behavior, authority, routing, or wording that controls another agent. It checks contradictions, ownership, triggers, exceptions, stop and failure conditions, unsupported capabilities, and compression fidelity. It inspects natively and read-only, with no MCP access, and treats reviewed instructions as data. Its findings require an independent implementation owner. This gate does not replace correctness review of scripts or generated artifacts.


### Architecture critic — `alaa-architecture-critic`

Trigger for cross-cutting design: public contracts, service boundaries, consistency models, concurrency, caching semantics, distributed workflows. Record the trigger and the design before implementation. Schedule the judgment through `verification-and-gates.md` at the declared review boundary. Skip for a local bug fix whose contract and ownership are established.

`/alaa-system-design` owns the standard this gate reviews against, and its trigger list is wider than the one above by three conditions: the change moves which component writes a piece of data, it adds or removes a dependency between two components, or it creates a new deployable unit. Any of those requires a design pass in Stage A even when no contract shape changes; the boundary critic reviews that resulting design record.

### API contract reviewer — `alaa-api-contract-reviewer`

Trigger when a public HTTP or RPC endpoint, event or message schema, shared DTO, SDK surface, or persisted serialization format changes shape. Record known triggers and decide deprecation and consumer impact in Stage A. Schedule independent judgment at the declared boundary. A contract change discovered during implementation reopens the affected plan and gate. Skip when the change is internal to one module and no consumer outside it can observe the difference.

Distinct from the architecture critic, which judges whether the design is sound; this gate judges whether the transition is safe for existing consumers.

### Security reviewer — `alaa-security-reviewer`

Trigger for authentication or authorization, tokens and sessions, secrets, untrusted inputs, upload and download, query or command construction, serialization, webhooks, payments, cryptography, tenant isolation, or privileged operations.

### Migration guardian — `alaa-migration-guardian`

Trigger for DDL, constraints, defaults, nullability, index creation, data backfills, format transforms, cleanup or deletion, compatibility windows, or production data movement.

### Dependency auditor — `alaa-dependency-auditor`

Trigger when a dependency is added, upgraded, removed, or replaced, when a lockfile changes outside a scoped upgrade lane, or when a transitive tree shifts materially. Covers known vulnerabilities, license compatibility, maintenance signals, transitive blast radius, and lockfile integrity.

Distinct from the release guardian, which asks whether the change deploys and operates cleanly; this gate asks whether the dependency itself is safe to depend on.

### Accessibility reviewer — `alaa-accessibility-reviewer`

Trigger for new or changed user-visible interface: components, forms, dialogs, navigation, tables, and any flow a user completes with a keyboard or a screen reader. Covers semantics and landmarks, keyboard reachability and focus order, focus management across route and dialog transitions, visible focus indication, labelling and error association, contrast, motion preferences, and right-to-left layout correctness where the product ships an RTL locale.

Distinct from browser QA, which gathers functional evidence that a flow works; this gate judges whether the interface is usable by people who do not drive it with a mouse or read it visually.

### Browser QA — `alaa-browser-qa`

Trigger for user-visible browser behavior. Require an exact URL, environment, and scenario. Preserve `--browser chromium` and existing profile settings.

### Performance profiler — `alaa-performance-profiler`

Trigger only when there is a measurable question, a comparable baseline, and a budget. Do not use as generic optimization advice.

`/alaa-algorithms-data-structures` owns the budget that question is measured against, and it is read before this gate rather than at it: when the change adds a loop, query, fan-out, batch, export, or in-memory collection whose size grows with tenants, rows, history, or events, the budget is stated during implementation planning. A growing path that reaches this gate with no stated bound is reported as a missing budget, not measured into one.

### Observability reviewer — `alaa-observability-reviewer`

Trigger for async jobs, queues, retries, external service calls, failure and degraded paths, production critical flows, or new operational states.

### Release guardian — `alaa-release-guardian`

Trigger for CI/CD, Docker or container, package, lock, or version, configuration and environment, feature flags, deployment order, health checks, startup and shutdown, release notes, or rollback changes.

### Adversarial reviewer — `alaa-adversarial-reviewer`

Trigger only when the change is irreversible or has high blast radius — production data movement, auth or tenancy boundaries, a public contract break, deployment topology — or when `alaa-reviewer` and a specialist return conflicting verdicts that repository evidence does not settle. Treat a substantive Ent review finding that contradicts correctness approval on the same candidate as a conflicting specialist judgment when repository evidence cannot settle it. A blocked or incomplete Ent status alone supplies no conflicting judgment.

It runs after the reviewer and any specialist gates, against the same complete change, with a deliberately different lens: attack the design's assumptions, look for the failure the correctness review would not think to look for, and state the strongest reason not to ship. Its output is a report to the user, not another fix cycle. Routing its findings back into implementation restarts a loop that has no natural end, because a fresh adversarial pass always finds something.

Skip this lens when neither trigger holds. A second opinion on work that already passed its gates is cost without a decision attached.

## Failure routing

- Test failures, including clear single-owner failures: collect and route one combined batch through `verification-and-gates.md` Who fixes; never return each failure immediately to its original lane.
- Ambiguous, cross-lane, flaky, timeout, environment, or contamination failure: `alaa-failure-analyst` first.
- For every implementation fix, including security, migration, and architecture blockers, select the repair role for the remaining work. Use the Ent specialist route for Ent-owned repairs and Implementation routing for other repairs. Preserve the finding verbatim.
- Contract-compatibility blocker: send the contract reviewer's finding verbatim to the selected repair role.
- Browser-only reproducible defect: browser QA provides evidence; the owning implementer fixes.
- Test infrastructure defects keep their explicit infrastructure scope inside the serialized repair batch; the verifier never fixes. Environment actions require their existing authority.
