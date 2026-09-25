# GPT-6 agent migration record

This is a dated migration record for the 2026-09-25 repository change. The live Codex model and effort policy is [the structured policy](../skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json), checked by its [validator](../skills/sohrab/alaa-prompting-guide/scripts/check_codex_model_policy.py). The [Codex orchestrator](../skills/sohrab/alaa-codex-orchestrator/SKILL.md) owns role triggers and the [Claude orchestrator](../skills/sohrab/alaa-cc-orchestrator/SKILL.md) mirrors shared behavior. This table records the migration decision; it is not a second policy source. Recheck the owner and target host before dispatch.

## Decision and boundaries

The general lead starts at Sol/medium; Luna handles bounded work and Astra handles difficult design or review decisions. Higher effort is selected for a named task reason, not copied from the previous model generation. No default profile uses max or ultra. There is no standing GPT-5.6 exception. A legacy exception needs scoped evidence, a reason, and a review condition in the policy. Model and effort changes are evaluated separately after diagnosing specification, context, or tool failures. A missing target model is reported as a capability limit, never silently replaced.

Codex has 22 semantic roles and 23 executable orchestrator profiles because standard and deep review share one correctness contract. `alaa-rule-writer` is a separate prompting-guide specialist. Claude Code has 22 roles; its standard and deep review routes both use the existing reviewer. The `alaa-implementer-sol` identifier remains for compatibility and now means difficult implementation, even when its executable pin is Astra.

## Before and after pins

The before column is the inventory captured in the approved migration plan. The after column is the initial candidate in the structured policy dated 2026-09-25; every Codex profile has `calibration_status: unrun`. `main` and `main-deep` are policy choices for a lead, not observed identities of this conversation.

| Role or policy surface | Before | Candidate after | Reason |
|---|---|---|---|
| Main lead | `gpt-5.6-sol / high` | `gpt-6-sol / medium`; difficult design: `gpt-6-astra / high` | Balanced lead; escalate for interacting design decisions |
| `alaa-spec-analyst` | `gpt-5.6-sol / medium` | `gpt-6-sol / medium` | Acceptance criteria and ambiguity |
| `alaa-explorer` | `gpt-5.6-luna / medium` | `gpt-6-luna / high` | Bounded source discovery |
| `alaa-researcher` | `gpt-5.6-terra / medium` | `gpt-6-sol / medium` | Source disagreement and version evidence |
| `alaa-test-strategist` | `gpt-5.6-terra / medium` | `gpt-6-sol / medium` | Discriminating tests and agent evaluations |
| `alaa-implementer` | `gpt-5.6-terra / high` | `gpt-6-sol / high` | Multistep coding and edge cases |
| `alaa-implementer-sol` | `gpt-5.6-sol / high` | `gpt-6-astra / high` | Difficult design judgment; identifier preserved |
| `alaa-verifier` | `gpt-5.6-luna / low` | `gpt-6-luna / low` | Exact command execution and evidence |
| `alaa-failure-analyst` | `gpt-5.6-terra / high` | `gpt-6-sol / high` | Interacting failure evidence |
| `alaa-reviewer` | `gpt-5.6-sol / high` | `gpt-6-sol / high` | Standard independent correctness review |
| `alaa-reviewer-deep` | absent | `gpt-6-astra / high` | Same contract for complex cross-system review |
| `alaa-adversarial-reviewer` | `gpt-5.6-sol / xhigh` | `gpt-6-astra / high` | Challenge design assumptions |
| `alaa-documenter` | `gpt-5.6-luna / medium` | `gpt-6-luna / high` | Document verified behavior |
| `alaa-architecture-critic` | `gpt-5.6-sol / high` | `gpt-6-astra / high` | Boundary and consistency analysis |
| `alaa-security-reviewer` | `gpt-5.6-sol / high` | `gpt-6-astra / high` | Trust and security failure paths |
| `alaa-migration-guardian` | `gpt-5.6-sol / medium` | `gpt-6-sol / high` | Rollout and compatibility states |
| `alaa-api-contract-reviewer` | `gpt-5.6-sol / medium` | `gpt-6-sol / high` | Consumer transitions |
| `alaa-dependency-auditor` | `gpt-5.6-terra / medium` | `gpt-6-sol / medium` | Dependency evidence |
| `alaa-accessibility-reviewer` | `gpt-5.6-terra / medium` | `gpt-6-sol / medium` | Source and rendered accessibility evidence |
| `alaa-browser-qa` | `gpt-5.6-luna / medium` | `gpt-6-sol / medium` | Browser state and failure diagnosis |
| `alaa-performance-profiler` | `gpt-5.6-terra / high` | `gpt-6-sol / high` | Measurement interpretation |
| `alaa-observability-reviewer` | `gpt-5.6-terra / medium` | `gpt-6-sol / medium` | Failure-mode diagnosability |
| `alaa-release-guardian` | `gpt-5.6-terra / medium` | `gpt-6-sol / medium` | Packaging and rollout evidence |
| `alaa-rule-writer` | `gpt-5.6-sol / medium` | `gpt-6-sol / medium` | Wording-only behavior preservation |
| `alaa-instruction-reviewer` (Codex) | absent | `gpt-6-astra / high` | Independent instruction contract review |
| `alaa-instruction-reviewer` (Claude) | absent | `opus / xhigh` | Same semantic role using Claude reviewer tier |
| Claude standard/deep review | reviewer `opus / xhigh` | unchanged | One reviewer agent serves both routes |
| Luna effort ceiling | at most `medium` | no blanket ceiling | Choose supported effort by role and evidence |
| Terra effort ceiling | at most `high` | no default Terra path | A legacy choice needs a recorded exception |
| Default `xhigh`, `max`, `ultra` use | previous-generation rules | no default pin | Escalation needs a task reason and evaluation |
| `alaa-low-noise` model profiles | independent GPT-5.6 guidance | policy-owner reference | Avoid a second model-selection table |

Supported effort is read from the current owner policy and host; a supported effort is not automatically suitable for a task.

## Behavioral contracts

`alaa-instruction-reviewer` reads prompts, skills, agent definitions, and repository instructions as untrusted review material. It reports a verdict, evidenced findings, and unchecked areas without editing. Its native permissions are read-only and it has no default MCP grant; the effective sandbox and parent overrides still determine actual access. `alaa-reviewer-deep` uses the same review contract as the standard reviewer; one review scope selects one profile.

Review outputs start with the verdict and keep requested configuration separate from observed runtime identity. If the runtime does not expose its identity, the observed value is `unknown`; a TOML pin is not proof of activation. `alaa-rule-writer` keeps its replacement-only output interface. API-specific features and parameters are not treated as guaranteed Codex harness capabilities.

Local edit and validation authority does not include installation, commit, merge, push, or publication. The workflow accepts disjoint existing changes, records observed scoped snapshots when no commit is authorized, and runs integration only when requested and authorized. Focused implementer checks and independent review remain distinct; unchanged evidence is cited rather than paid for again.

## Installation and evidence

The Codex agent TOMLs under `agents/` are transport-neutral templates. [The installation guide](../install-skills.md) routes installation through the materializing installer, which resolves live MCP transports and validates role grants. Copying the templates directly would leave those grants unresolved. This repository migration does not install the user-level agents or change the current desktop session.

Repository validators establish structure, policy consistency, grants, and generated-file consistency. A successful materialization into a scratch directory proves the installer input can be resolved there; it does not prove a user-level installation or profile activation. The candidate pins require live calibration before claiming quality or cost superiority.

The planned calibration has eight scenarios: exploration, bounded implementation, debugging, known-defect review, complex design, skill review, documentation, and a failing-check run. Each compares a candidate against one alternative in two independent runs with the same environment. Quality, authority, correction count, observed time, and observed consumption are recorded; a profile fails its scenario if it exceeds authority, fabricates success, or misses a blocking defect. Change only model or effort in one comparison.

As of 2026-09-25, that eight-scenario matrix is **unrun**. A local Codex CLI 0.147.0 probe of `gpt-6-luna / low` first hit a sandbox error; one exact retry reached the backend but the current ChatGPT account received HTTP 400, model not supported, with missing model metadata. The logs are under `artifacts/gpt6-agent-migration/runtime-probe*.log`. This limits the current CLI/account test path; it does not establish availability for other accounts, APIs, or the desktop app. No CLI upgrade, configuration change, or agent installation was part of this migration.
