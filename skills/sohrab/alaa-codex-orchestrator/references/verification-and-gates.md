# Verification and Gate Policy

## Evidence quality

Accept evidence only when it includes the exact command, working directory, relevant environment/resource limits, exit/result, and observed output. A lane summary saying "tests pass" is insufficient.

A cited result — one carried forward instead of re-run — additionally names the timestamp of the run and the tree it ran against, and the lane that observed it. `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns the four conditions under which a result stays citable and the rule that the exhaustive tier is never among them.

## Gate order

1. Lane-local focused-tier checks by implementers.
2. Integrated independent affected-tier verification by `alaa-verifier`.
3. Failure analysis/fix cycles when needed.
4. Full independent `alaa-reviewer`.
5. Conditional specialist gates.
6. Documentation write lane.
7. Documentation checks, including the size grade `/alaa-repo-docs` (`$alaa-repo-docs`) requires.
8. Base integrated into the work branch, then exhaustive-tier verification once, on the tree that will land.
9. Final reusable-context curation through `$alaa-extract-agent-lessons` after the evidence is stable.
10. Final diff/status reconciliation, then the integration handshake.

A specialist may run earlier when its purpose is plan pressure-testing, especially architecture critic and test strategist.

## What each execution profile keeps

The profile is chosen in Phase A from the finished plan. It decides how gate 4 is performed and how much ceremony the phases carry. It never decides which specialists fire: gate 5 is conditional at every profile, on the triggers `references/routing-matrix.md` owns and nowhere else. A profile that named the specialists it excludes would be a second copy of that trigger list, and the copy is what goes stale.

| Profile | Gates that run | Gates that do not |
|---|---|---|
| `lean` | every gate, with gate 4 performed by the main thread itself against a diff it did not write rather than dispatched | none by profile |
| `standard` | every gate above, specialists by trigger | none by profile |
| `hardened` | every gate above, plus the architecture critic in Phase A and the adversarial reviewer after gate 5 | none |

Escalation is one-way. A `lean` run whose diff leaves the lane plan, or which turns out to touch a gated surface, becomes `standard` and dispatches `alaa-reviewer` against the complete change before proceeding.

## Gate reopen rule

A repository promotion discovered after evidence was declared stable reopens the owning write lane and every
affected verification, review, documentation, and documentation-check gate. After those gates pass, rerun final
reusable-context curation. Durable memory publication alone does not reopen repository gates.

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
- spot-check against verified behavior;
- the size grade `alaa-repo-docs references/15-document-size-and-clustering.md` requires, measured with `alaa-repo-docs scripts/check_markdown_links.py` in its line-budget mode. Consume that result rather than judging the grade here: its exit `1` on an unapproved document at the largest grade is a failed gate, and its exit `2` proves nothing.

## Final success criteria

The orchestrator may report completion only when:

- every acceptance criterion maps to evidence, each marked run or cited and carrying its tier;
- the exhaustive tier ran once, fresh, on the tree that is being merged, with no integration after it;
- no mandatory command is failed, flaky, timed out, blocked, or contaminated;
- reviewer and triggered specialist blockers/majors are resolved or explicitly accepted by the user;
- final touched files match authorized scopes;
- documentation ran or was explicitly skipped for a grounded reason;
- the final reusable-context pass reported persisted, deferred, rejected, or no admitted candidates;
- no `pipeline reopen required` result remains unresolved;
- every plan checkbox matches what actually landed, and every subtask this run changed carries its commit;
- the integration handshake was presented and the user's answer recorded;
- no destructive/external action was performed without authorization.
