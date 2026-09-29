# Discovery and acceptance templates

## Spec analyst

```xml
<task>Convert this goal into a checkable acceptance contract and a lane decomposition: <goal>.</task>
<trigger>The request uses quality language that is not yet checkable, two competent readers would define "done" differently, a contract is implied but never stated, or the goal bundles several outcomes that need separating before lanes can be drawn.</trigger>
<request_verbatim><the user's own wording, unparaphrased></request_verbatim>
<repository_facts><paths, contracts, conventions, and prior lane outcomes already established in this session></repository_facts>
<known_constraints><compatibility windows, environments, deadlines, and decisions the user has already made></known_constraints>
<action_safety>Read-only. Do not implement, design the solution, write tests, or resolve a product decision the user owns.</action_safety>
<output>Restated outcome in one sentence; ACCEPTANCE CRITERIA numbered, each observable and mapped to how it would be verified; NON-GOALS and explicit exclusions; IMPLIED CONTRACTS; PROPOSED LANES, one line each with outcome, owned scope, exclusions, dependencies; OPEN DECISIONS with options and tradeoffs; UNKNOWNS not resolvable from the repository.</output>
```

## Explorer

```xml
<task>Map the execution path and ownership for: <question>.</task>
<focus>Entry points, symbols, data flow, tests, configuration, repository rules, coupling.</focus>
<action_safety>Strictly read-only. No external research and no proposed design unless options were requested.</action_safety>
```

## Researcher

```xml
<task>Establish the prior-context or external/version-specific facts needed for: <decision question>.</task>
<memory_query><exact prior session, decision, file, or shared-contract query; otherwise none. When set, apply /alaa-memory-os once and report recalled claims separately from repository verification.</memory_query>
<versions><versions derived from repository manifests/locks></versions>
<source_priority>Repository evidence and primary/official sources are proof; memory is a lead to verify.</source_priority>
<decision_boundary>Inform the orchestrator; do not decide or edit.</decision_boundary>
```
