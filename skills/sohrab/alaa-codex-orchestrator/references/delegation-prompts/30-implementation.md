# Implementation templates

## Implementer lane

```xml
<task>Implement lane <n>: <bounded outcome>.</task>
<role_selection><outcome/scope; settled and open decisions; failure/invariant reasoning; registered profile, selection reason and exceptional-admission evidence go once in `<task_controls>`></role_selection>
<scope><owned files/modules>; exclude <everything else>.</scope>
<acceptance_criteria><numbered, in the envelope criterion shape></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<skills><resolved lane bindings, including its matching clean-code owner or explicit repository baseline></skills>
<verification tier="focused">
  <commands><exact targeted commands: this lane's failure-mode tests plus lint, type, and build checks scoped to its files></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
  <excluded>the full suite, the race detector, the end-to-end suite, and any other lane's checks</excluded>
</verification>
<task_acceptance><only for the explicitly assigned task owner: exact bounded task-acceptance selectors at task end, or not assigned; never boundary affected/exhaustive checks></task_acceptance>
<action_safety>No unrelated work, commit, deploy, publish, destructive action, or global configuration change.</action_safety>
```

Select the exact registered variant from the ratified lane record using `routing-matrix.md`; demanding workhorse work alone does not admit the exceptional implementation profile.

## Collected verification repair

Use the implementer envelope above for the single serialized batch fix lane selected under `verification-and-gates.md` Gate economics. Replace the lane scope with the combined authorized repair scope; carry every failure verbatim, its classification and owner, retired conflicting writers and exact focused retests. When Gate economics continues an existing implementer, send this repair content with `<cadence>`, `<beads_identity>` and `<return>` as the continuation message rather than a new envelope; the original `<task_controls>` stands; if Implementation routing changed the profile or task pair, dispatch fresh under Gate economics instead. For an admitted early repair, scope only the recorded obstruction and return to collection without Review. Boundary retests remain the verifier's responsibility.
