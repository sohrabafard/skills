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

Use `routing-matrix.md` to select directly from the ratified lane record. Pass the same bounded lane block to the real registered variant; the compatibility role name never selects model or effort; explicitly supply the recorded task pair on the verified invocation surface. Preserve surviving work; no trial ladder or replay of completed work.

## Implementer escalation lane

```xml
<task>Implement escalated lane <n>: <bounded outcome whose design is not yet decided>.</task>
<role_selection><outcome/scope; settled and open decisions; failure/invariant reasoning; registered profile, selection reason and exceptional-admission evidence go once in `<task_controls>`></role_selection>
<scope><owned files/modules>; exclude <everything else>.</scope>
<acceptance_criteria><numbered, in the envelope criterion shape></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<design_constraints><architecture decisions, contracts, call sites, tests, and documented failure semantics that bound the design></design_constraints>
<skills><resolved lane bindings, including its matching clean-code owner or explicit repository baseline></skills>
<verification tier="focused">
  <commands><exact targeted commands: this lane's failure-mode tests plus lint, type, and build checks scoped to its files></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
  <excluded>the full suite, the race detector, the end-to-end suite, and any other lane's checks</excluded>
</verification>
<task_acceptance><only for the explicitly assigned task owner: exact bounded task-acceptance selectors at task end, or not assigned; never boundary affected/exhaustive checks></task_acceptance>
<action_safety>No unrelated work, commit, deploy, publish, destructive action, or global configuration change.</action_safety>
<output>Lane outcome in one sentence; design decision, alternatives rejected, and the deciding evidence; touched files and why each changed, plus each contract, interface or settled decision a later lane or repair owner must know, with file:line; acceptance criteria mapped to implementation/tests; verification evidence with command, cwd, resource policy, exit/result; residual risks and checks not run; blockers or boundary conflicts.</output>
```

## Collected verification repair

Use the implementer envelope above for the single serialized batch fix lane selected under `verification-and-gates.md` Gate economics. Replace the lane scope with the combined authorized repair scope; carry every failure verbatim, its classification and owner, retired conflicting writers and exact focused retests. When Gate economics continues an existing implementer, send this repair content with `<cadence>`, `<beads_identity>` and `<return>` as the continuation message rather than a new envelope; the original `<task_controls>` stands; if Implementation routing changed the profile or task pair, dispatch fresh under Gate economics instead. For an admitted early repair, scope only the recorded obstruction and return to collection without Review. Boundary retests remain the verifier's responsibility.
