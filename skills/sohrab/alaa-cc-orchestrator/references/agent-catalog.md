# Agent Catalog

The orchestrator is the lead session, not a custom subagent. Every agent below is auto-installed from `agents/*.md` into `~/.claude/agents`. Pins and escalation rules live in `model-effort-policy.md`; triggers live in `routing-matrix.md`.

Twenty-one roles are available. A typical goal fires three to five of them. Breadth here is a menu, not a fleet.

## Specification and evidence

| Agent | Model / effort | Access | Use | Never use for |
|---|---|---|---|---|
| `alaa-spec-analyst` | Opus / high | read-only | Turn a vague goal into a checkable acceptance contract and a lane decomposition | Implementation, or inventing product decisions the user owns |
| `alaa-explorer` | Sonnet / medium | read-only | Repository ownership and execution-path mapping | External research or design decisions |
| `alaa-researcher` | Sonnet / medium | read-only | Official docs, versions, standards, third-party contracts | Implementation or final decision-making |
| `alaa-test-strategist` | Sonnet / high | read-only | High-value test matrix before subtle work | Writing tests or running the final gate |

## Implementation and verification

| Agent | Model / effort | Access | Use | Never use for |
|---|---|---|---|---|
| `alaa-implementer` | Sonnet / high | workspace write | Routine bounded implementation lanes | High-judgment design lanes or self-review |
| `alaa-implementer-opus` | Opus / xhigh | workspace write | Lanes that must themselves make non-obvious design decisions | Routine low-judgment edits |
| `alaa-verifier` | Sonnet / low | artifacts only | Exact commands and reproducible evidence | Fixing, debugging, or changing commands |
| `alaa-failure-analyst` | Opus / high | read-only | Diagnose ambiguous, flaky, environment, or cross-lane failures | Applying fixes |

## Review

| Agent | Model / effort | Access | Verdict |
|---|---|---|---|
| `alaa-reviewer` | Opus / xhigh | read-only | `APPROVED`, `APPROVED-WITH-NITS`, `CHANGES-REQUESTED` |
| `alaa-adversarial-reviewer` | Opus / xhigh | read-only | `NO-BLOCKING-OBJECTION`, `OBJECTION-WITH-CONDITIONS`, `DO-NOT-SHIP` |
| `alaa-documenter` | Sonnet / medium | docs write | Verified documentation only, never intended behavior |

## Conditional specialist gates

| Agent | Model / effort | Trigger | Gate output |
|---|---|---|---|
| `alaa-architecture-critic` | Opus / xhigh | Public contracts, boundaries, distributed workflow, consistency, caching, concurrency | `SOUND`, `SOUND-WITH-CONDITIONS`, `REVISE` |
| `alaa-security-reviewer` | Opus / xhigh | Auth, authorization, secrets, untrusted input, uploads, queries, payments, webhooks, crypto, tenancy | `PASS`, `PASS-WITH-HARDENING`, `BLOCK` |
| `alaa-migration-guardian` | Opus / high | Schema or data changes, backfill, index, cleanup, zero-downtime compatibility | `SAFE`, `SAFE-WITH-CONDITIONS`, `BLOCK` |
| `alaa-api-contract-reviewer` | Opus / high | Public endpoint, event schema, shared DTO, SDK surface, persisted format | `COMPATIBLE`, `COMPATIBLE-WITH-MIGRATION`, `BREAKING` |
| `alaa-dependency-auditor` | Sonnet / high | Dependency added, upgraded, removed, replaced, or lockfile drift | `CLEAR`, `CLEAR-WITH-CONDITIONS`, `BLOCK` |
| `alaa-accessibility-reviewer` | Sonnet / high | New or changed user-visible interface | `ACCESSIBLE`, `ACCESSIBLE-WITH-GAPS`, `BLOCK` |
| `alaa-browser-qa` | Sonnet / medium | User-visible web flow, frontend regression, navigation, form, visual behavior | `PASS`, `FAIL`, `BLOCKED`, `FLAKY` |
| `alaa-performance-profiler` | Sonnet / high | Measurable latency, throughput, CPU, memory, or query regression | Verdict against declared baseline and budget |
| `alaa-observability-reviewer` | Sonnet / high | New runtime failure paths, jobs, distributed calls, retries, degraded operation | `PASS`, `PASS-WITH-GAPS`, `BLOCK` |
| `alaa-release-guardian` | Sonnet / high | CI/CD, container, config and env, dependencies, packaging, deploy and release | `READY`, `READY-WITH-CONDITIONS`, `NOT-READY` |

## Code-intelligence scope

Each agent file fixes which code-intelligence servers that role may reach, because a role that cannot
ask a server's question gains nothing from holding it and pays for its tool descriptions in every
dispatch. `/alaa-code-intelligence-routing` owns the grant classes and the named tool sets;
`references/80-agent-scoping.md` inside that skill is the definition. This table is only the assignment.

| Agent | Structural and semantic | Laravel Boost |
|---|---|---|
| `alaa-explorer` | CodeGraph | docs |
| `alaa-spec-analyst` | CodeGraph | docs |
| `alaa-architecture-critic` | CodeGraph | docs |
| `alaa-test-strategist` | CodeGraph | docs |
| `alaa-api-contract-reviewer` | CodeGraph | inspect |
| `alaa-migration-guardian` | CodeGraph | inspect |
| `alaa-observability-reviewer` | CodeGraph | inspect |
| `alaa-performance-profiler` | CodeGraph | inspect |
| `alaa-reviewer` | CodeGraph + Serena read set | inspect |
| `alaa-adversarial-reviewer` | CodeGraph + Serena read set | inspect |
| `alaa-security-reviewer` | CodeGraph + Serena read set | inspect |
| `alaa-failure-analyst` | CodeGraph + Serena read set | inspect |
| `alaa-implementer`, `alaa-implementer-opus` | full, minus Serena's shell tool | full, minus `tinker` and `record-rule` |
| `alaa-researcher` | none | docs |
| `alaa-dependency-auditor` | none | docs |
| `alaa-accessibility-reviewer` | none | docs |
| `alaa-release-guardian` | none | docs |
| `alaa-documenter` | none | docs |
| `alaa-browser-qa` | none | inspect |
| `alaa-verifier` | none | none |

`docs` is `search-docs` and `application-info` — what the installed framework does, at the version this
project actually has. `inspect` adds the read-only application surfaces: schema, connections, URL
resolution, last error, application log, browser log. `full` is everything Boost registers except
`tinker`, which executes arbitrary PHP, and `record-rule`, which writes into `.ai/rules/` and would let
a lane rewrite the instructions other lanes follow.

Read-only lanes receive Serena tools by exact name rather than the whole server. An MCP server is a
separate process, so a withheld `Edit` tool and a restrictive permission mode do not stop that server's
own rename and delete tools; only the allow list does. The same reason removes Serena's shell tool from
the implementation lanes, which already hold `Bash` under the runtime's own approval rules.

A grant that names a server the project has not installed is inert, not broken. The role answers its
question through native tools and labels the answer partial when a lost server carried a completeness
guarantee.

## How the tiers divide

Opus lanes are the ones that must exercise independent owner-level judgment: leading, reviewing, challenging, and the implementation lanes whose design is not yet decided. Sonnet lanes are the ones with a defined target — apply a ratified decision, run a known check, judge a change against a published standard, capture evidence. The dividing question is never how sensitive the surface is; it is how much of the decision is still open when the lane starts.

Sonnet never runs above `high`. A lane that needs more thinking than that needs Opus instead, and the correct move is to change the model rather than raise the effort. No agent is pinned at `max`; that level exists only as a named per-invocation retry after a documented failure at `xhigh`.

Do not escalate because a command is slow or a goal is important. The verifier stays at `low` while the failure analyst or the escalated implementer handles the difficult reasoning.
