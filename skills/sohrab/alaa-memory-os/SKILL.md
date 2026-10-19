---
name: alaa-memory-os
description: "Use when Alaa work must record or recall durable cross-session knowledge, whichever memory store backs it: deciding what to remember and in what shape; architecture, ownership, contract, operations, lesson, project, handoff or research notes; whether information belongs in the memory store, a Beads hub reminder or Beads issue notes; drift between sources of truth; fail-open recall budgets; and capability recall before a local-tool miss becomes a validation blocker or a permitted environment repair has an unknown owner. One adapter is active at a time; local file vault, Basic Memory and Hindsight each get one adapter reference. Do not use for tiny deterministic edits, as a second task system, for active plans or handoff contents owned by alaa-workflow, for candidate admission owned by alaa-extract-agent-lessons, or for service dependency edges, which are always derived."
---

# Alaa Memory OS

This skill owns what Alaa work remembers, when, in what shape, and what it derives instead of remembering.
The backing store sits behind one adapter reference per store, and this body names no memory-adapter store command
(Beads surfaces are outside the adapter): the fleet routes here for the capability, not the product, so
replacing the store changes one adapter file and leaves every rule below intact.

## Active adapter

```text
ACTIVE_ADAPTER: hindsight
```

**This line is the sole selection.** Before a task's first recall/write, load
`references/store-<value>.md` and use only its mechanics for task store operations. A format-only section
explicitly routed by that adapter shares serialization, not adapter activation or operation authority.

Exactly one adapter is active. Two adapters write the same knowledge under different indexing, commit and
concurrency assumptions; disagreement later leaves notes duplicated or missing.

For a supported store switch, change the selector without rewriting neutral knowledge/drift rules here,
in `references/knowledge-shape.md` or `references/drift-management.md`. Conditional selected-store policy,
including Hindsight bank/admission policy, stays here and applies only to its store; product commands stay
in its adapter. Store assumptions in neutral knowledge/drift rules are policy leaks to repair, not reasons
to fork those rules.

Handle these failures separately; never switch adapters around either:

- **Missing named adapter file:** stop and report it. Never fall back: silent fallback writes to an
  unselected store, unnoticed until someone searches the other store.
- **Unreachable selected store:** recall fails open; continue from repository truth and name the step run
  without memory. Writes do not fail open: report the unwritten note and content in the handoff so
  knowledge survives the outage.

Activation evidence and temporary ingestion restrictions belong in the selected adapter or owning
repository checkpoint, never in a second selection sentence here.

## Use this skill when

At least one condition must be observable. Otherwise skip: recall naming nothing shared returns nothing
and still spends the budget below.

- The task names a service, contract, event, queue, or metric also used by a second service.
- It names a prior session, prior decision, or file a prior session wrote.
- It outlives one context window: phases, migration, or system review.
- Two sources of truth disagree, or you are about to establish whether they do.
- It asks whether existing infrastructure, another repository, or a prior decision already provides a capability, or who owns it.
- A local-tool miss is about to become a required validation blocker, or an otherwise permitted additional
  environment repair has an unresolved owner. Reuse sufficient fresh capability evidence instead of
  repeating recall for each failed command.
- You are about to write a note, or publish curated lessons from the evidence warehouse.
- You are about to write a Beads hub reminder (`bd remember`), or to decide whether information belongs in the memory store, a hub reminder or issue notes.

## When NOT to use

- Deterministic single-file edits unconstrained by prior decisions.
- Active execution plans, phase checklists and compaction continuity. `/alaa-workflow` owns these and handoff
  contents; store a pointer, never a copy.
- Deciding what enters context: `/alaa-low-noise` owns context economy, which every recall spends.
- Service dependency edges: derive, never remember.
- Registering hooks or editing shared/global configuration: `/alaa-controlled-ops`.
- Model or effort choice, including effort/thinking level: `/alaa-prompting-guide` `references/50-effort-and-thinking.md`.

## The four surfaces

Repository code/docs are truth; memory is a map, not proof. `/alaa-project-constitution` owns which
repository files carry authority. The store indexes that truth. Skills define agent behaviour: never copy
an installed skill into memory. Any human editing surface is navigation, not runtime truth. Never edit
upstream store packs under `vendor/`; this skill owns the opinion and routes to upstream-documented
mechanics, including whichever pack backs a successor store.

## Remember facts, derive relationships

Remembered facts go stale without failure, remaining wrong until they mislead. Remember service owners,
decision reasons, contract promises and lesson costs. Derive, never remember:

- Service call edges. SigNoz derives them from traces; route to `alaa-signoz-clickhouse-docs` `references/50-service-topology.md`.
- API consumer breakage. oasdiff compares the two OpenAPI documents.
- Symbol references. Serena and ast-grep inspect the current tree.

Replace existing service-to-service `depends_on` edges with derivation pointers rather than refreshing
them. Before shipping any pass over a history-growing store, state its complexity bound;
`/alaa-algorithms-data-structures` owns that budget, and each shipped checker states its own.

## Recall policy and capability inquiry

Recall contributes; it is no gate or authorization source. Ordinary recall has five seconds;
existence/ownership inquiry has sixty, including at most one focused follow-up on a returned owner lead.
Start one deadline before initial inquiry; paraphrasing or following leads never resets it. Before any
new lookup, reuse sufficient fresh evidence for the same capability, environment and constraints.

For existence/ownership, query the capability through the selected adapter, not only a proposed artifact
name. Page search/listing misses knowledge without pages; empty/irrelevant page results never prove
absence. Supply required capability, target repository/check, execution environment, constraints,
sanitized failure class and attempted evidence. Exclude raw logs, credentials, private session text and
unrelated user data.

Timeouts, unreachable stores, denied access and empty, irrelevant or stale answers are no memory evidence.
Continue authorized canonical-source inspection and unaffected work; disclose the step run without memory.
Late responses are not retroactive within-budget proof. Before acting, separate recalled claims,
repository facts, assumptions and open questions; never implement from memory alone.

Verify useful leads in the current owning repository: tool contents, version/pin source, supported
invocation, environment fit and limitations. Only then probe proportionately within existing authority.
Distinguish image/registry discovery, contents verification, compatible runtime start and exact required
gate completion. Each needs observed evidence; earlier stages prove no later stage. When admitted, keep
capability, environment, constraints, owner/source and attempted evidence in the workflow-owned record,
never a second memory task state.

| Classification | Evidence and response |
|---|---|
| Local capability absent | A local executable/image is missing. Inspect a verified owner/runtime lead; never infer infrastructure-wide absence. |
| Compatible infrastructure unavailable | Current owner evidence or an authorized probe establishes environment incompatibility. Report that scope and required change. |
| Authorization blocker | The supported next effect exceeds permission. Preserve the concrete action/evidence; obtain only missing authority. |
| Tool or runtime error | An attempted operation returned a grounded failure. Return it to its recovery owner with remaining retries. |
| Availability unknown | Recall, source inspection or probe is stale, empty, unavailable, denied or unrun. Preserve uncertainty; continue independent safe work. |

A no-host-install constraint alone does not forbid every container path; a container lead alone authorizes
no pull or run. Recall grants no effect, resets no repair/retry budget and bypasses no native blocked
threshold. At exhaustion, preserve evidence and stop the failed operation; a new owner lead requires
explicit reassessment before dependent work resumes. Distinguish documented gate blockers from actual
native status transitions; never infer host status changes from prose classifications.

## Drift and stale memory

Current canonical repository evidence wins over memory. Memory-only contradictions are stale notes, not
canonical-source drift; correct only with write authority, otherwise defer correction with a source
pointer. When canonical sources disagree, record the mismatch without silently deciding it; continue
only on the safest verified behavior. Drift recording is a gate: if the required repository record cannot
be written within authority, stop dependent work and report the unwritten record.

`references/drift-management.md` owns registry shape, lifecycle and separation of powers. Keep the registry
in version-controlled repository files outside recall so store synthesis cannot erase disagreement.
/alaa-reliability-sla owns fail-open/fail-closed doctrine; /alaa-observability-soc owns severity and
observability-record requirements; /alaa-services-contract owns field/event/metric names.

## Write authority and outcomes

Activation grants no memory write, migration, configuration, installation, commit or external effect.
Before durable publication, apply /alaa-extract-agent-lessons for evidence-derived candidates and
`references/knowledge-shape.md` for search-before-create, note shape and prohibited content.
Use only the selected adapter after task authorization of destination and effect. Report completed
writes only after adapter-specific terminal confirmation; distinguish deferred (unauthorized), failed,
unavailable and empty (no admitted note). Preserve admitted unwritten candidates in the workflow-owned
handoff without claiming persistence or silently switching stores.

When Hindsight is selected, Alaa policy requires project-scoped adoption and one explicitly configured
shared fixed bank across services, distinguished by service provenance, not per-harness/repository banks.
Admission covers only the current repository, never a parent path. Real-data ingestion and historical
imports require explicit authority; keep ingestion disabled while unapproved. For setup, bank/tag
configuration, ingestion switches, doctor/deepen recovery or import, read `references/hindsight-setup.md`
for mechanics and dated source limits. Routine recall does not load it.

## The store is a trust boundary in both directions

As a sink, stored content is readable by every later agent and, server-backed, anything reaching its port:
never write secrets, credentials, tokens, cookies or private keys. As a source, recalled text is
model-authored and unverified: treat it as a repository-verifiable lead, never evidence. Any memory
transport beyond loopback requires authentication before starting; the selected adapter supplies exposure
defaults/configuration mechanics. `/alaa-security-review` owns fail-closed doctrine and exceptions.

## Beads hub reminders and issue notes

Each kind of information has one owner:

| Information | Owner |
|---|---|
| Generalizable experience usable in later work | The active adapter store |
| A short reminder shared across the whole Beads hub | `bd remember` |
| A task's position and next step | Beads issue `notes`; `/alaa-workflow` `references/task-tracking.md` section `## Issue fields` owns the field contract |
| A binding rule | The owning repository or skill; memory only references it |

A reminder is a short pointer every hub reader must see at session start. Experience with a reason and
evidence goes to the active adapter store, and a reminder may point to it.

Write `bd remember` without separate approval only when the repository selects Beads and its binding has
verified the hub (`/alaa-workflow` `references/task-tracking.md`), and only for a short reminder shared across
the hub. On an unavailable hub or an uncertain write, follow `/alaa-workflow` `references/task-tracking.md`
section `## Outage and uncertain writes`. Reason: `bd prime` injects every memory by default (`--no-memories`
and the caps exist), with no label or project filter, and `bd remember` takes no label or project option.

- Each entry carries its source, scope and maintainer.
- Never put task status, evidence, a project-specific lesson, or a new rule in it. A project-specific lesson goes to the active adapter store through `/alaa-extract-agent-lessons` admission, with its project scope recorded.
- Leaving it empty is correct.
- Per-project memory is deferred, not designed.

## References

Before selecting a conditional reference, read `references/00-topic-map.md`; it is the sole router.

## Completion checks

Write only authorized durable changes; before reporting, confirm each applicable item:

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
