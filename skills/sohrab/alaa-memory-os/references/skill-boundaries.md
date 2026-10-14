# Skill Boundaries

The previous version of this file named four owners and was written before several rounds of fleet rewrites,
so two of its four claims had gone stale. Every claim below states what it depends on, so the next reader can
tell which ones need re-checking.

## What this skill owns

Cross-engagement durability: what is worth remembering, in what shape, with what confidence, what is derived
instead of remembered, and the drift protocol. Nothing else in the fleet owns this. `/alaa-workflow` owns continuity *within* one engagement — the plan, the checkpoint, and the handoff
package — and all three are scoped to that engagement. Knowledge that must survive after the engagement ends
is this skill's.

## What it does not own, and who does

| Question | Owner |
|---|---|
| Which evidence becomes a durable candidate, and in what reusable shape | `/alaa-extract-agent-lessons` |
| Active plans, phase state, continuity across compaction, and what a handoff package contains | `/alaa-workflow` |
| What enters the context window at all, and what gets printed | `/alaa-low-noise` |
| Whether an observability record is required, and at what level | `/alaa-observability-soc` |
| What a log field, event, code, or metric is called | `/alaa-services-contract` |
| Why a mechanism fails open or closed, and how to shape it | `/alaa-reliability-sla` |
| Fail-closed doctrine for a security decision, and exceptions to it | `/alaa-security-review` |
| Complexity budgets and structure choice for a growing pass | `/alaa-algorithms-data-structures` |
| Test design beyond "every assertion needs a red fixture" | `/alaa-testing-strategy` |
| Subsystem design | `/alaa-system-design` |
| Which repository files carry authority | `/alaa-project-constitution` |
| Editing shared or global configuration, including a settings file | `/alaa-controlled-ops` |
| Model and effort choice | `/alaa-prompting-guide` |
| Deriving the service call graph from telemetry | `alaa-signoz-clickhouse-docs` `references/50-service-topology.md` |

## Three corrections to the previous version

**`alaa-low-noise` has two levers, not one.** The retired text described it as owning "bounded terminal and
output discipline, avoiding raw dumps and noisy logs" — the output lever only. It also owns **context
economy**, which governs what enters the context window at all, and that is the more valuable of the two. This
matters directly here: a memory skill that injects recalled text is spending context economy, so the lever the
old boundary statement did not know about is precisely the one this skill consumes. Every recall is a
context-economy decision, and the recall budget in `SKILL.md` exists partly for that reason and not only for
latency.

**"Concise handoff pointers" was a trespass, and the counterpart says so in its own words.** The retired
`compact-and-handoff.md` conceded that `/alaa-workflow` is authoritative for active
execution and then defined a six-field handoff package anyway. `alaa-workflow`
`references/artifact-lifecycle.md` says of exactly that material: "Do not restate them here." That prohibition
is addressed to a sibling file inside `alaa-workflow`; it binds harder across a skill boundary. The two
six-field lists did not even agree, and `alaa-workflow`'s decomposition is the better one.

What survives is one sentence: **the memory store holds a pointer to the plan and its handoff package, and
`/alaa-workflow` owns what the handoff contains.** That file is retired; this sentence
replaces all of it.

**The curation owner was missing from the table entirely.** `/alaa-extract-agent-lessons` routes into this skill for publication and says so in its own step 4, but
nothing here pointed back, so a task could reach publication having never run admission. That is the
shape of omission this file warns about: the rule was already enforced negatively by the do-not-store
list, and the missing half was who produces the storable form.

## Selected product mechanics

Read only the `ACTIVE_ADAPTER` adapter for product packs, note/schema syntax and search commands.
Basic Memory's historical pack inventory is reachable only from `references/store-basic-memory.md`;
Hindsight's upstream routing only from `references/store-hindsight.md`. An inactive adapter is an archive,
not an additional recall or write surface.
