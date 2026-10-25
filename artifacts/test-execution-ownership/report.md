# Test execution ownership migration — 2026-10-26

The local source migration is complete and independently verified. No commit, installation or publication was requested or performed.

## Completed ownership changes

- [Testing strategy](../../skills/sohrab/alaa-testing-strategy/SKILL.md) now owns generic [execution](../../skills/sohrab/alaa-testing-strategy/references/100-test-execution.md), [resources](../../skills/sohrab/alaa-testing-strategy/references/110-execution-resources.md) and [result classification](../../skills/sohrab/alaa-testing-strategy/references/120-result-classification.md). Its four pre-existing test-design doctrines remain preserved.
- Both [Codex](../../skills/sohrab/alaa-codex-orchestrator/SKILL.md) and [Claude](../../skills/sohrab/alaa-cc-orchestrator/SKILL.md) source instructions, roles and templates load that owner. Legacy runner paths forward to canonical testing-strategy runners; orchestrators retain allocation, independence, scheduling and acceptance authority.
- [Workflow integration](../../skills/sohrab/alaa-workflow/references/workspace-and-integration.md) owns per-file, generated-output and shared-resource writers, stopped-writer proof and resume against the same checkout/diff. Disjoint work may share a checkout; worktrees are not created automatically.
- The approved minimal `repository-tooling-capability-check` heading, metadata and both index repairs unblock existing structure gates. A one-paragraph Laravel-upgrade pointer repair follows the separately owned runtime-ops retirement. User work and foreign runtime-ops changes were preserved.

## Verification and limits

[Independent verification 4](verification-4/report.md) records all 19 commands passing, including all six mandatory gates and 12 WSL POSIX runner smoke cases. Runtime fixture counts are 2528 and 2471; each includes the same 1796 shared fixtures and must not be summed as independent coverage. Aggregate checks cover rendered outputs and provider grants. Before/after fingerprints were stable.

[Correctness](correctness-approval.md) and final [instruction review](instruction-review.md) are APPROVED. [Packaging review](release-review.md) is narrowly READY-WITH-CONDITIONS; the required source gates subsequently passed, while installation remains unrequested. The offline workflow validator does not prove live Beads state; the parent separately verified live binding, ownership and readbacks.

This proves source contracts and local POSIX execution. Installed activation, live-agent obedience and native Windows behavior remain unverified. Earlier Windows attempts came from the lead's cross-platform compatibility inference, not a user requirement; WSL IPC and then unsigned UNC script policy stopped them before runner probes. No host settings changed and no further attempt was made. The user's question was not a blanket prohibition; runtime-ops routing now respects its declared scope.

Verified HEAD: `183f5c5a19daaa0c31c5aa41ce8ce2868181aa34`. Task scope: 284 files, SHA-256 `9f25664ba53311cd8fe16a7a8b608835ca5ff07316881edb24bb23963d5dea86`. Broader tested inputs: 2260 files, SHA-256 `847f3c801966d478b1b7c71339f5a701daa48959d42f7145ddd0446423f187c8`. Exact manifests and commands remain in verification 4.

## Further extraction options — proposals only

These five options describe future work; none was implemented in this migration. The orchestrator would retain lane allocation, dependencies, independence, gate scheduling and final verdicts.

| Candidate and current source | Proposed detail owner and what would move | What the orchestrator keeps |
|---|---|---|
| [Communication principles](../../skills/sohrab/alaa-codex-orchestrator/SKILL.md), including length and wording | Existing `alaa-low-noise` and `alaa-prompting-guide`: response economy, wording and compression detail | Required reporting milestones and the instruction to apply the owners |
| [Stage E and documentation gate](../../skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md#stage-e-documentation-and-final-validation) | Existing `alaa-repo-docs`: content, links, examples and size-check procedures; retain its current size-ladder ownership | Final documentation lane, its placement after review and consumption of its gate verdict |
| [Stage A solution choice](../../skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md#stage-a-plan), step 5 | Existing `alaa-system-design` and domain owners: alternatives, representation, access path and complexity decision details | Require a chosen solution before decomposition; schedule independent design judgment |
| [Stage A capability inquiry](../../skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md#stage-a-plan), step 4 | Existing `alaa-memory-os` and `alaa-services-contract`: reusable capability/infrastructure lookup, registry evidence and unknown outcomes | Trigger inquiry before approval; carry its result into allocation and dependencies |
| [Review-boundary commit protocol and Stage F](../../skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md#stage-f-requested-integration) | Existing `alaa-workflow`: commit/integration operational steps, snapshot and base-branch reconciliation details | Enforce explicit authority and passed review/gates before scheduling integration |

When assessing documentation acceptance, read [documentation evidence](docs/evidence.md) for changed-file scope, link checks, classifications, source stability and intentionally unchanged documents. Return to the [upgrade evidence index](../../outputs/README.md).
