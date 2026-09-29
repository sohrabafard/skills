# Contract and security review templates

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
