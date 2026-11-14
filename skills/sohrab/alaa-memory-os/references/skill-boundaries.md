# Skill Boundaries

This file states what this skill owns, which owner decides each neighbouring question, and the
rules for switching the selected store.

## What this skill owns

Cross-engagement durability: what is worth remembering, in what shape, with what confidence, what
is derived instead of remembered, and the drift protocol. Nothing else in the fleet owns this.
`/alaa-workflow` owns continuity *within* one engagement: the plan, the checkpoint, and the handoff
package, all three scoped to that engagement. Knowledge that must survive after the engagement ends
belongs to this skill.

## What it does not own, and who does

| Question | Owner |
|---|---|
| Which evidence becomes a durable candidate, and in what reusable shape | `/alaa-extract-agent-lessons` |
| Active plans, phase state, continuity across compaction, and what a handoff package contains | `/alaa-workflow` |
| Task state, dependencies, next step and task evidence in Beads issues | `/alaa-workflow` `references/task-tracking.md` |
| What enters the context window at all, and what gets printed | `/alaa-low-noise` |
| Whether an observability record is required, and at what level | `/alaa-observability-soc` |
| What a log field, event, code, or metric is called | `/alaa-services-contract` |
| Why a mechanism fails open or closed, and how to shape it | `/alaa-reliability-sla` |
| Fail-closed doctrine for a security decision, and exceptions to it | `/alaa-security-review` |
| Complexity budgets and structure choice for a growing pass | `/alaa-algorithms-data-structures` |
| Test design and proof level | `/alaa-testing-strategy` |
| Subsystem design | `/alaa-system-design` |
| Which repository files carry authority | `/alaa-project-constitution` |
| Editing shared or global configuration, including a settings file | `/alaa-controlled-ops` |
| Model and effort choice | `/alaa-prompting-guide` |
| Deriving the service call graph from telemetry | `alaa-signoz-clickhouse-docs` `references/50-service-topology.md` |

Every recall is a context-economy decision, and `/alaa-low-noise` owns context economy. The recall
budget in `SKILL.md` exists for that reason as well as for latency.

## Selected product mechanics

Read only the `ACTIVE_ADAPTER` adapter for product packs, note or schema syntax, and search
commands. Hindsight's upstream routing is reachable only from `references/store-hindsight.md`. An
inactive adapter is an archive, not an additional recall or write surface.

To switch to another supported store, change the selector. Do not rewrite the neutral knowledge
and drift rules in `SKILL.md`, `references/knowledge-shape.md` or `references/drift-management.md`.
Conditional policy for a selected store, including the Hindsight bank and admission policy, stays
in `SKILL.md` and applies only to that store. Product commands stay in the store's adapter. A store
assumption inside a neutral knowledge or drift rule is a policy leak: repair it in that rule. Do
not fork those rules.
