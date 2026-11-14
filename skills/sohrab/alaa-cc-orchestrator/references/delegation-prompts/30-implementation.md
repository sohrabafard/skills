# Implementation templates

## Implementer lane

```xml
<task>Implement lane <n>: <bounded outcome>.</task>
<role_selection><outcome/scope; settled and open decisions; failure/invariant reasoning; registered profile, selection reason, verified admission predicates and exceptional-admission evidence go once in `<task_controls>`></role_selection>
<scope><owned files/modules and the test files that cover them and that no other lane owns>; exclude <everything else>.</scope>
<acceptance_criteria><numbered, in the envelope criterion shape></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<skills><resolved lane bindings, each written as a call, never as a bare mention, including its matching clean-code owner or explicit repository baseline></skills>
<verification tier="focused">
  <commands><exact targeted commands: this lane's failure-mode tests plus lint, type, and build checks scoped to its files></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
  <excluded>the full suite, the race detector, the end-to-end suite, and any other lane's checks</excluded>
</verification>
<baseline_failures><tests or checks that already fail before this lane starts, each with the command that shows it, or: none recorded></baseline_failures>
<task_acceptance><only for the explicitly assigned task owner: exact bounded task-acceptance selectors at task end, or not assigned; never boundary affected/exhaustive checks></task_acceptance>
<action_safety>No unrelated work, deploy, publish, destructive action, or global configuration change; commit only as `<commit>` grants.</action_safety>
<commit><lane branch name: commit your owned paths by path when the focused checks pass> | <none: return the work uncommitted></commit>
```

Record the verified admission predicates in `<task_controls>` of every implementation dispatch. For a mechanical or bounded route, record the selected route's own predicates with their recorded values. For a workhorse or stack-bound route, record the workload class and the stack-family test result. A dispatch without them is incomplete: complete it before you send it, because the lane checks those predicates instead of reading `routing-matrix.md`. Fill `<commit>` with the lane branch that `verification-and-gates.md` *Before any dispatch* step 4 prescribes, or with `none`.

Use `routing-matrix.md` to select directly from the ratified lane record. Pass the same bounded lane block to the real registered variant. For a single-stack lane outside the mechanical and bounded branches, the registered variant is the stack-bound role that routing-matrix.md names. The compatibility role name never selects model or effort; pass the recorded effort as the `effort` parameter and the recorded model's alias, as `model-effort-policy.md` maps it, as the `model` parameter of the verified Agent invocation. Preserve surviving work. Require no trial ladder and no replay of completed work. Demanding work alone does not admit the exceptional implementation profile.

## Collected verification repair

For each scoped assignment in the serialized repair batch selected under `verification-and-gates.md` Who fixes, use the envelope above for a managed implementer. For an Ent-owned repair, use the Ent specialist dispatch contract from the common router in `implement` mode. Apply the same scoped repair and retest limits. Use the authorized scope of this assignment. Carry each assigned failure verbatim with its classification and owner, the retired conflicting writers, and the exact focused retests. When Who fixes continues an existing implementer, send this repair content with `<cadence>`, `<beads_identity>` and `<return>` as the continuation message rather than a new envelope. Apply the common envelope's Mandatory Ponytail binding route before continuing. The original `<task_controls>` stands. If Failure routing selects another role, profile or task pair, dispatch fresh under Who fixes. For an admitted early repair, scope only the recorded obstruction and return to collection without Review. Prove each fix under `verification-and-gates.md` After a fix.
