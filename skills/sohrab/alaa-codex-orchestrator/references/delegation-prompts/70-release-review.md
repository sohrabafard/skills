# Dependency and release review templates

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

## Release guardian

```xml
<task>Gate release readiness for: <change>.</task>
<scope><CI, container, config, dependencies, deployment, health, docs as applicable></scope>
<evidence><build/verification/review results></evidence>
<question>Identify conditions, ordered rollout, rollback, manual steps, and unverified prerequisites.</question>
```
