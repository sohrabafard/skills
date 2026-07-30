# Skill Boundaries

The previous version of this file named four owners and was written before several rounds of fleet rewrites,
so two of its four claims had gone stale. Every claim below states what it depends on, so the next reader can
tell which ones need re-checking.

## What this skill owns

Cross-engagement durability: what is worth remembering, in what shape, with what confidence, what is derived
instead of remembered, and the drift protocol. Nothing else in the fleet owns this. `/alaa-workflow`
(`$alaa-workflow`) owns continuity *within* one engagement — the plan, the checkpoint, and the handoff
package — and all three are scoped to that engagement. Knowledge that must survive after the engagement ends
is this skill's.

## What it does not own, and who does

| Question | Owner |
|---|---|
| Active plans, phase state, continuity across compaction, and what a handoff package contains | `/alaa-workflow` (`$alaa-workflow`) |
| What enters the context window at all, and what gets printed | `/alaa-low-noise` (`$alaa-low-noise`) |
| Whether an observability record is required, and at what level | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| What a log field, event, code, or metric is called | `/alaa-services-contract` (`$alaa-services-contract`) |
| Why a mechanism fails open or closed, and how to shape it | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Fail-closed doctrine for a security decision, and exceptions to it | `/alaa-security-review` (`$alaa-security-review`) |
| Complexity budgets and structure choice for a growing pass | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Test design beyond "every assertion needs a red fixture" | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Subsystem design | `/alaa-system-design` (`$alaa-system-design`) |
| Which repository files carry authority | `/alaa-project-constitution` (`$alaa-project-constitution`) |
| Editing shared or global configuration, including a settings file | `/alaa-controlled-ops` (`$alaa-controlled-ops`) |
| Model and effort choice | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
| Deriving the service call graph from telemetry | `alaa-signoz-clickhouse-docs` `references/50-service-topology.md` |

## Two corrections to the previous version

**`alaa-low-noise` has two levers, not one.** The retired text described it as owning "bounded terminal and
output discipline, avoiding raw dumps and noisy logs" — the output lever only. It also owns **context
economy**, which governs what enters the context window at all, and that is the more valuable of the two. This
matters directly here: a memory skill that injects recalled text is spending context economy, so the lever the
old boundary statement did not know about is precisely the one this skill consumes. Every recall is a
context-economy decision, and the recall budget in `SKILL.md` exists partly for that reason and not only for
latency.

**"Concise handoff pointers" was a trespass, and the counterpart says so in its own words.** The retired
`compact-and-handoff.md` conceded that `/alaa-workflow` (`$alaa-workflow`) is authoritative for active
execution and then defined a six-field handoff package anyway. `alaa-workflow`
`references/artifact-lifecycle.md` says of exactly that material: "Do not restate them here." That prohibition
is addressed to a sibling file inside `alaa-workflow`; it binds harder across a skill boundary. The two
six-field lists did not even agree, and `alaa-workflow`'s decomposition is the better one.

What survives is one sentence: **the memory store holds a pointer to the plan and its handoff package, and
`/alaa-workflow` (`$alaa-workflow`) owns what the handoff contains.** That file is retired; this sentence
replaces all of it.

## The vendored Basic Memory pack

The pack is an upstream git subtree. It is never edited. This skill wraps it: it owns the opinion about when a
vendored skill applies, and routes into the vendored skill for the mechanics upstream documents well.

**Recommended for normal work** — verified by reading each skill's own frontmatter:

| Path | What it owns |
|---|---|
| `vendor/basic-memory/memory-notes/SKILL.md` | Frontmatter, observations with semantic categories, relations with wiki-links. |
| `vendor/basic-memory/memory-schema/SKILL.md` | Schema definitions, note validation, and schema-versus-usage drift. |
| `vendor/basic-memory/memory-metadata-search/SKILL.md` | Querying notes by custom frontmatter fields. |
| `vendor/basic-memory/memory-capture/SKILL.md` | Capturing a thread into one note, rewritten in place rather than duplicated. |
| `vendor/basic-memory/memory-continue/SKILL.md` | Rebuilding context from the graph when resuming. |

**Gated: use only when explicitly asked.** `memory-ingest`, `memory-reflect`, `memory-defrag`,
`memory-curate`, `memory-lifecycle`, `memory-research`, `memory-tasks`, `memory-ci-capture`, and
`memory-literary-analysis`, each at `vendor/basic-memory/NAME/SKILL.md`. These rewrite, consolidate, or expire
existing knowledge, which is exactly the class of operation that must not run unasked against an audit trail.
`memory-literary-analysis` was missing from the retired list entirely.

Two local opinions the upstream pack does not have, and they are the reason the wrap exists:

- `memory-tasks` is not an execution-state owner in Alaa coding work, and must not duplicate active
  `/alaa-workflow` (`$alaa-workflow`) state.
- The drift detection in `memory-schema` is schema-versus-usage drift, which is metadata maintenance. It is
  not contract drift and does not open a drift record. See `references/drift-management.md`.

**Verify the pack inventory rather than trusting this table**, because a subtree pull changes it:

```bash
find vendor/basic-memory -name SKILL.md | sort
```

That command also exposes a live hazard: the subtree contains a **nested duplicate** directory holding a
subset of the same skills, so some names resolve at two depths. Route to the top-level path only. Installer
paths are owned by `install-skills.md`, not by this file — and that file has pointed at the nested duplicate,
which is why an environment can end up with the subset installed and the rest missing. Check what is actually
installed before assuming a gated skill is unavailable.

## The successor store's pack

Whatever documentation pack backs the successor store is bound by the same rule: vendored, never edited,
wrapped rather than restated. `references/store-hindsight.md` names the pack for the currently documented
successor and routes into it.
