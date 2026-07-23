# Verification and Gate Policy

## Evidence quality

Accept evidence only when it includes the exact command, working directory, relevant environment/resource limits, exit/result, and observed output. A lane summary saying "tests pass" is insufficient.

## Gate order

1. Lane-local checks by implementers.
2. Integrated independent verification by `alaa-verifier`.
3. Failure analysis/fix cycles when needed.
4. Full independent `alaa-reviewer`.
5. Conditional specialist gates.
6. Documentation write lane.
7. Documentation checks and final diff/status reconciliation.

A specialist may run earlier when its purpose is plan pressure-testing, especially architecture critic and test strategist.

## Finding ownership

- Findings are routed verbatim to the lane that owns the behavior.
- Cross-cutting findings become a new serialized lane with an explicit scope.
- Security, migration, or architecture blockers default to `alaa-implementer-sol`.
- The reviewer/specialist never fixes its own finding.

## Maximum cycles

Two fix-review cycles are the default. Verification reruns necessary to evaluate those fixes do not count as extra review cycles. After two unresolved cycles, stop and report options rather than oscillating.

## Documentation gate

Because the documenter writes after code review, documentation changes require at least:

- final diff scope check;
- repository docs formatter/linter when available;
- touched-link validation when available;
- example/config snippet validation when safely supported;
- spot-check against verified behavior.

## Final success criteria

The orchestrator may report completion only when:

- every acceptance criterion maps to evidence;
- no mandatory command is failed, flaky, timed out, blocked, or contaminated;
- reviewer and triggered specialist blockers/majors are resolved or explicitly accepted by the user;
- final touched files match authorized scopes;
- documentation ran or was explicitly skipped for a grounded reason;
- no destructive/external action was performed without authorization.
