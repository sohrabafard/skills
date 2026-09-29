# Workflow Prompt Pack - Remaining skill modernization

- Plan: `docs/_agent_plans/20260926-084940_remaining-skill-modernization.md`
- Verification status: source role pins and official mechanics checked; effective activation unknown
- Verified on: 2026-09-26
- Verification sources: repository alaa-prompting-guide and orchestrator agents; https://learn.chatgpt.com/docs/agent-configuration/subagents ; https://code.claude.com/docs/en/sub-agents
- Implementer runtime/model: Codex / alaa-implementer-sol gpt-6-astra high for shared instruction/compatibility decisions; canonical routine profile for bounded lanes after preflight
- Independent reviewer runtime/model: Codex / alaa-reviewer gpt-6-sol high; alaa-instruction-reviewer gpt-6-astra high
- Documenter runtime/model: not separately dispatched; skill documentation belongs to each writer

## Implementer
**Outcome:** Execute only the phase-owned approved correction.
**Read first:** Plan, checkpoint, full target skill and canonical owners.
**Scope:** Per-skill write allowlist; no research-only source changes.
**Validation:** Focused owner gates and plan acceptance scenarios.
**Done:** Changed behavior and observed proof agree.
**Blocked:** Return exact blocker, preserved evidence and safe recovery.

## Independent reviewer
**Outcome:** Independent correctness, authority and instruction-contract judgment.
**Read first:** Approved scope, actual diff, sources and frozen evidence.
**Scope:** Read-only; never repair reviewed work.
**Validation:** Verify preserved behavior, compatibility, trigger coverage and proof levels.
**Done:** Findings by severity, verdict and evidence limits.
**Blocked:** Name missing decisive evidence without weakening the gate.

## Execution prompt

The runtime-specific prompt exceeds the soft 250-word target to retain the multi-phase scope and permission boundaries.

```text
$alaa-codex-orchestrator

Act as the lead for the remaining first-party skill modernization program. Let alaa-workflow own the multi-phase program and use the orchestrator for owned lanes. Do not perform ordinary implementation in the lead while viable writers exist. User-selected lead model: GPT-6 Astra; observed serving identity remains unknown. Decisions in Persian; saved files in English.

Read first:
- AGENTS.md, skills/sohrab/AGENTS.md and applicable nested instructions.
- docs/_agent_plans/20260926-084940_remaining-skill-modernization.md
- docs/agents/20260926-084940_remaining-skill-modernization-state.md
- docs/_agent_plans/20260926-084940_remaining-skill-modernization__phase-prompts.md
- artifacts/skill-modernization-audit-20260925/audit.md, per-skill.json, inventory.json and versions.md.
- Current repository prompting-guide, workflow and orchestrator sources; all prior checkpoints named in the plan.

Verify root, branch, HEAD, dirty state, content identity and existing work before dispatch. Planning baseline: main at 5d29c92c07bac8bcdc52f1c0c8bd107e5a5d8364, tracked clean; full untracked enumeration had archive permission warnings, so it was not certified complete. Preserve unrelated work. Prior GPT/Claude migrations and normalization/Arvan/W2 are recorded source-complete; compare affected current files with their evidence, never redo them.

Execute the plan's selected local corrections and research, not a blanket rewrite:
1. Bounded closure of the Kubernetes work's remaining freshness/workflow/reviewer gates, without repeating unchanged passing checks.
2. F05/F06/F07 shared-source corrections: Hindsight compatibility guidance, paired orchestrator host-aware mechanics through the canonical owner, and routing consolidation preserving all triggers.
3. Remaining F09 compatibility groups: data-layer, Laravel RabbitMQ, Go, ClickHouse schema/operations, GitLab CI, HAProxy, Ansible validator, Quasar and Shaka.
4. F08 and every remaining Not assessed row: evidence completion only. Assess A instruction design, B domain accuracy and C ownership/packaging separately; classify size and priority independently. New changes discovered here need a concrete user selection before implementation.
5. Independent integration and complete per-skill disposition.

Preserve explicit deferrals: service-runtime-kit-governance, alaa-permission-generator, actual Vector validate/test recovery and prior SigNoz/Vector runtime/activation proof. Their source work must not be reopened. F10 installations and F12 root installation-document changes remain outside scope. No new roles, model/effort remapping, retirement, major consumer migration, or automatic support-floor increase.

The plan's per-skill table is the write allowlist. Read-only research is allowed across the original 69 first-party skills; newly added skills stay outside this program. Read each affected skill fully, including references/scripts/metadata, and narrow domain owners before changes. Shared core edits are one serialized lane. Independent compatibility lanes own disjoint skill directories; lead alone owns workflow/evidence. Keep completed W2 semantics unchanged when touching router layout.

Revalidate time-sensitive facts from official stable release/tag documentation, grouping research by dependency. Separate documented version, observed consumer/binary, latest stable, proposed supported range and migration implications. Unknown consumer facts stay unknown. Public docs do not prove deployed behavior. Preserve version-qualified older support and installed-source authority; stop only affected work on material drift.

Preserve domain depth, security, authority limits, failure handling, exceptions, evidence requirements and completion conditions. Shared invariants remain model-neutral; runtime adaptations stay under prompting-guide. Distinguish intentional correction from behavior-preserving compression. Do not claim quality, speed or cost gains without controlled evidence.

Use canonical roles and independent verification/review; no writer approves its own work. Run focused meaningful tests, relevant owner gates, root structure/index/reference/lifecycle gates, workflow validation and diff checks. Freeze scoped hashes around evidence. Maintain separate source, fixture, runtime, activation and evaluation verdicts. Missing roles/tools/network/provider contracts block only dependent work.

Fresh Kubernetes closure gets one new bounded recovery cycle; each failed operation permits at most one cause-specific repair and one materially different retry, then stop that operation. Never retry the explicitly deferred Vector runtime failure. Preserve gates rather than weakening assertions.

No install, dependency/tool/service upgrade, live benchmark/model comparison, authenticated provider/cluster/production access, external messaging, commit/tag/merge/push/publication/deployment, deletion, global configuration or installed-copy change is authorized. Do not edit root scripts/indexes/manifests/vendor. Record out-of-scope fixes as proposals.

Finish with each of the original 69 skills assigned a truthful disposition, selected corrections and independent evidence, research findings awaiting selection, deferred/blocked work, updated checkpoint and canonical lifecycle verdicts. A finalized program does not imply every item passed or was implemented. Execute no unselected recommendation.
```
