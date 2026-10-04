# Implementation templates

## Implementer lane

```xml
<task>Implement lane <n>: <bounded outcome>.</task>
<role_selection><selected role; remaining-work reason; for difficult work: open decision, named criterion, correctness/failure consequence></role_selection>
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

When the routing matrix admits difficult work, dispatch the separate `alaa-implementer-opus` agent with the same lane block and its role-selection evidence. It is its own agent with its own pin, not a per-invocation override on `alaa-implementer`.

## Implementer escalation lane

```xml
<task>Implement escalated lane <n>: <bounded outcome whose design is not yet decided>.</task>
<role_selection><selected role; remaining-work reason; for difficult work: open decision, named criterion, correctness/failure consequence></role_selection>
<scope><owned files/modules>; exclude <everything else>.</scope>
<acceptance_criteria><numbered criteria></acceptance_criteria>
<dependencies><completed lane contracts or none></dependencies>
<design_constraints><architecture decisions, contracts, call sites, tests, and documented failure semantics that bound the design></design_constraints>
<skills><resolved lane bindings, including its matching clean-code owner or explicit repository baseline></skills>
<verification>
  <commands><exact targeted commands></commands>
  <low_priority_runner><absolute path when CPU-heavy></low_priority_runner>
  <resource_limits><priority, CPU count, workers, timeout></resource_limits>
</verification>
<action_safety>No unrelated work, commit, deploy, publish, destructive action, or global configuration change.</action_safety>
<output>Lane outcome in one sentence; design decision, alternatives rejected, and the deciding evidence; touched files and why each changed; acceptance criteria mapped to implementation/tests; verification evidence with command, cwd, resource policy, exit/result; residual risks and checks not run; blockers or boundary conflicts.</output>
```
