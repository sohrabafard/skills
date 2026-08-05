# Delegation Prompt Templates

Use the smallest applicable template. Replace placeholders with concrete repository facts and absolute script paths where required.

## Common dispatch envelope

```xml
<goal><one-sentence outcome></goal>
<context><relevant repository facts, prior lane outcomes, and preserved behavior></context>
<scope>
  <owned>files/modules or read-only questions</owned>
  <excluded>explicit exclusions</excluded>
</scope>
<acceptance_criteria><numbered checkable criteria></acceptance_criteria>
<constraints><safety, compatibility, resource, and user constraints></constraints>
<authority>what the agent may and may not change or execute</authority>
<return>the shape of the return and its line bound; findings, verdicts, counts, and artifact paths only, never transcripts, full diffs, or raw logs</return>
<output>use the agent's native output contract</output>
```

Every dispatch carries the `<return>` field. An unbounded child return is the most common way a parent's context is flooded, and the parent pays that cost on every remaining turn of the goal, not only on the turn the return arrives.

## Spec analyst

```xml
<task>Convert this goal into a checkable acceptance contract and a lane decomposition: <goal>.</task>
<trigger>The request uses quality language that is not yet checkable, two competent readers would define "done" differently, a contract is implied but never stated, or the goal bundles several outcomes that need separating before lanes can be drawn.</trigger>
<request_verbatim><the user's own wording, unparaphrased></request_verbatim>
<repository_facts><paths, contracts, conventions, and prior lane outcomes already established in this run></repository_facts>
<known_constraints><compatibility windows, environments, deadlines, and decisions the user has already made></known_constraints>
<action_safety>Read-only. Do not implement, design the solution, write tests, or resolve a product decision the user owns.</action_safety>
<output>RESTATED OUTCOME in one sentence; ACCEPTANCE CRITERIA numbered, each observable and mapped to how it would be verified; NON-GOALS including outcomes implied but deliberately out of scope; IMPLIED CONTRACTS; PROPOSED LANES, one line each with outcome, owned scope, exclusions, dependencies; OPEN DECISIONS with options and tradeoffs; UNKNOWNS.</output>
```

## Explorer

```xml
<task>Map the execution path and ownership for: <question>.</task>
<focus>Entry points, symbols, data flow, tests, configuration, repository rules, coupling.</focus>
<action_safety>Strictly read-only. No external research and no proposed design unless options were requested.</action_safety>
```

## Researcher

```xml
<task>Establish the external/version-specific facts needed for: <decision question>.</task>
<versions><versions derived from repository manifests/locks></versions>
<source_priority>Repository evidence, then primary/official sources.</source_priority>
<decision_boundary>Inform the orchestrator; do not decide or edit.</decision_boundary>
```

## Test strategist

```xml
<task>Design the minimal test matrix that proves: <acceptance criteria>.</task>
<doctrine>Apply $alaa-testing-strategy, which owns the method: derive the matrix from the failure modes this change introduces, name the plausible broken implementation each test must fail against, place each behaviour at exactly one layer, bind every double that can drift, and assign each claim the proof level it requires.</doctrine>
<failure_models><plausible broken implementations and failure modes to catch></failure_models>
<repository_commands><known test commands and helpers></repository_commands>
<action_safety>Read-only; do not write tests.</action_safety>
```

## Implementer lane

```xml
<task>Implement lane <n>: <bounded outcome>.</task>
<scope><owned files/modules>; exclude <everything else>.</scope>
<acceptance_criteria><numbered criteria></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<clean_code_skill><matching installed skill or repository baseline></clean_code_skill>
<verification tier="focused">
  <commands><exact targeted commands: this lane's failure-mode tests plus lint, type, and build checks scoped to its files></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
  <excluded>the full suite, the race detector, the end-to-end suite, and any other lane's checks</excluded>
</verification>
<action_safety>No unrelated work, commit, deploy, publish, destructive action, or global configuration change.</action_safety>
```

Use `alaa-implementer-sol` instead of `alaa-implementer` when the routing matrix says to escalate.

## Verifier

```xml
<task>Independently verify the combined change for: <goal>.</task>
<repository><absolute worktree path></repository>
<initial_expectation><expected clean/known git status></initial_expectation>
<commands>
  <command id="1" cpu_heavy="true|false" timeout_seconds="...">exact command and cwd</command>
</commands>
<artifacts><permitted artifact directory only></artifacts>
<resource_policy>
  Windows runner: <absolute SKILL_ROOT>/scripts/Invoke-AlaaLowPriority.ps1
  Unix runner: <absolute SKILL_ROOT>/scripts/run-low-priority.sh
  Priority: BelowNormal; CPU count: <n>; only one heavy command at a time.
</resource_policy>
<tier>affected | exhaustive — affected once per phase, exhaustive once on the final candidate</tier>
<already_observed><commands whose recorded results are still valid, with the run that produced each; do not re-run these></already_observed>
<rerun_policy>none | one identical rerun for flake detection</rerun_policy>
<action_safety>Evidence only. Never fix or alter command semantics.</action_safety>
```

## Failure analyst

```xml
<task>Diagnose this verification failure without editing: <status and command>.</task>
<evidence><verifier output, logs, artifacts, git status, relevant lane summaries></evidence>
<question>Classify the failure, identify first cause and owner, and propose the smallest falsifying check or fix instruction.</question>
<diagnostic_authority>Read-only; targeted command only if explicitly listed here.</diagnostic_authority>
```

## Reviewer

```xml
<task>Review the complete change for: <goal>.</task>
<plan><lanes and acceptance criteria></plan>
<diff_scope><base/head or touched files></diff_scope>
<verification_evidence><integrated verifier results></verification_evidence>
<stance>Fresh context, read-only, findings-first, no fixes.</stance>
<adversarial>true|false</adversarial>
```

## Architecture critic

```xml
<task>Pressure-test this proposed architecture before implementation: <plan>.</task>
<standard>Judge it against $alaa-system-design, which owns this design method: the six conditions requiring a design pass, the boundary and seam tests, contract-before-code, one writer per datum with every second copy labelled cache or fork, the dependency classification, and the two-candidate rule. Its references/70-review-and-readiness.md states what blocks at each step.</standard>
<design_record><path to the design record under review, or a statement that no design pass was run and which of the six conditions fired></design_record>
<invariants><required correctness, compatibility, security, and operability invariants></invariants>
<evidence><architecture docs, relevant code paths, external contracts></evidence>
<question>Find blockers, hidden assumptions, simpler alternatives, rollout/rollback conditions.</question>
```

## API contract reviewer

```xml
<task>Judge whether this contract transition is safe for existing consumers: <surface and shape change>.</task>
<trigger>A public HTTP or RPC endpoint, event or message schema, shared DTO, SDK surface, or persisted serialization format changes shape. Dispatch in Phase A before code exists; dispatch in Phase D instead only when the contract change emerged during implementation.</trigger>
<surfaces><old and new shape per field and per operation, with the schemas, serializers, and published specs that define them></surfaces>
<consumers><known call sites, published specs, collections, client code, and the upgrade cadence of the slowest consumer></consumers>
<versioning><existing versioning strategy, deprecation policy, and any window already promised></versioning>
<rollout><planned producer and consumer deploy order, and the environments involved></rollout>
<action_safety>Read-only. Never edit the contract, the published specification, or the contract tests, and never design the replacement surface.</action_safety>
<output>First line exactly VERDICT: COMPATIBLE | VERDICT: COMPATIBLE-WITH-MIGRATION | VERDICT: BREAKING; then BREAKING CHANGES with surface, consumer impact, required migration; COMPATIBILITY WINDOW AND ROLLOUT ORDER; SPEC AND CONTRACT-TEST DRIFT; EVIDENCE INSPECTED.</output>
```

## Security reviewer

```xml
<task>Perform a defensive security review of: <change scope>.</task>
<trust_boundaries><actors, inputs, privileges, sensitive assets></trust_boundaries>
<verification><security tests/evidence already run></verification>
<action_safety>Repository-only, read-only, no external exploitation.</action_safety>
```

## Migration guardian

```xml
<task>Gate this schema/data migration: <change>.</task>
<database><technology/version and deployment model></database>
<rollout><old/new app and schema sequence></rollout>
<data_scale><known scale or explicitly unknown></data_scale>
<question>Check compatibility, locks/load, backfill, validation, rollback/roll-forward, abort thresholds.</question>
```

## Dependency auditor

```xml
<task>Audit this dependency change: <packages added, upgraded, removed, or replaced>.</task>
<trigger>A dependency was added, upgraded, removed, or replaced, a lockfile changed outside a scoped upgrade lane, or a transitive tree shifted materially.</trigger>
<change><resolved before and after versions per package, and the manifest and lockfile diff></change>
<manifests><absolute manifest and lockfile paths, the project's own license, and its distribution model></manifests>
<audit_tooling><the repository's existing audit, license, and lock-verification commands, or none available></audit_tooling>
<action_safety>Read-only. Never upgrade, pin, add resolutions or overrides, regenerate a lockfile, edit a manifest, or install anything.</action_safety>
<output>First line exactly VERDICT: CLEAR | VERDICT: CLEAR-WITH-CONDITIONS | VERDICT: BLOCK; then FINDINGS with package@version, severity, category, evidence, remediation; TRANSITIVE IMPACT; LOCKFILE INTEGRITY; UNVERIFIED CLAIMS; EVIDENCE INSPECTED.</output>
```

## Accessibility reviewer

```xml
<task>Review accessibility for: <changed interface>.</task>
<trigger>New or changed user-visible interface — components, forms, dialogs, navigation, tables, and any flow a user completes with a keyboard or a screen reader.</trigger>
<surface><components, templates, styles, and routes in scope, and the flows they compose></surface>
<rendered_evidence><snapshots, accessibility tree output, automated scan results, or explicitly none></rendered_evidence>
<design_system><design tokens, focus-style resets, and motion conventions in force></design_system>
<locales><shipped locales, and whether an RTL locale is among them></locales>
<action_safety>Read-only. Never fix markup, styles, or components, and never pass a check that requires rendered evidence you were not given.</action_safety>
<output>First line exactly VERDICT: ACCESSIBLE | VERDICT: ACCESSIBLE-WITH-GAPS | VERDICT: BLOCK; then FINDINGS with file:line, severity, the barrier, who it blocks, concrete fix; RTL AND LOCALE NOTES; NOT ASSESSED; EVIDENCE INSPECTED.</output>
```

## Browser QA

```xml
<task>Execute browser QA for: <user-visible behavior>.</task>
<environment><URL, existing server, auth/test data, viewport></environment>
<scenarios><exact steps and expected results></scenarios>
<browser_constraint>Preserve --browser chromium and configured profile. Do not start duplicate services.</browser_constraint>
<artifacts><absolute permitted artifact directory></artifacts>
```

## Performance profiler

```xml
<task>Measure: <metric/question>.</task>
<budget_owner>$alaa-algorithms-data-structures owns the complexity budget this measurement is judged against — the operation, the dimension that grows, the bound, and the input size the bound was measured at. Read it when the declared budget names no growing dimension, or when the finding is that the path has no enforced maximum.</budget_owner>
<workload><scenario, data shape, concurrency, warmup></workload>
<baseline_budget><baseline and pass/fail budget></baseline_budget>
<environment><comparable environment facts></environment>
<resource_policy><low-priority runner, CPU count, timeout></resource_policy>
<artifacts><profile/trace output directory></artifacts>
```

## Observability reviewer

```xml
<task>Review production diagnosability for: <change>.</task>
<failure_states><new/changed success, failure, retry, degraded states></failure_states>
<telemetry_stack><repo-observed logs/metrics/traces/alerts conventions></telemetry_stack>
<question>Map states to signals, decisions, alerts, runbooks, privacy/cardinality risks.</question>
```

## Release guardian

```xml
<task>Gate release readiness for: <change>.</task>
<scope><CI, container, config, dependencies, deployment, health, docs as applicable></scope>
<evidence><build/verification/review results></evidence>
<question>Identify conditions, ordered rollout, rollback, manual steps, and unverified prerequisites.</question>
```

## Adversarial reviewer

```xml
<task>Apply the adversarial lens to the complete change for: <goal>.</task>
<trigger>The change is irreversible or has high blast radius — production data movement, auth or tenancy boundaries, a public contract break, deployment topology — or `alaa-reviewer` and a specialist returned conflicting verdicts that repository evidence does not settle.</trigger>
<diff_scope><base/head or touched files></diff_scope>
<prior_gates><reviewer and specialist verdicts and findings verbatim, including the unresolved conflict when that is the trigger></prior_gates>
<verification_evidence><integrated verifier results and what each command actually exercised></verification_evidence>
<blast_radius><what is irreversible, who is affected, and the cost of undoing it></blast_radius>
<stance>Fresh independent lens, read-only, no fixes. Do not re-run the correctness review or restate findings `alaa-reviewer` already raised.</stance>
<disposition>Reported to the user as a ship decision. Findings are not routed into another fix cycle.</disposition>
<output>First line exactly VERDICT: NO-BLOCKING-OBJECTION | VERDICT: OBJECTION-WITH-CONDITIONS | VERDICT: DO-NOT-SHIP; then OBJECTIONS with the assumption attacked, the concrete failure scenario, the cost to undo, confidence 0-1; WHAT WOULD CHANGE MY VERDICT; EVIDENCE INSPECTED.</output>
```

## Fix-cycle dispatch

```xml
<task>Resolve reviewer/specialist findings in original lane <n>.</task>
<findings_verbatim><file:line, severity, failure, required fix></findings_verbatim>
<original_scope_and_acceptance>unchanged unless the orchestrator explicitly revises them</original_scope_and_acceptance>
<verification><the focused checks for each fixed finding, plus the affected-tier checks the fix reaches></verification>
<output>For each finding: fixed | disputed with repository evidence; touched files; verification; new risks.</output>
```

## Documenter

```xml
<task>Update documentation for verified shipped change: <goal>.</task>
<change_summary><actual behavior, files, configuration/API/operational changes></change_summary>
<verdicts><review and specialist verdicts></verdicts>
<scope><expected documentation files/sections></scope>
<checks><docs formatter, links, examples, scope check, and the size grade></checks>
<size_grade>Grade every eligible narrative document by the ladder in alaa-repo-docs references/15-document-size-and-clustering.md and report each final grade with the reason that file requires.</size_grade>
<action_safety>Documentation files only; no intended or unverified behavior.</action_safety>
```
