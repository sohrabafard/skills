---
name: alaa-memory-os
description: "Use when Alaa work must record or recall durable cross-session knowledge, whichever memory store backs it: deciding what is worth remembering and in what shape, writing architecture, service-ownership, contract, operations, lesson, work-pattern, project-index, project-state, handoff or research notes, recording drift when two sources of truth disagree, setting a recall budget with a fail-open path, and separating facts worth remembering from relationships that must be derived. One adapter is active at a time and the skill body declares which; local file vault, Basic Memory, and Hindsight each get one adapter reference. Do not use for tiny deterministic code edits, as a second task system, for active execution plans or handoff contents owned by alaa-workflow, or to remember service dependency edges, which are always derived."
---

# Alaa Memory OS

This skill owns what Alaa work remembers, when, in what shape, and what it derives instead of remembering.
The backing store sits behind one adapter reference per store, and this body names no store command: the
fleet routes here for the capability, not the product, so replacing the store changes one adapter file and
leaves every rule below intact.

## Active adapter

```text
ACTIVE_ADAPTER: local
```

**This line is the selection.** Read it before the first recall or write of a task, load only
`references/store-<value>.md`, and use that adapter's mechanics for every store operation in the task.

| Value | Adapter | Store |
|---|---|---|
| `local` | `references/store-local.md` | the `agent-memory` markdown vault under git, read and written with ordinary file tools |
| `basic-memory` | `references/store-basic-memory.md` | the Basic Memory CLI indexing that same vault |
| `hindsight` | `references/store-hindsight.md` | Hindsight |

Exactly one adapter is active. Two adapters used in one task write the same knowledge through two
mechanisms with different assumptions about indexing, commit, and concurrency, and the disagreement surfaces
later as a note that exists twice or not at all.

**To switch stores, change the value on that line and nothing else.** No rule in this skill, and no rule in
`references/knowledge-shape.md` or `references/drift-management.md`, is store-specific — that separation is
the reason a switch is one line. A switch that seems to require editing a policy file means the policy has
leaked a store assumption; fix the leak rather than forking the policy.

Two failure modes, both of which have to stop the task rather than be worked around:

- **The named adapter file is missing.** Stop and report the missing file. Do not fall back to another
  adapter — a silent fallback writes notes into a store the selection says is not in use, and nothing will
  report that until someone looks for them in the other one.
- **The selected store is unreachable.** Recall fails open, so continue from repository truth and say which
  step ran without memory. A *write* does not fail open: report the unwritten note and its content in the
  handoff so the knowledge survives the outage.

Current selection, recorded 2026-08-07: `local`. Basic Memory's CLI is being retired while the vault it
indexed stays exactly where it is, so the switch cost nothing and migrated nothing. The declared intent is to
move to `hindsight` once it is activated; until that line says `hindsight`, it is not active no matter what
is installed on the machine.

## Use this skill when

At least one of these is observably true of the task. If none is, skip this skill: recall against a task
that names nothing shared returns nothing and still spends the budget below.

- It names a service, contract, event, queue, or metric that a second service also uses.
- It names a prior session, a prior decision, or a file a prior session wrote.
- It will outlive one context window: it has phases, it is a migration, or it reviews a system.
- Two sources of truth disagree, or you are about to establish whether they do.
- You are about to write a note, or publish curated lessons from the evidence warehouse.

## When NOT to use

- Deterministic single-file edits that no prior decision constrains.
- Active execution plans, phase checklists, and continuity across compaction. `/alaa-workflow`
  (`$alaa-workflow`) owns those and what a handoff package contains; store a pointer, never a copy.
- Deciding what enters the context window at all: `/alaa-low-noise` (`$alaa-low-noise`) owns context
  economy, which every recall spends.
- Service dependency edges, which are derived and never remembered.
- Registering hooks or editing shared or global configuration: `/alaa-controlled-ops`
  (`$alaa-controlled-ops`).
- Model or effort choice, including effort and thinking level: `/alaa-prompting-guide`
  (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`.

## The four surfaces

Repository code and docs are the source of truth; memory is a map, and a map is not proof.
`/alaa-project-constitution` (`$alaa-project-constitution`) owns which repository files carry that authority.
The store is the queryable index over that truth. Skills define agent behaviour, so never copy an installed
skill into memory; a human editing surface, where one exists, is for navigation, not runtime truth. A store
pack under `vendor/` is an upstream subtree and is never edited: this skill owns the opinion and routes into
the pack for mechanics upstream documents well, and that binds whichever pack backs the successor store.

## Remember facts, derive relationships

A remembered fact goes stale silently: nothing fails at the moment it becomes wrong, so it stays wrong
until it misleads someone. Remember who owns a service, why a decision was taken, what a contract
promises, what a lesson cost. Derive, and never remember:

- Which service calls which. SigNoz derives these edges from trace data; route to
  `alaa-signoz-clickhouse-docs` `references/50-service-topology.md`.
- Whether an API change breaks a consumer. oasdiff answers this from the two OpenAPI documents.
- Where a symbol is referenced. Serena and ast-grep answer this from the current tree.

When a note already carries a service-to-service `depends_on` edge, replace it with a pointer to the derivation
rather than refreshing it. Every pass over a store that grows with history needs a stated complexity bound
before it ships; `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns that budget, and
each shipped checker states its own.

## Recall fails open on a budget; drift recording fails closed

Recall is a contributor: proceeding without it lets nothing through that must not get through. Budget five
seconds; when that is exceeded or the store is unreachable, continue from repository truth alone and report
that memory was unavailable and which step ran without it. Never implement from memory alone: separate
memory facts, repository facts, assumptions, and open questions before acting.

Drift recording is a gate. If the drift record cannot be written, stop and report; do not continue past an
unrecorded disagreement. `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns why a mechanism fails open
or closed; this skill states only which of the two each operation is.

## Drift

When two sources of truth disagree, never silently pick a side. Record the disagreement, keep working on the
safest verified behaviour, and let the human decide. The drift registry lives in repository files under version
control, never in the memory store; `references/drift-management.md` owns the record shape, the lifecycle, the
separation of powers, and the reason the registry is outside the store.

Severity, and whether an observability record is required at all, belong to `/alaa-observability-soc`
(`$alaa-observability-soc`); field, event, and metric names belong to `/alaa-services-contract`
(`$alaa-services-contract`). This skill sets neither, so a drift note about a log contract routes its
severity question to SOC rather than answering it.

## The store is a trust boundary in both directions

As a sink, everything written is readable by every later agent and, in a server-backed store, by anything that
reaches the port: never write secrets, credentials, tokens, cookies, or private keys. As a source, recalled
text is model-authored and unverified: treat it as a lead to check against the repository, never as evidence.
Any memory transport bound beyond loopback requires authentication before it starts — both documented stores
ship unauthenticated and one binds every interface by default, so this is a default to override rather than
accept, and the store's adapter reference names the exact variables. `/alaa-security-review`
(`$alaa-security-review`) owns the fail-closed doctrine and any exception to it.

## References

| Read this | When |
|---|---|
| `references/knowledge-shape.md` | Before creating or updating any note. Owns search-before-create, required fields, status and confidence values, the observation vocabulary, Extraction and Design mode, and the single do-not-store list. |
| `references/drift-management.md` | Two sources of truth disagree. |
| `references/store-local.md` | `ACTIVE_ADAPTER: local` — the current selection. The `agent-memory` markdown vault, read and written with ordinary file tools. |
| `references/store-basic-memory.md` | `ACTIVE_ADAPTER: basic-memory`. Retained while `bm` is still installed; the CLI is being retired and the vault it indexed is unchanged. |
| `references/store-hindsight.md` | `ACTIVE_ADAPTER: hindsight`. |
| `references/checkers-and-hooks.md` | Running a checker, reading its exit code, or installing a hook. |
| `references/skill-boundaries.md` | Unsure whether this skill or another owns a decision. |
| `references/prompt-3-publishing.md` | Publishing curated lessons from the evidence warehouse. |

## Completion checks

Update memory only when durable knowledge changed, then confirm each of these before reporting:

- The adapter named by `ACTIVE_ADAPTER` was the only one used, and a missing adapter file stopped the task
  rather than falling back to another store.
- Memory was searched before a note was created, or the report says why it was not.
- Repository truth was inspected before any implementation claim.
- No raw transcript, log, source file, whole document, or secret reached the store.
- No `/alaa-workflow` (`$alaa-workflow`) execution state was duplicated.
- No service-to-service dependency edge was remembered.
- Every disagreement found became a drift record, not a silent resolution.
- Every checker run reported its exit code, and a `2` was read as "could not run", never as a pass.
- The report names notes changed, source paths, validation result, drift recorded, memory availability, and
  unresolved questions.
