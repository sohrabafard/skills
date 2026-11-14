---
name: alaa-memory-os
description: "Durable cross-session memory policy for Alaa work, whichever memory store backs it. Use when work must record or recall durable cross-session knowledge: deciding what to remember and in what shape; architecture, ownership, contract, operations, lesson, project, handoff or research notes; whether information belongs in the memory store, a Beads hub reminder or Beads issue notes; drift between sources of truth; fail-open recall budgets; and capability recall before a local-tool miss becomes a validation blocker or a permitted environment repair has an unknown owner. One adapter is active at a time; the local file vault and Hindsight each get one adapter reference. Do not use for tiny deterministic edits, as a second task system, for active plans or handoff contents owned by alaa-workflow, for candidate admission owned by alaa-extract-agent-lessons, or for service dependency edges, which are always derived."
---

# Alaa Memory OS

This skill owns what Alaa work remembers, when, in what shape, and what it derives instead of remembering.
Each backing store has one adapter reference. This body names no store command of a memory adapter;
Beads surfaces are outside the adapter. Reason: the fleet routes here for the capability, not the product.

## Active adapter

```text
ACTIVE_ADAPTER: hindsight
```

Valid values are `local` and `hindsight`. No other store exists.

**This line is the sole selection.** Before a task's first recall or write, load
`references/store-<value>.md`. Use only its mechanics for memory store operations. A format-only section
that the adapter explicitly routes to shares serialization only; it grants no adapter activation and no
operation authority.

Exactly one adapter is active. Reason: two adapters write the same knowledge under different indexing, commit and
concurrency assumptions, and their disagreement later leaves notes duplicated or missing.

Before you change the selector, or edit an adapter, a store-conditional policy, or a neutral knowledge or drift rule, read
`references/skill-boundaries.md`. It owns the store-switch rules.

Handle these two failures separately. Never switch adapters to work around either one:

- **Missing named adapter file:** stop and report it. Never fall back. Reason: a silent fallback writes to an
  unselected store, unnoticed until someone searches the other store.
- **Unreachable selected store:** recall fails open. Continue from repository truth and name each step that ran
  without memory. Writes do not fail open. Report the unwritten note and its content in the handoff, so the
  knowledge survives the outage.

Record activation evidence and temporary ingestion restrictions in the selected adapter or in the owning
repository checkpoint. Never record them as a second selection sentence.

## Use this skill when

At least one condition must be observable. Otherwise skip this skill. Reason: a recall that names nothing
shared returns nothing and still spends the budget below.

- The task names a service, contract, event, queue, or metric that a second service also uses.
- It names a prior session, a prior decision, or a file that a prior session wrote.
- It outlives one context window: phases, migration, or system review.
- Two sources of truth disagree, or you are about to establish whether they do.
- It asks whether existing infrastructure, another repository, or a prior decision already provides a capability, or who owns it.
- A local-tool miss is about to become a required validation blocker, or an otherwise permitted additional
  environment repair has an unresolved owner. Reuse sufficient fresh capability evidence instead of
  repeating recall for each failed command.
- You are about to write a note, or publish curated lessons from the evidence warehouse.
- You are about to write a Beads hub reminder (`bd remember`), or to decide whether information belongs in the memory store, a hub reminder or issue notes.

## When NOT to use

- A deterministic single-file edit that no prior decision constrains.
- Active execution plans, phase checklists and compaction continuity. `/alaa-workflow` owns these and the
  handoff contents. Store a pointer to them, never a copy.
- Deciding what enters context: `/alaa-low-noise` owns context economy, which every recall spends.
- Service dependency edges: derive them, never remember them.
- Registering hooks or editing shared or global configuration: `/alaa-controlled-ops`.
- Model or effort choice, including the effort or thinking level: `/alaa-prompting-guide` `references/50-effort-and-thinking.md`.

## The four surfaces

Repository code and documentation are truth. Memory is a map, not proof. `/alaa-project-constitution` owns
which repository files carry authority. Skills define agent behaviour, so never copy an installed skill into
memory. A human editing surface is navigation, not runtime truth. Never edit an upstream store pack under
`vendor/`. This skill owns the opinion and routes to the mechanics that upstream documents, including the
pack that backs any successor store.

## Remember facts, derive relationships

Remembered facts go stale without failure and stay wrong until they mislead. Remember service owners,
decision reasons, contract promises and lesson costs. Derive these, never remember them:

- Service call edges. SigNoz derives them from traces; route to `alaa-signoz-clickhouse-docs` `references/50-service-topology.md`.
- API consumer breakage. oasdiff compares the two OpenAPI documents.
- Symbol references. Serena and ast-grep inspect the current tree.

Replace existing service-to-service `depends_on` edges with derivation pointers. Do not refresh them.

## Recall policy and capability inquiry

Recall contributes. It is neither a gate nor a source of authorization. Ordinary recall has a five-second
budget. An existence or ownership inquiry has a sixty-second budget, which includes at most one focused
follow-up on a returned owner lead. Start one deadline before the initial inquiry. Paraphrasing or following
a lead never resets it. Before any new lookup, reuse sufficient fresh evidence for the same capability,
environment and constraints.

For an existence or ownership inquiry, query the capability through the selected adapter, not only a proposed
artifact name. Page search and page listing miss knowledge that has no page. Empty or irrelevant page results
never prove absence. Supply the required capability, the target repository or check, the execution
environment, the constraints, the sanitized failure class and the evidence already attempted. Exclude raw
logs, credentials, private session text and unrelated user data.

A timeout, an unreachable store, denied access, and an empty, irrelevant or stale answer are not memory
evidence. Continue authorized inspection of canonical sources and unaffected work. Disclose each step that ran
without memory. A late response is not retroactive proof within the budget. Before acting, separate recalled
claims, repository facts, assumptions and open questions. Never implement from memory alone.

Verify each useful lead in the current owning repository: the tool contents, the version or pin source, the
supported invocation, the environment fit and the limitations. Only then probe proportionately within existing
authority. Distinguish four stages: image or registry discovery, contents verification, a compatible runtime
start, and completion of the exact required gate. Each stage needs observed evidence. An earlier stage proves
no later stage. When the workflow has admitted durable state, keep the capability, environment, constraints, owner or source, and
attempted evidence in the workflow-owned record, never as a second task state in memory.

| Classification | Evidence and response |
|---|---|
| Local capability absent | A local executable or image is missing. Inspect a verified owner or runtime lead; never infer that the capability is absent across the infrastructure. |
| Compatible infrastructure unavailable | Current owner evidence or an authorized probe establishes that the environment is incompatible. Report that scope and the required change. |
| Authorization blocker | The supported next effect exceeds permission. Preserve the concrete action and its evidence; obtain only the missing authority. |
| Tool or runtime error | An attempted operation returned a grounded failure. Return it to its recovery owner with the remaining retries. |
| Availability unknown | Recall, source inspection or a probe is stale, empty, unavailable, denied or unrun. Preserve the uncertainty; continue independent safe work. |

A no-host-install constraint alone does not forbid every container path. A container lead alone authorizes
no pull and no run. Recall grants no effect, resets no repair or retry budget, and bypasses no native blocked
threshold. When that budget or the native blocked threshold is exhausted, preserve the evidence and stop the failed operation. A new owner lead
requires an explicit reassessment before dependent work resumes. Distinguish a documented gate blocker from an
actual native status transition. Never infer a host status change from a classification written in prose.

## Drift and stale memory

Current canonical repository evidence wins over memory. A memory-only contradiction is a stale note, not
canonical-source drift. A stored caution or prohibition whose stated reason no longer holds is also a stale
note, and its correction may set its `status` to `archived` through the selected adapter. Correct a stale
note only with write authority. Otherwise defer the correction with a source pointer. When canonical sources
disagree, record the mismatch without silently deciding it. Continue only on the safest verified behavior.
Drift recording is a gate: if the required repository record cannot be written within authority, stop
dependent work and report the unwritten record.

`references/drift-management.md` owns the registry shape, the lifecycle and the separation of powers. Keep
the registry in version-controlled repository files outside recall, so store synthesis cannot erase a
disagreement. `/alaa-reliability-sla` owns fail-open and fail-closed doctrine.

## Write authority and outcomes

Activation grants no memory write, migration, configuration, installation, commit or external effect.
Before durable publication, apply /alaa-extract-agent-lessons to evidence-derived candidates, and apply
`references/knowledge-shape.md` for search-before-create, note shape and prohibited content. Write only
through the selected adapter, and only after the task authorizes the destination and the effect. Report a
write as completed only after the adapter's terminal confirmation. Report each other outcome by name:
deferred (not authorized), failed, unavailable, or empty (no admitted note). Preserve admitted but unwritten
candidates in the workflow-owned handoff. Do not claim persistence. Never switch stores silently.

When Hindsight is selected, Alaa policy requires project-scoped adoption and one explicitly configured fixed
bank shared across services. Services on that bank are distinguished by service provenance, never by a bank
per harness or per repository. Admission covers only the current repository, never a parent path. Real-data
ingestion and historical imports require explicit authority; keep ingestion disabled until it is approved.
For setup, bank or tag configuration, ingestion switches, doctor or deepen recovery, or import, read
`references/hindsight-setup.md` for the mechanics and dated source limits. Routine recall does not load it.

## The store is a trust boundary in both directions

As a sink, stored content is readable by every later agent and, when the store is server-backed, by anything
that reaches its port. Never write secrets, credentials, tokens, cookies or private keys. As a source, recalled
text is model-authored and unverified. Treat it as a lead to verify in the repository, never as evidence. Any
memory transport beyond loopback requires authentication before it starts. The selected adapter supplies the
exposure defaults and the configuration mechanics. `/alaa-security-review` owns the fail-closed doctrine and
its exceptions.

## Beads hub reminders and issue notes

Each kind of information has one owner:

| Information | Owner |
|---|---|
| Generalizable experience usable in later work | The active adapter store |
| A short reminder shared across the whole Beads hub | `bd remember` |
| A task's position and next step | Beads issue `notes`, or the plan cursor under `Task store: local`; `/alaa-workflow` `references/task-tracking.md` section `## Issue fields` owns the field contract |
| A binding rule | The owning repository or skill; memory only references it |

A reminder is a short pointer every hub reader must see at session start. Experience with a reason and
evidence goes to the active adapter store, and a reminder may point to it.

Write `bd remember` without separate approval only when Beads is available and its binding has verified the hub
(`/alaa-workflow` `references/task-tracking.md`), and only for a short reminder shared across the hub.
Reason: `bd prime` injects every memory by default, with no label or project filter (`--no-memories` and the
caps exist), and `bd remember` takes no label or project option. When the hub is unavailable, write no
reminder, and re-evaluate it when Beads is available. On an uncertain write, follow
`/alaa-workflow` `references/task-tracking.md` section `## Outage and uncertain writes`.

- Each entry carries its source, scope and maintainer.
- Never put task status, evidence, a project-specific lesson, or a new rule in it. Send a project-specific lesson to the active adapter store through `/alaa-extract-agent-lessons` admission, with its project scope recorded.
- Leaving it empty is correct.
- Per-project memory is deferred, not designed.

## References

Before you select a conditional reference, read `references/00-topic-map.md`. It is the sole router.

## Completion checks

Write only authorized durable changes. Before you report, confirm each applicable item:

- Only the `ACTIVE_ADAPTER` adapter was used; a missing adapter file stopped the task without fallback.
- Memory was searched before note creation, or the report says why not.
- Repository truth was inspected before any implementation claim.
- No raw transcript, log, source file, whole document or secret reached the store.
- No `/alaa-workflow` execution state was duplicated.
- No service-to-service dependency edge was remembered.
- Nothing forbidden in the Beads hub reminders section was written to `bd remember`.
- Canonical disagreements became repository drift records; stale memory alone was corrected with authority
  or deferred.
- Every checker run reported its exit code, and a `2` was read as "could not run", never as a pass.
- The report names notes changed, source paths, validation result, drift recorded, memory availability, and
  unresolved questions.
