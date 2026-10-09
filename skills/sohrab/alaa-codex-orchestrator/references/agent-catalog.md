# Agent Catalog

The orchestrator leads the session; it is not a custom subagent. Installation requires explicit authorization. Role triggers and actual task model/effort allocation live in `routing-matrix.md`; /alaa-prompting-guide owns capabilities and runtime mechanics. All role definitions omit model and effort pins. Legacy model/effort-named IDs retain workload and authority compatibility; their names select neither control.

The manifest lists the executable agents available in this source pack.

## Specification and evidence

| Agent | Sandbox | Use | Never use for |
|---|---|---|---|
| `alaa-spec-analyst` | read-only | Turn a vague goal into a checkable acceptance contract and a lane decomposition | Implementation, or inventing product decisions the user owns |
| `alaa-explorer` | read-only | Repository ownership and execution-path mapping | External research or design decisions |
| `alaa-researcher` | read-only | Prior-context recall through `/alaa-memory-os`; official docs, versions, standards, third-party contracts | Memory writes, implementation, or final decision-making |
| `alaa-test-strategist` | read-only | High-value test matrix before subtle work | Writing tests or running the final gate |
| `alaa-planner` | read-only | Advisory plan with clear contracts and constraints | Editing or owning the durable plan |
| `alaa-planner-high` | read-only | Advisory plan resolving interacting uncertainties | Editing or owning the durable plan |

## Implementation and verification

| Agent | Sandbox | Use | Never use for |
|---|---|---|---|
| `alaa-implementer` | workspace-write | Normal engineering with grounded scope and acceptance criteria. | Self-review or unrecorded profile admission |
| `alaa-implementer-astra` | workspace-write | Compatibility implementation identity; exceptional model selection requires the all-role task admission. Complexity, sensitivity, file count, failure count and imagined insufficiency alone do not qualify. Reuse applicable prior evidence; no mandatory trial ladder, synthetic benchmark or replay of completed work. | Self-review or unrecorded profile admission |
| `alaa-implementer-high` | workspace-write | Substantial interacting engineering reasoning. | Self-review or unrecorded profile admission |
| `alaa-implementer-luna` | workspace-write | Exact mechanical edits with every fit predicate, or balanced-priority reproduced local bug with traced cause, bounded decisions and regression oracle | Mechanical branch: semantic discretion or design changes; both branches: ambiguous scope, unresolved cross-boundary contracts, trust, shared-state or consistency design, or wider authority |
| `alaa-implementer-low` | workspace-write | Bounded semantic edits with recorded fit and cheap discriminating checks | Unresolved cross-boundary design, consistency or trust |
| `alaa-implementer-luna-high` | workspace-write | Local reproduced bug with traced cause, bounded decisions and regression oracle | Unresolved cross-boundary contracts, trust or shared-state design |
| `alaa-implementer-luna-low` | workspace-write | Bounded local reproduced bug at the canonical cost priority | Self-review, unrecorded admission or wider authority |
| `alaa-implementer-xhigh` | workspace-write | Sustained demanding workhorse reasoning from the batch mapping | Self-review, unrecorded admission or wider authority |
| `alaa-implementer-astra-medium` | workspace-write | Exact official task/priority admission with reasoning need and rejected cheaper/decomposed alternatives | Self-review, unrecorded admission or wider authority |
| `alaa-implementer-astra-xhigh` | workspace-write | Exact official task/priority admission with sustained reasoning need and rejected cheaper/decomposed alternatives | Self-review, unrecorded admission or wider authority |
| `alaa-verifier` | workspace-write (artifacts only) | Exact commands and reproducible evidence | Fixing, debugging, or changing commands |
| `alaa-failure-analyst` | read-only | Diagnose ambiguous, flaky, environment, or cross-lane failures | Applying fixes |

## Review

| Agent | Sandbox | Verdict |
|---|---|---|
| `alaa-reviewer` | read-only | `APPROVED`, `APPROVED-WITH-NITS`, `CHANGES-REQUESTED` |
| `alaa-adversarial-reviewer` | read-only | `NO-BLOCKING-OBJECTION`, `OBJECTION-WITH-CONDITIONS`, `DO-NOT-SHIP` |
| `alaa-documenter` | workspace-write (docs only) | Verified documentation only, never intended behavior |
| `alaa-instruction-reviewer` | read-only native inspection | `APPROVED`, `APPROVED-WITH-NITS`, `CHANGES-REQUESTED` |
| `alaa-reviewer-deep` | read-only | Same correctness contract and verdicts as `alaa-reviewer` |

## Conditional specialist gates

| Agent | Sandbox | Subject | Gate output |
|---|---|---|---|
| `alaa-architecture-critic` | read-only | Public contracts, boundaries, distributed workflow, consistency, caching, concurrency | `SOUND`, `SOUND-WITH-CONDITIONS`, `REVISE` |
| `alaa-security-reviewer` | read-only | Auth, authorization, secrets, untrusted input, uploads, queries, payments, webhooks, crypto, tenancy | `PASS`, `PASS-WITH-HARDENING`, `BLOCK` |
| `alaa-migration-guardian` | read-only | Schema or data changes, backfill, index, cleanup, zero-downtime compatibility | `SAFE`, `SAFE-WITH-CONDITIONS`, `BLOCK` |
| `alaa-api-contract-reviewer` | read-only | Public endpoint, event schema, shared DTO, SDK surface, persisted format | `COMPATIBLE`, `COMPATIBLE-WITH-MIGRATION`, `BREAKING` |
| `alaa-dependency-auditor` | read-only | Dependency added, upgraded, removed, replaced, or lockfile drift | `CLEAR`, `CLEAR-WITH-CONDITIONS`, `BLOCK` |
| `alaa-accessibility-reviewer` | read-only | New or changed user-visible interface | `ACCESSIBLE`, `ACCESSIBLE-WITH-GAPS`, `BLOCK` |
| `alaa-browser-qa` | workspace-write | User-visible web flow, frontend regression, navigation, form, visual behavior | `PASS`, `FAIL`, `BLOCKED`, `FLAKY` |
| `alaa-performance-profiler` | workspace-write | Measurable latency, throughput, CPU, memory, or query regression | Verdict against declared baseline and budget |
| `alaa-observability-reviewer` | read-only | New runtime failure paths, jobs, distributed calls, retries, degraded operation | `PASS`, `PASS-WITH-GAPS`, `BLOCK` |
| `alaa-release-guardian` | read-only | CI/CD, container, config and env, dependencies, packaging, deploy and release | `READY`, `READY-WITH-CONDITIONS`, `NOT-READY` |

The `Subject` column orients and decides nothing: it names what a gate is about so the roster can be
scanned, and it is deliberately shorter than the condition that fires the gate. `references/routing-matrix.md` owns every trigger, and a gate is fired from that file alone — a
roster line read as a trigger under-fires, because the conditions it leaves out are still conditions.

## Code-intelligence scope

Each installed agent receives the narrowest live server grant its question class earns. Servers not
assigned here, including servers unknown to this pack, are disabled in that role.

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
| `alaa-reviewer`, `alaa-reviewer-deep`, `alaa-adversarial-reviewer`, `alaa-security-reviewer` | CodeGraph + Serena read set | docs, schema |
| `alaa-failure-analyst` | CodeGraph + Serena read set | docs, app-errors, browser |
| Every registered implementer profile | full, minus Serena's shell tool | full |
| `alaa-researcher`, `alaa-dependency-auditor`, `alaa-release-guardian` | none | docs |
| `alaa-accessibility-reviewer`, `alaa-documenter` | none | docs, routing |
| `alaa-browser-qa` | none | docs, routing, browser, app-errors |
| `alaa-verifier`, `alaa-instruction-reviewer` | none | none |

The Serena read set and framework classes come from
`alaa-code-intelligence-routing references/80-agent-scoping.md`: `docs` is `search-docs` and
`application-info`; `schema` is `database-schema` and `database-connections`; `routing` is
`get-absolute-url`; `app-errors` is `last-error` and `read-log-entries`; and `browser` is
`browser-logs`. Read-only roles receive only the classes their question requires. Implementation roles inherit Laravel Boost's native surface; this orchestrator does not create a second server-wide Boost policy.

A custom-agent TOML is a configuration layer. Omitting `mcp_servers` inherits the parent, while naming
a server with only `enabled_tools`, `disabled_tools`, or `enabled` is malformed because the table has
no transport. An empty map also does not clear the inherited map. The portable files under `agents/`
therefore carry a materialization marker and no MCP table. The supported installers query
`codex mcp list --json`, preserve each live server's `command` or `url` discriminator, apply this
role's exact allow/deny set, set unassigned servers to `enabled = false`, validate the generated
TOMLs, and record an inventory fingerprint. A changed inventory requires a newly authorized materialization before
dispatch; activation never installs. A catalog server absent from the live inventory remains unavailable rather than being
invented with a machine-specific transport.

Run `python scripts/check_agent_grants.py` after any source-agent change and
`python scripts/check_agent_grants.py --self-test` after changing the checker. Exit `0` is clean,
exit `1` reports a grant mismatch, and exit `2` means the checker could not run; both nonzero results
fail the gate. The pack validator checks the templates, and both installers materialize and validate
the resolved live grants. Plain copies are unsupported because they would inherit the parent grant.

## Memory scope

`alaa-researcher`, `alaa-explorer`, and `alaa-architecture-critic` receive the `hindsight` server
restricted to `hindsight_search_knowledge_pages`, `hindsight_read_knowledge_page`,
`hindsight_list_knowledge_pages`, and `hindsight_reflect`; every other role has it disabled, like any
unassigned server. These are the roles whose question can be whether something already exists or who owns
it, which `/alaa-memory-os` answers; reflect is in the set because knowledge-page search cannot reveal a
topic that has no page. No role holds a retain, ingest, or capture tool, because a memory write is the main
thread's decision under `/alaa-memory-os`. The set belongs to that skill's `hindsight` adapter: when its
`ACTIVE_ADAPTER` changes, change this set and the grant checker together.

## Policy and runtime evidence

Read `model-effort-policy.md` for the canonical policy route and profile precedence. Catalog sandbox/access labels are requested role restrictions; inspect effective sandbox, parent overrides, and MCP permissions before relying on enforcement. Unknown runtime identity or permission state remains unknown.
