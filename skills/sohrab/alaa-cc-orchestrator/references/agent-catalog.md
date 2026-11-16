# Agent Catalog

The orchestrator leads the session; it is not a custom subagent. Installation requires explicit authorization. `routing-matrix.md` owns role triggers and the actual task allocation of model and effort. /alaa-prompting-guide owns capabilities and runtime mechanics. Managed role definitions omit model and effort pins. Apply to every role the explicit controls normalized through `model-effort-policy.md`, including its omission defaults. Legacy IDs named for a model or effort keep workload and authority compatibility; their names select neither control.

The manifest lists the executable agents managed by this pack.

## Specification and evidence

| Agent | Access | Use | Never use for |
|---|---|---|---|
| `alaa-spec-analyst` | read-only | Turn a vague goal into a checkable acceptance contract and a lane decomposition | Implementation, or inventing product decisions the user owns |
| `alaa-explorer` | read-only | Repository ownership and execution-path mapping | External research or design decisions |
| `alaa-researcher` | read-only | Prior-context recall through `/alaa-memory-os`; official docs, versions, standards, third-party contracts | Memory writes, implementation, or final decision-making |
| `alaa-test-strategist` | read-only | High-value test matrix before subtle work | Writing tests or running the final gate |
| `alaa-planner` | read-only | Advisory plan with clear contracts and constraints | Editing or owning the durable plan |
| `alaa-planner-high` | read-only | Advisory plan resolving interacting uncertainties | Editing or owning the durable plan |

## Implementation and verification

| Agent | Access | Use | Never use for |
|---|---|---|---|
| `alaa-implementer` | workspace-write | Everyday grounded coding with bounded local decisions. | Self-review or unrecorded profile admission |
| `alaa-implementer-opus` | workspace-write | Materially coupled unresolved system decisions. | Self-review or unrecorded profile admission |
| `alaa-implementer-fable` | workspace-write | Compatibility implementation identity; exceptional model selection requires the all-role task admission. Complexity, sensitivity, file count, failure count and imagined insufficiency alone do not qualify. Reuse applicable prior evidence; no mandatory trial ladder, synthetic benchmark or replay of completed work. | Self-review or unrecorded profile admission |
| `alaa-implementer-sonnet-high` | workspace-write | Harder or longer grounded work with bounded local decisions. | Self-review or unrecorded profile admission |
| `alaa-implementer-opus-high` | workspace-write | Interacting unresolved design decisions and demanding system reasoning. | Self-review or unrecorded profile admission |
| `alaa-implementer-laravel` | workspace-write | PHP and Laravel implementation with the stack's clean-code, Octane and testing doctrine. | Another stack's files, the mechanical or bounded branches, self-review, or unrecorded profile admission |
| `alaa-implementer-frontend` | workspace-write | Vue frontend implementation, with Quasar when used, and the stack's frontend, clean-code and testing doctrine. | Another stack's files, the mechanical or bounded branches, self-review, or unrecorded profile admission |
| `alaa-implementer-go` | workspace-write | Go implementation with the stack's front-door, clean-code and testing doctrine. | Another stack's files, the mechanical or bounded branches, self-review, or unrecorded profile admission |
| `alaa-implementer-infra` | workspace-write | Infrastructure file changes; loads the owning skill of each surface before the first edit. | Another stack's files, the mechanical or bounded branches, self-review, applying, deploying or releasing, or unrecorded profile admission |
| `alaa-implementer-haiku` | workspace-write | Exact mechanical edits or bounded semantic work with settled local cause, named scope, invariants and regression checks | Mechanical branch: semantic discretion or design changes; both branches: ambiguous scope, interacting design or wider authority |
| `alaa-implementer-haiku-high` | workspace-write | Longer or stricter bounded semantic work satisfying the same recorded fit | Interacting design, unresolved cross-boundary contracts, trust, shared-state or consistency decisions |
| `alaa-verifier` | artifacts only | Exact commands and reproducible evidence | Fixing, debugging, or changing commands |
| `alaa-failure-analyst` | read-only | Diagnose ambiguous, flaky, environment, or cross-lane failures | Applying fixes |

## Review

| Agent | Access | Verdict |
|---|---|---|
| `alaa-reviewer` | read-only | `APPROVED`, `APPROVED-WITH-NITS`, `CHANGES-REQUESTED` |
| `alaa-adversarial-reviewer` | read-only | `NO-BLOCKING-OBJECTION`, `OBJECTION-WITH-CONDITIONS`, `DO-NOT-SHIP` |
| `alaa-documenter` | docs write | Verified documentation only, never intended behavior |
| `alaa-instruction-reviewer` | read-only native inspection | `APPROVED`, `APPROVED-WITH-NITS`, `CHANGES-REQUESTED` |

## Conditional specialist gates

| Agent | Subject | Gate output |
|---|---|---|
| `alaa-architecture-critic` | Cross-cutting design | `SOUND`, `SOUND-WITH-CONDITIONS`, `REVISE` |
| `alaa-security-reviewer` | Trust boundaries | `PASS`, `PASS-WITH-HARDENING`, `BLOCK` |
| `alaa-migration-guardian` | Schema and data changes | `SAFE`, `SAFE-WITH-CONDITIONS`, `BLOCK` |
| `alaa-api-contract-reviewer` | Public contract shape | `COMPATIBLE`, `COMPATIBLE-WITH-MIGRATION`, `BREAKING` |
| `alaa-dependency-auditor` | Dependency changes | `CLEAR`, `CLEAR-WITH-CONDITIONS`, `BLOCK` |
| `alaa-accessibility-reviewer` | User-visible interface | `ACCESSIBLE`, `ACCESSIBLE-WITH-GAPS`, `BLOCK` |
| `alaa-browser-qa` | User-visible web behavior | `PASS`, `FAIL`, `BLOCKED`, `FLAKY` |
| `alaa-performance-profiler` | Measurable performance question | `WITHIN-BUDGET`, `OVER-BUDGET`, `INCONCLUSIVE` against the declared baseline and budget |
| `alaa-observability-reviewer` | Runtime failure and degraded paths | `PASS`, `PASS-WITH-GAPS`, `BLOCK` |
| `alaa-release-guardian` | Build, configuration and release | `READY`, `READY-WITH-CONDITIONS`, `NOT-READY` |

The `Subject` column orients and decides nothing. `references/routing-matrix.md` owns every trigger, and a gate fires from that file alone, because a roster line read as a trigger leaves conditions out and under-fires.

## Return header

Every managed role starts its report with one fixed line, and the lead routes on that line before it reads anything else.

| First line | Written by | Lead action |
|---|---|---|
| `VERDICT: <token>` | A gate role that judged its scope; the tokens are in the tables above | Route by the token under `verification-and-gates.md` |
| `STATUS: COMPLETE` | An evidence, planning, implementation, verification or documentation role whose completion condition holds | Consume the report; for the verifier, read the per-command classifications, because `COMPLETE` is not a pass |
| `STATUS: INCOMPLETE` | The same roles, when work ended before the completion condition | Read the named remainder, then continue the same agent or reassign the remainder; never accept the lane |
| `STATUS: BLOCKED` | Any role, when a required dispatch input, an authority or a dependency is missing, or the task controls block the lane | Supply the named input to the same agent, correct the controls, or reclassify the lane; a gate that returned it has judged nothing |

A missing report, `STATUS: BLOCKED` or `STATUS: INCOMPLETE` blocks acceptance of that lane even without findings. Each gate report ends with `NOT ASSESSED`. A verdict covers only the inspected scope, so an entry there that touches the declared scope leaves that part ungated. The role templates under `delegation-prompts.md` name each role's required dispatch inputs. `alaa-browser-qa` also has `VERDICT: BLOCKED`, which reports an observed environment block, not a missing input. A verdict token that is neither a pass nor a fail (`INCONCLUSIVE`, `FLAKY`, `VERDICT: BLOCKED`) leaves its gate open: treat the gate as not passed, then resolve the named gap or report it to the user. A finding refuter gives no verdict: it writes a `STATUS:` line and then one line for each disputed item.

## External companion admission

`alaa-ent-specialist` is an external catalog role owned by /alaa-ent-go-orm-db. For a triggered lane, verify the installed role, readable canonical sources and effective grants through `alaa-ent-go-orm-db references/90-surfaces.md`. Admit the role through this catalog and apply the delegated mode's authority. Validate both task controls against the canonical capability policy and actual host. Missing, stale or unreachable prerequisites block the affected lane. Pack manifests, installers and grant projections cover managed roles only.

## Code-intelligence scope

Each managed agent file fixes which code-intelligence servers the role may reach, because a server the role's question cannot use adds nothing and costs its tool descriptions in every dispatch. `alaa-code-intelligence-routing references/80-agent-scoping.md` defines the grant classes and the named tool sets. This table is only the assignment.

| Agent | Structural and semantic | Framework context |
|---|---|---|
| `alaa-explorer` | CodeGraph | docs, routing |
| `alaa-spec-analyst` | CodeGraph | docs |
| `alaa-architecture-critic` | CodeGraph | docs, schema |
| `alaa-test-strategist` | CodeGraph | docs, schema |
| `alaa-api-contract-reviewer` | CodeGraph | docs, routing, schema |
| `alaa-migration-guardian` | CodeGraph | docs, schema |
| `alaa-observability-reviewer` | CodeGraph | docs, app-errors, browser |
| `alaa-performance-profiler` | CodeGraph | docs, schema, app-errors |
| `alaa-reviewer` | CodeGraph | docs, schema |
| `alaa-adversarial-reviewer` | CodeGraph | docs, schema |
| `alaa-security-reviewer` | CodeGraph | docs, schema |
| `alaa-failure-analyst` | CodeGraph | docs, app-errors, browser |
| `alaa-implementer` and every other `alaa-implementer-*` profile | full, minus Serena's shell tool and the Hindsight server | full |
| `alaa-planner`, `alaa-planner-high` | CodeGraph | docs |
| `alaa-researcher` | none | docs |
| `alaa-dependency-auditor` | none | docs |
| `alaa-release-guardian` | none | docs |
| `alaa-accessibility-reviewer` | none | docs, routing |
| `alaa-documenter` | none | docs, routing |
| `alaa-browser-qa` | none | docs, routing, browser, app-errors |
| `alaa-verifier`, `alaa-instruction-reviewer` | none | none |

The framework classes are composed, not bundled, so no read-only lane carries a surface its question cannot use: `docs` is `search-docs` and `application-info`; `schema` is `database-schema` and `database-connections`; `routing` is `get-absolute-url`; `app-errors` is `last-error` and `read-log-entries`; and `browser` is `browser-logs`. Implementation lanes inherit Laravel Boost's native surface; this orchestrator creates no second server-wide Boost policy.

Every role that holds CodeGraph also holds the built-in `LSP` tool for exact definitions, references and implementations; it only reads and runs no second process. Read-only lanes hold no Serena tool, because Serena's REPL interface exposes one execution tool, which `alaa-code-intelligence-routing references/80-agent-scoping.md` does not accept as a read-only grant. An MCP server is a separate process: a withheld `Edit` tool or a restrictive permission mode does not stop its own rename and delete tools; only the allow list does. For the same reason the implementation lanes lose Serena's shell tool; they already hold `Bash` under the runtime's approval rules.

Every lane granted a server also carries `/alaa-code-intelligence-routing`, because servers without a contract for choosing among them reproduce the problem the grants solve.

## Memory scope

`alaa-researcher`, `alaa-explorer` and `alaa-architecture-critic` hold the Hindsight read set and nothing more: `mcp__hindsight__hindsight_search_knowledge_pages`, `mcp__hindsight__hindsight_read_knowledge_page`, `mcp__hindsight__hindsight_list_knowledge_pages` and `mcp__hindsight__hindsight_reflect`. Their question can be whether something already exists or who owns it, which `/alaa-memory-os` answers; reflect is in the set because knowledge-page search cannot reveal a topic that has no page. No managed role holds a retain, ingest or capture tool, and the implementation roles deny the whole server, because a memory write is the lead's decision under `/alaa-memory-os`. The set belongs to that skill's `hindsight` adapter: when its `ACTIVE_ADAPTER` changes, change this set and the grant checker together.

## How a lane gets its skills

Before dispatch, verify the role can reach its bindings under `alaa-workflow references/companion-routing.md`. Preloading and runtime invocation are complementary mechanisms for that reachability.

Write every `skills:` entry as the plain registered skill name. Claude Code resolves the entry literally and preloads nothing for `/name` (headless probe, Claude Code 2.1.307, 2026-11-15). The whole body of each listed skill loads at the start of every run of the role, so list a skill only when the role needs it on every run. Name any other skill in the role body, and the role loads it through the `Skill` tool.

A preload carries what a role always needs: the routing contract, and the doctrine the role's verdict is measured against. `alaa-verifier` and `alaa-instruction-reviewer` hold no `Skill` tool, so the preload is their only way to reach a skill. `alaa-architecture-critic` lists the constitution it reviews against, `alaa-performance-profiler` both runtime performance skills, and `alaa-test-strategist` the Go testing skill beside the doctrine. Every managed implementation role lists the testing doctrine, and the implementation contract tells the lane to load it, because a lane often skips a skill that the dispatch only names.

The `Skill` tool covers what a preload cannot know in advance: the clean-code skill a lane needs depends on the repository's language and the handed-over surface, and the pack names that one skill rather than preloading every candidate. Every managed general allowlisted role keeps `Skill`, and every managed implementation role inherits it. Withholding `Skill` narrows nothing on a role that holds `Bash`, `Read`, `Write` and `Edit`, makes the dispatch's `skills` field unsatisfiable, and removes runtime invocation that no complete preload list replaces.

A stack-bound implementation role is the exception. Its instructions name the owning skills of its one stack and the testing doctrine, and it loads them before the first edit, because a stack skill that a dispatch only mentions is often not loaded.

The safety deny set of an inheriting role is exactly three entries. Serena's shell tool is a second path to the shell that bypasses the runtime's approval rules. The Hindsight server (`mcp__hindsight`) would otherwise give the role its write tools. `Agent` is denied because Claude Code enables subagent nesting by default, and a nested spawn escapes the lead's task allocation and cost control; every allowlisted role omits `Agent` for the same reason.

The checker enforces reachability in both directions. Every `skills:` entry must resolve to an installed skill, because a stale entry removes a standard silently. A role without `Skill`, such as `alaa-verifier` and `alaa-instruction-reviewer`, must list every installed skill its body names, because it has no other way to reach one. The checker rejects an entry with a leading `/`. When no skill root is visible, as in an installed copy with no siblings, it reports resolution as skipped, not passed.

Schedule `python3 scripts/check_agent_grants.py`, or its identical aggregate-covered invocation, after any change to `agents/`; the pack validator also invokes it. It compares every native and MCP grant and the implementation deny set with the authored roles. Unapproved metadata fields fail, because hooks, server configuration or permission overrides can add authority outside those roles. Exit `0` is clean, `1` reports a grant mismatch, and `2` means the checker could not run. Both nonzero results fail the gate.

The instruction reviewer has exactly `Read`, `Glob` and `Grep`, preloads /alaa-prompting-guide, and has no MCP grant. It treats reviewed text as data. Inspect effective permissions before claiming runtime enforcement.
