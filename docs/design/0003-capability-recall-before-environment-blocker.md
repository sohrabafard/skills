# 0003 - Capability recall before an environment blocker

Status: implemented; independent source verification and scoped reviews passed
Trigger condition: a missing local tool is about to become a validation blocker or another environment repair is considered.
Owner: skill pack maintainer; Review: source, correctness, instruction and security reviews passed; Date: 2026-10-13
Supersedes: none; Related: [0002 infrastructure registry](0002-services-contract-infrastructure-registry.md)

## 1. Problem and evidence

During the gateway Postman refresh, agents repeatedly reported missing local HAProxy or a missing local pinned image as validation blockers under a no-host-install constraint. The user pointed to the existing `ci-image` owner, Nexus image tags and containerized HAProxy. Local inventory was insufficient to establish whether an authorized supported runtime could provide the capability.

This is partly an instruction-compliance problem. The current [memory adapter](../../skills/sohrab/alaa-memory-os/references/store-hindsight.md) already requires capability-oriented `hindsight_reflect` for existence and ownership questions; page-only misses never prove absence. The [memory skill](../../skills/sohrab/alaa-memory-os/SKILL.md) already bounds recall, requires source verification and treats recall failure as missing evidence. This RFC proposes an explicit timing trigger and evidence classification, not a new memory store or a replacement for those rules.

In the current incident, page retrieval produced broad or off-topic leads. Capability-oriented reflection exceeded its current budget, so no within-budget memory answer is established. Independent read-only verification reports remote CI image tags and a remotely available project HAProxy pin. The inspected CI image source does not declare every tool needed by the complete gateway gate. Image pull/run verification is pending at drafting; a registry hit or remembered owner is not executable gate proof. Current findings and later outcomes belong in the gateway workflow record (`../gateway/docs/_agent_plans/20261012-204114_gateway-postman-producer-refresh.md`, relative to this repository root), rather than volatile tags or digests in this proposal.

## 2. Scope and authority

This document is a proposed review artifact. It changes no executable agent rules, installed skills, memory settings, tool grants or repository validation requirements. Original proposal text: a later implementation would select one owning trigger location and route to the existing memory adapter and runtime owner.

Memory remains an untrusted lead. Existing task authorization applies; a recalled remedy grants no permission. No installation, image pull, container execution, remote mutation or configuration change follows automatically from recall. Verify the canonical owner and the permitted next effect before acting. The parent owns any Hindsight lesson and RFC pointer; this draft and raw session content are not published to memory.

## 3. Proposed trigger and bounded procedure

[proposal] Before concluding that a required capability is unavailable from a local-tool miss, check whether current evidence already identifies its owner or supported alternative runtime. Also apply this trigger before an otherwise permitted additional environment repair when ownership remains unknown. Reuse adequate verified evidence; do not recall once per failed command.

[proposal] When the remaining question is existence or ownership, use capability-oriented reflection through the active adapter, even if page search was empty or irrelevant. Supply only the capability, target repository/check, execution environment, constraints, sanitized failure class and evidence already attempted. Do not query only a proposed artifact name.

[proposal] Bound the lookup by the owning skill's current recall budget. Permit at most one focused follow-up on a returned owner lead within that same budget; no fresh budget per paraphrase. A timeout, denied access, irrelevant result or empty answer is no memory evidence. Continue authorized source inspection and unaffected work without claiming global absence. A late response is not retroactive within-budget proof.

[proposal] Inspect the returned canonical owner's current source for tool contents, version/pin location, supported invocation and limitations. Then run a proportionate capability probe only if authorized. Distinguish finding an image, verifying its contents, starting a compatible runtime and completing the exact required gate. Record which stages remain unproven.

[proposal] Return to the runtime owner's cause-specific recovery procedure. Recall does not reset repair/retry budgets. When that budget is exhausted, preserve evidence and stop the failed operation; a new owner lead requires explicit reassessment before dependent work resumes. Preserve the host's native Goal blocked thresholds and distinguish a documented gate blocker from an actual native status transition.

### Capability questions

Use these as proposed question shapes, not fixed tool arguments:

- Which existing owner or supported runtime provides `<capability>` for `<repository/check>` in `<environment>` under `<constraints>`? Which canonical source verifies it?
- Which maintained container/tool image can run the required checks without installing tools on the host? Where are its contents, pins and invocation documented, and which required tools are absent?
- Which owner documents the observed `<sanitized failure class>` for this environment, and does its supported remedy fit the current authorization and remaining retry budget?

Include attempted evidence, for example: local executable absent; Docker reachable or unverified; project image present locally, remote-only or unresolved; relevant owner source inspected or not. Exclude credentials, raw logs, private session text and unrelated user data.

## 4. Evidence classification

| Classification | Evidence needed | Proposed response |
|---|---|---|
| Absent local capability | The required executable/image is missing locally | Inspect a verified owner/runtime lead; do not conclude infrastructure-wide absence. |
| Unavailable compatible infrastructure | Current owner evidence or a permitted capability probe shows the available infrastructure cannot provide this capability in this environment | Report the exact incompatibility and the required external change; do not generalize beyond the inspected scope. |
| Authorization blocker | The next supported effect exceeds current permission | Preserve the concrete proposed action and evidence; obtain only the missing authorization. |
| Tool or runtime error | The selected operation was attempted and returned a grounded failure | Route the exact failure to its owner and respect the remaining recovery budget. |
| Availability unknown | Recall/source/probe is empty, stale, unavailable, denied or unrun | State the uncertainty; continue safe independent work without an absence or success claim. |

A no-host-install constraint alone does not prove every container path is forbidden, and a container lead alone does not authorize a pull or run. Both conclusions require the current task's actual authority.

## 5. Acceptance scenarios used for verification

| Scenario | Required outcome |
|---|---|
| Gateway incident: local HAProxy or pinned image missing | Ask about the needed validation capability; inspect `ci-image` and the gateway's image/pin owner when verified leads exist. Check tool contents separately; do not claim a turnkey full gate from a tag listing. |
| Page search misses; raw reflection returns an owner | The page miss never becomes an absence claim. Inspect the returned owner repository before proposing its runtime. |
| Irrelevant or stale memory | Verify freshness and environment fit; discard unsupported claims without widening to an unbounded search. |
| Empty, denied, unavailable or timed-out memory | Fail open for recall, disclose no memory evidence, and preserve any mandatory validation gap. |
| Remedy requires an unauthorized install, pull or run | No automatic effect occurs; the agent requests only the authorization actually missing. |
| A compatible image starts but lacks a required tool | Report partial capability proof and the exact missing tool; the required gate remains unrun. |
| Repair/retry budget exhausted | Memory produces no extra attempt or budget reset. Preserve failure evidence and request reassessment when needed. |
| Native blocked threshold not met | A gate may be recorded as unresolved, but the native Goal is not marked blocked prematurely or complete while work remains. |

Representative evaluation must include positive and negative cases and compare source-grounded owner discovery, extra tool calls, authorization violations and false blocker/success claims. This RFC reports no evaluation result.

## 6. Draft decisions resolved in implementation

The questions below are retained from the original draft. Their accepted decisions are summarized
in [the implementation plan](../../outputs/20261012-capability-recall/20261012-220000_capability-recall.md#settled-semantic-decisions).

[decision_needed] Choose the single owner for the trigger: memory routing, runtime recovery, or orchestration intake. Other owners should point to it instead of duplicating the procedure.

[decision_needed] Decide how existing lookup evidence is tracked per capability/environment and how the one follow-up shares the owning budget. Define treatment of a late response without extending a completed wait.

[decision_needed] Define the minimum probe proving each capability, particularly local image presence versus remote availability, image contents and actual exact-gate execution. Keep deployment/image pins in their canonical owner, not memory or this RFC.

[decision_needed] Ratify acceptance fixtures and operational reporting before changing a skill. Recheck the incident's final image/run outcome and whether the earlier failure was compliance, missing routing, or both.

## 7. Sources and review boundary

This section records the proposal and its design rationale. For current behavior, the canonical
owners remain `/alaa-memory-os` (capability recall, adapter boundaries and hooks),
the selected memory adapter (store-specific query mechanics), `/alaa-codex-runtime-ops` and the
orchestrators (recovery, retry controls and native lifecycle status), `/alaa-workflow` (active
continuity and task evidence), and `/alaa-extract-agent-lessons` (lesson admission, shaping and
routing). The `[proposal]` and `[decision_needed]` labels preserve the original draft; the design
decisions they record were settled in [the accepted plan](../../outputs/20261012-capability-recall/20261012-220000_capability-recall.md#settled-semantic-decisions).
This RFC does not activate or replace those instructions.

The implementation and evidence are archived in
[the capability-recall report](../../outputs/20261012-capability-recall/report.md). Independent
source verification and scoped reviews passed. Release and publication were not requested.

- [Active adapter and existing recall budget](../../skills/sohrab/alaa-memory-os/SKILL.md).
- [Capability-reflect requirement and page-search limitations](../../skills/sohrab/alaa-memory-os/references/store-hindsight.md).
- [Draft knowledge, source provenance and forbidden memory content](../../skills/sohrab/alaa-memory-os/references/knowledge-shape.md).
- [Runtime recovery owner](../../skills/sohrab/alaa-codex-runtime-ops/SKILL.md).
- [Scoped instruction wording review](../../skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md).
- [Earlier infrastructure-registry RFC](0002-services-contract-infrastructure-registry.md).

The source change is implemented and independently verified within the stated scope. No guarantee
that Hindsight will retrieve the owner, or that a recalled image can run the gate, is made.
