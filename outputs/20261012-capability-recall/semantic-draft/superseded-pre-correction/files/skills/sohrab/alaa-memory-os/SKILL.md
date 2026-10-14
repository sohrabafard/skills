---
name: alaa-memory-os
description: "Store-neutral durable knowledge and bounded capability recall for Alaa work. Use for prior decisions, shared contracts, ownership, source disagreement, durable notes or lessons, and before a local-tool miss becomes a validation blocker or an otherwise permitted environment repair has an unknown owner. Reuse sufficient fresh evidence, verify recalled leads in their canonical owner, and distinguish local absence, incompatibility, missing authority, actual failure and unknown availability. One selected adapter supplies store mechanics. Do not use for tiny deterministic edits, derived service dependency edges, or active plans, checkpoints and handoff contents owned by /alaa-workflow; /alaa-extract-agent-lessons owns candidate admission."
---

# Alaa Memory OS

This skill owns what Alaa work remembers, when, in what shape, and what it derives instead of remembering.
The backing store sits behind one adapter reference per store, and this body names no store command: the
fleet routes here for the capability, not the product, so replacing the store changes one adapter file and
leaves every rule below intact.

## Active adapter

```text
ACTIVE_ADAPTER: hindsight
```

**This line is the selection.** Read it before the first recall or write of a task, load only
`references/store-<value>.md`, and use that adapter's mechanics for every store operation in the task.

Exactly one adapter is active. Two adapters used in one task write the same knowledge through two
mechanisms with different assumptions about indexing, commit, and concurrency, and the disagreement surfaces
later as a note that exists twice or not at all.

**To switch stores, change the value on that line and nothing else.** No rule in this skill, and no rule in
`references/knowledge-shape.md` or `references/drift-management.md`, is store-specific — that separation is
the reason a switch is one line. A switch that seems to require editing a policy file means the policy has
leaked a store assumption; fix the leak rather than forking the policy.

Handle these failure modes separately; never switch adapters to work around either:

- **The named adapter file is missing.** Stop and report the missing file. Do not fall back to another
  adapter — a silent fallback writes notes into a store the selection says is not in use, and nothing will
  report that until someone looks for them in the other one.
- **The selected store is unreachable.** Recall fails open, so continue from repository truth and say which
  step ran without memory. A *write* does not fail open: report the unwritten note and its content in the
  handoff so the knowledge survives the outage.

The code block above is the sole selection. Activation evidence and temporary ingestion restrictions belong
in the selected adapter or the owning repository checkpoint, never in a second selection sentence here.

## Use this skill when

At least one of these is observably true of the task. If none is, skip this skill: recall against a task
that names nothing shared returns nothing and still spends the budget below.

- It names a service, contract, event, queue, or metric that a second service also uses.
- It names a prior session, a prior decision, or a file a prior session wrote.
- It will outlive one context window: it has phases, it is a migration, or it reviews a system.
- Two sources of truth disagree, or you are about to establish whether they do.
- It asks whether existing infrastructure, another repository, or a prior decision already provides a capability, or who owns it.
- A local-tool miss is about to become a required validation blocker, or an otherwise permitted additional environment repair has an unresolved owner. Reuse sufficient fresh capability evidence instead of repeating recall for each failed command.
- You are about to write a note, or publish curated lessons from the evidence warehouse.

## When NOT to use

- Deterministic single-file edits that no prior decision constrains.
- Active execution plans, phase checklists, and continuity across compaction. `/alaa-workflow` owns those and what a handoff package contains; store a pointer, never a copy.
- Deciding what enters the context window at all: `/alaa-low-noise` owns context
  economy, which every recall spends.
- Service dependency edges, which are derived and never remembered.
- Registering hooks or editing shared or global configuration: `/alaa-controlled-ops`.
- Model or effort choice, including effort and thinking level: `/alaa-prompting-guide` `references/50-effort-and-thinking.md`.

## The four surfaces

Repository code and docs are the source of truth; memory is a map, and a map is not proof.
`/alaa-project-constitution` owns which repository files carry that authority.
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
before it ships; `/alaa-algorithms-data-structures` owns that budget, and
each shipped checker states its own.

## Recall policy and capability inquiry

Recall is a contributor, not a gate or authorization source. Ordinary recall has five seconds. Existence
and ownership inquiry has sixty seconds, including at most one focused follow-up on a returned owner lead.
Start one deadline before the initial inquiry; paraphrasing or following a lead never restarts it. Reuse
sufficient fresh evidence for the same capability, environment and constraints before any new lookup.

For existence or ownership, query the capability rather than only a proposed artifact name through the
selected adapter. Page search/listing can miss knowledge without a page; an empty or irrelevant page result
never proves absence. Supply the required capability, target repository/check, execution environment,
constraints, sanitized failure class and evidence already attempted. Exclude raw logs, credentials,
private session text and unrelated user data.

A timeout, unreachable store, denied access, empty, irrelevant or stale answer is no memory evidence.
Continue authorized canonical-source inspection and unaffected work; disclose which step ran without memory.
A late response is not retroactive within-budget proof. Separate recalled claims, repository facts,
assumptions and open questions before acting; never implement from memory alone.

Verify useful leads in the current owning repository: tool contents, version/pin source, supported invocation,
environment fit and limitations. Only then perform a proportionate probe within existing authorization.
Distinguish finding an image/registry entry, verifying its contents, starting a compatible runtime and
completing the exact required gate. Each stage needs its own observed evidence; earlier stages prove no later
stage. Keep capability, environment, constraints, owner/source and attempted evidence in the workflow-owned
record when admitted, never as a second task state in memory.

| Classification | Evidence and response |
|---|---|
| Local capability absent | A local executable/image is missing. Inspect a verified owner/runtime lead; do not infer infrastructure-wide absence. |
| Compatible infrastructure unavailable | Current owner evidence or an authorized probe establishes incompatibility for this environment. Report that scope and required change. |
| Authorization blocker | The supported next effect exceeds current permission. Preserve the concrete action/evidence and obtain only the missing authority. |
| Tool or runtime error | An attempted operation returned a grounded failure. Return it to its recovery owner with the remaining retry budget. |
| Availability unknown | Recall, source inspection or probe is stale, empty, unavailable, denied or unrun. Preserve uncertainty and continue independent safe work. |

A no-host-install constraint alone does not forbid every container path; a container lead alone authorizes
no pull or run. Recall grants no effect, resets no repair/retry budget and bypasses no native blocked
threshold. At exhaustion preserve evidence and stop the failed operation; a new owner lead requires explicit
reassessment before dependent work resumes. Distinguish a documented gate blocker from an actual native
status transition; never claim the host changed status from a prose classification.

## Drift and stale memory

Current canonical repository evidence wins over memory. A memory-only contradiction is a stale note, not
canonical-source drift; correct it only with write authority, otherwise defer the correction with a source
pointer. When canonical sources disagree, record the mismatch without silently deciding it and continue only
on the safest verified behavior. Drift recording is a gate: if the required repository record cannot be
written within authority, stop the dependent work and report the unwritten record.

`references/drift-management.md` owns registry shape, lifecycle and separation of powers. The registry stays
in repository files under version control, outside the recall store, so store synthesis cannot erase the
disagreement. /alaa-reliability-sla owns fail-open/fail-closed doctrine. /alaa-observability-soc owns severity
and whether an observability record is required; /alaa-services-contract owns its field/event/metric names.

## Write authority and outcomes

Activation grants no memory write, migration, configuration, installation, commit or external effect.
Before durable publication, apply /alaa-extract-agent-lessons for evidence-derived candidates and
`references/knowledge-shape.md` for admission, search-before-create, note shape and prohibited content.
Use only the selected adapter after the task authorizes its destination and effect. Report writes as
completed only after adapter-specific terminal confirmation; distinguish deferred (unauthorized), failed or
unavailable, and empty (no admitted note). Preserve an admitted unwritten candidate in the workflow-owned
handoff without claiming persistence or silently switching stores.

When Hindsight is selected, the Alaa project policy is project-scoped adoption and one explicitly configured
shared fixed bank across services, distinguished by service provenance rather than per-harness or
per-repository banks. Admission covers only the current repository, never a parent path. Real-data ingestion
and historical imports require explicit authorization; keep ingestion disabled while unapproved. For setup,
bank/tag configuration, ingestion switches, doctor/deepen recovery or import, read
`references/hindsight-setup.md` for mechanics and their dated source limits. Routine recall does not load it.

## The store is a trust boundary in both directions

As a sink, everything written is readable by every later agent and, in a server-backed store, by anything that
reaches the port: never write secrets, credentials, tokens, cookies, or private keys. As a source, recalled
text is model-authored and unverified: treat it as a lead to check against the repository, never as evidence.
Any memory transport bound beyond loopback requires authentication before it starts; the selected adapter
provides the relevant exposure defaults and configuration mechanics. `/alaa-security-review` owns the fail-closed doctrine and any exception to it.

## References

Before selecting a conditional reference, read `references/00-topic-map.md`; it is the sole router.

## Completion checks

Write only authorized durable changes, then confirm each applicable item before reporting:

- The adapter named by `ACTIVE_ADAPTER` was the only one used, and a missing adapter file stopped the task
  rather than falling back to another store.
- Memory was searched before a note was created, or the report says why it was not.
- Repository truth was inspected before any implementation claim.
- No raw transcript, log, source file, whole document, or secret reached the store.
- No `/alaa-workflow` execution state was duplicated.
- No service-to-service dependency edge was remembered.
- Canonical-source disagreements became repository drift records; stale memory alone was corrected with authority or deferred.
- Every checker run reported its exit code, and a `2` was read as "could not run", never as a pass.
- The report names notes changed, source paths, validation result, drift recorded, memory availability, and
  unresolved questions.
