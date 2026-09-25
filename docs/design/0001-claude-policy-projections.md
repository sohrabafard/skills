# 0001 - Claude policy and executable projections

Status: reviewed
Trigger condition: one structured policy adds a validation dependency for executable Claude metadata.
Owner: migration lead; Reviewer: policy_architecture, SOUND after one revision; Date: 2026-09-25
Supersedes: none; Superseded by: none

## 1. Frame

Claude executable profiles must agree with one evidenced policy without changing GPT policy. The affected journeys are profile selection, pack validation and plugin generation.
The constitution archetype signal table has no match for this repository-owned skill library; examples of services do not make the library a service. Existing AGENTS contracts govern it; no constitution is created.

## 2. Scope and boundary

Extend alaa-prompting-guide, the existing model/effort owner. Claude orchestrator and plugin checkers consume its policy; they do not choose pins. Runtime/provider and installed copies are external dependencies, inspected only.
Boundary tests: data stays with the declared policy owner; policy changes and projections are reviewed together; missing policy blocks source validation, while unavailable runtime blocks activation claims only. No new deployable unit or service is needed.

## 3. Contract

Only local file readers/writers and validator commands change. HTTP routes, events, jobs and scheduled triggers: none.
New owner: `skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json`.
Schema v1 accepts these required fields and rejects missing/wrong types and unsupported versions. Unknown keys are rejected at each owned object; an optional `notes` string is permitted for non-normative caveats.

| Object | Exact shape |
|---|---|
| Root | `schema_version`: integer exactly 1 (not boolean); `policy_version`: semantic-version string; `surface`: literal `claude-code`; `verified_on`: real ISO date; `sources`: nonempty array; `models`, `profiles`: nonempty objects |
| Source | `id`: unique nonempty string; `url`: HTTPS URL; `verified_on`: real ISO date; `scope`: nonempty string |
| Model, keyed by exact API ID | `supported_efforts`: unique array drawn from low/medium/high/xhigh/max; `default_effort`: member or null when unsupported; `thinking_mode`: adaptive-always-on, adaptive or extended; `source_ids`: nonempty array referencing source IDs; optional `minimum_claude_code`: semantic-version string backed by those sources |
| Profile, keyed by role ID | `kind`: agent or policy-only; `model`: registered model key; `effort`: supported member or null only for an empty supported list; `rationale`, `escalation_criterion`: nonempty strings; `confidence`: low, medium or high; `calibration_status`: unrun or evaluated; `availability`: object; `source_ids`: nonempty existing source-ID array; `artifacts`: array of repository-relative paths; optional `evaluation_evidence`: repository-relative existing file, required only for evaluated status |
| Availability | `minimum_claude_code`: semantic-version string; `provider_requirement`: nonempty string; `account_status`: literal unknown, since source policy cannot prove account entitlement |

Coverage is closed: exactly `main` (policy-only, artifacts empty), the existing 22 `alaa-*` Claude agent role identifiers and `alaa-rule-writer` (all kind agent). Each orchestrator role maps to its same-name markdown under `skills/sohrab/alaa-cc-orchestrator/agents/`; rule-writer maps to `skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude/alaa-rule-writer.md`. Each agent has exactly one artifact; paths cannot be absolute, escape the repository, duplicate a target, or map a role to another name. Every managed markdown agent is covered and no unknown executable profile is accepted. The existing pack roster remains an independent guard against deleting a profile and file together. Role bodies, grants and description are outside this model/effort projection contract.

CLI integration contract: `python scripts/check_claude_model_policy.py [--policy PATH] [--agent-root PATH ...] [--self-test]` from prompting-guide. Defaults select the canonical policy and both managed agent roots; explicit roots are validated as a selected subset against the same canonical mapping and must contain at least one managed artifact. `--self-test` runs isolated negative fixtures. The agent/package lane invokes this CLI rather than depending on an unspecified Python internal API. A valid policy with mismatching/unknown/duplicate metadata produces exit 1; unreadable files or malformed JSON/YAML produce exit 2; neither can pass a parent gate. No parser fallback silently omits a file.

All profiles start unrun, with no evaluation evidence. Static fixtures may record synthetic observed identity and precedence examples only as contract tests, never as live results. Unknown account/serving facts are explicit, never inferred from configuration. A model without effort support uses null and omits executable effort metadata.
Review correction 1 adds model-level CLI minima so comparator-only models are covered. Assigned profiles require a sourced model minimum and a profile minimum at least as high; verified candidate records enforce both, comparator records enforce their model minimum. A missing model minimum prevents a completed verified comparison/calibration claim; unrun or explicitly blocked work remains representable. Opus, Sonnet and Fable minima are sourced; Haiku has no invented minimum. Malformed or unreadable calibration evidence preserves unavailable-proof exit 2.
Validators compare executable metadata to profiles and check the policy's own types, required evidence and model/effort combinations. Existing checker exits remain 0 clean, 1 findings, 2 unavailable proof; either nonzero blocks dependent completion. Repeating a read-only check is safe; an identical failed retry is not automatic.
Consumers changing: Claude pack/grant/contract validation and rule-writer validation, plus plugin generation only where it projects or checks these inputs. GPT policy and public CLI interfaces remain compatible. Provider deployment names are runtime mappings, not silently accepted policy aliases.

## 4. Data and consistency

The policy lane writes the canonical JSON; the agent lane writes checked model/effort metadata after that schema is frozen. Only those two metadata fields are derived projections. Agent bodies, grants and other metadata remain canonical authored source and are never treated as a reconstructible cache or discarded. Before packaging, projection drift fails validation; a missing/mismatched owner fails closed. Historical migration tables are dated records, never selectors.
Readers access the current local owner directly, without network or shared mutable state. Validation freezes scoped file hashes and rejects concurrent changes. No database, tenant state or distributed consistency is introduced.

## 5. Failure and load

Required local policy and parser dependencies are correctness dependencies: unreadable/malformed input gives unavailable proof or findings, never fallback. Runtime provider access contributes only activation evidence and may remain unknown. Traversal is bounded to declared policy/profile/generated files; cost is linear in their bytes. No broad filesystem scan, service or benchmark is required. First resource bound is finite local file input, not a growing online workload.

## 6. Alternatives

Chosen: one structured owner with checked explicit executable pins. It wins on visible drift and reproducible selection; it costs a maintained checker.
Rejected: rolling aliases plus independent prose tables. It loses on provider/version ambiguity and unchecked duplicated policy; reconsider only if runtime resolution becomes an observed, reproducible deployment contract.
Rejected: generating every agent body from policy. It conflates role authority with model policy; reconsider only if real body duplication requires one canonical contract. Generate only profiles whose shared body has a demonstrated duplication gap.

## 7. Rollout and reversal

Land policy and tests locally, then projections and affected packaging, then independent gates. No installation or publication occurs. Home files and links are not edited; existing skill symlinks expose source changes and that visibility is disclosed separately from stale user-agent copies. Reversal is an authorized source revision; no data migration occurs. Compatibility with older Claude CLIs is not claimed for new full model IDs; activation requires the documented version and account access.

## 8. Open questions

Exact role pins and supported-effort evidence are research-dependent and must be ratified in the plan before implementation. Account eligibility, actual serving identity and comparative gains remain unproven; they block only activation/performance claims. No local fallback is introduced and provider safeguards must remain intact.
