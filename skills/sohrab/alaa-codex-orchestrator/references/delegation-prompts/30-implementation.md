# Implementation templates

## Implementer lane

```xml
<task>Implement lane <n>: <bounded outcome>.</task>
<role_selection><exact registered profile from ratified plan; outcome/scope; settled and open decisions; failure/invariant reasoning; selection reason; exceptional admission: canonical-supported exact official task/priority with reasoning need and rejected cheaper/decomposed alternatives, applicable high-workhorse inadequacy with context/spec/tool corrections, or explicit user direction></role_selection>
<scope><owned files/modules>; exclude <everything else>.</scope>
<acceptance_criteria><numbered criteria></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<skills><resolved lane bindings, including its matching clean-code owner or explicit repository baseline></skills>
<verification tier="focused">
  <commands><exact targeted commands: this lane's failure-mode tests plus lint, type, and build checks scoped to its files></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
  <excluded>the full suite, the race detector, the end-to-end suite, and any other lane's checks</excluded>
</verification>
<action_safety>No unrelated work, commit, deploy, publish, destructive action, or global configuration change.</action_safety>
```

Select the exact registered variant from the ratified lane record using `routing-matrix.md`; demanding workhorse work alone does not admit the exceptional implementation profile.
