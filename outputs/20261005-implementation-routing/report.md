# Implementation routing tune - verified source change

> Subsequent authorized change: [Codex difficult-role rename](role-rename.md) to `alaa-implementer-astra`, source version 5.0.0. This report records the earlier 4.2.1 routing snapshot.

The paired orchestrators now select implementation roles from unresolved design work, reassess follow-ups, and preserve independent gates. Both source packages are version 4.2.1.

- Base: main at `1c04f0472ee8b09566073cc54861432f94cfcf93`.
- Branch: `codex/tune-implementation-routing`.
- Scope: 21 source paths in the two orchestrator packages; task records in this directory and its archive-index entry.
- Plan: [execution plan](docs/_agent_plans/20261005-implementation-routing.md).
- Source identity: [SHA256 manifest](source-manifest.json); hashes cover the final uncommitted source, not installed agents.

## Changes

The routing matrices own admission. A difficult assignment records its concrete unresolved design decision, named criterion and correctness/failure consequence. Sensitive but settled changes stay with the default role. Failure routing now uses that same admission instead of automatically escalating security, migration and architecture findings.

Follow-up boundaries reassess remaining work. A settled task returns to the default role with a serialized handoff; ordinary progress on the same unresolved design retains its writer. Pipeline-profile escalation remains separate. Agent descriptions, bodies, catalogs and existing dispatch templates consume this rule. IDs, model/effort pins, tool grants, central policies and independent gates are preserved.

## Independent scenario analysis

The instruction reviewer assessed the ten raw cases before reading the plan or source diff. These are hypothetical instruction selections, not live model trials or a quality/cost benchmark.

| Case | Codex / Claude outcome | Deciding fact |
|---|---|---|
| 1 | Default / default | Migration design and rollback are already settled. |
| 2 | Default / default | Critical security fix is precisely specified. |
| 3 | Difficult / difficult | Transaction/acknowledgement ordering has unresolved crash windows. |
| 4 | Default / default | Only specified edits remain after difficult design work. |
| 5 | Retain difficult writer / same | The same justified decision remains open. |
| 6 | Environment owner / same | Docker access failure has not exercised the product; no model upgrade. |
| 7 | Default / default | Approved instruction wording and regeneration procedure. |
| 8 | Difficult / difficult | Ownership/interruption mechanisms still need engineering design. |
| 9 | Documenter / documenter | Documentation-only link change; hardened pipeline remains. |
| 10 | Product decision / same | Retry/discard semantics belong to the product owner. |

## Review and proof

- Independent instruction review: APPROVED after one minor finding. Both catalogs initially excluded all unresolved design; their final cells defer to the matrix's difficult-role admission instead.
- Parent correctness review: approved the final scoped diff and preservation evidence.
- [Initial verification](verification-initial.txt): all 12 dispatched native checks exited zero on the initial 21-path snapshot.
- [Final verification](verification-final.txt): both pack validators, fleet-reference check, skill-pack validator and whitespace check exited zero after the two catalog corrections. Only those two source hashes changed; the other 19 remained identical.
- [Focused checks](focused-checks.md): both contract checks and Codex renderer check passed; controlled generation changed only the manifest.
- All 21 changed source files are LF UTF-8 without BOM. Existing root validators reported warnings/informational records without failures.
- The first workflow validation rejected incomplete skill-source paths and a trailing punctuation token. Those task-record fields were repaired. Final lifecycle validation also required the snapshot to spell out HEAD, SHA256 and paths in its accepted field format; after formatting corrections, final validation passed. No source behavior changed during these artifact repairs.
- Initial native checks have exit/summary receipts but not complete raw output; final affected checks retain separate stdout/stderr logs in the task's host cache.
- A provider capacity error interrupted the implementation lane before source writes. The same role resumed; no model substitution occurred.

## Completion and limits

| State | Verdict |
|---|---|
| IMPLEMENTED | Proven on the recorded source snapshot. |
| MERGE_CANDIDATE | Proven for this local source change by native checks and independent review. |
| RELEASE_CANDIDATE | Not requested. |
| PUBLISHED | Not requested. |

No install, commit, push or model benchmarking was performed. Installed custom-agent definitions were not updated; source validation does not establish runtime activation or serving identity. Preserve the uncommitted tree until an authorized commit. The installed Codex skill is a source symlink, while installed custom-agent TOMLs are separate copies.

Reusable-context curation: the admitted decision was promoted directly into its authorized skill owner. No duplicate memory note or active-task memory was written; Hindsight recall tools were unavailable, and current repository evidence supplied the facts.

## Agent accounting

| Lane | Configured profile | Requested override | Observed identity |
|---|---|---|---|
| routing_spec | gpt-6.1-sol / medium | None | Unknown |
| routing_impl | gpt-6.1-sol / high | None | Unknown |
| routing_review | gpt-6-astra / high | None | Unknown |
| routing_verify | gpt-6-luna / low | None | Unknown |

Four agents, four roles. The implementer applied a settled plan and did not require difficult-role admission; the instruction reviewer uses its fixed specialist profile. Verification: 12 initial commands plus five affected reruns, with four earlier focused checks cited. Workflow-file checks are recorded separately above. Branch span to an authorized commit is unavailable because no commit was requested.