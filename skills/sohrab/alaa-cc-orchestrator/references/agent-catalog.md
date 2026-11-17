# Agent Catalog

`assets/manifest.json` lists the managed agents. A managed role definition carries no model or effort pin, and a role name selects neither. `routing-matrix.md` selects the role and the pair for each dispatch.

## Specification and evidence

| Agent | Access | Use | Never use for |
|---|---|---|---|
| `alaa-spec-analyst` | read-only | Turn a vague goal into a checkable acceptance contract and a lane decomposition | Implementation, or inventing product decisions the user owns |
| `alaa-explorer` | read-only | Repository ownership and execution-path mapping | External research or design decisions |
| `alaa-researcher` | read-only | Prior-context recall through `/alaa-memory-os`; official docs, versions, standards, third-party contracts | Memory writes, implementation, or final decision-making |
| `alaa-test-strategist` | read-only | High-value test matrix before subtle work | Writing tests or running the final gate |
| `alaa-planner` | read-only | Advisory plan draft | Editing or owning the durable plan |

## Implementation and verification

`routing-matrix.md` *Implementation routing* selects the implementation role from the owned files. No implementation role reviews its own work or runs without a recorded admission.

| Agent | Access | Use | Never use for |
|---|---|---|---|
| `alaa-implementer-laravel`, `alaa-implementer-frontend`, `alaa-implementer-go`, `alaa-implementer-haproxy`, `alaa-implementer-delivery` | workspace-write | Stack-bound roles, for every fit row | Another stack's files beyond listed incidental files, self-review; applying, deploying or releasing |
| `alaa-implementer` | workspace-write | A stack with no bound role, or an inseparable two-family lane; the dispatch names the owning skills | A lane that one stack-bound role covers, self-review; applying, deploying or releasing |
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

`routing-matrix.md` *Specialist gates* owns every trigger; a gate fires from that file alone.

| Agent | Gate output |
|---|---|
| `alaa-architecture-critic` | `SOUND`, `SOUND-WITH-CONDITIONS`, `REVISE` |
| `alaa-security-reviewer` | `PASS`, `PASS-WITH-HARDENING`, `BLOCK` |
| `alaa-migration-guardian` | `SAFE`, `SAFE-WITH-CONDITIONS`, `BLOCK` |
| `alaa-api-contract-reviewer` | `COMPATIBLE`, `COMPATIBLE-WITH-MIGRATION`, `BREAKING` |
| `alaa-dependency-auditor` | `CLEAR`, `CLEAR-WITH-CONDITIONS`, `BLOCK` |
| `alaa-accessibility-reviewer` | `ACCESSIBLE`, `ACCESSIBLE-WITH-GAPS`, `BLOCK` |
| `alaa-browser-qa` | `PASS`, `FAIL`, `BLOCKED`, `FLAKY` |
| `alaa-performance-profiler` | `WITHIN-BUDGET`, `OVER-BUDGET`, `INCONCLUSIVE` against the declared baseline and budget |
| `alaa-observability-reviewer` | `PASS`, `PASS-WITH-GAPS`, `BLOCK` |
| `alaa-release-guardian` | `READY`, `READY-WITH-CONDITIONS`, `NOT-READY` |

## Return header

Every managed role starts its report with one fixed line. Route on that line before you read anything else.

| First line | Written by | Lead action |
|---|---|---|
| `VERDICT: <token>` | A gate role that judged its scope; the tokens are in the tables above | Route by the token under `verification-and-gates.md` |
| `STATUS: COMPLETE` | An evidence, planning, implementation, verification or documentation role whose completion condition holds | Consume the report; for the verifier, read the per-command classifications, because `COMPLETE` is not a pass |
| `STATUS: INCOMPLETE` | The same roles, when work ended before the completion condition | Read the named remainder, then continue the same agent or reassign the remainder; never accept the lane |
| `STATUS: BLOCKED` | Any role, when a required dispatch input, an authority or a dependency is missing, or the task controls block the lane | Supply the named input to the same agent, correct the controls, or reclassify the lane; a gate that returned it has judged nothing |

- A missing report, `STATUS: BLOCKED` or `STATUS: INCOMPLETE` blocks acceptance of that lane even without findings.
- Each gate report ends with `NOT ASSESSED`. A verdict covers only the inspected scope, so an entry there that touches the declared scope leaves that part ungated.
- `alaa-browser-qa` also has `VERDICT: BLOCKED`, which reports an observed environment block, not a missing input.
- A verdict token that is neither a pass nor a fail (`INCONCLUSIVE`, `FLAKY`, `VERDICT: BLOCKED`) leaves its gate open: treat the gate as not passed, then resolve the named gap or report it to the user.
- A finding refuter gives no verdict: it writes a `STATUS:` line and then one line for each disputed item.

## External companion admission

`alaa-ent-specialist` is an external role owned by /alaa-ent-go-orm-db. For a triggered lane, verify the installed role, readable canonical sources and effective grants through `alaa-ent-go-orm-db references/90-surfaces.md`, and apply the delegated mode's authority. Validate both task controls against the canonical capability policy and actual host. Missing, stale or unreachable prerequisites block the affected lane. Pack manifests, installers and grant projections cover managed roles only.

## Code-intelligence scope

Each managed agent file fixes which code-intelligence servers the role may reach. `alaa-code-intelligence-routing references/80-agent-scoping.md` defines the grant classes and gives their reasons. This table is the assignment.

| Agent | Structural and semantic | Framework context |
|---|---|---|
| `alaa-explorer` | CodeGraph | docs, routing |
| `alaa-spec-analyst`, `alaa-planner` | CodeGraph | docs |
| `alaa-architecture-critic`, `alaa-test-strategist`, `alaa-migration-guardian`, `alaa-reviewer`, `alaa-adversarial-reviewer`, `alaa-security-reviewer` | CodeGraph | docs, schema |
| `alaa-api-contract-reviewer` | CodeGraph | docs, routing, schema |
| `alaa-observability-reviewer`, `alaa-failure-analyst` | CodeGraph | docs, app-errors, browser |
| `alaa-performance-profiler` | CodeGraph | docs, schema, app-errors |
| Every `alaa-implementer*` role | full, minus Serena's shell tool and the Hindsight server | full |
| `alaa-researcher`, `alaa-dependency-auditor`, `alaa-release-guardian` | none | docs |
| `alaa-accessibility-reviewer`, `alaa-documenter` | none | docs, routing |
| `alaa-browser-qa` | none | docs, routing, browser, app-errors |
| `alaa-verifier`, `alaa-instruction-reviewer` | none | none |

- Framework classes: `docs` is `search-docs` and `application-info`; `schema` is `database-schema` and `database-connections`; `routing` is `get-absolute-url`; `app-errors` is `last-error` and `read-log-entries`; `browser` is `browser-logs`. Implementation lanes inherit Laravel Boost's native surface.
- Every role that holds CodeGraph also holds the built-in `LSP` tool. Read-only lanes hold no Serena tool, and implementation lanes lose Serena's shell tool.
- Every lane granted a server also carries `/alaa-code-intelligence-routing`.

## Memory scope

`alaa-researcher`, `alaa-explorer` and `alaa-architecture-critic` hold the Hindsight read set and nothing more: `mcp__hindsight__hindsight_search_knowledge_pages`, `mcp__hindsight__hindsight_read_knowledge_page`, `mcp__hindsight__hindsight_list_knowledge_pages` and `mcp__hindsight__hindsight_reflect`. Reflect is in the set because knowledge-page search cannot reveal a topic that has no page. No managed role holds a retain, ingest or capture tool, and the implementation roles deny the whole server, because a memory write is the lead's decision under `/alaa-memory-os`. The set belongs to that skill's `hindsight` adapter: when its `ACTIVE_ADAPTER` changes, change this set and the grant checker together.

## How a lane gets its skills

Before dispatch, verify the role can reach its bindings under `alaa-workflow references/companion-routing.md`.

Write every `skills:` entry as the plain registered skill name. Claude Code resolves the entry literally and preloads nothing for `/name` (headless probe, Claude Code 2.1.307, 2026-11-15). The whole body of each listed skill loads at the start of every run of the role, so list only what the role needs on every run: the routing contract, and the doctrine its verdict is measured against. Name any other skill in the role body; the role loads it through the `Skill` tool.

- `alaa-verifier` and `alaa-instruction-reviewer` hold no `Skill` tool, so each lists every installed skill that its body names.
- Every managed implementation role lists the testing doctrine. A stack-bound role also lists the owning skills of its stack, and names in its instructions, as a call with its condition, each skill that only some lanes need, because a lane often skips a skill that the dispatch only names. `alaa-implementer` lists no stack skill: its dispatch names them.
- Every other managed role keeps `Skill`. Withholding it narrows nothing on a role that holds `Bash`, `Read`, `Write` and `Edit`, and it makes the dispatch's `skills` field unsatisfiable.
- An inheriting role denies exactly three entries: Serena's shell tool, which bypasses the runtime's approval rules; the Hindsight server (`mcp__hindsight`), which would give the role write tools; and `Agent`, because nesting is on by default and a nested spawn escapes the lead's task allocation. Every allowlisted role omits `Agent` for the same reason.
- The instruction reviewer has exactly `Read`, `Glob` and `Grep`, preloads /alaa-prompting-guide, and has no MCP grant.

After any change to `agents/`, run `python3 scripts/check_agent_grants.py`; the pack validator also runs it. It compares every native and MCP grant, the implementation deny set and each `skills:` entry with the authored roles, and it fails an unapproved metadata field or an entry with a leading `/`. When no skill root is visible, it reports resolution as skipped, not passed. Exit `0` is clean, `1` reports a grant mismatch, and `2` means the checker could not run. Both nonzero results fail the gate.
