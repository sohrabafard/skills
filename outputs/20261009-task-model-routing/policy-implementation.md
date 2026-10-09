# Task-selected model controls: policy implementation

Status: scoped implementation complete and frozen for independent review. AGENT alaa-implementer-high; configured/requested GPT-6.1 Sol high; observed identity unknown. Native workspace-write enforcement is known; server-side MCP enforcement unknown. No installation, commit, paid comparison or shared runtime change.

## Implemented contract and decisions

- Both canonical policies use schema 2: Codex policy 2.0.0 and Claude policy 3.0.0. Managed profiles contain only kind, task-selected mode and artifact identity. All 34 Codex and 30 Claude authority roles, including rule-writer, have no role-default model/effort. Main/main-deep remain externally configured, with no implied self-reconfiguration.
- Capability support and source guidance stay in prompting-guide; actual per-task allocation, priority, admission and deliberate departure belong to the runtime orchestrator. The complete OpenAI 27x3 and Claude source tables survive unchanged. Existing model/effort-named role IDs are compatibility names, not selection. No Cartesian role expansion or extra presets.
- Existing projection and validation entry points are retained with deliberately changed schema semantics. Shared validate_task_selection(role, selection, policy, resolved=None) validates BOTH explicit controls and optional realized pair; missing/unsupported/unknown/mismatched resolved controls reject the affected lane. This static API discovers no runtime/account and does not infer observed identity.
- neutral_agent_text(kind,text,profile) removes only parsed executable top-level control keys and verifies authority/body unchanged. Both standalone rule-writer wrappers are neutral with their unchanged contract and read-only grants. The paired writer owns all orchestrator renderers/manifests and was signaled schema-ready before rendering.
- Current sourced mechanics: Codex unpinned roles permit explicit spawn controls; stale pins override them and disk edits do not prove reload. Claude non-fork invocation effort since 2.1.292 is subject to environment/model-force/provider controls. Both requested and resolved controls are distinct from observed serving identity. Unknown serving identity does not require a paid probe when configured resolution is established.
- Standalone delegation, including replacement-only rule-writer, uses the parent's narrow allocation procedure and records explicit controls/reason in a compact dispatch if no durable plan is admitted; no mandatory full pipeline or workflow artifacts solely for selection.
- Calibration moved from role-default status to explicit scenario/task-pair result evidence. Both corpora retain eight concrete comparison designs and unrun status. Claude completed evidence now records and checks model AND effort invocation/precedence, non-fork support, minima, mismatch and fallback. No numeric savings or model superiority is claimed.

## Ownership and compression

The intentional contract change was drafted before wording compression. The rewrite retains each role's authority, permissions, tools/skills and verdict responsibility; both explicit control requirements; stale/forced/unsupported blocked cases; and source caveats. Main-session controls remain external. Removed role-pin rationales/calibration are intentional behavior changes, not compression omissions. Runtime orchestrator references now own allocation/admission instead of a second decision algorithm here.

Necessary root/pack ownership clauses were corrected. Parent-authorized follow-up fixes five exact inbound clauses in services-contract, golang refs05, security-review, reliability-sla and testing-strategy; no domain behavior changed. Other generic 'load prompting-guide' routes remain truthfully transitive through its owner handoff. No unrelated Go/runtime configuration edit.

Body word count: 873 -> 935. Added material is explicit task-control validation and standalone realization boundaries. Policies shrink by removing role-default selection machinery; complete evidence tables retained.

## Focused observed verification

All commands below ran from skills/sohrab/alaa-prompting-guide, with python -B, normal lightweight processes and no CPU-heavy suite. Each returned exit 0 after final code/fixture changes:

- python -B scripts/check_codex_model_policy.py --self-test: 34 roles, distinct pairs, missing/unsupported controls, effective mismatch, missing-role coverage and stale-pin rejection.
- python -B scripts/check_claude_model_policy.py --self-test: 38 schema/parser fixtures plus 30 all-role explicit-control/pin/coverage cases.
- python -B scripts/profile_projection.py --self-test: all-role TOML/YAML neutral projection, idempotence, authority/body preservation, fixed/ambiguous control rejection.
- python -B scripts/check_agent_evals.py --self-test: task-pair corpus flexibility, missing controls, single-factor comparisons and result completeness/identity fixtures.
- python -B scripts/check_claude_agent_evals.py --self-test: task-pair corpus, both control precedence, non-fork boundary, model minima, forced/effort mismatch, fallback and malformed-evidence exit fixtures.
- python -B scripts/check_rule_writer_grants.py --self-test: green source shape and 12 red fixtures, stale frontier pins in both runtimes, bounded grants and unchanged loaded contract.
- python -B scripts/check_rule_writer_grants.py: real neutral wrappers, contract parity and read-only grants passed.

A local edit script initially read UTF-8 through CP1252. One cause-specific retry used explicit UTF-8; introduced mojibake was repaired only in touched inputs. Final targeted search found no such corruption; no broad encoding cleanup. No verification gate failed.

Root scoped git diff --check over the 38 owned source paths also returned exit 0; only existing Git line-ending notices.

Parent owns independent aggregate structure/fleet/grant/authority review and actual installed/control realization. These focused checks prove source contracts, not activation, account availability or live model quality. No affected/exhaustive gate or model call was run by this lane.

## Frozen source handoff

No source blocker remains. The current chat registry remains stale/fixed; installing/reloading source is outside this lane and was not performed. If an actual target cannot realize both selected controls, only an available exact verified compatibility realization or a blocked affected lane is allowed. Preserve independent ready lanes.

Source snapshot algorithm: sorted UTF-8 relative path + NUL + file bytes + NUL, SHA-256 `c840013f171a9d3c037e8667e44ad06a9e04138f6903c3dd25c21b07275b3f7b`; 38 owned source files, excluding this progress record.

Changed owned source paths:

- `AGENTS.md`
- `skills/sohrab/AGENTS.md`
- `skills/sohrab/alaa-golang/references/05-what-this-skill-does-not-own.md`
- `skills/sohrab/alaa-prompting-guide/SKILL.md`
- `skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json`
- `skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json`
- `skills/sohrab/alaa-prompting-guide/assets/evals/agent-comparisons.json`
- `skills/sohrab/alaa-prompting-guide/assets/evals/claude-agent-comparisons.json`
- `skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude/alaa-rule-writer.md`
- `skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex/alaa-rule-writer.toml`
- `skills/sohrab/alaa-prompting-guide/assets/rule-writer/dispatch.md`
- `skills/sohrab/alaa-prompting-guide/references/00-topic-map.md`
- `skills/sohrab/alaa-prompting-guide/references/11-codex-runtime-features.md`
- `skills/sohrab/alaa-prompting-guide/references/12-gpt-6.md`
- `skills/sohrab/alaa-prompting-guide/references/21-opus-5-5.md`
- `skills/sohrab/alaa-prompting-guide/references/31-sonnet-5-5.md`
- `skills/sohrab/alaa-prompting-guide/references/36-haiku-5-5.md`
- `skills/sohrab/alaa-prompting-guide/references/41-claude-code-runtime-features.md`
- `skills/sohrab/alaa-prompting-guide/references/42-fable-5-1.md`
- `skills/sohrab/alaa-prompting-guide/references/50-effort-and-thinking.md`
- `skills/sohrab/alaa-prompting-guide/references/80-subagent-authoring.md`
- `skills/sohrab/alaa-prompting-guide/references/90-model-selection.md`
- `skills/sohrab/alaa-prompting-guide/references/92-agent-evaluation.md`
- `skills/sohrab/alaa-prompting-guide/references/93-claude-evaluation.md`
- `skills/sohrab/alaa-prompting-guide/scripts/check_agent_evals.py`
- `skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py`
- `skills/sohrab/alaa-prompting-guide/scripts/check_claude_model_policy.py`
- `skills/sohrab/alaa-prompting-guide/scripts/check_codex_model_policy.py`
- `skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py`
- `skills/sohrab/alaa-prompting-guide/scripts/claude_model_policy.py`
- `skills/sohrab/alaa-prompting-guide/scripts/codex_model_policy.py`
- `skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/policy-cases.json`
- `skills/sohrab/alaa-prompting-guide/scripts/profile_projection.py`
- `skills/sohrab/alaa-prompting-guide/scripts/task_model_controls.py`
- `skills/sohrab/alaa-reliability-sla/SKILL.md`
- `skills/sohrab/alaa-security-review/SKILL.md`
- `skills/sohrab/alaa-services-contract/SKILL.md`
- `skills/sohrab/alaa-testing-strategy/SKILL.md`

## Parent integration delta after lane freeze

The recorded 38-file lane hash is historical. Parent later corrected the same ownership row in `alaa-repo-docs/SKILL.md` and repaired the new unconditional parser import in `scripts/profile_projection.py`. Its optional stdlib/backport/strict-source fallback passed the changed self-test. Independent release review verified both renderers with both parser imports masked; see `release-review.md`. Final combined source hashes belong to the independent verification record.
