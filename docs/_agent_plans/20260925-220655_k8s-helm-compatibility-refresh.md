# Workflow Plan - Kubernetes and Helm skill compatibility refresh

- Task ID: `20260925-220655_k8s-helm-compatibility-refresh`
- Mode: `execution`
- Profile: `resumable`
- Status: blocked
- Created: `2026-09-25T22:06:55Z`
- Parent plan: not created
- Prompt pack: `docs/_agent_plans/20260925-220655_k8s-helm-compatibility-refresh__phase-prompts.md`
- Checkpoint: `docs/agents/20260925-220655_k8s-helm-compatibility-refresh-state.md`
- Machine state: not created
- Base branch and commit: main at `12680f2fd18f4a5ac3822cc3cc130b05524053fd`
- Work branch: current `main` checkout; clear scoped ownership, no integration requested
- Worktree: current repository; no additional worktree created

## Summary and Outcome

The user approved one combined Kubernetes/Helm compatibility refresh, handled in a separate chat by one lead. This approval does not expand to the whole modernization inventory. Planning created no skill changes.
At planning, version-awareness.md was dated 2026-07-29 and documented Kubernetes 1.36 and Helm 4.2.0/3.21.0. Execution refreshed that snapshot from official sources dated 2026-09-26, preserving old consumer paths. Source implementation and focused proof completed; three final gates remain blocked as recorded below.

## Scope

- Approved: refresh alaa-k8s-helm version/support guidance, affected commands/examples/references, and bounded checker correctness repairs only if demonstrated necessary.
- Source ownership: skills/sohrab/alaa-k8s-helm/** only.
- Lead ownership: this plan, its prompt/checkpoint companions, artifacts/k8s-helm-compatibility-refresh/**.
- Excluded: other skills, consumers, vendor, indexes, root scripts, manifests, dependencies, installed copies, global/runtime configuration, tool or cluster upgrades, benchmarks and external effects.
- Deferred explicitly: service-runtime-kit-governance and alaa-permission-generator.
- Prior selected normalization/Arvan and W2 plans remain separate; no approval to redo them.
- No model/effort mapping changes; selected lead model is a user preference, not serving-identity proof.

## Handoff Package

- Confirmed facts: unchanged baseline HEAD; installed Helm 4.2.3 and kubectl client 1.36.1; dated official compatibility ledger; eight skill files changed; focused proof and five independent source gates passed on the candidate manifest. Instruction review APPROVED. See artifacts/k8s-helm-compatibility-refresh/final-evidence.md.
- Open assumptions: actual consumer/server versions, installed skill activation, serving identities and effective child enforcement remain unknown. Helm 3/4.3 runtime coverage absent. Correctness review, live checker freshness and workflow completion are blocked; exact failures and recovery actions are recorded in subject evidence.
- Ruled out: forcing latest major onto consumers or using a cluster for documentation discovery exceeds scope.
- Read first on resume: AGENTS.md; skills/sohrab/AGENTS.md; this plan and checkpoint; skills/sohrab/alaa-prompting-guide/SKILL.md; skills/sohrab/alaa-codex-orchestrator/SKILL.md; skills/sohrab/alaa-workflow/SKILL.md; skills/sohrab/alaa-k8s-helm/SKILL.md; references/00-topic-map.md under that skill; all affected references/scripts/metadata; skills/sohrab/caas-arvan-kuber/SKILL.md as read-only dependency.
- Environment notes: PowerShell on Windows; use BelowNormal process priority and python -B. All saved paths are repository-relative.
- Traps: upstream support is different from the authoring compatibility floor; local lint does not prove admission/runtime behavior; successful source edits do not prove installed activation.

## Ordered Work

### Phase 1 - Ground compatibility and preserve behavior

- Status: completed
- Depends on: none
- Owned scope: read-only source/official research and subject evidence.
- Excluded from this phase: source changes and cluster/provider access.
- Work:
  - [x] Revalidate root, HEAD, dirty state, prior execution and GPT/Claude migration completion evidence.
  - [x] Read the complete skill surface before classifying affected instructions.
  - [x] Build a dated compatibility ledger: documented versions, observable consumers/binaries, latest stable/support, proposed range, implications and unknowns.
  - [x] Map affected commands/APIs to versioned official evidence; verify Helm client-library range and major-specific flags rather than extrapolating.
- Acceptance criteria: every concrete proposed correction has evidence; consumer unknowns and breaking decisions are explicit.
- Validation commands: git status --short; git rev-parse HEAD; read-only installed tool version commands only where available.
- Evidence observed: artifacts/k8s-helm-compatibility-refresh/preflight.md and compatibility-ledger.md; writer read complete skill/dependency except dependency OpenAPI governed by its summarizer-only rule. Research established dated official versions, tag-specific flags and source tensions. Three freshness checker defects reproduced in-process before editing.
- Snapshot: HEAD 12680f2fd18f4a5ac3822cc3cc130b05524053fd; SHA-256 c0c05a776e1aa5a8435b251df879986b7cc926d9d71911142bf3e48f4a5590a9; deterministic relative path/content manifest in artifacts/k8s-helm-compatibility-refresh/phase1-manifest.sha256 (57 skill/gate files, method snapshot.py). Phase 1 made no skill source changes.

### Phase 2 - Apply bounded corrections

- Status: completed
- Depends on: Phase 1
- Owned scope: one writer for skills/sohrab/alaa-k8s-helm/**.
- Excluded from this phase: all other skill sources and dependencies.
- Work:
  - [x] Refresh references/version-awareness.md and references/SOURCES.md where necessary.
  - [x] Change only impacted topic references, commands and examples; keep canonical version ownership.
  - [x] Repair scripts/check_versions.py only for an observed defect, with meaningful offline regression fixtures if changed.
  - [x] Record intentional behavior changes separately from behavior-preserving wording.
- Acceptance criteria: preserve namespace/RBAC/security/OpenShift safeguards, API discovery, immutable identity, validation gates, exceptions, failures and completion conditions; no implicit consumer support removal.
- Validation commands: checker --help and --self-test; focused checks derived from changed examples and script contracts.
- Evidence observed: writer/implementation-evidence.md under the subject artifact directory; seven distinct focused commands passed (eight executions after final prose alignment); check_versions self-test 17 cases and check_manifests self-test 7 cases. One diagnostic wording change preserves the externalIPs rejection predicate.
- Snapshot: HEAD 12680f2fd18f4a5ac3822cc3cc130b05524053fd; SHA-256 df86cde6dc83d0486e00a8aedc3325654831659ca88c6272de25539d7e82c8e2; paths skills/sohrab/alaa-k8s-helm/** and four root gate scripts enumerated by artifacts/k8s-helm-compatibility-refresh/candidate-manifest.sha256. Complete source diff: artifacts/k8s-helm-compatibility-refresh/candidate.diff.

### Phase 3 - Independently validate and hand back

- Status: blocked
- Depends on: Phase 2
- Owned scope: read-only reviewers/verifier; lead serializes workflow/evidence updates.
- Excluded from this phase: unselected repairs, installations and runtime activation.
- Work:
  - [ ] Fresh independent instruction/correctness review checks version qualifiers, preserved capabilities, ownership and failure paths.
  - [ ] Execute the validation matrix; preserve unavailable or failed proof as such.
  - [ ] Reconcile findings through the same writer, then rerun only affected checks.
  - [x] Update checkpoint and completion evidence.
- Acceptance criteria: required source gates pass, independent review has no unresolved in-scope blocking finding, runtime limitations remain visible.
- Validation commands: see validation matrix below.
- Evidence observed: instruction-review.md APPROVED; verification-agent/verdict.md records five source gates exit 0; lead chart lint/render/manifest and source-link checks passed. Live freshness returned exit 2 twice. Workflow validator returned exit 1 twice. Correctness-review dispatch failed twice at runtime thread capacity. No third retry or role substitution. See final-evidence.md and blocker records in the subject artifact directory.
- Snapshot: HEAD 12680f2fd18f4a5ac3822cc3cc130b05524053fd; SHA-256 df86cde6dc83d0486e00a8aedc3325654831659ca88c6272de25539d7e82c8e2; paths skills/sohrab/alaa-k8s-helm/** and four root gate scripts in candidate-manifest.sha256; verifier independently matched all 58 hashes before and after execution.

## Sources and Compatibility Targets

Revalidate at execution; these are authoritative entry points, not permission to upgrade:
- https://kubernetes.io/releases/
- https://kubernetes.io/releases/1.37/
- https://kubernetes.io/releases/version-skew-policy/
- https://kubernetes.io/docs/reference/using-api/deprecation-guide/
- https://github.com/helm/helm/releases
- https://helm.sh/docs/topics/version_skew/
- https://helm.sh/blog/helm-v3-end-of-life/

Exact patches, dates, Helm compiled Kubernetes libraries and supported bands must be checked against released tags and official documentation. Preserve explicit consumer-specific version paths. New incompatible support policy requires a separate user decision.

## Validation Matrix and Proof

Run from the repository root:
- python -B skills/sohrab/alaa-k8s-helm/scripts/check_versions.py --self-test
- python -B skills/sohrab/alaa-k8s-helm/scripts/check_versions.py
- python -B scripts/validate_sohrab_skill_pack.py
- python -B scripts/check_skill_index.py
- python -B scripts/check_fleet_references.py
- python -B scripts/check_lifecycle_contract.py
- python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-220655_k8s-helm-compatibility-refresh.md
- git diff --check

Inspect exact script CLI contracts before additional checks. If manifest predicates/examples change, run the available manifest self-tests and local fixture validation. For changed charts/Helm commands, lint/template local fixtures using installed exact Helm versions only. Missing versions mean missing runtime coverage, not permission to install. Read-only official freshness fetch failure is a blocker/unknown, not a stale-version finding or pass. Source gates do not prove cluster admission, runtime activation or consumer compatibility.

## Delegation and Integration

Execution profile: standard, retaining user-requested independent correctness and instruction review.
Decision: preserve the existing authoring floor and older Helm consumer path; extend awareness to the
new stable minor, correct unsupported removal claims, and repair only demonstrated freshness defects.
Reject raising the compatibility floor from upstream support alone or removing support on a calendar date.
The single writer owns skill sources and writer evidence only; lead owns workflow updates.

One lead coordinates one cohesive writer; no parallel writers inside this skill. Use current source role mappings: difficult compatibility/instruction work may use alaa-implementer-sol (configured gpt-6-astra/high); independent alaa-instruction-reviewer and correctness reviewer apply their canonical pins. Revalidate mappings and runtime availability; do not infer observed serving identity. Lead alone writes workflow companions, after writer completion. Reviewers never repair their own findings. No separate documenter is needed because the deliverable is the skill documentation itself.

## Evaluation and Completion

Expected benefit is fewer stale or contradictory version instructions. Validate dated traceability, explicit supported ranges, tested command syntax where tools exist, and preserved safety assertions. Speed/cost/model-quality gains are hypotheses; no benchmark or numerical claim is authorized. No before/after effort table is needed because no mapping changes are selected.

Traceability: approved version verification -> Phase 1; compatibility/example/reference corrections -> Phase 2; preserved Arvan boundary and validation -> all phases, independently gated in Phase 3.

## Authority, Stop Conditions and Recovery

The original chat produced the plan; this execution applied only the selected local implementation. No commit, tag, merge, publication, installation, dependency upgrade, deployment, live cluster/provider operation, benchmark, global configuration or destructive action is authorized.
Preserve unrelated dirty files. On material source drift stop only affected work, explain evidence and resolve the decision. On each failed operation allow one cause-specific repair and one materially different retry; then retain evidence and report the smallest recovery action. Out-of-scope defects are recorded, never silently repaired. Missing migration evidence makes only dependent conclusions provisional.

## Completion and recovery checkpoint

- IMPLEMENTED: proven on the recorded uncommitted content snapshot; preserve the working tree for recovery.
- MERGE_CANDIDATE: not proven; freshness, workflow validation and correctness review remain blocked.
- RELEASE_CANDIDATE: not requested.
- PUBLISHED: not requested.
- Final curation: no additional admitted durable candidates; verified compatibility knowledge is already in its owning skill and volatile run failures remain in evidence. No memory publication or unselected source promotion.
- Recovery order: authorize another workflow-format repair/check; restore approved Python HTTPS reachability before rechecking freshness; authorize a fresh canonical correctness-review dispatch after capacity is available. Reuse unchanged passing evidence and rerun only inputs affected by a subsequent correction.
