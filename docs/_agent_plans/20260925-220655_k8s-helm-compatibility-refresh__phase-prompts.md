# Workflow Prompt Pack - Kubernetes and Helm skill compatibility refresh

- Plan: `docs/_agent_plans/20260925-220655_k8s-helm-compatibility-refresh.md`
- Verification status: installed role sources matched at execution; instruction review approved; verifier source gates passed; correctness dispatch blocked by runtime capacity. Observed serving identities and effective child enforcement remain unknown.
- Verified on: 2026-09-26
- Verification sources: repository prompting-guide policy and agent sources; https://learn.chatgpt.com/docs/agent-configuration/subagents
- Implementer runtime/model: Codex / configured alaa-implementer-sol gpt-6-astra high; observed identity unknown
- Independent reviewer runtime/model: Codex / canonical alaa-reviewer gpt-6-sol high and instruction reviewer policy; observed identity unknown
- Documenter runtime/model: not used; documentation belongs to the single writer

## Implementer

**Outcome:** Refresh verified Kubernetes and Helm compatibility guidance.

**Scope:** Only the plan-owned skill and workflow artifacts.

**Validation:** Execute the plan validation matrix and preserve unavailable proof.

**Done:** Accepted source corrections, independent review and evidence agree.

**Blocked:** Record the exact unmet gate and recovery action.

## Execution prompt

```text
$alaa-codex-orchestrator

Act as the lead orchestrator for the approved Kubernetes and Helm skill compatibility refresh in this repository. The user selected GPT-6 Astra; do not infer observed runtime identity. Communicate decisions in Persian and write repository artifacts in English. One lead owns this task and delegates a single cohesive implementation lane with independent review.

Read first:
- AGENTS.md and skills/sohrab/AGENTS.md, including applicable nested instructions.
- docs/_agent_plans/20260925-220655_k8s-helm-compatibility-refresh.md
- docs/agents/20260925-220655_k8s-helm-compatibility-refresh-state.md
- docs/_agent_plans/20260925-220655_k8s-helm-compatibility-refresh__phase-prompts.md
- Repository sources of alaa-prompting-guide, alaa-codex-orchestrator, alaa-workflow, and alaa-k8s-helm.
- The complete affected skill, its references, scripts, agent metadata, and the read-only caas-arvan-kuber dependency before changing instructions.

Verify repository root, current HEAD, branch, dirty state, and whether this plan has already been executed. Planning baseline was main at 12680f2fd18f4a5ac3822cc3cc130b05524053fd, with no tracked changes. Preserve all unrelated work. Read current GPT/Claude migration evidence; do not redo either migration. Stop only affected work if baseline drift materially changes compatibility or authority.

Implement only the selected plan. Source writes are limited to skills/sohrab/alaa-k8s-helm/**. The lead may update this workflow family and save evidence under artifacts/k8s-helm-compatibility-refresh/. Other skills, consumers, vendor, installed copies, indexes, manifests, root scripts, model policy, and runtime configuration are excluded. In particular, service-runtime-kit-governance and alaa-permission-generator remain deferred; do not reopen normalization, Arvan, or W2 work.

Revalidate official Kubernetes releases, support/skew/API-deprecation documentation and Helm releases, compatibility and Helm 3 lifecycle documentation. Record dated source URLs and distinguish stable from preview. For each relevant version, separate what the skill documents, what local consumers or binaries demonstrably use, upstream support, and the proposed authoring range. Unknown consumer versions remain unknown. Do not contact a cluster for discovery.

Refresh version-awareness.md and only affected guidance, commands, examples and references. Keep version facts under their canonical owner. Preserve older consumer guidance where still required, using explicit version conditions. A new upstream major never authorizes dropping consumer support. If a breaking policy change is necessary, present the concrete decision and pause that portion. Repair the local freshness checker only if an observed correctness defect requires it, preserving its read-only behavior and gate semantics.

Preserve namespace safety, RBAC, least privilege, OpenShift arbitrary-UID/nonroot handling, resource identity, served-API checks, chart validation, failure handling, and generic Kubernetes versus Arvan ownership. Do not weaken checks or compress away expert exceptions.

Use one owned writer and fresh independent instruction/correctness review under current canonical role mappings; serialize shared workflow writes. Run the plan's offline checker self-test, read-only freshness check, relevant local example/chart checks with installed tools, repository gates, workflow validation and diff checks. Report missing Helm-version runtime coverage explicitly. Distinguish source correctness, installed activation, consumer/runtime proof and measured quality. No performance/cost claim without measurement.

For each failed operation allow at most one cause-specific repair and one materially different retry, then record the blocker and recovery action. Do not weaken assertions to pass. No installation, dependency upgrade, live benchmark, live cluster/provider operation, commit, merge, publication, deployment, deletion or global configuration change is authorized.

Finish with the actual diff, dated compatibility ledger, preserved/changed behavior, independent review verdict, exact passed/failed/unrun/blocked evidence, and updated checkpoint. Execute no unselected recommendations.
```

## Independent reviewer

Read the plan, current instructions, changed sources and decisive evidence independently. Report correctness, instruction-contract and compatibility findings with severity and paths. Preserve unknown runtime coverage. Never edit or weaken assertions. Return a verdict and exact validation limits.

## Documenter (optional)

Not dispatched for this plan; avoid overlapping documentation ownership.
